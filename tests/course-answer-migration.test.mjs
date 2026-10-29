import assert from 'node:assert/strict';
import test from 'node:test';
import { readFileSync } from 'node:fs';
import { CURRENT_ANSWER_BANK_VERSION, migrateSavedCourseAnswers } from '../src/course-answer-migration.ts';

const idFor = (n) => `course-${String(n).padStart(2, '0')}`;
const rotated = (n, oldLetter) => String.fromCharCode(65 + ((oldLetter.charCodeAt(0) - 65 + (n - 1) % 4) % 4));

test('all 69 legacy course answers preserve correct and wrong outcomes after rotation', () => {
  const answers = Object.fromEntries(Array.from({ length: 69 }, (_, i) => [idFor(i + 1), ['A', 'B', 'C', 'D']]));
  const prior = { answers, questionIds: Object.keys(answers), startedAt: 123 };
  const migrated = migrateSavedCourseAnswers(prior);
  assert.equal(migrated.answerBankVersion, CURRENT_ANSWER_BANK_VERSION);
  assert.equal(migrated.startedAt, 123);
  for (let n = 1; n <= 69; n += 1) {
    const id = idFor(n);
    assert.deepEqual(migrated.originalCourseAnswers[id], ['A', 'B', 'C', 'D']);
    assert.deepEqual(migrated.answers[id], ['A', 'B', 'C', 'D'].map((letter) => rotated(n, letter)));
    assert.equal(migrated.answers[id][0], rotated(n, 'A'), `${id}: legacy correct A changed meaning`);
    for (const wrong of migrated.answers[id].slice(1)) assert.notEqual(wrong, migrated.answers[id][0], `${id}: legacy distractor became correct`);
  }
  assert.deepEqual(prior.answers[idFor(2)], ['A', 'B', 'C', 'D'], 'migration mutated the original stored object');
  assert.strictEqual(migrateSavedCourseAnswers(migrated), migrated, 'a second migration must be idempotent');
});

test('migration preserves unrelated question answers, misses, empty selections, and already-versioned attempts', () => {
  const prior = { answerBankVersion: 1, answers: { 'w8-01': ['D'], 'course-01': [], 'course-02': ['B'], 'course-69': ['D'] } };
  const migrated = migrateSavedCourseAnswers(prior);
  assert.deepEqual(migrated.answers['w8-01'], ['D']);
  assert.deepEqual(migrated.answers['course-01'], []);
  assert.equal(migrated.originalCourseAnswers['course-01'], undefined);
  assert.deepEqual(migrated.originalCourseAnswers['course-02'], ['B']);
  assert.deepEqual(migrated.answers['course-02'], [rotated(2, 'B')]);
  assert.deepEqual(migrated.answers['course-69'], [rotated(69, 'D')]);
  const futureVersion = { ...prior, answerBankVersion: 99 };
  assert.strictEqual(migrateSavedCourseAnswers(futureVersion), futureVersion, 'do not rewrite answers from newer banks');
});

test('new history items retain the bank version and provenance so an old attempt is never migrated twice', () => {
  const source = readFileSync(new URL('../app/page.tsx', import.meta.url), 'utf8');
  const buildHistory = source.match(/function buildHistoryItem\([\s\S]*?\n  }\n/);
  assert.ok(buildHistory, 'missing history creation');
  assert.match(buildHistory[0], /answerBankVersion:\s*attempt\.answerBankVersion/);
  assert.match(buildHistory[0], /originalCourseAnswers:\s*attempt\.originalCourseAnswers/);
  const old = migrateSavedCourseAnswers({ answers: { 'course-02': ['A'] } });
  const finished = { ...old, finishedAt: 100 };
  assert.strictEqual(migrateSavedCourseAnswers(finished), finished);
  assert.deepEqual(finished.originalCourseAnswers['course-02'], ['A']);
  assert.deepEqual(finished.answers['course-02'], ['B']);
});

test('rewritten AI scenarios keep legacy right/wrong outcomes after their answer left slot A', () => {
  const bank = JSON.parse(readFileSync(new URL('../public/question-bank.json', import.meta.url), 'utf8'));
  const rewritten = bank.filter((q) => ['original', 'emerging'].includes(q.sourceCategory));
  assert.equal(rewritten.length, 20);
  const fromV2 = migrateSavedCourseAnswers({ answerBankVersion: 2, answers: Object.fromEntries(rewritten.map((q) => [q.id, ['A']])) });
  const wrongFromV2 = migrateSavedCourseAnswers({ answerBankVersion: 2, answers: Object.fromEntries(rewritten.map((q) => [q.id, ['B']])) });
  for (const q of rewritten) {
    assert.deepEqual(fromV2.answers[q.id], q.correctIds, `${q.id}: legacy correct A must map to the new key`);
    assert.notDeepEqual(wrongFromV2.answers[q.id], q.correctIds, `${q.id}: legacy distractor became correct`);
    assert.deepEqual(fromV2.originalCourseAnswers[q.id], ['A']);
  }
  const courseAlreadyMigrated = migrateSavedCourseAnswers({ answerBankVersion: 2, answers: { 'course-02': ['B'] } });
  assert.deepEqual(courseAlreadyMigrated.answers['course-02'], ['B'], 'version 2 course answers must not rotate twice');
});

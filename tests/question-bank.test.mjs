import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const bank = JSON.parse(fs.readFileSync(path.join(root, "public", "question-bank.json"), "utf8"));

test("question bank has the agreed 225-item source mix", () => {
  const counts = bank.reduce((current, question) => ({ ...current, [question.sourceCategory]: (current[question.sourceCategory] ?? 0) + 1 }), {});
  assert.equal(bank.length, 225);
  assert.equal(counts.captured, 75);
  assert.equal(counts.csv, 61);
  assert.equal(counts["course-derived"], 69);
  assert.equal(counts.original, 15);
  assert.equal(counts.emerging, 5);
});

test("every question has valid answers and a study explanation", () => {
  const ids = new Set();
  for (const question of bank) {
    assert.ok(question.id && !ids.has(question.id), `duplicate or missing id: ${question.id}`);
    ids.add(question.id);
    assert.ok(question.prompt.length > 10, `${question.id} has no usable prompt`);
    assert.ok(question.options.length >= 2, `${question.id} has too few options`);
    assert.ok(question.rationale.length > 10, `${question.id} has no rationale`);
    assert.equal(question.correctIds.length, question.selectCount, `${question.id} has an invalid select count`);
    for (const correctId of question.correctIds) assert.ok(question.options.some((option) => option.id === correctId), `${question.id} points to a missing correct option`);
  }
});

test("professional full-mock pool can satisfy all 75 domain quotas", () => {
  const quotas = { "1": 19, "2": 22, "3": 19, "4": 15 };
  const eligible = bank.filter((question) => question.coreEligible && !question.emerging);
  assert.ok(eligible.length >= 75);
  for (const [domain, quota] of Object.entries(quotas)) {
    assert.ok(eligible.filter((question) => question.domain === domain).length >= quota, `domain ${domain} cannot satisfy its quota`);
  }
});

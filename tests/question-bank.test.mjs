import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { optionExplanations } from "../content/option-explanations.mjs";
import { acceptedOptionIds, isCorrectAnswer } from "../src/answer-grading.ts";

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

test("every answer option has distinct teaching feedback, with no missing authored distractors", () => {
  for (const question of bank) {
    const explanations = question.options.map((option) => option.explanation);
    assert.ok(explanations.every((value) => typeof value === "string" && value.length >= 50), `${question.id} has missing/short feedback`);
    assert.equal(new Set(explanations).size, question.options.length, `${question.id} repeats the same feedback across choices`);
    for (const option of question.options) {
      const authored = optionExplanations[question.id]?.[option.id];
      if (authored) assert.equal(option.explanation, authored, `${question.id}/${option.id}: regenerate the question bank`);
    }
  }
  for (const [id, options] of Object.entries(optionExplanations)) {
    const question = bank.find((item) => item.id === id);
    assert.ok(question, `feedback refers to unknown question ${id}`);
    for (const optionId of Object.keys(options)) assert.ok(question.options.some((option) => option.id === optionId), `feedback refers to unknown option ${id}/${optionId}`);
  }
});

test("multi-response grading requires exactly the full correct combination", () => {
  const question = bank.find((item) => item.id === "w8-9");
  assert.ok(isCorrectAnswer(question, ["D", "B", "A"]));
  assert.equal(isCorrectAnswer(question, ["A", "B"]), false);
  assert.equal(isCorrectAnswer(question, ["A", "B", "D", "F"]), false);
  assert.equal(isCorrectAnswer(question, ["A", "A", "B"]), false);
  assert.equal(isCorrectAnswer(question, []), false);
});

test("corrected and ambiguous historical keys retain provenance and grade valid alternatives", () => {
  const transit = bank.find((item) => item.id === "csv-20");
  assert.deepEqual(transit.recordedCorrectIds, ["A"]);
  assert.ok(isCorrectAnswer(transit, ["D"]));
  assert.equal(isCorrectAnswer(transit, ["A"]), false);
  for (const [id, recorded, alternative] of [["w8-31", "C", "B"], ["w8-60", "D", "A"]]) {
    const question = bank.find((item) => item.id === id);
    assert.deepEqual(question.correctIds, [recorded]);
    assert.ok(isCorrectAnswer(question, [recorded]));
    assert.ok(isCorrectAnswer(question, [alternative]));
    assert.equal(isCorrectAnswer(question, [recorded, alternative]), false);
    assert.deepEqual(acceptedOptionIds(question), [recorded, alternative]);
    assert.ok(question.studyNote);
    assert.ok(question.studyReferences.every((url) => url.startsWith("https://docs.aws.amazon.com/")));
  }
});

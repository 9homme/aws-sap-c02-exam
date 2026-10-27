import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { filterStudyQuestions, selectStudyQuestions } from "../src/question-selection.ts";

const bank = JSON.parse(readFileSync(new URL("../public/question-bank.json", import.meta.url), "utf8"));
const defaults = { domain: "all", source: "all", includeEmerging: false };

test("50- and 75-question study sets have the exact requested number of unique questions", () => {
  const pool = filterStudyQuestions(bank, defaults);
  const originalOrder = pool.map((question) => question.id);
  for (const size of [50, 75]) {
    const selected = selectStudyQuestions(pool, size);
    assert.equal(selected.length, size);
    assert.equal(new Set(selected).size, size);
    assert.ok(selected.every((id) => pool.some((question) => question.id === id)));
  }
  assert.deepEqual(pool.map((question) => question.id), originalOrder);
});

test("the 15 original scenarios never silently become a requested 50- or 75-question set", () => {
  const pool = filterStudyQuestions(bank, { ...defaults, source: "original" });
  assert.equal(pool.length, 15);
  assert.throws(() => selectStudyQuestions(pool, 50), RangeError);
  assert.throws(() => selectStudyQuestions(pool, 75), RangeError);
  assert.equal(selectStudyQuestions(pool, 15).length, 15);
});

test("all 75 captured Week 8 questions can be practiced as one study set", () => {
  const pool = filterStudyQuestions(bank, { ...defaults, source: "captured" });
  assert.equal(pool.length, 75);
  assert.equal(new Set(selectStudyQuestions(pool, 75)).size, 75);
});

test("combined filters, empty pools, and optional emerging questions are respected", () => {
  const filtered = filterStudyQuestions(bank, { ...defaults, domain: "1", source: "original" });
  assert.ok(filtered.length > 0);
  assert.ok(filtered.every((question) => question.domain === "1" && question.sourceCategory === "original"));
  assert.throws(() => selectStudyQuestions(filtered, 50), RangeError);
  const empty = filterStudyQuestions(bank, { ...defaults, source: "emerging" });
  assert.equal(empty.length, 0);
  assert.throws(() => selectStudyQuestions(empty, 10), RangeError);
  const emerging = filterStudyQuestions(bank, { ...defaults, source: "emerging", includeEmerging: true });
  assert.equal(emerging.length, 5);
  assert.equal(selectStudyQuestions(emerging, 5).length, 5);
});

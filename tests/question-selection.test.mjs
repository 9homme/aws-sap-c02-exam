import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { filterStudyQuestions, selectStudyQuestions, STUDY_SIZES } from "../src/question-selection.ts";
import { SOURCE_GROUPS, sourceGroupFor } from "../src/source-groups.ts";

const bank = JSON.parse(readFileSync(new URL("../public/question-bank.json", import.meta.url), "utf8"));
const defaults = { domain: "all", source: "all", includeEmerging: false };

test("all offered study set lengths return the exact number of unique questions", () => {
  const pool = filterStudyQuestions(bank, defaults);
  const originalOrder = pool.map((question) => question.id);
  assert.deepEqual(STUDY_SIZES, [10, 25, 50, 75, 100, 150, 200]);
  for (const size of STUDY_SIZES) {
    const selected = selectStudyQuestions(pool, size);
    assert.equal(selected.length, size);
    assert.equal(new Set(selected).size, size);
    assert.ok(selected.every((id) => pool.some((question) => question.id === id)));
  }
  assert.deepEqual(pool.map((question) => question.id), originalOrder);
});

test("All starts the exact filtered pool, including optional emerging questions", () => {
  for (const filters of [defaults, { ...defaults, includeEmerging: true }, { ...defaults, source: "original" }]) {
    const pool = filterStudyQuestions(bank, filters);
    const selected = selectStudyQuestions(pool, pool.length);
    assert.equal(selected.length, pool.length);
    assert.deepEqual(new Set(selected), new Set(pool.map((question) => question.id)));
  }
});

test("the 15 original scenarios never silently become a requested larger study set", () => {
  const pool = filterStudyQuestions(bank, { ...defaults, source: "original" });
  assert.equal(pool.length, 15);
  for (const size of [25, 50, 75, 100, 150, 200]) {
    assert.throws(() => selectStudyQuestions(pool, size), RangeError);
  }
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

test("three source groups cover the entire bank exactly once without changing source provenance", () => {
  assert.deepEqual(SOURCE_GROUPS.map((group) => [group.id, group.sources.length]), [["recorded", 2], ["course", 1], ["generated", 3]]);
  const ids = new Set();
  for (const group of SOURCE_GROUPS) {
    for (const category of group.sources) {
      assert.ok(!ids.has(category), `duplicate source: ${category}`);
      ids.add(category);
      assert.equal(sourceGroupFor(category), group.id);
    }
  }
  assert.equal(sourceGroupFor("unknown"), null);
  assert.deepEqual(new Set(bank.map((question) => question.sourceCategory)), ids);
  assert.equal(filterStudyQuestions(bank, { ...defaults, group: "recorded" }).length, 136);
  assert.equal(filterStudyQuestions(bank, { ...defaults, group: "course" }).length, 69);
  assert.equal(filterStudyQuestions(bank, { ...defaults, group: "generated" }).length, 122);
  assert.equal(filterStudyQuestions(bank, { ...defaults, group: "generated", includeEmerging: true }).length, 127);
  assert.equal(filterStudyQuestions(bank, { ...defaults }).length, 327);
  assert.equal(filterStudyQuestions(bank, { ...defaults, includeEmerging: true }).length, 332);
  assert.equal(filterStudyQuestions(bank, { ...defaults, group: "generated", source: "professional" }).length, 107);
});

test("source subfilters combine with group, domain and emerging opt-in", () => {
  const recordedCSV = filterStudyQuestions(bank, { ...defaults, group: "recorded", source: "csv" });
  assert.equal(recordedCSV.length, 61);
  const mismatched = filterStudyQuestions(bank, { ...defaults, group: "recorded", source: "original" });
  assert.equal(mismatched.length, 0);
  const domainSlice = filterStudyQuestions(bank, { ...defaults, group: "generated", source: "original", domain: "2" });
  assert.ok(domainSlice.length > 0);
  assert.ok(domainSlice.every((question) => question.domain === "2" && question.sourceCategory === "original"));
  const optionalDisabled = filterStudyQuestions(bank, { ...defaults, group: "generated", source: "emerging" });
  assert.equal(optionalDisabled.length, 0);
  const optionalEnabled = filterStudyQuestions(bank, { ...defaults, group: "generated", source: "emerging", includeEmerging: true });
  assert.equal(optionalEnabled.length, 5);
});

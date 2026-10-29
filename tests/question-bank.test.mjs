import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { acceptedOptionIds, isCorrectAnswer } from "../src/answer-grading.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const bank = JSON.parse(fs.readFileSync(path.join(root, "public", "question-bank.json"), "utf8"));

test("question bank keeps AWS Skill Builder provenance and scores the expanded AI pool", () => {
  const counts = bank.reduce((current, question) => ({ ...current, [question.sourceCategory]: (current[question.sourceCategory] ?? 0) + 1 }), {});
  assert.equal(bank.length, 332);
  assert.equal(counts.captured, 75);
  assert.equal(counts.csv, 61);
  assert.equal(counts["course-derived"], 69);
  assert.equal(counts.original, 15);
  assert.equal(counts.professional, 107);
  assert.equal(counts.emerging, 5);
  assert.ok(bank.filter((q) => ["captured", "csv"].includes(q.sourceCategory)).every((q) => q.sourceLabel.includes("AWS Skill Builder")));
});

test("every scored AI Professional case has realistic multi-constraint teaching feedback and balanced answer slots", () => {
  const professional = bank.filter((q) => q.sourceCategory === "professional");
  const positions = { A: 0, B: 0, C: 0, D: 0 };
  for (const item of professional) {
    assert.ok(item.prompt.length >= 850, `${item.id}: scenario too short`);
    assert.ok(item.requirements.length >= 2 && item.requirements.length <= 3, `${item.id}: requires 2–3 constraints`);
    assert.ok(item.products.length >= 2, `${item.id}: incomplete service comparisons`);
    assert.ok(item.options.length >= 4, `${item.id}: fewer than four options`);
    assert.ok(item.review.options && Object.keys(item.review.options).length === item.options.length);
    assert.ok(item.options.every((option) => option.explanation.length >= 50 && /[ก-๙]/.test(option.explanation)));
    assert.ok(item.review.references.every(({ url }) => /^https:\/\/(docs\.aws\.amazon\.com|aws\.amazon\.com)\//.test(url)));
    for (const id of item.correctIds) if (id in positions) positions[id] += 1;
  }
  assert.ok(Math.max(...Object.values(positions)) - Math.min(...Object.values(positions)) <= 2, `answer letter bias: ${JSON.stringify(positions)}`);
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
    assert.ok(explanations.every((value) => typeof value === "string" && value.length >= 90), `${question.id} has missing/short feedback`);
    assert.equal(new Set(explanations).size, question.options.length, `${question.id} repeats the same feedback across choices`);
    for (const option of question.options) {
      assert.equal(option.explanation, question.review.options[option.id], `${question.id}/${option.id}: API explanation differs from UI`);
      assert.ok(/[ก-๙]/.test(option.explanation), `${question.id}/${option.id}: explanation is missing Thai teaching context`);
    }
  }

});

test("every course-derived recap retains balanced answers, Thai explanations, and source provenance", () => {
  const counts = { A: 0, B: 0, C: 0, D: 0 };
  const repairs = new Set([3, 6, 8, 9, 10, 31, 37, 45, 50, 51, 52, 59, 68]);
  for (let number = 1; number <= 69; number += 1) {
    const id = `course-${String(number).padStart(2, "0")}`;
    const question = bank.find((entry) => entry.id === id);
    assert.ok(question, `Missing recap ${id}`);
    assert.equal(question.options.length, 4);
    const correct = question.correctIds[0];
    assert.equal(question.correctIds.length, 1);
    assert.ok(correct in counts);
    counts[correct] += 1;
    for (let slot = 0; slot < 4; slot += 1) {
      const option = question.options[slot];
      assert.equal(option.id, String.fromCharCode(65 + slot));
      if (option.id === correct) {
        assert.equal(option.explanation, question.review.reasoning, `${id}/${option.id}: correct choice explanation changed`);
      }
      assert.ok((option.explanation.match(/[ก-๙]/g) ?? []).length >= 30, `${id}/${option.id}: missing Thai feedback`);
      assert.equal(option.explanation, question.review.options[option.id], `${id}/${option.id}: displayed feedback drifted`);
    }
    assert.equal(Boolean(question.repairedRecap), repairs.has(number), `${id}: repaired recap marker inconsistent`);
    if (repairs.has(number)) assert.ok(typeof question.recordedCourseAnswer === 'string' && question.recordedCourseAnswer.length > 0, `${id}: missing original source answer`);
  }
  assert.ok(Math.max(...Object.values(counts)) - Math.min(...Object.values(counts)) <= 1, `course answer bias ${JSON.stringify(counts)}`);
});

test('course recaps give actionable questions and distinguish estimates from AWS service requirements', () => {
  const get = (n) => bank.find((entry) => entry.id === `course-${String(n).padStart(2, '0')}`);
  assert.match(get(3).options.find((choice) => choice.id === get(3).correctIds[0]).text, /source Region.*copy action/i);
  for (const n of [8, 9, 10, 31]) {
    assert.ok(get(n).prompt.length >= 140, `${get(n).id}: underspecified question`);
    assert.doesNotMatch(get(n).prompt, /select the three next steps|Framework content\s*:|Review phases\s*:/);
  }
  for (const n of [51, 52]) {
    assert.match(get(n).prompt, /course example/);
    assert.match(get(n).options.find((choice) => choice.id === get(n).correctIds[0]).text, /actual.*depends|actual.*varies/i);
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

test("every question has a complete Thai teaching review linked to official documentation", () => {
  for (const question of bank) {
    const review = question.review;
    assert.ok(review, `${question.id}: missing review`);
    assert.equal(review.reviewedAt, "2026-10-29");
    assert.match(review.decisiveClue, /[ก-๙]/, `${question.id}: missing Thai clue`);
    assert.ok(review.reasoning.length >= 60, `${question.id}: reasoning is too short to teach the decision`);
    assert.match(review.reasoning, /[ก-๙]/);
    assert.deepEqual(Object.keys(review.options).sort(), question.options.map((option) => option.id).sort(), `${question.id}: option mapping changed`);
    for (const [id, explanation] of Object.entries(review.options)) {
      assert.match(explanation, /[ก-๙]/, `${question.id}/${id}: missing Thai explanation`);
      assert.ok(explanation.length >= 50, `${question.id}/${id}: missing reasoning`);
    }
    assert.equal(new Set(Object.values(review.options)).size, question.options.length, `${question.id}: identical feedback for different options`);
    assert.ok(review.references.length > 0, `${question.id}: missing supporting source`);
    for (const source of review.references) {
      assert.ok(source.title.length > 3);
      const url = new URL(source.url);
      assert.equal(url.protocol, "https:");
      assert.ok(["docs.aws.amazon.com", "aws.amazon.com", "aws.github.io"].includes(url.hostname), `${question.id}: nonofficial source ${source.url}`);
      assert.ok(!url.pathname.includes("aws-certification"), `${question.id}: exam guide is not evidence for a service capability`);
    }
    if (review.reviewStatus) {
      assert.ok(["ambiguous", "historical"].includes(review.reviewStatus));
      assert.ok(review.caveat?.length > 40, `${question.id}: caveat must explain the issue`);
    }
  }
});

test("all 94 Bible products retain at least two tagged Professional cases", () => {
  const bible = fs.readFileSync(path.join(root, "content/aws-sap-c02-thai-exam-bible.md"), "utf8");
  const primer = bible.split("### Accounts, identity และ governance")[1].split("## 4. Domain")[0];
  const products = primer.split("\n")
    .filter((line) => line.startsWith("| ") && !/^\| (Product|[-: ])/.test(line))
    .map((line) => line.split("|")[1].trim());
  const key = (name) => name.replace(/\s+\(.*$/, "").replace(/^(AWS|Amazon)\s+/i, "").toLowerCase().replace(/[^a-z0-9]+/g, "");
  assert.equal(products.length, 94);
  for (const product of products) {
    const cases = bank.filter((q) => q.sourceCategory === "professional" && q.products.some((tag) => key(tag) === key(product)));
    assert.ok(cases.length >= 2, `${product}: insufficient scored coverage`);
  }
});

test("qualifier-driven Professional cases are longer than the Week 8 mock and state 2-3 requirements", () => {
  const added = bank.filter((q) => q.sourceCategory === "professional" && Number(q.id.split("-")[1]) >= 64);
  assert.equal(added.length, 44);
  const qualifiers = /MOST cost-effectively|LEAST amount of time|BEST performance|MOST secure|MINIMIZE/;
  for (const q of added) {
    assert.ok(q.prompt.length >= 1100 && q.prompt.length <= 1600, `${q.id}: prompt length ${q.prompt.length}`);
    assert.ok(q.requirements.length >= 2 && q.requirements.length <= 3, `${q.id}: needs 2-3 requirements`);
    assert.match(q.prompt, qualifiers, `${q.id}: missing deciding qualifier`);
    assert.ok(q.options.every((o) => o.text.length >= 250 && o.text.length <= 450), `${q.id}: option length outside 250-450`);
  }
});

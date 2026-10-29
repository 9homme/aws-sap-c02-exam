import assert from "node:assert/strict";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { fileURLToPath, pathToFileURL } from "node:url";
import test from "node:test";
import ts from "typescript";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";

// Render the actual component, including its grading helper, without browser storage.
const component = new URL("../app/AnswerExplanations.tsx", import.meta.url);
const temporary = await mkdtemp(fileURLToPath(new URL(".render-", import.meta.url)));
let AnswerExplanations;
try {
  const source = await readFile(component, "utf8");
  const compiled = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext, jsx: ts.JsxEmit.ReactJSX, target: ts.ScriptTarget.ES2022 } }).outputText
    .replace('"../src/answer-grading"', JSON.stringify(new URL("../src/answer-grading.ts", import.meta.url).href));
  await writeFile(`${temporary}/component.mjs`, compiled);
  ({ default: AnswerExplanations } = await import(pathToFileURL(`${temporary}/component.mjs`).href));
} finally {
  await rm(temporary, { recursive: true, force: true });
}
const bank = JSON.parse(await readFile(new URL("../public/question-bank.json", import.meta.url), "utf8"));
const render = (id, selected, originalCourseSelection) => renderToStaticMarkup(React.createElement(AnswerExplanations, { question: bank.find((q) => q.id === id), selected, originalCourseSelection }));

test("correct and incorrect submissions both show every option explanation immediately", () => {
  for (const selected of [["B"], ["A"]]) {
    const html = render("w8-3", selected);
    assert.match(html, /โจทย์ให้ตัดสินจากอะไร/);
    assert.match(html, /วิธีคิดทีละขั้น/);
    assert.match(html, /คุณเลือกข้อนี้/);
    assert.equal((html.match(/<details[^>]*class="option-explanation[^>]*open=""/g) ?? []).length, 4);
    for (const explanation of Object.values(bank.find((q) => q.id === "w8-3").review.options)) {
      assert.ok(html.includes(explanation.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#x27;")));
    }
    assert.match(html, /เอกสารประกอบคำอธิบาย/);
  }
});

test("incomplete multiple-response answers distinguish correct selections from a correct combination", () => {
  const partial = render("w8-9", ["A", "B"]);
  assert.match(partial, /ยังเลือกไม่ครบชุด/);
  assert.match(partial, /A \+ B \+ D/);
  assert.doesNotMatch(render("w8-9", ["A", "B", "D"]), /ยังเลือกไม่ครบชุด/);
});

test("accepted alternatives are not presented as a missed mandatory answer", () => {
  const html = render("w8-31", ["B"]);
  assert.match(html, /ยอมรับเป็นอีกคำตอบหนึ่ง/);
  assert.doesNotMatch(html, /คำตอบที่ถูก · คุณไม่ได้เลือก/);
});

test("uncertain keys disclose the limitation without calling an alternative impossible", () => {
  const html = render("w8-26", ["A"]);
  assert.match(html, /โจทย์หรือเฉลยมีความกำกวม/);
  assert.match(html, /ไม่อยู่ในเฉลยที่บันทึกไว้ · คุณเลือกข้อนี้/);
  assert.doesNotMatch(html, /ไม่ตรงเงื่อนไข · คุณเลือกข้อนี้/);
});

test("course-derived options disclose their app-authored provenance", () => {
  assert.match(render("course-01", ["A"]), /ไม่ใช่ตัวเลือกต้นฉบับของ AWS/);
  assert.match(render("course-04", ["D"]), /ตัวเลือกลวง/);
  assert.match(render("course-45", ["A"]), /ต้นฉบับบันทึกคอร์สก่อนแก้ความคลาดเคลื่อน/);
});

test("legacy course history review explains why the option letter and text changed", () => {
  const html = render('course-02', ['B'], ['A']);
  assert.match(html, /เดิมคุณเลือก A/);
  assert.match(html, /แปลงตำแหน่งเป็น B/);
  assert.match(html, /ไม่ใช่ข้อความตัวเลือกที่คุณเห็นตอนตอบครั้งแรก/);
});

import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

test("ships the Architect Lab product shell instead of the starter preview", async () => {
  const [page, bibleReader, bible, html, css] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../app/BibleReader.tsx", import.meta.url), "utf8"),
    readFile(new URL("../content/aws-sap-c02-thai-exam-bible.md", import.meta.url), "utf8"),
    readFile(new URL("../index.html", import.meta.url), "utf8"),
    readFile(new URL("../app/globals.css", import.meta.url), "utf8"),
  ]);

  assert.match(page, /Architect Lab/);
  assert.match(page, /Start full mock/);
  assert.match(page, /Saved on this device/);
  assert.match(page, /คัมภีร์/);
  assert.doesNotMatch(page, /SkeletonPreview|codex-preview/);
  assert.match(html, /Architect Lab — SAP-C02 Practice/);
  assert.match(html, /og\.png/);
  assert.match(css, /--canvas/);
  assert.match(css, /question-card/);
  assert.match(css, /bible-sidebar/);
  assert.match(css, /bible-article p \{[^}]*font-size: 17\.5px/s);
  assert.match(css, /bible-article li \{[^}]*font-size: 16\.5px/s);
  assert.match(css, /question-grid \{ display: flex/);
  assert.match(css, /drawer-backdrop/);
  assert.match(css, /@media \(max-width: 430px\)/);
  assert.match(bibleReader, /ค้นหาในคัมภีร์/);
  assert.match(bibleReader, /topic-toggle/);
  assert.match(bibleReader, /lang="th"/);
  assert.equal((bible.match(/^##\s/gm) ?? []).length, 28);
  assert.match(bible, /AWS Product Primer/);
  assert.match(bible, /มันคืออะไรแบบง่าย/);
  assert.match(bible, /Domain 1 — Design Solutions for Organizational Complexity/);
  assert.match(bible, /แผนเตรียมสอบ 21 วัน/);
  assert.match(bible, /เห็นคำนี้ ให้คิดถึงสิ่งนี้/);
  await access(new URL("../public/og.png", import.meta.url));
});

import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

test("ships the Architect Lab product shell instead of the starter preview", async () => {
  const [page, html, css] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../index.html", import.meta.url), "utf8"),
    readFile(new URL("../app/globals.css", import.meta.url), "utf8"),
  ]);

  assert.match(page, /Architect Lab/);
  assert.match(page, /Start full mock/);
  assert.match(page, /Saved on this device/);
  assert.doesNotMatch(page, /SkeletonPreview|codex-preview/);
  assert.match(html, /Architect Lab — SAP-C02 Practice/);
  assert.match(html, /og\.png/);
  assert.match(css, /--canvas/);
  assert.match(css, /question-card/);
  await access(new URL("../public/og.png", import.meta.url));
});

# Architect Lab — SAP-C02 Practice

A browser-based AWS Solutions Architect Professional quiz app with 332 questions, Thai answer explanations, study mode, a 75-question timed mock, saved attempts, and a searchable Thai study Bible.

## Run locally

```bash
npm install
npm run dev
```

Open `/exam` for quizzes or `/bible` for the study Bible. Progress is saved in this browser's local storage.

## App files

- `app/` — quiz, answer review, study Bible interface, and styles.
- `src/` — app entry point, question selection, grading, and saved-answer migration.
- `public/question-bank.json` — the single source for all questions, options, answer keys, Thai explanations, references, and source provenance. Edit this file directly to update quiz content.
- `content/aws-sap-c02-thai-exam-bible.md` — the study Bible.
- `tests/` — app behavior and question-bank integrity checks.
- `scripts/emit-worker.mjs` — creates the hosting worker during production builds.
- `vite.config.ts`, `vercel.json`, `.openai/hosting.json` — build and hosting configuration.

Builds copy the existing question bank without rewriting it or generating review reports. Per-question review records live in `audit/v2/<id>.json` (summary in `audit/status.tsv`); `python3 audit/tools/apply.py` merges them into `public/question-bank.json` and refuses prompt, option-text, or answer changes for recorded Skill Builder and course questions.

## Checks and production

```bash
npm test
npm run lint
npm run build
npm start
```

`npm test` includes a production build. Deploy the resulting `dist/` folder. Tests check answer grading, source filters, saved-answer migration, Thai explanations, and coverage of all 94 Bible products/features.

## Question sources and answer caveats

The bank contains 136 AWS Skill Builder captures (75 Week 8 questions and 61 earlier assessment questions), 69 app-authored course recaps, and 127 AI-authored questions (15 original, 107 Professional scenarios, and five optional emerging cases). AI-authored questions are not official AWS exam questions. Emerging cases are excluded by default.

Original source wording, corrected keys, accepted alternative answers, and ambiguity warnings remain in the question bank and answer-review UI. The 22 legacy ambiguous/historical flags have not all been independently verified against current AWS documentation; passing structural checks does not establish technical accuracy of every answer.

Historical scores use the current bank. The saved-answer migration preserves outcomes for the 69 course recaps after their answer-slot rotation and discloses changed distractor wording. Keep question IDs and option IDs stable when editing content to preserve saved attempts.

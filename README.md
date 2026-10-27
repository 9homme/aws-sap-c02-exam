# Architect Lab — SAP-C02 Practice

A browser-based AWS Certified Solutions Architect – Professional practice site.

## What it includes

- 225 source-labelled questions from the supplied Week 8 practice bank, CSV quiz bank, Weeks 5–7 course material, plus carefully marked original and optional emerging-AI questions.
- Study mode with 10, 25, 50, or 75 questions, immediate correction, and concise rationale. Filtered question counts are shown before starting; unavailable sizes are disabled instead of silently shortened, with an explicit option to practice all questions in a smaller pool.
- Every answer option has a teaching explanation in Study feedback and submitted mock reviews. Selected wrong choices and correct choices open automatically; other options can be expanded for comparison. Explanations are app-authored additions to the captured material.
- A 75-question, 180-minute full mock that uses the SAP-C02 domain mix.
- Saved in-progress attempts, past results, missed-question practice, and topic/domain performance summaries.
- A searchable Thai SAP-C02 study bible with 28 sidebar topics, beginner-friendly AWS product explanations, service comparisons, exam traps, decision rules, and a 21-day preparation plan.
- Responsive navigation, touch-friendly quiz controls, scrollable comparison tables, and a mobile topic drawer.

All progress is stored only in the browser's local storage on the device being used.

The original-scenario source contains 15 supplementary questions; a full mock draws 75 questions across eligible sources. The Week 8 captured source contains the full 75-question practice-exam record.

Teaching content is maintained in `content/option-explanations.mjs` and included by the bank generator. Visible answer-key notes preserve historical context: the imported Transit Gateway subnet key is corrected, and the Object Lock and Security Hub questions accept documented alternative single answers. Current-service caveats link to AWS documentation; the original CSV and Markdown captures remain unchanged.

Bookmark `/exam` for the practice dashboard and `/bible` for the Thai study Bible. Both routes support direct loading and browser Back/Forward navigation.
The included Vercel SPA rewrite keeps both bookmarked routes working when opened directly or refreshed.

## Development

```bash
node scripts/generate-question-bank.mjs
npm install
npm run dev
```

Run the production check with `npm run build`, or all automated checks with `npm test`.

The question data is generated in [public/question-bank.json](public/question-bank.json). Original and emerging-AI items are explicitly labelled in the interface so they can be filtered or excluded from core mock scoring.

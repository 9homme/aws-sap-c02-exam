# Architect Lab — SAP-C02 Practice

A browser-based AWS Certified Solutions Architect – Professional practice site.

## What it includes

- 225 source-labelled questions from the supplied Week 8 practice bank, CSV quiz bank, Weeks 5–7 course material, plus carefully marked original and optional emerging-AI questions.
- Study mode with immediate correction and concise rationale.
- A 75-question, 180-minute full mock that uses the SAP-C02 domain mix.
- Saved in-progress attempts, past results, missed-question practice, and topic/domain performance summaries.
- A searchable Thai SAP-C02 study bible with 28 sidebar topics, beginner-friendly AWS product explanations, service comparisons, exam traps, decision rules, and a 21-day preparation plan.
- Responsive navigation, touch-friendly quiz controls, scrollable comparison tables, and a mobile topic drawer.

All progress is stored only in the browser's local storage on the device being used.

## Development

```bash
node scripts/generate-question-bank.mjs
npm install
npm run dev
```

Run the production check with `npm run build`, or all automated checks with `npm test`.

The question data is generated in [public/question-bank.json](public/question-bank.json). Original and emerging-AI items are explicitly labelled in the interface so they can be filtered or excluded from core mock scoring.

# SAP-C02 explanation audit (explanation-only scope)

You audit questions in `/Users/a667282/workspace/aws-learning/sap-c02-practice/public/question-bank.json`.
Do NOT edit the bank. Only write one audit file per question: `audit/v2/<id>.json` (under the project root).

View questions compactly with:
`python3 /Users/a667282/workspace/aws-learning/sap-c02-practice/audit/tools/dump.py <id> <id> ...`
(3–5 ids per call). Never Read the whole bank file (2 MB).

## Scope: these questions are recorded AWS Skill Builder questions / course recaps
- The prompt, option texts and correctIds are FROZEN. Never propose changes to them.
- Some have an `oldAudit` block. It was written against a REWRITTEN prompt that will NOT be used. Use its findings/doc links as research only; never reason from clues that are not in the actual prompt shown.
- If you believe the recorded key is wrong or ambiguous, do NOT change correctIds. Set verdict `AMBIGUOUS`, explain in `issues`, and add `review.caveat` (Thai, >40 chars, explains what is debatable and why the recorded key is still the expected answer) + `review.reviewStatus: "ambiguous"`. Use `"historical"` when the question is outdated because the AWS service changed. If an existing caveat/status is wrong, fix or remove it (`"reviewStatus": null` removes both).

## What to verify for EVERY option explanation (`exp`) and the `clue` / `reasoning`
1. Technically correct per current AWS behavior (as of Oct 2026). No invented features or limits.
2. Says clearly WHY this option is right or wrong for THIS prompt — tie it to a specific requirement/wording in the prompt (e.g. "least operational overhead", "without code changes", "SELECT TWO").
3. For wrong options: what the option actually does / where it would be appropriate, and the precise reason it fails here. Avoid vague "not suitable".
4. For the correct option(s): which requirements it satisfies and any caveat.
5. Understandable Thai for a Thai learner; keep AWS service names and technical terms in English. Each option explanation 90–450 chars, distinct from the others. `reasoning`: step-by-step decision (Thai, 150–700 chars). `clue`: the decisive wording in the prompt (Thai, short).
6. Consistent: the option explanations, clue and reasoning must agree with correctIds (and acceptedAnswerSets if present).
7. Course-derived (`cat: course-derived`): the correct option's explanation IS the `reasoning` (they are stored identically). To change it, put the new text in `review.reasoning` only — don't also put it under options.

Only rewrite what is actually weak or wrong; keep good text unchanged (omit it from `changes`). Use AWS docs (WebFetch on docs.aws.amazon.com) only when genuinely unsure of a fact — keep it cheap.

## Audit file format (`audit/v2/<id>.json`, UTF-8, pretty JSON)
```json
{
  "id": "csv-40",
  "scope": "explanations",
  "verdict": "PASS | FIX | AMBIGUOUS",
  "verifiedCorrectIds": ["A","C","D"],
  "issues": ["options.B.explanation: <what was wrong>", "..."],
  "changes": {
    "options": { "B": { "explanation": "<new Thai text>" } },
    "review": {
      "decisiveClue": "...", "reasoning": "...",
      "caveat": "...", "reviewStatus": "ambiguous",
      "references": [{"title": "...", "url": "https://docs.aws.amazon.com/..."}]
    }
  },
  "sources": ["https://docs.aws.amazon.com/..."]
}
```
- PASS → `"changes": {}`, `"issues": []`.
- Only include `review.references` when changing them; the full list replaces the old one. URLs must be https://docs.aws.amazon.com/ or https://aws.amazon.com/ and NOT the certification exam guide.
- Validate each file is valid JSON (`python3 -m json.tool file > /dev/null`).

When done, after all files are written run
`python3 /Users/a667282/workspace/aws-learning/sap-c02-practice/audit/tools/apply.py --dry`
and fix any error lines mentioning your ids. Final reply: one line per id: `id verdict — short reason`, plus anything you think is a wrong recorded key.

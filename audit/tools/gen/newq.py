"""Stage a new AI Professional question in audit/new/<id>.json using the plan in audit/tools/plan_new.py."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from plan_new import PLAN, REQS

ROOT = "/Users/a667282/workspace/aws-learning/sap-c02-practice"
TASKS = {"1": "Organizational complexity", "2": "New solution design", "3": "Continuous improvement", "4": "Migration and modernization"}
ROWS = {r[0]: r for r in PLAN}
os.makedirs(f"{ROOT}/audit/new", exist_ok=True)


def newq(*a, **k):
    try:
        _newq(*a, **k)
    except AssertionError as e:
        print('FAIL', e)


def _newq(qid, topic, prompt, options, clue, reasoning, refs):
    _, domain, qual, _, _, _, key, products = ROWS[qid]
    errs = []
    if not 1100 <= len(prompt) <= 1600: errs.append(("prompt", len(prompt)))
    for oid, (text, exp) in options.items():
        if not 250 <= len(text) <= 450: errs.append((oid, "text", len(text)))
        if not 90 <= len(exp) <= 600: errs.append((oid, "exp", len(exp)))
    if not options[key][1].startswith("ถูก"): errs.append(("key exp must start with ถูก", key))
    errs += [(oid, "non-key starts with ถูก") for oid, (_, e) in options.items() if oid != key and e.startswith("ถูก")]
    if not 150 <= len(reasoning) <= 900: errs.append(("reasoning", len(reasoning)))
    assert sorted(options) == ["A", "B", "C", "D"] and not errs, (qid, errs)
    q = {"id": qid, "sourceCategory": "professional", "sourceLabel": "AI-authored · Professional multi-requirement",
         "sourceDetail": f"Original multi-constraint scenario — {topic}", "coreEligible": True, "emerging": False,
         "domain": domain, "task": TASKS[domain], "topic": topic, "type": "multiple-choice", "selectCount": 1,
         "prompt": prompt, "options": [{"id": k, "text": options[k][0], "explanation": options[k][1]} for k in "ABCD"],
         "correctIds": [key], "rationale": reasoning,
         "wrongAnswerHelp": "Start with the explicit business constraint, then eliminate choices that solve a different layer of the architecture or add unnecessary operational work.",
         "references": [u for _, u in refs], "products": products, "requirements": REQS[qid],
         "review": {"decisiveClue": clue, "reasoning": reasoning,
                    "options": {k: options[k][1] for k in "ABCD"},
                    "references": [{"title": t, "url": u} for t, u in refs], "reviewedAt": "2026-10-29"}}
    json.dump(q, open(f"{ROOT}/audit/new/{qid}.json", "w"), ensure_ascii=False, indent=2)
    print(qid, key, qual, len(prompt))

# Usage: python3 dump.py ID [ID...]  -> compact view of questions (+ old audit issues for reference)
import json, sys, os
ROOT = "/Users/a667282/workspace/aws-learning/sap-c02-practice"
bank = {q["id"]: q for q in json.load(open(f"{ROOT}/public/question-bank.json"))}
for qid in sys.argv[1:]:
    q = bank[qid]; r = q["review"]
    out = {"id": qid, "cat": q["sourceCategory"], "domain": q["domain"], "topic": q["topic"],
           "selectCount": q["selectCount"], "prompt": q["prompt"],
           "options": [{"id": o["id"], "text": o["text"], "exp": o["explanation"]} for o in q["options"]],
           "correctIds": q["correctIds"], "clue": r["decisiveClue"], "reasoning": r["reasoning"]}
    for k in ("acceptedAnswerSets", "recordedCorrectIds", "studyNote", "requirements"):
        if q.get(k): out[k] = q[k]
    if q["rationale"] != r["reasoning"]: out["recordedRationale"] = q["rationale"]
    for k in ("caveat", "reviewStatus"):
        if r.get(k): out[k] = r[k]
    out["refs"] = [x["url"] for x in r["references"]]
    old = f"{ROOT}/audit/{qid}.json"
    if os.path.exists(old):
        a = json.load(open(old))
        iss = a.get("issues", [])
        out["oldAudit(reference only; written against a REWRITTEN prompt)"] = {
            "verdict": a.get("verdict"), "verifiedCorrectIds": a.get("verifiedCorrectIds"),
            "issues": json.dumps(iss, ensure_ascii=False)[:1800], "sources": a.get("sources", [])[:8]}
    print(json.dumps(out, ensure_ascii=False, indent=0)); print("-----")

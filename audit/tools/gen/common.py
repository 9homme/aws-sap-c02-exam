import json
ROOT = "/Users/a667282/workspace/aws-learning/sap-c02-practice"
BANK = {q["id"]: q for q in json.load(open(f"{ROOT}/public/question-bank.json"))}


def emit(qid, correct, *, prompt, options, clue, reasoning, rationale, refs, issues, clear_status=False, caveat=None, status=None):
    q = BANK[qid]
    correct = correct if isinstance(correct, list) else [correct]
    for oid, (text, exp) in options.items():
        assert 90 <= len(exp) <= 520, (qid, oid, len(exp))
    review = {"decisiveClue": clue, "reasoning": reasoning,
              "references": [{"title": t, "url": u} for t, u in refs]}
    if caveat:
        review["caveat"], review["reviewStatus"] = caveat, status or "ambiguous"
    elif clear_status or q["review"].get("reviewStatus"):
        review["reviewStatus"] = None
    audit = {"id": qid, "scope": "full", "verdict": "FIX",
             "originalCorrectIds": q["correctIds"], "verifiedCorrectIds": correct,
             "issues": issues,
             "changes": {"prompt": prompt, "correctIds": correct, "rationale": rationale,
                         "options": {k: {"text": t, "explanation": e} for k, (t, e) in options.items()},
                         "review": review},
             "sources": [u for _, u in refs]}
    with open(f"{ROOT}/audit/v2/{qid}.json", "w") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    print(qid, "->", correct, len(prompt))


def patch(qid, verdict="PASS", issues=(), options=None, review=None, correct=None):
    q = BANK[qid]
    ch = {}
    if options:
        for oid, e in options.items():
            assert 90 <= len(e) <= 520, (qid, oid, len(e))
        ch["options"] = {k: {"explanation": e} for k, e in options.items()}
    if review: ch["review"] = review
    if correct: ch["correctIds"] = correct
    audit = {"id": qid, "scope": "full", "verdict": verdict, "originalCorrectIds": q["correctIds"],
             "verifiedCorrectIds": correct or q["correctIds"], "issues": list(issues), "changes": ch,
             "sources": [r["url"] for r in q["review"]["references"]]}
    with open(f"{ROOT}/audit/v2/{qid}.json", "w") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    print(qid, verdict)


import re
def clean_prompt(p):
    p = p.replace("The architecture review board will approve a design only when it satisfies every non-negotiable requirement:", "The solution must meet all of the following requirements:")
    p = re.sub(r"\s*The team will reject an alternative[^.]*\.", "", p)
    p = re.sub(r"\s*The selected approach must be workable[^.]*\.", "", p)
    p = p.replace("Which solution meets ALL of the stated requirements with the most appropriate operational trade-offs?", "Which solution meets these requirements with the LEAST operational overhead?")
    p = p.replace("The architecture decision must satisfy all of the following independent acceptance criteria:", "The solution must meet all of the following requirements:")
    p = re.sub(r"\s*Assume the existing production estate[^.]*\.", "", p)
    p = re.sub(r"\s*The team will review the network and security boundaries[^.]*\.", "", p)
    p = p.replace("Select the solution that satisfies ALL criteria, not merely the service with the most familiar name.", "Which solution meets these requirements with the LEAST operational overhead?")
    return p


def tfix(qid, options, clue, reasoning, refs, extra_issue=None, edits=()):
    """Rewrite options of a template-style professional question; keep scenario, key letter, products."""
    q = BANK[qid]
    key = q["correctIds"][0]
    assert set(options) == {o["id"] for o in q["options"]}
    for oid, (t, e) in options.items():
        assert 90 <= len(e) <= 560, (qid, oid, len(e))
    prompt = clean_prompt(q["prompt"])
    for old, new in edits:
        assert old in prompt, (qid, old)
        prompt = prompt.replace(old, new)
    assert len(prompt) >= 850, (qid, len(prompt))
    issues = ["options: ตัวลวงเดิมผิดอย่างชัดเจน (อ้างความสามารถที่บริการไม่มี) ทำให้ตอบได้จากการจำชื่อบริการ ไม่ใช่ระดับ SAP-C02 Professional; เขียนใหม่ให้แต่ละตัวลวงทำงานได้จริงบางส่วนแต่ตกเงื่อนไขหนึ่งข้อ",
              "prompt: ลบประโยค boilerplate (architecture review board / workable for the stated environment)",
              "review.reasoning: เดิมคัดลอก requirement ภาษาอังกฤษมาต่อกัน ไม่ได้อธิบายการตัดตัวเลือก"]
    if extra_issue: issues.append(extra_issue)
    audit = {"id": qid, "scope": "full", "verdict": "FIX", "originalCorrectIds": q["correctIds"], "verifiedCorrectIds": [key],
             "issues": issues,
             "changes": {"prompt": prompt,
                         "options": {k: {"text": t, "explanation": e} for k, (t, e) in options.items()},
                         "review": {"decisiveClue": clue, "reasoning": reasoning,
                                    "references": [{"title": t, "url": u} for t, u in refs]}},
             "sources": [u for _, u in refs]}
    with open(f"{ROOT}/audit/v2/{qid}.json", "w") as f:
        json.dump(audit, f, ensure_ascii=False, indent=2)
    print(qid, key, len(prompt))

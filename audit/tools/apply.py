# Usage: python3 apply.py [--dry]  -> merges audit/v2/*.json into public/question-bank.json
import json, glob, sys
ROOT = "/Users/a667282/workspace/aws-learning/sap-c02-practice"
P = f"{ROOT}/public/question-bank.json"
bank = json.load(open(P)); by = {q["id"]: q for q in bank}
RECORDED = {"captured", "csv", "course-derived"}   # question/answer text is frozen
errs = []; applied = 0
for f in sorted(glob.glob(f"{ROOT}/audit/v2/*.json")):
    a = json.load(open(f)); q = by[a["id"]]; ch = a.get("changes", {}) or {}; r = q["review"]
    frozen = q["sourceCategory"] in RECORDED
    if frozen and (ch.get("prompt") or ch.get("correctIds") or any("text" in v for v in ch.get("options", {}).values())):
        errs.append(f"{a['id']}: prompt/option text/correctIds change not allowed for {q['sourceCategory']}"); continue
    if "prompt" in ch: q["prompt"] = ch["prompt"]
    if "correctIds" in ch: q["correctIds"] = ch["correctIds"]
    if "rationale" in ch and not frozen: q["rationale"] = ch["rationale"]
    opts = {o["id"]: o for o in q["options"]}
    for oid, v in ch.get("options", {}).items():
        if oid not in opts: errs.append(f"{a['id']}: unknown option {oid}"); continue
        if "text" in v: opts[oid]["text"] = v["text"]
        if "explanation" in v: opts[oid]["explanation"] = v["explanation"]
    rv = ch.get("review", {})
    for k in ("decisiveClue", "reasoning", "caveat", "references"):
        if k in rv: r[k] = rv[k]
    if "references" in rv and not frozen: q["references"] = [x["url"] for x in rv["references"]]
    if "reviewStatus" in rv:
        if rv["reviewStatus"]: r["reviewStatus"] = rv["reviewStatus"]
        else: r.pop("reviewStatus", None); r.pop("caveat", None)
    if q["sourceCategory"] == "course-derived":   # correct option text == reasoning (test invariant)
        c = opts[q["correctIds"][0]]
        if "reasoning" in rv: c["explanation"] = r["reasoning"]
        else: r["reasoning"] = c["explanation"]
    if q["sourceCategory"] == "professional": q["rationale"] = r["reasoning"]
    r["options"] = {o["id"]: o["explanation"] for o in q["options"]}
    r["reviewedAt"] = "2026-10-29"
    # sanity
    for o in q["options"]:
        if len(o["explanation"]) < 90: errs.append(f"{a['id']}/{o['id']}: explanation <90 chars")
    if len({o['explanation'] for o in q['options']}) != len(q['options']): errs.append(f"{a['id']}: duplicate explanations")
    if len(r["reasoning"]) < 60: errs.append(f"{a['id']}: reasoning <60")
    for x in r["references"]:
        if not x["url"].startswith(("https://docs.aws.amazon.com/", "https://aws.amazon.com/")) or "aws-certification" in x["url"]:
            errs.append(f"{a['id']}: bad ref {x['url']}")
    applied += 1
print("applied", applied); print("\n".join(errs) or "no errors")
if "--dry" not in sys.argv and not errs:
    json.dump(bank, open(P, "w"), ensure_ascii=False, indent=2); open(P, "a").write("\n"); print("written")

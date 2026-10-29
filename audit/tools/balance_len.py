# Run after audit/tools/gen/n*.py: reduce the "correct answer is the longest option" giveaway in audit/new/*.json.
# Appends neutral operational steps (no capability that could satisfy a requirement) to the longest distractor.
import json, glob, random
ROOT = "/Users/a667282/workspace/aws-learning/sap-c02-practice"
NEUTRAL = ["Tag all new resources with the owning team and cost center.",
           "Document the new configuration in the operations runbook.",
           "Validate the change in a staging environment before production.",
           "Define the resources in AWS CloudFormation templates for repeatable deployment.",
           "Review the design with the architecture board before rollout."]
TARGET_LONGEST = 11  # ≈ 25% of 44
files = sorted(glob.glob(f"{ROOT}/audit/new/*.json"))
qs = [json.load(open(f)) for f in files]
rng = random.Random(7)

def correct_is_longest(q):
    k = q["correctIds"][0]; L = {o["id"]: len(o["text"]) for o in q["options"]}
    return L[k] == max(L.values())

cands = [q for q in qs if correct_is_longest(q)]
rng.shuffle(cands)
need = max(0, len(cands) - TARGET_LONGEST)
fixed = 0
for q in cands:
    if fixed >= need: break
    k = q["correctIds"][0]; ck = len(next(o for o in q["options"] if o["id"] == k)["text"])
    d = max((o for o in q["options"] if o["id"] != k), key=lambda o: len(o["text"]))
    text = d["text"]
    for s in rng.sample(NEUTRAL, len(NEUTRAL)):
        if len(text) > ck + 10: break
        if len(text) + 1 + len(s) <= 450: text = f"{text} {s}"
    if len(text) > ck + 10:
        d["text"] = text; fixed += 1
for q, f in zip(qs, files):
    json.dump(q, open(f, "w"), ensure_ascii=False, indent=2)
print("candidates", len(cands), "fixed", fixed, "now longest:", sum(correct_is_longest(q) for q in qs))

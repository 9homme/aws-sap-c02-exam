# Usage: python3 add_new.py [--dry]  -> insert/replace audit/new/*.json questions after the last professional question
import json, glob, sys
ROOT = "/Users/a667282/workspace/aws-learning/sap-c02-practice"
P = f"{ROOT}/public/question-bank.json"
bank = json.load(open(P))
new = {q["id"]: q for q in (json.load(open(f)) for f in glob.glob(f"{ROOT}/audit/new/*.json"))}
bank = [q for q in bank if q["id"] not in new]
last = max(i for i, q in enumerate(bank) if q["sourceCategory"] == "professional")
ordered = sorted(new.values(), key=lambda q: int(q["id"].split("-")[1]))
bank[last + 1:last + 1] = ordered
print("bank size", len(bank), "new", len(ordered))
if "--dry" not in sys.argv:
    json.dump(bank, open(P, "w"), ensure_ascii=False, indent=2); open(P, "a").write("\n"); print("written")

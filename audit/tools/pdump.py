import json,sys
b={q["id"]:q for q in json.load(open("/Users/a667282/workspace/aws-learning/sap-c02-practice/public/question-bank.json"))}
for i in sys.argv[1:]:
    q=b[i]; print(f"## {i} sel={q['selectCount']} key={q['correctIds']} {q.get('reviewStatus','')}{q['review'].get('reviewStatus','')}")
    print("P:",q["prompt"])
    for o in q["options"]: print(f"{o['id']}) {o['text']}\n   >> {o['explanation']}")
    print("R:",q["review"]["reasoning"])
    if q["review"].get("caveat"): print("CAV:",q["review"]["caveat"])
    print("REF:"," ".join(r["url"] for r in q["review"]["references"]))

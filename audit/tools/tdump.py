import json,sys,re
b={q["id"]:q for q in json.load(open("/Users/a667282/workspace/aws-learning/sap-c02-practice/public/question-bank.json"))}
def clean(p):
    p=p.replace("The architecture review board will approve a design only when it satisfies every non-negotiable requirement:","The solution must meet all of the following requirements:")
    p=re.sub(r"\s*The team will reject an alternative[^.]*\.","",p)
    p=re.sub(r"\s*The selected approach must be workable[^.]*\.","",p)
    p=p.replace("The architecture decision must satisfy all of the following independent acceptance criteria:","The solution must meet all of the following requirements:")
    p=re.sub(r"\s*Assume the existing production estate[^.]*\.","",p)
    p=re.sub(r"\s*The team will review the network and security boundaries[^.]*\.","",p)
    p=p.replace("Select the solution that satisfies ALL criteria, not merely the service with the most familiar name.","Which solution meets these requirements with the LEAST operational overhead?")
    return p
for i in sys.argv[1:]:
    q=b[i]; c=q["correctIds"][0]
    p=clean(q["prompt"])
    print(f"## {i} key={c} len={len(p)} dom={q['domain']} prods={q['products']}")
    print("P:",p)
    print("OK:",[o["text"] for o in q["options"] if o["id"]==c][0])
    print("REF:"," ".join(r["url"] for r in q["review"]["references"]))

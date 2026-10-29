#!/bin/zsh
# Check titles of reference URLs in staged new questions; print only suspicious ones.
cd /Users/a667282/workspace/aws-learning/sap-c02-practice
python3 -c "
import json,glob
print('\n'.join(sorted({r['url'] for f in glob.glob('audit/new/*.json') for r in json.load(open(f))['review']['references']})))" > audit/tools/new-urls.txt
zsh audit/tools/checkurls.sh audit/tools/new-urls.txt | python3 -c "
import sys
for l in sys.stdin:
    if ' - ' not in l.split('|')[0]: print('BAD', l.strip())
print('checked')"

#!/bin/zsh
# usage: checkurls.sh file-with-urls ; prints title per URL
while read u; do
  t=$(curl -s -L --max-time 20 "$u" | tr '\n' ' ' | grep -o '<title>[^<]*</title>' | head -1)
  echo "$t | $u"
done < "$1"

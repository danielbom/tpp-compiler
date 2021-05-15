#!/usr/bin/bash

content=`cat .*.dot`
content=`echo -e "digraph G {\\n\\n${content//digraph/subgraph} \\n\\n}" > $1`

for f in `ls .*.dot`; do 
  if [ "$f" != "$1" ]; then 
    rm $f
  fi
done

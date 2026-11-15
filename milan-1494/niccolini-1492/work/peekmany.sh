#!/bin/bash
# usage: peekmany.sh IMG SCALE STEP "x0 y0 x1 y1 name" ...
I=$1; SC=$2; ST=$3; shift 3
S=/private/tmp/claude-501/-Users-aaymeloglu--claude-assistant/bb84367b-ee61-4584-a4ee-8cb8e710bd86/scratchpad
for r in "$@"; do set -- $r; uv run --with pillow python peek.py $I $1 $2 $3 $4 $SC $S/$5.png $ST; done

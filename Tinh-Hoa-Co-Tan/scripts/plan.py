"""Generate bounded per-run GH Actions matrix; catalog size has no fixed limit."""
import json
import sys
from pathlib import Path

all_ids=sorted(p.stem for p in (Path(__file__).resolve().parents[1]/'episodes').glob('tap-*.json'))
arg=(sys.argv[1] if len(sys.argv)>1 else 'latest').strip().lower()
if not all_ids: raise SystemExit('No episode files!')
if arg=='latest': ids=[all_ids[-1]]
elif arg=='all': ids=all_ids
elif arg.startswith('range:'):
    a,b=arg[6:].split('-',1)
    ids=[f'tap-{n:04d}' for n in range(int(a),int(b)+1)]
else: ids=[a.strip() for a in arg.split(',') if a.strip()]
if len(ids)>128:
    raise SystemExit('Maximum 128 per workflow run; use range:0001-0128 etc. Catalog size is unlimited.')
if not ids or any(i not in all_ids for i in ids):
    raise SystemExit(f'Invalid episode selection {ids}; catalog has {len(all_ids)} entries.')
print(json.dumps({'include':[{'episode':id} for id in dict.fromkeys(ids)]},separators=(',',':')))

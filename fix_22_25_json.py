import json
import os
import re

def fix_formulas(file_num):
    path = f'Series-Dai-So-To-Hop/comb{file_num}_formulas.json'
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        data = json.load(f)

    for k, v in data.items():
        v = re.sub(r'\bdp\b', '"dp"', v)
        v = re.sub(r'\bmask\b', '"mask"', v)
        v = re.sub(r'\bcap\b', 'sect', v)
        v = re.sub(r'\bdots\b', '...', v)
        v = re.sub(r'\bcdot\b', 'dot.c', v)
        v = re.sub(r'\bxR\b', 'x R', v)
        v = re.sub(r'\bempty\b', 'emptyset', v)
        data[k] = v

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

for i in [22, 23, 24, 25]:
    fix_formulas(i)

print("Fixed JSONs")

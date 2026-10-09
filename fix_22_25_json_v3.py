import json
import os

def fix_formulas(file_num):
    path = f'Series-Dai-So-To-Hop/comb{file_num}_formulas.json'
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        data = json.load(f)

    for k, v in data.items():
        v = v.replace('p to q', 'p -> q')
        data[k] = v

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

for i in [22, 23, 24, 25]:
    fix_formulas(i)

print("Fixed JSONs v3")

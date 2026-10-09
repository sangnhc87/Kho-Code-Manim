import json

f19 = 'Series-Dai-So-To-Hop/comb19_formulas.json'
with open(f19, 'r') as f: data = json.load(f)

if 'special_0' in data: data['special_0'] = data['special_0'].replace('N_(no A)', 'N_("no A")')
if 'special_2' in data: data['special_2'] = data['special_2'].replace('N_(no A)', 'N_("no A")')
if 'special_3' in data: data['special_3'] = data['special_3'].replace('N_(A, no B)', 'N_("A, no B")')

with open(f19, 'w') as f: json.dump(data, f, indent=2)

print("Fixed JSON 19")

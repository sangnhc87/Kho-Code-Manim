import json

f17 = 'Series-Dai-So-To-Hop/comb17_formulas.json'
with open(f17, 'r') as f: data = json.load(f)
if 'binary_2' in data: data['binary_2'] = data['binary_2'].replace('ab + ba', 'a b + b a')
with open(f17, 'w') as f: json.dump(data, f, indent=2)

f18 = 'Series-Dai-So-To-Hop/comb18_formulas.json'
with open(f18, 'r') as f: data = json.load(f)
if 'proof_5' in data: data['proof_5'] = data['proof_5'].replace('N_(co A)+N_(khong A)', 'N_("co A") + N_("khong A")')
with open(f18, 'w') as f: json.dump(data, f, indent=2)

print("Fixed JSON")

import json

f20 = 'Series-Dai-So-To-Hop/comb20_formulas.json'
with open(f20, 'r') as f: data = json.load(f)

if 'evenodd_3' in data: data['evenodd_3'] = data['evenodd_3'].replace('N_(chan)=N_(le)', 'N_("chan")=N_("le")')
if 'challenge_5' in data: data['challenge_5'] = data['challenge_5'].replace('boxed(S=112500)', 'S=112500')

with open(f20, 'w') as f: json.dump(data, f, indent=2)
print("Fixed 20")

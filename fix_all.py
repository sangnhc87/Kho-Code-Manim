import re

# Fix 22
with open("Series-Dai-So-To-Hop/comb22_lesson_data.py", 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('dp[i+1,k,q_0]+="dp"[i,k,q]', '"dp"[i+1,k,q_0]+="dp"[i,k,q]')
c = c.replace('dp[i+1,k+1,q_1]+="dp"[i,k,q]', '"dp"[i+1,k+1,q_1]+="dp"[i,k,q]')
c = c.replace('dp[i+1,k,q_0]+=dp[i,k,q]', '"dp"[i+1,k,q_0]+="dp"[i,k,q]')
c = c.replace('dp[i+1,k+1,q_1]+=dp[i,k,q]', '"dp"[i+1,k+1,q_1]+="dp"[i,k,q]')
c = c.replace('dp[', '"dp"[')
c = c.replace('dp_', '"dp"_')
with open("Series-Dai-So-To-Hop/comb22_lesson_data.py", 'w', encoding='utf-8') as f:
    f.write(c.replace('""dp""', '"dp"'))

# Fix 25
with open("Series-Dai-So-To-Hop/comb25_lesson_data.py", 'r', encoding='utf-8') as f:
    c = f.read()

reps = {
    'quay': '"quay"',
    'guong': '"guong"',
    'Fix': '"Fix"',
    'prod': 'product', # wait, prod is just \prod in latex. In typst it's `product` or `product`? No, it's `product` in Typst.
    'cdot': 'dot.c',
    'jr': 'j r',
    'orbits': '"orbits"',
    'Orb': '"Orb"',
    'Stab': '"Stab"',
    'cube': '"cube"',
    'orbit': '"orbit"',
    '""Fix""': '"Fix"',
    '""quay""': '"quay"',
    '""guong""': '"guong"',
    '""orbits""': '"orbits"',
    '""Orb""': '"Orb"',
    '""Stab""': '"Stab"',
    '""cube""': '"cube"',
    '""orbit""': '"orbit"',
}

for k, v in reps.items():
    c = c.replace(k, v)

with open("Series-Dai-So-To-Hop/comb25_lesson_data.py", 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed")

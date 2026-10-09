import re
import ast

def replace_in_dict(d, replacements):
    new_dict = {}
    for k, v in d.items():
        if isinstance(v, tuple):
            new_tuple = []
            for item in v:
                if isinstance(item, str):
                    for old, new in replacements:
                        item = item.replace(old, new)
                elif isinstance(item, tuple):
                    new_item = []
                    for sub in item:
                        if isinstance(sub, str):
                            for old, new in replacements:
                                sub = sub.replace(old, new)
                        new_item.append(sub)
                    item = tuple(new_item)
                new_tuple.append(item)
            new_dict[k] = tuple(new_tuple)
        else:
            new_dict[k] = v
    return new_dict

reps_22 = [
    ("dp_(t+1,q)=sum_(p to q)dp_(t,p)", '"dp"_(t+1,q)=sum_(p -> q)"dp"_(t,p)'),
    ('dp_("mask"+2^j) += dp_("mask")', '"dp"_("mask"+2^j) += "dp"_("mask")'),
    ('dp_(mask+2^j) += dp_(mask)', '"dp"_("mask"+2^j) += "dp"_("mask")'),
    ('dp[0000]', '"dp"[0000]'),
    ('dp[1111]', '"dp"[1111]'),
    ('dp[i,k,q]', '"dp"[i,k,q]'),
    ('dp[i+1,k,q_0]+=dp[i,k,q]', '"dp"[i+1,k,q_0]+="dp"[i,k,q]'),
    ('dp[i+1,k+1,q_1]+=dp[i,k,q]', '"dp"[i+1,k+1,q_1]+="dp"[i,k,q]'),
    ('N=sum_q dp_(10,4,q,0)', 'N=sum_q "dp"_(10,4,q,0)'),
    ('0 <= mask < 2^4', '0 <= "mask" < 2^4')
]

reps_23 = [
    ('N(E_(i_1) cap dots cap E_(i_k))', 'N(E_(i_1) inter ... inter E_(i_k))'),
    ('6!-3 cdot 5!', '6!-3 dot.c 5!'),
    ('6!-3 cdot 5!+3 cdot 4!', '6!-3 dot.c 5!+3 dot.c 4!'),
    ('C_2^5 D_3=10 cdot 2=20', 'C_2^5 D_3=10 dot.c 2=20'),
    ('R_B(x)=R_(B-p)(x)+xR_(B-r-c)(x)', 'R_B(x)=R_(B-p)(x)+x R_(B-r-c)(x)'),
    ('xR_(B-r-c)(x)', 'x R_(B-r-c)(x)'),
    ('R_empty(x)=1', 'R_emptyset(x)=1')
]

reps_24 = [
    ("L=UUDUDD", 'L="UUDUDD"')
]

reps_25 = [
    ('N_(quay)', 'N_("quay")'),
    ('N_(guong)', 'N_("guong")'),
    ('Fix(g)', '"Fix"(g)'),
    ('Fix(e)', '"Fix"(e)'),
    ('Fix(r', '"Fix"(r'),
    ('prod_', 'product_'),
    ('cdot', 'dot.c'),
    ('zeta^(-jr)', 'zeta^(-j r)'),
    ('N_(orbits)', 'N_("orbits")'),
    ('Orb(x)', '"Orb"(x)'),
    ('Stab(x)', '"Stab"(x)'),
    ('G_(cube)', 'G_("cube")'),
    ('N_(orbit)', 'N_("orbit")')
]

import sys
sys.path.append('Series-Dai-So-To-Hop')

import importlib
for num, reps in [(22, reps_22), (23, reps_23), (24, reps_24), (25, reps_25)]:
    try:
        # Instead of parsing, we will just read the file as text and do string replace.
        # This is safer if we just replace the EXACT string literals in the file.
        with open(f"Series-Dai-So-To-Hop/comb{num}_lesson_data.py", 'r', encoding='utf-8') as f:
            text = f.read()
        
        for old, new in reps:
            # We ONLY want to replace it inside string literals.
            # Easiest way is to replace `'{old}'` with `'{new}'`
            # and `"{old}"` with `"{new}"`
            # But the strings might be parts of bigger strings, e.g. `'dp[0000]=1'`
            # Just doing simple string replace is mostly fine if it doesn't match python code.
            # `dp_(t+1,q)` doesn't appear in python code outside strings.
            # `dp[` doesn't either, wait! `dp=` is python code.
            # `dp[` is in `dp[0]=1` which IS python code!
            # So `dp[0000]` is safe, `0000` is not python code (Syntax error for leading zeros).
            # `dp[i,k,q]` - python tuple index `dp[i,k,q]` might be python code? Not in this script.
            # To be absolutely safe, let's just do text replace!
            text = text.replace(old, new)

        with open(f"Series-Dai-So-To-Hop/comb{num}_lesson_data.py", 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print(e)

print("Done string replace")

import re

for i in [24, 25]:
    path = f"Series-Dai-So-To-Hop/comb{i}_lesson_data.py"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        continue
    
    # 24
    content = content.replace("L=UUDUDD", 'L="UUDUDD"')

    # 25
    content = content.replace('N=frac(1,6)sum_(g in G)|Fix(g)|', 'N=frac(1,6)sum_(g in G)|"Fix"(g)|')
    content = content.replace('|Fix(g)|=2^(c(g))', '|"Fix"(g)|=2^(c(g))')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replaced strings in lesson_data for 24 and 25")

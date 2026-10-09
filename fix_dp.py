import re

for i in [22, 23, 24, 25]:
    path = f"Series-Dai-So-To-Hop/comb{i}_lesson_data.py"
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        continue
    
    # Just fix all 'dp' to '"dp"' when it's next to '[' or '_'
    content = re.sub(r'(?<!")\bdp\b(?!")', '"dp"', content)
    
    # And fix any `x R` or `sect` remaining
    content = content.replace("sect", "inter")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replaced strings using regex")

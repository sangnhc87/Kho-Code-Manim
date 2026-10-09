with open("Series-Dai-So-To-Hop/comb22_lesson_data.py", 'r', encoding='utf-8') as f:
    c = f.read()
# Find and replace all `dp[` and `dp_` inside strings only.
# Actually, since I reverted, there are no `dp` assignments except in `tilings` which is `dp = [0]*(n+2)`.
# So `dp[` or `dp_` are safe to replace if they are not assignments.
c = c.replace("dp[i+1", '"dp"[i+1')
c = c.replace("dp[i", '"dp"[i')
c = c.replace('""dp""', '"dp"')
with open("Series-Dai-So-To-Hop/comb22_lesson_data.py", 'w', encoding='utf-8') as f:
    f.write(c)
print("Done")

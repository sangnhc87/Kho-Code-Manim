with open("Series-Dai-So-To-Hop/comb23_lesson_data.py", 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('6!-3 dot.c 5!+3 cdot 4!', '6!-3 dot.c 5!+3 dot.c 4!')
with open("Series-Dai-So-To-Hop/comb23_lesson_data.py", 'w', encoding='utf-8') as f:
    f.write(c)

with open("Series-Dai-So-To-Hop/comb24_lesson_data.py", 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('peaks(w)=#(UD)', '"peaks"(w)=#("UD")')
with open("Series-Dai-So-To-Hop/comb24_lesson_data.py", 'w', encoding='utf-8') as f:
    f.write(c)
print("Done")

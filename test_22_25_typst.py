import json
import subprocess
import tempfile
import os

for file_num in [22, 23, 24, 25]:
    path = f'Series-Dai-So-To-Hop/comb{file_num}_formulas.json'
    if not os.path.exists(path): continue
    with open(path, 'r') as f:
        data = json.load(f)

    for k, v in data.items():
        with tempfile.NamedTemporaryFile(suffix='.typ', mode='w') as f:
            f.write(f"#align(center)[$ {v} $]\n")
            f.flush()
            try:
                subprocess.run(['typst', 'compile', f.name], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"FAIL {file_num} - {k}: {v}\n{e.stderr}")

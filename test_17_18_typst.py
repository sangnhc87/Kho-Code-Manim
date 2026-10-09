import json
import subprocess
import tempfile

for file_num in [17, 18]:
    with open(f'Series-Dai-So-To-Hop/comb{file_num}_formulas.json', 'r') as f:
        data = json.load(f)

    for k, v in data.items():
        with tempfile.NamedTemporaryFile(suffix='.typ', mode='w') as f:
            f.write(f"#align(center)[$ {v} $]\n")
            f.flush()
            try:
                subprocess.run(['typst', 'compile', f.name], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"FAIL {k}: {v}\n{e.stderr}")

import sys
import subprocess
import tempfile
import os
sys.path.append('Series-Dai-So-To-Hop')

for num in [22, 23, 24, 25]:
    try:
        module = __import__(f'comb{num}_lesson_data')
        formulas = module.FORMULAS
        for k, v in formulas.items():
            if not isinstance(v, str):
                v = v[0] # Just in case it's a tuple
            with tempfile.NamedTemporaryFile(suffix='.typ', mode='w') as f:
                f.write(f"#align(center)[$ {v} $]\n")
                f.flush()
                try:
                    subprocess.run(['typst', 'compile', f.name], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"FAIL {num} - {k}: {v}\n{e.stderr}")
    except Exception as e:
        print(f"Error {num}: {e}")

import subprocess
import tempfile
import sys

formula = "a mod b"
with tempfile.NamedTemporaryFile(suffix='.typ', mode='w') as f:
    f.write(f"#align(center)[$ {formula} $]\n")
    f.flush()
    try:
        subprocess.run(['typst', 'compile', f.name], check=True, capture_output=True, text=True)
        print("SUCCESS")
    except subprocess.CalledProcessError as e:
        print("FAIL:\n", e.stderr)

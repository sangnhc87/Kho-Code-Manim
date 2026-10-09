import re
from pathlib import Path

for file in Path('.github/workflows').glob('render-stat*.yml'):
    content = file.read_text()
    if 'git commit -m' in content and 'git push' in content:
        # replace `git push` with `git pull --rebase origin main && git push`
        # But wait, we should do it safely.
        content = content.replace('git push', 'git pull --rebase origin main\n          git push')
        # deduplicate in case it was already there
        content = content.replace('git pull --rebase origin main\n          git pull --rebase origin main\n          git push', 'git pull --rebase origin main\n          git push')
        file.write_text(content)

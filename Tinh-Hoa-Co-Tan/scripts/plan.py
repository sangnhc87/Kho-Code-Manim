#!/usr/bin/env python3
"""Ma trận GitHub Actions: latest | all | unpublished | ep-0001,ep-0002 | range:1-12 | new:ep-0007,ep-0008."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ids = sorted(p.stem for p in (ROOT / 'episodes').glob('ep-*.json'))
arg = (sys.argv[1] if len(sys.argv) > 1 else 'latest').strip()
if not ids:
    raise SystemExit('Chưa có tập nào trong episodes/')
if arg == 'latest':
    pick = [ids[-1]]
elif arg == 'all':
    pick = ids
elif arg == 'unpublished':
    hist_path = ROOT.parent / 'youtube_uploaded_history.json'
    hist = json.loads(hist_path.read_text(encoding='utf-8')) if hist_path.exists() else {}
    pick = [i for i in ids if f'cotan3_short_{i}' not in hist]  # kênh hiện chỉ đăng Shorts
elif arg.startswith('range:'):
    a, b = arg[6:].split('-', 1)
    pick = [f'ep-{n:04d}' for n in range(int(a), int(b) + 1)]
elif arg.startswith('new:'):
    pick = [x for x in arg[4:].split(',') if x]
else:
    pick = [x.strip() for x in arg.split(',') if x.strip()]
pick = list(dict.fromkeys(pick))
missing = [i for i in pick if i not in ids]
if missing or not pick:
    raise SystemExit(f'Lựa chọn không hợp lệ: {missing or arg}')
if len(pick) > 64:
    raise SystemExit('Tối đa 64 tập mỗi lần chạy; hãy dùng range:')
print(json.dumps({'include': [{'episode': i} for i in pick]}, separators=(',', ':')))

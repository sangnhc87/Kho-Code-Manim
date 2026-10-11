#!/usr/bin/env python3
"""Gộp cache chessdb khi xung đột git: hợp hai từ điển FEN -> phản hồi.

    python Tinh-Hoa-Co-Tan/scripts/merge_cdb.py <file.json> [...]   (file đang có dấu xung đột)
Lấy bản 'ours' và 'theirs' từ git index (stage 2, 3) rồi ghi bản hợp nhất.
"""
import json
import subprocess
import sys


def stage(path, n):
    try:
        return json.loads(subprocess.check_output(['git', 'show', f':{n}:{path}'], text=True))
    except subprocess.CalledProcessError:
        return {}


if len(sys.argv) > 2 and sys.argv[1] == '--dir':
    # Gộp một thư mục cache khác (ví dụ của tiến trình chạy song song) vào data/cdb.
    from pathlib import Path
    dst_dir = Path(__file__).resolve().parents[1] / 'data' / 'cdb'
    for src in Path(sys.argv[2]).glob('*.json'):
        dst = dst_dir / src.name
        merged = {**json.loads(src.read_text(encoding='utf-8')),
                  **(json.loads(dst.read_text(encoding='utf-8')) if dst.exists() else {})}
        dst.write_text(json.dumps(merged, ensure_ascii=False, sort_keys=True, indent=0) + '\n', encoding='utf-8')
    sys.exit(0)

for path in sys.argv[1:]:
    merged = {**stage(path, 2), **stage(path, 3)}
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(merged, ensure_ascii=False, sort_keys=True, indent=0) + '\n')
    subprocess.check_call(['git', 'add', path])
    print('gộp', path, len(merged))

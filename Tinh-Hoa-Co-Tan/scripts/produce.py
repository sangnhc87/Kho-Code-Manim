#!/usr/bin/env python3
"""Dựng MP4 cho một tập: python scripts/produce.py --episode ep-0001 [--quality full] [--voice edge]."""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.typst_cards import make_cards  # noqa: E402
from src.voice import generate_voice  # noqa: E402
from xq.validate import validate_episode  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--episode', required=True)
    p.add_argument('--quality', choices=['preview', 'full'], default='preview')
    p.add_argument('--voice', choices=['edge', 'zalo', 'mock'], default='edge')
    p.add_argument('--skip-render', action='store_true')
    args = p.parse_args()
    path = ROOT / 'episodes' / f'{args.episode}.json'
    if not path.is_file():
        raise SystemExit(f'Không có tập {path}')
    data = json.loads(path.read_text(encoding='utf-8'))
    validate_episode(data)
    out = ROOT / 'output' / args.episode
    out.mkdir(parents=True, exist_ok=True)
    if args.skip_render:
        print(f'Hợp lệ: {args.episode} – {len(data["beats"])} phân đoạn, '
              f'{sum(len(b["steps"]) for b in data["beats"])} câu thoại')
        return
    timing = generate_voice(data, out / 'voice', args.voice)
    make_cards(data, out / 'cards')
    env = os.environ.copy()
    env['XIANGQI_EPISODE'] = str(path)
    env['XIANGQI_OUTPUT'] = str(out)
    env['PYTHONPATH'] = str(ROOT)
    quality = ['-r', '1920,1080', '--fps', '30'] if args.quality == 'full' else ['-r', '854,480', '--fps', '15']
    cmd = [sys.executable, '-m', 'manim', *quality, '--disable_caching', str(ROOT / 'src' / 'scene.py'),
           'XiangqiLesson', '--media_dir', str(out / 'media'), '-o', args.episode]
    subprocess.run(cmd, env=env, check=True, cwd=ROOT)
    found = list((out / 'media').rglob(args.episode + '.mp4'))
    if not found:
        raise RuntimeError('Manim không xuất được video')
    final = out / f'{args.episode}.mp4'
    shutil.copy2(found[0], final)
    total = sum(c['seconds'] for clips in timing for c in clips)
    print(f'OUTPUT {final} | lời đọc ~{total / 60:.1f} phút')


if __name__ == '__main__':
    main()

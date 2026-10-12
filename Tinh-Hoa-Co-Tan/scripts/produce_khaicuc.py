#!/usr/bin/env python3
"""Dựng video khai cục dài theo chương.

python scripts/produce_khaicuc.py --episode kc-0001 --check            # kiểm tra kịch bản
python scripts/produce_khaicuc.py --episode kc-0001 --matrix           # ma trận chương cho Actions
python scripts/produce_khaicuc.py --episode kc-0001 --chapter 2 [--quality full]   # render 1 chương
python scripts/produce_khaicuc.py --episode kc-0001 --concat DIR       # ghép chương + mô tả có mốc chương
"""
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
from src.voice import duration, generate_voice  # noqa: E402
from xq.board import Position  # noqa: E402


def load(ep):
    path = ROOT / 'khaicuc' / 'episodes' / f'{ep}.json'
    if not path.is_file():
        raise SystemExit(f'Không có {path}')
    return path, json.loads(path.read_text(encoding='utf-8'))


def check(data):
    n = 0
    for ci, ch in enumerate(data['chapters']):
        for b in ch['beats']:
            if not b.get('steps'):
                raise ValueError(f'Chương {ci + 1}: phân đoạn {b.get("label")} không có lời')
            pos = Position.from_fen(b['fen']) if b.get('fen') else None
            for s in b['steps']:
                if not s.get('say', '').strip():
                    raise ValueError(f'Chương {ci + 1}: thiếu lời đọc')
                if s.get('move'):
                    pos = pos.play(s['move'])   # báo lỗi nếu nước sai luật
                    n += 1
    print(f'Hợp lệ: {data["id"]} – {len(data["chapters"])} chương, {n} nước đi, ước tính {data["est_minutes"]} phút')


def render_chapter(ep, path, data, ci, quality, voice):
    out = ROOT / 'output' / ep
    out.mkdir(parents=True, exist_ok=True)
    chapter = data['chapters'][ci]
    if ci in (0, len(data['chapters']) - 1):
        make_cards(data, out / 'cards')
    timing = generate_voice({'beats': chapter['beats']}, out / f'voice_{ci}', voice)
    env = os.environ.copy()
    env.update(KC_EPISODE=str(path), KC_CHAPTER=str(ci), KC_OUTPUT=str(out), PYTHONPATH=str(ROOT))
    q = ['-r', '1920,1080', '--fps', '30'] if quality == 'full' else ['-r', '854,480', '--fps', '15']
    name = f'{ep}_c{ci}'
    subprocess.run([sys.executable, '-m', 'manim', *q, '--disable_caching', str(ROOT / 'src' / 'khaicuc_scene.py'),
                    'KhaiCucChapter', '--media_dir', str(out / 'media'), '-o', name], env=env, check=True, cwd=ROOT)
    found = list((out / 'media').rglob(name + '.mp4'))
    if not found:
        raise RuntimeError('Manim không xuất được video')
    final = out / f'{name}.mp4'
    shutil.copy2(found[0], final)
    secs = duration(final)
    (out / f'{name}.json').write_text(json.dumps({'chapter': ci, 'title': chapter['title'], 'seconds': secs}), encoding='utf-8')
    print(f'OUTPUT {final} | {secs / 60:.1f} phút')


def stamp(sec):
    h, r = divmod(int(sec), 3600)
    m, s = divmod(r, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


def concat(ep, data, folder):
    folder = Path(folder)
    n = len(data['chapters'])
    parts = [folder / f'{ep}_c{i}.mp4' for i in range(n)]
    missing = [str(p) for p in parts if not p.exists()]
    if missing:
        raise SystemExit(f'Thiếu chương: {missing}')
    listing = folder / 'list.txt'
    listing.write_text(''.join(f"file '{p.resolve()}'\n" for p in parts), encoding='utf-8')
    final = folder / f'{ep}.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(listing), '-c', 'copy', str(final)], check=True)
    t, lines = 0.0, []
    for i in range(n):
        info = json.loads((folder / f'{ep}_c{i}.json').read_text(encoding='utf-8'))
        lines.append(f'{stamp(t)} {info["title"]}')
        t += info['seconds']
    if lines and not lines[0].startswith('0:00'):
        lines[0] = '0:00' + lines[0][len(lines[0].split()[0]):]
    desc = (f'{data["title"]}\n\nPhân tích khai cục từng nước, có điểm đánh giá của máy Pikafish, ý đồ hai bên và khẩu quyết.\n\n'
            'MỤC LỤC\n' + '\n'.join(lines) +
            '\n\n☕ Ủng hộ kênh: VPBank 10389821115\n\n#cotuong #khaicuc #xiangqi #tinhhoacotan')
    (folder / 'yt_title.txt').write_text(data['youtube']['title'], encoding='utf-8')
    (folder / 'yt_desc.txt').write_text(desc, encoding='utf-8')
    (folder / 'yt_tags.txt').write_text(','.join(data['youtube']['tags']), encoding='utf-8')
    print(f'OUTPUT {final} | tổng {t / 60:.1f} phút')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--episode', required=True)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--matrix', action='store_true')
    ap.add_argument('--chapter', type=int)
    ap.add_argument('--concat')
    ap.add_argument('--quality', choices=['preview', 'full'], default='preview')
    ap.add_argument('--voice', default='edge')
    a = ap.parse_args()
    path, data = load(a.episode)
    if a.matrix:
        print(json.dumps({'include': [{'chapter': i} for i in range(len(data['chapters']))]}, separators=(',', ':')))
    elif a.check:
        check(data)
    elif a.concat:
        concat(a.episode, data, a.concat)
    elif a.chapter is not None:
        render_chapter(a.episode, path, data, a.chapter, a.quality, a.voice)
    else:
        raise SystemExit('Chọn --check, --matrix, --chapter hoặc --concat')


if __name__ == '__main__':
    main()

"""After rendering: subtitles + YouTube description (with chapters) from the
real beat start times recorded by the scene.

python scripts/finalize.py --ep int01
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import episode, voice  # noqa: E402

AUTHOR_INFO = '''👨‍🏫 Giảng viên: Thầy Nguyễn Văn Sang
📌 Dự án: Toán Trực Quan Bằng Hoạt Họa Manim & Typst
🔔 Đăng ký kênh để theo dõi trọn bộ series 36 tập Nguyên Hàm – Tích Phân – Ứng Dụng!'''


def series_entry(n: int) -> dict:
    data = json.loads((ROOT / 'series_plan.json').read_text('utf-8'))
    return next(e for e in data['episodes'] if e['n'] == n)


def description(lesson, plan, starts) -> str:
    ep = lesson.EPISODE
    meta = series_entry(ep['number'])
    chapters = voice.chapters(plan, starts)
    lines = [f"{ep['code']} – {ep['title']}: {ep['subtitle']} | {meta['tag']}",
             'Series: Nguyên Hàm – Tích Phân – Ứng Dụng Chuyên Sâu (36 tập) · Toán 12 (GDPT 2018)', '',
             '⏱️ NỘI DUNG']
    lines += [f'{voice.stamp(t)} {name}' for t, name in chapters]
    lines += ['', '📝 BÀI TẬP TỰ LUYỆN']
    lines += [f'{i}) {q}  →  Đáp số: {a}' for i, (q, a) in enumerate(lesson.EXERCISES, 1)]
    if ep.get('next_code'):
        lines += ['', f"▶️ Tập tiếp theo: {ep['next_code']} – {ep['next_title']}"]
    lines += ['', AUTHOR_INFO, '',
              '#NguyenHam #TichPhan #Toan12 #OnThiTotNghiep #ThayNguyenVanSang #Manim']
    return '\n'.join(lines)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ep', default='int01')
    a = ap.parse_args()
    lesson, p = episode.load(a.ep), episode.paths(a.ep)
    plan = json.loads(p['plan'].read_text('utf-8'))
    if p['timeline'].exists():
        tl = json.loads(p['timeline'].read_text('utf-8'))
        starts = tl['starts']
        print('timeline from render, overruns:', tl.get('overruns'))
    else:  # planned timing (exact unless a beat overran)
        starts, t = [], 0.0
        for b in plan['beats']:
            starts.append(t)
            t += b['duration']
        print('timeline from plan (no render yet)')
    if len(starts) != len(plan['beats']):
        raise SystemExit('timeline/plan mismatch: re-render after prepare_voice')
    p['srt'].write_text(voice.build_srt(plan, starts), encoding='utf-8')
    p['youtube'].parent.mkdir(parents=True, exist_ok=True)
    text = description(lesson, plan, starts)
    p['youtube'].write_text(text, encoding='utf-8')
    print(text)
    print(f"{lesson.EPISODE['code']}_FINALIZE_OK srt={p['srt'].name} desc={p['youtube'].name}")

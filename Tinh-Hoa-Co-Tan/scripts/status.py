#!/usr/bin/env python3
"""Tiến độ series: python scripts/status.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_episodes import next_topics  # noqa: E402

topics = json.loads((ROOT / 'curriculum' / 'topics.json').read_text(encoding='utf-8'))['topics']
catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
hist_path = ROOT.parent / 'youtube_uploaded_history.json'
hist = json.loads(hist_path.read_text(encoding='utf-8')) if hist_path.exists() else {}

eps = catalog['episodes']
video = [e for e in eps if f"cotan3_ep-{e['ep']:04d}" in hist]
short = [e for e in eps if f"cotan3_short_ep-{e['ep']:04d}" in hist]
print(f'Giáo trình: {len(topics)} chủ đề, {sum(t["episodes"] for t in topics)} tập dự kiến')
print(f'Đã dựng: {len(eps)} tập | đã đăng video: {len(video)} | đã đăng Short: {len(short)}')
missing = [f"ep-{e['ep']:04d}" for e in eps if e not in video]
if missing:
    print('Chưa đăng video:', ', '.join(missing))
print('Chủ đề kế tiếp:', ', '.join(t['id'] for t in next_topics(topics, catalog, 6)))
for e in eps[-5:]:
    key = f"cotan3_ep-{e['ep']:04d}"
    print(f"  ep-{e['ep']:04d} {e['title'][:60]:60} {hist.get(key, {}).get('url', '')}")

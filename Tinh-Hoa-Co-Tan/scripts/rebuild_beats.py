#!/usr/bin/env python3
"""Sinh lại kịch bản (beats) từ phân tích đã lưu, dùng lời bình mới nhất. Không gọi mạng.

    python scripts/rebuild_beats.py ep-0009 ep-0010      # các tập chỉ định
    python scripts/rebuild_beats.py --unpublished         # mọi tập chưa đăng YouTube
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_episodes import youtube_meta  # noqa: E402
from xq.commentary import build_episode  # noqa: E402
from xq.validate import validate_episode  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('episodes', nargs='*')
    ap.add_argument('--unpublished', action='store_true')
    args = ap.parse_args()
    topics = {t['id']: t for t in json.loads((ROOT / 'curriculum' / 'topics.json').read_text(encoding='utf-8'))['topics']}
    ids = list(args.episodes)
    if args.unpublished:
        hist_path = ROOT.parent / 'youtube_uploaded_history.json'
        hist = json.loads(hist_path.read_text(encoding='utf-8')) if hist_path.exists() else {}
        ids += [p.stem for p in sorted((ROOT / 'episodes').glob('ep-*.json')) if f'cotan3_{p.stem}' not in hist]
    for ep_id in dict.fromkeys(ids):
        path = ROOT / 'episodes' / f'{ep_id}.json'
        data = json.loads(path.read_text(encoding='utf-8'))
        topic = data.get('topic_data') or topics[data['topic']]
        data['beats'] = build_episode(data['analysis'], topic, data['number'])
        if 'classic' not in data:  # tập từ sách giữ nguyên mô tả có ghi nguồn
            data['youtube'] = youtube_meta(data['number'], topic, data['analysis'], data['title'])
        validate_episode(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print('dựng lại', ep_id)


if __name__ == '__main__':
    main()

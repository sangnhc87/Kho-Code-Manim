#!/usr/bin/env python3
"""Khôi phục youtube_uploaded_history.json từ log GitHub Actions (cần gh CLI).

    python Tinh-Hoa-Co-Tan/scripts/recover_history.py <run_id> [<run_id> ...]
Đọc log từng job render (ep-XXXX), lấy Video ID của video chính và Short.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = 'sangnhc87/Kho-Code-Manim'
HIST = Path(__file__).resolve().parents[2] / 'youtube_uploaded_history.json'


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True)


hist = json.loads(HIST.read_text(encoding='utf-8'))
added = 0
for run in sys.argv[1:]:
    jobs = json.loads(gh('run', 'view', run, '-R', REPO, '--json', 'jobs'))['jobs']
    for job in jobs:
        m = re.search(r'\((ep-\d{4})\)', job['name'])
        if not m:
            continue
        ep = m.group(1)
        try:
            log = gh('api', f'repos/{REPO}/actions/jobs/{job["databaseId"]}/logs')
        except subprocess.CalledProcessError:
            continue
        titles = re.findall(r'Tiêu đề: (.+)', log)
        ids = re.findall(r'Video ID:\s*([A-Za-z0-9_-]{11})', log)
        for title, vid in zip(titles, ids):
            key = f'cotan3_short_{ep}' if '#Shorts' in title else f'cotan3_{ep}'
            if key in hist:
                continue
            hist[key] = {'title': title.strip(), 'video_id': vid, 'url': f'https://youtu.be/{vid}',
                         'file': f'Tinh-Hoa-Co-Tan/output/{ep}/{ep}{"_short" if "Shorts" in title else ""}.mp4',
                         'uploaded_at': job.get('completedAt', '')[:19].replace('T', ' ')}
            added += 1
            print('khôi phục', key, vid)
HIST.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('thêm', added, 'mục')

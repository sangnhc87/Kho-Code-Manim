"""Inspect a rendered episode: streams, resolution, duration vs plan, audio
loudness, and one still per part.
python scripts/qa_video.py --ep int01 --video X.mp4 --quality fullhd --voice on
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import episode  # noqa: E402

EXPECTED = {'preview': (854, 480), 'fullhd': (1920, 1080)}


def probe(video: Path) -> dict:
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                                   '-of', 'json', str(video)], text=True)
    return json.loads(out)


def mean_volume(video: Path) -> float:
    proc = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(video), '-af', 'volumedetect',
                           '-vn', '-f', 'null', '-'], capture_output=True, text=True)
    m = re.search(r'mean_volume:\s*(-?[\d.]+) dB', proc.stderr)
    return float(m.group(1)) if m else -99.0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ep', default='int01')
    ap.add_argument('--video', required=True)
    ap.add_argument('--quality', choices=list(EXPECTED), default='preview')
    ap.add_argument('--voice', choices=['on', 'off'], default='off')
    a = ap.parse_args()
    lesson, p = episode.load(a.ep), episode.paths(a.ep)
    video = Path(a.video)
    info = probe(video)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = [s for s in info['streams'] if s['codec_type'] == 'audio']
    dur = float(info['format']['duration'])
    plan = json.loads(p['plan'].read_text('utf-8'))
    tl = json.loads(p['timeline'].read_text('utf-8')) if p['timeline'].exists() else {}
    report = {'video': str(video), 'width': v['width'], 'height': v['height'], 'duration': round(dur, 2),
              'planned': plan['total_duration'], 'audio_streams': len(audio),
              'overruns': tl.get('overruns', [])}
    assert (v['width'], v['height']) == EXPECTED[a.quality], f'resolution {v["width"]}x{v["height"]}'
    assert abs(dur - tl.get('total', plan['total_duration'])) < 2.0, 'video length differs from timeline'
    if a.voice == 'on':
        assert audio, 'voice=on but no audio stream'
        report['mean_volume_db'] = mean_volume(video)
        assert report['mean_volume_db'] > -40, 'audio is (almost) silent'
    out = p['artifacts']
    out.mkdir(parents=True, exist_ok=True)
    starts = tl.get('starts') or [sum(b['duration'] for b in plan['beats'][:i])
                                  for i in range(len(plan['beats']))]
    for i, b in enumerate(plan['beats']):  # one still per beat, near its end
        t = starts[i] + b['duration'] * 0.85
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', str(video), '-frames:v', '1',
                        '-vf', 'scale=960:-2', str(out / f'{i + 1:02d}_{b["id"]}.jpg')], check=True)
    (out / 'qa_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('QA_OK', json.dumps(report, ensure_ascii=False))

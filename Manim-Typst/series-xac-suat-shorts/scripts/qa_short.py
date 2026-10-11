"""Check a rendered Short: vertical size, ≤ 3 min, audio present, one still per beat.
python scripts/qa_short.py --short xss001 --video X.mp4 --quality full --voice on
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import shortlib  # noqa: E402

EXPECTED = {'preview': (540, 960), 'full': (1080, 1920)}


def mean_volume(video: Path) -> float:
    proc = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(video), '-af', 'volumedetect', '-vn', '-f', 'null',
                           '-'], capture_output=True, text=True)
    m = re.search(r'mean_volume:\s*(-?[\d.]+) dB', proc.stderr)
    return float(m.group(1)) if m else -99.0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--short', default='xss001')
    ap.add_argument('--video', required=True)
    ap.add_argument('--quality', choices=list(EXPECTED), default='preview')
    ap.add_argument('--voice', choices=['on', 'off'], default='off')
    a = ap.parse_args()
    p = shortlib.paths(a.short)
    video = Path(a.video)
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of',
                                               'json', str(video)], text=True))
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    audio = [s for s in info['streams'] if s['codec_type'] == 'audio']
    dur = float(info['format']['duration'])
    plan = json.loads(p['plan'].read_text('utf-8'))
    tl = json.loads(p['timeline'].read_text('utf-8')) if p['timeline'].exists() else {}
    report = {'video': str(video), 'size': f"{v['width']}x{v['height']}", 'duration': round(dur, 2),
              'planned': plan['total_duration'], 'overruns': tl.get('overruns', [])}
    assert (v['width'], v['height']) == EXPECTED[a.quality], report['size']
    assert dur <= 180.0, f'{dur:.1f}s is longer than a Short allows'
    if a.voice == 'on':
        assert audio, 'voice=on but no audio stream'
        report['mean_volume_db'] = mean_volume(video)
        assert report['mean_volume_db'] > -40, 'audio is (almost) silent'
    out = p['artifacts']
    out.mkdir(parents=True, exist_ok=True)
    starts = tl.get('starts') or [sum(b['duration'] for b in plan['beats'][:i]) for i in range(len(plan['beats']))]
    for i, b in enumerate(plan['beats']):
        t = min(dur - .1, starts[i] + b['duration'] * .9)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', str(video), '-frames:v', '1',
                        '-vf', 'scale=540:-2', str(out / f'{i + 1:02d}_{b["id"]}.jpg')], check=True)
    print('QA_OK', json.dumps(report, ensure_ascii=False))

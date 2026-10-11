"""Subtitles + YouTube title/description/tags for one Short: python scripts/finalize.py --short xss001"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import shortlib, voice  # noqa: E402

LEVEL = {'L1': 'Mở đầu', 'L2': 'Cơ bản', 'L3': 'Thông hiểu', 'L4': 'Vận dụng', 'L5': 'Khó', 'L6': 'Rất khó'}
TAGS = 'shorts,xác suất,toán 10,toán 11,toán 12,ôn thi tốt nghiệp,thử thách toán,Thầy Nguyễn Văn Sang'


def metadata(n: int) -> dict:
    e = shortlib.plan_entry(n)
    title = f"Xác suất #{n:03d} · {e['title']} – bạn giải được không? #Shorts"
    desc = '\n'.join([
        f"🎯 Thử thách xác suất #{n:03d} · Mức {LEVEL[e['level']]}",
        '',
        f"❓ {e['problem']}",
        '',
        'Dừng video, tự giải rồi xem lời giải bằng hình động. Đáp án ở cuối video.',
        'Mọi đáp án trong series đều được kiểm tra lại bằng máy tính (liệt kê, phân số chính xác, mô phỏng).',
        '',
        '📚 Series "Xác suất 3 phút": 120 thử thách từ dễ đến rất khó: xác suất cổ điển, quy tắc cộng – nhân, '
        'xác suất có điều kiện, toàn phần, Bayes.',
        '👨‍🏫 Thầy Nguyễn Văn Sang',
        '',
        '#Shorts #XacSuat #Toan10 #Toan11 #Toan12 #OnThiTotNghiep',
    ])
    return {'title': title, 'description': desc, 'tags': TAGS}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--short', default='xss001')
    a = ap.parse_args()
    code = shortlib.normalise(a.short)
    p = shortlib.paths(code)
    plan = json.loads(p['plan'].read_text('utf-8'))
    tl = json.loads(p['timeline'].read_text('utf-8')) if p['timeline'].exists() else {}
    starts = tl.get('starts') or [sum(b['duration'] for b in plan['beats'][:i]) for i in range(len(plan['beats']))]
    p['srt'].parent.mkdir(parents=True, exist_ok=True)
    p['srt'].write_text(voice.build_srt(plan, starts), encoding='utf-8')
    meta = metadata(int(code[3:]))
    assert len(meta['title']) <= 100, meta['title']
    p['youtube'].write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{code.upper()}_FINALIZE_OK {meta["title"]}')

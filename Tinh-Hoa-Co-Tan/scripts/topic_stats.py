#!/usr/bin/env python3
"""Khảo sát bảng tra chessdb cho từng loại thế tàn: tỉ lệ Thắng/Hòa và độ dài thắng.

Dùng để viết phần lý thuyết dựa trên số liệu, ví dụ:
    python scripts/topic_stats.py NA:A P:- N:AA --n 60
(vật chất Đỏ:Đen, '-' là chỉ còn Tướng). Kết quả ghi vào data/topic_stats.json.
"""
import argparse
import json
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq import cdb  # noqa: E402
from xq.sample import random_position  # noqa: E402


def survey(red, black, n, rng):
    res = {'W': 0, 'D': 0, 'L': 0}
    dtms = []
    for _ in range(n):
        pos = random_position(red, black, turn='w', rng=rng)
        try:
            wdl, dtm = cdb.value(pos.fen())
        except cdb.CdbError as exc:
            print('  bỏ qua:', exc, flush=True)
            continue
        res[wdl] += 1
        if wdl == 'W':
            dtms.append(dtm)
    total = sum(res.values()) or 1
    out = {'n': total, **{k: round(v / total, 3) for k, v in res.items()}}
    if dtms:
        out['dtm_median'] = statistics.median(dtms)
        out['dtm_max_seen'] = max(dtms)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('classes', nargs='+')
    ap.add_argument('--n', type=int, default=60)
    ap.add_argument('--seed', type=int, default=1)
    args = ap.parse_args()
    path = ROOT / 'data' / 'topic_stats.json'
    data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    rng = random.Random(args.seed)
    for cls in args.classes:
        red, black = (s.replace('-', '') for s in cls.split(':'))
        data[cls] = survey(red, black, args.n, rng)
        print(cls, data[cls], flush=True)
        cdb.flush()
        path.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + '\n',
                        encoding='utf-8')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Nhập thế tàn cục từ kỳ phổ kinh điển (kho cộng đồng vietcotuong.com) và tra bảng chessdb.

    python scripts/import_classics.py end-games/Co-Tan-Thuc-Dung [end-games/...]

Chỉ lưu dữ kiện (FEN, biến của sách, kết quả sách, kết quả bảng tra) vào
curriculum/classics/<bộ sưu tập>.json; không sao chép lời bình gốc.
Nguồn: https://github.com/chasoft/community-xiangqi-games-database
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq import cdb  # noqa: E402
from xq.dpxq import parse, replay  # noqa: E402

REPO = 'chasoft/community-xiangqi-games-database'
RAW = f'https://raw.githubusercontent.com/{REPO}/main/data/'
OUT = ROOT / 'curriculum' / 'classics'
BOOK_RESULT = {'红胜': 'W', '红先胜': 'W', '胜': 'W', '和局': 'D', '和': 'D', '红先和': 'D', '黑胜': 'L', '红负': 'L'}


def fetch(url):
    ctx = cdb._SSL
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=30, context=ctx) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception:
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f'Không tải được {url}')


def list_collection(path):
    url = f'https://api.github.com/repos/{REPO}/contents/data/{urllib.parse.quote(path)}'
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github+json',
                                               **({'Authorization': f'Bearer {os.environ["GITHUB_TOKEN"]}'}
                                                  if os.environ.get('GITHUB_TOKEN') else {})})
    with urllib.request.urlopen(req, timeout=30, context=cdb._SSL) as r:
        items = json.load(r)
    return sorted(i['name'] for i in items if i['type'] == 'file' and not i['name'].endswith(('.json', '.md')))


def tablebase(fen):
    try:
        res = cdb.query(fen)
    except (cdb.CdbError, ValueError) as exc:
        return {'status': 'error', 'error': str(exc)[:120]}
    if res['status'] == 'mate':
        return {'status': 'mate'}
    if res['status'] != 'egtb':
        return {'status': res['status']}
    best = res['moves'][0]
    return {'status': 'egtb', 'wdl': best['wdl'], 'dtm': best['dtm'],
            'keep': sum(m['wdl'] == best['wdl'] for m in res['moves']), 'legal': len(res['moves'])}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for coll in sys.argv[1:]:
        name = coll.rstrip('/').split('/')[-1]
        out_path = OUT / f'{name}.json'
        data = json.loads(out_path.read_text(encoding='utf-8')) if out_path.exists() else {
            'source': f'https://github.com/{REPO}/tree/main/data/{coll}', 'collection': coll, 'items': {}}
        files = list_collection(coll)
        print(coll, len(files), 'thế')
        for i, f in enumerate(files):
            if f in data['items']:
                continue
            try:
                g = parse(fetch(RAW + urllib.parse.quote(f'{coll}/{f}')))
            except Exception as exc:
                print('  lỗi', f, exc)
                continue
            legal_book = len(replay(g['fen'], g['moves'])) - 1
            item = {'fen': g['fen'], 'title': g['title'], 'book_result': BOOK_RESULT.get(g['result'], g['result']),
                    'book_moves': g['moves'][:legal_book], 'pieces': g['fen'].split()[0].count('/') * 0 +
                    sum(c.isalpha() for c in g['fen'].split()[0]), 'tb': tablebase(g['fen'])}
            data['items'][f] = item
            if i % 10 == 0:
                print(f'  {i}/{len(files)} {f} {item["tb"]}', flush=True)
                cdb.flush()
                out_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        cdb.flush()
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        st = {}
        for it in data['items'].values():
            k = it['tb'].get('wdl', it['tb']['status'])
            st[k] = st.get(k, 0) + 1
        print(coll, 'xong:', st)


if __name__ == '__main__':
    main()

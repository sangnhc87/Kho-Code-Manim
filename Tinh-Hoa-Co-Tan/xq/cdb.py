"""Truy vấn Cơ sở dữ liệu đám mây chessdb.cn (bảng tra cờ tàn - EGTB, độ đo DTM).

Mỗi kết quả được lưu vào data/cdb/<vật chất>.json và commit cùng repo, nên
CI chỉ gọi mạng khi gặp thế cờ mới. Không cần chạy Pikafish hay engine nào.

Ý nghĩa ghi chú của chessdb: "W-M-0023" = bên đi thắng, chiếu bí sau 23 nước
nửa (ply) khi hai bên chơi tối ưu; "D-M-0000" = hòa; "L-M-0022" = thua.
"""
from __future__ import annotations

import json
import os
import re
import ssl
import time
import urllib.parse
import urllib.request
from pathlib import Path

from .board import Position

API = 'https://www.chessdb.cn/chessdb.php'
CACHE_DIR = Path(__file__).resolve().parents[1] / 'data' / 'cdb'
NOTE_RE = re.compile(r'\(([WDL])-M-(\d+)\)')
MIN_INTERVAL = float(os.getenv('CDB_INTERVAL', '0.35'))
_last_call = [0.0]
_mem: dict[str, dict] = {}

try:  # macOS Python thường thiếu chứng chỉ gốc; certifi khắc phục.
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL = None


class CdbError(RuntimeError):
    pass


def _cache_file(fen):
    pos = Position.from_fen(fen)
    key = pos.material('w') + '_' + pos.material('b')
    return CACHE_DIR / f'{key}.json'


def _load(path):
    key = str(path)
    if key not in _mem:
        _mem[key] = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    return _mem[key]


def flush():
    for key, data in _mem.items():
        path = Path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=0) + '\n',
                        encoding='utf-8')


def _fetch(fen):
    if os.getenv('CDB_OFFLINE') == '1':
        raise CdbError(f'Thiếu cache cho {fen} (CDB_OFFLINE=1)')
    params = urllib.parse.urlencode({'action': 'queryall', 'board': fen, 'egtbmetric': 'dtm',
                                     'showall': 1, 'learn': 0})
    last = None
    for attempt in range(6):
        wait = MIN_INTERVAL - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.time()
        try:
            req = urllib.request.Request(f'{API}?{params}',
                                         headers={'User-Agent': 'TinhHoaCoTan/3.0 (education)'})
            with urllib.request.urlopen(req, timeout=30, context=_SSL) as r:
                text = r.read().decode('utf-8', 'replace').strip().rstrip('\x00').strip()
            if text:
                return text
        except Exception as exc:  # mạng chập chờn: thử lại có giãn cách
            last = exc
        time.sleep(1.5 * (attempt + 1))
    raise CdbError(f'chessdb không trả lời cho {fen}: {last}')


def parse(text):
    if text in ('checkmate', 'stalemate'):
        return {'status': 'mate', 'moves': []}
    if text in ('invalid board', 'unknown'):
        return {'status': text.replace(' ', '_'), 'moves': []}
    moves = []
    for chunk in text.split('|'):
        item = dict(kv.split(':', 1) for kv in chunk.split(',') if ':' in kv)
        if 'move' not in item:
            continue
        m = NOTE_RE.search(item.get('note', ''))
        moves.append({'move': item['move'],
                      'score': int(item['score']) if item.get('score', '').lstrip('-').isdigit() else None,
                      'wdl': m.group(1) if m else None,
                      'dtm': int(m.group(2)) if m else None})
    egtb = bool(moves) and all(mv['wdl'] for mv in moves)
    return {'status': 'egtb' if egtb else 'book', 'moves': moves}


def query(fen):
    """Kết quả tất cả nước đi hợp lệ: [{'move','wdl','dtm','score'}], đã sắp tốt → xấu."""
    pos = Position.from_fen(fen)
    fen = pos.fen()
    path = _cache_file(fen)
    data = _load(path)
    if fen not in data or parse(data[fen])['status'] == 'book':
        # Thế cờ tàn đôi khi được trả về tạm thời chưa kèm nhãn bảng tra: hỏi lại.
        for _ in range(3):
            data[fen] = _fetch(fen)
            if parse(data[fen])['status'] != 'book':
                break
            time.sleep(2)
    res = parse(data[fen])
    if res['status'] == 'mate':
        return res
    legal = set(pos.legal_moves())
    got = {m['move'] for m in res['moves']}
    if res['status'] == 'egtb' and got != legal:
        raise CdbError(f'Danh sách nước của chessdb khác luật ({fen}): '
                       f'thiếu {sorted(legal - got)}, thừa {sorted(got - legal)}')
    return res


def value(fen):
    """(kết quả cho bên đi: 'W'/'D'/'L', số nước nửa đến chiếu bí) của một thế."""
    res = query(fen)
    if res['status'] == 'mate':
        return 'L', 0
    if res['status'] != 'egtb':
        raise CdbError(f'Thế {fen} ngoài bảng tra cờ tàn ({res["status"]})')
    best = res['moves'][0]
    return best['wdl'], best['dtm']

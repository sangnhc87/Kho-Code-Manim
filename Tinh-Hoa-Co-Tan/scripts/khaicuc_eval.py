#!/usr/bin/env python3
"""Chấm điểm bằng Pikafish mọi thế trong cây khai cục (chạy trên GitHub Actions).

python scripts/khaicuc_eval.py --opening thuanphao --engine ./pikafish --movetime 400
-> khaicuc/eval/<slug>.json = {fen: {"turn", "depth", "lines": [{"cp"|"mate", "pv": [...]}]}}
Điểm luôn tính theo góc nhìn của ĐỎ (dương = Đỏ hơn). 'mate' dương = Đỏ chiếu bí sau n nước.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from xq.board import Position  # noqa: E402

INFO = re.compile(r'info depth (\d+).*? multipv (\d+) score (cp|mate) (-?\d+).*? pv (.+)$')


class Engine:
    def __init__(self, path, threads, hash_mb, multipv):
        self.p = subprocess.Popen([path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1,
                                  cwd=str(Path(path).resolve().parent))
        self.send('uci')
        self.wait('uciok')
        self.send(f'setoption name Threads value {threads}')
        self.send(f'setoption name Hash value {hash_mb}')
        self.send(f'setoption name MultiPV value {multipv}')
        self.send('isready')
        self.wait('readyok')

    def send(self, s):
        self.p.stdin.write(s + '\n')
        self.p.stdin.flush()

    def wait(self, token, collect=None):
        for line in self.p.stdout:
            if collect is not None:
                collect.append(line)
            if line.startswith(token):
                return

    def analyse(self, fen, movetime):
        self.send(f'position fen {fen}')
        self.send(f'go movetime {movetime}')
        lines = []
        self.wait('bestmove', lines)
        best = {}
        for ln in lines:
            m = INFO.search(ln)
            if m:
                depth, mpv, kind, val, pv = m.groups()
                best[int(mpv)] = (int(depth), kind, int(val), pv.split())
        return [best[k] for k in sorted(best)]

    def close(self):
        try:
            self.send('quit')
            self.p.wait(timeout=5)
        except Exception:
            self.p.kill()


def walk(node, pos, out):
    out.append(pos)
    for c in node.get('c', []):
        walk(c, pos.play(c['m']), out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--opening', required=True)
    ap.add_argument('--engine', required=True)
    ap.add_argument('--movetime', type=int, default=400)
    ap.add_argument('--threads', type=int, default=2)
    ap.add_argument('--hash', type=int, default=256)
    ap.add_argument('--multipv', type=int, default=3)
    a = ap.parse_args()
    data = json.loads((ROOT / 'khaicuc' / 'openings' / f'{a.opening}.json').read_text(encoding='utf-8'))
    start = Position.from_fen(data['fen'])
    positions = []
    walk(data['tree'], start, positions)
    seen, uniq = set(), []
    for p in positions:
        if p.fen() not in seen:
            seen.add(p.fen())
            uniq.append(p)
    eng = Engine(a.engine, a.threads, a.hash, a.multipv)
    out, t0 = {}, time.time()
    for i, pos in enumerate(uniq, 1):
        fen = pos.fen()
        lines = []
        for depth, kind, val, pv in eng.analyse(fen + ' - - 0 1', a.movetime):
            sign = 1 if pos.turn == 'w' else -1
            lines.append({kind: val * sign, 'pv': pv[:8]})
            out_depth = depth
        out[fen] = {'turn': pos.turn, 'depth': out_depth if lines else 0, 'lines': lines}
        if i % 50 == 0:
            print(f'{a.opening}: {i}/{len(uniq)} thế, {time.time() - t0:.0f}s', flush=True)
    eng.close()
    dest = ROOT / 'khaicuc' / 'eval'
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f'{a.opening}.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Xong {a.opening}: {len(out)} thế, {time.time() - t0:.0f}s')


if __name__ == '__main__':
    main()

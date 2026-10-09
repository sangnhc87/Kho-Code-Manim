#!/usr/bin/env python3
"""Optional Pikafish single-position UCI analysis (NOT an endgame proof).
Usage: python scripts/check_pikafish.py --episode tap-0001 --engine /path/to/pikafish
"""
import argparse
import json
import subprocess
import sys
import time
import queue
import threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.core import read_episode


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--episode',required=True)
    p.add_argument('--engine',required=True)
    p.add_argument('--depth',type=int,default=22)
    p.add_argument('--timeout',type=float,default=90)
    a=p.parse_args()
    if a.depth<1 or a.depth>100: raise SystemExit('Depth must be 1..100')
    data=read_episode(ROOT/'episodes'/f'{a.episode}.json')
    # Only check the initial position; a single engine PV is no game-theoretic proof.
    fen=data['fen']
    if len(fen.split())==2:
        fen+=' - - 0 1'
    with subprocess.Popen([a.engine],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL,text=True,bufsize=1) as proc:
        incoming=queue.Queue()
        def reader():
            for line in proc.stdout:
                incoming.put(line.strip())
            incoming.put(None)
        threading.Thread(target=reader,daemon=True).start()
        def send(cmd):
            proc.stdin.write(cmd+'\n'); proc.stdin.flush()
        def receive_until(prefixes, timeout):
            deadline=time.monotonic()+timeout
            lines=[]
            while time.monotonic()<deadline:
                try:
                    line=incoming.get(timeout=max(.01,deadline-time.monotonic()))
                except queue.Empty:
                    break
                if line is None: raise RuntimeError('Engine process exited')
                if not line: continue
                lines.append(line)
                if any(line.startswith(prefix) for prefix in prefixes):
                    return lines
            raise TimeoutError('Engine response timeout waiting for '+str(prefixes))
        send('uci'); receive_until(['uciok'],a.timeout)
        send('isready'); receive_until(['readyok'],a.timeout)
        send('setoption name Threads value 2')
        send('position fen '+fen)
        send('go depth '+str(a.depth))
        lines=receive_until(['bestmove'],a.timeout)
        send('quit')
    best=next((line.split()[1] for line in reversed(lines) if line.startswith('bestmove')),None)
    info=next((line for line in reversed(lines) if ' score ' in line),None)
    report={'episode':a.episode,'engine_depth':a.depth,'fen':fen,'bestmove':best,
            'final_info':info,'note':'Chỉ là gợi ý engine ở thế mở đầu; KHÔNG chứng minh cả biến thắng.'}
    out=ROOT/'output'/a.episode
    out.mkdir(parents=True,exist_ok=True)
    (out/'engine_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': main()

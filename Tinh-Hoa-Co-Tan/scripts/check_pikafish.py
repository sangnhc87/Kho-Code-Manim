#!/usr/bin/env python3
"""Check EVERY illustrated move using Pikafish; analyse the initial position.
Legality and a finite-depth PV do not prove a forced win or mate distance.
Pass --eval-file for the NNUE supplied with the SAME engine release.
"""
import argparse
import hashlib
import json
import queue
import re
import subprocess
import sys
import threading
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.core import Board, read_episode
from src.engine_coords import board_fen, flip_move


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episode', required=True)
    parser.add_argument('--engine', required=True)
    parser.add_argument('--eval-file', required=True)
    parser.add_argument('--depth', type=int, default=22)
    parser.add_argument('--timeout', type=float, default=90)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not 1 <= args.depth <= 100 or args.timeout <= 0:
        parser.error('Depth must be 1..100 and timeout must be positive')
    path = ROOT / 'episodes' / f'{args.episode}.json'
    data = read_episode(path)
    engine, network = Path(args.engine).resolve(), Path(args.eval_file).resolve()
    incoming, transcript = queue.Queue(), []
    proc = subprocess.Popen([str(engine)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, bufsize=1)
    def reader():
        for line in proc.stdout:
            incoming.put(line.strip())
        incoming.put(None)
    threading.Thread(target=reader, daemon=True).start()
    def send(command):
        transcript.append('> ' + command.replace(str(network), network.name))
        proc.stdin.write(command + '\n')
        proc.stdin.flush()
    def receive_until(prefix):
        deadline, lines = time.monotonic() + args.timeout, []
        while time.monotonic() < deadline:
            try:
                line = incoming.get(timeout=max(.01, deadline-time.monotonic()))
            except queue.Empty:
                break
            if line is None:
                raise RuntimeError('Pikafish exited: ' + '\n'.join(lines[-8:]))
            transcript.append(line.replace(str(network), network.name))
            lines.append(line)
            if 'CRITICAL ERROR' in line or 'info string ERROR:' in line:
                raise RuntimeError(line)
            if line.startswith(prefix):
                return lines
        raise TimeoutError('Pikafish timeout waiting for ' + prefix)
    try:
        send('uci')
        handshake = receive_until('uciok')
        identity = next(line.removeprefix('id name ') for line in handshake
                        if line.startswith('id name '))
        send('setoption name EvalFile value ' + str(network))
        send('setoption name Threads value 2')
        send('isready')
        receive_until('readyok')
        checks = []
        for beat_index, beat in enumerate(data['beats'], 1):
            board = Board.fen(beat['fen'])
            for move_index, move in enumerate(beat.get('moves', []), 1):
                fen, uci = board_fen(board), flip_move(move)
                send('position fen ' + fen)
                send('go perft 1')
                lines = receive_until('Nodes searched:')
                legal = sorted(match.group(1) for line in lines
                               if (match := re.fullmatch(r'([a-i][0-9][a-i][0-9]): 1', line)))
                if uci not in legal:
                    raise ValueError(f'Beat {beat_index}, move {move_index}: '
                                     f'{move} ({uci} UCI) illegal in Pikafish')
                checks.append({'beat': beat_index, 'move_index': move_index, 'fen': fen,
                               'display_move': move, 'uci_move': uci, 'legal_uci_moves': legal})
                board.play(move[:2], move[2:])
        send('position fen ' + board_fen(Board.fen(data['fen'])))
        send('go depth ' + str(args.depth))
        analysis = receive_until('bestmove')
        best = analysis[-1].split()[1]
        info = next((line for line in reversed(analysis) if ' score ' in line), None)
        send('quit')
        proc.wait(timeout=10)
        if proc.returncode:
            raise RuntimeError(f'Pikafish exited with status {proc.returncode}')
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        proc.stdin.close()
        proc.stdout.close()
    report = {'episode': args.episode, 'episode_sha256': sha256(path),
              'engine': identity, 'engine_sha256': sha256(engine),
              'network_sha256': sha256(network), 'depth': args.depth,
              'coordinate_convention': 'Display a0=top-left; UCI a0=bottom-left; y_UCI=9-y_display',
              'verified_moves': len(checks), 'checks': checks,
              'initial_bestmove_uci': best,
              'initial_bestmove_display': flip_move(best) if best != '(none)' else None,
              'initial_final_info': info,
              'note': 'Pikafish confirms legality of each illustrated move. Finite-depth search '
                      'does not prove the capture-advisor retrograde result, mate distance, '
                      'or official repetition adjudication.', 'uci_transcript': transcript}
    out = args.report or ROOT / 'output' / args.episode / 'engine_report.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f'{identity}: verified {len(checks)} moves; initial bestmove '
          f'{best} UCI / {report["initial_bestmove_display"]} display; report: {out}')


if __name__ == '__main__':
    main()

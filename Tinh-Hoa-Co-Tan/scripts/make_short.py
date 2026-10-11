#!/usr/bin/env python3
"""Dựng YouTube Short câu đố cho một tập: python scripts/make_short.py --episode ep-0001 [--quality full].

Short gồm: đề bài + đếm ngược, đáp án (vài nước đầu của biến chính), kết luận,
lời mời xem tập đầy đủ. Lời đọc giới hạn để video dưới 60 giây.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.voice import generate_voice  # noqa: E402
from xq.commentary import moves_count  # noqa: E402

MAX_SECONDS = 52


def game_short(data, max_plies):
    """Short cho tập thực chiến: dừng ở khoảnh khắc then chốt đầu tiên của ván."""
    from xq.board import Position
    from xq.notation import vn_move
    trap = next((b for b in data['beats'] if b['kind'] == 'trap'), None)
    if trap:
        fen = trap['fen']
        moves = [st['move'] for st in trap['steps'] if st.get('move')][:max_plies]
        headline, tag = 'Danh thủ đã đi sai – còn bạn?', 'THỰC CHIẾN DANH THỦ'
        ask = 'Ở thế này, trong một ván đấu thật, danh thủ đã đi sai. Bạn có tìm ra nước đúng không?'
    else:
        line = next(b for b in data['beats'] if b['kind'] == 'line' and any(st.get('mark') in ('only', 'hold') for st in b['steps']))
        st = next(x for x in line['steps'] if x.get('mark') in ('only', 'hold'))
        pos = Position.from_fen(data['fen'])
        for b in data['beats']:
            if b['kind'] != 'line':
                continue
            for x in b['steps']:
                if x is st:
                    break
                if x.get('move'):
                    pos = pos.play(x['move'])
            else:
                continue
            break
        fen, moves = pos.fen(), [st['move']]
        headline, tag = 'Chỉ có một nước đúng!', 'THỰC CHIẾN DANH THỦ'
        ask = 'Trong ván đấu thật này, chỉ có đúng một nước giữ được kết quả. Bạn tìm ra không?'
    pos = Position.from_fen(fen)
    steps = [{'say': ask, 'countdown': 5}]
    for k, m in enumerate(moves):
        vn = vn_move(pos, m)
        steps.append({'say': (f'Đáp án: {vn}!' if k == 0 else f'{vn}.'), 'move': m, 'mark': 'answer' if k == 0 else None})
        pos = pos.play(m)
    g = data.get('game', {})
    steps.append({'say': 'Bạn có tìm ra không? Theo dõi kênh Tinh Hoa Cờ Tàn để xem thêm thực chiến danh thủ!'})
    return {'number': data['number'], 'fen': fen, 'headline': headline, 'tag': tag,
            'verdict': 'Tàn cuộc thực chiến', 'wdl': 'W', 'steps': steps,
            'footer': 'Tinh Hoa Cờ Tàn • Thực chiến danh thủ'}


PIECE = {'R': 'Xe', 'N': 'Mã', 'C': 'Pháo', 'P': 'Binh', 'A': 'Sĩ', 'B': 'Tượng', 'K': 'Tướng'}


def mate_short(data):
    from scripts.build_episodes import sac_phrase
    from xq.board import Position
    from xq.notation import vn_move
    m = data['mate']
    n, side = m['n'], m['side']
    sp = sac_phrase(m['sacrifices'])
    headline = f'{side} đi – chiếu bí trong {n} nước!'
    tag = 'SÁT CỤC'
    ask = f'{side} đi, chiếu bí trong {n} nước. Bạn tìm ra không?'
    g = data.get('game')
    if g:
        where = f'Ván đấu thật năm {g["year"]}' if g.get('year') else 'Một ván đấu thật'
        who = g.get('loser') or ('Đen' if side == 'Đỏ' else 'Đỏ')
        if g.get('resigned'):
            ask = f'{where}. Đến thế này, {who} xin thua. Vì sao? Bạn có nhìn ra không?'
            headline = f'Vì sao {who} xin thua?'
        else:
            ask = f'{where}. {g.get("winner") or side} kết thúc ván bằng đòn chiếu bí {n} nước. Bạn tìm ra không?'
        tag = 'THỰC CHIẾN DANH THỦ'
    steps = [{'say': ask, 'countdown': 5}]
    from xq.patterns import mate_patterns
    end = Position.from_fen(data['fen'])
    for x in m['line']:
        end = end.play(x['move'])
    found = mate_patterns(end)
    pattern = found[0] if found else ''
    pos = Position.from_fen(data['fen'])
    attacker = pos.turn
    for k, x in enumerate(m['line']):
        vn = vn_move(pos, x['move'])
        nxt = pos.play(x['move'])
        if pos.turn == attacker:
            if nxt.is_mate():
                say, tagx = f'{vn}. Chiếu bí!', 'BÍ!'
                if pattern:
                    say = f'{vn}. Chiếu bí! Thế sát {pattern}.'
            elif x.get('sacrifice'):
                say, tagx = f'{vn}! Thí {PIECE[x["sacrifice"]]}!', f'THÍ {PIECE[x["sacrifice"]].upper()}!'
            else:
                say, tagx = f'{vn}, chiếu!', None
            if k == 0:
                say = 'Đáp án: ' + say
            steps.append({'say': say, 'move': x['move'], 'mark': 'answer' if k == 0 else None, 'tag': tagx})
        else:
            cap = f', ăn {PIECE[x["capture"].upper()]}' if x.get('capture') else ''
            forced = ', bắt buộc' if x.get('forced') and not cap else ''
            steps.append({'say': f'{vn}{cap}{forced}.', 'move': x['move']})
        pos = nxt
    steps.append({'say': 'Bạn giải đúng không? Theo dõi kênh để xem sát cục mỗi ngày!'})
    return {'number': data['number'], 'fen': data['fen'], 'headline': headline, 'tag': tag,
            'verdict': (pattern if pattern else f'Bí trong {n} nước'), 'wdl': 'W', 'steps': steps,
            'footer': 'Tinh Hoa Cờ Tàn • Sát cục mỗi ngày',
            'flash': f'{side.upper()} ĐI • BÍ {n} NƯỚC'}


def short_script(data, max_plies):
    if data.get('kind') == 'mate':
        return mate_short(data)
    if data.get('kind') == 'game':
        return game_short(data, max_plies)
    a = data['analysis']
    main = a['main']
    val = a['value']
    root_side = 'Đỏ' if a['fen'].split()[1] == 'w' else 'Đen'
    if val['wdl'] == 'W':
        headline, tag = 'Đỏ đi trước – tìm nước thắng!', 'THỬ THÁCH CỜ TÀN'
        verdict = f'Đỏ thắng, chiếu bí sau {moves_count(val["dtm"])} nước'
        ask = 'Đỏ đi trước. Bạn có tìm ra nước thắng không? Hãy tạm dừng và để lại đáp án ở phần bình luận.'
    else:
        headline, tag = f'{root_side} đi – tìm nước giữ hòa!', 'THỬ THÁCH THỦ HÒA'
        verdict = 'Hòa nếu Đen phòng thủ chính xác'
        ask = f'{root_side} đi trước. Chỉ có rất ít nước giữ được hòa. Bạn tìm ra không?'
    steps = [{'say': ask, 'countdown': 5}]
    first = main[0]
    why = ''
    if first['only']:
        why = ' Đây là nước duy nhất ' + ('giữ hòa.' if first['wdl'] == 'D' else 'thắng.')
    elif first.get('only_fastest'):
        why = ' Nước thắng nhanh nhất.'
    steps.append({'say': f'Đáp án: {first["vn"]}!{why}', 'move': first['move'], 'mark': 'answer'})
    for ply in main[1:max_plies]:
        mark = 'only' if ply['only'] and ply['wdl'] == 'W' else ('hold' if ply['only'] and ply['wdl'] == 'D' else None)
        say = ply['vn'] + ('. Hết cờ!' if ply['mate'] else '.')
        steps.append({'say': say, 'move': ply['move'], 'mark': mark})
    steps.append({'say': f'Kết quả: {verdict}. Bạn giải đúng không? Theo dõi kênh Tinh Hoa Cờ Tàn nhé!'})
    return {'number': data['number'], 'fen': a['fen'], 'headline': headline, 'tag': tag,
            'verdict': verdict, 'wdl': val['wdl'], 'steps': steps}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--episode', required=True)
    ap.add_argument('--quality', choices=['preview', 'full'], default='preview')
    ap.add_argument('--voice', choices=['edge', 'zalo', 'mock'], default='edge')
    args = ap.parse_args()
    data = json.loads((ROOT / 'episodes' / f'{args.episode}.json').read_text(encoding='utf-8'))
    out = ROOT / 'output' / args.episode
    out.mkdir(parents=True, exist_ok=True)
    plies = min(len(data['analysis']['main']), 9) if data.get('analysis') else 7
    while True:
        short = short_script(data, plies)
        timing = generate_voice({'beats': [{'steps': short['steps']}]}, out / 'voice_short', args.voice)
        total = sum(c['seconds'] + .5 for c in timing[0]) + 6.5
        if total <= MAX_SECONDS or plies <= 2 or data.get('kind') == 'mate':
            break
        plies -= 1
    (out / 'short.json').write_text(json.dumps(short, ensure_ascii=False, indent=1), encoding='utf-8')
    env = os.environ.copy()
    env['XIANGQI_OUTPUT'] = str(out)
    env['PYTHONPATH'] = str(ROOT)
    res = ['-r', '1080,1920', '--fps', '30'] if args.quality == 'full' else ['-r', '540,960', '--fps', '15']
    subprocess.run([sys.executable, '-m', 'manim', *res, '--disable_caching', str(ROOT / 'src' / 'short_scene.py'),
                    'XiangqiShort', '--media_dir', str(out / 'media_short'), '-o', f'{args.episode}_short'],
                   env=env, check=True, cwd=ROOT)
    found = list((out / 'media_short').rglob(f'{args.episode}_short.mp4'))
    final = out / f'{args.episode}_short.mp4'
    shutil.copy2(found[0], final)
    print(f'SHORT {final} | ~{total:.0f} giây')


if __name__ == '__main__':
    main()

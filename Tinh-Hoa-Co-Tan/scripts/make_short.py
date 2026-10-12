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
# Facebook Reel tối đa 90 giây. Ước lượng giọng + đệm; phần đếm ngược/chữ nổi cộng thêm khoảng 6 giây.
REEL_MAX_SECONDS = 82


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


def is_thuc_dung(data):
    classic = data.get('classic') or {}
    topic = data.get('topic_data') or {}
    return classic.get('collection') == 'Co-Tan-Thuc-Dung' or topic.get('id') == 'classic-Co-Tan-Thuc-Dung'


def reel_copy(data):
    """Tiêu đề/mô tả dùng chung cho YouTube Short và Facebook Reel."""
    topic = data.get('topic_data') or {}
    raw = str(topic.get('book_number') or data.get('number') or '')
    num = f'{int(raw):03d}' if raw.isdigit() else raw
    sub = (data.get('subtitle') or topic.get('short') or 'Cờ tàn').strip()
    wdl = (data.get('verdict') or {}).get('wdl', 'W')
    first = ((data.get('analysis') or {}).get('main') or [{}])[0]
    quiet = first and not first.get('check') and not first.get('capture')
    if wdl == 'D':
        hook = 'giữ hòa được không?'
    elif quiet:
        hook = 'đừng chiếu vội!'
    elif first.get('only'):
        hook = 'chỉ một nước đúng!'
    else:
        hook = 'bạn thấy bẫy chưa?'
    title = f'Cờ Tàn Thực Dụng #{num} · {sub} – {hook} #Shorts'
    if len(title) > 100:
        title = f'Cờ Tàn Thực Dụng #{num} · {hook} #Shorts'
    if len(title) > 100:
        title = f'Cờ Tàn Thực Dụng #{num} #Shorts'
    take = topic.get('takeaway_short') or ''
    desc = '\n'.join([
        f'Cờ Tàn Thực Dụng, thế số {num}. {sub}.',
        'Dừng video, tự tìm nước, rồi xem lời giải trên bàn cờ.',
        f'Điểm nhớ: {take}' if take else '',
        'Kết luận kiểm chứng bằng bảng tra cờ tàn chessdb.cn.',
        'Sách: Tượng kỳ thực dụng tàn cục – Đồ Cảnh Minh.',
        '',
        '#Shorts #CoTuong #CoTan #CoTanThucDung',
    ])
    return {'title': title, 'description': '\n'.join(x for x in desc.splitlines())}


_SO = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười']


def _so(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return str(n)
    return _SO[n] if 0 <= n <= 10 else str(n)


def _fact(ply, i):
    """Chỉ nói điều bảng tra xác nhận. Không thêm câu đệm."""
    from xq.commentary import word
    if ply.get('mate'):
        return f'Ăn {word(ply["capture"])}, hết cờ.' if ply.get('capture') else 'Hết cờ.'
    if ply.get('n_legal') == 1:
        return 'Không còn nước nào khác.'
    if ply.get('only') and ply.get('wdl') == 'D':
        return ('Chỉ nước này giữ hòa.', 'Đi khác là thua.', 'Phải đi đúng ô này.')[i % 3]
    if ply.get('only') and ply.get('wdl') == 'W':
        return ('Chỉ nước này còn thắng.', 'Đi khác là tuột thắng.', 'Một nước thôi.')[i % 3]
    keep, legal = ply.get('n_keep') or 0, ply.get('n_legal') or 0
    if 0 < keep < legal and keep <= 2:
        giu = 'còn thắng' if ply.get('wdl') == 'W' else 'giữ hòa'
        return f'Chỉ {_so(keep)} nước {giu}.'
    bits = []
    if ply.get('capture'):
        bits.append(f'ăn {word(ply["capture"])}')
    if ply.get('check'):
        bits.append('chiếu')
    if bits:
        text = ', '.join(bits)
        return text[0].upper() + text[1:] + '.'
    note = _positional(ply)
    return note


def _positional(ply):
    piece = (ply.get('piece') or '').upper()
    if piece not in ('K', 'P') or ply.get('check') or ply.get('capture'):
        return ''
    from xq.board import Position, parse_sq
    from xq.commentary import facing_files
    before = Position.from_fen(ply['fen'])
    after = before.play(ply['move'])
    if piece == 'K':
        if set(facing_files(after)) - set(facing_files(before)):
            return 'Chiếm lộ, Tướng đối phương không bước sang được.'
        return ''
    dest = parse_sq(ply['move'][2:])
    if 3 <= dest[0] <= 5 and dest[1] >= 7:
        before_in = any(3 <= sq[0] <= 5 and sq[1] >= 7 and p == 'P' for sq, p in before.cells.items())
        if not before_in:
            return 'Binh áp sát cung.'
    return ''


def classic_reel(data, max_plies):
    """Short/Reel khoảng 85 giây: câu đố có bẫy, nước then chốt, biến chính, điểm nhớ."""
    topic = data.get('topic_data') or {}
    a = data['analysis']
    main = a['main'][:max_plies]
    val = a['value']
    num = topic.get('book_number') or data.get('number')
    sub = data.get('subtitle') or topic.get('short') or 'thế này'
    root_side = 'Đỏ' if a['fen'].split()[1] == 'w' else 'Đen'
    first = main[0]
    quiet = not first.get('check') and not first.get('capture')
    bad = next((m for m in first.get('ranked') or [] if m.get('wdl') != first.get('wdl')), None)
    nword = _so(num)
    legal = _so(first.get('n_legal') or 0)
    if val['wdl'] == 'D':
        headline = f'Thế {num}: giữ hòa được không?'
        tag = '5 GIÂY • THỦ HÒA'
        verdict = 'Hòa, nếu không tham'
        if bad and bad.get('wdl') == 'L':
            ask = f'{sub}. {root_side} đi. {bad["vn"]} nhìn hợp, nhưng đi là thua. Nước nào giữ hòa?'
        elif first.get('only'):
            ask = f'{sub}. {root_side} đi. {legal.capitalize()} nước, chỉ một nước giữ hòa. Bạn thấy không?'
        elif first.get('n_bad'):
            ask = f'{sub}. {root_side} đi. Có nước giữ hòa, có nước thua. Bạn chọn nước nào?'
        else:
            ask = f'{sub}. {root_side} đi. Nước đầu chưa phân thắng bại. Khó là những nước sau, phải giữ đúng từng ô.'
        flash = f'THẾ {num} • GIỮ HÒA'
        ending = 'Hòa, nếu giữ đúng những nước bắt buộc. Bạn theo kịp không?'
    elif first.get('only'):
        headline = f'Thế {num}: chỉ một nước'
        tag = '5 GIÂY • MỘT NƯỚC'
        verdict = f'Thắng sau {_so(moves_count(val["dtm"]))} nước'
        ask = f'{sub}. {root_side} có {legal} nước. Chỉ một nước thắng. Bạn tìm ra không?'
        flash = f'THẾ {num} • MỘT NƯỚC'
        ending = f'Đi đúng nước đầu, Đỏ thắng sau {_so(moves_count(val["dtm"]))} nước. Bạn có tìm ra không?'
    elif quiet:
        headline = f'Thế {num}: đừng chiếu vội'
        tag = '5 GIÂY • NƯỚC CHỜ'
        verdict = f'Thắng sau {_so(moves_count(val["dtm"]))} nước'
        ask = f'{sub}. {root_side} đi. Nước thắng không chiếu, không ăn quân. Bạn dám đi không?'
        flash = f'THẾ {num} • NƯỚC CHỜ'
        ending = f'Đi đúng nước đầu, Đỏ thắng sau {_so(moves_count(val["dtm"]))} nước. Bạn có tìm ra không?'
    else:
        headline = f'Thế {num}: tìm nước thắng'
        tag = '5 GIÂY • TÌM NƯỚC'
        verdict = f'Thắng sau {_so(moves_count(val["dtm"]))} nước'
        ask = f'{sub}. {root_side} đi trước. {legal.capitalize()} nước hợp lệ, không phải nước nào cũng thắng. Nước nào thắng?'
        flash = f'THẾ {num} • TÌM NƯỚC'
        ending = f'Đi đúng nước đầu, Đỏ thắng sau {_so(moves_count(val["dtm"]))} nước. Bạn có tìm ra không?'
    steps = [{'say': f'Cờ tàn thực dụng, thế số {nword}. {ask}', 'countdown': 5}]
    answer = f'Đáp án: {first["vn"]}.'
    why = _fact(first, 0)
    if why:
        answer += ' ' + why
    if bad and bad['vn'] not in answer:
        if bad.get('wdl') == 'L':
            answer += f' Đi {bad["vn"]} là thua.'
        elif bad.get('wdl') == 'D':
            answer += f' Đi {bad["vn"]} thì chỉ hòa.'
        else:
            answer += f' Đừng đi {bad["vn"]}.'
    steps.append({'say': answer, 'move': first['move'], 'mark': 'answer'})
    for i, ply in enumerate(main[1:], 1):
        fact = _fact(ply, i)
        say = f'{ply["vn"]}.' + (f' {fact}' if fact else '')
        mark = 'only' if ply.get('only') and ply.get('wdl') == 'W' else (
            'hold' if ply.get('only') and ply.get('wdl') == 'D' else None)
        steps.append({'say': say, 'move': ply['move'], 'mark': mark})
    steps.append({'say': ending})
    return {
        'number': data['number'], 'fen': a['fen'], 'headline': headline, 'tag': tag,
        'verdict': verdict, 'wdl': val['wdl'], 'steps': steps,
        'brand': 'CỜ TÀN THỰC DỤNG', 'flash': flash,
        'footer': f'Thực dụng tàn cục • thế số {num}',
    }


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
    ap.add_argument('--no-render', action='store_true', help='Chỉ tạo lời đọc, không dựng hình')
    args = ap.parse_args()
    data = json.loads((ROOT / 'episodes' / f'{args.episode}.json').read_text(encoding='utf-8'))
    out = ROOT / 'output' / args.episode
    out.mkdir(parents=True, exist_ok=True)
    classic = is_thuc_dung(data)
    cap = REEL_MAX_SECONDS if classic else MAX_SECONDS
    plies = min(len(data['analysis']['main']), 14 if classic else 9) if data.get('analysis') else 7
    while True:
        short = classic_reel(data, plies) if classic else short_script(data, plies)
        timing = generate_voice({'beats': [{'steps': short['steps']}]}, out / 'voice_short', args.voice)
        total = sum(c['seconds'] + .5 for c in timing[0]) + 6.5
        if total <= cap or plies <= 2 or data.get('kind') == 'mate':
            break
        plies -= 1
    (out / 'short.json').write_text(json.dumps(short, ensure_ascii=False, indent=1), encoding='utf-8')
    if args.no_render:
        print(f'SCRIPT {args.episode} | {plies} nước | ~{total:.0f} giây')
        for step in short['steps']:
            print(' -', step['say'])
        return
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

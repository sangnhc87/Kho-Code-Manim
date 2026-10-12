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


def _bite(ply, side_name):
    """Một câu ngắn, đổi theo nước — không lặp một câu đệm."""
    if ply.get('mate'):
        return 'Hết cờ. Không còn ô nào để chạy.'
    if ply.get('capture') and ply.get('check'):
        return 'Ăn quân và chiếu. Đòn này mới đau.'
    if ply.get('capture'):
        return 'Ăn được. Nhưng chưa phải lúc mừng.'
    if ply.get('only') and ply.get('wdl') == 'D':
        return 'Chỉ nước này giữ hòa. Đi khác là thua.'
    if ply.get('only'):
        return 'Nước duy nhất. Đi lệch một ô là hỏng.'
    if ply.get('check'):
        return 'Chiếu. Tướng đối phương hết đường thở.'
    piece = ply.get('piece') or ''
    if piece in ('P', 'p'):
        return 'Binh tiến đúng một nhịp. Vội là chết.'
    if piece in ('K', 'k'):
        verb = 'lùi' if 'thoái' in ply.get('vn', '') else 'tiến' if 'tiến' in ply.get('vn', '') else 'dịch'
        return f'{side_name} {verb} Tướng, chưa vội ăn. Nước chờ này mới khóa được thế.'
    if piece in ('R', 'r'):
        return 'Xe chiếm thông lộ. Đừng đổi sớm.'
    if piece in ('N', 'n'):
        return 'Mã nhảy vào đúng mắt. Nhìn kỹ chân Mã.'
    if piece in ('C', 'c'):
        return 'Pháo cần giá. Nước này dựng giá.'
    return 'Chưa ăn quân. Ép đối phương trước.'


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
    if val['wdl'] == 'D':
        headline = f'Thế {num}: giữ hòa được không?'
        tag = '5 GIÂY • THỦ HÒA'
        verdict = 'Hòa — nếu không tham'
        ask = f'{sub}. {root_side} đi. Một nước nghe rất ngon, nhưng đi là thua. Bạn có thấy nước giữ hòa không?'
        flash = f'THẾ {num} • ĐỪNG THAM'
    elif quiet:
        headline = f'Thế {num}: đừng chiếu vội!'
        tag = '5 GIÂY • NƯỚC CHỜ'
        verdict = f'Thắng sau {moves_count(val["dtm"])} nước'
        ask = f'{sub}. {root_side} đi trước. Nước thắng không chiếu, không ăn quân. Bạn dám đi không?'
        flash = f'THẾ {num} • NƯỚC CHỜ'
    elif first.get('only'):
        headline = f'Thế {num}: chỉ một nước!'
        tag = '5 GIÂY • DUY NHẤT'
        verdict = f'Thắng sau {moves_count(val["dtm"])} nước'
        ask = f'{sub}. Chỉ đúng một nước thắng. Đi khác là tuột. Bạn tìm ra không?'
        flash = f'THẾ {num} • MỘT NƯỚC'
    else:
        headline = f'Thế {num}: bạn thấy bẫy chưa?'
        tag = '5 GIÂY • TÌM NƯỚC THẮNG'
        verdict = f'Thắng sau {moves_count(val["dtm"])} nước'
        ask = f'{sub}. {root_side} đi trước. Nhìn thì dễ. Đi thật mới thấy bẫy. Nước nào thắng?'
        flash = f'THẾ {num} • CÓ BẪY'
    steps = [{'say': f'Cờ Tàn Thực Dụng, thế số {num}. {ask}', 'countdown': 5}]
    if first.get('only'):
        why = ' Chỉ một nước đúng.'
    elif quiet:
        why = ' Không chiếu. Không ăn. Vậy mà thắng.'
    elif first.get('n_bad'):
        why = f' Có {first["n_bad"]} nước nhìn ngon mà hỏng.'
    else:
        why = ' Đây là nước nhanh nhất.'
    steps.append({'say': f'Đáp án: {first["vn"]}!{why}', 'move': first['move'], 'mark': 'answer'})
    bad = next((m for m in first.get('ranked') or [] if m.get('wdl') != first.get('wdl')), None)
    if bad:
        steps.append({'say': f'Nhiều người sẽ đi {bad["vn"]}. Nghe hợp lý. Đi xong là mất thế.'})
    seen = set()
    alts = [
        'Cứ ép, đừng đổi quân.',
        'Giữ nhịp. Đối phương đang hết chỗ.',
        'Nhìn cung trước khi ăn.',
    ]
    alt_i = 0
    for ply in main[1:]:
        who = 'Đỏ' if ply.get('side') == 'w' else 'Đen'
        bite = _bite(ply, who)
        if bite in seen:
            bite = alts[alt_i % len(alts)]
            alt_i += 1
        seen.add(bite)
        mark = 'only' if ply.get('only') and ply.get('wdl') == 'W' else (
            'hold' if ply.get('only') and ply.get('wdl') == 'D' else None)
        steps.append({'say': f'{ply["vn"]}. {bite}', 'move': ply['move'], 'mark': mark})
    lure = next((t for t in a.get('traps') or [] if t.get('lure')), None)
    if lure and lure['lure']['vn'] != (bad or {}).get('vn'):
        steps.append({'say': f'Còn một bẫy ngọt hơn: {lure["lure"]["vn"]}. Đối phương hóa giải, và bạn thành người thua.'})
    take = topic.get('takeaway') or topic.get('takeaway_short') or verdict
    steps.append({'say': f'Nhớ một câu: {take} Bảng tra xác nhận: {verdict}.'})
    steps.append({'say': 'Bạn đi đúng nước đầu không? Comment đáp án, rồi xem thế tiếp theo.'})
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

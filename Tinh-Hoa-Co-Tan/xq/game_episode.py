"""Tập 'Thực chiến danh thủ': chấm tàn cuộc của một ván đấu thật bằng bảng tra."""
from __future__ import annotations

import re

from .analyze import play_line
from .board import Position
from .commentary import Writer, material_words, moves_count
from .notation import vn_move
from .players import describe, vn_name

SIDE = {'w': 'Đỏ', 'b': 'Đen'}
RESULT = {'红胜': 'Đỏ thắng', '红先胜': 'Đỏ thắng', '黑胜': 'Đen thắng', '红负': 'Đen thắng', '和局': 'Hòa', '和': 'Hòa'}


def year_of(date):
    m = re.search(r'(19|20)\d\d', date or '')
    if m:
        return m.group(0)
    m = re.match(r'(\d\d)[-./]', date or '')
    return ('19' + m.group(1)) if m else ''


def status_for(wdl_mover, dtm, mover):
    """Kết luận bảng tra nhìn từ phía Đỏ, sau khi bên mover vừa đi xong (wdl tính cho mover)."""
    if wdl_mover == 'D':
        return 'Bảng tra: Hòa'
    red_wins = (wdl_mover == 'W') == (mover == 'w')
    return f'Bảng tra: {"Đỏ" if red_wins else "Đen"} thắng' + (f' • còn {moves_count(dtm)} nước' if dtm else '')


def result_word(wdl, mover):
    if wdl == 'D':
        return 'hòa'
    return f'{SIDE[mover]} thắng' if wdl == 'W' else f'{SIDE["b" if mover == "w" else "w"]} thắng'


def build_game_episode(game, collection_title, ep):
    es = game['endgame']
    w = Writer(f'game-{ep}')
    red = describe(game['red'], 'w')
    black = describe(game['black'], 'b')
    year = year_of(game.get('date'))
    event = game.get('event') or ''
    root = Position.from_fen(es['entry_fen'])
    plies = es['plies']
    name = {'w': red, 'b': black}
    beats = []
    intro = (f'Hôm nay là tàn cuộc thực chiến: {red} cầm quân Đỏ gặp {black} cầm quân Đen'
             + (f', năm {year}' if year else '') + '. ')
    intro += (f'Sau {es["entry_ply"] // 2} hiệp, trên bàn còn {len(root.cells)} quân: '
              f'Đỏ có {material_words(root, "w")}; Đen có {material_words(root, "b")}. {SIDE[root.turn]} đi.')
    bullets = [f'Đỏ: {vn_name(game["red"]) or game["red"]}', f'Đen: {vn_name(game["black"]) or game["black"]}']
    if year:
        bullets.append(f'Năm {year}' + (f' • {event}' if event and not re.search(r'[一-鿿]', event) else ''))
    bullets.append(f'Vào tàn cuộc ở hiệp {es["entry_ply"] // 2 + 1}')
    beats.append({'kind': 'intro', 'label': 'THỰC CHIẾN DANH THỦ', 'headline': f'{vn_name(game["red"]) or "Đỏ"} – {vn_name(game["black"]) or "Đen"}',
                  'fen': es['entry_fen'], 'panel': {'bullets': bullets}, 'steps': [{'say': intro}]})
    first = plies[0]
    if first['before'] == 'D':
        verdict = 'Hòa'
    else:
        winner = SIDE[first['side']] if first['before'] == 'W' else SIDE['b' if first['side'] == 'w' else 'w']
        verdict = f'{winner} thắng, chiếu bí sau {moves_count(first["dtm_best"])} nước'
    real = RESULT.get(game.get('result', ''), game.get('result', ''))
    errors = [p for p in plies if p['error']]
    finds = [p for p in plies if p['only_found']]
    theory = [f'Từ thời điểm này, số quân đã đủ ít để bảng tra cờ tàn chessdb chấm chính xác từng nước. '
              f'Kết luận của bảng tra: {verdict.lower() if verdict == "Hòa" else verdict}.',
              f'Kết quả thực tế của ván đấu: {real.lower() if real == "Hòa" else real}.']
    if errors:
        theory.append(f'Giữa hai điều đó là {len(errors)} sai lầm làm thay đổi kết quả. Hãy cùng tìm xem chúng nằm ở đâu.')
    elif finds:
        theory.append(f'Trên đường đi có {len(finds)} lần một bên chỉ có đúng một nước giữ được kết quả. Liệu các danh thủ có tìm ra?')
    beats.append({'kind': 'theory', 'label': 'BẢNG TRA CHẤM ĐIỂM', 'headline': 'Thắng, hòa hay thua?',
                  'panel': {'bullets': [f'Bảng tra: {verdict}', f'Ván thật: {real}',
                                        f'{len(errors)} sai lầm • {len(finds)} nước duy nhất']},
                  'steps': [{'say': s} for s in theory]})

    key = {i for i, p in enumerate(plies) if p['error'] or p['only_found']}
    steps = []
    chunk_no = 0

    def flush(headline):
        nonlocal steps, chunk_no
        if steps:
            chunk_no += 1
            beats.append({'kind': 'line', 'label': f'DIỄN BIẾN • CHẶNG {chunk_no}', 'headline': headline,
                          'steps': steps})
            steps = []

    puzzles = 0
    praised = set()
    for i, p in enumerate(plies):
        pos = Position.from_fen(p['fen'])
        vn = vn_move(pos, p['move'])
        who = name[p['side']]
        if puzzles < 3 and (p['error'] or (p['only_found'] and not praised)):
            flush(w.pick('Diễn biến ván đấu', 'Hai bên giằng co', 'Tiếp tục tàn cuộc'))
            puzzles += 1
            n = p['n_keep']
            hint = (f'Ở thế này {SIDE[p["side"]]} có {p["n_legal"]} nước đi, nhưng chỉ '
                    + ('đúng một nước' if n == 1 else f'{n} nước') + f' giữ được kết quả {result_word(p["before"], p["side"])}.')
            beats.append({'kind': 'puzzle', 'label': 'THỬ THÁCH', 'headline': f'{SIDE[p["side"]]} đi thế nào?',
                          'panel': {'countdown': 5}, 'steps': [{'say': hint + ' Bạn sẽ chọn nước nào?'}]})
        after = Position.from_fen(p['fen']).play(p['move'])
        st = status_for(p['after'], p['dtm_played'], p['side'])
        if p['error']:
            best_vn = vn_move(pos, p['best'])
            say = (f'Trong ván, {who} đi {vn}. Sai lầm! Trước nước này {SIDE[p["side"]]} '
                   f'{"đang thắng" if p["before"] == "W" else "giữ được hòa"}, nhưng sau nước này kết quả thành '
                   f'{result_word(p["after"], p["side"])}. Nước đúng là {best_vn}.')
            steps.append({'say': say, 'move': p['move'], 'mark': 'bad', 'status': st})
            flush('Sai lầm quyết định')
            attacker = p['side'] if p['before'] == 'W' else ('b' if p['side'] == 'w' else 'w')
            line, _ = play_line(p['fen'], attacker, max_plies=6, prefer=[p['best']])
            tsteps = [{'say': f'Hãy quay lại xem nước đúng: {best_vn}.'}]
            for x in line:
                tsteps.append({'say': f'{x["vn"]}' + ('. Hết cờ.' if x['mate'] else '.'), 'move': x['move']})
            tsteps.append({'say': f'Như vậy, với {best_vn}, {SIDE[p["side"]]} giữ được kết quả '
                                  f'{result_word(p["before"], p["side"])}. Quay lại ván đấu thật.'})
            beats.append({'kind': 'trap', 'label': 'NƯỚC ĐÚNG LẼ RA', 'headline': f'{best_vn}!', 'rewind': True,
                          'fen': p['fen'], 'return_fen': after.fen(), 'steps': tsteps,
                          'panel': {'verdict': f'{best_vn}: {result_word(p["before"], p["side"])}'}})
        elif p['only_found'] and len(praised) < 2 and p['move'] not in praised:
            praised.add(p['move'])
            say = (f'{who} đi {vn}! Đây là nước duy nhất giữ được kết quả '
                   f'{result_word(p["before"], p["side"])}, và danh thủ đã tìm ra.')
            steps.append({'say': say, 'move': p['move'], 'mark': 'only' if p['before'] == 'W' else 'hold', 'status': st})
            flush('Nước duy nhất!')
        elif p['only_found']:
            steps.append({'say': w.pick(f'{vn}, lại là nước duy nhất.', f'{who} tiếp tục tìm đúng: {vn}.'),
                          'move': p['move'], 'status': st})
        else:
            say = w.pick(f'{vn}.', f'{SIDE[p["side"]]} đi {vn}.', f'{who} đi {vn}.')
            if after.is_mate():
                say = f'{vn}. ' + ('Chiếu bí!' if after.in_check(after.turn) else 'Đối phương hết nước đi.')
            steps.append({'say': say, 'move': p['move'], 'status': st})
            if len(steps) >= 8:
                flush(w.pick('Diễn biến ván đấu', 'Hai bên giằng co', 'Tiếp tục tàn cuộc'))
    if steps:
        steps.append({'say': f'Ván đấu kết thúc ở đây với kết quả: {real.lower() if real == "Hòa" else real}.'})
        flush('Kết thúc ván đấu')
    lessons = [f'Bảng tra: {verdict}; ván thật: {real}']
    say = [f'Tóm tắt. Bảng tra kết luận {verdict.lower() if verdict == "Hòa" else verdict} ngay khi vào tàn cuộc, '
           f'còn ván thật kết thúc {real.lower() if real == "Hòa" else real}.']
    if errors:
        e = errors[0]
        lessons.append(f'{len(errors)} sai lầm làm đổi kết quả')
        say.append(f'Sai lầm đầu tiên là {vn_move(Position.from_fen(e["fen"]), e["move"])} của {name[e["side"]]}; '
                   f'nước đúng là {vn_move(Position.from_fen(e["fen"]), e["best"])}.')
    if finds:
        lessons.append(f'{len(finds)} nước duy nhất được tìm ra')
        say.append(f'Đáng khen là {len(finds)} lần các kỳ thủ tìm ra nước duy nhất dưới áp lực thi đấu.')
    lessons.append('Ngay cả danh thủ cũng có thể sai ở tàn cuộc')
    say.append('Ngay cả các danh thủ hàng đầu cũng có thể sai ở tàn cuộc, nhất là khi thời gian suy nghĩ đã cạn. '
               'Học kỹ tàn cuộc là cách chắc chắn nhất để không đánh rơi những ván thắng.')
    say.append('Nếu thấy hữu ích, hãy bấm thích, đăng ký kênh và chia sẻ cho bạn cờ. Hẹn gặp lại.')
    beats.append({'kind': 'summary', 'label': 'TỔNG KẾT', 'headline': 'Bài học từ ván đấu', 'panel': {'bullets': lessons},
                  'steps': [{'say': s} for s in say]})
    return beats, {'red': red, 'black': black, 'year': year, 'errors': len(errors), 'finds': len(finds),
                   'verdict': verdict, 'real': real}

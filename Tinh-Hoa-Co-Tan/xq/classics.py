"""Tập dựng từ thế cờ kinh điển trong sách (curriculum/classics/*.json)."""
from __future__ import annotations

from .board import Position
from .commentary import material_words, moves_count
from .notation import vn_move

BOOKS = {
    'Co-Tan-Thuc-Dung': {'name': 'Tượng kỳ thực dụng tàn cục', 'author': 'Đồ Cảnh Minh', 'short': 'Thực dụng tàn cục'},
}
ORDER = 'RNCP'
WORD = {'R': 'Xe', 'N': 'Mã', 'C': 'Pháo', 'P': 'Binh'}


def category(pos):
    red = pos.material('w')
    names = [WORD[u] for u in ORDER if u in red]
    return 'Tàn ' + ' '.join(names) if names else 'Tàn cơ bản'


def book_number(file_name):
    """Số thứ tự trong sách (ví dụ '151-eg-xqsycj-tjm-150-...' là thế số 150)."""
    parts = file_name.split('-')
    return parts[4].lstrip('0') if len(parts) > 4 and parts[4].isdigit() else parts[0].lstrip('0')


def short_material(pos, side):
    """Tên gọn theo thói quen cờ tướng: 'Xe Sĩ', 'Mã Binh', 'Sĩ Tượng toàn', 'Song Sĩ'."""
    count = {}
    for p in pos.cells.values():
        if (p.isupper()) == (side == 'w') and p.upper() != 'K':
            count[p.upper()] = count.get(p.upper(), 0) + 1
    pawn = 'Binh' if side == 'w' else 'Tốt'
    names = {'R': 'Xe', 'N': 'Mã', 'C': 'Pháo', 'P': pawn}
    out = []
    for u in 'RNCP':
        n = count.get(u, 0)
        if n == 1:
            out.append(names[u])
        elif n == 2:
            out.append('Song ' + names[u])
        elif n:
            out.append(f'{("ba", "bốn", "năm")[n - 3]} {names[u]}')
    a, b = count.get('A', 0), count.get('B', 0)
    if a == 2 and b == 2:
        out.append('Sĩ Tượng toàn')
    else:
        out += (['Song Sĩ'] if a == 2 else ['Sĩ'] * a) + (['Song Tượng'] if b == 2 else ['Tượng'] * b)
    return ' '.join(out) if out else 'Tướng đơn'


def matching_topic(pos, topics):
    want = (pos.material('w').replace('K', ''), pos.material('b').replace('K', ''))
    for t in topics:
        if t.get('kind') == 'classic' or 'material' not in t:
            continue
        have = tuple(''.join(sorted(m, key='RNCABP'.index)) for m in t['material'])
        if have == want:
            return t
    return None


def verdict_text(wdl, dtm):
    if wdl == 'W':
        return f'Đỏ thắng, chiếu bí sau {moves_count(dtm)} nước'
    if wdl == 'D':
        return 'hòa'
    return 'Đỏ thua'


def classic_topic(collection, file_name, item, analysis, topics):
    book = BOOKS.get(collection, {'name': collection.replace('-', ' '), 'author': '', 'short': collection})
    pos = Position.from_fen(item['fen'])
    num = book_number(file_name)
    red, black = material_words(pos, 'w'), material_words(pos, 'b')
    red_short, black_short = short_material(pos, 'w'), short_material(pos, 'b')
    val = analysis['value']
    tb = verdict_text(val['wdl'], val['dtm'])
    book_res = {'W': 'Đỏ thắng', 'D': 'hòa', 'L': 'Đỏ thua'}.get(item.get('book_result'), '')
    by = f' của {book["author"]}' if book['author'] else ''
    theory = [f'Thế cờ hôm nay là thế số {num} trong cuốn {book["name"]}{by}, một giáo trình cờ tàn kinh điển.',
              f'Đỏ còn {red}; Đen còn {black}.']
    if book_res:
        if book_res.split()[-1] == ('thắng' if val['wdl'] == 'W' else 'hòa' if val['wdl'] == 'D' else 'thua'):
            theory.append(f'Sách kết luận {book_res}, và bảng tra cờ tàn chessdb xác nhận: {tb}.')
        else:
            theory.append(f'Điều thú vị: sách kết luận {book_res}, nhưng bảng tra chessdb cho kết quả {tb}. '
                          'Bảng tra tính theo luật đi quân cơ bản, chưa xét các luật thi đấu về chiếu dai, đuổi dai; '
                          'đó có thể là nguyên nhân của sự khác biệt.')
    main = analysis['main']
    if item.get('book_moves') and main:
        bm = item['book_moves'][0]
        root = Position.from_fen(analysis['fen'])
        ranked = {m['move']: m for m in main[0]['ranked']}
        if bm in ranked:
            vn = vn_move(root, bm)
            r = ranked[bm]
            if bm == main[0]['move']:
                theory.append(f'Nước đầu trong sách là {vn}, cũng chính là nước bảng tra chọn.')
            elif r['wdl'] == main[0]['wdl'] and r['wdl'] == 'W' and r['dtm'] > val['dtm']:
                theory.append(f'Sách đi {vn}; bảng tra xác nhận nước này cũng thắng, '
                              f'nhưng chậm hơn {moves_count(r["dtm"]) - moves_count(val["dtm"])} nước so với đường nhanh nhất.')
            elif r['wdl'] == main[0]['wdl']:
                theory.append(f'Sách đi {vn}, một nước cũng giữ được kết quả như bảng tra.')
            else:
                theory.append(f'Sách đi {vn}; theo bảng tra, nước này cho kết quả {verdict_text(r["wdl"], r["dtm"])}.')
    match = matching_topic(pos, topics)
    if match:
        bullets = list(match['bullets'])
        takeaway, take_short = match['takeaway'], match['takeaway_short']
    else:
        bullets = [f'Đỏ: {red_short}', f'Đen: {black_short}', f'Bảng tra: {tb}']
        if val['wdl'] == 'W':
            takeaway = f'Trong tàn cuộc {red_short} đấu {black_short}, hãy ghi nhớ nước then chốt {main[0]["vn"]} và kế hoạch của bên tấn công.'
        else:
            takeaway = f'Tàn cuộc {red_short} đấu {black_short} là thế hòa khi phòng thủ chính xác; hãy ghi nhớ đội hình phòng thủ của Đen.'
        take_short = 'Ghi nhớ nước then chốt' if val['wdl'] == 'W' else 'Ghi nhớ đội hình thủ hòa'
    short = f'{red_short} đấu {black_short}'
    return {
        'id': f'classic-{collection}', 'kind': 'classic', 'category': category(pos),
        'title': f'{short[0].upper() + short[1:]} – {book["short"]} số {num}',
        'short': short[0].upper() + short[1:], 'theory': theory, 'bullets': bullets[:4],
        'takeaway': takeaway, 'takeaway_short': take_short,
        'book': book, 'book_number': num, 'source_file': file_name,
    }

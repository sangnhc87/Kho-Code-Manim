#!/usr/bin/env python3
"""Build episodes/tap-0002.json: Mã Khéo Thắng Đơn Tượng using exact retrograde solver.
"""
import json
from pathlib import Path
from src.core import Board
from scripts.solve_matuong import solve, fen_of, legal_moves

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '2bk5/9/9/4N4/9/9/9/4K4/9/9 w'


def fen_board(b):
    rows = []
    for y in range(10):
        line = ''; blank = 0
        for x in range(9):
            piece = b.cells.get((x, y))
            if piece:
                if blank: line += str(blank); blank = 0
                line += piece
            else: blank += 1
        if blank: line += str(blank)
        rows.append(line)
    return '/'.join(rows) + ' ' + ('w' if b.turn == 'red' else 'b')


def position_after(moves):
    b = Board.fen(INITIAL)
    for mv in moves: b.play(mv[:2], mv[2:])
    return fen_board(b)


def beaten(mvs, label, headline, narration, insight, pause=1.4, **extra):
    prefix, following = mvs
    beat = {
        'label': label,
        'headline': headline,
        'narration': narration,
        'insight': insight,
        'fen': position_after(prefix),
        'moves': following,
        'pause': pause
    }
    beat.update(extra)
    return beat


def best_line(state, idx, res, dist, max_moves=25):
    steps = []
    st = state
    for _ in range(max_moves):
        choices = []
        for mv, nxt in legal_moves(st):
            if nxt == 'CAPTURE_B': choices.append((mv, -1, 0, nxt))
            elif nxt in idx: choices.append((mv, res[idx[nxt]], dist[idx[nxt]], nxt))
        target = -1 if res[idx[st]] == 1 else 1
        pos = [z for z in choices if z[1] == target]
        if not pos: break
        mv, _, _, nxt = min(pos, key=lambda z: z[2]) if target == -1 else max(pos, key=lambda z: z[2])
        steps.append(mv)
        if nxt == 'CAPTURE_B': break
        st = nxt
    return steps


def main():
    states, idx, res, depth = solve()
    start = next(s for s in states if fen_of(*s) == INITIAL)
    assert res[idx[start]] == 1 and depth[idx[start]] == 9

    openings = {m: n for m, n in legal_moves(start)}
    mainline = best_line(start, idx, res, depth)
    assert mainline == ['e3c2', 'd0d1', 'c2e1', 'c0a2', 'e1d3', 'd1d0', 'd3b2', 'a2c0', 'b2c0']

    # Slow win line starting with e3f1
    slow = ['e3f1'] + best_line(openings['e3f1'], idx, res, depth)
    assert len(slow) == 15 and slow[-1] == 'c3a2'

    # Blunder by black: d1d0 at move 2
    quick_capture = ['e3c2', 'd0d1', 'c2e1', 'd1d0', 'e1c0']

    # Black alternative: a2c4 at move 3
    alt_elephant = ['e3c2', 'd0d1', 'c2e1', 'c0a2', 'e1d3', 'a2c4', 'd3b2', 'd1d0', 'b2c4']

    # Blunder by red: e7e8 leads to draw
    draw_blunder = ['e7e8', 'c0e2']
    assert res[idx[openings['e7e8']]] == 0

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — Mã bắt Tượng?',
            'Đỏ còn Tướng và Mã, Đen còn Tướng và một Tượng khuyết. Đỏ đi trước. Trong cờ tàn thực chiến, Đơn Mã khéo thắng Đơn Tượng là một bài học căn bản vô cùng tinh diệu. Chìa khóa quyết định là Tướng Đỏ phải khống chế trung lộ, phối hợp cùng Mã phong tỏa các điểm bay của Tượng, ép Tượng Đen vào chỗ chết. Chúng ta cùng phân tích chi tiết các biến đi.',
            'ĐỎ ĐI TRƯỚC  •  MỤC TIÊU: BẮT TƯỢNG', 2.0, spotlight='e3'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Mã 5 tiến 7',
            'Nước đầu tiên then chốt: Đỏ đi Mã 5 tiến 7 chiếu tướng, nhanh chóng nhảy sang sườn đối phương để chuẩn bị khép góc. Đen đứng trước thế cờ này chỉ có một nước hợp lệ là tiến Tướng 4 tiến 1 tránh chiếu.',
            'CHIẾU TƯỚNG  •  MÃ 5 TIẾN 7', 1.3, horse_leg=['e3', 'c2']
        ),
        beaten(
            (mainline[:1], mainline[1:4]), 'BIẾN CHÍNH', 'Ép Tượng ra biên',
            'Đen tiến Tướng 4 tiến 1. Đỏ tiếp tục Mã 7 tiến 5 chiếm giữ trung tâm. Đứng trước sức ép của quân Mã, Tượng Đen không dám về tâm mà buộc phải đi Tượng 3 tiến 1 dạt ra biên. Thế cờ bắt đầu bước vào giai đoạn quyết định.',
            'TƯỚNG 4 TIẾN 1  •  TƯỢNG 3 TIẾN 1', 1.7
        ),
        beaten(
            (mainline[:4], mainline[4:7]), 'BIẾN CHÍNH', 'Khóa chặt đường Tượng',
            'Đỏ bình tĩnh đi Mã 5 thoái 6 điều chỉnh vị trí. Tướng Đen buộc phải thoái Tướng 4 thoái 1. Ngay lập tức, Đỏ tung đòn quyết định: Mã 6 tiến 8. Quân Mã đã khóa chặt đường rút của Tượng biên, đẩy Tượng Đen vào tử lộ.',
            'MÃ 5 THOÁI 6  •  MÃ 6 TIẾN 8', 1.6
        ),
        beaten(
            (mainline[:7], mainline[7:]), 'BIẾN CHÍNH', 'Bắt Tượng sau 9 hiệp',
            'Tượng Đen hết đường chạy, đành bay Tượng 1 thoái 3 về đáy. Mã Đỏ chỉ việc nhảy Mã 8 tiến 7 tóm gọn Tượng Đen. Toàn bộ biến chính chỉ mất chín hiệp đấu. Bắt được Tượng, Đỏ nắm chắc phần thắng trong tay.',
            '9 HIỆP ĐẤU  •  BẮT GỌN TƯỢNG', 1.8, spotlight='c0'
        ),
        beaten(
            (mainline[:3], ['d1d0', 'e1c0']), 'ĐEN SAI LẦM', 'Tướng lùi sớm — mất Tượng',
            'Quay lại thời điểm Đỏ vừa đưa Mã 7 tiến 5. Nếu Đen không chịu bay Tượng ra biên mà lại thoái Tướng 4 thoái 1, Đỏ lập tức nhảy Mã 5 tiến 7 chém thẳng Tượng Đen. Sai lầm này khiến Đen mất Tượng chỉ sau năm hiệp.',
            'TƯỚNG 4 THOÁI 1  •  MÃ 5 TIẾN 7', 1.4
        ),
        beaten(
            (mainline[:5], ['a2c4', 'd3b2', 'd1d0', 'b2c4']), 'NHÁNH KHÁC', 'Tượng bay lên hà — vẫn mất',
            'Nếu ở hiệp thứ ba, Tượng Đen không thoái về mà bay lên hà Tượng 1 tiến 3, Đỏ vẫn nhảy Mã 6 tiến 8. Tượng Đen bị tê liệt không thể di chuyển. Tướng Đen thoái 1 thì Mã Đỏ thoái 7 tóm gọn Tượng.',
            'TƯỢNG 1 TIẾN 3  •  MÃ 8 THOÁI 7', 1.5, spotlight='c4'
        ),
        beaten(
            ([], slow[:1]), 'ĐỎ ĐI CHẬM', 'Mã 5 tiến 4: thắng chậm',
            'Bây giờ xét lựa chọn khác của Đỏ: Nếu nước đầu Đỏ không nhảy Mã 5 tiến 7 mà lại chọn Mã 5 tiến 4 chiếu Tướng, Đỏ vẫn có thể thắng nhưng sẽ tốn nhiều hiệp hơn. Cùng theo dõi biến đi này kéo dài tới mười lăm hiệp.',
            'THẮNG CHẬM: 15 HIỆP', 1.3
        ),
        beaten(
            (slow[:1], slow[1:7]), 'THẮNG CHẬM', 'Mã phải đi đường vòng',
            'Đen tiến Tướng 4 tiến 1 tránh chiếu. Đỏ thoái Tướng 5 thoái 1 chờ thời. Tượng Đen tiến ra biên, Đỏ phải cho Mã nhảy thoái 2 rồi thoái 3 để tìm hướng tấn công mới.',
            'MÃ PHẢI ĐI ĐƯỜNG VÒNG', 1.2
        ),
        beaten(
            (slow[:7], slow[7:]), 'THẮNG CHẬM', 'Đến hiệp 15 mới bắt Tượng',
            'Từ đây, Mã Đỏ phải tiếp tục nhảy tiến 4, tiến 6 rồi tiến 7 khống chế. Cuối cùng Mã 7 tiến 9 mới bắt được Tượng. Mất tròn mười lăm hiệp, lâu hơn sáu hiệp so với biến Mã 5 tiến 7 lúc đầu.',
            '15 HIỆP  SO VỚI  9 HIỆP', 1.7
        ),
        beaten(
            ([], draw_blunder), 'NƯỚC SAI', 'Tướng đi sai: mất thế thắng',
            'Nước sai nghiêm trọng ở thế cờ ban đầu là Đỏ vội vàng đi Tướng 5 thoái 1. Đen lập tức bay Tượng 3 tiến 5 chiếm điểm tựa trung tâm. Tượng Đen liên kết an toàn, Đỏ mất hoàn toàn khả năng ép bắt Tượng và ván cờ dẫn tới hòa cuộc.',
            'ĐỎ ĐI SAI  •  ĐEN CẦM HÒA', 1.8
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '9 — 15 — Cầm hòa',
            'Tổng kết thế tàn Mã khéo thắng Đơn Tượng: Phải dùng Tướng giữ chặt trung lộ, Mã 5 tiến 7 ép Tượng ra biên rồi khép góc bắt gọn sau chín hiệp. Đi Mã 5 tiến 4 bị chậm mất mười lăm hiệp. Còn vội điều Tướng sẽ để đối phương cầm hòa. Hết tập hai.',
            'Mã 5.7: 9 HIỆP  •  Mã 5.4: 15 HIỆP  •  Tướng đi sai: HÒA', 2.1
        )
    ]

    obj = {
        'id': 'tap-0002',
        'title': 'MÃ KHÉO THẮNG ĐƠN TƯỢNG',
        'subtitle': 'Đỏ đi trước • Ép bắt Tượng trong mô hình 4 quân; thế cờ kinh điển.',
        'goal_text': 'MỤC TIÊU: BẮT TƯỢNG',
        'fen': INITIAL,
        'analysis_status': 'four_piece_elephant_retrograde',
        'verification_note': 'Exhaustive 4-piece retrograde solver to capture black elephant under ordinary legal moves. Long-check/chase repetition not covered. 9/15 are plies to capture elephant.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0002.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline), 'slow:', len(slow))


if __name__ == '__main__':
    main()

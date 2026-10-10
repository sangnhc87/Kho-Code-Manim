#!/usr/bin/env python3
"""Build episodes/tap-0005.json: Mã Chốt Cao Thắng Khuyết 1 Tượng (deep study).

Position proven by exhaustive AND-OR mate search: Red forces a Xiangqi stalemate
win (bi nuoc) in 13 moves. The knight captures the lone elephant, then the pawn
and knight break both advisors, ending in stalemate.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '4P1b2/4ak3/5a3/9/7N1/9/9/5K3/9/9 w'


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


def main():
    # Verified by scripts/solve_machot.py (stalemate win in 13; fastest win).
    mainline = ['h4f3', 'e1d2', 'f7e7', 'f2e1', 'f3h2', 'f1f2', 'h2g0', 'f2f1',
                'g0h2', 'f1f2', 'e7e8', 'e1f0', 'e0f0', 'd2e1', 'h2g0', 'f2f1',
                'f0e0', 'e1d2', 'e8e9', 'd2e1', 'g0e1', 'f1f2', 'e1g0', 'f2f1', 'e9d9']
    blunder = ['g0i2', 'f3h2']  # Black elephant to the edge -> mate in 2

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — khuyết 1 Tượng, bí nước sau 13 nước',
            'Đỏ còn Tướng, Mã và một Chốt cao. Đen còn Tướng, hai Sĩ và chỉ một Tượng — thế "khuyết một Tượng". Thiếu Tượng, phòng tuyến Đen mất điểm tựa, hai Sĩ cũng lỏng lẻo theo. Đây là bài cờ tàn rất sâu: Đỏ phải đi trọn mười ba nước, lần lượt chém Tượng rồi phá đôi Sĩ, cuối cùng dồn Tướng Đen vào thế bí nước. Chúng ta cùng phân tích từng biến.',
            'ĐỎ ĐI TRƯỚC  •  BÍ NƯỚC TRONG 13 NƯỚC', 2.1, spotlight='h4'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Mã 2 tiến 4',
            'Nước mở đầu chuẩn xác: Đỏ đi Mã 2 tiến 4 dồn thẳng vào Tượng Đen. Đen buộc phải đưa Sĩ 5 tiến 4 che chắn — đây là nước thủ lâu nhất, vì mọi nước khác đều thua nhanh hơn hẳn. Quân Mã bắt đầu cuộc vây ráp Tượng khuyết.',
            'MÃ 2 TIẾN 4  •  DỒN TƯỢNG KHUYẾT', 1.6, horse_leg=['h4', 'f3']
        ),
        beaten(
            (mainline[:1], mainline[1:7]), 'BIẾN CHÍNH', 'Mã vờn Tượng — Mã 2 tiến 3 chém Tượng',
            'Đen đưa Sĩ 5 tiến 4, Sĩ 6 thoái 5 đổi vị trí. Đỏ bình tĩnh đưa Tướng 4 bình 5 chiếm trung lộ, rồi Mã 4 tiến 2 dồn ép. Tướng Đen tiến 1, thì Mã 2 tiến 3 chém gọn Tượng khuyết duy nhất! Từ đây Đen trơ trọi hai Sĩ.',
            'MÃ VỜN TƯỢNG  •  CHÉM TƯỢNG KHUYẾT', 2.0, spotlight='g0'
        ),
        beaten(
            (mainline[:7], mainline[7:13]), 'BIẾN CHÍNH', 'Chốt 5 bình 4 — ăn Sĩ',
            'Tướng Đen thoái 1 cố thủ. Đỏ kiên nhẫn Mã 3 thoái 2 rồi Tướng 5 thoái 1 chờ thời. Đen đưa Sĩ 5 thoái 6 che cung, thì Chốt 5 bình 4 chém gọn Sĩ Đen tại cột 4! Mỗi bước Đỏ đều nhịp nhàng, không cho Đen thở.',
            'CHỐT 5 BÌNH 4  •  CHÉM SĨ', 1.9, spotlight='f0'
        ),
        beaten(
            (mainline[:13], mainline[13:]), 'BIẾN CHÍNH', 'Mã 3 thoái 5 ăn Sĩ — bí nước',
            'Đen còn một Sĩ cố gắng Sĩ 4 thoái 5, Sĩ 5 tiến 4 qua lại. Đỏ đưa Mã 2 tiến 3, Chốt 4 bình 5 dồn ép, Tướng 5 thoái 1 chiếm cao điểm. Đến nước hai mươi mốt, Mã 3 thoái 5 ăn nốt Sĩ cuối cùng! Tướng Đen không còn nước nào để đi — bí nước, theo luật cờ tướng Đen thua. Tròn mười ba nước Đỏ.',
            'MÃ ĂN SĨ CUỐI  •  BÍ NƯỚC', 2.1, spotlight='e1'
        ),
        beaten(
            (mainline[:1], blunder), 'ĐEN SAI LẦM', 'Tượng tiến 9 — thua ngay lập tức',
            'Quay lại sau nước Mã 2 tiến 4. Nếu Đen không che chắn bằng Sĩ mà lại đưa Tượng 7 tiến 9 chạy ra biên, thì Mã Đỏ chỉ việc Mã 4 tiến 2 — chiếu hết tức khắc chỉ sau hai nước Đỏ! Rút Tượng ra biên khiến Cửu cung Đen lộ hoàn toàn, thua ngay.',
            'TƯỢNG CHẠY BIÊN  •  CHIẾU HẾT TỨC KHẮC', 1.7, spotlight='h2'
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '13 nước — Mã Chốt phá thế khuyết Tượng',
            'Tổng kết bài Mã Chốt cao thắng khuyết một Tượng: Mã tiến 4 dồn ép, vờn Tượng rồi chém Tượng khuyết, Chốt bình 4 phá Sĩ, Mã thoái 5 ăn nốt Sĩ cuối, dồn Tướng Đen bí nước trong mười ba nước. Tượng Đen chạy biên là thua ngay. Hết tập năm.',
            'MÃ CHỐT CAO  •  13 NƯỚC BÍ NƯỚC', 2.2
        )
    ]

    obj = {
        'id': 'tap-0005',
        'title': 'MÃ CHỐT CAO THẮNG KHUYẾT 1 TƯỢNG',
        'subtitle': 'Đỏ đi trước • Mã Chốt cao hợp đồng phá thế khuyết 1 Tượng; cờ tàn kinh điển.',
        'category': 'Tàn Mã Chốt',
        'goal_text': 'MỤC TIÊU: THẮNG CỜ',
        'fen': INITIAL,
        'analysis_status': 'andor_mate_search',
        'verification_note': 'Exhaustive AND-OR mate search (repetition and 60-move rule ignored): Red forces a Xiangqi stalemate win (bi nuoc, a loss for the side to move) in 13 moves against all Black replies; fastest win. Knight captures the lone elephant, then pawn and knight break both advisors.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0005.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

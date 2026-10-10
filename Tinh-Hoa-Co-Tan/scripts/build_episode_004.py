#!/usr/bin/env python3
"""Build episodes/tap-0004.json: Mã Chốt Cao Thắng Khuyết 1 Sĩ (deep study).

Position proven by exhaustive AND-OR mate search (scripts/solve_machot.py):
Red forces mate in 13 moves. The knight and pawn maneuver for 10 moves before
capturing the sole defender advisor, then mate. First move e2d2 is the key.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '3a5/4k4/b3P4/9/2b6/9/1N7/9/9/5K3 w'


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
    # Verified by scripts/solve_machot.py (mate in 13; fastest win, defender delays maximally).
    mainline = ['e2d2', 'c4e2', 'b6d5', 'a2c4', 'd5e3', 'c4a2', 'e3g2', 'e1e0',
                'd2e2', 'a2c4', 'e2d2', 'd0e1', 'd2d1', 'e1f2', 'g2i1', 'f2e1',
                'i1h3', 'e1f2', 'h3f2', 'e0f0', 'd1e1', 'c4e2', 'f9e9', 'e2g4', 'f2h1']
    blunder = ['a2c0', 'b6c4', 'c0e2', 'f9e9', 'e1f1', 'd2e2', 'f1f0', 'e2d2',
               'd0e1', 'd2d1', 'f0e0', 'd1e1', 'e0f0', 'c4d6']

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — khuyết 1 Sĩ, thắng sau 13 nước',
            'Đỏ còn Tướng, Mã và một Chốt cao đã vượt sông. Đen còn Tướng, một Sĩ và hai Tượng — thế "khuyết một Sĩ". Nghe tưởng đơn giản, nhưng đây là bài cờ tàn rất sâu: Đỏ phải đi trọn mười ba nước chính xác mới bắt chết Tướng Đen. Mã Đỏ phiêu lưu khắp bàn cờ, Chốt thọc sâu từng bước, rồi mới chém gọn quân Sĩ khuyết và kết liễu. Chúng ta cùng phân tích từng biến.',
            'ĐỎ ĐI TRƯỚC  •  CHIẾU HẾT TRONG 13 NƯỚC', 2.1, spotlight='e2'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Chốt 5 bình 6',
            'Nước mở đầu chuẩn xác: Đỏ đi Chốt 5 bình 6 ép Đen phải lựa chọn. Đen buộc phải đáp Tượng 3 thoái 5 để giữ thế thủ lâu nhất — mọi nước khác đều thua nhanh hơn hẳn. Đòn bình Chốt mở đường cho Chốt tiến sâu và Mã lên ngựa.',
            'CHỐT 5 BÌNH 6  •  ÉP TƯỢNG PHẢI THOÁI', 1.6, spotlight='d2'
        ),
        beaten(
            (mainline[:1], mainline[1:9]), 'BIẾN CHÍNH', 'Mã điều động — Chốt chém Tượng',
            'Đen thoái Tượng 3 thoái 5. Đỏ phóng Mã 8 tiến 6, Mã 6 tiến 5 rồi Mã 5 tiến 3, điều động trường kỳ vào vị trí tấn công. Đen đưa Tượng 1 tiến 3 rồi thoái 1, Tướng 5 thoái 1 tránh né. Đến nước thứ chín, Đỏ đi Chốt 6 bình 5 chém gọn Tượng Đen ở cột 5!',
            'MÃ ĐIỀU ĐỘNG  •  CHỐT CHÉM TƯỢNG', 2.0, horse_leg=['b6', 'd5']
        ),
        beaten(
            (mainline[:9], mainline[9:19]), 'BIẾN CHÍNH', 'Chốt tiến sâu — Mã chém Sĩ',
            'Sau khi mất Tượng, Đen đưa Tượng 1 tiến 3 rồi Sĩ 4 tiến 5 bịt lối. Đỏ kiên nhẫn đưa Chốt 5 bình 6 rồi Chốt 6 tiến 1, mỗi bước dồn ép không ngừng. Mã Đỏ vòng vo Mã 3 tiến 1, Mã 1 thoái 2, ép Sĩ Đen nhảy lên nhảy xuống. Nước thứ mười chín, Mã 2 tiến 4 chém gọn Sĩ khuyết duy nhất!',
            'CHỐT THỌC SÂU  •  MÃ CHÉM GỌN SĨ', 2.1, spotlight='f2'
        ),
        beaten(
            (mainline[:19], mainline[19:]), 'BIẾN CHÍNH', 'Tướng khóa cung — Mã chiếu hết',
            'Mất Sĩ, Cửu cung Đen trống trải. Tướng Đen bình 6 tránh né, Đỏ đưa Chốt 6 bình 5 ép Tượng thoái 5, rồi Tướng 4 bình 5 chiếm trung lộ khóa chặt Cửu cung. Tượng Đen đành tiến 7, thì Mã 4 tiến 2 chiếu hết! Tròn mười ba nước đi, Đỏ bắt sống Tướng Đen.',
            'TƯỚNG KHÓA CUNG  •  MÃ CHIẾU HẾT', 1.9, spotlight='h1'
        ),
        beaten(
            (mainline[:1], blunder), 'ĐEN SAI LẦM', 'Thoái nhầm Tượng — thua nhanh gấp đôi',
            'Quay lại sau nước Chốt 5 bình 6. Nếu Đen thoái nhầm Tượng 1 thoái 3 thay vì Tượng 3 thoái 5, Tượng còn lại lập tức bị Mã 8 tiến 7 chém gọn! Đen cố chống đỡ bằng Tượng 3 tiến 5, nhưng Chốt 6 bình 5 ăn thêm Tượng, rồi Chốt 6 bình 5 ăn nốt Sĩ — Đen bí nước chỉ sau tám nước Đỏ. Thoái sai một Tượng, trả giá cả ván cờ.',
            'THOÁI NHẦM TƯỢNG  •  BÍ NƯỚC SAU 8 NƯỚC', 1.8, spotlight='c4'
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '13 nước — Mã Chốt phá thế khuyết Sĩ',
            'Tổng kết bài Mã Chốt cao thắng khuyết một Sĩ: Chốt bình 6 ép Tượng, Mã điều động ba nước dồn ép, Chốt thọc sâu chém Tượng rồi Mã chém Sĩ khuyết, cuối cùng Tướng khóa cung và Mã chiếu hết trong mười ba nước. Nếu Đen thoái nhầm Tượng, thua nhanh gấp đôi. Hết tập bốn.',
            'MÃ CHỐT CAO  •  13 NƯỚC CHIẾU HẾT', 2.2
        )
    ]

    obj = {
        'id': 'tap-0004',
        'title': 'MÃ CHỐT CAO THẮNG KHUYẾT 1 SĨ',
        'subtitle': 'Đỏ đi trước • Mã Chốt cao hợp đồng phá thế khuyết 1 Sĩ; cờ tàn kinh điển.',
        'category': 'Tàn Mã Chốt',
        'goal_text': 'MỤC TIÊU: THẮNG CỜ',
        'fen': INITIAL,
        'analysis_status': 'andor_mate_search',
        'verification_note': 'Exhaustive AND-OR mate search (repetition and 60-move rule ignored): Red forces mate in 13 moves against all Black replies; fastest win, defender delays maximally. Knight and pawn maneuver for 10 moves before capturing the sole defender advisor, then mate.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0004.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build episodes/tap-0004.json: Mã Chốt Cao Thắng Khuyết 1 Sĩ (deep study).

Position proven by exhaustive AND-OR mate search (scripts/solve_machot.py):
Red forces a Xiangqi stalemate win (bi nuoc) in 14 moves. The pawn advances
step by step; knight and pawn capture both elephants and the lone advisor
before stalemating the General.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '6b2/3ka4/5P3/9/2b6/9/1N7/9/9/4K4 w'


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
    # Verified by scripts/solve_machot.py (stalemate win in 14; fastest win).
    mainline = ['f2f1', 'c4e2', 'b6d5', 'e1d0', 'd5c3', 'd1d2', 'c3e2', 'd2d1',
                'e2g3', 'd1d2', 'f1f0', 'd0e1', 'f0g0', 'e1f2', 'g3f1', 'd2d1',
                'g0f0', 'f2e1', 'f0e0', 'd1d2', 'f1h2', 'e1f2', 'h2g0', 'd2d1',
                'g0f2', 'd1d2', 'e0d0']
    blunder = ['g0i2', 'f1e1', 'd1d0', 'b6c4', 'i2g4', 'c4e3', 'g4i2', 'e3c2']

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — khuyết 1 Sĩ, bí nước sau 14 nước',
            'Đỏ còn Tướng, Mã và một Chốt cao đã lọt sâu vào Cửu cung. Đen còn Tướng, một Sĩ và hai Tượng — thế "khuyết một Sĩ". Thiếu một Sĩ, phòng tuyến Đen không còn kín kẽ. Đây là bài cờ tàn rất sâu: Đỏ phải đi trọn mười bốn nước chính xác, lần lượt chém đôi Tượng rồi chém nốt quân Sĩ khuyết, cuối cùng dồn Tướng Đen vào thế bí nước. Chúng ta cùng phân tích từng biến.',
            'ĐỎ ĐI TRƯỚC  •  BÍ NƯỚC TRONG 14 NƯỚC', 2.1, spotlight='f2'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Chốt 4 tiến 1',
            'Nước mở đầu chuẩn xác: Đỏ đi Chốt 4 tiến 1 đâm thẳng xuống đáy Cửu cung, ép Đen phải lựa chọn. Đen buộc phải đáp Tượng 3 thoái 5 để giữ thế thủ lâu nhất — mọi nước khác đều thua nhanh hơn hẳn. Chốt thọc sâu mở đường cho Mã lên ngựa hợp vây.',
            'CHỐT 4 TIẾN 1  •  ĐÂM THẲNG CỬU CUNG', 1.6, spotlight='f1'
        ),
        beaten(
            (mainline[:1], mainline[1:7]), 'BIẾN CHÍNH', 'Mã 8 tiến 6 — Mã 7 tiến 5 ăn Tượng',
            'Đen thoái Tượng 3 thoái 5. Đỏ phóng Mã 8 tiến 6 dồn ép, Đen đưa Sĩ 5 thoái 4 che cung. Đỏ tiếp Mã 6 tiến 7, buộc Tướng Đen tiến 1, thì Mã 7 tiến 5 chém gọn Tượng Đen ở cột 5! Quân Mã vờn quanh rồi ra đòn chớp nhoáng.',
            'MÃ VỜN QUANH  •  CHÉM TƯỢNG', 2.0, horse_leg=['b6', 'd5']
        ),
        beaten(
            (mainline[:7], mainline[7:13]), 'BIẾN CHÍNH', 'Chốt tiến sâu — Chốt 4 bình 3 ăn Tượng',
            'Tướng Đen thoái 1, Đỏ đưa Mã 5 thoái 3 chuyển cánh. Tướng Đen lại tiến 1. Đỏ kiên nhẫn Chốt 4 tiến 1 thêm một bước, ép Sĩ Đen tiến lên che chắn, thì Chốt 4 bình 3 chém gọn Tượng thứ hai tại cột 3! Đôi Tượng của Đen giờ đã bị nhổ sạch.',
            'CHỐT THỌC SÂU  •  CHÉM NỐT TƯỢNG', 2.0, spotlight='g0'
        ),
        beaten(
            (mainline[:13], mainline[13:25]), 'BIẾN CHÍNH', 'Chốt Mã phối hợp — Mã 3 thoái 4 ăn Sĩ',
            'Đen đưa Sĩ 5 tiến 6 cố thủ. Đỏ đưa Mã 3 tiến 4, rồi Chốt 3 bình 4, Chốt 4 bình 5 lần lượt dồn ép, buộc Sĩ Đen nhảy lên nhảy xuống theo ý Đỏ. Mã vòng vèo Mã 4 thoái 2, Mã 2 tiến 3, đến nước hai mươi lăm, Mã 3 thoái 4 chém gọn quân Sĩ khuyết cuối cùng!',
            'CHỐT MÃ PHỐI HỢP  •  CHÉM GỌN SĨ', 2.1, spotlight='f2'
        ),
        beaten(
            (mainline[:25], mainline[25:]), 'BIẾN CHÍNH', 'Chốt 5 bình 6 — bí nước',
            'Mất hết Sĩ Tượng, Tướng Đen trơ trọi giữa Cửu cung. Tướng Đen tiến 1, Đỏ đi Chốt 5 bình 6 khóa nốt lối thoát — Tướng Đen không còn nước nào để đi, bí nước, theo luật cờ tướng Đen thua cuộc. Tròn mười bốn nước Đỏ, Mã Chốt cao nhổ sạch phòng tuyến và bắt chết Tướng Đen.',
            'CHỐT 5 BÌNH 6  •  BÍ NƯỚC', 1.9, spotlight='d0'
        ),
        beaten(
            (mainline[:1], blunder), 'ĐEN SAI LẦM', 'Tượng chạy biên — lộ Sĩ, thua nhanh',
            'Quay lại sau nước Chốt 4 tiến 1. Nếu Đen không thoái Tượng 3 thoái 5 mà lại đưa Tượng 7 tiến 9 chạy ra biên, quân Sĩ lập tức bị lộ. Chốt Đỏ bình 5 chém Sĩ ngay, Mã 8 tiến 7 chém nốt Tượng, rồi Mã 5 tiến 7 chiếu hết chỉ sau năm nước Đỏ! Tượng chạy biên để lộ Sĩ là sai lầm chí mạng.',
            'TƯỢNG CHẠY BIÊN  •  CHIẾU HẾT SAU 5 NƯỚC', 1.8, spotlight='e1'
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '14 nước — Mã Chốt phá thế khuyết Sĩ',
            'Tổng kết bài Mã Chốt cao thắng khuyết một Sĩ: Chốt tiến sâu từng bước, Mã vờn quanh chém đôi Tượng, rồi Chốt Mã phối hợp chém nốt Sĩ khuyết, cuối cùng dồn Tướng Đen bí nước trong mười bốn nước. Tượng Đen chạy biên để lộ Sĩ là thua nhanh. Hết tập bốn.',
            'MÃ CHỐT CAO  •  14 NƯỚC BÍ NƯỚC', 2.3
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
        'verification_note': 'Exhaustive AND-OR mate search (repetition and 60-move rule ignored): Red forces a Xiangqi stalemate win (bi nuoc, a loss for the side to move) in 14 moves against all Black replies; fastest win. Knight and pawn capture both elephants and the sole advisor before stalemating the General.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0004.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

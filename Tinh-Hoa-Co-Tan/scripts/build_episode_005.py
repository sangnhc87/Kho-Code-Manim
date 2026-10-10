#!/usr/bin/env python3
"""Build episodes/tap-0005.json: Mã Chốt Cao Thắng Khuyết 1 Tượng.

Position proven by exhaustive AND-OR mate search (scripts/solve_machot.py):
Red forces a Xiangqi stalemate win (bi nuoc, which is a loss for the side to
move) in 6 moves. First move d5c3 (Mã 6 tiến 7) is the unique winning move.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '3a1a3/9/b1P1k4/9/9/3N5/9/5K3/9/9 w'


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
    # Verified by scripts/solve_machot.py (stalemate win in 6; fastest win).
    mainline = ['d5c3', 'e2e1', 'c3a2', 'e1d1', 'f7e7', 'd0e1', 'a2b0', 'd1d0', 'c2c1', 'd0e0', 'c1c0']
    blunder = ['e1e2', 'a2c1', 'e2e1', 'c2d2']  # Black e1e2 after c3a2 -> stalemate in 4

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — phá Tượng khuyết?',
            'Đỏ còn Tướng, Mã và một Chốt cao. Đen còn Tướng, hai Sĩ và chỉ một Tượng — thế "khuyết một Tượng". Thiếu một Tượng, phòng tuyến của Đen mất đi điểm tựa che chắn, hai Sĩ cũng vì thế mà lỏng lẻo. Bài học hôm nay: Mã và Chốt cao hợp sức phá vỡ thế khuyết Tượng, bắt chết Tướng Đen. Chúng ta cùng phân tích từng biến.',
            'ĐỎ ĐI TRƯỚC  •  THẾ KHUYẾT 1 TƯỢNG', 2.0, spotlight='d5'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Mã 6 tiến 7',
            'Nước mở đầu then chốt: Đỏ đi Mã 6 tiến 7 nhảy sang cánh, dồn thẳng vào Tượng Đen. Đây là nước duy nhất giữ được chiến thắng nhanh — thắng cờ chỉ trong sáu nước Đỏ. Tướng Đen buộc phải thoái 1 tránh thế.',
            'MÃ 6 TIẾN 7  •  NƯỚC DUY NHẤT', 1.4, horse_leg=['d5', 'c3']
        ),
        beaten(
            (mainline[:1], mainline[1:5]), 'BIẾN CHÍNH', 'Mã 7 tiến 9 — ăn Tượng!',
            'Tướng Đen thoái 1 về. Đỏ lập tức Mã 7 tiến 9 chém gọn Tượng Đen! Từ đây Đen chỉ còn trơ trọi hai Sĩ. Đen cố điều Tướng 5 bình 4 tránh né, Đỏ bình tĩnh đưa Tướng 4 bình 5 chiếm trung lộ, khóa chặt lộ Tướng Đen.',
            'MÃ ĂN TƯỢNG  •  TƯỚNG CHIẾM TRUNG LỘ', 1.7, horse_leg=['c3', 'a2']
        ),
        beaten(
            (mainline[:5], mainline[5:]), 'BIẾN CHÍNH', 'Chốt 7 tiến 1 — bí nước',
            'Đen đi Sĩ 4 tiến 5 chống đỡ. Đỏ kiên nhẫn Mã 9 tiến 8 khóa cung, rồi đưa Chốt 7 tiến 1 từng bước xuống tận đáy. Tướng Đen bị dồn vào thế không còn nước nào để đi — bí nước, theo luật cờ tướng Đen thua cuộc. Tròn sáu nước Đỏ, Mã Chốt cao hợp vây kín mít Cửu cung.',
            'CHỐT THỌC SÂU  •  BÍ NƯỚC', 1.8, spotlight='c0'
        ),
        beaten(
            (mainline[:3], blunder), 'ĐEN SAI LẦM', 'Tướng 5 tiến 1 — thua nhanh hơn',
            'Quay lại sau khi Mã Đỏ ăn Tượng. Nếu Đen không đi Tướng 5 bình 4 mà nóng vội Tướng 5 tiến 1, Mã Đỏ liền Mã 9 tiến 7 khóa cửa, Chốt 7 bình 6 siết chặt — Tướng Đen bí nước ngay, chỉ sau bốn nước Đỏ. Sai lầm tiến Tướng khiến Đen thua nhanh hơn hẳn.',
            'TIẾN TƯỚNG VỘI  •  BÍ NƯỚC SỚM', 1.5, spotlight='d2'
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '6 nước — Mã ăn Tượng, Chốt bí nước',
            'Tổng kết bài Mã Chốt cao thắng khuyết một Tượng: Mã tiến 7 ép Tướng, tiến 9 ăn Tượng, Tướng chiếm trung lộ rồi Chốt thọc sâu bí nước trong sáu nước. Tướng Đen khinh suất tiến lên sẽ thua càng nhanh. Hết tập năm.',
            'MÃ CHỐT CAO  •  6 NƯỚC', 2.1
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
        'verification_note': 'Exhaustive AND-OR mate search (repetition and 60-move rule ignored): Red forces a Xiangqi stalemate win (bi nuoc, a loss for the side to move) in 6 moves against all Black replies. Unique winning first move d5c3.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0005.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

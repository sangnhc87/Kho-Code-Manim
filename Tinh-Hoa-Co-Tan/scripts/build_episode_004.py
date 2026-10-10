#!/usr/bin/env python3
"""Build episodes/tap-0004.json: Mã Chốt Cao Thắng Khuyết 1 Sĩ.

Position proven by exhaustive AND-OR mate search (scripts/solve_machot.py):
Red forces mate in 6 moves. First move g2f2 (Chốt 3 bình 4) captures the lone
defender advisor, and is the unique fastest winning move.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '2b2k3/9/4baP2/9/9/N8/9/4K4/9/9 w'


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
    # Verified by scripts/solve_machot.py (mate in 6; fastest win, defender delays maximally).
    mainline = ['g2f2', 'c0a2', 'a5b3', 'f0e0', 'b3c1', 'e0d0', 'f2e2', 'd0d1', 'e2e1', 'd1d2', 'c1b3']
    blunder = ['e2c4', 'a5c4', 'c0e2', 'c4d2', 'e2g4', 'f2f1']  # Black e2c4 after g2f2 -> mate in 4

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — phá Sĩ khuyết Tượng?',
            'Đỏ còn Tướng, Mã và một Chốt cao đã vượt sông. Đen còn Tướng, một Sĩ và hai Tượng — đúng thế "khuyết một Sĩ". Mất một Sĩ, Cửu cung Đen lập tức lộ khe hở chí mạng: Sĩ không còn đủ đôi để che chắn lộ Tướng. Bài học hôm nay: Mã và Chốt cao phối hợp thế nào để khai thác khe hở ấy, bắt sống Tướng Đen. Chúng ta cùng vào phân tích từng biến.',
            'ĐỎ ĐI TRƯỚC  •  THẾ KHUYẾT 1 SĨ', 2.0, spotlight='g2'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Chốt 3 bình 4 — ăn Sĩ!',
            'Đòn phá cửa ngay lập tức: Đỏ đi Chốt 3 bình 4 chém gọn Sĩ Đen tại cột 4! Khuyết đi Sĩ còn lại duy nhất, Cửu cung Đen trống trải. Đây chính là nước duy nhất đưa đến chiếu hết nhanh nhất, chỉ trong sáu nước Đỏ.',
            'CHỐT 3 BÌNH 4  •  CHÉM GỌN SĨ', 1.5, spotlight='f2'
        ),
        beaten(
            (mainline[:1], mainline[1:5]), 'BIẾN CHÍNH', 'Mã 9 tiến 8 — Mã 8 tiến 7',
            'Đen đi Tượng 3 tiến 1 rút về phòng thủ. Đỏ lập tức điều Mã 9 tiến 8 rồi Mã 8 tiến 7, đưa quân Mã áp sát Cửu cung, sẵn sàng hợp vây. Tướng Đen bị dồn ép phải đi Tướng 6 bình 5, mỗi bước đều nằm trong toan tính của Đỏ.',
            'MÃ ÁP SÁT  •  DỒN TƯỚNG ĐEN', 1.7, horse_leg=['a5', 'b3']
        ),
        beaten(
            (mainline[:5], mainline[5:]), 'BIẾN CHÍNH', 'Chốt 4 bình 5 — Mã 7 thoái 8 chiếu hết',
            'Đòn kết liễu phối hợp tuyệt đẹp: Tướng Đen chạy sang lộ 4, Đỏ liền Chốt 4 bình 5 chém nốt Tượng Đen ở cột 5, rồi Chốt 5 tiến 1 dồn ép Tướng Đen. Tướng Đen nhích lên từng bước, thì Mã 7 thoái 8 chiếu hết gọn gàng ở nước thứ mười một. Chốt cao đâm thẳng, Mã khóa cung — Tướng Đen không còn đường thoát.',
            'PHỐI HỢP CHỐT MÃ  •  CHIẾU HẾT', 1.8, spotlight='e2'
        ),
        beaten(
            (mainline[:1], blunder), 'ĐEN SAI LẦM', 'Tượng 5 tiến 3 — thua nhanh hơn',
            'Quay lại sau khi Đỏ ăn Sĩ. Nếu Đen không rút Tượng 3 tiến 1 mà lại đi Tượng 5 tiến 3, tưởng chừng đuổi Chốt, thì Mã Đỏ nhảy Mã 9 tiến 7 chém ngay Tượng ấy! Đen cố cứu vãn bằng Tượng 3 tiến 5 và Tượng 5 tiến 7, nhưng Chốt 4 tiến 1 chiếu hết chỉ sau bốn nước Đỏ. Để lộ Tượng khiến Đen thua nhanh gấp rưỡi.',
            'LỘ TƯỢNG  •  THUA NHANH', 1.5, spotlight='c4'
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '6 nước — Chốt phá Sĩ, Mã khóa cung',
            'Tổng kết bài Mã Chốt cao thắng khuyết một Sĩ: Chốt cao bình 4 ăn ngay Sĩ khuyết, Mã tiến lên khóa cung, Chốt thọc sâu phối hợp chiếu hết trong sáu nước. Nếu Đen khinh suất để lộ Tượng, thua càng nhanh. Hết tập bốn.',
            'MÃ CHỐT CAO  •  6 NƯỚC CHIẾU HẾT', 2.1
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
        'verification_note': 'Exhaustive AND-OR mate search (repetition and 60-move rule ignored): Red forces mate in 6 moves against all Black replies; fastest win, defender delays maximally. Unique fastest first move g2f2 captures the sole defender advisor.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0004.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build episodes/tap-0006.json: Mã Chốt Khéo Thắng Sĩ Tượng Toàn.

Position proven by exhaustive AND-OR mate search (scripts/solve_machot.py):
Red forces mate in 5 moves against the full advisor+elephant defense.
First move e7d5 (Mã 5 tiến 6) is the unique fastest winning move.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '3a5/4a4/3kb4/5P3/2b6/9/9/4NK3/9/9 w'


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
    # Verified by scripts/solve_machot.py (mate in 5; fastest win).
    mainline = ['e7d5', 'e1f2', 'd5c3', 'd0e1', 'f3e3', 'e2g4', 'f7e7', 'e1f0', 'e3d3']
    blunder = ['e1f0', 'e3d3']  # Black e1f0 after f3e3 -> mate in 4

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — phá Sĩ Tượng toàn?',
            'Đây là đỉnh cao của chuyên đề Mã Chốt: Đỏ chỉ còn Tướng, Mã và một Chốt cao, còn Đen giữ nguyên vẹn hai Sĩ hai Tượng — thế Sĩ Tượng toàn tưởng như vững chắc. Thế nhưng bằng kỹ thuật phối hợp điêu luyện, Mã và Chốt cao vẫn khéo léo xuyên thủng phòng tuyến, bắt chết Tướng Đen. Chúng ta cùng phân tích từng biến đi.',
            'ĐỎ ĐI TRƯỚC  •  SĨ TƯỢNG TOÀN', 2.0, spotlight='e7'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Mã 5 tiến 6',
            'Nước mở đầu chuẩn xác: Đỏ đi Mã 5 tiến 6 nhảy vào sát Cửu cung, uy hiếp trực diện. Đây là nước duy nhất đưa đến chiếu hết nhanh nhất — chỉ trong năm nước Đỏ. Đen buộc phải đi Sĩ 5 tiến 6 để che chắn.',
            'MÃ 5 TIẾN 6  •  NƯỚC DUY NHẤT', 1.4, horse_leg=['e7', 'd5']
        ),
        beaten(
            (mainline[:1], mainline[1:5]), 'BIẾN CHÍNH', 'Mã 6 tiến 7 — Chốt 4 bình 5',
            'Đen đưa Sĩ 5 tiến 6 lên. Đỏ tiếp tục Mã 6 tiến 7 chuyển cánh, ép Đen phải Sĩ 4 tiến 5. Liền đó, Đỏ đi Chốt 4 bình 5 thọc thẳng vào trung lộ — mũi đột kích xé toang phòng tuyến Sĩ Tượng đôi bên.',
            'MÃ CHUYỂN CÁNH  •  CHỐT THỌC TRUNG LỘ', 1.7, horse_leg=['d5', 'c3']
        ),
        beaten(
            (mainline[:5], mainline[5:]), 'BIẾN CHÍNH', 'Tướng 4 bình 5 — Chốt 5 bình 6 chiếu hết',
            'Đen cố đi Tượng 5 tiến 7 vùng vẫy. Đỏ điềm nhiên đưa Tướng 4 bình 5 chiếm trung lộ, phong tỏa hoàn toàn Cửu cung. Đen đành Sĩ 5 thoái 6, thì Chốt 5 bình 6 chiếu hết! Năm nước Đỏ gọn gàng, Sĩ Tượng toàn cũng phải gục ngã trước Mã Chốt cao phối hợp.',
            'TƯỚNG CHIẾM TRUNG LỘ  •  CHIẾU HẾT', 1.8, spotlight='d3'
        ),
        beaten(
            (mainline[:5], blunder), 'ĐEN SAI LẦM', 'Sĩ 5 thoái 6 sớm — thua ngay',
            'Quay lại sau khi Đỏ đi Chốt 4 bình 5. Nếu Đen không đi Tượng 5 tiến 7 mà vội Sĩ 5 thoái 6, thì Chốt Đỏ chỉ việc bình 6 chiếu hết tức khắc — Đen thua ngay lập tức chỉ sau bốn nước Đỏ. Che chắn sai nước khiến Sĩ Tượng toàn sụp đổ nhanh chóng.',
            'CHE CHẮN SAI  •  CHIẾU HẾT TỨC KHẮC', 1.5, spotlight='d3'
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '5 nước — Mã Chốt phá Sĩ Tượng toàn',
            'Tổng kết bài Mã Chốt khéo thắng Sĩ Tượng toàn: Mã tiến 6 nhập cung, tiến 7 chuyển cánh, Chốt bình 5 thọc trung lộ, Tướng chiếm trung lộ rồi Chốt bình 6 chiếu hết trong năm nước. Hết tập sáu.',
            'MÃ CHỐT CAO  •  5 NƯỚC', 2.1
        )
    ]

    obj = {
        'id': 'tap-0006',
        'title': 'MÃ CHỐT KHÉO THẮNG SĨ TƯỢNG TOÀN',
        'subtitle': 'Đỏ đi trước • Mã Chốt cao khéo phá Sĩ Tượng toàn; đỉnh cao cờ tàn mã chốt.',
        'category': 'Tàn Mã Chốt',
        'goal_text': 'MỤC TIÊU: THẮNG CỜ',
        'fen': INITIAL,
        'analysis_status': 'andor_mate_search',
        'verification_note': 'Exhaustive AND-OR mate search (repetition and 60-move rule ignored): Red forces mate in 5 moves against all Black replies; fastest win, defender delays maximally. Unique fastest first move e7d5.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0006.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

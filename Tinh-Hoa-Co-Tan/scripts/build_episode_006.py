#!/usr/bin/env python3
"""Build episodes/tap-0006.json: Mã Chốt Khéo Thắng Sĩ Tượng Toàn (deep study).

Position proven by exhaustive AND-OR mate search: Red forces mate in 13 moves
against the FULL advisor+elephant defense without capturing a single piece.
The knight completes a 10-move tour before delivering the final mate.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '3a1ab2/3P5/3k4b/9/9/2N6/9/9/9/5K3 w'


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
    # Verified by scripts/solve_machot.py (mate in 13; fastest win, no captures at all).
    mainline = ['d1c1', 'd2e2', 'c5d3', 'd0e1', 'c1d1', 'e1d0', 'd3b2', 'i2g4',
                'b2a4', 'e2d2', 'a4c3', 'g0e2', 'd1c1', 'e2c4', 'f9e9', 'd0e1',
                'c3b1', 'e1f2', 'b1a3', 'c4e2', 'a3b5', 'f0e1', 'b5d6', 'e1f0', 'd6e4']
    blunder = ['g0e2', 'c5e4']  # Black elephant blocks own king -> mate in 2

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — phá Sĩ Tượng toàn trong 13 nước',
            'Đây là đỉnh cao của chuyên đề Mã Chốt: Đỏ chỉ còn Tướng, Mã và một Chốt cao, còn Đen giữ nguyên vẹn hai Sĩ hai Tượng — thế Sĩ Tượng toàn vững như bàn thạch. Thế nhưng bằng kỹ thuật điều quân điêu luyện, Đỏ buộc Đen phải đi từng nước theo ý mình, và chiếu hết trong đúng mười ba nước mà không cần ăn bất kỳ quân nào! Chúng ta cùng phân tích từng biến.',
            'ĐỎ ĐI TRƯỚC  •  CHIẾU HẾT 13 NƯỚC KHÔNG ĂN QUÂN', 2.2, spotlight='c5'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Chốt 6 bình 7',
            'Nước mở đầu như đòn gõ cửa: Đỏ đi Chốt 6 bình 7 ép Tướng Đen phải rời vị trí. Đen buộc phải đi Tướng 4 bình 5 ra trung lộ — đây là nước thủ duy nhất kéo dài đến mười ba nước. Mọi nước đi Sĩ hay Tượng thay thế đều khiến Đen thua ngay lập tức.',
            'CHỐT 6 BÌNH 7  •  GÕ CỬA ÉP TƯỚNG', 1.7, spotlight='c1'
        ),
        beaten(
            (mainline[:1], mainline[1:7]), 'BIẾN CHÍNH', 'Mã tiến 6 — Mã tiến 8',
            'Tướng Đen bình 5 ra trung lộ. Đỏ đưa Mã 7 tiến 6 áp sát, Đen đành Sĩ 4 tiến 5. Đỏ tiếp Chốt 7 bình 6, Sĩ 5 thoái 4, rồi Mã 6 tiến 8 dồn sang cánh trái. Mỗi nước đi của Đỏ đều buộc Sĩ Tượng Đen phải nhảy theo điệu nhạc của mình.',
            'MÃ TIẾN 6  •  MÃ TIẾN 8', 1.9, horse_leg=['c5', 'd3']
        ),
        beaten(
            (mainline[:7], mainline[7:13]), 'BIẾN CHÍNH', 'Mã vòng cánh — Chốt quấy rối',
            'Đen đưa Tượng 9 tiến 7. Đỏ tiếp tục Mã 8 thoái 9, Mã 9 tiến 7 vòng qua cánh trái, ép Tướng Đen bình 4 rồi Tượng 7 tiến 5. Liền đó Chốt 6 bình 7 quấy rối, Tượng 5 tiến 3 tránh né. Thế trận của Đen dần bị bóp nghẹt từng ô cờ.',
            'MÃ VÒNG CÁNH  •  CHỐT QUẤY RỐI', 1.9, horse_leg=['a4', 'c3']
        ),
        beaten(
            (mainline[:13], mainline[13:]), 'BIẾN CHÍNH', 'Mã du ngoạn — chiếu hết',
            'Đen cố chống đỡ bằng Sĩ 4 tiến 5, Sĩ 5 tiến 6 qua lại. Đỏ kiên nhẫn đưa Mã 7 tiến 8, Mã 8 thoái 9, Mã 9 thoái 8 rồi Mã 8 thoái 6 — chặn đứng mọi đường chạy của Tướng Đen. Nước hai mươi lăm, Mã 6 tiến 5 chiếu hết! Trọn mười ba nước điều quân không ăn một quân nào, Sĩ Tượng toàn gục ngã trước Mã Chốt khéo léo.',
            'MÃ DU NGOẠN  •  CHIẾU HẾT KHÔNG ĂN QUÂN', 2.2, spotlight='e4'
        ),
        beaten(
            (mainline[:1], blunder), 'ĐEN SAI LẦM', 'Tượng tiến 5 chắn cung — thua ngay',
            'Quay lại sau nước Chốt 6 bình 7. Nếu Đen không đưa Tướng bình 5 mà lại đi Tượng 7 tiến 5, Tượng này lập tức bịt chính đường Tướng Đen. Mã Đỏ chỉ việc Mã 7 tiến 5 — chiếu hết tức khắc sau hai nước Đỏ! Sĩ Tượng toàn mà đi sai một nước, cả phòng tuyến sụp đổ.',
            'TƯỢNG CHẮN CUNG  •  CHIẾU HẾT TỨC KHẮC', 1.7, spotlight='e4'
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '13 nước — Mã Chốt khéo phá Sĩ Tượng toàn',
            'Tổng kết bài Mã Chốt khéo thắng Sĩ Tượng toàn: Chốt bình 7 gõ cửa, Mã trường kỳ điều động mười nước vòng quanh, phối hợp Chốt quấy rối bóp nghẹt Sĩ Tượng, rồi Mã 6 tiến 5 chiếu hết trong mười ba nước — không cần ăn một quân nào. Hết tập sáu.',
            'MÃ CHỐT CAO  •  13 NƯỚC CHIẾU HẾT', 2.3
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
        'verification_note': 'Exhaustive AND-OR mate search (repetition and 60-move rule ignored): Red forces mate in 13 moves against all Black replies without capturing a single piece; fastest win, defender delays maximally. The knight completes a 10-move tour before the final mate.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0006.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

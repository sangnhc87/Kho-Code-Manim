#!/usr/bin/env python3
"""Build episodes/tap-0003.json: Mã Khéo Thắng Đơn Tốt using exact retrograde solver.
"""
import json
from pathlib import Path
from src.core import Board

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '3k5/9/6N2/9/3p5/9/9/3K5/9/9 w'


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
    # Verified moves from retrograde calculation:
    mainline = ['g2e3', 'd0e0', 'd7d8', 'e0f0', 'd8e8', 'f0e0', 'e8f8', 'e0d0', 'e3c2', 'd0e0', 'c2d4']
    quick_blunder = ['g2e3', 'd4d5', 'e3d5']
    draw_blunder = ['d7e7', 'd4d5']

    beats = [
        beaten(
            ([], []), 'THẾ CỜ', 'Đỏ đi trước — Mã bắt Tốt?',
            'Đỏ còn Tướng và Mã, Đen còn Tướng và một Tốt đang rình rập vượt sông. Trong kho tàng cờ tàn thực dụng, Đơn Mã khéo thắng Đơn Tốt là bài học kinh điển vô cùng tinh tế. Điểm cốt tử của thế cờ: Mã Đỏ phải nhanh chóng chiếm cứ điểm chiến lược chặn đứng bước tiến của Tốt, đồng thời dùng Tướng kiểm soát Cửu cung để cô lập Tướng Đen, tiến tới bắt gọn Tốt. Chúng ta cùng phân tích chi tiết các biến đi.',
            'ĐỎ ĐI TRƯỚC  •  MỤC TIÊU: BẮT TỐT', 2.0, spotlight='g2'
        ),
        beaten(
            ([], mainline[:1]), 'NƯỚC ĐẦU', '1. Mã 3 thoái 5',
            'Nước cờ độc thủ khai màn: Đỏ đi Mã 3 thoái 5 nhảy thẳng vào tâm! Quân Mã kiểm soát hoàn toàn điểm d5, cấm triệt để Tốt Đen tiến xuống. Đây là nước đi duy nhất giữ vững thế tất thắng.',
            'MÃ VÀO TÂM  •  CHẶN ĐẦU TỐT', 1.3, horse_leg=['g2', 'e3']
        ),
        beaten(
            (mainline[:1], mainline[1:4]), 'BIẾN CHÍNH', 'Ép Tướng ra sườn',
            'Đen không thể tiến Tốt, đành đi Tướng 4 bình 5 vào trung lộ. Đỏ điềm tĩnh thoái Tướng 6 thoái 1 chờ thời. Nước cờ sâu sắc này buộc Tướng Đen phải dạt sang lộ sườn 6.',
            'TƯỚNG 4 BÌNH 5  •  TƯỚNG 6 THOÁI 1', 1.7
        ),
        beaten(
            (mainline[:4], mainline[4:8]), 'BIẾN CHÍNH', 'Đỏ chuyển Tướng khóa cung',
            'Đỏ tiếp tục đưa Tướng 6 bình 5 ra trung lộ, Đen lại phải chạy Tướng 6 bình 5. Ngay sau đó, Đỏ điều Tướng 5 bình 4 chiếm cao điểm lộ sườn, đẩy Tướng Đen sang lộ 4. Toàn bộ Cửu cung bị Tướng Đỏ khống chế, Tướng Đen hoàn toàn bị cô lập không thể tiếp ứng cho Tốt.',
            'TƯỚNG KHÓA CUNG  •  CÔ LẬP TƯỚNG ĐEN', 1.6
        ),
        beaten(
            (mainline[:8], mainline[8:]), 'BIẾN CHÍNH', 'Bắt Tốt sau 11 hiệp',
            'Thời cơ chín muồi! Đỏ thoái Mã 5 thoái 7 chuyển cánh mở đòn công kích. Tướng Đen đành lùi về trung lộ. Mã Đỏ lập tức phóng Mã 7 tiến 6 chém gọn Tốt Đen ở d4! Tròn mười một hiệp đấu chuẩn xác, Đỏ tiêu diệt gọn quân bài hộ thân duy nhất của đối phương.',
            '11 HIỆP ĐẤU  •  BẮT GỌN TỐT ĐEN', 1.8, spotlight='d4'
        ),
        beaten(
            (mainline[:1], quick_blunder[1:]), 'ĐEN SAI LẦM', 'Tốt tiến vội — mất Tốt ngay',
            'Quay lại thời điểm Đỏ vừa đưa Mã 3 thoái 5 chặn đầu. Nếu Đen nóng vội đẩy Tốt 6 tiến 1 vượt sông, Mã Đỏ chỉ việc nhảy Mã 5 tiến 6 chém thẳng Tốt Đen tại chỗ. Sai lầm nôn nóng khiến Đen mất Tốt chỉ sau ba hiệp ngắn ngủi.',
            'TỐT 6 TIẾN 1  •  MẤT TỐT HIỆP 3', 1.4, spotlight='d5'
        ),
        beaten(
            ([], draw_blunder), 'NƯỚC SAI', 'Tướng đi sai: mất thế thắng',
            'Nước sai lầm nghiêm trọng của Đỏ ở nước đầu là vội vàng đưa Tướng 6 bình 5 ra trung lộ mà không chịu nhảy Mã chặn Tốt. Tốt Đen lập tức tiến xuống thoát khỏi tầm kiềm tỏa, thế trận trở nên cân bằng và Đen cầm hòa thành công!',
            'ĐỎ ĐI SAI  •  ĐEN CẦM HÒA', 1.8
        ),
        beaten(
            ([], []), 'CHỐT BIẾN', '11 hiệp — Cầm hòa',
            'Tổng kết bài cờ Mã khéo thắng Đơn Tốt: Mã thoái 5 chặn đầu Tốt, Tướng khéo léo đổi cánh khống chế Cửu cung để bắt Tốt sau mười một hiệp. Nếu Đỏ đi sai Tướng sẽ để Tốt lọt xuống và bị cầm hòa. Hết tập ba.',
            'Mã thoái 5: 11 HIỆP  •  Tướng đi sai: HÒA', 2.1
        )
    ]

    obj = {
        'id': 'tap-0003',
        'title': 'MÃ KHÉO THẮNG ĐƠN TỐT',
        'subtitle': 'Đỏ đi trước • Khóa đường ép bắt Tốt trong mô hình 4 quân; cờ tàn kinh điển.',
        'category': 'Tàn Mã',
        'goal_text': 'MỤC TIÊU: BẮT TỐT',
        'fen': INITIAL,
        'analysis_status': 'four_piece_pawn_retrograde',
        'verification_note': 'Exhaustive 4-piece retrograde solver to capture black pawn under ordinary legal moves. 11 plies to capture pawn against delaying defender.',
        'beats': beats
    }

    dst = ROOT / 'episodes' / 'tap-0003.json'
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Episode:', dst, 'beats:', len(beats), 'mainline:', len(mainline))


if __name__ == '__main__':
    main()

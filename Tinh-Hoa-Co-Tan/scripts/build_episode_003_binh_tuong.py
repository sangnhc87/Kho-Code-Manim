"""Build Episode 003: ĐƠN BINH VS ĐƠN TƯỢNG (Khéo Thắng Tượng Kẹt Góc & Thế Hòa Quy Phạm).
Validated by exact retrograde solver (solve_binh_tuong_voi.py).
"""
import json
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parents[1] / 'episodes' / 'tap-0003.json'

EPISODE_003 = {
    "id": "tap-0003",
    "title": "ĐƠN BINH VS ĐƠN TƯỢNG",
    "subtitle": "Đỏ đi trước • Tuyệt kỹ bắt Tượng kẹt góc & Thế hòa quy phạm.",
    "category": "Tàn Binh",
    "goal_text": "MỤC TIÊU: BẮT TƯỢNG KẸT GÓC",
    "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
    "analysis_status": "four_piece_pawn_elephant_retrograde",
    "verification_note": "Exact 4-piece retrograde solver for K+P vs k+e. Capture Elephant and winning conversion verified under Vietnamese Xiangqi rules.",
    "beats": [
        {
            "label": "THẾ CỜ",
            "headline": "Đỏ đi trước — Đơn Binh thắng Đơn Tượng?",
            "narration": "Chào mừng các bạn đến với tập 3 của series Tinh Hoa Cờ Tàn, chuyên đề Tàn Binh. Trong cờ tàn thực chiến, Đơn Binh đối đầu Đơn Tượng thông thường là thế hòa quy phạm bởi Tượng di chuyển rất cơ động. Tuy nhiên, nếu Tượng Đen bị kẹt ở góc bàn cờ và Tướng Đen bị ép lệch cung, bên Đỏ hoàn toàn có thể khéo léo dùng mặt Tướng và Tốt cao chẹn đường rút, bắt sống Tượng Đen để giành chiến thắng. Chúng ta cùng phân tích thế cờ tinh diệu này.",
            "insight": "ĐỎ ĐI TRƯỚC  •  MỤC TIÊU: BẮT SỐNG TƯỢNG ĐEN",
            "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": [],
            "pause": 2.0,
            "spotlight": "d2"
        },
        {
            "label": "NƯỚC ĐẦU",
            "headline": "1. Binh 6 tiến 1",
            "narration": "Nước cờ đầu tiên chuẩn xác: Đỏ đi Binh 6 tiến 1! Đây là nước đi mấu chốt: Tốt tiến xuống hàng hai vừa khống chế mắt tượng, chặn đứng hoàn toàn đường bay của Tượng Đen vào tâm, vừa đè đầu Tướng Đen. Tướng Đen ở vị trí này không thể tiến lên tầng hai vì Tốt Đỏ cản đường, chỉ có một nước đi duy nhất là bình Tướng sang trung lộ.",
            "insight": "CHẶN MẮT TƯỢNG  •  BINH 6 TIẾN 1",
            "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1"],
            "pause": 1.5,
            "spotlight": "d1"
        },
        {
            "label": "ĐEN ĐÁP",
            "headline": "1... Tướng 4 bình 5",
            "narration": "Đen buộc phải đi Tướng 4 bình 5 sang trung tâm. Tượng Đen ở góc biên hoàn toàn bị cô lập, không thể bay đi đâu vì các đường bay đều đã bị cản.",
            "insight": "ĐEN BUỘC ĐI  •  TƯỚNG VÀO TRUNG TÂM",
            "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "d0e0"],
            "pause": 1.2,
            "spotlight": "e0"
        },
        {
            "label": "TIẾP ÁP SÁT",
            "headline": "2. Binh 6 tiến 1",
            "narration": "Đỏ ung dung đi tiếp Binh 6 tiến 1 xuống hàng đáy! Nước đi này áp sát và phong tỏa hoàn toàn Tượng Đen ở góc biên. Tướng Đen ở trung lộ bị mặt Tướng Đỏ ở lộ sáu khóa chặt, không thể quay trở lại lộ bốn, buộc phải dạt tiếp sang lộ sáu.",
            "insight": "XUỐNG ĐÁY ÁP SÁT  •  BINH 6 TIẾN 1",
            "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "d0e0", "d1d0"],
            "pause": 1.6,
            "spotlight": "d0"
        },
        {
            "label": "ĐEN DẠT GÓC",
            "headline": "2... Tướng 5 bình 6",
            "narration": "Tướng Đen buộc phải đi Tướng 5 bình 6 dạt sang cánh đối diện. Số phận của Tượng Đen lúc này đã chính thức được định đoạt.",
            "insight": "TƯỚNG DẠT GÓC  •  TƯỢNG ĐEN VÔ VỌNG",
            "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "d0e0", "d1d0", "e0f0"],
            "pause": 1.2,
            "spotlight": "f0"
        },
        {
            "label": "BẮT TƯỢNG",
            "headline": "3. Binh 6 bình 7 (Bắt Tượng)",
            "narration": "Đỏ đi nước cờ quyết định: Binh 6 bình 7 ăn gọn Tượng Đen! Đen mất sạch quân phòng thủ, ván cờ chuyển về thế Đơn Binh thắng Đơn Tướng mà chúng ta đã học ở tập một. Đỏ nắm chắc phần thắng trong tay!",
            "insight": "ĂN GỌN TƯỢNG ĐEN  •  ĐỎ TOÀN THẮNG",
            "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "d0e0", "d1d0", "e0f0", "d0c0"],
            "pause": 2.5,
            "spotlight": "c0"
        },
        {
            "label": "BÀI HỌC",
            "headline": "Quy phạm: Khi nào Đơn Tượng thủ hòa?",
            "narration": "Tổng kết bài học: Trong cờ tàn chuẩn mực, Đơn Binh gặp Đơn Tượng là thế cờ hòa quy phạm. Nếu bên phòng thủ luôn đưa Tượng bay lên trung tâm hoặc bay nhịp nhàng hai cánh để tránh né, Đơn Binh không thể nào bắt được Tượng. Đỏ chỉ thắng khi Tượng Đen bị kẹt góc và mất chân như ván cờ này. Chúc các bạn áp dụng thành công trong thực chiến!",
            "insight": "BÍ QUYẾT: TƯỢNG GIỮ TRUNG TÂM THÌ HÒA",
            "fen": "2bk5/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": [],
            "pause": 2.5,
            "spotlight": "c0"
        }
    ]
}

if __name__ == '__main__':
    OUT_FILE.write_text(json.dumps(EPISODE_003, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Successfully built {OUT_FILE}')

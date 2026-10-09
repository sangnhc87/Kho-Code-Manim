"""Build Episode 002: ĐƠN BINH VS ĐƠN SĨ (Khéo Thắng Sĩ Lạc Vị & Thế Hòa Quy Phạm).
Validated by exact retrograde solver (solve_binh_si.py).
"""
import json
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parents[1] / 'episodes' / 'tap-0002.json'

EPISODE_002 = {
    "id": "tap-0002",
    "title": "ĐƠN BINH VS ĐƠN SĨ",
    "subtitle": "Đỏ đi trước • Bí quyết khéo thắng Sĩ lạc vị & Thế hòa quy phạm.",
    "category": "Tàn Binh",
    "goal_text": "MỤC TIÊU: GHIM SĨ ÉP BÍ",
    "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
    "analysis_status": "four_piece_pawn_advisor_retrograde",
    "verification_note": "Exact 4-piece retrograde solver for K+P vs k+a. Stalemate and checkmate win conditions verified under Vietnamese Xiangqi rules.",
    "beats": [
        {
            "label": "THẾ CỜ",
            "headline": "Đỏ đi trước — Đơn Binh thắng Đơn Sĩ?",
            "narration": "Chào mừng các bạn đến với tập 2 của series Tinh Hoa Cờ Tàn, chuyên đề Tàn Binh. Trong lý thuyết cờ tàn quy phạm, Đơn Binh gặp Đơn Sĩ thông thường là cờ hòa nếu bên phòng thủ đi chuẩn xác. Tuy nhiên, nếu Sĩ Đen bị treo cao lạc vị và Tướng Đen bị ép lệch góc, bên Đỏ hoàn toàn có thể khéo thắng bằng nghệ thuật dùng mặt Tướng ghim Sĩ vô cùng tinh diệu. Chúng ta cùng phân tích thế cờ mẫu mực này.",
            "insight": "ĐỎ ĐI TRƯỚC  •  MỤC TIÊU: GHIM SĨ ÉP BÍ",
            "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
            "moves": [],
            "pause": 2.0,
            "spotlight": "f1"
        },
        {
            "label": "NƯỚC ĐẦU",
            "headline": "1. Tướng 4 bình 5",
            "narration": "Nước cờ mở màn then chốt: Đỏ đi Tướng 4 bình 5 chiếm lĩnh trung lộ! Nước đi này vừa khống chế trục giữa của bàn cờ, vừa chuẩn bị điều Tướng sang cánh bên để ép chặt Tướng Đen. Lúc này, Tướng Đen không thể ra giữa, còn Sĩ Đen ở góc cao cũng không dám thoái về tâm vì sẽ bị Tốt Đỏ ăn mất ngay. Đen buộc phải dâng Tướng lên lầu hai.",
            "insight": "CHIẾM TRUNG LỘ  •  TƯỚNG 4 BÌNH 5",
            "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
            "moves": ["f7e7"],
            "pause": 1.5,
            "spotlight": "e7"
        },
        {
            "label": "ĐEN ĐÁP",
            "headline": "1... Tướng 4 tiến 1",
            "narration": "Đen buộc phải đi Tướng 4 tiến 1 lên lầu hai để tạm thời né tránh. Nếu vội vàng thoái Sĩ về tâm, Tốt Đỏ chỉ việc ăn Sĩ là thắng cờ dễ dàng.",
            "insight": "ĐEN BẮT BUỘC  •  TƯỚNG LÊN LẦU 2",
            "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
            "moves": ["f7e7", "d0d1"],
            "pause": 1.2,
            "spotlight": "d1"
        },
        {
            "label": "GHIM QUÂN",
            "headline": "2. Tướng 5 bình 6 (Ghim Sĩ)",
            "narration": "Đỏ lập tức ra đòn độc hiểm: Tướng 5 bình 6! Tướng Đỏ chiếm lộ sáu đối diện thẳng hàng với Tướng Đen. Nước đi này tạo ra thế ghim chết Sĩ Đen ở giữa theo luật lộ mặt Tướng. Sĩ Đen bị trói chặt hoàn toàn, không thể di chuyển đi bất kỳ đâu!",
            "insight": "ĐÒN GHIM MẶT TƯỚNG  •  SĨ ĐEN TÊ LIỆT",
            "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
            "moves": ["f7e7", "d0d1", "e7d7"],
            "pause": 1.6,
            "spotlight": "d7"
        },
        {
            "label": "ĐEN THOÁI",
            "headline": "2... Tướng 4 thoái 1",
            "narration": "Đứng trước đòn ghim nghiệt ngã, Sĩ không thể nhúc nhích, Tướng Đen không thể sang lộ năm, chỉ có duy nhất một nước đi hợp lệ là Tướng 4 thoái 1 lùi về đáy cung.",
            "insight": "ĐEN HẾT ĐƯỜNG  •  TƯỚNG THOÁI VỀ ĐÁY",
            "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
            "moves": ["f7e7", "d0d1", "e7d7", "d1d0"],
            "pause": 1.2,
            "spotlight": "d0"
        },
        {
            "label": "TUYỆT SÁT",
            "headline": "3. Binh 4 bình 5 (Khốn Tử Tuyệt Sát)",
            "narration": "Đỏ ung dung tung nhát kiếm kết liễu: Binh 4 bình 5! Tốt Đỏ nhập tâm khóa chặt trung lộ. Lúc này Sĩ Đen dù đứng cạnh Tốt nhưng tuyệt đối không thể ăn Tốt vì sẽ phạm luật lộ mặt Tướng. Tướng Đen bị kẹt cứng ở góc không còn bất kỳ nước đi nào hợp lệ. Đen rơi vào thế khốn tử tuyệt sát và chấp nhận thua cuộc!",
            "insight": "TỐT NHẬP TÂM  •  SĨ BỊ GHIM CHẾT",
            "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
            "moves": ["f7e7", "d0d1", "e7d7", "d1d0", "f1e1"],
            "pause": 2.5,
            "spotlight": "e1"
        },
        {
            "label": "BÀI HỌC",
            "headline": "Quy phạm: Khi nào Đơn Sĩ thủ hòa?",
            "narration": "Tổng kết bài học: Đơn Binh chỉ khéo thắng khi Sĩ đối phương bị treo cao lạc vị và Tướng bị đẩy lệch cánh. Nếu bên phòng thủ luôn giữ Sĩ ở trung tâm che chở cho Tướng, Đơn Binh không thể tạo thế ghim và ván cờ sẽ hòa. Nắm vững bí quyết này sẽ giúp bạn tấn công sắc bén và phòng thủ vững vàng trong thực chiến. Hẹn gặp lại các bạn ở tập tiếp theo!",
            "insight": "BÍ QUYẾT: SĨ GIỮ TÂM THÌ HÒA  •  SĨ LẠC VỊ THÌ BẠI",
            "fen": "3k5/5P3/3a5/9/9/9/9/5K3/9/9 w",
            "moves": [],
            "pause": 2.5,
            "spotlight": "d2"
        }
    ]
}

if __name__ == '__main__':
    OUT_FILE.write_text(json.dumps(EPISODE_002, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Successfully built {OUT_FILE}')

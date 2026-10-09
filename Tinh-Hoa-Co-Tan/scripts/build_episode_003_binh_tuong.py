"""Build Episode 003: ĐƠN BINH ĐỐI ĐƠN TƯỢNG (THẾ HÒA QUY PHẠM).
Lý thuyết cờ tàn chuẩn mực: Đơn Binh Tất Hòa Đơn Tượng.
Minh họa nghệ thuật dùng Tượng bay chuyển cánh hóa giải hoàn toàn Đơn Binh.
"""
import json
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parents[1] / 'episodes' / 'tap-0003.json'

EPISODE_003 = {
    "id": "tap-0003",
    "title": "ĐƠN BINH ĐỐI ĐƠN TƯỢNG",
    "subtitle": "Thế hòa quy phạm • Tuyệt kỹ dùng Tượng chuyển cánh thủ hòa trước Đơn Binh.",
    "category": "Tàn Binh",
    "goal_text": "MỤC TIÊU: THỦ HÒA QUY PHẠM",
    "fen": "4k1b2/9/9/3P5/9/9/9/3K5/9/9 w",
    "analysis_status": "four_piece_pawn_elephant_retrograde",
    "verification_note": "Canonical draw endgame verified: Single Soldier cannot defeat Single Elephant. Black Elephant maneuvers between files 3, 5, 7 ensuring a solid draw.",
    "beats": [
        {
            "label": "KỲ LÝ",
            "headline": "Kỳ lý chuẩn mực: Đơn Binh có thắng được Đơn Tượng?",
            "narration": "Chào mừng các bạn đến với tập 3 của series Tinh Hoa Cờ Tàn, chuyên đề Tàn Binh. Trong kỳ lý cờ tướng quy phạm, cổ nhân đúc kết: Đơn Binh tất hòa Đơn Tượng! Đơn Binh tuyệt đối không thể thắng được Đơn Tượng nếu bên phòng thủ đi chuẩn xác. Tượng có đặc tính bay rộng hai cánh, trong khi Binh đi chậm từng bước một. Hôm nay, chúng ta cùng thưởng thức nghệ thuật dùng Tượng bay chuyển cánh để thủ hòa nhàn nhã trước Đơn Binh.",
            "insight": "KỲ LÝ CỐT LÕI  •  ĐƠN BINH TẤT HÒA ĐƠN TƯỢNG",
            "fen": "4k1b2/9/9/3P5/9/9/9/3K5/9/9 w",
            "moves": [],
            "pause": 2.2,
            "spotlight": "d3"
        },
        {
            "label": "ĐỎ ÁP SÁT",
            "headline": "1. Binh 6 tiến 1 — 1... Tượng 3 tiến 5",
            "narration": "Bên Đỏ tìm cách gây áp lực: Binh 6 tiến 1 áp sát hàng hai. Đen ung dung đối phó bằng nước cờ mẫu mực: Tượng 3 tiến 5! Tượng Đen bay thẳng lên trung tâm chiếm giữ vị trí đắc địa, sẵn sàng cơ động chuyển cánh.",
            "insight": "TƯỢNG LÊN TÂM  •  TƯỢNG 3 TIẾN 5",
            "fen": "4k1b2/9/9/3P5/9/9/9/3K5/9/9 w",
            "moves": ["d3d2", "g0e2"],
            "pause": 1.6,
            "spotlight": "e2"
        },
        {
            "label": "ĐEN CHUYỂN CÁNH",
            "headline": "2. Binh 6 tiến 1 — 2... Tượng 5 tiến 7",
            "narration": "Đỏ tiến tiếp Binh 6 tiến 1 ép xuống hàng đáy. Đen thể hiện đẳng cấp phòng thủ nhẹ nhàng: Tượng 5 tiến 7! Tượng Đen bay lên bờ sông lộ bảy, hoàn toàn thoát khỏi tầm uy hiếp của Binh Đỏ.",
            "insight": "BAY LÊN HÀ  •  TƯỢNG 5 TIẾN 7",
            "fen": "4k1b2/9/9/3P5/9/9/9/3K5/9/9 w",
            "moves": ["d3d2", "g0e2", "d2d1", "e2c4"],
            "pause": 1.6,
            "spotlight": "c4"
        },
        {
            "label": "ĐỎ ĐUỔI THEO",
            "headline": "3. Binh 6 bình 7 — 3... Tượng 7 thoái 5",
            "narration": "Đỏ sốt ruột đi Binh 6 bình 7 đuổi theo sang lộ bảy. Đen điềm tĩnh đi Tượng 7 thoái 5 bay ngược trở lại trung tâm. Binh Đỏ đuổi đằng tây thì Tượng Đen bay sang đằng đông!",
            "insight": "VỀ LẠI TÂM  •  TƯỢNG 7 THOÁI 5",
            "fen": "4k1b2/9/9/3P5/9/9/9/3K5/9/9 w",
            "moves": ["d3d2", "g0e2", "d2d1", "e2c4", "d1c1", "c4e2"],
            "pause": 1.6,
            "spotlight": "e2"
        },
        {
            "label": "HÓA GIẢI HOÀN TOÀN",
            "headline": "4. Binh 7 bình 8 — 4... Tượng 5 thoái 3",
            "narration": "Đỏ tiếp tục bình Binh sang lộ tám. Đen chỉ việc đi Tượng 5 thoái 3 trở về vị trí xuất phát ban đầu. Ván cờ lặp lại tuần hoàn, Đỏ hoàn toàn bất lực. Kể cả Đỏ có tìm cách bắt Tượng thì Binh cũng chìm xuống đáy biến thành Binh lụt tàn phế, gặp Đơn Tướng ván cờ vẫn hòa tuyệt đối!",
            "insight": "HÓA GIẢI HOÀN TOÀN  •  THẾ HÒA QUY PHẠM",
            "fen": "4k1b2/9/9/3P5/9/9/9/3K5/9/9 w",
            "moves": ["d3d2", "g0e2", "d2d1", "e2c4", "d1c1", "c4e2", "c1b1", "e2g0"],
            "pause": 2.2,
            "spotlight": "g0"
        },
        {
            "label": "TỔNG KẾT",
            "headline": "Khẩu quyết kinh điển: Đơn Binh tất hòa Đơn Tượng",
            "narration": "Tổng kết bài học: Đơn Binh đối Đơn Tượng là thế hòa quy phạm kinh điển của cờ tướng. Người cầm Đen khi chỉ còn Đơn Tượng hãy tự tin bay Tượng nhịp nhàng hai cánh để giữ vững thế hòa. Người cầm Đỏ khi chỉ còn Đơn Binh hãy hiểu rõ kỳ lý để chủ động đề nghị hòa cờ, tránh kéo dài vô ích. Cảm ơn các bạn đã theo dõi tập 3, hẹn gặp lại ở chuyên đề Song Binh!",
            "insight": "BÍ QUYẾT: TƯỢNG BAY HAI CÁNH VỮNG NHƯ THÀNH",
            "fen": "4k1b2/9/9/3P5/9/9/9/3K5/9/9 w",
            "moves": [],
            "pause": 2.5,
            "spotlight": "e0"
        }
    ]
}

if __name__ == '__main__':
    OUT_FILE.write_text(json.dumps(EPISODE_003, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Successfully built {OUT_FILE}')

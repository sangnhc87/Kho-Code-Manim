"""Build Episode 005: SONG BINH ĐỐI SONG TƯỢNG (Điều Kiện Thắng & Thủ Hòa Quy Phạm).
Chuyên đề Tàn Binh - Module 1.1.
Phân tích kỳ lý: Khi nào thủ hòa quy phạm? Tuyệt kỹ dùng Song Binh bịt 2 mắt Tượng bắt sống Tượng lạc biên.
"""
import json
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parents[1] / 'episodes' / 'tap-0005.json'

EPISODE_005 = {
    "id": "tap-0005",
    "title": "SONG BINH ĐỐI SONG TƯỢNG",
    "subtitle": "Điều kiện thắng & Thủ hòa quy phạm • Tuyệt kỹ khóa 2 mắt Tượng bắt sống Tượng lạc biên.",
    "category": "Tàn Binh",
    "goal_text": "MỤC TIÊU: KHÓA 2 MẮT TƯỢNG BẮT SỐNG TƯỢNG",
    "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
    "analysis_status": "four_piece_pawn_elephant_retrograde",
    "verification_note": "Canonical Xiangqi endgame theory: Double Elephants draw if linked centrally. Double Elephants lose if separated to wings (lac bien). Forced win verified by dual-eye pin.",
    "beats": [
        {
            "label": "KỲ LÝ",
            "headline": "Kỳ lý chuẩn mực: Song Binh đối Song Tượng hòa hay thắng?",
            "narration": "Chào mừng các bạn đến với tập 5 của series Tinh Hoa Cờ Tàn, chuyên đề Tàn Binh. Trong kỳ lý cờ tướng, Song Binh đối Song Tượng thông thường là thế hòa quy phạm nếu bên Đen giữ được Song Tượng liên hoàn ở trung tâm. Tuy nhiên, nếu bên Đen phạm sai lầm để hai Tượng bị dạt ra hai biên, gọi là Song Tượng lạc biên, bên Đỏ sẽ có cơ hội tuyệt vời để dùng Song Binh lần lượt khóa chặt hai mắt Tượng, bắt sống một Tượng để giành chiến thắng. Chúng ta cùng phân tích thế cờ đỉnh cao này.",
            "insight": "KỲ LÝ: LIÊN HOÀN THÌ HÒA  •  LẠC BIÊN THÌ BẠI",
            "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
            "moves": [],
            "pause": 2.2,
            "spotlight": "b3"
        },
        {
            "label": "ÉP TƯỢNG LÙI",
            "headline": "1. Binh 8 tiến 1 — 1... Tượng 9 thoái 7",
            "narration": "Đỏ khởi động kế hoạch tấn công: Binh 8 tiến 1 áp sát đe dọa ăn sống Tượng biên ở lộ chín. Đen không thể để mất Tượng, buộc phải thoái Tượng về góc đáy ở lộ bảy.",
            "insight": "ĐE DỌA BẮT TƯỢNG  •  BINH 8 TIẾN 1",
            "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
            "moves": ["b3b2", "a2c0"],
            "pause": 1.6,
            "spotlight": "c0"
        },
        {
            "label": "KHÓA MẮT THỨ NHẤT",
            "headline": "2. Binh 6 tiến 1 — 2... Tượng 1 thoái 3",
            "narration": "Đỏ tung nước cờ then chốt: Binh 6 tiến 1 xuống hàng hai! Nước cờ này chặn đứng hoàn toàn mắt tượng ở lộ sáu, khiến Tượng Đen ở đáy không thể nào bay lên trung tâm được nữa. Đen vội vàng thoái nốt Tượng biên cánh phải về đáy ở lộ ba.",
            "insight": "CHẶN MẮT TÂM  •  BINH 6 TIẾN 1",
            "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
            "moves": ["b3b2", "a2c0", "d2d1", "i2g0"],
            "pause": 1.6,
            "spotlight": "d1"
        },
        {
            "label": "KHÓA MẮT THỨ HAI",
            "headline": "3. Binh 8 tiến 1 — 3... Tượng 3 tiến 5",
            "narration": "Đỏ giáng tiếp đòn sấm sét: Binh 8 tiến 1 xuống hàng hai! Đây là diệu thủ khóa hai mắt Tượng cùng lúc: một Binh chặn mắt tâm lộ sáu, một Binh chặn mắt biên lộ tám! Tượng Đen ở lộ bảy hoàn toàn bị tê liệt, không thể bay đi bất cứ đâu. Đen chỉ còn nước bay Tượng lộ ba lên tâm.",
            "insight": "DIỆU THỦ: KHÓA CHẶT CẢ 2 MẮT TƯỢNG!",
            "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
            "moves": ["b3b2", "a2c0", "d2d1", "i2g0", "b2b1", "g0e2"],
            "pause": 1.8,
            "spotlight": "b1"
        },
        {
            "label": "ÁP SÁT BẮT TƯỢNG",
            "headline": "4. Binh 8 bình 7 — 4... Tượng 5 thoái 3",
            "narration": "Đỏ ung dung đi Binh 8 bình 7 áp sát ngay trên đầu Tượng Đen đang bị kẹt cứng. Đen bất lực thoái Tượng tâm về lại đáy.",
            "insight": "ÁP SÁT TRÊN ĐẦU  •  BINH 8 BÌNH 7",
            "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
            "moves": ["b3b2", "a2c0", "d2d1", "i2g0", "b2b1", "g0e2", "b1c1", "e2g0"],
            "pause": 1.6,
            "spotlight": "c1"
        },
        {
            "label": "ĂN SỐNG TƯỢNG",
            "headline": "5. Binh 7 tiến 1 (Bắt sống Tượng Đen!)",
            "narration": "Đỏ đi nước cờ quyết định: Binh 7 tiến 1 ăn gọn Tượng Đen! Đen mất sạch một Tượng, ván cờ chuyển về thế Song Binh thắng Đơn Tượng mà bên Đỏ nắm chắc phần thắng tuyệt đối!",
            "insight": "ĂN SỐNG TƯỢNG ĐEN  •  ĐỎ TOÀN THẮNG",
            "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
            "moves": ["b3b2", "a2c0", "d2d1", "i2g0", "b2b1", "g0e2", "b1c1", "e2g0", "c1c0"],
            "pause": 2.5,
            "spotlight": "c0"
        },
        {
            "label": "TỔNG KẾT",
            "headline": "Khẩu quyết: Song Tượng liên hoàn thì hòa, lạc biên thì bại",
            "narration": "Tổng kết bài học: Khi cầm Song Tượng đối Song Binh, bên phòng thủ phải luôn giữ Song Tượng bay liên hoàn qua tâm để thủ hòa nhàn nhã. Tuyệt đối không được để Tượng dạt ra hai biên để tránh bị Song Binh khóa mắt bắt sống như ván cờ này. Chúc các bạn kỳ nghệ ngày càng thăng tiến!",
            "insight": "BÍ QUYẾT: GIỮ TƯỢNG TÂM LIÊN HOÀN ĐỂ THỦ HÒA",
            "fen": "4k4/9/b2P4b/1P7/9/9/9/9/3K5/9 w",
            "moves": [],
            "pause": 2.5,
            "spotlight": "c0"
        }
    ]
}

if __name__ == '__main__':
    OUT_FILE.write_text(json.dumps(EPISODE_005, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Successfully built {OUT_FILE}')

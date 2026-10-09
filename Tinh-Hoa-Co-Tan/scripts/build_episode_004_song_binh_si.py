"""Build Episode 004: SONG BINH PHÁ SONG SĨ (Song Binh Thắng Song Sĩ).
Chuyên đề Tàn Binh - Module 1.1.
Tuyệt kỹ thí Binh xé lẻ Song Sĩ & Sát cục kinh điển.
"""
import json
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parents[1] / 'episodes' / 'tap-0004.json'

EPISODE_004 = {
    "id": "tap-0004",
    "title": "SONG BINH PHÁ SONG SĨ",
    "subtitle": "Đỏ đi trước • Tuyệt kỹ thí Binh xé lẻ Song Sĩ & Sát cục kinh điển.",
    "category": "Tàn Binh",
    "goal_text": "MỤC TIÊU: PHÁ SONG SĨ & SÁT CỤC",
    "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
    "analysis_status": "four_piece_pawn_advisor_retrograde",
    "verification_note": "Exact 5-piece K+2P vs k+2a retrograde analysis. Red delivers a forced checkmate with pawn sacrifice and rib penetration.",
    "beats": [
        {
            "label": "THẾ CỜ",
            "headline": "Đỏ đi trước — Song Binh cao thắng Song Sĩ",
            "narration": "Chào mừng các bạn đến với tập 4 của series Tinh Hoa Cờ Tàn, chuyên đề Tàn Binh. Trong kỳ lý cờ tướng, nếu như Đơn Binh bất lực trước Song Sĩ thì Song Binh còn ở hàng cao lại hoàn toàn có thể phá tan phòng tuyến Song Sĩ để giành chiến thắng. Trong thế cờ này, Đỏ sở hữu Song Binh cao ở lộ năm và lộ sáu cùng mặt Tướng chiếm lộ sáu trợ lực. Đen có Tướng và Song Sĩ liên hoàn ở hàng đáy. Chúng ta cùng chiêm ngưỡng nghệ thuật phối hợp đỉnh cao của Song Binh.",
            "insight": "ĐỎ ĐI TRƯỚC  •  MỤC TIÊU: PHÁ CUNG SÁT CỤC",
            "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
            "moves": [],
            "pause": 2.2,
            "spotlight": "e2"
        },
        {
            "label": "THÍ BINH",
            "headline": "1. Binh 5 tiến 1",
            "narration": "Đỏ mở màn bằng nước cờ sấm sét: Binh 5 tiến 1! Đỏ dũng cảm thí Binh đâm thẳng vào tâm cung chiếu tướng! Nước cờ diệu thủ này ép một trong hai Sĩ Đen buộc phải ăn lên tâm, xé tan hoàn toàn cấu trúc Song Sĩ liên hoàn ở hàng đáy.",
            "insight": "DIỆU THỦ THÍ BINH  •  BINH 5 TIẾN 1",
            "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
            "moves": ["e2e1"],
            "pause": 1.6,
            "spotlight": "e1"
        },
        {
            "label": "ĐEN ĂN LÊN",
            "headline": "1... Sĩ 6 tiến 5",
            "narration": "Đen không có lựa chọn nào khác, buộc phải đi Sĩ 6 tiến 5 ăn Binh Đỏ. Lúc này hàng đáy của Đen đã xuất hiện lỗ hổng chí mạng ở góc lộ sáu.",
            "insight": "ĐEN BUỘC ĂN  •  SĨ 6 TIẾN 5",
            "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
            "moves": ["e2e1", "d0e1"],
            "pause": 1.5,
            "spotlight": "e1"
        },
        {
            "label": "BINH HAI ÁP SÁT",
            "headline": "2. Binh 6 tiến 1",
            "narration": "Binh thứ hai của Đỏ lập tức xuất trận: Binh 6 tiến 1 áp sát hàng hai! Nước cờ này khóa chặt góc lộ sáu và khống chế hoàn toàn cửa cung nhờ có mặt Tướng Đỏ ở lộ sáu làm điểm tựa.",
            "insight": "KHÓA CỬA CUNG  •  BINH 6 TIẾN 1",
            "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
            "moves": ["e2e1", "d0e1", "d2d1"],
            "pause": 1.6,
            "spotlight": "d1"
        },
        {
            "label": "ĐEN GIÃY GIỤA",
            "headline": "2... Sĩ 5 tiến 4",
            "narration": "Đen tuyệt vọng nhảy Sĩ 5 tiến 4 tìm đường thoát thân. Tướng Đen ở đáy lúc này đã hoàn toàn bị cô lập, không còn lối thoát.",
            "insight": "SĨ BỎ VỊ  •  TƯỚNG ĐEN CÔ LẬP",
            "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
            "moves": ["e2e1", "d0e1", "d2d1", "e1d2"],
            "pause": 1.5,
            "spotlight": "d2"
        },
        {
            "label": "SÁT CỤC",
            "headline": "3. Binh 6 tiến 1 (Chiếu bí!)",
            "narration": "Đỏ tung đòn kết liễu hoàn hảo: Binh 6 tiến 1 đâm thẳng xuống đáy! Chiếu bí! Tướng Đen bị Binh Đỏ khóa chặt, bên phải vướng Sĩ của chính mình, bên trái bị mặt Tướng Đỏ khống chế lộ sáu. Bên Đen chính thức buông cờ chịu thua!",
            "insight": "ĐÂM ĐÁY CHIẾU BÍ  •  ĐỎ TOÀN THẮNG",
            "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
            "moves": ["e2e1", "d0e1", "d2d1", "e1d2", "d1d0"],
            "pause": 2.5,
            "spotlight": "d0"
        },
        {
            "label": "TỔNG KẾT",
            "headline": "Khẩu quyết: Song Binh cao tất thắng Song Sĩ",
            "narration": "Tổng kết bài học: Song Binh cao phối hợp mặt Tướng là vũ khí sắc bén để phá Song Sĩ. Bí quyết cốt lõi là thí một Binh vào tâm cung để xé lẻ Song Sĩ liên hoàn, sau đó dùng Binh còn lại kết hợp mặt Tướng khóa sườn đâm đáy kết liễu. Chúc các bạn vận dụng thành công tuyệt kỹ này trong thực chiến!",
            "insight": "BÍ QUYẾT: THÍ BINH VÀO TÂM  •  KHÓA SƯỜN ĐÂM ĐÁY",
            "fen": "3aka3/9/3PP4/9/9/9/9/9/3K5/9 w",
            "moves": [],
            "pause": 2.5,
            "spotlight": "d0"
        }
    ]
}

if __name__ == '__main__':
    OUT_FILE.write_text(json.dumps(EPISODE_004, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Successfully built {OUT_FILE}')

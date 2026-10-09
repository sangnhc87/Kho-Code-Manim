"""Build Episode 001: ĐƠN BINH THẮNG ĐƠN TƯỚNG (Quy Tắc Tốt Cao Nhập Cung).
Validated by exact retrograde solver (solve_binh_tuong.py).
"""
import json
from pathlib import Path

OUT_FILE = Path(__file__).resolve().parents[1] / 'episodes' / 'tap-0001.json'

EPISODE_001 = {
    "id": "tap-0001",
    "title": "ĐƠN BINH THẮNG ĐƠN TƯỚNG",
    "subtitle": "Đỏ đi trước • Tuyệt kỹ Tốt cao nhập cung & Bài học Tốt kỵ trầm đáy.",
    "category": "Tàn Binh",
    "goal_text": "MỤC TIÊU: ÉP SÁT TƯỚNG ĐEN",
    "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
    "analysis_status": "three_piece_pawn_retrograde",
    "verification_note": "Exact 3-piece retrograde solver for K+P vs k. Stalemate and checkmate win conditions verified under Vietnamese Xiangqi rules.",
    "beats": [
        {
            "label": "THẾ CỜ",
            "headline": "Đỏ đi trước — Tốt khéo thắng Tướng",
            "narration": "Chào mừng các bạn đến với tập đầu tiên của series Tinh Hoa Cờ Tàn, chuyên đề Tàn Binh. Trong cờ tàn thực chiến, Đơn Binh thắng Đơn Tướng là bài học vỡ lòng căn bản nhất. Nhiều người nghĩ một Tốt không thể thắng nổi Tướng, nhưng nếu biết cách phối hợp mặt Tướng để Tốt chiếm lĩnh các cứ điểm hiểm yếu, Đỏ hoàn toàn có thể ép Tướng Đen vào thế khốn tử tuyệt sát. Tuy nhiên, nếu đi sai, Tốt rơi xuống đáy bàn cờ sẽ biến thành Tốt tịt và bị hòa cuộc. Chúng ta cùng phân tích chi tiết thế trận này.",
            "insight": "ĐỎ ĐI TRƯỚNG  •  MỤC TIÊU: ÉP SÁT TƯỚNG ĐEN",
            "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": [],
            "pause": 2.0,
            "spotlight": "d2"
        },
        {
            "label": "NƯỚC ĐẦU",
            "headline": "1. Binh 6 tiến 1",
            "narration": "Nước cờ đầu tiên chuẩn xác: Đỏ đi Binh 6 tiến 1! Đây là nước đi mấu chốt để giữ thế Tốt cao, khống chế chặt chẽ hàng hai của cung đối phương. Đứng trước nước cờ này, Tướng Đen không thể tiến lên lộ năm vì Tốt Đỏ đang kiểm soát, cũng không thể bình sang lộ bốn vì mặt Tướng Đỏ đang khống chế. Nước đi hợp lệ duy nhất của Đen là bình Tướng sang lộ sáu tránh đòn.",
            "insight": "GIỮ THẾ TỐT CAO  •  BINH 6 TIẾN 1",
            "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1"],
            "pause": 1.5,
            "spotlight": "d1"
        },
        {
            "label": "ĐEN ĐÁP",
            "headline": "1... Tướng 5 bình 6",
            "narration": "Đen buộc phải đi Tướng 5 bình 6, dạt sang góc cung bên cánh trái. Tướng Đen tạm thời thoát khỏi trung lộ nhưng đã bị đẩy vào góc chết.",
            "insight": "ĐEN BẮT BUỘC  •  TƯỚNG DẠT RA GÓC",
            "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "e0f0"],
            "pause": 1.2,
            "spotlight": "f0"
        },
        {
            "label": "TUYỆT SÁT",
            "headline": "2. Binh 6 bình 5 (Tuyệt Sát)",
            "narration": "Đỏ tung đòn quyết định: Binh 6 bình 5 chiếu tướng! Tốt Đỏ nhập tâm chiếm lĩnh trung lộ của cung Đen. Tướng Đen tại vị trí này hoàn toàn tê liệt: không thể tiến một lên lầu hai vì Tốt Đỏ khống chế, cũng không thể bình sang trung lộ vì Tốt Đỏ đang đứng chiếu trực tiếp. Đen rơi vào thế tuyệt sát, hết nước đi và chịu thua tâm phục khẩu phục!",
            "insight": "TỐT NHẬP TÂM  •  CHIẾU BÍ TUYỆT SÁT",
            "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "e0f0", "d1e1"],
            "pause": 2.5,
            "spotlight": "e1"
        },
        {
            "label": "BIẾN SAI LẦM",
            "headline": "Cạm bẫy: Tốt kỵ trầm đáy!",
            "narration": "Bây giờ chúng ta cùng xem xét biến đi sai lầm đắt giá: Sau khi Đen dạt Tướng ra góc ở nước thứ nhất, nếu Đỏ nôn nóng đi Binh 6 tiến 1 xuống đáy bàn cờ. Đây là sai lầm chí mạng! Tốt khi xuống đáy sẽ biến thành Tốt tịt, hoàn toàn mất khả năng kiểm soát hàng hai.",
            "insight": "SAI LẦM: TỐT XUỐNG ĐÁY BÀN CỜ",
            "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "e0f0", "d1d0"],
            "pause": 1.8,
            "spotlight": "d0"
        },
        {
            "label": "HÒA CUỘC",
            "headline": "2... Tướng 6 tiến 1 (Thủ Hòa)",
            "narration": "Nhận thấy Tốt Đỏ đã trầm đáy vô hại, Đen lập tức đi Tướng 6 tiến 1 leo lên lầu hai! Lúc này Tốt Đỏ ở đáy chỉ có thể bò ngang lạch bạch, vĩnh viễn không thể chiếu tới Tướng Đen. Trận đấu khép lại với kết quả hòa cuộc đầy tiếc nuối cho bên Đỏ.",
            "insight": "TƯỚNG LÊN LẦU 2  •  ĐEN THỦ HÒA",
            "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": ["d2d1", "e0f0", "d1d0", "f0f1"],
            "pause": 2.0,
            "spotlight": "f1"
        },
        {
            "label": "BÀI HỌC",
            "headline": "Bí quyết: Tốt cao khóa cung",
            "narration": "Bài học cốt tử của tập hôm nay: Trong tàn cuộc Đơn Binh thắng Đơn Tướng, Tốt phải luôn giữ ở vị trí Tốt cao, phối hợp cùng mặt Tướng khống chế đường đi của đối phương rồi nhập tâm dứt điểm. Tuyệt đối không được để Tốt trầm đáy. Cảm ơn các bạn đã theo dõi, hẹn gặp lại ở tập tiếp theo!",
            "insight": "GHI NHỚ: GIỮ TỐT CAO  •  KỴ TRẦM ĐÁY",
            "fen": "4k4/9/3P5/9/9/9/9/3K5/9/9 w",
            "moves": [],
            "pause": 2.5,
            "spotlight": "d2"
        }
    ]
}

if __name__ == '__main__':
    OUT_FILE.write_text(json.dumps(EPISODE_001, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Successfully built {OUT_FILE}')

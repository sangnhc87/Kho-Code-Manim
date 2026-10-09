"""
Bộ siêu dữ liệu chuẩn hóa cho 2 khóa học toán học trực quan của Thầy Nguyễn Văn Sang:
1. Series Trải Phẳng Hình Học Không Gian 3D (20 bài)
2. Series Đại Số Tổ Hợp & Xác Suất (25 bài)
Tiêu đề tối đa 95 ký tự để tương thích tuyệt đối với quy định YouTube Data API.
"""

AUTHOR_INFO = """
👨‍🏫 Giảng viên: Thầy Nguyễn Văn Sang
📌 Dự án: Toán Trực Quan Bằng Hoạt Họa Manim & Typst
🔔 Đăng ký kênh để theo dõi trọn bộ bài giảng Toán THPT & Luyện thi Đại học chất lượng cao!
"""

# ==============================================================================
# KHÓA HỌC 1: KỸ THUẬT TRẢI PHẲNG HÌNH HỌC KHÔNG GIAN 3D (20 BÀI)
# ==============================================================================
PLAYLIST_TRAI_PHANG = {
    "title": "Hình Học Không Gian: Kỹ Thuật Trải Phẳng & Cực Trị Đường Đi Ngắn Nhất - Thầy Nguyễn Văn Sang",
    "description": "Trọn bộ 20 bài giảng trực quan hóa 3D phương pháp trải phẳng giải quyết bài toán tìm đường đi ngắn nhất, cực trị hình học không gian THPT và bồi dưỡng HSG."
}

TRAI_PHANG_LESSONS = {
    1: {
        "title": "Bài 01: Trải Phẳng 2 Mặt Khối Lập Phương | Bài Toán Kiến Bò - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D
Chuyên đề: Cực trị khoảng cách & Đường đi ngắn nhất trên đa diện

Nội dung bài 01:
- Khái niệm mở phẳng (unfolding) 2 mặt kề nhau quanh bản lề chung.
- Khảo sát mô hình kinh điển: Quãng đường ngắn nhất giữa 2 điểm trên mặt khối lập phương.
- Định lý đoạn thẳng nối 2 điểm là đường ngắn nhất trên mặt phẳng trải.

{AUTHOR_INFO}
#Toan11 #Toan12 #HinhHocKhongGian #TraiPhang #Manim #ThayNguyenVanSang #CucTriHinhHoc""",
        "tags": ["hình học không gian", "trải phẳng", "cực trị hình học", "manim", "thầy nguyễn văn sang", "toán 11", "toán 12", "lập phương"],
        "file_pattern": "trai_phang_01"
    },
    2: {
        "title": "Bài 02: Trải Phẳng 4 Mặt Xung Quanh Khối Lập Phương - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 02:
- Phương pháp trải phẳng chuỗi 4 mặt xung quanh của khối lập phương trên cùng một dải băng.
- So sánh các khả năng đi qua mặt đáy so với đi vòng quanh các mặt bên.
- Kỹ thuật tính khoảng cách Pythagoras trên lưới trải phẳng.

{AUTHOR_INFO}
#Toan11 #Toan12 #HinhHocKhongGian #TraiPhang #Manim #ThayNguyenVanSang""",
        "tags": ["hình học không gian", "trải phẳng", "khối lập phương", "toán 11", "toán 12", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_02"
    },
    3: {
        "title": "Bài 03: Trải Phẳng 5 Mặt Hình Hộp Chữ Nhật | Mô Hình Không Nắp - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 03:
- Mô hình hộp chữ nhật không nắp kích thước 3 chiều a, b, c.
- Biện luận lộ trình di chuyển khi điểm xuất phát và điểm đích nằm ở các vị trí đối xứng.
- Quy tắc so sánh tổng bình phương trên các mặt phẳng mở khác nhau.

{AUTHOR_INFO}
#HinhHocKhongGian #HopChuNhat #TraiPhang #Manim #ThayNguyenVanSang""",
        "tags": ["hình hộp chữ nhật", "trải phẳng", "hình học không gian", "toán 12", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_03"
    },
    4: {
        "title": "Bài 04: Trải Phẳng Toàn Phần 6 Mặt Lập Phương | Kiến Bò Kinh Điển - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 04:
- Khảo sát trọn vẹn 6 mặt của khối lập phương: Có bao nhiêu cách trải phẳng hợp lệ?
- Lựa chọn sơ đồ trải phẳng tối ưu để tìm đường đi ngắn nhất giữa 2 đỉnh đối diện.
- Bài toán thực tế kiến bò trên vỏ hộp bánh.

{AUTHOR_INFO}
#BaiToanKienBo #LapPhuong #HinhHocKhongGian #TraiPhang #ThayNguyenVanSang""",
        "tags": ["kiến bò", "lập phương", "trải phẳng 6 mặt", "toán học trực quan"],
        "file_pattern": "trai_phang_04"
    },
    5: {
        "title": "Bài 05: Trải Phẳng Lăng Trụ Tam Giác Đều | Đường Đi Vòng Mặt Bên - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 05:
- Trải phẳng 3 mặt bên của hình lăng trụ tam giác đều thành hình chữ nhật lớn.
- Khảo sát vết cắt của đường đi ngắn nhất trên các cạnh bên.
- Tìm điều kiện tiếp xúc và góc nghiêng tối thiểu.

{AUTHOR_INFO}
#LangTruTamGiac #HinhKhongGian #TraiPhang #ThayNguyenVanSang""",
        "tags": ["lăng trụ tam giác", "trải phẳng", "đường đi ngắn nhất", "toán 11"],
        "file_pattern": "trai_phang_05"
    },
    6: {
        "title": "Bài 06: Trải Phẳng Lăng Trụ Lục Giác Đều | Bài Toán Vòng Đa Diện - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 06:
- Trực quan hóa lăng trụ lục giác đều mở phẳng trên mặt phẳng 2D.
- Đường trắc địa (geodesic) trên mặt lăng trụ.
- Ứng dụng trong bài toán kiến trúc và kết cấu hình học thực tế.

{AUTHOR_INFO}
#LucGiacDeu #LangTru #HinhHocKhongGian #Manim #ThayNguyenVanSang""",
        "tags": ["lục giác đều", "lăng trụ lục giác", "trải phẳng", "toán thpt"],
        "file_pattern": "trai_phang_06"
    },
    7: {
        "title": "Bài 07: Trải Phẳng Khối Tứ Diện Đều | Lưới Tam Giác Đều Đồng Dạng - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 07:
- Khối tứ diện đều ABCD và mô hình trải phẳng 4 mặt tam giác đều.
- Dạng toán tìm đường đi ngắn nhất xuất phát từ một đỉnh đi qua tất cả các mặt bên rồi trở về đỉnh cũ.
- Chu vi thiết diện bé nhất tạo bởi mặt phẳng cắt.

{AUTHOR_INFO}
#TuDienDeu #HinhHocKhongGian #TraiPhang #ThayNguyenVanSang""",
        "tags": ["tứ diện đều", "trải phẳng tứ diện", "toán 11", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_07"
    },
    8: {
        "title": "Bài 08: Trải Phẳng Chóp Tứ Giác Đều | Vòng Dây Quanh Mặt Bên - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 08:
- Mở phẳng 4 mặt bên hình tam giác cân xung quanh đỉnh chóp S.
- Tính góc ở đỉnh của hình quạt ghép tạo bởi 4 mặt phẳng bên.
- Điều kiện tồn tại đường đi khép kín không cắt qua đáy chóp.

{AUTHOR_INFO}
#ChopTuGiacDeu #HinhChop #TraiPhang #Manim #ThayNguyenVanSang""",
        "tags": ["chóp tứ giác đều", "hình chóp", "trải phẳng", "toán 12"],
        "file_pattern": "trai_phang_08"
    },
    9: {
        "title": "Bài 09: Trải Phẳng Hình Chóp Tam Giác S.ABC | Cực Trị Đường Gấp Khúc - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 09:
- Chóp tam giác có các góc phẳng ở đỉnh nhọn.
- Trải phẳng liên hoàn các tam giác mặt bên để thẳng hàng hóa đường gấp khúc.
- Kỹ thuật tính độ dài bằng định lý Cosin trên mặt phẳng mở.

{AUTHOR_INFO}
#ChopTamGiac #HinhHoc3D #TraiPhang #ThayNguyenVanSang""",
        "tags": ["chóp tam giác", "định lý cosin", "trải phẳng", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_09"
    },
    10: {
        "title": "Bài 10: Trải Phẳng Hình Chóp Cụt Vuông | Lộ Trình Tối Ưu Đa Diện - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 10:
- Khảo sát hình chóp cụt vuông với 4 mặt bên là các hình thang cân.
- Trải phẳng các hình thang cân nối tiếp và xác định hình dáng đường trắc địa ngắn nhất.
- Kỹ thuật so sánh giữa đường đi men theo mặt phẳng bên và đường đi qua đáy.

{AUTHOR_INFO}
#ChopCutVuong #HinhChopCut #TraiPhang #Manim #Typst #ThayNguyenVanSang""",
        "tags": ["chóp cụt vuông", "hình chóp cụt", "trải phẳng", "toán trực quan", "manim typst"],
        "file_pattern": "trai_phang_10"
    },
    11: {
        "title": "Bài 11: Trải Phẳng Mặt Trụ Tròn Xoay | Dây Quấn 1 Vòng Quanh Trụ - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 11:
- Khái niệm trải phẳng mặt cong sang hình chữ nhật (chu vi đáy = chiều rộng).
- Bài toán con nhện và con ruồi trên mặt trụ tròn xoay.
- Công thức tổng quát tính chiều dài sợi dây quấn ngắn nhất theo bán kính R và chiều cao h.

{AUTHOR_INFO}
#HinhTru #MatTru #TraiPhang #DayQuan #ThayNguyenVanSang""",
        "tags": ["hình trụ", "mặt trụ", "dây quấn", "toán 12", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_11"
    },
    12: {
        "title": "STAT12: Phương Sai & Độ Lệch Chuẩn Của Mẫu Ghép Nhóm - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 12: Phương sai và độ lệch chuẩn của mẫu số liệu ghép nhóm

Nội dung trọng tâm bài 12:
- Phương pháp tính phương sai và độ lệch chuẩn bằng giá trị đại diện.
- So sánh sự khác biệt giữa tính trên dữ liệu gốc và dữ liệu ghép nhóm.
- Ứng dụng đo mức độ phân tán của dữ liệu ghép nhóm trong thực tế.

{AUTHOR_INFO}
#ThongKe #PhuongSai #DoLechChuan #MauGhepNhom #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["phương sai", "độ lệch chuẩn", "mẫu ghép nhóm", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT12"
    },
    13: {
        "title": "STAT13: So Sánh Hai Mẫu Số Liệu - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 13: So sánh hai mẫu số liệu

Nội dung trọng tâm bài 13:
- Phân tích sự khác biệt giữa hai mẫu số liệu.
- So sánh điểm trung bình và mức độ phân tán (phương sai, độ lệch chuẩn).
- Đánh giá hình dạng phân bố và ý nghĩa thực tế.

{AUTHOR_INFO}
#ThongKe #SoSanhMauSoLieu #Toan10 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["so sánh hai mẫu số liệu", "phương sai", "độ lệch chuẩn", "toán 10", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT13"
    },
    14: {
        "title": "STAT14: Bài Toán Thống Kê Tổng Hợp Và Vận Dụng Thực Tế - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 14: Bài toán thống kê tổng hợp và vận dụng thực tế

Nội dung trọng tâm bài 14:
- Tổng hợp các kiến thức thống kê đã học.
- Ứng dụng để giải quyết bài toán thực tế (ví dụ: chọn quầy phục vụ dựa trên thời gian chờ).
- Đánh giá toàn diện dựa trên số trung bình, trung vị và các độ đo phân tán.

{AUTHOR_INFO}
#ThongKe #TongHopThongKe #VanDungThucTe #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["thống kê tổng hợp", "vận dụng thực tế", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT14"
    }
}


# ==============================================================================
# KHÓA HỌC 2: ĐẠI SỐ TỔ HỢP TỪ NỀN TẢNG ĐẾN OLYMPIAD (25 BÀI)
# ==============================================================================
PLAYLIST_TO_HOP = {
    "title": "Đại Số Tổ Hợp & Xác Suất: Từ Nền Tảng Đến Thực Chiến Olympiad - Thầy Nguyễn Văn Sang",
    "description": "Trọn bộ 25 bài giảng đại số tổ hợp trực quan hóa bằng Manim & Typst. Đi từ quy tắc đếm cơ bản đến phương pháp gộp khối, hàm sinh, bao hàm loại trừ, Burnside và Pólya."
}

TO_HOP_LESSONS = {
    1: {"title": "COMB01: Quy Tắc Cộng | Bản Chất Đếm Rời Rạc & Phân Chia Trường Hợp - Thầy Nguyễn Văn Sang", "file": "COMB01.mp4", "tags": ["quy tắc cộng", "tổ hợp", "toán 10", "đại số tổ hợp", "thầy nguyễn văn sang"]},
    2: {"title": "COMB02: Quy Tắc Nhân | Các Công Đoạn Liên Tiếp & Quy Tắc Cây - Thầy Nguyễn Văn Sang", "file": "COMB02.mp4", "tags": ["quy tắc nhân", "tổ hợp", "toán 10", "phương pháp đếm"]},
    3: {"title": "COMB03: Sơ Đồ Cây & Không Gian Mẫu | Trực Quan Hóa Khả Năng Rời Rạc - Thầy Nguyễn Văn Sang", "file": "COMB03.mp4", "tags": ["sơ đồ cây", "không gian mẫu", "xác suất", "tổ hợp"]},
    4: {"title": "COMB04: Thứ Tự Có Quan Trọng? | Phân Biệt Hoán Vị, Chỉnh Hợp, Tổ Hợp - Thầy Nguyễn Văn Sang", "file": "COMB04.mp4", "tags": ["thứ tự", "hoán vị", "chỉnh hợp", "tổ hợp", "phân biệt"]},
    5: {"title": "COMB05: Hoán Vị (Permutations) | Sắp Xếp N Phần Tử & Giai Thừa n! - Thầy Nguyễn Văn Sang", "file": "COMB05.mp4", "tags": ["hoán vị", "giai thừa", "toán 10", "thầy nguyễn văn sang"]},
    6: {"title": "COMB06: Chỉnh Hợp A(n, k) | Chọn & Sắp Thứ Tự K Phần Tử Từ N - Thầy Nguyễn Văn Sang", "file": "COMB06.mp4", "tags": ["chỉnh hợp", "A_n_k", "toán 10", "đại số tổ hợp"]},
    7: {"title": "COMB07: Tổ Hợp C(n, k) | Chọn Tập Con Không Phân Biệt Thứ Tự - Thầy Nguyễn Văn Sang", "file": "COMB07.mp4", "tags": ["tổ hợp", "C_n_k", "chọn tập con", "toán 10"]},
    8: {"title": "COMB08: Tổng Hợp Phương Pháp Đếm | Kỹ Thuật Nhận Diện Dạng Toán - Thầy Nguyễn Văn Sang", "file": "COMB08.mp4", "tags": ["tổng hợp phương pháp đếm", "bài tập đếm", "toán 10", "thầy nguyễn văn sang"]},
    9: {"title": "COMB09: Chọn Có Lặp & Lập Dãy Số | Phương Pháp Vách Ngăn Kinh Điển - Thầy Nguyễn Văn Sang", "file": "COMB09.mp4", "tags": ["chọn có lặp", "vách ngăn", "tổ hợp lặp", "toán 11"]},
    10: {"title": "COMB10: Hoán Vị Lặp | Đổi Chỗ Phần Tử Giống Nhau & Anagram - Thầy Nguyễn Văn Sang", "file": "COMB10.mp4", "tags": ["hoán vị lặp", "anagram", "đại số tổ hợp", "toán thpt"]},
    11: {"title": "COMB11: Hoán Vị Vòng Tròn | Xếp Bàn Tròn & Vòng Hoa Đối Xứng - Thầy Nguyễn Văn Sang", "file": "COMB11.mp4", "tags": ["hoán vị vòng tròn", "bàn tròn", "đối xứng", "toán 11"]},
    12: {
        "title": "STAT12: Phương Sai & Độ Lệch Chuẩn Của Mẫu Ghép Nhóm - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 12: Phương sai và độ lệch chuẩn của mẫu số liệu ghép nhóm

Nội dung trọng tâm bài 12:
- Phương pháp tính phương sai và độ lệch chuẩn bằng giá trị đại diện.
- So sánh sự khác biệt giữa tính trên dữ liệu gốc và dữ liệu ghép nhóm.
- Ứng dụng đo mức độ phân tán của dữ liệu ghép nhóm trong thực tế.

{AUTHOR_INFO}
#ThongKe #PhuongSai #DoLechChuan #MauGhepNhom #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["phương sai", "độ lệch chuẩn", "mẫu ghép nhóm", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT12"
    },
    13: {
        "title": "STAT13: So Sánh Hai Mẫu Số Liệu - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 13: So sánh hai mẫu số liệu

Nội dung trọng tâm bài 13:
- Phân tích sự khác biệt giữa hai mẫu số liệu.
- So sánh điểm trung bình và mức độ phân tán (phương sai, độ lệch chuẩn).
- Đánh giá hình dạng phân bố và ý nghĩa thực tế.

{AUTHOR_INFO}
#ThongKe #SoSanhMauSoLieu #Toan10 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["so sánh hai mẫu số liệu", "phương sai", "độ lệch chuẩn", "toán 10", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT13"
    },
    14: {
        "title": "STAT14: Bài Toán Thống Kê Tổng Hợp Và Vận Dụng Thực Tế - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 14: Bài toán thống kê tổng hợp và vận dụng thực tế

Nội dung trọng tâm bài 14:
- Tổng hợp các kiến thức thống kê đã học.
- Ứng dụng để giải quyết bài toán thực tế (ví dụ: chọn quầy phục vụ dựa trên thời gian chờ).
- Đánh giá toàn diện dựa trên số trung bình, trung vị và các độ đo phân tán.

{AUTHOR_INFO}
#ThongKe #TongHopThongKe #VanDungThucTe #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["thống kê tổng hợp", "vận dụng thực tế", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT14"
    }
}


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
        "title": "Bài 12: Trải Phẳng Mặt Trụ Quấn K Vòng | Đường Xoắn Ốc Helix - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 12:
- Đường xoắn ốc (Helix) trên mặt trụ khi dây quấn đúng k vòng đều đặn.
- Phương pháp ghép k hình chữ nhật trải phẳng nối tiếp nhau.
- Công thức Pythagoras tổng quát: L = sqrt(h^2 + (2*pi*R*k)^2).

{AUTHOR_INFO}
#DuongXoanOc #Helix #HinhTru #TraiPhang #ThayNguyenVanSang""",
        "tags": ["đường xoắn ốc", "helix", "quấn k vòng", "hình trụ", "trải phẳng"],
        "file_pattern": "trai_phang_12"
    },
    13: {
        "title": "Bài 13: Trải Phẳng Hình Nón Tròn Xoay | Góc Ở Đỉnh Hình Quạt Tròn - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 13:
- Mở phẳng mặt xung quanh hình nón thành hình quạt tròn bán kính bằng đường sinh l.
- Công thức tính góc ở tâm của hình quạt: alpha = 360 * (R / l).
- Bài toán vòng dây xuất phát từ điểm A trên đáy, quấn 1 vòng quanh nón rồi quay lại A.

{AUTHOR_INFO}
#HinhNon #MatNon #TraiPhang #HinhQuatTron #ThayNguyenVanSang""",
        "tags": ["hình nón", "mặt nón", "hình quạt tròn", "toán 12", "trải phẳng"],
        "file_pattern": "trai_phang_13"
    },
    14: {
        "title": "Bài 14: Trải Phẳng Hình Nón Cụt | Dải Vành Cung Tròn Xoay - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 14:
- Trải phẳng mặt bên hình nón cụt thành dải hình vành khuyên giới hạn bởi 2 cung tròn đồng tâm.
- Kỹ thuật tính góc mở và bán kính của 2 đường cong biên.
- Ứng dụng thực tế: Thiết kế phễu, chao đèn và bồn chứa hình nón cụt.

{AUTHOR_INFO}
#HinhNonCut #NonCut #TraiPhang #Manim #ThayNguyenVanSang""",
        "tags": ["hình nón cụt", "nón cụt", "trải phẳng", "toán 12", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_14"
    },
    15: {
        "title": "Bài 15: Silo Công Nghiệp Trụ Nối Nón | Trải Phẳng Mặt Phức Hợp - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 15:
- Kết hợp mặt trụ (thân silo) và mặt nón cụt (phễu xả liệu) trong các nhà máy xi măng, lương thực.
- Kỹ thuật trải phẳng liên hoàn qua mặt phân cách đường tròn giao tuyến.
- Tối ưu hóa chiều dài cầu thang xoắn ốc hoặc đường ống chạy dọc vỏ silo.

{AUTHOR_INFO}
#Silo #ToanThucTe #HinhHocKhongGian #TraiPhang #ThayNguyenVanSang""",
        "tags": ["silo", "toán thực tế", "trụ nối nón", "trải phẳng", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_15"
    },
    16: {
        "title": "Bài 16: Mô Hình Mái Nhà Lăng Trụ Tam Giác | Toán Kiến Trúc - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 16:
- Bài toán thiết kế dây cáp neo giữ và dây chống sét trên mái nhà lăng trụ.
- Mở phẳng 2 mặt mái dốc và mặt tường đầu hồi.
- So sánh các phương án né tránh gờ nóc nhà để tiết kiệm vật tư.

{AUTHOR_INFO}
#MaiNha #ToanKienTruc #TraiPhang #HinhHocKhongGian #ThayNguyenVanSang""",
        "tags": ["mái nhà", "toán kiến trúc", "trải phẳng", "lăng trụ", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_16"
    },
    17: {
        "title": "Bài 17: Điểm Đích Di Động Trên Cạnh | Kết Hợp Bất Đẳng Thức - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 17:
- Điểm đầu A cố định, điểm cuối M di chuyển tự do trên một cạnh của đa diện.
- Trải phẳng kết hợp kỹ thuật hạ đường vuông góc tìm khoảng cách cực tiểu.
- Bài toán biến thiên khoảng cách trong đề thi HSG và VDC THPTQG.

{AUTHOR_INFO}
#DiemDiDong #CucTriKhoangCach #TraiPhang #ToanVDC #ThayNguyenVanSang""",
        "tags": ["điểm di động", "cực trị", "vận dụng cao", "toán 12", "trải phẳng"],
        "file_pattern": "trai_phang_17"
    },
    18: {
        "title": "Bài 18: Bài Toán Mặt Bị Cấm (Vật Cản) | Lộ Trình Vòng Tránh - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 18:
- Bài toán thực chiến: Có một hoặc nhiều mặt bị cấm đi qua (ví dụ: đáy ẩm ướt, nắp nóng, kính vỡ).
- Loại bỏ các nhánh trải phẳng không hợp lệ và tìm đường đi tối ưu trên các nhánh còn lại.
- So sánh giữa đường thẳng trên lưới mở và đường men theo cạnh rìa.

{AUTHOR_INFO}
#VatCan #MatBiCam #TraiPhang #ThuatToanHinhHoc #ThayNguyenVanSang""",
        "tags": ["vật cản", "mặt bị cấm", "trải phẳng", "toán 12", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_18"
    },
    19: {
        "title": "Bài 19: Hộp Chữ Nhật Tham Số Kích Thước | Biện Luận a, b, c - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 19:
- Hình hộp chữ nhật kích thước tổng quát a x b x c với điều kiện a ≤ b ≤ c.
- Biện luận tường minh lộ trình nào trong 3 cách trải phẳng sẽ cho độ dài ngắn nhất.
- Bất đẳng thức đại số rút ra từ nguyên lý hình học trải phẳng.

{AUTHOR_INFO}
#BienLuanHinhHoc #HopChuNhat #ThamSo #TraiPhang #ThayNguyenVanSang""",
        "tags": ["biện luận", "hộp chữ nhật", "tham số", "trải phẳng", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_19"
    },
    20: {
        "title": "Bài 20: Capstone Thuật Toán Trải Phẳng Mọi Đa Diện Lồi - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Kỹ Thuật Trải Phẳng Hình Học Không Gian 3D

Nội dung bài 20 (Tổng kết Capstone):
- Hệ thống hóa toàn bộ thuật toán trải phẳng tìm đường đi ngắn nhất trên đa diện lồi bất kỳ.
- Ma trận chuyển tiếp giữa các mặt kề, kiểm tra giao cạnh nội phần và chọn cực tiểu toàn cục.
- Cầu nối giữa Hình học không gian cổ điển và Hình học tính toán (Computational Geometry) trong khoa học máy tính.

{AUTHOR_INFO}
#Capstone #ThuatToanHinhHoc #TraiPhang #ComputationalGeometry #ThayNguyenVanSang""",
        "tags": ["capstone", "thuật toán hình học", "trải phẳng", "toán trực quan", "thầy nguyễn văn sang"],
        "file_pattern": "trai_phang_20"
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
    12: {"title": "COMB12: Phương Pháp Buộc Khối (Gộp Khối) | Phần Tử Đứng Cạnh Nhau - Thầy Nguyễn Văn Sang", "file": "COMB12.mp4", "tags": ["buộc khối", "gộp khối", "đứng cạnh nhau", "phương pháp đếm"]},
    13: {"title": "COMB13: Phương Pháp Vách Ngăn Khe | Phần Tử Không Đứng Cạnh Nhau - Thầy Nguyễn Văn Sang", "file": "COMB13.mp4", "tags": ["vách ngăn khe", "không đứng cạnh nhau", "kỹ thuật đếm", "toán 10"]},
    14: {"title": "COMB14: Phương Pháp Đếm Phần Bù | Toàn Thể Trừ Vi Phạm (Quy Tắc Ngược) - Thầy Nguyễn Văn Sang", "file": "COMB14.mp4", "tags": ["đếm phần bù", "quy tắc bù", "toán 10", "thầy nguyễn văn sang"]},
    15: {"title": "COMB15: Lập Số Tự Nhiên Theo Điều Kiện | Chẵn Lẻ, Chia Hết, Khác Nhau - Thầy Nguyễn Văn Sang", "file": "COMB15.mp4", "tags": ["lập số", "chữ số khác nhau", "chia hết", "toán 10"]},
    16: {"title": "COMB16: Chia Nhóm & Phân Công Vai Trò | Tránh Lỗi Đếm Trùng - Thầy Nguyễn Văn Sang", "file": "COMB16.mp4", "tags": ["chia nhóm", "phân công", "lỗi đếm trùng", "toán thpt"]},
    17: {"title": "COMB17: Nhị Thức Newton (a + b)^n | Bản Chất Khai Triển & Hệ Số - Thầy Nguyễn Văn Sang", "file": "COMB17.mp4", "tags": ["nhị thức newton", "khai triển", "hệ số", "toán 10", "toán 11"]},
    18: {"title": "COMB18: Tam Giác Pascal | Tính Chất Đối Xứng & Hàng Lũy Thừa - Thầy Nguyễn Văn Sang", "file": "COMB18.mp4", "tags": ["tam giác pascal", "pascal triangle", "tính chất tổ hợp"]},
    19: {"title": "COMB19: Số Tập Con Của Tập Hợp n Phần Tử | Đẳng Thức Tổng C_n^k = 2^n - Thầy Nguyễn Văn Sang", "file": "COMB19.mp4", "tags": ["tập con", "2^n", "đẳng thức tổ hợp", "thầy nguyễn văn sang"]},
    20: {"title": "COMB20: Tính Tổng Hệ Số Nhị Thức | Giá Trị Đặc Biệt & Đạo Hàm - Thầy Nguyễn Văn Sang", "file": "COMB20.mp4", "tags": ["tính tổng hệ số", "đạo hàm nhị thức", "toán vận dụng cao"]},
    21: {"title": "COMB21: Phương Pháp Hàm Sinh (Generating Functions) | Toán Đếm Nâng Cao - Thầy Nguyễn Văn Sang", "file": "COMB21.mp4", "tags": ["hàm sinh", "generating functions", "olympiad", "toán nâng cao"]},
    22: {"title": "COMB22: Quy Hoạch Động Trong Tổ Hợp | Thiết Lập Hệ Thức Truy Hồi - Thầy Nguyễn Văn Sang", "file": "COMB22.mp4", "tags": ["quy hoạch động", "hệ thức truy hồi", "dynamic programming", "toán tin"]},
    23: {"title": "COMB23: Bao Hàm Loại Trừ (PIE) & Đa Thức Quân Xe | Xáo Trộn Hoàn Toàn - Thầy Nguyễn Văn Sang", "file": "COMB23.mp4", "tags": ["bao hàm loại trừ", "PIE", "quân xe", "derangement", "olympiad"]},
    24: {"title": "COMB24: Số Catalan, Dãy Dyck & Nguyên Lý Phản Xạ | Tổ Hợp Olympiad - Thầy Nguyễn Văn Sang", "file": "COMB24.mp4", "tags": ["số catalan", "dãy dyck", "nguyên lý phản xạ", "olympiad math"]},
    25: {"title": "COMB25: Bổ Đề Burnside & Định Lý Pólya | Đếm Số Quỹ Đạo Dưới Nhóm - Thầy Nguyễn Văn Sang", "file": "COMB25.mp4", "tags": ["burnside", "polya", "lý thuyết nhóm", "đếm quỹ đạo", "olympiad toán"]}
}

# ==============================================================================
# KHÓA HỌC 3: XÁC SUẤT & THỐNG KÊ TOÁN HỌC TRỰC QUAN (TOÁN 10 - 11 - 12)
# ==============================================================================
PLAYLIST_THONG_KE = {
    "title": "Xác Suất & Thống Kê: Trực Quan Hóa Dữ Liệu Toán THPT - Thầy Nguyễn Văn Sang",
    "description": "Trọn bộ bài giảng trực quan hóa Thống kê và Xác suất THPT theo chương trình GDPT mới bằng hoạt họa Manim và Typst. Khảo sát dữ liệu thực tế, bảng tần số, biểu đồ, các số đặc trưng đo xu thế trung tâm và độ phân tán."
}

THONG_KE_LESSONS = {
    1: {
        "title": "STAT01: Dữ Liệu Biết Nói | Bảng Tần Số & Biểu Đồ Thống Kê - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 01: Dữ liệu biết nói – Từ 40 số liệu đến bức tranh toàn cảnh lớp học

Nội dung trọng tâm bài 01:
- Dữ liệu định lượng và dữ liệu phân loại trong thực tế.
- Kỹ thuật chuyển từ dữ liệu thô sang dãy có thứ tự (sắp xếp tăng dần).
- Xây dựng bảng tần số và bảng tần số tương đối (tỷ lệ phần trăm).
- Trực quan hóa bằng biểu đồ cột chuẩn (gốc tọa độ 0) và biểu đồ điểm (dot plot).
- Cảnh báo các lỗi sai kinh điển: Biểu đồ cắt xén trục tung gây ngộ nhận thống kê.
- Đặt nền móng cho các số đặc trưng: Trung bình (Mean), Trung vị (Median), Mốt (Mode).

{AUTHOR_INFO}
#ThongKe #Toan10 #Toan11 #Toan12 #Manim #Typst #ThayNguyenVanSang #XacSuatThongKe""",
        "tags": ["thống kê", "toán 10", "toán 11", "toán 12", "xác suất thống kê", "bảng tần số", "biểu đồ cột", "manim", "typst", "thầy nguyễn văn sang"],
        "file_pattern": "STAT01"
    },
    2: {
        "title": "STAT02: Biểu Đồ Thống Kê | Cột, Đoạn Thẳng, Hình Quạt & Histogram - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 02: Biểu đồ thống kê – Một bộ dữ liệu, nhiều góc nhìn trực quan

Nội dung trọng tâm bài 02:
- Chuyển đổi linh hoạt từ bảng số liệu sang các dạng trực quan tương ứng.
- Biểu đồ cột (Bar chart) & Biểu đồ điểm (Dot plot): So sánh tần số rời rạc.
- Biểu đồ hình quạt tròn (Pie chart): Tỷ lệ cơ cấu và góc ở tâm theo phần trăm.
- Biểu đồ đoạn thẳng (Line graph): Quan sát xu hướng biến thiên theo thời gian.
- Histogram (Biểu đồ tần số ghép nhóm): Phân phối mật độ và diện tích hình chữ nhật.
- Nguyên tắc trung thực trong thống kê: Tránh ngụy biện trực quan khi chọn biểu đồ.

{AUTHOR_INFO}
#ThongKe #BieuDoThongKe #Histogram #Manim #Typst #ThayNguyenVanSang #Toan10 #Toan11 #Toan12""",
        "tags": ["biểu đồ thống kê", "toán 10", "toán 11", "toán 12", "biểu đồ cột", "hình quạt tròn", "histogram", "manim", "typst", "thầy nguyễn văn sang"],
        "file_pattern": "STAT02"
    },
    3: {
        "title": "STAT03: Số Trung Bình, Trung Vị & Mốt | Xu Thế Trung Tâm Dữ Liệu - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 03: Số đặc trưng đo xu thế trung tâm – Ba con số kể ba câu chuyện

Nội dung trọng tâm bài 03:
- Số trung bình cộng (Mean): Trọng tâm cân bằng đại số của toàn bộ mẫu số liệu.
- Trung vị (Median): Điểm chia đôi mẫu số liệu đã sắp thứ tự, tính bất biến trước ngoại lai.
- Mốt (Mode): Giá trị có tần số xuất hiện cao nhất, đa mốt và đơn mốt.
- Phân tích ảnh hưởng của giá trị bất thường (outlier / giá trị dị biệt).
- So sánh khi nào nên dùng số trung bình, khi nào trung vị là thước đo tin cậy hơn.

{AUTHOR_INFO}
#ThongKe #SoTrungBinh #TrungVi #Mot #Outlier #Toan10 #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["số trung bình", "trung vị", "mốt", "toán 10", "toán 11", "toán 12", "số đặc trưng", "outlier", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT03"
    },
    4: {
        "title": "STAT04: Tứ Phân Vị Q1, Q2, Q3 | Chia Nhỏ Dữ Liệu - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 04: Tứ phân vị Q1, Q2, Q3 – Điểm mốc quan trọng của dữ liệu

Nội dung trọng tâm bài 04:
- Sắp xếp và chia dữ liệu thành 4 phần bằng nhau.
- Cách tính tứ phân vị với số lượng mẫu chẵn và lẻ.
- Ý nghĩa của tứ phân vị thứ nhất (Q1), thứ hai (Q2 / Trung vị) và thứ ba (Q3).
- Trực quan hóa vị trí các tứ phân vị trên trục số.

{AUTHOR_INFO}
#ThongKe #TuPhanVi #Quartiles #Toan10 #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["thống kê", "tứ phân vị", "toán 10", "toán 11", "toán 12", "quartiles", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT04"
    },
    5: {
        "title": "STAT05: Khoảng Biến Thiên, IQR & Biểu Đồ Hộp | Đo Độ Phân Tán Dữ Liệu - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 05: Khoảng biến thiên, Khoảng tứ phân vị (IQR) & Biểu đồ hộp (Box plot)

Nội dung trọng tâm bài 05:
- Đo lường độ phân tán dữ liệu bằng Khoảng biến thiên (Range) và Khoảng tứ phân vị (IQR = Q3 - Q1).
- Vẽ biểu đồ hộp (Box-and-whisker plot) từ 5 con số đặc trưng: Min, Q1, Q2, Q3, Max.
- Phát hiện các điểm bất thường (Outliers) dựa trên rào dưới và rào trên.
- So sánh phân bố dữ liệu giữa nhiều nhóm thông qua biểu đồ hộp.

{AUTHOR_INFO}
#ThongKe #KhoangBienThien #IQR #BieuDoHop #BoxPlot #Toan10 #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["khoảng biến thiên", "iqr", "biểu đồ hộp", "box plot", "toán 10", "toán 11", "toán 12", "độ phân tán", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT05"
    },
    6: {
        "title": "STAT06: Phương Sai & Độ Lệch Chuẩn | Đo Độ Phân Tán Quanh Trung Bình - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 06: Phương sai và độ lệch chuẩn

Nội dung trọng tâm bài 06:
- Vì sao cùng số trung bình vẫn chưa đủ để so sánh hai mẫu số liệu.
- Độ lệch so với trung bình, tổng độ lệch bằng 0 và lý do phải bình phương.
- Công thức phương sai, độ lệch chuẩn và ý nghĩa của chúng.
- Ảnh hưởng của giá trị bất thường lên phương sai.

{AUTHOR_INFO}
#ThongKe #PhuongSai #DoLechChuan #Toan10 #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["phương sai", "độ lệch chuẩn", "độ phân tán", "toán 10", "toán 11", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT06"
    },
    7: {
        "title": "STAT07: Mẫu Số Liệu Ghép Nhóm & Histogram - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 07: Mẫu số liệu ghép nhóm và Histogram

Nội dung trọng tâm bài 07:
- Chuyển 40 điểm rời rạc sang bảng ghép nhóm.
- Ranh giới lớp, tần số, tần số tích lũy và tần số tương đối.
- Vẽ histogram và hiểu vai trò của diện tích.
- Thông tin bị mất khi ghép nhóm và ảnh hưởng của cách chia lớp.

{AUTHOR_INFO}
#ThongKe #MauGhepNhom #Histogram #Toan10 #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["mẫu số liệu ghép nhóm", "histogram", "tần số tích lũy", "toán 10", "toán 11", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT07"
    },
    8: {
        "title": "STAT08: Số Trung Bình & Mốt Của Mẫu Ghép Nhóm - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 08: Số trung bình và mốt của mẫu số liệu ghép nhóm

Nội dung trọng tâm bài 08:
- Giá trị đại diện của lớp và số trung bình ghép nhóm.
- Sai số khi ghép nhóm và so sánh các cách chia lớp.
- Lớp mốt và công thức nội suy mốt.
- Histogram với độ rộng lớp khác nhau và bài toán ngược với tần số chưa biết.

{AUTHOR_INFO}
#ThongKe #MauGhepNhom #Mot #SoTrungBinh #Toan10 #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["mẫu ghép nhóm", "số trung bình", "mốt", "toán 10", "toán 11", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT08"
    },
    9: {
        "title": "STAT09: Trung Vị Của Mẫu Số Liệu Ghép Nhóm - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 09: Trung vị của mẫu số liệu ghép nhóm

Nội dung trọng tâm bài 09:
- Xác định nhóm chứa trung vị bằng tần số tích lũy.
- Phép nội suy tuyến tính tìm trung vị.
- Giải thích bản chất hình học qua đường ogive và biểu đồ tần số tích lũy.

{AUTHOR_INFO}
#ThongKe #TrungVi #MauGhepNhom #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["trung vị", "mẫu ghép nhóm", "toán 11", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT09"
    },
    10: {
        "title": "STAT10: Tứ Phân Vị Của Mẫu Số Liệu Ghép Nhóm - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 10: Tứ phân vị mẫu số liệu ghép nhóm

Nội dung trọng tâm bài 10:
- Tìm Q1, Q2 (trung vị) và Q3 cho số liệu ghép nhóm.
- Ứng dụng tứ phân vị trong phân tích dữ liệu thực tế.

{AUTHOR_INFO}
#ThongKe #TuPhanVi #MauGhepNhom #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["tứ phân vị", "mẫu ghép nhóm", "toán 11", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT10"
    },
    11: {
        "title": "STAT11: Khoảng Biến Thiên & Khoảng Tứ Phân Vị Của Mẫu Ghép Nhóm - Thầy Nguyễn Văn Sang",
        "description": f"""Khóa học: Xác Suất & Thống Kê Toán Học Trực Quan (Toán 10 - 11 - 12)
Bài 11: Khoảng biến thiên và khoảng tứ phân vị (IQR) của mẫu ghép nhóm

Nội dung trọng tâm bài 11:
- Cách tính khoảng biến thiên khi chỉ biết các khoảng ghép nhóm.
- Tính IQR và ý nghĩa đo độ phân tán.
- Đánh giá sự mất mát thông tin khi ghép nhóm.

{AUTHOR_INFO}
#ThongKe #KhoangBienThien #IQR #MauGhepNhom #Toan11 #Toan12 #ThayNguyenVanSang #Manim""",
        "tags": ["khoảng biến thiên", "iqr", "mẫu ghép nhóm", "toán 11", "toán 12", "manim", "thầy nguyễn văn sang"],
        "file_pattern": "STAT11"
    }
}

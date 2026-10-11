"""Tên kỳ thủ: chữ Hán -> tên Việt quen dùng. Chỉ ghi những tên đã kiểm; tên lạ trả về None."""

NAMES = {
    '胡荣华': 'Hồ Vinh Hoa', '吕钦': 'Lữ Khâm', '许银川': 'Hứa Ngân Xuyên', '王天一': 'Vương Thiên Nhất',
    '赵鑫鑫': 'Triệu Hâm Hâm', '蒋川': 'Tưởng Xuyên', '杨官璘': 'Dương Quan Lân', '李来群': 'Lý Lai Quần',
    '柳大华': 'Liễu Đại Hoa', '赵国荣': 'Triệu Quốc Vinh', '徐天红': 'Từ Thiên Hồng', '王嘉良': 'Vương Gia Lương',
    '李义庭': 'Lý Nghĩa Đình', '汪洋': 'Uông Dương', '洪智': 'Hồng Trí', '孙勇征': 'Tôn Dũng Chinh',
    '谢靖': 'Tạ Tĩnh', '郑惟桐': 'Trịnh Duy Đồng', '陶汉明': 'Đào Hán Minh', '于幼华': 'Vu Ấu Hoa',
    '刘殿中': 'Lưu Điện Trung', '傅光明': 'Phó Quang Minh', '蔡福如': 'Thái Phúc Như', '卜凤波': 'Bốc Phượng Ba',
    '阎文清': 'Diêm Văn Thanh', '张强': 'Trương Cường', '聂铁文': 'Niếp Thiết Văn', '景学义': 'Cảnh Học Nghĩa',
    '许国义': 'Hứa Quốc Nghĩa', '陈孝堃': 'Trần Hiếu Khôn', '王斌': 'Vương Bân', '金波': 'Kim Ba',
    '庄玉庭': 'Trang Ngọc Đình', '万春林': 'Vạn Xuân Lâm', '申鹏': 'Thân Bằng', '黄海林': 'Hoàng Hải Lâm',
    '阮成保': 'Nguyễn Thành Bảo', '赖理兄': 'Lại Lý Huynh', '郑亚生': 'Trềnh A Sáng', '阮黄林': 'Nguyễn Hoàng Lâm',
    '杨官麟': 'Dương Quan Lân', '陈孝坤': 'Trần Hiếu Khôn', '戴荣光': 'Đới Vinh Quang', '季本涵': 'Quý Bản Hàm',
    '惠颂祥': 'Huệ Tụng Tường', '李国勋': 'Lý Quốc Huân', '钱洪发': 'Tiền Hồng Phát', '赵庆阁': 'Triệu Khánh Các',
    '杨德琪': 'Dương Đức Kỳ', '李艾东': 'Lý Ngải Đông', '言穆江': 'Ngôn Mục Giang', '黎德志': 'Lê Đức Chí',
}


def vn_name(name):
    return NAMES.get((name or '').strip())


def describe(name, side):
    """Tên để đọc: tên Việt nếu biết, nếu không thì 'kỳ thủ cầm quân Đỏ/Đen'."""
    v = vn_name(name)
    return v if v else f'kỳ thủ cầm quân {"Đỏ" if side == "w" else "Đen"}'

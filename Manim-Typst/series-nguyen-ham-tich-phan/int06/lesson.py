"""INT06 – Nguyên hàm có điều kiện & hàm từng khúc: tìm C, nối liên tục.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT06',
    'number': 6,
    'title': 'Nguyên hàm có điều kiện',
    'subtitle': 'Tìm C, nguyên hàm hai lần & hàm từng khúc',
    'next_code': 'INT07',
    'next_title': 'Nguyên hàm phân thức hữu tỉ',
}

PARTS = (
    ('hook', 'Mở đầu'),
    ('core', 'Bản chất'),
    ('examples', 'Ví dụ'),
    ('exam', 'Đề thi mới'),
    ('outro', 'Tổng kết'),
)


@dataclass(frozen=True)
class Beat:
    id: str
    part: str
    text: str
    chapter: str | None = None


BEATS = (
    # ---------------- MỞ ĐẦU ----------------
    Beat('h1', 'hook',
         'Một chiếc xe xuất phát và tăng tốc đều trong ba giây đầu, sau đó giữ nguyên vận tốc sáu mét mỗi giây. '
         'Vận tốc được cho bởi hai công thức khác nhau trên hai khoảng thời gian. Muốn biết vị trí của xe, '
         'ta phải lấy nguyên hàm của một hàm số cho theo từng khúc, rồi nối các mảnh lại sao cho chiếc xe '
         'không bị dịch chuyển tức thời.',
         'Mở đầu: vận tốc cho theo từng khúc'),
    Beat('h2', 'hook',
         'Đây là tập sáu của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'nguyên hàm có điều kiện, nguyên hàm hai lần và hàm số cho theo từng khúc.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ thành thạo ba dạng. Một, dùng một hoặc nhiều điều kiện để tìm hằng số C. '
         'Hai, lấy nguyên hàm hai lần, từ gia tốc ra vận tốc rồi ra vị trí. '
         'Ba, hàm từng khúc: mỗi khúc một hằng số, và hàn các khúc lại bằng tính liên tục.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Nhắc lại dạng quen thuộc nhất: biết F phẩy bằng f và một giá trị F của x không bằng y không. '
         'Ta tìm họ nguyên hàm, rồi thay điều kiện vào để tìm C. Về hình học, điều kiện chọn ra đúng một đường cong '
         'trong cả họ, đường đi qua điểm x không, y không.',
         'Dạng 1: điều kiện xác định C'),
    Beat('c2', 'core',
         'Điều kiện không nhất thiết là một giá trị đơn lẻ. Ví dụ, F là nguyên hàm của hai x cộng một, và F của một '
         'cộng F của hai bằng mười. Ta có F bằng x bình phương cộng x cộng C. Thay vào: hai cộng C, cộng sáu cộng C, '
         'bằng mười. Vậy C bằng một. Chỉ cần đếm đúng: mỗi lần thay là một chữ C.'),
    Beat('c3', 'core',
         'Dạng hai: nguyên hàm hai lần. Biết đạo hàm cấp hai của f bằng sáu x, f phẩy của không bằng hai và '
         'f của không bằng một. Lấy nguyên hàm lần thứ nhất: f phẩy bằng ba x bình phương cộng C một, '
         'điều kiện cho C một bằng hai. Lấy nguyên hàm lần thứ hai: f bằng x lập phương cộng hai x cộng C hai, '
         'và C hai bằng một.',
         'Dạng 2: nguyên hàm hai lần'),
    Beat('c4', 'core',
         'Ý nghĩa vật lý: từ gia tốc, nguyên hàm một lần ra vận tốc, nguyên hàm thêm lần nữa ra vị trí. '
         'Mỗi lần lấy nguyên hàm sinh ra một hằng số mới, nên cần đúng hai điều kiện: vận tốc ban đầu '
         'và vị trí ban đầu. Thiếu một điều kiện là không xác định được hàm số.'),
    Beat('c5', 'core',
         'Dạng ba, quan trọng nhất: hàm số cho theo từng khúc. Xét f của x bằng hai x khi x lớn hơn hoặc bằng một, '
         'và bằng hai khi x nhỏ hơn một. Tại x bằng một, hai công thức cho cùng giá trị hai, nên f liên tục, '
         'đồ thị chỉ gãy góc chứ không đứt.',
         'Dạng 3: hàm số cho theo từng khúc'),
    Beat('c6', 'core',
         'Lấy nguyên hàm trên từng khúc. Với x lớn hơn hoặc bằng một: x bình phương cộng C một. '
         'Với x nhỏ hơn một: hai x cộng C hai. Hai khúc có hai hằng số khác nhau. '
         'Nếu chọn tùy ý, hai mảnh đồ thị của F sẽ bị lệch nhau tại x bằng một.'),
    Beat('c7', 'core',
         'Nhưng F có đạo hàm tại mọi điểm, nên F phải liên tục. Hai mảnh phải hàn khít tại x bằng một: '
         'một cộng C một bằng hai cộng C hai. Trên hình, ta kéo mảnh bên phải cho tới khi khớp với mảnh bên trái. '
         'Đây chính là bước mà nhiều bạn bỏ quên.',
         'Hàn các khúc bằng tính liên tục'),
    Beat('c8', 'core',
         'Bây giờ thêm điều kiện F của không bằng một. Điểm không thuộc khúc bên trái, nên C hai bằng một. '
         'Từ phương trình hàn, C một bằng hai. Vậy F bằng x bình phương cộng hai khi x lớn hơn hoặc bằng một, '
         'và bằng hai x cộng một khi x nhỏ hơn một. Chẳng hạn F của hai bằng sáu.'),
    Beat('c9', 'core',
         'Lưu ý chuyên sâu: nếu f bị đứt quãng, tức có bước nhảy, thì đạo hàm của F không thể nhảy giá trị như vậy, '
         'và f không có nguyên hàm trên cả trục số. Vì thế đề thi luôn cho f liên tục tại điểm nối. '
         'Em hãy kiểm tra điều đó trước khi giải.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Quay lại chiếc xe ở đầu bài: v của t bằng hai t khi t từ không đến ba, và bằng sáu khi t lớn hơn ba. '
         'Vị trí ban đầu bằng không. Trên khúc đầu, s bằng t bình phương. Trên khúc sau, s bằng sáu t cộng C. '
         'Hàn tại t bằng ba: chín bằng mười tám cộng C, nên C bằng âm chín.',
         'Ví dụ 1: chiếc xe tăng tốc rồi chạy đều'),
    Beat('e2', 'examples',
         'Vậy sau năm giây, s bằng sáu nhân năm trừ chín, bằng hai mươi mốt mét. Hãy quan sát: '
         'đồ thị vị trí cong trong ba giây đầu, rồi chuyển mượt thành đường thẳng, không có bước nhảy nào.'),
    Beat('e3', 'examples',
         'Ví dụ hai, chuyên sâu: nguyên hàm của trị tuyệt đối x. Khi x không âm, được x bình phương chia hai cộng C một. '
         'Khi x âm, được âm x bình phương chia hai cộng C hai. Hàn tại không cho C một bằng C hai. '
         'Kết quả viết gọn: x nhân trị tuyệt đối x, chia hai, cộng C.',
         'Ví dụ 2: nguyên hàm của |x|'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f bằng ba x bình phương khi x lớn hơn hoặc bằng một, và bằng ba khi '
         'x nhỏ hơn một. F là nguyên hàm của f trên R và F của không bằng hai. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: điểm không thuộc khúc bên trái, F bằng ba x cộng C hai, và C hai bằng hai. '
         'Ý b sai: hàn tại một cho một cộng C một bằng ba cộng hai, tức C một bằng bốn, không phải hai.'),
    Beat('x3', 'exam',
         'Ý c đúng: F của hai bằng tám cộng bốn, bằng mười hai. Ý d đúng: âm một thuộc khúc bên trái, '
         'F của âm một bằng âm ba cộng hai, bằng âm một.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. F là nguyên hàm của hàm số bằng hai x cộng một khi x không âm, bằng e mũ x khi x âm, '
         'và F của không bằng một. Tính F của hai cộng F của âm lô ga nê pe hai. Khúc phải: x bình phương cộng x cộng một. '
         'Hàn tại không: một cộng C hai bằng một, nên C hai bằng không. Vậy kết quả là bảy cộng một phần hai, bằng bảy phẩy năm.',
         'Trả lời ngắn và quy trình 3 bước'),
    Beat('x5', 'exam',
         'Quy trình ba bước cho hàm từng khúc. Bước một, lấy nguyên hàm từng khúc, mỗi khúc một hằng số riêng. '
         'Bước hai, hàn tại điểm nối bằng tính liên tục. Bước ba, dùng điều kiện đề cho, và nhớ xem điểm đó '
         'thuộc khúc nào.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, mỗi điều kiện cho một phương trình của C. Hai, nguyên hàm hai lần cần hai hằng số '
         'và hai điều kiện. Ba, hàm từng khúc: mỗi khúc một C, hàn bằng tính liên tục, rồi mới dùng điều kiện.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, F phẩy bằng bốn x lập phương trừ một, F của một cộng F của âm một bằng bốn, tìm F. '
         'Hai, đạo hàm cấp hai của f bằng mười hai x bình phương, f phẩy của một bằng năm, f của một bằng hai, tính f của hai. '
         'Ba, f bằng hai x khi x lớn hơn hoặc bằng hai, bằng bốn khi x nhỏ hơn hai, F của không bằng không, tính F của ba.'),
    Beat('o3', 'outro',
         'Ở tập bảy, ta sẽ học cách tìm nguyên hàm của phân thức hữu tỉ: chia đa thức và tách phân thức. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook_v': "v(t) = cases(2t & \"khi\" 0 <= t <= 3, 6 & \"khi\" t > 3)",
    'c1_a': "F'(x) = f(x), quad F(x_0) = y_0",
    'c1_b': "F(x) = G(x) + C arrow.double.long C = y_0 - G(x_0)",
    'c2_task': "F'(x) = 2x + 1, quad F(1) + F(2) = 10",
    'c2_s1': "F(x) = x^2 + x + C",
    'c2_s2': "(2 + C) + (6 + C) = 10 arrow.double.long C = gold(1)",
    'c3_task': "f''(x) = 6x, quad f'(0) = 2, quad f(0) = 1",
    'c3_s1': "f'(x) = 3x^2 + C_1, quad C_1 = 2",
    'c3_s2': "f(x) = x^3 + 2x + C_2, quad C_2 = 1",
    'c3_s3': "f(x) = x^3 + 2x + 1",
    'chain': "a(t) arrow.r.long^(integral) v(t) arrow.r.long^(integral) s(t)",
    'pw_f': "f(x) = cases(2x & \"khi\" x >= 1, 2 & \"khi\" x < 1)",
    'pw_F': "F(x) = cases(x^2 + green(C_1) & \"khi\" x >= 1, 2x + purple(C_2) & \"khi\" x < 1)",
    'weld': "1 + C_1 = 2 + C_2",
    'pw_c2': "F(0) = 1 arrow.double.long C_2 = 1 arrow.double.long C_1 = 2",
    'pw_res': "F(x) = cases(x^2 + 2 & \"khi\" x >= 1, 2x + 1 & \"khi\" x < 1)",
    'pw_val': "F(2) = 4 + 2 = gold(6)",
    'e1_s1': "s(t) = cases(t^2 & \"khi\" 0 <= t <= 3, 6t + C & \"khi\" t > 3)",
    'e1_s2': "9 = 18 + C arrow.double.long C = -9",
    'e1_s3': "s(5) = 30 - 9 = gold(21)",
    'e3_s1': "integral |x| dif x = cases(x^2/2 + C_1 & \"khi\" x >= 0, -x^2/2 + C_2 & \"khi\" x < 0)",
    'e3_s2': "C_1 = C_2 arrow.double.long integral |x| dif x = (x|x|)/2 + C",
    'tf_f': "f(x) = cases(3x^2 & \"khi\" x >= 1, 3 & \"khi\" x < 1), quad F(0) = 2",
    'tf_a': "F(x) = 3x + 2 \"khi\" x < 1",
    'tf_b': "F(x) = x^3 + 2 \"khi\" x >= 1",
    'tf_c': "F(2) = 12",
    'tf_d': "F(-1) = -1",
    'tf_b_calc': "1 + C_1 = 3 + 2 arrow.double.long C_1 = 4",
    'tf_cd_calc': "F(2) = 8 + 4 = 12, quad F(-1) = -3 + 2 = -1",
    'sa_task': "f(x) = cases(2x + 1 & \"khi\" x >= 0, e^x & \"khi\" x < 0), quad F(0) = 1",
    'sa_s1': "F(x) = cases(x^2 + x + 1 & \"khi\" x >= 0, e^x + C_2 & \"khi\" x < 0), quad 1 + C_2 = 1",
    'sa_s2': "F(2) + F(-ln 2) = 7 + 1/2 = gold(\"7,5\")",
    'sum1': "F(x_0) = y_0 arrow.double.long C",
    'sum2': "f'' arrow.r f' arrow.r f: quad C_1, C_2",
    'sum3': "F(x_0^-) = F(x_0^+) arrow.double.long C_1, C_2",
    'hw1': "F'(x) = 4x^3 - 1, quad F(1) + F(-1) = 4",
    'hw2': "f''(x) = 12x^2, quad f'(1) = 5, quad f(1) = 2, quad f(2) = ?",
    'hw3': "f(x) = cases(2x & \"khi\" x >= 2, 4 & \"khi\" x < 2), quad F(0) = 0, quad F(3) = ?",
    'hw_ans1': "F(x) = x^4 - x + 1",
    'hw_ans2': "f(2) = 18",
    'hw_ans3': "F(3) = 13",
    'next1': "(x^2 + 1)/(x - 1) = x + 1 + 2/(x - 1)",
    'next2': "1/((x - 1)(x + 2)) = 1/3 (1/(x - 1) - 1/(x + 2))",
}

EXERCISES = (
    ("F'(x) = 4x³ − 1, F(1) + F(−1) = 4. Tìm F.", 'F(x) = x⁴ − x + 1'),
    ("f''(x) = 12x², f'(1) = 5, f(1) = 2. Tính f(2).", 'f(2) = 18'),
    ('f(x) = 2x (x ≥ 2), 4 (x < 2); F(0) = 0. Tính F(3).', 'F(3) = 13'),
)

TRUE_FALSE = (
    ('F(x) = 3x + 2 khi x < 1', True),
    ('F(x) = x³ + 2 khi x ≥ 1', False),
    ('F(2) = 12', True),
    ('F(−1) = −1', True),
)

x, t, C, C1, C2 = sp.symbols('x t C C1 C2', real=True)


def same_primitive(F, f, var=x):
    return sp.simplify(sp.diff(F, var) - f) == 0


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    # dạng 1b: two values
    F = x**2 + x + C
    assert same_primitive(F, 2*x + 1) and sp.solve(sp.Eq(F.subs(x, 1) + F.subs(x, 2), 10), C) == [1]
    # dạng 2: twice
    fp = 3*x**2 + C1
    c1 = sp.solve(sp.Eq(fp.subs(x, 0), 2), C1)[0]
    f = x**3 + c1*x + C2
    c2 = sp.solve(sp.Eq(f.subs(x, 0), 1), C2)[0]
    assert same_primitive(fp, 6*x) and c1 == 2 and same_primitive(f, fp.subs(C1, c1)) and c2 == 1
    # dạng 3: piecewise f(x) = 2x (x>=1), 2 (x<1); continuous at 1
    assert (2*x).subs(x, 1) == 2
    R, L = x**2 + C1, 2*x + C2
    c2p = sp.solve(sp.Eq(L.subs(x, 0), 1), C2)[0]
    c1p = sp.solve(sp.Eq(R.subs(x, 1), L.subs({x: 1, C2: c2p})), C1)[0]
    assert (c1p, c2p) == (2, 1) and R.subs({C1: c1p, x: 2}) == 6
    # example 1: car
    s1 = t**2
    S2 = 6*t + C
    cS = sp.solve(sp.Eq(s1.subs(t, 3), S2.subs(t, 3)), C)[0]
    assert same_primitive(s1, 2*t, t) and cS == -9 and S2.subs({C: cS, t: 5}) == 21
    # example 2: |x|
    G = x*sp.Abs(x)/2
    for v in (-2, -sp.Rational(1, 2), sp.Rational(1, 3), 3):
        assert sp.diff(G, x).subs(x, v) == abs(v)
    # true / false
    Lt, Rt = 3*x + C2, x**3 + C1
    c2t = sp.solve(sp.Eq(Lt.subs(x, 0), 2), C2)[0]
    c1t = sp.solve(sp.Eq(Rt.subs(x, 1), Lt.subs({x: 1, C2: c2t})), C1)[0]
    claims = (c2t == 2, c1t == 2, Rt.subs({C1: c1t, x: 2}) == 12, Lt.subs({C2: c2t, x: -1}) == -1)
    assert (3*x**2).subs(x, 1) == 3 and c1t == 4
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    Rs = x**2 + x + 1
    Ls = sp.exp(x) + C2
    c2s = sp.solve(sp.Eq(Ls.subs(x, 0), Rs.subs(x, 0)), C2)[0]
    total = Rs.subs(x, 2) + Ls.subs({C2: c2s, x: -sp.log(2)})
    assert (2*x + 1).subs(x, 0) == sp.exp(0) and c2s == 0 and sp.simplify(total - sp.Rational(15, 2)) == 0
    # exercises
    F1 = x**4 - x + C
    cc = sp.solve(sp.Eq(F1.subs(x, 1) + F1.subs(x, -1), 4), C)[0]
    assert cc == 1
    g1 = 4*x**3 + C1
    k1 = sp.solve(sp.Eq(g1.subs(x, 1), 5), C1)[0]
    g = x**4 + k1*x + C2
    k2 = sp.solve(sp.Eq(g.subs(x, 1), 2), C2)[0]
    assert k1 == 1 and k2 == 0 and g.subs({C2: k2, x: 2}) == 18
    L3, R3 = 4*x + C2, x**2 + C1
    q2 = sp.solve(sp.Eq(L3.subs(x, 0), 0), C2)[0]
    q1 = sp.solve(sp.Eq(R3.subs(x, 2), L3.subs({x: 2, C2: q2})), C1)[0]
    assert q1 == 4 and R3.subs({C1: q1, x: 3}) == 13
    # teaser
    assert sp.simplify((x**2 + 1)/(x - 1) - (x + 1 + 2/(x - 1))) == 0
    assert sp.simplify(1/((x - 1)*(x + 2)) - (1/(x - 1) - 1/(x + 2))/3) == 0
    return True


validate()

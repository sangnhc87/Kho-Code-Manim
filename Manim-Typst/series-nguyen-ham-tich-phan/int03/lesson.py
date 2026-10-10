"""INT03 – Nguyên hàm của 1/x và hàm số mũ: ln|x| trên từng khoảng, eˣ, aˣ.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT03',
    'number': 3,
    'title': 'Nguyên hàm của 1/x và hàm mũ',
    'subtitle': 'Hai nhánh của 1/x · hàm eˣ và aˣ',
    'next_code': 'INT04',
    'next_title': 'Nguyên hàm hàm số lượng giác',
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
         'Ở tập trước, công thức nguyên hàm của x mũ alpha dùng được cho mọi số mũ, trừ đúng một giá trị: '
         'alpha bằng âm một. Trên trục số mũ, có một lỗ thủng tại âm một. Đó chính là hàm một chia x, '
         'một hàm rất hay gặp. Hôm nay ta vá lỗ thủng ấy, rồi gặp hàm số đặc biệt nhất của giải tích: '
         'hàm e mũ x, hàm có đạo hàm bằng chính nó.',
         'Mở đầu: lỗ thủng tại α = −1'),
    Beat('h2', 'hook',
         'Đây là tập ba của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'nguyên hàm của một chia x và các hàm số mũ.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, vì sao nguyên hàm của một chia x là lô ga nê pe '
         'của trị tuyệt đối x. Hai, nguyên hàm của e mũ x và a mũ x. '
         'Ba, hai cái bẫy hay gặp: hằng số trên hai khoảng, và nhầm hàm mũ với hàm lũy thừa.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Bắt đầu với x dương. Ta đã biết đạo hàm của lô ga nê pe của x bằng một chia x. '
         'Đọc ngược lại: trên khoảng từ không đến dương vô cùng, nguyên hàm của một chia x là '
         'lô ga nê pe của x cộng C. Trên hình, độ dốc của đường lô ga rít luôn bằng chiều cao của đường một chia x.',
         'Nguyên hàm của 1/x'),
    Beat('c2', 'core',
         'Còn khi x âm thì sao? Lô ga nê pe của x không xác định. Hãy lấy đối xứng đồ thị qua trục tung, '
         'được hàm lô ga nê pe của âm x. Đạo hàm của nó bằng âm một chia âm x, tức là một chia x. '
         'Vậy trên khoảng âm, lô ga nê pe của âm x cũng là một nguyên hàm của một chia x.'),
    Beat('c3', 'core',
         'Gộp hai trường hợp bằng trị tuyệt đối: nguyên hàm của một chia x bằng lô ga nê pe của trị tuyệt đối x, '
         'cộng C. Trị tuyệt đối không phải để trang trí: thiếu nó, công thức sai với mọi x âm.'),
    Beat('c4', 'core',
         'Lưu ý chuyên sâu: hàm một chia x xác định trên hai khoảng rời nhau, nên hai nhánh có thể mang '
         'hai hằng số khác nhau, C một bên phải và C hai bên trái. Hình bên trái cho thấy hai nhánh '
         'được tịnh tiến độc lập mà đạo hàm không thay đổi.'),
    Beat('c5', 'core',
         'Chuyển sang hàm e mũ x. Tính chất nổi tiếng: đạo hàm của e mũ x bằng chính e mũ x. '
         'Vì vậy nguyên hàm của e mũ x là e mũ x cộng C. Trên đồ thị, tại mọi điểm, độ dốc tiếp tuyến '
         'đúng bằng chiều cao của điểm đó.',
         'Hàm số e mũ x'),
    Beat('c6', 'core',
         'Vì sao lại là số e? Xét các đường a mũ x với cơ số a khác nhau. Độ dốc tại x bằng không '
         'chính là lô ga nê pe của a. Khi a tăng dần, độ dốc này tăng theo, và có đúng một cơ số làm độ dốc '
         'bằng một: đó là số e, xấp xỉ hai phẩy bảy một tám.'),
    Beat('c7', 'core',
         'Với cơ số a tổng quát, dương và khác một: đạo hàm của a mũ x bằng a mũ x nhân lô ga nê pe của a. '
         'Chia cho lô ga nê pe của a, ta được nguyên hàm của a mũ x bằng a mũ x chia lô ga nê pe của a, cộng C.',
         'Hàm số a mũ x'),
    Beat('c8', 'core',
         'Áp dụng: nguyên hàm của hai mũ x là hai mũ x chia lô ga nê pe hai. Với cơ số một phần hai, '
         'lô ga nê pe của một phần hai là số âm, bằng âm lô ga nê pe hai, nên kết quả mang dấu trừ. '
         'Nguyên hàm của mười mũ x là mười mũ x chia lô ga nê pe mười.'),
    Beat('c9', 'core',
         'Cái bẫy thứ hai: nhầm hàm mũ với hàm lũy thừa. Khi biến x nằm ở cơ số, như x mũ n, ta tăng số mũ. '
         'Khi biến x nằm ở số mũ, như hai mũ x, ta chia cho lô ga nê pe của cơ số. '
         'Viết nguyên hàm của hai mũ x thành hai mũ x cộng một chia x cộng một là sai hoàn toàn.'),
    Beat('c10', 'core',
         'Đến đây, bảng nguyên hàm cơ bản của chúng ta đã có sáu dòng: hằng số, lũy thừa, một chia x, '
         'e mũ x và a mũ x. Đây là bộ công cụ nền cho mọi bài toán nguyên hàm phía sau.',
         'Bảng nguyên hàm cơ bản'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: tìm nguyên hàm của ba chia x cộng hai e mũ x trừ năm mũ x. Áp dụng quy tắc tuyến tính '
         'cho từng hạng tử: ba lô ga nê pe trị tuyệt đối x, cộng hai e mũ x, trừ năm mũ x chia lô ga nê pe năm, cộng C.',
         'Ví dụ 1: tổng hợp ba công thức'),
    Beat('e2', 'examples',
         'Ví dụ hai: nguyên hàm của x bình phương cộng hai x trừ ba, chia cho x. Tách phân thức: '
         'được x cộng hai trừ ba chia x. Nguyên hàm là x bình phương chia hai, cộng hai x, trừ ba lô ga nê pe '
         'trị tuyệt đối x, cộng C. Hình bên trái kiểm tra trên khoảng x dương.',
         'Ví dụ 2: tách phân thức ra 1/x'),
    Beat('e3', 'examples',
         'Ví dụ ba: nguyên hàm của e mũ x nhân với một cộng e mũ âm x. Nhân phân phối, e mũ x nhân e mũ âm x '
         'bằng một, nên biểu thức trở thành e mũ x cộng một. Nguyên hàm là e mũ x cộng x cộng C.',
         'Ví dụ 3: nhân phân phối với eˣ'),
    Beat('e4', 'examples',
         'Ví dụ bốn, bài toán thực tế. Một quần thể vi khuẩn tăng với tốc độ N phẩy của t bằng năm trăm e mũ t '
         'con mỗi giờ. Lúc đầu có một nghìn năm trăm con. Hỏi sau hai giờ có khoảng bao nhiêu con?',
         'Ví dụ 4: tăng trưởng vi khuẩn'),
    Beat('e5', 'examples',
         'N là nguyên hàm của tốc độ tăng: N của t bằng năm trăm e mũ t cộng C. Điều kiện ban đầu: năm trăm cộng C '
         'bằng một nghìn năm trăm, nên C bằng một nghìn. Tại t bằng hai: năm trăm e bình phương cộng một nghìn, '
         'xấp xỉ bốn nghìn sáu trăm chín mươi lăm con.'),
    Beat('e6', 'examples',
         'Hãy quan sát: số vi khuẩn tăng ngày càng nhanh, vì chính tốc độ năm trăm e mũ t cũng tăng theo thời gian. '
         'Đồ thị N cong dần lên, và đúng hai giờ sau, bộ đếm dừng ở khoảng bốn nghìn sáu trăm chín mươi lăm. '
         'Trong đề thi, dạng câu trả lời ngắn thường yêu cầu làm tròn đến hàng đơn vị như thế này.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f của x bằng hai mũ x cộng một chia x, trên khoảng dương. '
         'Gọi F là một nguyên hàm của f. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: áp dụng hai công thức mới cho từng hạng tử. Ý b sai: đây là cái bẫy nhầm hàm mũ với lũy thừa. '
         'Nguyên hàm đúng của hai mũ x là hai mũ x chia lô ga nê pe hai.'),
    Beat('x3', 'exam',
         'Ý c đúng: F của một bằng hai chia lô ga nê pe hai cộng lô ga nê pe một cộng C, mà lô ga nê pe một bằng không, '
         'nên C bằng không. Ý d sai: F của hai bằng bốn chia lô ga nê pe hai cộng lô ga nê pe hai, '
         'không phải lô ga nê pe bốn.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn, đúng dạng hai nhánh. F là nguyên hàm của một chia x trên tập số thực khác không, '
         'F của một bằng hai và F của âm một bằng ba. Tính F của e cộng F của âm e. '
         'Hai nhánh có hai hằng số: C một bằng hai, C hai bằng ba. Vậy kết quả là một cộng hai, cộng một cộng ba, bằng bảy.',
         'Trả lời ngắn: hai nhánh của ln|x|'),
    Beat('x5', 'exam',
         'Mẹo nhận dạng nhanh. Thấy một chia x: viết lô ga nê pe trị tuyệt đối x, đừng quên trị tuyệt đối. '
         'Thấy e mũ x: giữ nguyên. Thấy a mũ x: giữ nguyên rồi chia lô ga nê pe a. '
         'Còn nếu biến nằm ở cơ số, quay về quy tắc lũy thừa.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba công thức. Nguyên hàm của một chia x là lô ga nê pe trị tuyệt đối x cộng C, xét trên từng khoảng. '
         'Nguyên hàm của e mũ x là e mũ x cộng C. Nguyên hàm của a mũ x là a mũ x chia lô ga nê pe a cộng C.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tìm nguyên hàm của bốn chia x trừ e mũ x. Hai, tìm nguyên hàm của ba mũ x nhân '
         'hai mũ x, gợi ý: gộp hai cơ số. Ba, biết F phẩy bằng e mũ x cộng hai x và F của không bằng ba, tính F của một. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập bốn, ta sẽ xây dựng nguyên hàm của các hàm số lượng giác sin, cos và các hàm liên quan. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'pow_alpha': "integral x^alpha dif x = x^(alpha+1)/(alpha+1) + C, quad coral(alpha != -1)",
    'inv1_q': "integral 1/x dif x = gold(?)",
    'd_ln': "(ln x)' = 1/x, quad x > 0",
    'i_ln_pos': "integral 1/x dif x = ln x + C, quad x > 0",
    'd_lnneg': "(ln(-x))' = (-1)/(-x) = 1/x, quad x < 0",
    'i_ln': "integral 1/x dif x = ln|x| + C",
    'piece_ln': "F(x) = cases(ln x + green(C_1) & \"khi\" x > 0, ln(-x) + purple(C_2) & \"khi\" x < 0)",
    'd_exp': "(e^x)' = e^x",
    'i_exp': "integral e^x dif x = e^x + C",
    'd_ax': "(a^x)' = a^x ln a",
    'd_ax2': "(a^x/(ln a))' = a^x",
    'i_ax': "integral a^x dif x = a^x/(ln a) + C, quad 0 < a != 1",
    'ex_2x': "integral 2^x dif x = 2^x/(ln 2) + C",
    'ex_half': "integral (1/2)^x dif x = (1/2)^x/(ln (1/2)) + C = -(1/2)^x/(ln 2) + C",
    'ex_10x': "integral 10^x dif x = 10^x/(ln 10) + C",
    'pow_vs': "integral x^n dif x = x^(n+1)/(n+1) + C",
    'exp_vs': "integral a^x dif x = a^x/(ln a) + C",
    'trap_ax': "integral 2^x dif x coral(!=) 2^(x+1)/(x+1) + C",
    'tbl1': "integral k dif x = k x + C",
    'tbl2': "integral x^alpha dif x = x^(alpha+1)/(alpha+1) + C",
    'tbl3': "integral 1/x dif x = ln|x| + C",
    'tbl4': "integral e^x dif x = e^x + C",
    'tbl5': "integral a^x dif x = a^x/(ln a) + C",
    'tbl6': "integral 0 dif x = C",
    'e1_task': "integral (3/x + 2e^x - 5^x) dif x",
    'e1_s1': "= 3 integral 1/x dif x + 2 integral e^x dif x - integral 5^x dif x",
    'e1_s2': "= 3 ln|x| + 2 e^x - 5^x/(ln 5) + C",
    'e2_task': "integral (x^2 + 2x - 3)/x dif x",
    'e2_s1': "(x^2 + 2x - 3)/x = x + 2 - 3/x",
    'e2_s2': "= x^2/2 + 2x - 3 ln|x| + C",
    'e3_task': "integral e^x (1 + e^(-x)) dif x",
    'e3_s1': "e^x (1 + e^(-x)) = e^x + e^x e^(-x) = e^x + 1",
    'e3_s2': "integral (e^x + 1) dif x = e^x + x + C",
    'e4_task': "N'(t) = 500 e^t, quad N(0) = 1500",
    'e4_s1': "N(t) = integral 500 e^t dif t = 500 e^t + C",
    'e4_s2': "N(0) = 500 + C = 1500 arrow.double.long C = 1000",
    'e4_s3': "N(2) = 500 e^2 + 1000 approx gold(4695)",
    'tf_f': "f(x) = 2^x + 1/x, quad x > 0",
    'tf_a': "integral f(x) dif x = 2^x \\/ ln 2 + ln x + C",
    'tf_b': "integral 2^x dif x = 2^(x+1) \\/ (x+1) + C",
    'tf_c': "F(1) = 2 \\/ ln 2 arrow.double.long F(x) = 2^x \\/ ln 2 + ln x",
    'tf_d': "F(2) = 4 \\/ ln 2 + ln 4",
    'tf_c_calc': "F(1) = 2/(ln 2) + ln 1 + C arrow.double.long C = 0",
    'tf_d_calc': "F(2) = 4/(ln 2) + ln 2 coral(!=) 4/(ln 2) + ln 4",
    'sa_task': "F'(x) = 1/x, quad F(1) = 2, quad F(-1) = 3, quad F(e) + F(-e) = ?",
    'sa_s2': "C_1 = F(1) = 2, quad C_2 = F(-1) = 3",
    'sa_s3': "F(e) + F(-e) = (1 + 2) + (1 + 3) = gold(7)",
    'rec1': "1/x arrow.r.long ln|x|",
    'rec2': "e^x arrow.r.long e^x",
    'rec3': "a^x arrow.r.long a^x/(ln a)",
    'sum1': "integral 1/x dif x = ln|x| + C",
    'sum2': "integral e^x dif x = e^x + C",
    'sum3': "integral a^x dif x = a^x/(ln a) + C",
    'hw1': "integral (4/x - e^x) dif x",
    'hw2': "integral 3^x dot 2^x dif x",
    'hw3': "F'(x) = e^x + 2x, quad F(0) = 3, quad F(1) = ?",
    'hw_ans1': "4 ln|x| - e^x + C",
    'hw_ans2': "6^x/(ln 6) + C",
    'hw_ans3': "F(1) = e + 3",
    'next1': "integral sin x dif x = -cos x + C, quad integral cos x dif x = sin x + C",
    'next2': "integral 1/(cos^2 x) dif x = tan x + C",
}

EXERCISES = (
    ('Tìm ∫(4/x − eˣ) dx.', '4 ln|x| − eˣ + C'),
    ('Tìm ∫3ˣ·2ˣ dx.', '6ˣ/ln 6 + C'),
    ("Biết F'(x) = eˣ + 2x, F(0) = 3. Tính F(1).", 'F(1) = e + 3'),
)

TRUE_FALSE = (
    ('∫f(x)dx = 2ˣ/ln 2 + ln x + C', True),
    ('∫2ˣ dx = 2ˣ⁺¹/(x + 1) + C', False),
    ('F(1) = 2/ln 2 ⇒ F(x) = 2ˣ/ln 2 + ln x', True),
    ('F(2) = 4/ln 2 + ln 4', False),
)

x, t, C = sp.symbols('x t C', real=True)
P = sp.symbols('P', positive=True)       # a positive variable
Q = sp.symbols('Q', negative=True)       # a negative variable
A = sp.symbols('A', positive=True)


def same_primitive(F, f, var=x):
    return sp.simplify(sp.diff(F, var) - f) == 0


def validate() -> bool:
    ids = [b.id for b in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(b.part) for b in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for b in BEATS if b.chapter) >= 3
    assert all(len(b.text.split()) >= 12 for b in BEATS)

    # 1/x on each interval, ln|x|
    assert same_primitive(sp.log(P), 1/P, P)
    assert same_primitive(sp.log(-Q), 1/Q, Q)
    assert sp.simplify(sp.log(sp.Abs(Q)) - sp.log(-Q)) == 0
    # e^x and a^x
    assert same_primitive(sp.exp(x), sp.exp(x))
    assert sp.simplify(sp.diff(A**x, x) - A**x*sp.log(A)) == 0
    assert same_primitive(A**x/sp.log(A), A**x)
    # slope of a^x at 0 is ln a; equals 1 exactly for a = e
    assert sp.diff(A**x, x).subs(x, 0) == sp.log(A) and sp.log(sp.E) == 1
    # applications
    assert same_primitive(2**x/sp.log(2), 2**x) and same_primitive(10**x/sp.log(10), 10**x)
    half = sp.Rational(1, 2)
    assert same_primitive(-half**x/sp.log(2), half**x) and sp.log(half) == -sp.log(2)
    # power vs exponential trap
    assert not same_primitive(2**(x + 1)/(x + 1), 2**x)
    # example 1
    assert same_primitive(3*sp.log(P) + 2*sp.exp(P) - 5**P/sp.log(5), 3/P + 2*sp.exp(P) - 5**P, P)
    # example 2
    assert sp.simplify((P**2 + 2*P - 3)/P - (P + 2 - 3/P)) == 0
    assert same_primitive(P**2/2 + 2*P - 3*sp.log(P), (P**2 + 2*P - 3)/P, P)
    # example 3
    assert sp.simplify(sp.exp(x)*(1 + sp.exp(-x)) - (sp.exp(x) + 1)) == 0
    assert same_primitive(sp.exp(x) + x, sp.exp(x)*(1 + sp.exp(-x)))
    # example 4: bacteria
    N = 500*sp.exp(t) + C
    c4 = sp.solve(sp.Eq(N.subs(t, 0), 1500), C)[0]
    assert c4 == 1000
    N2 = (N.subs(C, c4)).subs(t, 2)
    assert round(float(N2)) == 4695
    # true/false on (0, +inf)
    f = 2**P + 1/P
    F = 2**P/sp.log(2) + sp.log(P)
    cF = sp.solve(sp.Eq(F.subs(P, 1) + C, 2/sp.log(2)), C)[0]
    claims = (
        same_primitive(F, f, P),
        same_primitive(2**(P + 1)/(P + 1), 2**P, P),
        cF == 0,
        sp.simplify((F + cF).subs(P, 2) - (4/sp.log(2) + sp.log(4))) == 0,
    )
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    assert sp.simplify((F + cF).subs(P, 2) - (4/sp.log(2) + sp.log(2))) == 0
    # short answer: two branches with C1 = 2, C2 = 3
    c1, c2 = 2, 3
    assert sp.log(1) + c1 == 2 and sp.log(-(-1)) + c2 == 3
    assert sp.simplify((sp.log(sp.E) + c1) + (sp.log(-(-sp.E)) + c2)) == 7
    # exercises
    assert same_primitive(4*sp.log(P) - sp.exp(P), 4/P - sp.exp(P), P)
    assert sp.simplify(3**x*2**x - 6**x) == 0 and same_primitive(6**x/sp.log(6), 6**x)
    F3 = sp.exp(x) + x**2 + 2
    assert same_primitive(F3, sp.exp(x) + 2*x) and F3.subs(x, 0) == 3 and F3.subs(x, 1) == sp.E + 3
    # next episode teaser
    assert same_primitive(-sp.cos(x), sp.sin(x)) and same_primitive(sp.tan(x), 1/sp.cos(x)**2)
    return True


validate()

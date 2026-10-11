"""INT13 – Tính chất của tích phân: tuyến tính, cộng khoảng, đổi cận, so sánh.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT13',
    'number': 13,
    'title': 'Tính chất của tích phân',
    'subtitle': 'Tuyến tính, cộng khoảng, so sánh',
    'next_code': 'INT14',
    'next_title': 'Tích phân chứa trị tuyệt đối & hàm từng khúc',
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
         'Đề thi thường cho một câu như sau: biết tích phân từ không đến hai của f bằng ba, tích phân của g bằng âm một, '
         'hãy tính tích phân của hai f trừ ba g cộng một. Ta không hề biết f và g là hàm gì! '
         'Bí quyết nằm ở các tính chất của tích phân, chủ đề của tập hôm nay.',
         'Mở đầu: tính tích phân khi không biết hàm số'),
    Beat('h2', 'hook',
         'Đây là tập mười ba của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: các tính chất của tích phân.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba nhóm tính chất. Một, tuyến tính: tách tổng và đưa hằng số ra ngoài. '
         'Hai, cộng khoảng và đổi cận. Ba, so sánh tích phân, ước lượng, và tính chất hàm chẵn, hàm lẻ.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Tính chất tuyến tính. Tích phân của k f cộng m g bằng k nhân tích phân của f, cộng m nhân tích phân của g. '
         'Lý do rất đơn giản: nguyên hàm có tính chất này, nên hiệu F của b trừ F của a cũng vậy. '
         'Về hình học, nhân f với k thì diện tích cũng nhân k.',
         'Tính chất tuyến tính'),
    Beat('c2', 'core',
         'Áp dụng cho bài mở đầu. Tích phân của hai f trừ ba g cộng một bằng hai nhân ba, trừ ba nhân âm một, '
         'cộng tích phân của một trên đoạn dài hai, tức là cộng hai. Kết quả: sáu cộng ba cộng hai, bằng mười một. '
         'Đừng quên số hạng hằng số: tích phân của một bằng độ dài đoạn.'),
    Beat('c3', 'core',
         'Tính chất cộng khoảng. Với b nằm giữa a và c, tích phân từ a đến c bằng tích phân từ a đến b cộng tích phân từ b đến c. '
         'Trên hình, miền diện tích được cắt làm hai mảnh tại b. Nhờ quy ước đổi cận, công thức còn đúng cả khi b nằm ngoài đoạn.',
         'Cộng khoảng và đổi cận'),
    Beat('c4', 'core',
         'Ví dụ: biết tích phân từ không đến một của f bằng hai và từ không đến ba bằng năm. Khi đó tích phân từ một đến ba '
         'bằng năm trừ hai, bằng ba. Và tích phân từ ba đến một, đổi chỗ cận, bằng âm ba.'),
    Beat('c4b', 'core',
         'Một chi tiết tinh tế: điểm chia b không nhất thiết nằm giữa a và c. Ví dụ, tích phân từ không đến một bằng tích phân '
         'từ không đến ba cộng tích phân từ ba đến một. Phần đi quá rồi quay lại tự triệt tiêu nhờ quy ước đổi cận. '
         'Vì vậy công thức cộng khoảng đúng với mọi ba số a, b, c trong miền liên tục.'),
    Beat('c5', 'core',
         'Tính chất so sánh. Nếu f lớn hơn hoặc bằng g trên đoạn từ a đến b thì tích phân của f lớn hơn hoặc bằng tích phân của g. '
         'Đặc biệt, f không âm thì tích phân không âm. Nếu m nhỏ hơn f nhỏ hơn M, thì tích phân bị kẹp giữa m nhân b trừ a '
         'và M nhân b trừ a, giữa hai hình chữ nhật.',
         'So sánh và ước lượng'),
    Beat('c6', 'core',
         'Hàm chẵn và hàm lẻ trên đoạn đối xứng từ âm a đến a. Với hàm lẻ, phần bên trái và bên phải có dấu ngược nhau, '
         'nên tích phân bằng không. Với hàm chẵn, hai phần bằng nhau, nên tích phân bằng hai lần tích phân từ không đến a.',
         'Hàm chẵn, hàm lẻ'),
    Beat('c7', 'core',
         'Cái bẫy quen thuộc: tích phân của một tích không bằng tích các tích phân. Ví dụ, tích phân từ không đến một của '
         'x nhân x bằng một phần ba, trong khi tích phân của x nhân với chính nó chỉ bằng một phần tư. '
         'Tương tự với thương.',
         'Bẫy tích và thương'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: hàm từng khúc. f bằng x bình phương khi x nhỏ hơn hoặc bằng một, bằng hai x trừ một khi x lớn hơn một. '
         'Tính tích phân từ không đến hai. Cắt tại một: tích phân từ không đến một của x bình phương bằng một phần ba, '
         'cộng tích phân từ một đến hai của hai x trừ một, bằng hai. Tổng là bảy phần ba.',
         'Ví dụ 1: cắt tại điểm nối'),
    Beat('e2', 'examples',
         'Ví dụ hai: ước lượng tích phân từ không đến một của e mũ x bình phương, một tích phân không tính được bằng nguyên hàm '
         'sơ cấp. Trên đoạn này, e mũ x bình phương nằm giữa một và e. Vậy tích phân nằm giữa một và e. '
         'Máy tính cho giá trị xấp xỉ một phẩy bốn sáu, đúng trong khoảng đó.',
         'Ví dụ 2: ước lượng'),
    Beat('e3', 'examples',
         'Ví dụ ba: tích phân từ âm hai đến hai của x lập phương cộng ba x bình phương. Phần x lập phương là hàm lẻ, '
         'cho không. Phần ba x bình phương là hàm chẵn, bằng hai lần tích phân từ không đến hai, tức là hai nhân tám, bằng mười sáu.',
         'Ví dụ 3: tách chẵn lẻ'),
    Beat('e4', 'examples',
         'Ví dụ bốn, bài toán ngược: tìm số dương m sao cho tích phân từ không đến m của hai x cộng một bằng sáu. '
         'Tích phân bằng m bình phương cộng m. Giải phương trình m bình phương cộng m trừ sáu bằng không, '
         'được m bằng hai hoặc m bằng âm ba. Vì m dương nên m bằng hai.',
         'Ví dụ 4: tìm cận'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Biết tích phân từ một đến ba của f bằng bốn, của g bằng âm hai, '
         'và tích phân từ ba đến năm của f bằng một. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: bốn cộng âm hai bằng hai. Ý b đúng: ba nhân bốn bằng mười hai.'),
    Beat('x3', 'exam',
         'Ý c sai: cộng khoảng cho bốn cộng một, bằng năm, không phải ba. Ý d sai: đây là bẫy tích. '
         'Tích phân của f nhân g không thể suy ra từ hai tích phân riêng lẻ.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. Biết tích phân từ không đến hai của f bằng năm. Tính tích phân từ không đến hai của ba f trừ hai x. '
         'Theo tuyến tính: ba nhân năm, trừ tích phân của hai x từ không đến hai bằng bốn. Kết quả mười một.',
         'Trả lời ngắn và mẹo hàm thay thế'),
    Beat('x5', 'exam',
         'Mẹo hàm thay thế: khi đề chỉ cho giá trị tích phân, hãy chọn một hàm hằng thỏa điều kiện. Ở bài vừa rồi, '
         'chọn f bằng năm phần hai trên đoạn dài hai, rồi bấm máy tính tích phân của ba nhân năm phần hai trừ hai x. '
         'Máy cho đúng mười một. Mẹo này chỉ dùng khi đề hỏi biểu thức tuyến tính theo f.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, tuyến tính: tách tổng hiệu, đưa hằng số ra ngoài, và tích phân của hằng số bằng hằng số nhân độ dài đoạn. '
         'Hai, cộng khoảng và đổi cận. Ba, so sánh, ước lượng, và tính chất chẵn lẻ trên đoạn đối xứng.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, biết tích phân từ không đến ba của f bằng sáu và của g bằng hai, tính tích phân của f trừ hai g cộng ba. '
         'Hai, tích phân từ âm hai đến hai của x lập phương cộng x. Ba, tích phân từ âm một đến một của ba x bình phương cộng năm x. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập mười bốn, ta xử lý tích phân chứa trị tuyệt đối và hàm cho theo từng khúc: xét dấu rồi tách cận. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "integral_0^2 f = 3, quad integral_0^2 g = -1 arrow.double.long integral_0^2 (2f - 3g + 1) dif x = gold(?)",
    'lin': "integral_a^b [k f(x) + m g(x)] dif x = k integral_a^b f(x) dif x + m integral_a^b g(x) dif x",
    'lin_ex': "integral_0^2 (2f - 3g + 1) dif x = 2 dot 3 - 3 dot (-1) + 2 = gold(11)",
    'const': "integral_a^b k dif x = k(b - a)",
    'chasles': "integral_a^c f(x) dif x = integral_a^b f(x) dif x + integral_b^c f(x) dif x",
    'ch_ex1': "integral_0^1 f = 2, quad integral_0^3 f = 5 arrow.double.long integral_1^3 f = 3",
    'ch_ex2': "integral_3^1 f = -integral_1^3 f = -3",
    'cmp1': "f(x) >= g(x) space forall x in [a; b] arrow.double.long integral_a^b f >= integral_a^b g",
    'ch_out': "integral_0^1 f = integral_0^3 f + integral_3^1 f",
    'e4_s1': "integral_0^m (2x + 1) dif x = m^2 + m = 6 arrow.double.long m = gold(2) quad (m > 0)",
    'cmp2': "m <= f <= M arrow.double.long m(b - a) <= integral_a^b f <= M(b - a)",
    'odd': "f(-x) = -f(x): quad integral_(-a)^a f(x) dif x = 0",
    'even': "f(-x) = f(x): quad integral_(-a)^a f(x) dif x = 2 integral_0^a f(x) dif x",
    'trap': "integral_0^1 x dot x dif x = 1/3 coral(!=) integral_0^1 x dif x dot integral_0^1 x dif x = 1/4",
    'e1_f': "f(x) = cases(x^2 & \"khi\" x <= 1, 2x - 1 & \"khi\" x > 1)",
    'e1_s1': "integral_0^2 f = integral_0^1 x^2 dif x + integral_1^2 (2x - 1) dif x = 1/3 + 2 = gold(7/3)",
    'e2_s1': "1 <= e^(x^2) <= e arrow.double.long 1 <= integral_0^1 e^(x^2) dif x <= e",
    'e2_s2': "integral_0^1 e^(x^2) dif x approx \"1,46\"",
    'e3_s1': "integral_(-2)^2 (x^3 + 3x^2) dif x = 0 + 2 integral_0^2 3x^2 dif x = gold(16)",
    'tf_given': "integral_1^3 f = 4, quad integral_1^3 g = -2, quad integral_3^5 f = 1",
    'tf_a': "integral_1^3 [f(x) + g(x)] dif x = 2",
    'tf_b': "integral_1^3 3f(x) dif x = 12",
    'tf_c': "integral_1^5 f(x) dif x = 3",
    'tf_d': "integral_1^3 f(x) g(x) dif x = -8",
    'tf_c_calc': "integral_1^5 f = integral_1^3 f + integral_3^5 f = 4 + 1 = 5 coral(!=) 3",
    'sa_task': "integral_0^2 f(x) dif x = 5, quad integral_0^2 [3f(x) - 2x] dif x = ?",
    'sa_s1': "= 3 dot 5 - integral_0^2 2x dif x = 15 - 4 = gold(11)",
    'tip': "f(x) = 5/2 arrow.double.long integral_0^2 (3 dot 5/2 - 2x) dif x = 11",
    'sum1': "integral (k f + m g) = k integral f + m integral g",
    'sum2': "integral_a^c = integral_a^b + integral_b^c",
    'sum3': "f(-x) = -f(x) arrow.double.long integral_(-a)^a f = 0",
    'hw1': "integral_0^3 f = 6, quad integral_0^3 g = 2, quad integral_0^3 (f - 2g + 3) dif x = ?",
    'hw2': "integral_(-2)^2 (x^3 + x) dif x",
    'hw3': "integral_(-1)^1 (3x^2 + 5x) dif x",
    'hw_ans1': "11",
    'hw_ans2': "0",
    'hw_ans3': "2",
    'next1': "integral_0^3 |x^2 - 3x + 2| dif x",
    'next2': "= integral_0^1 (dots) - integral_1^2 (dots) + integral_2^3 (dots)",
}

EXERCISES = (
    ('∫₀³f = 6, ∫₀³g = 2: tính ∫₀³(f − 2g + 3) dx.', '11'),
    ('∫₋₂²(x³ + x) dx', '0'),
    ('∫₋₁¹(3x² + 5x) dx', '2'),
)

TRUE_FALSE = (
    ('∫₁³[f + g] dx = 2', True),
    ('∫₁³3f dx = 12', True),
    ('∫₁⁵f dx = 3', False),
    ('∫₁³f·g dx = −8', False),
)

x = sp.symbols('x', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R = sp.integrate, sp.Rational
    assert 2*3 - 3*(-1) + I(1, (x, 0, 2)) == 11
    # linearity with concrete functions
    f, g = x**2, sp.sin(x)
    assert sp.simplify(I(2*f - 3*g, (x, 0, 2)) - (2*I(f, (x, 0, 2)) - 3*I(g, (x, 0, 2)))) == 0
    # Chasles
    assert sp.simplify(I(f, (x, 0, 3)) - (I(f, (x, 0, 1)) + I(f, (x, 1, 3)))) == 0
    assert 5 - 2 == 3 and I(f, (x, 3, 1)) == -I(f, (x, 1, 3))
    m = sp.symbols('m', positive=True)
    assert sp.solve(sp.Eq(I(2*x + 1, (x, 0, m)), 6), m) == [2]
    assert sp.simplify(I(f, (x, 0, 1)) - (I(f, (x, 0, 3)) + I(f, (x, 3, 1)))) == 0
    # comparison / bounds
    assert 1 <= float(I(sp.exp(x**2), (x, 0, 1))) <= float(sp.E)
    assert round(float(sp.Integral(sp.exp(x**2), (x, 0, 1)).evalf()), 2) == 1.46
    # odd / even
    assert I(x**3, (x, -2, 2)) == 0 and I(3*x**2, (x, -2, 2)) == 2*I(3*x**2, (x, 0, 2)) == 16
    # product trap
    assert I(x*x, (x, 0, 1)) == R(1, 3) and I(x, (x, 0, 1))**2 == R(1, 4)
    # example 1
    assert I(x**2, (x, 0, 1)) + I(2*x - 1, (x, 1, 2)) == R(7, 3)
    # true / false with witness functions on [1, 3] and [3, 5]
    fw = sp.Piecewise((2, x <= 3), (R(1, 2), True))      # ∫1..3 = 4, ∫3..5 = 1
    gw = -1 + 0*x                                        # ∫1..3 = -2
    claims = (I(fw + gw, (x, 1, 3)) == 2, I(3*fw, (x, 1, 3)) == 12, I(fw, (x, 1, 5)) == 3,
              I(fw*gw, (x, 1, 3)) == -8)
    assert I(fw, (x, 1, 3)) == 4 and I(fw, (x, 3, 5)) == 1 and I(gw, (x, 1, 3)) == -2
    # d) is not determined: f = x, g = -1 has the same integrals but ∫fg = -4
    assert I(x, (x, 1, 3)) == 4 and I(x*(-1), (x, 1, 3)) == -4
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer and replacement-function trick
    assert 3*5 - I(2*x, (x, 0, 2)) == 11 and I(3*R(5, 2) - 2*x, (x, 0, 2)) == 11
    # exercises
    assert 6 - 2*2 + 3*3 == 11 and I(x**3 + x, (x, -2, 2)) == 0 and I(3*x**2 + 5*x, (x, -1, 1)) == 2
    return True


validate()

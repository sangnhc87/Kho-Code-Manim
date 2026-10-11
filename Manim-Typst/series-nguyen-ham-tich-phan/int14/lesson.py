"""INT14 – Tích phân chứa trị tuyệt đối & hàm từng khúc: xét dấu rồi tách cận.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT14',
    'number': 14,
    'title': 'Tích phân chứa trị tuyệt đối',
    'subtitle': 'Và hàm từng khúc: xét dấu rồi tách cận',
    'next_code': 'INT15',
    'next_title': 'Tích phân, độ dời và quãng đường',
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
         'Tính tích phân từ không đến ba của trị tuyệt đối x bình phương trừ ba x cộng hai. '
         'Nhiều bạn bỏ dấu trị tuyệt đối ra ngoài, tính tích phân bên trong được ba phần hai, rồi lấy trị tuyệt đối. '
         'Kết quả đó sai! Đáp số đúng là mười một phần sáu. Vì sao lại lệch nhau?',
         'Mở đầu: bỏ trị tuyệt đối ra ngoài có được không?'),
    Beat('h2', 'hook',
         'Đây là tập mười bốn của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'tích phân chứa trị tuyệt đối và hàm cho theo từng khúc.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, ý nghĩa hình học: trị tuyệt đối lật phần âm lên trên trục. '
         'Hai, quy trình ba bước: tìm nghiệm, xét dấu, tách cận. Ba, cách xử lý hàm từng khúc và hàm max, min.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Nhìn đồ thị của f bằng x bình phương trừ ba x cộng hai trên đoạn từ không đến ba. '
         'Phần từ một đến hai nằm dưới trục hoành, mang dấu âm, nên khi tính tích phân nó bị trừ đi. '
         'Lấy trị tuyệt đối thì phần âm được lật lên trên trục, và mọi mảnh đều được cộng vào.',
         'Ý nghĩa hình học: lật phần âm'),
    Beat('c2', 'core',
         'Vì vậy tích phân của trị tuyệt đối f chính là tổng diện tích hình học giữa đồ thị và trục hoành. '
         'Nó luôn lớn hơn hoặc bằng trị tuyệt đối của tích phân. Dấu bằng chỉ xảy ra khi f không đổi dấu trên đoạn.'),
    Beat('c3', 'core',
         'Định nghĩa trị tuyệt đối cho ta công cụ: trị tuyệt đối của f bằng f khi f không âm, '
         'và bằng trừ f khi f âm. Muốn bỏ dấu trị tuyệt đối, ta phải biết dấu của f trên từng đoạn.',
         'Quy trình ba bước'),
    Beat('c4', 'core',
         'Quy trình ba bước. Bước một: giải f bằng không, giữ lại các nghiệm nằm trong đoạn lấy tích phân. '
         'Bước hai: lập bảng xét dấu của f. Bước ba: tách cận tại các nghiệm, đoạn nào f âm thì đổi dấu, rồi tính từng tích phân.'),
    Beat('c5', 'core',
         'Áp dụng cho bài mở đầu. Phương trình x bình phương trừ ba x cộng hai bằng không có hai nghiệm một và hai, '
         'cả hai đều nằm trong đoạn từ không đến ba. Bảng xét dấu: dương, âm, dương.'),
    Beat('c5b', 'core',
         'Lưu ý: chỉ giữ những nghiệm nằm trong đoạn lấy tích phân. Nếu trên cả đoạn f không đổi dấu, '
         'ta được phép đưa trị tuyệt đối ra ngoài. Ví dụ, trên đoạn từ hai đến ba, x bình phương trừ ba x cộng hai không âm, '
         'nên tích phân của trị tuyệt đối bằng trị tuyệt đối của tích phân, bằng năm phần sáu. '
         'Còn trên đoạn từ không đến ba thì không được, vì f đổi dấu.'),
    Beat('c6', 'core',
         'Một ví dụ dễ hình dung: tích phân từ âm một đến hai của trị tuyệt đối x. Đồ thị là hai tam giác vuông cân. '
         'Tam giác bên trái có diện tích một phần hai, tam giác bên phải có diện tích hai. Tổng là năm phần hai.'),
    Beat('c7', 'core',
         'Hàm cho theo từng khúc cũng xử lý bằng cách tách cận, nhưng điểm cắt là điểm nối giữa các công thức. '
         'Trên mỗi đoạn con, ta dùng đúng công thức của khúc đó. Hàm max và min cũng là hàm từng khúc: '
         'so sánh hai hàm để biết hàm nào lớn hơn trên từng đoạn.',
         'Hàm từng khúc, max và min'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, hoàn thành bài mở đầu. Tách thành ba tích phân: từ không đến một giữ nguyên, từ một đến hai đổi dấu, '
         'từ hai đến ba giữ nguyên. Ba giá trị lần lượt là năm phần sáu, một phần sáu và năm phần sáu. '
         'Tổng bằng mười một phần sáu.',
         'Ví dụ 1: hoàn thành bài mở đầu'),
    Beat('e2', 'examples',
         'Ví dụ hai: tích phân từ không đến pi của trị tuyệt đối cốt x. Cốt x đổi dấu tại pi phần hai. '
         'Từ không đến pi phần hai, cốt x dương, tích phân bằng một. Từ pi phần hai đến pi, cốt x âm, đổi dấu cũng được một. '
         'Kết quả là hai, trong khi tích phân của cốt x không có trị tuyệt đối lại bằng không.',
         'Ví dụ 2: hàm lượng giác'),
    Beat('e3', 'examples',
         'Ví dụ ba: tích phân từ không đến hai của max của x và x bình phương. Trên đoạn từ không đến một, '
         'x lớn hơn x bình phương. Trên đoạn từ một đến hai, x bình phương lớn hơn. '
         'Vậy tích phân bằng một phần hai cộng bảy phần ba, bằng mười bảy phần sáu.',
         'Ví dụ 3: hàm max'),
    Beat('e4', 'examples',
         'Ví dụ bốn: hàm f bằng x bình phương cộng a khi x nhỏ hơn hoặc bằng một, bằng hai x cộng một khi x lớn hơn một. '
         'Tìm a để f liên tục, rồi tính tích phân từ không đến hai. Tại x bằng một, hai khúc phải gặp nhau: '
         'một cộng a bằng ba, nên a bằng hai.',
         'Ví dụ 4: hàm từng khúc có tham số'),
    Beat('e5', 'examples',
         'Khi a bằng hai, cắt tại điểm nối x bằng một. Tích phân từ không đến một của x bình phương cộng hai bằng bảy phần ba. '
         'Tích phân từ một đến hai của hai x cộng một bằng bốn. Tổng là mười chín phần ba.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f bằng x bình phương trừ bốn trên đoạn từ không đến ba. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: với x từ không đến hai, x bình phương không vượt quá bốn. '
         'Ý b đúng: tích phân từ không đến ba của x bình phương trừ bốn bằng chín trừ mười hai, bằng âm ba.'),
    Beat('x3', 'exam',
         'Ý c sai: đây chính là cái bẫy bỏ trị tuyệt đối ra ngoài. Ý d đúng: tách cận tại hai, '
         'đoạn đầu đổi dấu được mười sáu phần ba, đoạn sau được bảy phần ba, tổng là hai mươi ba phần ba.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: tính tích phân từ không đến hai của trị tuyệt đối e mũ x trừ hai, làm tròn đến hàng phần trăm. '
         'e mũ x bằng hai khi x bằng l n hai. Trước l n hai, biểu thức âm nên đổi dấu, sau đó giữ nguyên.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Tính hai tích phân rồi cộng lại, ta được e bình phương trừ bảy cộng bốn l n hai, xấp xỉ ba phẩy một sáu. '
         'Ghi vào phiếu trả lời: ba, phẩy, một, sáu. Em có thể bấm máy tính với hàm Abs để kiểm tra kết quả.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, tích phân của trị tuyệt đối là tổng diện tích, phần âm được lật lên. '
         'Hai, quy trình: tìm nghiệm trong đoạn, xét dấu, tách cận và đổi dấu đoạn âm. '
         'Ba, hàm từng khúc và hàm max, min: cắt tại điểm nối hoặc giao điểm.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tích phân từ không đến hai của trị tuyệt đối x trừ một. '
         'Hai, tích phân từ không đến hai pi của trị tuyệt đối sin x. Ba, tích phân từ không đến ba của trị tuyệt đối '
         'x bình phương trừ một. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập mười lăm, ta dùng đúng ý tưởng này cho chuyển động: tích phân của vận tốc cho độ dời, '
         'còn tích phân của trị tuyệt đối vận tốc mới là quãng đường. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "integral_0^3 abs(x^2 - 3x + 2) dif x = gold(?)",
    'hook_wrong': "abs(integral_0^3 (x^2 - 3x + 2) dif x) = 3/2 quad coral(times)",
    'hook_right': "integral_0^3 abs(x^2 - 3x + 2) dif x = 11/6 quad green(checkmark)",
    'f_def': "f(x) = x^2 - 3x + 2",
    'signed': "integral_0^3 f(x) dif x = 5/6 - 1/6 + 5/6 = 3/2",
    'flipped': "integral_0^3 abs(f(x)) dif x = 5/6 + 1/6 + 5/6 = 11/6",
    'ineq': "integral_a^b abs(f(x)) dif x >= abs(integral_a^b f(x) dif x)",
    'absdef': "abs(f(x)) = cases(f(x) & \"khi\" f(x) >= 0, -f(x) & \"khi\" f(x) < 0)",
    'roots': "x^2 - 3x + 2 = 0 arrow.double.long x = 1 in [0; 3], quad x = 2 in [0; 3]",
    'out_ok': "integral_2^3 abs(x^2 - 3x + 2) dif x = abs(integral_2^3 (x^2 - 3x + 2) dif x) = 5/6",
    'out_no': "integral_0^3 abs(x^2 - 3x + 2) dif x coral(!=) abs(integral_0^3 (x^2 - 3x + 2) dif x)",
    'absx': "integral_(-1)^2 abs(x) dif x = 1/2 + 2 = gold(5/2)",
    'piece': "integral_a^b f(x) dif x = integral_a^c f_1(x) dif x + integral_c^b f_2(x) dif x",
    'maxmin': "max(f, g) = cases(f & \"khi\" f >= g, g & \"khi\" f < g)",
    'e1_s1': "integral_0^3 abs(f) = integral_0^1 f dif x - integral_1^2 f dif x + integral_2^3 f dif x",
    'e1_s2': "= 5/6 + 1/6 + 5/6 = gold(11/6)",
    'e2_task': "integral_0^pi abs(cos x) dif x",
    'e2_s1': "= integral_0^(pi\\/2) cos x dif x - integral_(pi\\/2)^pi cos x dif x = 1 + 1 = gold(2)",
    'e2_s2': "integral_0^pi cos x dif x = 0",
    'e3_task': "integral_0^2 max(x, x^2) dif x",
    'e3_s1': "= integral_0^1 x dif x + integral_1^2 x^2 dif x = 1/2 + 7/3 = gold(17/6)",
    'e4_f': "f(x) = cases(x^2 + a & \"khi\" x <= 1, 2x + 1 & \"khi\" x > 1)",
    'e4_s1': "1 + a = 2 dot 1 + 1 arrow.double.long a = gold(2)",
    'e5_s1': "integral_0^2 f = integral_0^1 (x^2 + 2) dif x + integral_1^2 (2x + 1) dif x",
    'e5_s2': "= 7/3 + 4 = gold(19/3)",
    'tf_given': "f(x) = x^2 - 4, quad x in [0; 3]",
    'tf_a': "f(x) <= 0 quad forall x in [0; 2]",
    'tf_b': "integral_0^3 f(x) dif x = -3",
    'tf_c': "integral_0^3 abs(f(x)) dif x = 3",
    'tf_d': "integral_0^3 abs(f(x)) dif x = 23/3",
    'tf_d_calc': "integral_0^2 (4 - x^2) dif x + integral_2^3 (x^2 - 4) dif x = 16/3 + 7/3 = 23/3",
    'sa_task': "integral_0^2 abs(e^x - 2) dif x approx ?",
    'sa_s1': "e^x = 2 arrow.double.long x = ln 2",
    'sa_s2': "= integral_0^(ln 2) (2 - e^x) dif x + integral_(ln 2)^2 (e^x - 2) dif x",
    'sa_s3': "= (2 ln 2 - 1) + (e^2 - 6 + 2 ln 2) = e^2 - 7 + 4 ln 2 approx gold(\"3,16\")",
    'sum_piece': "integral_a^b f = integral_a^c f_1 + integral_c^b f_2",
    'sum2': "integral_a^b abs(f) = sum plus.minus integral_(x_i)^(x_(i+1)) f",
    'sum3': "integral_a^b abs(f) >= abs(integral_a^b f)",
    'hw1': "integral_0^2 abs(x - 1) dif x",
    'hw2': "integral_0^(2pi) abs(sin x) dif x",
    'hw3': "integral_0^3 abs(x^2 - 1) dif x",
    'hw_ans1': "1",
    'hw_ans2': "4",
    'hw_ans3': "22/3",
    'next1': "d = integral_(t_1)^(t_2) v(t) dif t",
    'next2': "s = integral_(t_1)^(t_2) abs(v(t)) dif t",
}

EXERCISES = (
    ('∫₀² |x − 1| dx', '1'),
    ('∫₀^2π |sin x| dx', '4'),
    ('∫₀³ |x² − 1| dx', '22/3'),
)

TRUE_FALSE = (
    ('f(x) ≤ 0 với mọi x ∈ [0; 2]', True),
    ('∫₀³ f(x) dx = −3', True),
    ('∫₀³ |f(x)| dx = 3', False),
    ('∫₀³ |f(x)| dx = 23/3', True),
)

x = sp.symbols('x', real=True)


def abs_integral(expr, lo, hi):
    """∫|expr| on [lo, hi] by the episode's own method: split at the roots, add |piece|."""
    cuts = sorted({lo, hi, *[r for r in sp.solveset(expr, x, sp.Interval(lo, hi))]}, key=float)
    return sp.nsimplify(sum(abs(sp.integrate(expr, (x, p, q))) for p, q in zip(cuts, cuts[1:])))


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, A, AI = sp.integrate, sp.Rational, sp.Abs, abs_integral
    f = x**2 - 3*x + 2
    # hook: |∫f| = 3/2 but ∫|f| = 11/6, pieces 5/6, -1/6, 5/6
    assert I(f, (x, 0, 3)) == R(3, 2)
    assert [I(f, (x, 0, 1)), I(f, (x, 1, 2)), I(f, (x, 2, 3))] == [R(5, 6), -R(1, 6), R(5, 6)]
    assert AI(f, 0, 3) == R(11, 6)
    assert sorted(sp.solve(f, x)) == [1, 2]
    assert [sp.sign(f.subs(x, v)) for v in (R(1, 2), R(3, 2), R(5, 2))] == [1, -1, 1]
    assert AI(f, 2, 3) == I(f, (x, 2, 3)) == R(5, 6) and AI(f, 0, 3) != abs(I(f, (x, 0, 3)))
    # |x| on [-1, 2]
    assert AI(x, -1, 2) == R(5, 2) and AI(x, -1, 0) == R(1, 2)
    # |cos x|
    assert AI(sp.cos(x), 0, sp.pi) == 2 and I(sp.cos(x), (x, 0, sp.pi)) == 0
    assert I(sp.cos(x), (x, 0, sp.pi / 2)) == 1 and -I(sp.cos(x), (x, sp.pi / 2, sp.pi)) == 1
    # max(x, x^2)
    assert I(sp.Max(x, x**2), (x, 0, 2)) == R(17, 6) == R(1, 2) + R(7, 3)
    # piecewise with parameter
    a = sp.symbols('a')
    assert sp.solve(sp.Eq(1 + a, 2*1 + 1), a) == [2]
    fp = sp.Piecewise((x**2 + 2, x <= 1), (2*x + 1, True))
    assert I(x**2 + 2, (x, 0, 1)) == R(7, 3) and I(2*x + 1, (x, 1, 2)) == 4 and I(fp, (x, 0, 2)) == R(19, 3)
    # true / false
    g = x**2 - 4
    claims = (all(g.subs(x, R(k, 10)) <= 0 for k in range(21)), I(g, (x, 0, 3)) == -3,
              AI(g, 0, 3) == 3, AI(g, 0, 3) == R(23, 3))
    assert I(4 - x**2, (x, 0, 2)) == R(16, 3) and I(g, (x, 2, 3)) == R(7, 3)
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    l2 = sp.log(2)
    p1, p2 = I(2 - sp.exp(x), (x, 0, l2)), I(sp.exp(x) - 2, (x, l2, 2))
    assert sp.simplify(p1 - (2*l2 - 1)) == 0 and sp.simplify(p2 - (sp.E**2 - 6 + 2*l2)) == 0
    val = sp.E**2 - 7 + 4*l2
    assert abs(float(sp.Integral(A(sp.exp(x) - 2), (x, 0, 2)).evalf()) - float(val)) < 1e-4
    assert f'{float(val):.2f}' == '3.16'
    # exercises
    assert AI(x - 1, 0, 2) == 1 and AI(sp.sin(x), 0, 2*sp.pi) == 4 \
        and AI(x**2 - 1, 0, 3) == R(22, 3)
    assert [ans for _, ans in EXERCISES] == ['1', '4', '22/3']
    return True


validate()

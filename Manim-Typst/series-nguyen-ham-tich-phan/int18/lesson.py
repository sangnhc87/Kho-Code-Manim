"""INT18 – Tích phân hàm ẩn & tính đối xứng: chẵn – lẻ, f(a + b − x).

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT18',
    'number': 18,
    'title': 'Hàm ẩn & tính đối xứng',
    'subtitle': 'Phép đổi biến x → a + b − x',
    'next_code': 'INT19',
    'next_title': 'Hàm ẩn từ phương trình vi phân đơn giản',
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
         'Tính tích phân từ không đến pi phần hai của sin x chia cho sin x cộng cốt x. '
         'Tìm nguyên hàm khá vất vả. Nhưng có một cách chỉ mất ba dòng, dựa vào tính đối xứng, '
         'và đáp số là pi phần tư.',
         'Mở đầu: ba dòng thay cho một trang'),
    Beat('h2', 'hook',
         'Đây là tập mười tám của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'tích phân hàm ẩn và tính đối xứng.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, phép đổi biến x thành a cộng b trừ x và ý nghĩa gập đối xứng. '
         'Hai, kỹ thuật cộng hai tích phân để triệt tiêu phần khó. '
         'Ba, tính tích phân của hàm ẩn khi chỉ biết một hệ thức như f của x cộng f của trừ x.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Tính chất then chốt: tích phân từ a đến b của f của x bằng tích phân từ a đến b của f của a cộng b trừ x. '
         'Về hình học, đồ thị của f của a cộng b trừ x là đồ thị của f lật qua đường thẳng đứng ở giữa đoạn. '
         'Lật một miền thì diện tích không đổi.',
         'Gập đối xứng: x → a + b − x'),
    Beat('c2', 'core',
         'Chứng minh bằng đổi biến: đặt t bằng a cộng b trừ x, d t bằng trừ d x. Khi x bằng a thì t bằng b, '
         'khi x bằng b thì t bằng a. Dấu trừ của d t vừa đủ để đảo cận trở lại. '
         'Ta thu được đúng tích phân ban đầu.'),
    Beat('c3', 'core',
         'Áp dụng cho bài mở đầu, với a bằng không, b bằng pi phần hai. Sin của pi phần hai trừ x là cốt x, '
         'nên I cũng bằng tích phân của cốt x chia sin x cộng cốt x. Cộng hai cách viết của I, '
         'tử số cộng lại bằng mẫu số. Hai I bằng tích phân của một, bằng pi phần hai. Vậy I bằng pi phần tư.',
         'Cộng hai tích phân'),
    Beat('c3b', 'core',
         'Khi nào nên nghĩ đến phép gập? Ba dấu hiệu thường gặp. Một, biểu thức chứa sin và cốt trên đoạn từ không đến pi phần hai, '
         'vì phép gập đổi sin thành cốt. Hai, x nhân một hàm của sin x trên đoạn từ không đến pi. '
         'Ba, đoạn đối xứng từ trừ a đến a, hoặc đề cho hệ thức giữa f của x và f của a cộng b trừ x.',
         'Dấu hiệu dùng phép gập'),
    Beat('c4', 'core',
         'Với đoạn đối xứng từ trừ a đến a, phép gập là x thành trừ x. Từ đó suy ra quen thuộc: hàm lẻ có tích phân bằng không, '
         'hàm chẵn có tích phân bằng hai lần nửa đoạn. Nhưng điều quan trọng hơn: tích phân của f của x '
         'luôn bằng tích phân của f của trừ x trên đoạn đối xứng.',
         'Hàm ẩn trên đoạn đối xứng'),
    Beat('c5', 'core',
         'Vì vậy, khi đề chỉ cho hệ thức f của x cộng f của trừ x bằng g của x, ta lấy tích phân hai vế từ trừ a đến a. '
         'Vế trái thành hai lần tích phân của f. Suy ra tích phân của f bằng một nửa tích phân của g. '
         'Không cần biết f là hàm gì!'),
    Beat('c6', 'core',
         'Tổng quát hơn, nếu f của x cộng f của a cộng b trừ x bằng g của x trên đoạn từ a đến b, '
         'thì tích phân của f trên đoạn đó bằng một nửa tích phân của g. Đây là chìa khóa cho rất nhiều câu vận dụng cao.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: hàm f liên tục thỏa f của x cộng f của trừ x bằng cốt x. Tính tích phân từ trừ pi phần hai đến pi phần hai của f. '
         'Theo hệ quả trên, tích phân bằng một nửa tích phân của cốt x trên đoạn đó, bằng một nửa nhân hai, bằng một.',
         'Ví dụ 1: biết f(x) + f(−x)'),
    Beat('e2', 'examples',
         'Ví dụ hai: tích phân từ không đến pi của x sin x. Gập đối xứng: I bằng tích phân của pi trừ x, nhân sin x, '
         'vì sin của pi trừ x vẫn là sin x. Cộng lại, hai I bằng pi nhân tích phân của sin x, bằng hai pi. '
         'Vậy I bằng pi, không cần từng phần.',
         'Ví dụ 2: khử x bằng đối xứng'),
    Beat('e2b', 'examples',
         'Tổng quát từ ví dụ hai: tích phân từ không đến pi của x nhân f của sin x bằng pi phần hai nhân tích phân của f của sin x. '
         'Chẳng hạn, tích phân của x sin x chia một cộng cốt bình phương x bằng pi phần hai nhân pi phần hai, '
         'bằng pi bình phương phần tư. Phần chứa x đã biến mất.'),
    Beat('e3', 'examples',
         'Ví dụ ba: biết tích phân từ một đến ba của f bằng sáu. Tính tích phân từ không đến một của f của hai x cộng một. '
         'Đặt t bằng hai x cộng một, d t bằng hai d x, cận mới từ một đến ba. Kết quả bằng một nửa nhân sáu, bằng ba.',
         'Ví dụ 3: hàm ẩn qua đổi biến'),
    Beat('e4', 'examples',
         'Ví dụ bốn: f liên tục thỏa f của x cộng hai f của một trừ x bằng ba x bình phương. Tính tích phân từ không đến một của f. '
         'Gọi I là tích phân cần tìm. Theo tính chất gập, tích phân của f của một trừ x cũng bằng I. '
         'Lấy tích phân hai vế: I cộng hai I bằng một. Vậy I bằng một phần ba.',
         'Ví dụ 4: hệ thức hai ẩn'),
    Beat('e5', 'examples',
         'Ví dụ năm, một bài kinh điển: tích phân từ không đến pi phần tư của l n của một cộng tan x. '
         'Gập đối xứng: một cộng tan của pi phần tư trừ x bằng hai chia một cộng tan x. '
         'Nên I cũng bằng tích phân của l n hai trừ l n của một cộng tan x. Cộng lại, hai I bằng pi phần tư nhân l n hai. '
         'Vậy I bằng pi phần tám nhân l n hai.',
         'Ví dụ 5: ln(1 + tan x)'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f liên tục trên R thỏa f của x cộng f của trừ x bằng hai x bình phương cộng hai. '
         'Gọi I là tích phân từ trừ một đến một của f. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: đây là tính chất gập trên đoạn đối xứng. '
         'Ý b đúng: lấy tích phân hai vế của hệ thức, vế trái bằng hai I.'),
    Beat('x3', 'exam',
         'Ý c đúng: tích phân của hai x bình phương cộng hai từ trừ một đến một bằng mười sáu phần ba, nên I bằng tám phần ba. '
         'Ý d sai: f bằng x bình phương cộng một cộng x cũng thỏa hệ thức nhưng không phải hàm chẵn. '
         'Hệ thức chỉ xác định phần chẵn của f.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: tính tích phân từ không đến pi phần hai của sin lập phương x chia cho sin lập phương cộng cốt lập phương, '
         'làm tròn đến hàng phần trăm. Gập đối xứng đổi sin thành cốt và ngược lại.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Cộng hai cách viết, tử bằng mẫu, nên hai I bằng pi phần hai, I bằng pi phần tư, xấp xỉ không phẩy bảy chín. '
         'Ghi vào phiếu: không, phẩy, bảy, chín. Số mũ ba không làm thay đổi gì cả: mọi số mũ đều cho pi phần tư.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, tích phân không đổi khi thay x bằng a cộng b trừ x. '
         'Hai, cộng hai cách viết để tử số khớp với mẫu số, hoặc để khử biến x. '
         'Ba, với hàm ẩn, lấy tích phân hai vế của hệ thức rồi giải phương trình theo I.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tích phân từ không đến pi phần hai của cốt mũ năm chia sin mũ năm cộng cốt mũ năm. '
         'Hai, f của x cộng f của trừ x bằng ba x bình phương, tính tích phân từ trừ một đến một của f. '
         'Ba, biết tích phân từ một đến năm của f bằng mười, tính tích phân từ không đến hai của f của hai x cộng một. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập mười chín, ta gặp một kiểu hàm ẩn khác: biết đạo hàm của f liên hệ với chính f, '
         'như f phẩy bằng x nhân f. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "integral_0^(pi\\/2) (sin x)/(sin x + cos x) dif x = gold(pi/4)",
    'flip': "integral_a^b f(x) dif x = integral_a^b f(a + b - x) dif x",
    'proof1': "t = a + b - x, quad dif t = -dif x, quad x: a arrow.r b arrow.double.long t: b arrow.r a",
    'proof2': "integral_a^b f(a + b - x) dif x = integral_b^a f(t) (-dif t) = integral_a^b f(t) dif t",
    'c3_s1': "I = integral_0^(pi\\/2) (cos x)/(cos x + sin x) dif x",
    'c3_s2': "2I = integral_0^(pi\\/2) (sin x + cos x)/(sin x + cos x) dif x = pi/2 arrow.double.long I = gold(pi/4)",
    'sym': "integral_(-a)^a f(x) dif x = integral_(-a)^a f(-x) dif x",
    'hid1': "f(x) + f(-x) = g(x) arrow.double.long integral_(-a)^a f(x) dif x = 1/2 integral_(-a)^a g(x) dif x",
    'hid2': "f(x) + f(a + b - x) = g(x) arrow.double.long integral_a^b f = 1/2 integral_a^b g",
    'e1_task': "f(x) + f(-x) = cos x",
    'e1_s1': "integral_(-pi\\/2)^(pi\\/2) f(x) dif x = 1/2 integral_(-pi\\/2)^(pi\\/2) cos x dif x = 1/2 dot 2 = gold(1)",
    'e2_task': "I = integral_0^pi x sin x dif x",
    'e2_s1': "I = integral_0^pi (pi - x) sin x dif x",
    'e2_s2': "2I = pi integral_0^pi sin x dif x = 2pi arrow.double.long I = gold(pi)",
    'signs1': "integral_0^(pi\\/2) R(sin x, cos x) dif x",
    'signs2': "integral_0^pi x f(sin x) dif x",
    'signs3': "integral_(-a)^a, quad f(x) + f(a + b - x) = g(x)",
    'xsin': "integral_0^pi x f(sin x) dif x = pi/2 integral_0^pi f(sin x) dif x",
    'xsin_ex': "integral_0^pi (x sin x)/(1 + cos^2 x) dif x = pi/2 dot pi/2 = gold(pi^2/4)",
    'e5_task': "I = integral_0^(pi\\/4) ln(1 + tan x) dif x",
    'e5_s1': "1 + tan(pi/4 - x) = 2/(1 + tan x) arrow.double.long I = integral_0^(pi\\/4) [ln 2 - ln(1 + tan x)] dif x",
    'e5_s2': "2I = pi/4 ln 2 arrow.double.long I = gold(pi/8 ln 2)",
    'e3_task': "integral_1^3 f(x) dif x = 6 arrow.double.long integral_0^1 f(2x + 1) dif x = ?",
    'e3_s1': "t = 2x + 1: quad integral_0^1 f(2x + 1) dif x = 1/2 integral_1^3 f(t) dif t = gold(3)",
    'e4_task': "f(x) + 2 f(1 - x) = 3x^2",
    'e4_s1': "integral_0^1 f(1 - x) dif x = integral_0^1 f(x) dif x = I",
    'e4_s2': "I + 2I = integral_0^1 3x^2 dif x = 1 arrow.double.long I = gold(1/3)",
    'tf_given': "f(x) + f(-x) = 2x^2 + 2, quad I = integral_(-1)^1 f(x) dif x",
    'tf_a': "integral_(-1)^1 f(-x) dif x = I",
    'tf_b': "2I = integral_(-1)^1 (2x^2 + 2) dif x",
    'tf_c': "I = 8/3",
    'tf_d': "f(-x) = f(x) quad forall x in RR",
    'tf_c_calc': "2I = 4/3 + 4 = 16/3 arrow.double.long I = 8/3",
    'tf_d_calc': "f(x) = x^2 + 1 + x: quad f(x) + f(-x) = 2x^2 + 2",
    'sa_task': "integral_0^(pi\\/2) (sin^3 x)/(sin^3 x + cos^3 x) dif x approx ?",
    'sa_s1': "I = integral_0^(pi\\/2) (cos^3 x)/(cos^3 x + sin^3 x) dif x",
    'sa_s2': "2I = pi/2 arrow.double.long I = pi/4 approx gold(\"0,79\")",
    'sum1': "integral_a^b f(x) = integral_a^b f(a + b - x)",
    'sum2': "I + I = integral_a^b 1 dif x",
    'sum3': "f(x) + f(-x) = g arrow.double.long integral f = 1/2 integral g",
    'hw1': "integral_0^(pi\\/2) (cos^5 x)/(sin^5 x + cos^5 x) dif x",
    'hw2': "f(x) + f(-x) = 3x^2, quad integral_(-1)^1 f(x) dif x",
    'hw3': "integral_1^5 f = 10, quad integral_0^2 f(2x + 1) dif x",
    'hw_ans1': "pi/4",
    'hw_ans2': "1",
    'hw_ans3': "5",
    'next1': "f'(x) = x f(x), quad f(0) = 1",
    'next2': "(f'(x))/(f(x)) = x arrow.double.long ln f(x) = x^2/2",
}

EXERCISES = (
    ('∫₀^(π/2) cos⁵x/(sin⁵x + cos⁵x) dx', 'π/4'),
    ('f(x) + f(−x) = 3x²: ∫₋₁¹ f(x) dx', '1'),
    ('∫₁⁵ f = 10: ∫₀² f(2x + 1) dx', '5'),
)

TRUE_FALSE = (
    ('∫₋₁¹ f(−x) dx = I', True),
    ('2I = ∫₋₁¹ (2x² + 2) dx', True),
    ('I = 8/3', True),
    ('f(−x) = f(x) với mọi x', False),
)

x, t = sp.symbols('x t', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, pi = sp.integrate, sp.Rational, sp.pi
    s, c = sp.sin(x), sp.cos(x)
    # hook (numeric check: SymPy's closed form is messy)
    hook = sp.Integral(s / (s + c), (x, 0, pi / 2)).evalf()
    assert abs(hook - float(pi / 4)) < 1e-10
    assert sp.simplify(s.subs(x, pi / 2 - x) - c) == 0
    # flip property on a concrete non-symmetric function
    f = sp.exp(x) * x
    assert sp.simplify(I(f, (x, 0, 2)) - I(f.subs(x, 2 - x), (x, 0, 2))) == 0
    # e1: any f with f(x) + f(-x) = cos x, e.g. f = cos(x)/2 + x^3
    fe = c / 2 + x**3
    assert sp.simplify(fe + fe.subs(x, -x) - c) == 0 and I(fe, (x, -pi / 2, pi / 2)) == 1
    # e2
    assert I(x * s, (x, 0, pi)) == pi and I((pi - x) * s, (x, 0, pi)) == pi and pi * I(s, (x, 0, pi)) == 2 * pi
    v1 = sp.Integral(x * s / (1 + c**2), (x, 0, pi)).evalf()
    assert abs(v1 - float(pi**2 / 4)) < 1e-10 and sp.integrate(s / (1 + c**2), (x, 0, pi)) == pi / 2
    tq = sp.tan(pi / 4 - x)
    assert sp.simplify(1 + sp.expand_trig(tq) - 2 / (1 + sp.tan(x))) == 0
    v5 = sp.Integral(sp.log(1 + sp.tan(x)), (x, 0, pi / 4)).evalf()
    assert abs(v5 - float(pi / 8 * sp.log(2))) < 1e-10
    # e3: concrete f with ∫1..3 f = 6 (f = 3)
    assert I(3, (x, 1, 3)) == 6 and I(3, (x, 0, 1)) == 3
    f3 = 3 * (x - 1) ** 2 * R(3, 4)  # another witness: ∫1..3 f = 6
    assert I(f3, (x, 1, 3)) == 6 and I(f3.subs(x, 2 * x + 1), (x, 0, 1)) == 3
    # e4: solve the functional equation exactly: f(x) + 2 f(1−x) = 3x²
    a0, a1, a2 = sp.symbols('a0 a1 a2')
    fp = a0 + a1 * x + a2 * x**2
    sol = sp.solve(sp.Poly(sp.expand(fp + 2 * fp.subs(x, 1 - x) - 3 * x**2), x).coeffs(), (a0, a1, a2))
    f4 = fp.subs(sol)
    assert I(f4, (x, 0, 1)) == R(1, 3)
    # true / false: witness f = x^2 + 1 + x
    g = 2 * x**2 + 2
    fw = x**2 + 1 + x
    assert sp.simplify(fw + fw.subs(x, -x) - g) == 0
    Iv = I(fw, (x, -1, 1))
    claims = (I(fw.subs(x, -x), (x, -1, 1)) == Iv, 2 * Iv == I(g, (x, -1, 1)), Iv == R(8, 3),
              sp.simplify(fw - fw.subs(x, -x)) == 0)
    assert I(g, (x, -1, 1)) == R(16, 3)
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer and exercise 1 (numeric)
    for n in (3, 5):
        val = sp.Integral(s**n / (s**n + c**n), (x, 0, pi / 2)).evalf()
        assert abs(val - float(pi / 4)) < 1e-10
    assert f'{float(pi / 4):.2f}' == '0.79'
    # exercises 2, 3
    fh = R(3, 2) * x**2 + x**5
    assert sp.simplify(fh + fh.subs(x, -x) - 3 * x**2) == 0 and I(fh, (x, -1, 1)) == 1
    assert I(R(5, 2), (x, 1, 5)) == 10 and I(R(5, 2), (x, 0, 2)) == 5
    # next teaser
    assert sp.dsolve(sp.Eq(sp.Function('y')(x).diff(x), x * sp.Function('y')(x)), ics={sp.Function('y')(0): 1}).rhs \
        == sp.exp(x**2 / 2)
    return True


validate()

"""INT19 – Hàm ẩn từ phương trình vi phân đơn giản: f'(x) = g(x)·h(f(x)).

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT19',
    'number': 19,
    'title': 'Hàm ẩn từ phương trình vi phân',
    'subtitle': "Dạng f'(x) = g(x)·h(f(x))",
    'next_code': 'INT20',
    'next_title': 'Tổng ôn tích phân theo 3 dạng câu hỏi',
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
         'Hàm số f dương, có f phẩy của x bằng x nhân f của x, và f của không bằng một. Tính f của hai. '
         'Đề không cho công thức của f, chỉ cho một hệ thức giữa đạo hàm và chính hàm số. '
         'Vậy mà ta tìm được chính xác: f của hai bằng e bình phương.',
         'Mở đầu: biết đạo hàm liên hệ với chính f'),
    Beat('h2', 'hook',
         'Đây là tập mười chín của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'hàm ẩn từ phương trình vi phân đơn giản.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, ý nghĩa hình học: trường hướng và đường cong đi qua một điểm. '
         'Hai, kỹ thuật tách biến: đưa mọi thứ chứa f về một vế. '
         'Ba, bốn dạng đạo hàm quen thuộc cần nhận ra ngay: l n f, một chia f, f bình phương và đạo hàm của tích.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Hệ thức f phẩy bằng x nhân f cho biết độ dốc của đồ thị tại mọi điểm. Vẽ một đoạn ngắn có độ dốc đó tại mỗi điểm, '
         'ta được trường hướng. Có vô số đường cong đi theo trường hướng này, '
         'nhưng chỉ có một đường đi qua điểm không, một. Điều kiện ban đầu chọn ra đúng một hàm.',
         'Trường hướng và điều kiện ban đầu'),
    Beat('c2', 'core',
         'Kỹ thuật tách biến. Với f phẩy bằng g của x nhân h của f, chia hai vế cho h của f, '
         'ta được f phẩy chia h của f bằng g của x. Vế trái chỉ chứa f, vế phải chỉ chứa x. '
         'Lấy tích phân hai vế từ a đến b là xong.',
         'Tách biến'),
    Beat('c3', 'core',
         'Vế trái thực chất là một phép đổi biến u bằng f của x, d u bằng f phẩy d x. '
         'Tích phân từ a đến b của f phẩy chia h của f, bằng tích phân từ f của a đến f của b của d u chia h của u. '
         'Đây chính là bài học đổi biến của tập mười sáu.'),
    Beat('c4', 'core',
         'Dạng một, hay gặp nhất: f phẩy bằng g nhân f, với f dương. Khi đó f phẩy chia f chính là đạo hàm của l n f. '
         'Lấy tích phân: l n f của b trừ l n f của a bằng tích phân của g.',
         'Bốn dạng cần nhận ra'),
    Beat('c5', 'core',
         'Dạng hai: f phẩy bằng g nhân f bình phương. Chia cho f bình phương, vế trái là đạo hàm của trừ một chia f. '
         'Suy ra một chia f của a trừ một chia f của b bằng tích phân của g. Chú ý thứ tự trừ để khỏi sai dấu.'),
    Beat('c6', 'core',
         'Dạng ba: f nhân f phẩy bằng g. Vế trái là đạo hàm của f bình phương chia hai. '
         'Dạng bốn: x nhân f phẩy cộng f bằng g. Vế trái là đạo hàm của tích x nhân f. '
         'Nhận ra vế trái là đạo hàm của cái gì, đó là toàn bộ bí quyết.'),
    Beat('c7', 'core',
         'Một chi tiết hay bị bỏ qua: muốn chia cho f hay lấy l n f, cần f khác không hoặc f dương. '
         'Đề thi luôn cho điều kiện này, ví dụ f dương trên đoạn đang xét. Hãy đọc kỹ và dùng nó khi biến đổi.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. f phẩy chia f bằng x. Lấy tích phân từ không đến hai: '
         'l n f của hai trừ l n f của không bằng tích phân của x, bằng hai. Vì f của không bằng một, l n một bằng không, '
         'nên l n f của hai bằng hai, f của hai bằng e bình phương.',
         'Ví dụ 1: dạng ln f'),
    Beat('e2', 'examples',
         'Ví dụ hai: f phẩy bằng hai x nhân f bình phương, f của không bằng trừ một. Tính f của một. '
         'Đạo hàm của trừ một chia f bằng hai x, nên trừ một chia f bằng x bình phương cộng C. '
         'Thay x bằng không: C bằng một. Vậy f bằng trừ một chia x bình phương cộng một, f của một bằng trừ một phần hai.',
         'Ví dụ 2: dạng 1/f'),
    Beat('e3', 'examples',
         'Ví dụ ba: f dương, f nhân f phẩy bằng x, f của không bằng một. Tính f của căn ba. '
         'Đạo hàm của f bình phương chia hai bằng x, nên f bình phương bằng x bình phương cộng C. '
         'Với f của không bằng một thì C bằng một. Vậy f của căn ba bằng căn bốn, bằng hai.',
         'Ví dụ 3: dạng f²'),
    Beat('e4', 'examples',
         'Ví dụ bốn: x nhân f phẩy cộng f bằng ba x bình phương, f của một bằng hai. Tính f của hai. '
         'Vế trái là đạo hàm của x nhân f. Lấy nguyên hàm: x nhân f bằng x lập phương cộng C. '
         'Tại x bằng một: hai bằng một cộng C, C bằng một. Vậy f của hai bằng tám cộng một, chia hai, bằng chín phần hai.',
         'Ví dụ 4: đạo hàm của tích'),
    Beat('e5', 'examples',
         'Khi đã tìm được f, đề có thể hỏi tiếp tích phân. Ở ví dụ bốn, f bằng x bình phương cộng một chia x. '
         'Tích phân từ một đến hai của f bằng bảy phần ba cộng l n hai. Câu hỏi nhiều bước như vậy rất phổ biến '
         'trong phần trả lời ngắn.'),
    Beat('e6', 'examples',
         'Mẹo kiểm tra: sau khi tìm được f, hãy thay ngược lại vào hệ thức đề cho và kiểm tra điều kiện ban đầu. '
         'Ví dụ f bằng e mũ x bình phương phần hai: đạo hàm là x nhân e mũ x bình phương phần hai, đúng bằng x nhân f, '
         'và f của không bằng một. Chỉ mất mười giây mà tránh được sai sót.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Hàm số f dương, f phẩy của x bằng hai x cộng một, nhân f của x, và f của không bằng một. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: vì f dương nên đạo hàm của l n f bằng f phẩy chia f, bằng hai x cộng một. '
         'Ý b đúng: l n f bằng x bình phương cộng x cộng C, và C bằng không vì f của không bằng một.'),
    Beat('x3', 'exam',
         'Ý c sai: f của một bằng e mũ hai, không phải e. Ý d đúng: tích phân từ không đến một của f phẩy chia f '
         'bằng l n f của một trừ l n f của không, bằng hai.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: hàm số f thỏa f phẩy bằng x nhân f bình phương và f của không bằng một phần hai. '
         'Tính f của một, làm tròn đến hàng phần trăm. Đây là dạng hai: đạo hàm của trừ một chia f bằng x.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Trừ một chia f bằng x bình phương phần hai cộng C. Thay x bằng không: trừ hai bằng C. '
         'Vậy f bằng hai chia bốn trừ x bình phương, f của một bằng hai phần ba, xấp xỉ không phẩy sáu bảy. '
         'Ghi vào phiếu: không, phẩy, sáu, bảy.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, hệ thức giữa f phẩy và f cho một trường hướng, điều kiện ban đầu chọn ra một hàm duy nhất. '
         'Hai, tách biến: f phẩy chia h của f bằng g của x, rồi lấy tích phân hai vế. '
         'Ba, nhận ra vế trái là đạo hàm của l n f, của trừ một chia f, của f bình phương phần hai, hay của x nhân f.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, f dương, f phẩy bằng ba x bình phương nhân f, f của không bằng hai, tính f của một. '
         'Hai, f dương, f nhân f phẩy bằng hai x, f của không bằng ba, tính f của hai. '
         'Ba, x nhân f phẩy cộng f bằng hai x, f của một bằng ba, tính f của hai. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Tập hai mươi là tập tổng ôn phần tích phân, với một mini đề gồm đủ ba dạng câu hỏi: trắc nghiệm, đúng sai '
         'và trả lời ngắn. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "f > 0, quad f'(x) = x f(x), quad f(0) = 1 arrow.double.long f(2) = gold(?)",
    'hook_ans': "f(2) = gold(e^2)",
    'field': "f'(x) = x f(x)",
    'sep1': "f'(x) = g(x) dot h(f(x))",
    'sep2': "(f'(x))/(h(f(x))) = g(x) arrow.double.long integral_a^b (f'(x))/(h(f(x))) dif x = integral_a^b g(x) dif x",
    'sub': "u = f(x): quad integral_a^b (f'(x))/(h(f(x))) dif x = integral_(f(a))^(f(b)) (dif u)/(h(u))",
    'type1': "f' = g f arrow.double.long (ln f)' = g arrow.double.long ln f(b) - ln f(a) = integral_a^b g",
    'type2': "f' = g f^2 arrow.double.long (-1/f)' = g arrow.double.long 1/(f(a)) - 1/(f(b)) = integral_a^b g",
    'type3': "f f' = g arrow.double.long (f^2/2)' = g",
    'type4': "x f' + f = g arrow.double.long (x f)' = g",
    'e1_s1': "ln f(2) - ln f(0) = integral_0^2 x dif x = 2",
    'e1_s2': "ln f(2) = 2 arrow.double.long f(2) = gold(e^2)",
    'e2_task': "f'(x) = 2x f^2(x), quad f(0) = -1, quad f(1) = ?",
    'e2_s1': "(-1/f)' = 2x arrow.double.long -1/f = x^2 + C, quad C = 1",
    'e2_s2': "f(x) = -1/(x^2 + 1) arrow.double.long f(1) = gold(-1/2)",
    'e3_task': "f > 0, quad f f' = x, quad f(0) = 1, quad f(sqrt(3)) = ?",
    'e3_s1': "(f^2/2)' = x arrow.double.long f^2 = x^2 + C, quad C = 1",
    'e3_s2': "f(sqrt(3)) = sqrt(3 + 1) = gold(2)",
    'e4_task': "x f'(x) + f(x) = 3x^2, quad f(1) = 2, quad f(2) = ?",
    'e4_s1': "(x f)' = 3x^2 arrow.double.long x f(x) = x^3 + C, quad C = 1",
    'e4_s2': "f(x) = (x^3 + 1)/x arrow.double.long f(2) = gold(9/2)",
    'e5_s1': "integral_1^2 (x^2 + 1/x) dif x = 7/3 + ln 2",
    'check': "f = e^(x^2\\/2): quad f' = x e^(x^2\\/2) = x f, quad f(0) = 1 quad green(checkmark)",
    'tf_given': "f > 0, quad f'(x) = (2x + 1) f(x), quad f(0) = 1",
    'tf_a': "(ln f(x))' = 2x + 1",
    'tf_b': "f(x) = e^(x^2 + x)",
    'tf_c': "f(1) = e",
    'tf_d': "integral_0^1 (f'(x))/(f(x)) dif x = 2",
    'tf_c_calc': "f(1) = e^(1 + 1) = e^2 coral(!= e)",
    'sa_task': "f'(x) = x f^2(x), quad f(0) = 1/2, quad f(1) approx ?",
    'sa_s1': "(-1/f)' = x arrow.double.long -1/f = x^2/2 + C, quad C = -2",
    'sa_s2': "f(x) = 2/(4 - x^2) arrow.double.long f(1) = 2/3 approx gold(\"0,67\")",
    'sum1': "f'/h(f) = g(x)",
    'sum2': "integral_a^b f'/h(f) = integral_a^b g",
    'sum3': "(ln f)', (-1/f)', (f^2/2)', (x f)'",
    'hw1': "f' = 3x^2 f, quad f(0) = 2, quad f(1) = ?",
    'hw2': "f f' = 2x, quad f(0) = 3, quad f(2) = ?",
    'hw3': "x f' + f = 2x, quad f(1) = 3, quad f(2) = ?",
    'hw_ans1': "2e",
    'hw_ans2': "sqrt(17)",
    'hw_ans3': "3",
    'next1': "integral_0^3 abs(x^2 - 3x + 2) dif x, quad integral_0^1 2x(x^2 + 1)^3 dif x, quad integral_0^1 x e^x dif x",
}

EXERCISES = (
    ("f' = 3x²f, f(0) = 2: f(1)?", '2e'),
    ("f·f' = 2x, f(0) = 3: f(2)?", '√17'),
    ("x f' + f = 2x, f(1) = 3: f(2)?", '3'),
)

TRUE_FALSE = (
    ("(ln f)' = 2x + 1", True),
    ('f(x) = e^(x² + x)', True),
    ('f(1) = e', False),
    ("∫₀¹ f'/f dx = 2", True),
)

x = sp.symbols('x', real=True)
F = sp.Function('f')


def solve(ode, x0, y0):
    return sp.dsolve(ode, F(x), ics={F(x0): y0}).rhs


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, E = sp.integrate, sp.Rational, sp.E
    fx, d = F(x), F(x).diff(x)
    # hook / e1 / check
    f1 = solve(sp.Eq(d, x * fx), 0, 1)
    assert sp.simplify(f1 - sp.exp(x**2 / 2)) == 0 and sp.simplify(f1.subs(x, 2) - E**2) == 0
    assert I(x, (x, 0, 2)) == 2
    assert sp.simplify(sp.diff(f1, x) - x * f1) == 0
    # e2
    f2 = -1 / (x**2 + 1)
    assert sp.simplify(sp.diff(f2, x) - 2 * x * f2**2) == 0 and f2.subs(x, 0) == -1 and f2.subs(x, 1) == -R(1, 2)
    assert sp.simplify(sp.diff(-1 / f2, x) - 2 * x) == 0
    # e3
    f3 = sp.sqrt(x**2 + 1)
    assert sp.simplify(f3 * sp.diff(f3, x) - x) == 0 and f3.subs(x, 0) == 1 and f3.subs(x, sp.sqrt(3)) == 2
    # e4 / e5
    f4 = (x**3 + 1) / x
    assert sp.simplify(x * sp.diff(f4, x) + f4 - 3 * x**2) == 0 and f4.subs(x, 1) == 2 and f4.subs(x, 2) == R(9, 2)
    assert sp.simplify(I(f4, (x, 1, 2)) - (R(7, 3) + sp.log(2))) == 0
    # true / false
    ft = solve(sp.Eq(d, (2 * x + 1) * fx), 0, 1)
    claims = (sp.simplify(sp.diff(sp.log(ft), x) - (2 * x + 1)) == 0, sp.simplify(ft - sp.exp(x**2 + x)) == 0,
              sp.simplify(ft.subs(x, 1) - E) == 0, sp.simplify(I(sp.diff(ft, x) / ft, (x, 0, 1)) - 2) == 0)
    assert sp.simplify(ft.subs(x, 1) - E**2) == 0
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    fs = 2 / (4 - x**2)
    assert sp.simplify(sp.diff(fs, x) - x * fs**2) == 0 and fs.subs(x, 0) == R(1, 2) and fs.subs(x, 1) == R(2, 3)
    assert f'{float(R(2, 3)):.2f}' == '0.67'
    # exercises
    h1 = 2 * sp.exp(x**3)
    assert sp.simplify(sp.diff(h1, x) - 3 * x**2 * h1) == 0 and h1.subs(x, 1) == 2 * E
    h2 = sp.sqrt(2 * x**2 + 9)
    assert sp.simplify(h2 * sp.diff(h2, x) - 2 * x) == 0 and h2.subs(x, 0) == 3 and h2.subs(x, 2) == sp.sqrt(17)
    h3 = (x**2 + 2) / x
    assert sp.simplify(x * sp.diff(h3, x) + h3 - 2 * x) == 0 and h3.subs(x, 1) == 3 and h3.subs(x, 2) == 3
    return True


validate()

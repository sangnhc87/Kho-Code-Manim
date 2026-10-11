"""INT21 – Diện tích hình phẳng giới hạn bởi đồ thị và trục Ox: S = ∫|f(x)| dx.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT21',
    'number': 21,
    'title': 'Diện tích hình phẳng với trục Ox',
    'subtitle': 'Diện tích luôn dương: xét dấu rồi tách cận',
    'next_code': 'INT22',
    'next_title': 'Diện tích giữa hai đường cong',
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
         'Tính diện tích hình phẳng giới hạn bởi đồ thị y bằng x bình phương trừ hai x, trục hoành, '
         'và hai đường thẳng x bằng không, x bằng ba. Nếu lấy tích phân từ không đến ba, ta được đúng bằng không! '
         'Nhưng trên hình rõ ràng có hai mảnh diện tích. Diện tích thật là tám phần ba.',
         'Mở đầu: tích phân bằng 0, diện tích khác 0'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi mốt, mở đầu phần C của series: ứng dụng hình học của tích phân. '
         'Chủ đề hôm nay: diện tích hình phẳng giới hạn bởi đồ thị và trục hoành.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, công thức S bằng tích phân của trị tuyệt đối f. '
         'Hai, cách xác định cận khi đề không cho sẵn hai đường thẳng đứng. '
         'Ba, các bẫy thường gặp, đặc biệt là quên trị tuyệt đối.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Cho hàm f liên tục trên đoạn từ a đến b. Hình phẳng giới hạn bởi đồ thị y bằng f của x, trục hoành, '
         'và hai đường thẳng x bằng a, x bằng b có diện tích S bằng tích phân từ a đến b của trị tuyệt đối f của x.',
         'Công thức diện tích'),
    Beat('c2', 'core',
         'Vì sao có trị tuyệt đối? Chia miền thành các dải hẹp. Mỗi dải có chiều cao là khoảng cách từ đồ thị đến trục, '
         'tức là trị tuyệt đối của f, luôn dương. Còn tích phân thường thì tính phần dưới trục là âm, '
         'nên các mảnh có thể triệt tiêu nhau như ở bài mở đầu.'),
    Beat('c3', 'core',
         'Ba trường hợp. Nếu f không âm trên đoạn, S bằng tích phân của f. Nếu f không dương, S bằng trừ tích phân của f. '
         'Nếu f đổi dấu, tách cận tại các nghiệm, như cách ta đã làm ở tập mười bốn.',
         'Ba trường hợp'),
    Beat('c4', 'core',
         'Khi đề chỉ nói hình phẳng giới hạn bởi đồ thị và trục hoành, không cho hai đường thẳng đứng, '
         'thì cận chính là các nghiệm của f bằng không. Ví dụ y bằng x bình phương trừ bốn x cộng ba cắt trục hoành tại một và ba, '
         'nên miền nằm trên đoạn từ một đến ba.',
         'Tìm cận khi đề không cho'),
    Beat('c5', 'core',
         'Mẹo tính nhanh: trên mỗi khoảng giữa hai nghiệm liên tiếp, f không đổi dấu, '
         'nên có thể đưa trị tuyệt đối ra ngoài tích phân của khoảng đó. Diện tích là tổng các trị tuyệt đối. '
         'Cách viết này rất tiện để bấm máy tính.'),
    Beat('c5b', 'core',
         'Với câu trắc nghiệm hay trả lời ngắn, có thể bấm máy tính trực tiếp: nhập tích phân của Abs của f, '
         'máy tự xử lý trị tuyệt đối. Nhưng với hàm có nhiều nghiệm, máy có thể chạy lâu hoặc kém chính xác, '
         'nên cách an toàn vẫn là tách cận tại các nghiệm rồi cộng các trị tuyệt đối.'),
    Beat('c6', 'core',
         'Hai bẫy hay gặp. Một, quên trị tuyệt đối, tính tích phân trên cả đoạn rồi ghi đáp số, có khi ra số âm. '
         'Diện tích không bao giờ âm. Hai, đưa trị tuyệt đối ra ngoài toàn bộ tích phân khi f đổi dấu, '
         'kết quả bị nhỏ hơn diện tích thật.',
         'Bẫy quên trị tuyệt đối'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. x bình phương trừ hai x bằng không tại x bằng không và x bằng hai. '
         'Trên đoạn từ không đến hai, f âm, tích phân bằng trừ bốn phần ba. Trên đoạn từ hai đến ba, f dương, tích phân bằng bốn phần ba. '
         'Diện tích bằng bốn phần ba cộng bốn phần ba, bằng tám phần ba.',
         'Ví dụ 1: bài mở đầu'),
    Beat('e2', 'examples',
         'Ví dụ hai: diện tích giới hạn bởi y bằng x bình phương trừ bốn x cộng ba và trục hoành. '
         'Cận là hai nghiệm một và ba. Trên đoạn này, f âm, tích phân bằng trừ bốn phần ba. '
         'Diện tích bằng bốn phần ba.',
         'Ví dụ 2: cận là nghiệm'),
    Beat('e3', 'examples',
         'Ví dụ ba: y bằng x lập phương trừ x và trục hoành. Ba nghiệm trừ một, không và một. '
         'Đồ thị đối xứng qua gốc tọa độ, hai mảnh có diện tích bằng nhau, mỗi mảnh bằng một phần tư. '
         'Tổng diện tích bằng một phần hai, trong khi tích phân từ trừ một đến một bằng không.',
         'Ví dụ 3: hàm bậc ba'),
    Beat('e4', 'examples',
         'Ví dụ bốn: y bằng l n x, trục hoành và đường thẳng x bằng e. Đề chỉ cho một đường thẳng đứng, '
         'cận còn lại là nghiệm của l n x bằng không, tức x bằng một. Diện tích bằng tích phân từ một đến e của l n x, '
         'bằng một, kết quả quen thuộc từ tập mười bảy.',
         'Ví dụ 4: thiếu một cận'),
    Beat('e5', 'examples',
         'Ví dụ năm, dạng đọc hình: đề cho đồ thị f cắt trục hoành tại c nằm giữa a và b, phần từ a đến c ở trên trục, '
         'phần từ c đến b ở dưới trục. Công thức đúng là S bằng tích phân từ a đến c của f, trừ tích phân từ c đến b của f. '
         'Hãy nhìn dấu trên hình để quyết định dấu trước mỗi tích phân.',
         'Ví dụ 5: đọc công thức từ hình'),
    Beat('e6', 'examples',
         'Ví dụ sáu, bài toán ngược rất hay gặp: đồ thị f cắt trục hoành tại c. Biết miền phía trên trục có diện tích ba, '
         'miền phía dưới có diện tích một. Tính tích phân từ a đến b của f. '
         'Phần trên mang dấu dương, phần dưới mang dấu âm, nên tích phân bằng ba trừ một, bằng hai, không phải bốn.',
         'Ví dụ 6: biết diện tích, tính tích phân'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Gọi D là hình phẳng giới hạn bởi đồ thị y bằng x bình phương trừ x trừ hai, '
         'trục hoành, x bằng không và x bằng ba. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: f bằng x cộng một nhân x trừ hai, âm trên khoảng từ không đến hai. '
         'Ý b sai: f đổi dấu tại hai nên không thể dùng tích phân của f trên cả đoạn.'),
    Beat('x3', 'exam',
         'Ý c đúng: tách tại hai và đổi dấu đoạn âm. Ý d sai: diện tích bằng mười phần ba cộng mười một phần sáu, '
         'bằng ba mươi mốt phần sáu, xấp xỉ năm phẩy mười bảy, lớn hơn năm.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: tính diện tích hình phẳng giới hạn bởi y bằng x bình phương trừ hai x trừ ba và trục hoành, '
         'làm tròn đến hàng phần mười. Cận là hai nghiệm trừ một và ba.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Trên đoạn từ trừ một đến ba, f âm. Tích phân bằng trừ ba mươi hai phần ba, nên diện tích bằng ba mươi hai phần ba, '
         'xấp xỉ mười phẩy sáu bảy, làm tròn được mười phẩy bảy. Ghi vào phiếu: một, không, phẩy, bảy.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, diện tích bằng tích phân của trị tuyệt đối f, không bao giờ âm. '
         'Hai, đề không cho cận thì cận là nghiệm của f bằng không. '
         'Ba, tách cận tại các nghiệm, trên mỗi khoảng có thể đưa trị tuyệt đối ra ngoài.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, diện tích giới hạn bởi y bằng x bình phương trừ một và trục hoành. '
         'Hai, y bằng x lập phương, trục hoành, x bằng trừ một và x bằng hai. '
         'Ba, y bằng cốt x, trục hoành, x bằng không và x bằng pi. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập hai mươi hai, ta tính diện tích giữa hai đường cong: tìm giao điểm, chia khoảng, '
         'và lấy đường trên trừ đường dưới. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "y = x^2 - 2x, quad y = 0, quad x = 0, quad x = 3",
    'hook_int': "integral_0^3 (x^2 - 2x) dif x = 0 quad coral(\"?!\")",
    'hook_s': "S = gold(8/3)",
    'area': "S = integral_a^b abs(f(x)) dif x",
    'case1': "f >= 0: quad S = integral_a^b f(x) dif x",
    'case2': "f <= 0: quad S = -integral_a^b f(x) dif x",
    'case3': "S = integral_a^c f dif x - integral_c^b f dif x",
    'roots': "x^2 - 4x + 3 = 0 arrow.double.long x = 1, x = 3",
    'split': "S = abs(integral_(x_1)^(x_2) f dif x) + abs(integral_(x_2)^(x_3) f dif x) + dots",
    'trap': "integral_0^3 (x^2 - 2x) dif x = 0 coral(!=) S",
    'e1_s1': "integral_0^2 (x^2 - 2x) dif x = -4/3, quad integral_2^3 (x^2 - 2x) dif x = 4/3",
    'e1_s2': "S = 4/3 + 4/3 = gold(8/3)",
    'e2_s1': "S = abs(integral_1^3 (x^2 - 4x + 3) dif x) = abs(-4/3) = gold(4/3)",
    'e3_task': "y = x^3 - x, quad y = 0",
    'e3_s1': "S = abs(integral_(-1)^0 (x^3 - x) dif x) + abs(integral_0^1 (x^3 - x) dif x) = 1/4 + 1/4 = gold(1/2)",
    'e4_task': "y = ln x, quad y = 0, quad x = e",
    'e4_s1': "ln x = 0 arrow.double.long x = 1: quad S = integral_1^e ln x dif x = gold(1)",
    'e5_s1': "S = integral_a^c f(x) dif x - integral_c^b f(x) dif x",
    'casio': "integral_a^b \"Abs\"(f(x)) dif x",
    'e6_s1': "integral_a^b f(x) dif x = S_1 - S_2 = 3 - 1 = gold(2)",
    'tf_given': "y = x^2 - x - 2, quad y = 0, quad x = 0, quad x = 3",
    'tf_a': "f(x) < 0 quad forall x in (0; 2)",
    'tf_b': "S = integral_0^3 f(x) dif x",
    'tf_c': "S = -integral_0^2 f(x) dif x + integral_2^3 f(x) dif x",
    'tf_d': "S < 5",
    'tf_b_calc': "integral_0^3 f(x) dif x = -3/2 < 0",
    'tf_d_calc': "S = 10/3 + 11/6 = 31/6 approx \"5,17\" > 5",
    'sa_task': "y = x^2 - 2x - 3, quad y = 0",
    'sa_s1': "x^2 - 2x - 3 = 0 arrow.double.long x = -1, x = 3",
    'sa_s2': "S = abs(integral_(-1)^3 (x^2 - 2x - 3) dif x) = 32/3 approx gold(\"10,7\")",
    'sum1': "S = integral_a^b abs(f(x)) dif x >= 0",
    'sum2': "f(x) = 0 arrow.double.long x_1, x_2, dots",
    'sum3': "S = sum abs(integral_(x_i)^(x_(i+1)) f)",
    'hw1': "y = x^2 - 1, quad y = 0",
    'hw2': "y = x^3, quad y = 0, quad x = -1, quad x = 2",
    'hw3': "y = cos x, quad y = 0, quad x = 0, quad x = pi",
    'hw_ans1': "4/3",
    'hw_ans2': "17/4",
    'hw_ans3': "2",
    'next1': "S = integral_a^b abs(f(x) - g(x)) dif x",
}

EXERCISES = (
    ('y = x² − 1 và trục Ox', '4/3'),
    ('y = x³, Ox, x = −1, x = 2', '17/4'),
    ('y = cos x, Ox, x = 0, x = π', '2'),
)

TRUE_FALSE = (
    ('f(x) < 0 với mọi x ∈ (0; 2)', True),
    ('S = ∫₀³ f(x) dx', False),
    ('S = −∫₀² f dx + ∫₂³ f dx', True),
    ('S < 5', False),
)

x = sp.symbols('x', real=True)


def area(expr, lo, hi):
    """Area between the graph and Ox on [lo, hi]: split at the roots, add |piece|."""
    cuts = sorted({sp.sympify(lo), sp.sympify(hi), *sp.solveset(expr, x, sp.Interval(lo, hi))}, key=float)
    return sp.nsimplify(sum(abs(sp.integrate(expr, (x, p, q))) for p, q in zip(cuts, cuts[1:])))


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, E, pi = sp.integrate, sp.Rational, sp.E, sp.pi
    f = x**2 - 2 * x
    assert I(f, (x, 0, 3)) == 0 and area(f, 0, 3) == R(8, 3)
    assert I(f, (x, 0, 2)) == -R(4, 3) and I(f, (x, 2, 3)) == R(4, 3)
    g = x**2 - 4 * x + 3
    assert sorted(sp.solve(g, x)) == [1, 3] and I(g, (x, 1, 3)) == -R(4, 3) and area(g, 1, 3) == R(4, 3)
    h = x**3 - x
    assert sorted(sp.solve(h, x)) == [-1, 0, 1] and area(h, -1, 1) == R(1, 2) and I(h, (x, -1, 1)) == 0
    assert I(h, (x, -1, 0)) == R(1, 4) and I(h, (x, 0, 1)) == -R(1, 4)
    assert sp.solve(sp.log(x), x) == [1] and sp.simplify(I(sp.log(x), (x, 1, E)) - 1) == 0
    # true / false
    t = x**2 - x - 2
    claims = (all(t.subs(x, R(k, 10)) < 0 for k in range(1, 20)), I(t, (x, 0, 3)) == area(t, 0, 3),
              -I(t, (x, 0, 2)) + I(t, (x, 2, 3)) == area(t, 0, 3), area(t, 0, 3) < 5)
    assert I(t, (x, 0, 3)) == -R(3, 2) and -I(t, (x, 0, 2)) == R(10, 3) and I(t, (x, 2, 3)) == R(11, 6)
    assert area(t, 0, 3) == R(31, 6) and f'{float(R(31, 6)):.2f}' == '5.17'
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    s = x**2 - 2 * x - 3
    assert sorted(sp.solve(s, x)) == [-1, 3] and I(s, (x, -1, 3)) == -R(32, 3) and area(s, -1, 3) == R(32, 3)
    assert f'{float(R(32, 3)):.1f}' == '10.7'
    # exercises
    assert area(x**2 - 1, -1, 1) == R(4, 3) and area(x**3, -1, 2) == R(17, 4) and area(sp.cos(x), 0, pi) == 2
    return True


validate()

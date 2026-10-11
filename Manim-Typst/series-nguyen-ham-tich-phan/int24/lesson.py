"""INT24 – Đọc diện tích từ đồ thị f': so sánh f(a), f(b), f(c).

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT24',
    'number': 24,
    'title': "Đọc diện tích từ đồ thị f'",
    'subtitle': 'So sánh f(a), f(b), f(c) không cần công thức',
    'next_code': 'INT25',
    'next_title': 'Thể tích vật thể theo thiết diện S(x)',
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
         'Đề chỉ cho đồ thị của đạo hàm f phẩy: từ không đến hai nằm trên trục với diện tích bốn, '
         'từ hai đến năm nằm dưới trục với diện tích bảy. Hãy sắp xếp f của không, f của hai và f của năm. '
         'Không có công thức nào của f, nhưng ta vẫn trả lời được chắc chắn.',
         "Mở đầu: chỉ có đồ thị f'"),
    Beat('h2', 'hook',
         'Đây là tập hai mươi bốn của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'đọc diện tích từ đồ thị của đạo hàm.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, diện tích dưới đồ thị f phẩy chính là độ biến thiên của f. '
         'Hai, cách so sánh các giá trị của f và tìm giá trị lớn nhất, nhỏ nhất. '
         'Ba, tính diện tích bằng hình học khi đồ thị f phẩy là đường thẳng hay đường tròn.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Chìa khóa là công thức Newton Leibniz đọc theo chiều ngược: f của b trừ f của a bằng tích phân từ a đến b của f phẩy. '
         'Nói bằng hình: diện tích có dấu dưới đồ thị f phẩy cho biết f đã tăng hay giảm bao nhiêu.',
         'Diện tích = độ biến thiên của f'),
    Beat('c2', 'core',
         'Trên đoạn mà f phẩy dương, đồ thị f phẩy nằm trên trục, f tăng đúng bằng diện tích phần đó. '
         'Trên đoạn mà f phẩy âm, f giảm đúng bằng diện tích phần nằm dưới trục. '
         'Ta có thể vẽ song song: mỗi mảnh diện tích là một bước đi lên hoặc đi xuống của f.'),
    Beat('c3', 'core',
         'Quy trình so sánh. Một, đọc dấu của f phẩy để lập bảng biến thiên của f. '
         'Hai, đọc diện tích các mảnh. Ba, viết mỗi giá trị cần so sánh theo một giá trị gốc, '
         'ví dụ f của hai bằng f của không cộng bốn, rồi so sánh các số cộng thêm.',
         'Quy trình so sánh'),
    Beat('c4', 'core',
         'Giá trị lớn nhất và nhỏ nhất. Cực đại xảy ra khi f phẩy đổi dấu từ dương sang âm, cực tiểu khi đổi từ âm sang dương. '
         'Nhưng giá trị lớn nhất trên đoạn còn phải so với hai đầu mút, và việc so sánh đó lại dựa vào diện tích.'),
    Beat('c5', 'core',
         'Khi đồ thị f phẩy là đoạn thẳng, parabol hay cung tròn, diện tích tính được bằng hình học: tam giác, hình thang, '
         'một phần tư hình tròn. Đề thi thường vẽ trên lưới ô vuông để ta đếm được diện tích.',
         'Tính diện tích bằng hình học'),
    Beat('c6', 'core',
         'Bẫy lớn nhất: nhầm đồ thị f phẩy với đồ thị f. Đồ thị f phẩy nằm trên trục nghĩa là f đang tăng, '
         'không phải f dương. Và điểm cao nhất của đồ thị f phẩy là nơi f tăng nhanh nhất, không phải cực đại của f.',
         'Bẫy: nhầm f với f′'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. f của hai bằng f của không cộng bốn. f của năm bằng f của hai trừ bảy, '
         'tức f của không trừ ba. So sánh ba số cộng thêm: không, cộng bốn, trừ ba. '
         'Vậy f của năm nhỏ hơn f của không, nhỏ hơn f của hai. Giá trị lớn nhất trên đoạn là f của hai.',
         'Ví dụ 1: bài mở đầu'),
    Beat('e2', 'examples',
         'Ví dụ hai: f phẩy bằng x trừ một trên đoạn từ không đến ba, đồ thị là một đường thẳng. '
         'Từ không đến một là tam giác dưới trục, diện tích một phần hai. Từ một đến ba là tam giác trên trục, diện tích hai. '
         'Vậy f nhỏ nhất tại một, và f của ba lớn hơn f của không là ba phần hai.',
         'Ví dụ 2: đồ thị là đường thẳng'),
    Beat('e3', 'examples',
         'Ví dụ ba: f của không bằng hai, đồ thị f phẩy trên đoạn từ không đến hai là một phần tư đường tròn bán kính hai. '
         'Diện tích bằng một phần tư nhân pi nhân bốn, bằng pi. Vậy f của hai bằng hai cộng pi, '
         'tính được mà không cần biết công thức của f phẩy.',
         'Ví dụ 3: cung tròn'),
    Beat('e4', 'examples',
         'Ví dụ bốn: f phẩy bằng x bình phương trừ hai x trên đoạn từ trừ một đến ba. Ba mảnh diện tích đều bằng bốn phần ba: '
         'trên, dưới, rồi trên. Vì vậy f của hai bằng f của trừ một, và f của ba bằng f của không. '
         'Giá trị lớn nhất đạt tại cả không và ba, giá trị nhỏ nhất đạt tại cả trừ một và hai.',
         'Ví dụ 4: các mảnh bằng nhau'),
    Beat('e5', 'examples',
         'Mẹo trình bày: vẽ một trục số dọc cho các giá trị của f, đặt f của điểm đầu tại số không, '
         'rồi đi lên hoặc đi xuống theo từng mảnh diện tích. Thứ tự trên trục dọc chính là đáp án so sánh.'),
    Beat('e6', 'examples',
         'Ví dụ năm, đếm nghiệm: với đồ thị f phẩy ở bài mở đầu và f của không bằng một. '
         'Trên đoạn từ không đến hai, f tăng từ một lên năm, nên không có nghiệm. Từ hai đến năm, f giảm từ năm xuống trừ hai, '
         'đi qua giá trị không đúng một lần. Vậy phương trình f bằng không có đúng một nghiệm trên đoạn từ không đến năm.',
         'Ví dụ 5: đếm nghiệm'),
    Beat('e7', 'examples',
         'Ví dụ sáu, vận dụng cao: xét g bằng f trừ x, thì g phẩy bằng f phẩy trừ một. '
         'Diện tích cần đọc bây giờ nằm giữa đồ thị f phẩy và đường thẳng y bằng một. Chẳng hạn f phẩy bằng x bình phương '
         'trên đoạn từ không đến hai: g của hai trừ g của không bằng tám phần ba trừ hai, bằng hai phần ba, nên g của hai lớn hơn.',
         'Ví dụ 6: hàm g = f − x'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Đồ thị f phẩy trên đoạn từ không đến sáu gồm ba mảnh: từ không đến một nằm trên trục, diện tích ba; '
         'từ một đến bốn nằm dưới trục, diện tích năm; từ bốn đến sáu nằm trên trục, diện tích bốn. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: f phẩy dương trên khoảng từ không đến một. '
         'Ý b đúng: f của bốn bằng f của một trừ năm, nhỏ hơn f của một.'),
    Beat('x3', 'exam',
         'Ý c sai: f của sáu bằng f của không cộng ba trừ năm cộng bốn, bằng f của không cộng hai, lớn hơn f của không. '
         'Ý d sai: f của một bằng f của không cộng ba, lớn hơn f của sáu, nên giá trị lớn nhất là f của một.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: biết f của một bằng năm, đồ thị f phẩy là đường thẳng đi qua hai điểm một, không và ba, bốn. '
         'Tính f của bốn. Đường thẳng có phương trình f phẩy bằng hai nhân x trừ một.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Từ một đến bốn, đồ thị f phẩy là tam giác trên trục với đáy ba và chiều cao sáu, diện tích chín. '
         'Vậy f của bốn bằng năm cộng chín, bằng mười bốn. Ghi vào phiếu: một, bốn.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, f của b trừ f của a bằng diện tích có dấu dưới đồ thị f phẩy. '
         'Hai, so sánh bằng cách quy mọi giá trị về một giá trị gốc rồi cộng trừ diện tích. '
         'Ba, đừng nhầm đồ thị f phẩy với đồ thị f.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, f phẩy bằng x trừ hai trên đoạn từ không đến bốn, so sánh f của không và f của bốn. '
         'Hai, f của không bằng một và f phẩy bằng hai x, tính f của ba. Ba, f phẩy bằng cốt x, tìm điểm mà f lớn nhất '
         'trên đoạn từ không đến hai pi. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Tập hai mươi lăm bước sang không gian ba chiều: tính thể tích vật thể bằng cách cắt lát và cộng dồn diện tích thiết diện. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "S_1 = 4 thin (0 arrow.r 2), quad S_2 = 7 thin (2 arrow.r 5)",
    'hook_q': "f(0), quad f(2), quad f(5): quad ?",
    'nl': "f(b) - f(a) = integral_a^b f'(x) dif x",
    'up': "f' > 0: quad f(b) = f(a) + S",
    'down': "f' < 0: quad f(b) = f(a) - S",
    'root': "f(2) = f(0) + 4, quad f(5) = f(0) - 3",
    'e1_s1': "f(5) < f(0) < f(2), quad max_([0; 5]) f = gold(f(2))",
    'e2_task': "f'(x) = x - 1, quad x in [0; 3]",
    'e2_s1': "f(1) = f(0) - 1/2, quad f(3) = f(1) + 2 = f(0) + 3/2",
    'e2_s2': "min f = gold(f(1)), quad max f = gold(f(3))",
    'e3_task': "f(0) = 2, quad f'(x) = sqrt(4 - x^2)",
    'e3_s1': "f(2) = f(0) + 1/4 dot pi dot 2^2 = gold(2 + pi)",
    'e4_task': "f'(x) = x^2 - 2x, quad x in [-1; 3]",
    'e4_s1': "f(0) = f(-1) + 4/3, quad f(2) = f(0) - 4/3, quad f(3) = f(2) + 4/3",
    'e4_s2': "max f = f(0) = f(3), quad min f = f(-1) = f(2)",
    'e6_s1': "f(0) = 1, quad f(2) = 5, quad f(5) = -2",
    'e7_s1': "g = f - x arrow.double.long g' = f' - 1",
    'e7_s2': "g(2) - g(0) = integral_0^2 (x^2 - 1) dif x = 8/3 - 2 = gold(2/3) > 0",
    'tf_given': "S_1 = 3 thin (0 arrow.r 1), quad S_2 = 5 thin (1 arrow.r 4), quad S_3 = 4 thin (4 arrow.r 6)",
    'tf_a': "(0; 1)",
    'tf_b': "f(4) < f(1)",
    'tf_c': "f(6) < f(0)",
    'tf_d': "max_([0; 6]) f = f(6)",
    'tf_calc': "f(1) = f(0) + 3, quad f(4) = f(0) - 2, quad f(6) = f(0) + 2",
    'sa_task': "f(1) = 5, quad f'(x) = 2(x - 1)",
    'sa_s1': "f(4) = f(1) + integral_1^4 2(x - 1) dif x = 5 + 1/2 dot 3 dot 6 = gold(14)",
    'sum1': "f(b) - f(a) = integral_a^b f'",
    'sum2': "f(c) = f(a) plus.minus S",
    'sum3': "f' > 0 arrow.double.long f arrow.tr",
    'hw1': "f'(x) = x - 2, quad x in [0; 4]",
    'hw2': "f(0) = 1, quad f'(x) = 2x, quad f(3) = ?",
    'hw3': "f'(x) = cos x, quad x in [0; 2pi], quad max f",
    'hw_ans1': "f(0) = f(4)",
    'hw_ans2': "10",
    'hw_ans3': "x = pi/2",
    'next1': "V = integral_a^b S(x) dif x",
}

EXERCISES = (
    ("f'(x) = x − 2 trên [0; 4]: so sánh f(0), f(4)", 'f(0) = f(4)'),
    ("f(0) = 1, f'(x) = 2x: f(3)", '10'),
    ("f'(x) = cos x trên [0; 2π]: f lớn nhất tại", 'x = π/2'),
)

TRUE_FALSE = (
    ('f đồng biến trên (0; 1)', True),
    ('f(4) < f(1)', True),
    ('f(6) < f(0)', False),
    ('max f trên [0; 6] là f(6)', False),
)

x = sp.symbols('x', real=True)


def piece_areas(pieces):
    """Signed areas of a piecewise f' given as [(expr, lo, hi)]."""
    return [sp.integrate(e, (x, lo, hi)) for e, lo, hi in pieces]


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, pi = sp.integrate, sp.Rational, sp.pi
    # hook / e1: witness f' = 3x(2 − x) on [0, 2], (14/9)(x − 2)(x − 5) on [2, 5]
    hook = [(3 * x * (2 - x), 0, 2), (R(14, 9) * (x - 2) * (x - 5), 2, 5)]
    assert piece_areas(hook) == [4, -7]
    f0 = 0
    f2, f5 = f0 + 4, f0 + 4 - 7
    assert f5 < f0 < f2 and max(f0, f2, f5) == f2
    # e2
    assert I(x - 1, (x, 0, 1)) == -R(1, 2) and I(x - 1, (x, 1, 3)) == 2
    vals = {0: 0, 1: -R(1, 2), 3: R(3, 2)}
    assert min(vals, key=vals.get) == 1 and max(vals, key=vals.get) == 3
    # e3: quarter circle
    assert sp.simplify(I(sp.sqrt(4 - x**2), (x, 0, 2)) - pi) == 0
    # e4: three equal pieces
    g = x**2 - 2 * x
    assert [I(g, (x, -1, 0)), I(g, (x, 0, 2)), I(g, (x, 2, 3))] == [R(4, 3), -R(4, 3), R(4, 3)]
    F = I(g, (x, -1, x))  # f(x) − f(−1)
    v = {p: F.subs(x, p) for p in (-1, 0, 2, 3)}
    assert v[2] == v[-1] == 0 and v[3] == v[0] == R(4, 3)
    # e5/e6: f(0) = 1 on the hook witness → exactly one root on [0, 5]
    Fh = sp.Piecewise((1 + I(3 * x * (2 - x), (x, 0, x)), x <= 2),
                      (5 + I(R(14, 9) * (x - 2) * (x - 5), (x, 2, x)), True))
    assert Fh.subs(x, 2) == 5 and Fh.subs(x, 5) == -2
    assert sp.Poly(sp.expand(5 + I(R(14, 9) * (x - 2) * (x - 5), (x, 2, x))), x).count_roots(2, 5) == 1
    # e7: g = f − x with f' = x²
    assert I(x**2 - 1, (x, 0, 2)) == R(2, 3)
    # true / false: witness f' with pieces 3, −5, 4
    tf = [(18 * x * (1 - x), 0, 1), (R(10, 9) * (x - 1) * (x - 4), 1, 4), (-3 * (x - 4) * (x - 6), 4, 6)]
    assert piece_areas(tf) == [3, -5, 4]
    fv = {0: 0, 1: 3, 4: -2, 6: 2}
    assert all((18 * x * (1 - x)).subs(x, R(k, 10)) > 0 for k in range(1, 10))
    claims = (True, fv[4] < fv[1], fv[6] < fv[0], max(fv, key=fv.get) == 6)
    assert max(fv, key=fv.get) == 1
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer: f' through (1, 0) and (3, 4)
    fp = 2 * (x - 1)
    assert fp.subs(x, 1) == 0 and fp.subs(x, 3) == 4 and 5 + I(fp, (x, 1, 4)) == 14 and R(1, 2) * 3 * 6 == 9
    # exercises
    assert I(x - 2, (x, 0, 4)) == 0 and 1 + I(2 * x, (x, 0, 3)) == 10
    Fc = I(sp.cos(x), (x, 0, x))
    assert sp.solve(sp.Eq(sp.diff(Fc, x), 0), x)[0] == pi / 2 and Fc.subs(x, pi / 2) == 1
    assert max(float(Fc.subs(x, pi * k / 8)) for k in range(17)) == 1.0
    return True


validate()

"""INT22 – Diện tích giữa hai đường cong: tìm giao điểm & chia khoảng.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT22',
    'number': 22,
    'title': 'Diện tích giữa hai đường cong',
    'subtitle': 'Tìm giao điểm, chia khoảng, trên trừ dưới',
    'next_code': 'INT23',
    'next_title': 'Diện tích hình ghép & bài toán tham số',
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
         'Parabol y bằng x bình phương và đường thẳng y bằng x cộng hai cắt nhau, tạo thành một miền giống chiếc thuyền. '
         'Diện tích chiếc thuyền đó bằng bao nhiêu? Đáp số là chín phần hai. '
         'Hôm nay ta học cách tính diện tích của mọi miền nằm giữa hai đường cong.',
         'Mở đầu: chiếc thuyền giữa parabol và đường thẳng'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: diện tích giữa hai đường cong.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, công thức tích phân của trị tuyệt đối hiệu hai hàm, '
         'hiểu bằng dải mỏng trên trừ dưới. Hai, quy trình: tìm giao điểm, chia khoảng, xác định đường nào ở trên. '
         'Ba, các miền phức tạp hơn, kể cả khi nên tính tích phân theo biến y.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Cho hai hàm f và g liên tục trên đoạn từ a đến b. Diện tích hình phẳng giới hạn bởi hai đồ thị '
         'và hai đường thẳng x bằng a, x bằng b là S bằng tích phân từ a đến b của trị tuyệt đối f trừ g. '
         'Khi g bằng không, ta trở về công thức của tập hai mươi mốt.',
         'Công thức diện tích giữa hai đường'),
    Beat('c2', 'core',
         'Hình dung một dải mỏng thẳng đứng quét từ trái sang phải. Chiều cao của dải là khoảng cách giữa hai đồ thị: '
         'đường trên trừ đường dưới. Cộng dồn diện tích các dải, ta được tích phân của trên trừ dưới.',
         'Dải mỏng: trên trừ dưới'),
    Beat('c3', 'core',
         'Một điều thú vị: vị trí của trục hoành không quan trọng. Nếu dời cả hai đồ thị lên hoặc xuống cùng một đoạn, '
         'hiệu trên trừ dưới không đổi, nên diện tích không đổi. Vì vậy ta không cần quan tâm miền nằm trên hay dưới trục.'),
    Beat('c4', 'core',
         'Quy trình ba bước. Một, giải phương trình f bằng g để tìm hoành độ giao điểm. '
         'Hai, trên mỗi khoảng giữa hai giao điểm, xác định đường nào nằm trên, bằng cách thử một điểm. '
         'Ba, tính tích phân của trên trừ dưới trên từng khoảng rồi cộng lại.',
         'Quy trình ba bước'),
    Beat('c5', 'core',
         'Khi hai đồ thị cắt nhau nhiều lần, vai trò trên và dưới đổi chỗ sau mỗi giao điểm. '
         'Nếu dùng một tích phân cho cả đoạn mà không có trị tuyệt đối, các phần sẽ triệt tiêu nhau như ở tập trước.'),
    Beat('c6', 'core',
         'Ba bẫy thường gặp. Một, lấy dưới trừ trên, ra số âm. Hai, quên tách khoảng khi hai đường cắt nhau ở giữa. '
         'Ba, nhầm với công thức thể tích, viết bình phương của f trừ g. Diện tích chỉ cần hiệu, không bình phương.',
         'Bẫy thường gặp'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. x bình phương bằng x cộng hai cho x bằng trừ một và x bằng hai. '
         'Thử x bằng không: đường thẳng bằng hai, parabol bằng không, vậy đường thẳng ở trên. '
         'Diện tích bằng tích phân từ trừ một đến hai của x cộng hai trừ x bình phương, bằng chín phần hai.',
         'Ví dụ 1: parabol và đường thẳng'),
    Beat('e2', 'examples',
         'Ví dụ hai: y bằng x lập phương và y bằng x. Giao tại trừ một, không và một. '
         'Trên khoảng từ trừ một đến không, đường cong bậc ba ở trên; từ không đến một, đường thẳng ở trên. '
         'Mỗi phần bằng một phần tư, tổng bằng một phần hai.',
         'Ví dụ 2: đổi vai trên dưới'),
    Beat('e3', 'examples',
         'Ví dụ ba: y bằng căn x và y bằng x bình phương. Giao tại không và một. Trên đoạn này căn x ở trên. '
         'Diện tích bằng tích phân của căn x trừ x bình phương, bằng hai phần ba trừ một phần ba, bằng một phần ba. '
         'Miền này có hình chiếc lá, đối xứng qua đường y bằng x.',
         'Ví dụ 3: chiếc lá'),
    Beat('e4', 'examples',
         'Ví dụ bốn: y bằng e mũ x, y bằng e và trục tung. Đường nằm ngang y bằng e cắt e mũ x tại x bằng một, '
         'và trục tung là x bằng không. Diện tích bằng tích phân từ không đến một của e trừ e mũ x, '
         'bằng e trừ, e trừ một, bằng một.',
         'Ví dụ 4: có đường nằm ngang'),
    Beat('e5', 'examples',
         'Ví dụ năm: miền giới hạn bởi y bằng căn x, y bằng hai trừ x và trục hoành. Biên dưới luôn là trục hoành, '
         'nhưng biên trên đổi từ căn x sang hai trừ x tại x bằng một. Chia hai khoảng: '
         'hai phần ba cộng một phần hai, bằng bảy phần sáu.',
         'Ví dụ 5: biên thay đổi'),
    Beat('e6', 'examples',
         'Cách khác cho ví dụ năm: tính theo y. Với y từ không đến một, biên trái là x bằng y bình phương, '
         'biên phải là x bằng hai trừ y. Diện tích bằng tích phân của phải trừ trái theo d y, '
         'bằng hai trừ một phần hai trừ một phần ba, cũng bằng bảy phần sáu, mà chỉ cần một tích phân.',
         'Ví dụ 6: tích phân theo y'),
    Beat('e7', 'examples',
         'Ví dụ bảy, dạng rất hay gặp: parabol y bằng x bình phương, tiếp tuyến của nó tại điểm một, một, và trục tung. '
         'Tiếp tuyến là y bằng hai x trừ một. Parabol luôn nằm trên tiếp tuyến, hiệu bằng x trừ một, bình phương. '
         'Diện tích bằng tích phân từ không đến một của x trừ một bình phương, bằng một phần ba.',
         'Ví dụ 7: parabol và tiếp tuyến'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Gọi D là hình phẳng giới hạn bởi y bằng x bình phương trừ hai x và y bằng x. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: x bình phương trừ hai x bằng x cho x bằng không hoặc x bằng ba. '
         'Ý b đúng: thử x bằng một, đường thẳng bằng một, parabol bằng trừ một, đường thẳng ở trên.'),
    Beat('x3', 'exam',
         'Ý c đúng: đó chính là công thức tích phân của trị tuyệt đối hiệu. '
         'Ý d sai: tích phân từ không đến ba của ba x trừ x bình phương bằng chín phần hai, không phải chín.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: tính diện tích hình phẳng giới hạn bởi y bằng x bình phương và y bằng x cộng sáu, '
         'làm tròn đến hàng phần mười. Giao điểm tại x bằng trừ hai và x bằng ba.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Đường thẳng ở trên. Diện tích bằng tích phân từ trừ hai đến ba của x cộng sáu trừ x bình phương, '
         'bằng một trăm hai mươi lăm phần sáu, xấp xỉ hai mươi phẩy tám. Ghi vào phiếu: hai, không, phẩy, tám. '
         'Mẹo: với parabol và đường thẳng, diện tích bằng hệ số a nhân độ dài khoảng mũ ba, chia sáu.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, diện tích bằng tích phân của trị tuyệt đối f trừ g, hiểu là trên trừ dưới. '
         'Hai, quy trình: giao điểm, chia khoảng, thử điểm để biết đường nào ở trên. '
         'Ba, khi biên thay đổi, chia khoảng hoặc chuyển sang tích phân theo y.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, y bằng x bình phương và y bằng hai x. Hai, y bằng x lập phương và y bằng bốn x. '
         'Ba, y bằng căn x và y bằng x. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập hai mươi ba, ta gặp các bài diện tích có tham số: kéo tham số để diện tích thay đổi, '
         'tìm giá trị làm hai phần bằng nhau. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "y = x^2, quad y = x + 2",
    'hook_s': "S = gold(9/2)",
    'area2': "S = integral_a^b abs(f(x) - g(x)) dif x",
    'strip': "S = integral_a^b (y_1(x) - y_2(x)) dif x",
    'shift': "(f + k) - (g + k) = f - g",
    'e1_s0': "x^2 = x + 2 arrow.double.long x = -1, x = 2",
    'e1_s1': "S = integral_(-1)^2 (x + 2 - x^2) dif x = gold(9/2)",
    'e2_task': "y = x^3, quad y = x",
    'e2_s1': "S = integral_(-1)^0 (x^3 - x) dif x + integral_0^1 (x - x^3) dif x = 1/4 + 1/4 = gold(1/2)",
    'e3_task': "y = sqrt(x), quad y = x^2",
    'e3_s1': "S = integral_0^1 (sqrt(x) - x^2) dif x = 2/3 - 1/3 = gold(1/3)",
    'e4_task': "y = e^x, quad y = e, quad x = 0",
    'e4_s1': "S = integral_0^1 (e - e^x) dif x = e - (e - 1) = gold(1)",
    'e5_task': "y = sqrt(x), quad y = 2 - x, quad y = 0",
    'e5_s1': "S = integral_0^1 sqrt(x) dif x + integral_1^2 (2 - x) dif x = 2/3 + 1/2 = gold(7/6)",
    'e6_s1': "x = y^2, quad x = 2 - y, quad y in [0; 1]",
    'e6_s2': "S = integral_0^1 (2 - y - y^2) dif y = 2 - 1/2 - 1/3 = gold(7/6)",
    'e7_task': "y = x^2, quad y = 2x - 1, quad x = 0",
    'e7_s1': "S = integral_0^1 (x^2 - 2x + 1) dif x = integral_0^1 (x - 1)^2 dif x = gold(1/3)",
    'tf_given': "y = x^2 - 2x, quad y = x",
    'tf_a': "x = 0, quad x = 3",
    'tf_b': "x > x^2 - 2x quad forall x in (0; 3)",
    'tf_c': "S = integral_0^3 abs(x^2 - 3x) dif x",
    'tf_d': "S = 9",
    'tf_d_calc': "S = integral_0^3 (3x - x^2) dif x = 27/2 - 9 = 9/2 coral(!= 9)",
    'sa_task': "y = x^2, quad y = x + 6",
    'sa_s1': "S = integral_(-2)^3 (x + 6 - x^2) dif x = 125/6 approx gold(\"20,8\")",
    'sa_tip': "S = abs(a) (x_2 - x_1)^3 / 6 = 5^3/6",
    'sum1': "S = integral_a^b abs(f - g) dif x",
    'sum2': "f(x) = g(x) arrow.double.long x_1, x_2, dots",
    'sum3': "S = integral_c^d (x_2(y) - x_1(y)) dif y",
    'hw1': "y = x^2, quad y = 2x",
    'hw2': "y = x^3, quad y = 4x",
    'hw3': "y = sqrt(x), quad y = x",
    'hw_ans1': "4/3",
    'hw_ans2': "8",
    'hw_ans3': "1/6",
    'next1': "S(m) = integral_0^m dots arrow.double.long S_1 = S_2",
}

EXERCISES = (
    ('y = x² và y = 2x', '4/3'),
    ('y = x³ và y = 4x', '8'),
    ('y = √x và y = x', '1/6'),
)

TRUE_FALSE = (
    ('Giao tại x = 0, x = 3', True),
    ('x > x² − 2x với mọi x ∈ (0; 3)', True),
    ('S = ∫₀³ |x² − 3x| dx', True),
    ('S = 9', False),
)

x, y = sp.symbols('x y', real=True)


def between(f, g, lo, hi):
    """Area between two graphs on [lo, hi]: split at the intersections, add |piece|."""
    d = f - g
    cuts = sorted({sp.sympify(lo), sp.sympify(hi), *sp.solveset(d, x, sp.Interval(lo, hi))}, key=float)
    return sp.nsimplify(sum(abs(sp.integrate(d, (x, p, q))) for p, q in zip(cuts, cuts[1:])))


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, E = sp.integrate, sp.Rational, sp.E
    # hook / e1
    assert sorted(sp.solve(x**2 - x - 2, x)) == [-1, 2] and (x + 2 - x**2).subs(x, 0) > 0
    assert I(x + 2 - x**2, (x, -1, 2)) == R(9, 2) == between(x**2, x + 2, -1, 2)
    # e2
    assert sorted(sp.solve(x**3 - x, x)) == [-1, 0, 1] and between(x**3, x, -1, 1) == R(1, 2)
    assert I(x**3 - x, (x, -1, 0)) == R(1, 4) and I(x - x**3, (x, 0, 1)) == R(1, 4)
    # e3
    assert I(sp.sqrt(x) - x**2, (x, 0, 1)) == R(1, 3)
    # e4
    assert sp.solve(sp.exp(x) - E, x) == [1] and sp.simplify(I(E - sp.exp(x), (x, 0, 1)) - 1) == 0
    # e5 / e6 (two ways)
    assert sp.solve(sp.sqrt(x) - (2 - x), x) == [1]
    s5 = I(sp.sqrt(x), (x, 0, 1)) + I(2 - x, (x, 1, 2))
    s6 = I(2 - y - y**2, (y, 0, 1))
    assert s5 == R(7, 6) == s6
    tang = 2 * x - 1
    assert sp.diff(x**2, x).subs(x, 1) == 2 and tang.subs(x, 1) == 1 and sp.factor(x**2 - tang) == (x - 1)**2
    assert I((x - 1)**2, (x, 0, 1)) == R(1, 3)
    # true / false
    f, g = x**2 - 2 * x, x
    S = between(f, g, 0, 3)
    claims = (sorted(sp.solve(f - g, x)) == [0, 3], all((g - f).subs(x, R(k, 10)) > 0 for k in range(1, 30)),
              sp.nsimplify(I(sp.Abs(x**2 - 3 * x), (x, 0, 1)) + I(sp.Abs(x**2 - 3 * x), (x, 1, 3))) == S, S == 9)
    assert S == R(9, 2) and I(3 * x - x**2, (x, 0, 3)) == R(9, 2)
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer and the a·L³/6 shortcut
    assert sorted(sp.solve(x**2 - x - 6, x)) == [-2, 3]
    sa = I(x + 6 - x**2, (x, -2, 3))
    assert sa == R(125, 6) == R(5**3, 6) and f'{float(sa):.1f}' == '20.8'
    # exercises
    assert between(x**2, 2 * x, 0, 2) == R(4, 3) and between(x**3, 4 * x, -2, 2) == 8
    assert I(sp.sqrt(x) - x, (x, 0, 1)) == R(1, 6)
    return True


validate()

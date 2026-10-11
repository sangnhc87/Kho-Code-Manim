"""INT23 – Diện tích hình ghép & bài toán tham số: tối ưu diện tích.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT23',
    'number': 23,
    'title': 'Diện tích có tham số',
    'subtitle': 'Hình ghép, chia đôi diện tích, tối ưu',
    'next_code': 'INT24',
    'next_title': "Đọc diện tích từ đồ thị f'",
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
         'Miền giới hạn bởi parabol y bằng bốn trừ x bình phương và trục hoành có diện tích ba mươi hai phần ba. '
         'Kéo một đường nằm ngang y bằng m từ dưới lên: phần phía trên nhỏ dần. '
         'Với m bằng bao nhiêu thì đường này chia miền thành hai phần bằng nhau? Đáp số xấp xỉ một phẩy bốn tám.',
         'Mở đầu: chia đôi diện tích'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi ba của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'diện tích hình ghép và bài toán tham số.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, tính diện tích hình ghép bằng cộng và trừ các miền đơn giản. '
         'Hai, biểu diễn diện tích thành hàm của tham số rồi giải phương trình. '
         'Ba, tìm tham số để diện tích nhỏ nhất, với công thức nhanh cho parabol và đường thẳng.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Hình ghép: khi miền có hình dạng phức tạp, hãy chia nó thành các miền đơn giản rồi cộng lại, '
         'hoặc lấy một miền lớn trừ đi phần thừa. Ví dụ miền dưới căn x, trên đường thẳng x trừ hai và trên trục hoành '
         'bằng toàn bộ miền dưới căn x, trừ đi một tam giác.',
         'Hình ghép: cộng và trừ'),
    Beat('c2', 'core',
         'Tham số trong cận: diện tích giới hạn bởi y bằng x bình phương, trục hoành và x bằng a là S của a bằng a lập phương chia ba. '
         'Diện tích lúc này là một hàm của a. Đề cho S bằng chín thì ta giải a lập phương bằng hai mươi bảy, được a bằng ba.',
         'Diện tích là hàm của tham số'),
    Beat('c3', 'core',
         'Tham số trong hàm: parabol y bằng x bình phương và đường thẳng y bằng m x, với m dương. '
         'Hai đồ thị cắt nhau tại không và m. Diện tích S của m bằng tích phân từ không đến m của m x trừ x bình phương, '
         'bằng m lập phương chia sáu. Kéo m lớn dần, diện tích tăng rất nhanh, theo lập phương.'),
    Beat('c4', 'core',
         'Nhắc lại công thức nhanh từ tập trước: diện tích giữa parabol hệ số a và một đường thẳng cắt nó tại x một và x hai '
         'bằng trị tuyệt đối a nhân x hai trừ x một, mũ ba, chia sáu. Chỉ cần biết khoảng cách giữa hai giao điểm.',
         'Công thức nhanh a·d³/6'),
    Beat('c5', 'core',
         'Bài toán tối ưu: đường thẳng đi qua điểm một, hai cắt parabol y bằng x bình phương tại hai điểm. '
         'Khi xoay đường thẳng, khoảng cách hai giao điểm thay đổi, và diện tích cũng thay đổi. '
         'Diện tích nhỏ nhất khi khoảng cách đó nhỏ nhất.',
         'Tối ưu diện tích'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: tìm m dương để diện tích giới hạn bởi y bằng x bình phương và y bằng m x bằng bốn phần ba. '
         'Ta có m lập phương chia sáu bằng bốn phần ba, nên m lập phương bằng tám, m bằng hai.',
         'Ví dụ 1: tìm m theo diện tích'),
    Beat('e2', 'examples',
         'Ví dụ hai: tìm a dương để diện tích giới hạn bởi y bằng e mũ x, trục hoành, x bằng không và x bằng a, '
         'bằng e bình phương trừ một. Diện tích bằng e mũ a trừ một. Giải ra a bằng hai.',
         'Ví dụ 2: tham số trong cận'),
    Beat('e3', 'examples',
         'Ví dụ ba, giải bài mở đầu. Phần phía trên đường y bằng m là miền giữa parabol và đường nằm ngang, '
         'hai giao điểm cách nhau hai căn của bốn trừ m. Theo công thức nhanh, diện tích bằng bốn phần ba nhân '
         'bốn trừ m, mũ ba phần hai. Cho bằng một nửa của ba mươi hai phần ba, tức mười sáu phần ba.',
         'Ví dụ 3: giải bài mở đầu'),
    Beat('e4', 'examples',
         'Ta được bốn trừ m, mũ ba phần hai, bằng bốn. Suy ra bốn trừ m bằng căn bậc ba của mười sáu, bằng hai căn bậc ba của hai. '
         'Vậy m bằng bốn trừ hai căn bậc ba của hai, xấp xỉ một phẩy bốn tám. Đường chia đôi không nằm giữa chiều cao, '
         'mà thấp hơn, vì phần dưới rộng hơn.'),
    Beat('e5', 'examples',
         'Ví dụ bốn, tối ưu. Đường thẳng qua điểm một, hai có hệ số góc k: y bằng k nhân x trừ một, cộng hai. '
         'Phương trình hoành độ giao điểm là x bình phương trừ k x cộng k trừ hai bằng không, có biệt thức bằng k bình phương '
         'trừ bốn k cộng tám.',
         'Ví dụ 4: diện tích nhỏ nhất'),
    Beat('e6', 'examples',
         'Khoảng cách hai giao điểm bằng căn của biệt thức. Diện tích bằng biệt thức mũ ba phần hai, chia sáu. '
         'Biệt thức bằng k trừ hai, bình phương, cộng bốn, nhỏ nhất bằng bốn khi k bằng hai. '
         'Vậy diện tích nhỏ nhất bằng tám chia sáu, bằng bốn phần ba.'),
    Beat('e7', 'examples',
         'Ví dụ năm, hình ghép: miền giới hạn bởi y bằng căn x, y bằng x trừ hai và trục hoành. '
         'Lấy diện tích dưới căn x từ không đến bốn, bằng mười sáu phần ba, trừ đi tam giác dưới đường thẳng từ hai đến bốn, '
         'bằng hai. Kết quả mười phần ba.',
         'Ví dụ 5: hình ghép'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho parabol y bằng x bình phương và đường thẳng y bằng m x, với m dương. '
         'Gọi S của m là diện tích hình phẳng giới hạn bởi hai đường. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: x bình phương bằng m x cho x bằng không hoặc x bằng m. '
         'Ý b đúng: tích phân từ không đến m của m x trừ x bình phương bằng m lập phương chia sáu.'),
    Beat('x3', 'exam',
         'Ý c sai: gấp đôi m thì diện tích gấp tám lần, vì diện tích tỉ lệ với m lập phương. '
         'Ý d đúng: m lập phương chia sáu bằng ba mươi sáu cho m lập phương bằng hai trăm mười sáu, m bằng sáu.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: đường thẳng y bằng k x cộng một cắt parabol y bằng x bình phương tại hai điểm. '
         'Tìm giá trị nhỏ nhất của diện tích hình phẳng giới hạn bởi hai đường, làm tròn đến hàng phần trăm.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Phương trình x bình phương trừ k x trừ một bằng không có biệt thức k bình phương cộng bốn. '
         'Diện tích bằng k bình phương cộng bốn, mũ ba phần hai, chia sáu, nhỏ nhất khi k bằng không: '
         'tám chia sáu, xấp xỉ một phẩy ba ba. Ghi vào phiếu: một, phẩy, ba, ba.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, hình ghép: cộng các miền đơn giản hoặc lấy miền lớn trừ phần thừa. '
         'Hai, tham số: viết diện tích thành hàm S của m, rồi giải phương trình. '
         'Ba, tối ưu: với parabol và đường thẳng, dùng công thức a nhân d lập phương chia sáu, rồi tìm d nhỏ nhất.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tìm m trong khoảng không đến hai để diện tích giữa y bằng hai x trừ x bình phương '
         'và y bằng m x bằng một phần sáu. Hai, tìm a dương để diện tích dưới e mũ x từ không đến a bằng e bình phương trừ một. '
         'Ba, đường y bằng m chia đôi miền giữa y bằng x bình phương và y bằng bốn. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập hai mươi bốn, ta đọc diện tích từ đồ thị của đạo hàm để so sánh các giá trị của f, '
         'một dạng vận dụng cao rất được yêu thích. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "y = 4 - x^2, quad y = 0: quad S = 32/3",
    'hook_q': "y = m: quad S_1 = S_2 arrow.double.long m approx gold(\"1,48\")",
    'comp': "S = integral_0^4 sqrt(x) dif x - integral_2^4 (x - 2) dif x",
    'pa': "S(a) = integral_0^a x^2 dif x = a^3/3 = 9 arrow.double.long a = gold(3)",
    'pm': "S(m) = integral_0^m (m x - x^2) dif x = m^3/6",
    'quick': "S = abs(a) (x_2 - x_1)^3 / 6",
    'opt': "S_min arrow.l.r.double (x_2 - x_1)_min",
    'e1_s1': "m^3/6 = 4/3 arrow.double.long m^3 = 8 arrow.double.long m = gold(2)",
    'e2_s1': "integral_0^a e^x dif x = e^a - 1 = e^2 - 1 arrow.double.long a = gold(2)",
    'e3_s1': "S_1(m) = 4/3 (4 - m)^(3\\/2) = 1/2 dot 32/3 = 16/3",
    'e4_s1': "(4 - m)^(3\\/2) = 4 arrow.double.long 4 - m = root(3, 16) = 2 root(3, 2)",
    'e4_s2': "m = 4 - 2 root(3, 2) approx gold(\"1,48\")",
    'e5_s1': "y = k(x - 1) + 2: quad x^2 - k x + k - 2 = 0, quad Delta = k^2 - 4k + 8",
    'e6_s1': "S = Delta^(3\\/2) / 6, quad Delta = (k - 2)^2 + 4 >= 4",
    'e6_s2': "S_min = 4^(3\\/2) / 6 = 8/6 = gold(4/3) quad (k = 2)",
    'e7_s1': "S = 16/3 - 2 = gold(10/3)",
    'tf_given': "y = x^2, quad y = m x quad (m > 0)",
    'tf_a': "x = 0, quad x = m",
    'tf_b': "S(m) = m^3/6",
    'tf_c': "S(2m) = 2 S(m)",
    'tf_d': "S(m) = 36 arrow.l.r.double m = 6",
    'tf_c_calc': "S(2m) = (2m)^3/6 = 8 S(m) coral(!= 2 S(m))",
    'sa_task': "y = k x + 1, quad y = x^2",
    'sa_s1': "x^2 - k x - 1 = 0, quad Delta = k^2 + 4 >= 4",
    'sa_s2': "S = (k^2 + 4)^(3\\/2) / 6 >= 8/6 approx gold(\"1,33\")",
    'sum1': "S = S_1 + S_2, quad S = S_0 - S_3",
    'sum2': "S(m) = c arrow.double.long m",
    'sum3': "S = abs(a) d^3 / 6",
    'hw1': "y = 2x - x^2, quad y = m x, quad S = 1/6",
    'hw2': "integral_0^a e^x dif x = e^2 - 1",
    'hw3': "y = x^2, quad y = 4, quad y = m: quad S_1 = S_2",
    'hw_ans1': "m = 1",
    'hw_ans2': "a = 2",
    'hw_ans3': "m = 2 root(3, 2)",
    'next1': "f(b) - f(a) = integral_a^b f'(x) dif x",
}

EXERCISES = (
    ('y = 2x − x² và y = mx (0 < m < 2), S = 1/6: tìm m', 'm = 1'),
    ('∫₀ᵃ eˣ dx = e² − 1: tìm a > 0', 'a = 2'),
    ('y = m chia đôi miền giữa y = x² và y = 4', 'm = 2∛2'),
)

TRUE_FALSE = (
    ('Giao tại x = 0, x = m', True),
    ('S(m) = m³/6', True),
    ('S(2m) = 2S(m)', False),
    ('S(m) = 36 ⇔ m = 6', True),
)

x, m, k, a = sp.symbols('x m k a', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, E = sp.integrate, sp.Rational, sp.E
    mp = sp.symbols('mp', positive=True)
    # hook / e3 / e4: y = m halves the region under 4 − x²
    total = I(4 - x**2, (x, -2, 2))
    assert total == R(32, 3)
    top = I(4 - x**2 - mp, (x, -sp.sqrt(4 - mp), sp.sqrt(4 - mp)))
    assert sp.simplify(top - R(4, 3) * (4 - mp)**R(3, 2)) == 0
    msol = 4 - 2 * sp.cbrt(2)
    assert sp.simplify((4 - msol)**R(3, 2) - 4) == 0 and abs(float(top.subs(mp, msol)) - 16 / 3) < 1e-12
    assert f'{float(msol):.2f}' == '1.48' and sp.simplify(sp.cbrt(16) - 2 * sp.cbrt(2)) == 0
    # composite region
    comp = I(sp.sqrt(x), (x, 0, 4)) - I(x - 2, (x, 2, 4))
    assert comp == R(10, 3) and I(sp.sqrt(x), (x, 0, 4)) == R(16, 3) and I(x - 2, (x, 2, 4)) == 2
    # S(a) = a^3/3 = 9
    ap = sp.symbols('ap', positive=True)
    assert I(x**2, (x, 0, ap)) == ap**3 / 3 and sp.solve(sp.Eq(ap**3 / 3, 9), ap) == [3]
    # S(m) = m^3/6 for y = x^2, y = mx
    Sm = I(mp * x - x**2, (x, 0, mp))
    assert sp.simplify(Sm - mp**3 / 6) == 0
    assert sp.solve(sp.Eq(Sm, R(4, 3)), mp) == [2] and sp.solve(sp.Eq(Sm, 36), mp) == [6]
    # quick formula |a| d^3 / 6 on an example (x^2 vs x + 6: d = 5)
    assert I(x + 6 - x**2, (x, -2, 3)) == R(5**3, 6)
    # e2
    assert sp.solve(sp.Eq(sp.exp(ap) - 1, E**2 - 1), ap) == [2]
    # optimisation through (1, 2)
    disc = sp.discriminant(x**2 - k * x + k - 2, x)
    assert sp.expand(disc - (k**2 - 4 * k + 8)) == 0 and sp.expand(disc - ((k - 2)**2 + 4)) == 0
    r1, r2 = sp.solve(x**2 - 2 * x + 0, x)  # k = 2: x^2 − 2x = 0
    assert I(2 * (x - 1) + 2 - x**2, (x, r1, r2)) == R(4, 3) == R(8, 6)
    # true / false
    claims = (sp.solve(x**2 - mp * x, x) == [0, mp], sp.simplify(Sm - mp**3 / 6) == 0,
              sp.simplify(Sm.subs(mp, 2 * mp) - 2 * Sm) == 0, sp.solve(sp.Eq(Sm, 36), mp) == [6])
    assert sp.simplify(Sm.subs(mp, 2 * mp) - 8 * Sm) == 0
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer: y = kx + 1 and y = x^2, minimum area at k = 0
    d2 = sp.discriminant(x**2 - k * x - 1, x)
    assert sp.expand(d2 - (k**2 + 4)) == 0
    smin = I(1 - x**2, (x, -1, 1))
    assert smin == R(4, 3) and f'{float(smin):.2f}' == '1.33'
    # exercises
    assert sp.solve(sp.Eq((2 - mp)**3 / 6, R(1, 6)), mp) == [1]
    assert sp.simplify(I(2 * x - x**2 - 1 * x, (x, 0, 1)) - R(1, 6)) == 0
    below = R(4, 3) * mp**R(3, 2)  # area between y = x^2 and y = m (below m)
    assert sp.simplify(I(mp - x**2, (x, -sp.sqrt(mp), sp.sqrt(mp))) - below) == 0
    mh = 2 * sp.cbrt(2)
    assert I(4 - x**2, (x, -2, 2)) == R(32, 3) and sp.simplify(below.subs(mp, mh) - R(16, 3)) == 0
    return True


validate()

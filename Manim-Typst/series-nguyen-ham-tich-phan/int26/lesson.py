"""INT26 – Thể tích khối tròn xoay quanh Ox: phương pháp đĩa.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT26',
    'number': 26,
    'title': 'Khối tròn xoay quanh Ox',
    'subtitle': 'Phương pháp đĩa: V = π∫f²(x)dx',
    'next_code': 'INT27',
    'next_title': 'Khối tròn xoay giữa hai đường',
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
         'Lấy miền phẳng dưới đồ thị y bằng căn x, với x từ không đến bốn, rồi quay nó một vòng quanh trục hoành. '
         'Ta được một vật thể giống chiếc chén. Thể tích của nó là bao nhiêu? Đáp số là tám pi, '
         'và cách tính chỉ cần một tích phân.',
         'Mở đầu: quay miền phẳng thành chiếc chén'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi sáu của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'thể tích khối tròn xoay quanh trục O x.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, công thức V bằng pi nhân tích phân của f bình phương, '
         'hiểu bằng các đĩa tròn mỏng. Hai, cách tránh những bẫy quen thuộc khi bình phương. '
         'Ba, dùng công thức để chứng minh thể tích hình nón và hình cầu.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Khi quay miền dưới đồ thị y bằng f của x quanh trục O x, mỗi điểm trên đồ thị vạch ra một đường tròn. '
         'Vì vậy thiết diện vuông góc với trục tại x là một hình tròn bán kính trị tuyệt đối f của x. '
         'Diện tích thiết diện là pi nhân f bình phương.',
         'Thiết diện là hình tròn'),
    Beat('c2', 'core',
         'Áp dụng công thức của tập trước, thể tích bằng tích phân của diện tích thiết diện: '
         'V bằng pi nhân tích phân từ a đến b của f bình phương. Mỗi lát mỏng là một chiếc đĩa tròn, '
         'nên cách tính này gọi là phương pháp đĩa.',
         'Công thức V = π∫f²'),
    Beat('c2b', 'core',
         'Đặt hai công thức cạnh nhau để khỏi nhầm. Diện tích miền phẳng là tích phân của trị tuyệt đối f, không có pi, không bình phương. '
         'Thể tích khi quay miền đó quanh O x là pi nhân tích phân của f bình phương. '
         'Đề thi thường hỏi cả hai trong cùng một câu đúng sai.'),
    Beat('c3', 'core',
         'Quy trình bốn bước. Một, xác định hàm f và hai cận a, b. Hai, bình phương f, rút gọn. '
         'Ba, tính tích phân. Bốn, đừng quên nhân pi. Phần lớn lỗi sai nằm ở bước hai và bước bốn.',
         'Quy trình bốn bước'),
    Beat('c4', 'core',
         'Khi f âm, miền nằm dưới trục hoành, nhưng quay quanh trục vẫn cho cùng một khối, '
         'vì bán kính là trị tuyệt đối f, và bình phương đã xóa dấu. Không cần tách cận như khi tính diện tích.'),
    Beat('c5', 'core',
         'Ba bẫy hay gặp. Một, quên bình phương, viết pi nhân tích phân của f. Hai, bình phương sai, '
         'ví dụ x cộng một bình phương thành x bình phương cộng một. Ba, bình phương cả tích phân, '
         'tức pi nhân bình phương của tích phân f, hoàn toàn khác pi nhân tích phân của f bình phương.',
         'Ba bẫy về bình phương'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. f bằng căn x, f bình phương bằng x. '
         'Thể tích bằng pi nhân tích phân từ không đến bốn của x, bằng pi nhân tám, bằng tám pi.',
         'Ví dụ 1: chiếc chén'),
    Beat('e2', 'examples',
         'Ví dụ hai, chứng minh thể tích hình nón. Quay tam giác dưới đường y bằng r chia h nhân x, '
         'với x từ không đến h. Thể tích bằng pi nhân r bình phương chia h bình phương nhân tích phân của x bình phương, '
         'bằng một phần ba pi r bình phương h.',
         'Ví dụ 2: hình nón'),
    Beat('e3', 'examples',
         'Ví dụ ba, chứng minh thể tích hình cầu. Quay nửa đường tròn y bằng căn của R bình phương trừ x bình phương '
         'quanh trục hoành. f bình phương bằng R bình phương trừ x bình phương, và tích phân từ trừ R đến R '
         'cho bốn phần ba R lập phương. Nhân pi: bốn phần ba pi R lập phương.',
         'Ví dụ 3: hình cầu'),
    Beat('e4', 'examples',
         'Ví dụ bốn: quay miền dưới y bằng sin x, với x từ không đến pi. '
         'Sin bình phương x bằng một trừ cốt hai x, chia hai. Tích phân từ không đến pi bằng pi chia hai. '
         'Vậy thể tích bằng pi bình phương chia hai.',
         'Ví dụ 4: hàm lượng giác'),
    Beat('e5', 'examples',
         'Ví dụ năm: y bằng e mũ x, với x từ không đến một. f bình phương là e mũ hai x, '
         'nguyên hàm là e mũ hai x chia hai. Thể tích bằng pi nhân e bình phương trừ một, chia hai.',
         'Ví dụ 5: hàm mũ'),
    Beat('e6', 'examples',
         'Ví dụ sáu: miền giới hạn bởi y bằng x bình phương trừ hai x và trục hoành nằm dưới trục. '
         'Không cần quan tâm dấu: bình phương lên rồi lấy tích phân từ không đến hai, '
         'được mười sáu phần mười lăm. Thể tích bằng mười sáu pi chia mười lăm.',
         'Ví dụ 6: miền dưới trục'),
    Beat('e7', 'examples',
         'Dạng ngược: quay miền dưới y bằng căn x, với x từ không đến a, được khối có thể tích tám pi. Tìm a. '
         'Thể tích bằng pi nhân a bình phương chia hai. Cho bằng tám pi, ta được a bình phương bằng mười sáu, a bằng bốn.',
         'Ví dụ 7: biết thể tích, tìm cận'),
    Beat('e8', 'examples',
         'Mẹo kiểm tra bằng máy tính: nhập pi nhân tích phân của f bình phương. Ví dụ năm cho pi nhân e bình phương trừ một, chia hai, '
         'máy tính ra khoảng mười phẩy không bốn. Nếu đáp án trắc nghiệm ở dạng chính xác, hãy bấm từng phương án để so sánh.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Gọi H là hình phẳng giới hạn bởi y bằng hai x trừ x bình phương và trục hoành, '
         'V là thể tích khối tròn xoay khi quay H quanh O x. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: hai x trừ x bình phương bằng không tại x bằng không và x bằng hai. '
         'Ý b sai: đó là bẫy quên bình phương.'),
    Beat('x3', 'exam',
         'Ý c đúng: đây chính là công thức đĩa. Ý d sai: tích phân của f bình phương bằng mười sáu phần mười lăm, '
         'nhưng thể tích phải nhân thêm pi, tức mười sáu pi chia mười lăm.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: quay miền dưới đồ thị y bằng một chia x, với x từ một đến ba, quanh trục hoành. '
         'Tính thể tích, làm tròn đến hàng phần trăm.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'f bình phương bằng một chia x bình phương, nguyên hàm là trừ một chia x. Tích phân từ một đến ba bằng '
         'một trừ một phần ba, bằng hai phần ba. Thể tích bằng hai pi chia ba, xấp xỉ hai phẩy không chín. '
         'Ghi vào phiếu: hai, phẩy, không, chín.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, quay quanh O x, thiết diện là hình tròn, thể tích bằng pi nhân tích phân của f bình phương. '
         'Hai, bình phương đúng, không bình phương cả tích phân, và nhớ nhân pi. '
         'Ba, công thức này chứng minh được thể tích hình nón và hình cầu.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, quay miền dưới y bằng x, với x từ không đến ba. '
         'Hai, quay nửa đường tròn y bằng căn bốn trừ x bình phương. Ba, quay miền dưới y bằng cốt x, '
         'với x từ không đến pi phần hai. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập hai mươi bảy, ta quay miền nằm giữa hai đường cong, được những chiếc đĩa có lỗ ở giữa, '
         'gọi là vành khăn. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "y = sqrt(x), quad x in [0; 4] quad arrow.ccw quad O x",
    'hook_v': "V = gold(8 pi)",
    'disc': "S(x) = pi f^2(x)",
    'vol': "V = pi integral_a^b f^2(x) dif x",
    'neg': "(-f)^2 = f^2",
    'trap1': "V coral(!=) pi integral_a^b f(x) dif x",
    'trap2': "(x + 1)^2 = x^2 + 2x + 1 coral(!=) x^2 + 1",
    'trap3': "pi integral_a^b f^2 dif x coral(!=) pi (integral_a^b f dif x)^2",
    'e1_s1': "V = pi integral_0^4 (sqrt(x))^2 dif x = pi integral_0^4 x dif x = gold(8 pi)",
    'e2_s1': "V = pi integral_0^h (r^2 x^2)/h^2 dif x = gold(1/3 pi r^2 h)",
    'e3_s1': "V = pi integral_(-R)^R (R^2 - x^2) dif x = gold(4/3 pi R^3)",
    'e4_s1': "V = pi integral_0^pi sin^2 x dif x = pi integral_0^pi (1 - cos 2x)/2 dif x = gold(pi^2/2)",
    'e5_s1': "V = pi integral_0^1 e^(2x) dif x = gold((pi (e^2 - 1))/2)",
    'e6_s1': "V = pi integral_0^2 (x^2 - 2x)^2 dif x = gold((16 pi)/15)",
    'cmp_s': "S = integral_a^b abs(f(x)) dif x",
    'cmp_v': "V = pi integral_a^b f^2(x) dif x",
    'e7_s1': "V = pi integral_0^a x dif x = (pi a^2)/2 = 8 pi arrow.double.long a = gold(4)",
    'e8_s1': "(pi (e^2 - 1))/2 approx \"10,04\"",
    'tf_given': "y = 2x - x^2, quad y = 0",
    'tf_a': "x = 0, quad x = 2",
    'tf_b': "V = pi integral_0^2 (2x - x^2) dif x",
    'tf_c': "V = pi integral_0^2 (2x - x^2)^2 dif x",
    'tf_d': "V = 16/15",
    'tf_d_calc': "integral_0^2 (2x - x^2)^2 dif x = 16/15 arrow.double.long V = (16 pi)/15 coral(!= 16/15)",
    'sa_task': "y = 1/x, quad x in [1; 3]",
    'sa_s1': "V = pi integral_1^3 1/x^2 dif x = pi (1 - 1/3) = (2 pi)/3 approx gold(\"2,09\")",
    'sum1': "V = pi integral_a^b f^2 dif x",
    'sum2': "pi integral f^2 != pi (integral f)^2",
    'sum3': "1/3 pi r^2 h, quad 4/3 pi R^3",
    'hw1': "y = x, quad x in [0; 3]",
    'hw2': "y = sqrt(4 - x^2)",
    'hw3': "y = cos x, quad x in [0; pi/2]",
    'hw_ans1': "9 pi",
    'hw_ans2': "(32 pi)/3",
    'hw_ans3': "pi^2/4",
    'next1': "V = pi integral_a^b (f^2 - g^2) dif x",
}

EXERCISES = (
    ('Quay y = x, x ∈ [0; 3]', '9π'),
    ('Quay y = √(4 − x²)', '32π/3'),
    ('Quay y = cos x, x ∈ [0; π/2]', 'π²/4'),
)

TRUE_FALSE = (
    ('Giao Ox tại x = 0, x = 2', True),
    ('V = π∫₀²(2x − x²) dx', False),
    ('V = π∫₀²(2x − x²)² dx', True),
    ('V = 16/15', False),
)

x, r, h, R = sp.symbols('x r h R', positive=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R_, pi, E = sp.integrate, sp.Rational, sp.pi, sp.E
    V = lambda f, a, b: pi * I(f**2, (x, a, b))  # noqa: E731
    assert V(sp.sqrt(x), 0, 4) == 8 * pi
    assert sp.simplify(V(r / h * x, 0, h) - pi * r**2 * h / 3) == 0
    assert sp.simplify(V(sp.sqrt(R**2 - x**2), -R, R) - R_(4, 3) * pi * R**3) == 0
    assert sp.simplify(V(sp.sin(x), 0, pi) - pi**2 / 2) == 0
    assert sp.simplify(V(sp.exp(x), 0, 1) - pi * (E**2 - 1) / 2) == 0
    assert V(x**2 - 2 * x, 0, 2) == R_(16, 15) * pi
    ap = sp.symbols('ap', positive=True)
    assert sp.solve(sp.Eq(V(sp.sqrt(x), 0, ap), 8 * pi), ap) == [4]
    assert f'{float(pi * (E**2 - 1) / 2):.2f}' == '10.04'
    # traps
    assert sp.expand((x + 1)**2) == x**2 + 2 * x + 1
    assert pi * I(x, (x, 0, 4)) != pi * I(sp.sqrt(x), (x, 0, 4))**2
    # true / false
    f = 2 * x - x**2
    Vt = V(f, 0, 2)
    t = sp.symbols('t', real=True)
    claims = (sorted(sp.solve(f.subs(x, t), t)) == [0, 2], pi * I(f, (x, 0, 2)) == Vt, Vt == pi * I(f**2, (x, 0, 2)),
              Vt == R_(16, 15))
    assert I(f**2, (x, 0, 2)) == R_(16, 15) and Vt == R_(16, 15) * pi
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    Vs = V(1 / x, 1, 3)
    assert Vs == 2 * pi / 3 and f'{float(Vs):.2f}' == '2.09'
    # exercises
    assert V(x, 0, 3) == 9 * pi and V(sp.sqrt(4 - x**2), -2, 2) == R_(32, 3) * pi
    assert sp.simplify(V(sp.cos(x), 0, pi / 2) - pi**2 / 4) == 0
    return True


validate()

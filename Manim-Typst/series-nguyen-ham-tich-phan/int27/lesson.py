"""INT27 – Khối tròn xoay giữa hai đường: vành khăn & bẫy π∫(f − g)².

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT27',
    'number': 27,
    'title': 'Khối tròn xoay giữa hai đường',
    'subtitle': 'Vành khăn: khối ngoài trừ khối trong',
    'next_code': 'INT28',
    'next_title': 'Chứng minh thể tích nón, cầu, chỏm cầu',
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
         'Quay miền nằm giữa đường thẳng y bằng x và parabol y bằng x bình phương quanh trục hoành. '
         'Rất nhiều bạn viết pi nhân tích phân của x trừ x bình phương, bình phương, và được pi chia ba mươi. '
         'Đáp số đúng là hai pi chia mười lăm, lớn gấp bốn lần. Sai ở đâu?',
         'Mở đầu: một lỗi rất phổ biến'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi bảy của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'khối tròn xoay giữa hai đường.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, thiết diện là vành khăn, một chiếc đĩa bị khoét lỗ ở giữa. '
         'Hai, công thức pi nhân tích phân của f bình phương trừ g bình phương. '
         'Ba, vì sao bình phương của hiệu là một cái bẫy.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Khi quay miền giữa hai đồ thị y bằng f và y bằng g, với f lớn hơn g và cả hai không âm, '
         'mỗi lát cắt vuông góc với trục là một vành khăn: hình tròn lớn bán kính f bị khoét đi hình tròn nhỏ bán kính g.',
         'Thiết diện là vành khăn'),
    Beat('c2', 'core',
         'Diện tích vành khăn bằng diện tích hình tròn lớn trừ hình tròn nhỏ: pi f bình phương trừ pi g bình phương. '
         'Lấy tích phân, ta được V bằng pi nhân tích phân từ a đến b của f bình phương trừ g bình phương. '
         'Nói cách khác: thể tích khối ngoài trừ thể tích khối trong.',
         'Công thức vành khăn'),
    Beat('c3', 'core',
         'Cái bẫy: f bình phương trừ g bình phương không bằng f trừ g, bình phương. '
         'Về hình học, f trừ g là bề dày của vành khăn. Bình phương của bề dày cho diện tích một hình tròn nhỏ, '
         'chứ không phải diện tích vành khăn, vì vành khăn nằm xa trục và rộng hơn nhiều.',
         'Bẫy bình phương của hiệu'),
    Beat('c3b', 'core',
         'Thử với số cụ thể: vành khăn có bán kính ngoài hai, bán kính trong một. Diện tích đúng là pi nhân bốn trừ một, bằng ba pi. '
         'Còn pi nhân hai trừ một, bình phương, chỉ bằng pi, nhỏ hơn ba lần. Một phép thử nhỏ như vậy giúp em nhớ mãi.'),
    Beat('c4', 'core',
         'Quy trình bốn bước. Một, tìm giao điểm để có cận. Hai, xác định đường ngoài, là đường xa trục hơn, '
         'và đường trong. Ba, bình phương từng hàm rồi mới trừ. Bốn, tính tích phân và nhân pi.',
         'Quy trình bốn bước'),
    Beat('c5', 'core',
         'Lưu ý: công thức này dùng khi miền nằm hoàn toàn một phía của trục hoành. '
         'Đề thi trong chương trình mới hầu như luôn cho miền như vậy. '
         'Nếu cả hai hàm đều âm, ta lấy trị tuyệt đối: đường ngoài vẫn là đường xa trục hơn.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. Giao điểm tại không và một. Trên đoạn này x lớn hơn x bình phương, '
         'nên đường ngoài là y bằng x. Thể tích bằng pi nhân tích phân của x bình phương trừ x mũ bốn, '
         'bằng pi nhân một phần ba trừ một phần năm, bằng hai pi chia mười lăm.',
         'Ví dụ 1: bài mở đầu'),
    Beat('e2', 'examples',
         'So sánh với cách sai: pi nhân tích phân của x trừ x bình phương, bình phương, chỉ bằng pi chia ba mươi, '
         'bằng một phần tư đáp số đúng. Sai lệch lớn như vậy, nên trắc nghiệm thường đặt đúng phương án sai này để bẫy.'),
    Beat('e3', 'examples',
         'Ví dụ hai: y bằng căn x và y bằng x bình phương, giao tại không và một. Đường ngoài là căn x. '
         'Thể tích bằng pi nhân tích phân của x trừ x mũ bốn, bằng ba pi chia mười.',
         'Ví dụ 2: chiếc lá quay'),
    Beat('e4', 'examples',
         'Ví dụ ba: y bằng ba trừ x bình phương và y bằng x bình phương cộng một, giao tại trừ một và một. '
         'Đường ngoài là ba trừ x bình phương. Hiệu bình phương rút gọn được tám trừ tám x bình phương. '
         'Thể tích bằng ba mươi hai pi chia ba.',
         'Ví dụ 3: hai parabol'),
    Beat('e5', 'examples',
         'Ví dụ bốn: y bằng e mũ x, y bằng một và x bằng một. Với x từ không đến một, e mũ x lớn hơn một, là đường ngoài. '
         'Thể tích bằng pi nhân tích phân của e mũ hai x trừ một, bằng pi nhân e bình phương trừ ba, chia hai.',
         'Ví dụ 4: có đường nằm ngang'),
    Beat('e6', 'examples',
         'Cách nhìn khác cho mọi bài vành khăn: thể tích bằng khối ngoài trừ khối trong. '
         'Ở ví dụ bốn, khối ngoài là khối quay e mũ x, khối trong là hình trụ bán kính một, cao một, thể tích pi. '
         'Lấy pi nhân e bình phương trừ một chia hai, trừ pi, được cùng kết quả.'),
    Beat('e7', 'examples',
         'Luyện phản xạ chọn công thức. Quay miền dưới một đường cong: dùng đĩa, pi nhân tích phân f bình phương. '
         'Quay miền giữa hai đường không cắt trục: dùng vành khăn, pi nhân tích phân f bình phương trừ g bình phương. '
         'Hỏi diện tích miền phẳng: không có pi, tích phân của trị tuyệt đối f trừ g. Ba công thức, ba tình huống.',
         'Chọn đúng công thức'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Quay miền giới hạn bởi y bằng hai x và y bằng x bình phương quanh trục hoành, '
         'được khối có thể tích V. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: hai x bằng x bình phương tại không và hai. '
         'Ý b đúng: thử x bằng một, đường thẳng bằng hai, parabol bằng một.'),
    Beat('x3', 'exam',
         'Ý c sai: đó chính là bẫy bình phương của hiệu. Ý d đúng: pi nhân tích phân của bốn x bình phương trừ x mũ bốn '
         'bằng pi nhân ba mươi hai phần ba trừ ba mươi hai phần năm, bằng sáu mươi tư pi chia mười lăm.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: quay miền giới hạn bởi y bằng căn x và y bằng x chia hai quanh trục hoành. '
         'Tính thể tích, làm tròn đến hàng phần trăm. Hai đường giao tại không và bốn.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Trên đoạn từ không đến bốn, căn x lớn hơn x chia hai. Thể tích bằng pi nhân tích phân của x trừ x bình phương chia bốn, '
         'bằng pi nhân tám trừ mười sáu phần ba, bằng tám pi chia ba, xấp xỉ tám phẩy ba tám. '
         'Ghi vào phiếu: tám, phẩy, ba, tám.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, quay miền giữa hai đường, thiết diện là vành khăn. '
         'Hai, thể tích bằng pi nhân tích phân của f bình phương trừ g bình phương, hay khối ngoài trừ khối trong. '
         'Ba, tuyệt đối không viết bình phương của hiệu.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, quay miền giữa y bằng x và y bằng x lập phương, với x từ không đến một. '
         'Hai, quay miền giữa y bằng một và y bằng x bình phương. Ba, quay miền giữa y bằng căn x và y bằng một, '
         'với x từ một đến bốn. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập hai mươi tám, ta dùng tích phân để dựng lại các công thức thể tích quen thuộc: hình nón, hình cầu và chỏm cầu. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "y = x, quad y = x^2 quad arrow.ccw quad O x",
    'hook_wrong': "pi integral_0^1 (x - x^2)^2 dif x = pi/30 quad coral(times)",
    'hook_right': "V = gold((2 pi)/15) quad green(checkmark)",
    'ring': "S(x) = pi f^2(x) - pi g^2(x)",
    'washer': "V = pi integral_a^b (f^2(x) - g^2(x)) dif x",
    'outin': "V = V_1 - V_2",
    'trap': "f^2 - g^2 coral(!=) (f - g)^2",
    'trap_geo': "pi (R^2 - r^2) coral(!=) pi (R - r)^2",
    'e1_s1': "V = pi integral_0^1 (x^2 - x^4) dif x = pi (1/3 - 1/5) = gold((2 pi)/15)",
    'e2_s1': "pi integral_0^1 (x - x^2)^2 dif x = pi/30 = 1/4 dot (2 pi)/15",
    'e3_task': "y = sqrt(x), quad y = x^2",
    'e3_s1': "V = pi integral_0^1 (x - x^4) dif x = pi (1/2 - 1/5) = gold((3 pi)/10)",
    'e4_task': "y = 3 - x^2, quad y = x^2 + 1",
    'e4_s1': "(3 - x^2)^2 - (x^2 + 1)^2 = 8 - 8x^2",
    'e4_s2': "V = pi integral_(-1)^1 (8 - 8x^2) dif x = gold((32 pi)/3)",
    'e5_task': "y = e^x, quad y = 1, quad x = 1",
    'e5_s1': "V = pi integral_0^1 (e^(2x) - 1) dif x = gold((pi (e^2 - 3))/2)",
    'e6_s1': "V = (pi (e^2 - 1))/2 - pi dot 1^2 dot 1 = (pi (e^2 - 3))/2",
    'num': "pi (2^2 - 1^2) = 3 pi quad coral(!=) quad pi (2 - 1)^2 = pi",
    'pick1': "V = pi integral_a^b f^2 dif x",
    'pick2': "V = pi integral_a^b (f^2 - g^2) dif x",
    'pick3': "S = integral_a^b abs(f - g) dif x",
    'tf_given': "y = 2x, quad y = x^2",
    'tf_a': "x = 0, quad x = 2",
    'tf_b': "2x >= x^2 quad forall x in [0; 2]",
    'tf_c': "V = pi integral_0^2 (2x - x^2)^2 dif x",
    'tf_d': "V = (64 pi)/15",
    'tf_d_calc': "V = pi integral_0^2 (4x^2 - x^4) dif x = pi (32/3 - 32/5) = (64 pi)/15",
    'sa_task': "y = sqrt(x), quad y = x/2",
    'sa_s1': "V = pi integral_0^4 (x - x^2/4) dif x = pi (8 - 16/3) = (8 pi)/3 approx gold(\"8,38\")",
    'sum1': "S(x) = pi (f^2 - g^2)",
    'sum2': "V = V_1 - V_2",
    'sum3': "f^2 - g^2 != (f - g)^2",
    'hw1': "y = x, quad y = x^3, quad x in [0; 1]",
    'hw2': "y = 1, quad y = x^2",
    'hw3': "y = sqrt(x), quad y = 1, quad x in [1; 4]",
    'hw_ans1': "(4 pi)/21",
    'hw_ans2': "(8 pi)/5",
    'hw_ans3': "(9 pi)/2",
    'next1': "V = 1/3 pi r^2 h, quad V = 4/3 pi R^3, quad V = pi h^2 (R - h/3)",
}

EXERCISES = (
    ('Quay miền giữa y = x và y = x³, x ∈ [0; 1]', '4π/21'),
    ('Quay miền giữa y = 1 và y = x²', '8π/5'),
    ('Quay miền giữa y = √x và y = 1, x ∈ [1; 4]', '9π/2'),
)

TRUE_FALSE = (
    ('Giao tại x = 0, x = 2', True),
    ('2x ≥ x² trên [0; 2]', True),
    ('V = π∫₀²(2x − x²)² dx', False),
    ('V = 64π/15', True),
)

x = sp.symbols('x', real=True)


def washer(f, g, a, b):
    return sp.pi * sp.integrate(f**2 - g**2, (x, a, b))


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, pi, E = sp.integrate, sp.Rational, sp.pi, sp.E
    # hook / e1 / e2
    good, bad = washer(x, x**2, 0, 1), pi * I((x - x**2)**2, (x, 0, 1))
    assert good == 2 * pi / 15 and bad == pi / 30 and sp.simplify(bad / good) == R(1, 4)
    # e3
    assert washer(sp.sqrt(x), x**2, 0, 1) == 3 * pi / 10
    # e4
    assert sorted(sp.solve(3 - x**2 - (x**2 + 1), x)) == [-1, 1]
    assert sp.expand((3 - x**2)**2 - (x**2 + 1)**2) == 8 - 8 * x**2 and washer(3 - x**2, x**2 + 1, -1, 1) == 32 * pi / 3
    # e5 / e6
    v5 = washer(sp.exp(x), 1, 0, 1)
    assert sp.simplify(v5 - pi * (E**2 - 3) / 2) == 0
    assert sp.simplify(pi * I(sp.exp(2 * x), (x, 0, 1)) - pi * 1 * 1 - v5) == 0
    assert sp.pi * (2**2 - 1**2) == 3 * sp.pi and sp.pi * (2 - 1)**2 == sp.pi
    # true / false
    Vt = washer(2 * x, x**2, 0, 2)
    claims = (sorted(sp.solve(2 * x - x**2, x)) == [0, 2], all((2 * x - x**2).subs(x, R(k, 10)) >= 0 for k in range(21)),
              pi * I((2 * x - x**2)**2, (x, 0, 2)) == Vt, Vt == 64 * pi / 15)
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    assert sorted(sp.solve(sp.sqrt(x) - x / 2, x)) == [0, 4]
    Vs = washer(sp.sqrt(x), x / 2, 0, 4)
    assert Vs == 8 * pi / 3 and f'{float(Vs):.2f}' == '8.38'
    # exercises
    assert washer(x, x**3, 0, 1) == 4 * pi / 21
    assert washer(1, x**2, -1, 1) == 8 * pi / 5
    assert washer(sp.sqrt(x), 1, 1, 4) == 9 * pi / 2
    return True


validate()

"""INT28 – Chứng minh thể tích nón, cầu, chỏm cầu: dựng lại công thức bằng tích phân.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT28',
    'number': 28,
    'title': 'Dựng lại công thức thể tích',
    'subtitle': 'Trụ, nón, cầu, chỏm cầu, nón cụt bằng tích phân',
    'next_code': 'INT29',
    'next_title': 'Bài toán chuyển động thực tế',
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
         'Thể tích chỏm cầu bằng pi h bình phương nhân R trừ h phần ba. Công thức này trông khá lạ, '
         'và rất khó nhớ nếu học thuộc lòng. Nhưng với tích phân, ta dựng lại nó chỉ trong ba dòng, '
         'và không bao giờ quên nữa.',
         'Mở đầu: công thức chỏm cầu từ đâu ra?'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi tám, khép lại phần ứng dụng hình học: dựng lại các công thức thể tích bằng tích phân.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, chiến lược chung: đặt vật thể vào hệ trục và tìm đường sinh. '
         'Hai, dựng lại thể tích hình trụ, hình nón, hình cầu. '
         'Ba, các khối khó hơn: chỏm cầu, nón cụt và khối elip tròn xoay.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Chiến lược chung: mọi khối tròn xoay đều sinh ra khi quay một đường y bằng f của x quanh trục O x. '
         'Việc của ta là chọn hệ trục khéo léo để đường sinh có phương trình đơn giản, xác định cận, '
         'rồi áp dụng công thức pi nhân tích phân của f bình phương.',
         'Chiến lược: tìm đường sinh'),
    Beat('c2', 'core',
         'Hình trụ bán kính r, chiều cao h: đường sinh là đường nằm ngang y bằng r, với x từ không đến h. '
         'Thể tích bằng pi nhân tích phân của r bình phương, bằng pi r bình phương h. '
         'Đúng là diện tích đáy nhân chiều cao.',
         'Hình trụ'),
    Beat('c2b', 'core',
         'Một biến thể: ống trụ rỗng, bán kính ngoài R, bán kính trong r, dài h. Đây là bài vành khăn của tập trước, '
         'với hai đường nằm ngang. Thể tích bằng pi nhân R bình phương trừ r bình phương, nhân h. '
         'Chú ý lại một lần nữa: không phải pi nhân R trừ r, bình phương.'),
    Beat('c3', 'core',
         'Hình nón: đường sinh là đoạn thẳng từ gốc tọa độ, y bằng r chia h nhân x. '
         'Tích phân của x bình phương từ không đến h cho h lập phương chia ba, nên thể tích bằng một phần ba pi r bình phương h. '
         'Hình nón bằng đúng một phần ba hình trụ cùng đáy, cùng chiều cao.',
         'Hình nón'),
    Beat('c4', 'core',
         'Hình cầu: đường sinh là nửa đường tròn y bằng căn của R bình phương trừ x bình phương, x từ trừ R đến R. '
         'Bình phương làm mất căn, tích phân của R bình phương trừ x bình phương cho bốn phần ba R lập phương. '
         'Thể tích hình cầu bằng bốn phần ba pi R lập phương.',
         'Hình cầu'),
    Beat('c5', 'core',
         'Một quan hệ đẹp do Archimedes phát hiện: hình cầu nội tiếp trong hình trụ cao hai R có thể tích bằng hai phần ba hình trụ. '
         'Hình trụ có thể tích hai pi R lập phương, hai phần ba của nó là bốn phần ba pi R lập phương. '
         'Archimedes tự hào về kết quả này đến mức muốn khắc nó lên bia mộ.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Chỏm cầu chiều cao h là phần hình cầu nằm giữa x bằng R trừ h và x bằng R. '
         'Vẫn đường sinh của hình cầu, chỉ đổi cận. Tích phân từ R trừ h đến R của R bình phương trừ x bình phương, '
         'rút gọn lại được pi h bình phương nhân R trừ h phần ba. Đó chính là công thức ở đầu bài.',
         'Chỏm cầu'),
    Beat('e2', 'examples',
         'Kiểm tra hai trường hợp đặc biệt. Khi h bằng R, chỏm cầu là nửa hình cầu: pi R bình phương nhân hai R phần ba, '
         'bằng hai phần ba pi R lập phương, đúng một nửa hình cầu. Khi h bằng hai R, ta được cả hình cầu. '
         'Công thức đúng ở cả hai đầu.'),
    Beat('e3', 'examples',
         'Nón cụt có bán kính hai đáy R và r, chiều cao h. Đường sinh là đoạn thẳng y bằng r cộng R trừ r chia h nhân x. '
         'Tích phân cho pi h chia ba nhân R bình phương cộng R r cộng r bình phương. '
         'Khi r bằng không, ta trở về hình nón.',
         'Nón cụt'),
    Beat('e3b', 'examples',
         'Thử với số: nón cụt có R bằng hai, r bằng một, h bằng ba. Thể tích bằng pi nhân ba chia ba, nhân bốn cộng hai cộng một, '
         'bằng bảy pi. Kiểm tra bằng hiệu hai hình nón: nón lớn cao sáu, đáy bán kính hai, trừ nón nhỏ cao ba, đáy bán kính một, '
         'tám pi trừ pi, cũng bằng bảy pi.'),
    Beat('e4', 'examples',
         'Khối elip tròn xoay: quay elip x bình phương chia a bình phương cộng y bình phương chia b bình phương bằng một quanh O x. '
         'y bình phương bằng b bình phương nhân một trừ x bình phương chia a bình phương. '
         'Thể tích bằng bốn phần ba pi a b bình phương. Khi a bằng b bằng R, ta lại được hình cầu.',
         'Khối elip tròn xoay'),
    Beat('e5', 'examples',
         'Bài toán thực tế: một chiếc bát hình bán cầu bán kính mười xăng ti mét chứa nước sâu bốn xăng ti mét. '
         'Phần nước là một chỏm cầu với R bằng mười, h bằng bốn. Thể tích bằng pi nhân mười sáu nhân mười trừ bốn phần ba, '
         'bằng bốn trăm mười sáu pi chia ba, khoảng bốn trăm ba mươi sáu xăng ti mét khối.',
         'Ví dụ: nước trong bát'),
    Beat('e6', 'examples',
         'Một điều thú vị để kết thúc phần ví dụ: đạo hàm của thể tích hình cầu theo R là bốn pi R bình phương, '
         'đúng bằng diện tích mặt cầu. Tương tự, đạo hàm của diện tích hình tròn pi R bình phương là chu vi hai pi R. '
         'Thêm một lớp vỏ mỏng dày d R thì thể tích tăng thêm khoảng diện tích mặt nhân d R.',
         'Bonus: thể tích và diện tích mặt cầu'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai về khối cầu bán kính ba, sinh bởi nửa đường tròn quay quanh O x. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: nửa đường tròn tâm gốc tọa độ bán kính ba có phương trình y bằng căn chín trừ x bình phương. '
         'Ý b đúng: đây là công thức đĩa với cận từ trừ ba đến ba.'),
    Beat('x3', 'exam',
         'Ý c sai: tích phân bằng ba mươi sáu, nên V bằng ba mươi sáu pi, không phải hai mươi bảy pi. '
         'Ý d đúng: chỏm cầu cao một có thể tích pi nhân ba trừ một phần ba, bằng tám pi chia ba.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: bồn chứa có dạng chỏm cầu bán kính năm mét, chiều cao hai mét. '
         'Tính thể tích bồn theo mét khối, làm tròn đến hàng đơn vị.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Thể tích bằng pi nhân bốn nhân năm trừ hai phần ba, bằng năm mươi hai pi chia ba, xấp xỉ năm mươi tư phẩy năm. '
         'Làm tròn đến hàng đơn vị được năm mươi tư. Hoặc tính trực tiếp tích phân từ ba đến năm của hai lăm trừ x bình phương, '
         'nhân pi, cũng ra kết quả đó.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, mọi công thức thể tích tròn xoay đều đến từ pi nhân tích phân của f bình phương. '
         'Hai, chọn hệ trục để đường sinh đơn giản: đường nằm ngang, đường thẳng qua gốc, nửa đường tròn. '
         'Ba, chỏm cầu là hình cầu với cận khác; quên công thức thì dựng lại.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, thể tích hình trụ bán kính hai, cao năm. Hai, chỏm cầu bán kính bốn, cao một. '
         'Ba, khối elip tròn xoay với a bằng ba, b bằng hai. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Từ tập hai mươi chín, ta bước sang phần D: ứng dụng thực tế, bắt đầu với các bài toán chuyển động như phanh xe '
         'và hai xe gặp nhau. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'cap': "V = pi h^2 (R - h/3)",
    'gen': "V = pi integral_a^b f^2(x) dif x",
    'cyl_f': "y = r, quad x in [0; h]",
    'cyl_v': "V = pi integral_0^h r^2 dif x = gold(pi r^2 h)",
    'cone_f': "y = r/h x, quad x in [0; h]",
    'cone_v': "V = pi r^2/h^2 integral_0^h x^2 dif x = gold(1/3 pi r^2 h)",
    'sph_f': "y = sqrt(R^2 - x^2), quad x in [-R; R]",
    'cap_f': "y = sqrt(R^2 - x^2), quad x in [R - h; R]",
    'sph_v': "V = pi integral_(-R)^R (R^2 - x^2) dif x = gold(4/3 pi R^3)",
    'arch': "2/3 dot pi R^2 dot 2R = 4/3 pi R^3",
    'cap_v': "V = pi integral_(R - h)^R (R^2 - x^2) dif x = gold(pi h^2 (R - h/3))",
    'cap_half': "h = R: quad pi R^2 dot (2R)/3 = 2/3 pi R^3",
    'cap_full': "h = 2R: quad pi dot 4R^2 dot R/3 = 4/3 pi R^3",
    'frus_f': "y = r + (R - r)/h x, quad x in [0; h]",
    'frus_v': "V = gold((pi h)/3 (R^2 + R r + r^2))",
    'ell_f': "x^2/a^2 + y^2/b^2 = 1 arrow.double.long y^2 = b^2 (1 - x^2/a^2)",
    'ell_v': "V = pi integral_(-a)^a b^2 (1 - x^2/a^2) dif x = gold(4/3 pi a b^2)",
    'bowl': "V = pi dot 4^2 (10 - 4/3) = (416 pi)/3 approx gold(\"436\") \"cm\"^3",
    'tube': "V = pi (R^2 - r^2) h quad coral(!=) quad pi (R - r)^2 h",
    'frus_num': "V = (pi dot 3)/3 (4 + 2 + 1) = gold(7 pi)",
    'frus_chk': "1/3 pi dot 2^2 dot 6 - 1/3 pi dot 1^2 dot 3 = 8 pi - pi = 7 pi",
    'shell1': "dif/(dif R) (4/3 pi R^3) = 4 pi R^2",
    'shell2': "dif/(dif R) (pi R^2) = 2 pi R",
    'tf_a': "y = sqrt(9 - x^2)",
    'tf_b': "V = pi integral_(-3)^3 (9 - x^2) dif x",
    'tf_c': "V = 27 pi",
    'tf_d': "V = (8 pi)/3",
    'tf_c_calc': "integral_(-3)^3 (9 - x^2) dif x = 36 arrow.double.long V = 36 pi coral(!= 27 pi)",
    'sa_s1': "V = pi dot 2^2 (5 - 2/3) = (52 pi)/3 approx \"54,45\" approx gold(54)",
    'sa_s2': "pi integral_3^5 (25 - x^2) dif x = (52 pi)/3",
    'sum1': "V = pi integral_a^b f^2 dif x",
    'sum2': "y = r, quad y = r/h x, quad y = sqrt(R^2 - x^2)",
    'sum3': "V = pi h^2 (R - h/3)",
    'hw1': "r = 2, quad h = 5",
    'hw2': "R = 4, quad h = 1",
    'hw3': "a = 3, quad b = 2",
    'hw_ans1': "20 pi",
    'hw_ans2': "(11 pi)/3",
    'hw_ans3': "16 pi",
    'next1': "s = integral_(t_1)^(t_2) abs(v(t)) dif t",
}

EXERCISES = (
    ('Hình trụ r = 2, h = 5', '20π'),
    ('Chỏm cầu R = 4, h = 1', '11π/3'),
    ('Khối elip tròn xoay a = 3, b = 2', '16π'),
)

TRUE_FALSE = (
    ('Đường sinh y = √(9 − x²)', True),
    ('V = π∫₋₃³(9 − x²) dx', True),
    ('V = 27π', False),
    ('Chỏm cầu cao 1 có V = 8π/3', True),
)

x = sp.symbols('x', real=True)
r, h, R, a, b = sp.symbols('r h R a b', positive=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, Q, pi = sp.integrate, sp.Rational, sp.pi
    V = lambda f, lo, hi: pi * I(f**2, (x, lo, hi))  # noqa: E731
    assert sp.simplify(V(r, 0, h) - pi * r**2 * h) == 0
    assert sp.simplify(V(r / h * x, 0, h) - pi * r**2 * h / 3) == 0
    sph = V(sp.sqrt(R**2 - x**2), -R, R)
    assert sp.simplify(sph - Q(4, 3) * pi * R**3) == 0
    assert sp.simplify(Q(2, 3) * pi * R**2 * 2 * R - sph) == 0
    cap = pi * I(R**2 - x**2, (x, R - h, R))
    assert sp.simplify(cap - pi * h**2 * (R - h / 3)) == 0
    assert sp.simplify(cap.subs(h, R) - sph / 2) == 0 and sp.simplify(cap.subs(h, 2 * R) - sph) == 0
    frus = V(r + (R - r) / h * x, 0, h)
    assert sp.simplify(frus - pi * h / 3 * (R**2 + R * r + r**2)) == 0
    assert sp.simplify(frus.subs(r, 0) - pi * R**2 * h / 3) == 0
    ell = pi * I(b**2 * (1 - x**2 / a**2), (x, -a, a))
    assert sp.simplify(ell - Q(4, 3) * pi * a * b**2) == 0 and sp.simplify(ell.subs({a: R, b: R}) - sph) == 0
    bowl = pi * 4**2 * (10 - Q(4, 3))
    assert bowl == Q(416, 3) * pi and round(float(bowl)) == 436
    assert sp.simplify(pi * I(100 - x**2, (x, 6, 10)) - bowl) == 0
    assert sp.simplify(frus.subs({R: 2, r: 1, h: 3}) - 7 * pi) == 0
    assert Q(1, 3) * pi * 4 * 6 - Q(1, 3) * pi * 1 * 3 == 7 * pi
    assert sp.diff(Q(4, 3) * pi * R**3, R) == 4 * pi * R**2 and sp.diff(pi * R**2, R) == 2 * pi * R
    # true / false
    Vs = V(sp.sqrt(9 - x**2), -3, 3)
    capv = pi * 1**2 * (3 - Q(1, 3))
    claims = (True, Vs == pi * I(9 - x**2, (x, -3, 3)), Vs == 27 * pi, capv == 8 * pi / 3)
    assert Vs == 36 * pi and sp.simplify(pi * I(9 - x**2, (x, 2, 3)) - capv) == 0
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    sa = pi * 2**2 * (5 - Q(2, 3))
    assert sa == 52 * pi / 3 and sp.simplify(pi * I(25 - x**2, (x, 3, 5)) - sa) == 0
    assert f'{float(sa):.2f}' == '54.45' and round(float(sa)) == 54  # → 54
    # exercises
    assert V(2, 0, 5) == 20 * pi and pi * 1 * (4 - Q(1, 3)) == Q(11, 3) * pi and Q(4, 3) * pi * 3 * 4 == 16 * pi
    return True


validate()

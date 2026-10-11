"""INT32 – Tích phân trong kinh tế và sinh học: từ tốc độ biên đến tổng lượng.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT32',
    'number': 32,
    'title': 'Tích phân trong kinh tế và sinh học',
    'subtitle': 'Từ chi phí biên, tốc độ tăng trưởng đến tổng lượng',
    'next_code': 'INT33',
    'next_title': 'Mô hình hóa từ dữ liệu thực',
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
         'Một xưởng có chi phí biên C phẩy của x bằng không phẩy ba x cộng hai mươi nghìn đồng cho mỗi sản phẩm. '
         'Xưởng đang sản xuất một trăm sản phẩm. Nếu sản xuất thêm một trăm sản phẩm nữa, chi phí tăng bao nhiêu? '
         'Đáp số là sáu triệu rưỡi đồng, và đó lại là một tích phân.',
         'Mở đầu: chi phí tăng thêm'),
    Beat('h2', 'hook',
         'Đây là tập ba mươi hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân trong kinh tế và sinh học.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, đại lượng biên là đạo hàm, tổng lượng là tích phân. '
         'Hai, lợi nhuận tăng thêm và sản lượng tối ưu. '
         'Ba, các mô hình tăng trưởng trong sinh học và y học.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Trong kinh tế, chi phí biên là chi phí để sản xuất thêm một sản phẩm, chính là đạo hàm C phẩy của x. '
         'Biết chi phí biên, ta tìm được chi phí tăng thêm khi sản lượng tăng từ a đến b: '
         'C của b trừ C của a bằng tích phân từ a đến b của C phẩy.',
         'Đại lượng biên là đạo hàm'),
    Beat('c2', 'core',
         'Tương tự, doanh thu biên là R phẩy, và lợi nhuận biên là doanh thu biên trừ chi phí biên. '
         'Lợi nhuận tăng thêm khi sản lượng tăng từ a đến b là tích phân của R phẩy trừ C phẩy. '
         'Trên đồ thị, đó là phần diện tích nằm giữa hai đường biên.',
         'Lợi nhuận tăng thêm'),
    Beat('c3', 'core',
         'Lợi nhuận tăng khi doanh thu biên lớn hơn chi phí biên, giảm khi ngược lại. '
         'Vì vậy sản lượng tối ưu là nơi doanh thu biên bằng chi phí biên, tức giao điểm của hai đường biên. '
         'Ý tưởng này giống hệt bài toán hai xe ở tập hai mươi chín.',
         'Sản lượng tối ưu'),
    Beat('c3b', 'core',
         'Một khái niệm nữa: thặng dư tiêu dùng. Với hàm cầu giá theo số lượng D của x và giá bán P, '
         'những người sẵn sàng trả cao hơn P đã được lợi. Tổng phần lợi đó là diện tích giữa đường cầu và đường giá: '
         'tích phân từ không đến Q của D trừ P. Ví dụ D bằng một trăm trừ không phẩy năm x, P bằng sáu mươi, '
         'thì Q bằng tám mươi và thặng dư bằng một nghìn sáu trăm.',
         'Thặng dư tiêu dùng'),
    Beat('c4', 'core',
         'Trong sinh học, tốc độ tăng trưởng của một quần thể là N phẩy của t. Số cá thể tại thời điểm T '
         'bằng số ban đầu cộng tích phân từ không đến T của tốc độ tăng trưởng. '
         'Mọi bài toán tốc độ đều theo cùng một khuôn: tổng lượng bằng giá trị đầu cộng tích phân của tốc độ.',
         'Tăng trưởng trong sinh học'),
    Beat('c5', 'core',
         'Trong y học, tốc độ đào thải thuốc thường giảm dần theo hàm mũ. Lượng thuốc bị đào thải sau T giờ '
         'là tích phân của tốc độ đào thải. Đơn vị cần nhất quán: mi li gam mỗi giờ nhân giờ cho mi li gam.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. Chi phí tăng thêm bằng tích phân từ một trăm đến hai trăm của không phẩy ba x cộng hai mươi, '
         'bằng không phẩy một năm nhân ba mươi nghìn, cộng hai nghìn, tức sáu nghìn năm trăm nghìn đồng, '
         'bằng sáu phẩy năm triệu đồng.',
         'Ví dụ 1: chi phí tăng thêm'),
    Beat('e2', 'examples',
         'Ví dụ hai: doanh thu biên một trăm trừ không phẩy hai x, chi phí biên hai mươi cộng không phẩy hai x, nghìn đồng mỗi sản phẩm. '
         'Lợi nhuận biên tám mươi trừ không phẩy bốn x bằng không tại x bằng hai trăm: đó là sản lượng tối ưu.',
         'Ví dụ 2: sản lượng tối ưu'),
    Beat('e3', 'examples',
         'Lợi nhuận tăng thêm khi nâng sản lượng từ một trăm lên hai trăm bằng tích phân của tám mươi trừ không phẩy bốn x, '
         'bằng tám nghìn trừ sáu nghìn, bằng hai nghìn nghìn đồng, tức hai triệu đồng. '
         'Nếu sản xuất vượt hai trăm, mỗi sản phẩm thêm lại làm lợi nhuận giảm.'),
    Beat('e4', 'examples',
         'Ví dụ ba: một đàn vi khuẩn có năm nghìn con, tốc độ tăng trưởng một nghìn nhân e mũ không phẩy hai t con mỗi giờ. '
         'Sau mười giờ, số vi khuẩn bằng năm nghìn cộng năm nghìn nhân e bình phương trừ một, '
         'bằng năm nghìn e bình phương, khoảng ba mươi sáu nghìn chín trăm bốn mươi lăm con.',
         'Ví dụ 3: vi khuẩn'),
    Beat('e5', 'examples',
         'Ví dụ bốn: tốc độ đào thải thuốc là hai mươi nhân e mũ trừ không phẩy năm t mi li gam mỗi giờ. '
         'Trong bốn giờ đầu, lượng thuốc bị đào thải bằng bốn mươi nhân một trừ e mũ trừ hai, '
         'khoảng ba mươi tư phẩy năm chín mi li gam.',
         'Ví dụ 4: đào thải thuốc'),
    Beat('e6', 'examples',
         'Ví dụ năm: dân số một thành phố tăng với tốc độ hai cộng không phẩy một t nghìn người mỗi năm. '
         'Sau mười năm, dân số tăng thêm tích phân từ không đến mười, bằng hai mươi cộng năm, bằng hai mươi lăm nghìn người.',
         'Ví dụ 5: dân số'),
    Beat('e7', 'examples',
         'Ví dụ sáu, bài toán ngược: dân số tăng với tốc độ a cộng không phẩy hai t nghìn người mỗi năm, '
         'và sau mười năm tăng thêm ba mươi nghìn người. Tích phân từ không đến mười bằng mười a cộng mười. '
         'Cho bằng ba mươi, ta được a bằng hai.',
         'Ví dụ 6: tìm tham số'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Một doanh nghiệp có chi phí biên C phẩy của x bằng hai x cộng năm mươi nghìn đồng, '
         'chi phí cố định C của không bằng một nghìn nghìn đồng. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: C bằng một nghìn cộng tích phân của hai u cộng năm mươi, bằng x bình phương cộng năm mươi x cộng một nghìn. '
         'Ý b đúng: C của mười bằng một trăm cộng năm trăm cộng một nghìn, bằng một nghìn sáu trăm.'),
    Beat('x3', 'exam',
         'Ý c sai: chi phí tăng thêm từ mười đến hai mươi bằng tích phân của hai x cộng năm mươi, bằng ba trăm cộng năm trăm, '
         'bằng tám trăm. Ý d đúng: chi phí biên tại x bằng mười là hai mươi cộng năm mươi, bằng bảy mươi.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: một quần thể cá ban đầu có hai nghìn con, tốc độ tăng trưởng ba trăm căn t con mỗi năm. '
         'Sau bốn năm có bao nhiêu con cá?',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Số cá tăng thêm bằng tích phân từ không đến bốn của ba trăm căn t, bằng ba trăm nhân hai phần ba nhân t mũ ba phần hai '
         'lấy cận, bằng hai trăm nhân tám, bằng một nghìn sáu trăm. Tổng cộng ba nghìn sáu trăm con. '
         'Ghi vào phiếu: ba, sáu, không, không.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, đại lượng biên và tốc độ là đạo hàm; tổng lượng là giá trị đầu cộng tích phân. '
         'Hai, lợi nhuận tăng thêm là tích phân của doanh thu biên trừ chi phí biên; tối ưu khi hai đại lượng biên bằng nhau. '
         'Ba, sinh học và y học dùng cùng khuôn đó, thường với hàm mũ.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, chi phí biên không phẩy bốn x cộng mười, tính chi phí tăng thêm từ năm mươi đến một trăm sản phẩm. '
         'Hai, doanh thu biên sáu mươi trừ không phẩy một x, chi phí biên hai mươi cộng không phẩy một x: sản lượng tối ưu. '
         'Ba, quần thể năm trăm cá thể, tốc độ năm mươi e mũ không phẩy một t: số cá thể sau mười năm. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập ba mươi ba, ta đi từ bảng số liệu thực tế đến hàm số và tích phân: mô hình hóa từ dữ liệu, '
         'với những câu trả lời ngắn nhiều bước. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "C'(x) = \"0,3\" x + 20 quad (\"nghìn đồng\"), quad x: 100 arrow.r 200",
    'marg': "C(b) - C(a) = integral_a^b C'(x) dif x",
    'profit': "P(b) - P(a) = integral_a^b (R'(x) - C'(x)) dif x",
    'opt': "R'(x) = C'(x) arrow.double.long P_max",
    'growth': "N(T) = N(0) + integral_0^T N'(t) dif t",
    'drug': "integral_0^T r(t) dif t quad (\"mg\"\\/\"h\" times \"h\" = \"mg\")",
    'e1_s1': "integral_100^200 (\"0,3\" x + 20) dif x = \"0,15\" (200^2 - 100^2) + 2000 = gold(6500)",
    'e1_s2': "6500 \"nghìn đồng\" = gold(\"6,5\") \"triệu đồng\"",
    'e2_s1': "P'(x) = (100 - \"0,2\" x) - (20 + \"0,2\" x) = 80 - \"0,4\" x = 0 arrow.double.long x = gold(200)",
    'e3_s1': "integral_100^200 (80 - \"0,4\" x) dif x = 8000 - 6000 = gold(2000) \"nghìn đồng\"",
    'e4_s1': "N(10) = 5000 + integral_0^10 1000 e^(\"0,2\" t) dif t = 5000 e^2 approx gold(36945)",
    'e5_s1': "integral_0^4 20 e^(-\"0,5\" t) dif t = 40(1 - e^(-2)) approx gold(\"34,59\") \"mg\"",
    'e6_s1': "integral_0^10 (2 + \"0,1\" t) dif t = 20 + 5 = gold(25) \"nghìn người\"",
    'cs': "\"CS\" = integral_0^Q (D(x) - P) dif x",
    'cs_ex': "integral_0^80 (40 - \"0,5\" x) dif x = 3200 - 1600 = gold(1600)",
    'inv1': "integral_0^10 (a + \"0,2\" t) dif t = 10a + 10 = 30",
    'inv2': "a = gold(2) quad (\"nghìn người/năm\")",
    'tf_given': "C'(x) = 2x + 50, quad C(0) = 1000",
    'tf_a': "C(x) = x^2 + 50x + 1000",
    'tf_b': "C(10) = 1600",
    'tf_c': "C(20) - C(10) = 400",
    'tf_d': "C'(10) = 70",
    'tf_c_calc': "integral_10^20 (2x + 50) dif x = 300 + 500 = 800 coral(!= 400)",
    'sa_task': "N(0) = 2000, quad N'(t) = 300 sqrt(t)",
    'sa_s1': "N(4) = 2000 + integral_0^4 300 sqrt(t) dif t = 2000 + 200 dot 8 = gold(3600)",
    'sum1': "Q(T) = Q(0) + integral_0^T Q'(t) dif t",
    'sum2': "R' = C' arrow.double.long P_max",
    'sum3': "integral_0^T a e^(k t) dif t",
    'hw1': "C'(x) = \"0,4\" x + 10, quad x: 50 arrow.r 100",
    'hw2': "R' = 60 - \"0,1\" x, quad C' = 20 + \"0,1\" x",
    'hw3': "N(0) = 500, quad N' = 50 e^(\"0,1\" t), quad N(10)",
    'hw_ans1': "2000",
    'hw_ans2': "x = 200",
    'hw_ans3': "500 e",
    'next1': "\"bảng số\" arrow.r f(x) arrow.r integral_a^b f(x) dif x",
}

EXERCISES = (
    ("C'(x) = 0,4x + 10: chi phí tăng thêm từ 50 đến 100 sản phẩm", '2000 (nghìn đồng)'),
    ("R' = 60 − 0,1x, C' = 20 + 0,1x: sản lượng tối ưu", 'x = 200'),
    ("N(0) = 500, N' = 50e^(0,1t): N(10)", '500e ≈ 1359'),
)

TRUE_FALSE = (
    ('C(x) = x² + 50x + 1000', True),
    ('C(10) = 1600', True),
    ('C(20) − C(10) = 400', False),
    ("C'(10) = 70", True),
)

x, t, u = sp.symbols('x t u', real=True)


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
    e1 = I(R(3, 10) * x + 20, (x, 100, 200))
    assert e1 == 6500 == R(15, 100) * (200**2 - 100**2) + 2000
    # e2 / e3
    P1 = (100 - R(2, 10) * x) - (20 + R(2, 10) * x)
    assert sp.expand(P1 - (80 - R(4, 10) * x)) == 0 and sp.solve(P1, x) == [200]
    assert I(P1, (x, 100, 200)) == 2000
    assert I(P1, (x, 200, 250)) < 0
    # e4
    N10 = 5000 + I(1000 * sp.exp(R(1, 5) * t), (t, 0, 10))
    assert sp.simplify(N10 - 5000 * E**2) == 0 and round(float(N10)) == 36945
    # e5
    d = I(20 * sp.exp(-R(1, 2) * t), (t, 0, 4))
    assert sp.simplify(d - 40 * (1 - sp.exp(-2))) == 0 and f'{float(d):.2f}' == '34.59'
    # e6
    assert I(2 + R(1, 10) * t, (t, 0, 10)) == 25
    assert sp.solve(100 - R(1, 2) * x - 60, x) == [80] and I(40 - R(1, 2) * x, (x, 0, 80)) == 1600
    a2 = sp.symbols('a2')
    assert sp.expand(I(a2 + R(1, 5) * t, (t, 0, 10)) - (10 * a2 + 10)) == 0 and sp.solve(10 * a2 + 10 - 30, a2) == [2]
    # true / false
    C = 1000 + I(2 * u + 50, (u, 0, x))
    claims = (sp.expand(C - (x**2 + 50 * x + 1000)) == 0, C.subs(x, 10) == 1600,
              C.subs(x, 20) - C.subs(x, 10) == 400, (2 * x + 50).subs(x, 10) == 70)
    assert C.subs(x, 20) - C.subs(x, 10) == 800 == I(2 * x + 50, (x, 10, 20))
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    sa = 2000 + I(300 * sp.sqrt(t), (t, 0, 4))
    assert sa == 3600
    # exercises
    assert I(R(4, 10) * x + 10, (x, 50, 100)) == 2000
    assert sp.solve((60 - R(1, 10) * x) - (20 + R(1, 10) * x), x) == [200]
    n = 500 + I(50 * sp.exp(R(1, 10) * t), (t, 0, 10))
    assert sp.simplify(n - 500 * E) == 0 and round(float(n)) == 1359
    return True


validate()

"""INT34 – Những bẫy sai kinh điển & kiểm tra bằng máy tính.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT34',
    'number': 34,
    'title': 'Bẫy sai kinh điển & cách kiểm tra',
    'subtitle': 'Phòng khám lỗi sai: tám lỗi hay gặp, kiểm tra bằng đạo hàm và máy tính',
    'next_code': 'INT35',
    'next_title': 'Luyện đề theo cấu trúc thi tốt nghiệp',
}

PARTS = (
    ('hook', 'Mở đầu'),
    ('core', 'Công cụ kiểm tra'),
    ('examples', 'Phòng khám lỗi sai'),
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
         'Một bạn học sinh tính tích phân từ không đến một của hai x nhân x bình phương cộng một, tất cả mũ ba. '
         'Bạn đặt u bằng x bình phương cộng một, rồi ra đáp số một phần tư. Lời giải trông rất gọn. '
         'Nhưng bấm máy tính, kết quả lại là ba phẩy bảy lăm. Lỗi nằm ở đâu? Hôm nay ta mở phòng khám lỗi sai.',
         'Mở đầu: lời giải gọn nhưng sai'),
    Beat('h2', 'hook',
         'Đây là tập ba mươi tư, mở đầu phần tổng ôn: những bẫy sai kinh điển và cách kiểm tra bằng máy tính.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, ba lớp kiểm tra: đạo hàm, máy tính và ước lượng. '
         'Hai, tám lỗi sai hay gặp nhất trong chương nguyên hàm, tích phân. '
         'Ba, cách nhận ra bẫy trong câu đúng sai và câu trả lời ngắn.'),
    # ---------------- PHẦN 1: CÔNG CỤ KIỂM TRA ----------------
    Beat('c1', 'core',
         'Lớp kiểm tra thứ nhất: đạo hàm. F là một nguyên hàm của f khi và chỉ khi F phẩy bằng f. '
         'Vì vậy, mọi kết quả nguyên hàm đều kiểm tra được bằng cách lấy đạo hàm ngược lại. '
         'Ví dụ: đạo hàm của x ln x trừ x bằng ln x cộng một trừ một, đúng bằng ln x.',
         'Lớp 1: kiểm tra bằng đạo hàm'),
    Beat('c2', 'core',
         'Lớp thứ hai: máy tính cầm tay có phím tích phân. Nhập tích phân từ một đến e của ln x, máy cho kết quả bằng một. '
         'Với tích phân xác định, hãy đổi đáp án phân số sang số thập phân rồi so với máy: '
         'mười lăm phần tư bằng ba phẩy bảy lăm, khớp; một phần tư bằng không phẩy hai lăm, không khớp.',
         'Lớp 2: kiểm tra bằng máy tính'),
    Beat('c3', 'core',
         'Lớp thứ ba: ước lượng. Nếu m nhỏ hơn hoặc bằng f, f nhỏ hơn hoặc bằng M trên đoạn a b, '
         'thì tích phân nằm giữa m nhân b trừ a và M nhân b trừ a. '
         'Ví dụ, e mũ x bình phương nằm giữa một và e trên đoạn không một, nên tích phân nằm giữa một và e. '
         'Máy cho khoảng một phẩy bốn sáu, hợp lý.',
         'Lớp 3: ước lượng bằng hình'),
    Beat('c4', 'core',
         'Tóm lại ba lớp kiểm tra. Nguyên hàm: lấy đạo hàm. Tích phân xác định: so với máy tính. '
         'Và luôn hỏi: dấu và độ lớn của kết quả có hợp lý với hình vẽ không? '
         'Bây giờ ta dùng ba lớp này để khám từng lỗi sai.'),
    # ---------------- PHẦN 2: PHÒNG KHÁM LỖI SAI ----------------
    Beat('e1', 'examples',
         'Lỗi một: quên trị tuyệt đối trong logarit. Nguyên hàm của một phần x là ln trị tuyệt đối x cộng C, không phải ln x. '
         'Kiểm tra: tích phân từ trừ hai đến trừ một của một phần x bằng trừ ln hai, khoảng trừ không phẩy sáu chín. '
         'Nếu viết ln x, ta không thể thay số âm vào.',
         'Lỗi 1: quên trị tuyệt đối'),
    Beat('e2', 'examples',
         'Lỗi hai: coi nguyên hàm của tích là tích các nguyên hàm. Nguyên hàm của x e mũ x không phải x bình phương trên hai nhân e mũ x. '
         'Lấy đạo hàm thử là thấy ngay thừa một số hạng. Đúng phải dùng từng phần: x trừ một, nhân e mũ x, cộng C.',
         'Lỗi 2: nguyên hàm của tích'),
    Beat('e3', 'examples',
         'Lỗi ba: quên chia cho hệ số a khi nguyên hàm f của a x cộng b. '
         'Nguyên hàm của hai x cộng một, mũ năm, bằng hai x cộng một mũ sáu, chia mười hai, chứ không phải chia sáu. '
         'Đạo hàm lại: sáu nhân hai, chia mười hai, đúng bằng một.',
         'Lỗi 3: quên chia hệ số'),
    Beat('e4', 'examples',
         'Lỗi bốn: sai dấu với hàm lượng giác. Đạo hàm của cos là trừ sin, nên nguyên hàm của sin hai x '
         'là trừ một phần hai cos hai x cộng C. Quên dấu trừ là lỗi rất phổ biến, và đạo hàm lại sẽ phát hiện ngay.',
         'Lỗi 4: sai dấu lượng giác'),
    Beat('e5', 'examples',
         'Lỗi năm, chính là bài mở đầu: đổi biến nhưng quên đổi cận. Khi x đi từ không đến một, '
         'u bằng x bình phương cộng một đi từ một đến hai. Tích phân từ một đến hai của u mũ ba bằng mười lăm phần tư, '
         'đúng bằng ba phẩy bảy lăm như máy tính.',
         'Lỗi 5: đổi biến quên đổi cận'),
    Beat('e6', 'examples',
         'Lỗi sáu: tính diện tích nhưng quên trị tuyệt đối. Với y bằng x bình phương trừ một trên đoạn không hai, '
         'tích phân bằng hai phần ba, vì phần âm đã triệt tiêu một phần diện tích. '
         'Phải tách tại nghiệm x bằng một: hai phần ba cộng bốn phần ba, diện tích bằng hai.',
         'Lỗi 6: diện tích quên trị tuyệt đối'),
    Beat('e7', 'examples',
         'Lỗi bảy: thể tích vành khăn. Quay miền giữa y bằng hai và y bằng x trên đoạn không một quanh trục hoành. '
         'Sai khi viết pi nhân tích phân của hiệu, bình phương. Đúng là pi nhân tích phân của hiệu các bình phương: '
         'bốn trừ x bình phương, được mười một pi phần ba.',
         'Lỗi 7: bình phương của hiệu'),
    Beat('e8', 'examples',
         'Lỗi tám: nhầm độ dời với quãng đường. Vận tốc v bằng t trừ hai trên đoạn không bốn: '
         'tích phân của v bằng không, đó là độ dời, vật quay về chỗ cũ. '
         'Nhưng quãng đường là tích phân của trị tuyệt đối v, bằng hai cộng hai, bằng bốn mét.',
         'Lỗi 8: độ dời và quãng đường'),
    Beat('e9', 'examples',
         'Trước khi nộp bài, hãy rà nhanh danh sách tám điểm: trị tuyệt đối trong ln, nguyên hàm của tích, chia hệ số, '
         'dấu lượng giác, đổi cận, trị tuyệt đối trong diện tích, bình phương trong thể tích, và quãng đường. '
         'Mỗi điểm chỉ mất vài giây, nhưng giữ lại rất nhiều điểm số.',
         'Danh sách kiểm tra'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu trắc nghiệm: tích phân từ không đến pi của sin x bằng bao nhiêu? '
         'Bốn phương án: không, trừ hai, hai và một. Hai phương án sai được dựng từ đúng các lỗi ta vừa học. '
         'Em hãy tạm dừng và chọn.',
         'Câu trắc nghiệm'),
    Beat('x2', 'exam',
         'Đáp án C. Nguyên hàm của sin x là trừ cos x, nên kết quả bằng trừ cos pi cộng cos không, bằng hai. '
         'Ai quên dấu trừ sẽ ra trừ hai; ai nghĩ diện tích hai phía triệt tiêu sẽ chọn không. '
         'Máy tính cũng cho đúng bằng hai.'),
    Beat('x3', 'exam',
         'Câu hỏi đúng sai: mỗi mệnh đề có thể chứa một bẫy. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x4', 'exam',
         'Ý a sai: thiếu hệ số một phần hai, đạo hàm của ln trị tuyệt đối hai x cộng một là hai chia hai x cộng một. '
         'Ý b đúng: tích phân từ không đến pi phần hai của cos x bằng sin pi phần hai trừ sin không, bằng một.'),
    Beat('x5', 'exam',
         'Ý c sai: đường thẳng y bằng x trừ một đổi dấu tại x bằng một, tích phân bằng không nhưng diện tích bằng một. '
         'Ý d đúng: vành khăn bán kính ngoài hai, bán kính trong một, thể tích bằng pi nhân bốn trừ một nhân ba, bằng chín pi.'),
    Beat('x6', 'exam',
         'Câu trả lời ngắn: một vật chuyển động với vận tốc v bằng t bình phương trừ bốn t cộng ba mét trên giây. '
         'Tính quãng đường vật đi được trong ba giây đầu, làm tròn đến hàng phần trăm. '
         'Cẩn thận: vận tốc đổi dấu.',
         'Câu trả lời ngắn'),
    Beat('x7', 'exam',
         'Vận tốc bằng không tại t bằng một và t bằng ba. Tích phân từ không đến một bằng bốn phần ba, '
         'tích phân từ một đến ba bằng trừ bốn phần ba. Độ dời bằng không, nhưng quãng đường bằng tám phần ba, '
         'khoảng hai phẩy sáu bảy mét. Ghi vào phiếu: hai, phẩy, sáu, bảy.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, nguyên hàm luôn kiểm tra được bằng đạo hàm. Hai, tích phân xác định kiểm tra bằng máy tính, '
         'đổi đáp án sang số thập phân để so. Ba, tám lỗi kinh điển xoay quanh dấu, hệ số, cận và trị tuyệt đối.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tích phân từ không đến một của ba x cộng một, bình phương. '
         'Hai, diện tích giữa y bằng x bình phương trừ x và trục hoành trên đoạn không hai. '
         'Ba, quãng đường với v bằng hai t trừ bốn trên đoạn không ba. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Tập sau, ta luyện một đề theo đúng cấu trúc thi tốt nghiệp: trắc nghiệm, đúng sai và trả lời ngắn, '
         'có đồng hồ đếm giờ và lời giải nhanh. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'h1_wrong': "integral_0^1 2x (x^2 + 1)^3 dif x = [u^4/4]_0^1 = 1/4",
    'h1_expr': "integral_0^1 2x (x^2 + 1)^3 dif x",
    'c1_rule': "integral f(x) dif x = F(x) + C quad arrow.l.r.double quad F'(x) = f(x)",
    'c1_ex': "(x ln x - x)' = ln x + 1 - 1 = ln x quad green(checkmark)",
    'c2_expr': "integral_1^e ln x dif x",
    'c2_cmp': "15/4 = \"3,75\" quad green(checkmark) wide 1/4 = \"0,25\" quad coral(times)",
    'c3_bound': "m <= f <= M quad arrow.r.double quad m(b - a) <= integral_a^b f(x) dif x <= M(b - a)",
    'c3_ex': "1 <= integral_0^1 e^(x^2) dif x <= e",
    'c3_expr': "integral_0^1 e^(x^2) dif x",
    'k1': "F'(x) = f(x)",
    'k2': "integral_a^b f(x) dif x approx \"máy\"",
    'k3': "m(b - a) <= I <= M(b - a)",
    'e1_wrong': "integral 1/x dif x = ln x + C",
    'e1_right': "integral 1/x dif x = ln abs(x) + C",
    'e1_check': "integral_(-2)^(-1) 1/x dif x = -ln 2 approx -\"0,69\"",
    'e2_wrong': "integral x e^x dif x = x^2/2 e^x + C",
    'e2_right': "integral x e^x dif x = (x - 1) e^x + C",
    'e2_check': "((x - 1) e^x)' = e^x + (x - 1) e^x = x e^x quad green(checkmark)",
    'e3_wrong': "integral (2x + 1)^5 dif x = (2x + 1)^6/6 + C",
    'e3_right': "integral (2x + 1)^5 dif x = (2x + 1)^6/12 + C",
    'e3_check': "((2x + 1)^6/12)' = (6 dot 2)/12 (2x + 1)^5 = (2x + 1)^5 quad green(checkmark)",
    'e4_wrong': "integral sin 2x dif x = 1/2 cos 2x + C",
    'e4_right': "integral sin 2x dif x = -1/2 cos 2x + C",
    'e4_check': "(-1/2 cos 2x)' = -1/2 dot (-2 sin 2x) = sin 2x quad green(checkmark)",
    'e5_wrong': "u = x^2 + 1: quad integral_0^1 u^3 dif u = 1/4",
    'e5_right': "u = x^2 + 1: quad integral_1^2 u^3 dif u = 15/4",
    'e5_check': "x: 0 arrow.r 1 quad arrow.r.double quad u: 1 arrow.r 2",
    'e6_wrong': "S = integral_0^2 (x^2 - 1) dif x = 2/3",
    'e6_right': "S = integral_0^1 (1 - x^2) dif x + integral_1^2 (x^2 - 1) dif x = 2/3 + 4/3 = 2",
    'e6_check': "integral_0^2 abs(x^2 - 1) dif x = 2",
    'e7_wrong': "V = pi integral_0^1 (2 - x)^2 dif x = (7 pi)/3",
    'e7_right': "V = pi integral_0^1 (2^2 - x^2) dif x = (11 pi)/3",
    'e7_check': "R^2 - r^2 coral(!=) (R - r)^2",
    'e8_wrong': "s = integral_0^4 (t - 2) dif t = 0",
    'e8_right': "s = integral_0^4 abs(t - 2) dif t = 2 + 2 = 4",
    'e8_check': "integral v = \"độ dời\", quad integral abs(v) = \"quãng đường\"",
    'mc_q': "integral_0^pi sin x dif x = ?",
    'mc_a': "0",
    'mc_b': "-2",
    'mc_c': "2",
    'mc_d': "1",
    'mc_sol': "[-cos x]_0^pi = -cos pi + cos 0 = 1 + 1 = gold(2)",
    'tf_a': "integral 1/(2x + 1) dif x = ln abs(2x + 1) + C",
    'tf_b': "integral_0^(pi\\/2) cos x dif x = 1",
    'tf_c': "S_(y = x - 1, thin x in [0; 2]) = integral_0^2 (x - 1) dif x",
    'tf_d': "V_(1 <= y <= 2, thin x in [0; 3]) = pi integral_0^3 (4 - 1) dif x = 9 pi",
    'sa_task': "v(t) = t^2 - 4t + 3 thin (\"m/s\"), quad t in [0; 3]",
    'sa_s1': "v = 0 arrow.l.r.double t = 1 \" hoặc \" t = 3",
    'sa_s2': "s = abs(integral_0^1 v dif t) + abs(integral_1^3 v dif t) = 4/3 + 4/3 = 8/3 approx gold(\"2,67\")",
    'sum1': "F' = f",
    'sum2': "15/4 = \"3,75\"",
    'sum3': "abs(x), quad 1/a, quad -cos",
    'hw1': "integral_0^1 (3x + 1)^2 dif x",
    'hw2': "y = x^2 - x, quad x in [0; 2]",
    'hw3': "v = 2t - 4, quad t in [0; 3]",
    'hw_ans1': "7",
    'hw_ans2': "1",
    'hw_ans3': "5 \"m\"",
    'next1': "12 \"trắc nghiệm\" + 4 \"đúng/sai\" + 6 \"trả lời ngắn\"",
}

CHECKLIST = (
    ('ln', "ln abs(x)"),
    ('tích', "integral f g != integral f dot integral g"),
    ('hệ số', "1/a F(a x + b)"),
    ('dấu', "integral sin = -cos"),
    ('cận', "x arrow.r u"),
    ('diện tích', "abs(f)"),
    ('thể tích', "R^2 - r^2"),
    ('quãng đường', "abs(v)"),
)
FORMULAS.update({f'ck{i}': f for i, (_, f) in enumerate(CHECKLIST)})

EXERCISES = (
    ('∫₀¹ (3x + 1)² dx', '7'),
    ('Diện tích giữa y = x² − x và Ox trên [0; 2]', '1'),
    ('Quãng đường với v = 2t − 4 trên [0; 3]', '5 m'),
)

TRUE_FALSE = (
    ('∫ 1/(2x + 1) dx = ln|2x + 1| + C', False),
    ('∫₀^{π/2} cos x dx = 1', True),
    ('Diện tích y = x − 1, x ∈ [0; 2] bằng ∫₀² (x − 1) dx', False),
    ('Thể tích vành khăn 1 ≤ y ≤ 2, x ∈ [0; 3] bằng 9π', True),
)

MC = (('mc_q', ('mc_a', 'mc_b', 'mc_c', 'mc_d'), 2, 'mc_sol'),)
SHORT = (('sa_task', '2,67'),)

x, t, u = sp.symbols('x t u', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, d = sp.integrate, sp.Rational, sp.diff
    pi = sp.pi
    # hook / lỗi 5
    good = I(2 * x * (x**2 + 1)**3, (x, 0, 1))
    assert good == R(15, 4) and I(u**3, (u, 1, 2)) == good and I(u**3, (u, 0, 1)) == R(1, 4)
    # tools
    assert sp.simplify(d(x * sp.log(x) - x, x) - sp.log(x)) == 0
    assert I(sp.log(x), (x, 1, sp.E)) == 1
    val = float(sp.Integral(sp.exp(x**2), (x, 0, 1)).evalf())
    assert 1 < val < float(sp.E) and f'{val:.2f}' == '1.46'
    # lỗi 1–4
    assert sp.simplify(I(1 / x, (x, -2, -1)) + sp.log(2)) == 0 and f'{float(-sp.log(2)):.2f}' == '-0.69'
    assert sp.simplify(d(x**2 / 2 * sp.exp(x), x) - x * sp.exp(x)) != 0
    assert sp.simplify(d((x - 1) * sp.exp(x), x) - x * sp.exp(x)) == 0
    assert sp.expand(d((2 * x + 1)**6 / 12, x) - (2 * x + 1)**5) == 0
    assert sp.expand(d((2 * x + 1)**6 / 6, x) - (2 * x + 1)**5) != 0
    assert sp.simplify(d(-sp.cos(2 * x) / 2, x) - sp.sin(2 * x)) == 0
    # lỗi 6
    assert I(x**2 - 1, (x, 0, 2)) == R(2, 3)
    assert I(1 - x**2, (x, 0, 1)) == R(2, 3) and I(x**2 - 1, (x, 1, 2)) == R(4, 3)
    # lỗi 7
    assert pi * I((2 - x)**2, (x, 0, 1)) == 7 * pi / 3 and pi * I(4 - x**2, (x, 0, 1)) == 11 * pi / 3
    # lỗi 8
    assert I(t - 2, (t, 0, 4)) == 0 and I(2 - t, (t, 0, 2)) + I(t - 2, (t, 2, 4)) == 4
    # trắc nghiệm
    assert I(sp.sin(x), (x, 0, pi)) == 2 and 'ABCD'[MC[0][2]] == 'C'
    # đúng / sai
    claims = (sp.simplify(d(sp.log(2 * x + 1), x) - 1 / (2 * x + 1)) == 0,
              I(sp.cos(x), (x, 0, pi / 2)) == 1,
              I(x - 1, (x, 0, 2)) == I(1 - x, (x, 0, 1)) + I(x - 1, (x, 1, 2)),
              pi * I(4 - 1, (x, 0, 3)) == 9 * pi)
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # trả lời ngắn
    v = t**2 - 4 * t + 3
    assert sp.solve(v, t) == [1, 3]
    assert I(v, (t, 0, 1)) == R(4, 3) and I(v, (t, 1, 3)) == -R(4, 3) and I(v, (t, 0, 3)) == 0
    assert f'{8 / 3:.2f}' == '2.67'
    # bài tập
    assert I((3 * x + 1)**2, (x, 0, 1)) == 7
    assert I(x - x**2, (x, 0, 1)) + I(x**2 - x, (x, 1, 2)) == 1
    assert I(4 - 2 * t, (t, 0, 2)) + I(2 * t - 4, (t, 2, 3)) == 5
    return True


validate()

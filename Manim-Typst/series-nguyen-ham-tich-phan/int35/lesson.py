"""INT35 – Luyện đề theo cấu trúc thi tốt nghiệp: 12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every answer of the test with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT35',
    'number': 35,
    'title': 'Luyện đề theo cấu trúc thi tốt nghiệp',
    'subtitle': '12 trắc nghiệm, 4 đúng/sai, 6 trả lời ngắn: toàn chương nguyên hàm – tích phân',
    'next_code': 'INT36',
    'next_title': 'Bản đồ tư duy toàn chương',
}

PARTS = (
    ('hook', 'Mở đầu'),
    ('mc', 'Trắc nghiệm'),
    ('tf', 'Đúng/Sai'),
    ('short', 'Trả lời ngắn'),
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
         'Đề thi tốt nghiệp môn Toán theo cấu trúc mới gồm ba phần: mười hai câu trắc nghiệm, '
         'bốn câu đúng sai, mỗi câu bốn ý, và sáu câu trả lời ngắn. Hôm nay ta luyện trọn một đề cùng cấu trúc, '
         'toàn bộ về nguyên hàm, tích phân và ứng dụng. Chuẩn bị giấy nháp và máy tính nhé.',
         'Mở đầu: một đề, ba phần'),
    Beat('h2', 'hook',
         'Đây là tập ba mươi lăm: luyện đề theo cấu trúc thi tốt nghiệp.'),
    Beat('h3', 'hook',
         'Cách tính điểm và phân bổ thời gian. Phần một: mỗi câu không phẩy hai lăm điểm, làm khoảng một phút một câu. '
         'Phần hai: mỗi câu tối đa một điểm, đúng một ý được không phẩy một, hai ý không phẩy hai lăm, ba ý không phẩy năm, '
         'đủ bốn ý được một điểm. Phần ba: mỗi câu không phẩy năm điểm. Đồng hồ ở góc màn hình nhắc em giữ nhịp.',
         'Cách tính điểm và thời gian'),
    # ---------------- PHẦN I: TRẮC NGHIỆM ----------------
    Beat('q1', 'mc',
         'Câu một: nguyên hàm của ba x bình phương cộng hai. '
         'Đáp án A: x lập phương cộng hai x cộng C. Đạo hàm lại đúng bằng ba x bình phương cộng hai.',
         'Phần I: 12 câu trắc nghiệm'),
    Beat('q2', 'mc',
         'Câu hai: nguyên hàm của e mũ ba x. Nhớ chia cho hệ số ba. '
         'Đáp án B: một phần ba e mũ ba x cộng C.'),
    Beat('q3', 'mc',
         'Câu ba: F là nguyên hàm của một phần x trên khoảng không đến dương vô cùng, và F của một bằng hai. Tính F của e. '
         'F bằng ln x cộng hai, nên F của e bằng ba. Đáp án C.'),
    Beat('q4', 'mc',
         'Câu bốn: nguyên hàm của cos hai x. Nguyên hàm của cos là sin, rồi chia cho hai. '
         'Đáp án D: một phần hai sin hai x cộng C. Phương án A sai dấu, một bẫy quen thuộc.'),
    Beat('q5', 'mc',
         'Câu năm: tích phân từ một đến hai của hai x cộng một. '
         'Nguyên hàm x bình phương cộng x, thay cận: sáu trừ hai bằng bốn. Đáp án B.'),
    Beat('q6', 'mc',
         'Câu sáu: tích phân từ không đến hai của f bằng ba, từ hai đến năm bằng trừ một. '
         'Cộng hai đoạn liền nhau: ba cộng trừ một bằng hai. Đáp án C. Phương án A là bẫy trừ thay vì cộng.'),
    Beat('q7', 'mc',
         'Câu bảy: tích phân từ không đến pi của x sin x. Dùng từng phần với u bằng x: '
         'trừ x cos x cộng sin x, thay cận được pi. Đáp án A.'),
    Beat('q8', 'mc',
         'Câu tám: tích phân từ không đến một của x chia x bình phương cộng một. Đặt u bằng x bình phương cộng một, '
         'u đi từ một đến hai, được một phần hai ln hai. Đáp án B.'),
    Beat('q9', 'mc',
         'Câu chín: diện tích giữa y bằng x bình phương và y bằng x. Hai đường cắt nhau tại không và một, '
         'trên đoạn đó x lớn hơn x bình phương: tích phân của x trừ x bình phương bằng một phần sáu. Đáp án D.',
         'Trắc nghiệm: ứng dụng'),
    Beat('q10', 'mc',
         'Câu mười: diện tích giữa y bằng x lập phương, trục hoành, x bằng trừ một và x bằng một. '
         'Tích phân bằng không vì hai phần đối xứng triệt tiêu, nhưng diện tích bằng hai lần một phần tư, '
         'bằng một phần hai. Đáp án C.'),
    Beat('q11', 'mc',
         'Câu mười một: quay miền dưới y bằng căn x, x từ không đến bốn, quanh trục hoành. '
         'Thể tích bằng pi nhân tích phân của x, bằng tám pi. Đáp án A.'),
    Beat('q12', 'mc',
         'Câu mười hai: vận tốc v bằng ba t bình phương mét trên giây. Quãng đường từ t bằng một đến t bằng hai '
         'bằng tích phân của ba t bình phương, bằng tám trừ một, bằng bảy mét. Đáp án B.'),
    # ---------------- PHẦN II: ĐÚNG / SAI ----------------
    Beat('d1', 'tf',
         'Phần hai, câu một. F là nguyên hàm của e mũ x cộng hai x, với F của không bằng ba. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Phần II: 4 câu đúng/sai'),
    Beat('d2', 'tf',
         'Ý a đúng: F bằng e mũ x cộng x bình phương cộng C, thay x bằng không được C bằng hai. Ý b đúng: F của một bằng e cộng ba. '
         'Ý c sai: tích phân bằng F một trừ F không, bằng e, không phải e cộng một. '
         'Ý d sai: tại x bằng trừ một, F phẩy âm, nên F không đồng biến trên R.'),
    Beat('d3', 'tf',
         'Câu hai: f liên tục và tích phân từ không đến hai của f bằng bốn. Xét bốn mệnh đề.'),
    Beat('d4', 'tf',
         'Ý a đúng: hằng số đưa ra ngoài, được tám. Ý b đúng: đặt u bằng hai x, được một phần hai nhân bốn, bằng hai. '
         'Ý c sai: tích phân của x từ không đến hai bằng hai, tổng là sáu. '
         'Ý d đúng: đổi biến u bằng hai trừ x, tích phân giữ nguyên bằng bốn.'),
    Beat('d5', 'tf',
         'Câu ba: hình phẳng giới hạn bởi y bằng x bình phương trừ hai x và y bằng x. Xét bốn mệnh đề.'),
    Beat('d6', 'tf',
         'Ý a đúng: phương trình hoành độ giao điểm cho x bằng không hoặc x bằng ba. '
         'Ý b sai: trên khoảng không ba, x lớn hơn x bình phương trừ hai x. Ý c đúng: tích phân của ba x trừ x bình phương bằng chín phần hai. '
         'Ý d đúng: hiệu không đổi dấu trên khoảng đó, nên lấy trị tuyệt đối ngoài tích phân cũng được.'),
    Beat('d7', 'tf',
         'Câu bốn: một vật chuyển động với vận tốc v bằng mười hai trừ ba t mét trên giây. Xét bốn mệnh đề.'),
    Beat('d8', 'tf',
         'Ý a đúng: v bằng không khi t bằng bốn. Ý b đúng: quãng đường đến khi dừng bằng hai mươi tư mét. '
         'Ý c đúng: độ dời trong sáu giây đầu bằng mười tám mét. '
         'Ý d sai: quãng đường trong sáu giây là hai mươi tư cộng sáu, bằng ba mươi mét, vì vật đã quay đầu.'),
    # ---------------- PHẦN III: TRẢ LỜI NGẮN ----------------
    Beat('t1', 'short',
         'Phần ba, câu một: F là nguyên hàm của bốn x mũ ba trừ hai x, F của một bằng ba. Tính F của hai. '
         'F bằng x mũ bốn trừ x bình phương cộng C, C bằng ba, nên F của hai bằng mười lăm.',
         'Phần III: 6 câu trả lời ngắn'),
    Beat('t2', 'short',
         'Câu hai: tích phân từ không đến pi phần hai của sin bình phương x, làm tròn đến hàng phần trăm. '
         'Hạ bậc: sin bình phương bằng một trừ cos hai x, chia hai. Kết quả pi phần tư, khoảng không phẩy bảy chín.'),
    Beat('t3', 'short',
         'Câu ba: tích phân từ một đến e của ln x chia x. Đặt u bằng ln x, u đi từ không đến một, '
         'được một phần hai. Ghi không phẩy năm.'),
    Beat('t4', 'short',
         'Câu bốn: diện tích giới hạn bởi y bằng e mũ x, y bằng một và x bằng một. '
         'Tích phân từ không đến một của e mũ x trừ một bằng e trừ hai, khoảng không phẩy bảy hai.'),
    Beat('t5', 'short',
         'Câu năm: quay miền giữa y bằng hai x trừ x bình phương và trục hoành quanh trục hoành. '
         'Thể tích bằng pi nhân tích phân từ không đến hai của bình phương, bằng mười sáu pi phần mười lăm, khoảng ba phẩy ba lăm.'),
    Beat('t6', 'short',
         'Câu sáu: nước chảy vào bể với lưu lượng hai mươi cộng sáu t lít mỗi phút. '
         'Lượng nước vào bể trong mười phút bằng hai trăm cộng ba trăm, bằng năm trăm lít.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Đây là bảng đáp án đầy đủ. Phần một: A, B, C, D, B, C, A, B, D, C, A, B. '
         'Phần hai: đúng đúng sai sai, đúng đúng sai đúng, đúng sai đúng đúng, đúng đúng đúng sai. '
         'Phần ba: mười lăm, không phẩy bảy chín, không phẩy năm, không phẩy bảy hai, ba phẩy ba lăm, năm trăm.',
         'Bảng đáp án và tự chấm điểm'),
    Beat('o2', 'outro',
         'Tự chấm điểm: phần một tối đa ba điểm, phần hai bốn điểm, phần ba ba điểm. '
         'Câu sai nào rơi vào tám bẫy của tập trước, hãy ghi lại vào sổ lỗi sai để không lặp lại lần sau.'),
    Beat('o3', 'outro',
         'Tập cuối cùng, ta vẽ bản đồ tư duy toàn chương và lộ trình chinh phục tám điểm, chín điểm. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

# (question key, option keys A–D, correct index, solution key)
MC = tuple((f'q{n}', tuple(f'q{n}{c}' for c in 'abcd'), 'ABCD'.index(k), f'q{n}_s')
           for n, k in enumerate('ABCDBCABDCAB', 1))

FORMULAS = {
    'q1': "integral (3x^2 + 2) dif x = ?",
    'q1a': "x^3 + 2x + C", 'q1b': "6x + C", 'q1c': "x^3 + C", 'q1d': "3x^3 + 2x + C",
    'q1_s': "(x^3 + 2x)' = 3x^2 + 2",
    'q2': "integral e^(3x) dif x = ?",
    'q2a': "3 e^(3x) + C", 'q2b': "1/3 e^(3x) + C", 'q2c': "e^(3x) + C", 'q2d': "e^(3x + 1)/(3x + 1) + C",
    'q2_s': "(1/3 e^(3x))' = 1/3 dot 3 e^(3x) = e^(3x)",
    'q3': "F' = 1/x \" trên \" (0; +infinity), quad F(1) = 2, quad F(e) = ?",
    'q3a': "2", 'q3b': "e", 'q3c': "3", 'q3d': "1",
    'q3_s': "F(x) = ln x + 2 arrow.r.double F(e) = 1 + 2 = 3",
    'q4': "integral cos 2x dif x = ?",
    'q4a': "-1/2 sin 2x + C", 'q4b': "2 sin 2x + C", 'q4c': "sin 2x + C", 'q4d': "1/2 sin 2x + C",
    'q4_s': "(1/2 sin 2x)' = 1/2 dot 2 cos 2x = cos 2x",
    'q5': "integral_1^2 (2x + 1) dif x = ?",
    'q5a': "3", 'q5b': "4", 'q5c': "5", 'q5d': "6",
    'q5_s': "[x^2 + x]_1^2 = 6 - 2 = 4",
    'q6': "integral_0^2 f = 3, quad integral_2^5 f = -1, quad integral_0^5 f = ?",
    'q6a': "4", 'q6b': "-3", 'q6c': "2", 'q6d': "-2",
    'q6_s': "integral_0^5 f = integral_0^2 f + integral_2^5 f = 3 + (-1) = 2",
    'q7': "integral_0^pi x sin x dif x = ?",
    'q7a': "pi", 'q7b': "2 pi", 'q7c': "0", 'q7d': "-pi",
    'q7_s': "[-x cos x + sin x]_0^pi = pi",
    'q8': "integral_0^1 x/(x^2 + 1) dif x = ?",
    'q8a': "ln 2", 'q8b': "1/2 ln 2", 'q8c': "2 ln 2", 'q8d': "ln 2 - 1",
    'q8_s': "u = x^2 + 1: quad 1/2 integral_1^2 (dif u)/u = 1/2 ln 2",
    'q9': "S_(y = x^2, thin y = x) = ?",
    'q9a': "1/2", 'q9b': "1/3", 'q9c': "5/6", 'q9d': "1/6",
    'q9_s': "integral_0^1 (x - x^2) dif x = 1/2 - 1/3 = 1/6",
    'q10': "S_(y = x^3, thin y = 0, thin x = -1, thin x = 1) = ?",
    'q10a': "0", 'q10b': "1/4", 'q10c': "1/2", 'q10d': "1",
    'q10_s': "integral_(-1)^1 abs(x^3) dif x = 2 dot 1/4 = 1/2",
    'q11': "V_(y = sqrt(x), thin x in [0; 4]) = ?",
    'q11a': "8 pi", 'q11b': "16 pi", 'q11c': "4 pi", 'q11d': "8",
    'q11_s': "pi integral_0^4 x dif x = pi dot 8 = 8 pi",
    'q12': "v = 3t^2 thin (\"m/s\"), quad s_([1; 2]) = ?",
    'q12a': "3", 'q12b': "7", 'q12c': "9", 'q12d': "12",
    'q12_s': "integral_1^2 3t^2 dif t = 8 - 1 = 7 thin \"m\"",
    # Phần II
    'd1_given': "F' = e^x + 2x, quad F(0) = 3",
    'd1a': "F(x) = e^x + x^2 + 2", 'd1b': "F(1) = e + 3",
    'd1c': "integral_0^1 (e^x + 2x) dif x = e + 1", 'd1d': "F \" đồng biến trên \" RR",
    'd2_given': "integral_0^2 f(x) dif x = 4",
    'd2a': "integral_0^2 2 f(x) dif x = 8", 'd2b': "integral_0^1 f(2x) dif x = 2",
    'd2c': "integral_0^2 (f(x) + x) dif x = 5", 'd2d': "integral_0^2 f(2 - x) dif x = 4",
    'd3_given': "y = x^2 - 2x, quad y = x",
    'd3a': "\"giao tại \" x = 0, thin x = 3", 'd3b': "x^2 - 2x > x \" trên \" (0; 3)",
    'd3c': "S = 9/2", 'd3d': "S = abs(integral_0^3 (x^2 - 3x) dif x)",
    'd4_given': "v(t) = 12 - 3t thin (\"m/s\")",
    'd4a': "v(4) = 0", 'd4b': "s_([0; 4]) = 24 thin \"m\"",
    'd4c': "integral_0^6 v(t) dif t = 18", 'd4d': "s_([0; 6]) = 18 thin \"m\"",
    # Phần III
    't1': "F' = 4x^3 - 2x, quad F(1) = 3, quad F(2) = ?",
    't1_s': "F = x^4 - x^2 + 3 arrow.r.double F(2) = 16 - 4 + 3 = gold(15)",
    't2': "integral_0^(pi\\/2) sin^2 x dif x approx ?",
    't2_s': "integral_0^(pi\\/2) (1 - cos 2x)/2 dif x = pi/4 approx gold(\"0,79\")",
    't3': "integral_1^e (ln x)/x dif x = ?",
    't3_s': "u = ln x: quad integral_0^1 u dif u = gold(1/2)",
    't4': "S_(y = e^x, thin y = 1, thin x = 1) approx ?",
    't4_s': "integral_0^1 (e^x - 1) dif x = e - 2 approx gold(\"0,72\")",
    't5': "V_(y = 2x - x^2, thin y = 0) approx ?",
    't5_s': "pi integral_0^2 (2x - x^2)^2 dif x = (16 pi)/15 approx gold(\"3,35\")",
    't6': "r(t) = 20 + 6t thin (\"L/phút\"), quad t in [0; 10]",
    't6_s': "integral_0^10 (20 + 6t) dif t = 200 + 300 = gold(500) thin \"L\"",
    # Mở đầu / tổng kết
    'score1': "12 times \"0,25\" = 3",
    'score2': "4 times 1 = 4",
    'score3': "6 times \"0,5\" = 3",
    'tf_rule': "1 \" ý\" arrow.r \"0,1\", quad 2 \" ý\" arrow.r \"0,25\", quad 3 \" ý\" arrow.r \"0,5\", quad 4 \" ý\" arrow.r 1",
    'next1': "\"nguyên hàm\" arrow.r \"tích phân\" arrow.r \"ứng dụng\"",
}

TF_KEYS = ('ĐĐSS', 'ĐĐSĐ', 'ĐSĐĐ', 'ĐĐĐS')
SHORT = (('t1', '15'), ('t2', '0,79'), ('t3', '0,5'), ('t4', '0,72'), ('t5', '3,35'), ('t6', '500'))

EXERCISES = tuple([(f'Câu {n} (trắc nghiệm)', 'ABCD'[k]) for n, (_, _, k, _) in enumerate(MC, 1)]
                  + [(f'Câu {n} (đúng/sai)', ' '.join(key)) for n, key in enumerate(TF_KEYS, 1)]
                  + [(f'Câu {n} (trả lời ngắn)', v) for n, (_, v) in enumerate(SHORT, 1)])

TRUE_FALSE = (
    ('F(x) = eˣ + x² + 2', True),
    ('F(1) = e + 3', True),
    ('∫₀¹ (eˣ + 2x) dx = e + 1', False),
    ('F đồng biến trên ℝ', False),
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

    I, R, d, pi, E = sp.integrate, sp.Rational, sp.diff, sp.pi, sp.E
    same = lambda a, b: sp.simplify(a - b) == 0  # noqa: E731
    # Phần I – check that the marked option is the right one (and only that one for the numeric ones)
    assert same(d(x**3 + 2 * x, x), 3 * x**2 + 2) and not same(d(3 * x**3 + 2 * x, x), 3 * x**2 + 2)
    assert same(d(sp.exp(3 * x) / 3, x), sp.exp(3 * x)) and not same(d(sp.exp(3 * x), x), sp.exp(3 * x))
    assert sp.log(E) + 2 == 3
    assert same(d(sp.sin(2 * x) / 2, x), sp.cos(2 * x)) and not same(d(-sp.sin(2 * x) / 2, x), sp.cos(2 * x))
    numeric = (I(2 * x + 1, (x, 1, 2)), 3 + (-1), I(x * sp.sin(x), (x, 0, pi)), I(x / (x**2 + 1), (x, 0, 1)),
               I(x - x**2, (x, 0, 1)), I(sp.Abs(x**3), (x, -1, 0)) * 2, pi * I(x, (x, 0, 4)), I(3 * t**2, (t, 1, 2)))
    options = {5: (3, 4, 5, 6), 6: (4, -3, 2, -2), 7: (pi, 2 * pi, 0, -pi), 8: (sp.log(2), sp.log(2) / 2, 2 * sp.log(2),
               sp.log(2) - 1), 9: (R(1, 2), R(1, 3), R(5, 6), R(1, 6)), 10: (0, R(1, 4), R(1, 2), 1),
               11: (8 * pi, 16 * pi, 4 * pi, 8), 12: (3, 7, 9, 12)}
    for (n, opts), val in zip(options.items(), numeric):
        hits = [k for k, o in enumerate(opts) if same(o, val)]
        assert hits == [MC[n - 1][2]], (n, hits)
    assert I(x**3, (x, -1, 1)) == 0   # the trap in câu 10
    assert ''.join('ABCD'[k] for _, _, k, _ in MC) == 'ABCDBCABDCAB'
    # Phần II
    F = sp.exp(x) + x**2 + 2
    assert same(d(F, x), sp.exp(x) + 2 * x) and F.subs(x, 0) == 3
    c1 = (True, same(F.subs(x, 1), E + 3), same(I(sp.exp(x) + 2 * x, (x, 0, 1)), E + 1),
          bool(sp.exp(-1) - 2 > 0))
    assert c1 == tuple(a for _, a in TRUE_FALSE) and ''.join('Đ' if c else 'S' for c in c1) == TF_KEYS[0]
    # ∫₀² f = 4: linear facts and two substitutions (checked on a sample f with that integral)
    g = 3 * x**2 / 2 - 2 * x + 2
    assert I(g, (x, 0, 2)) == 4
    c2 = (I(2 * g, (x, 0, 2)) == 8, I(g.subs(x, 2 * x), (x, 0, 1)) == 2, I(g + x, (x, 0, 2)) == 5,
          I(g.subs(x, 2 - x), (x, 0, 2)) == 4)
    assert ''.join('Đ' if c else 'S' for c in c2) == TF_KEYS[1]
    h = x - (x**2 - 2 * x)
    c3 = (sorted(sp.solve(h, x)) == [0, 3], bool(-h.subs(x, 1) > 0), I(h, (x, 0, 3)) == R(9, 2),
          sp.Abs(I(x**2 - 3 * x, (x, 0, 3))) == R(9, 2))
    assert ''.join('Đ' if c else 'S' for c in c3) == TF_KEYS[2]
    v = 12 - 3 * t
    dist6 = I(v, (t, 0, 4)) + sp.Abs(I(v, (t, 4, 6)))
    c4 = (sp.solve(v, t) == [4], I(v, (t, 0, 4)) == 24, I(v, (t, 0, 6)) == 18, dist6 == 18)
    assert dist6 == 30 and ''.join('Đ' if c else 'S' for c in c4) == TF_KEYS[3]
    # Phần III
    F1 = x**4 - x**2 + 3
    assert same(d(F1, x), 4 * x**3 - 2 * x) and F1.subs(x, 1) == 3 and F1.subs(x, 2) == 15
    s2 = I(sp.sin(x)**2, (x, 0, pi / 2))
    assert same(s2, pi / 4) and f'{float(s2):.2f}' == '0.79'
    assert I(sp.log(x) / x, (x, 1, E)) == R(1, 2)
    s4 = I(sp.exp(x) - 1, (x, 0, 1))
    assert same(s4, E - 2) and f'{float(s4):.2f}' == '0.72'
    s5 = pi * I((2 * x - x**2)**2, (x, 0, 2))
    assert same(s5, 16 * pi / 15) and f'{float(s5):.2f}' == '3.35'
    assert I(20 + 6 * t, (t, 0, 10)) == 500
    assert [v for _, v in SHORT] == ['15', '0,79', '0,5', '0,72', '3,35', '500']
    # scoring
    assert 12 * R(1, 4) + 4 + 6 * R(1, 2) == 10
    return True


validate()

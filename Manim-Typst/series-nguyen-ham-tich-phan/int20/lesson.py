"""INT20 – Tổng ôn tích phân theo 3 dạng câu hỏi: mini-đề 10 câu.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT20',
    'number': 20,
    'title': 'Tổng ôn tích phân',
    'subtitle': 'Mini-đề 10 câu theo 3 dạng câu hỏi',
    'next_code': 'INT21',
    'next_title': 'Diện tích hình phẳng giới hạn bởi đồ thị và trục Ox',
}

PARTS = (
    ('hook', 'Mở đầu'),
    ('core', 'Bảng tổng hợp'),
    ('examples', 'Trắc nghiệm'),
    ('exam', 'Đúng/Sai – Trả lời ngắn'),
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
         'Mười câu hỏi, đủ ba dạng của đề thi tốt nghiệp mới: sáu câu trắc nghiệm, một câu đúng sai bốn ý, '
         'và ba câu trả lời ngắn. Tất cả đều nằm trong chín tập vừa học. Em làm được bao nhiêu câu?',
         'Mở đầu: mini-đề 10 câu'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tổng ôn phần tích phân.'),
    Beat('h3', 'hook',
         'Cách dùng video này: xem bảng tổng hợp các công cụ, rồi với mỗi câu hỏi, hãy tạm dừng video và tự làm trước. '
         'Chấm điểm cho mình sau mỗi câu. Cuối video, em sẽ biết phần nào cần xem lại.'),
    # ---------------- BẢNG TỔNG HỢP ----------------
    Beat('c1', 'core',
         'Bảng tổng hợp, nhóm một: công cụ tính. Công thức Newton Leibniz: tích phân bằng F của b trừ F của a. '
         'Tính chất tuyến tính và cộng khoảng. Trị tuyệt đối: xét dấu rồi tách cận.',
         'Bảng tổng hợp các công cụ'),
    Beat('c2', 'core',
         'Nhóm hai: kỹ thuật biến đổi. Đổi biến số, nhớ đổi cận. Từng phần, chọn u theo thứ tự nhất log, nhì đa, tam lượng, tứ mũ. '
         'Tính đối xứng với phép thay x bằng a cộng b trừ x, và hàm ẩn từ hệ thức của f phẩy và f.'),
    Beat('c3', 'core',
         'Nhóm ba: ứng dụng. Tích phân của vận tốc là độ dời, tích phân của trị tuyệt đối vận tốc là quãng đường. '
         'Và chiến thuật cho ba dạng câu hỏi: trắc nghiệm thì loại trừ và bấm máy kiểm tra, '
         'đúng sai thì xét từng ý độc lập, trả lời ngắn thì chú ý làm tròn và cách ghi phiếu.',
         'Chiến thuật ba dạng câu hỏi'),
    Beat('c4', 'core',
         'Trước khi làm đề, điểm lại năm cái bẫy hay gặp nhất. Một, quên chia hệ số khi lấy nguyên hàm của e mũ hai x. '
         'Hai, đưa trị tuyệt đối ra ngoài tích phân. Ba, đổi biến mà quên đổi cận. '
         'Bốn, chọn u ngược thứ tự khi từng phần. Năm, sai dấu khi lấy nguyên hàm của e mũ trừ x.',
         'Năm bẫy thường gặp'),
    # ---------------- TRẮC NGHIỆM ----------------
    Beat('q1', 'examples',
         'Câu một. Tích phân từ không đến hai của ba x bình phương trừ hai x bằng bao nhiêu? Em hãy tạm dừng video. '
         'Nguyên hàm là x lập phương trừ x bình phương. Thay cận: tám trừ bốn, bằng bốn. Đáp án A.',
         'Câu 1–6: trắc nghiệm'),
    Beat('q2', 'examples',
         'Câu hai. Biết tích phân từ một đến ba của f bằng năm, của g bằng trừ hai. Tính tích phân của hai f trừ ba g. '
         'Theo tuyến tính: hai nhân năm, trừ ba nhân trừ hai, bằng mười cộng sáu, bằng mười sáu. Đáp án C.'),
    Beat('q3', 'examples',
         'Câu ba. Tích phân từ không đến một của e mũ hai x. Nguyên hàm là e mũ hai x chia hai, '
         'thay cận được e bình phương trừ một, chia hai. Đáp án B. Bẫy thường gặp là quên chia hai, chọn A.'),
    Beat('q4', 'examples',
         'Câu bốn. Tích phân từ không đến hai của trị tuyệt đối x trừ một. Đồ thị là hai tam giác, '
         'mỗi tam giác có diện tích một phần hai. Tổng bằng một. Đáp án C. Ai chọn không là đã bỏ trị tuyệt đối ra ngoài.'),
    Beat('q5', 'examples',
         'Câu năm. Tích phân từ không đến một của hai x nhân x bình phương cộng một, bình phương. '
         'Đặt u bằng x bình phương cộng một, cận mới từ một đến hai. Tích phân của u bình phương bằng tám phần ba trừ một phần ba, '
         'bằng bảy phần ba. Đáp án D.'),
    Beat('q6', 'examples',
         'Câu sáu. Tích phân từ một đến e của l n x. Từng phần với u bằng l n x, d v bằng d x: '
         'x l n x lấy cận, bằng e, trừ tích phân của một, bằng e trừ một. Kết quả là một. Đáp án B.'),
    # ---------------- ĐÚNG/SAI & TRẢ LỜI NGẮN ----------------
    Beat('x1', 'exam',
         'Câu bảy, dạng đúng sai. Một chất điểm có vận tốc v bằng sáu trừ hai t, mét trên giây, với t từ không đến năm giây. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu 7: Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: v bằng không khi t bằng ba, chất điểm dừng rồi đổi chiều. '
         'Ý b đúng: độ dời là tích phân của v từ không đến năm, bằng ba mươi trừ hai mươi lăm, bằng năm mét.'),
    Beat('x3', 'exam',
         'Ý c sai: quãng đường phải tách cận tại ba. Từ không đến ba được chín mét, từ ba đến năm chất điểm lùi bốn mét. '
         'Quãng đường là mười ba mét, nên ý d đúng.'),
    Beat('x4', 'exam',
         'Trước ba câu trả lời ngắn, nhắc lại cách ghi phiếu. Phiếu có bốn ô, dấu phẩy và dấu trừ mỗi thứ chiếm một ô. '
         'Ví dụ trừ một phẩy năm cần đủ bốn ô. Nếu kết quả có nhiều chữ số thập phân, làm tròn theo yêu cầu của đề, '
         'rồi mới ghi vào phiếu.',
         'Cách ghi phiếu trả lời ngắn'),
    Beat('s1', 'exam',
         'Câu tám, trả lời ngắn. Tính tích phân từ không đến pi phần hai của x cốt x, làm tròn đến hàng phần trăm. '
         'Từng phần: x sin x lấy cận, bằng pi phần hai, trừ tích phân của sin x, bằng một. '
         'Kết quả pi phần hai trừ một, xấp xỉ không phẩy năm bảy.',
         ),
    Beat('s2', 'exam',
         'Câu chín. Hàm f liên tục thỏa f của x cộng f của trừ x bằng x bình phương. '
         'Tính tích phân từ trừ hai đến hai của f, làm tròn đến hàng phần trăm. '
         'Bằng một nửa tích phân của x bình phương từ trừ hai đến hai, tức một nửa của mười sáu phần ba, '
         'bằng tám phần ba, xấp xỉ hai phẩy sáu bảy.'),
    Beat('s3', 'exam',
         'Câu mười. Ô tô đang chạy hai mươi mét trên giây thì phanh, vận tốc sau đó là hai mươi trừ bốn t. '
         'Tính quãng đường từ lúc phanh đến khi dừng. Ô tô dừng khi t bằng năm. '
         'Tích phân từ không đến năm của hai mươi trừ bốn t bằng một trăm trừ năm mươi, bằng năm mươi mét.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Đáp án cả đề: câu một A, câu hai C, câu ba B, câu bốn C, câu năm D, câu sáu B. '
         'Câu bảy: đúng, đúng, sai, đúng. Câu tám không phẩy năm bảy, câu chín hai phẩy sáu bảy, câu mười năm mươi.',
         'Tổng kết và hướng ôn tập'),
    Beat('o2', 'outro',
         'Tự chấm điểm. Sai câu ba hoặc câu tám: xem lại tập mười hai và tập mười bảy. Sai câu bốn hoặc câu bảy: '
         'xem tập mười bốn và mười lăm. Sai câu năm: xem tập mười sáu. Sai câu chín: xem tập mười tám. '
         'Mỗi lỗi sai là một bài học cần ôn lại.'),
    Beat('o3', 'outro',
         'Phần B khép lại tại đây. Từ tập hai mốt, ta bước sang phần C: ứng dụng tích phân tính diện tích hình phẳng, '
         'bắt đầu với miền giới hạn bởi đồ thị và trục hoành. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'tool1': "integral_a^b f(x) dif x = F(b) - F(a)",
    'tool2': "integral_a^c = integral_a^b + integral_b^c",
    'tool3': "integral_a^b abs(f) = sum plus.minus integral f",
    'tech1': "u = u(x): quad integral_a^b arrow.r integral_(u(a))^(u(b))",
    'tech2': "integral u dif v = u v - integral v dif u",
    'tech3': "integral_a^b f(x) dif x = integral_a^b f(a + b - x) dif x",
    'app1': "Delta s = integral v dif t, quad S = integral abs(v) dif t",
    'q1': "integral_0^2 (3x^2 - 2x) dif x",
    'q1_s': "lr((x^3 - x^2) |)_0^2 = 8 - 4 = gold(4)",
    'q2': "integral_1^3 f = 5, quad integral_1^3 g = -2, quad integral_1^3 (2f - 3g) dif x = ?",
    'q2_s': "2 dot 5 - 3 dot (-2) = gold(16)",
    'q3': "integral_0^1 e^(2x) dif x",
    'q3_s': "lr(e^(2x)/2 |)_0^1 = gold((e^2 - 1)/2)",
    'q4': "integral_0^2 abs(x - 1) dif x",
    'q4_s': "1/2 + 1/2 = gold(1)",
    'q5': "integral_0^1 2x(x^2 + 1)^2 dif x",
    'q5_s': "u = x^2 + 1: quad integral_1^2 u^2 dif u = 8/3 - 1/3 = gold(7/3)",
    'q6': "integral_1^e ln x dif x",
    'q6_s': "lr(x ln x |)_1^e - integral_1^e dif x = e - (e - 1) = gold(1)",
    'o_4': "4", 'o_6': "6", 'o_8': "8", 'o_2': "2",
    'o_13': "13", 'o_10': "10", 'o_16': "16",
    'o_e1': "e^2 - 1", 'o_e2': "(e^2 - 1)/2", 'o_e3': "2(e^2 - 1)", 'o_e4': "e^2",
    'o_0': "0", 'o_1': "1", 'o_half': "1/2",
    'o_83': "8/3", 'o_76': "7/6", 'o_73': "7/3",
    'o_e': "e", 'o_em1': "e - 1",
    'tf_given': "v(t) = 6 - 2t quad (\"m/s\"), quad t in [0; 5]",
    'tf_a': "v(3) = 0",
    'tf_b': "integral_0^5 v(t) dif t = 5",
    'tf_c': "S = 5 \"m\"",
    'tf_d': "S = 13 \"m\"",
    'tf_calc': "S = integral_0^3 (6 - 2t) dif t + abs(integral_3^5 (6 - 2t) dif t) = 9 + 4 = 13",
    's1': "integral_0^(pi\\/2) x cos x dif x approx ?",
    's1_s': "= lr(x sin x |)_0^(pi\\/2) - integral_0^(pi\\/2) sin x dif x = pi/2 - 1 approx gold(\"0,57\")",
    's2': "f(x) + f(-x) = x^2, quad integral_(-2)^2 f(x) dif x approx ?",
    's2_s': "= 1/2 integral_(-2)^2 x^2 dif x = 1/2 dot 16/3 = 8/3 approx gold(\"2,67\")",
    's3': "v(t) = 20 - 4t quad (\"m/s\")",
    's3_s': "v = 0 arrow.double.long t = 5: quad S = integral_0^5 (20 - 4t) dif t = 100 - 50 = gold(50)",
    'next1': "S = integral_a^b abs(f(x)) dif x",
}

# (question key, option keys A–D, correct index, solution key)
MC = (
    ('q1', ('o_4', 'o_6', 'o_8', 'o_2'), 0, 'q1_s'),
    ('q2', ('o_4', 'o_13', 'o_16', 'o_10'), 2, 'q2_s'),
    ('q3', ('o_e1', 'o_e2', 'o_e3', 'o_e4'), 1, 'q3_s'),
    ('q4', ('o_0', 'o_2', 'o_1', 'o_half'), 2, 'q4_s'),
    ('q5', ('o_83', 'o_76', 'o_1', 'o_73'), 3, 'q5_s'),
    ('q6', ('o_e', 'o_1', 'o_em1', 'o_0'), 1, 'q6_s'),
)

SHORT = (('s1', '0,57'), ('s2', '2,67'), ('s3', '50'))

EXERCISES = (  # the mini-test itself, with its key (used for the description and the lecture notes)
    ('Câu 1: ∫₀² (3x² − 2x) dx', 'A (4)'),
    ('Câu 2: ∫₁³ f = 5, ∫₁³ g = −2, ∫₁³ (2f − 3g) dx', 'C (16)'),
    ('Câu 3: ∫₀¹ e^(2x) dx', 'B ((e² − 1)/2)'),
    ('Câu 4: ∫₀² |x − 1| dx', 'C (1)'),
    ('Câu 5: ∫₀¹ 2x(x² + 1)² dx', 'D (7/3)'),
    ('Câu 6: ∫₁^e ln x dx', 'B (1)'),
    ('Câu 7: v(t) = 6 − 2t, t ∈ [0; 5]', 'Đ Đ S Đ'),
    ('Câu 8: ∫₀^(π/2) x cos x dx', '0,57'),
    ('Câu 9: f(x) + f(−x) = x², ∫₋₂² f(x) dx', '2,67'),
    ('Câu 10: v(t) = 20 − 4t, quãng đường phanh', '50'),
)

TRUE_FALSE = (
    ('v(3) = 0', True),
    ('∫₀⁵ v(t) dt = 5', True),
    ('S = 5 m', False),
    ('S = 13 m', True),
)

x, t = sp.symbols('x t', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, E, pi = sp.integrate, sp.Rational, sp.E, sp.pi
    value = {'o_4': 4, 'o_6': 6, 'o_8': 8, 'o_2': 2, 'o_13': 13, 'o_10': 10, 'o_16': 16,
             'o_e1': E**2 - 1, 'o_e2': (E**2 - 1) / 2, 'o_e3': 2 * (E**2 - 1), 'o_e4': E**2,
             'o_0': 0, 'o_1': 1, 'o_half': R(1, 2), 'o_83': R(8, 3), 'o_76': R(7, 6), 'o_73': R(7, 3),
             'o_e': E, 'o_em1': E - 1}
    answers = {
        'q1': I(3 * x**2 - 2 * x, (x, 0, 2)),
        'q2': 2 * 5 - 3 * (-2),
        'q3': I(sp.exp(2 * x), (x, 0, 1)),
        'q4': I(sp.Abs(x - 1), (x, 0, 1)) + I(sp.Abs(x - 1), (x, 1, 2)),
        'q5': I(2 * x * (x**2 + 1)**2, (x, 0, 1)),
        'q6': I(sp.log(x), (x, 1, E)),
    }
    for q, opts, k, _ in MC:
        assert len(set(opts)) == 4
        hits = [i for i, o in enumerate(opts) if sp.simplify(value[o] - answers[q]) == 0]
        assert hits == [k], (q, hits)
    assert ''.join('ABCD'[k] for _, _, k, _ in MC) == 'ACBCDB'
    assert I(sp.Abs(x - 1), (x, 0, 2)) == 1 and I(x * 0 + 1, (x, 0, 1)) == 1
    # true / false
    v = 6 - 2 * t
    dist = I(v, (t, 0, 3)) + abs(I(v, (t, 3, 5)))
    claims = (v.subs(t, 3) == 0, I(v, (t, 0, 5)) == 5, dist == 5, dist == 13)
    assert I(v, (t, 0, 3)) == 9 and I(v, (t, 3, 5)) == -4
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answers
    s1 = I(x * sp.cos(x), (x, 0, pi / 2))
    assert sp.simplify(s1 - (pi / 2 - 1)) == 0 and f'{float(s1):.2f}' == '0.57'
    fw = x**2 / 2 + x**3   # any f with f(x) + f(−x) = x²
    assert sp.simplify(fw + fw.subs(x, -x) - x**2) == 0
    s2 = I(fw, (x, -2, 2))
    assert s2 == R(8, 3) == R(1, 2) * I(x**2, (x, -2, 2)) and f'{float(s2):.2f}' == '2.67'
    assert sp.solve(20 - 4 * t, t) == [5] and I(20 - 4 * t, (t, 0, 5)) == 50
    assert [a for _, a in SHORT] == ['0,57', '2,67', '50']
    return True


validate()

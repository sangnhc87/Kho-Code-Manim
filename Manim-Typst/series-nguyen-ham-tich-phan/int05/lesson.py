"""INT05 – Nguyên hàm của f(ax + b): hàm hợp tuyến tính, vì sao phải chia cho a.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT05',
    'number': 5,
    'title': 'Nguyên hàm của f(ax + b)',
    'subtitle': 'Hàm hợp tuyến tính – vì sao chia cho a',
    'next_code': 'INT06',
    'next_title': 'Nguyên hàm có điều kiện & hàm từng khúc',
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
         'Ở tập trước, ta đã dùng kết quả: nguyên hàm của cốt hai x bằng sin hai x chia hai. Con số hai ở mẫu từ đâu ra? '
         'Nếu thay hai bằng ba, bằng năm, hay bằng âm một, kết quả thay đổi thế nào? '
         'Hôm nay ta trả lời câu hỏi đó cho mọi hàm số có dạng f của a x cộng b.',
         'Mở đầu: số 2 ở mẫu từ đâu ra?'),
    Beat('h2', 'hook',
         'Đây là tập năm của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'nguyên hàm của f của a x cộng b, và vì sao luôn phải chia cho a.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, quy tắc tổng quát và cách chứng minh bằng đạo hàm hàm hợp. '
         'Hai, ý nghĩa hình học: co giãn đồ thị theo phương ngang làm độ dốc nhân lên a lần. '
         'Ba, hai cái bẫy: quên chia a, và áp dụng sai khi bên trong không phải bậc nhất.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Giả sử F là một nguyên hàm của f. Theo quy tắc đạo hàm hàm hợp, đạo hàm của F của a x cộng b bằng '
         'a nhân f của a x cộng b. Thừa ra một thừa số a, nên ta chia cho a để bù lại. '
         'Vậy nguyên hàm của f của a x cộng b bằng một phần a nhân F của a x cộng b, cộng C, với a khác không.',
         'Quy tắc tổng quát'),
    Beat('c2', 'core',
         'Vì sao lại là a? Hãy nhìn đồ thị sin x và sin hai x. Đồ thị sin hai x là sin x bị nén theo phương ngang '
         'hai lần. Nén ngang làm đồ thị dốc gấp đôi: tại các điểm tương ứng, độ dốc của sin hai x luôn gấp hai lần '
         'độ dốc của sin x.',
         'Bản chất hình học: nén ngang'),
    Beat('c3', 'core',
         'Khi nén với hệ số a bất kỳ, độ dốc nhân lên a lần. Đó là lý do đạo hàm sinh ra thừa số a, '
         'và nguyên hàm phải chia cho a. Hình bên trái cho thấy khi a tăng, đường cong dày đặc hơn '
         'và tiếp tuyến dốc hơn đúng a lần.'),
    Beat('c4', 'core',
         'Còn số b thì sao? Số b chỉ tịnh tiến đồ thị theo phương ngang, không làm thay đổi độ dốc. '
         'Vì vậy b không xuất hiện ở mẫu số: chỉ có a là quan trọng.'),
    Beat('c5', 'core',
         'Áp dụng quy tắc cho bảng nguyên hàm cơ bản, ta được bảng mở rộng. Lũy thừa của a x cộng b, '
         'một chia a x cộng b, e mũ a x cộng b, cốt và sin của a x cộng b: tất cả đều giống bảng cũ, '
         'chỉ thêm một phần a ở phía trước.',
         'Bảng nguyên hàm mở rộng'),
    Beat('c6', 'core',
         'Ba ví dụ nhanh. Nguyên hàm của hai x cộng một mũ năm là hai x cộng một mũ sáu, chia mười hai. '
         'Nguyên hàm của e mũ ba x trừ một là e mũ ba x trừ một chia ba. Còn nguyên hàm của một chia một trừ hai x '
         'là âm một phần hai lô ga nê pe trị tuyệt đối của một trừ hai x: chú ý a bằng âm hai nên có dấu trừ.'),
    Beat('c7', 'core',
         'Cái bẫy thứ nhất: quên chia a, hoặc nhân a thay vì chia. Viết nguyên hàm của cốt ba x bằng ba sin ba x là sai. '
         'Lấy đạo hàm kiểm tra sẽ được chín cốt ba x. Đúng phải là sin ba x chia ba.',
         'Hai cái bẫy'),
    Beat('c8', 'core',
         'Cái bẫy thứ hai nguy hiểm hơn: quy tắc chỉ đúng khi bên trong là bậc nhất. Nguyên hàm của e mũ x bình phương '
         'không phải e mũ x bình phương chia hai x. Đạo hàm của biểu thức đó phức tạp hơn nhiều. '
         'Với biểu thức bên trong bậc hai trở lên, ta phải khai triển hoặc dùng phương pháp khác.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: nguyên hàm của ba x trừ hai, mũ bốn. Ở đây a bằng ba và số mũ mới là năm. '
         'Kết quả là ba x trừ hai mũ năm, chia ba nhân năm, tức là chia mười lăm, cộng C. '
         'So với cách khai triển cả biểu thức, cách này nhanh hơn rất nhiều.',
         'Ví dụ 1–2: áp dụng trực tiếp'),
    Beat('e2', 'examples',
         'Ví dụ hai: nguyên hàm của một chia hai x cộng một, cộng e mũ hai x. '
         'Cả hai hạng tử đều có a bằng hai. Kết quả là một phần hai lô ga nê pe trị tuyệt đối hai x cộng một, '
         'cộng một phần hai e mũ hai x, cộng C.'),
    Beat('e3', 'examples',
         'Ví dụ ba: tìm F là nguyên hàm của sin của hai x trừ pi phần ba, biết F của pi phần sáu bằng một. '
         'Ta có F bằng âm một phần hai cốt của hai x trừ pi phần ba cộng C. Tại pi phần sáu, góc bên trong bằng không, '
         'nên âm một phần hai cộng C bằng một, suy ra C bằng ba phần hai.',
         'Ví dụ 3–4: có điều kiện và căn thức'),
    Beat('e4', 'examples',
         'Ví dụ bốn: nguyên hàm của một chia căn hai x cộng một. Viết lại thành hai x cộng một mũ âm một phần hai. '
         'Số mũ mới là một phần hai, a bằng hai, nên ta chia cho hai nhân một phần hai, bằng một. '
         'Kết quả gọn đến bất ngờ: căn của hai x cộng một, cộng C.'),
    Beat('e5', 'examples',
         'Ví dụ năm, bài toán thực tế. Một bể chứa năm trăm lít nước bị rò. Tốc độ rò giảm dần theo thời gian: '
         'r của t bằng hai mươi e mũ âm không phẩy một t, lít mỗi giờ. Hỏi sau mười giờ, bể đã mất bao nhiêu lít nước?',
         'Ví dụ 5: bể nước bị rò'),
    Beat('e6', 'examples',
         'Lượng nước đã mất L là nguyên hàm của r. Ở đây a bằng âm không phẩy một, nên L bằng âm hai trăm e mũ '
         'âm không phẩy một t cộng C. Lúc đầu chưa mất nước, nên C bằng hai trăm. Sau mười giờ, '
         'L bằng hai trăm nhân một trừ e mũ âm một, xấp xỉ một trăm hai mươi sáu phẩy bốn lít.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai, tất cả xoay quanh việc chia cho a. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: a bằng hai nên chia hai. Ý b sai: thiếu một phần hai, đúng phải là một phần hai lô ga nê pe '
         'trị tuyệt đối hai x trừ một.'),
    Beat('x3', 'exam',
         'Ý c đúng: ở đây a bằng âm ba, nên một phần a là âm một phần ba. Ý d sai: ngoài việc chia cho số mũ mới là bốn, '
         'còn phải chia cho a bằng hai, nên đúng phải là chia tám.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. F là nguyên hàm của e mũ hai x trừ hai, và F của một bằng một. Tính F của hai, '
         'làm tròn đến hàng phần trăm. F bằng một phần hai e mũ hai x trừ hai cộng C. F của một bằng một phần hai cộng C '
         'bằng một, nên C bằng một phần hai. F của hai bằng e bình phương chia hai cộng một phần hai, xấp xỉ bốn phẩy một chín.',
         'Trả lời ngắn và mẹo nhẩm nhanh'),
    Beat('x5', 'exam',
         'Mẹo nhẩm nhanh hai bước. Bước một: coi a x cộng b như một biến mới, viết nguyên hàm theo bảng cơ bản. '
         'Bước hai: chia cho a. Trước khi làm, kiểm tra biểu thức bên trong có đúng là bậc nhất hay không.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, nguyên hàm của f của a x cộng b bằng một phần a nhân F của a x cộng b cộng C. '
         'Hai, a xuất hiện vì nén ngang làm độ dốc nhân a, còn b chỉ tịnh tiến. '
         'Ba, quy tắc chỉ dùng khi bên trong là bậc nhất, và đừng quên dấu khi a âm.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tìm nguyên hàm của một trừ ba x mũ năm. Hai, tìm nguyên hàm của e mũ âm x cộng sin bốn x. '
         'Ba, biết F phẩy bằng một chia hai x cộng ba và F của âm một bằng hai, tính F của một phần hai. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập sáu, ta sẽ luyện kỹ dạng nguyên hàm có điều kiện và hàm số cho theo từng khúc, '
         'một dạng rất hay ra trong câu đúng sai. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook1': "integral cos 2x dif x = (sin 2x)/gold(2) + C",
    'hook2': "integral cos 5x dif x = gold(?), quad integral e^(-x) dif x = gold(?)",
    'chain': "[F(a x + b)]' = gold(a) dot f(a x + b)",
    'rule': "integral f(a x + b) dif x = 1/gold(a) F(a x + b) + C, quad a != 0",
    'sin_x': "cyan(y = sin x)",
    'sin_2x': "gold(y = sin 2x)",
    'slope_rel': "(sin 2x)' = gold(2) cos 2x",
    'shift_b': "(sin(x + b))' = cos(x + b)",
    'tb_pow': "integral (a x + b)^alpha dif x = 1/a dot (a x + b)^(alpha+1)/(alpha+1) + C",
    'tb_inv': "integral 1/(a x + b) dif x = 1/a ln|a x + b| + C",
    'tb_exp': "integral e^(a x + b) dif x = 1/a e^(a x + b) + C",
    'tb_cos': "integral cos(a x + b) dif x = 1/a sin(a x + b) + C",
    'tb_sin': "integral sin(a x + b) dif x = -1/a cos(a x + b) + C",
    'q1': "integral (2x + 1)^5 dif x = (2x + 1)^6/12 + C",
    'q2': "integral e^(3x - 1) dif x = e^(3x - 1)/3 + C",
    'q3': "integral 1/(1 - 2x) dif x = coral(-1/2) ln|1 - 2x| + C",
    'trap1': "integral cos 3x dif x coral(!=) 3 sin 3x + C",
    'trap1_ok': "integral cos 3x dif x = (sin 3x)/3 + C",
    'trap2': "integral e^(x^2) dif x coral(!=) e^(x^2)/(2x) + C",
    'e1_task': "integral (3x - 2)^4 dif x",
    'e1_s1': "= 1/3 dot (3x - 2)^5/5 + C = (3x - 2)^5/15 + C",
    'e2_task': "integral (1/(2x + 1) + e^(2x)) dif x",
    'e2_s1': "= 1/2 ln|2x + 1| + 1/2 e^(2x) + C",
    'e3_task': "F'(x) = sin(2x - pi/3), quad F(pi/6) = 1",
    'e3_s1': "F(x) = -1/2 cos(2x - pi/3) + C",
    'e3_s2': "F(pi/6) = -1/2 cos 0 + C = 1 arrow.double.long C = 3/2",
    'e4_task': "integral 1/sqrt(2x + 1) dif x = integral (2x + 1)^(-1/2) dif x",
    'e4_s1': "= 1/2 dot (2x + 1)^(1/2)/(1/2) + C = sqrt(2x + 1) + C",
    'e5_task': "r(t) = 20 e^(-0.1 t), quad L(0) = 0",
    'e5_s1': "L(t) = 20 dot 1/(-0.1) e^(-0.1 t) + C = -200 e^(-0.1 t) + C",
    'e5_s2': "L(0) = -200 + C = 0 arrow.double.long C = 200",
    'e5_s3': "L(10) = 200(1 - e^(-1)) approx gold(\"126,4\")",
    'tf_a': "integral e^(2x) dif x = e^(2x) \\/ 2 + C",
    'tf_b': "integral 1 \\/ (2x - 1) dif x = ln|2x - 1| + C",
    'tf_c': "integral cos(1 - 3x) dif x = -1 \\/ 3 dot sin(1 - 3x) + C",
    'tf_d': "integral (2x - 1)^3 dif x = (2x - 1)^4 \\/ 4 + C",
    'tf_b_calc': "integral 1/(2x - 1) dif x = 1/2 ln|2x - 1| + C",
    'tf_d_calc': "integral (2x - 1)^3 dif x = (2x - 1)^4/(2 dot 4) + C = (2x - 1)^4/8 + C",
    'sa_task': "F'(x) = e^(2x - 2), quad F(1) = 1, quad F(2) approx ?",
    'sa_s1': "F(x) = 1/2 e^(2x - 2) + C, quad 1/2 + C = 1 arrow.double.long C = 1/2",
    'sa_s2': "F(2) = e^2/2 + 1/2 approx gold(\"4,19\")",
    'tip1': "u = a x + b",
    'tip2': "integral f(u) dif u = F(u) + C",
    'tip3': "\"chia cho\" a",
    'sum1': "integral f(a x + b) dif x = 1/a F(a x + b) + C",
    'sum2': "(sin a x)' = a cos a x",
    'sum3': "integral e^(x^2) dif x coral(!=) e^(x^2)/(2x)",
    'hw1': "integral (1 - 3x)^5 dif x",
    'hw2': "integral (e^(-x) + sin 4x) dif x",
    'hw3': "F'(x) = 1/(2x + 3), quad F(-1) = 2, quad F(1/2) = ?",
    'hw_ans1': "-(1 - 3x)^6/18 + C",
    'hw_ans2': "-e^(-x) - (cos 4x)/4 + C",
    'hw_ans3': "2 + ln 2",
    'next1': "F(x) = cases(x^2 + C_1 & \"khi\" x >= 0, x + C_2 & \"khi\" x < 0)",
    'next2': "F(0^-) = F(0^+) arrow.double.long C_1 = C_2",
}

EXERCISES = (
    ('Tìm ∫(1 − 3x)⁵ dx.', '−(1 − 3x)⁶/18 + C'),
    ('Tìm ∫(e⁻ˣ + sin 4x) dx.', '−e⁻ˣ − cos 4x/4 + C'),
    ("Biết F'(x) = 1/(2x + 3), F(−1) = 2. Tính F(1/2).", 'F(1/2) = 2 + ln 2'),
)

TRUE_FALSE = (
    ('∫e²ˣ dx = e²ˣ/2 + C', True),
    ('∫1/(2x − 1) dx = ln|2x − 1| + C', False),
    ('∫cos(1 − 3x) dx = −(1/3) sin(1 − 3x) + C', True),
    ('∫(2x − 1)³ dx = (2x − 1)⁴/4 + C', False),
)

x, t, C = sp.symbols('x t C', real=True)
P = sp.symbols('P', positive=True)
a, b = sp.symbols('a b', real=True, nonzero=True)
pi = sp.pi


def same_primitive(F, f, var=x):
    return sp.simplify(sp.diff(F, var) - f) == 0


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    s, c, e = sp.sin, sp.cos, sp.exp
    # general rule with a concrete F (sin): d/dx [F(ax+b)/a] = f(ax+b)
    assert same_primitive(s(a*x + b)/a, c(a*x + b))
    assert sp.simplify(sp.diff(s(2*x), x) - 2*c(2*x)) == 0
    assert sp.diff(s(x + b), x) == c(x + b)  # b only shifts
    # extended table
    al = sp.Rational(3, 2)
    assert same_primitive((2*x + 1)**(al + 1)/(2*(al + 1)), (2*x + 1)**al)
    assert same_primitive(sp.log(a*x + b)/a, 1/(a*x + b))
    assert same_primitive(e(a*x + b)/a, e(a*x + b))
    assert same_primitive(-c(a*x + b)/a, s(a*x + b))
    # quick examples
    assert same_primitive((2*x + 1)**6/12, (2*x + 1)**5)
    assert same_primitive(e(3*x - 1)/3, e(3*x - 1))
    assert same_primitive(-sp.log(1 - 2*x)/2, 1/(1 - 2*x))
    # traps
    assert not same_primitive(3*s(3*x), c(3*x)) and sp.diff(3*s(3*x), x) == 9*c(3*x)
    assert same_primitive(s(3*x)/3, c(3*x))
    assert not same_primitive(e(x**2)/(2*x), e(x**2))
    # examples
    assert same_primitive((3*x - 2)**5/15, (3*x - 2)**4)
    assert same_primitive(sp.log(2*P + 1)/2 + e(2*P)/2, 1/(2*P + 1) + e(2*P), P)
    F3 = -c(2*x - pi/3)/2 + C
    c3 = sp.solve(sp.Eq(F3.subs(x, pi/6), 1), C)[0]
    assert same_primitive(F3, s(2*x - pi/3)) and c3 == sp.Rational(3, 2)
    assert same_primitive(sp.sqrt(2*P + 1), 1/sp.sqrt(2*P + 1), P)
    L = -200*e(-t/10) + C
    cL = sp.solve(sp.Eq(L.subs(t, 0), 0), C)[0]
    L10 = (L.subs(C, cL)).subs(t, 10)
    assert same_primitive(L, 20*e(-t/10), t) and cL == 200
    assert sp.simplify(L10 - 200*(1 - e(-1))) == 0 and round(float(L10), 1) == 126.4
    # true / false (x > 1/2 for the log)
    claims = (
        same_primitive(e(2*x)/2, e(2*x)),
        same_primitive(sp.log(2*x - 1), 1/(2*x - 1)),
        same_primitive(-s(1 - 3*x)/3, c(1 - 3*x)),
        same_primitive((2*x - 1)**4/4, (2*x - 1)**3),
    )
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    assert same_primitive(sp.log(2*x - 1)/2, 1/(2*x - 1)) and same_primitive((2*x - 1)**4/8, (2*x - 1)**3)
    # short answer
    Fs = e(2*x - 2)/2 + C
    cs = sp.solve(sp.Eq(Fs.subs(x, 1), 1), C)[0]
    v = Fs.subs(C, cs).subs(x, 2)
    assert cs == sp.Rational(1, 2) and round(float(v), 2) == 4.19
    # exercises
    assert same_primitive(-(1 - 3*x)**6/18, (1 - 3*x)**5)
    assert same_primitive(-e(-x) - c(4*x)/4, e(-x) + s(4*x))
    F_ = sp.log(sp.Abs(2*x + 3))/2 + C  # on (-3/2, +inf)
    cf = sp.solve(sp.Eq(F_.subs(x, -1), 2), C)[0]
    assert cf == 2 and sp.simplify(F_.subs(C, cf).subs(x, sp.Rational(1, 2)) - (2 + sp.log(2))) == 0
    assert same_primitive(sp.log(2*P + 3)/2, 1/(2*P + 3), P)
    return True


validate()

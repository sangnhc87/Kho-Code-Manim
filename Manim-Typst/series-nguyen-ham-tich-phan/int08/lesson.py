"""INT08 – Phương pháp đổi biến số: nhận diện u và du (mở rộng).

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT08',
    'number': 8,
    'title': 'Phương pháp đổi biến số',
    'subtitle': 'Nhận diện u và du',
    'next_code': 'INT09',
    'next_title': 'Phương pháp nguyên hàm từng phần',
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
         'Ở tập năm, ta biết quy tắc chia cho a chỉ dùng được khi bên trong là bậc nhất, nên nguyên hàm của e mũ '
         'x bình phương không làm được theo cách đó. Nhưng nếu đề cho hai x nhân e mũ x bình phương thì sao? '
         'Hãy để ý: hai x chính là đạo hàm của x bình phương. Sự xuất hiện của đạo hàm phần bên trong là chìa khóa '
         'của phương pháp đổi biến số.',
         'Mở đầu: hai x là đạo hàm của x²'),
    Beat('h2', 'hook',
         'Đây là tập tám của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: phương pháp đổi biến số. '
         'Đây là nội dung mở rộng, rất hữu ích cho học sinh giỏi và các kỳ thi đánh giá năng lực.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, đổi biến chính là đạo hàm hàm hợp đọc ngược. '
         'Hai, quy trình bốn bước: chọn u, tính d u, đổi toàn bộ sang u, rồi trả về x. '
         'Ba, bảng nhận diện nhanh các dạng thường gặp và những bẫy cần tránh.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Nhắc lại đạo hàm hàm hợp: đạo hàm của F của u của x bằng f của u của x nhân u phẩy của x. '
         'Đọc ngược lại: nguyên hàm của f của u nhân u phẩy bằng F của u cộng C. '
         'Như vậy, khi thấy một hàm của u nhân với đạo hàm của u, ta lấy nguyên hàm theo u.',
         'Đạo hàm hàm hợp đọc ngược'),
    Beat('c2', 'core',
         'Để viết gọn, ta dùng vi phân: d u bằng u phẩy của x nhân d x. Khi đó cả cụm f của u nhân u phẩy d x '
         'trở thành f của u d u, một nguyên hàm đơn giản theo biến mới u.'),
    Beat('c3', 'core',
         'Ý nghĩa hình học của d u: hãy đặt trục x và trục u song song. Với u bằng x bình phương, một đoạn nhỏ '
         'độ dài d x trên trục x được ánh xạ thành đoạn d u trên trục u, dài gấp hai x lần. '
         'Hệ số co giãn đó chính là u phẩy, và nó phải có mặt trong biểu thức thì mới đổi biến được.',
         'Ý nghĩa của du'),
    Beat('c4', 'core',
         'Quy trình bốn bước. Bước một, chọn u là phần bên trong, thường là phần mà đạo hàm của nó xuất hiện bên ngoài. '
         'Bước hai, tính d u. Bước ba, đổi toàn bộ biểu thức sang u, không để sót x nào. '
         'Bước bốn, tính nguyên hàm theo u rồi thay ngược u bằng biểu thức của x.',
         'Quy trình 4 bước'),
    Beat('c5', 'core',
         'Áp dụng cho bài mở đầu. Đặt u bằng x bình phương, thì d u bằng hai x d x. Biểu thức trở thành '
         'nguyên hàm của e mũ u d u, bằng e mũ u cộng C. Trả về biến x: e mũ x bình phương cộng C. '
         'Kiểm tra bằng đạo hàm: đúng bằng hai x e mũ x bình phương.'),
    Beat('c6', 'core',
         'Đạo hàm của u chỉ cần xuất hiện sai khác một hằng số. Ví dụ, nguyên hàm của x nhân x bình phương cộng một '
         'mũ năm. Đặt u bằng x bình phương cộng một, d u bằng hai x d x, nên x d x bằng d u chia hai. '
         'Kết quả là một phần hai nguyên hàm của u mũ năm, bằng x bình phương cộng một mũ sáu chia mười hai, cộng C.',
         'Sai khác hằng số vẫn đổi được'),
    Beat('c7', 'core',
         'Với lượng giác: nguyên hàm của sin x nhân cốt lập phương x. Đặt u bằng cốt x, d u bằng âm sin x d x. '
         'Biểu thức trở thành âm nguyên hàm của u lập phương d u, bằng âm cốt mũ bốn x chia bốn, cộng C.'),
    Beat('c8', 'core',
         'Với lô ga rít: nguyên hàm của lô ga nê pe x chia x. Đặt u bằng lô ga nê pe x, d u bằng d x chia x. '
         'Kết quả là u bình phương chia hai, tức lô ga nê pe x tất cả bình phương chia hai, cộng C.'),
    Beat('c9', 'core',
         'Tổng hợp thành bảng nhận diện nhanh. Thấy x nhân một hàm của x bình phương: đặt u bằng x bình phương. '
         'Thấy e mũ một biểu thức nhân đạo hàm của nó: đặt u là số mũ. Thấy sin nhân lũy thừa của cốt, hoặc ngược lại: '
         'đặt u là hàm có lũy thừa. Thấy lô ga nê pe x chia x: đặt u bằng lô ga nê pe x.',
         'Bảng nhận diện nhanh'),
    Beat('c10', 'core',
         'Ba cái bẫy hay gặp. Một, quên trả về biến x ở bước cuối. Hai, quên đổi d x, dẫn tới thiếu hệ số như '
         'một phần hai. Ba, chọn u mà đạo hàm của nó không có mặt trong biểu thức, khi đó phép đổi biến bế tắc.',
         'Ba cái bẫy'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: nguyên hàm của e mũ x chia e mũ x cộng một. Đặt u bằng e mũ x cộng một, d u bằng e mũ x d x. '
         'Ta được nguyên hàm của d u chia u, bằng lô ga nê pe của e mũ x cộng một, cộng C. '
         'Không cần trị tuyệt đối vì biểu thức luôn dương.',
         'Ví dụ 1–3'),
    Beat('e2', 'examples',
         'Ví dụ hai: nguyên hàm của x nhân căn x bình phương cộng ba. Đặt u bằng x bình phương cộng ba, x d x bằng d u chia hai. '
         'Được một phần hai nguyên hàm của u mũ một phần hai, bằng một phần ba nhân x bình phương cộng ba mũ ba phần hai, cộng C.'),
    Beat('e3', 'examples',
         'Ví dụ ba: nguyên hàm của sin căn x chia căn x, với x dương. Đặt u bằng căn x, d u bằng d x chia hai căn x. '
         'Biểu thức trở thành hai nhân nguyên hàm của sin u d u, bằng âm hai cốt căn x, cộng C.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f của x bằng x nhân e mũ x bình phương. F là một nguyên hàm của f trên R. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: đạo hàm của x bình phương là hai x. Ý b sai: đây là bẫy quên hệ số. Vì x d x bằng d u chia hai, '
         'kết quả phải có một phần hai đứng trước.'),
    Beat('x3', 'exam',
         'Ý c đúng, chính là kết quả có hệ số một phần hai. Ý d đúng: F bằng một phần hai e mũ x bình phương cộng C, '
         'F của không bằng một phần hai cộng C bằng một nên C bằng một phần hai, và F của một bằng e cộng một, chia hai.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. F là nguyên hàm của cốt x nhân sin bình phương x, F của không bằng không. '
         'Tính F của pi phần hai, làm tròn đến hàng phần trăm. Đặt u bằng sin x, d u bằng cốt x d x. '
         'F bằng sin lập phương x chia ba cộng C, và C bằng không. Vậy F của pi phần hai bằng một phần ba, '
         'xấp xỉ không phẩy ba ba.',
         'Trả lời ngắn và mẹo kiểm tra'),
    Beat('x5', 'exam',
         'Mẹo kiểm tra nhanh: sau khi đổi biến, lấy đạo hàm kết quả theo x. Nếu ra đúng biểu thức ban đầu, kể cả hệ số, '
         'là chắc chắn đúng. Nếu lệch một hằng số như hai hay một phần hai, em đã quên đổi d x.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, đổi biến là đạo hàm hàm hợp đọc ngược: thấy hàm của u nhân u phẩy. '
         'Hai, quy trình bốn bước: chọn u, tính d u, đổi hết sang u, trả về x. '
         'Ba, đạo hàm của u chỉ cần xuất hiện sai khác hằng số, nhưng phải bù hằng số đó.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, nguyên hàm của ba x bình phương nhân x lập phương cộng một mũ bốn. '
         'Hai, nguyên hàm của cốt x chia sin x cộng hai. Ba, nguyên hàm của lô ga nê pe x bình phương chia x. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập chín, ta học phương pháp nguyên hàm từng phần, dành cho tích của hai hàm khác loại như x nhân e mũ x. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook1': "integral e^(x^2) dif x",
    'hook2': "integral gold(2x) e^(x^2) dif x = ?, quad (x^2)' = gold(2x)",
    'chain': "[F(u(x))]' = f(u(x)) dot u'(x)",
    'rule': "integral f(u(x)) u'(x) dif x = F(u(x)) + C",
    'diff': "dif u = u'(x) dif x",
    'rule_u': "integral f(u(x)) u'(x) dif x = integral f(u) dif u",
    'map': "u = x^2: quad dif u = gold(2x) dif x",
    'step1': "u = g(x)",
    'step2': "dif u = u'(x) dif x",
    'step3': "integral f(u) dif u",
    'step4': "F(u) + C arrow.r F(u(x)) + C",
    'ex0_1': "u = x^2, quad dif u = 2x dif x",
    'ex0_2': "integral 2x e^(x^2) dif x = integral e^u dif u = e^u + C = e^(x^2) + C",
    'ex0_chk': "(e^(x^2))' = 2x e^(x^2)",
    'k1': "integral x (x^2 + 1)^5 dif x, quad u = x^2 + 1, quad x dif x = (dif u)/2",
    'k2': "= 1/2 integral u^5 dif u = (x^2 + 1)^6/12 + C",
    'tr1': "integral sin x cos^3 x dif x, quad u = cos x, quad dif u = -sin x dif x",
    'tr2': "= -integral u^3 dif u = -(cos^4 x)/4 + C",
    'lg1': "integral (ln x)/x dif x, quad u = ln x, quad dif u = (dif x)/x",
    'lg2': "= integral u dif u = (ln^2 x)/2 + C",
    'rec1': "x dot f(x^2) arrow.r u = x^2",
    'rec2': "e^(g(x)) dot g'(x) arrow.r u = g(x)",
    'rec3': "sin x dot cos^n x arrow.r u = cos x",
    'rec4': "(ln x)/x arrow.r u = ln x",
    'e1_task': "integral e^x/(e^x + 1) dif x, quad u = e^x + 1, quad dif u = e^x dif x",
    'e1_s1': "= integral (dif u)/u = ln(e^x + 1) + C",
    'e2_task': "integral x sqrt(x^2 + 3) dif x, quad u = x^2 + 3, quad x dif x = (dif u)/2",
    'e2_s1': "= 1/2 integral u^(1/2) dif u = 1/3 (x^2 + 3)^(3/2) + C",
    'e3_task': "integral (sin sqrt(x))/sqrt(x) dif x, quad u = sqrt(x), quad dif u = (dif x)/(2 sqrt(x))",
    'e3_s1': "= 2 integral sin u dif u = -2 cos sqrt(x) + C",
    'tf_f': "f(x) = x e^(x^2)",
    'tf_a': "u = x^2 arrow.double.long dif u = 2x dif x",
    'tf_b': "integral f(x) dif x = e^(x^2) + C",
    'tf_c': "integral f(x) dif x = 1 \\/ 2 dot e^(x^2) + C",
    'tf_d': "F(0) = 1 arrow.double.long F(1) = (e + 1) \\/ 2",
    'tf_b_calc': "(e^(x^2))' = 2x e^(x^2) coral(!=) x e^(x^2)",
    'tf_d_calc': "F = 1/2 e^(x^2) + C, quad 1/2 + C = 1 arrow.double.long C = 1/2",
    'sa_task': "F'(x) = cos x sin^2 x, quad F(0) = 0, quad F(pi/2) approx ?",
    'sa_s1': "u = sin x, quad dif u = cos x dif x arrow.double.long F(x) = (sin^3 x)/3 + C",
    'sa_s2': "C = 0 arrow.double.long F(pi/2) = 1/3 approx gold(\"0,33\")",
    'chk': "(1/2 e^(x^2))' = x e^(x^2) quad checkmark",
    'sum1': "integral f(u) u' dif x = F(u) + C",
    'sum2': "u arrow.r dif u arrow.r integral f(u) dif u arrow.r x",
    'sum3': "x dif x = (dif u)/2",
    'hw1': "integral 3x^2 (x^3 + 1)^4 dif x",
    'hw2': "integral (cos x)/(sin x + 2) dif x",
    'hw3': "integral (ln^2 x)/x dif x",
    'hw_ans1': "(x^3 + 1)^5/5 + C",
    'hw_ans2': "ln(sin x + 2) + C",
    'hw_ans3': "(ln^3 x)/3 + C",
    'next1': "integral u dif v = u v - integral v dif u",
    'next2': "integral x e^x dif x = x e^x - e^x + C",
}

EXERCISES = (
    ('Tìm ∫3x²(x³ + 1)⁴ dx.', '(x³ + 1)⁵/5 + C'),
    ('Tìm ∫cos x/(sin x + 2) dx.', 'ln(sin x + 2) + C'),
    ('Tìm ∫ln²x/x dx.', 'ln³x/3 + C'),
)

TRUE_FALSE = (
    ('u = x² ⇒ du = 2x dx', True),
    ('∫f(x)dx = e^(x²) + C', False),
    ('∫f(x)dx = (1/2)e^(x²) + C', True),
    ('F(0) = 1 ⇒ F(1) = (e + 1)/2', True),
)

x, C = sp.symbols('x C', real=True)
P = sp.symbols('P', positive=True)


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

    e, s, c, ln, sq = sp.exp, sp.sin, sp.cos, sp.log, sp.sqrt
    assert same_primitive(e(x**2), 2*x*e(x**2))
    assert sp.diff(x**2, x) == 2*x
    assert same_primitive((x**2 + 1)**6/12, x*(x**2 + 1)**5)
    assert same_primitive(-c(x)**4/4, s(x)*c(x)**3)
    assert same_primitive(ln(P)**2/2, ln(P)/P, P)
    assert same_primitive(ln(e(x) + 1), e(x)/(e(x) + 1))
    assert same_primitive((x**2 + 3)**sp.Rational(3, 2)/3, x*sq(x**2 + 3))
    assert same_primitive(-2*c(sq(P)), s(sq(P))/sq(P), P)
    # true / false
    f = x*e(x**2)
    F = e(x**2)/2
    cF = sp.solve(sp.Eq(F.subs(x, 0) + C, 1), C)[0]
    claims = (
        sp.diff(x**2, x) == 2*x,
        same_primitive(e(x**2), f),
        same_primitive(F, f),
        sp.simplify((F + cF).subs(x, 1) - (sp.E + 1)/2) == 0,
    )
    assert claims == tuple(ans for _, ans in TRUE_FALSE) and cF == sp.Rational(1, 2)
    # short answer
    Fs = s(x)**3/3
    assert same_primitive(Fs, c(x)*s(x)**2) and Fs.subs(x, 0) == 0 and Fs.subs(x, sp.pi/2) == sp.Rational(1, 3)
    assert round(1/3, 2) == 0.33
    # exercises
    assert same_primitive((x**3 + 1)**5/5, 3*x**2*(x**3 + 1)**4)
    assert same_primitive(ln(s(x) + 2), c(x)/(s(x) + 2))
    assert same_primitive(ln(P)**3/3, ln(P)**2/P, P)
    # teaser
    assert same_primitive(x*e(x) - e(x), x*e(x))
    return True


validate()

"""INT07 – Nguyên hàm phân thức hữu tỉ: chia đa thức & tách phân thức (mở rộng).

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT07',
    'number': 7,
    'title': 'Nguyên hàm phân thức hữu tỉ',
    'subtitle': 'Chia đa thức & tách phân thức',
    'next_code': 'INT08',
    'next_title': 'Phương pháp đổi biến số',
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
         'Nguyên hàm của x bình phương cộng một, chia cho x trừ một. Hàm này không có trong bảng nguyên hàm, '
         'và cũng không phải tổng các lũy thừa đơn giản. Nhưng chỉ với hai công cụ là chia đa thức và tách phân thức, '
         'ta sẽ đưa mọi phân thức như vậy về các hạng tử quen thuộc trong bảng.',
         'Mở đầu: phân thức không có trong bảng'),
    Beat('h2', 'hook',
         'Đây là tập bảy của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: nguyên hàm phân thức hữu tỉ. '
         'Đây là nội dung mở rộng, ngoài chương trình bắt buộc, rất hữu ích cho học sinh giỏi và các kỳ thi đánh giá năng lực.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ có ba kỹ năng. Một, chia đa thức khi bậc của tử lớn hơn hoặc bằng bậc của mẫu. '
         'Hai, tách phân thức thành các phân thức đơn giản bằng hệ số bất định và mẹo che nghiệm. '
         'Ba, nhận ra dạng tử số là đạo hàm của mẫu số.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Bước đầu tiên luôn là so sánh bậc. Nếu bậc của tử nhỏ hơn bậc của mẫu, phân thức gọi là thực sự, ta tách ngay. '
         'Nếu bậc của tử lớn hơn hoặc bằng bậc của mẫu, ta phải chia đa thức trước, giống như đổi phân số tối giản '
         'thành hỗn số.',
         'Bước 1: so sánh bậc và chia đa thức'),
    Beat('c2', 'core',
         'Với x bình phương cộng một chia x trừ một: viết x bình phương cộng một bằng x trừ một nhân x cộng một, cộng hai. '
         'Vậy phân thức bằng x cộng một cộng hai chia x trừ một. Bây giờ mọi hạng tử đều có trong bảng: '
         'nguyên hàm là x bình phương chia hai cộng x cộng hai lô ga nê pe trị tuyệt đối x trừ một, cộng C.'),
    Beat('c3', 'core',
         'Trường hợp tử và mẫu cùng bậc một, ví dụ hai x cộng ba chia x cộng một. Tách tử theo mẫu: hai x cộng ba bằng '
         'hai nhân x cộng một, cộng một. Phân thức bằng hai cộng một chia x cộng một, và nguyên hàm là hai x cộng '
         'lô ga nê pe trị tuyệt đối x cộng một, cộng C.'),
    Beat('c4', 'core',
         'Bước hai: tách phân thức thực sự. Với mẫu có hai nghiệm phân biệt, ví dụ x trừ một nhân x cộng hai, '
         'ta tách một chia tích đó thành hiệu hai phân thức đơn giản, nhân với một phần ba. '
         'Quy đồng lại để kiểm tra: tử số đúng bằng một.',
         'Bước 2: tách phân thức'),
    Beat('c5', 'core',
         'Tổng quát, dùng hệ số bất định. Viết ba x cộng một chia x trừ một nhân x cộng một bằng A chia x trừ một, '
         'cộng B chia x cộng một. Quy đồng: ba x cộng một bằng A nhân x cộng một, cộng B nhân x trừ một. '
         'Thay x bằng một: bốn bằng hai A, nên A bằng hai. Thay x bằng âm một: âm hai bằng âm hai B, nên B bằng một.'),
    Beat('c6', 'core',
         'Vậy nguyên hàm bằng hai lô ga nê pe trị tuyệt đối x trừ một cộng lô ga nê pe trị tuyệt đối x cộng một, cộng C. '
         'Mẹo nhanh, gọi là che nghiệm: muốn tìm A, che thừa số x trừ một ở mẫu, rồi thay x bằng một vào phần còn lại. '
         'Ba nhân một cộng một, chia một cộng một, bằng hai.'),
    Beat('c7', 'core',
         'Khi mẫu có nghiệm kép, ví dụ x trừ một tất cả bình phương, ta tách thành A chia x trừ một cộng B chia x trừ một '
         'bình phương. Với x chia x trừ một bình phương: x bằng x trừ một cộng một, nên được một chia x trừ một cộng '
         'một chia x trừ một bình phương. Nguyên hàm là lô ga nê pe trị tuyệt đối x trừ một, trừ một chia x trừ một, cộng C.',
         'Mẫu có nghiệm kép'),
    Beat('c8', 'core',
         'Một dạng đặc biệt cần nhận ra ngay: tử số là đạo hàm của mẫu số. Vì đạo hàm của lô ga nê pe trị tuyệt đối u '
         'bằng u phẩy chia u, nên nguyên hàm của u phẩy chia u là lô ga nê pe trị tuyệt đối u cộng C. '
         'Ví dụ, nguyên hàm của hai x chia x bình phương cộng một là lô ga nê pe của x bình phương cộng một.',
         'Tử số là đạo hàm của mẫu'),
    Beat('c9', 'core',
         'Tổng hợp thành sơ đồ quyết định. Bậc tử lớn hơn hoặc bằng bậc mẫu: chia đa thức. Tử là đạo hàm của mẫu: '
         'lô ga nê pe ngay. Mẫu có nghiệm phân biệt: tách A, B. Mẫu có nghiệm kép: thêm hạng tử bình phương.',
         'Sơ đồ quyết định'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: nguyên hàm của x lập phương trừ x cộng hai, chia x cộng một. Bậc tử lớn hơn, nên chia đa thức: '
         'x lập phương trừ x cộng hai bằng x cộng một nhân x bình phương trừ x, cộng hai. Nguyên hàm là x lập phương '
         'chia ba, trừ x bình phương chia hai, cộng hai lô ga nê pe trị tuyệt đối x cộng một, cộng C.',
         'Ví dụ 1: chia đa thức'),
    Beat('e2', 'examples',
         'Ví dụ hai: nguyên hàm của năm x trừ một chia x bình phương trừ x trừ hai. Mẫu bằng x trừ hai nhân x cộng một. '
         'Che nghiệm: A bằng năm nhân hai trừ một, chia hai cộng một, bằng ba. B bằng âm năm trừ một, chia âm một trừ hai, '
         'bằng hai. Kết quả: ba lô ga nê pe trị tuyệt đối x trừ hai cộng hai lô ga nê pe trị tuyệt đối x cộng một, cộng C.',
         'Ví dụ 2: tách bằng mẹo che nghiệm'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f của x bằng hai x cộng một, chia x bình phương cộng x, trên khoảng dương. '
         'F là một nguyên hàm của f. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: quy đồng một chia x cộng một chia x cộng một, được đúng hai x cộng một chia x nhân x cộng một. '
         'Ý b đúng: tử số hai x cộng một chính là đạo hàm của mẫu x bình phương cộng x.'),
    Beat('x3', 'exam',
         'Ý c sai: đây là cái bẫy nhân hai lô ga rít. Tổng hai lô ga rít là lô ga rít của tích, không phải tích hai lô ga rít. '
         'Ý d đúng: F của một bằng lô ga nê pe hai cộng C bằng lô ga nê pe hai nên C bằng không, '
         'và F của hai bằng lô ga nê pe sáu.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. F là nguyên hàm của một chia x nhân x cộng một trên khoảng dương, F của một bằng không. '
         'Tính F của hai, làm tròn đến hàng phần trăm. Tách: một chia x trừ một chia x cộng một. F bằng lô ga nê pe '
         'của x chia x cộng một, cộng C, và C bằng lô ga nê pe hai. Vậy F của hai bằng lô ga nê pe bốn phần ba, '
         'xấp xỉ không phẩy hai chín.',
         'Trả lời ngắn và mẹo che nghiệm'),
    Beat('x5', 'exam',
         'Mẹo che nghiệm, nhắc lại từng bước. Muốn tìm hệ số ứng với nghiệm a: che thừa số x trừ a ở mẫu, '
         'thay x bằng a vào phần còn lại. Chỉ mất vài giây cho mỗi hệ số, và chỉ dùng được khi các nghiệm phân biệt.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, bậc tử lớn hơn hoặc bằng bậc mẫu thì chia đa thức trước. Hai, mẫu phân tích được thì tách '
         'thành các phân thức đơn giản, dùng hệ số bất định hoặc che nghiệm. Ba, tử là đạo hàm của mẫu thì ra '
         'lô ga nê pe trị tuyệt đối mẫu ngay.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, nguyên hàm của x bình phương cộng x cộng một, chia x cộng một. '
         'Hai, nguyên hàm của một chia x bình phương trừ bốn. Ba, nguyên hàm của hai x chia x bình phương cộng ba. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập tám, ta học phương pháp đổi biến số, công cụ mạnh nhất để xử lý các hàm hợp phức tạp. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "integral (x^2 + 1)/(x - 1) dif x = gold(?)",
    'div1': "x^2 + 1 = (x - 1)(x + 1) + 2",
    'div2': "(x^2 + 1)/(x - 1) = x + 1 + 2/(x - 1)",
    'div3': "integral (x^2 + 1)/(x - 1) dif x = x^2/2 + x + 2 ln|x - 1| + C",
    'lin1': "2x + 3 = 2(x + 1) + 1",
    'lin2': "integral (2x + 3)/(x + 1) dif x = integral (2 + 1/(x + 1)) dif x = 2x + ln|x + 1| + C",
    'sep1': "1/((x - 1)(x + 2)) = 1/3 (1/(x - 1) - 1/(x + 2))",
    'sep_chk': "1/(x - 1) - 1/(x + 2) = ((x + 2) - (x - 1))/((x - 1)(x + 2)) = 3/((x - 1)(x + 2))",
    'sep2': "integral 1/((x - 1)(x + 2)) dif x = 1/3 ln|(x - 1)/(x + 2)| + C",
    'ab1': "(3x + 1)/((x - 1)(x + 1)) = A/(x - 1) + B/(x + 1)",
    'ab2': "3x + 1 = A(x + 1) + B(x - 1)",
    'ab3': "x = 1: 4 = 2A arrow.double.long A = gold(2), quad x = -1: -2 = -2B arrow.double.long B = gold(1)",
    'ab4': "integral (3x + 1)/(x^2 - 1) dif x = 2 ln|x - 1| + ln|x + 1| + C",
    'cover': "A = lr((3x + 1)/(x + 1) |)_(x = 1) = 4/2 = 2",
    'dbl1': "x/(x - 1)^2 = ((x - 1) + 1)/(x - 1)^2 = 1/(x - 1) + 1/(x - 1)^2",
    'dbl2': "integral x/(x - 1)^2 dif x = ln|x - 1| - 1/(x - 1) + C",
    'dlog1': "(ln|u|)' = (u')/u arrow.double.long integral (u')/u dif x = ln|u| + C",
    'dlog2': "integral (2x)/(x^2 + 1) dif x = ln(x^2 + 1) + C",
    'e1_task': "integral (x^3 - x + 2)/(x + 1) dif x",
    'e1_s1': "x^3 - x + 2 = (x + 1)(x^2 - x) + 2",
    'e1_s2': "= x^3/3 - x^2/2 + 2 ln|x + 1| + C",
    'e2_task': "integral (5x - 1)/(x^2 - x - 2) dif x, quad x^2 - x - 2 = (x - 2)(x + 1)",
    'e2_s1': "A = lr((5x - 1)/(x + 1) |)_(x = 2) = 9/3 = 3, quad B = lr((5x - 1)/(x - 2) |)_(x = -1) = (-6)/(-3) = 2",
    'e2_s2': "= 3 ln|x - 2| + 2 ln|x + 1| + C",
    'tf_f': "f(x) = (2x + 1)/(x^2 + x), quad x > 0",
    'tf_a': "(2x + 1) \\/ (x^2 + x) = 1 \\/ x + 1 \\/ (x + 1)",
    'tf_b': "integral f(x) dif x = ln(x^2 + x) + C",
    'tf_c': "integral f(x) dif x = ln x dot ln(x + 1) + C",
    'tf_d': "F(1) = ln 2 arrow.double.long F(2) = ln 6",
    'tf_c_calc': "ln x + ln(x + 1) = ln(x(x + 1)) coral(!=) ln x dot ln(x + 1)",
    'tf_d_calc': "F = ln(x^2 + x) + C, quad ln 2 + C = ln 2 arrow.double.long C = 0, quad F(2) = ln 6",
    'sa_task': "F'(x) = 1/(x(x + 1)), quad x > 0, quad F(1) = 0, quad F(2) approx ?",
    'sa_s1': "1/(x(x + 1)) = 1/x - 1/(x + 1) arrow.double.long F(x) = ln x/(x + 1) + C",
    'sa_s2': "F(1) = ln 1/2 + C = 0 arrow.double.long C = ln 2",
    'sa_s3': "F(2) = ln 2/3 + ln 2 = ln 4/3 approx gold(\"0,29\")",
    'cover_rule': "A_a = lr((P(x))/(Q(x)/(x - a)) |)_(x = a)",
    'sum1': "(x^2 + 1)/(x - 1) = x + 1 + 2/(x - 1)",
    'sum2': "A/(x - a) + B/(x - b)",
    'sum3': "integral (u')/u dif x = ln|u| + C",
    'hw1': "integral (x^2 + x + 1)/(x + 1) dif x",
    'hw2': "integral 1/(x^2 - 4) dif x",
    'hw3': "integral (2x)/(x^2 + 3) dif x",
    'hw_ans1': "x^2/2 + ln|x + 1| + C",
    'hw_ans2': "1/4 ln|(x - 2)/(x + 2)| + C",
    'hw_ans3': "ln(x^2 + 3) + C",
    'next1': "integral 2x e^(x^2) dif x, quad u = x^2, quad dif u = 2x dif x",
    'next2': "integral e^u dif u = e^u + C = e^(x^2) + C",
}

EXERCISES = (
    ('Tìm ∫(x² + x + 1)/(x + 1) dx.', 'x²/2 + ln|x + 1| + C'),
    ('Tìm ∫1/(x² − 4) dx.', '(1/4) ln|(x − 2)/(x + 2)| + C'),
    ('Tìm ∫2x/(x² + 3) dx.', 'ln(x² + 3) + C'),
)

TRUE_FALSE = (
    ('(2x + 1)/(x² + x) = 1/x + 1/(x + 1)', True),
    ('∫f(x)dx = ln(x² + x) + C', True),
    ('∫f(x)dx = ln x · ln(x + 1) + C', False),
    ('F(1) = ln 2 ⇒ F(2) = ln 6', True),
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

    ln = sp.log
    # division
    assert sp.expand((x - 1)*(x + 1) + 2) == x**2 + 1
    assert sp.simplify((x**2 + 1)/(x - 1) - (x + 1 + 2/(x - 1))) == 0
    assert same_primitive(x**2/2 + x + 2*ln(x - 1), (x**2 + 1)/(x - 1))
    assert sp.expand(2*(x + 1) + 1) == 2*x + 3 and same_primitive(2*x + ln(x + 1), (2*x + 3)/(x + 1))
    # separation
    assert sp.simplify(1/((x - 1)*(x + 2)) - (1/(x - 1) - 1/(x + 2))/3) == 0
    assert same_primitive(ln((x - 1)/(x + 2))/3, 1/((x - 1)*(x + 2)))
    a, b = sp.symbols('a b')
    sol = sp.solve([sp.Eq((3*x + 1).subs(x, 1), (a*(x + 1) + b*(x - 1)).subs(x, 1)),
                    sp.Eq((3*x + 1).subs(x, -1), (a*(x + 1) + b*(x - 1)).subs(x, -1))], [a, b])
    assert sol == {a: 2, b: 1}
    assert sp.simplify((3*x + 1)/(x**2 - 1) - (2/(x - 1) + 1/(x + 1))) == 0
    assert same_primitive(2*ln(x - 1) + ln(x + 1), (3*x + 1)/(x**2 - 1))
    assert ((3*x + 1)/(x + 1)).subs(x, 1) == 2  # cover-up
    # double root
    assert sp.simplify(x/(x - 1)**2 - (1/(x - 1) + 1/(x - 1)**2)) == 0
    assert same_primitive(ln(x - 1) - 1/(x - 1), x/(x - 1)**2)
    # u'/u
    assert same_primitive(ln(x**2 + 1), 2*x/(x**2 + 1))
    # example 1
    assert sp.expand((x + 1)*(x**2 - x) + 2) == x**3 - x + 2
    assert same_primitive(x**3/3 - x**2/2 + 2*ln(x + 1), (x**3 - x + 2)/(x + 1))
    # example 2 (cover-up values)
    assert sp.factor(x**2 - x - 2) == (x - 2)*(x + 1)
    assert ((5*x - 1)/(x + 1)).subs(x, 2) == 3 and ((5*x - 1)/(x - 2)).subs(x, -1) == 2
    assert same_primitive(3*ln(x - 2) + 2*ln(x + 1), (5*x - 1)/(x**2 - x - 2))
    # true / false on (0, +inf)
    f = (2*P + 1)/(P**2 + P)
    Fb = ln(P**2 + P)
    cF = sp.solve(sp.Eq(Fb.subs(P, 1) + C, ln(2)), C)[0]
    claims = (
        sp.simplify(f - (1/P + 1/(P + 1))) == 0,
        same_primitive(Fb, f, P),
        same_primitive(ln(P)*ln(P + 1), f, P),
        cF == 0 and sp.simplify(Fb.subs(P, 2) - ln(6)) == 0,
    )
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    Fs = ln(P/(P + 1)) + C
    cs = sp.solve(sp.Eq(Fs.subs(P, 1), 0), C)[0]
    v = Fs.subs(C, cs).subs(P, 2)
    assert same_primitive(Fs, 1/(P*(P + 1)), P) and sp.simplify(cs - ln(2)) == 0
    assert sp.simplify(v - ln(sp.Rational(4, 3))) == 0 and round(float(v), 2) == 0.29
    # exercises
    assert sp.expand(x*(x + 1) + 1) == x**2 + x + 1
    assert same_primitive(x**2/2 + ln(x + 1), (x**2 + x + 1)/(x + 1))
    assert same_primitive(ln((x - 2)/(x + 2))/4, 1/(x**2 - 4))
    assert same_primitive(ln(x**2 + 3), 2*x/(x**2 + 3))
    # teaser
    assert same_primitive(sp.exp(x**2), 2*x*sp.exp(x**2))
    return True


validate()

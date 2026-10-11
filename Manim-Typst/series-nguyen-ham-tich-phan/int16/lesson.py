"""INT16 – Tích phân đổi biến số: đổi biến phải đổi cận.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT16',
    'number': 16,
    'title': 'Tích phân đổi biến số',
    'subtitle': 'Đổi biến phải đổi cận',
    'next_code': 'INT17',
    'next_title': 'Tích phân từng phần',
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
         'Tính tích phân từ không đến một của hai x nhân x bình phương cộng một, tất cả mũ ba. '
         'Một bạn đặt u bằng x bình phương cộng một, viết lại thành tích phân từ không đến một của u mũ ba, '
         'và được một phần tư. Sai rồi! Đáp số đúng là mười lăm phần tư, gấp mười lăm lần. Lỗi nằm ở đâu?',
         'Mở đầu: đổi biến nhưng quên đổi cận'),
    Beat('h2', 'hook',
         'Đây là tập mười sáu của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân đổi biến số.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, công thức đổi biến và vì sao phải đổi cận. '
         'Hai, quy trình bốn bước với bảng đổi cận. Ba, đổi biến lượng giác cho căn của một trừ x bình phương.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Công thức đổi biến: tích phân từ a đến b của f của u của x, nhân u phẩy x, d x, bằng tích phân từ u của a '
         'đến u của b của f của u, d u. Nó đến từ quy tắc đạo hàm hàm hợp mà ta đã gặp ở phần nguyên hàm.',
         'Công thức đổi biến'),
    Beat('c2', 'core',
         'Vì sao cận thay đổi? Biến x chạy từ không đến một. Khi đó u bằng x bình phương cộng một chạy từ một đến hai. '
         'Tích phân mới tính theo u, nên cận phải là giá trị của u, không phải giá trị của x.'),
    Beat('c3', 'core',
         'Nhìn bằng hình: diện tích dưới đồ thị hai x nhân x bình phương cộng một mũ ba trên đoạn từ không đến một, '
         'bằng đúng diện tích dưới đồ thị u mũ ba trên đoạn từ một đến hai. Miền lấy tích phân bị co giãn và dịch chuyển, '
         'nhưng diện tích được giữ nguyên, đều bằng mười lăm phần tư.',
         'Miền tích phân co giãn theo u'),
    Beat('c4', 'core',
         'Quy trình bốn bước. Một, chọn u, thường là biểu thức bên trong hàm hợp. Hai, tính d u theo d x. '
         'Ba, lập bảng đổi cận: x bằng a thì u bằng bao nhiêu, x bằng b thì u bằng bao nhiêu. '
         'Bốn, tính tích phân mới theo u, và không cần thay lại x.',
         'Quy trình bốn bước'),
    Beat('c5', 'core',
         'Áp dụng cho bài mở đầu. Đặt u bằng x bình phương cộng một, d u bằng hai x d x. '
         'x bằng không thì u bằng một, x bằng một thì u bằng hai. Tích phân trở thành tích phân từ một đến hai '
         'của u mũ ba, bằng u mũ bốn phần bốn lấy cận, bằng mười sáu trừ một, chia bốn, bằng mười lăm phần tư.'),
    Beat('c6', 'core',
         'Cách khác: tìm nguyên hàm theo x, là x bình phương cộng một, mũ bốn, chia bốn, rồi thay cận không và một. '
         'Kết quả vẫn là mười lăm phần tư. Hai cách đều đúng. Lỗi chỉ xảy ra khi trộn hai cách: '
         'đã chuyển sang u mà vẫn giữ cận của x.'),
    Beat('c7', 'core',
         'Dấu hiệu chọn u: trong tích phân có một hàm hợp, và đạo hàm của phần bên trong xuất hiện làm thừa số. '
         'Gặp cốt x đi cùng hàm của sin x, đặt u bằng sin x. Gặp một chia x đi cùng hàm của l n x, đặt u bằng l n x. '
         'Gặp x đi cùng hàm của x bình phương, đặt u bằng x bình phương. Thiếu hệ số thì bù bằng một hằng số.',
         'Dấu hiệu chọn u'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: tích phân từ không đến pi phần hai của sin bình phương x nhân cốt x. '
         'Đặt u bằng sin x, d u bằng cốt x d x. x bằng không thì u bằng không, x bằng pi phần hai thì u bằng một. '
         'Tích phân bằng tích phân từ không đến một của u bình phương, bằng một phần ba.',
         'Ví dụ 1: đặt u = sin x'),
    Beat('e2', 'examples',
         'Ví dụ hai: tích phân từ một đến e của l n x chia x. Đặt u bằng l n x, d u bằng d x chia x. '
         'Cận mới: x bằng một thì u bằng không, x bằng e thì u bằng một. Kết quả là tích phân từ không đến một của u, '
         'bằng một phần hai.',
         'Ví dụ 2: đặt u = ln x'),
    Beat('e3', 'examples',
         'Ví dụ ba: tích phân từ không đến một của x nhân e mũ x bình phương. Đặt u bằng x bình phương, '
         'd u bằng hai x d x, nên x d x bằng một nửa d u. Cận mới từ không đến một. '
         'Kết quả: một phần hai nhân e trừ một.',
         'Ví dụ 3: hệ số một nửa'),
    Beat('e3b', 'examples',
         'Chú ý: cận mới có thể bị đảo chiều. Với tích phân từ không đến một của x nhân một trừ x bình phương, mũ ba, '
         'đặt u bằng một trừ x bình phương thì x bằng không cho u bằng một, x bằng một cho u bằng không. '
         'Cứ giữ đúng thứ tự: tích phân từ một đến không của trừ một nửa u mũ ba, bằng một phần tám. Đừng tự ý đổi chỗ cận.',
         'Cận mới bị đảo chiều'),
    Beat('e4', 'examples',
         'Ví dụ bốn, đổi biến lượng giác: tích phân từ không đến một của căn một trừ x bình phương. '
         'Đặt x bằng sin t, d x bằng cốt t d t, cận mới từ không đến pi phần hai. Căn một trừ sin bình phương là cốt t, '
         'nên tích phân bằng tích phân của cốt bình phương t, bằng pi phần tư.',
         'Ví dụ 4: đổi biến lượng giác'),
    Beat('e5', 'examples',
         'Kết quả pi phần tư có ý nghĩa hình học rất đẹp: đồ thị y bằng căn một trừ x bình phương là nửa trên đường tròn '
         'bán kính một. Từ không đến một, miền dưới đồ thị là một phần tư hình tròn, diện tích đúng bằng pi phần tư.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho I bằng tích phân từ không đến hai của hai x chia x bình phương cộng một. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: đặt u bằng x bình phương cộng một thì d u bằng hai x d x. '
         'Ý b sai: đây chính là bẫy giữ nguyên cận cũ. Cận đúng là từ một đến năm.'),
    Beat('x3', 'exam',
         'Ý c đúng: tích phân từ một đến năm của một chia u bằng l n năm. '
         'Ý d đúng: l n năm xấp xỉ một phẩy sáu một, nhỏ hơn hai.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: tính tích phân từ không đến căn ba của x nhân căn x bình phương cộng một, '
         'làm tròn đến hàng phần trăm. Đặt u bằng x bình phương cộng một, cận mới từ một đến bốn, '
         'và x d x bằng một nửa d u.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Tích phân bằng một nửa nhân tích phân từ một đến bốn của căn u, bằng một phần ba nhân u mũ ba phần hai lấy cận, '
         'bằng một phần ba nhân tám trừ một, bằng bảy phần ba, xấp xỉ hai phẩy ba ba. Ghi vào phiếu: hai, phẩy, ba, ba.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, công thức đổi biến: đổi cả hàm, cả vi phân và cả cận. '
         'Hai, quy trình bốn bước với bảng đổi cận, không cần quay về x. '
         'Ba, gặp căn một trừ x bình phương, hãy nghĩ đến đặt x bằng sin t.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tích phân từ không đến một của ba x bình phương nhân x lập phương cộng một, bình phương. '
         'Hai, tích phân từ không đến pi phần hai của cốt x nhân e mũ sin x. '
         'Ba, tích phân từ không đến l n hai của e mũ x chia e mũ x cộng một. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập mười bảy, ta học tích phân từng phần, công cụ cho tích của hai loại hàm khác nhau như x nhân e mũ x. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "integral_0^1 2x(x^2 + 1)^3 dif x = gold(?)",
    'hook_wrong': "u = x^2 + 1: quad integral_0^1 u^3 dif u = 1/4 quad coral(times)",
    'hook_right': "integral_1^2 u^3 dif u = 15/4 quad green(checkmark)",
    'sub': "integral_a^b f(u(x)) u'(x) dif x = integral_(u(a))^(u(b)) f(u) dif u",
    'bounds': "x: 0 arrow.r 1 quad arrow.double.long quad u = x^2 + 1: 1 arrow.r 2",
    'eq_area': "integral_0^1 2x(x^2 + 1)^3 dif x = integral_1^2 u^3 dif u = 15/4",
    'c5_s1': "u = x^2 + 1, quad dif u = 2x dif x",
    'c5_s2': "integral_0^1 2x(x^2 + 1)^3 dif x = integral_1^2 u^3 dif u = lr(u^4/4 |)_1^2 = (16 - 1)/4 = gold(15/4)",
    'c6_s1': "integral 2x(x^2 + 1)^3 dif x = (x^2 + 1)^4/4 + C",
    'c6_s2': "lr((x^2 + 1)^4/4 |)_0^1 = 16/4 - 1/4 = gold(15/4)",
    'e1_task': "integral_0^(pi\\/2) sin^2 x cos x dif x",
    'e1_s1': "u = sin x, quad dif u = cos x dif x",
    'e1_s2': "= integral_0^1 u^2 dif u = gold(1/3)",
    'e2_task': "integral_1^e (ln x)/x dif x",
    'e2_s1': "u = ln x, quad dif u = (dif x)/x",
    'e2_s2': "= integral_0^1 u dif u = gold(1/2)",
    'e3_task': "integral_0^1 x e^(x^2) dif x",
    'e3_s1': "u = x^2, quad x dif x = 1/2 dif u",
    'e3_s2': "= 1/2 integral_0^1 e^u dif u = gold((e - 1)/2)",
    'pat1': "integral f(sin x) cos x dif x: quad u = sin x",
    'pat2': "integral f(ln x) dot 1/x dif x: quad u = ln x",
    'pat3': "integral f(x^2) dot x dif x: quad u = x^2",
    'rev_task': "integral_0^1 x(1 - x^2)^3 dif x",
    'rev_s1': "u = 1 - x^2, quad x dif x = -1/2 dif u",
    'rev_s2': "= integral_1^0 (-1/2) u^3 dif u = 1/2 integral_0^1 u^3 dif u = gold(1/8)",
    'e4_task': "integral_0^1 sqrt(1 - x^2) dif x",
    'e4_s1': "x = sin t, quad dif x = cos t dif t, quad t: 0 arrow.r pi/2",
    'e4_s2': "= integral_0^(pi\\/2) cos^2 t dif t = integral_0^(pi\\/2) (1 + cos 2t)/2 dif t = gold(pi/4)",
    'e5': "S = (pi dot 1^2)/4 = pi/4",
    'tf_given': "I = integral_0^2 (2x)/(x^2 + 1) dif x",
    'tf_a': "u = x^2 + 1 arrow.double.long dif u = 2x dif x",
    'tf_b': "I = integral_0^2 1/u dif u",
    'tf_c': "I = ln 5",
    'tf_d': "I < 2",
    'tf_b_calc': "x = 0 arrow.r u = 1, quad x = 2 arrow.r u = 5: quad I = integral_1^5 1/u dif u",
    'tf_d_calc': "ln 5 approx \"1,61\" < 2",
    'sa_task': "integral_0^(sqrt(3)) x sqrt(x^2 + 1) dif x approx ?",
    'sa_s1': "u = x^2 + 1: quad 1 arrow.r 4, quad x dif x = 1/2 dif u",
    'sa_s2': "= 1/2 integral_1^4 sqrt(u) dif u = lr(1/3 u^(3\\/2) |)_1^4 = (8 - 1)/3 = 7/3 approx gold(\"2,33\")",
    'sum1': "integral_a^b f(u(x)) u' dif x = integral_(u(a))^(u(b)) f(u) dif u",
    'sum2': "x = a arrow.r u(a), quad x = b arrow.r u(b)",
    'sum3': "sqrt(1 - x^2): quad x = sin t",
    'hw1': "integral_0^1 3x^2 (x^3 + 1)^2 dif x",
    'hw2': "integral_0^(pi\\/2) cos x dot e^(sin x) dif x",
    'hw3': "integral_0^(ln 2) e^x/(e^x + 1) dif x",
    'hw_ans1': "7/3",
    'hw_ans2': "e - 1",
    'hw_ans3': "ln(3/2)",
    'next1': "integral_0^1 x e^x dif x",
    'next2': "integral u dif v = u v - integral v dif u",
}

EXERCISES = (
    ('∫₀¹ 3x²(x³ + 1)² dx', '7/3'),
    ('∫₀^(π/2) cos x · e^(sin x) dx', 'e − 1'),
    ('∫₀^(ln 2) eˣ/(eˣ + 1) dx', 'ln(3/2)'),
)

TRUE_FALSE = (
    ('u = x² + 1 ⇒ du = 2x dx', True),
    ('I = ∫₀² (1/u) du', False),
    ('I = ln 5', True),
    ('I < 2', True),
)

x, u, t = sp.symbols('x u t', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, pi = sp.integrate, sp.Rational, sp.pi
    # hook
    assert I(2*x*(x**2 + 1)**3, (x, 0, 1)) == R(15, 4) == I(u**3, (u, 1, 2))
    assert I(u**3, (u, 0, 1)) == R(1, 4)
    assert sp.simplify(sp.diff((x**2 + 1)**4 / 4, x) - 2*x*(x**2 + 1)**3) == 0
    assert R(16, 4) - R(1, 4) == R(15, 4)
    # examples
    assert I(sp.sin(x)**2 * sp.cos(x), (x, 0, pi / 2)) == R(1, 3) == I(u**2, (u, 0, 1))
    assert I(sp.log(x) / x, (x, 1, sp.E)) == R(1, 2) == I(u, (u, 0, 1))
    assert sp.simplify(I(x * sp.exp(x**2), (x, 0, 1)) - (sp.E - 1) / 2) == 0
    assert sp.simplify(I(sp.sqrt(1 - x**2), (x, 0, 1)) - pi / 4) == 0
    assert sp.simplify(I(sp.cos(t)**2, (t, 0, pi / 2)) - pi / 4) == 0
    assert I(x * (1 - x**2)**3, (x, 0, 1)) == R(1, 8) == I(-R(1, 2) * u**3, (u, 1, 0))
    # true / false
    Iv = I(2*x / (x**2 + 1), (x, 0, 2))
    claims = (sp.diff(x**2 + 1, x) == 2*x, I(1 / u, (u, 0, 2)) == Iv,
              sp.simplify(Iv - sp.log(5)) == 0, float(Iv) < 2)
    assert sp.simplify(I(1 / u, (u, 1, 5)) - Iv) == 0 and round(float(Iv), 2) == 1.61
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    val = I(x * sp.sqrt(x**2 + 1), (x, 0, sp.sqrt(3)))
    assert sp.simplify(val - R(7, 3)) == 0 and sp.simplify(R(1, 2) * I(sp.sqrt(u), (u, 1, 4)) - R(7, 3)) == 0
    assert f'{float(val):.2f}' == '2.33'
    # exercises
    assert I(3*x**2 * (x**3 + 1)**2, (x, 0, 1)) == R(7, 3)
    assert sp.simplify(I(sp.cos(x) * sp.exp(sp.sin(x)), (x, 0, pi / 2)) - (sp.E - 1)) == 0
    assert sp.simplify(I(sp.exp(x) / (sp.exp(x) + 1), (x, 0, sp.log(2))) - sp.log(R(3, 2))) == 0
    # next episode teaser
    assert I(x * sp.exp(x), (x, 0, 1)) == 1
    return True


validate()

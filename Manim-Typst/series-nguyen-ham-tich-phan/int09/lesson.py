"""INT09 – Phương pháp nguyên hàm từng phần: chọn u, dv & sơ đồ đường chéo (mở rộng).

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT09',
    'number': 9,
    'title': 'Nguyên hàm từng phần',
    'subtitle': 'Chọn u, dv & sơ đồ đường chéo',
    'next_code': 'INT10',
    'next_title': 'Từ tốc độ thay đổi đến đại lượng',
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
         'Nguyên hàm của x nhân e mũ x. Đây là tích của hai hàm khác loại: một đa thức và một hàm mũ. '
         'Không tách được như tổng, và đổi biến cũng bế tắc vì đạo hàm của phần bên trong không xuất hiện. '
         'Ta cần một công cụ mới, sinh ra từ quy tắc đạo hàm của một tích.',
         'Mở đầu: tích của hai hàm khác loại'),
    Beat('h2', 'hook',
         'Đây là tập chín của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: phương pháp nguyên hàm từng phần. '
         'Đây là nội dung mở rộng, dành cho học sinh giỏi và các kỳ thi đánh giá năng lực.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, công thức từng phần và ý nghĩa hình học bằng diện tích. '
         'Hai, quy tắc chọn u theo thứ tự nhất lô, nhì đa, tam lượng, tứ mũ. '
         'Ba, sơ đồ đường chéo để làm nhanh, và dạng lặp lại quay về chính nó.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Đạo hàm của tích u nhân v bằng u phẩy v cộng u v phẩy. Lấy nguyên hàm hai vế rồi chuyển vế, ta được công thức: '
         'nguyên hàm của u d v bằng u v trừ nguyên hàm của v d u. Ý tưởng là đổi một nguyên hàm khó '
         'thành một nguyên hàm dễ hơn.',
         'Công thức từng phần'),
    Beat('c2', 'core',
         'Ý nghĩa hình học rất đẹp. Vẽ đường cong trên mặt phẳng với trục ngang là v và trục đứng là u. '
         'Phần diện tích màu xanh, nằm dưới đường cong, chính là nguyên hàm của u d v. Phần màu vàng, nằm bên trái '
         'đường cong, là nguyên hàm của v d u. Hai phần ghép lại đúng bằng hiệu diện tích hai hình chữ nhật u v.',
         'Ý nghĩa hình học: ghép diện tích'),
    Beat('c3', 'core',
         'Bước quan trọng nhất là chọn u. Thứ tự ưu tiên để chọn u là: nhất lô, nhì đa, tam lượng, tứ mũ. '
         'Tức là lô ga rít trước, rồi đến đa thức, rồi lượng giác, cuối cùng là hàm mũ. Phần còn lại là d v.',
         'Chọn u: nhất lô, nhì đa, tam lượng, tứ mũ'),
    Beat('c4', 'core',
         'Áp dụng cho x nhân e mũ x. Đa thức đứng trước hàm mũ, nên đặt u bằng x, d v bằng e mũ x d x. '
         'Khi đó d u bằng d x và v bằng e mũ x. Công thức cho: x e mũ x trừ nguyên hàm của e mũ x, '
         'bằng x e mũ x trừ e mũ x cộng C.'),
    Beat('c5', 'core',
         'Nếu chọn ngược, u bằng e mũ x và d v bằng x d x, thì v bằng x bình phương chia hai, '
         'và nguyên hàm còn lại là x bình phương e mũ x chia hai: khó hơn bài ban đầu. '
         'Đó là lý do thứ tự chọn u rất quan trọng.'),
    Beat('c6', 'core',
         'Với nguyên hàm của lô ga nê pe x, tưởng như không có tích, nhưng ta coi d v bằng d x. '
         'Đặt u bằng lô ga nê pe x, d u bằng d x chia x, v bằng x. Kết quả là x lô ga nê pe x trừ x cộng C.',
         'Hai ví dụ kinh điển'),
    Beat('c7', 'core',
         'Với x nhân cốt x: đa thức đứng trước lượng giác, nên u bằng x, d v bằng cốt x d x, v bằng sin x. '
         'Được x sin x trừ nguyên hàm của sin x, tức là x sin x cộng cốt x cộng C.'),
    Beat('c8', 'core',
         'Khi đa thức có bậc cao, ví dụ x bình phương e mũ x, phải từng phần nhiều lần. Sơ đồ đường chéo giúp làm nhanh: '
         'cột trái lấy đạo hàm liên tiếp của x bình phương cho tới khi bằng không, cột phải lấy nguyên hàm liên tiếp '
         'của e mũ x. Nhân theo đường chéo với dấu cộng, trừ xen kẽ.',
         'Sơ đồ đường chéo'),
    Beat('c9', 'core',
         'Kết quả: x bình phương e mũ x, trừ hai x e mũ x, cộng hai e mũ x, cộng C. Một đa thức bậc n '
         'cần đúng n lần từng phần, tương ứng n đường chéo trước khi cột đạo hàm về không.'),
    Beat('c10', 'core',
         'Dạng chuyên sâu: nguyên hàm lặp lại. Với e mũ x nhân sin x, từng phần hai lần sẽ quay về chính nguyên hàm '
         'ban đầu, gọi là I. Ta được phương trình I bằng e mũ x sin x trừ e mũ x cốt x trừ I. '
         'Giải ra: I bằng e mũ x nhân sin x trừ cốt x, chia hai, cộng C.',
         'Dạng lặp lại'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: nguyên hàm của x lô ga nê pe x. Lô ga rít đứng đầu, nên u bằng lô ga nê pe x, d v bằng x d x, '
         'v bằng x bình phương chia hai. Kết quả là x bình phương lô ga nê pe x chia hai, trừ x bình phương chia bốn, cộng C.',
         'Ví dụ 1–2'),
    Beat('e2', 'examples',
         'Ví dụ hai: nguyên hàm của x sin hai x. Đặt u bằng x, v bằng âm cốt hai x chia hai. '
         'Kết quả là âm x cốt hai x chia hai, cộng sin hai x chia bốn, cộng C.'),
    Beat('e3', 'examples',
         'Ví dụ ba, dùng sơ đồ đường chéo: nguyên hàm của x lập phương e mũ x. Cột đạo hàm: x lập phương, ba x bình phương, '
         'sáu x, sáu, rồi không. Cột nguyên hàm toàn là e mũ x. Nhân chéo với dấu xen kẽ, ta được x lập phương e mũ x, '
         'trừ ba x bình phương e mũ x, cộng sáu x e mũ x, trừ sáu e mũ x, cộng C. Ba lần từng phần chỉ gói gọn trong một bảng.',
         'Ví dụ 3: sơ đồ đường chéo bậc ba'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f của x bằng x e mũ x. F là một nguyên hàm của f trên R. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: đây là cách chọn chuẩn theo thứ tự ưu tiên. Ý b sai: dấu cộng phải là dấu trừ. '
         'Lấy đạo hàm vế phải sẽ ra x e mũ x cộng hai e mũ x, không bằng f.'),
    Beat('x3', 'exam',
         'Ý c đúng: x e mũ x trừ e mũ x chính là e mũ x nhân x trừ một. Ý d sai: F của không bằng âm một cộng C '
         'bằng không nên C bằng một, và F của một bằng không cộng một, bằng một chứ không phải e.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. F là nguyên hàm của lô ga nê pe x trên khoảng dương, F của một bằng không. Tính F của hai, '
         'làm tròn đến hàng phần trăm. F bằng x lô ga nê pe x trừ x cộng C, F của một bằng âm một cộng C nên C bằng một. '
         'Vậy F của hai bằng hai lô ga nê pe hai trừ một, xấp xỉ không phẩy ba chín.',
         'Trả lời ngắn và mẹo kiểm tra'),
    Beat('x5', 'exam',
         'Mẹo kiểm tra: kết quả từng phần luôn có dạng u v trừ một phần bù. Lấy đạo hàm để kiểm tra, '
         'đặc biệt chú ý dấu. Phần lớn lỗi sai của từng phần nằm ở dấu trừ trước nguyên hàm thứ hai. '
         'Ví dụ, đạo hàm của x e mũ x trừ e mũ x bằng e mũ x cộng x e mũ x trừ e mũ x, còn lại đúng x e mũ x.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, nguyên hàm của u d v bằng u v trừ nguyên hàm của v d u. Hai, chọn u theo thứ tự nhất lô, '
         'nhì đa, tam lượng, tứ mũ. Ba, đa thức bậc cao dùng sơ đồ đường chéo, còn dạng lặp lại thì giải phương trình theo I.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, nguyên hàm của x e mũ hai x. Hai, nguyên hàm của lô ga nê pe của x cộng một. '
         'Ba, nguyên hàm của x bình phương cốt x, dùng sơ đồ đường chéo. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Tập mười sẽ khép lại phần nguyên hàm bằng các bài toán thực tế: từ tốc độ thay đổi tìm lại đại lượng, '
         'cùng một bài tổng ôn. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "integral x e^x dif x = gold(?)",
    'prod': "(u v)' = u' v + u v'",
    'parts': "integral u dif v = u v - integral v dif u",
    'area': "integral u dif v + integral v dif u = u_2 v_2 - u_1 v_1",
    'pick1': "u = x, quad dif v = e^x dif x arrow.double.long dif u = dif x, quad v = e^x",
    'pick2': "integral x e^x dif x = x e^x - integral e^x dif x = x e^x - e^x + C",
    'bad1': "u = e^x, quad dif v = x dif x arrow.double.long v = x^2/2",
    'bad2': "integral x e^x dif x = x^2/2 e^x - integral x^2/2 e^x dif x quad coral(\"?!\")",
    'ln1': "u = ln x, quad dif v = dif x arrow.double.long dif u = (dif x)/x, quad v = x",
    'ln2': "integral ln x dif x = x ln x - integral dif x = x ln x - x + C",
    'cos1': "u = x, quad dif v = cos x dif x arrow.double.long v = sin x",
    'cos2': "integral x cos x dif x = x sin x - integral sin x dif x = x sin x + cos x + C",
    'tab_res': "integral x^2 e^x dif x = x^2 e^x - 2x e^x + 2 e^x + C",
    'loop1': "I = integral e^x sin x dif x = e^x sin x - e^x cos x - I",
    'loop2': "I = (e^x (sin x - cos x))/2 + C",
    'e1_s1': "u = ln x, quad dif v = x dif x arrow.double.long v = x^2/2",
    'e1_s2': "integral x ln x dif x = (x^2 ln x)/2 - x^2/4 + C",
    'e2_s1': "u = x, quad dif v = sin 2x dif x arrow.double.long v = -(cos 2x)/2",
    'e2_s2': "integral x sin 2x dif x = -(x cos 2x)/2 + (sin 2x)/4 + C",
    'e3_tab': "x^3 arrow.r 3x^2 arrow.r 6x arrow.r 6 arrow.r 0, quad e^x, e^x, e^x, e^x",
    'e3_res': "integral x^3 e^x dif x = x^3 e^x - 3x^2 e^x + 6x e^x - 6 e^x + C",
    'tf_f': "f(x) = x e^x",
    'tf_a': "u = x, dif v = e^x dif x arrow.double.long dif u = dif x, v = e^x",
    'tf_b': "integral f(x) dif x = x e^x + e^x + C",
    'tf_c': "integral f(x) dif x = e^x (x - 1) + C",
    'tf_d': "F(0) = 0 arrow.double.long F(1) = e",
    'tf_b_calc': "(x e^x + e^x)' = x e^x + 2 e^x coral(!=) x e^x",
    'tf_d_calc': "F = e^x (x - 1) + C, quad -1 + C = 0 arrow.double.long C = 1, quad F(1) = 1",
    'sa_task': "F'(x) = ln x, quad x > 0, quad F(1) = 0, quad F(2) approx ?",
    'sa_s1': "F(x) = x ln x - x + C, quad F(1) = -1 + C = 0 arrow.double.long C = 1",
    'sa_s2': "F(2) = 2 ln 2 - 1 approx gold(\"0,39\")",
    'chk': "(x e^x - e^x)' = e^x + x e^x - e^x = x e^x",
    'sum1': "integral u dif v = u v - integral v dif u",
    'sum2': "ln x succ x^n succ sin x succ e^x",
    'sum3': "I = A - I arrow.double.long I = A/2",
    'hw1': "integral x e^(2x) dif x",
    'hw2': "integral ln(x + 1) dif x",
    'hw3': "integral x^2 cos x dif x",
    'hw_ans1': "(x e^(2x))/2 - e^(2x)/4 + C",
    'hw_ans2': "(x + 1) ln(x + 1) - x + C",
    'hw_ans3': "x^2 sin x + 2x cos x - 2 sin x + C",
    'next1': "v(t) = 3t^2 + 2 arrow.r.long s(t) = t^3 + 2t + C",
    'next2': "P'(t) = 50 e^(0.02 t) arrow.r.long P(t) = 2500 e^(0.02 t) + C",
}

EXERCISES = (
    ('Tìm ∫x e²ˣ dx.', 'x e²ˣ/2 − e²ˣ/4 + C'),
    ('Tìm ∫ln(x + 1) dx.', '(x + 1) ln(x + 1) − x + C'),
    ('Tìm ∫x² cos x dx.', 'x² sin x + 2x cos x − 2 sin x + C'),
)

TRUE_FALSE = (
    ('u = x, dv = eˣdx ⇒ du = dx, v = eˣ', True),
    ('∫f(x)dx = x eˣ + eˣ + C', False),
    ('∫f(x)dx = eˣ(x − 1) + C', True),
    ('F(0) = 0 ⇒ F(1) = e', False),
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

    e, s, c, ln = sp.exp, sp.sin, sp.cos, sp.log
    u, v = sp.Function('u')(x), sp.Function('v')(x)
    assert sp.simplify(sp.diff(u*v, x) - (sp.diff(u, x)*v + u*sp.diff(v, x))) == 0
    # area identity for u = sqrt(v), v in [1, 4]
    V = sp.symbols('V', positive=True)
    U = sp.symbols('U', positive=True)
    A1 = sp.integrate(sp.sqrt(V), (V, 1, 4))
    A2 = sp.integrate(U**2, (U, 1, 2))
    assert sp.simplify(A1 + A2 - (2*4 - 1*1)) == 0
    assert same_primitive(x*e(x) - e(x), x*e(x))
    assert same_primitive(P*ln(P) - P, ln(P), P)
    assert same_primitive(x*s(x) + c(x), x*c(x))
    assert same_primitive(x**2*e(x) - 2*x*e(x) + 2*e(x), x**2*e(x))
    assert same_primitive(e(x)*(s(x) - c(x))/2, e(x)*s(x))
    assert same_primitive(P**2*ln(P)/2 - P**2/4, P*ln(P), P)
    assert same_primitive(-x*c(2*x)/2 + s(2*x)/4, x*s(2*x))
    assert same_primitive(x**3*e(x) - 3*x**2*e(x) + 6*x*e(x) - 6*e(x), x**3*e(x))
    # true / false
    F = e(x)*(x - 1)
    cF = sp.solve(sp.Eq(F.subs(x, 0) + C, 0), C)[0]
    claims = (
        sp.diff(e(x), x) == e(x),
        same_primitive(x*e(x) + e(x), x*e(x)),
        same_primitive(F, x*e(x)),
        sp.simplify((F + cF).subs(x, 1) - sp.E) == 0,
    )
    assert claims == tuple(ans for _, ans in TRUE_FALSE) and (F + cF).subs(x, 1) == 1
    assert sp.expand(sp.diff(x*e(x) + e(x), x)) == x*e(x) + 2*e(x)
    # short answer
    Fs = P*ln(P) - P + 1
    assert Fs.subs(P, 1) == 0 and round(float(Fs.subs(P, 2)), 2) == 0.39
    # exercises
    assert same_primitive(x*e(2*x)/2 - e(2*x)/4, x*e(2*x))
    assert same_primitive((P + 1)*ln(P + 1) - P, ln(P + 1), P)
    assert same_primitive(x**2*s(x) + 2*x*c(x) - 2*s(x), x**2*c(x))
    # teaser
    assert same_primitive(2500*e(sp.Rational(1, 50)*x), 50*e(sp.Rational(1, 50)*x))
    return True


validate()

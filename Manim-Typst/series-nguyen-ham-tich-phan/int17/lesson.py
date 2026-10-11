"""INT17 – Tích phân từng phần: chọn u – dv theo thứ tự ưu tiên.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT17',
    'number': 17,
    'title': 'Tích phân từng phần',
    'subtitle': 'Chọn u – dv theo thứ tự ưu tiên',
    'next_code': 'INT18',
    'next_title': 'Tích phân hàm ẩn & tính đối xứng',
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
         'Tính tích phân từ không đến một của x nhân e mũ x. Không có bảng nguyên hàm nào cho tích này, '
         'và đổi biến số cũng không giúp được gì. Vậy mà đáp số lại gọn đến bất ngờ: đúng bằng một. '
         'Công cụ giúp ta làm điều đó là tích phân từng phần.',
         'Mở đầu: tích của hai loại hàm'),
    Beat('h2', 'hook',
         'Đây là tập mười bảy của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân từng phần.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, công thức từng phần và ý nghĩa hình học của nó. '
         'Hai, quy tắc chọn u: nhất log, nhì đa, tam lượng, tứ mũ. Ba, các dạng phải dùng từng phần hai lần.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Công thức xuất phát từ đạo hàm của tích: u nhân v, phẩy, bằng u phẩy v cộng u v phẩy. '
         'Lấy tích phân hai vế từ a đến b rồi chuyển vế, ta được: tích phân của u d v bằng u v lấy cận từ a đến b, '
         'trừ tích phân của v d u.',
         'Công thức từng phần'),
    Beat('c2', 'core',
         'Ý nghĩa hình học: vẽ đường cong với hoành độ u và tung độ v. Phần diện tích nằm giữa đường cong và trục tung '
         'là tích phân của u d v. Phần nằm giữa đường cong và trục hoành là tích phân của v d u. '
         'Hai phần ghép lại đúng bằng hình chữ nhật lớn trừ hình chữ nhật nhỏ, tức là u v lấy cận.',
         'Diện tích hình chữ nhật uv tách làm hai'),
    Beat('c3', 'core',
         'Muốn dùng công thức, ta tách biểu thức dưới dấu tích phân thành u nhân d v. Quy tắc chọn u theo thứ tự ưu tiên: '
         'nhất log, nhì đa, tam lượng, tứ mũ. Tức là ưu tiên chọn u là hàm logarit, rồi đến đa thức, rồi lượng giác, '
         'cuối cùng là hàm mũ. Phần còn lại là d v.',
         'Nhất log, nhì đa, tam lượng, tứ mũ'),
    Beat('c4', 'core',
         'Lý do: u được lấy đạo hàm nên cần trở nên đơn giản hơn. Logarit đạo hàm thành phân thức, đa thức giảm bậc. '
         'Còn d v được lấy nguyên hàm nên phải dễ tìm v, mà e mũ x hay sin, cốt thì nguyên hàm rất dễ.'),
    Beat('c5', 'core',
         'Áp dụng cho bài mở đầu. Đặt u bằng x, d v bằng e mũ x d x, suy ra d u bằng d x, v bằng e mũ x. '
         'Tích phân bằng x e mũ x lấy cận từ không đến một, trừ tích phân của e mũ x. '
         'Ta được e trừ, e trừ một, bằng một.'),
    Beat('c6', 'core',
         'Nếu chọn ngược, đặt u bằng e mũ x và d v bằng x d x, thì v bằng x bình phương phần hai, '
         'và tích phân mới chứa x bình phương nhân e mũ x, còn khó hơn bài ban đầu. '
         'Chọn sai thứ tự làm bài toán phức tạp thêm.',
         'Chọn ngược thì sao?'),
    Beat('c7', 'core',
         'Khi nào dùng từng phần, khi nào dùng đổi biến? Nếu thấy hàm hợp đi kèm đạo hàm của phần bên trong, hãy đổi biến. '
         'Nếu thấy tích của hai loại hàm khác nhau, như đa thức nhân hàm mũ, đa thức nhân lượng giác, '
         'hay logarit nhân đa thức, thì dùng từng phần. Ví dụ x nhân e mũ x bình phương là đổi biến, '
         'còn x nhân e mũ x là từng phần.',
         'Từng phần hay đổi biến?'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: tích phân từ một đến e của l n x. Chỉ có một hàm, ta vẫn dùng từng phần với u bằng l n x, d v bằng d x. '
         'd u bằng d x chia x, v bằng x. Kết quả: x l n x lấy cận, trừ tích phân của một, bằng e trừ, e trừ một, bằng một.',
         'Ví dụ 1: u = ln x'),
    Beat('e2', 'examples',
         'Ví dụ hai: tích phân từ không đến pi phần hai của x cốt x. Đa thức đứng trước lượng giác, nên u bằng x, '
         'd v bằng cốt x d x, v bằng sin x. Ta được x sin x lấy cận, bằng pi phần hai, trừ tích phân của sin x, bằng một. '
         'Kết quả: pi phần hai trừ một.',
         'Ví dụ 2: đa thức và lượng giác'),
    Beat('e3', 'examples',
         'Ví dụ ba: tích phân từ một đến e của x l n x. Logarit được ưu tiên, nên u bằng l n x, d v bằng x d x, '
         'v bằng x bình phương phần hai. Ta được e bình phương phần hai, trừ tích phân của x phần hai, '
         'bằng e bình phương trừ một, chia bốn. Kết quả: e bình phương cộng một, chia bốn.',
         'Ví dụ 3: logarit và đa thức'),
    Beat('e4', 'examples',
         'Ví dụ bốn: tích phân từ không đến một của x bình phương e mũ x. Từng phần lần một hạ x bình phương xuống hai x: '
         'được e trừ hai nhân tích phân của x e mũ x. Tích phân còn lại chính là bài mở đầu, bằng một. '
         'Kết quả: e trừ hai.',
         'Ví dụ 4: từng phần hai lần'),
    Beat('e4b', 'examples',
         'Mẹo trình bày nhanh cho đa thức nhân hàm mũ: sơ đồ đường chéo. Cột trái lấy đạo hàm liên tiếp của x bình phương: '
         'hai x, hai, rồi không. Cột phải lấy nguyên hàm liên tiếp của e mũ x. Nhân chéo với dấu cộng, trừ, cộng xen kẽ, '
         'ta có nguyên hàm x bình phương trừ hai x cộng hai, nhân e mũ x. Thay cận được e trừ hai, khớp với kết quả trên.',
         'Sơ đồ đường chéo'),
    Beat('e5', 'examples',
         'Dạng đặc biệt: tích phân của e mũ x nhân sin x. Từng phần hai lần, tích phân ban đầu xuất hiện lại ở vế phải. '
         'Coi nó là ẩn I rồi giải phương trình bậc nhất. Từ không đến pi, ta được I bằng e mũ pi cộng một, chia hai.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho I bằng tích phân từ không đến một của hai x cộng một, nhân e mũ x. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a sai: theo thứ tự ưu tiên, đa thức đứng trước hàm mũ, nên u là hai x cộng một. '
         'Ý b đúng: d u bằng hai d x, nên tích phân còn lại có hệ số hai.'),
    Beat('x3', 'exam',
         'Ý c đúng: ba e trừ một, trừ hai nhân e trừ một, bằng e cộng một. '
         'Ý d sai: e cộng một xấp xỉ ba phẩy bảy hai, nhỏ hơn bốn.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: tính tích phân từ không đến một của x nhân e mũ trừ x, làm tròn đến hàng phần trăm. '
         'Đặt u bằng x, d v bằng e mũ trừ x d x, suy ra v bằng trừ e mũ trừ x. Chú ý dấu trừ!',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Ta được trừ x e mũ trừ x lấy cận, bằng trừ một phần e, cộng tích phân của e mũ trừ x, bằng một trừ một phần e. '
         'Tổng là một trừ hai phần e, xấp xỉ không phẩy hai sáu. Ghi vào phiếu: không, phẩy, hai, sáu.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, công thức: tích phân u d v bằng u v lấy cận trừ tích phân v d u. '
         'Hai, chọn u theo thứ tự nhất log, nhì đa, tam lượng, tứ mũ. '
         'Ba, đa thức bậc cao thì từng phần nhiều lần, còn mũ nhân lượng giác thì giải phương trình theo I.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tích phân từ không đến pi của x sin x. Hai, tích phân từ một đến hai của x l n x. '
         'Ba, tích phân từ không đến một của x e mũ hai x. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập mười tám, ta học tích phân hàm ẩn và tính đối xứng, với phép đổi biến x thành a cộng b trừ x. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "integral_0^1 x e^x dif x = gold(?)",
    'hook_ans': "integral_0^1 x e^x dif x = gold(1)",
    'prod': "(u v)' = u' v + u v'",
    'parts': "integral_a^b u dif v = lr(u v |)_a^b - integral_a^b v dif u",
    'geo': "integral u dif v + integral v dif u = u_2 v_2 - u_1 v_1",
    'c5_s1': "u = x, quad dif v = e^x dif x arrow.double.long dif u = dif x, quad v = e^x",
    'c5_s2': "integral_0^1 x e^x dif x = lr(x e^x |)_0^1 - integral_0^1 e^x dif x = e - (e - 1) = gold(1)",
    'c6_s1': "u = e^x, quad dif v = x dif x arrow.double.long v = x^2/2",
    'c6_s2': "lr(x^2/2 e^x |)_0^1 - integral_0^1 x^2/2 e^x dif x quad coral(\"?!\")",
    'e1_task': "integral_1^e ln x dif x",
    'e1_s1': "u = ln x, quad dif v = dif x arrow.double.long dif u = (dif x)/x, quad v = x",
    'e1_s2': "= lr(x ln x |)_1^e - integral_1^e dif x = e - (e - 1) = gold(1)",
    'e2_task': "integral_0^(pi\\/2) x cos x dif x",
    'e2_s1': "u = x, quad dif v = cos x dif x arrow.double.long v = sin x",
    'e2_s2': "= lr(x sin x |)_0^(pi\\/2) - integral_0^(pi\\/2) sin x dif x = gold(pi/2 - 1)",
    'e3_task': "integral_1^e x ln x dif x",
    'e3_s1': "u = ln x, quad dif v = x dif x arrow.double.long v = x^2/2",
    'e3_s2': "= e^2/2 - integral_1^e x/2 dif x = e^2/2 - (e^2 - 1)/4 = gold((e^2 + 1)/4)",
    'e4_task': "integral_0^1 x^2 e^x dif x",
    'e4_s1': "= lr(x^2 e^x |)_0^1 - 2 integral_0^1 x e^x dif x = e - 2 dot 1 = gold(e - 2)",
    'diag': "integral x^2 e^x dif x = (x^2 - 2x + 2) e^x + C",
    'diag_val': "lr((x^2 - 2x + 2) e^x |)_0^1 = e - 2",
    'e5_s1': "I = integral_0^pi e^x sin x dif x = e^pi + 1 - I",
    'e5_s2': "arrow.double.long I = gold((e^pi + 1)/2)",
    'tf_given': "I = integral_0^1 (2x + 1) e^x dif x",
    'tf_a': "u = e^x",
    'tf_b': "I = lr((2x + 1) e^x |)_0^1 - 2 integral_0^1 e^x dif x",
    'tf_c': "I = e + 1",
    'tf_d': "I > 4",
    'tf_c_calc': "I = (3e - 1) - 2(e - 1) = e + 1 approx \"3,72\" < 4",
    'sa_task': "integral_0^1 x e^(-x) dif x approx ?",
    'sa_s1': "u = x, quad dif v = e^(-x) dif x arrow.double.long v = -e^(-x)",
    'sa_s2': "= lr(-x e^(-x) |)_0^1 + integral_0^1 e^(-x) dif x = -1/e + 1 - 1/e = 1 - 2/e approx gold(\"0,26\")",
    'sum1': "integral u dif v = u v - integral v dif u",
    'sum2': "ln x succ x^n succ sin, cos succ e^x",
    'sum3': "I = A - I arrow.double.long I = A/2",
    'hw1': "integral_0^pi x sin x dif x",
    'hw2': "integral_1^2 x ln x dif x",
    'hw3': "integral_0^1 x e^(2x) dif x",
    'hw_ans1': "pi",
    'hw_ans2': "2 ln 2 - 3/4",
    'hw_ans3': "(e^2 + 1)/4",
    'next1': "integral_a^b f(x) dif x = integral_a^b f(a + b - x) dif x",
    'next2': "integral_0^pi x sin x dif x = pi/2 integral_0^pi sin x dif x",
}

EXERCISES = (
    ('∫₀^π x sin x dx', 'π'),
    ('∫₁² x ln x dx', '2 ln 2 − 3/4'),
    ('∫₀¹ x e^(2x) dx', '(e² + 1)/4'),
)

TRUE_FALSE = (
    ('Nên đặt u = eˣ', False),
    ('I = [(2x + 1)eˣ]₀¹ − 2∫₀¹ eˣ dx', True),
    ('I = e + 1', True),
    ('I > 4', False),
)

x = sp.symbols('x', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, E, pi = sp.integrate, sp.Rational, sp.E, sp.pi
    ex = sp.exp(x)

    def parts(uu, dvv, a, b):
        vv = I(dvv, x)
        return (uu * vv).subs(x, b) - (uu * vv).subs(x, a) - I(vv * sp.diff(uu, x), (x, a, b))

    # hook and choice
    assert I(x * ex, (x, 0, 1)) == 1 == sp.simplify(parts(x, ex, 0, 1))
    # examples
    assert sp.simplify(I(sp.log(x), (x, 1, E)) - 1) == 0 == sp.simplify(parts(sp.log(x), 1, 1, E) - 1)
    assert sp.simplify(I(x * sp.cos(x), (x, 0, pi / 2)) - (pi / 2 - 1)) == 0
    assert sp.simplify(I(x * sp.log(x), (x, 1, E)) - (E**2 + 1) / 4) == 0
    assert sp.simplify(E**2 / 2 - (E**2 - 1) / 4 - (E**2 + 1) / 4) == 0
    assert sp.simplify(I(x**2 * ex, (x, 0, 1)) - (E - 2)) == 0
    Ie = I(ex * sp.sin(x), (x, 0, pi))
    assert sp.simplify(Ie - (sp.exp(pi) + 1) / 2) == 0 and sp.simplify(Ie - (sp.exp(pi) + 1 - Ie)) == 0
    F = (x**2 - 2*x + 2) * ex
    assert sp.simplify(sp.diff(F, x) - x**2 * ex) == 0 and sp.simplify(F.subs(x, 1) - F.subs(x, 0) - (E - 2)) == 0
    # geometric picture with u = x, v = e^x on [0, 1]: ∫u dv + ∫v du = u2 v2 − u1 v1
    assert sp.simplify(I(x * ex, (x, 0, 1)) + I(ex, (x, 0, 1)) - (1 * E - 0 * 1)) == 0
    # true / false
    Iv = I((2*x + 1) * ex, (x, 0, 1))
    claims = (False,  # polynomial before exponential: u = 2x + 1
              sp.simplify(((2*x + 1) * ex).subs(x, 1) - ((2*x + 1) * ex).subs(x, 0) - 2 * I(ex, (x, 0, 1)) - Iv) == 0,
              sp.simplify(Iv - (E + 1)) == 0, float(Iv) > 4)
    assert sp.simplify((3*E - 1) - 2*(E - 1) - (E + 1)) == 0 and round(float(Iv), 2) == 3.72
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    val = I(x * sp.exp(-x), (x, 0, 1))
    assert sp.simplify(val - (1 - 2 / E)) == 0 and f'{float(val):.2f}' == '0.26'
    # exercises
    assert I(x * sp.sin(x), (x, 0, pi)) == pi
    assert sp.simplify(I(x * sp.log(x), (x, 1, 2)) - (2 * sp.log(2) - R(3, 4))) == 0
    assert sp.simplify(I(x * sp.exp(2*x), (x, 0, 1)) - (E**2 + 1) / 4) == 0
    # next teaser: x ↦ π − x
    assert sp.simplify(I(x * sp.sin(x), (x, 0, pi)) - pi / 2 * I(sp.sin(x), (x, 0, pi))) == 0
    return True


validate()

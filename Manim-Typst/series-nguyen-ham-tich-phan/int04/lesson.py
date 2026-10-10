"""INT04 – Nguyên hàm hàm số lượng giác: bảng cơ bản & kỹ thuật hạ bậc.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT04',
    'number': 4,
    'title': 'Nguyên hàm lượng giác',
    'subtitle': 'Bảng cơ bản & kỹ thuật hạ bậc',
    'next_code': 'INT05',
    'next_title': 'Nguyên hàm của f(ax + b)',
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
         'Mọi thứ dao động quanh ta, từ con lắc, chiếc lò xo đến dòng điện xoay chiều, đều được mô tả bằng hàm sin '
         'và hàm cốt. Khi biết vận tốc của một vật dao động, muốn tìm lại vị trí của nó, ta cần nguyên hàm '
         'của các hàm số lượng giác.',
         'Mở đầu: những gì dao động'),
    Beat('h2', 'hook',
         'Đây là tập bốn của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'nguyên hàm hàm số lượng giác, bảng cơ bản và kỹ thuật hạ bậc.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, bốn công thức nguyên hàm lượng giác cơ bản và dấu trừ dễ nhầm. '
         'Hai, ý nghĩa hình học: nguyên hàm làm sóng lệch pha một phần tư chu kỳ. '
         'Ba, kỹ thuật hạ bậc để tính nguyên hàm của sin bình phương và cốt bình phương.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Ta đọc ngược bảng đạo hàm. Đạo hàm của sin x là cốt x, nên nguyên hàm của cốt x là sin x cộng C. '
         'Đạo hàm của cốt x là âm sin x, nên đạo hàm của âm cốt x là sin x. '
         'Vậy nguyên hàm của sin x là âm cốt x cộng C.',
         'Nguyên hàm của sin và cốt'),
    Beat('c2', 'core',
         'Lỗi sai phổ biến nhất là quên dấu trừ, viết nguyên hàm của sin x bằng cốt x. Hãy kiểm tra bằng hình: '
         'đường vàng là âm cốt x, đường xanh là sin x. Độ dốc của đường vàng luôn bằng chiều cao của đường xanh. '
         'Nếu bỏ dấu trừ, mọi độ dốc đều bị đảo dấu.'),
    Beat('c3', 'core',
         'Có một cách nhìn rất đẹp. Đồ thị cốt x chính là đồ thị sin x dịch sang trái một phần tư chu kỳ, '
         'tức là pi phần hai. Lấy đạo hàm làm sóng dịch sang trái, nên lấy nguyên hàm làm sóng dịch sang phải pi phần hai. '
         'Dịch sin x sang phải pi phần hai, ta được đúng đường âm cốt x.',
         'Bản chất: lệch pha một phần tư chu kỳ'),
    Beat('c4', 'core',
         'Tiếp theo là hai công thức với tang và cô tang. Đạo hàm của tang x bằng một chia cốt bình phương x, '
         'nên nguyên hàm của một chia cốt bình phương x là tang x cộng C. '
         'Đạo hàm của cô tang x bằng âm một chia sin bình phương x, nên nguyên hàm của một chia sin bình phương x '
         'là âm cô tang x cộng C.',
         'Nguyên hàm của 1/cos²x và 1/sin²x'),
    Beat('c5', 'core',
         'Lưu ý chuyên sâu: tang x chỉ xác định trên từng khoảng giữa hai đường tiệm cận đứng. '
         'Giống như với lô ga nê pe trị tuyệt đối x, trên mỗi khoảng ta có thể có một hằng số riêng. '
         'Đề thi thường cho sẵn một khoảng cụ thể, chẳng hạn từ âm pi phần hai đến pi phần hai.'),
    Beat('c6', 'core',
         'Bây giờ là sin bình phương x. Nhiều bạn bắt chước quy tắc lũy thừa và viết sin lập phương chia ba. '
         'Lấy đạo hàm để kiểm tra: kết quả là sin bình phương nhân cốt x, không phải sin bình phương. Sai. '
         'Cách đúng là hạ bậc: sin bình phương x bằng một trừ cốt hai x, tất cả chia hai.',
         'Kỹ thuật hạ bậc'),
    Beat('c7', 'core',
         'Ta cần thêm nguyên hàm của cốt hai x. Theo đạo hàm hàm hợp ở lớp mười một, đạo hàm của sin hai x '
         'bằng hai cốt hai x. Vậy nguyên hàm của cốt hai x là sin hai x chia hai cộng C. '
         'Quy tắc tổng quát cho f của a x cộng b sẽ được xây dựng ở tập năm.'),
    Beat('c8', 'core',
         'Ghép lại: nguyên hàm của sin bình phương x bằng x chia hai trừ sin hai x chia bốn, cộng C. '
         'Hình bên trái xác nhận: độ dốc của đường vàng luôn bằng chiều cao của sin bình phương. '
         'Tương tự, nguyên hàm của cốt bình phương x là x chia hai cộng sin hai x chia bốn, cộng C.'),
    Beat('c9', 'core',
         'Một dạng hay gặp khác là tang bình phương x. Dùng hằng đẳng thức: tang bình phương bằng '
         'một chia cốt bình phương trừ một. Vậy nguyên hàm của tang bình phương x là tang x trừ x cộng C.'),
    Beat('c10', 'core',
         'Tổng kết phần lý thuyết bằng bảng nguyên hàm lượng giác: bốn công thức cơ bản, '
         'cùng hai công thức hạ bậc cho sin bình phương và cốt bình phương.',
         'Bảng nguyên hàm lượng giác'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: tìm nguyên hàm của hai sin x trừ ba cốt x cộng một chia cốt bình phương x. '
         'Tách từng hạng tử và nhớ dấu trừ của sin: kết quả là âm hai cốt x trừ ba sin x cộng tang x cộng C.',
         'Ví dụ 1: tổng hợp bảng cơ bản'),
    Beat('e2', 'examples',
         'Ví dụ hai: nguyên hàm của sin x chia hai cộng cốt x chia hai, tất cả bình phương. '
         'Khai triển: sin bình phương cộng cốt bình phương bằng một, còn hai sin nhân cốt của x chia hai bằng sin x. '
         'Biểu thức trở thành một cộng sin x, có nguyên hàm x trừ cốt x cộng C.',
         'Ví dụ 2: dùng công thức lượng giác'),
    Beat('e5', 'examples',
         'Ví dụ ba: tìm nguyên hàm F của bốn sin bình phương x, biết F của không bằng một. Hạ bậc: bốn sin bình phương x '
         'bằng hai trừ hai cốt hai x. Nguyên hàm là hai x trừ sin hai x cộng C. Điều kiện F của không bằng một cho C bằng một, '
         'nên F của x bằng hai x trừ sin hai x cộng một.',
         'Ví dụ 3–4: hạ bậc và góc nhân đôi'),
    Beat('e6', 'examples',
         'Ví dụ bốn: nguyên hàm của sin x nhân cốt x. Đây là một tích, không tách được. Nhưng sin x cốt x bằng '
         'một nửa sin hai x. Nguyên hàm của sin hai x là âm cốt hai x chia hai, nên kết quả là âm cốt hai x chia bốn cộng C.'),
    Beat('e3', 'examples',
         'Ví dụ năm, dao động của lò xo. Một vật dao động trên trục ngang với vận tốc v của t bằng hai cốt t, '
         'đơn vị xăng ti mét mỗi giây. Lúc đầu vật ở vị trí một xăng ti mét. Tìm vị trí của vật tại t bằng pi phần hai.',
         'Ví dụ 5: dao động của lò xo'),
    Beat('e4', 'examples',
         'Vị trí là nguyên hàm của vận tốc: x của t bằng hai sin t cộng C. Điều kiện x của không bằng một cho C bằng một. '
         'Tại t bằng pi phần hai, x bằng hai cộng một, bằng ba xăng ti mét, đúng ở biên dao động. '
         'Hãy quan sát vật chạy đồng thời với điểm trên đồ thị.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f của x bằng sin x cộng cốt x. Gọi F là một nguyên hàm của f trên R. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: nguyên hàm của sin là âm cốt, của cốt là sin. Ý b sai: đây là cái bẫy lũy thừa của hàm lượng giác. '
         'Đạo hàm của sin lập phương chia ba là sin bình phương nhân cốt x, phải dùng hạ bậc.'),
    Beat('x3', 'exam',
         'Ý c đúng: F bằng sin x trừ cốt x cộng C, F của không bằng âm một cộng C bằng không nên C bằng một, '
         'và F của pi phần hai bằng một trừ không cộng một, bằng hai. Ý d sai: f bình phương bằng một cộng sin hai x, '
         'có nguyên hàm x trừ cốt hai x chia hai, dấu trừ chứ không phải dấu cộng.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. Biết F là nguyên hàm của một chia cốt bình phương x trên khoảng từ âm pi phần hai '
         'đến pi phần hai, và F của pi phần tư bằng ba. Tính F của pi phần ba, làm tròn đến hàng phần trăm. '
         'F bằng tang x cộng C, một cộng C bằng ba nên C bằng hai. Vậy F của pi phần ba bằng căn ba cộng hai, '
         'xấp xỉ ba phẩy bảy ba.',
         'Trả lời ngắn và mẹo máy tính'),
    Beat('x5', 'exam',
         'Mẹo thực chiến: khi kiểm tra nguyên hàm lượng giác bằng máy tính, nhất định phải chuyển sang chế độ ra đi an. '
         'Ví dụ, đạo hàm của âm cốt x tại x bằng một là xấp xỉ không phẩy tám bốn một, '
         'bằng đúng sin một. Ở chế độ độ, kết quả sẽ sai hoàn toàn.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, nguyên hàm của sin là âm cốt, của cốt là sin. Hai, nguyên hàm của một chia cốt bình phương '
         'là tang, của một chia sin bình phương là âm cô tang, xét trên từng khoảng. '
         'Ba, gặp sin bình phương hay cốt bình phương, hãy hạ bậc trước.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tìm nguyên hàm của ba cốt x trừ một chia sin bình phương x. '
         'Hai, tìm nguyên hàm của cốt bình phương x. Ba, biết F phẩy bằng sin x và F của pi bằng ba, tính F của không. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập năm, ta sẽ xây dựng quy tắc tổng quát cho nguyên hàm của f của a x cộng b, '
         'và hiểu vì sao luôn phải chia cho a. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook_v': "v(t) = 2 cos t arrow.r.long x(t) = gold(?)",
    'd_sin': "(sin x)' = cos x",
    'd_cos': "(cos x)' = -sin x",
    'i_cos': "integral cos x dif x = sin x + C",
    'i_sin': "integral sin x dif x = gold(-) cos x + C",
    'trap_sin': "integral sin x dif x coral(!=) cos x + C",
    'f_sin': "cyan(f(x) = sin x)",
    'F_mcos': "gold(F(x) = -cos x)",
    'shift1': "cos x = sin(x + pi/2)",
    'shift2': "-cos x = sin(x - pi/2)",
    'd_tan': "(tan x)' = 1/(cos^2 x)",
    'i_tan': "integral 1/(cos^2 x) dif x = tan x + C",
    'd_cot': "(cot x)' = -1/(sin^2 x)",
    'i_cot': "integral 1/(sin^2 x) dif x = -cot x + C",
    'tan_dom': "x != pi/2 + k pi",
    'cot_dom': "x != k pi",
    'trap_sq': "(sin^3 x / 3)' = sin^2 x cos x coral(!=) sin^2 x",
    'hb_sin': "sin^2 x = (1 - cos 2x)/2",
    'hb_cos': "cos^2 x = (1 + cos 2x)/2",
    'd_sin2x': "(sin 2x)' = 2 cos 2x",
    'i_cos2x': "integral cos 2x dif x = (sin 2x)/2 + C",
    'i_sin2': "integral sin^2 x dif x = x/2 - (sin 2x)/4 + C",
    'i_cos2': "integral cos^2 x dif x = x/2 + (sin 2x)/4 + C",
    'f_sin2': "cyan(f(x) = sin^2 x)",
    'tan2_id': "tan^2 x = 1/(cos^2 x) - 1",
    'i_tan2': "integral tan^2 x dif x = tan x - x + C",
    'tb1': "integral cos x dif x = sin x + C",
    'tb2': "integral sin x dif x = -cos x + C",
    'tb3': "integral 1/(cos^2 x) dif x = tan x + C",
    'tb4': "integral 1/(sin^2 x) dif x = -cot x + C",
    'tb5': "integral sin^2 x dif x = x/2 - (sin 2x)/4 + C",
    'tb6': "integral cos^2 x dif x = x/2 + (sin 2x)/4 + C",
    'e1_task': "integral (2 sin x - 3 cos x + 1/(cos^2 x)) dif x",
    'e1_s1': "= -2 cos x - 3 sin x + tan x + C",
    'e2_task': "integral (sin x/2 + cos x/2)^2 dif x",
    'e2_s1': "(sin x/2 + cos x/2)^2 = 1 + 2 sin x/2 cos x/2 = 1 + sin x",
    'e2_s2': "integral (1 + sin x) dif x = x - cos x + C",
    'e5_task': "integral 4 sin^2 x dif x, quad F(0) = 1",
    'e5_s1': "4 sin^2 x = 2 - 2 cos 2x",
    'e5_s2': "F(x) = 2x - sin 2x + C, quad F(0) = C = 1",
    'e5_s3': "F(x) = 2x - sin 2x + gold(1)",
    'e6_task': "integral sin x cos x dif x",
    'e6_s1': "sin x cos x = 1/2 sin 2x",
    'i_sin2x': "integral sin 2x dif x = -(cos 2x)/2 + C",
    'e6_s2': "integral sin x cos x dif x = -(cos 2x)/4 + C",
    'e3_task': "v(t) = 2 cos t, quad x(0) = 1",
    'e3_s1': "x(t) = integral 2 cos t dif t = 2 sin t + C",
    'e3_s2': "x(0) = C = 1 arrow.double.long x(t) = 2 sin t + 1",
    'e3_s3': "x(pi/2) = 2 + 1 = gold(3)",
    'tf_f': "f(x) = sin x + cos x",
    'tf_a': "integral f(x) dif x = -cos x + sin x + C",
    'tf_b': "integral sin^2 x dif x = (sin^3 x) \\/ 3 + C",
    'tf_c': "F(0) = 0 arrow.double.long F(pi/2) = 2",
    'tf_d': "integral f^2(x) dif x = x + (cos 2x) \\/ 2 + C",
    'tf_c_calc': "F = sin x - cos x + C, quad F(0) = -1 + C = 0 arrow.double.long C = 1",
    'tf_d_calc': "f^2 = 1 + sin 2x arrow.double.long integral f^2 dif x = x - (cos 2x)/2 + C",
    'sa_task': "F'(x) = 1/(cos^2 x), quad F(pi/4) = 3, quad F(pi/3) approx ?",
    'sa_s1': "F(x) = tan x + C, quad 1 + C = 3 arrow.double.long C = 2",
    'sa_s2': "F(pi/3) = sqrt(3) + 2 approx gold(\"3,73\")",
    'casio1': "lr(d/(dif x) (-cos x) |)_(x = 1) approx 0.841",
    'casio2': "sin 1 approx 0.841",
    'sum1': "integral sin x dif x = -cos x + C",
    'sum2': "integral 1/(cos^2 x) dif x = tan x + C",
    'sum3': "sin^2 x = (1 - cos 2x)/2",
    'hw1': "integral (3 cos x - 1/(sin^2 x)) dif x",
    'hw2': "integral cos^2 x dif x",
    'hw3': "F'(x) = sin x, quad F(pi) = 3, quad F(0) = ?",
    'hw_ans1': "3 sin x + cot x + C",
    'hw_ans2': "x/2 + (sin 2x)/4 + C",
    'hw_ans3': "F(0) = 1",
    'next1': "integral f(a x + b) dif x = 1/a F(a x + b) + C",
    'next2': "integral cos 3x dif x = (sin 3x)/3 + C, quad integral e^(2x) dif x = e^(2x)/2 + C",
}

EXERCISES = (
    ('Tìm ∫(3cos x − 1/sin²x) dx.', '3 sin x + cot x + C'),
    ('Tìm ∫cos²x dx.', 'x/2 + sin 2x/4 + C'),
    ("Biết F'(x) = sin x, F(π) = 3. Tính F(0).", 'F(0) = 1'),
)

TRUE_FALSE = (
    ('∫f(x)dx = −cos x + sin x + C', True),
    ('∫sin²x dx = sin³x/3 + C', False),
    ('F(0) = 0 ⇒ F(π/2) = 2', True),
    ('∫f²(x)dx = x + cos 2x/2 + C', False),
)

x, t, C = sp.symbols('x t C', real=True)
pi = sp.pi


def same_primitive(F, f, var=x):
    return sp.simplify(sp.diff(F, var) - f) == 0


def validate() -> bool:
    ids = [b.id for b in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(b.part) for b in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for b in BEATS if b.chapter) >= 3
    assert all(len(b.text.split()) >= 12 for b in BEATS)

    s, c = sp.sin, sp.cos
    # basic table
    assert same_primitive(s(x), c(x)) and same_primitive(-c(x), s(x)) and not same_primitive(c(x), s(x))
    assert same_primitive(sp.tan(x), 1/c(x)**2) and same_primitive(-sp.cot(x), 1/s(x)**2)
    # quarter-period shift
    assert sp.simplify(c(x) - s(x + pi/2)) == 0 and sp.simplify(-c(x) - s(x - pi/2)) == 0
    # power trap + power reduction
    assert sp.simplify(sp.diff(s(x)**3/3, x) - s(x)**2*c(x)) == 0 and not same_primitive(s(x)**3/3, s(x)**2)
    assert sp.simplify(s(x)**2 - (1 - c(2*x))/2) == 0 and sp.simplify(c(x)**2 - (1 + c(2*x))/2) == 0
    assert same_primitive(s(2*x)/2, c(2*x)) and sp.diff(s(2*x), x) == 2*c(2*x)
    assert same_primitive(x/2 - s(2*x)/4, s(x)**2) and same_primitive(x/2 + s(2*x)/4, c(x)**2)
    assert sp.simplify(sp.tan(x)**2 - (1/c(x)**2 - 1)) == 0 and same_primitive(sp.tan(x) - x, sp.tan(x)**2)
    # examples
    assert same_primitive(-2*c(x) - 3*s(x) + sp.tan(x), 2*s(x) - 3*c(x) + 1/c(x)**2)
    assert sp.simplify((s(x/2) + c(x/2))**2 - (1 + s(x))) == 0 and same_primitive(x - c(x), 1 + s(x))
    X = 2*s(t) + C
    cc = sp.solve(sp.Eq(X.subs(t, 0), 1), C)[0]
    assert cc == 1 and same_primitive(X, 2*c(t), t) and (X.subs(C, cc)).subs(t, pi/2) == 3
    # examples 3-4: power reduction with a condition, double angle
    F5 = 2*x - s(2*x) + C
    assert sp.simplify(4*s(x)**2 - (2 - 2*c(2*x))) == 0 and same_primitive(F5, 4*s(x)**2) and F5.subs(x, 0) == C
    assert sp.simplify(s(x)*c(x) - s(2*x)/2) == 0 and same_primitive(-c(2*x)/2, s(2*x))
    assert same_primitive(-c(2*x)/4, s(x)*c(x))
    # true / false
    f = s(x) + c(x)
    F = -c(x) + s(x)
    c0 = sp.solve(sp.Eq(F.subs(x, 0) + C, 0), C)[0]
    claims = (
        same_primitive(F, f),
        same_primitive(s(x)**3/3, s(x)**2),
        (F + c0).subs(x, pi/2) == 2,
        same_primitive(x + c(2*x)/2, f**2),
    )
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    assert sp.simplify(f**2 - (1 + s(2*x))) == 0 and same_primitive(x - c(2*x)/2, f**2)
    # short answer
    Fs = sp.tan(x) + C
    cs = sp.solve(sp.Eq(Fs.subs(x, pi/4), 3), C)[0]
    val = Fs.subs(C, cs).subs(x, pi/3)
    assert cs == 2 and sp.simplify(val - (sp.sqrt(3) + 2)) == 0 and round(float(val), 2) == 3.73
    # casio tip (radians)
    assert abs(float(sp.diff(-c(x), x).subs(x, 1)) - 0.841) < 5e-4
    # exercises
    assert same_primitive(3*s(x) + sp.cot(x), 3*c(x) - 1/s(x)**2)
    assert same_primitive(x/2 + s(2*x)/4, c(x)**2)
    F3 = -c(x) + C
    c3 = sp.solve(sp.Eq(F3.subs(x, pi), 3), C)[0]
    assert c3 == 2 and F3.subs(C, c3).subs(x, 0) == 1
    # teaser
    assert same_primitive(s(3*x)/3, c(3*x)) and same_primitive(sp.exp(2*x)/2, sp.exp(2*x))
    return True


validate()

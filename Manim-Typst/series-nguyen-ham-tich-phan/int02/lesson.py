"""INT02 – Tính chất nguyên hàm & nguyên hàm của hàm lũy thừa.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT02',
    'number': 2,
    'title': 'Tính chất nguyên hàm',
    'subtitle': 'Hàm lũy thừa & quy tắc tuyến tính',
    'next_code': 'INT03',
    'next_title': 'Nguyên hàm của 1/x và hàm số mũ',
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
         'Ở tập trước, ta tìm nguyên hàm của hai x bằng cách đoán: x bình phương có đạo hàm là hai x. '
         'Nhưng nếu đề bài cho ba x bình phương trừ bốn x cộng năm, hay căn bậc hai của x, '
         'chẳng lẽ lần nào cũng phải đoán? Ta cần những quy tắc tính nhanh, giống như các quy tắc tính đạo hàm.',
         'Mở đầu: không thể đoán mãi'),
    Beat('h2', 'hook',
         'Đây là tập hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'Tính chất của nguyên hàm, nguyên hàm của hàm lũy thừa và quy tắc tuyến tính.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ có ba công cụ. Một, công thức nguyên hàm của hàm lũy thừa. '
         'Hai, hai tính chất: đưa hằng số ra ngoài, và tách tổng hiệu. '
         'Ba, nhận diện cái bẫy kinh điển: nguyên hàm của một tích không bằng tích các nguyên hàm.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Nguyên tắc chung rất đơn giản: mỗi công thức đạo hàm, đọc theo chiều ngược lại, cho ta một công thức nguyên hàm. '
         'Đạo hàm của hằng số bằng không, nên nguyên hàm của không là hằng số C. '
         'Đạo hàm của x bằng một, nên nguyên hàm của một là x cộng C.',
         'Đảo ngược bảng đạo hàm'),
    Beat('c2', 'core',
         'Tổng quát hơn, nguyên hàm của hằng số k là k x cộng C. Về hình học, hàm f bằng hai là hằng số, '
         'nên trường hướng gồm các đoạn thẳng cùng độ dốc hai ở mọi nơi. Các nguyên hàm là '
         'những đường thẳng song song, y bằng hai x cộng C.'),
    Beat('c3', 'core',
         'Bây giờ đến hàm lũy thừa. Ta biết đạo hàm của x mũ n cộng một bằng n cộng một nhân x mũ n. '
         'Chia hai vế cho n cộng một, ta được đạo hàm của x mũ n cộng một chia n cộng một đúng bằng x mũ n. '
         'Vậy nguyên hàm của x mũ n bằng x mũ n cộng một, chia n cộng một, cộng C.',
         'Nguyên hàm của hàm lũy thừa'),
    Beat('c4', 'core',
         'Cách nhớ: tăng số mũ thêm một, rồi chia cho số mũ mới. Với x lập phương: số mũ ba tăng thành bốn, '
         'rồi chia cho bốn, được x mũ bốn chia bốn. Tương tự, nguyên hàm của x bình phương là x lập phương chia ba, '
         'nguyên hàm của x mũ năm là x mũ sáu chia sáu.'),
    Beat('c5', 'core',
         'Kiểm tra bằng hình. Đường màu xanh là f bằng x bình phương, đường màu vàng là F bằng x lập phương chia ba. '
         'Khi điểm xét chạy dọc trục hoành, độ dốc tiếp tuyến của đường vàng luôn bằng đúng chiều cao '
         'của đường xanh tại cùng hoành độ. Đó chính là F phẩy bằng f.'),
    Beat('c6', 'core',
         'Công thức còn đúng với số mũ alpha là số thực bất kỳ khác âm một, trên khoảng mà hàm xác định. '
         'Chẳng hạn căn x bằng x mũ một phần hai, nên nguyên hàm là hai phần ba x mũ ba phần hai cộng C. '
         'Còn một chia x bình phương bằng x mũ âm hai, nên nguyên hàm là âm một chia x cộng C.'),
    Beat('c7', 'core',
         'Vì sao phải loại alpha bằng âm một? Khi đó số mũ mới bằng không, và ta phải chia cho không, vô nghĩa. '
         'Nguyên hàm của một chia x là một trường hợp đặc biệt, gắn với hàm lô ga rít, ta sẽ học ở tập ba.'),
    Beat('c8', 'core',
         'Tính chất thứ nhất: nguyên hàm của k nhân f bằng k nhân nguyên hàm của f, với k khác không. '
         'Lý do: đạo hàm của k F bằng k nhân F phẩy, bằng k f. Về hình học, nhân k làm đồ thị giãn theo phương '
         'thẳng đứng, và mọi độ dốc cũng được nhân lên k lần.',
         'Tính chất 1: hằng số ra ngoài'),
    Beat('c9', 'core',
         'Điều kiện k khác không là cần thiết. Nguyên hàm của không nhân f là cả họ hằng số C, '
         'trong khi không nhân với nguyên hàm của f chỉ là số không. Hai vế không còn bằng nhau.'),
    Beat('c10', 'core',
         'Tính chất thứ hai: nguyên hàm của tổng hay hiệu bằng tổng hay hiệu các nguyên hàm. '
         'Lý do: đạo hàm của F cộng G bằng f cộng g. Trên hình, độ dốc của đường tổng tại mỗi điểm '
         'đúng bằng tổng hai độ dốc thành phần.',
         'Tính chất 2: tổng và hiệu'),
    Beat('c11', 'core',
         'Gộp hai tính chất, ta tính được mọi đa thức theo từng hạng tử. Với ba x bình phương trừ bốn x cộng năm: '
         'ba nhân x lập phương chia ba, trừ bốn nhân x bình phương chia hai, cộng năm x. '
         'Kết quả là x lập phương trừ hai x bình phương cộng năm x cộng C.'),
    Beat('c12', 'core',
         'Lưu ý: mỗi hạng tử sinh ra một hằng số riêng, nhưng tổng các hằng số vẫn là một hằng số. '
         'Vì vậy, cuối cùng ta chỉ viết một chữ C duy nhất.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: tìm nguyên hàm của hai x trừ một, tất cả bình phương. Không có quy tắc nguyên hàm '
         'cho bình phương của một biểu thức, vì vậy việc đầu tiên là khai triển.',
         'Ví dụ 1: khai triển trước khi tính'),
    Beat('e2', 'examples',
         'Hai x trừ một, tất cả bình phương, bằng bốn x bình phương trừ bốn x cộng một. '
         'Nguyên hàm từng hạng tử: bốn phần ba x lập phương, trừ hai x bình phương, cộng x, cộng C. '
         'Hình bên trái xác nhận: độ dốc của F luôn bằng chiều cao của f.'),
    Beat('e3', 'examples',
         'Ví dụ hai: tìm nguyên hàm của x bình phương cộng một, chia cho x bình phương. '
         'Cũng không có quy tắc cho thương, nên ta tách phân thức thành tổng các lũy thừa.',
         'Ví dụ 2: tách phân thức'),
    Beat('e4', 'examples',
         'Chia từng hạng tử cho x bình phương, ta được một cộng x mũ âm hai. '
         'Nguyên hàm là x trừ một chia x cộng C, xét trên từng khoảng không chứa số không. '
         'Bên trái, ta kiểm tra trên khoảng x dương.'),
    Beat('e5', 'examples',
         'Ví dụ ba, bài toán thực tế. Nước chảy vào một bể với tốc độ r của t bằng ba t bình phương cộng hai t, '
         'đơn vị lít mỗi phút. Lúc đầu bể có mười lít nước. Hỏi sau bốn phút, trong bể có bao nhiêu lít?',
         'Ví dụ 3: bể nước'),
    Beat('e6', 'examples',
         'Thể tích V là một nguyên hàm của tốc độ chảy, vì V phẩy bằng r. '
         'Theo quy tắc tuyến tính, V của t bằng t lập phương cộng t bình phương cộng C. '
         'Điều kiện V của không bằng mười cho C bằng mười.'),
    Beat('e7', 'examples',
         'Tại t bằng bốn: sáu mươi tư cộng mười sáu cộng mười, bằng chín mươi lít. '
         'Hãy quan sát mực nước dâng lên đồng thời với điểm chạy trên đồ thị thể tích.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Bây giờ là cái bẫy kinh điển. Có quy tắc cho tổng, vậy có quy tắc cho tích không? '
         'Nhiều bạn viết: nguyên hàm của f nhân g bằng nguyên hàm của f nhân nguyên hàm của g. Điều này sai.',
         'Bẫy: nguyên hàm của một tích'),
    Beat('x2', 'exam',
         'Phản ví dụ: lấy f và g cùng bằng x. Đúng ra, nguyên hàm của x nhân x là x lập phương chia ba. '
         'Cách làm sai cho x mũ bốn chia bốn, có đạo hàm là x lập phương, không phải x bình phương. '
         'Trên hình, đường màu đỏ dốc quá mức cần thiết.'),
    Beat('x3', 'exam',
         'Câu hỏi dạng đúng sai. Cho hàm số f của x bằng ba x bình phương cộng hai x trừ một. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x4', 'exam',
         'Ý a đúng, áp dụng quy tắc lũy thừa cho từng hạng tử. Ý b sai: đây chính là cái bẫy tích. '
         'Lấy đạo hàm vế phải được bốn x lập phương cộng ba x bình phương trừ hai x, không bằng x nhân f của x.'),
    Beat('x5', 'exam',
         'Ý c đúng: F bằng x lập phương cộng x bình phương trừ x cộng C. F của một bằng hai cho C bằng một, '
         'nên F của không bằng một. Ý d đúng: f trừ ba x bình phương bằng hai x trừ một, '
         'có nguyên hàm x bình phương trừ x cộng C.'),
    Beat('x6', 'exam',
         'Câu trả lời ngắn. Biết F phẩy bằng sáu x bình phương trừ bốn x cộng một, và F của một bằng ba. Tính F của hai. '
         'Ta có F bằng hai x lập phương trừ hai x bình phương cộng x cộng C. F của một bằng một cộng C bằng ba, '
         'nên C bằng hai. Vậy F của hai bằng mười sáu trừ tám cộng hai cộng hai, bằng mười hai.',
         'Trả lời ngắn và mẹo đổi về lũy thừa'),
    Beat('x7', 'exam',
         'Mẹo thực chiến: trước khi tính, hãy đổi mọi căn và phân thức về dạng lũy thừa. Căn x là x mũ một phần hai, '
         'một chia x mũ n là x mũ âm n, căn bậc ba của x bình phương là x mũ hai phần ba. '
         'Ví dụ, một chia căn x là x mũ âm một phần hai, có nguyên hàm là hai căn x cộng C.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, nguyên hàm của x mũ alpha bằng x mũ alpha cộng một chia alpha cộng một, cộng C, '
         'với alpha khác âm một. Hai, hằng số khác không được đưa ra ngoài dấu nguyên hàm. '
         'Ba, nguyên hàm của tổng hiệu bằng tổng hiệu các nguyên hàm, nhưng với tích và thương thì không.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tìm nguyên hàm của x bình phương trừ ba x cộng hai. '
         'Hai, tìm nguyên hàm của x cộng một chia căn x, với x dương. '
         'Ba, biết F phẩy bằng bốn x lập phương trừ hai x và F của một bằng ba, tính F của hai. '
         'Đáp số hiện ở cuối màn hình, em hãy tự làm trước khi xem.'),
    Beat('o3', 'outro',
         'Ở tập ba, ta sẽ giải quyết trường hợp đặc biệt alpha bằng âm một, với nguyên hàm của một chia x, '
         'và nguyên hàm của các hàm số mũ. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook_poly': "integral (3x^2 - 4x + 5) dif x = gold(?)",
    'hook_sqrt': "integral sqrt(x) dif x = gold(?)",
    'recap': "integral 2x dif x = x^2 + C",
    'd_const': "(C)' = 0",
    'i_const': "integral 0 dif x = C",
    'd_x': "(x)' = 1",
    'i_x': "integral 1 dif x = x + C",
    'd_kx': "(k x)' = k",
    'i_k': "integral k dif x = k x + C",
    'k2': "integral 2 dif x = 2x + C",
    'der1': "(x^(n+1))' = (n+1) x^n",
    'der2': "(x^(n+1)/(n+1))' = x^n",
    'pow_n': "integral x^n dif x = x^(n+1)/(n+1) + C",
    'step_a': "x^gold(3)",
    'step_b': "x^gold(4)",
    'step_c': "x^4/gold(4)",
    'ex_x3': "integral x^3 dif x = x^4/4 + C",
    'ex_x2': "integral x^2 dif x = x^3/3 + C",
    'ex_x5': "integral x^5 dif x = x^6/6 + C",
    'f_sq': "cyan(f(x) = x^2)",
    'F_cube': "gold(F(x) = x^3/3)",
    'pow_alpha': "integral x^alpha dif x = x^(alpha+1)/(alpha+1) + C, quad alpha != -1",
    'sqrt_ex': "integral sqrt(x) dif x = integral x^(1/2) dif x = frac(2, 3) x^(3/2) + C",
    'inv2_ex': "integral 1/x^2 dif x = integral x^(-2) dif x = -1/x + C",
    'alpha_m1': "alpha = -1: quad x^(-1+1)/(-1+1) = x^0/coral(0)",
    'inv1_q': "integral 1/x dif x = gold(?)",
    'rule_k': "integral k f(x) dif x = k integral f(x) dif x, quad k != 0",
    'proof_k': "(k F)' = k F' = k f",
    'kex': "integral 3x^2 dif x = 3 integral x^2 dif x = x^3 + C",
    'k0a': "integral 0 dot f(x) dif x = C",
    'k0b': "0 dot integral f(x) dif x = 0",
    'rule_sum': "integral [f(x) plus.minus g(x)] dif x = integral f(x) dif x plus.minus integral g(x) dif x",
    'proof_sum': "(F plus.minus G)' = f plus.minus g",
    'poly1': "integral (3x^2 - 4x + 5) dif x",
    'poly2': "= 3 dot x^3/3 - 4 dot x^2/2 + 5x + C",
    'poly3': "= x^3 - 2x^2 + 5x + C",
    'oneC': "C_1 + C_2 + C_3 = gold(C)",
    'e1_task': "integral (2x - 1)^2 dif x",
    'e1_s1': "(2x - 1)^2 = 4x^2 - 4x + 1",
    'e1_s2': "integral (4x^2 - 4x + 1) dif x = frac(4, 3) x^3 - 2x^2 + x + C",
    'e2_task': "integral (x^2 + 1)/x^2 dif x",
    'e2_s1': "(x^2 + 1)/x^2 = 1 + x^(-2)",
    'e2_s2': "integral (1 + x^(-2)) dif x = x - 1/x + C",
    'e3_task': "r(t) = 3t^2 + 2t, quad V(0) = 10",
    'e3_s1': "V(t) = integral (3t^2 + 2t) dif t = t^3 + t^2 + C",
    'e3_s2': "V(0) = C = 10",
    'e3_s3': "V(t) = t^3 + t^2 + gold(10)",
    'e3_s4': "V(4) = 64 + 16 + 10 = gold(90)",
    'trap1': "integral f g dif x coral(!=) integral f dif x dot integral g dif x",
    'trap_ok': "green(integral x dot x dif x = integral x^2 dif x = x^3/3 + C)",
    'trap_bad': "coral(integral x dif x dot integral x dif x = x^2/2 dot x^2/2 = x^4/4)",
    'trap_chk': "(x^4/4)' = x^3 coral(!=) x^2",
    'tf_f': "f(x) = 3x^2 + 2x - 1",
    'tf_a': "integral f(x) dif x = x^3 + x^2 - x + C",
    'tf_b': "integral x f(x) dif x = x (x^3 + x^2 - x) + C",
    'tf_c': "F(1) = 2 arrow.double.long F(0) = 1",
    'tf_d': "integral (f(x) - 3x^2) dif x = x^2 - x + C",
    'tf_b_chk': "[x (x^3 + x^2 - x)]' = 4x^3 + 3x^2 - 2x",
    'tf_c_calc': "1 + C = 2 arrow.double.long C = 1",
    'tf_d_calc': "f(x) - 3x^2 = 2x - 1",
    'sa_task': "F'(x) = 6x^2 - 4x + 1, quad F(1) = 3, quad F(2) = ?",
    'sa_s1': "F(x) = 2x^3 - 2x^2 + x + C",
    'sa_s2': "F(1) = 1 + C = 3 arrow.double.long C = 2",
    'sa_s3': "F(2) = 16 - 8 + 2 + 2 = gold(12)",
    'cv1': "sqrt(x) = x^(1/2)",
    'cv2': "1/x^n = x^(-n)",
    'cv3': "root(3, x^2) = x^(2/3)",
    'cv_ex': "integral 1/sqrt(x) dif x = integral x^(-1/2) dif x = 2 sqrt(x) + C",
    'sum1': "integral x^alpha dif x = x^(alpha+1)/(alpha+1) + C",
    'sum2': "integral k f = k integral f",
    'sum3': "integral (f plus.minus g) = integral f plus.minus integral g",
    'hw1': "integral (x^2 - 3x + 2) dif x",
    'hw2': "integral (x + 1)/sqrt(x) dif x",
    'hw3': "F'(x) = 4x^3 - 2x, quad F(1) = 3, quad F(2) = ?",
    'hw_ans1': "x^3/3 - (3x^2)/2 + 2x + C",
    'hw_ans2': "frac(2, 3) x sqrt(x) + 2 sqrt(x) + C",
    'hw_ans3': "F(2) = 15",
    'next1': "integral 1/x dif x = ln|x| + C",
    'next2': "integral e^x dif x = e^x + C, quad integral a^x dif x = a^x/(ln a) + C",
}

EXERCISES = (
    ('Tìm ∫(x² − 3x + 2) dx.', 'x³/3 − 3x²/2 + 2x + C'),
    ('Tìm ∫(x + 1)/√x dx với x > 0.', '(2/3)x√x + 2√x + C'),
    ("Biết F'(x) = 4x³ − 2x, F(1) = 3. Tính F(2).", 'F(2) = 15'),
)

TRUE_FALSE = (
    ('∫f(x)dx = x³ + x² − x + C', True),
    ('∫x·f(x)dx = x(x³ + x² − x) + C', False),
    ('F(1) = 2 ⇒ F(0) = 1', True),
    ('∫(f(x) − 3x²)dx = x² − x + C', True),
)

x, t, C, n = sp.symbols('x t C n', real=True)
X = sp.symbols('X', positive=True)


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

    # table and constants
    assert same_primitive(x, 1) and same_primitive(2*x, 2) and same_primitive(sp.Integer(5), 0)
    # power rule (symbolic n) and examples
    assert sp.simplify(sp.diff(x**(n + 1)/(n + 1), x) - x**n) == 0
    for k in (2, 3, 5):
        assert same_primitive(x**(k + 1)/(k + 1), x**k)
    assert same_primitive(sp.Rational(2, 3)*X**sp.Rational(3, 2), sp.sqrt(X), X)
    assert same_primitive(-1/x, 1/x**2)
    # linearity
    assert same_primitive(x**3, 3*x**2)
    assert same_primitive(x**3 - 2*x**2 + 5*x, 3*x**2 - 4*x + 5)
    assert same_primitive(x**2 + x, 2*x + 1)
    # example 1: expand first
    assert sp.expand((2*x - 1)**2) == 4*x**2 - 4*x + 1
    assert same_primitive(sp.Rational(4, 3)*x**3 - 2*x**2 + x, (2*x - 1)**2)
    # example 2: split the fraction
    assert sp.simplify((x**2 + 1)/x**2 - (1 + x**-2)) == 0
    assert same_primitive(x - 1/x, (x**2 + 1)/x**2)
    # example 3: water tank
    V = sp.integrate(3*t**2 + 2*t, t) + C
    V = V.subs(C, sp.solve(sp.Eq(V.subs(t, 0), 10), C)[0])
    assert sp.simplify(V - (t**3 + t**2 + 10)) == 0 and V.subs(t, 4) == 90
    # the product trap
    assert same_primitive(x**3/3, x*x) and not same_primitive(x**4/4, x*x)
    assert sp.diff(x**4/4, x) == x**3
    # true / false
    f = 3*x**2 + 2*x - 1
    F = x**3 + x**2 - x
    claims = (
        same_primitive(F, f),
        same_primitive(x*F, x*f),
        (F + (2 - F.subs(x, 1))).subs(x, 0) == 1,  # F(1) = 2 fixes C = 1
        same_primitive(x**2 - x, f - 3*x**2),
    )
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    assert sp.expand(sp.diff(x*F, x)) == 4*x**3 + 3*x**2 - 2*x
    # short answer
    Fs = 2*x**3 - 2*x**2 + x + C
    assert same_primitive(Fs, 6*x**2 - 4*x + 1)
    cs = sp.solve(sp.Eq(Fs.subs(x, 1), 3), C)[0]
    assert cs == 2 and Fs.subs(C, cs).subs(x, 2) == 12
    # power conversions
    assert same_primitive(2*sp.sqrt(X), 1/sp.sqrt(X), X)
    assert sp.simplify(sp.cbrt(X**2) - X**sp.Rational(2, 3)) == 0
    # exercises
    assert same_primitive(x**3/3 - sp.Rational(3, 2)*x**2 + 2*x, x**2 - 3*x + 2)
    assert same_primitive(sp.Rational(2, 3)*X*sp.sqrt(X) + 2*sp.sqrt(X), (X + 1)/sp.sqrt(X), X)
    F3 = x**4 - x**2 + 3
    assert same_primitive(F3, 4*x**3 - 2*x) and F3.subs(x, 1) == 3 and F3.subs(x, 2) == 15
    # next episode teaser facts
    assert same_primitive(sp.log(X), 1/X, X) and same_primitive(sp.exp(x), sp.exp(x))
    return True


validate()

"""INT12 – Định nghĩa tích phân & công thức Newton–Leibniz: F(b) − F(a), diện tích có dấu.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT12',
    'number': 12,
    'title': 'Định nghĩa tích phân',
    'subtitle': 'Newton–Leibniz & diện tích có dấu',
    'next_code': 'INT13',
    'next_title': 'Tính chất của tích phân',
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
         'Ở tập trước, ta phát hiện diện tích dưới đường x bình phương trên đoạn từ không đến hai bằng hiệu giá trị '
         'của nguyên hàm tại hai đầu mút. Liệu đó có phải trùng hợp? Và nếu đồ thị chui xuống dưới trục hoành, '
         'diện tích có còn dương không? Hôm nay ta biến phát hiện ấy thành một định nghĩa chính xác.',
         'Mở đầu: từ phát hiện đến định nghĩa'),
    Beat('h2', 'hook',
         'Đây là tập mười hai của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: định nghĩa tích phân, '
         'công thức Newton Leibniz và diện tích có dấu.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, định nghĩa tích phân bằng hiệu F của b trừ F của a. '
         'Hai, vì sao kết quả không phụ thuộc vào hằng số C hay tên biến. '
         'Ba, ý nghĩa diện tích có dấu, và vì sao tích phân có thể âm hoặc bằng không.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Định nghĩa. Cho hàm số f liên tục trên đoạn từ a đến b, và F là một nguyên hàm của f trên đoạn đó. '
         'Hiệu F của b trừ F của a được gọi là tích phân từ a đến b của f, kí hiệu tích phân từ a đến b của f của x d x. '
         'Ta còn viết gọn là F của x, lấy cận từ a đến b. Đây chính là công thức Newton Leibniz.',
         'Định nghĩa và công thức Newton–Leibniz'),
    Beat('c2', 'core',
         'Vì sao không phải lo chọn nguyên hàm nào? Nếu thay F bằng F cộng C, hiệu tại hai đầu mút là F của b cộng C '
         'trừ F của a trừ C, và hai chữ C triệt tiêu. Vì thế khi tính tích phân, ta chọn nguyên hàm đơn giản nhất, '
         'không cần viết C.'),
    Beat('c3', 'core',
         'Tích phân cũng không phụ thuộc tên biến. Tích phân từ a đến b của f của x d x bằng tích phân của f của t d t, '
         'hay của f của u d u. Biến lấy tích phân chỉ là một biến câm, kết quả là một con số.'),
    Beat('c4', 'core',
         'Ba ví dụ nhanh. Tích phân từ một đến hai của ba x bình phương bằng x lập phương lấy cận, bằng tám trừ một, bằng bảy. '
         'Tích phân từ không đến pi của sin x bằng âm cốt x lấy cận, bằng một cộng một, bằng hai. '
         'Tích phân từ một đến e của một chia x bằng lô ga nê pe x lấy cận, bằng một.',
         'Ba ví dụ nhanh'),
    Beat('c5', 'core',
         'Bây giờ là điểm tinh tế. Xét sin x trên đoạn từ không đến hai pi. Phần đồ thị phía trên trục hoành cho diện tích '
         'dương bằng hai, phần phía dưới cho phần mang dấu âm, bằng âm hai. Tích phân cộng hai phần lại: '
         'hai trừ hai, bằng không.',
         'Diện tích có dấu'),
    Beat('c6', 'core',
         'Như vậy tích phân là diện tích có dấu: phần trên trục hoành tính dương, phần dưới tính âm. '
         'Khi hàm số không đổi dấu và dương, tích phân đúng bằng diện tích. Khi hàm đổi dấu, tích phân khác diện tích, '
         'và ta sẽ xử lý bằng trị tuyệt đối ở các tập sau.'),
    Beat('c7', 'core',
         'Ý nghĩa vật lý giúp nhớ lâu. Tích phân của vận tốc theo thời gian là độ dời, có dấu: tiến thì dương, lùi thì âm. '
         'Còn quãng đường đi được luôn dương, là tích phân của trị tuyệt đối vận tốc. Chủ đề này sẽ được đào sâu ở tập mười lăm.'),
    Beat('c8', 'core',
         'Hai quy ước cần nhớ. Tích phân từ a đến a bằng không, vì không có đoạn nào để cộng. '
         'Và đổi chỗ hai cận thì tích phân đổi dấu: tích phân từ b đến a bằng âm tích phân từ a đến b.',
         'Hai quy ước về cận'),
    Beat('c9', 'core',
         'Phân biệt thật rõ hai khái niệm. Nguyên hàm là cả một họ hàm số, viết có cộng C. Tích phân từ a đến b là một con số '
         'cụ thể, không có C. Viết tích phân bằng x lập phương cộng C là một lỗi trình bày rất hay gặp, '
         'và có thể bị trừ điểm.',
         'Nguyên hàm khác tích phân'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: tích phân từ không đến một của e mũ x cộng hai x. Nguyên hàm là e mũ x cộng x bình phương. '
         'Lấy cận: e cộng một, trừ một cộng không, bằng e.',
         'Ví dụ 1–3'),
    Beat('e2', 'examples',
         'Ví dụ hai: tích phân từ không đến pi phần hai của cốt hai x. Nguyên hàm là sin hai x chia hai. '
         'Tại pi phần hai, sin pi bằng không; tại không cũng bằng không. Kết quả bằng không, dù hàm số không hề bằng không: '
         'phần dương và phần âm bù trừ nhau đúng như trên hình.'),
    Beat('e3', 'examples',
         'Ví dụ ba: tích phân từ một đến bốn của một chia căn x. Nguyên hàm là hai căn x. '
         'Lấy cận: hai nhân hai, trừ hai nhân một, bằng hai.'),
    Beat('e4', 'examples',
         'Ví dụ bốn: tích phân từ âm một đến hai của x bình phương trừ một. Nguyên hàm là x lập phương chia ba trừ x. '
         'Tại hai được hai phần ba, tại âm một cũng được hai phần ba. Kết quả bằng không! Trên hình, phần âm từ âm một đến một '
         'và phần dương từ một đến hai có cùng độ lớn bốn phần ba, nên triệt tiêu nhau.',
         'Ví dụ 4: đổi dấu và bằng không'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho f của x bằng hai x trừ hai trên đoạn từ không đến ba. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: nguyên hàm x bình phương trừ hai x, lấy cận từ không đến ba được chín trừ sáu, bằng ba. '
         'Ý b đúng: trên đoạn từ không đến một, hàm số âm, tích phân bằng một trừ hai, bằng âm một.'),
    Beat('x3', 'exam',
         'Ý c sai: diện tích phải cộng giá trị tuyệt đối từng phần, bằng một cộng bốn, bằng năm, không phải ba. '
         'Ý d đúng: đổi chỗ hai cận thì tích phân đổi dấu, bằng âm ba.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. Tính tích phân từ không đến hai của ba x bình phương trừ hai x cộng một. '
         'Nguyên hàm là x lập phương trừ x bình phương cộng x. Lấy cận: tám trừ bốn cộng hai, bằng sáu.',
         'Trả lời ngắn và mẹo máy tính'),
    Beat('x5', 'exam',
         'Mẹo thực chiến: máy tính cầm tay có phím tích phân. Nhập hàm số, cận dưới, cận trên, máy cho ngay kết quả số. '
         'Dùng nó để kiểm tra đáp số, chẳng hạn tích phân từ một đến hai của ba x bình phương cho đúng bảy. '
         'Với lượng giác, nhớ chuyển sang chế độ ra đi an.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, tích phân từ a đến b của f bằng F của b trừ F của a, với F là một nguyên hàm bất kỳ. '
         'Hai, kết quả không phụ thuộc hằng số C và tên biến. '
         'Ba, tích phân là diện tích có dấu, có thể âm hoặc bằng không khi hàm đổi dấu.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tích phân từ không đến một của bốn x lập phương trừ hai x. '
         'Hai, tích phân từ không đến pi phần ba của hai sin x. Ba, tích phân từ một đến e của một cộng một chia x. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập mười ba, ta học các tính chất của tích phân: tuyến tính, cộng khoảng và so sánh, '
         'những công cụ giúp tính nhanh và lập luận chặt chẽ. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook1': "integral_0^2 x^2 dif x = 8/3 = F(2) - F(0)",
    'def': "integral_a^b f(x) dif x = F(b) - F(a) = lr(F(x) |)_a^b",
    'cond': "F'(x) = f(x), quad x in [a; b]",
    'noC': "(F(b) + C) - (F(a) + C) = F(b) - F(a)",
    'dummy': "integral_a^b f(x) dif x = integral_a^b f(t) dif t = integral_a^b f(u) dif u",
    'q1': "integral_1^2 3x^2 dif x = lr(x^3 |)_1^2 = 8 - 1 = gold(7)",
    'q2': "integral_0^pi sin x dif x = lr(-cos x |)_0^pi = 1 + 1 = gold(2)",
    'q3': "integral_1^e 1/x dif x = lr(ln x |)_1^e = gold(1)",
    'sgn': "integral_0^(2 pi) sin x dif x = green(2) + coral((-2)) = 0",
    'sgn2': "integral_a^b f(x) dif x = S_+ - S_-",
    'phys1': "integral_(t_1)^(t_2) v(t) dif t = Delta s",
    'phys2': "integral_(t_1)^(t_2) |v(t)| dif t = L",
    'conv1': "integral_a^a f(x) dif x = 0",
    'conv2': "integral_b^a f(x) dif x = -integral_a^b f(x) dif x",
    'e1': "integral_0^1 (e^x + 2x) dif x = lr((e^x + x^2) |)_0^1 = (e + 1) - 1 = gold(e)",
    'e2': "integral_0^(pi/2) cos 2x dif x = lr((sin 2x)/2 |)_0^(pi/2) = 0 - 0 = gold(0)",
    'e3': "integral_1^4 1/sqrt(x) dif x = lr(2 sqrt(x) |)_1^4 = 4 - 2 = gold(2)",
    'nh_vs_tp': "integral x^2 dif x = x^3/3 + C quad \"vs\" quad integral_0^1 x^2 dif x = 1/3",
    'e4': "integral_(-1)^2 (x^2 - 1) dif x = lr((x^3/3 - x) |)_(-1)^2 = 2/3 - 2/3 = gold(0)",
    'tf_f': "f(x) = 2x - 2, quad [0; 3]",
    'tf_a': "integral_0^3 f(x) dif x = 3",
    'tf_b': "integral_0^1 f(x) dif x = -1",
    'tf_c': "S = 3",
    'tf_d': "integral_3^0 f(x) dif x = -3",
    'tf_ab_calc': "lr((x^2 - 2x) |)_0^3 = 3, quad lr((x^2 - 2x) |)_0^1 = -1",
    'tf_c_calc': "S = |-1| + |4| = 5 coral(!=) 3",
    'sa_task': "integral_0^2 (3x^2 - 2x + 1) dif x = ?",
    'sa_s1': "= lr((x^3 - x^2 + x) |)_0^2 = 8 - 4 + 2 = gold(6)",
    'casio': "integral_1^2 3x^2 dif x = 7",
    'sum1': "integral_a^b f = F(b) - F(a)",
    'sum2': "(F + C)(b) - (F + C)(a)",
    'sum3': "integral_0^(2 pi) sin x dif x = 0",
    'hw1': "integral_0^1 (4x^3 - 2x) dif x",
    'hw2': "integral_0^(pi/3) 2 sin x dif x",
    'hw3': "integral_1^e (1 + 1/x) dif x",
    'hw_ans1': "0",
    'hw_ans2': "1",
    'hw_ans3': "e",
    'next1': "integral_a^b [k f + m g] = k integral_a^b f + m integral_a^b g",
    'next2': "integral_a^c f = integral_a^b f + integral_b^c f",
}

EXERCISES = (
    ('∫₀¹(4x³ − 2x) dx', '0'),
    ('∫₀^(π/3) 2 sin x dx', '1'),
    ('∫₁ᵉ(1 + 1/x) dx', 'e'),
)

TRUE_FALSE = (
    ('∫₀³ f(x)dx = 3', True),
    ('∫₀¹ f(x)dx = −1', True),
    ('Diện tích giữa đồ thị f và Ox trên [0; 3] bằng 3', False),
    ('∫₃⁰ f(x)dx = −3', True),
)

x, C = sp.symbols('x C', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, pi, s, c = sp.integrate, sp.pi, sp.sin, sp.cos
    assert I(x**2, (x, 0, 2)) == sp.Rational(8, 3)
    F = x**3
    assert sp.simplify(((F + C).subs(x, 2) - (F + C).subs(x, 1)) - 7) == 0
    assert I(3*x**2, (x, 1, 2)) == 7 and I(s(x), (x, 0, pi)) == 2 and I(1/x, (x, 1, sp.E)) == 1
    assert I(s(x), (x, 0, 2*pi)) == 0 and I(s(x), (x, pi, 2*pi)) == -2
    assert I(x, (x, -1, 1)) == 0
    assert I(x**2, (x, 3, 3)) == 0 and I(x**2, (x, 2, 1)) == -I(x**2, (x, 1, 2))
    assert I(sp.exp(x) + 2*x, (x, 0, 1)) == sp.E
    assert I(c(2*x), (x, 0, pi/2)) == 0
    assert I(1/sp.sqrt(x), (x, 1, 4)) == 2
    assert I(x**2 - 1, (x, -1, 2)) == 0 and I(x**2 - 1, (x, -1, 1)) == -sp.Rational(4, 3)
    assert I(x**2 - 1, (x, 1, 2)) == sp.Rational(4, 3) and I(x**2, (x, 0, 1)) == sp.Rational(1, 3)
    f = 2*x - 2
    area_ = I(sp.Abs(f), (x, 0, 3))
    claims = (I(f, (x, 0, 3)) == 3, I(f, (x, 0, 1)) == -1, area_ == 3, I(f, (x, 3, 0)) == -3)
    assert claims == tuple(ans for _, ans in TRUE_FALSE) and area_ == 5
    assert I(3*x**2 - 2*x + 1, (x, 0, 2)) == 6
    assert I(4*x**3 - 2*x, (x, 0, 1)) == 0 and I(2*s(x), (x, 0, pi/3)) == 1 and I(1 + 1/x, (x, 1, sp.E)) == sp.E
    return True


validate()

"""INT11 – Diện tích dưới đường cong & tổng Riemann: vì sao tích phân là diện tích.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT11',
    'number': 11,
    'title': 'Diện tích dưới đường cong',
    'subtitle': 'Tổng Riemann – vì sao tích phân là diện tích',
    'next_code': 'INT12',
    'next_title': 'Định nghĩa tích phân & Newton–Leibniz',
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
         'Nếu một chiếc xe chạy đều sáu mét mỗi giây trong ba giây, quãng đường là sáu nhân ba bằng mười tám mét. '
         'Trên đồ thị vận tốc, con số đó chính là diện tích hình chữ nhật dưới đường vận tốc. '
         'Nhưng nếu vận tốc thay đổi liên tục, đồ thị là một đường cong. Làm sao tính diện tích dưới một đường cong?',
         'Mở đầu: quãng đường là diện tích'),
    Beat('h2', 'hook',
         'Chào mừng các em đến với Phần B của series: tích phân. Tập mười một: diện tích dưới đường cong và tổng Riemann, '
         'lời giải thích vì sao tích phân chính là diện tích.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, cách xấp xỉ diện tích bằng các hình chữ nhật mảnh, gọi là tổng Riemann. '
         'Hai, khi các hình chữ nhật mảnh dần, tổng tiến tới diện tích thật. '
         'Ba, một bất ngờ lớn: diện tích đó tính được bằng nguyên hàm.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Bắt đầu từ trường hợp dễ nhất. Vận tốc không đổi bằng sáu: đồ thị là đường nằm ngang, và miền dưới nó '
         'từ không đến ba là một hình chữ nhật. Diện tích bằng chiều cao sáu nhân chiều rộng ba, đúng bằng quãng đường mười tám mét.',
         'Từ hình chữ nhật đến đường cong'),
    Beat('c2', 'core',
         'Nếu vận tốc thay đổi theo từng bậc, mỗi đoạn một giá trị, thì quãng đường là tổng diện tích của nhiều hình chữ nhật. '
         'Ý tưởng then chốt: một đường cong bất kỳ có thể được xấp xỉ bằng các bậc thang như vậy.'),
    Beat('c3', 'core',
         'Xét f của x bằng x bình phương trên đoạn từ không đến hai. Chia đoạn thành n phần bằng nhau, mỗi phần rộng '
         'đen ta x bằng hai chia n. Trên mỗi phần, dựng hình chữ nhật có chiều cao bằng giá trị của f tại mút phải. '
         'Tổng diện tích các hình chữ nhật gọi là tổng Riemann.',
         'Tổng Riemann'),
    Beat('c4', 'core',
         'Với bốn hình chữ nhật, tổng phải bằng ba phẩy bảy lăm, lớn hơn diện tích thật vì các hình nhô lên trên đường cong. '
         'Tăng lên tám hình: ba phẩy một tám. Mười sáu hình: hai phẩy chín hai. Sáu mươi tư hình: hai phẩy bảy ba. '
         'Phần thừa ngày càng nhỏ.'),
    Beat('c5', 'core',
         'Làm tương tự với mút trái, các hình chữ nhật nằm dưới đường cong, nên tổng nhỏ hơn diện tích thật. '
         'Diện tích thật bị kẹp giữa tổng trái và tổng phải. Khi n tiến ra vô cùng, cả hai tổng cùng tiến tới '
         'một số duy nhất: tám phần ba, xấp xỉ hai phẩy sáu sáu bảy.',
         'Kẹp giữa tổng trái và tổng phải'),
    Beat('c5b', 'core',
         'Còn một cách chọn chiều cao khôn ngoan hơn: lấy giá trị tại điểm giữa mỗi đoạn. Mỗi hình chữ nhật vừa nhô lên '
         'một chút, vừa hụt xuống một chút, phần thừa và phần thiếu bù trừ cho nhau. Chỉ với bốn hình, tổng điểm giữa đã bằng '
         'hai phẩy sáu hai lăm, rất sát giá trị đúng hai phẩy sáu sáu bảy.',
         'Tổng điểm giữa'),
    Beat('c6', 'core',
         'Và đây là điều bất ngờ. Lấy một nguyên hàm của x bình phương, là x lập phương chia ba. Tính hiệu tại hai đầu mút: '
         'tám phần ba trừ không, bằng tám phần ba. Đúng bằng giới hạn của các tổng Riemann! '
         'Diện tích dưới đường cong được tính bằng nguyên hàm.',
         'Bất ngờ: diện tích bằng nguyên hàm'),
    Beat('c7', 'core',
         'Vì sao lại như vậy? Gọi S của x là diện tích từ a đến x. Khi x tăng thêm một lượng nhỏ h, diện tích tăng thêm '
         'một dải mảnh, xấp xỉ f của x nhân h. Vậy S phẩy bằng f: hàm diện tích chính là một nguyên hàm của f. '
         'Đó là cầu nối giữa Phần A và Phần B.'),
    Beat('c8', 'core',
         'Từ đây ta có kí hiệu tích phân từ a đến b của f của x d x. Dấu tích phân là chữ S kéo dài, nghĩa là tổng, '
         'còn d x là chiều rộng vô cùng nhỏ của mỗi hình chữ nhật. Tập sau, ta sẽ định nghĩa chính xác và học công thức '
         'Newton Leibniz.',
         'Kí hiệu tích phân'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, dạng bài thực tế. Bảng đo vận tốc của một vật mỗi giây: không, ba, tám, mười lăm, hai mươi tư mét mỗi giây, '
         'tại t bằng không, một, hai, ba, bốn. Ước lượng quãng đường trong bốn giây. Tổng trái là không cộng ba cộng tám cộng '
         'mười lăm, bằng hai mươi sáu. Tổng phải là ba cộng tám cộng mười lăm cộng hai mươi tư, bằng năm mươi.',
         'Ví dụ 1: ước lượng từ bảng số liệu'),
    Beat('e2', 'examples',
         'Vận tốc tăng dần nên quãng đường thật nằm giữa hai mươi sáu và năm mươi mét. Trung bình hai tổng là ba mươi tám. '
         'Nếu biết công thức v bằng t bình phương cộng hai t, nguyên hàm cho giá trị chính xác ba mươi bảy phẩy ba ba mét.'),
    Beat('e3', 'examples',
         'Ví dụ hai, kiểm tra với hình quen thuộc. Diện tích dưới đường y bằng x từ không đến hai là một tam giác, '
         'bằng một nửa nhân hai nhân hai, bằng hai. Dùng nguyên hàm x bình phương chia hai: bốn chia hai trừ không, '
         'cũng bằng hai. Hai cách cho cùng một kết quả.',
         'Ví dụ 2: kiểm tra bằng tam giác'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Cho f của x bằng hai x trên đoạn từ không đến ba, chia thành ba đoạn con bằng nhau. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: ba chia ba bằng một. Ý b đúng: các mút phải là một, hai, ba, nên tổng phải bằng hai cộng bốn cộng sáu, '
         'nhân một, bằng mười hai.'),
    Beat('x3', 'exam',
         'Ý c đúng: các mút trái là không, một, hai, tổng trái bằng không cộng hai cộng bốn, bằng sáu. '
         'Ý d sai: diện tích thật là một tam giác, bằng một nửa nhân ba nhân sáu, bằng chín, nằm giữa sáu và mười hai.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. Tính tổng Riemann phải với bốn hình chữ nhật cho f của x bằng x bình phương trên đoạn không đến hai. '
         'Đen ta x bằng không phẩy năm, các mút phải là không phẩy năm, một, một phẩy năm, hai. '
         'Tổng bằng không phẩy năm nhân không phẩy hai lăm cộng một cộng hai phẩy hai lăm cộng bốn, bằng ba phẩy bảy lăm.',
         'Trả lời ngắn và mẹo kẹp'),
    Beat('x5', 'exam',
         'Mẹo nhận định nhanh: nếu hàm số tăng, tổng trái nhỏ hơn diện tích và tổng phải lớn hơn. '
         'Nếu hàm số giảm thì ngược lại. Câu đúng sai thường hỏi chính điều này. '
         'Hãy nhìn hai hình: với hàm tăng, các hình chữ nhật điểm trái nằm gọn dưới đường cong; với hàm giảm, '
         'chúng lại nhô lên trên. Chỉ cần xác định chiều biến thiên là biết ngay chiều của bất đẳng thức.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, diện tích dưới đường cong được xấp xỉ bằng tổng các hình chữ nhật mảnh, tổng Riemann. '
         'Hai, khi số hình chữ nhật tiến ra vô cùng, tổng tiến tới diện tích thật. '
         'Ba, diện tích đó bằng hiệu giá trị của một nguyên hàm tại hai đầu mút.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tính tổng Riemann phải với bốn hình chữ nhật cho f bằng x cộng một trên đoạn không đến hai. '
         'Hai, dùng nguyên hàm tính diện tích dưới y bằng ba x bình phương trên đoạn không đến một. '
         'Ba, vận tốc đo tại t bằng không, hai, bốn, sáu phút là mười, mười bốn, mười sáu, mười tám mét mỗi phút, '
         'ước lượng quãng đường bằng tổng trái.'),
    Beat('o3', 'outro',
         'Tập mười hai sẽ định nghĩa chính xác tích phân bằng công thức Newton Leibniz, và giải thích diện tích có dấu. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'rect': "s = v dot t = 6 dot 3 = 18",
    'riemann': "S_n = sum_(i=1)^n f(x_i) Delta x, quad Delta x = (b - a)/n",
    'limit': "lim_(n -> infinity) S_n = 8/3 approx \"2,667\"",
    'squeeze': "L_n < S < R_n",
    'mid4': "M_4 = \"0,5\" dot (\"0,0625\" + \"0,5625\" + \"1,5625\" + \"3,0625\") = gold(\"2,625\")",
    'antider': "F(x) = x^3/3: quad F(2) - F(0) = 8/3",
    'strip': "S(x + h) - S(x) approx f(x) dot h arrow.double.long S'(x) = f(x)",
    'notation': "integral_a^b f(x) dif x",
    'e1_left': "L = (0 + 3 + 8 + 15) dot 1 = 26",
    'e1_right': "R = (3 + 8 + 15 + 24) dot 1 = 50",
    'e1_exact': "integral_0^4 (t^2 + 2t) dif t = 64/3 + 16 approx gold(\"37,33\")",
    'e3_tri': "S = 1/2 dot 2 dot 2 = 2",
    'e3_F': "F(x) = x^2/2: quad F(2) - F(0) = 2",
    'tf_f': "f(x) = 2x, quad [0; 3], quad n = 3",
    'tf_a': "Delta x = 1",
    'tf_b': "R_3 = 12",
    'tf_c': "L_3 = 6",
    'tf_d': "S = 12",
    'tf_b_calc': "R_3 = (2 + 4 + 6) dot 1 = 12, quad L_3 = (0 + 2 + 4) dot 1 = 6",
    'tf_d_calc': "S = 1/2 dot 3 dot 6 = 9 coral(!=) 12",
    'sa_task': "f(x) = x^2, quad [0; 2], quad n = 4, quad R_4 = ?",
    'sa_s1': "Delta x = \"0,5\": quad x_i = \"0,5\"; 1; \"1,5\"; 2",
    'sa_s2': "R_4 = \"0,5\" dot (\"0,25\" + 1 + \"2,25\" + 4) = gold(\"3,75\")",
    'tip1': "f arrow.tr: quad L_n < S < R_n",
    'tip2': "f arrow.br: quad R_n < S < L_n",
    'sum1': "S_n = sum f(x_i) Delta x",
    'sum2': "S = lim_(n -> infinity) S_n",
    'sum3': "S = F(b) - F(a)",
    'hw1': "f(x) = x + 1, quad [0; 2], quad n = 4, quad R_4 = ?",
    'hw2': "y = 3x^2, quad [0; 1], quad S = ?",
    'hw3': "v = 10; 14; 16; 18 quad (t = 0; 2; 4; 6), quad L = ?",
    'hw_ans1': "R_4 = \"4,5\"",
    'hw_ans2': "S = 1",
    'hw_ans3': "L = 80",
    'next1': "integral_a^b f(x) dif x = F(b) - F(a)",
    'next2': "integral_(-1)^1 x dif x = 0",
}

EXERCISES = (
    ('f(x) = x + 1 trên [0; 2], n = 4: tổng Riemann phải.', 'R₄ = 4,5'),
    ('Diện tích dưới y = 3x² trên [0; 1].', 'S = 1'),
    ('v(0), v(2), v(4), v(6) = 10, 14, 16, 18 m/phút: tổng trái.', '80 m'),
)

TRUE_FALSE = (
    ('Δx = 1', True),
    ('R₃ = 12', True),
    ('L₃ = 6', True),
    ('Diện tích S = 12', False),
)

x, n = sp.symbols('x n', positive=True)
i = sp.symbols('i', integer=True, positive=True)


def right_sum(f, a, b, k):
    dx = sp.Rational(b - a, k)
    return sum(f.subs(x, a + j*dx) for j in range(1, k + 1))*dx


def left_sum(f, a, b, k):
    dx = sp.Rational(b - a, k)
    return sum(f.subs(x, a + j*dx) for j in range(0, k))*dx


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    f = x**2
    R = {k: right_sum(f, 0, 2, k) for k in (4, 8, 16, 64)}
    assert R[4] == sp.Rational(15, 4)
    assert [round(float(R[k]), 2) for k in (8, 16, 64)] == [3.19, 2.92, 2.73]
    L = {k: left_sum(f, 0, 2, k) for k in (4, 8, 16, 64)}
    exact = sp.integrate(f, (x, 0, 2))
    assert exact == sp.Rational(8, 3)
    assert all(L[k] < exact < R[k] for k in R)
    mid = sum((sp.Rational(2*j + 1, 4))**2 for j in range(4))*sp.Rational(1, 2)
    assert mid == sp.Rational(21, 8) and [sp.Rational(2*j + 1, 4)**2 for j in range(4)] == \
        [sp.Rational(1, 16), sp.Rational(9, 16), sp.Rational(25, 16), sp.Rational(49, 16)]
    # closed form of R_n tends to 8/3
    Rn = (8/n**3)*sp.summation(i**2, (i, 1, n))
    assert sp.limit(Rn, n, sp.oo) == sp.Rational(8, 3)
    assert (x**3/3).subs(x, 2) - 0 == sp.Rational(8, 3)
    # example 1: table of speeds v = t^2 + 2t
    t = sp.symbols('t')
    v = [(t**2 + 2*t).subs(t, k) for k in range(5)]
    assert v == [0, 3, 8, 15, 24] and sum(v[:4]) == 26 and sum(v[1:]) == 50
    ex = sp.integrate(t**2 + 2*t, (t, 0, 4))
    assert ex == sp.Rational(112, 3) and round(float(ex), 2) == 37.33
    # example 2: triangle
    assert sp.integrate(x, (x, 0, 2)) == 2
    # true / false: f = 2x on [0, 3], n = 3
    g = 2*x
    claims = (sp.Rational(3, 3) == 1, right_sum(g, 0, 3, 3) == 12, left_sum(g, 0, 3, 3) == 6,
              sp.integrate(g, (x, 0, 3)) == 12)
    assert claims == tuple(ans for _, ans in TRUE_FALSE) and sp.integrate(g, (x, 0, 3)) == 9
    # short answer
    assert right_sum(f, 0, 2, 4) == sp.Rational(375, 100)
    # exercises
    assert right_sum(x + 1, 0, 2, 4) == sp.Rational(9, 2)
    assert sp.integrate(3*x**2, (x, 0, 1)) == 1
    assert (10 + 14 + 16)*2 == 80
    # teaser
    assert sp.integrate(x, (x, -1, 1)) == 0
    return True


validate()

"""INT10 – Từ tốc độ thay đổi đến đại lượng: nguyên hàm trong thực tế & tổng ôn Phần A.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT10',
    'number': 10,
    'title': 'Từ tốc độ thay đổi đến đại lượng',
    'subtitle': 'Nguyên hàm trong thực tế & tổng ôn Phần A',
    'next_code': 'INT11',
    'next_title': 'Diện tích dưới đường cong & tổng Riemann',
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
         'Trong đời sống, ta thường đo được tốc độ thay đổi trước khi biết chính đại lượng: đồng hồ tốc độ của xe, '
         'tốc độ tăng dân số mỗi năm, chi phí làm thêm một sản phẩm, hay tốc độ nguội đi của một cốc nước nóng. '
         'Nguyên hàm là chiếc cầu nối từ tốc độ thay đổi trở về đại lượng ban đầu.',
         'Mở đầu: tốc độ thay đổi ở khắp nơi'),
    Beat('h2', 'hook',
         'Đây là tập mười của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: từ tốc độ thay đổi đến đại lượng, '
         'và cũng là tập tổng ôn khép lại Phần A về nguyên hàm.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, quy trình chung cho mọi bài toán thực tế dùng nguyên hàm. '
         'Hai, cách đọc đơn vị và ý nghĩa của hằng số C. Ba, bốn mô hình tiêu biểu: dân số, chi phí, nhiệt độ và chuyển động.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Mọi bài toán đều theo cùng một khuôn. Biết tốc độ thay đổi Q phẩy của t, và biết giá trị của Q tại một thời điểm. '
         'Lấy nguyên hàm để được Q bằng một nguyên hàm cộng C, rồi dùng giá trị đã biết để tìm C. '
         'Cuối cùng, thay thời điểm cần hỏi để tính đại lượng.',
         'Quy trình chung'),
    Beat('c2', 'core',
         'Hãy để ý đơn vị. Nếu Q đo bằng người và t đo bằng năm, thì Q phẩy có đơn vị người mỗi năm. '
         'Lấy nguyên hàm theo t sẽ nhân lại đơn vị năm, đưa ta trở về đơn vị người. '
         'Hằng số C luôn mang đúng đơn vị của Q, và thường chính là giá trị ban đầu.',
         'Đơn vị và ý nghĩa của C'),
    Beat('c3', 'core',
         'Một quan sát rất quan trọng: độ thay đổi Q của b trừ Q của a không phụ thuộc vào C, vì hai chữ C triệt tiêu nhau. '
         'Muốn biết đại lượng tăng thêm bao nhiêu trong một khoảng thời gian, ta thậm chí không cần điều kiện ban đầu. '
         'Đây chính là hạt giống của tích phân ở Phần B.',
         'Độ thay đổi không phụ thuộc C'),
    Beat('c4', 'core',
         'Bảng đối chiếu giúp em nhận ra mô hình ngay khi đọc đề. Vận tốc là tốc độ thay đổi của vị trí. '
         'Chi phí biên là tốc độ thay đổi của tổng chi phí. Tốc độ tăng trưởng ứng với dân số, lưu lượng chảy ứng với '
         'thể tích nước. Thấy cặp nào, lấy nguyên hàm vế trái để được vế phải.',
         'Bảng đối chiếu thực tế'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Mô hình một, dân số. Một thị trấn có mười nghìn người, tốc độ tăng dân số là năm mươi nhân e mũ không phẩy '
         'không hai t người mỗi năm. Lấy nguyên hàm: P bằng hai nghìn năm trăm e mũ không phẩy không hai t cộng C. '
         'Điều kiện ban đầu cho C bằng bảy nghìn năm trăm.',
         'Mô hình 1: dân số'),
    Beat('e2', 'examples',
         'Sau mười năm, P bằng hai nghìn năm trăm e mũ không phẩy hai cộng bảy nghìn năm trăm, xấp xỉ mười nghìn năm trăm '
         'năm mươi tư người. Đồ thị cong lên dần vì tốc độ tăng cũng tăng theo thời gian.'),
    Beat('e3', 'examples',
         'Mô hình hai, chi phí biên. Chi phí để sản xuất thêm sản phẩm thứ x là không phẩy ba x cộng hai mươi nghìn đồng, '
         'và chi phí cố định là năm trăm nghìn đồng. Lấy nguyên hàm: tổng chi phí C của x bằng không phẩy một lăm x bình phương '
         'cộng hai mươi x cộng năm trăm.',
         'Mô hình 2: chi phí biên'),
    Beat('e4', 'examples',
         'Câu hỏi thực tế: tăng sản lượng từ một trăm lên hai trăm sản phẩm thì tốn thêm bao nhiêu? Lấy C của hai trăm '
         'trừ C của một trăm: mười nghìn năm trăm trừ bốn nghìn, bằng sáu nghìn năm trăm nghìn đồng. '
         'Chi phí cố định năm trăm đã triệt tiêu, đúng như quan sát ở phần trước.'),
    Beat('e5', 'examples',
         'Mô hình ba, nhiệt độ. Một cốc nước chín mươi độ nguội đi với tốc độ âm hai e mũ âm không phẩy một t độ mỗi phút. '
         'Nguyên hàm: T bằng hai mươi e mũ âm không phẩy một t cộng C, và C bằng bảy mươi. '
         'Sau mười phút, nhiệt độ xấp xỉ bảy mươi bảy phẩy bốn độ, và về lâu dài tiến dần tới bảy mươi độ.',
         'Mô hình 3: nhiệt độ'),
    Beat('e6', 'examples',
         'Mô hình bốn, phanh xe. Một ô tô đang chạy hai mươi mét mỗi giây thì phanh, vận tốc giảm theo v bằng hai mươi trừ năm t. '
         'Xe dừng khi v bằng không, tức t bằng bốn giây. Quãng đường phanh là s của bốn, với s bằng hai mươi t trừ hai phẩy năm '
         't bình phương: tám mươi trừ bốn mươi, bằng bốn mươi mét.',
         'Mô hình 4: quãng đường phanh'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai dựa trên mô hình dân số. Tốc độ tăng là năm mươi e mũ không phẩy không hai t người mỗi năm, '
         'dân số ban đầu mười nghìn người. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: chia năm mươi cho không phẩy không hai được hai nghìn năm trăm. Ý b đúng: hai nghìn năm trăm cộng C '
         'bằng mười nghìn, nên C bằng bảy nghìn năm trăm.'),
    Beat('x3', 'exam',
         'Ý c đúng: P của mười xấp xỉ mười nghìn năm trăm năm mươi tư người. Ý d sai: dân số chỉ tăng thêm khoảng năm trăm '
         'năm mươi tư người trong mười năm, không phải một nghìn.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. Chiều cao của một cây tăng với tốc độ một chia t cộng một mét mỗi năm, lúc trồng cây cao không phẩy năm mét. '
         'Tìm chiều cao sau bốn năm, làm tròn đến hàng phần trăm. h bằng lô ga nê pe của t cộng một, cộng không phẩy năm. '
         'Vậy h của bốn bằng lô ga nê pe năm cộng không phẩy năm, xấp xỉ hai phẩy một một mét.',
         'Trả lời ngắn và bản đồ Phần A'),
    Beat('x5', 'exam',
         'Tổng ôn Phần A bằng bản đồ chọn phương pháp. Gặp tổng hiệu: tách từng hạng tử theo bảng. Gặp f của a x cộng b: '
         'chia cho a. Gặp phân thức: chia đa thức hoặc tách. Gặp hàm của u nhân u phẩy: đổi biến. '
         'Gặp tích hai hàm khác loại: từng phần. Và luôn dùng điều kiện để tìm C.'),
    Beat('x6', 'exam',
         'Nhìn lại chín tập đã qua: bản chất nguyên hàm, tính chất và hàm lũy thừa, một chia x và hàm mũ, lượng giác, '
         'quy tắc chia cho a, nguyên hàm có điều kiện và hàm từng khúc, phân thức hữu tỉ, đổi biến số, và từng phần. '
         'Tất cả hội tụ trong tập hôm nay: biết tốc độ thay đổi, tìm lại đại lượng.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, đại lượng bằng nguyên hàm của tốc độ thay đổi, cộng hằng số xác định từ điều kiện ban đầu. '
         'Hai, hằng số C mang đơn vị của đại lượng, thường là giá trị ban đầu. '
         'Ba, độ thay đổi giữa hai thời điểm không phụ thuộc C.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, vật có gia tốc sáu t, vận tốc ban đầu hai, vị trí ban đầu không, tính quãng đường sau hai giây. '
         'Hai, doanh thu biên một trăm trừ không phẩy hai x, doanh thu ban đầu bằng không, tính doanh thu khi bán ba trăm sản phẩm. '
         'Ba, nước chảy vào bể với tốc độ bốn căn t lít mỗi phút, bể ban đầu rỗng, tính lượng nước sau chín phút.'),
    Beat('o3', 'outro',
         'Phần A đã khép lại. Từ tập mười một, ta bước sang Phần B: tích phân, bắt đầu từ câu hỏi diện tích dưới một đường cong '
         'và tổng Riemann. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'proc1': "Q'(t) \"+\" Q(t_0) arrow.r.long Q(t) = integral Q'(t) dif t",
    'proc2': "Q(t) = G(t) + C, quad C = Q(t_0) - G(t_0)",
    'unit1': "[Q'] = [Q]/[t] arrow.double.long [integral Q' dif t] = [Q]",
    'diff1': "Q(b) - Q(a) = (G(b) + C) - (G(a) + C) = G(b) - G(a)",
    'p_task': "P'(t) = 50 e^(0.02 t), quad P(0) = 10000",
    'p_s1': "P(t) = 2500 e^(0.02 t) + C, quad 2500 + C = 10000 arrow.double.long C = 7500",
    'p_s2': "P(10) = 2500 e^(0.2) + 7500 approx gold(10554)",
    'c_task': "C'(x) = 0.3 x + 20, quad C(0) = 500",
    'c_s1': "C(x) = 0.15 x^2 + 20 x + 500",
    'c_s2': "C(200) - C(100) = 10500 - 4000 = gold(6500)",
    't_task': "T'(t) = -2 e^(-0.1 t), quad T(0) = 90",
    't_s1': "T(t) = 20 e^(-0.1 t) + 70",
    't_s2': "T(10) = 20 e^(-1) + 70 approx gold(\"77,4\")",
    'b_task': "v(t) = 20 - 5t, quad s(0) = 0",
    'b_s1': "v = 0 arrow.double.long t = 4, quad s(t) = 20t - 5/2 t^2",
    'b_s2': "s(4) = 80 - 40 = gold(40)",
    'tf_f': "P'(t) = 50 e^(0.02 t), quad P(0) = 10000",
    'tf_a': "P(t) = 2500 e^(0.02 t) + C",
    'tf_b': "C = 7500",
    'tf_c': "P(10) approx 10554",
    'tf_d': "P(10) - P(0) approx 1000",
    'tf_d_calc': "P(10) - P(0) = 2500 (e^(0.2) - 1) approx 554 coral(!=) 1000",
    'sa_task': "h'(t) = 1/(t + 1), quad h(0) = 0.5, quad h(4) approx ?",
    'sa_s1': "h(t) = ln(t + 1) + 0.5",
    'sa_s2': "h(4) = ln 5 + 0.5 approx gold(\"2,11\")",
    'sum1': "Q(t) = integral Q'(t) dif t + C",
    'sum2': "C = Q(t_0) - G(t_0)",
    'sum3': "Q(b) - Q(a) = G(b) - G(a)",
    'hw1': "a(t) = 6t, quad v(0) = 2, quad s(0) = 0, quad s(2) = ?",
    'hw2': "R'(x) = 100 - 0.2x, quad R(0) = 0, quad R(300) = ?",
    'hw3': "V'(t) = 4 sqrt(t), quad V(0) = 0, quad V(9) = ?",
    'hw_ans1': "s(2) = 12",
    'hw_ans2': "R(300) = 21000",
    'hw_ans3': "V(9) = 72",
    'next1': "S approx sum_(i=1)^n f(x_i) Delta x",
    'next2': "integral_a^b f(x) dif x = F(b) - F(a)",
}

EXERCISES = (
    ('a(t) = 6t, v(0) = 2, s(0) = 0. Tính s(2).', 's(2) = 12'),
    ("R'(x) = 100 − 0,2x, R(0) = 0. Tính R(300).", 'R(300) = 21000'),
    ("V'(t) = 4√t, V(0) = 0. Tính V(9).", 'V(9) = 72'),
)

TRUE_FALSE = (
    ('P(t) = 2500e^(0,02t) + C', True),
    ('C = 7500', True),
    ('P(10) ≈ 10554', True),
    ('P(10) − P(0) ≈ 1000', False),
)

t, x, C = sp.symbols('t x C', real=True)
T_ = sp.symbols('T_', positive=True)


def same_primitive(F, f, var=t):
    return sp.simplify(sp.diff(F, var) - f) == 0


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    e, R = sp.exp, sp.Rational
    # population
    G = 2500*e(R(1, 50)*t)
    assert same_primitive(G, 50*e(R(1, 50)*t))
    cP = sp.solve(sp.Eq(G.subs(t, 0) + C, 10000), C)[0]
    P10 = (G + cP).subs(t, 10)
    assert cP == 7500 and round(float(P10)) == 10554
    # cost
    Cx = R(3, 20)*x**2 + 20*x + 500
    assert sp.simplify(sp.diff(Cx, x) - (R(3, 10)*x + 20)) == 0 and Cx.subs(x, 0) == 500
    assert Cx.subs(x, 200) == 10500 and Cx.subs(x, 100) == 4000
    # temperature
    Tt = 20*e(-t/10) + 70
    assert same_primitive(Tt, -2*e(-t/10)) and Tt.subs(t, 0) == 90 and round(float(Tt.subs(t, 10)), 1) == 77.4
    assert sp.limit(Tt, t, sp.oo) == 70
    # braking
    s = 20*t - R(5, 2)*t**2
    assert same_primitive(s, 20 - 5*t) and sp.solve(20 - 5*t, t) == [4] and s.subs(t, 4) == 40
    # true / false
    claims = (same_primitive(G, 50*e(R(1, 50)*t)), cP == 7500, round(float(P10)) == 10554,
              abs(float(P10 - 10000) - 1000) < 1)
    assert claims == tuple(ans for _, ans in TRUE_FALSE) and round(float(P10 - 10000)) == 554
    # short answer
    h = sp.log(T_ + 1) + R(1, 2)
    assert same_primitive(h, 1/(T_ + 1), T_) and h.subs(T_, 0) == R(1, 2) and round(float(h.subs(T_, 4)), 2) == 2.11
    # exercises
    v = 3*t**2 + 2
    sv = t**3 + 2*t
    assert same_primitive(v, 6*t) and same_primitive(sv, v) and sv.subs(t, 2) == 12
    Rv = 100*x - x**2/10
    assert sp.simplify(sp.diff(Rv, x) - (100 - x/5)) == 0 and Rv.subs(x, 300) == 21000
    V = R(8, 3)*T_**R(3, 2)
    assert same_primitive(V, 4*sp.sqrt(T_), T_) and V.subs(T_, 9) == 72
    return True


validate()

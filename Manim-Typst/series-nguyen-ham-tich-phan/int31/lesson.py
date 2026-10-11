"""INT31 – Bồn chứa, bể nước và lưu lượng.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT31',
    'number': 31,
    'title': 'Bồn chứa và lưu lượng',
    'subtitle': 'Lượng nước bằng tích phân của lưu lượng',
    'next_code': 'INT32',
    'next_title': 'Tích phân trong kinh tế và sinh học',
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
         'Một bể rỗng chứa được một nghìn lít. Vòi nước mở càng lúc càng mạnh, lưu lượng hai mươi cộng bốn t lít mỗi phút. '
         'Bao lâu thì đầy bể? Không thể lấy một nghìn chia cho lưu lượng, vì lưu lượng thay đổi liên tục. '
         'Đáp số là khoảng mười bảy phẩy chín phút, và tích phân cho ta câu trả lời.',
         'Mở đầu: lưu lượng thay đổi'),
    Beat('h2', 'hook',
         'Đây là tập ba mươi mốt của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: bồn chứa, bể nước và lưu lượng.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, lượng nước bằng tích phân của lưu lượng. '
         'Hai, bài toán vừa chảy vào vừa chảy ra. Ba, liên hệ giữa lượng nước và mực nước trong bể.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Lưu lượng là tốc độ thay đổi của thể tích nước: V phẩy của t bằng r của t. '
         'Vì vậy thể tích nước thay đổi một lượng bằng tích phân của lưu lượng: V của T trừ V của không '
         'bằng tích phân từ không đến T của r. Đây lại là công thức Newton Leibniz, với một ý nghĩa mới.',
         'Lưu lượng là đạo hàm của thể tích'),
    Beat('c2', 'core',
         'Trên đồ thị lưu lượng theo thời gian, lượng nước chảy vào chính là diện tích dưới đồ thị. '
         'Lưu lượng không đổi thì diện tích là hình chữ nhật, quen thuộc như lưu lượng nhân thời gian. '
         'Lưu lượng thay đổi thì ta cần tích phân.'),
    Beat('c2b', 'core',
         'Vì sao là tích phân? Chia thời gian thành nhiều khoảng nhỏ. Trong mỗi khoảng, lưu lượng gần như không đổi, '
         'nên lượng nước xấp xỉ r của t nhân delta t, một cột hình chữ nhật. Cộng các cột lại và cho khoảng chia nhỏ dần, '
         'tổng tiến tới tích phân, giống hệt tập mười một.'),
    Beat('c3', 'core',
         'Khi vừa có nước chảy vào, vừa có nước chảy ra, lưu lượng thực bằng lưu lượng vào trừ lưu lượng ra. '
         'Lượng nước trong bể tăng khi lưu lượng thực dương, giảm khi lưu lượng thực âm, '
         'và đạt lớn nhất đúng lúc lưu lượng vào bằng lưu lượng ra.',
         'Vào và ra'),
    Beat('c4', 'core',
         'Với bể hình trụ diện tích đáy S, thể tích nước bằng S nhân chiều cao mực nước. '
         'Vì vậy mực nước dâng thêm một lượng bằng lượng nước chảy vào chia cho S, '
         'và tốc độ dâng bằng lưu lượng chia S.',
         'Mực nước trong bể trụ'),
    Beat('c5', 'core',
         'Cẩn thận với đơn vị: một mét khối bằng một nghìn lít, một phút bằng sáu mươi giây. '
         'Lưu lượng cho theo lít mỗi phút thì thời gian phải tính bằng phút. '
         'Rất nhiều lỗi sai trong bài thực tế đến từ đơn vị chứ không phải từ tích phân.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. Lượng nước sau T phút bằng tích phân từ không đến T của hai mươi cộng bốn t, '
         'bằng hai mươi T cộng hai T bình phương. Cho bằng một nghìn, giải phương trình bậc hai, '
         'lấy nghiệm dương: T bằng trừ năm cộng năm căn hai mốt, khoảng mười bảy phẩy chín một phút.',
         'Ví dụ 1: thời gian đầy bể'),
    Beat('e2', 'examples',
         'Ví dụ hai: bể đang có hai trăm lít. Nước chảy vào ba mươi lít mỗi phút, chảy ra hai t lít mỗi phút. '
         'Thể tích V của t bằng hai trăm cộng ba mươi t trừ t bình phương. '
         'Lớn nhất khi ba mươi bằng hai t, tức t bằng mười lăm, lúc đó bể có bốn trăm hai mươi lăm lít.',
         'Ví dụ 2: vừa vào vừa ra'),
    Beat('e3', 'examples',
         'Sau thời điểm đó, nước ra nhiều hơn vào. Bể cạn khi hai trăm cộng ba mươi t trừ t bình phương bằng không, '
         'tức t bằng mười lăm cộng căn bốn trăm hai mươi lăm, khoảng ba mươi lăm phẩy sáu hai phút.'),
    Beat('e4', 'examples',
         'Ví dụ ba: bể trụ có diện tích đáy hai mét vuông. Nước chảy vào với lưu lượng không phẩy một t mét khối mỗi phút. '
         'Sau mười phút, lượng nước vào là tích phân từ không đến mười của không phẩy một t, bằng năm mét khối. '
         'Mực nước dâng năm chia hai, bằng hai phẩy năm mét.',
         'Ví dụ 3: mực nước dâng'),
    Beat('e5', 'examples',
         'Ví dụ bốn, đọc đồ thị: máy bơm khởi động trong hai phút, lưu lượng tăng đều từ không lên sáu mươi lít mỗi phút, '
         'bơm đều mười phút, rồi tắt dần trong hai phút. Lượng nước bơm được là diện tích hình thang: '
         'sáu mươi cộng sáu trăm cộng sáu mươi, bằng bảy trăm hai mươi lít.',
         'Ví dụ 4: đọc đồ thị lưu lượng'),
    Beat('e6', 'examples',
         'Ví dụ năm: một bể bị rò rỉ với lưu lượng tám nhân e mũ trừ t chia mười lít mỗi phút, giảm dần theo thời gian. '
         'Mười phút đầu rò mất tám mươi nhân một trừ một phần e, khoảng năm mươi phẩy năm bảy lít. '
         'Dù rò mãi mãi, tổng lượng nước mất cũng không vượt quá tám mươi lít, vì e mũ trừ t chia mười tiến về không.',
         'Ví dụ 5: bể rò rỉ'),
    Beat('e7', 'examples',
         'Ví dụ sáu, bài toán ngược: bể chín trăm lít đầy sau đúng mười phút với lưu lượng a cộng sáu t. Tìm a. '
         'Lượng nước sau mười phút là mười a cộng ba trăm. Cho bằng chín trăm, được a bằng sáu mươi lít mỗi phút.',
         'Ví dụ 6: tìm tham số'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Một bể chứa được năm trăm lít, đang có một trăm lít. Nước chảy vào với lưu lượng '
         'ba t bình phương lít mỗi phút. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: V bằng một trăm cộng tích phân của ba u bình phương từ không đến t, bằng một trăm cộng t lập phương. '
         'Ý b đúng: sau bốn phút, bể có một trăm sáu mươi tư lít.'),
    Beat('x3', 'exam',
         'Ý c sai: bể đầy khi t lập phương bằng bốn trăm, t khoảng bảy phẩy ba bảy phút, không phải tám. '
         'Ý d đúng: lượng nước vào trong phút thứ ba, từ hai đến ba, bằng hai mươi bảy trừ tám, bằng mười chín lít.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: một bồn rỗng chứa được hai nghìn lít, nước chảy vào với lưu lượng năm mươi cộng hai t lít mỗi phút. '
         'Sau bao nhiêu phút thì đầy bồn? Làm tròn đến hàng phần mười.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Lượng nước sau T phút bằng năm mươi T cộng T bình phương. Cho bằng hai nghìn: T bình phương cộng năm mươi T trừ hai nghìn '
         'bằng không, nghiệm dương T bằng trừ hai lăm cộng căn hai nghìn sáu trăm hai lăm, khoảng hai mươi sáu phẩy hai phút. '
         'Ghi vào phiếu: hai, sáu, phẩy, hai.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, lượng nước bằng tích phân của lưu lượng, là diện tích dưới đồ thị lưu lượng. '
         'Hai, vào và ra: lấy hiệu, lượng nước lớn nhất khi hai lưu lượng bằng nhau. '
         'Ba, bể trụ: mực nước dâng bằng lượng nước chia diện tích đáy, và luôn kiểm tra đơn vị.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, lưu lượng mười cộng hai t lít mỗi phút, tính lượng nước sau mười phút. '
         'Hai, bể rỗng, vào hai mươi lít mỗi phút, ra t lít mỗi phút: lượng nước lớn nhất. '
         'Ba, bể trụ đáy bốn mét vuông, lưu lượng không phẩy hai t mét khối mỗi phút: mực nước dâng sau mười phút. '
         'Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập ba mươi hai, cùng ý tưởng này áp dụng cho kinh tế và sinh học: chi phí biên, lợi nhuận, tốc độ tăng trưởng. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "r(t) = 20 + 4t quad (\"L\"\\/\"phút\"), quad V_\"bể\" = 1000 \"L\"",
    'flow': "V'(t) = r(t) arrow.double.long V(T) - V(0) = integral_0^T r(t) dif t",
    'net': "r_\"thực\" = r_\"vào\" - r_\"ra\"",
    'peak': "V_max arrow.l.r.double r_\"vào\" = r_\"ra\"",
    'level': "Delta h = (Delta V)/S, quad h'(t) = r(t)/S",
    'units': "1 \"m\"^3 = 1000 \"L\", quad 1 \"phút\" = 60 \"s\"",
    'e1_s1': "integral_0^T (20 + 4t) dif t = 20T + 2T^2 = 1000",
    'e1_s2': "T = -5 + 5 sqrt(21) approx gold(\"17,91\") \"phút\"",
    'e2_s1': "V(t) = 200 + integral_0^t (30 - 2u) dif u = 200 + 30t - t^2",
    'e2_s2': "30 = 2t arrow.double.long t = 15, quad V_max = V(15) = gold(425) \"L\"",
    'e3_s1': "200 + 30t - t^2 = 0 arrow.double.long t = 15 + sqrt(425) approx gold(\"35,62\") \"phút\"",
    'e4_s1': "Delta V = integral_0^10 \"0,1\" t dif t = 5 \"m\"^3",
    'e4_s2': "Delta h = 5/2 = gold(\"2,5\") \"m\"",
    'e5_s1': "V = 60 + 600 + 60 = gold(720) \"L\"",
    'riem': "V approx sum r(t_i) Delta t arrow.r integral_0^T r(t) dif t",
    'leak1': "integral_0^10 8 e^(-t\\/10) dif t = 80(1 - 1/e) approx gold(\"50,57\") \"L\"",
    'leak2': "integral_0^T 8 e^(-t\\/10) dif t = 80(1 - e^(-T\\/10)) < 80",
    'inv1': "integral_0^10 (a + 6t) dif t = 10a + 300 = 900",
    'inv2': "a = gold(60) quad (\"L\"\\/\"phút\")",
    'tf_given': "V(0) = 100 \"L\", quad r(t) = 3t^2 quad (\"L\"\\/\"phút\"), quad V_max = 500 \"L\"",
    'tf_a': "V(t) = 100 + t^3",
    'tf_b': "V(4) = 164",
    'tf_c': "\"Đầy bể lúc\" t = 8",
    'tf_d': "integral_2^3 3t^2 dif t = 19",
    'tf_c_calc': "t^3 = 400 arrow.double.long t = root(3, 400) approx \"7,37\" coral(!= 8)",
    'sa_s1': "integral_0^T (50 + 2t) dif t = 50T + T^2 = 2000",
    'sa_s2': "T = -25 + sqrt(2625) approx gold(\"26,2\") \"phút\"",
    'sum1': "Delta V = integral_0^T r(t) dif t",
    'sum2': "r_\"vào\" = r_\"ra\" arrow.double.long V_max",
    'sum3': "Delta h = (Delta V)/S",
    'hw1': "r = 10 + 2t, quad T = 10",
    'hw2': "r_\"vào\" = 20, quad r_\"ra\" = t, quad V(0) = 0",
    'hw3': "S = 4 \"m\"^2, quad r = \"0,2\" t, quad T = 10",
    'hw_ans1': "200 \"L\"",
    'hw_ans2': "200 \"L\"",
    'hw_ans3': "\"2,5\" \"m\"",
    'next1': "C(x) = C(0) + integral_0^x C'(u) dif u",
}

EXERCISES = (
    ('r = 10 + 2t (L/phút): lượng nước sau 10 phút', '200 L'),
    ('Vào 20 L/phút, ra t L/phút, bể rỗng: lượng nước lớn nhất', '200 L'),
    ('Bể trụ đáy 4 m², r = 0,2t m³/phút: mực nước dâng sau 10 phút', '2,5 m'),
)

TRUE_FALSE = (
    ('V(t) = 100 + t³', True),
    ('V(4) = 164', True),
    ('Đầy bể lúc t = 8', False),
    ('Phút thứ 3 vào 19 L', True),
)

t, u, T = sp.symbols('t u T', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R = sp.integrate, sp.Rational
    pos = lambda sols: [s for s in sols if s.is_positive]  # noqa: E731
    # hook / e1
    assert sp.expand(I(20 + 4 * t, (t, 0, T)) - (20 * T + 2 * T**2)) == 0
    T1 = pos(sp.solve(20 * T + 2 * T**2 - 1000, T))[0]
    assert sp.simplify(T1 - (-5 + 5 * sp.sqrt(21))) == 0 and f'{float(T1):.2f}' == '17.91'
    # e2 / e3
    V = 200 + I(30 - 2 * u, (u, 0, t))
    assert sp.expand(V - (200 + 30 * t - t**2)) == 0
    assert sp.solve(sp.diff(V, t), t) == [15] and V.subs(t, 15) == 425
    te = pos(sp.solve(V, t))[0]
    assert sp.simplify(te - (15 + sp.sqrt(425))) == 0 and f'{float(te):.2f}' == '35.62'
    # e4
    dV = I(R(1, 10) * t, (t, 0, 10))
    assert dV == 5 and dV / 2 == R(5, 2)
    # e5 (trapezoid)
    rg = sp.Piecewise((30 * t, t <= 2), (60, t <= 12), (60 - 30 * (t - 12), True))
    assert I(rg, (t, 0, 14)) == 720 and (I(rg, (t, 0, 2)), I(rg, (t, 2, 12)), I(rg, (t, 12, 14))) == (60, 600, 60)
    lk = I(8 * sp.exp(-t / 10), (t, 0, 10))
    assert sp.simplify(lk - 80 * (1 - sp.exp(-1))) == 0 and f'{float(lk):.2f}' == '50.57'
    assert sp.simplify(I(8 * sp.exp(-t / 10), (t, 0, T)) - 80 * (1 - sp.exp(-T / 10))) == 0
    assert sp.limit(80 * (1 - sp.exp(-T / 10)), T, sp.oo) == 80
    a6 = sp.symbols('a6')
    assert sp.expand(I(a6 + 6 * t, (t, 0, 10)) - (10 * a6 + 300)) == 0 and sp.solve(10 * a6 + 300 - 900, a6) == [60]
    # true / false
    Vt = 100 + I(3 * u**2, (u, 0, t))
    tfull = sp.real_root(400, 3)
    claims = (sp.expand(Vt - (100 + t**3)) == 0, Vt.subs(t, 4) == 164, Vt.subs(t, 8) == 500,
              I(3 * t**2, (t, 2, 3)) == 19)
    assert sp.simplify(Vt.subs(t, tfull) - 500) == 0 and f'{float(tfull):.2f}' == '7.37'
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    Ts = pos(sp.solve(50 * T + T**2 - 2000, T))[0]
    assert sp.simplify(Ts - (-25 + sp.sqrt(2625))) == 0 and f'{float(Ts):.1f}' == '26.2'
    assert sp.expand(I(50 + 2 * t, (t, 0, T)) - (50 * T + T**2)) == 0
    # exercises
    assert I(10 + 2 * t, (t, 0, 10)) == 200
    W = I(20 - u, (u, 0, t))
    assert sp.solve(sp.diff(W, t), t) == [20] and W.subs(t, 20) == 200
    assert I(R(2, 10) * t, (t, 0, 10)) / 4 == R(5, 2)
    return True


validate()

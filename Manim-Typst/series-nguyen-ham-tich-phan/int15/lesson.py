"""INT15 – Tích phân, độ dời và quãng đường: v(t), a(t).

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT15',
    'number': 15,
    'title': 'Độ dời và quãng đường',
    'subtitle': 'Tích phân của vận tốc, gia tốc',
    'next_code': 'INT16',
    'next_title': 'Tích phân đổi biến số',
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
         'Một chất điểm chuyển động trên đường thẳng với vận tốc v bằng t bình phương trừ bốn t cộng ba, mét trên giây. '
         'Sau bốn giây, nó chỉ cách vị trí ban đầu bốn phần ba mét. Nhưng tổng quãng đường nó đã đi lại là bốn mét, '
         'gấp ba lần! Chuyện gì đã xảy ra?',
         'Mở đầu: cách chỗ cũ 4/3 m nhưng đã đi 4 m'),
    Beat('h2', 'hook',
         'Đây là tập mười lăm của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'tích phân, độ dời và quãng đường.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ phân biệt rõ ba điều. Một, tích phân của vận tốc là độ dời. '
         'Hai, tích phân của trị tuyệt đối vận tốc là quãng đường. Ba, tích phân của gia tốc là độ thay đổi vận tốc.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Gọi s của t là tọa độ của chất điểm. Vận tốc là đạo hàm của tọa độ, nên s là một nguyên hàm của v. '
         'Theo công thức Newton Leibniz, tích phân từ a đến b của v bằng s của b trừ s của a: '
         'đó là độ dời, tức là vị trí cuối trừ vị trí đầu.',
         'Tích phân của vận tốc là độ dời'),
    Beat('c2', 'core',
         'Hãy xem chất điểm ở bài mở đầu chạy. Từ không đến một giây, v dương, nó tiến lên bốn phần ba mét. '
         'Từ một đến ba giây, v âm, nó quay đầu lùi lại bốn phần ba mét, về đúng chỗ cũ. '
         'Từ ba đến bốn giây, nó lại tiến bốn phần ba mét.'),
    Beat('c2b', 'core',
         'Nhìn lại đồ thị tọa độ s của t: nó đi lên, rồi đi xuống, rồi lại đi lên. Những thời điểm chất điểm đổi chiều, '
         't bằng một và t bằng ba, chính là các điểm cực trị của s, nơi đạo hàm v bằng không và đổi dấu. '
         'Vậy muốn tìm lúc đổi chiều, ta giải v bằng không và kiểm tra v có đổi dấu hay không.'),
    Beat('c3', 'core',
         'Trên đồ thị vận tốc, phần nằm dưới trục ứng với lúc chạy lùi. Tích phân của v là diện tích có dấu, '
         'nên phần lùi bị trừ đi: độ dời bằng bốn phần ba. Quãng đường thì đếm mọi mét đã đi, '
         'nên ta lật phần âm lên: quãng đường là tích phân của trị tuyệt đối v, bằng bốn.',
         'Quãng đường: tích phân của |v|'),
    Beat('c4', 'core',
         'Như vậy, khi vận tốc không đổi dấu, độ dời và quãng đường có độ lớn bằng nhau. '
         'Khi vận tốc đổi dấu, tức là chất điểm đổi chiều, ta phải dùng đúng quy trình của tập mười bốn: '
         'giải v bằng không, xét dấu, rồi tách cận.'),
    Beat('c5', 'core',
         'Cùng ý tưởng cho gia tốc. Gia tốc là đạo hàm của vận tốc, nên tích phân của a từ t một đến t hai bằng '
         'v của t hai trừ v của t một. Muốn biết vận tốc tại thời điểm t, ta lấy vận tốc ban đầu cộng tích phân của gia tốc.',
         'Gia tốc và vận tốc'),
    Beat('c6', 'core',
         'Một mẹo kiểm tra nhanh bằng đơn vị: diện tích dưới đồ thị vận tốc theo thời gian có đơn vị mét trên giây nhân giây, '
         'tức là mét. Diện tích dưới đồ thị gia tốc có đơn vị mét trên giây. '
         'Nếu đơn vị không khớp với câu hỏi, em đã chọn sai hàm để lấy tích phân.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, hoàn thành bài mở đầu. Giải t bình phương trừ bốn t cộng ba bằng không, được t bằng một và t bằng ba. '
         'Xét dấu: dương, âm, dương. Ba tích phân lần lượt là bốn phần ba, âm bốn phần ba và bốn phần ba. '
         'Độ dời là tổng có dấu, bằng bốn phần ba. Quãng đường là tổng độ lớn, bằng bốn.',
         'Ví dụ 1: độ dời và quãng đường'),
    Beat('e2', 'examples',
         'Ví dụ hai: một vật xuất phát từ trạng thái nghỉ với gia tốc a bằng sáu trừ hai t. '
         'Vận tốc bằng không cộng tích phân của gia tốc, được v bằng sáu t trừ t bình phương. '
         'Vật dừng lại khi t bằng sáu giây, và trong khoảng đó v không âm.',
         'Ví dụ 2: từ gia tốc đến quãng đường'),
    Beat('e3', 'examples',
         'Vậy quãng đường vật đi được cho đến khi dừng là tích phân từ không đến sáu của sáu t trừ t bình phương, '
         'bằng một trăm lẻ tám trừ bảy mươi hai, bằng ba mươi sáu mét.'),
    Beat('e3b', 'examples',
         'Đề thi còn hay hỏi thêm hai ý. Vận tốc lớn nhất đạt được khi gia tốc bằng không, tức là t bằng ba, '
         'khi đó v bằng chín mét trên giây. Còn tốc độ trung bình bằng quãng đường chia thời gian: '
         'ba mươi sáu chia sáu, bằng sáu mét trên giây. Chú ý: tốc độ trung bình không phải trung bình cộng của các vận tốc.'),
    Beat('e4', 'examples',
         'Ví dụ ba: đọc đồ thị. Một ô tô tăng tốc đều từ không lên mười mét trên giây trong bốn giây, '
         'chạy đều sáu giây, rồi phanh dừng hẳn trong hai giây. Quãng đường là diện tích hình thang dưới đồ thị: '
         'hai mươi cộng sáu mươi cộng mười, bằng chín mươi mét. Không cần viết công thức của v!',
         'Ví dụ 3: đọc đồ thị vận tốc'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Một chất điểm có vận tốc v bằng ba t bình phương trừ sáu t, mét trên giây, '
         'với t từ không đến ba giây. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: tích phân từ không đến ba của ba t bình phương trừ sáu t bằng hai mươi bảy trừ hai mươi bảy, bằng không. '
         'Chất điểm quay về đúng chỗ xuất phát. Ý b sai: độ dời bằng không nhưng quãng đường thì không.'),
    Beat('x3', 'exam',
         'Ý c đúng: v âm trên khoảng từ không đến hai và dương sau đó, nên chất điểm đổi chiều tại t bằng hai. '
         'Ý d sai: gia tốc là sáu t trừ sáu, tại t bằng hai gia tốc bằng sáu. '
         'Đừng nhầm: vận tốc bằng không không có nghĩa là gia tốc bằng không.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn. Một ô tô đang chạy với vận tốc mười lăm mét trên giây thì phanh, '
         'vận tốc sau đó là v bằng mười lăm trừ ba t. Hỏi từ lúc phanh đến khi dừng hẳn, ô tô đi thêm bao nhiêu mét?',
         'Câu trả lời ngắn: quãng đường phanh'),
    Beat('x5', 'exam',
         'Ô tô dừng khi v bằng không, tức là t bằng năm giây. Quãng đường bằng tích phân từ không đến năm '
         'của mười lăm trừ ba t, bằng bảy mươi lăm trừ ba mươi bảy phẩy năm, bằng ba mươi bảy phẩy năm mét. '
         'Ghi vào phiếu: ba, bảy, phẩy, năm. Bẫy thường gặp là lấy cận trên tùy ý thay vì thời điểm dừng.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, độ dời bằng tích phân của v, là diện tích có dấu. '
         'Hai, quãng đường bằng tích phân của trị tuyệt đối v: xét dấu v, tách cận tại lúc đổi chiều. '
         'Ba, vận tốc bằng vận tốc ban đầu cộng tích phân của gia tốc.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, v bằng hai t trừ bốn, tính quãng đường trong năm giây đầu. '
         'Hai, a bằng bốn trừ hai t và vận tốc ban đầu bằng năm, tính vận tốc tại t bằng ba. '
         'Ba, ô tô phanh với v bằng mười hai trừ bốn t, tính quãng đường đến khi dừng. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập mười sáu, ta học phương pháp đổi biến số trong tích phân, với nguyên tắc vàng: '
         'đổi biến thì phải đổi cận. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook_v': "v(t) = t^2 - 4t + 3 quad (\"m/s\"), quad t in [0; 4]",
    'h_d': "Delta s = 4/3 \"m\"",
    'h_s': "S = 4 \"m\"",
    'disp': "integral_a^b v(t) dif t = s(b) - s(a)",
    'dist': "S = integral_a^b abs(v(t)) dif t",
    'ineq': "abs(integral_a^b v(t) dif t) <= integral_a^b abs(v(t)) dif t",
    'pos': "s(t) = t^3/3 - 2t^2 + 3t",
    'vel': "integral_(t_1)^(t_2) a(t) dif t = v(t_2) - v(t_1)",
    'dv': "v(t_2) - v(t_1)",
    'vel2': "v(t) = v(0) + integral_0^t a(u) dif u",
    'units': "[\"m/s\"] times [\"s\"] = [\"m\"], quad [\"m/s\"^2] times [\"s\"] = [\"m/s\"]",
    'e1_s1': "t^2 - 4t + 3 = 0 arrow.double.long t = 1, quad t = 3",
    'e1_s2': "integral_0^1 v dif t = 4/3, quad integral_1^3 v dif t = -4/3, quad integral_3^4 v dif t = 4/3",
    'e1_d': "Delta s = 4/3 - 4/3 + 4/3 = gold(4/3)",
    'e1_s': "S = 4/3 + 4/3 + 4/3 = gold(4)",
    'e2_a': "a(t) = 6 - 2t, quad v(0) = 0",
    'e2_v': "v(t) = 0 + integral_0^t (6 - 2u) dif u = 6t - t^2",
    'e2_stop': "v(t) = 0 arrow.double.long t = 6",
    'e3_s': "S = integral_0^6 (6t - t^2) dif t = 108 - 72 = gold(36)",
    'vmax': "a(t) = 0 arrow.double.long t = 3, quad v_max = v(3) = gold(9)",
    'vavg': "v_\"tb\" = S / (Delta t) = 36 / 6 = gold(6)",
    'e4_s': "S = 20 + 60 + 10 = gold(90)",
    'tf_given': "v(t) = 3t^2 - 6t quad (\"m/s\"), quad t in [0; 3]",
    'tf_a': "integral_0^3 v(t) dif t = 0",
    'tf_b': "S = 0 \"m\"",
    'tf_c': "t = 2",
    'tf_d': "a(2) = 0",
    'tf_b_calc': "S = integral_0^2 (6t - 3t^2) dif t + integral_2^3 (3t^2 - 6t) dif t = 4 + 4 = 8",
    'tf_d_calc': "a(t) = v'(t) = 6t - 6 arrow.double.long a(2) = 6 coral(!= 0)",
    'sa_task': "v(t) = 15 - 3t quad (\"m/s\")",
    'sa_s1': "v(t) = 0 arrow.double.long t = 5",
    'sa_s2': "S = integral_0^5 (15 - 3t) dif t = 75 - \"37,5\" = gold(\"37,5\")",
    'sum1': "Delta s = integral_a^b v dif t",
    'sum2': "S = integral_a^b abs(v) dif t",
    'sum3': "v(t) = v_0 + integral_0^t a",
    'hw1': "v = 2t - 4, quad t in [0; 5], quad S = ?",
    'hw2': "a = 4 - 2t, quad v(0) = 5, quad v(3) = ?",
    'hw3': "v = 12 - 4t, quad S_\"phanh\" = ?",
    'hw_ans1': "13",
    'hw_ans2': "8",
    'hw_ans3': "18",
    'next1': "integral_0^1 2x(x^2 + 1)^3 dif x",
    'next2': "u = x^2 + 1: quad x = 0 arrow.r u = 1, quad x = 1 arrow.r u = 2",
}

EXERCISES = (
    ('v = 2t − 4, t ∈ [0; 5]: quãng đường?', '13'),
    ('a = 4 − 2t, v(0) = 5: v(3)?', '8'),
    ('v = 12 − 4t: quãng đường phanh?', '18'),
)

TRUE_FALSE = (
    ('∫₀³ v(t) dt = 0', True),
    ('Quãng đường S = 0 m', False),
    ('Chất điểm đổi chiều tại t = 2', True),
    ('a(2) = 0', False),
)

t = sp.symbols('t', real=True)


def abs_integral(expr, lo, hi):
    """∫|expr| on [lo, hi]: split at the roots, add |piece| (the INT14 method)."""
    cuts = sorted({sp.sympify(lo), sp.sympify(hi), *sp.solveset(expr, t, sp.Interval(lo, hi))}, key=float)
    return sp.nsimplify(sum(abs(sp.integrate(expr, (t, p, q))) for p, q in zip(cuts, cuts[1:])))


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, AI = sp.integrate, sp.Rational, abs_integral
    v = t**2 - 4*t + 3
    s = t**3 / 3 - 2*t**2 + 3*t
    assert sp.diff(s, t) == v and s.subs(t, 0) == 0
    assert [s.subs(t, k) for k in (1, 3, 4)] == [R(4, 3), 0, R(4, 3)]
    assert sorted(sp.solve(v, t)) == [1, 3]
    assert [I(v, (t, 0, 1)), I(v, (t, 1, 3)), I(v, (t, 3, 4))] == [R(4, 3), -R(4, 3), R(4, 3)]
    assert I(v, (t, 0, 4)) == R(4, 3) and AI(v, 0, 4) == 4
    # from acceleration
    u = sp.symbols('u')
    vel = I(6 - 2*u, (u, 0, t))
    assert sp.expand(vel - (6*t - t**2)) == 0 and sp.solve(vel, t) == [0, 6]
    assert all(vel.subs(t, k) >= 0 for k in range(7))
    assert I(vel, (t, 0, 6)) == 36 and 108 - 72 == 36
    assert sp.solve(sp.diff(vel, t), t) == [3] and vel.subs(t, 3) == 9 and max(vel.subs(t, k) for k in range(7)) == 9
    assert sp.Rational(36, 6) == 6
    # graph reading (trapezoid): 0 -> 10 m/s in 4 s, 10 m/s for 6 s, 10 -> 0 in 2 s
    vg = sp.Piecewise((R(10, 4)*t, t <= 4), (10, t <= 10), (10 - 5*(t - 10), True))
    assert I(vg, (t, 0, 12)) == 90 and (I(vg, (t, 0, 4)), I(vg, (t, 4, 10)), I(vg, (t, 10, 12))) == (20, 60, 10)
    # true / false
    w = 3*t**2 - 6*t
    acc = sp.diff(w, t)
    claims = (I(w, (t, 0, 3)) == 0, AI(w, 0, 3) == 0,
              sp.solve(w, t) == [0, 2] and w.subs(t, 1) < 0 and w.subs(t, R(5, 2)) > 0, acc.subs(t, 2) == 0)
    assert I(6*t - 3*t**2, (t, 0, 2)) == 4 and I(w, (t, 2, 3)) == 4 and AI(w, 0, 3) == 8 and acc.subs(t, 2) == 6
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer: braking
    assert sp.solve(15 - 3*t, t) == [5] and I(15 - 3*t, (t, 0, 5)) == R(75, 2)
    # exercises
    assert AI(2*t - 4, 0, 5) == 13
    assert (5 + I(4 - 2*u, (u, 0, t))).subs(t, 3) == 8
    assert sp.solve(12 - 4*t, t) == [3] and I(12 - 4*t, (t, 0, 3)) == 18
    assert [a for _, a in EXERCISES] == ['13', '8', '18']
    return True


validate()

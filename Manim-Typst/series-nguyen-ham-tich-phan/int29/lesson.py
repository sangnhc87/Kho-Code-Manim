"""INT29 – Bài toán chuyển động thực tế: phanh xe, hai xe gặp nhau.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT29',
    'number': 29,
    'title': 'Bài toán chuyển động thực tế',
    'subtitle': 'Phanh xe, đuổi kịp, hai xe gặp nhau',
    'next_code': 'INT30',
    'next_title': 'Thiết kế: cổng parabol, logo, mảnh vườn',
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
         'Xe A chạy đều hai mươi mét trên giây. Cùng lúc, xe B xuất phát từ trạng thái nghỉ tại cùng vị trí, '
         'tăng tốc với vận tốc v bằng hai t. Khi nào B đuổi kịp A? Nhiều bạn trả lời: lúc mười giây, khi hai đồ thị vận tốc cắt nhau. '
         'Sai! Lúc đó khoảng cách hai xe lại xa nhất. Đáp số đúng là hai mươi giây.',
         'Mở đầu: hai đồ thị cắt nhau có phải là gặp nhau?'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi chín, mở đầu phần D về ứng dụng thực tế: bài toán chuyển động, '
         'từ phanh xe đến hai xe gặp nhau.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, vị trí bằng vị trí ban đầu cộng tích phân của vận tốc. '
         'Hai, gặp nhau khi hai vị trí bằng nhau, tức là hai diện tích bằng nhau. '
         'Ba, bài toán phanh xe và khoảng cách an toàn.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Nhắc lại từ tập mười lăm: vị trí tại thời điểm t bằng vị trí ban đầu cộng tích phân từ không đến t của vận tốc. '
         'Với nhiều xe, ta viết riêng vị trí của từng xe trên cùng một trục tọa độ, chọn gốc và chiều dương rõ ràng.',
         'Vị trí từ vận tốc'),
    Beat('c2', 'core',
         'Hai xe gặp nhau khi vị trí của chúng bằng nhau. Nếu hai xe xuất phát cùng lúc, cùng chỗ, cùng chiều, '
         'điều kiện này có nghĩa là diện tích dưới hai đồ thị vận tốc, từ không đến t, bằng nhau.',
         'Gặp nhau: hai diện tích bằng nhau'),
    Beat('c3', 'core',
         'Vậy giao điểm của hai đồ thị vận tốc nói gì? Đó là lúc hai xe có cùng vận tốc. Trước thời điểm đó, '
         'một xe nhanh hơn nên khoảng cách tăng dần; sau đó, xe kia nhanh hơn nên khoảng cách giảm. '
         'Vì thế giao điểm là lúc khoảng cách lớn nhất, không phải lúc gặp nhau.',
         'Giao điểm đồ thị vận tốc'),
    Beat('c4', 'core',
         'Bài toán phanh: xe đang chạy với vận tốc v không, phanh với gia tốc không đổi độ lớn a. '
         'Vận tốc v bằng v không trừ a t, xe dừng khi t bằng v không chia a. '
         'Quãng đường phanh bằng tích phân, cho kết quả v không bình phương chia hai a.',
         'Bài toán phanh xe'),
    Beat('c5', 'core',
         'Hai chú ý về đơn vị. Vận tốc thường cho bằng ki lô mét trên giờ, phải đổi sang mét trên giây bằng cách chia ba phẩy sáu. '
         'Và thời gian phản xạ: trước khi phanh, xe vẫn chạy đều trong khoảng thời gian người lái phản ứng.',
         'Đơn vị và thời gian phản xạ'),
    Beat('c6', 'core',
         'Quy trình bốn bước cho mọi bài hai xe. Một, chọn gốc tọa độ, chiều dương và mốc thời gian. '
         'Hai, viết vận tốc của từng xe, chú ý xe nào xuất phát muộn hơn. Ba, viết vị trí của từng xe bằng tích phân. '
         'Bốn, giải phương trình hai vị trí bằng nhau, và loại nghiệm không phù hợp.',
         'Quy trình bốn bước'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu. Vị trí xe A là hai mươi t, vị trí xe B là tích phân của hai t, bằng t bình phương. '
         'Gặp nhau khi t bình phương bằng hai mươi t, tức t bằng hai mươi giây, lúc đó cả hai đi được bốn trăm mét.',
         'Ví dụ 1: đuổi kịp'),
    Beat('e2', 'examples',
         'Khoảng cách hai xe là hai mươi t trừ t bình phương, lớn nhất tại t bằng mười, đúng lúc hai vận tốc bằng nhau. '
         'Khi đó khoảng cách bằng hai trăm trừ một trăm, bằng một trăm mét. '
         'Trên hình, đó là phần diện tích nằm giữa hai đồ thị vận tốc từ không đến mười.'),
    Beat('e3', 'examples',
         'Ví dụ hai: ô tô chạy bảy mươi hai ki lô mét trên giờ, tức hai mươi mét trên giây, phanh với gia tốc năm mét trên giây bình phương. '
         'Xe dừng sau bốn giây. Quãng đường phanh bằng tích phân từ không đến bốn của hai mươi trừ năm t, bằng bốn mươi mét.',
         'Ví dụ 2: phanh xe'),
    Beat('e4', 'examples',
         'Ví dụ ba, khoảng cách an toàn: phía trước năm mươi mét có vật cản. Người lái mất một giây để phản xạ, '
         'xe đi thêm hai mươi mét, rồi phanh như ví dụ hai thêm bốn mươi mét. Tổng sáu mươi mét, lớn hơn năm mươi: va chạm!',
         'Ví dụ 3: khoảng cách an toàn'),
    Beat('e5', 'examples',
         'Muốn an toàn, quãng đường phanh tối đa còn ba mươi mét. Hai mươi bình phương chia hai a nhỏ hơn hoặc bằng ba mươi, '
         'suy ra a lớn hơn hoặc bằng hai mươi phần ba, khoảng sáu phẩy sáu bảy mét trên giây bình phương.'),
    Beat('e6', 'examples',
         'Ví dụ bốn, hai xe ngược chiều: cách nhau ba trăm mét, xe A chạy đều mười mét trên giây, xe B từ nghỉ với vận tốc hai t, '
         'chạy về phía A. Gặp nhau khi tổng quãng đường bằng ba trăm: mười t cộng t bình phương bằng ba trăm. '
         'Giải ra t bằng trừ năm cộng năm căn mười ba, khoảng mười ba giây.',
         'Ví dụ 4: ngược chiều'),
    Beat('e7', 'examples',
         'Ví dụ năm, xuất phát lệch giờ: xe A chạy đều mười mét trên giây. Hai giây sau, xe B xuất phát từ cùng chỗ với vận tốc '
         'bốn nhân t trừ hai. Vị trí xe B là tích phân từ hai đến t, bằng hai nhân t trừ hai, bình phương. '
         'Giải mười t bằng hai nhân t trừ hai bình phương, lấy nghiệm lớn hơn hai: khoảng tám phẩy năm ba giây.',
         'Ví dụ 5: xuất phát lệch giờ'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Xe A chạy đều mười lăm mét trên giây. Xe B xuất phát cùng lúc, cùng chỗ, từ trạng thái nghỉ, '
         'với vận tốc ba t. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: ba t bằng mười lăm khi t bằng năm. '
         'Ý b sai: tại t bằng năm, A đi bảy mươi lăm mét còn B chỉ đi ba mươi bảy phẩy năm mét.'),
    Beat('x3', 'exam',
         'Ý c đúng: khoảng cách lớn nhất tại t bằng năm, bằng bảy mươi lăm trừ ba mươi bảy phẩy năm, bằng ba mươi bảy phẩy năm mét. '
         'Ý d đúng: mười lăm t bằng một phẩy năm t bình phương cho t bằng mười.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: ô tô chạy năm mươi tư ki lô mét trên giờ thì người lái thấy vật cản. Sau không phẩy năm giây phản xạ, '
         'xe phanh với vận tốc v bằng mười lăm trừ năm t. Tính tổng quãng đường từ lúc thấy vật cản đến khi dừng.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Năm mươi tư ki lô mét trên giờ bằng mười lăm mét trên giây. Trong không phẩy năm giây phản xạ, xe đi bảy phẩy năm mét. '
         'Khi phanh, xe dừng sau ba giây và đi thêm hai mươi hai phẩy năm mét. Tổng cộng ba mươi mét. Ghi vào phiếu: ba, không.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, vị trí bằng vị trí đầu cộng tích phân của vận tốc. '
         'Hai, gặp nhau khi hai vị trí bằng nhau; giao điểm đồ thị vận tốc là lúc khoảng cách lớn nhất. '
         'Ba, phanh xe: quãng đường v không bình phương chia hai a, cộng thêm quãng đường phản xạ.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, xe A đều mười mét trên giây, xe B từ nghỉ với v bằng hai t, cùng chỗ: khi nào B đuổi kịp? '
         'Hai, xe ba mươi sáu ki lô mét trên giờ phanh với gia tốc hai: quãng đường phanh? '
         'Ba, v A bằng hai mươi, v B bằng bốn t: khoảng cách lớn nhất? Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập ba mươi, ta dùng tích phân để thiết kế: cổng hình parabol, logo, mảnh vườn, và tính chi phí theo diện tích. '
         'Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook_a': "v_A = 20, quad v_B = 2t",
    'pos': "s(t) = s(0) + integral_0^t v(u) dif u",
    'meet': "s_A (t) = s_B (t) arrow.l.r.double integral_0^t v_A = integral_0^t v_B",
    'gap': "d(t) = s_A (t) - s_B (t), quad d'(t) = v_A - v_B = 0",
    'brake1': "v = v_0 - a t = 0 arrow.double.long t = v_0/a",
    'brake2': "s = integral_0^(v_0\\/a) (v_0 - a t) dif t = (v_0^2)/(2a)",
    'kmh': "1 \"km/h\" = 1/(3\",\"6) \"m/s\"",
    'e1_s1': "s_A = 20 t, quad s_B = integral_0^t 2u dif u = t^2",
    'e1_s2': "t^2 = 20 t arrow.double.long t = gold(20) \"s\", quad s = 400 \"m\"",
    'e2_s1': "d(t) = 20t - t^2, quad d_max = d(10) = gold(100) \"m\"",
    'e3_s1': "72 \"km/h\" = 20 \"m/s\", quad v = 20 - 5t = 0 arrow.double.long t = 4",
    'e3_s2': "s = integral_0^4 (20 - 5t) dif t = gold(40) \"m\"",
    'e4_s1': "20 dot 1 + 40 = 60 > 50",
    'e5_s1': "(20^2)/(2a) <= 30 arrow.double.long a >= 20/3 approx gold(\"6,67\") \"m/s\"^2",
    'e6_s1': "10 t + t^2 = 300 arrow.double.long t = -5 + 5 sqrt(13) approx gold(\"13,03\") \"s\"",
    'late1': "v_B = 4(t - 2) quad (t >= 2), quad s_B = integral_2^t 4(u - 2) dif u = 2(t - 2)^2",
    'late2': "10 t = 2(t - 2)^2 arrow.double.long t = (9 + sqrt(65))/2 approx gold(\"8,53\") \"s\"",
    'tf_given': "v_A = 15, quad v_B = 3t quad (\"m/s\")",
    'tf_a': "t = 5: quad v_A = v_B",
    'tf_b': "t = 5: quad s_A = s_B",
    'tf_c': "d_max = \"37,5\" \"m\"",
    'tf_d': "t = 10: quad s_A = s_B",
    'tf_b_calc': "s_A (5) = 75, quad s_B (5) = integral_0^5 3t dif t = \"37,5\"",
    'tf_d_calc': "15 t = \"1,5\" t^2 arrow.double.long t = 10",
    'sa_s1': "54 \"km/h\" = 15 \"m/s\": quad s_1 = 15 dot \"0,5\" = \"7,5\"",
    'sa_s2': "s_2 = integral_0^3 (15 - 5t) dif t = \"22,5\" arrow.double.long s = gold(30) \"m\"",
    'sum1': "s(t) = s(0) + integral_0^t v",
    'sum2': "v_A = v_B arrow.double.long d_max",
    'sum3': "s = (v_0^2)/(2a)",
    'hw1': "v_A = 10, quad v_B = 2t",
    'hw2': "36 \"km/h\", quad a = 2",
    'hw3': "v_A = 20, quad v_B = 4t",
    'hw_ans1': "t = 10 \"s\"",
    'hw_ans2': "25 \"m\"",
    'hw_ans3': "50 \"m\"",
    'next1': "S = integral_a^b (f(x) - g(x)) dif x",
}

EXERCISES = (
    ('A đều 10 m/s, B từ nghỉ v = 2t, cùng chỗ: B đuổi kịp lúc', 't = 10 s'),
    ('Xe 36 km/h phanh với gia tốc 2 m/s²: quãng đường phanh', '25 m'),
    ('v_A = 20, v_B = 4t: khoảng cách lớn nhất', '50 m'),
)

TRUE_FALSE = (
    ('t = 5: v_A = v_B', True),
    ('t = 5: B đuổi kịp A', False),
    ('Khoảng cách lớn nhất 37,5 m', True),
    ('B đuổi kịp A lúc t = 10', True),
)

t, u = sp.symbols('t u', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R = sp.integrate, sp.Rational
    # hook / e1 / e2
    sA, sB = 20 * t, I(2 * u, (u, 0, t))
    assert sB == t**2 and sp.solve(sp.Eq(sA, sB), t) == [0, 20] and sA.subs(t, 20) == 400
    d = sA - sB
    assert sp.solve(sp.diff(d, t), t) == [10] and d.subs(t, 10) == 100 and 2 * 10 == 20
    # brake formula
    v0, a = sp.symbols('v0 a', positive=True)
    assert sp.simplify(I(v0 - a * t, (t, 0, v0 / a)) - v0**2 / (2 * a)) == 0
    # e3 / e4 / e5
    assert R(72, 1) / R(36, 10) == 20 and sp.solve(20 - 5 * t, t) == [4] and I(20 - 5 * t, (t, 0, 4)) == 40
    assert 20 * 1 + 40 == 60 > 50
    ap = sp.symbols('ap', positive=True)
    assert sp.solve(sp.Eq(R(400) / (2 * ap), 30), ap) == [R(20, 3)] and f'{20 / 3:.2f}' == '6.67'
    # e6
    roots = sp.solve(10 * t + t**2 - 300, t)
    tp = [r for r in roots if r.is_positive][0]
    assert sp.simplify(tp - (-5 + 5 * sp.sqrt(13))) == 0 and f'{float(tp):.2f}' == '13.03'
    sBl = I(4 * (u - 2), (u, 2, t))
    assert sp.expand(sBl - 2 * (t - 2)**2) == 0
    rl = [r for r in sp.solve(10 * t - 2 * (t - 2)**2, t) if r > 2][0]
    assert sp.simplify(rl - (9 + sp.sqrt(65)) / 2) == 0 and f'{float(rl):.2f}' == '8.53'
    # true / false
    sA2, sB2 = 15 * t, I(3 * u, (u, 0, t))
    claims = (3 * 5 == 15, sA2.subs(t, 5) == sB2.subs(t, 5), (sA2 - sB2).subs(t, 5) == R(75, 2),
              sp.solve(sp.Eq(sA2, sB2), t) == [0, 10])
    assert sp.solve(sp.diff(sA2 - sB2, t), t) == [5] and sB2.subs(t, 5) == R(75, 2)
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    assert R(54) / R(36, 10) == 15 and 15 * R(1, 2) == R(15, 2)
    assert sp.solve(15 - 5 * t, t) == [3] and I(15 - 5 * t, (t, 0, 3)) == R(45, 2) and R(15, 2) + R(45, 2) == 30
    # exercises
    assert sp.solve(sp.Eq(10 * t, t**2), t) == [0, 10]
    assert R(36) / R(36, 10) == 10 and R(10**2, 2 * 2) == 25
    dd = 20 * t - 2 * t**2
    assert sp.solve(sp.diff(dd, t), t) == [5] and dd.subs(t, 5) == 50
    return True


validate()

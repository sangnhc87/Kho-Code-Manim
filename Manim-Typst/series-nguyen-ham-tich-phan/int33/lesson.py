"""INT33 – Mô hình hóa từ dữ liệu thực: bảng số → hàm số → tích phân.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT33',
    'number': 33,
    'title': 'Mô hình hóa từ dữ liệu thực',
    'subtitle': 'Bảng số, hàm số, tích phân và quy tắc hình thang',
    'next_code': 'INT34',
    'next_title': 'Những bẫy sai kinh điển & kiểm tra bằng máy tính',
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


T_DATA = (0, 2, 4, 6, 8)
V_DATA = (0, 6, 10, 12, 12)

BEATS = (
    # ---------------- MỞ ĐẦU ----------------
    Beat('h1', 'hook',
         'Một chiếc xe được đo vận tốc mỗi hai giây: không, sáu, mười, mười hai, rồi mười hai mét trên giây. '
         'Không ai cho ta công thức của vận tốc, chỉ có một bảng số. Xe đã đi được bao xa trong tám giây? '
         'Có hai cách trả lời: tìm một hàm số khớp dữ liệu, hoặc cộng các hình thang. Hai kết quả rất gần nhau.',
         'Mở đầu: chỉ có một bảng số'),
    Beat('h2', 'hook',
         'Đây là tập ba mươi ba, khép lại phần ứng dụng thực tế: mô hình hóa từ dữ liệu thực.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, quy trình mô hình hóa: từ bảng số đến hàm số. '
         'Hai, quy tắc hình thang khi không có công thức. '
         'Ba, các bài trả lời ngắn nhiều bước kết hợp mô hình và tích phân.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Quy trình mô hình hóa năm bước. Một, đọc dữ liệu và vẽ các điểm. Hai, chọn dạng hàm phù hợp, '
         'ví dụ bậc nhất, bậc hai hay hàm mũ. Ba, tìm hệ số từ dữ liệu. Bốn, tính tích phân. '
         'Năm, kiểm tra lại với các điểm dữ liệu còn lại.',
         'Quy trình mô hình hóa'),
    Beat('c2', 'core',
         'Tìm hệ số: mỗi điểm dữ liệu cho một phương trình. Với hàm bậc hai đi qua gốc tọa độ, v bằng a t bình phương cộng b t, '
         'chỉ cần hai điểm là đủ hai phương trình. Các điểm còn lại dùng để kiểm tra mô hình có tốt hay không.'),
    Beat('c2b', 'core',
         'Chọn dạng hàm thế nào? Nhìn hiệu giữa hai lần đo liên tiếp: sáu, bốn, hai, không. '
         'Hiệu không đổi là dấu hiệu của hàm bậc nhất. Hiệu giảm đều, mỗi bước bớt hai, là dấu hiệu của hàm bậc hai. '
         'Còn nếu tỉ số giữa hai lần đo không đổi, ta nghĩ đến hàm mũ. Ở đây v của không bằng không, nên hệ số tự do bằng không.'),
    Beat('c3', 'core',
         'Khi không tìm được công thức, ta dùng quy tắc hình thang: nối các điểm dữ liệu bằng đoạn thẳng, '
         'và cộng diện tích các hình thang. Với các bước đo cách đều h, tích phân xấp xỉ h nhân, '
         'một nửa giá trị đầu cộng các giá trị giữa cộng một nửa giá trị cuối.',
         'Quy tắc hình thang'),
    Beat('c4', 'core',
         'Quy tắc hình thang cho kết quả chính xác khi hàm là bậc nhất. Với đồ thị cong xuống, các đoạn thẳng nằm dưới đường cong, '
         'nên hình thang hơi thiếu; với đồ thị cong lên thì ngược lại. Đo dày hơn thì sai số nhỏ hơn.'),
    Beat('c5', 'core',
         'Hai cách bổ sung cho nhau: mô hình hàm số cho công thức để dự đoán, quy tắc hình thang không cần giả thiết gì về dạng hàm. '
         'Trong đề thi mới, câu trả lời ngắn thường hỏi một trong hai cách, và yêu cầu làm tròn cẩn thận.',
         'Mô hình và hình thang'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, giải bài mở đầu bằng mô hình. Chọn v bằng a t bình phương cộng b t. Từ v của hai bằng sáu và v của bốn bằng mười, '
         'giải được a bằng trừ một phần tư, b bằng bảy phần hai. Kiểm tra: v của sáu bằng mười hai, v của tám bằng mười hai, '
         'khớp hoàn toàn.',
         'Ví dụ 1: tìm hàm khớp dữ liệu'),
    Beat('e2', 'examples',
         'Quãng đường bằng tích phân từ không đến tám của trừ một phần tư t bình phương cộng bảy phần hai t, '
         'bằng hai trăm lẻ tám phần ba, khoảng sáu mươi chín phẩy ba ba mét.'),
    Beat('e2b', 'examples',
         'Mô hình còn cho phép dự đoán. Thay t bằng mười, được v bằng mười; thay t bằng mười bốn, được v bằng không: '
         'mô hình nói xe dừng hẳn sau mười bốn giây. Nhưng dữ liệu chỉ đo đến giây thứ tám, '
         'nên dự đoán ngoài vùng dữ liệu, gọi là ngoại suy, luôn cần kiểm chứng thêm.'),
    Beat('e3', 'examples',
         'Ví dụ hai, cùng dữ liệu nhưng dùng quy tắc hình thang với bước h bằng hai: '
         'hai nhân, không cộng sáu cộng mười cộng mười hai cộng sáu, bằng sáu mươi tám mét. '
         'Hơi thiếu so với mô hình, đúng như dự đoán vì đồ thị cong xuống.',
         'Ví dụ 2: quy tắc hình thang'),
    Beat('e4', 'examples',
         'Ví dụ ba: cường độ mưa đo mỗi giờ là không, bốn, mười, sáu, hai mi li mét mỗi giờ. '
         'Tổng lượng mưa trong bốn giờ, theo quy tắc hình thang, bằng không cộng bốn cộng mười cộng sáu cộng một, '
         'bằng hai mươi mốt mi li mét.',
         'Ví dụ 3: lượng mưa'),
    Beat('e5', 'examples',
         'Ví dụ bốn, nhiều bước: mặt cắt một con mương được đo độ sâu tại năm điểm cách nhau một mét: '
         'không, một phẩy hai, một phẩy sáu, một phẩy hai, không. Dữ liệu khớp parabol y bằng một phẩy sáu trừ không phẩy bốn x bình phương.',
         'Ví dụ 4: mặt cắt con mương'),
    Beat('e6', 'examples',
         'Diện tích mặt cắt bằng tích phân từ trừ hai đến hai, bằng sáu mươi tư phần mười lăm, khoảng bốn phẩy hai bảy mét vuông. '
         'Nước chảy với vận tốc không phẩy năm mét trên giây, nên lưu lượng khoảng hai phẩy một ba mét khối mỗi giây. '
         'Quy tắc hình thang cho bốn mét vuông, nhỏ hơn một chút.'),
    Beat('e7', 'examples',
         'Ví dụ năm, tìm số liệu bị thiếu: cường độ mưa đo mỗi giờ là không, bốn, a, sáu, hai mi li mét mỗi giờ, '
         'và tổng lượng mưa theo quy tắc hình thang là mười chín mi li mét. '
         'Tổng bằng không cộng bốn cộng a cộng sáu cộng một, tức mười một cộng a. '
         'Cho bằng mười chín, ta được a bằng tám mi li mét mỗi giờ.',
         'Ví dụ 5: tìm số liệu bị thiếu'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Vận tốc một vật được đo mỗi giây: một, ba, năm, bảy, chín mét trên giây tại t từ không đến bốn. '
         'Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: dữ liệu khớp chính xác v bằng hai t cộng một. '
         'Ý b đúng: tích phân từ không đến bốn của hai t cộng một bằng mười sáu cộng bốn, bằng hai mươi mét.'),
    Beat('x3', 'exam',
         'Ý c đúng: với hàm bậc nhất, quy tắc hình thang cho kết quả chính xác: một nửa cộng ba cộng năm cộng bảy cộng bốn phẩy năm, '
         'bằng hai mươi. Ý d sai: hình chữ nhật trái chỉ cho một cộng ba cộng năm cộng bảy, bằng mười sáu.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: lưu lượng nước vào bể được đo mỗi năm phút: mười, mười bốn, hai mươi, mười tám, mười hai lít mỗi phút. '
         'Dùng quy tắc hình thang, ước lượng lượng nước vào bể trong hai mươi phút.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Bước h bằng năm. Tổng bằng năm nhân, năm cộng mười bốn cộng hai mươi cộng mười tám cộng sáu, bằng năm nhân sáu mươi ba, '
         'bằng ba trăm mười lăm lít. Ghi vào phiếu: ba, một, năm.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, mô hình hóa: chọn dạng hàm, tìm hệ số từ dữ liệu, kiểm tra với điểm còn lại, rồi lấy tích phân. '
         'Hai, quy tắc hình thang: h nhân, một nửa đầu cộng các giá trị giữa cộng một nửa cuối. '
         'Ba, hình thang chính xác với hàm bậc nhất, sai số nhỏ khi đo dày.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, quy tắc hình thang với bước một và dữ liệu hai, bốn, tám, bốn. '
         'Hai, vận tốc dạng a t bình phương với v của hai bằng tám, tính quãng đường trong ba giây. '
         'Ba, mương sâu không, một, một phẩy năm, một, không, cách nhau một mét: diện tích theo hình thang. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Phần D khép lại tại đây. Từ tập ba mươi tư là phần tổng ôn, bắt đầu với những bẫy sai kinh điển '
         'và cách kiểm tra đáp án bằng máy tính. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'steps': "\"dữ liệu\" arrow.r f(x) arrow.r \"hệ số\" arrow.r integral arrow.r \"kiểm tra\"",
    'fit_sys': "v = a t^2 + b t: quad cases(4a + 2b = 6, 16a + 4b = 10)",
    'diffs': "Delta v: quad 6, quad 4, quad 2, quad 0",
    'form_lin': "Delta v \"không đổi\" arrow.r.double v = a t + b",
    'form_quad': "Delta v \"giảm đều\" arrow.r.double v = a t^2 + b t + c",
    'form_exp': "v_(k+1)/v_k \"không đổi\" arrow.r.double v = A e^(k t)",
    'trap': "integral_a^b f approx h (y_0/2 + y_1 + dots + y_(n-1) + y_n/2)",
    'e1_s1': "a = -1/4, quad b = 7/2: quad v(6) = 12, quad v(8) = 12 quad green(checkmark)",
    'e2_s1': "s = integral_0^8 (-1/4 t^2 + 7/2 t) dif t = 208/3 approx gold(\"69,33\") \"m\"",
    'e3_s1': "s approx 2 (0/2 + 6 + 10 + 12 + 12/2) = gold(68) \"m\"",
    'e2b_s1': "v(10) = 10, quad v(14) = 0",
    'e7_s1': "1 dot (0/2 + 4 + a + 6 + 2/2) = 11 + a = 19",
    'e7_s2': "a = gold(8) thin \"mm/h\"",
    'e4_s1': "1 dot (0/2 + 4 + 10 + 6 + 2/2) = gold(21) \"mm\"",
    'e5_s1': "y = \"1,6\" - \"0,4\" x^2: quad y(plus.minus 1) = \"1,2\", quad y(plus.minus 2) = 0",
    'e6_s1': "S = integral_(-2)^2 (\"1,6\" - \"0,4\" x^2) dif x = 64/15 approx gold(\"4,27\") \"m\"^2",
    'e6_s2': "Q = S dot \"0,5\" approx gold(\"2,13\") \"m\"^3\\/\"s\"",
    'e6_s3': "\"hình thang:\" quad 1 dot (0 + \"1,2\" + \"1,6\" + \"1,2\" + 0) = 4",
    'tf_given': "t: 0, 1, 2, 3, 4; quad v: 1, 3, 5, 7, 9",
    'tf_a': "v(t) = 2t + 1",
    'tf_b': "integral_0^4 v(t) dif t = 20",
    'tf_c': "\"hình thang:\" quad 1/2 + 3 + 5 + 7 + 9/2 = 20",
    'tf_d': "\"chữ nhật trái:\" quad 1 + 3 + 5 + 7 = 20",
    'sa_task': "r thin (\"L/phút\"): quad 10, 14, 20, 18, 12 quad (h = 5)",
    'sa_s1': "5 (10/2 + 14 + 20 + 18 + 12/2) = 5 dot 63 = gold(315) \"L\"",
    'sum1': "\"dữ liệu\" arrow.r f arrow.r integral f",
    'sum2': "h (y_0/2 + y_1 + dots + y_n/2)",
    'sum3': "f \"bậc nhất\" arrow.double.long \"chính xác\"",
    'hw1': "h = 1: quad 2, 4, 8, 4",
    'hw2': "v = a t^2, quad v(2) = 8, quad s(3) = ?",
    'hw3': "0, 1, \"1,5\", 1, 0 quad (h = 1)",
    'hw_ans1': "15",
    'hw_ans2': "18 \"m\"",
    'hw_ans3': "\"3,5\" \"m\"^2",
    'next1': "pi integral (f - g)^2 coral(!=) pi integral (f^2 - g^2)",
}

EXERCISES = (
    ('Hình thang, h = 1, dữ liệu 2, 4, 8, 4', '15'),
    ('v = at², v(2) = 8: quãng đường trong 3 giây', '18 m'),
    ('Mương sâu 0; 1; 1,5; 1; 0 (cách 1 m): diện tích', '3,5 m²'),
)

TRUE_FALSE = (
    ('v(t) = 2t + 1 khớp dữ liệu', True),
    ('Quãng đường 4 giây = 20 m', True),
    ('Hình thang cho 20', True),
    ('Hình chữ nhật trái cho 20', False),
)

t, x = sp.symbols('t x', real=True)


def trap(values, h):
    return h * (sum(values) - sp.Rational(values[0] + values[-1], 2))


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R = sp.integrate, sp.Rational
    a, b = sp.symbols('a b')
    sol = sp.solve([4 * a + 2 * b - 6, 16 * a + 4 * b - 10], [a, b])
    assert sol == {a: -R(1, 4), b: R(7, 2)}
    v = -R(1, 4) * t**2 + R(7, 2) * t
    assert [v.subs(t, k) for k in T_DATA] == list(V_DATA)
    s = I(v, (t, 0, 8))
    assert s == R(208, 3) and f'{float(s):.2f}' == '69.33'
    assert trap(V_DATA, 2) == 68 and 68 < s   # concave → trapezoid underestimates
    d = [q - p for p, q in zip(V_DATA, V_DATA[1:])]
    assert d == [6, 4, 2, 0] and len({q - p for p, q in zip(d, d[1:])}) == 1
    assert v.subs(t, 10) == 10 and v.subs(t, 14) == 0
    m = sp.symbols('m')
    assert sp.solve(trap((0, 4, m, 6, 2), 1) - 19, m) == [8]
    # rain
    assert trap((0, 4, 10, 6, 2), 1) == 21
    # channel
    y = R(8, 5) - R(2, 5) * x**2
    assert [y.subs(x, k) for k in (-2, -1, 0, 1, 2)] == [0, R(6, 5), R(8, 5), R(6, 5), 0]
    S = I(y, (x, -2, 2))
    assert S == R(64, 15) and f'{float(S):.2f}' == '4.27' and f'{float(S * R(1, 2)):.2f}' == '2.13'
    assert trap((0, R(6, 5), R(8, 5), R(6, 5), 0), 1) == 4
    # true / false
    vt = 2 * t + 1
    claims = ([vt.subs(t, k) for k in range(5)] == [1, 3, 5, 7, 9], I(vt, (t, 0, 4)) == 20,
              trap((1, 3, 5, 7, 9), 1) == 20, 1 + 3 + 5 + 7 == 20)
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    assert trap((10, 14, 20, 18, 12), 5) == 315
    # exercises
    assert trap((2, 4, 8, 4), 1) == 15
    aa = sp.solve(a * 4 - 8, a)[0]
    assert aa == 2 and I(aa * t**2, (t, 0, 3)) == 18
    assert trap((0, 1, R(3, 2), 1, 0), 1) == R(7, 2)
    return True


validate()

"""INT36 – Bản đồ tư duy toàn chương · chiến lược 8+/9+ · lộ trình tự học.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT36',
    'number': 36,
    'title': 'Bản đồ tư duy toàn chương',
    'subtitle': 'Một ý tưởng, năm nhánh kiến thức, chiến lược chinh phục 8+ / 9+',
    'next_code': '',
    'next_title': 'Hoàn thành series',
}

PARTS = (
    ('hook', 'Mở đầu'),
    ('map', 'Bản đồ tư duy'),
    ('strategy', 'Chiến lược 8+ / 9+'),
    ('roadmap', 'Lộ trình tự học'),
    ('outro', 'Tổng kết'),
)


@dataclass(frozen=True)
class Beat:
    id: str
    part: str
    text: str
    chapter: str | None = None


# (code, name, colour key, first–last episode) of the five branches
BRANCHES = (
    ('A', 'Nguyên hàm', (1, 10)),
    ('B', 'Tích phân', (11, 20)),
    ('C', 'Diện tích, thể tích', (21, 28)),
    ('D', 'Thực tế, mô hình hóa', (29, 33)),
    ('E', 'Tổng ôn, luyện đề', (34, 36)),
)

BEATS = (
    # ---------------- MỞ ĐẦU ----------------
    Beat('h1', 'hook',
         'Ba mươi lăm tập, năm phần kiến thức, hàng trăm công thức và ví dụ. Làm sao nhớ hết? '
         'Bí quyết là không nhớ rời rạc, mà xếp tất cả lên một bản đồ, xoay quanh một ý tưởng duy nhất. '
         'Hôm nay ta vẽ bản đồ đó, từng nhánh một.',
         'Mở đầu: gom cả chương vào một bản đồ'),
    Beat('h2', 'hook',
         'Đây là tập ba mươi sáu, tập cuối của series: bản đồ tư duy toàn chương.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ có ba thứ. Một, bản đồ tư duy năm nhánh của cả chương. '
         'Hai, chiến lược riêng cho mục tiêu tám điểm và chín điểm, kèm hai câu thử thách. '
         'Ba, một lộ trình tự học bốn tuần dùng lại toàn bộ series.'),
    # ---------------- BẢN ĐỒ TƯ DUY ----------------
    Beat('m1', 'map',
         'Ở trung tâm là dấu tích phân. Nhánh A, nguyên hàm, từ tập một đến tập mười: '
         'đi ngược đạo hàm, bảng nguyên hàm cơ bản của lũy thừa, mũ, logarit, lượng giác, '
         'rồi hai kỹ thuật chủ lực: đổi biến số và từng phần.',
         'Nhánh A: nguyên hàm'),
    Beat('m2', 'map',
         'Nhánh B, tích phân, từ tập mười một đến hai mươi. Tích phân là giới hạn của tổng diện tích các hình chữ nhật, '
         'và được tính bằng F của b trừ F của a. Đi kèm là các tính chất chèn cận, trị tuyệt đối, '
         'đổi biến, từng phần và hàm ẩn đối xứng.',
         'Nhánh B: tích phân'),
    Beat('m3', 'map',
         'Nhánh C, ứng dụng hình học, từ tập hai mươi mốt đến hai mươi tám. Diện tích bằng tích phân trị tuyệt đối của hiệu hai hàm. '
         'Thể tích bằng tích phân diện tích thiết diện; khi quay quanh trục hoành, thiết diện là hình tròn, '
         'hoặc vành khăn với hiệu các bình phương.',
         'Nhánh C: diện tích, thể tích'),
    Beat('m4', 'map',
         'Nhánh D, ứng dụng thực tế, từ tập hai mươi chín đến ba mươi ba. Quãng đường là tích phân trị tuyệt đối vận tốc. '
         'Tổng lượng bằng giá trị đầu cộng tích phân của tốc độ thay đổi, dùng cho bồn nước, kinh tế, sinh học. '
         'Khi chỉ có bảng số, dùng quy tắc hình thang.',
         'Nhánh D: thực tế, mô hình hóa'),
    Beat('m5', 'map',
         'Nhánh E, tổng ôn, từ tập ba mươi tư đến ba mươi sáu: tám bẫy sai kinh điển, ba lớp kiểm tra bằng đạo hàm, '
         'máy tính và ước lượng, cùng một đề luyện theo cấu trúc mười hai, bốn, sáu.',
         'Nhánh E: tổng ôn'),
    Beat('m5b', 'map',
         'Các nhánh không tách rời nhau. Đổi biến và từng phần của nhánh A được dùng lại trong nhánh B. '
         'Trị tuyệt đối của nhánh B quay lại trong diện tích ở nhánh C và quãng đường ở nhánh D. '
         'Còn tám bẫy sai ở nhánh E sinh ra chính từ những mối nối này.',
         'Mối nối giữa các nhánh'),
    Beat('m6', 'map',
         'Nhìn lại toàn bộ bản đồ, mọi nhánh đều dùng chung một ý tưởng: cắt nhỏ, xấp xỉ, rồi cộng lại. '
         'Cắt nhỏ diện tích thành hình chữ nhật, cắt nhỏ thể tích thành lát mỏng, cắt nhỏ thời gian thành từng khoảng ngắn. '
         'Giới hạn của tổng đó chính là tích phân.',
         'Một ý tưởng xuyên suốt'),
    # ---------------- CHIẾN LƯỢC 8+ / 9+ ----------------
    Beat('s1', 'strategy',
         'Mục tiêu tám điểm: nắm chắc bốn việc. Bảng nguyên hàm cơ bản không sai dấu, sai hệ số. '
         'Tích phân bằng F b trừ F a và các tính chất. Diện tích, thể tích dạng chuẩn. '
         'Và bài chuyển động trong câu đúng sai. Phần lớn điểm của đề nằm ở đây.',
         'Chiến lược 8+'),
    Beat('s2', 'strategy',
         'Mục tiêu chín điểm: thêm bốn dạng vận dụng cao. Hàm ẩn và tính đối xứng, bài toán có tham số, '
         'mô hình hóa từ dữ liệu, và các câu trả lời ngắn nhiều bước. '
         'Ta thử ngay hai câu thử thách.',
         'Chiến lược 9+'),
    Beat('s2b', 'strategy',
         'Trong phòng thi, nhận dạng nhanh nhờ từ khóa. Gặp chữ diện tích: tích phân trị tuyệt đối của hiệu. '
         'Quay quanh trục hoành: pi nhân tích phân bình phương. Quãng đường: tích phân trị tuyệt đối vận tốc. '
         'Tổng lượng: giá trị đầu cộng tích phân tốc độ. Chỉ có bảng số: quy tắc hình thang.',
         'Từ khóa nhận dạng'),
    Beat('s3', 'strategy',
         'Thử thách một: tìm a dương để diện tích giữa parabol y bằng x bình phương và đường thẳng y bằng a x bằng ba mươi sáu. '
         'Khi a tăng, giao điểm thứ hai x bằng a dịch sang phải và diện tích tăng rất nhanh. Em hãy tạm dừng và thử.',
         'Thử thách 9+: tham số'),
    Beat('s4', 'strategy',
         'Diện tích bằng tích phân từ không đến a của a x trừ x bình phương, bằng a mũ ba phần sáu. '
         'Cho bằng ba mươi sáu, a mũ ba bằng hai trăm mười sáu, nên a bằng sáu. '
         'Thử lại bằng máy tính: tích phân từ không đến sáu của sáu x trừ x bình phương đúng bằng ba mươi sáu.'),
    Beat('s5', 'strategy',
         'Thử thách hai: hàm f liên tục thỏa f của x cộng hai f của một trừ x bằng ba x với mọi x. '
         'Tính tích phân từ không đến một của f. Không cần tìm f, chỉ cần một bước khéo léo.',
         'Thử thách 9+: hàm ẩn'),
    Beat('s6', 'strategy',
         'Lấy tích phân hai vế từ không đến một. Đổi biến u bằng một trừ x cho thấy tích phân của f của một trừ x cũng bằng I. '
         'Vậy I cộng hai I bằng ba phần hai, nên I bằng một phần hai. '
         'Kiểm tra: hàm thỏa mãn là f bằng hai trừ ba x, tích phân của nó đúng bằng một phần hai.'),
    Beat('s7', 'strategy',
         'Chiến lược trong phòng thi. Làm chắc phần một trước, không sa đà câu khó. '
         'Phần hai: mỗi ý một lời giải ngắn, vì đúng đủ bốn ý mới được trọn một điểm. '
         'Phần ba: luôn kiểm tra kết quả bằng máy tính trước khi ghi vào phiếu.',
         'Chiến lược trong phòng thi'),
    # ---------------- LỘ TRÌNH TỰ HỌC ----------------
    Beat('r1', 'roadmap',
         'Lộ trình bốn tuần dùng lại series. Tuần một: nhánh A, mười tập nguyên hàm. Tuần hai: nhánh B, tích phân. '
         'Tuần ba: nhánh C và D, các ứng dụng. Tuần bốn: nhánh E, sửa lỗi sai và luyện đề có bấm giờ.',
         'Lộ trình bốn tuần'),
    Beat('r2', 'roadmap',
         'Với mỗi tập, học theo bốn bước: xem phần bản chất, tạm dừng và tự giải ví dụ trước khi xem lời giải, '
         'làm ba bài tự luyện ở cuối video, rồi ghi mọi lỗi sai vào sổ. '
         'Lời giảng đầy đủ của từng tập có trong phần mô tả.'),
    Beat('r2b', 'roadmap',
         'Ngày trước kỳ thi, đừng học thêm dạng mới. Hãy vẽ lại bản đồ tư duy, đọc lại bảng nguyên hàm, '
         'lướt qua tám bẫy sai và sổ lỗi sai của chính mình, rồi ngủ đủ giấc để giữ đầu óc tỉnh táo.',
         'Ngày trước kỳ thi'),
    Beat('r3', 'roadmap',
         'Một mẹo cuối: mỗi tối, vẽ lại bản đồ tư duy này từ trí nhớ trong năm phút. '
         'Nhánh nào vẽ chưa trọn, đó là tập em cần xem lại ngày mai.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt cả chương trong ba ý. Một, nguyên hàm và đạo hàm là hai chiều của cùng một phép toán. '
         'Hai, tích phân là giới hạn của tổng: cắt nhỏ rồi cộng lại. '
         'Ba, mọi ứng dụng đều là chọn đúng đại lượng để cắt nhỏ.',
         'Tổng kết và bài tập thử thách'),
    Beat('o2', 'outro',
         'Ba bài thử thách cuối series. Một, tìm a dương để tích phân từ không đến a của hai x trừ một bằng sáu. '
         'Hai, f của x cộng f của trừ x bằng cos x, tính tích phân từ trừ pi phần hai đến pi phần hai của f. '
         'Ba, diện tích giữa y bằng x bình phương và y bằng hai x cộng ba. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ba mươi sáu tập đã khép lại. Cảm ơn các em đã đồng hành cùng series nguyên hàm, tích phân và ứng dụng chuyên sâu. '
         'Chúc các em tự tin chinh phục kỳ thi. Hẹn gặp lại ở series tiếp theo!'),
)

FORMULAS = {
    'core': "integral",
    'spine': "integral_a^b f(x) dif x = lim_(n arrow.r infinity) sum_(i = 1)^n f(x_i) Delta x",
    'idea': "\"cắt nhỏ\" arrow.r \"xấp xỉ\" arrow.r \"cộng lại\" arrow.r integral",
    # nhánh A
    'a1': "F'(x) = f(x)",
    'a2': "integral x^alpha dif x = x^(alpha + 1)/(alpha + 1) + C",
    'a3': "integral 1/x dif x = ln abs(x) + C, quad integral e^x dif x = e^x + C",
    'a4': "integral f(u) u' dif x = integral f(u) dif u, quad integral u dif v = u v - integral v dif u",
    # nhánh B
    'b1': "integral_a^b f(x) dif x = F(b) - F(a)",
    'b2': "integral_a^b f = integral_a^c f + integral_c^b f",
    'b3': "integral_a^b abs(f(x)) dif x = sum abs(integral f)",
    'b4': "integral_a^b f(x) dif x = integral_a^b f(a + b - x) dif x",
    # nhánh C
    'c1': "S = integral_a^b abs(f(x) - g(x)) dif x",
    'c2': "V = integral_a^b S(x) dif x",
    'c3': "V = pi integral_a^b f^2(x) dif x",
    'c4': "V = pi integral_a^b (f^2 - g^2) dif x",
    # nhánh D
    'd1': "s = integral_(t_1)^(t_2) abs(v(t)) dif t",
    'd2': "Q(T) = Q(0) + integral_0^T Q'(t) dif t",
    'd3': "integral_a^b f approx h (y_0/2 + y_1 + dots + y_n/2)",
    # nhánh E
    'e1': "F' = f, quad integral_a^b f approx \"máy tính\"",
    'e2': "abs(x), quad 1/a, quad -cos, quad \"đổi cận\", quad R^2 - r^2",
    'e3': "12 + 4 + 6",
    # thử thách
    'ch1': "S_(y = x^2, thin y = a x) = 36, quad a > 0",
    'ch1_s1': "integral_0^a (a x - x^2) dif x = a^3/6",
    'ch1_s2': "a^3/6 = 36 arrow.l.r.double a^3 = 216 arrow.l.r.double a = gold(6)",
    'ch2': "f(x) + 2 f(1 - x) = 3x quad forall x, quad integral_0^1 f(x) dif x = ?",
    'ch2_s1': "integral_0^1 f(1 - x) dif x = integral_0^1 f(u) dif u = I",
    'ch2_s2': "I + 2I = integral_0^1 3x dif x = 3/2 arrow.r.double I = gold(1/2)",
    'ch2_s3': "f(x) = 2 - 3x: quad integral_0^1 (2 - 3x) dif x = 1/2 quad green(checkmark)",
    # tổng kết
    'sum1': "F' = f arrow.l.r.double integral f = F + C",
    'sum2': "integral = lim sum",
    'sum3': "\"cắt nhỏ đúng đại lượng\"",
    'hw1': "integral_0^a (2x - 1) dif x = 6, quad a > 0",
    'hw2': "f(x) + f(-x) = cos x, quad integral_(-pi\\/2)^(pi\\/2) f(x) dif x",
    'hw3': "S_(y = x^2, thin y = 2x + 3)",
    'hw_ans1': "a = 3",
    'hw_ans2': "1",
    'hw_ans3': "32/3",
}

EXERCISES = (
    ('Tìm a > 0: ∫₀ᵃ (2x − 1) dx = 6', 'a = 3'),
    ('f(x) + f(−x) = cos x: ∫_{−π/2}^{π/2} f(x) dx', '1'),
    ('Diện tích giữa y = x² và y = 2x + 3', '32/3'),
)

TRUE_FALSE = ()

x, a, u = sp.symbols('x a u', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)
    assert [r for _, _, r in BRANCHES] == [(1, 10), (11, 20), (21, 28), (29, 33), (34, 36)]

    I, R = sp.integrate, sp.Rational
    # thử thách 1
    ap = sp.symbols('ap', positive=True)
    S = I(ap * x - x**2, (x, 0, ap))
    assert sp.simplify(S - ap**3 / 6) == 0 and sp.solve(sp.Eq(S, 36), ap) == [6]
    assert I(6 * x - x**2, (x, 0, 6)) == 36
    # thử thách 2: f(x) + 2 f(1 − x) = 3x  ⇒  f = 2 − 3x, ∫₀¹ f = 1/2
    f = 2 - 3 * x
    assert sp.expand(f + 2 * f.subs(x, 1 - x) - 3 * x) == 0
    assert I(f, (x, 0, 1)) == R(1, 2) and I(3 * x, (x, 0, 1)) / 3 == R(1, 2)
    # bài tập
    assert sp.solve(sp.Eq(I(2 * x - 1, (x, 0, ap)), 6), ap) == [3]
    g = sp.cos(x) / 2 + x**3  # one f with f(x) + f(−x) = cos x
    assert sp.simplify(g + g.subs(x, -x) - sp.cos(x)) == 0 and I(g, (x, -sp.pi / 2, sp.pi / 2)) == 1
    assert sorted(sp.solve(x**2 - 2 * x - 3, x)) == [-1, 3]
    assert I(2 * x + 3 - x**2, (x, -1, 3)) == R(32, 3)
    return True


validate()

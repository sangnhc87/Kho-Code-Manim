"""INT25 – Thể tích vật thể theo thiết diện S(x): cắt lát – cộng dồn.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT25',
    'number': 25,
    'title': 'Thể tích theo thiết diện',
    'subtitle': 'Cắt lát, xếp chồng, cộng dồn: V = ∫S(x)dx',
    'next_code': 'INT26',
    'next_title': 'Thể tích khối tròn xoay quanh Ox',
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
         'Một ổ bánh mì được cắt thành rất nhiều lát mỏng. Thể tích ổ bánh bằng tổng thể tích các lát, '
         'và mỗi lát gần như một tấm phẳng: diện tích mặt cắt nhân độ dày. '
         'Ý tưởng đơn giản này cho ta công thức tính thể tích của mọi vật thể, chỉ cần biết diện tích mặt cắt.',
         'Mở đầu: cắt bánh mì thành lát'),
    Beat('h2', 'hook',
         'Đây là tập hai mươi lăm của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: '
         'thể tích vật thể theo thiết diện.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, công thức V bằng tích phân của S của x, hiểu bằng cắt lát và cộng dồn. '
         'Hai, cách tìm diện tích thiết diện cho các hình quen thuộc. '
         'Ba, dùng công thức này để chứng minh thể tích hình chóp bằng một phần ba diện tích đáy nhân chiều cao.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Đặt vật thể dọc theo trục O x, từ x bằng a đến x bằng b. Cắt vật thể bởi mặt phẳng vuông góc với trục tại điểm x, '
         'ta được một thiết diện có diện tích S của x. Khi S liên tục, thể tích V bằng tích phân từ a đến b của S của x.',
         'Công thức V = ∫S(x)dx'),
    Beat('c2', 'core',
         'Vì sao? Chia vật thể thành n lát mỏng, mỗi lát có độ dày delta x. Thể tích mỗi lát xấp xỉ S của x nhân delta x. '
         'Cộng dồn n lát, ta được một tổng Riemann. Khi các lát mỏng dần, tổng tiến tới tích phân, '
         'giống hệt cách ta định nghĩa diện tích ở tập mười một.'),
    Beat('c2b', 'core',
         'Kiểm tra bằng đơn vị: S của x có đơn vị diện tích, mét vuông, nhân với d x có đơn vị độ dài, ta được mét khối. '
         'Vì vậy thứ nằm dưới dấu tích phân phải là một diện tích. Nếu em lấy tích phân của độ dài cạnh, '
         'kết quả chỉ là một diện tích, không phải thể tích. Đây là bẫy rất hay gặp.'),
    Beat('c3', 'core',
         'Quy trình ba bước. Một, chọn trục và xác định vật thể nằm từ a đến b. '
         'Hai, tại vị trí x, mô tả thiết diện và tính diện tích S của x. '
         'Ba, tính tích phân từ a đến b của S của x. Bước hai là bước quan trọng nhất.',
         'Quy trình ba bước'),
    Beat('c4', 'core',
         'Nhắc lại diện tích các thiết diện hay gặp. Hình vuông cạnh a có diện tích a bình phương. '
         'Tam giác đều cạnh a có diện tích a bình phương nhân căn ba chia bốn. '
         'Nửa hình tròn bán kính r có diện tích pi r bình phương chia hai. Hình chữ nhật thì nhân hai cạnh.',
         'Diện tích thiết diện hay gặp'),
    Beat('c5', 'core',
         'Nguyên lý Cavalieri: hai vật thể có thiết diện bằng nhau tại mọi vị trí x thì có thể tích bằng nhau. '
         'Một chồng đồng xu xếp thẳng và một chồng bị xô lệch có cùng thể tích. '
         'Đây chính là nội dung của công thức tích phân thể tích.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một: vật thể nằm giữa x bằng không và x bằng bốn, thiết diện tại x là hình vuông cạnh căn x. '
         'Diện tích S của x bằng căn x bình phương, bằng x. Thể tích bằng tích phân từ không đến bốn của x, bằng tám.',
         'Ví dụ 1: thiết diện hình vuông'),
    Beat('e2', 'examples',
         'Ví dụ hai: thiết diện tại x là tam giác đều cạnh x, với x từ không đến ba. '
         'Diện tích S của x bằng căn ba chia bốn nhân x bình phương. '
         'Thể tích bằng căn ba chia bốn nhân tích phân của x bình phương, bằng chín căn ba chia bốn.',
         'Ví dụ 2: thiết diện tam giác đều'),
    Beat('e2b', 'examples',
         'Dạng đề hay gặp: vật thể có đáy là miền phẳng. Đáy là miền giới hạn bởi y bằng căn x, trục hoành, x từ không đến bốn. '
         'Thiết diện vuông góc với O x là nửa hình tròn có đường kính là đoạn từ trục đến đồ thị, dài căn x. '
         'Bán kính căn x chia hai, diện tích pi x chia tám. Thể tích bằng pi chia tám nhân tám, bằng pi.',
         'Ví dụ: đáy là miền phẳng'),
    Beat('e3', 'examples',
         'Ví dụ ba, chứng minh công thức hình chóp. Chóp có đáy hình vuông cạnh a, chiều cao h. '
         'Đặt trục O x từ đỉnh xuống đáy. Thiết diện cách đỉnh x là hình vuông cạnh a x chia h, theo tam giác đồng dạng.',
         'Ví dụ 3: chứng minh thể tích hình chóp'),
    Beat('e4', 'examples',
         'Diện tích thiết diện bằng a bình phương x bình phương chia h bình phương. '
         'Tích phân từ không đến h cho a bình phương nhân h chia ba. Đó chính là một phần ba diện tích đáy nhân chiều cao, '
         'công thức em đã học từ lớp chín, giờ được chứng minh bằng tích phân.'),
    Beat('e5', 'examples',
         'Ví dụ bốn: thiết diện tại x là hình chữ nhật có hai cạnh x và căn của chín trừ x bình phương, với x từ không đến ba. '
         'Thể tích bằng tích phân của x nhân căn chín trừ x bình phương. Đổi biến u bằng chín trừ x bình phương, '
         'ta được thể tích bằng chín.',
         'Ví dụ 4: kết hợp đổi biến'),
    Beat('e6', 'examples',
         'Một trường hợp đặc biệt rất quan trọng: nếu thiết diện tại x là hình tròn bán kính f của x, '
         'thì S của x bằng pi nhân f bình phương, và thể tích bằng pi nhân tích phân của f bình phương. '
         'Đó chính là thể tích khối tròn xoay mà ta sẽ học kỹ ở tập sau.',
         'Hướng tới khối tròn xoay'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Một vật thể nằm giữa hai mặt phẳng x bằng một và x bằng ba. '
         'Thiết diện tại x là hình vuông cạnh hai x. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: diện tích hình vuông cạnh hai x là bốn x bình phương. '
         'Ý b sai: phải lấy tích phân của diện tích S, không phải của cạnh hai x.'),
    Beat('x3', 'exam',
         'Ý c đúng: tích phân từ một đến ba của bốn x bình phương bằng bốn phần ba nhân hai mươi sáu, '
         'bằng một trăm lẻ bốn phần ba. Ý d đúng: giá trị đó xấp xỉ ba mươi tư phẩy bảy.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: một vật thể nằm giữa x bằng không và x bằng pi, thiết diện tại x là tam giác đều '
         'cạnh hai căn sin x. Tính thể tích, làm tròn đến hàng phần trăm.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Diện tích tam giác đều cạnh hai căn sin x bằng căn ba chia bốn nhân bốn sin x, bằng căn ba sin x. '
         'Thể tích bằng căn ba nhân tích phân từ không đến pi của sin x, bằng hai căn ba, xấp xỉ ba phẩy bốn sáu. '
         'Ghi vào phiếu: ba, phẩy, bốn, sáu.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, thể tích bằng tích phân của diện tích thiết diện: cắt lát rồi cộng dồn. '
         'Hai, bước quan trọng nhất là viết đúng S của x. '
         'Ba, công thức này chứng minh được thể tích hình chóp, và là nền tảng cho khối tròn xoay ở tập sau.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, thiết diện là hình vuông cạnh x, với x từ không đến hai. '
         'Hai, thiết diện là tam giác đều cạnh x, với x từ không đến hai. '
         'Ba, thiết diện là nửa hình tròn bán kính x, với x từ không đến ba. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập hai mươi sáu, thiết diện trở thành hình tròn khi ta quay một miền phẳng quanh trục O x: '
         'đó là khối tròn xoay và phương pháp đĩa. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'vol': "V = integral_a^b S(x) dif x",
    'slice': "Delta V approx S(x) dot Delta x",
    'riemann': "V = lim_(n arrow.r infinity) sum_(i=1)^n S(x_i) Delta x = integral_a^b S(x) dif x",
    'sq': "S = a^2",
    'tri': "S = (a^2 sqrt(3))/4",
    'semi': "S = (pi r^2)/2",
    'rect': "S = a dot b",
    'e1_s1': "S(x) = (sqrt(x))^2 = x arrow.double.long V = integral_0^4 x dif x = gold(8)",
    'e2_s1': "S(x) = sqrt(3)/4 x^2 arrow.double.long V = sqrt(3)/4 integral_0^3 x^2 dif x = gold((9 sqrt(3))/4)",
    'e3_s1': "ell(x) = (a x)/h",
    'e4_s1': "S(x) = (a^2 x^2)/h^2 arrow.double.long V = integral_0^h (a^2 x^2)/h^2 dif x = (a^2 h)/3",
    'e4_s2': "V = 1/3 dot a^2 dot h = 1/3 S dot h",
    'e5_s1': "V = integral_0^3 x sqrt(9 - x^2) dif x = 1/2 integral_0^9 sqrt(u) dif u = gold(9)",
    'units': "[\"m\"^2] times [\"m\"] = [\"m\"^3]",
    'base_s': "r = sqrt(x)/2 arrow.double.long S(x) = (pi r^2)/2 = (pi x)/8",
    'base_v': "V = integral_0^4 (pi x)/8 dif x = gold(pi)",
    'disk': "S(x) = pi f^2(x) arrow.double.long V = pi integral_a^b f^2(x) dif x",
    'tf_given': "x in [1; 3], quad ell(x) = 2x",
    'tf_a': "S(x) = 4x^2",
    'tf_b': "V = integral_1^3 2x dif x",
    'tf_c': "V = 104/3",
    'tf_d': "V approx \"34,7\"",
    'tf_c_calc': "V = integral_1^3 4x^2 dif x = 4/3 (27 - 1) = 104/3 approx \"34,67\"",
    'sa_task': "x in [0; pi], quad ell(x) = 2 sqrt(sin x)",
    'sa_s1': "S(x) = sqrt(3)/4 dot 4 sin x = sqrt(3) sin x",
    'sa_s2': "V = sqrt(3) integral_0^pi sin x dif x = 2 sqrt(3) approx gold(\"3,46\")",
    'sum1': "V = integral_a^b S(x) dif x",
    'sum2': "S(x): quad a^2, quad (a^2 sqrt(3))/4, quad (pi r^2)/2",
    'sum3': "V = 1/3 S h",
    'hw1': "x in [0; 2], quad S = x^2",
    'hw2': "x in [0; 2], quad S = sqrt(3)/4 x^2",
    'hw3': "x in [0; 3], quad S = (pi x^2)/2",
    'hw_ans1': "8/3",
    'hw_ans2': "(2 sqrt(3))/3",
    'hw_ans3': "(9 pi)/2",
    'next1': "V = pi integral_a^b f^2(x) dif x",
}

EXERCISES = (
    ('Thiết diện hình vuông cạnh x, x ∈ [0; 2]', '8/3'),
    ('Thiết diện tam giác đều cạnh x, x ∈ [0; 2]', '2√3/3'),
    ('Thiết diện nửa hình tròn bán kính x, x ∈ [0; 3]', '9π/2'),
)

TRUE_FALSE = (
    ('S(x) = 4x²', True),
    ('V = ∫₁³ 2x dx', False),
    ('V = 104/3', True),
    ('V ≈ 34,7', True),
)

x, u, a, h = sp.symbols('x u a h', positive=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, pi, s3 = sp.integrate, sp.Rational, sp.pi, sp.sqrt(3)
    # e1
    assert sp.sqrt(x)**2 == x and I(x, (x, 0, 4)) == 8
    # e2
    assert sp.simplify(I(s3 / 4 * x**2, (x, 0, 3)) - 9 * s3 / 4) == 0
    # e3/e4: pyramid
    Vp = I(a**2 * x**2 / h**2, (x, 0, h))
    assert sp.simplify(Vp - a**2 * h / 3) == 0
    # e5
    assert I(x * sp.sqrt(9 - x**2), (x, 0, 3)) == 9 == R(1, 2) * I(sp.sqrt(u), (u, 0, 9))
    assert sp.simplify(pi * (sp.sqrt(x) / 2)**2 / 2 - pi * x / 8) == 0 and I(pi * x / 8, (x, 0, 4)) == pi
    # true / false
    S = (2 * x)**2
    V = I(S, (x, 1, 3))
    claims = (sp.expand(S - 4 * x**2) == 0, I(2 * x, (x, 1, 3)) == V, V == R(104, 3), f'{float(V):.1f}' == '34.7')
    assert f'{float(V):.2f}' == '34.67'
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    side = 2 * sp.sqrt(sp.sin(x))
    St = sp.simplify(s3 / 4 * side**2)
    assert sp.simplify(St - s3 * sp.sin(x)) == 0
    Vt = I(s3 * sp.sin(x), (x, 0, pi))
    assert sp.simplify(Vt - 2 * s3) == 0 and f'{float(Vt):.2f}' == '3.46'
    # exercises
    assert I(x**2, (x, 0, 2)) == R(8, 3)
    assert sp.simplify(I(s3 / 4 * x**2, (x, 0, 2)) - 2 * s3 / 3) == 0
    assert sp.simplify(I(pi * x**2 / 2, (x, 0, 3)) - 9 * pi / 2) == 0
    return True


validate()

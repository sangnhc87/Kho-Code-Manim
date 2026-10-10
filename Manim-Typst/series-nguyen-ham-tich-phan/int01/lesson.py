"""INT01 – Đi ngược đạo hàm: bản chất nguyên hàm.

Single source of truth for the episode: narration beats, Typst formulas and
the mathematical facts shown on screen. Importable without Manim/Typst/network;
``validate()`` checks every number in the video with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT01',
    'number': 1,
    'title': 'Đi ngược đạo hàm',
    'subtitle': 'Bản chất của nguyên hàm',
    'next_code': 'INT02',
    'next_title': 'Tính chất nguyên hàm & hàm lũy thừa',
}

# Five blocks of the series standard (KE_HOACH_SERIES_36_TAP.md, section 2).
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
    chapter: str | None = None  # starts a YouTube chapter when set


BEATS = (
    # ---------------- MỞ ĐẦU ----------------
    Beat('h1', 'hook',
         'Hãy tưởng tượng em đang ngồi trên một chiếc xe. Đồng hồ quãng đường bị hỏng, '
         'chỉ còn đồng hồ tốc độ hoạt động. Tại mỗi thời điểm, em biết xe chạy nhanh bao nhiêu, '
         'nhưng không biết xe đã đi tới đâu.',
         'Mở đầu: chiếc xe mất đồng hồ quãng đường'),
    Beat('h2', 'hook',
         'Câu hỏi đặt ra là: chỉ từ vận tốc, liệu ta có khôi phục được vị trí của xe hay không? '
         'Ở lớp mười một, ta đi từ vị trí sang vận tốc bằng phép lấy đạo hàm. '
         'Hôm nay, ta sẽ đi theo chiều ngược lại.'),
    Beat('h3', 'hook',
         'Phép toán đi ngược đạo hàm có tên là nguyên hàm. Chào mừng các em đến với tập một của series '
         'Nguyên hàm, tích phân và ứng dụng chuyên sâu: Đi ngược đạo hàm, bản chất của nguyên hàm.'),
    Beat('h4', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, nguyên hàm là gì. Hai, vì sao luôn có hằng số C. '
         'Ba, cách dùng một điều kiện để chọn đúng một nguyên hàm, và áp dụng vào bài toán chuyển động.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Bắt đầu bằng một bài toán thật đơn giản. Tìm một hàm số F sao cho đạo hàm của F bằng hai x, '
         'tại mọi giá trị của x.',
         'Bài toán đi ngược đạo hàm'),
    Beat('c2', 'core',
         'Đồ thị bên trái là đường thẳng y bằng hai x. Đây là đồ thị của đạo hàm, chưa phải hàm ta cần tìm. '
         'Nó cho biết: tại mỗi hoành độ x, đồ thị của F phải dốc bao nhiêu. '
         'Tại x bằng một, độ dốc phải bằng hai. Tại x bằng âm một, độ dốc phải bằng âm hai.'),
    Beat('c3', 'core',
         'Ta biến thông tin đó thành hình ảnh. Tại mỗi điểm của mặt phẳng, vẽ một đoạn thẳng nhỏ '
         'có hệ số góc bằng hai x. Bên trái trục tung, các đoạn dốc xuống. Bên phải, các đoạn dốc lên, '
         'càng xa trục tung càng dốc. Hình này gọi là trường hướng.',
         'Trường hướng và họ nguyên hàm'),
    Beat('c4', 'core',
         'Đồ thị của F phải đi theo đúng các hướng này, giống như một chiếc lá trôi theo dòng nước. '
         'Thả một điểm xuất phát tại gốc tọa độ. Đường cong mà nó vạch ra chính là parabol '
         'y bằng x bình phương.'),
    Beat('c5', 'core',
         'Kiểm tra lại bằng đạo hàm: x bình phương có đạo hàm là hai x, đúng như yêu cầu. '
         'Ta nói: F của x bằng x bình phương là một nguyên hàm của hàm số f của x bằng hai x.'),
    Beat('c6', 'core',
         'Nhưng hãy thử thả điểm xuất phát ở chỗ khác, chẳng hạn tại điểm không phẩy hai. '
         'Đường cong mới cũng đi đúng theo trường hướng: đó là parabol x bình phương cộng hai. '
         'Thả tại điểm không phẩy âm một, ta được x bình phương trừ một.'),
    Beat('c7', 'core',
         'Khi điểm xuất phát trượt lên xuống, ta thu được vô số đường cong, tất cả đều khớp với trường hướng. '
         'Mỗi đường ứng với một giá trị của hằng số C, và có phương trình y bằng x bình phương cộng C.'),
    Beat('c8', 'core',
         'Vì sao cộng thêm C không làm thay đổi đạo hàm? Về đại số, đạo hàm của hằng số bằng không. '
         'Về hình học, cộng C chỉ tịnh tiến đồ thị lên hoặc xuống, nên tại cùng một hoành độ, '
         'các tiếp tuyến luôn song song với nhau, dù điểm xét chạy tới đâu.'),
    Beat('c9', 'core',
         'Bây giờ ta phát biểu chính xác. Cho hàm số f xác định trên K, với K là một khoảng, một đoạn '
         'hoặc một nửa khoảng. Hàm số F được gọi là nguyên hàm của f trên K nếu F phẩy của x bằng f của x '
         'với mọi x thuộc K.',
         'Định nghĩa và định lý'),
    Beat('c10', 'core',
         'Từ hình ảnh vừa rồi, ta có định lý quan trọng. Nếu F là một nguyên hàm của f trên K, '
         'thì mọi nguyên hàm của f trên K đều có dạng F của x cộng C, với C là một hằng số. '
         'Ngược lại, với mỗi hằng số C, hàm F cộng C cũng là một nguyên hàm của f.'),
    Beat('c11', 'core',
         'Vì sao không thể có nguyên hàm nào khác? Lấy hai nguyên hàm, chẳng hạn x bình phương trừ một '
         'và x bình phương cộng hai. Cho điểm xét chạy dọc trục hoành: khoảng cách theo phương thẳng đứng '
         'giữa hai đồ thị luôn luôn bằng ba.'),
    Beat('c12', 'core',
         'Tổng quát, nếu G và F cùng là nguyên hàm của f, thì đạo hàm của G trừ F bằng f trừ f, bằng không '
         'trên K. Một hàm số có đạo hàm bằng không trên một khoảng thì là hàm hằng. '
         'Vậy G bằng F cộng một hằng số.'),
    Beat('c13', 'core',
         'Cả họ nguyên hàm được viết gọn bằng một kí hiệu. Ta viết: tích phân f của x d x bằng F của x cộng C, '
         'và đọc là họ nguyên hàm của f. Chẳng hạn, nguyên hàm của hai x d x bằng x bình phương cộng C.',
         'Kí hiệu họ nguyên hàm'),
    Beat('c14', 'core',
         'Một lưu ý chuyên sâu: kết luận chỉ khác nhau một hằng số chỉ đúng trên từng khoảng. '
         'Hàm số âm một chia x bình phương không xác định tại x bằng không. '
         'Hàm một chia x là một nguyên hàm của nó trên từng khoảng: từ âm vô cùng đến không, '
         'và từ không đến dương vô cùng.',
         'Bẫy: nguyên hàm trên từng khoảng'),
    Beat('c15', 'core',
         'Nếu dịch nhánh bên phải lên một đơn vị, và nhánh bên trái xuống hai đơn vị, hàm mới vẫn có '
         'đạo hàm bằng âm một chia x bình phương tại mọi x khác không. Hai nhánh mang hai hằng số khác nhau. '
         'Đây là cái bẫy hay gặp trong câu hỏi đúng sai.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một. Tìm nguyên hàm F của hàm số f của x bằng ba x bình phương, biết F của một bằng năm.',
         'Ví dụ 1: nguyên hàm thỏa điều kiện'),
    Beat('e2', 'examples',
         'Bước một, tìm họ nguyên hàm. Ta nhớ đạo hàm của x lập phương bằng ba x bình phương. '
         'Vậy họ nguyên hàm là x lập phương cộng C. Bên trái là một vài thành viên của họ này.'),
    Beat('e3', 'examples',
         'Bước hai, dùng điều kiện. Đồ thị phải đi qua điểm một phẩy năm. Thay x bằng một, '
         'ta được một cộng C bằng năm, suy ra C bằng bốn. Trên hình, đường cong được kéo lên '
         'cho tới khi đi qua đúng điểm này.'),
    Beat('e4', 'examples',
         'Vậy F của x bằng x lập phương cộng bốn. Kiểm tra lại: đạo hàm bằng ba x bình phương, '
         'và F của một bằng năm. Cả hai điều kiện đều thỏa mãn.'),
    Beat('e5', 'examples',
         'Ví dụ hai, quay lại chiếc xe ở đầu bài. Xe chuyển động thẳng với vận tốc v của t bằng hai t cộng một, '
         'đơn vị mét trên giây. Lúc bắt đầu, xe ở vị trí hai mét so với mốc. Hỏi sau ba giây, xe ở vị trí nào?',
         'Ví dụ 2: tìm vị trí từ vận tốc'),
    Beat('e6', 'examples',
         'Vị trí s là một nguyên hàm của vận tốc, vì s phẩy bằng v. Đạo hàm của t bình phương cộng t '
         'bằng hai t cộng một, nên s của t bằng t bình phương cộng t cộng C.'),
    Beat('e7', 'examples',
         'Điều kiện s của không bằng hai cho ta C bằng hai. Vậy s của t bằng t bình phương cộng t cộng hai. '
         'Hằng số C ở đây có ý nghĩa thực tế rất rõ: đó chính là vị trí ban đầu của xe.'),
    Beat('e8', 'examples',
         'Tại t bằng ba, s bằng chín cộng ba cộng hai, bằng mười bốn mét. Hãy quan sát chiếc xe chạy, '
         'đồng thời với điểm chạy trên đồ thị vị trí. Đúng ba giây sau, xe dừng ở vạch mười bốn mét.'),
    Beat('e9', 'examples',
         'Tính từ lúc bắt đầu, xe đã đi thêm mười bốn trừ hai, bằng mười hai mét. '
         'Hiệu s của ba trừ s của không này sẽ gặp lại ở các tập sau, với tên gọi tích phân.'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Bây giờ là một câu hỏi dạng đúng sai của đề thi tốt nghiệp. Cho hàm số f của x bằng sáu x bình phương '
         'trừ hai x. Gọi F là nguyên hàm của f trên R thỏa mãn F của không bằng một. '
         'Em hãy tạm dừng video và tự đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng, vì đó chính là định nghĩa nguyên hàm. Ý b sai: hàm này có đạo hàm đúng, nhưng tại không '
         'nó bằng không, chứ không bằng một. Đúng phải là F của x bằng hai x lập phương trừ x bình phương cộng một.'),
    Beat('x3', 'exam',
         'Ý c đúng: F của một bằng hai trừ một cộng một, bằng hai. Ý d đúng: G chỉ khác F một hằng số, '
         'nên G vẫn là một nguyên hàm của f, chỉ là không thỏa điều kiện F của không bằng một.'),
    Beat('x4', 'exam',
         'Thêm một câu trả lời ngắn. Biết F là một nguyên hàm của hai x, và F của hai bằng một. Tính F của ba. '
         'Ta có F bằng x bình phương cộng C. Thay x bằng hai: bốn cộng C bằng một, nên C bằng âm ba. '
         'Vậy F của ba bằng chín trừ ba, bằng sáu.',
         'Câu trả lời ngắn và mẹo kiểm tra'),
    Beat('x5', 'exam',
         'Mẹo thực chiến: muốn kiểm tra một nguyên hàm, hãy lấy đạo hàm ngược lại. Trên máy tính cầm tay, '
         'tính đạo hàm của F tại một điểm, rồi so sánh với giá trị của f tại điểm đó. '
         'Ví dụ, đạo hàm của x lập phương cộng bốn tại hai bằng mười hai, và f của hai cũng bằng mười hai.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt bài học bằng ba ý. Một, nguyên hàm là đi ngược đạo hàm: F là nguyên hàm của f khi F phẩy bằng f. '
         'Hai, trên một khoảng, các nguyên hàm chỉ khác nhau một hằng số C; về hình học, đó là các đồ thị '
         'tịnh tiến theo phương thẳng đứng. Ba, một điều kiện ban đầu xác định được hằng số C.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, tìm họ nguyên hàm của bốn x lập phương. Hai, tìm F biết F phẩy bằng hai x cộng ba, '
         'và F của không bằng một. Ba, một vật có vận tốc ba t bình phương mét trên giây, vị trí ban đầu bằng không. '
         'Tìm vị trí của vật sau hai giây. Đáp số hiện ở cuối màn hình, em hãy tự làm trước khi xem.'),
    Beat('o3', 'outro',
         'Ở tập hai, ta sẽ xây dựng các tính chất của nguyên hàm và nguyên hàm của hàm lũy thừa, '
         'cùng một cái bẫy rất hay gặp với tích và thương. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

# Typst math (display mode). Colour helpers gold/cyan/green/purple/coral/soft
# are defined in common/typst_build.py.
FORMULAS = {
    'task': "F'(x) = gold(2x)",
    'f_2x': "f(x) = 2x",
    'x2_deriv': "(x^2)' = 2x",
    'F_x2': "F(x) = cyan(x^2)",
    'family': "F(x) = x^2 + gold(C)",
    'c_deriv': "(x^2 + C)' = 2x + 0 = 2x",
    'def': "F'(x) = f(x), quad forall x in K",
    'thm': "F(x) + gold(C), quad C in RR",
    'F1': "purple(F_1 (x) = x^2 - 1)",
    'F2': "green(F_2 (x) = x^2 + 2)",
    'gap': "F_2 - F_1 = (x^2 + 2) - (x^2 - 1) = gold(3)",
    'proof1': "(G - F)' = f - f = 0",
    'proof2': "arrow.double.long quad G - F = C",
    'proof3': "arrow.double.long quad G = F + gold(C)",
    'notation': "integral f(x) dif x = F(x) + C",
    'notation_ex': "integral gold(2x) dif x = cyan(x^2) + C",
    'inv_x': "(1/x)' = -1/x^2, quad x != 0",
    'piece': "G(x) = cases(display(1/x) + green(1) & \"khi\" x > 0, display(1/x) - purple(2) & \"khi\" x < 0)",
    'ex1_task': "f(x) = 3x^2, quad F(1) = 5",
    'ex1_s1': "integral 3x^2 dif x = x^3 + C",
    'ex1_s2': "F(1) = 1 + C = 5 arrow.double.long C = gold(4)",
    'ex1_ans': "F(x) = x^3 + 4",
    'ex1_check': "F'(x) = 3x^2, quad F(1) = 1 + 4 = 5",
    'ex2_task': "v(t) = 2t + 1, quad s(0) = 2",
    'ex2_s1': "s(t) = integral (2t + 1) dif t = t^2 + t + C",
    'ex2_s2': "s(0) = C = 2",
    'ex2_s3': "s(t) = t^2 + t + gold(2)",
    'ex2_s4': "s(3) = 9 + 3 + 2 = gold(14)",
    'ex2_disp': "s(3) - s(0) = 14 - 2 = gold(12)",
    'tf_f': "f(x) = 6x^2 - 2x, quad F(0) = 1",
    'tf_a': "F'(x) = 6x^2 - 2x, thick forall x in RR",
    'tf_b': "F(x) = 2x^3 - x^2",
    'tf_c': "F(1) = 2",
    'tf_d': "G(x) = 2x^3 - x^2 - 5",
    'tf_sol': "F(x) = 2x^3 - x^2 + gold(1)",
    'tf_c_calc': "F(1) = 2 - 1 + 1 = 2",
    'tf_d_calc': "G(x) - F(x) = -6",
    'sa_task': "F'(x) = 2x, quad F(2) = 1, quad F(3) = ?",
    'sa_s1': "F(x) = x^2 + C, quad 4 + C = 1 arrow.double.long C = -3",
    'sa_s2': "F(3) = 9 - 3 = gold(6)",
    'casio1': "lr(d/(dif x) (x^3 + 4) |)_(x = 2) = gold(12)",
    'casio2': "f(2) = 3 dot 2^2 = gold(12)",
    'sum1': "F'(x) = f(x)",
    'sum2': "integral f(x) dif x = F(x) + C",
    'sum3': "F(x_0) = y_0 arrow.double.long C",
    'hw1': "integral 4x^3 dif x",
    'hw2': "F'(x) = 2x + 3, quad F(0) = 1",
    'hw3': "v(t) = 3t^2, quad s(0) = 0, quad s(2) = ?",
    'hw_ans1': "x^4 + C",
    'hw_ans2': "x^2 + 3x + 1",
    'hw_ans3': "s(2) = 8",
    'next1': "integral (f plus.minus g) dif x, quad integral k f(x) dif x, quad integral x^alpha dif x",
    'next2': "integral f g dif x coral(!=) integral f dif x dot integral g dif x",
}

# Exercises shown in the outro and in the YouTube description.
EXERCISES = (
    ('Tìm ∫4x³ dx.', 'x⁴ + C'),
    ("Tìm F biết F'(x) = 2x + 3 và F(0) = 1.", 'F(x) = x² + 3x + 1'),
    ('Vật có v(t) = 3t² (m/s), s(0) = 0. Tìm s(2).', 's(2) = 8 m'),
)

TRUE_FALSE = (
    ("F'(x) = 6x² − 2x với mọi x ∈ ℝ", True),
    ('F(x) = 2x³ − x²', False),
    ('F(1) = 2', True),
    ('G(x) = 2x³ − x² − 5 là một nguyên hàm của f', True),
)

x, t, C = sp.symbols('x t C', real=True)


def validate() -> bool:
    ids = [b.id for b in BEATS]
    assert len(ids) == len(set(ids)), 'duplicate beat id'
    part_ids = [p for p, _ in PARTS]
    assert all(b.part in part_ids for b in BEATS)
    # parts appear in order and each part is non-empty
    order = [part_ids.index(b.part) for b in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter, 'YouTube chapters must start at 00:00'
    assert sum(1 for b in BEATS if b.chapter) >= 3
    assert all(len(b.text.split()) >= 12 for b in BEATS)

    d = sp.diff
    # core: x^2 and the whole family x^2 + C
    assert sp.simplify(d(x**2, x) - 2*x) == 0
    assert sp.simplify(d(x**2 + C, x) - 2*x) == 0
    # parallel tangents: slope at x0 independent of C
    for c in (-1, 0, 2):
        for x0 in (-1, 1):
            assert d(x**2 + c, x).subs(x, x0) == 2*x0
    # constant gap between two primitives
    assert sp.simplify((x**2 + 2) - (x**2 - 1)) == 3
    # 1/x branches with different constants still have derivative -1/x^2
    assert sp.simplify(d(1/x, x) + 1/x**2) == 0
    assert sp.simplify(d(1/x + 1, x) + 1/x**2) == 0 and sp.simplify(d(1/x - 2, x) + 1/x**2) == 0
    # example 1
    F1 = sp.integrate(3*x**2, x) + C
    c1 = sp.solve(sp.Eq(F1.subs(x, 1), 5), C)[0]
    assert c1 == 4 and sp.simplify(F1.subs(C, c1) - (x**3 + 4)) == 0
    # example 2
    v = 2*t + 1
    s = sp.integrate(v, t) + C
    c2 = sp.solve(sp.Eq(s.subs(t, 0), 2), C)[0]
    s = s.subs(C, c2)
    assert c2 == 2 and sp.simplify(s - (t**2 + t + 2)) == 0
    assert s.subs(t, 3) == 14 and s.subs(t, 3) - s.subs(t, 0) == 12
    # true/false question
    f = 6*x**2 - 2*x
    F = sp.integrate(f, x) + C
    F = F.subs(C, sp.solve(sp.Eq(F.subs(x, 0), 1), C)[0])
    assert sp.simplify(F - (2*x**3 - x**2 + 1)) == 0
    statements = (
        sp.simplify(d(F, x) - f) == 0,
        sp.simplify(F - (2*x**3 - x**2)) == 0,
        F.subs(x, 1) == 2,
        sp.simplify(d(2*x**3 - x**2 - 5, x) - f) == 0,
    )
    assert statements == tuple(ans for _, ans in TRUE_FALSE)
    assert sp.simplify((2*x**3 - x**2 - 5) - F) == -6
    # short answer
    Fs = x**2 + C
    cs = sp.solve(sp.Eq(Fs.subs(x, 2), 1), C)[0]
    assert cs == -3 and Fs.subs(C, cs).subs(x, 3) == 6
    # casio tip
    assert d(x**3 + 4, x).subs(x, 2) == 12 == (3*x**2).subs(x, 2)
    # exercises
    assert sp.simplify(sp.integrate(4*x**3, x) - x**4) == 0
    hw2 = x**2 + 3*x + C
    hw2 = hw2.subs(C, sp.solve(sp.Eq(hw2.subs(x, 0), 1), C)[0])
    assert sp.simplify(d(hw2, x) - (2*x + 3)) == 0 and hw2.subs(x, 0) == 1
    hw3 = sp.integrate(3*t**2, t)
    assert hw3.subs(t, 0) == 0 and hw3.subs(t, 2) == 8
    return True


validate()

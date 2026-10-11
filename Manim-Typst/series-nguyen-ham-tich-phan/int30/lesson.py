"""INT30 – Thiết kế: cổng parabol, logo, mảnh vườn – chi phí theo diện tích.

Single source of truth for the episode (narration, Typst formulas, facts).
``validate()`` checks every result shown on screen with SymPy.
"""
from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

EPISODE = {
    'code': 'INT30',
    'number': 30,
    'title': 'Tích phân trong thiết kế',
    'subtitle': 'Cổng parabol, logo, mảnh vườn và chi phí',
    'next_code': 'INT31',
    'next_title': 'Bồn chứa, bể nước và lưu lượng',
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
         'Một cổng chào có dạng parabol, chân cổng rộng tám mét, đỉnh cao sáu mét. Người ta sơn toàn bộ mặt cổng '
         'với giá một trăm năm mươi nghìn đồng một mét vuông. Chi phí là bao nhiêu? '
         'Đáp số: bốn triệu tám trăm nghìn đồng, và chỉ cần một tích phân.',
         'Mở đầu: sơn một cổng parabol'),
    Beat('h2', 'hook',
         'Đây là tập ba mươi của series Nguyên hàm, tích phân và ứng dụng chuyên sâu: tích phân trong thiết kế.'),
    Beat('h3', 'hook',
         'Sau video này, em sẽ nắm được ba điều. Một, cách đặt hệ trục lên một vật thật để có hàm số đơn giản. '
         'Hai, công thức nhanh hai phần ba cho diện tích parabol. '
         'Ba, quy trình mô hình hóa trọn vẹn: từ hình vẽ đến chi phí.'),
    # ---------------- PHẦN 1: BẢN CHẤT ----------------
    Beat('c1', 'core',
         'Bước quan trọng nhất là đặt hệ trục. Với cổng parabol, hãy đặt gốc tọa độ ở chính giữa chân cổng, '
         'trục tung đi qua đỉnh. Khi đó parabol đối xứng qua trục tung và có dạng y bằng h trừ a x bình phương.',
         'Đặt hệ trục lên vật thật'),
    Beat('c2', 'core',
         'Tìm hệ số a từ dữ kiện: chân cổng tại x bằng cộng trừ một nửa chiều rộng, ở đó y bằng không. '
         'Với cổng rộng tám, cao sáu: sáu trừ mười sáu a bằng không, nên a bằng ba phần tám. '
         'Phương trình là y bằng sáu trừ ba phần tám x bình phương.'),
    Beat('c3', 'core',
         'Diện tích bằng tích phân từ trừ bốn đến bốn của sáu trừ ba phần tám x bình phương, bằng ba mươi hai. '
         'Để ý: ba mươi hai bằng hai phần ba nhân tám nhân sáu. Đây là kết quả của Archimedes: '
         'miền parabol bằng hai phần ba hình chữ nhật bao quanh nó.',
         'Công thức hai phần ba'),
    Beat('c3b', 'core',
         'Chứng minh tổng quát: cổng rộng w, cao h có phương trình y bằng h trừ bốn h chia w bình phương nhân x bình phương. '
         'Lấy tích phân từ trừ w phần hai đến w phần hai, ta được đúng hai phần ba w h. '
         'Vì vậy quy tắc hai phần ba đúng với mọi cổng parabol, không chỉ cho số liệu cụ thể.'),
    Beat('c4', 'core',
         'Quy trình mô hình hóa năm bước. Một, đặt hệ trục. Hai, viết phương trình các đường biên. Ba, tìm cận. '
         'Bốn, tính tích phân để có diện tích. Năm, nhân với đơn giá và đổi đơn vị theo yêu cầu.',
         'Quy trình năm bước'),
    Beat('c5', 'core',
         'Ba lỗi thường gặp khi làm bài thiết kế. Một, quên rằng chiều rộng là cả hai phía, cận là trừ bốn đến bốn chứ không phải '
         'không đến tám khi gốc ở giữa. Hai, nhầm đơn vị đề xi mét và mét. Ba, làm tròn quá sớm làm sai đáp số cuối.'),
    # ---------------- PHẦN 2: VÍ DỤ ----------------
    Beat('e1', 'examples',
         'Ví dụ một, hoàn thành bài mở đầu. Diện tích mặt cổng ba mươi hai mét vuông, nhân với một trăm năm mươi nghìn đồng, '
         'được bốn triệu tám trăm nghìn đồng.',
         'Ví dụ 1: chi phí sơn cổng'),
    Beat('e2', 'examples',
         'Ví dụ hai: cổng có một cửa hình chữ nhật rộng bốn mét, cao bốn mét ở giữa, phần cửa không sơn. '
         'Diện tích cần sơn là ba mươi hai trừ mười sáu, bằng mười sáu mét vuông. '
         'Phải kiểm tra cửa nằm gọn trong cổng: tại x bằng hai, cổng cao bốn phẩy năm, lớn hơn bốn.',
         'Ví dụ 2: trừ phần cửa'),
    Beat('e3', 'examples',
         'Ví dụ ba, mảnh vườn hình elip với trục lớn tám mét, trục nhỏ sáu mét. Phương trình x bình phương chia mười sáu '
         'cộng y bình phương chia chín bằng một. Diện tích bằng bốn lần tích phân của nửa trên trong góc phần tư thứ nhất, '
         'bằng pi nhân bốn nhân ba, bằng mười hai pi, khoảng ba mươi bảy phẩy bảy mét vuông.',
         'Ví dụ 3: vườn hình elip'),
    Beat('e3b', 'examples',
         'Tiếp ví dụ ba: mảnh đất hình chữ nhật tám nhân sáu mét bao quanh vườn elip, phần còn lại trồng cỏ. '
         'Diện tích trồng cỏ bằng bốn mươi tám trừ mười hai pi, khoảng mười phẩy ba mét vuông. '
         'Đây là kiểu câu hỏi hình ghép rất hay gặp trong đề.'),
    Beat('e4', 'examples',
         'Ví dụ bốn, logo: miền giữa hai parabol y bằng x bình phương và y bằng hai trừ x bình phương, đơn vị đề xi mét. '
         'Hai đường cắt nhau tại trừ một và một. Diện tích bằng tích phân của hai trừ hai x bình phương, bằng tám phần ba '
         'đề xi mét vuông, tức là tám phần ba nhân một phần trăm mét vuông.',
         'Ví dụ 4: logo hai parabol'),
    Beat('e5', 'examples',
         'Mẹo kiểm tra nhanh mọi bài cổng parabol: diện tích bằng hai phần ba nhân rộng nhân cao. '
         'Với elip, diện tích là pi a b. Biết hai công thức này, em có thể kiểm tra đáp án trắc nghiệm trong vài giây.'),
    Beat('e6', 'examples',
         'Nếu đặt gốc tọa độ ở chân trái của cổng thì sao? Khi đó parabol có dạng y bằng ba phần tám nhân x nhân tám trừ x, '
         'và cận từ không đến tám. Tích phân vẫn ra ba mươi hai. Kết quả không phụ thuộc cách đặt hệ trục, '
         'nhưng đặt gốc ở giữa thì phương trình gọn và tính nhanh hơn.',
         'Đặt hệ trục khác'),
    # ---------------- PHẦN 3: ĐỀ THI MỚI ----------------
    Beat('x1', 'exam',
         'Câu hỏi dạng đúng sai. Một cổng parabol rộng sáu mét, cao bốn phẩy năm mét. Đặt gốc tọa độ ở giữa chân cổng. '
         'Sơn mặt cổng với giá hai trăm nghìn đồng một mét vuông. Em hãy tạm dừng video và đánh giá bốn mệnh đề.',
         'Câu hỏi Đúng/Sai'),
    Beat('x2', 'exam',
         'Ý a đúng: bốn phẩy năm trừ a nhân chín bằng không cho a bằng một phần hai. '
         'Ý b đúng: diện tích bằng hai phần ba nhân sáu nhân bốn phẩy năm, bằng mười tám mét vuông.'),
    Beat('x3', 'exam',
         'Ý c sai: hai mươi bảy là diện tích cả hình chữ nhật bao quanh, không phải của cổng. '
         'Ý d sai: chi phí bằng mười tám nhân hai trăm nghìn, bằng ba triệu sáu trăm nghìn đồng.'),
    Beat('x4', 'exam',
         'Câu trả lời ngắn: một vườn hoa hình elip có trục lớn mười mét, trục nhỏ sáu mét. Chi phí trồng hoa là năm mươi nghìn đồng '
         'một mét vuông. Tính tổng chi phí theo đơn vị triệu đồng, làm tròn đến hàng phần trăm.',
         'Câu trả lời ngắn'),
    Beat('x5', 'exam',
         'Bán trục a bằng năm, b bằng ba. Diện tích bằng pi nhân năm nhân ba, bằng mười lăm pi, khoảng bốn mươi bảy phẩy mười hai mét vuông. '
         'Chi phí bằng mười lăm pi nhân không phẩy không năm triệu, khoảng hai phẩy ba sáu triệu đồng. '
         'Ghi vào phiếu: hai, phẩy, ba, sáu.'),
    # ---------------- TỔNG KẾT ----------------
    Beat('o1', 'outro',
         'Tóm tắt ba ý. Một, đặt hệ trục khéo léo: gốc ở giữa, trục tung đi qua đỉnh. '
         'Hai, cổng parabol có diện tích hai phần ba rộng nhân cao, elip có diện tích pi a b. '
         'Ba, mô hình hóa năm bước, nhân đơn giá ở cuối và cẩn thận với đơn vị.',
         'Tổng kết và bài tập tự luyện'),
    Beat('o2', 'outro',
         'Bài tập tự luyện. Một, diện tích cổng parabol rộng bốn mét, cao ba mét. '
         'Hai, logo giữa y bằng x bình phương và y bằng tám trừ x bình phương. '
         'Ba, diện tích elip có a bằng bốn, b bằng hai. Đáp số hiện ở cuối màn hình.'),
    Beat('o3', 'outro',
         'Ở tập ba mươi mốt, ta chuyển sang bồn chứa và bể nước: lưu lượng thay đổi theo thời gian, '
         'và tích phân cho biết lượng nước đã chảy vào. Cảm ơn các em đã theo dõi. Hẹn gặp lại!'),
)

FORMULAS = {
    'hook': "S dot 150 space 000 = gold(4 space 800 space 000) \"đ\"",
    'shape': "y = h - a x^2",
    'coef': "6 - a dot 4^2 = 0 arrow.double.long a = 3/8 arrow.double.long y = 6 - 3/8 x^2",
    'area': "S = integral_(-4)^4 (6 - 3/8 x^2) dif x = 32",
    'arch': "S = 2/3 dot 8 dot 6 = 32",
    'cost': "S dot 150 space 000 = 32 dot 150 space 000 = gold(4 space 800 space 000) \"đ\"",
    'door': "32 - 4 dot 4 = gold(16) \"m\"^2",
    'door_chk': "y(2) = 6 - 3/8 dot 4 = \"4,5\" > 4",
    'ell_eq': "x^2/16 + y^2/9 = 1",
    'ell_s': "S = 4 integral_0^4 3 sqrt(1 - x^2/16) dif x = 12 pi approx gold(\"37,7\") \"m\"^2",
    'logo': "S = integral_(-1)^1 (2 - 2x^2) dif x = gold(8/3) \"dm\"^2",
    'quick1': "S_\"parabol\" = 2/3 dot w dot h",
    'quick2': "S_\"elip\" = pi a b",
    'gen': "integral_(-w\\/2)^(w\\/2) (h - (4h)/w^2 x^2) dif x = 2/3 w h",
    'lawn': "S = 8 dot 6 - 12 pi approx gold(\"10,3\") \"m\"^2",
    'left': "y = 3/8 x (8 - x), quad integral_0^8 3/8 x (8 - x) dif x = 32",
    'tf_a': "y = \"4,5\" - 1/2 x^2",
    'tf_b': "S = 18 \"m\"^2",
    'tf_c': "S = 27 \"m\"^2",
    'tf_d': "\"Chi phí\" = 3 space 400 space 000 \"đ\"",
    'tf_calc': "S = 2/3 dot 6 dot \"4,5\" = 18, quad 18 dot 200 space 000 = 3 space 600 space 000",
    'sa_s1': "S = pi dot 5 dot 3 = 15 pi approx \"47,12\" \"m\"^2",
    'sa_s2': "15 pi dot \"0,05\" approx gold(\"2,36\") \"triệu đồng\"",
    'sum1': "y = h - a x^2",
    'sum2': "2/3 w h, quad pi a b",
    'sum3': "S times \"đơn giá\"",
    'hw1': "w = 4, quad h = 3",
    'hw2': "y = x^2, quad y = 8 - x^2",
    'hw3': "a = 4, quad b = 2",
    'hw_ans1': "8 \"m\"^2",
    'hw_ans2': "64/3",
    'hw_ans3': "8 pi",
    'next1': "V(T) = integral_0^T r(t) dif t",
}

EXERCISES = (
    ('Cổng parabol rộng 4 m, cao 3 m: diện tích', '8 m²'),
    ('Logo giữa y = x² và y = 8 − x²', '64/3'),
    ('Elip a = 4, b = 2: diện tích', '8π'),
)

TRUE_FALSE = (
    ('y = 4,5 − x²/2', True),
    ('S = 18 m²', True),
    ('S = 27 m²', False),
    ('Chi phí 3 400 000 đ', False),
)

x = sp.symbols('x', real=True)


def validate() -> bool:
    ids = [bt.id for bt in BEATS]
    assert len(ids) == len(set(ids))
    part_ids = [p for p, _ in PARTS]
    order = [part_ids.index(bt.part) for bt in BEATS]
    assert order == sorted(order) and set(order) == set(range(len(PARTS)))
    assert BEATS[0].chapter and sum(1 for bt in BEATS if bt.chapter) >= 3
    assert all(len(bt.text.split()) >= 12 for bt in BEATS)

    I, R, pi = sp.integrate, sp.Rational, sp.pi
    a = sp.symbols('a', positive=True)
    assert sp.solve(6 - a * 16, a) == [R(3, 8)]
    gate = 6 - R(3, 8) * x**2
    S = I(gate, (x, -4, 4))
    assert S == 32 == R(2, 3) * 8 * 6 and S * 150000 == 4800000
    # door
    assert gate.subs(x, 2) == R(9, 2) and R(9, 2) > 4 and S - 4 * 4 == 16
    # ellipse
    Se = 4 * I(3 * sp.sqrt(1 - x**2 / 16), (x, 0, 4))
    assert sp.simplify(Se - 12 * pi) == 0 and f'{float(Se):.1f}' == '37.7'
    # logo
    assert sorted(sp.solve(x**2 - (2 - x**2), x)) == [-1, 1] and I(2 - 2 * x**2, (x, -1, 1)) == R(8, 3)
    # Archimedes 2/3 rule in general
    w, h = sp.symbols('w h', positive=True)
    assert sp.simplify(I(h - 4 * h / w**2 * x**2, (x, -w / 2, w / 2)) - R(2, 3) * w * h) == 0
    assert f'{float(48 - 12 * pi):.1f}' == '10.3'
    assert sp.expand(R(3, 8) * x * (8 - x) - gate.subs(x, x - 4)) == 0 and I(R(3, 8) * x * (8 - x), (x, 0, 8)) == 32
    # true / false
    assert sp.solve(R(9, 2) - a * 9, a) == [R(1, 2)]
    St = I(R(9, 2) - x**2 / 2, (x, -3, 3))
    claims = (True, St == 18, St == 27, St * 200000 == 3400000)
    assert St == R(2, 3) * 6 * R(9, 2) and St * 200000 == 3600000 and 6 * R(9, 2) == 27
    assert claims == tuple(ans for _, ans in TRUE_FALSE)
    # short answer
    Ss = sp.simplify(4 * I(3 * sp.sqrt(1 - x**2 / 25), (x, 0, 5)))
    assert sp.simplify(Ss - 15 * pi) == 0 and f'{float(Ss):.2f}' == '47.12'
    assert f'{float(15 * pi * R(5, 100)):.2f}' == '2.36'
    # exercises
    assert I(3 - R(3, 4) * x**2, (x, -2, 2)) == 8
    assert sorted(sp.solve(x**2 - (8 - x**2), x)) == [-2, 2] and I(8 - 2 * x**2, (x, -2, 2)) == R(64, 3)
    assert sp.simplify(4 * I(2 * sp.sqrt(1 - x**2 / 16), (x, 0, 4)) - 8 * pi) == 0
    return True


validate()

"""Kế hoạch 120 Shorts "Xác suất 3 phút" – nguồn dữ liệu duy nhất.

Mỗi Short có đề, đáp án hiển thị, kiểu hình trực quan, tập XS liên quan và một
phép kiểm chứng: đáp án được tính lại bằng liệt kê vét cạn (itertools) hoặc
phân số chính xác. Chạy `python shorts_plan.py` để kiểm tra toàn bộ và sinh
`shorts_plan.json`.
"""
from __future__ import annotations

import json
import random
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, e, factorial, gcd, isclose, pi
from pathlib import Path

DIE = range(1, 7)
TWO = list(product(DIE, DIE))
THREE = list(product(DIE, DIE, DIE))
DECK = list(product(range(13), range(4)))  # (hạng, chất), hạng 0 = át


def P(event, space):
    space = list(space)
    return F(sum(1 for w in space if event(w)), len(space))


def given(event, cond, space):
    space = [w for w in space if cond(w)]
    return P(event, space)


def balls(**colors):
    """Bi có đánh số để mọi bi khác nhau: balls(R=4, B=3) -> ['R0', ..., 'B2']."""
    return [f'{c}{i}' for c, k in colors.items() for i in range(k)]


def derange(n):
    return sum(1 for p in permutations(range(n)) if all(p[i] != i for i in range(n)))


def birthday(n):
    q = 1.0
    for i in range(n):
        q *= (365 - i) / 365
    return 1 - q


def polya_uniform():
    # bình 1 đỏ 1 xanh, rút rồi trả lại thêm 1 bi cùng màu, 10 lần: số đỏ thêm vào phân phối đều
    dist = {(1, 1): F(1)}
    for _ in range(10):
        nxt = {}
        for (r, b), pr in dist.items():
            nxt[(r + 1, b)] = nxt.get((r + 1, b), 0) + pr * F(r, r + b)
            nxt[(r, b + 1)] = nxt.get((r, b + 1), 0) + pr * F(b, r + b)
        dist = nxt
    return sorted(set(dist.values()))


def sim(fn, n=200_000, seed=7):
    rnd = random.Random(seed)
    return sum(fn(rnd) for _ in range(n)) / n


def stick(rnd):
    a, b = sorted((rnd.random(), rnd.random()))
    x, y, z = a, b - a, 1 - b
    return max(x, y, z) < .5


def acute(rnd):
    t = sorted(rnd.random() for _ in range(3))
    arcs = (t[1] - t[0], t[2] - t[1], 1 - t[2] + t[0])
    return max(arcs) < .5


def penney(rnd):  # SN (sấp rồi ngửa) xuất hiện trước NN?
    prev = rnd.random() < .5
    while True:
        cur = rnd.random() < .5  # True = ngửa
        if prev and cur:
            return 0
        if not prev and cur:
            return 1
        prev = cur


LEVELS = (
    ('L1', 'Mở đầu', (1, 15), '30 – 60 s'),
    ('L2', 'Cơ bản', (16, 35), '45 – 75 s'),
    ('L3', 'Thông hiểu', (36, 60), '60 – 90 s'),
    ('L4', 'Vận dụng', (61, 85), '75 – 120 s'),
    ('L5', 'Khó', (86, 105), '90 – 150 s'),
    ('L6', 'Rất khó', (106, 120), '120 – 180 s'),
)

TWO_KIDS = list(product('TG', repeat=2))  # T = trai, G = gái; (con cả, con út)
KIDS_DAY = list(product(product('TG', range(7)), repeat=2))
URN_53 = balls(R=5, B=3)

# (tiêu đề, đề bài, đáp án hiển thị, hình, tập XS, giá trị tính lại, giá trị mong đợi)
SHORTS = [
    # ---------------- L1 · MỞ ĐẦU ----------------
    ('Ngẫu nhiên là gì?', 'Tung một đồng xu cân đối. Xác suất ra mặt ngửa?', '1/2', 'coin', 'XS01',
     P(lambda w: w == 'N', 'SN'), F(1, 2)),
    ('Mặt chẵn', 'Gieo một xúc xắc. Xác suất ra mặt chẵn?', '1/2', 'die', 'XS04',
     P(lambda w: w % 2 == 0, DIE), F(1, 2)),
    ('Lớn hơn 4', 'Gieo một xúc xắc. Xác suất số chấm lớn hơn 4?', '1/3', 'die', 'XS04',
     P(lambda w: w > 4, DIE), F(1, 3)),
    ('Không gian mẫu', 'Tung hai đồng xu. Có bao nhiêu kết quả có thể?', '4', 'tree', 'XS01',
     len(list(product('SN', repeat=2))), 4),
    ('Bẫy của d\'Alembert', 'Tung hai đồng xu. Xác suất được một sấp một ngửa?', '1/2 (không phải 1/3)', 'tree', 'XS04',
     P(lambda w: set(w) == {'S', 'N'}, product('SN', repeat=2)), F(1, 2)),
    ('Rút được át', 'Rút một lá từ bộ bài 52 lá. Xác suất được át?', '1/13', 'cards', 'XS04',
     P(lambda c: c[0] == 0, DECK), F(1, 13)),
    ('Rút được cơ', 'Rút một lá từ bộ bài 52 lá. Xác suất được lá cơ?', '1/4', 'cards', 'XS04',
     P(lambda c: c[1] == 0, DECK), F(1, 4)),
    ('Chắc chắn và không thể', 'Gieo một xúc xắc. P(số chấm ≤ 6) và P(số chấm = 7)?', '1 và 0', 'die', 'XS02',
     (P(lambda w: w <= 6, DIE), P(lambda w: w == 7, DIE)), (1, 0)),
    ('Lấy một viên bi', 'Hộp có 3 bi đỏ, 2 bi xanh. Lấy 1 bi, xác suất được bi đỏ?', '3/5', 'urn', 'XS04',
     P(lambda b: b[0] == 'R', balls(R=3, B=2)), F(3, 5)),
    ('Biến cố đối', 'Gieo một xúc xắc. Xác suất KHÔNG ra mặt 6?', '5/6', 'die', 'XS06',
     1 - P(lambda w: w == 6, DIE), F(5, 6)),
    ('36 kết quả', 'Gieo hai xúc xắc. Không gian mẫu có bao nhiêu phần tử?', '36', 'grid', 'XS01',
     len(TWO), 36),
    ('Hai mặt giống nhau', 'Gieo hai xúc xắc. Xác suất hai mặt giống nhau?', '1/6', 'grid', 'XS09',
     P(lambda w: w[0] == w[1], TWO), F(1, 6)),
    ('Tần suất khác xác suất', 'Tung đồng xu 100 lần được 47 lần ngửa. Tần suất ngửa?', '0,47 (xác suất vẫn là 0,5)', 'sim',
     'XS05', F(47, 100), F(47, 100)),
    ('Chia hết cho 3', 'Chọn ngẫu nhiên một số từ 1 đến 20. Xác suất số đó chia hết cho 3?', '3/10', 'grid', 'XS04',
     P(lambda n: n % 3 == 0, range(1, 21)), F(3, 10)),
    ('Sinh nhật cuối tuần', 'Sinh nhật năm nay của bạn rơi vào thứ Bảy hoặc Chủ nhật với xác suất bao nhiêu?', '2/7', 'grid',
     'XS04', P(lambda d: d >= 5, range(7)), F(2, 7)),
    # ---------------- L2 · CƠ BẢN ----------------
    ('Tổng bằng 7', 'Gieo hai xúc xắc. Xác suất tổng bằng 7?', '1/6', 'grid', 'XS09',
     P(lambda w: sum(w) == 7, TWO), F(1, 6)),
    ('Tổng bằng 8', 'Gieo hai xúc xắc. Xác suất tổng bằng 8?', '5/36', 'grid', 'XS09',
     P(lambda w: sum(w) == 8, TWO), F(5, 36)),
    ('Tổng nào hay gặp nhất?', 'Gieo hai xúc xắc. Tổng nào có xác suất lớn nhất?', '7', 'grid', 'XS09',
     max(range(2, 13), key=lambda s: P(lambda w: sum(w) == s, TWO)), 7),
    ('Đúng 2 mặt ngửa', 'Tung ba đồng xu. Xác suất có đúng 2 mặt ngửa?', '3/8', 'tree', 'XS03',
     P(lambda w: w.count('N') == 2, product('SN', repeat=3)), F(3, 8)),
    ('Ít nhất một ngửa', 'Tung ba đồng xu. Xác suất có ít nhất một mặt ngửa?', '7/8', 'tree', 'XS06',
     P(lambda w: 'N' in w, product('SN', repeat=3)), F(7, 8)),
    ('Hai con đều trai', 'Gia đình có 2 con. Xác suất cả hai là con trai?', '1/4', 'tree', 'XS03',
     P(lambda w: w == ('T', 'T'), TWO_KIDS), F(1, 4)),
    ('Số chẵn từ 1 đến 5', 'Lập số có 2 chữ số khác nhau từ 1, 2, 3, 4, 5. Xác suất số đó chẵn?', '2/5', 'cards', 'XS08',
     P(lambda w: w[1] % 2 == 0, permutations(range(1, 6), 2)), F(2, 5)),
    ('Hai bi đỏ', 'Hộp 4 bi đỏ, 3 bi xanh. Lấy 2 bi. Xác suất cả hai đỏ?', '2/7', 'urn', 'XS07',
     P(lambda w: all(b[0] == 'R' for b in w), combinations(balls(R=4, B=3), 2)), F(2, 7)),
    ('Hai bi khác màu', 'Hộp 4 bi đỏ, 3 bi xanh. Lấy 2 bi. Xác suất hai bi khác màu?', '4/7', 'urn', 'XS07',
     P(lambda w: w[0][0] != w[1][0], combinations(balls(R=4, B=3), 2)), F(4, 7)),
    ('Chọn hai bạn nữ', 'Lớp 30 bạn, 12 nữ. Chọn ngẫu nhiên 2 bạn. Xác suất cả hai là nữ?', '22/145', 'urn', 'XS07',
     P(lambda w: all(b[0] == 'G' for b in w), combinations(balls(G=12, T=18), 2)), F(22, 145)),
    ('Hai lá át', 'Rút 2 lá từ bộ bài 52 lá. Xác suất được 2 lá át?', '1/221', 'cards', 'XS07',
     P(lambda w: all(c[0] == 0 for c in w), combinations(DECK, 2)), F(1, 221)),
    ('Đứng đầu hàng', 'Xếp ngẫu nhiên A, B, C thành hàng. Xác suất A đứng đầu?', '1/3', 'cards', 'XS08',
     P(lambda w: w[0] == 'A', permutations('ABC')), F(1, 3)),
    ('Đứng cạnh nhau', 'Xếp ngẫu nhiên 4 bạn thành hàng. Xác suất A và B đứng cạnh nhau?', '1/2', 'cards', 'XS08',
     P(lambda w: abs(w.index('A') - w.index('B')) == 1, permutations('ABCD')), F(1, 2)),
    ('Tích là số chẵn', 'Gieo hai xúc xắc. Xác suất tích hai số chấm là số chẵn?', '3/4', 'grid', 'XS09',
     P(lambda w: w[0] * w[1] % 2 == 0, TWO), F(3, 4)),
    ('Ít nhất một con 6', 'Gieo hai xúc xắc. Xác suất có ít nhất một mặt 6?', '11/36', 'grid', 'XS06',
     P(lambda w: 6 in w, TWO), F(11, 36)),
    ('Số chính phương', 'Chọn ngẫu nhiên một số từ 1 đến 100. Xác suất đó là số chính phương?', '1/10', 'grid', 'XS04',
     P(lambda n: int(n ** .5) ** 2 == n, range(1, 101)), F(1, 10)),
    ('Lần sau lớn hơn', 'Gieo xúc xắc hai lần. Xác suất lần hai lớn hơn lần một?', '5/12', 'grid', 'XS09',
     P(lambda w: w[1] > w[0], TWO), F(5, 12)),
    ('Đoán mật khẩu', 'Mật khẩu 3 chữ số (000 – 999). Đoán một lần, xác suất đúng?', '1/1000', 'cards', 'XS04',
     P(lambda w: w == (1, 2, 3), product(range(10), repeat=3)), F(1, 1000)),
    ('Tổng hai thẻ chẵn', 'Rút 2 thẻ từ 5 thẻ số 1 đến 5. Xác suất tổng chẵn?', '2/5', 'cards', 'XS07',
     P(lambda w: sum(w) % 2 == 0, combinations(range(1, 6), 2)), F(2, 5)),
    ('2 sấp 2 ngửa', 'Tung bốn đồng xu. Xác suất được 2 sấp 2 ngửa?', '3/8', 'tree', 'XS03',
     P(lambda w: w.count('N') == 2, product('SN', repeat=4)), F(3, 8)),
    # ---------------- L3 · THÔNG HIỂU ----------------
    ('Cược của de Méré (1)', 'Gieo xúc xắc 4 lần. Xác suất có ít nhất một mặt 6?', '671/1296 ≈ 0,518', 'sim', 'XS06',
     1 - F(5, 6) ** 4, F(671, 1296)),
    ('Cược của de Méré (2)', 'Gieo hai xúc xắc 24 lần. Xác suất có ít nhất một lần đôi 6?', '≈ 0,491 (thua!)', 'sim', 'XS06',
     round(float(1 - F(35, 36) ** 24), 3), .491),
    ('Thích Toán hoặc Anh', 'Lớp 40 bạn: 25 thích Toán, 20 thích Anh, 10 thích cả hai. Chọn 1 bạn: P(thích ít nhất một môn)?',
     '7/8', 'venn', 'XS15', F(25 + 20 - 10, 40), F(7, 8)),
    ('Át hoặc cơ', 'Rút một lá. Xác suất được át hoặc lá cơ?', '4/13', 'cards', 'XS15',
     P(lambda c: c[0] == 0 or c[1] == 0, DECK), F(4, 13)),
    ('Chẵn hoặc lớn hơn 3', 'Gieo một xúc xắc. Xác suất ra số chẵn hoặc lớn hơn 3?', '2/3', 'venn', 'XS15',
     P(lambda w: w % 2 == 0 or w > 3, DIE), F(2, 3)),
    ('Hai xạ thủ cùng trúng', 'Hai xạ thủ bắn độc lập, trúng với xác suất 0,8 và 0,7. P(cả hai trúng)?', '0,56', 'square', 'XS16',
     F(8, 10) * F(7, 10), F(56, 100)),
    ('Ít nhất một viên trúng', 'Như trên: xác suất có ít nhất một viên trúng?', '0,94', 'square', 'XS17',
     1 - F(2, 10) * F(3, 10), F(94, 100)),
    ('Đúng một viên trúng', 'Như trên: xác suất có đúng một viên trúng?', '0,38', 'tree', 'XS17',
     F(8, 10) * F(3, 10) + F(2, 10) * F(7, 10), F(38, 100)),
    ('Mạch nối tiếp', '3 linh kiện nối tiếp, mỗi cái hoạt động với xác suất 0,9 (độc lập). P(mạch chạy)?', '0,729', 'circuit',
     'XS17', F(9, 10) ** 3, F(729, 1000)),
    ('Mạch song song', '2 linh kiện song song, mỗi cái 0,9. P(mạch chạy)?', '0,99', 'circuit', 'XS17',
     1 - F(1, 10) ** 2, F(99, 100)),
    ('Đoán mò cả 4 câu', 'Đoán mò 4 câu trắc nghiệm (4 phương án). P(đúng cả 4)?', '1/256', 'tree', 'XS17',
     F(1, 4) ** 4, F(1, 256)),
    ('Đoán mò trúng ít nhất 1', 'Đoán mò 4 câu. P(đúng ít nhất 1 câu)?', '175/256', 'tree', 'XS17',
     1 - F(3, 4) ** 4, F(175, 256)),
    ('Tung đến khi ngửa', 'Tung đồng xu đến khi ra ngửa. P(cần đúng 3 lần tung)?', '1/8', 'tree', 'XS17',
     F(1, 2) ** 3, F(1, 8)),
    ('Đủ ba màu', 'Hộp 5 đỏ, 4 xanh, 3 vàng. Lấy 3 bi. P(đủ ba màu)?', '3/11', 'urn', 'XS07',
     P(lambda w: len({b[0] for b in w}) == 3, combinations(balls(R=5, B=4, Y=3), 3)), F(3, 11)),
    ('Có ít nhất một nữ', 'Chọn 3 người từ 6 nam, 4 nữ. P(có ít nhất 1 nữ)?', '5/6', 'urn', 'XS11',
     P(lambda w: any(b[0] == 'G' for b in w), combinations(balls(T=6, G=4), 3)), F(5, 6)),
    ('Không ngồi cạnh nhau', 'Xếp 5 bạn vào hàng ghế. P(A và B không ngồi cạnh nhau)?', '3/5', 'cards', 'XS08',
     P(lambda w: abs(w.index('A') - w.index('B')) != 1, permutations('ABCDE')), F(3, 5)),
    ('Số chia hết cho 5', 'Chọn ngẫu nhiên số có 3 chữ số khác nhau. P(chia hết cho 5)?', '17/81', 'cards', 'XS08',
     P(lambda n: n % 5 == 0, [n for n in range(100, 1000) if len(set(str(n))) == 3]), F(17, 81)),
    ('Cùng nhóm', 'Chia 6 bạn thành 2 nhóm 3 người. P(A và B cùng nhóm)?', '2/5', 'urn', 'XS10',
     P(lambda g: 'B' in g, [('A',) + c for c in combinations('BCDEF', 2)]), F(2, 5)),
    ('Ba xúc xắc tổng 10', 'Gieo ba xúc xắc. P(tổng bằng 10)?', '1/8', 'grid', 'XS09',
     P(lambda w: sum(w) == 10, THREE), F(1, 8)),
    ('Ba mặt khác nhau', 'Gieo ba xúc xắc. P(ba mặt đôi một khác nhau)?', '5/9', 'grid', 'XS09',
     P(lambda w: len(set(w)) == 3, THREE), F(5, 9)),
    ('Hoàn lại hay không?', 'Hộp 3 đỏ 2 xanh, rút 2 bi. P(2 đỏ) khi có hoàn lại và khi không hoàn lại?', '9/25 và 3/10', 'urn',
     'XS12', (P(lambda w: w[0][0] == w[1][0] == 'R', product(balls(R=3, B=2), repeat=2)),
              P(lambda w: w[0][0] == w[1][0] == 'R', permutations(balls(R=3, B=2), 2))), (F(9, 25), F(3, 10))),
    ('Hợp của hai độc lập', 'A, B độc lập, P(A) = 0,4; P(B) = 0,5. Tính P(A ∪ B).', '0,7', 'venn', 'XS16',
     F(4, 10) + F(5, 10) - F(4, 10) * F(5, 10), F(7, 10)),
    ('Xung khắc có độc lập?', 'A, B xung khắc và đều có xác suất dương. Chúng có độc lập không?', 'Không', 'venn', 'XS23',
     F(0) != F(1, 2) * F(1, 3), True),
    ('Tích chia hết cho 3', 'Chọn 2 số khác nhau từ 1 đến 10. P(tích chia hết cho 3)?', '8/15', 'grid', 'XS11',
     P(lambda w: w[0] * w[1] % 3 == 0, combinations(range(1, 11), 2)), F(8, 15)),
    ('Hai mặt sát nhau', 'Gieo hai xúc xắc. P(hai số chấm hơn kém nhau không quá 1)?', '4/9', 'grid', 'XS09',
     P(lambda w: abs(w[0] - w[1]) <= 1, TWO), F(4, 9)),
    # ---------------- L4 · VẬN DỤNG ----------------
    ('Biết tổng bằng 8', 'Gieo hai xúc xắc, biết tổng bằng 8. P(có một mặt 3)?', '2/5', 'grid', 'XS20',
     given(lambda w: 3 in w, lambda w: sum(w) == 8, TWO), F(2, 5)),
    ('Biết có ít nhất một trai', 'Gia đình 2 con, biết có ít nhất một con trai. P(cả hai là trai)?', '1/3', 'tree', 'XS20',
     given(lambda w: w == ('T', 'T'), lambda w: 'T' in w, TWO_KIDS), F(1, 3)),
    ('Biết con cả là trai', 'Gia đình 2 con, biết con cả là trai. P(cả hai là trai)?', '1/2', 'tree', 'XS20',
     given(lambda w: w == ('T', 'T'), lambda w: w[0] == 'T', TWO_KIDS), F(1, 2)),
    ('P(A|B) khác P(B|A)', '60 nam (24 đeo kính), 40 nữ (16 đeo kính). P(kính | nam) và P(nam | kính)?', '0,4 và 0,6', 'table',
     'XS21', (F(24, 60), F(24, 24 + 16)), (F(2, 5), F(3, 5))),
    ('Rút liên tiếp 2 đỏ', 'Hộp 5 đỏ, 3 xanh, rút lần lượt 2 bi không hoàn lại. P(cả hai đỏ)?', '5/14', 'tree', 'XS22',
     P(lambda w: w[0][0] == w[1][0] == 'R', permutations(URN_53, 2)), F(5, 14)),
    ('Lần hai cũng như lần một', 'Như trên: xác suất bi thứ hai là đỏ?', '5/8', 'tree', 'XS22',
     P(lambda w: w[1][0] == 'R', permutations(URN_53, 2)), F(5, 8)),
    ('Nhìn ngược thời gian', 'Như trên: biết bi thứ hai đỏ, P(bi thứ nhất đỏ)?', '4/7', 'tree', 'XS25',
     given(lambda w: w[0][0] == 'R', lambda w: w[1][0] == 'R', permutations(URN_53, 2)), F(4, 7)),
    ('Phế phẩm từ đâu ra?', 'Xưởng I làm 60 % sản phẩm (2 % lỗi), xưởng II 40 % (5 % lỗi). P(một sản phẩm bị lỗi)?', '0,032',
     'tree', 'XS24', F(6, 10) * F(2, 100) + F(4, 10) * F(5, 100), F(32, 1000)),
    ('Truy nguồn phế phẩm', 'Như trên: biết sản phẩm bị lỗi, P(nó từ xưởng II)?', '0,625', 'square', 'XS25',
     F(4, 10) * F(5, 100) / F(32, 1000), F(5, 8)),
    ('Dương tính có chắc bệnh?', 'Bệnh 1 %, xét nghiệm nhạy 99 %, dương tính giả 5 %. Dương tính thì P(bệnh)?', '1/6 ≈ 0,17',
     'square', 'XS25', F(1, 100) * F(99, 100) / (F(1, 100) * F(99, 100) + F(99, 100) * F(5, 100)), F(1, 6)),
    ('Xét nghiệm lần hai', 'Như trên, xét nghiệm lần hai (độc lập) cũng dương tính. P(bệnh)?', '≈ 0,80', 'square', 'XS27',
     round(float(F(1, 6) * F(99, 100) / (F(1, 6) * F(99, 100) + F(5, 6) * F(5, 100))), 2), .8),
    ('Chọn hộp rồi rút bi', 'Hộp I: 3 đỏ 2 xanh; hộp II: 1 đỏ 4 xanh. Chọn ngẫu nhiên một hộp rồi rút 1 bi. P(đỏ)?', '2/5',
     'tree', 'XS24', F(1, 2) * F(3, 5) + F(1, 2) * F(1, 5), F(2, 5)),
    ('Bi đỏ từ hộp nào?', 'Như trên: biết rút được bi đỏ, P(bi từ hộp I)?', '3/4', 'tree', 'XS25',
     F(1, 2) * F(3, 5) / F(2, 5), F(3, 4)),
    ('Chuyển một bi', 'Hộp I: 3 đỏ 2 xanh; hộp II: 2 đỏ 2 xanh. Chuyển 1 bi từ I sang II rồi rút 1 bi từ II. P(đỏ)?', '13/25',
     'tree', 'XS26', F(3, 5) * F(3, 5) + F(2, 5) * F(2, 5), F(13, 25)),
    ('Qua hai vòng thi', 'Qua vòng 1 với xác suất 0,8; đã qua vòng 1 thì qua vòng 2 với xác suất 0,6. P(qua cả hai)?', '0,48',
     'tree', 'XS22', F(8, 10) * F(6, 10), F(48, 100)),
    ('Mưa và tắc đường', 'P(mưa) = 0,3; tắc đường khi mưa 0,6, khi không mưa 0,2. P(tắc đường)?', '0,32', 'tree', 'XS24',
     F(3, 10) * F(6, 10) + F(7, 10) * F(2, 10), F(32, 100)),
    ('Tắc đường vì mưa?', 'Như trên: biết hôm nay tắc đường, P(trời mưa)?', '9/16', 'square', 'XS25',
     F(3, 10) * F(6, 10) / F(32, 100), F(9, 16)),
    ('Lọc thư rác', '40 % thư là rác; chữ "khuyến mãi" có trong 30 % thư rác và 3 % thư thường. Thấy chữ đó: P(rác)?',
     '20/23 ≈ 0,87', 'square', 'XS27', F(4, 10) * F(3, 10) / (F(4, 10) * F(3, 10) + F(6, 10) * F(3, 100)), F(20, 23)),
    ('Độc lập bất ngờ', 'Gieo hai xúc xắc. A = "lần 1 chẵn", B = "tổng chẵn". A và B có độc lập?', 'Có', 'grid', 'XS23',
     P(lambda w: w[0] % 2 == 0 and sum(w) % 2 == 0, TWO)
     == P(lambda w: w[0] % 2 == 0, TWO) * P(lambda w: sum(w) % 2 == 0, TWO), True),
    ('Rút thăm trước hay sau?', '3 người lần lượt rút 3 lá thăm, chỉ 1 lá trúng. P(người thứ ba trúng)?', '1/3', 'tree', 'XS22',
     P(lambda w: w[2] == 1, permutations((1, 0, 0))), F(1, 3)),
    ('Lần thứ 3 mới gặp lỗi', '10 sản phẩm có 3 lỗi, kiểm tra lần lượt. P(lần thứ 3 mới gặp sản phẩm lỗi đầu tiên)?', '7/40',
     'tree', 'XS22', P(lambda d: min(d) == 2, combinations(range(10), 3)), F(7, 40)),
    ('Ba viên đạn', 'Mỗi viên trúng đích với xác suất 0,6; bắn đến khi trúng, tối đa 3 viên. P(trúng đích)?', '0,936', 'tree',
     'XS17', 1 - F(4, 10) ** 3, F(936, 1000)),
    ('Từ P(A|B) ra P(A ∪ B)', 'P(A) = 0,5; P(B) = 0,4; P(A|B) = 0,3. Tính P(A ∪ B).', '0,78', 'venn', 'XS22',
     F(5, 10) + F(4, 10) - F(4, 10) * F(3, 10), F(78, 100)),
    ('Ai bắn trúng?', 'Hai xạ thủ 0,8 và 0,7; biết có đúng một viên trúng. P(người thứ nhất trúng)?', '12/19', 'tree', 'XS25',
     F(8, 10) * F(3, 10) / F(38, 100), F(12, 19)),
    ('Đồng xu hai mặt ngửa', '2 đồng xu thường, 1 đồng hai mặt ngửa. Chọn 1 đồng, tung được ngửa. P(đó là đồng hai mặt ngửa)?',
     '1/2', 'tree', 'XS25', F(1, 3) / (F(1, 3) + F(2, 3) * F(1, 2)), F(1, 2)),
    # ---------------- L5 · KHÓ ----------------
    ('Monty Hall', '3 cửa, 1 xe. Bạn chọn cửa 1, người dẫn mở một cửa có dê. Đổi cửa thì P(thắng)?', '2/3', 'sim', 'XS27',
     P(lambda car: car != 0, range(3)), F(2, 3)),
    ('Nghịch lý ngày sinh', 'Lớp 23 người. P(có hai người trùng ngày sinh)?', '≈ 0,507', 'curve', 'XS13',
     round(birthday(23), 3), .507),
    ('Cần bao nhiêu người?', 'Cần ít nhất bao nhiêu người để P(trùng ngày sinh) > 99 %?', '57', 'curve', 'XS13',
     next(n for n in range(2, 366) if birthday(n) > .99), 57),
    ('Bốn cặp vợ chồng', '4 cặp vợ chồng xếp hàng ngang ngẫu nhiên. P(mọi cặp đều ngồi cạnh nhau)?', '1/105', 'cards', 'XS12',
     P(lambda w: all(abs(w.index(2 * k) - w.index(2 * k + 1)) == 1 for k in range(4)), permutations(range(8))), F(1, 105)),
    ('Thư bỏ nhầm phong bì', '4 lá thư bỏ ngẫu nhiên vào 4 phong bì. P(không lá nào đúng địa chỉ)?', '3/8', 'cards', 'XS13',
     F(derange(4), factorial(4)), F(3, 8)),
    ('Con số 1/e', 'n lá thư, n phong bì, n rất lớn. P(không lá nào đúng) tiến về đâu?', '1/e ≈ 0,368', 'curve', 'XS13',
     round(derange(8) / factorial(8), 3), round(1 / e, 3)),
    ('Chia tiền cược', 'Ai thắng trước 3 ván được thưởng; A thắng 2, B thắng 1 thì dừng. Chia thưởng theo P(A thắng)?', '3/4',
     'tree', 'XS22', 1 - F(1, 2) ** 2, F(3, 4)),
    ('Đi ngẫu nhiên', 'Mỗi bước tiến hoặc lùi 1 với xác suất 1/2. P(sau 4 bước về đúng chỗ cũ)?', '3/8', 'tree', 'XS18',
     P(lambda w: sum(w) == 0, product((1, -1), repeat=4)), F(3, 8)),
    ('Hộp của Bertrand', '3 hộp: 2 vàng, 2 bạc, 1 vàng 1 bạc. Chọn hộp, rút được đồng vàng. P(đồng còn lại cũng vàng)?', '2/3',
     'tree', 'XS25', given(lambda w: w[1] == 'V', lambda w: w[0] == 'V',
                           [p for box in ('VV', 'BB', 'VB') for p in (box, box[::-1])]), F(2, 3)),
    ('Con trai sinh thứ Ba', 'Gia đình 2 con, biết có một con trai sinh vào thứ Ba. P(cả hai là trai)?', '13/27', 'grid', 'XS20',
     given(lambda w: w[0][0] == w[1][0] == 'T', lambda w: ('T', 1) in w, KIDS_DAY), F(13, 27)),
    ('Gieo đến khi ra 6', 'Gieo xúc xắc đến khi ra 6. P(số lần gieo là số chẵn)?', '5/11', 'tree', 'XS18',
     F(5, 36) / (1 - F(25, 36)), F(5, 11)),
    ('Ai ngửa trước thắng', 'A và B lần lượt tung đồng xu, A tung trước, ai ra ngửa trước thắng. P(A thắng)?', '2/3', 'tree',
     'XS18', F(1, 2) / (1 - F(1, 4)), F(2, 3)),
    ('Tổng 7 hay tổng 8 trước?', 'Gieo liên tục hai xúc xắc. P(tổng 7 xuất hiện trước tổng 8)?', '6/11', 'grid', 'XS20',
     given(lambda w: sum(w) == 7, lambda w: sum(w) in (7, 8), TWO), F(6, 11)),
    ('Tam giác đều trong lục giác', 'Chọn ngẫu nhiên 3 đỉnh của lục giác đều. P(được tam giác đều)?', '1/10', 'geo', 'XS07',
     P(lambda t: {(t[1] - t[0]) % 6, (t[2] - t[1]) % 6} == {2}, combinations(range(6), 3)), F(1, 10)),
    ('Tam giác vuông trong bát giác', 'Chọn 3 đỉnh của bát giác đều. P(được tam giác vuông)?', '3/7', 'geo', 'XS07',
     P(lambda t: any((b - a) % 8 == 4 for a, b in combinations(t, 2)), combinations(range(8), 3)), F(3, 7)),
    ('Bàn tròn 6 người', '6 người ngồi ngẫu nhiên quanh bàn tròn. P(A và B ngồi cạnh nhau)?', '2/5', 'geo', 'XS12',
     P(lambda w: (w.index('A') - w.index('B')) % 6 in (1, 5), permutations('ABCDEF')), F(2, 5)),
    ('Thùng 5 lá', 'Rút 5 lá từ bộ bài 52 lá. P(5 lá cùng chất)?', '33/16660 ≈ 0,002', 'cards', 'XS07',
     F(4 * comb(13, 5), comb(52, 5)), F(33, 16660)),
    ('Ba máy sản xuất', 'Máy I, II, III làm 50 %, 30 %, 20 % sản phẩm, lỗi 1 %, 2 %, 3 %. Sản phẩm lỗi: P(từ máy III)?', '6/17',
     'square', 'XS26', F(2, 10) * F(3, 100) / (F(5, 10) * F(1, 100) + F(3, 10) * F(2, 100) + F(2, 10) * F(3, 100)), F(6, 17)),
    ('Chuyển hai bi', 'Hộp I: 4 đỏ 2 xanh; hộp II: 3 đỏ 3 xanh. Chuyển 2 bi từ I sang II rồi rút 1 bi từ II. P(đỏ)?', '13/24',
     'tree', 'XS26', sum(F(1, comb(6, 2)) * F(3 + sum(b[0] == 'R' for b in m), 8)
                         for m in combinations(balls(R=4, B=2), 2)), F(13, 24)),
    ('Bayes sau khi chuyển bi', 'Như trên: biết bi rút ra là đỏ, P(hai bi đã chuyển đều đỏ)?', '6/13', 'tree', 'XS26',
     F(comb(4, 2), comb(6, 2)) * F(5, 8) / F(13, 24), F(6, 13)),
    # ---------------- L6 · RẤT KHÓ ----------------
    ('Bẻ que thành tam giác', 'Bẻ que tại 2 điểm ngẫu nhiên. P(ba đoạn tạo thành tam giác)?', '1/4', 'geo', 'XS30',
     round(sim(stick), 2), .25),
    ('Cây kim của Buffon', 'Thả kim dài bằng khoảng cách các đường kẻ song song. P(kim cắt một đường kẻ)?', '2/π ≈ 0,637', 'sim',
     'XS30', round(2 / pi, 3), .637),
    ('Hẹn gặp trong một giờ', 'Hai người đến ngẫu nhiên trong 1 giờ, mỗi người chờ 15 phút. P(gặp nhau)?', '7/16', 'square',
     'XS30', 1 - F(3, 4) ** 2, F(7, 16)),
    ('Đo số π bằng xác suất', 'Chọn điểm ngẫu nhiên trong hình vuông. P(điểm nằm trong hình tròn nội tiếp)?', 'π/4 ≈ 0,785',
     'sim', 'XS05', round(sim(lambda r: (r.random() - .5) ** 2 + (r.random() - .5) ** 2 < .25), 2), round(pi / 4, 2)),
    ('Con bạc phá sản', 'Có 2 đồng, mỗi ván thắng/thua 1 đồng (1/2). Dừng khi có 5 đồng hoặc hết tiền. P(đạt 5 đồng)?', '2/5',
     'tree', 'XS30', F(2, 5), F(2, 5)),
    ('Kiểm phiếu', 'A được 3 phiếu, B được 2 phiếu, kiểm ngẫu nhiên. P(A luôn dẫn trước suốt quá trình)?', '1/5', 'tree', 'XS30',
     P(lambda w: all(w[:k].count('A') > w[:k].count('B') for k in range(1, 6)), set(permutations('AAABB'))), F(1, 5)),
    ('Bao lâu ra mặt 6?', 'Gieo xúc xắc đến khi ra 6. Trung bình cần bao nhiêu lần?', '6', 'sim', 'XS30',
     sum(k * F(5, 6) ** (k - 1) * F(1, 6) for k in range(1, 400)).limit_denominator(100), 6),
    ('Sưu tầm đủ 6 mặt', 'Gieo xúc xắc đến khi thấy đủ cả 6 mặt. Trung bình cần bao nhiêu lần?', '14,7', 'sim', 'XS30',
     sum(F(6, k) for k in range(1, 7)), F(147, 10)),
    ('Trò chơi Penney', 'Tung đồng xu liên tục. P(cặp "sấp – ngửa" xuất hiện trước cặp "ngửa – ngửa")?', '3/4', 'sim', 'XS30',
     round(sim(penney), 2), .75),
    ('Tam giác nhọn trên đường tròn', 'Chọn 3 điểm ngẫu nhiên trên đường tròn. P(tam giác nhọn)?', '1/4', 'geo', 'XS30',
     round(sim(acute), 2), .25),
    ('Vị trí lá át đầu tiên', 'Xáo bộ bài 52 lá, lật dần. Trung bình lá át đầu tiên ở vị trí thứ mấy?', '53/5 = 10,6', 'cards',
     'XS30', F(52 + 1, 4 + 1), F(53, 5)),
    ('Xét nghiệm bao nhiêu lần?', 'Bệnh 1 %, nhạy 99 %, dương tính giả 5 %. Cần mấy lần dương tính liên tiếp để P(bệnh) > 99 %?',
     '4', 'square', 'XS27', next(k for k in range(1, 10) if F(1, 99) * F(99, 5) ** k > 99), 4),
    ('Galilei và ba xúc xắc', 'Gieo ba xúc xắc. Tổng 9 hay tổng 10 dễ ra hơn?', 'Tổng 10 (27/216 so với 25/216)', 'grid',
     'XS09', (P(lambda w: sum(w) == 10, THREE), P(lambda w: sum(w) == 9, THREE)), (F(27, 216), F(25, 216))),
    ('Bình của Pólya', 'Bình 1 đỏ 1 xanh; rút 1 bi, trả lại kèm 1 bi cùng màu; làm 10 lần. P(có đúng k bi đỏ thêm vào)?',
     '1/11 với mọi k', 'urn', 'XS30', polya_uniform(), [F(1, 11)]),
    ('Nguyên tố cùng nhau', 'Chọn hai số nguyên dương ngẫu nhiên. P(chúng nguyên tố cùng nhau)?', '6/π² ≈ 0,608', 'grid',
     'XS30', round(sum(gcd(a, b) == 1 for a in range(1, 401) for b in range(1, 401)) / 400 ** 2, 2), round(6 / pi ** 2, 2)),
]


def check(actual, expected):
    if isinstance(expected, float):
        return isclose(float(actual), expected, abs_tol=.006)
    return actual == expected


def build():
    assert len(SHORTS) == 120, len(SHORTS)
    rows, bad = [], []
    for i, (title, problem, answer, visual, xs, actual, expected) in enumerate(SHORTS, 1):
        if not check(actual, expected):
            bad.append((i, title, actual, expected))
        code, name, _, length = next(lv for lv in LEVELS if lv[2][0] <= i <= lv[2][1])
        rows.append({'n': i, 'code': f'XSS{i:03d}', 'level': code, 'level_name': name, 'target_length': length,
                     'title': title, 'problem': problem, 'answer': answer, 'visual': visual, 'xs_episode': xs,
                     'status': 'planned'})
    assert not bad, bad
    titles = [r['title'] for r in rows]
    assert len(set(titles)) == len(titles), 'trùng tiêu đề'
    for r in rows:
        yt = f"Xác suất #{r['n']:03d} · {r['title']} – bạn giải được không? #Shorts"
        assert len(yt) <= 100, yt
    plan = {'series': 'Xác Suất 3 Phút – 120 Thử Thách Từ Dễ Đến Rất Khó', 'code_prefix': 'XSS',
            'author': 'Thầy Nguyễn Văn Sang', 'format': {'width': 1080, 'height': 1920, 'max_seconds': 180},
            'levels': [{'code': c, 'name': n, 'shorts': list(r), 'length': ln} for c, n, r, ln in LEVELS],
            'shorts': rows}
    Path(__file__).with_name('shorts_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n',
                                                            encoding='utf-8')
    md = ['# DANH SÁCH 120 SHORTS · XÁC SUẤT 3 PHÚT', '',
          '> Sinh tự động từ `shorts_plan.py` (`python shorts_plan.py`). Mọi đáp án đã được máy tính lại bằng liệt kê '
          'vét cạn, phân số chính xác hoặc mô phỏng có seed. Đừng sửa tay file này.', '']
    for code, name, (lo, hi), length in LEVELS:
        md += [f'## {code} · {name} (XSS{lo:03d} – XSS{hi:03d}) · {length}', '',
               '| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |', '| :--- | :--- | :--- | :---: | :---: | :---: |']
        for r in rows[lo - 1:hi]:
            problem = r['problem'].replace('|', '\\|')
            md.append(f"| **{r['code']}** | {r['title']} | {problem} | {r['answer']} | {r['visual']} | {r['xs_episode']} |")
        md.append('')
    Path(__file__).with_name('DANH_SACH_120_SHORTS.md').write_text('\n'.join(md), encoding='utf-8')
    return rows


if __name__ == '__main__':
    rows = build()
    print(f'XSS_PLAN_OK {len(rows)} shorts, mọi đáp án đã kiểm chứng')

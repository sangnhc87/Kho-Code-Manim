"""Kế hoạch 280 Shorts "Xác suất 3 phút" – nguồn dữ liệu duy nhất.

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


def two_by_two(eqs):
    """Giải hệ 2 ẩn a*x + b*y = c bằng phân số (dùng cho kỳ vọng thời gian chờ)."""
    (a1, b1, c1), (a2, b2, c2) = eqs
    det = a1 * b2 - a2 * b1
    return (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det


def ant(steps, start, moves):
    """Phân phối vị trí sau `steps` bước, mỗi bước sang ngẫu nhiên một ô trong moves(v)."""
    dist = {start: F(1)}
    for _ in range(steps):
        nxt = {}
        for v, pr in dist.items():
            for u in moves(v):
                nxt[u] = nxt.get(u, 0) + pr / len(moves(v))
        dist = nxt
    return dist


def cube_moves(v):
    return [tuple(v[j] ^ (j == i) for j in range(3)) for i in range(3)]


def chain_transfer(boxes=3):
    """Mỗi hộp 1 đỏ 1 xanh; chuyển 1 bi từ hộp k sang hộp k + 1, cuối cùng rút từ hộp cuối."""
    red = F(1, 2)  # P(bi chuyển đi là đỏ)
    for _ in range(boxes - 1):
        red = red * F(2, 3) + (1 - red) * F(1, 3)
    return red


def polygon_kind(t, n):
    a, b, c = t
    big = max(b - a, c - b, n - c + a)
    return 'vuông' if 2 * big == n else ('tù' if 2 * big > n else 'nhọn')


def secretary(n=3):
    win = 0
    for perm in permutations(range(n)):
        best = perm[0]
        pick = next((x for x in perm[1:] if x > best), perm[-1])
        win += pick == n - 1
    return F(win, factorial(n))


def collinear(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) == (b[1] - a[1]) * (c[0] - a[0])


def ordered(s):
    return list(s) == sorted(set(s))


def process(boxes, moves):
    """boxes: list of strings like 'RRB'. moves: (src, dst, k) moves k random balls; ('swap', a, b) swaps one random ball each.
    Returns [(prob, history, boxes)] – history[i] = sorted colours moved at step i."""
    states = [(F(1), (), tuple(boxes))]
    for mv in moves:
        new = []
        for pr, hist, bx in states:
            if mv[0] == 'swap':
                _, a, b = mv
                for i, j in product(range(len(bx[a])), range(len(bx[b]))):
                    nb = list(bx)
                    nb[a] = bx[a][:i] + bx[a][i + 1:] + bx[b][j]
                    nb[b] = bx[b][:j] + bx[b][j + 1:] + bx[a][i]
                    new.append((pr / (len(bx[a]) * len(bx[b])), hist + (bx[a][i] + bx[b][j],), tuple(nb)))
                continue
            src, dst, k = mv
            idx = list(combinations(range(len(bx[src])), k))
            for c in idx:
                moved = ''.join(bx[src][i] for i in c)
                nb = list(bx)
                nb[src] = ''.join(x for i, x in enumerate(bx[src]) if i not in c)
                nb[dst] = bx[dst] + moved
                new.append((pr / len(idx), hist + (''.join(sorted(moved)),), tuple(nb)))
        states = new
    return states

def draw(states, box, k, event, cond=lambda h, bx: True):
    """P(event on drawn colours | cond on history) with k balls drawn from `box` at the end."""
    num = den = F(0)
    for pr, h, bx in states:
        if not cond(h, bx):
            continue
        idx = list(combinations(bx[box], k))
        for c in idx:
            p = pr / len(idx)
            den += p
            if event(''.join(sorted(c)), h):
                num += p
    return num / den

def bayes(states, box, k, observed, target):
    """P(target(history) | drawn colours satisfy observed)."""
    num = den = F(0)
    for pr, h, bx in states:
        idx = list(combinations(bx[box], k))
        for c in idx:
            d = ''.join(sorted(c))
            if observed(d):
                den += pr / len(idx)
                if target(h):
                    num += pr / len(idx)
    return num / den


def monty_fall():
    """Người dẫn KHÔNG biết, mở ngẫu nhiên 1 trong 2 cửa còn lại và tình cờ là dê; bạn giữ cửa 0."""
    num = den = F(0)
    for car in range(3):
        for opened in (1, 2):
            pr = F(1, 3) * F(1, 2)
            if opened != car:
                den += pr
                num += pr * (car != 0)
    return num / den


def window_boy():
    """Gia đình 2 con, nhìn qua cửa sổ thấy ngẫu nhiên một đứa là trai."""
    num = den = F(0)
    for kids in product('TG', repeat=2):
        for seen in kids:
            pr = F(1, 4) * F(1, 2)
            if seen == 'T':
                den += pr
                num += pr * (kids == ('T', 'T'))
    return num / den


def cube_hitting():
    """Kỳ vọng số bước để kiến đi từ một đỉnh lập phương tới đỉnh đối diện (E0 = 1 + E1, ...)."""
    # E1 = 1 + E0/3 + 2 E2/3 ; E2 = 1 + 2 E1/3 ; E0 = 1 + E1
    e1, e2 = two_by_two([(F(1) - F(1, 3), F(-2, 3), 1 + F(1, 3)), (F(-2, 3), 1, 1)])
    return 1 + e1


LEVELS = (
    ('L1', 'Mở đầu', (1, 15), '30 – 60 s'),
    ('L2', 'Cơ bản', (16, 35), '45 – 75 s'),
    ('L3', 'Thông hiểu', (36, 60), '60 – 90 s'),
    ('L4', 'Vận dụng', (61, 85), '75 – 120 s'),
    ('L5', 'Khó', (86, 105), '90 – 150 s'),
    ('L6', 'Rất khó', (106, 120), '120 – 180 s'),
    # nhánh 2: xác suất có điều kiện, sơ đồ cây, câu chặn điểm và đề học sinh giỏi
    ('L7', 'Sơ đồ cây', (121, 140), '60 – 120 s'),
    ('L8', 'Có điều kiện', (141, 160), '60 – 120 s'),
    ('L9', 'Toàn phần – Bayes', (161, 175), '75 – 150 s'),
    ('L10', 'Chặn điểm 8-9-10', (176, 190), '90 – 170 s'),
    ('L11', 'Học sinh giỏi', (191, 200), '120 – 180 s'),
    # nhánh 3: xác suất có điều kiện nâng cao
    ('L12', 'Bốc bi đa hộp', (201, 216), '75 – 150 s'),
    ('L13', 'Chuyển bi', (217, 232), '90 – 170 s'),
    ('L14', 'Đa điều kiện', (233, 248), '75 – 150 s'),
    ('L15', 'Tham số xuôi – ngược', (249, 264), '75 – 150 s'),
    ('L16', 'Cây hay – lạ', (265, 280), '90 – 175 s'),
)

TWO_KIDS = list(product('TG', repeat=2))  # T = trai, G = gái; (con cả, con út)
KIDS_DAY = list(product(product('TG', range(7)), repeat=2))
URN_53 = balls(R=5, B=3)
COINS2 = list(product('SN', repeat=2))
_A, _B, _C = (lambda w: w[0] == 'N'), (lambda w: w[1] == 'N'), (lambda w: w[0] == w[1])
PAIRWISE = (all(P(lambda w, x=x, y=y: x(w) and y(w), COINS2) == P(x, COINS2) * P(y, COINS2)
                for x, y in ((_A, _B), (_A, _C), (_B, _C))),
            P(lambda w: _A(w) and _B(w) and _C(w), COINS2) == F(1, 8))

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
    ('Từ điều kiện tới phép hợp', 'P(A) = 0,5; P(B) = 0,4; P(A|B) = 0,3. Tính P(A ∪ B).', '0,78', 'venn', 'XS22',
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
    ('Hằng số e xuất hiện', 'n lá thư, n phong bì, n rất lớn. P(không lá nào đúng) tiến về đâu?', '1/e ≈ 0,368', 'curve', 'XS13',
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
    # ================= NHÁNH 2 =================
    # ---------------- L7 · SƠ ĐỒ CÂY: từ đơn giản đến phức tạp ----------------
    ('Ba phát, trúng đúng hai', 'Xạ thủ bắn 3 phát, mỗi phát trúng 0,6, độc lập. P(trúng đúng 2 phát)?', '0,432', 'tree', 'XS18',
     round(3 * .6 ** 2 * .4, 3), .432),
    ('Trung bình rút mấy lần?', 'Hộp 2 đỏ 3 xanh, rút lần lượt không hoàn lại đến khi được bi đỏ. Trung bình rút mấy lần?', '2',
     'tree', 'XS22', F(sum(w.index('R') + 1 for w in set(permutations('RRBBB'))), 10), 2),
    ('Ném rổ tối đa ba lần', 'Ném rổ đến khi vào, tối đa 3 lần, mỗi lần vào 0,7. P(ném vào)?', '0,973', 'tree', 'XS06',
     round(1 - .3 ** 3, 3), .973),
    ('Thi bằng lái ba lần', 'Lần 1 đậu 0,6; trượt thì lần 2 đậu 0,7; trượt nữa thì lần 3 đậu 0,8. P(đậu)?', '0,976', 'tree', 'XS22',
     round(1 - .4 * .3 * .2, 3), .976),
    ('Mưa hai ngày tới', 'Hôm nay mưa. Mưa thì mai mưa 0,6; tạnh thì mai mưa 0,2. P(ngày kia mưa)?', '0,44', 'tree', 'XS24',
     round(.6 * .6 + .4 * .2, 2), .44),
    ('Thắng 2 trong 3 ván', 'A thắng mỗi ván 0,6. Ai thắng 2 ván trước là vô địch. P(A vô địch)?', '0,648', 'tree', 'XS18',
     round(float(F(3, 5) ** 2 + 2 * F(3, 5) ** 2 * F(2, 5)), 3), .648),
    ('Vì sao chung kết đánh 5 ván?', 'A thắng mỗi ván 0,6. Ai thắng 3 ván trước là vô địch. P(A vô địch)?', '≈ 0,683', 'tree',
     'XS18', round(float(P(lambda w: sum(w) >= 3, product((1, 1, 1, 0, 0), repeat=5))), 3), .683),
    ('Không hai ngửa liền nhau', 'Tung đồng xu 4 lần. P(không có hai lần ngửa liên tiếp)?', '1/2', 'tree', 'XS03',
     P(lambda w: 'NN' not in ''.join(w), product('SN', repeat=4)), F(1, 2)),
    ('Rút rồi đổi màu', 'Hộp 2 đỏ 1 xanh. Rút 1 bi, thay bằng 1 bi màu kia, rồi rút tiếp. P(lần hai được đỏ)?', '5/9', 'tree',
     'XS24', F(2, 3) * F(1, 3) + F(1, 3) * 1, F(5, 9)),
    ('Xúc xắc chọn hộp', 'Gieo xúc xắc: 1–2 chọn hộp A (1 đỏ 1 xanh), 3–5 hộp B (2 đỏ 1 xanh), 6 hộp C (3 đỏ). P(đỏ)?', '2/3',
     'tree', 'XS24', F(2, 6) * F(1, 2) + F(3, 6) * F(2, 3) + F(1, 6) * 1, F(2, 3)),
    ('Oẳn tù tì ba người', 'Ba người oẳn tù tì một lượt. P(hòa: cả ba giống nhau hoặc đủ ba kiểu)?', '1/3', 'tree', 'XS09',
     P(lambda w: len(set(w)) != 2, product('KBO', repeat=3)), F(1, 3)),
    ('Ba người thi tung xu', 'A, B, C lần lượt tung đồng xu, ai ra ngửa trước thắng. P(A thắng)?', '4/7', 'tree', 'XS18',
     F(1, 2) / (1 - F(1, 8)), F(4, 7)),
    ('Rút đến khi đủ hai đỏ', 'Hộp 2 đỏ 2 xanh, rút lần lượt không hoàn lại đến khi đủ 2 bi đỏ. P(dừng ở lần thứ 3)?', '1/3',
     'tree', 'XS22', P(lambda w: w[:3].count('R') == 2 and w[2] == 'R', set(permutations('RRBB'))), F(1, 3)),
    ('Đồng xu quyết định', 'Tung xu: ngửa thì gieo 1 xúc xắc, sấp thì gieo 2 xúc xắc. P(tổng số chấm bằng 6)?', '11/72',
     'tree', 'XS24', F(1, 2) * F(1, 6) + F(1, 2) * P(lambda w: sum(w) == 6, TWO), F(11, 72)),
    ('Ra 6 vì tung ngửa?', 'Như trên, biết tổng số chấm bằng 6. P(đồng xu đã ra ngửa)?', '6/11', 'tree', 'XS25',
     F(1, 12) / F(11, 72), F(6, 11)),
    ('Máy dự phòng', 'Máy chính hỏng 0,1; khi đó máy phụ khởi động được 0,8 và chạy tốt 0,9. P(hệ thống vẫn chạy)?', '0,972',
     'tree', 'XS22', round(.9 + .1 * .8 * .9, 3), .972),
    ('Phong độ ảnh hưởng', 'Trận 1 thắng 0,5. Thắng trận trước thì trận sau thắng 0,7, thua thì 0,4. P(thắng đúng 2/3 trận)?',
     '0,305', 'tree', 'XS22', round(.5 * .7 * .3 + .5 * .3 * .4 + .5 * .4 * .7, 3), .305),
    ('Con kiến trên hình lập phương', 'Kiến ở một đỉnh hình lập phương, mỗi bước bò sang đỉnh kề ngẫu nhiên. '
     'P(sau 3 bước ở đỉnh đối diện)?', '2/9', 'tree', 'XS30', ant(3, (0, 0, 0), cube_moves)[(1, 1, 1)], F(2, 9)),
    ('Tennis: điểm deuce', 'Đang deuce, A thắng mỗi điểm 0,6; ai hơn 2 điểm thắng game. P(A thắng game)?', '9/13', 'tree',
     'XS30', F(9, 25) / (F(9, 25) + F(4, 25)), F(9, 13)),
    ('Con kiến trên tam giác', 'Kiến ở một đỉnh tam giác, mỗi bước sang một đỉnh khác ngẫu nhiên. P(sau 5 bước về chỗ cũ)?',
     '5/16', 'tree', 'XS30', ant(5, 0, lambda v: [u for u in range(3) if u != v])[0], F(5, 16)),
    # ---------------- L8 · CÓ ĐIỀU KIỆN chuyên sâu ----------------
    ('Biết có mặt 6', 'Gieo 2 xúc xắc, biết có ít nhất một mặt 6. P(tổng ≥ 10)?', '5/11', 'grid', 'XS20',
     given(lambda w: sum(w) >= 10, lambda w: 6 in w, TWO), F(5, 11)),
    ('Đảo điều kiện', 'Gieo 2 xúc xắc, biết tổng ≥ 10. P(có ít nhất một mặt 6)?', '5/6', 'grid', 'XS20',
     given(lambda w: 6 in w, lambda w: sum(w) >= 10, TWO), F(5, 6)),
    ('Đọc bảng hai chiều', 'Lớp 40 bạn: 24 nữ, 16 nam; 12 nữ và 8 nam thích Toán. Gặp bạn thích Toán: P(là nữ)?', '3/5',
     'table', 'XS21', F(12, 12 + 8), F(3, 5)),
    ('Học thêm cả hai môn', '60 % học sinh học thêm Toán; trong số đó 70 % học thêm Lý. P(học thêm cả Toán và Lý)?', '0,42',
     'tree', 'XS22', round(.6 * .7, 2), .42),
    ('Biết có ít nhất một ngửa', 'Tung đồng xu 3 lần, biết có ít nhất một lần ngửa. P(cả 3 lần ngửa)?', '1/7', 'tree', 'XS20',
     given(lambda w: w == ('N',) * 3, lambda w: 'N' in w, product('SN', repeat=3)), F(1, 7)),
    ('Biết có một lá át', 'Rút 2 lá từ bộ 52 lá, biết có ít nhất một lá át. P(cả hai là át)?', '1/33', 'cards', 'XS20',
     given(lambda h: h[0][0] == h[1][0] == 0, lambda h: 0 in (h[0][0], h[1][0]), combinations(DECK, 2)), F(1, 33)),
    ('Biết có át bích', 'Rút 2 lá, biết trong đó có át bích. P(cả hai là át)?', '1/17', 'cards', 'XS28',
     given(lambda h: h[0][0] == h[1][0] == 0, lambda h: (0, 0) in h, combinations(DECK, 2)), F(1, 17)),
    ('Hai mặt khác nhau', 'Gieo 2 xúc xắc, biết hai mặt khác nhau. P(tổng bằng 7)?', '1/5', 'grid', 'XS20',
     given(lambda w: sum(w) == 7, lambda w: w[0] != w[1], TWO), F(1, 5)),
    ('Ba lá cơ liên tiếp', 'Rút lần lượt 3 lá không hoàn lại. P(cả 3 lá đều là cơ)?', '11/850', 'cards', 'XS22',
     F(13, 52) * F(12, 51) * F(11, 50), F(11, 850)),
    ('Biết tích chẵn', 'Gieo 2 xúc xắc, biết tích hai số chấm là số chẵn. P(tổng là số chẵn)?', '1/3', 'grid', 'XS20',
     given(lambda w: sum(w) % 2 == 0, lambda w: w[0] * w[1] % 2 == 0, TWO), F(1, 3)),
    ('Chỉ một mũi tên trúng', 'A trúng 0,8, B trúng 0,6, mỗi người bắn 1 mũi. Biết bia trúng đúng 1 mũi. P(mũi đó của A)?',
     '8/11', 'tree', 'XS25', F(8, 10) * F(4, 10) / (F(8, 10) * F(4, 10) + F(2, 10) * F(6, 10)), F(8, 11)),
    ('Bia đã bị trúng', 'A trúng 0,8, B trúng 0,6, mỗi người bắn 1 mũi. Biết bia bị trúng. P(cả hai cùng trúng)?', '12/23',
     'tree', 'XS20', F(48, 100) / (1 - F(8, 100)), F(12, 23)),
    ('Người sau trúng thăm', '10 lá thăm có 3 lá trúng, rút lần lượt. Biết người thứ 2 trúng: P(người thứ 1 cũng trúng)?',
     '2/9', 'urn', 'XS20', given(lambda w: w[0][0] == 'W', lambda w: w[1][0] == 'W', permutations(balls(W=3, L=7), 2)),
     F(2, 9)),
    ('Biết tổng chẵn', 'Gieo 2 xúc xắc, biết tổng là số chẵn. P(cả hai mặt đều là 6)?', '1/18', 'grid', 'XS20',
     given(lambda w: w == (6, 6), lambda w: sum(w) % 2 == 0, TWO), F(1, 18)),
    ('Hai lần ngửa liên tiếp', 'Một xu chuẩn, một xu hai mặt ngửa. Chọn 1 đồng, tung 2 lần đều ngửa. P(đã chọn xu chuẩn)?', '1/5',
     'tree', 'XS25', F(1, 8) / (F(1, 8) + F(1, 2)), F(1, 5)),
    ('Ít nhất hai con trai', 'Gia đình 3 con, biết có ít nhất 2 con trai. P(cả 3 đều là trai)?', '1/4', 'tree', 'XS20',
     given(lambda w: w.count('T') == 3, lambda w: w.count('T') >= 2, product('TG', repeat=3)), F(1, 4)),
    ('Đôi một độc lập', 'Tung 2 xu. A: xu 1 ngửa; B: xu 2 ngửa; C: hai xu giống nhau. A, B, C có độc lập (cả ba) không?',
     'Không (chỉ đôi một độc lập)', 'grid', 'XS23', PAIRWISE, (True, False)),
    ('Biết có đúng 3 ngửa', 'Tung xu 5 lần, biết có đúng 3 lần ngửa. P(lần đầu ra ngửa)?', '3/5', 'tree', 'XS20',
     given(lambda w: w[0] == 'N', lambda w: w.count('N') == 3, product('SN', repeat=5)), F(3, 5)),
    ('Biết có bi đỏ', 'Hộp 3 đỏ 2 xanh, rút 2 bi, biết có ít nhất 1 bi đỏ. P(cả hai đỏ)?', '1/3', 'urn', 'XS20',
     given(lambda h: all(b[0] == 'R' for b in h), lambda h: any(b[0] == 'R' for b in h), combinations(balls(R=3, B=2), 2)),
     F(1, 3)),
    ('Hai nhân chứng', 'Sự kiện xảy ra với xác suất 1/2. A nói thật 3/4, B nói thật 4/5, cả hai nói "có". P(thật sự có)?',
     '12/13', 'tree', 'XS27', F(3, 4) * F(4, 5) / (F(3, 4) * F(4, 5) + F(1, 4) * F(1, 5)), F(12, 13)),
    # ---------------- L9 · TOÀN PHẦN – BAYES nâng cao ----------------
    ('Đi học muộn', '40 % đi xe buýt; đi muộn 10 % nếu đi buýt, 5 % nếu tự đi. P(một bạn đi muộn)?', '0,07', 'tree', 'XS24',
     round(.4 * .1 + .6 * .05, 2), .07),
    ('Muộn vì xe buýt?', 'Như trên, biết bạn đó đi muộn. P(bạn đi xe buýt)?', '4/7', 'tree', 'XS25',
     F(4, 100) / F(7, 100), F(4, 7)),
    ('Nhân chứng taxi', '85 % taxi màu xanh lá, 15 % xanh dương; nhân chứng nhận đúng màu 80 %. Nói "xanh dương": P(đúng)?',
     '12/29 ≈ 0,41', 'square', 'XS27', F(15 * 80, 15 * 80 + 85 * 20), F(12, 29)),
    ('Biết hay đoán mò?', 'Học sinh biết đáp án 60 %, không biết thì đoán 1 trong 4. Trả lời đúng: P(thật sự biết)?', '6/7',
     'tree', 'XS25', F(3, 5) / (F(3, 5) + F(2, 5) * F(1, 4)), F(6, 7)),
    ('Dự báo có mưa', 'Ngày mưa 20 %. Mưa thì đài báo mưa 90 %, tạnh vẫn báo mưa 30 %. Đài báo mưa: P(mưa)?', '3/7', 'tree',
     'XS27', F(2, 10) * F(9, 10) / (F(2, 10) * F(9, 10) + F(8, 10) * F(3, 10)), F(3, 7)),
    ('Ba nhà cung cấp', 'Đèn từ 3 nơi: 45 %, 35 %, 20 %; đạt chuẩn 98 %, 96 %, 95 %. P(đèn đạt chuẩn)?', '0,967', 'tree', 'XS26',
     round(.45 * .98 + .35 * .96 + .2 * .95, 3), .967),
    ('Tìm ngược tỉ lệ lỗi', 'Máy A làm 60 % sản phẩm, lỗi 2 %; tỉ lệ lỗi chung là 3 %. Tỉ lệ lỗi của máy B?', '4,5 %', 'tree',
     'XS24', (F(3, 100) - F(6, 10) * F(2, 100)) / F(4, 10), F(45, 1000)),
    ('Hai bi đỏ từ hộp nào?', 'Hộp I: 2 đỏ 3 xanh; hộp II: 3 đỏ 2 xanh. Chọn hộp, rút 2 bi đều đỏ. P(hộp II)?', '3/4', 'tree',
     'XS25', F(comb(3, 2), 10) / (F(comb(3, 2), 10) + F(comb(2, 2), 10)), F(3, 4)),
    ('Tín hiệu bị nhiễu', 'Gửi bit 1 với xác suất 0,3, bit 0 với 0,7; mỗi bit bị lật 10 %. Nhận 1: P(đã gửi 1)?', '27/34',
     'tree', 'XS27', F(3, 10) * F(9, 10) / (F(3, 10) * F(9, 10) + F(7, 10) * F(1, 10)), F(27, 34)),
    ('Gửi lặp hai lần', 'Như trên nhưng gửi mỗi bit 2 lần, nhận được "1 1". P(đã gửi 1)?', '243/250 = 0,972', 'tree', 'XS27',
     F(3, 10) * F(81, 100) / (F(3, 10) * F(81, 100) + F(7, 10) * F(1, 100)), F(243, 250)),
    ('Câu hỏi nhạy cảm', 'Tung xu: ngửa thì trả lời thật "có quay cóp không?", sấp thì nói "có". 60 % nói "có". Tỉ lệ quay cóp?',
     '20 %', 'tree', 'XS24', (F(3, 5) - F(1, 2)) / F(1, 2), F(1, 5)),
    ('Súng tốt hay súng thường?', '3 súng tốt trúng 0,9; 2 súng thường trúng 0,6. Chọn 1 súng, bắn trúng. P(súng tốt)?', '9/13',
     'tree', 'XS26', F(3, 5) * F(9, 10) / (F(3, 5) * F(9, 10) + F(2, 5) * F(6, 10)), F(9, 13)),
    ('Bắn tiếp phát hai', 'Như trên, dùng lại khẩu súng đó bắn phát thứ hai. P(lại trúng)?', '21/26', 'tree', 'XS26',
     F(9, 13) * F(9, 10) + F(4, 13) * F(6, 10), F(21, 26)),
    ('Chuyền bi qua ba hộp', 'Ba hộp đều 1 đỏ 1 xanh. Chuyển 1 bi từ I sang II, 1 bi từ II sang III, rồi rút từ III. P(đỏ)?',
     '1/2', 'tree', 'XS26', chain_transfer(3) * F(2, 3) + (1 - chain_transfer(3)) * F(1, 3), F(1, 2)),
    ('Ba đồng xu bí ẩn', 'Xu chuẩn, xu lệch P(ngửa) = 3/4, xu hai mặt ngửa. Chọn 1 đồng, tung ra ngửa. P(lần sau cũng ngửa)?',
     '29/36', 'tree', 'XS26', (F(1, 4) + F(9, 16) + 1) / (F(1, 2) + F(3, 4) + 1), F(29, 36)),
    # ---------------- L10 · CÂU CHẶN ĐIỂM 8 – 9 – 10 ----------------
    ('Phương trình có nghiệm', 'Gieo xúc xắc 2 lần được b rồi c. P(phương trình x² + bx + c = 0 có nghiệm)?', '19/36', 'grid',
     'XS29', P(lambda w: w[0] ** 2 >= 4 * w[1], TWO), F(19, 36)),
    ('Hai đội mạnh cùng bảng', '8 đội chia ngẫu nhiên thành 2 bảng 4 đội. P(hai đội mạnh nhất cùng bảng)?', '3/7', 'cards',
     'XS10', P(lambda g: (0 in g) == (1 in g), combinations(range(8), 4)), F(3, 7)),
    ('Nữ không đứng cạnh nhau', '5 nam, 5 nữ xếp hàng ngang. P(không có hai bạn nữ nào đứng cạnh nhau)?', '1/42', 'cards',
     'XS12', P(lambda w: 'GG' not in ''.join(w), set(permutations('TTTTTGGGGG'))), F(1, 42)),
    ('Bàn tròn xen kẽ', '4 nam, 4 nữ ngồi ngẫu nhiên quanh bàn tròn. P(nam nữ ngồi xen kẽ)?', '1/35', 'geo', 'XS12',
     P(lambda w: all(('M' + ''.join(w))[i] != ('M' + ''.join(w))[(i + 1) % 8] for i in range(8)), permutations('MMMFFFF')),
     F(1, 35)),
    ('Chữ số tăng dần', 'Chọn ngẫu nhiên một số có 3 chữ số. P(các chữ số tăng dần từ trái sang phải)?', '7/75', 'grid', 'XS08',
     P(lambda n: ordered(str(n)), range(100, 1000)), F(7, 75)),
    ('Ba số lập cấp số cộng', 'Chọn 3 số khác nhau từ 1 đến 20. P(ba số lập thành cấp số cộng)?', '3/38', 'grid', 'XS10',
     P(lambda t: t[1] - t[0] == t[2] - t[1], combinations(range(1, 21), 3)), F(3, 38)),
    ('Ba điểm thẳng hàng', 'Chọn 3 trong 9 điểm của lưới 3 × 3. P(ba điểm thẳng hàng)?', '2/21', 'geo', 'XS07',
     P(lambda t: collinear(*t), combinations(product(range(3), repeat=2), 3)), F(2, 21)),
    ('Ba cạnh tam giác', 'Gieo 3 xúc xắc. P(ba số chấm là độ dài ba cạnh của một tam giác)?', '37/72', 'grid', 'XS09',
     P(lambda w: 2 * max(w) < sum(w), THREE), F(37, 72)),
    ('An rút trước, Bình rút sau', 'Hộp 6 đỏ 4 xanh. An lấy 1 bi, Bình lấy tiếp 2 bi; biết 2 bi của Bình cùng màu. '
     'P(An lấy đỏ)?', '4/7', 'tree', 'XS29',
     given(lambda w: w[0][0] == 'R', lambda w: w[1][0] == w[2][0], permutations(balls(R=6, B=4), 3)), F(4, 7)),
    ('Gặp một bạn nam', '45 % học sinh thích bóng đá; trong đó 60 % là nam, nhóm còn lại 30 % là nam. Gặp bạn nam: '
     'P(thích bóng đá)?', '18/29 ≈ 0,62', 'tree', 'XS29', F(45 * 60, 45 * 60 + 55 * 30), F(18, 29)),
    ('Trúng đủ hai phát thì dừng', 'Bắn đến khi trúng 2 phát thì dừng, mỗi phát trúng 0,6. P(dừng ở phát thứ 4)?', '0,1728',
     'tree', 'XS18', round(3 * .6 * .4 ** 2 * .6, 4), .1728),
    ('Tam giác tù trong 12-giác', 'Chọn 3 đỉnh của đa giác đều 12 cạnh. P(được tam giác tù)?', '6/11', 'geo', 'XS07',
     P(lambda t: polygon_kind(t, 12) == 'tù', combinations(range(12), 3)), F(6, 11)),
    ('Hai số từ 1 đến 100', 'Chọn 2 số khác nhau từ 1 đến 100. P(tích của chúng chia hết cho 3)?', '83/150', 'grid', 'XS29',
     P(lambda t: t[0] * t[1] % 3 == 0, combinations(range(1, 101), 2)), F(83, 150)),
    ('Ngửa nhiều hơn sấp', 'Tung đồng xu 10 lần. P(số lần ngửa nhiều hơn số lần sấp)?', '193/512 ≈ 0,377', 'tree', 'XS18',
     P(lambda w: sum(w) > 5, product((0, 1), repeat=10)), F(193, 512)),
    ('Đoán bừa 10 câu', 'Đề 10 câu, mỗi câu 4 phương án, đoán bừa tất cả. P(đúng ít nhất 5 câu)?', '≈ 0,078', 'curve', 'XS18',
     round(float(sum(comb(10, k) * F(1, 4) ** k * F(3, 4) ** (10 - k) for k in range(5, 11))), 3), .078),
    # ---------------- L11 · HỌC SINH GIỎI: hay, lạ, khó ----------------
    ('Gối của Lewis Carroll', 'Túi có 1 bi, đỏ hoặc trắng (1/2). Bỏ thêm 1 bi đỏ, rút ra được đỏ. P(bi còn lại là đỏ)?', '2/3',
     'tree', 'XS30', given(lambda w: w[1] == 'R', lambda w: w[0] == 'R', [('R', 'R'), ('R', 'R'), ('R', 'W'), ('W', 'R')]),
     F(2, 3)),
    ('Nghịch lý Simpson', 'Thuốc A khỏi 81/87 ca nhẹ, 192/263 ca nặng; B: 234/270 và 55/80. Thuốc nào khỏi chung nhiều hơn?',
     'B (83 % so với 78 %)', 'table', 'XS28',
     (F(81, 87) > F(234, 270), F(192, 263) > F(55, 80), F(81 + 192, 350) < F(234 + 55, 350)), (True, True, True)),
    ('Thêm một đồng xu', 'An tung 4 đồng xu, Bình tung 3 đồng xu. P(An được nhiều mặt ngửa hơn Bình)?', '1/2', 'tree', 'XS30',
     P(lambda w: sum(w[:4]) > sum(w[4:]), product((0, 1), repeat=7)), F(1, 2)),
    ('Viên bi cuối cùng', 'Hộp 5 đỏ 3 xanh, rút lần lượt đến hết. P(viên bi cuối cùng màu xanh)?', '3/8', 'urn', 'XS30',
     P(lambda w: w[-1] == 'B', set(permutations('RRRRRBBB'))), F(3, 8)),
    ('Bước lên cầu thang', 'Mỗi bước lên 1 hoặc 2 bậc với xác suất như nhau. P(chân chạm đúng bậc thứ 4)?', '11/16', 'tree',
     'XS30', P(lambda w: 4 in [sum(w[:k]) for k in range(5)], product((1, 2), repeat=4)), F(11, 16)),
    ('Chọn người giỏi nhất', '3 ứng viên lần lượt. Bỏ qua người đầu, chọn người đầu tiên giỏi hơn mọi người trước. '
     'P(chọn được người giỏi nhất)?', '1/2', 'cards', 'XS30', secretary(3), F(1, 2)),
    ('Chờ hai ngửa liên tiếp', 'Tung đồng xu đến khi có hai lần ngửa liên tiếp. Trung bình cần bao nhiêu lần?', '6', 'sim', 'XS30',
     two_by_two([(F(1, 2), F(-1, 2), 1), (F(-1, 2), 1, 1)])[0], 6),
    ('Loạt luân lưu', 'Mỗi đội sút 5 quả luân lưu, mỗi quả vào 0,75. P(hòa sau 5 lượt)?', '≈ 0,29', 'sim', 'XS30',
     round(float(sum(comb(5, k) ** 2 * F(3, 4) ** (2 * k) * F(1, 4) ** (10 - 2 * k) for k in range(6))), 2), .29),
    ('Giải độc đắc 6/45', 'Chọn 6 số trong 45 số. P(trùng đủ 6 số được quay)?', '1/8 145 060', 'cards', 'XS07',
     F(1, comb(45, 6)), F(1, 8145060)),
    ('Monty Hall 100 cửa', '100 cửa, 1 cửa có xe. Bạn chọn 1, người dẫn mở 98 cửa có dê. Đổi cửa: P(trúng xe)?', '99/100',
     'cards', 'XS28', 1 - F(1, 100), F(99, 100)),
    # ================= NHÁNH 3 · XÁC SUẤT CÓ ĐIỀU KIỆN NÂNG CAO =================
    # ---------------- L12 · BỐC BI ĐA HỘP, NHIỀU GIAI ĐOẠN ----------------
    ('Mỗi hộp một bi', 'Hộp I: 3 đỏ 2 xanh; hộp II: 2 đỏ 4 xanh. Rút mỗi hộp 1 bi. P(hai bi cùng màu)?', '7/15', 'tree', 'XS17',
     F(3, 5) * F(2, 6) + F(2, 5) * F(4, 6), F(7, 15)),
    ('Cùng màu thì màu gì?', 'Như trên, biết hai bi cùng màu. P(cả hai bi đều đỏ)?', '3/7', 'tree', 'XS20',
     F(3, 5) * F(2, 6) / F(7, 15), F(3, 7)),
    ('Ba hộp, đúng hai đỏ', 'Hộp k có k đỏ và 4 − k xanh (k = 1, 2, 3). Rút mỗi hộp 1 bi. P(đúng 2 bi đỏ)?', '13/32', 'tree',
     'XS18', P(lambda w: sum(c == 'R' for c in w) == 2, product('RBBB', 'RRBB', 'RRRB')), F(13, 32)),
    ('Bi đỏ duy nhất từ đâu?', 'Như trên, biết rút được đúng 1 bi đỏ. P(bi đỏ đó từ hộp 3)?', '9/13', 'tree', 'XS25',
     given(lambda w: w[2] == 'R', lambda w: sum(c == 'R' for c in w) == 1, product('RBBB', 'RRBB', 'RRRB')), F(9, 13)),
    ('Tung xu chọn hộp', 'Hộp I: 4 đỏ 1 xanh; hộp II: 1 đỏ 4 xanh. Tung xu chọn hộp, rút 2 bi. P(1 đỏ 1 xanh)?', '2/5', 'tree',
     'XS24', F(1, 2) * F(4, 10) + F(1, 2) * F(4, 10), F(2, 5)),
    ('Bi thứ hai cùng hộp', 'Như trên: rút 1 bi được đỏ, rút tiếp bi thứ hai cùng hộp. P(bi thứ hai cũng đỏ)?', '3/5', 'tree',
     'XS26', F(4, 5) * F(3, 4) + F(1, 5) * 0, F(3, 5)),
    ('Hoàn lại vẫn phụ thuộc', 'Như trên nhưng rút có hoàn lại: lần 1 đỏ. P(lần 2 cũng đỏ)?', '17/25', 'tree', 'XS23',
     (F(1, 2) * F(4, 5) ** 2 + F(1, 2) * F(1, 5) ** 2) / F(1, 2), F(17, 25)),
    ('Xúc xắc chọn hộp, hai bi đỏ', 'Gieo xúc xắc: ra 6 chọn hộp A (5 đỏ 1 xanh), khác 6 chọn hộp B (2 đỏ 4 xanh). '
     'Rút 2 bi đều đỏ. P(hộp A)?', '2/3', 'tree', 'XS25',
     F(1, 6) * F(10, 15) / (F(1, 6) * F(10, 15) + F(5, 6) * F(1, 15)), F(2, 3)),
    ('Luân phiên hai hộp', 'An rút ở hộp I (2 đỏ 3 xanh), Bình ở hộp II (3 đỏ 1 xanh), luân phiên, không hoàn lại; '
     'ai được đỏ trước thắng. P(An thắng)?', '19/40', 'tree', 'XS22',
     F(2, 5) + F(3, 5) * F(1, 4) * F(2, 4), F(19, 40)),
    ('Đến khi đủ hai màu', 'Hộp 3 đỏ 2 xanh, rút lần lượt đến khi có đủ hai màu. P(cần đúng 3 lần)?', '3/10', 'tree', 'XS22',
     P(lambda w: len(set(w[:2])) == 1 and w[2] != w[0], set(permutations('RRRBB'))), F(3, 10)),
    ('Hai bi xanh liền nhau', 'Hộp 4 đỏ 2 xanh, rút lần lượt đến hết. P(hai bi xanh được rút liền nhau)?', '1/3', 'urn', 'XS12',
     P(lambda w: 'BB' in ''.join(w), set(permutations('RRRRBB'))), F(1, 3)),
    ('Đỏ luôn không ít hơn', 'Hộp 3 đỏ 3 xanh, rút lần lượt đến hết. P(mọi lúc số đỏ đã rút ≥ số xanh)?', '1/4', 'urn', 'XS30',
     P(lambda w: all(w[:k].count('R') >= w[:k].count('B') for k in range(7)), set(permutations('RRRBBB'))), F(1, 4)),
    ('Số lớn nhất là 7', 'Rút 3 bi từ 10 bi đánh số 1 đến 10. P(số lớn nhất là 7)?', '1/8', 'urn', 'XS07',
     P(lambda t: max(t) == 7, combinations(range(1, 11), 3)), F(1, 8)),
    ('Nhỏ nhất 3, lớn nhất 7', 'Như trên, biết số nhỏ nhất là 3. P(số lớn nhất là 7)?', '1/7', 'urn', 'XS20',
     given(lambda t: max(t) == 7, lambda t: min(t) == 3, combinations(range(1, 11), 3)), F(1, 7)),
    ('Ba hộp, hai bi khác màu', 'Hộp I: 2 đỏ 2 xanh; II: 3 đỏ 1 xanh; III: 4 đỏ. Chọn hộp, rút 2 bi khác màu. P(hộp I)?', '4/7',
     'tree', 'XS26', F(4, 6) / (F(4, 6) + F(3, 6) + 0), F(4, 7)),
    ('Thêm bi cùng màu', 'Hộp 1 đỏ 1 xanh; rút 1 bi, trả lại kèm 1 bi cùng màu, rút lần 2 được đỏ. P(lần 1 đỏ)?', '2/3', 'tree',
     'XS25', F(1, 2) * F(2, 3) / (F(1, 2) * F(2, 3) + F(1, 2) * F(1, 3)), F(2, 3)),
    # ---------------- L13 · CHUYỂN BI ĐA GIAI ĐOẠN ----------------
    ('Chuyển một, rút hai', 'Hộp I: 3 đỏ 2 xanh; II: 2 đỏ 2 xanh. Chuyển 1 bi từ I sang II, rồi rút 2 bi từ II. P(2 đỏ)?',
     '11/50', 'tree', 'XS24', draw(process(['RRRBB', 'RRBB'], [(0, 1, 1)]), 1, 2, lambda d, h: d == 'RR'), F(11, 50)),
    ('Bi chuyển màu gì?', 'Như trên, biết 2 bi rút từ II đều đỏ. P(bi đã chuyển là đỏ)?', '9/11', 'tree', 'XS25',
     bayes(process(['RRRBB', 'RRBB'], [(0, 1, 1)]), 1, 2, lambda d: d == 'RR', lambda h: h[0] == 'R'), F(9, 11)),
    ('Chuyển đi rồi chuyển về', 'Hộp I: 2 đỏ 1 xanh; II: 1 đỏ 2 xanh. Chuyển 1 bi I → II, rồi 1 bi II → I, rút từ I. P(đỏ)?',
     '7/12', 'tree', 'XS24', draw(process(['RRB', 'RBB'], [(0, 1, 1), (1, 0, 1)]), 0, 1, lambda d, h: d == 'R'), F(7, 12)),
    ('Truy ngược hai lần chuyển', 'Như trên, biết bi rút từ I là đỏ. P(bi chuyển I → II lúc đầu là đỏ)?', '4/7', 'tree', 'XS25',
     bayes(process(['RRB', 'RBB'], [(0, 1, 1), (1, 0, 1)]), 0, 1, lambda d: d == 'R', lambda h: h[0] == 'R'), F(4, 7)),
    ('Chuyển hai, rút hai', 'Hộp I: 3 đỏ 3 xanh; II: 2 đỏ 2 xanh. Chuyển 2 bi I → II, rồi rút 2 bi từ II. P(cùng màu)?',
     '32/75', 'tree', 'XS24', draw(process(['RRRBBB', 'RRBB'], [(0, 1, 2)]), 1, 2, lambda d, h: len(set(d)) == 1), F(32, 75)),
    ('Hai bi chuyển đều đỏ?', 'Như trên, biết 2 bi rút từ II đều đỏ. P(2 bi đã chuyển đều đỏ)?', '3/8', 'tree', 'XS26',
     bayes(process(['RRRBBB', 'RRBB'], [(0, 1, 2)]), 1, 2, lambda d: d == 'RR', lambda h: h[0] == 'RR'), F(3, 8)),
    ('Đổi bi giữa hai hộp', 'Hộp I: 3 đỏ 1 xanh; II: 1 đỏ 3 xanh. Đổi ngẫu nhiên 1 bi của I lấy 1 bi của II, rồi rút từ I. '
     'P(đỏ)?', '5/8', 'tree', 'XS24', draw(process(['RRRB', 'RBBB'], [('swap', 0, 1)]), 0, 1, lambda d, h: d == 'R'),
     F(5, 8)),
    ('Đổi hai lần, về như cũ', 'Như trên, đổi bi 2 lần. P(hộp I lại có đúng 3 đỏ 1 xanh)?', '11/32', 'tree', 'XS24',
     sum(p for p, h, b in process(['RRRB', 'RBBB'], [('swap', 0, 1)] * 2) if sorted(b[0]) == sorted('RRRB')), F(11, 32)),
    ('Đồng xu quyết định số bi', 'Ngửa: chuyển 1 bi, sấp: chuyển 2 bi từ hộp I (3 đỏ 1 xanh) sang II (1 đỏ 1 xanh); '
     'rút 1 bi từ II. P(đỏ)?', '29/48', 'tree', 'XS26',
     F(1, 2) * draw(process(['RRRB', 'RB'], [(0, 1, 1)]), 1, 1, lambda d, h: d == 'R')
     + F(1, 2) * draw(process(['RRRB', 'RB'], [(0, 1, 2)]), 1, 1, lambda d, h: d == 'R'), F(29, 48)),
    ('Bi bị giấu đi', 'Hộp 3 đỏ 2 xanh. Lấy 1 bi cất đi không xem, rồi rút 1 bi. P(bi rút ra đỏ)?', '3/5', 'tree', 'XS28',
     draw(process(['RRRBB', ''], [(0, 1, 1)]), 0, 1, lambda d, h: d == 'R'), F(3, 5)),
    ('Bi giấu màu gì?', 'Như trên, biết bi rút ra đỏ. P(bi đã cất đi cũng đỏ)?', '1/2', 'tree', 'XS25',
     bayes(process(['RRRBB', ''], [(0, 1, 1)]), 0, 1, lambda d: d == 'R', lambda h: h[0] == 'R'), F(1, 2)),
    ('Chuyền qua ba hộp', 'Hộp I: 2 đỏ; II và III: mỗi hộp 1 đỏ 1 xanh. Chuyển 1 bi I → II → III rồi rút từ III. P(đỏ)?',
     '5/9', 'tree', 'XS24', draw(process(['RR', 'RB', 'RB'], [(0, 1, 1), (1, 2, 1)]), 2, 1, lambda d, h: d == 'R'), F(5, 9)),
    ('Hai hộp đổ vào một', 'Lấy 1 bi từ I (2 đỏ 1 xanh) và 1 bi từ II (1 đỏ 2 xanh) bỏ vào III (1 đỏ). Rút từ III. P(đỏ)?',
     '2/3', 'tree', 'XS24', draw(process(['RRB', 'RBB', 'R'], [(0, 2, 1), (1, 2, 1)]), 2, 1, lambda d, h: d == 'R'), F(2, 3)),
    ('Bi từ hộp II đỏ không?', 'Như trên, biết bi rút từ III là đỏ. P(bi lấy từ II là đỏ)?', '4/9', 'tree', 'XS26',
     bayes(process(['RRB', 'RBB', 'R'], [(0, 2, 1), (1, 2, 1)]), 2, 1, lambda d: d == 'R', lambda h: h[1] == 'R'), F(4, 9)),
    ('Chuyển hai vào hộp toàn xanh', 'Chuyển 2 bi từ I (4 đỏ 2 xanh) sang II (2 xanh), rút 1 bi II được đỏ. '
     'P(đúng 1 bi đỏ đã được chuyển)?', '2/5', 'tree', 'XS26',
     bayes(process(['RRRRBB', 'BB'], [(0, 1, 2)]), 1, 1, lambda d: d == 'R', lambda h: h[0] == 'BR'), F(2, 5)),
    ('Đi một vòng trở về', 'Hộp I: 3 đỏ 2 xanh; II: 2 đỏ 3 xanh. Chuyển 1 bi I → II rồi 1 bi II → I. P(hộp I như cũ)?', '17/30',
     'tree', 'XS24',
     sum(p for p, h, b in process(['RRRBB', 'RRBBB'], [(0, 1, 1), (1, 0, 1)]) if sorted(b[0]) == sorted('RRRBB')), F(17, 30)),
    # ---------------- L14 · ĐA ĐIỀU KIỆN, ĐA PHÉP THỬ ----------------
    ('Hai điều kiện cùng lúc', 'Gieo 2 xúc xắc, biết tổng chẵn và có mặt 6. P(tổng ≥ 10)?', '3/5', 'grid', 'XS20',
     given(lambda w: sum(w) >= 10, lambda w: sum(w) % 2 == 0 and 6 in w, TWO), F(3, 5)),
    ('Ngửa đầu và ít nhất hai ngửa', 'Tung xu 3 lần, biết lần 1 ngửa và có ít nhất 2 ngửa. P(cả 3 lần ngửa)?', '1/3', 'tree',
     'XS20', given(lambda w: w.count('N') == 3, lambda w: w[0] == 'N' and w.count('N') >= 2, product('SN', repeat=3)),
     F(1, 3)),
    ('Ai bắn trượt?', 'Ba xạ thủ trúng 0,5; 0,6; 0,7. Biết đúng 2 người trúng. P(người thứ nhất trượt)?', '21/44', 'tree', 'XS25',
     F(21, 100) / (F(21, 100) + F(14, 100) + F(9, 100)), F(21, 44)),
    ('Ít nhất hai người trúng', 'Như trên, biết có ít nhất 2 người trúng. P(cả 3 cùng trúng)?', '21/65', 'tree', 'XS20',
     F(21, 100) / (F(44, 100) + F(21, 100)), F(21, 65)),
    ('Xúc xắc rồi đồng xu', 'Gieo xúc xắc được k chấm rồi tung k đồng xu. P(không có mặt ngửa nào)?', '21/128', 'tree', 'XS24',
     sum(F(1, 6) * F(1, 2) ** k for k in range(1, 7)), F(21, 128)),
    ('Không ngửa nào, xúc xắc ra mấy?', 'Như trên, biết không có mặt ngửa nào. P(xúc xắc ra 1 chấm)?', '32/63', 'tree', 'XS25',
     F(1, 12) / F(21, 128), F(32, 63)),
    ('Gieo đến khi ra 6: không nhớ', 'Gieo đến khi ra 6. Biết cần ít nhất 3 lần. P(cần đúng 4 lần)?', '5/36', 'tree', 'XS20',
     (F(5, 6) ** 3 * F(1, 6)) / F(5, 6) ** 2, F(5, 36)),
    ('Có cả trai lẫn gái', 'Gia đình 4 con, biết có cả trai lẫn gái. P(đúng 2 trai)?', '3/7', 'tree', 'XS20',
     given(lambda w: w.count('T') == 2, lambda w: 0 < w.count('T') < 4, product('TG', repeat=4)), F(3, 7)),
    ('Xu bí ẩn: lần hai', 'Chọn ngẫu nhiên xu chuẩn hoặc xu lệch (ngửa 0,9), tung 2 lần. Lần 1 ngửa: P(lần 2 ngửa)?', '53/70',
     'tree', 'XS23', (F(1, 2) * F(1, 4) + F(1, 2) * F(81, 100)) / (F(1, 2) * F(1, 2) + F(1, 2) * F(9, 10)), F(53, 70)),
    ('Xu bí ẩn: lần ba', 'Như trên, biết 2 lần đầu đều ngửa. P(lần 3 ngửa)?', '427/530 ≈ 0,806', 'tree', 'XS26',
     (F(1, 8) + F(729, 1000)) / (F(1, 4) + F(81, 100)), F(427, 530)),
    ('Bị loại ở vòng nào?', 'Qua vòng 1: 0,8; qua 1 thì qua vòng 2: 0,6; qua 2 thì qua vòng 3: 0,5. Biết bị loại. '
     'P(loại ở vòng 2)?', '8/19', 'tree', 'XS25', F(32, 100) / (F(20, 100) + F(32, 100) + F(24, 100)), F(8, 19)),
    ('Ba mặt khác nhau có 6?', 'Gieo 3 xúc xắc, biết ba mặt khác nhau. P(có mặt 6)?', '1/2', 'grid', 'XS20',
     given(lambda w: 6 in w, lambda w: len(set(w)) == 3, THREE), F(1, 2)),
    ('Có 6 thì khác nhau?', 'Gieo 3 xúc xắc, biết có ít nhất một mặt 6. P(ba mặt khác nhau)?', '60/91', 'grid', 'XS20',
     given(lambda w: len(set(w)) == 3, lambda w: 6 in w, THREE), F(60, 91)),
    ('Ba phát trúng liên tiếp', 'Bắn 5 phát (mỗi phát trúng 0,6), biết trúng đúng 3 phát. P(3 phát trúng liên tiếp)?', '3/10',
     'tree', 'XS18', given(lambda w: '111' in ''.join(map(str, w)), lambda w: sum(w) == 3, product((0, 1), repeat=5)),
     F(3, 10)),
    ('Chọn n rồi chọn m', 'Chọn ngẫu nhiên n từ 1 đến 4, rồi chọn ngẫu nhiên m từ 1 đến n. P(m = 1)?', '25/48', 'tree', 'XS24',
     sum(F(1, 4) * F(1, n) for n in range(1, 5)), F(25, 48)),
    ('Lần ngược hai bước chọn', 'Như trên, biết m = 1. P(n = 1)?', '12/25', 'tree', 'XS25',
     F(1, 4) / F(25, 48), F(12, 25)),
    # ---------------- L15 · BÀI TOÁN CHỨA THAM SỐ: XUÔI – NGƯỢC ----------------
    ('Hộp có bao nhiêu bi?', 'Hộp có n bi, trong đó 3 đỏ. Rút 2 bi, P(2 đỏ) = 1/5. Tìm n.', 'n = 6', 'urn', 'XS07',
     [n for n in range(3, 60) if F(comb(3, 2), comb(n, 2)) == F(1, 5)], [6]),
    ('Hai đáp số cho x', 'Hộp 5 đỏ, x xanh. Rút 2 bi, P(khác màu) = 5/9. Tìm x.', 'x = 4 hoặc x = 5', 'urn', 'XS07',
     [x for x in range(60) if F(5 * x, comb(5 + x, 2)) == F(5, 9)], [4, 5]),
    ('Tìm xác suất bắn trúng', 'Bắn 2 phát độc lập, P(trúng ít nhất 1 phát) = 0,96. Tìm xác suất trúng p mỗi phát.', 'p = 0,8',
     'tree', 'XS17', [F(k, 100) for k in range(101) if (1 - F(k, 100)) ** 2 == F(4, 100)], [F(4, 5)]),
    ('Bắn bao nhiêu phát?', 'Mỗi phát trúng 0,3. Bắn ít nhất bao nhiêu phát để P(trúng ít nhất 1) ≥ 0,95?', '9', 'tree', 'XS18',
     next(n for n in range(1, 50) if 1 - F(7, 10) ** n >= F(95, 100)), 9),
    ('Tỉ lệ bệnh là bao nhiêu?', 'Xét nghiệm nhạy 90 %, dương tính giả 10 %. P(bệnh | dương tính) = 0,5. Tìm tỉ lệ bệnh x.',
     'x = 0,1', 'square', 'XS27',
     [F(k, 100) for k in range(1, 100) if F(9, 10) * F(k, 100) / (F(9, 10) * F(k, 100) + F(1, 10) * (1 - F(k, 100))) == F(1, 2)],
     [F(1, 10)]),
    ('Tìm số bi đỏ hộp II', 'Hộp I: 2 đỏ 3 xanh; II: x đỏ 2 xanh. Chọn hộp ngẫu nhiên rồi rút 1 bi, P(đỏ) = 1/2. Tìm x.', 'x = 3',
     'tree', 'XS24', [x for x in range(60) if F(1, 2) * (F(2, 5) + F(x, x + 2)) == F(1, 2)], [3]),
    ('Tham số sau khi chuyển bi', 'Chuyển 1 bi từ I (3 đỏ 1 xanh) sang II (a đỏ 2 xanh), rút từ II: P(đỏ) = 5/8. Tìm a.', 'a = 3',
     'tree', 'XS24', [a for a in range(60) if F(3, 4) * F(a + 1, a + 3) + F(1, 4) * F(a, a + 3) == F(5, 8)], [3]),
    ('Tìm tay nghề xạ thủ', 'Hai xạ thủ trúng p và 0,8. P(đúng 1 người trúng) = 0,38. Tìm p.', 'p = 0,7', 'tree', 'XS17',
     [F(k, 100) for k in range(101) if F(k, 100) * F(2, 10) + (1 - F(k, 100)) * F(8, 10) == F(38, 100)], [F(7, 10)]),
    ('Điều kiện là một phép hợp', 'A, B độc lập, P(A) = 0,5; P(B) = 0,4. Tính P(A | A ∪ B).', '5/7', 'square', 'XS23',
     F(1, 2) / (1 - F(1, 2) * F(3, 5)), F(5, 7)),
    ('Nhóm có bao nhiêu bạn?', 'n bạn xếp hàng ngang, P(Hà và Lan đứng cạnh nhau) = 1/4. Tìm n.', 'n = 8', 'cards', 'XS12',
     [n for n in range(2, 60) if F(2, n) == F(1, 4)], [8]),
    ('n đỏ, n xanh', 'Hộp n đỏ, n xanh. Rút 2 bi, P(cùng màu) = 4/9. Tìm n.', 'n = 5', 'urn', 'XS07',
     [n for n in range(1, 60) if F(2 * comb(n, 2), comb(2 * n, 2)) == F(4, 9)], [5]),
    ('Đồng xu lệch bao nhiêu?', 'Xu lệch, ngửa với xác suất p > 1/2. Tung 2 lần, P(1 ngửa 1 sấp) = 0,48. Tìm p.', 'p = 0,6',
     'tree', 'XS18', [F(k, 100) for k in range(51, 101) if 2 * F(k, 100) * (1 - F(k, 100)) == F(48, 100)], [F(3, 5)]),
    ('p nào tốt nhất?', 'Xu lệch ngửa p, tung 3 lần. p bằng bao nhiêu thì P(đúng 2 ngửa) lớn nhất?', 'p = 2/3', 'curve', 'XS18',
     max((F(k, 300) for k in range(301)), key=lambda p: 3 * p * p * (1 - p)), F(2, 3)),
    ('Ít nhất bao nhiêu bi đỏ?', 'Hộp n đỏ, 3 xanh. Tìm n nhỏ nhất để P(rút 2 bi đều đỏ) > 1/2.', 'n = 8', 'urn', 'XS07',
     next(n for n in range(2, 60) if F(comb(n, 2), comb(n + 3, 2)) > F(1, 2)), 8),
    ('Đài báo nhầm bao nhiêu?', 'Mưa 30 %; trời mưa thì báo mưa 90 %. P(mưa | báo mưa) = 0,72. Tìm tỉ lệ báo mưa khi trời tạnh.',
     '0,15', 'tree', 'XS27',
     [F(k, 100) for k in range(101) if F(27, 100) / (F(27, 100) + F(7, 10) * F(k, 100)) == F(72, 100)], [F(3, 20)]),
    ('Chọn hộp I với xác suất p', 'Hộp I: 3 đỏ 1 xanh; II: 1 đỏ 3 xanh; chọn I với xác suất p. Rút được đỏ thì P(hộp I) = 0,9. '
     'Tìm p.', 'p = 0,75', 'tree', 'XS25',
     [F(k, 100) for k in range(101) if 3 * F(k, 100) / (3 * F(k, 100) + 1 - F(k, 100)) == F(9, 10)], [F(3, 4)]),
    # ---------------- L16 · CÂY HAY – LẠ – PHỨC TẠP ----------------
    ('Xu lệch hóa công bằng', 'Xu lệch ngửa 0,7. Tung từng cặp: NS thì A, SN thì B, còn lại tung lại. Trung bình mấy cặp?',
     '50/21 ≈ 2,38', 'tree', 'XS30', 1 / (2 * F(7, 10) * F(3, 10)), F(50, 21)),
    ('Trò craps', 'Gieo 2 xúc xắc: 7, 11 thắng; 2, 3, 12 thua; khác thì gieo tiếp đến khi lặp lại số đó (thắng) hoặc ra 7 (thua). '
     'P(thắng)?', '244/495 ≈ 0,493', 'tree', 'XS30',
     F(8, 36) + sum(F(c, 36) * F(c, c + 6) for c in (3, 4, 5, 5, 4, 3)), F(244, 495)),
    ('Con bạc có lợi thế', 'Có 2 đồng, mỗi ván thắng 2/3 (thêm 1 đồng) hoặc thua. Dừng khi có 4 đồng hoặc hết tiền. P(đạt 4)?',
     '4/5', 'tree', 'XS30', (1 - F(1, 2) ** 2) / (1 - F(1, 2) ** 4), F(4, 5)),
    ('Dẫn 2–0 trong loạt 7 ván', 'Thắng 4 ván trước là vô địch, A thắng mỗi ván 0,6 và đang dẫn 2–0. P(A vô địch)?', '≈ 0,913',
     'tree', 'XS30', round(float(sum(comb(1 + k, k) * F(3, 5) ** 2 * F(2, 5) ** k for k in range(4))), 3), .913),
    ('Người dẫn không biết', 'Monty Hall nhưng người dẫn không biết, mở ngẫu nhiên và tình cờ ra dê. Đổi cửa: P(trúng xe)?', '1/2',
     'tree', 'XS28', monty_fall(), F(1, 2)),
    ('Dòng họ tuyệt chủng', 'Mỗi cá thể sinh 0, 1, 2 con với xác suất 1/4, 1/4, 1/2. P(dòng họ từ một cá thể tuyệt chủng)?', '1/2',
     'tree', 'XS30', min(q for q in (F(1, 2), F(1)) if q == F(1, 4) + q / 4 + q * q / 2), F(1, 2)),
    ('Bàn Galton', 'Bi rơi qua 4 hàng đinh, mỗi đinh lệch trái hoặc phải 1/2. P(rơi vào ô chính giữa)?', '3/8', 'tree', 'XS18',
     P(lambda w: sum(w) == 2, product((0, 1), repeat=4)), F(3, 8)),
    ('Hai khâu kiểm tra', 'Hàng lỗi 10 %; mỗi khâu bắt lỗi 90 %, báo nhầm hàng tốt 5 %. Hàng qua cả 2 khâu: P(là hàng lỗi)?',
     '4/3253 ≈ 0,0012', 'tree', 'XS27',
     F(1, 10) * F(1, 100) / (F(1, 10) * F(1, 100) + F(9, 10) * F(95, 100) ** 2), F(4, 3253)),
    ('Nhánh đấu loại trực tiếp', 'A gặp B, C gặp D, thắng vào chung kết. A thắng ai cũng 0,6; các trận khác 1/2. P(C vô địch)?',
     '0,22', 'tree', 'XS22', round(.5 * (.6 * .4 + .4 * .5), 2), .22),
    ('Chuột trong mê cung', 'Chuột chọn ngẫu nhiên 1 trong 3 cửa: cửa 1 ra ngoài sau 2 phút, cửa 2, 3 quay lại sau 3 và 5 phút. '
     'Trung bình bao lâu ra?', '10 phút', 'tree', 'XS30', (F(2) + 3 + 5) / 3 / (1 - F(2, 3)), 10),
    ('Hơn nhau hai ngửa', 'Tung xu đến khi số ngửa hơn số sấp 2 hoặc ngược lại. P(dừng sau đúng 4 lần)?', '1/4', 'tree', 'XS30',
     P(lambda w: w[0] != w[1] and w[2] == w[3], product((0, 1), repeat=4)), F(1, 4)),
    ('Ba người, cùng tháng sinh', '3 người. P(có ít nhất 2 người sinh cùng tháng)?', '17/72', 'tree', 'XS13',
     1 - F(12 * 11 * 10, 12 ** 3), F(17, 72)),
    ('Kiến về đỉnh đối diện', 'Kiến đi ngẫu nhiên trên cạnh hình lập phương. Trung bình bao nhiêu bước tới đỉnh đối diện?', '10',
     'tree', 'XS30', cube_hitting(), 10),
    ('Bốn bạn chuyền bóng', '4 bạn, mỗi lần chuyền bóng ngẫu nhiên cho 1 trong 3 bạn kia. P(sau 4 lần, bóng về người đầu)?',
     '7/27', 'tree', 'XS30', ant(4, 0, lambda v: [u for u in range(4) if u != v])[0], F(7, 27)),
    ('Cậu bé bên cửa sổ', 'Gia đình 2 con; nhìn qua cửa sổ thấy ngẫu nhiên 1 đứa là trai. P(cả hai là trai)?', '1/2', 'tree',
     'XS28', window_boy(), F(1, 2)),
    ('Ba người, ba cơ hội', 'A, B, C lần lượt gieo xúc xắc; A thắng nếu ra 1; B nếu ra 1, 2; C nếu ra 1, 2, 3. P(A thắng)?', '3/13',
     'tree', 'XS30', F(1, 6) / (1 - F(5, 6) * F(4, 6) * F(3, 6)), F(3, 13)),
]


def check(actual, expected):
    if isinstance(expected, float):
        return isclose(float(actual), expected, abs_tol=.006)
    return actual == expected


def build():
    assert len(SHORTS) == 280, len(SHORTS)
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
    plan = {'series': 'Xác Suất 3 Phút – 280 Thử Thách Từ Dễ Đến Học Sinh Giỏi', 'code_prefix': 'XSS',
            'author': 'Thầy Nguyễn Văn Sang', 'format': {'width': 1080, 'height': 1920, 'max_seconds': 180},
            'levels': [{'code': c, 'name': n, 'shorts': list(r), 'length': ln} for c, n, r, ln in LEVELS],
            'shorts': rows}
    Path(__file__).with_name('shorts_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n',
                                                            encoding='utf-8')
    md = ['# DANH SÁCH 280 SHORTS · XÁC SUẤT 3 PHÚT', '',
          '> Sinh tự động từ `shorts_plan.py` (`python shorts_plan.py`). Mọi đáp án đã được máy tính lại bằng liệt kê '
          'vét cạn, phân số chính xác hoặc mô phỏng có seed. Đừng sửa tay file này.', '']
    for code, name, (lo, hi), length in LEVELS:
        md += [f'## {code} · {name} (XSS{lo:03d} – XSS{hi:03d}) · {length}', '',
               '| Mã | Tiêu đề | Đề bài | Đáp án | Hình | Tập đầy đủ |', '| :--- | :--- | :--- | :---: | :---: | :---: |']
        for r in rows[lo - 1:hi]:
            problem = r['problem'].replace('|', '\\|')
            md.append(f"| **{r['code']}** | {r['title']} | {problem} | {r['answer']} | {r['visual']} | {r['xs_episode']} |")
        md.append('')
    Path(__file__).with_name('DANH_SACH_SHORTS.md').write_text('\n'.join(md), encoding='utf-8')
    return rows


if __name__ == '__main__':
    rows = build()
    print(f'XSS_PLAN_OK {len(rows)} shorts, mọi đáp án đã kiểm chứng')

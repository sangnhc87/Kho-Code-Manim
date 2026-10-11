"""XSS091 · Con số 1/e — xác suất không lá thư nào đúng địa chỉ dần tới 1/e ≈ 0,368."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import e, factorial
from pathlib import Path

from manim import FadeIn, RIGHT, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT, WHITE  # noqa: E402

EPISODE = {'code': 'XSS091', 'answer': '1/e ≈ 0,368'}
PROBLEM = ['$n$ lá thư bỏ ngẫu nhiên vào $n$ phong',
           'bì. Khi $n$ rất lớn, xác suất KHÔNG lá',
           'nào đúng địa chỉ tiến về đâu?']
OPTIONS = ['0', '1/e approx "0,368"', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / e


def p_der(n):
    return sum(F((-1) ** k, factorial(k)) for k in range(n + 1))


BEATS = [
    Beat('hook', 'hook', 'Thử thách trước, với bốn lá thư, xác suất không lá nào đúng địa chỉ là ba phần tám. '
                         'Nếu có một nghìn, một triệu lá thư thì sao? Nhiều thư như vậy, chắc phải có lá trúng chứ?'),
    Beat('guess', 'hook', 'Dần về không, khoảng không phẩy ba sáu tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tính lần lượt: một lá thư, xác suất bằng không. Hai lá, một phần hai. Ba lá, một phần ba. '
                        'Bốn lá, ba phần tám. Năm lá, khoảng không phẩy ba sáu bảy.'),
    Beat('s2', 'solve', 'Các con số dao động rồi đứng yên rất nhanh ở khoảng không phẩy ba sáu tám. '
                        'Bao hàm loại trừ cho công thức: một trừ một cộng một phần hai giai thừa trừ một phần ba giai thừa, cứ thế.'),
    Beat('s3', 'solve', 'Tổng xen dấu đó chính là khai triển của một chia e, với e là hằng số Euler, khoảng hai phẩy bảy một tám. '
                        'Vậy xác suất tiến về một chia e, khoảng ba mươi bảy phần trăm, dù có bao nhiêu lá thư.'),
    Beat('answer', 'solve', 'Đáp án: một chia e. Hằng số e của giải tích xuất hiện ngay trong một bài toán đếm phong bì, '
                            'một trong những kết quả đẹp nhất của xác suất!'),
    Beat('outro', 'outro', outro_text(91)),
]

FORMULAS = formulas('1/e approx "0,368"', OPTIONS,
                    series='P_n = 1 - 1/(1!) + 1/(2!) - 1/(3!) + dots + (-1)^n/(n!)',
                    limit='P_n arrow.r 1/e approx "0,368"')


def validate() -> bool:
    for n in range(1, 7):
        der = sum(all(p[i] != i for i in range(n)) for p in permutations(range(n)))
        assert F(der, factorial(n)) == p_der(n)
    assert p_der(4) == F(3, 8) and abs(float(p_der(12)) - 1 / e) < 1e-9
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS091(ShortScene):
    N = 91

    def hook_visual(self, t0):
        self.board_top = -1.2

    def beat_s1(self, T):
        t0 = self.now()
        rows = VGroup()
        for n in range(1, 9):
            rows.add(VGroup(self.TM(f'$n = {n}$:', 26, SOFT), self.MNum(float(p_der(n)), 4, WHITE if n < 6 else GOLD, 30))
                     .arrange(buff=.3))
        rows.arrange_in_grid(4, 2, buff=(.8, .22), flow_order='dr').move_to([0, 1.5, 0])
        self.rows = rows
        for i, r in enumerate(rows[:5]):
            self.wait_until(.08 + .17 * i, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows[5:], lag_ratio=.3), run_time=self.rt(.15))
        self.play(*[r[1].animate.set_color(GOLD) for r in self.rows[4:]], run_time=self.rt(.04))
        self.wait_until(.5, t0)
        self.write_board(self.M('series', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        m = self.M('limit', 2.1)
        self.write_board(m)
        self.frame(m)
        self.write_board(tx('e ≈ 2,718: hằng số Euler', 26, CYAN), anim='fade')

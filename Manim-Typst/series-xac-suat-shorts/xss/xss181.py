"""XSS181 · Ba số lập cấp số cộng — chọn hai số cùng tính chẵn lẻ làm hai đầu: 2·C(10,2)/C(20,3) = 3/38."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS181', 'answer': '3/38'}
PROBLEM = ['Chọn ngẫu nhiên $3$ số khác nhau',
           'từ $1$ đến $20$. Xác suất ba số đó',
           'lập thành cấp số cộng?']
OPTIONS = ['1/19', '3/38', '9/76']
CORRECT = 1
ANSWER_VALUE = 3 / 38

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba số khác nhau từ một đến hai mươi. Xác suất ba số đó, xếp theo thứ tự, '
                         'lập thành một cấp số cộng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười chín, ba phần ba mươi tám, hay chín phần bảy mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba số a, b, c lập cấp số cộng khi b là trung bình cộng của a và c. '
                        'Vậy chỉ cần chọn hai đầu a và c sao cho a cộng c chẵn, số giữa tự động được xác định.'),
    Beat('s2', 'solve', 'a cộng c chẵn khi hai số cùng chẵn hoặc cùng lẻ. Từ một đến hai mươi có mười số chẵn, mười số lẻ: '
                        'tổ hợp chập hai của mười, nhân hai, bằng chín mươi bộ.'),
    Beat('s3', 'solve', 'Không gian mẫu có tổ hợp chập ba của hai mươi, một nghìn một trăm bốn mươi. '
                        'Xác suất chín mươi phần một nghìn một trăm bốn mươi, tức ba phần ba mươi tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần ba mươi tám. Đếm cấp số cộng qua hai số đầu cuối cùng tính chẵn lẻ, nhanh và không sót!'),
    Beat('outro', 'outro', outro_text(181)),
]

FORMULAS = formulas('3/38', OPTIONS,
                    mid='b = (a + c)/2 arrow.l.r.double a + c " chẵn"',
                    cnt='n(A) = 2 C_10^2 = 90',
                    prob='P = 90/(C_20^3) = 90/1140 = 3/38')


def validate() -> bool:
    good = sum(t[1] - t[0] == t[2] - t[1] for t in combinations(range(1, 21), 3))
    assert good == 90 == 2 * comb(10, 2) and F(good, comb(20, 3)) == F(3, 38)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS181(ShortScene):
    N = 181

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.nums = VGroup(*[token(str(k), CYAN if k % 2 == 0 else CORAL, .3, 18) for k in range(1, 21)]) \
            .arrange_in_grid(4, 5, buff=.25).move_to([0, 1.3, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.nums, lag_ratio=.03), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        pick = [self.nums[k - 1] for k in (3, 8, 13)]
        self.play(*[p[0].animate.set_stroke(GOLD, 6) for p in pick], *[p.animate.scale(1.2) for p in pick], run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.M('mid', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('cnt', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

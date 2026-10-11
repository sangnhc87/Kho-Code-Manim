"""XSS213 · Số lớn nhất là 7 — chọn 7 và 2 số từ 1..6: C(6,2)/C(10,3) = 15/120 = 1/8."""
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

EPISODE = {'code': 'XSS213', 'answer': '1/8'}
PROBLEM = ['Rút ngẫu nhiên $3$ bi từ $10$ bi đánh',
           'số $1$ đến $10$. Xác suất số lớn nhất',
           'trong ba bi là $7$?']
OPTIONS = ['1/10', '1/8', '3/10']
CORRECT = 1
ANSWER_VALUE = 1 / 8

BEATS = [
    Beat('hook', 'hook', 'Mười viên bi đánh số từ một đến mười. Rút ngẫu nhiên ba viên. Xác suất số lớn nhất trong ba viên đúng bằng bảy là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười, một phần tám, hay ba phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Số lớn nhất là bảy nghĩa là: viên số bảy có mặt, và hai viên còn lại đều nhỏ hơn bảy. Các số tám, chín, mười bị loại.'),
    Beat('s2', 'solve', 'Hai viên còn lại chọn từ một đến sáu: tổ hợp chập hai của sáu, mười lăm cách. '
                        'Không gian mẫu: tổ hợp chập ba của mười, một trăm hai mươi.'),
    Beat('s3', 'solve', 'Xác suất mười lăm phần một trăm hai mươi, tức một phần tám. Thử thách tiếp: thêm điều kiện số nhỏ nhất bằng ba.'),
    Beat('answer', 'solve', 'Đáp án: một phần tám. Bài "lớn nhất bằng k": chốt k, chọn phần còn lại từ các số nhỏ hơn!'),
    Beat('outro', 'outro', outro_text(213)),
]

FORMULAS = formulas('1/8', OPTIONS,
                    cnt='n(A) = C_6^2 = 15, quad n(Omega) = C_10^3 = 120',
                    prob='P = 15/120 = 1/8')


def validate() -> bool:
    t = list(combinations(range(1, 11), 3))
    assert F(sum(max(x) == 7 for x in t), len(t)) == F(1, 8) == F(comb(6, 2), comb(10, 3))
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS213(ShortScene):
    N = 213

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.nums = VGroup(*[token(str(k), CYAN, .32, 22) for k in range(1, 11)]).arrange_in_grid(2, 5, buff=.35) \
            .move_to([0, 1.7, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.nums, lag_ratio=.08), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.nums[6].animate.scale(1.3), self.nums[6][0].animate.set_fill(GOLD), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(*[self.nums[k].animate.set_opacity(.15) for k in (7, 8, 9)], run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[self.nums[k][0].animate.set_fill(CORAL) for k in range(6)], run_time=self.rt(.05))
        self.wait_until(.35, t0)
        self.write_board(self.M('cnt', 1.6))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)



"""XSS214 · Nhỏ nhất 3, lớn nhất 7 — biết min = 3: C(7,2) = 21 bộ; thêm max = 7: 3 bộ: 1/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS214', 'answer': '1/7'}
PROBLEM = ['Rút $3$ bi từ $10$ bi số $1$ đến $10$,',
           'biết số nhỏ nhất là $3$. Xác suất',
           'số lớn nhất là $7$?']
OPTIONS = ['1/8', '1/7', '1/5']
CORRECT = 1
ANSWER_VALUE = 1 / 7

BEATS = [
    Beat('hook', 'hook', 'Vẫn mười viên bi số một đến mười, rút ba viên. Bạn được biết số nhỏ nhất là ba. '
                         'Biết điều đó, xác suất số lớn nhất là bảy là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tám, một phần bảy, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện số nhỏ nhất là ba: có viên số ba, hai viên còn lại lớn hơn ba, chọn từ bốn đến mười: '
                        'tổ hợp chập hai của bảy, hai mươi mốt bộ.'),
    Beat('s2', 'solve', 'Thêm số lớn nhất là bảy: có viên số bảy, viên giữa chọn từ bốn, năm, sáu: ba bộ.'),
    Beat('s3', 'solve', 'Xác suất ba phần hai mươi mốt, tức một phần bảy. Hai điều kiện cùng lúc kẹp số còn lại vào một khoảng hẹp.'),
    Beat('answer', 'solve', 'Đáp án: một phần bảy. Đa điều kiện trên số: mỗi điều kiện chốt một số và thu hẹp phạm vi của các số khác!'),
    Beat('outro', 'outro', outro_text(214)),
]

FORMULAS = formulas('1/7', OPTIONS,
                    nb='n(B) = C_7^2 = 21',
                    nab='n(A sect B) = 3',
                    prob='P(A | B) = 3/21 = 1/7')


def validate() -> bool:
    b = [t for t in combinations(range(1, 11), 3) if min(t) == 3]
    assert len(b) == comb(7, 2) and F(sum(max(t) == 7 for t in b), len(b)) == F(1, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS214(ShortScene):
    N = 214

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.nums = VGroup(*[token(str(k), CYAN, .32, 22) for k in range(1, 11)]).arrange_in_grid(2, 5, buff=.35) \
            .move_to([0, 1.7, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.nums, lag_ratio=.08), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.nums[2][0].animate.set_fill(GOLD), self.nums[2].animate.scale(1.3), run_time=self.rt(.05))
        self.play(*[self.nums[k].animate.set_opacity(.15) for k in (0, 1)], run_time=self.rt(.04))
        self.wait_until(.5, t0)
        self.write_board(self.M('nb', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.nums[6][0].animate.set_fill(GREEN), self.nums[6].animate.scale(1.3), run_time=self.rt(.05))
        self.play(*[self.nums[k].animate.set_opacity(.15) for k in (7, 8, 9)],
                  *[self.nums[k][0].animate.set_fill(CORAL) for k in (3, 4, 5)], run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.write_board(self.M('nab', 2.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

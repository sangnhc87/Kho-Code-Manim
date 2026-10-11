"""XSS066 · Lần hai cũng như lần một — P(bi thứ 2 đỏ) = 5/8·4/7 + 3/8·5/7 = 5/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import DOWN, FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from xss.xss065 import BALLS, BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS066', 'answer': '5/8'}
PROBLEM = ['Hộp $5$ bi đỏ, $3$ bi xanh. Rút lần lượt $2$ bi', 'không hoàn lại. Xác suất bi THỨ HAI là đỏ?']
OPTIONS = ['4/7', '5/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 5 / 8

BEATS = [
    Beat('hook', 'hook', 'Vẫn hộp năm đỏ, ba xanh, rút lần lượt hai viên không hoàn lại. '
                         'Lần này hỏi: xác suất viên thứ hai là đỏ bằng bao nhiêu? Viên thứ nhất đã lấy mất một viên rồi!'),
    Beat('guess', 'hook', 'Bốn phần bảy, năm phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Viên thứ hai đỏ xảy ra theo hai nhánh: đỏ rồi đỏ, hoặc xanh rồi đỏ. '
                        'Nhánh đỏ đỏ: năm phần tám nhân bốn phần bảy, bằng hai mươi phần năm mươi sáu.'),
    Beat('s2', 'solve', 'Nhánh xanh đỏ: ba phần tám nhân năm phần bảy, bằng mười lăm phần năm mươi sáu. '
                        'Cộng hai nhánh: ba mươi lăm phần năm mươi sáu, rút gọn còn năm phần tám.'),
    Beat('s3', 'solve', 'Đúng bằng xác suất viên thứ nhất đỏ! Khi chưa biết lần một ra gì, mọi lượt rút đều công bằng như nhau. '
                        'Đây là công thức xác suất toàn phần.'),
    Beat('answer', 'solve', 'Đáp án: năm phần tám. Rút trước hay rút sau, nếu không ai nhìn thấy, cơ hội như nhau!'),
    Beat('outro', 'outro', outro_text(66)),
]

FORMULAS = formulas('5/8', OPTIONS,
                    rr='5/8 dot 4/7 = 20/56',
                    br='3/8 dot 5/7 = 15/56',
                    tot='P = 20/56 + 15/56 = 35/56 = 5/8')


def validate() -> bool:
    perms = list(permutations(range(8), 2))
    assert F(sum(BALLS[b] == 'R' for _, b in perms), len(perms)) == F(5, 8) == F(5, 8) * F(4, 7) + F(3, 8) * F(5, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS066(TreeMixin, ShortScene):
    N = 66

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='rút')
        self.wait_until(.55, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.write_board(self.M('rr', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('br', 2.0))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('tot', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(tx('= P(viên thứ nhất đỏ)', 30, GOLD, bold=True), anim='fade')
        self.play(FadeIn(tx('toàn phần', 24, SOFT).next_to(self.board_items[-1], DOWN, buff=.15)), run_time=self.rt(.03))

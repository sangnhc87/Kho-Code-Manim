"""XSS362 · Toàn đỏ thì xúc xắc ra mấy? — P(k = 1 | đều đỏ) = (1/6 · 4/7)/(1/6) = 4/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, SurroundingRectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from xss._dicetree import ALLRED, BRANCHES, TOTAL  # noqa: E402

EPISODE = {'code': 'XSS362', 'answer': '4/7'}
PROBLEM = ['Gieo xúc xắc được $k$, rút $k$ bi từ hộp',
           '$4$ đỏ $3$ xanh. Biết $k$ bi đều đỏ. Xác',
           'suất xúc xắc ra $1$?']
OPTIONS = ['1/6', '4/7', '1/2']
CORRECT = 1
ANSWER_VALUE = 4 / 7

BEATS = [
    Beat('hook', 'hook', 'Tiếp bài trước: gieo xúc xắc được k, rút k bi từ hộp bốn đỏ ba xanh. Biết các bi rút ra đều đỏ. '
                         'Xác suất xúc xắc đã ra mặt một là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, bốn phần bảy, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Từ bài trước, xác suất toàn đỏ bằng một phần sáu: đó là mẫu số của công thức Bayes.'),
    Beat('s2', 'solve', 'Nhánh xúc xắc ra một rồi rút một bi đỏ: một phần sáu nhân bốn phần bảy.'),
    Beat('s3', 'solve', 'Chia cho một phần sáu, được bốn phần bảy. Rút được toàn đỏ là dấu hiệu mạnh rằng chỉ rút rất ít bi.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy. Từ một phần sáu ban đầu, niềm tin vọt lên hơn một nửa.'),
    Beat('outro', 'outro', outro_text(362)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    tot='P("đều đỏ") = 1/6',
                    num='P(k = 1, "đỏ") = 1/6 dot 4/7',
                    prob='P(k = 1 | "đều đỏ") = (1/6 dot 4/7)/(1/6) = 4/7')


def validate() -> bool:
    assert F(1, 6) * ALLRED[1] / TOTAL == F(4, 7)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS362(TreeMixin, ShortScene):
    N = 362

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=7.4, r=.3, edge_size=24)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), FadeIn(self.levels[2]), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('tot', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(SurroundingRectangle(self.leaves[0][0], color=GOLD, buff=.08)), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.write_board(self.M('num', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

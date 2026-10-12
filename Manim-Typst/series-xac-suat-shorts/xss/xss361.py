"""XSS361 · Xúc xắc quyết định số bi — P(k bi đều đỏ) = (1/6)(4/7 + 2/7 + 4/35 + 1/35 + 0 + 0) = (1/6)·1 = 1/6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from xss._dicetree import ALLRED, BRANCHES, TOTAL  # noqa: E402

EPISODE = {'code': 'XSS361', 'answer': '1/6'}
PROBLEM = ['Gieo xúc xắc được $k$, rồi rút $k$ bi từ hộp',
           '$4$ đỏ $3$ xanh. Xác suất $k$ bi rút ra đều',
           'là bi đỏ?']
OPTIONS = ['1/6', '1/7', '2/7']
CORRECT = 0
ANSWER_VALUE = 1 / 6

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc được số k, rồi rút k bi từ hộp có bốn đỏ ba xanh. '
                         'Xác suất tất cả k bi rút ra đều đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần bảy, hay hai phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một: xúc xắc ra k với xác suất một phần sáu. Tầng hai: rút k bi đều đỏ, bằng tổ hợp chập k của bốn chia tổ hợp chập k của bảy.'),
    Beat('s2', 'solve', 'Với k bằng một đến bốn: bốn phần bảy, hai phần bảy, bốn phần ba mươi lăm, một phần ba mươi lăm. Với năm và sáu bằng không, vì chỉ có bốn bi đỏ.'),
    Beat('s3', 'solve', 'Bốn nhánh cộng lại vừa đúng bằng một! Nhân với một phần sáu, xác suất bằng một phần sáu.'),
    Beat('answer', 'solve', 'Đáp án: một phần sáu. Hai hành động nối tiếp: hành động trước quyết định luật của hành động sau.'),
    Beat('outro', 'outro', outro_text(361)),
]

FORMULAS = formulas('1/6', OPTIONS,
                    leaf='P(Đ | k) = (C_4^k)/(C_7^k)',
                    vals='4/7 + 2/7 + 4/35 + 1/35 = 1',
                    prob='P = 1/6 dot 1 = 1/6')


def validate() -> bool:
    assert sum(ALLRED[k] for k in range(1, 5)) == 1 and TOTAL == F(1, 6)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS361(TreeMixin, ShortScene):
    N = 361

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=7.4, r=.3, edge_size=24)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.15), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('leaf', 1.5))

    def beat_s2(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))

    def beat_s3(self, T):
        self.clear_board(.03)
        self.write_board(self.M('vals', 1.4))
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

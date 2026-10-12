"""XSS376 · Ra 6 được gieo thêm — chẵn: lần đầu 2 hoặc 4 (1/3), hoặc 6 rồi thêm số chẵn (1/6 · 1/2); P(đầu 6 | chẵn) = (1/12)/(5/12) = 1/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402

EPISODE = {'code': 'XSS376', 'answer': '1/5'}
PROBLEM = ['Gieo xúc xắc; ra $6$ thì gieo thêm $1$ lần',
           'và cộng điểm. Biết tổng điểm chẵn. Xác',
           'suất lần đầu ra $6$?']
OPTIONS = ['1/6', '1/5', '1/4']
CORRECT = 1
ANSWER_VALUE = .2
BRANCHES = [('1–5', CYAN, '5/6', [('C', GREEN, '2/5', [])]), ('6', CORAL, '1/6', [('C', GREEN, '1/2', [])])]


def even():
    a = F(sum(k % 2 == 0 for k in range(1, 6)), 6)
    b = F(1, 6) * F(sum((6 + k) % 2 == 0 for k in range(1, 7)), 6)
    return a, b


BEATS = [
    Beat('hook', 'hook', 'Gieo một xúc xắc. Nếu ra sáu thì được gieo thêm một lần và cộng điểm. Biết tổng điểm là số chẵn. '
                         'Xác suất lần đầu đã ra sáu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần năm, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh lần đầu không ra sáu, năm phần sáu: tổng chính là số đó, chẵn khi ra hai hoặc bốn, hai phần năm.'),
    Beat('s2', 'solve', 'Nhánh ra sáu, một phần sáu: tổng sáu cộng k chẵn khi lần thêm ra số chẵn, một phần hai. Lá này bằng một phần mười hai.'),
    Beat('s3', 'solve', 'Tổng chẵn: một phần ba cộng một phần mười hai, bằng năm phần mười hai. Xác suất một phần mười hai chia năm phần mười hai, bằng một phần năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Hành động thứ hai chỉ xảy ra ở một nhánh: cây lệch vẫn dùng Bayes như thường.'),
    Beat('outro', 'outro', outro_text(376)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    a='5/6 dot 2/5 = 1/3',
                    b='1/6 dot 1/2 = 1/12',
                    prob='P = (1/12)/(1/3 + 1/12) = 1/5')


def validate() -> bool:
    a, b = even()
    assert (a, b) == (F(1, 3), F(1, 12)) and b / (a + b) == F(1, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS376(TreeMixin, ShortScene):
    N = 376

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.0, r=.42)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('a', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('b', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

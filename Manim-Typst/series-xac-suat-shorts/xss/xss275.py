"""XSS275 · Hơn nhau hai ngửa — sau mỗi cặp tung: NN/SS kết thúc (1/2), NS/SN về hòa: dừng ở lần 4 = 1/2·1/2 = 1/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS275', 'answer': '1/4'}
PROBLEM = ['Tung xu đến khi số ngửa hơn số sấp',
           '$2$ đơn vị hoặc ngược lại. Xác suất',
           'dừng sau đúng $4$ lần tung?']
OPTIONS = ['1/8', '1/4', '3/8']
CORRECT = 1
ANSWER_VALUE = .25
BRANCHES = [('dừng', GREEN, '1/2', []),
            ('hòa', SOFT, '1/2', [('dừng', GOLD, '1/2', []), ('hòa', SOFT, '1/2', [])])]


def stop_at(k):
    good = 0
    for w in product((1, -1), repeat=k):
        s, t = 0, None
        for i, x in enumerate(w, 1):
            s += x
            if abs(s) == 2:
                t = i
                break
        good += t == k
    return F(good, 2 ** k)


BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu liên tục, đếm hiệu số ngửa trừ sấp. Dừng khi hiệu bằng cộng hai hoặc trừ hai. '
                         'Xác suất dừng sau đúng bốn lần tung là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tám, một phần tư, hay ba phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo: nhìn từng cặp tung. Bắt đầu hiệu bằng không. Sau hai lần, hai ngửa hoặc hai sấp thì hiệu bằng cộng trừ hai, dừng; '
                        'một ngửa một sấp thì về không, như lúc đầu.'),
    Beat('s2', 'solve', 'Vậy mỗi cặp tung là một vòng: dừng một phần hai, lặp lại một phần hai. Không thể dừng sau số lẻ lần tung.'),
    Beat('s3', 'solve', 'Dừng sau đúng bốn lần: cặp đầu hòa, cặp hai dừng: một phần hai nhân một phần hai, bằng một phần tư.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Gộp hai lần tung thành một bước, cây vô hạn trở nên đơn giản như tung đồng xu!'),
    Beat('outro', 'outro', outro_text(275)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    step='P("dừng sau 1 cặp") = P(N N) + P(S S) = 1/2',
                    prob='P("dừng ở lần 4") = 1/2 dot 1/2 = 1/4')


def validate() -> bool:
    assert stop_at(2) == F(1, 2) and stop_at(3) == 0 and stop_at(4) == F(1, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS275(TreeMixin, ShortScene):
    N = 275

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.6, width=5.6, root_label='hiệu = 0', r=.46)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.03))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.4, t0)
        self.write_board(self.M('step', 1.6))

    def beat_s3(self, T):
        self.clear_board(.03)
        self.play(self.leaves[1][0].animate.scale(1.35), run_time=self.rt(.05))
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m, CORAL)

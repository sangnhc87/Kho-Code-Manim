"""XSS279 · Cậu bé bên cửa sổ — thấy ngẫu nhiên 1 đứa là trai: (1/4·1)/(1/4·1 + 1/2·1/2) = 1/2 (khác 1/3!)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS279', 'answer': '1/2'}
PROBLEM = ['Gia đình có $2$ con. Nhìn qua cửa sổ, bạn',
           'thấy ngẫu nhiên $1$ đứa và đó là con trai.',
           'Xác suất cả hai con đều là trai?']
OPTIONS = ['1/3', '1/2', '1/4']
CORRECT = 1
ANSWER_VALUE = .5
BRANCHES = [('TT', CYAN, '1/4', [('T', GOLD, '1', [])]),
            ('TG', SOFT, '1/2', [('T', GOLD, '1/2', []), ('G', CORAL, '1/2', [])]),
            ('GG', CORAL, '1/4', [('G', CORAL, '1', [])])]


def window():
    num = den = F(0)
    for kids in product('TG', repeat=2):
        for seen in kids:
            pr = F(1, 4) * F(1, 2)
            if seen == 'T':
                den += pr
                num += pr * (kids == ('T', 'T'))
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Ở thử thách cũ: biết gia đình hai con có ít nhất một con trai, xác suất hai trai là một phần ba. '
                         'Lần này bạn nhìn qua cửa sổ, thấy ngẫu nhiên một đứa trẻ, đó là con trai. Xác suất hai con đều là trai có còn là một phần ba?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một là gia đình: hai trai một phần tư, một trai một gái một phần hai, hai gái một phần tư. '
                        'Tầng hai là đứa trẻ bạn tình cờ nhìn thấy.'),
    Beat('s2', 'solve', 'Gia đình hai trai: chắc chắn thấy trai. Gia đình trai gái: chỉ một nửa khả năng thấy đứa trai. Hai lá "thấy trai": một phần tư và một phần tư.'),
    Beat('s3', 'solve', 'Bayes: một phần tư chia một phần hai, bằng một phần hai, khác hẳn một phần ba! '
                        'Cách thông tin đến với ta, hỏi thăm hay tình cờ nhìn thấy, làm thay đổi xác suất.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Trong xác suất có điều kiện, phải hỏi: thông tin này được tạo ra như thế nào?'),
    Beat('outro', 'outro', outro_text(279)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    leaves='1/4 dot 1 = 1/4, quad 1/2 dot 1/2 = 1/4',
                    prob='P(T T | "thấy T") = (1/4)/(1/4 + 1/4) = 1/2 eq.not 1/3')


def validate() -> bool:
    assert window() == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS279(TreeMixin, ShortScene):
    N = 279

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.6, width=7.2, root_label='gia đình', r=.42,
                                                  edge_size=26)
        self.wait_until(.85, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.03))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        boys = [n for n, path in self.leaves if path[-1][0] == 'T' and len(path) == 2]
        girls = [n for n, path in self.leaves if not (path[-1][0] == 'T' and len(path) == 2)]
        self.play(*[n.animate.set_opacity(.15) for n in girls], *[n.animate.scale(1.25) for n in boys], run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.write_board(self.M('leaves', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)
        self.play(FadeIn(tx('cách biết thông tin quyết định!', 24, GREEN).move_to([0, -3.3, 0])), run_time=self.rt(.04))

"""XSS155 · Hai lần ngửa liên tiếp — xu chuẩn NN 1/4, xu hai mặt ngửa NN 1: (1/8)/(1/8 + 1/2) = 1/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS155', 'answer': '1/5'}
PROBLEM = ['Một xu chuẩn, một xu hai mặt ngửa. Chọn',
           'ngẫu nhiên $1$ đồng, tung $2$ lần đều ngửa.',
           'Xác suất đã chọn xu chuẩn?']
OPTIONS = ['1/2', '1/5', '1/3']
CORRECT = 1
ANSWER_VALUE = .2
BRANCHES = [('C', CYAN, '1/2', [('NN', GOLD, '1/4', []), ('khác', SOFT, '3/4', [])]),
            ('G', CORAL, '1/2', [('NN', GOLD, '1', [])])]

BEATS = [
    Beat('hook', 'hook', 'Trong túi có một đồng xu chuẩn và một đồng xu gian có hai mặt đều là ngửa. '
                         'Bạn chọn ngẫu nhiên một đồng, tung hai lần, cả hai lần đều ngửa. Xác suất bạn đang cầm đồng xu chuẩn là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần năm, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây hai tầng: chọn xu chuẩn hay xu gian, mỗi loại một phần hai. Xu chuẩn cho hai ngửa với xác suất một phần tư, '
                        'xu gian thì chắc chắn.'),
    Beat('s2', 'solve', 'Lá chuẩn rồi hai ngửa: một phần tám. Lá gian rồi hai ngửa: một phần hai. Tổng xác suất hai ngửa là năm phần tám.'),
    Beat('s3', 'solve', 'Xác suất xu chuẩn bằng một phần tám chia năm phần tám, tức một phần năm. '
                        'Mỗi lần ra ngửa nữa, niềm tin vào xu chuẩn lại giảm một nửa.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Bằng chứng lặp lại làm thay đổi niềm tin rất nhanh!'),
    Beat('outro', 'outro', outro_text(155)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    leaves='1/2 dot 1/4 = 1/8, quad 1/2 dot 1 = 1/2',
                    prob='P(C | N N) = (1/8)/(1/8 + 1/2) = 1/5')


def validate() -> bool:
    assert F(1, 8) / (F(1, 8) + F(1, 2)) == F(1, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS155(TreeMixin, ShortScene):
    N = 155

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.coins = VGroup(VGroup(coin('N', .6), coin('S', .6)).arrange(buff=.15),
                            VGroup(coin('N', .6), coin('N', .6)).arrange(buff=.15)).arrange(buff=1.4).move_to([0, 1.5, 0])
        self.labs = VGroup(tx('xu chuẩn', 24, CYAN).next_to(self.coins[0], [0, -1, 0]),
                           tx('xu gian', 24, CORAL).next_to(self.coins[1], [0, -1, 0]))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.coins), FadeIn(self.labs), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.coins.animate.set_opacity(0), self.labs.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.coins, self.labs)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.4, root_label='chọn xu')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.12))
        self.play(FadeIn(tx('C: chuẩn   G: gian', 22, SOFT).move_to([0, -.95, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        nn = [n for n, path in self.leaves if path[-1][0] == 'NN']
        self.play(*[n.animate.scale(1.3) for n in nn], self.leaves[1][0].animate.set_opacity(.15), run_time=self.rt(.06))
        self.wait_until(.35, t0)
        self.write_board(self.M('leaves', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

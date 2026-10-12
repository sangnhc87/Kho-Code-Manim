"""XSS272 · Hai khâu kiểm tra — lọt cả 2 khâu: lỗi 0,1·0,1² = 0,001; tốt 0,9·0,95² ≈ 0,812: P(lỗi | qua) = 4/3253 ≈ 0,0012."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS272', 'answer': '4/3253 ≈ 0,0012'}
PROBLEM = ['Hàng lỗi $10%$; mỗi khâu kiểm tra bắt lỗi',
           '$90%$, báo nhầm hàng tốt $5%$. Hàng qua cả',
           '$2$ khâu: xác suất là hàng lỗi?']
OPTIONS = ['"0,01"', '4/3253 approx "0,0012"', '"0,1"']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('L', CORAL, '"0,1"', [('qua', GOLD, '"0,1"^2', []), ('loại', SOFT, '', [])]),
            ('T', GREEN, '"0,9"', [('qua', GOLD, '"0,95"^2', []), ('loại', SOFT, '', [])])]

BEATS = [
    Beat('hook', 'hook', 'Nhà máy có mười phần trăm hàng lỗi. Mỗi khâu kiểm tra phát hiện hàng lỗi chín mươi phần trăm, nhưng cũng loại nhầm năm phần trăm hàng tốt. '
                         'Một sản phẩm qua được cả hai khâu. Xác suất nó vẫn là hàng lỗi?'),
    Beat('guess', 'hook', 'Không phẩy không một, khoảng không phẩy không không một hai, hay không phẩy một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây hai tầng, mỗi khâu độc lập. Hàng lỗi lọt một khâu với xác suất không phẩy một, lọt cả hai: không phẩy một bình phương, không phẩy không một.'),
    Beat('s2', 'solve', 'Hàng tốt qua cả hai: không phẩy chín lăm bình phương. Hai lá "qua": không phẩy một nhân không phẩy không một bằng không phẩy không không một; '
                        'không phẩy chín nhân không phẩy chín không hai lăm, khoảng không phẩy tám một hai.'),
    Beat('s3', 'solve', 'Bayes: bốn phần ba nghìn hai trăm năm mươi ba, khoảng không phẩy mười hai phần trăm. Hai lớp kiểm tra giảm hàng lỗi gần một trăm lần!'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy không không một hai. Kiểm tra nhiều lớp là Bayes nhân lên nhiều lần!'),
    Beat('outro', 'outro', outro_text(272)),
]

FORMULAS = formulas('4/3253 approx "0,0012"', OPTIONS,
                    leaves='"0,1" dot "0,01" = "0,001", quad "0,9" dot "0,9025" approx "0,812"',
                    bayes='P(L | "qua") = ("0,001")/("0,001" + "0,81225") = 4/3253')


def validate() -> bool:
    a, b = F(1, 10) * F(1, 100), F(9, 10) * F(95, 100) ** 2
    assert a / (a + b) == F(4, 3253)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS272(TreeMixin, ShortScene):
    N = 272

    def hook_visual(self, t0):
        self.board_top = -1.55
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=6.8, root_label='sản phẩm', r=.46)
        self.wait_until(.8, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.06))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        passed = [n for n, path in self.leaves if path[-1][0] == 'qua']
        self.play(*[n.animate.scale(1.25) for n in passed], run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.write_board(self.M('leaves', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.5)
        self.write_board(m)
        self.frame(m)

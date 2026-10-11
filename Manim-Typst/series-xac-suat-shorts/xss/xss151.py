"""XSS151 · Chỉ một mũi tên trúng — lá TX: 0,32, lá XT: 0,12; P(của A | đúng 1 trúng) = 0,32/0,44 = 8/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS151', 'answer': '8/11'}
PROBLEM = ['A trúng $"0,8"$, B trúng $"0,6"$, mỗi người',
           'bắn $1$ mũi. Biết bia trúng đúng $1$ mũi.',
           'Xác suất mũi đó của A?']
OPTIONS = ['"0,8"', '8/11', '4/7']
CORRECT = 1
ANSWER_VALUE = 8 / 11
T, X = ('T', GREEN), ('X', CORAL)
BRANCHES = [(*T, '"0,8"', [(*T, '"0,6"', []), (*X, '"0,4"', [])]),
            (*X, '"0,2"', [(*T, '"0,6"', []), (*X, '"0,4"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hai cung thủ: A trúng với xác suất không phẩy tám, B trúng không phẩy sáu, mỗi người bắn một mũi. '
                         'Trọng tài báo: bia có đúng một mũi tên. Xác suất mũi đó là của A là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy tám, tám phần mười một, hay bốn phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây hai tầng: tầng một là A, tầng hai là B. Bốn lá: trúng trúng, trúng trượt, trượt trúng, trượt trượt.'),
    Beat('s2', 'solve', 'Điều kiện "đúng một mũi trúng" giữ lại hai lá: A trúng B trượt, không phẩy tám nhân không phẩy bốn bằng không phẩy ba hai; '
                        'A trượt B trúng, không phẩy hai nhân không phẩy sáu bằng không phẩy một hai.'),
    Beat('s3', 'solve', 'Xác suất mũi tên của A bằng không phẩy ba hai chia không phẩy bốn bốn, tức tám phần mười một.'),
    Beat('answer', 'solve', 'Đáp án: tám phần mười một. Lọc lá theo điều kiện, rồi lấy tỉ lệ: đó là Bayes trên sơ đồ cây!'),
    Beat('outro', 'outro', outro_text(151)),
]

FORMULAS = formulas('8/11', OPTIONS,
                    tx='P(T X) = "0,8" dot "0,4" = "0,32"',
                    xt='P(X T) = "0,2" dot "0,6" = "0,12"',
                    prob='P = ("0,32")/("0,32" + "0,12") = 8/11')


def validate() -> bool:
    assert F(32, 100) / (F(32, 100) + F(12, 100)) == F(8, 11)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS151(TreeMixin, ShortScene):
    N = 151

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='A bắn')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('T: trúng   X: trượt   (tầng 2: B)', 22, SOFT).move_to([0, -.95, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        keep = [self.leaves[1][0], self.leaves[2][0]]
        drop = [self.leaves[0][0], self.leaves[3][0]]
        self.play(*[n.animate.set_opacity(.15) for n in drop], *[n.animate.scale(1.3) for n in keep], run_time=self.rt(.06))
        self.write_board(self.M('tx', 1.9))
        self.wait_until(.55, t0)
        self.write_board(self.M('xt', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

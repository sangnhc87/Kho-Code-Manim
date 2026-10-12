"""XSS371 · Hộp vàng hay hộp trắng? — tổng ≥ 10 (1/6) → hộp vàng 4đ1x, ngược lại hộp trắng 1đ4x; P(≥ 10 | đỏ) = (1/6·4/5)/(1/6·4/5 + 5/6·1/5) = 4/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS371', 'answer': '4/9'}
PROBLEM = ['Gieo $2$ xúc xắc: tổng $>= 10$ thì rút từ',
           'hộp vàng ($4$ đỏ $1$ xanh), ngược lại hộp',
           'trắng ($1$ đỏ $4$ xanh). Rút được đỏ. Xác',
           'suất tổng $>= 10$?']
OPTIONS = ['1/6', '4/9', '4/5']
CORRECT = 1
ANSWER_VALUE = 4 / 9
HIGH = F(sum(a + b >= 10 for a in range(1, 7) for b in range(1, 7)), 36)
BRANCHES = [('≥10', GOLD, '1/6', [('Đ', CORAL, '4/5', [])]), ('<10', SOFT, '5/6', [('Đ', CORAL, '1/5', [])])]

BEATS = [
    Beat('hook', 'hook', 'Gieo hai xúc xắc. Tổng từ mười trở lên thì rút từ hộp vàng, bốn đỏ một xanh; ngược lại rút từ hộp trắng, một đỏ bốn xanh. '
                         'Rút được bi đỏ. Xác suất tổng đã từ mười trở lên?'),
    Beat('guess', 'hook', 'Một phần sáu, bốn phần chín, hay bốn phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tổng từ mười trở lên: bốn sáu, năm năm, năm sáu và các hoán vị, có sáu cặp trên ba mươi sáu, tức một phần sáu.'),
    Beat('s2', 'solve', 'Hai lá đỏ: một phần sáu nhân bốn phần năm bằng bốn phần ba mươi; năm phần sáu nhân một phần năm bằng năm phần ba mươi.'),
    Beat('s3', 'solve', 'Bayes: bốn chia bốn cộng năm, bằng bốn phần chín. Hộp vàng rất dễ ra đỏ, nhưng hiếm được chọn.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần chín. Đừng quên tần suất cơ sở: nhánh hiếm vẫn khó thắng dù khả năng cao.'),
    Beat('outro', 'outro', outro_text(371)),
]

FORMULAS = formulas('4/9', OPTIONS,
                    high='P("tổng" >= 10) = 6/36 = 1/6',
                    leafs='1/6 dot 4/5 = 4/30, quad 5/6 dot 1/5 = 5/30',
                    prob='P = 4/(4 + 5) = 4/9')


def validate() -> bool:
    a, b = HIGH * F(4, 5), (1 - HIGH) * F(1, 5)
    assert HIGH == F(1, 6) and a / (a + b) == F(4, 9)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS371(TreeMixin, ShortScene):
    N = 371

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.0, r=.44, edge_size=28)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[1]), run_time=self.rt(.06))
        self.write_board(self.M('high', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.clear_board(.03)
        self.write_board(self.M('leafs', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS396 · Hai sản phẩm cùng lô — I (60 %, lỗi 3 %), II (40 %, lỗi 5 %); 2 sản phẩm cùng dây chuyền đều lỗi:
0,6·0,03² = 0,00054 vs 0,4·0,05² = 0,001 → P(I) = 27/77."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS396', 'answer': '27/77'}
PROBLEM = ['Dây chuyền I ($60 %$) lỗi $3 %$, II ($40 %$)',
           'lỗi $5 %$. Lấy $2$ sản phẩm cùng một dây',
           'chuyền, cả $2$ đều lỗi. $P("dây chuyền I")$?']
OPTIONS = ['27/77', '50/77', '3/5']
CORRECT = 0
ANSWER_VALUE = 27 / 77
A = F(6, 10) * F(3, 100) ** 2
B = F(4, 10) * F(5, 100) ** 2
BRANCHES = [('I', GOLD, '"0,6"', [('L', CORAL, '"0,03"', [('L', CORAL, '"0,03"', [])])]),
            ('II', PURPLE, '"0,4"', [('L', CORAL, '"0,05"', [('L', CORAL, '"0,05"', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Dây chuyền một làm sáu mươi phần trăm sản phẩm, lỗi ba phần trăm; dây chuyền hai làm bốn mươi phần trăm, lỗi năm phần trăm. '
                         'Lấy hai sản phẩm cùng một dây chuyền, cả hai đều lỗi. Xác suất chúng từ dây chuyền một?'),
    Beat('guess', 'hook', 'Hai mươi bảy phần bảy mươi bảy, năm mươi phần bảy mươi bảy, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai sản phẩm cùng dây chuyền thì độc lập khi biết dây chuyền: lỗi cả hai là bình phương tỉ lệ lỗi.'),
    Beat('s2', 'solve', 'Dây chuyền một: không phẩy sáu nhân không phẩy không ba bình phương, năm mươi tư phần một trăm nghìn. Dây chuyền hai: không phẩy bốn nhân không phẩy không năm bình phương, một trăm phần một trăm nghìn.'),
    Beat('s3', 'solve', 'Bayes: năm mươi tư chia một trăm năm mươi tư, bằng hai mươi bảy phần bảy mươi bảy.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi bảy phần bảy mươi bảy. Hai lỗi liên tiếp khuếch đại chênh lệch tỉ lệ lỗi theo bình phương.'),
    Beat('outro', 'outro', outro_text(396)),
]

FORMULAS = formulas('27/77', OPTIONS,
                    leafs='"0,6" dot "0,03"^2 = 54/10^5, quad "0,4" dot "0,05"^2 = 100/10^5',
                    prob='P("I" | "2 lỗi") = 54/(54 + 100) = 27/77')


def validate() -> bool:
    assert A / (A + B) == F(27, 77)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS396(TreeMixin, ShortScene):
    N = 396

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.25, width=5.0, r=.36, edge_size=26)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.05))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2]), FadeIn(self.levels[3]), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        self.write_board(self.M('leafs', 1.2))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

"""XSS243 · Bị loại ở vòng nào? — loại V1 0,2; V2 0,32; V3 0,24 → P(V2 | loại) = 0,32/0,76 = 8/19."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS243', 'answer': '8/19'}
PROBLEM = ['Qua vòng $1$: $"0,8"$; qua $1$ thì qua vòng $2$:',
           '$"0,6"$; qua $2$ thì qua vòng $3$: $"0,5"$. Biết bị',
           'loại. Xác suất loại ở vòng $2$?']
OPTIONS = ['1/3', '8/19', '"0,32"']
CORRECT = 1
ANSWER_VALUE = 8 / 19
Q, L = ('Q', GREEN), ('L', CORAL)
BRANCHES = [(*L, '"0,2"', []),
            (*Q, '"0,8"', [(*L, '"0,4"', []), (*Q, '"0,6"', [(*L, '"0,5"', []), (*Q, '"0,5"', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Một cuộc thi ba vòng. Qua vòng một với xác suất không phẩy tám. Đã qua vòng một thì qua vòng hai không phẩy sáu, '
                         'qua vòng hai thì qua vòng ba không phẩy năm. Một thí sinh bị loại. Xác suất bạn ấy bị loại ở vòng hai?'),
    Beat('guess', 'hook', 'Một phần ba, tám phần mười chín, hay không phẩy ba hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây dừng sớm: mỗi lần bị loại là một lá. Loại vòng một: không phẩy hai. Loại vòng hai: không phẩy tám nhân không phẩy bốn, bằng không phẩy ba hai.'),
    Beat('s2', 'solve', 'Loại vòng ba: không phẩy tám nhân không phẩy sáu nhân không phẩy năm, bằng không phẩy hai bốn. Tổng xác suất bị loại: không phẩy bảy sáu.'),
    Beat('s3', 'solve', 'Điều kiện là "bị loại": không phẩy ba hai chia không phẩy bảy sáu, bằng tám phần mười chín. Không phẩy ba hai là bẫy: quên chia.'),
    Beat('answer', 'solve', 'Đáp án: tám phần mười chín. Điều kiện là một tập các lá: cộng chúng làm mẫu số!'),
    Beat('outro', 'outro', outro_text(243)),
]

FORMULAS = formulas('8/19', OPTIONS,
                    out='"0,2" + "0,32" + "0,24" = "0,76"',
                    prob='P("loại V2" | "bị loại") = ("0,32")/("0,76") = 8/19')


def validate() -> bool:
    l1, l2, l3 = F(2, 10), F(8, 10) * F(4, 10), F(8, 10) * F(6, 10) * F(5, 10)
    assert l2 / (l1 + l2 + l3) == F(8, 19)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS243(TreeMixin, ShortScene):
    N = 243

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.15, width=6.0, root_label='vòng 1', r=.38,
                                                  edge_size=28)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.1))
        self.play(FadeIn(tx('Q: qua   L: loại', 22, SOFT).move_to([0, -1.3, 0])), run_time=self.rt(.03))

    def beat_s2(self, T):
        t0 = self.now()
        out = [n for n, path in self.leaves if path[-1][0] == 'L']
        self.play(*[n.animate.scale(1.3) for n in out], self.leaves[-1][0].animate.set_opacity(.15), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.write_board(self.M('out', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

"""XSS076 · Mưa và tắc đường — toàn phần: 0,3·0,6 + 0,7·0,2 = 0,32."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS076', 'answer': '0,32'}
PROBLEM = ['$P("mưa") = "0,3"$. Tắc đường với xác suất',
           '$"0,6"$ khi mưa, $"0,2"$ khi không mưa. Xác',
           'suất hôm nay tắc đường?']
OPTIONS = ['"0,4"', '"0,32"', '"0,8"']
CORRECT = 1
ANSWER_VALUE = .32
BRANCHES = [('M', CYAN, '"0,3"', [('T', CORAL, '"0,6"', []), ('K', GREEN, '"0,4"', [])]),
            ('N', GOLD, '"0,7"', [('T', CORAL, '"0,2"', []), ('K', GREEN, '"0,8"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Xác suất trời mưa hôm nay là không phẩy ba. Trời mưa thì tắc đường với xác suất không phẩy sáu, '
                         'trời không mưa thì chỉ không phẩy hai. Xác suất hôm nay bạn bị kẹt xe là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bốn, không phẩy ba hai, hay không phẩy tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tắc đường có hai nguyên nhân: có mưa hoặc không mưa. Vẽ cây với hai nhánh thời tiết, '
                        'rồi tới tắc hay không tắc.'),
    Beat('s2', 'solve', 'Nhánh mưa rồi tắc: không phẩy ba nhân không phẩy sáu, bằng không phẩy một tám. '
                        'Nhánh không mưa rồi tắc: không phẩy bảy nhân không phẩy hai, bằng không phẩy một bốn.'),
    Beat('s3', 'solve', 'Xác suất toàn phần: cộng hai nhánh, được không phẩy ba hai. '
                        'Không phẩy tám là cộng thẳng hai xác suất có điều kiện, hoàn toàn sai.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy ba hai. Chia theo nguyên nhân, mỗi nguyên nhân nhân xác suất, rồi cộng lại!'),
    Beat('outro', 'outro', outro_text(76)),
]

FORMULAS = formulas('"0,32"', OPTIONS,
                    rain='"0,3" dot "0,6" = "0,18"',
                    dry='"0,7" dot "0,2" = "0,14"',
                    tot='P(T) = "0,18" + "0,14" = "0,32"')


def validate() -> bool:
    assert F(3, 10) * F(6, 10) + F(7, 10) * F(2, 10) == F(32, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS076(TreeMixin, ShortScene):
    N = 76

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='hôm nay')

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('M: mưa  N: nắng  T: tắc  K: không tắc', 22, SOFT).move_to([0, -.45, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('rain', 2.0))
        self.wait_until(.5, t0)
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('dry', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(tx('"0,6 + 0,2": SAI', 28, CORAL, bold=True), anim='fade')

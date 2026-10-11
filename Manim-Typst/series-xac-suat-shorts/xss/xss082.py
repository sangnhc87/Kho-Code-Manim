"""XSS082 · Ba viên đạn — p = 0,6, bắn đến khi trúng, tối đa 3 viên: 1 − 0,4³ = 0,936."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS082', 'answer': '0,936'}
PROBLEM = ['Mỗi viên đạn trúng đích với xác suất',
           '$"0,6"$. Bắn đến khi trúng thì dừng, tối',
           'đa $3$ viên. Xác suất trúng đích?']
OPTIONS = ['"1,8"', '"0,936"', '"0,6"']
CORRECT = 1
ANSWER_VALUE = .936
BRANCHES = [('T', GREEN, '"0,6"', []),
            ('X', CORAL, '"0,4"', [('T', GREEN, '"0,6"', []), ('X', CORAL, '"0,4"', [('T', GREEN, '"0,6"', []),
                                                                                   ('X', CORAL, '"0,4"', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Một xạ thủ có ba viên đạn, mỗi viên trúng đích với xác suất không phẩy sáu. '
                         'Anh bắn cho đến khi trúng thì dừng. Xác suất anh trúng đích là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phẩy tám, không phẩy chín ba sáu, hay không phẩy sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây xác suất: viên một trúng thì dừng. Trượt thì bắn viên hai, trượt nữa thì bắn viên ba.'),
    Beat('s2', 'solve', 'Trường hợp duy nhất không trúng đích: trượt cả ba viên. Xác suất là không phẩy bốn mũ ba, '
                        'bằng không phẩy không sáu tư.'),
    Beat('s3', 'solve', 'Vậy xác suất trúng đích bằng một trừ không phẩy không sáu tư, bằng không phẩy chín ba sáu. '
                        'Cộng ba lần không phẩy sáu ra một phẩy tám là vô lý.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín ba sáu. Thêm cơ hội thử lại, xác suất thành công tăng rất nhanh!'),
    Beat('outro', 'outro', outro_text(82)),
]

FORMULAS = formulas('"0,936"', OPTIONS,
                    miss='P("trượt cả 3") = "0,4"^3 = "0,064"',
                    prob='P = 1 - "0,064" = "0,936"')


def validate() -> bool:
    assert 1 - F(4, 10) ** 3 == F(936, 1000) == F(6, 10) + F(4, 10) * F(6, 10) + F(4, 10) ** 2 * F(6, 10)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS082(TreeMixin, ShortScene):
    N = 82

    def hook_visual(self, t0):
        self.board_top = -1.85
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.25, width=6.8, root_label='bắn', r=.4, edge_size=34)

    def beat_s1(self, T):
        for lv in self.levels:
            self.play(FadeIn(lv, lag_ratio=.3), run_time=self.rt(.12))
        self.play(FadeIn(tx('T: trúng   X: trượt', 26, SOFT).move_to([0, -1.45, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[-1][0].animate.scale(1.4), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.M('miss', 1.8))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('3 × 0,6 = 1,8: vô lý', 28, CORAL, bold=True), anim='fade')



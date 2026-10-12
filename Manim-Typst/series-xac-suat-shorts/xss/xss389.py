"""XSS389 · C thắng ngay vòng đầu? — C thắng ở vòng k với q^(3k+2)/6; P(C) = q²/6 / (1 − q³); P(vòng 1 | C thắng) = 1 − q³ = 91/216."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS389', 'answer': '91/216'}
PROBLEM = ['A, B, C lần lượt gieo xúc xắc, ai ra $6$',
           'trước thắng. Biết C thắng. Xác suất C',
           'thắng ở lượt gieo đầu tiên của C?']
OPTIONS = ['91/216', '1/3', '25/91']
CORRECT = 0
ANSWER_VALUE = 91 / 216
Q = F(5, 6)
WIN_C = Q ** 2 / 6 / (1 - Q ** 3)
BRANCHES = [('A', CYAN, '1/6', []),
            ('≠6', SOFT, '5/6', [('B', GOLD, '1/6', []),
                                 ('≠6', SOFT, '5/6', [('C', CORAL, '1/6', []), ('lại', SOFT, '5/6', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Ba bạn A, B, C lần lượt gieo xúc xắc theo vòng, ai ra sáu trước thì thắng. Biết C là người thắng. '
                         'Xác suất C thắng ngay ở lượt gieo đầu tiên của mình?'),
    Beat('guess', 'hook', 'Chín mươi mốt phần hai trăm mười sáu, một phần ba, hay hai mươi lăm phần chín mươi mốt? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi q bằng năm phần sáu. C thắng ở vòng một với xác suất q bình phương nhân một phần sáu. Mỗi vòng trượt cả ba nhân thêm q mũ ba.'),
    Beat('s2', 'solve', 'Tổng cấp số nhân: xác suất C thắng bằng q bình phương phần sáu chia một trừ q mũ ba.'),
    Beat('s3', 'solve', 'Tỉ số giữa vòng một và tổng chính là một trừ q mũ ba, tức một trừ một trăm hai mươi lăm phần hai trăm mười sáu, bằng chín mươi mốt phần hai trăm mười sáu.'),
    Beat('answer', 'solve', 'Đáp án: chín mươi mốt phần hai trăm mười sáu. Cây lặp: biết người thắng, vòng thắng tuân theo phân phối hình học.'),
    Beat('outro', 'outro', outro_text(389)),
]

FORMULAS = formulas('91/216', OPTIONS,
                    ck='P(C "thắng vòng" k) = q^(3k-1) dot 1/6, quad q = 5/6',
                    tot='P(C) = (q^2 dot 1/6)/(1 - q^3)',
                    prob='P = 1 - q^3 = 1 - 125/216 = 91/216')


def validate() -> bool:
    assert (Q ** 2 / 6) / WIN_C == F(91, 216)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS389(TreeMixin, ShortScene):
    N = 389

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.15, width=5.4, r=.32, edge_size=24)
        self.wait_until(.65, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('ck', 1.3))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('tot', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

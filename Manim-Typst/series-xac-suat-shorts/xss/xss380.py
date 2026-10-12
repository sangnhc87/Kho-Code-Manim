"""XSS380 · Kết thúc trước lượt 5 — ván kết thúc ở lượt k với (5/6)^(k−1)/6; A thắng ở lượt 1, 3: (1 + q²)/(1 + q + q² + q³) = 1/(1 + q) = 6/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS380', 'answer': '6/11'}
PROBLEM = ['A, B lần lượt gieo xúc xắc (A trước),',
           'ai ra $6$ trước thắng. Biết ván đấu kết',
           'thúc trước lượt $5$. Xác suất A thắng?']
OPTIONS = ['1/2', '6/11', '6/7']
CORRECT = 1
ANSWER_VALUE = 6 / 11
Q = F(5, 6)
T = {k: Q ** (k - 1) / 6 for k in range(1, 5)}
BRANCHES = [('A', CYAN, '1/6', []),
            ('≠6', SOFT, '5/6', [('B', CORAL, '1/6', []),
                                ('≠6', SOFT, '5/6', [('A', CYAN, '1/6', []),
                                                    ('≠6', SOFT, '5/6', [('B', CORAL, '1/6', [])])])])]

BEATS = [
    Beat('hook', 'hook', 'A và B lần lượt gieo xúc xắc, A gieo trước, ai ra sáu trước thì thắng. Biết ván đấu kết thúc trước lượt thứ năm. '
                         'Xác suất A thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, sáu phần mười một, hay sáu phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ván kết thúc ở lượt k với xác suất năm phần sáu mũ k trừ một nhân một phần sáu. A gieo ở lượt một và ba, B ở lượt hai và bốn.'),
    Beat('s2', 'solve', 'Gọi q bằng năm phần sáu. A thắng: một cộng q bình phương. Tổng bốn lượt: một cộng q cộng q bình phương cộng q mũ ba, bằng một cộng q nhân một cộng q bình phương.'),
    Beat('s3', 'solve', 'Rút gọn còn một chia một cộng q, tức sáu phần mười một. Đúng bằng xác suất A thắng khi không giới hạn lượt!'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười một. Cắt cây ở số lượt chẵn không làm thay đổi tỉ lệ thắng.'),
    Beat('outro', 'outro', outro_text(380)),
]

FORMULAS = formulas('6/11', OPTIONS,
                    tk='P("dừng ở lượt" k) = q^(k-1) dot 1/6, quad q = 5/6',
                    prob='P(A) = (1 + q^2)/((1 + q)(1 + q^2)) = 1/(1 + q) = 6/11')


def validate() -> bool:
    assert (T[1] + T[3]) / sum(T.values()) == F(6, 11) == 1 / (1 + Q)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS380(TreeMixin, ShortScene):
    N = 380

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=.95, width=5.6, r=.3, edge_size=22)
        self.wait_until(.65, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[FadeIn(lv) for lv in self.levels[2:]], run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('tk', 1.3))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.clear_board(.03)

    def beat_s3(self, T):
        m = self.M('prob', 1.4)
        self.write_board(m)
        self.frame(m)

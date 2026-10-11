"""XSS126 · Thắng 2 trong 3 ván — cây dừng sớm: 0,6² + 2·0,6²·0,4 = 0,648."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS126', 'answer': '0,648'}
PROBLEM = ['A thắng mỗi ván với xác suất $"0,6"$.',
           'Ai thắng $2$ ván trước là vô địch.',
           'Xác suất A vô địch?']
OPTIONS = ['"0,6"', '"0,648"', '"0,36"']
CORRECT = 1
ANSWER_VALUE = .648
A, B = ('A', CYAN, '"0,6"'), ('B', CORAL, '"0,4"')
BRANCHES = [(*A, [(*A, []), (*B, [(*A, []), (*B, [])])]),
            (*B, [(*A, [(*A, []), (*B, [])]), (*B, [])])]

BEATS = [
    Beat('hook', 'hook', 'Trận chung kết đánh tối đa ba ván, ai thắng hai ván trước là vô địch. '
                         'A mạnh hơn, thắng mỗi ván với xác suất không phẩy sáu. Xác suất A vô địch là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy sáu, không phẩy sáu bốn tám, hay không phẩy ba sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ cây dừng sớm: ai thắng hai ván là nhánh kết thúc. Có nhánh dừng sau hai ván, có nhánh phải đánh ván ba.'),
    Beat('s2', 'solve', 'A vô địch ở ba lá: A A, xác suất không phẩy ba sáu; A B A và B A A, mỗi lá không phẩy sáu bình phương '
                        'nhân không phẩy bốn, cộng lại không phẩy hai tám tám.'),
    Beat('s3', 'solve', 'Tổng: không phẩy ba sáu cộng không phẩy hai tám tám, bằng không phẩy sáu bốn tám. '
                        'Đánh ba ván giúp người mạnh hơn có lợi hơn so với chỉ một ván!'),
    Beat('answer', 'solve', 'Đáp án: không phẩy sáu bốn tám. Thử thách tiếp theo: nếu đánh năm ván thì sao?'),
    Beat('outro', 'outro', outro_text(126)),
]

FORMULAS = formulas('"0,648"', OPTIONS,
                    aa='P(A A) = "0,6"^2 = "0,36"',
                    aba='P(A B A) + P(B A A) = 2 dot "0,6"^2 dot "0,4" = "0,288"',
                    tot='P = "0,36" + "0,288" = "0,648"')


def validate() -> bool:
    p = sum(F(3, 5) ** w.count('A') * F(2, 5) ** w.count('B') for w in product('AB', repeat=3) if w.count('A') >= 2)
    assert float(p) == .648
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS126(TreeMixin, ShortScene):
    N = 126

    def hook_visual(self, t0):
        self.board_top = -1.75
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.05), dy=1.3, width=7.2, root_label='ván 1', r=.36,
                                                  edge_size=27)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[3], lag_ratio=.2), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        wins = [n for n, path in self.leaves if [b[0] for b in path].count('A') == 2]
        self.play(*[n.animate.scale(1.35) for n in wins], run_time=self.rt(.06))
        self.write_board(self.M('aa', 1.9))
        self.wait_until(.45, t0)
        self.write_board(self.M('aba', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('đánh nhiều ván: người mạnh có lợi', 26, SOFT), anim='fade')

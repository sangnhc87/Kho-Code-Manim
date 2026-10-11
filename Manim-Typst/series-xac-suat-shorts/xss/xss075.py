"""XSS075 · Qua hai vòng thi — công thức nhân có điều kiện: 0,8 · 0,6 = 0,48."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS075', 'answer': '0,48'}
PROBLEM = ['Qua vòng $1$ với xác suất $"0,8"$. Nếu đã qua vòng $1$ thì qua',
           'vòng $2$ với xác suất $"0,6"$. Xác suất qua cả hai vòng?']
OPTIONS = ['"1,4"', '"0,48"', '"0,6"']
CORRECT = 1
ANSWER_VALUE = .48
BRANCHES = [('Q', GREEN, '"0,8"', [('Q', GREEN, '"0,6"', []), ('R', CORAL, '"0,4"', [])]),
            ('R', CORAL, '"0,2"', [])]

BEATS = [
    Beat('hook', 'hook', 'Một cuộc thi có hai vòng. Bạn qua vòng một với xác suất không phẩy tám. '
                         'Nếu đã qua vòng một, bạn qua vòng hai với xác suất không phẩy sáu. Xác suất qua cả hai vòng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phẩy bốn, không phẩy bốn tám, hay không phẩy sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Để ý chữ "nếu đã qua vòng một": không phẩy sáu là xác suất có điều kiện, '
                        'chỉ áp dụng cho những ai đã vượt vòng một.'),
    Beat('s2', 'solve', 'Công thức nhân xác suất: xác suất A và B bằng xác suất A nhân xác suất B khi biết A. '
                        'Không phẩy tám nhân không phẩy sáu, bằng không phẩy bốn tám.'),
    Beat('s3', 'solve', 'Không phẩy sáu là bẫy: đó chỉ là phần của vòng hai. Muốn qua cả hai vòng, '
                        'trước hết phải qua vòng một đã.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bốn tám. Công thức nhân không cần độc lập, chỉ cần dùng đúng xác suất có điều kiện!'),
    Beat('outro', 'outro', outro_text(75)),
]

FORMULAS = formulas('"0,48"', OPTIONS,
                    rule='P(A B) = P(A) dot P(B|A)',
                    calc='"0,8" dot "0,6" = "0,48"')


def validate() -> bool:
    assert F(8, 10) * F(6, 10) == F(48, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS075(TreeMixin, ShortScene):
    N = 75

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=5.4, root_label='vòng 1')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.play(FadeIn(tx('Q: qua   R: rớt', 24, SOFT).move_to([0, -.45, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('rule', 1.9))
        self.wait_until(.5, t0)
        self.play(self.leaves[0][0].animate.scale(1.35), run_time=self.rt(.05))
        m = self.M('calc', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.clear_board(.03)
        self.write_board(tx('0,6 chỉ là phần của vòng 2', 30, CORAL, bold=True), anim='fade')
        self.write_board(tx('nhân dọc theo nhánh', 28, GOLD), anim='fade')

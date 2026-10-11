"""XSS061 · Biết tổng bằng 8 — không gian mẫu thu hẹp còn 5 ô, 2 ô có mặt 3: P(A|B) = 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS061', 'answer': '2/5'}
PROBLEM = ['Gieo hai con xúc xắc, biết tổng bằng $8$.', 'Xác suất có một con ra mặt $3$?']
OPTIONS = ['1/18', '2/5', '1/3']
CORRECT = 1
ANSWER_VALUE = .4
SPACE = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Bạn gieo hai con xúc xắc trong cốc, bạn bè chỉ nói: tổng bằng tám. '
                         'Với thông tin đó, xác suất có một con ra mặt ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười tám, hai phần năm, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Thông tin tổng bằng tám đã loại bỏ rất nhiều kết quả. Không gian mẫu mới chỉ còn năm ô: '
                        'hai sáu, ba năm, bốn bốn, năm ba, sáu hai.'),
    Beat('s2', 'solve', 'Trong năm ô đó, có mặt ba ở đúng hai ô: ba năm và năm ba. '
                        'Xác suất có điều kiện bằng hai phần năm.'),
    Beat('s3', 'solve', 'Đó chính là công thức xác suất có điều kiện: xác suất A giao B chia cho xác suất B, '
                        'hai phần ba mươi sáu chia năm phần ba mươi sáu, bằng hai phần năm. '
                        'Một phần mười tám là quên mất điều kiện.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Biết thêm thông tin là thu hẹp không gian mẫu!'),
    Beat('outro', 'outro', outro_text(61)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    cnt='n(B) = 5, quad n(A B) = 2',
                    rule='P(A|B) = (P(A B))/(P(B)) = (2/36)/(5/36) = 2/5')


def validate() -> bool:
    b = [w for w in SPACE if sum(w) == 8]
    assert len(b) == 5 and F(sum(3 in w for w in b), len(b)) == F(2, 5)
    assert F(sum(3 in w and sum(w) == 8 for w in SPACE), 36) == F(1, 18)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS061(DiceGridMixin, ShortScene):
    N = 61

    def hook_visual(self, t0):
        self.d1 = die(3, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(5, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.04))
        self.remove(self.d1, self.d2)
        self.show_grid(.2, sums=True)
        self.wait_until(.45, t0)
        cond = [self.g.cells[8 - a - 1][a - 1] for a in range(2, 7)]
        rest = [c for row in self.g.cells for c in row if c not in cond]
        self.play(*[c.animate.set_opacity(.12) for c in rest], *[c.animate.set_fill(CYAN, .55) for c in cond],
                  self.sum_labels.animate.set_opacity(.35), run_time=self.rt(.12))
        self.write_board(tx('chỉ còn 5 ô', 32, CYAN, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.g.cells[4][2].animate.set_fill(GOLD, .9), self.g.cells[2][4].animate.set_fill(GOLD, .9),
                  run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.write_board(self.M('cnt', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('rule', 1.5)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.65, t0)
        self.write_board(tx('1/18: quên mất điều kiện', 26, CORAL, bold=True), anim='fade')

"""XSS029 · Tích là số chẵn — biến cố đối: cả hai lẻ 9/36 → 1 − 1/4 = 3/4."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS029', 'answer': '3/4'}
PROBLEM = ['Gieo hai con xúc xắc.', 'Xác suất tích hai số chấm là số chẵn?']
OPTIONS = ['1/2', '2/3', '3/4']
CORRECT = 2
ANSWER_VALUE = .75

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc rồi nhân hai số chấm. Xác suất tích là số chẵn là bao nhiêu? '
                         'Nhiều bạn đoán một phần hai, nhưng tích khác tổng đấy!'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tích là số chẵn khi có ít nhất một thừa số chẵn. Đếm trực tiếp khá lâu, '
                        'nên ta xét biến cố đối: tích là số lẻ.'),
    Beat('s2', 'solve', 'Tích lẻ khi cả hai con đều lẻ: con thứ nhất có ba mặt lẻ, con thứ hai cũng ba mặt lẻ. '
                        'Ba nhân ba bằng chín ô trên bảng ba mươi sáu ô.'),
    Beat('s3', 'solve', 'Xác suất tích lẻ là chín phần ba mươi sáu, tức một phần tư. '
                        'Vậy xác suất tích chẵn bằng một trừ một phần tư, bằng ba phần tư.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tư. Chỉ cần một con chẵn là đủ, nên tích chẵn rất dễ xảy ra.'),
    Beat('outro', 'outro', outro_text(29)),
]

FORMULAS = formulas('3/4', OPTIONS,
                    odd='P("tích lẻ") = 9/36 = 1/4',
                    prob='P("tích chẵn") = 1 - 1/4 = 3/4')


def validate() -> bool:
    space = list(product(range(1, 7), repeat=2))
    assert Fraction(sum(a * b % 2 == 0 for a, b in space), 36) == Fraction(3, 4)
    assert Fraction(sum(a % 2 and b % 2 for a, b in space), 36) == Fraction(1, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS029(DiceGridMixin, ShortScene):
    N = 29

    def hook_visual(self, t0):
        self.d1 = die(3, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(4, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.1))

    def beat_s1(self, T):
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.04))
        self.remove(self.d1, self.d2)
        self.show_grid(.35)

    def beat_s2(self, T):
        t0 = self.now()
        odd = [self.g.cells[j][i] for i in (0, 2, 4) for j in (0, 2, 4)]
        self.light(odd, CORAL, .05)
        self.wait_until(.7, t0)
        self.write_board(tx('9 ô: cả hai lẻ', 30, CORAL, bold=True), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('odd', 1.9))
        self.wait_until(.45, t0)
        rest = [self.g.cells[j][i] for i in range(6) for j in range(6) if not (i % 2 == 0 and j % 2 == 0)]
        self.play(*[c.animate.set_fill(GREEN, .45) for c in rest], run_time=self.rt(.1))
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)

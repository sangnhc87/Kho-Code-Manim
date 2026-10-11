"""XSS127 · Vì sao chung kết đánh 5 ván? — A thắng ván cuối: p³(1 + 3q + 6q²) ≈ 0,683, so với 0,648 và 0,6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import DOWN, UP, DashedLine, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS127', 'answer': '≈ 0,683'}
PROBLEM = ['A thắng mỗi ván với xác suất $"0,6"$.',
           'Ai thắng $3$ ván trước là vô địch.',
           'Xác suất A vô địch?']
OPTIONS = ['"0,6"', '"0,648"', 'approx "0,683"']
CORRECT = 2
ANSWER_VALUE = .683
p, q = F(3, 5), F(2, 5)


def best_of(n):
    need = n // 2 + 1
    return sum(comb(need - 1 + k, k) * p ** need * q ** k for k in range(need))


BEATS = [
    Beat('hook', 'hook', 'Vì sao các trận chung kết hay đánh năm ván hoặc bảy ván? A thắng mỗi ván với xác suất không phẩy sáu, '
                         'ai thắng ba ván trước là vô địch. Xác suất A vô địch là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy sáu, không phẩy sáu bốn tám, hay khoảng không phẩy sáu tám ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây có quá nhiều nhánh, nên ta đếm thông minh: chia theo số ván đã đánh. '
                        'Mẹo then chốt: ván cuối cùng luôn do A thắng.'),
    Beat('s2', 'solve', 'Thắng sau ba ván: không phẩy sáu mũ ba. Sau bốn ván: ba ván đầu A thắng hai, tổ hợp chập hai của ba cách. '
                        'Sau năm ván: bốn ván đầu thắng hai, tổ hợp chập hai của bốn, bằng sáu cách.'),
    Beat('s3', 'solve', 'Cộng lại được khoảng không phẩy sáu tám ba. So sánh: một ván không phẩy sáu, ba ván không phẩy sáu bốn tám, '
                        'năm ván không phẩy sáu tám ba, bảy ván không phẩy bảy một.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy sáu tám ba. Càng đánh nhiều ván, may rủi càng ít, người giỏi hơn càng dễ thắng!'),
    Beat('outro', 'outro', outro_text(127)),
]

FORMULAS = formulas('approx "0,683"', OPTIONS,
                    w3='"3 ván": "0,6"^3 = "0,216"',
                    w4='"4 ván": C_3^2 dot "0,6"^3 dot "0,4" = "0,2592"',
                    w5='"5 ván": C_4^2 dot "0,6"^3 dot "0,4"^2 = "0,20736"',
                    tot='P = "0,216" + "0,2592" + "0,20736" approx "0,683"')


def validate() -> bool:
    assert abs(float(best_of(5)) - .68256) < 1e-12 and float(best_of(3)) == .648
    full = sum(p ** w.count('A') * q ** w.count('B') for w in product('AB', repeat=5) if w.count('A') >= 3)
    assert full == best_of(5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS127(ShortScene):
    N = 127

    def hook_visual(self, t0):
        self.board_top = -1.3
        base, top = -.55, 2.6
        self.bars, self.labs = VGroup(), VGroup()
        for i, n in enumerate((1, 3, 5, 7)):
            v = float(best_of(n))
            x = -2.7 + 1.8 * i
            b = Rectangle(width=1.0, height=(top - base) * (v - .4) / .4, stroke_width=0,
                          fill_color=GREEN if n == 5 else CYAN, fill_opacity=.85)
            b.move_to([x, base + b.height / 2, 0])
            self.bars.add(b)
            self.labs.add(VGroup(self.MNum(v, 3, SOFT, 26).next_to(b, UP, buff=.08),
                                 self.TM(f'${n}$ ván', 24, SOFT).next_to([x, base, 0], DOWN, buff=.12)))
        self.axis = DashedLine([-3.4, base, 0], [3.4, base, 0], color=STROKE, stroke_width=2)
        self.wait_until(.55, t0)
        self.play(FadeIn(self.axis), GrowFromEdge(self.bars[0], DOWN), FadeIn(self.labs[0]), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(GrowFromEdge(self.bars[1], DOWN), FadeIn(self.labs[1]), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('w3', 1.6))
        self.wait_until(.3, t0)
        self.write_board(self.M('w4', 1.6))
        self.wait_until(.65, t0)
        self.write_board(self.M('w5', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 1.8)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.45, t0)
        self.play(GrowFromEdge(self.bars[2], DOWN), FadeIn(self.labs[2]), run_time=self.rt(.08))
        self.wait_until(.7, t0)
        self.play(GrowFromEdge(self.bars[3], DOWN), FadeIn(self.labs[3]), run_time=self.rt(.08))



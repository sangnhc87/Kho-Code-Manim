"""XSS252 · Bắn bao nhiêu phát? — 1 − 0,7ⁿ ≥ 0,95 ⇔ 0,7ⁿ ≤ 0,05 ⇔ n ≥ 9 (0,7⁸ ≈ 0,058; 0,7⁹ ≈ 0,040)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, DashedLine, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS252', 'answer': '9'}
PROBLEM = ['Mỗi phát trúng với xác suất $"0,3"$. Phải',
           'bắn ít nhất bao nhiêu phát để xác suất',
           'trúng ít nhất $1$ phát $>= "0,95"$?']
OPTIONS = ['4', '9', '17']
CORRECT = 1
ANSWER_VALUE = None
VALS = [1 - .7 ** n for n in range(1, 11)]

BEATS = [
    Beat('hook', 'hook', 'Một xạ thủ chỉ trúng ba mươi phần trăm mỗi phát. Phải bắn ít nhất bao nhiêu phát để chắc chắn chín mươi lăm phần trăm '
                         'có ít nhất một phát trúng?'),
    Beat('guess', 'hook', 'Bốn phát, chín phát, hay mười bảy phát? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ít nhất một phát trúng bằng một trừ trượt hết: một trừ không phẩy bảy mũ n. Cần lớn hơn hoặc bằng không phẩy chín lăm.'),
    Beat('s2', 'solve', 'Tức không phẩy bảy mũ n nhỏ hơn hoặc bằng không phẩy không năm. Thử: mũ tám khoảng không phẩy không năm tám, chưa đủ; mũ chín khoảng không phẩy không bốn, đạt.'),
    Beat('s3', 'solve', 'Vậy cần ít nhất chín phát. Biểu đồ cho thấy xác suất tăng nhanh lúc đầu rồi chậm dần khi tiến gần một.'),
    Beat('answer', 'solve', 'Đáp án: chín phát. Tìm n nhỏ nhất: lập bất phương trình mũ, thử dần hoặc dùng logarit!'),
    Beat('outro', 'outro', outro_text(252)),
]

FORMULAS = formulas('9', OPTIONS,
                    ineq='1 - "0,7"^n >= "0,95" arrow.l.r.double "0,7"^n <= "0,05"',
                    test='"0,7"^8 approx "0,058" > "0,05", quad "0,7"^9 approx "0,040" <= "0,05"')


def validate() -> bool:
    assert next(n for n in range(1, 50) if 1 - F(7, 10) ** n >= F(95, 100)) == 9
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS252(ShortScene):
    N = 252

    def hook_visual(self, t0):
        self.board_top = -1.3
        base, h = -.1, 2.9
        self.bars = VGroup()
        for k, v in enumerate(VALS):
            r = Rectangle(width=.5, height=h * v, stroke_width=0, fill_color=GREEN if v >= .95 else CYAN, fill_opacity=.85)
            r.move_to([-3.0 + .66 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k + 1}$', 20, SOFT).next_to([-3.0 + .66 * k, base, 0], DOWN, buff=.08) for k in range(10)])
        self.line = DashedLine([-3.4, base + h * .95, 0], [3.4, base + h * .95, 0], color=GOLD, stroke_width=3)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), FadeIn(self.line), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))
        self.wait_until(.45, t0)
        self.write_board(self.M('ineq', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('test', 1.4))
        self.play(self.bars[7].animate.set_fill(CORAL, .85), self.bars[8].animate.scale(1.08), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.TM('$n_min = 9$', 40, GOLD, bold=True)
        self.write_board(m)
        self.frame(m)

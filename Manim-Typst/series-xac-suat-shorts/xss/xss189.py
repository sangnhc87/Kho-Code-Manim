"""XSS189 · Ngửa nhiều hơn sấp — đối xứng: (1 − C(10,5)/2¹⁰)/2 = 193/512."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS189', 'answer': '193/512 ≈ 0,377'}
PROBLEM = ['Tung đồng xu cân đối $10$ lần. Xác suất',
           'số lần ngửa nhiều hơn số lần sấp?']
OPTIONS = ['1/2', '193/512 approx "0,377"', '"0,623"']
CORRECT = 1
ANSWER_VALUE = 193 / 512

BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu mười lần. Xác suất số lần ngửa nhiều hơn số lần sấp là bao nhiêu? '
                         'Đồng xu cân đối, vậy chắc là một phần hai?'),
    Beat('guess', 'hook', 'Một phần hai, khoảng không phẩy ba bảy bảy, hay không phẩy sáu hai ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có ba khả năng: ngửa nhiều hơn, sấp nhiều hơn, hoặc bằng nhau năm năm. '
                        'Do đối xứng, hai khả năng đầu có xác suất bằng nhau.'),
    Beat('s2', 'solve', 'Bằng nhau năm năm: tổ hợp chập năm của mười, hai trăm năm mươi hai trên một nghìn không trăm hai mươi bốn, '
                        'khoảng hai mươi lăm phần trăm. Không hề nhỏ!'),
    Beat('s3', 'solve', 'Phần còn lại chia đôi: một trừ hai trăm năm mươi hai phần một nghìn không trăm hai mươi bốn, chia hai, '
                        'bằng một trăm chín mươi ba phần năm trăm mười hai, khoảng không phẩy ba bảy bảy.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy ba bảy bảy. Đối xứng giúp tránh phải cộng sáu số hạng tổ hợp!'),
    Beat('outro', 'outro', outro_text(189)),
]

FORMULAS = formulas('193/512 approx "0,377"', OPTIONS,
                    tie='P("5 – 5") = (C_10^5)/2^10 = 252/1024',
                    sym='P = 1/2 (1 - 252/1024) = 193/512')


def validate() -> bool:
    direct = F(sum(comb(10, k) for k in range(6, 11)), 1024)
    assert direct == (1 - F(252, 1024)) / 2 == F(193, 512)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS189(ShortScene):
    N = 189

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.35, 3.1
        self.bars = VGroup()
        for k in range(11):
            r = Rectangle(width=.5, height=max(.03, h * comb(10, k) / 252), stroke_width=0,
                          fill_color=GOLD if k == 5 else (CYAN if k > 5 else CORAL), fill_opacity=.85)
            r.move_to([-3.0 + .6 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k}$', 20, SOFT).next_to([-3.0 + .6 * k, base, 0], DOWN, buff=.08) for k in range(11)])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.axis), *[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[b.animate.set_opacity(.35) for b in self.bars[:5]], run_time=self.rt(.05))
        self.play(*[b.animate.set_opacity(.85) for b in self.bars[:5]], *[b.animate.set_opacity(.35) for b in self.bars[6:]],
                  run_time=self.rt(.05))
        self.play(*[b.animate.set_opacity(.85) for b in self.bars], run_time=self.rt(.03))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.bars[5].animate.set_stroke(GOLD, 4), run_time=self.rt(.04))
        self.wait_until(.3, t0)
        self.write_board(self.M('tie', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sym', 1.9)
        self.write_board(m)
        self.frame(m)

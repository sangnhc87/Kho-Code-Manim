"""XSS237 · Xúc xắc rồi đồng xu — gieo k, tung k xu: P(không ngửa) = 1/6 Σ (1/2)^k = 21/128."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS237', 'answer': '21/128'}
PROBLEM = ['Gieo xúc xắc được $k$ chấm, rồi tung $k$',
           'đồng xu. Xác suất không có mặt ngửa nào?']
OPTIONS = ['1/64', '21/128', '1/6']
CORRECT = 1
ANSWER_VALUE = 21 / 128
TERMS = [F(1, 6) * F(1, 2) ** k for k in range(1, 7)]

BEATS = [
    Beat('hook', 'hook', 'Hai hành động nối tiếp: gieo một con xúc xắc được k chấm, rồi tung k đồng xu. '
                         'Xác suất không có đồng xu nào ra ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu mươi tư, hai mươi mốt phần một trăm hai mươi tám, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Kết quả xúc xắc quyết định số đồng xu. Biết k, xác suất không ngửa nào là một phần hai mũ k: '
                        'k bằng một thì một phần hai, k bằng sáu thì chỉ một phần sáu mươi tư.'),
    Beat('s2', 'solve', 'Công thức toàn phần trên sáu nhánh: một phần sáu nhân tổng một phần hai, một phần tư, cho đến một phần sáu mươi tư.'),
    Beat('s3', 'solve', 'Tổng trong ngoặc là sáu mươi ba phần sáu mươi tư. Nhân một phần sáu được hai mươi mốt phần một trăm hai mươi tám.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi mốt phần một trăm hai mươi tám. Thử thách tiếp: biết không có ngửa nào, xúc xắc đã ra mấy?'),
    Beat('outro', 'outro', outro_text(237)),
]

FORMULAS = formulas('21/128', OPTIONS,
                    cond='P("không ngửa" | k) = (1/2)^k',
                    tot='P = 1/6 (1/2 + 1/4 + dots + 1/64) = 1/6 dot 63/64 = 21/128')


def validate() -> bool:
    assert sum(TERMS) == F(21, 128)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS237(ShortScene):
    N = 237

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.1, 2.9
        self.bars = VGroup()
        for k in range(1, 7):
            r = Rectangle(width=.7, height=h * float(F(1, 2) ** k) / .5, stroke_width=0, fill_color=CYAN, fill_opacity=.85)
            r.move_to([-2.75 + 1.1 * (k - 1), base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'$k = {k}$', 20, SOFT).next_to([-2.75 + 1.1 * (k - 1), base, 0], DOWN, buff=.08)
                             for k in range(1, 7)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('cond', 2.1))

    def beat_s2(self, T):
        self.clear_board(.03)
        self.play(*[b.animate.set_fill(GOLD, .85) for b in self.bars], run_time=self.rt(.06))

    def beat_s3(self, T):
        m = self.M('tot', 1.4)
        self.write_board(m)
        self.frame(m)

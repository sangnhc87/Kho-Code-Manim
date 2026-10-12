"""XSS283 · Ếch về chỗ cũ — 6 bước ±1, về gốc ⇔ 3 trái 3 phải: C(6,3)/2⁶ = 20/64 = 5/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS283', 'answer': '5/16'}
PROBLEM = ['Ếch mỗi bước nhảy sang trái hoặc phải',
           '$1$ ô (mỗi hướng $1/2$). Xác suất sau',
           '$6$ bước ếch về đúng chỗ cũ?']
OPTIONS = ['1/2', '5/16', '1/6']
CORRECT = 1
ANSWER_VALUE = 5 / 16

BEATS = [
    Beat('hook', 'hook', 'Chú ếch say rượu: mỗi bước nhảy trái hoặc phải một ô, năm mươi năm mươi. Sau sáu bước, xác suất ếch quay về đúng chỗ cũ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, năm phần mười sáu, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Về chỗ cũ nghĩa là số bước trái bằng số bước phải: ba trái, ba phải. Có hai mũ sáu, sáu mươi tư dãy đồng khả năng.'),
    Beat('s2', 'solve', 'Chọn ba vị trí cho bước trái: tổ hợp chập ba của sáu, hai mươi dãy. Vị trí cuối có phân phối dạng chuông, cao nhất ở giữa.'),
    Beat('s3', 'solve', 'Xác suất hai mươi phần sáu mươi tư, tức năm phần mười sáu. Sau số lẻ bước thì không bao giờ về được gốc!'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười sáu. Đi ngẫu nhiên về gốc: đếm số cách chia đều trái và phải!'),
    Beat('outro', 'outro', outro_text(283)),
]

FORMULAS = formulas('5/16', OPTIONS,
                    prob='P = (C_6^3)/2^6 = 20/64 = 5/16')


def validate() -> bool:
    assert F(sum(sum(w) == 0 for w in product((1, -1), repeat=6)), 64) == F(5, 16) == F(comb(6, 3), 64)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS283(ShortScene):
    N = 283

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.1, 2.9
        self.bars = VGroup()
        for i, k in enumerate(range(-6, 7, 2)):
            r = Rectangle(width=.7, height=h * comb(6, (k + 6) // 2) / 20, stroke_width=0, fill_color=GOLD if k == 0 else CYAN,
                          fill_opacity=.85)
            r.move_to([-3.0 + 1.0 * i, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k}$', 22, SOFT).next_to([-3.0 + 1.0 * i, base, 0], DOWN, buff=.08)
                             for i, k in enumerate(range(-6, 7, 2))])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.TM('về gốc ⇔ $3$ trái, $3$ phải', 30, GOLD))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))
        self.wait_until(.4, t0)

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

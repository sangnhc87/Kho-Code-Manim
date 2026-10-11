"""XSS013 · Tần suất khác xác suất — 47 lần ngửa / 100: tần suất 0,47, xác suất vẫn 0,5."""
from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from manim import DOWN, RIGHT, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS013', 'answer': '0,47 (xác suất vẫn là 0,5)'}
PROBLEM = ['Tung đồng xu $100$ lần, được $47$ lần ngửa.', 'Tần suất xuất hiện mặt ngửa?']
OPTIONS = ['"0,5"', '"0,47"', '47']
CORRECT = 1
ANSWER_VALUE = .47
HEADS = 47


def layout():
    order = [1] * HEADS + [0] * (100 - HEADS)
    random.Random(13).shuffle(order)
    return order


BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu một trăm lần, được bốn mươi bảy lần ngửa. Tần suất xuất hiện mặt ngửa '
                         'là bao nhiêu? Và có phải đồng xu bị lệch không?'),
    Beat('guess', 'hook', 'Không phẩy năm, không phẩy bốn bảy, hay bốn mươi bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Một trăm lần tung hiện thành một trăm đồng xu nhỏ: bốn mươi bảy đồng vàng là ngửa, '
                        'năm mươi ba đồng bạc là sấp.'),
    Beat('s2', 'solve', 'Tần suất bằng số lần xảy ra chia cho số lần thử: bốn mươi bảy phần một trăm, '
                        'tức không phẩy bốn bảy.'),
    Beat('s3', 'solve', 'Đồng xu không hề lệch. Xác suất lý thuyết vẫn là không phẩy năm; tần suất chỉ dao động quanh nó, '
                        'và càng tung nhiều lần thì càng sát. Đó là luật số lớn.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bốn bảy. Tần suất là con số đo được, xác suất là con số lý thuyết.'),
    Beat('outro', 'outro', outro_text(13)),
]

FORMULAS = formulas('"0,47"', OPTIONS,
                    freq='f = 47/100 = "0,47"',
                    theory='P = "0,5"',
                    law='n " lớn" arrow.r.double f approx P')


def validate() -> bool:
    assert sum(layout()) == HEADS and Fraction(HEADS, 100) == Fraction(47, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS013(ShortScene):
    N = 13

    def hook_visual(self, t0):
        self.c = coin('N', 1.3).move_to([0, 1.3, 0])
        self.play(FadeIn(self.c, scale=.6), run_time=self.rt(.05))
        self.wait_until(.35, t0)
        self.c = self.flip(self.c, 'SNNSN', self.rt(.4))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.c.animate.scale(.1).set_opacity(0), run_time=self.rt(.05))
        self.remove(self.c)
        dots = VGroup(*[coin('N' if h else 'S', .17) for h in layout()]).arrange_in_grid(10, 10, buff=.06)
        dots.move_to([0, 1.55, 0])
        self.play(FadeIn(dots, lag_ratio=.01), run_time=self.rt(.4))
        self.dots = dots
        self.wait_until(.7, t0)
        legend = VGroup(VGroup(coin('N', .18), tx('47 ngửa', 26, GOLD, bold=True)).arrange(RIGHT, buff=.15),
                        VGroup(coin('S', .18), tx('53 sấp', 26, SOFT, bold=True)).arrange(RIGHT, buff=.15)) \
            .arrange(RIGHT, buff=.6).next_to(dots, DOWN, buff=.25)
        self.play(FadeIn(legend), run_time=self.rt(.06))
        self.legend = legend

    def beat_s2(self, T):
        t0 = self.now()
        self.board_top = -1.3
        self.wait_until(.35, t0)
        m = self.M('freq', 2.2)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('theory', 2.1))
        self.wait_until(.55, t0)
        self.write_board(self.M('law', 1.8))
        self.write_board(tx('luật số lớn', 28, CYAN, bold=True), anim='fade')

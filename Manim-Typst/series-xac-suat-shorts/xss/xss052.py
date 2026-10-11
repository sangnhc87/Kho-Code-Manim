"""XSS052 · Số chia hết cho 5 — số có 3 chữ số khác nhau: (72 + 64)/648 = 17/81."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS052', 'answer': '17/81'}
PROBLEM = ['Chọn ngẫu nhiên một số có $3$ chữ số đôi một khác nhau.', 'Xác suất số đó chia hết cho $5$?']
OPTIONS = ['1/5', '17/81', '1/10']
CORRECT = 1
ANSWER_VALUE = 17 / 81

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên một số có ba chữ số, các chữ số đôi một khác nhau. '
                         'Xác suất số đó chia hết cho năm là bao nhiêu? Một phần năm thì quá dễ đoán, liệu có đúng?'),
    Beat('guess', 'hook', 'Một phần năm, mười bảy phần tám mươi mốt, hay một phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm không gian mẫu: chữ số hàng trăm khác không, có chín cách. Hàng chục còn chín cách, '
                        'hàng đơn vị còn tám cách. Tổng cộng sáu trăm bốn mươi tám số.'),
    Beat('s2', 'solve', 'Chia hết cho năm khi tận cùng là không hoặc năm. Tận cùng không: hàng trăm chín cách, '
                        'hàng chục tám cách, được bảy mươi hai số. Tận cùng năm: hàng trăm chỉ còn tám cách vì '
                        'không được là không, hàng chục tám cách, được sáu mươi tư số.'),
    Beat('s3', 'solve', 'Tổng cộng một trăm ba mươi sáu số. Xác suất bằng một trăm ba mươi sáu phần sáu trăm bốn mươi tám, '
                        'rút gọn còn mười bảy phần tám mươi mốt, hơi lớn hơn một phần năm.'),
    Beat('answer', 'solve', 'Đáp án: mười bảy phần tám mươi mốt. Chữ số không luôn cần tách trường hợp riêng!'),
    Beat('outro', 'outro', outro_text(52)),
]

FORMULAS = formulas('17/81', OPTIONS,
                    n='n(Omega) = 9 dot 9 dot 8 = 648',
                    zero='"tận cùng 0:" quad 9 dot 8 = 72',
                    five='"tận cùng 5:" quad 8 dot 8 = 64',
                    prob='P = (72 + 64)/648 = 136/648 = 17/81')


def validate() -> bool:
    nums = [n for n in range(100, 1000) if len(set(str(n))) == 3]
    assert len(nums) == 648 and F(sum(n % 5 == 0 for n in nums), 648) == F(17, 81)
    assert sum(n % 10 == 0 for n in nums) == 72 and sum(n % 10 == 5 for n in nums) == 64
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS052(ShortScene):
    N = 52

    def slots(self, labels, colors):
        g = VGroup()
        for lab, col in zip(labels, colors):
            c = card(1.6, 1.6, col, PANEL, stroke_width=4)
            g.add(VGroup(c, self.TM(lab, 34, col, bold=True).move_to(c)))
        return g.arrange(buff=.3).move_to([0, 1.5, 0])

    def hook_visual(self, t0):
        self.s = self.slots(['$?$', '$?$', '$?$'], [STROKE] * 3)
        names = VGroup(*[tx(n, 22, SOFT).next_to(b, DOWN, buff=.12) for n, b in zip(('trăm', 'chục', 'đơn vị'), self.s)])
        self.names = names
        self.wait_until(.45, t0)
        self.play(FadeIn(self.s, lag_ratio=.2), FadeIn(names), run_time=self.rt(.2))

    def swap(self, labels, colors):
        new = self.slots(labels, colors)
        self.play(*[m.animate.set_opacity(0) for m in self.s], FadeIn(new), run_time=self.rt(.06))
        self.remove(self.s)
        self.s = new

    def beat_s1(self, T):
        t0 = self.now()
        self.swap(['$9$', '$9$', '$8$'], [CYAN] * 3)
        self.wait_until(.6, t0)
        self.board_top = -.95
        self.write_board(self.M('n', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.swap(['$9$', '$8$', '$0$'], [GOLD] * 3)
        self.write_board(self.M('zero', 1.8))
        self.wait_until(.45, t0)
        self.swap(['$8$', '$8$', '$5$'], [CORAL] * 3)
        self.write_board(self.M('five', 1.8))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)

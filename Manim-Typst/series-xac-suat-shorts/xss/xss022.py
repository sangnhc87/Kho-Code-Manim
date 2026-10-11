"""XSS022 · Số chẵn từ 1 đến 5 — 20 số, 8 số chẵn: 2/5 (mẹo: chỉ cần nhìn chữ số cuối)."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, PANEL, SOFT, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS022', 'answer': '2/5'}
PROBLEM = ['Lập số có $2$ chữ số khác nhau từ $1, 2, 3, 4, 5$.', 'Chọn ngẫu nhiên một số. Xác suất số đó chẵn?']
OPTIONS = ['1/2', '2/5', '3/5']
CORRECT = 1
ANSWER_VALUE = .4

BEATS = [
    Beat('hook', 'hook', 'Từ năm chữ số một, hai, ba, bốn, năm, lập các số có hai chữ số khác nhau. '
                         'Chọn ngẫu nhiên một số. Xác suất số đó chẵn là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần năm, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm không gian mẫu: chữ số hàng chục có năm cách chọn, hàng đơn vị còn bốn cách. '
                        'Năm nhân bốn bằng hai mươi số.'),
    Beat('s2', 'solve', 'Số chẵn khi chữ số cuối là hai hoặc bốn: hai cách. Hàng chục còn bốn cách. '
                        'Hai nhân bốn bằng tám số chẵn. Xác suất bằng tám phần hai mươi, tức hai phần năm.'),
    Beat('s3', 'solve', 'Mẹo nhanh: chữ số cuối là một trong năm chữ số, khả năng như nhau, và có hai chữ số chẵn. '
                        'Nên xác suất là hai phần năm ngay lập tức!'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm, không phải một phần hai, vì trong năm chữ số chỉ có hai chữ số chẵn.'),
    Beat('outro', 'outro', outro_text(22)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    n='n(Omega) = 5 dot 4 = 20',
                    a='n(A) = 2 dot 4 = 8',
                    prob='P(A) = 8/20 = 2/5')


def validate() -> bool:
    nums = list(permutations(range(1, 6), 2))
    assert len(nums) == 20 and Fraction(sum(b % 2 == 0 for _, b in nums), 20) == Fraction(2, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS022(ShortScene):
    N = 22

    def hook_visual(self, t0):
        self.digits = VGroup(*[token(str(d), GOLD if d % 2 == 0 else SOFT, .42) for d in range(1, 6)]) \
            .arrange(buff=.3).move_to([0, 2.3, 0])
        self.slots = VGroup(*[card(1.8, 1.7, STROKE, PANEL, stroke_width=3) for _ in range(2)]).arrange(buff=.4) \
            .move_to([0, .75, 0])
        names = VGroup(tx('chục', 30, SOFT).move_to(self.slots[0]),
                       tx('đơn vị', 30, SOFT).move_to(self.slots[1]))
        self.names = names
        self.wait_until(.35, t0)
        self.play(FadeIn(self.digits, lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(self.slots), FadeIn(names), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        five = self.TM('$5$ cách', 30, GOLD, bold=True).next_to(self.slots[0], DOWN, buff=.2)
        four = self.TM('$4$ cách', 30, GOLD, bold=True).next_to(self.slots[1], DOWN, buff=.2)
        self.play(FadeIn(five), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        self.play(FadeIn(four), run_time=self.rt(.08))
        self.counts = VGroup(five, four)
        self.wait_until(.55, t0)
        self.board_top = -1.0
        self.write_board(self.M('n', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.counts.animate.set_opacity(0), run_time=self.rt(.03))
        two = self.TM('$2$ cách', 30, GOLD, bold=True).next_to(self.slots[1], DOWN, buff=.2)
        four = self.TM('$4$ cách', 30, SOFT, bold=True).next_to(self.slots[0], DOWN, buff=.2)
        self.play(FadeIn(two), self.slots[1].animate.set_stroke(GOLD, 5), run_time=self.rt(.08))
        self.wait_until(.25, t0)
        self.play(FadeIn(four), run_time=self.rt(.06))
        self.write_board(self.M('a', 2.0))
        self.wait_until(.65, t0)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.play(*[d.animate.scale(1.25) for d in (self.digits[1], self.digits[3])], run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.clear_board(.03)
        self.write_board(tx('chữ số cuối: 2 chẵn / 5 chữ số', 30, GOLD, bold=True), anim='fade')

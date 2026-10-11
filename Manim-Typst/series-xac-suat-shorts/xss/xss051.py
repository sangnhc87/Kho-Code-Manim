"""XSS051 · Không ngồi cạnh nhau — 5 bạn: 1 − 2·4!/5! = 1 − 2/5 = 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path

from manim import DOWN, FadeIn, RoundedRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS051', 'answer': '3/5'}
PROBLEM = ['Xếp ngẫu nhiên $5$ bạn vào $5$ ghế',
           'hàng ngang. Xác suất A và B',
           'KHÔNG ngồi cạnh nhau?']
OPTIONS = ['2/5', '3/5', '4/5']
CORRECT = 1
ANSWER_VALUE = .6
COLOR = {'A': GOLD, 'B': CYAN, 'C': CORAL, 'D': PURPLE, 'E': GREEN}

BEATS = [
    Beat('hook', 'hook', 'Năm bạn ngồi ngẫu nhiên vào năm ghế xếp hàng ngang. A và B vừa giận nhau. '
                         'Xác suất A và B không phải ngồi cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, ba phần năm, hay bốn phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm trường hợp ngược lại dễ hơn: A và B ngồi cạnh nhau. Gộp A B thành một khối, '
                        'cùng ba bạn còn lại là bốn phần tử, xếp được bốn giai thừa bằng hai mươi bốn cách.'),
    Beat('s2', 'solve', 'Trong khối, A và B đổi chỗ được hai cách, nên có bốn mươi tám cách ngồi cạnh nhau, '
                        'trên tổng số năm giai thừa bằng một trăm hai mươi cách. Xác suất cạnh nhau là hai phần năm.'),
    Beat('s3', 'solve', 'Vậy xác suất không ngồi cạnh nhau bằng một trừ hai phần năm, bằng ba phần năm. '
                        'Gộp khối để đếm cạnh nhau, rồi lấy biến cố đối để ra không cạnh nhau.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Không cạnh nhau: tính cạnh nhau trước, rồi lấy một trừ!'),
    Beat('outro', 'outro', outro_text(51)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    block='n("cạnh") = 4! dot 2! = 48',
                    near='P("cạnh") = 48/120 = 2/5',
                    prob='P = 1 - 2/5 = 3/5')


def validate() -> bool:
    perms = list(permutations('ABCDE'))
    assert F(sum(abs(p.index('A') - p.index('B')) != 1 for p in perms), len(perms)) == F(3, 5)
    assert factorial(4) * 2 == 48
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS051(ShortScene):
    N = 51

    def hook_visual(self, t0):
        self.line = VGroup(*[token(c, COLOR[c], .48) for c in 'ACDBE']).arrange(buff=.3).move_to([0, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.line, lag_ratio=.2), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        new = VGroup(VGroup(token('A', COLOR['A'], .48), token('B', COLOR['B'], .48)).arrange(buff=.06),
                     *[token(c, COLOR[c], .48) for c in 'CDE']).arrange(buff=.35).move_to([0, 1.3, 0])
        blk = RoundedRectangle(width=new[0].width + .25, height=1.25, corner_radius=.22, stroke_color=SOFT,
                               stroke_width=5).move_to(new[0])
        self.play(FadeIn(new), self.line.animate.set_opacity(0), run_time=self.rt(.08))
        self.remove(self.line)
        self.play(FadeIn(blk), FadeIn(tx('khối', 24, SOFT).next_to(blk, DOWN, buff=.12)), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        self.write_board(self.M('block', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('near', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)

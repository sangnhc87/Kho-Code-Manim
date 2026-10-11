"""XSS028 · Đứng cạnh nhau — 4 bạn, A và B cạnh nhau: gộp khối 3!·2!/4! = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import permutations
from math import factorial
from pathlib import Path

from manim import DOWN, FadeIn, FadeOut, RoundedRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS028', 'answer': '1/2'}
PROBLEM = ['Xếp ngẫu nhiên $4$ bạn thành hàng.', 'Xác suất hai bạn A và B đứng cạnh nhau?']
OPTIONS = ['1/4', '1/3', '1/2']
CORRECT = 2
ANSWER_VALUE = .5
COLOR = {'A': GOLD, 'B': CYAN, 'C': CORAL, 'D': PURPLE}

BEATS = [
    Beat('hook', 'hook', 'Bốn bạn xếp hàng ngẫu nhiên để chụp ảnh. A và B là bạn thân. '
                         'Xác suất A và B đứng cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn bạn xếp hàng có bốn giai thừa, bằng hai mươi bốn cách, mỗi cách đồng khả năng.'),
    Beat('s2', 'solve', 'Mẹo gộp khối: buộc A và B thành một khối. Khối này cùng C và D là ba phần tử, '
                        'xếp được ba giai thừa bằng sáu cách. Trong khối, A và B đổi chỗ được hai cách.'),
    Beat('s3', 'solve', 'Số cách thuận lợi: sáu nhân hai bằng mười hai. Xác suất bằng mười hai phần hai mươi bốn, '
                        'tức một phần hai. Lớn hơn bạn nghĩ, đúng không?'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Hàng càng ngắn, hai người càng dễ đứng cạnh nhau.'),
    Beat('outro', 'outro', outro_text(28)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    n='n(Omega) = 4! = 24',
                    block='n(A) = 3! dot 2! = 12',
                    prob='P = 12/24 = 1/2')


def validate() -> bool:
    perms = list(permutations('ABCD'))
    assert Fraction(sum(abs(p.index('A') - p.index('B')) == 1 for p in perms), len(perms)) == Fraction(1, 2)
    assert factorial(3) * factorial(2) == 12
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS028(ShortScene):
    N = 28

    def hook_visual(self, t0):
        self.line = VGroup(*[token(ch, COLOR[ch], .55) for ch in 'CADB']).arrange(buff=.3).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.line, lag_ratio=.25), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('n', 2.3))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        new = VGroup(VGroup(token('A', COLOR['A'], .55), token('B', COLOR['B'], .55)).arrange(buff=.08),
                     token('C', COLOR['C'], .55), token('D', COLOR['D'], .55)).arrange(buff=.45).move_to([0, 1.3, 0])
        blk = RoundedRectangle(width=new[0].width + .3, height=1.45, corner_radius=.25, stroke_color=GREEN,
                               stroke_width=5).move_to(new[0])
        lab = tx('1 khối', 28, GREEN, bold=True).next_to(blk, DOWN, buff=.15)
        self.play(FadeOut(self.line), FadeIn(new), run_time=self.rt(.1))
        self.play(FadeIn(blk), FadeIn(lab), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        self.write_board(self.M('block', 2.2))
        self.write_board(tx('3! cách xếp khối, 2! cách trong khối', 24, SOFT), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

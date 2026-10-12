"""XSS284 · Ếch trên hình vuông — đỉnh chẵn/lẻ xen kẽ; đỉnh đối diện ⇔ tổng bước ≡ 2 (mod 4): 8/16 = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, STROKE  # noqa: E402
from xss._frogkit import frog  # noqa: E402

EPISODE = {'code': 'XSS284', 'answer': '1/2'}
PROBLEM = ['Ếch ở một đỉnh hình vuông, mỗi bước nhảy',
           'sang một trong hai đỉnh kề. Xác suất sau',
           '$4$ bước ếch ở đỉnh đối diện?']
OPTIONS = ['1/4', '1/2', '3/8']
CORRECT = 1
ANSWER_VALUE = .5

BEATS = [
    Beat('hook', 'hook', 'Ếch đứng ở một đỉnh hình vuông, mỗi bước nhảy sang một trong hai đỉnh kề. Sau bốn bước, xác suất ếch ở đỉnh đối diện là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần hai, hay ba phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tô màu xen kẽ bốn đỉnh. Mỗi bước ếch đổi màu, nên sau bốn bước ếch ở lại màu ban đầu: chỉ có thể ở đỉnh xuất phát hoặc đỉnh đối diện.'),
    Beat('s2', 'solve', 'Đánh số đỉnh theo vòng. Mỗi bước cộng hoặc trừ một, theo modulo bốn. Đỉnh đối diện ứng với tổng bằng hai hoặc trừ hai: '
                        'ba bước một chiều, một bước chiều kia: tám dãy.'),
    Beat('s3', 'solve', 'Về gốc ứng với tổng bằng không hoặc cộng trừ bốn: tám dãy còn lại. Mỗi bên tám trên mười sáu, tức một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Tô màu chẵn lẻ giúp loại ngay nửa số đỉnh không thể tới!'),
    Beat('outro', 'outro', outro_text(284)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    cnt='S equiv 2 space "(mod 4)": C_4^1 + C_4^3 = 8',
                    prob='P = 8/16 = 1/2')


def validate() -> bool:
    assert F(sum(sum(w) % 4 == 2 for w in product((1, -1), repeat=4)), 16) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS284(ShortScene):
    N = 284

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.sq = Square(side_length=2.6, stroke_color=STROKE, stroke_width=4).move_to([0, 1.4, 0])
        self.v = self.sq.get_vertices()
        self.dots = VGroup(*[Square(side_length=.38, fill_color=CYAN if i % 2 == 0 else GOLD, fill_opacity=1, stroke_width=0).move_to(p)
                             for i, p in enumerate(self.v)])
        self.fr = frog(.2).move_to(self.v[0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.sq), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.dots), run_time=self.rt(.06))
        self.bring_to_front(self.fr)
        for k in (1, 2, 1, 2):
            self.play(self.fr.animate.move_to(self.v[k]), run_time=self.rt(.04))
        self.wait_until(.6, t0)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('cnt', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)



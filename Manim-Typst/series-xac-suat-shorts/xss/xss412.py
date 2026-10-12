"""XSS412 · Đồng xu trên nền gạch — tâm đồng xu đều trong ô 4 × 4; nằm gọn ⇔ tâm cách mọi cạnh ≥ 1: hình vuông 2 × 2 → 4/16 = 1/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Circle, Dot, FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, STROKE  # noqa: E402

EPISODE = {'code': 'XSS412', 'answer': '1/4'}
PROBLEM = ['Ném đồng xu bán kính $1$ lên nền gạch ô',
           'vuông cạnh $4$. Xác suất đồng xu nằm gọn',
           'trong một ô gạch?']
OPTIONS = ['1/4', '1/2', '9/16']
CORRECT = 0
ANSWER_VALUE = .25
U = .8  # one unit on screen

BEATS = [
    Beat('hook', 'hook', 'Ném một đồng xu bán kính một xăng ti mét lên nền gạch gồm các ô vuông cạnh bốn xăng ti mét. '
                         'Xác suất đồng xu nằm gọn trong một ô, không chạm đường ron?'),
    Beat('guess', 'hook', 'Một phần tư, một phần hai, hay chín phần mười sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đồng xu được xác định bởi tâm. Do lặp lại, chỉ cần xét tâm rơi đều trong một ô vuông cạnh bốn.'),
    Beat('s2', 'solve', 'Nằm gọn nghĩa là tâm cách mọi cạnh của ô ít nhất một. Vùng đó là hình vuông nhỏ cạnh bốn trừ hai, bằng hai.'),
    Beat('s3', 'solve', 'Tỉ số diện tích: hai bình phương chia bốn bình phương, bằng bốn phần mười sáu, tức một phần tư.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Đây là bài toán Buffon phiên bản đồng xu, nền của trò chơi ném xu ở hội chợ.'),
    Beat('outro', 'outro', outro_text(412)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    side='4 - 2 dot 1 = 2',
                    prob='P = 2^2/4^2 = 1/4')


def validate() -> bool:
    assert F(2 ** 2, 4 ** 2) == F(1, 4)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS412(ShortScene):
    N = 412

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.tile = Square(4 * U, stroke_color=STROKE, stroke_width=5).move_to([0, .9, 0])
        self.coin = VGroup(Circle(radius=U, color=GOLD, fill_opacity=.5), Dot(radius=.06, color=GOLD)).move_to([.5, 1.3, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.tile), FadeIn(self.coin), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.coin[0].animate.set_opacity(.15), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.inner = Square(2 * U, stroke_width=0, fill_color=GREEN, fill_opacity=.5).move_to([0, .9, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.inner), run_time=self.rt(.06))
        bad = VGroup(Circle(radius=U, color=CORAL, fill_opacity=.3), Dot(radius=.06, color=CORAL)).move_to([1.5 * U * 1.2, .9 + 1.6 * U, 0])
        self.play(FadeIn(bad), run_time=self.rt(.05))
        self.write_board(self.M('side', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

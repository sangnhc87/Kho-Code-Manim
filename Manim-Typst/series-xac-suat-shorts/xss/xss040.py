"""XSS040 · Chẵn hoặc lớn hơn 3 — {2;4;6} ∪ {4;5;6} = {2;4;5;6}: 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import die_row  # noqa: E402

EPISODE = {'code': 'XSS040', 'answer': '2/3'}
PROBLEM = ['Gieo một con xúc xắc.', 'Xác suất ra số chẵn hoặc số lớn hơn $3$?']
OPTIONS = ['1', '2/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 2 / 3

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc. Xác suất ra số chẵn hoặc số lớn hơn ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Bằng một, hai phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Số chẵn: hai, bốn, sáu, xác suất một phần hai. Lớn hơn ba: bốn, năm, sáu, cũng một phần hai. '
                        'Cộng lại bằng một, tức chắc chắn xảy ra? Rõ ràng mặt một thì không thỏa!'),
    Beat('s2', 'solve', 'Hai biến cố này không xung khắc: bốn và sáu vừa chẵn vừa lớn hơn ba. '
                        'Phần chung có xác suất hai phần sáu, phải trừ đi.'),
    Beat('s3', 'solve', 'Ba phần sáu cộng ba phần sáu trừ hai phần sáu bằng bốn phần sáu, tức hai phần ba. '
                        'Kiểm tra trực tiếp: các mặt thỏa là hai, bốn, năm, sáu, đúng bốn mặt.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Chỉ được cộng thẳng khi hai biến cố xung khắc, tức không có phần chung.'),
    Beat('outro', 'outro', outro_text(40)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    wrong='1/2 + 1/2 = 1 quad coral(times)',
                    both='A B = {4; 6}',
                    prob='P = 3/6 + 3/6 - 2/6 = 4/6 = 2/3')


def validate() -> bool:
    assert Fraction(sum(v % 2 == 0 or v > 3 for v in range(1, 7)), 6) == Fraction(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS040(ShortScene):
    N = 40

    def hook_visual(self, t0):
        self.row = die_row(s=.95).move_to([0, 1.4, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.row, lag_ratio=.15), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        even = VGroup(self.row[1], self.row[3], self.row[5])
        self.play(*[d[0].animate.set_stroke(CYAN, 6) for d in even], run_time=self.rt(.06))
        self.play(FadeIn(tx('chẵn', 28, CYAN, bold=True).next_to(self.row, UP, buff=.25)), run_time=self.rt(.04))
        self.wait_until(.35, t0)
        self.play(*[self.row[i].animate.shift(UP * -.3) for i in (3, 4, 5)], run_time=self.rt(.06))
        self.play(FadeIn(tx('lớn hơn 3', 28, CORAL, bold=True).next_to(self.row[4], [0, -1, 0], buff=.25)),
                  run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.write_board(self.M('wrong', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[self.row[i][0].animate.set_fill(GOLD, 1) for i in (3, 5)], run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.write_board(self.M('both', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)

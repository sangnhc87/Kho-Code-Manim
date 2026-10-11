"""XSS002 · Mặt chẵn — không gian mẫu 6 mặt, biến cố {2; 4; 6}."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import RIGHT, UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import die, die_row, roll_faces  # noqa: E402

EPISODE = {'code': 'XSS002', 'answer': '1/2'}
PROBLEM = ['Gieo một con xúc xắc cân đối.', 'Xác suất ra mặt chẵn bằng bao nhiêu?']
OPTIONS = ['1/6', '1/3', '1/2']
CORRECT = 2
ANSWER_VALUE = .5

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc. Mặt chẵn hay mặt lẻ dễ ra hơn? '
                         'Và xác suất ra mặt chẵn bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần ba, hay một phần hai? Chọn nhanh! Ba, hai, một!'),
    Beat('s1', 'solve', 'Xúc xắc có sáu mặt, từ một đến sáu chấm. Xúc xắc cân đối nên sáu mặt có khả năng như nhau: '
                        'không gian mẫu có sáu phần tử.'),
    Beat('s2', 'solve', 'Mặt chẵn gồm hai, bốn và sáu chấm: ba kết quả thuận lợi. '
                        'Xác suất bằng ba phần sáu, rút gọn còn một phần hai.'),
    Beat('s3', 'solve', 'Mẹo nhớ nhanh: ba mặt chẵn, ba mặt lẻ, chia đôi đều nhau. '
                        'Nên chẵn và lẻ có cơ hội ngang nhau.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai, đúng bằng xác suất tung đồng xu ra mặt ngửa!'),
    Beat('outro', 'outro', outro_text(2)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    omega='Omega = {1; 2; 3; 4; 5; 6}',
                    nomega='n(Omega) = 6',
                    event='A = {2; 4; 6}',
                    prob='P(A) = 3/6 = 1/2')


def validate() -> bool:
    assert Fraction(sum(v % 2 == 0 for v in range(1, 7)), 6) == Fraction(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS002(ShortScene):
    N = 2

    def hook_visual(self, t0):
        self.d = die(1, 1.9).move_to([0, 1.3, 0])
        self.play(FadeIn(self.d, scale=.6), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.d = self.roll(self.d, roll_faces(4, 7, 2), self.rt(.5))

    def beat_s1(self, T):
        t0 = self.now()
        self.row = die_row(s=.95).move_to([0, 1.5, 0])
        self.play(self.d.animate.scale(.5).move_to(self.row[3]), run_time=self.rt(.06))
        self.remove(self.d)
        self.play(FadeIn(self.row, lag_ratio=.15), run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.write_board(self.M('omega', 1.9))
        self.wait_until(.75, t0)
        self.write_board(self.M('nomega', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        even = VGroup(self.row[1], self.row[3], self.row[5])
        odd = VGroup(self.row[0], self.row[2], self.row[4])
        self.play(even.animate.shift(UP * .35), odd.animate.set_opacity(.3), run_time=self.rt(.08))
        self.play(*[d[0].animate.set_stroke(GOLD, 6) for d in even], run_time=self.rt(.04))
        self.write_board(self.M('event', 1.9))
        self.wait_until(.55, t0)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.clear_board(.03)
        odd = VGroup(self.row[0], self.row[2], self.row[4])
        self.play(odd.animate.set_opacity(1), run_time=self.rt(.06))
        labels = VGroup(tx('3 mặt chẵn', 32, GOLD, bold=True), tx('3 mặt lẻ', 32, CYAN, bold=True)) \
            .arrange(RIGHT, buff=.8).move_to([0, .4, 0])
        self.play(FadeIn(labels, shift=UP * .1), run_time=self.rt(.1))
        self.write_board(tx('cơ hội ngang nhau', 34, SOFT), anim='fade')

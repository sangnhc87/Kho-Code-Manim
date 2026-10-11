"""XSS008 · Chắc chắn và không thể — P = 1 và P = 0, hai đầu mút của thang xác suất."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import PI, UP, FadeIn, Triangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import cross, tx  # noqa: E402
from common.short import BOARD_X, PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN  # noqa: E402
from common.visuals import die_row  # noqa: E402

EPISODE = {'code': 'XSS008', 'answer': '1 và 0'}
PROBLEM = ['Gieo một con xúc xắc.', 'Tính $P("số chấm" <= 6)$ và $P("số chấm" = 7)$.']
OPTIONS = ['1 " và " 0', '0 " và " 1', '1/6 " và " 1/6']
CORRECT = 0
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc. Xác suất được số chấm nhỏ hơn hoặc bằng sáu là bao nhiêu? '
                         'Còn xác suất được bảy chấm thì sao?'),
    Beat('guess', 'hook', 'Một và không, không và một, hay cả hai bằng một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mặt nào cũng có từ một đến sáu chấm, nên cả sáu kết quả đều thuận lợi. '
                        'Sáu phần sáu bằng một: đây là biến cố chắc chắn.'),
    Beat('s2', 'solve', 'Không mặt nào có bảy chấm, nên không có kết quả thuận lợi nào. '
                        'Không phần sáu bằng không: đây là biến cố không thể.'),
    Beat('s3', 'solve', 'Mọi xác suất đều nằm giữa hai đầu mút này: không là không thể, một là chắc chắn. '
                        'Nếu bạn tính ra số âm hoặc lớn hơn một, chắc chắn đã có lỗi ở đâu đó.'),
    Beat('answer', 'solve', 'Đáp án: một và không. Thang xác suất luôn đi từ không đến một!'),
    Beat('outro', 'outro', outro_text(8)),
]

FORMULAS = formulas('1 " và " 0', OPTIONS,
                    sure='P = 6/6 = 1',
                    never='P = 0/6 = 0',
                    range='0 <= P(A) <= 1')


def validate() -> bool:
    faces = range(1, 7)
    assert Fraction(sum(v <= 6 for v in faces), 6) == 1 and Fraction(sum(v == 7 for v in faces), 6) == 0
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS008(ShortScene):
    N = 8

    def hook_visual(self, t0):
        self.row = die_row(s=.95).move_to([0, 1.5, 0])
        self.wait_until(.25, t0)
        self.play(FadeIn(self.row, lag_ratio=.15), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[d[0].animate.set_stroke(GREEN, 6) for d in self.row], run_time=self.rt(.1))
        self.play(FadeIn(tx('cả 6 mặt đều thỏa', 30, GREEN, bold=True).next_to(self.row, UP, buff=.3)),
                  run_time=self.rt(.06))
        self.wait_until(.45, t0)
        m = self.M('sure', 2.2)
        self.write_board(m)
        self.write_board(tx('biến cố chắc chắn', 30, GREEN, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[d[0].animate.set_stroke(CORAL, 6) for d in self.row],
                  *[FadeIn(cross(CORAL, .6).move_to(d)) for d in self.row], run_time=self.rt(.1))
        self.wait_until(.45, t0)
        self.write_board(self.M('never', 2.2))
        self.write_board(tx('biến cố không thể', 30, CORAL, bold=True), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('range', 2.2))
        self.wait_until(.3, t0)
        m = self.meter(1.0, y=-2.55)
        zero = Triangle(fill_color=CORAL, fill_opacity=1, stroke_width=0).scale(.13).rotate(PI)
        zero.move_to([BOARD_X - 3.0, -2.25, 0])
        self.play(FadeIn(m[0]), FadeIn(m[1]), FadeIn(zero), run_time=self.rt(.1))
        self.board_items += [m, zero]
        self.play(m[1][1].animate.set_color(GOLD), run_time=self.rt(.02))

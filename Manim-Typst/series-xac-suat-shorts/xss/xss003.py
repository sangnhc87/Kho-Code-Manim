"""XSS003 · Lớn hơn 4 — "lớn hơn 4" chỉ gồm 5 và 6 (bẫy tính cả mặt 4)."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import die, die_row, roll_faces  # noqa: E402

EPISODE = {'code': 'XSS003', 'answer': '1/3'}
PROBLEM = ['Gieo một con xúc xắc cân đối.', 'Xác suất số chấm lớn hơn $4$?']
OPTIONS = ['1/2', '1/3', '1/6']
CORRECT = 1
ANSWER_VALUE = 1 / 3

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc. Xác suất được số chấm lớn hơn bốn là bao nhiêu? '
                         'Câu này có một cái bẫy rất nhiều bạn dính.'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Không gian mẫu vẫn là sáu mặt, từ một đến sáu chấm, cả sáu mặt đồng khả năng.'),
    Beat('s2', 'solve', 'Bẫy nằm ở đây: lớn hơn bốn thì không tính mặt bốn. '
                        'Chỉ có năm và sáu chấm, tức hai kết quả thuận lợi.'),
    Beat('s3', 'solve', 'Xác suất bằng hai phần sáu, rút gọn còn một phần ba. '
                        'Nếu đề hỏi lớn hơn hoặc bằng bốn, đáp án sẽ là một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Luôn đọc kỹ chữ lớn hơn và lớn hơn hoặc bằng nhé!'),
    Beat('outro', 'outro', outro_text(3)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    nomega='n(Omega) = 6',
                    event='A = {5; 6}',
                    prob='P(A) = 2/6 = 1/3',
                    ge='P("số chấm" >= 4) = 3/6 = 1/2')


def validate() -> bool:
    assert Fraction(sum(v > 4 for v in range(1, 7)), 6) == Fraction(1, 3)
    assert Fraction(sum(v >= 4 for v in range(1, 7)), 6) == Fraction(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS003(ShortScene):
    N = 3

    def hook_visual(self, t0):
        self.d = die(1, 1.9).move_to([0, 1.3, 0])
        self.play(FadeIn(self.d, scale=.6), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.d = self.roll(self.d, roll_faces(5, 6, 3), self.rt(.4))

    def beat_s1(self, T):
        t0 = self.now()
        self.row = die_row(s=.95).move_to([0, 1.5, 0])
        self.play(self.d.animate.scale(.5).move_to(self.row[4]), run_time=self.rt(.08))
        self.remove(self.d)
        self.play(FadeIn(self.row, lag_ratio=.15), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.write_board(self.M('nomega', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        four = self.row[3]
        x = cross(CORAL, .9).move_to(four)
        self.play(four.animate.set_opacity(.35), FadeIn(x, scale=1.4), run_time=self.rt(.08))
        self.play(FadeIn(tx('không tính mặt 4!', 30, CORAL, bold=True).next_to(four, UP, buff=.25)),
                  run_time=self.rt(.05))
        self.wait_until(.5, t0)
        hi = VGroup(self.row[4], self.row[5])
        self.play(hi.animate.shift(UP * .35), *[d[0].animate.set_stroke(GOLD, 6) for d in hi],
                  VGroup(*self.row[:3]).animate.set_opacity(.3), run_time=self.rt(.08))
        self.write_board(self.M('event', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('ge', 1.6), anim='fade')

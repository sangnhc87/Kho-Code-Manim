"""XSS010 · Biến cố đối — P(không ra 6) = 1 − 1/6 = 5/6."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402
from common.visuals import die, die_row, roll_faces  # noqa: E402

EPISODE = {'code': 'XSS010', 'answer': '5/6'}
PROBLEM = ['Gieo một con xúc xắc.', 'Xác suất KHÔNG ra mặt $6$?']
OPTIONS = ['1/6', '5/6', '1']
CORRECT = 1
ANSWER_VALUE = 5 / 6

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc. Xác suất không ra mặt sáu là bao nhiêu? '
                         'Có một cách tính cực nhanh mà dân thi cử nào cũng nên biết.'),
    Beat('guess', 'hook', 'Một phần sáu, năm phần sáu, hay bằng một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cách đếm trực tiếp: các mặt không phải sáu là một, hai, ba, bốn và năm, tức năm kết quả. '
                        'Xác suất bằng năm phần sáu.'),
    Beat('s2', 'solve', 'Cách nhanh hơn: ra mặt sáu và không ra mặt sáu là hai biến cố đối nhau. '
                        'Luôn có đúng một trong hai xảy ra, nên tổng xác suất của chúng bằng một.'),
    Beat('s3', 'solve', 'Vậy xác suất không ra sáu bằng một trừ một phần sáu, bằng năm phần sáu. '
                        'Mẹo này cực mạnh với những bài có chữ ít nhất.'),
    Beat('answer', 'solve', 'Đáp án: năm phần sáu. Nhớ công thức: xác suất biến cố đối bằng một trừ xác suất biến cố.'),
    Beat('outro', 'outro', outro_text(10)),
]

FORMULAS = formulas('5/6', OPTIONS,
                    direct='P = 5/6',
                    comp='P(overline(A)) = 1 - P(A)',
                    calc='P(overline(A)) = 1 - 1/6 = 5/6')


def validate() -> bool:
    assert Fraction(sum(v != 6 for v in range(1, 7)), 6) == 1 - Fraction(1, 6) == Fraction(5, 6)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS010(ShortScene):
    N = 10

    def hook_visual(self, t0):
        self.d = die(1, 1.9).move_to([0, 1.3, 0])
        self.play(FadeIn(self.d, scale=.6), run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.d = self.roll(self.d, roll_faces(6, 6, 10), self.rt(.4))

    def beat_s1(self, T):
        t0 = self.now()
        self.row = die_row(s=.95).move_to([0, 1.5, 0])
        self.play(self.d.animate.scale(.5).move_to(self.row[5]), run_time=self.rt(.05))
        self.remove(self.d)
        self.play(FadeIn(self.row, lag_ratio=.12), run_time=self.rt(.1))
        x = cross(CORAL, .7).move_to(self.row[5])
        self.play(self.row[5].animate.set_opacity(.35), FadeIn(x, scale=1.4),
                  *[d[0].animate.set_stroke(GREEN, 5) for d in self.row[:5]], run_time=self.rt(.1))
        self.x6 = x
        self.wait_until(.6, t0)
        self.write_board(self.M('direct', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        a = tx('ra mặt 6', 28, CORAL, bold=True).next_to(self.row[5], UP, buff=.3)
        b = tx('không ra mặt 6', 28, GREEN, bold=True).next_to(VGroup(*self.row[:5]), UP, buff=.3)
        self.play(FadeIn(a), FadeIn(b), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        m = self.M('comp', 2.2)
        self.write_board(m)
        self.frame(m, CYAN)

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('calc', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('dùng cho bài "ít nhất"', 28, CYAN), anim='fade')

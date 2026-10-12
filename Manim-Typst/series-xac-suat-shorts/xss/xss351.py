"""XSS351 · Hai dãy ghế đối diện — 3 cột × 2 ghế; C(6;3) = 20 cách chọn ghế cho nam; mỗi cột một nam một nữ: 2³ = 8 → 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, FadeOut, SurroundingRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss._seatkit import seat, seat_row  # noqa: E402

EPISODE = {'code': 'XSS351', 'answer': '2/5'}
PROBLEM = ['Hai dãy ghế đối diện, mỗi dãy $3$ ghế;',
           '$3$ nam $3$ nữ ngồi ngẫu nhiên. Xác suất',
           'nam nào cũng ngồi đối diện một nữ?']
OPTIONS = ['2/5', '1/5', '1/10']
CORRECT = 0
ANSWER_VALUE = .4
P_ = {'M': ('Na', CYAN), 'F': ('Nữ', CORAL)}

BEATS = [
    Beat('hook', 'hook', 'Hai dãy ghế đối diện nhau, mỗi dãy ba ghế. Ba nam và ba nữ ngồi ngẫu nhiên. '
                         'Xác suất bạn nam nào cũng ngồi đối diện một bạn nữ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, một phần năm, hay một phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Sáu ghế chia thành ba cặp đối diện. Chọn ba ghế cho nam: hai mươi cách đồng khả năng.'),
    Beat('s2', 'solve', 'Nam nào cũng đối diện nữ nghĩa là mỗi cặp ghế có đúng một nam. Mỗi cặp chọn nam ngồi phía trên hay phía dưới: hai mũ ba, tám cách.'),
    Beat('s3', 'solve', 'Xác suất tám phần hai mươi, bằng hai phần năm.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Gom ghế thành các cặp đối diện, bài toán trở về chọn một trong hai cho mỗi cặp.'),
    Beat('outro', 'outro', outro_text(351)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    all='C_6^3 = 20',
                    good='2^3 = 8',
                    prob='P = 8/20 = 2/5')


def validate() -> bool:
    orders = set(permutations('MMMFFF'))
    good = sum(all(o[i] != o[i + 3] for i in range(3)) for o in orders)
    assert good == 8 and F(good, len(orders)) == F(2, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS351(ShortScene):
    N = 351

    def place(self, pattern, frac=.06):
        new = seat([P_[c] for c in pattern], list(self.top) + list(self.bot))
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.top = seat_row(3, y=2.0, gap=.6)
        self.bot = seat_row(3, y=.6, gap=.6)
        self.play(FadeIn(self.top), FadeIn(self.bot), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.place('MMFFMF')

    def beat_s1(self, T):
        t0 = self.now()
        cols = VGroup(*[SurroundingRectangle(VGroup(self.top[i], self.bot[i]), color=GOLD, buff=.12) for i in range(3)])
        self.play(FadeIn(cols), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.place('MFMFMF', .05)
        self.wait_until(.6, t0)
        self.place('FFMMMF', .05)
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

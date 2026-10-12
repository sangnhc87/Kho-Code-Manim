"""XSS346 · Ba gia đình — 3 nhà × 2 người vào dãy 6 ghế: buộc mỗi nhà thành khối: 3! · 2³ = 48 / 720 = 1/15."""
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

EPISODE = {'code': 'XSS346', 'answer': '1/15'}
PROBLEM = ['$3$ gia đình, mỗi nhà $2$ người, ngồi ngẫu',
           'nhiên vào dãy $6$ ghế. Xác suất ai cũng',
           'ngồi cạnh người nhà mình?']
OPTIONS = ['1/15', '1/20', '1/10']
CORRECT = 0
ANSWER_VALUE = 1 / 15
FAM = {'A': ('A', CYAN), 'B': ('B', CORAL), 'C': ('C', GOLD)}

BEATS = [
    Beat('hook', 'hook', 'Ba gia đình, mỗi nhà hai người, ngồi ngẫu nhiên vào một dãy sáu ghế. '
                         'Xác suất ai cũng ngồi cạnh người nhà mình là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười lăm, một phần hai mươi, hay một phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Sáu người khác nhau ngồi vào sáu ghế: sáu giai thừa, bảy trăm hai mươi cách.'),
    Beat('s2', 'solve', 'Để mỗi nhà ngồi cạnh nhau, buộc mỗi nhà thành một khối. Ba khối xếp được ba giai thừa cách, trong mỗi khối hai người đổi chỗ được hai cách: sáu nhân tám, bốn mươi tám.'),
    Beat('s3', 'solve', 'Xác suất bốn mươi tám phần bảy trăm hai mươi, tức một phần mười lăm.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười lăm. Buộc khối là kỹ thuật chuẩn cho mọi bài ngồi cạnh nhau.'),
    Beat('outro', 'outro', outro_text(346)),
]

FORMULAS = formulas('1/15', OPTIONS,
                    all='6! = 720',
                    blocks='3! dot 2^3 = 48',
                    prob='P = 48/720 = 1/15')


def validate() -> bool:
    good = sum(all(abs(p.index(2 * k) - p.index(2 * k + 1)) == 1 for k in range(3)) for p in permutations(range(6)))
    assert good == 48 and F(good, 720) == F(1, 15)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS346(ShortScene):
    N = 346

    def place(self, pattern, frac=.06):
        new = seat([FAM[c] for c in pattern], self.seats)
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.seats = seat_row(6, y=1.3)
        self.play(FadeIn(self.seats), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.place('ABCABC')

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.place('BBAACC', .06)
        blocks = VGroup(*[SurroundingRectangle(VGroup(self.seats[2 * i], self.seats[2 * i + 1]), color=GOLD, buff=.08) for i in range(3)])
        self.play(FadeIn(blocks), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        self.write_board(self.M('blocks', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS358 · Hai toa bốn chỗ — An ngồi đâu đó; 7 chỗ còn lại như nhau cho Bình, 3 chỗ cùng toa với An → 3/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402
from common.visuals import token  # noqa: E402
from xss._seatkit import seat_row, train  # noqa: E402

EPISODE = {'code': 'XSS358', 'answer': '3/7'}
PROBLEM = ['$8$ người xếp ngẫu nhiên vào $2$ toa, mỗi',
           'toa $4$ chỗ. Xác suất An và Bình ngồi',
           'cùng một toa?']
OPTIONS = ['3/7', '1/2', '4/7']
CORRECT = 0
ANSWER_VALUE = 3 / 7

BEATS = [
    Beat('hook', 'hook', 'Tám người xếp ngẫu nhiên vào hai toa tàu, mỗi toa bốn chỗ. Xác suất An và Bình ngồi cùng một toa là bao nhiêu? Nhiều bạn đoán ngay một nửa.'),
    Beat('guess', 'hook', 'Ba phần bảy, một phần hai, hay bốn phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cho An ngồi trước, ở đâu cũng được. Bình nhận một trong bảy chỗ còn lại, các chỗ đều đồng khả năng.'),
    Beat('s2', 'solve', 'Toa của An còn ba chỗ trống, toa kia có bốn chỗ. Bình cùng toa với An với xác suất ba phần bảy.'),
    Beat('s3', 'solve', 'Không phải một nửa, vì An đã chiếm mất một chỗ trong toa của mình.'),
    Beat('answer', 'solve', 'Đáp án: ba phần bảy. Đặt một người trước, rồi đếm chỗ còn lại cho người kia.'),
    Beat('outro', 'outro', outro_text(358)),
]

FORMULAS = formulas('3/7', OPTIONS,
                    prob='P = 3/7')


def validate() -> bool:
    good = sum((p.index(0) < 4) == (p.index(1) < 4) for p in permutations(range(8)))
    assert F(good, 40320) == F(3, 7)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS358(ShortScene):
    N = 358

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.cars = train(2, y=1.3, w=3.2, h=1.3, scene=self)
        self.slots = VGroup(*[seat_row(4, w=.55, gap=.12).move_to(c[0]) for c in self.cars])
        self.play(FadeIn(self.cars), FadeIn(self.slots), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.an = token('An', CYAN, .26).move_to(self.slots[0][1])
        self.play(FadeIn(self.an, scale=1.4), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        free = [s for i, row in enumerate(self.slots) for j, s in enumerate(row) if (i, j) != (0, 1)]
        self.play(*[s.animate.set_stroke(CORAL, 4) for s in free], run_time=self.rt(.06))
        self.free = free

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.play(*[s.animate.set_fill(GREEN, .6) for s in self.free[:3]], run_time=self.rt(.06))
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(self.an.animate.scale(1.3), run_time=self.rt(.05))

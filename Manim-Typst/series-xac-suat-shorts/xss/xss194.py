"""XSS194 · Viên bi cuối cùng — mọi vị trí như nhau: P(bi cuối xanh) = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, PANEL, SOFT  # noqa: E402
from common.visuals import ball, urn  # noqa: E402

EPISODE = {'code': 'XSS194', 'answer': '3/8'}
PROBLEM = ['Hộp $5$ đỏ $3$ xanh, rút lần lượt không',
           'hoàn lại đến hết. Xác suất viên',
           'bi cuối cùng màu xanh?']
OPTIONS = ['1/8', '3/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 3 / 8

BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đỏ và ba bi xanh. Rút lần lượt từng bi, không hoàn lại, cho đến hết. '
                         'Xác suất viên bi cuối cùng màu xanh là bao nhiêu? Nghe như phải vẽ cây tám tầng?'),
    Beat('guess', 'hook', 'Một phần tám, ba phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Rút lần lượt đến hết chính là xếp tám viên bi thành một hàng ngẫu nhiên. Mọi thứ tự đều đồng khả năng.'),
    Beat('s2', 'solve', 'Vị trí cuối cùng không có gì đặc biệt so với vị trí đầu tiên. Bi ở vị trí đầu là xanh với xác suất ba phần tám, '
                        'nên vị trí cuối cũng vậy.'),
    Beat('s3', 'solve', 'Đếm cho chắc: chọn vị trí cho ba bi xanh có năm mươi sáu cách; vị trí cuối là xanh thì còn hai bi xanh vào bảy vị trí, '
                        'hai mươi mốt cách. Hai mươi mốt phần năm mươi sáu bằng ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Rút đến hết thì mọi vị trí đều bình đẳng, không cần vẽ cây!'),
    Beat('outro', 'outro', outro_text(194)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    sym='P("cuối xanh") = P("đầu xanh") = 3/8',
                    cnt='(C_7^2)/(C_8^3) = 21/56 = 3/8')


def validate() -> bool:
    seqs = set(permutations('RRRRRBBB'))
    assert F(sum(s[-1] == 'B' for s in seqs), len(seqs)) == F(3, 8) == F(21, 56)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS194(ShortScene):
    N = 194

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.u = urn('RRRRRBBB', cols=4, r=.32).move_to([0, 2.2, 0])
        self.slots = VGroup(*[card(.7, .7, SOFT, PANEL, radius=.35, stroke_width=2) for _ in range(8)]).arrange(buff=.12) \
            .move_to([0, .6, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.slots, lag_ratio=.1), run_time=self.rt(.1))
        order = 'RBRRBRRB'
        self.wait_until(.4, t0)
        self.row = VGroup(*[ball(c, .28).move_to(s) for c, s in zip(order, self.slots)])
        self.play(FadeIn(self.row, lag_ratio=.12), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.slots[0].animate.set_stroke(GOLD, 6), self.slots[-1].animate.set_stroke(GOLD, 6), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        m = self.M('sym', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('cnt', 1.9), anim='fade')

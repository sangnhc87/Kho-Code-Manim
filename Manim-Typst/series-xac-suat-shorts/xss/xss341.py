"""XSS341 · Chia bi vào ba hộp — 3 đỏ 3 xanh vào 3 hộp × 2 chỗ: C(6;3) = 20 cách đặt màu; mỗi hộp 1 đỏ 1 xanh: 2³ = 8 → 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS341', 'answer': '2/5'}
PROBLEM = ['Chia ngẫu nhiên $3$ bi đỏ, $3$ bi xanh vào',
           '$3$ hộp, mỗi hộp $2$ bi. Xác suất hộp nào',
           'cũng có $1$ đỏ $1$ xanh?']
OPTIONS = ['2/5', '1/3', '8/27']
CORRECT = 0
ANSWER_VALUE = .4
SPOTS = list(combinations(range(6), 3))   # slots taken by red balls; boxes are slot pairs (0,1), (2,3), (4,5)
GOOD = [s for s in SPOTS if all(len({2 * b, 2 * b + 1} & set(s)) == 1 for b in range(3))]

BEATS = [
    Beat('hook', 'hook', 'Ba bi đỏ và ba bi xanh được chia ngẫu nhiên vào ba hộp, mỗi hộp hai bi. '
                         'Xác suất hộp nào cũng có một đỏ một xanh là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, một phần ba, hay tám phần hai mươi bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Coi ba hộp là sáu chỗ ngồi. Chỉ cần biết ba chỗ nào nhận bi đỏ: tổ hợp chập ba của sáu, hai mươi cách đồng khả năng.'),
    Beat('s2', 'solve', 'Hộp nào cũng một đỏ thì mỗi hộp chọn một trong hai chỗ cho bi đỏ: hai mũ ba, tám cách.'),
    Beat('s3', 'solve', 'Xác suất tám phần hai mươi, tức hai phần năm. Cẩn thận: đáp án tám phần hai mươi bảy là coi nhầm các bi được thả độc lập.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Chia đều vào hộp tương đương xếp hàng vào chỗ ngồi.'),
    Beat('outro', 'outro', outro_text(341)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    all='C_6^3 = 20',
                    good='2^3 = 8',
                    prob='P = 8/20 = 2/5')


def validate() -> bool:
    assert len(SPOTS) == 20 and len(GOOD) == 8
    assert F(len(GOOD), len(SPOTS)) == F(2, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS341(ShortScene):
    N = 341

    def boxes(self, cols):
        return VGroup(*[urn(cols[2 * i:2 * i + 2], cols=2, r=.3) for i in range(3)]).arrange(buff=.5).move_to([0, 1.3, 0])

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.cur = self.boxes('RRBRBB')
        self.wait_until(.5, t0)
        self.play(FadeIn(self.cur, lag_ratio=.2), run_time=self.rt(.1))

    def swap(self, cols, frac=.05):
        new = self.boxes(cols)
        self.play(FadeOut(self.cur), FadeIn(new), run_time=self.rt(frac))
        self.cur = new

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.swap('RBBRRB')
        self.wait_until(.6, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        for f, c in ((.1, 'RBRBRB'), (.35, 'BRRBBR'), (.6, 'RBBRRB')):
            self.wait_until(f, t0)
            self.swap(c, .04)
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS432 · Chia kẹo — nghiệm (a; b; c) ≥ 0 của a + b + c = 10: C(12;2) = 66; nghiệm dương: C(9;2) = 36 → 6/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS432', 'answer': '6/11'}
PROBLEM = ['$10$ viên kẹo giống nhau chia cho $3$ bạn,',
           'mọi cách chia đồng khả năng. Xác suất',
           'bạn nào cũng có kẹo?']
OPTIONS = ['6/11', '1/2', '2/3']
CORRECT = 0
ANSWER_VALUE = 6 / 11
ALL = sum(1 for a in range(11) for b in range(11 - a))
POS = sum(1 for a in range(1, 11) for b in range(1, 11 - a) if 10 - a - b >= 1)

BEATS = [
    Beat('hook', 'hook', 'Mười viên kẹo giống hệt nhau được chia cho ba bạn, và mọi cách chia, tức mọi bộ số kẹo, đồng khả năng. '
                         'Xác suất bạn nào cũng có ít nhất một viên?'),
    Beat('guess', 'hook', 'Sáu phần mười một, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi cách chia là một nghiệm a cộng b cộng c bằng mười với a, b, c không âm. Mẹo chia vách: xếp mười viên kẹo và hai vách ngăn thành một hàng.'),
    Beat('s2', 'solve', 'Chọn hai vị trí cho vách trong mười hai chỗ: sáu mươi sáu cách chia. Bạn nào cũng có kẹo: đặt hai vách vào chín khe giữa các viên kẹo, ba mươi sáu cách.'),
    Beat('s3', 'solve', 'Xác suất ba mươi sáu phần sáu mươi sáu, tức sáu phần mười một.'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười một. Kẹo và vách: công cụ đếm kinh điển cho các vật giống nhau.'),
    Beat('outro', 'outro', outro_text(432)),
]

FORMULAS = formulas('6/11', OPTIONS,
                    all='C_12^2 = 66',
                    pos='C_9^2 = 36',
                    prob='P = 36/66 = 6/11')


def validate() -> bool:
    assert (ALL, POS) == (comb(12, 2), comb(9, 2)) == (66, 36)
    assert F(POS, ALL) == F(6, 11)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS432(ShortScene):
    N = 432

    def hook_visual(self, t0):
        self.board_top = -1.3
        items = VGroup()
        for k in range(12):
            if k in (3, 7):
                items.add(Line([0, -.35, 0], [0, .35, 0], color=CORAL, stroke_width=8))
            else:
                items.add(token(' ', GOLD, .2))
        self.row = items.arrange(buff=.18).move_to([0, 1.3, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(VGroup(*[it for k, it in enumerate(items) if k not in (3, 7)]), lag_ratio=.05), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.play(FadeIn(self.row[3]), FadeIn(self.row[7]), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('all', 1.5))
        self.wait_until(.55, t0)
        self.write_board(self.M('pos', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS331 · Đến khi trùng màu — 3 màu × 2 bi; cần đúng 4 lần ⇔ 3 bi đầu khác màu (lần 4 chắc chắn trùng): 1 · 4/5 · 2/4 = 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS331', 'answer': '2/5'}
PROBLEM = ['Hộp có $3$ màu, mỗi màu $2$ bi. Rút lần',
           'lượt đến khi có $2$ bi cùng màu. Xác suất',
           'cần đúng $4$ lần rút?']
OPTIONS = ['2/5', '1/3', '8/15']
CORRECT = 0
ANSWER_VALUE = .4
ORDERS = set(permutations('RRBBYY'))


def stop(o):
    seen = set()
    for i, c in enumerate(o):
        if c in seen:
            return i + 1
        seen.add(c)


BEATS = [
    Beat('hook', 'hook', 'Hộp có sáu bi: hai đỏ, hai xanh, hai vàng. Rút lần lượt cho đến khi được hai bi cùng màu thì dừng. '
                         'Xác suất phải rút đúng bốn lần là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, một phần ba, hay tám phần mười lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chỉ có ba màu, nên bi thứ tư chắc chắn trùng màu với một bi trước. Vậy cần đúng bốn lần khi và chỉ khi ba bi đầu đôi một khác màu.'),
    Beat('s2', 'solve', 'Bi thứ nhất tùy ý. Bi thứ hai khác màu: bốn trên năm bi còn lại. Bi thứ ba khác cả hai màu trước: hai trên bốn.'),
    Beat('s3', 'solve', 'Nhân lại: một nhân bốn phần năm nhân hai phần tư, bằng hai phần năm.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Nguyên lý chuồng bồ câu cho biết điểm dừng muộn nhất, phần còn lại là nhân xác suất có điều kiện.'),
    Beat('outro', 'outro', outro_text(331)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    pig='"lần 4 luôn trùng màu"',
                    prob='P = 1 dot 4/5 dot 2/4 = 2/5')


def validate() -> bool:
    assert F(sum(stop(o) == 4 for o in ORDERS), len(ORDERS)) == F(2, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS331(ShortScene):
    N = 331

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn('RRBBYY', cols=3, r=.3).move_to([0, 2.0, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))
        self.row = ball_row('RBYB', y=.15, r=.32, buff=.35)
        self.wait_until(.5, t0)
        self.play(FadeIn(self.row, lag_ratio=.4), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.play(self.row[3].animate.scale(1.35), run_time=self.rt(.05))
        self.write_board(self.M('pig', 1.3))

    def beat_s2(self, T):
        t0 = self.now()
        for i, f in enumerate((.1, .35, .7)):
            self.wait_until(f, t0)
            self.play(self.row[i].animate.scale(1.25), run_time=self.rt(.04))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

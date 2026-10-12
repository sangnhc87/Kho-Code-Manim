"""XSS420 · Xếp hàng không có tiền thối — 2 người tờ 10 nghìn (M), 2 người tờ 20 nghìn (H); không ai chờ ⇔ mọi tiền tố có số M ≥ số H: MHMH, MMHH → 2/6 = 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS420', 'answer': '1/3'}
PROBLEM = ['$2$ người cầm tờ $10$ nghìn, $2$ người cầm tờ',
           '$20$ nghìn xếp hàng mua vé $10$ nghìn; quầy',
           'không có tiền lẻ. $P("không ai phải chờ")$?']
OPTIONS = ['1/3', '1/2', '1/6']
CORRECT = 0
ANSWER_VALUE = 1 / 3
ORDERS = sorted(set(permutations('MMHH')))


def ok(o):
    bal = 0
    for c in o:
        bal += 1 if c == 'M' else -1
        if bal < 0:
            return False
    return True


BEATS = [
    Beat('hook', 'hook', 'Bốn người xếp hàng mua vé giá mười nghìn: hai người cầm tờ mười nghìn, hai người cầm tờ hai mươi nghìn. Quầy vé ban đầu không có tiền lẻ. '
                         'Xác suất không ai phải chờ tiền thối?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chỉ cần biết thứ tự loại tiền: chọn hai vị trí cho tờ mười nghìn, sáu thứ tự đồng khả năng.'),
    Beat('s2', 'solve', 'Không ai chờ khi tại mọi thời điểm, số người trả tờ mười nghìn luôn không ít hơn số người trả tờ hai mươi nghìn. Người đầu tiên phải cầm tờ mười nghìn.'),
    Beat('s3', 'solve', 'Chỉ có hai thứ tự thỏa mãn: mười, hai mươi, mười, hai mươi; và mười, mười, hai mươi, hai mươi. Xác suất hai phần sáu, tức một phần ba.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Số thứ tự tốt là số Catalan, cùng họ với bài đường đi không xuống dưới trục.'),
    Beat('outro', 'outro', outro_text(420)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    all='C_4^2 = 6',
                    prob='P = 2/6 = 1/3')


def validate() -> bool:
    good = [o for o in ORDERS if ok(o)]
    assert len(ORDERS) == 6 and len(good) == 2 and F(len(good), 6) == F(1, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS420(ShortScene):
    N = 420

    def hook_visual(self, t0):
        self.board_top = -1.5
        rows = VGroup(*[VGroup(*[token('10' if c == 'M' else '20', CYAN if c == 'M' else CORAL, .26) for c in o]).arrange(buff=.1) for o in ORDERS])
        self.rows = rows.arrange_in_grid(rows=3, cols=2, buff=(.9, .3)).move_to([0, .95, 0])
        self.wait_until(.55, t0)

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows, lag_ratio=.15), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.play(*[r.animate.set_opacity(.25) for r, o in zip(self.rows, ORDERS) if not ok(o)], run_time=self.rt(.06))

    def beat_s3(self, T):
        self.play(*[r.animate.scale(1.15) for r, o in zip(self.rows, ORDERS) if ok(o)], run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)



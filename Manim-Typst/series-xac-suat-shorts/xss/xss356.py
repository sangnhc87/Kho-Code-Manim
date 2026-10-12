"""XSS356 · Biết A trước B — P(A đầu hàng | A trước B) = P(A đầu)/P(A trước B) = (1/5)/(1/2) = 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS356', 'answer': '2/5'}
PROBLEM = ['$5$ học sinh xếp hàng ngẫu nhiên. Biết A',
           'đứng trước B. Xác suất A đứng đầu hàng?']
OPTIONS = ['1/5', '2/5', '1/2']
CORRECT = 1
ANSWER_VALUE = .4
COND = [p for p in permutations('ABCDE') if p.index('A') < p.index('B')]
COL = {'A': CYAN, 'B': CORAL}

BEATS = [
    Beat('hook', 'hook', 'Năm học sinh xếp hàng ngẫu nhiên. Biết A đứng trước B, không nhất thiết sát nhau. Xác suất A đứng đầu hàng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, hai phần năm, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Không điều kiện, A đứng đầu với xác suất một phần năm. A đứng trước B với xác suất một phần hai, do đối xứng.'),
    Beat('s2', 'solve', 'Nếu A đứng đầu thì chắc chắn A trước B. Nên giao của hai biến cố chính là A đứng đầu.'),
    Beat('s3', 'solve', 'Xác suất có điều kiện bằng một phần năm chia một phần hai, tức hai phần năm. Thông tin A trước B làm khả năng A đứng đầu tăng gấp đôi.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Khi biến cố này kéo theo biến cố kia, phép giao trở nên rất gọn.'),
    Beat('outro', 'outro', outro_text(356)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    base='P("A đầu") = 1/5, quad P("A trước B") = 1/2',
                    prob='P = (1/5)/(1/2) = 2/5')


def validate() -> bool:
    assert F(sum(p[0] == 'A' for p in COND), len(COND)) == F(2, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS356(ShortScene):
    N = 356

    def line(self, order, frac=.06):
        new = VGroup(*[token(c, COL.get(c, SOFT), .36) for c in order]).arrange(buff=.3).move_to([0, 1.3, 0])
        self.play(*([FadeOut(self.row)] if self.row else []), FadeIn(new), run_time=self.rt(frac))
        self.row = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.row = None
        self.wait_until(.35, t0)
        self.line('CAEBD')

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('base', 1.3))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.line('ACDEB', .06)

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS406 · Tổng số ngửa là 2 — 4 đồng xu như nhau, biết tổng 2 ngửa: C(4;2) = 6 cách đồng khả năng; mỗi người 1 ngửa: 2·2 = 4 → 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS406', 'answer': '2/3'}
PROBLEM = ['An và Bình mỗi người tung $2$ đồng xu.',
           'Biết tổng số ngửa là $2$. Xác suất mỗi',
           'người có đúng $1$ ngửa?']
OPTIONS = ['2/3', '1/2', '1/3']
CORRECT = 0
ANSWER_VALUE = 2 / 3
TWO = [s for s in product('NS', repeat=4) if s.count('N') == 2]

BEATS = [
    Beat('hook', 'hook', 'An và Bình mỗi người tung hai đồng xu. Biết tổng cộng có đúng hai mặt ngửa. '
                         'Xác suất mỗi người có đúng một ngửa là bao nhiêu? Nhiều bạn đoán một phần ba.'),
    Beat('guess', 'hook', 'Hai phần ba, một phần hai, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn đồng xu, mười sáu kết quả đồng khả năng. Có đúng hai ngửa: chọn hai trong bốn đồng, sáu kết quả.'),
    Beat('s2', 'solve', 'Mỗi người một ngửa: An chọn đồng ngửa của mình hai cách, Bình hai cách, bốn kết quả. Còn lại An hai ngửa, hoặc Bình hai ngửa.'),
    Beat('s3', 'solve', 'Xác suất bốn phần sáu, tức hai phần ba. Ba trường hợp một một, hai không, không hai không đồng khả năng.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Đếm trên các kết quả gốc đồng khả năng, đừng đếm trên các nhóm.'),
    Beat('outro', 'outro', outro_text(406)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    cond='C_4^2 = 6',
                    good='2 dot 2 = 4',
                    prob='P = 4/6 = 2/3')


def validate() -> bool:
    good = [s for s in TWO if s[:2].count('N') == 1]
    assert len(TWO) == 6 and F(len(good), len(TWO)) == F(2, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS406(ShortScene):
    N = 406

    def hook_visual(self, t0):
        self.board_top = -1.5
        rows = VGroup(*[VGroup(VGroup(coin(s[0], .26), coin(s[1], .26)).arrange(buff=.08),
                               VGroup(coin(s[2], .26), coin(s[3], .26)).arrange(buff=.08)).arrange(buff=.35) for s in TWO])
        self.rows = rows.arrange_in_grid(rows=3, cols=2, buff=(.9, .25)).move_to([0, .95, 0])
        self.wait_until(.6, t0)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.rows, lag_ratio=.15), run_time=self.rt(.15))
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        good = [r for r, s in zip(self.rows, TWO) if s[:2].count('N') == 1]
        self.wait_until(.2, t0)
        self.play(*[r.animate.scale(1.12) for r in good], *[r.animate.set_opacity(.3) for r, s in zip(self.rows, TWO) if s[:2].count('N') != 1],
                  run_time=self.rt(.08))
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS333 · Ba số tăng dần — 3 lần rút có hoàn lại từ 1..5: 125 dãy; tăng ngặt ⇔ chọn 3 số khác nhau rồi xếp tăng: C(5;3) = 10 → 2/25."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS333', 'answer': '2/25'}
PROBLEM = ['Rút $3$ lần có hoàn lại từ $5$ bi đánh số',
           '$1$ đến $5$. Xác suất số sau luôn lớn hơn',
           'số trước?']
OPTIONS = ['2/25', '1/6', '4/25']
CORRECT = 0
ANSWER_VALUE = 2 / 25
INC = [s for s in product(range(1, 6), repeat=3) if s[0] < s[1] < s[2]]

BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đánh số từ một đến năm. Rút ba lần, mỗi lần ghi số rồi trả bi lại. '
                         'Xác suất ba số ghi được tăng dần ngặt là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần hai mươi lăm, một phần sáu, hay bốn phần hai mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có hoàn lại nên có năm mũ ba, một trăm hai mươi lăm dãy đồng khả năng.'),
    Beat('s2', 'solve', 'Dãy tăng ngặt thì ba số phải khác nhau, và mỗi bộ ba số khác nhau chỉ có đúng một cách xếp tăng. Số dãy bằng tổ hợp chập ba của năm, tức mười.'),
    Beat('s3', 'solve', 'Xác suất mười phần một trăm hai mươi lăm, bằng hai phần hai mươi lăm. Cạm bẫy: một phần sáu chỉ đúng khi không có số trùng.'),
    Beat('answer', 'solve', 'Đáp án: hai phần hai mươi lăm. Dãy tăng ngặt chính là một tập con, đếm bằng tổ hợp.'),
    Beat('outro', 'outro', outro_text(333)),
]

FORMULAS = formulas('2/25', OPTIONS,
                    all='5^3 = 125',
                    inc='C_5^3 = 10',
                    prob='P = 10/125 = 2/25')


def validate() -> bool:
    assert len(INC) == 10 and F(len(INC), 125) == F(2, 25)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS333(ShortScene):
    N = 333

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.pool = ball_row('YYYYY', y=2.2, r=.34, buff=.15, labels=[1, 2, 3, 4, 5], size=26)
        self.play(FadeIn(self.pool, lag_ratio=.15), run_time=self.rt(.1))
        self.wait_until(.55, t0)
        self.cur = ball_row('BBB', y=.6, r=.38, buff=.5, labels=[2, 4, 5], size=28)
        self.play(FadeIn(self.cur, lag_ratio=.4), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        for f, labs in ((.15, [3, 1, 3]), (.45, [1, 3, 5])):
            self.wait_until(f, t0)
            new = ball_row('BBB' if labs != [3, 1, 3] else 'RRR', y=.6, r=.38, buff=.5, labels=labs, size=28)
            self.play(FadeOut(self.cur), FadeIn(new), run_time=self.rt(.06))
            self.cur = new
        self.write_board(self.M('inc', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

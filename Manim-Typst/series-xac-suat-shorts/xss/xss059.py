"""XSS059 · Tích chia hết cho 3 — chọn 2 số khác nhau từ 1…10: 1 − C(7,2)/C(10,2) = 8/15."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, PANEL_2, SOFT, STROKE, WHITE  # noqa: E402

EPISODE = {'code': 'XSS059', 'answer': '8/15'}
PROBLEM = ['Chọn ngẫu nhiên $2$ số khác nhau',
           'từ $1$ đến $10$. Xác suất tích hai',
           'số chia hết cho $3$?']
OPTIONS = ['3/10', '8/15', '1/3']
CORRECT = 1
ANSWER_VALUE = 8 / 15

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên hai số khác nhau từ một đến mười. Xác suất tích của chúng chia hết cho ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần mười, tám phần mười lăm, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chọn hai số từ mười số: tổ hợp chập hai của mười, bằng bốn mươi lăm cách. '
                        'Từ một đến mười chỉ có ba bội của ba: ba, sáu và chín.'),
    Beat('s2', 'solve', 'Tích chia hết cho ba khi có ít nhất một số là bội của ba. Biến cố đối: cả hai số đều không chia '
                        'hết cho ba, chọn từ bảy số còn lại, tổ hợp chập hai của bảy, bằng hai mươi mốt cách.'),
    Beat('s3', 'solve', 'Xác suất bằng một trừ hai mươi mốt phần bốn mươi lăm, bằng hai mươi bốn phần bốn mươi lăm, '
                        'tức tám phần mười lăm. Hơn một nửa, dù chỉ có ba bội của ba!'),
    Beat('answer', 'solve', 'Đáp án: tám phần mười lăm. Tích chia hết cho ba chỉ cần một thừa số làm được việc đó.'),
    Beat('outro', 'outro', outro_text(59)),
]

FORMULAS = formulas('8/15', OPTIONS,
                    n='n(Omega) = C_10^2 = 45',
                    none='n(overline(A)) = C_7^2 = 21',
                    prob='P(A) = 1 - 21/45 = 24/45 = 8/15')


def validate() -> bool:
    pairs = list(combinations(range(1, 11), 2))
    assert comb(10, 2) == 45 and comb(7, 2) == 21
    assert F(sum(a * b % 3 == 0 for a, b in pairs), 45) == F(8, 15)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS059(ShortScene):
    N = 59

    def hook_visual(self, t0):
        self.cells = VGroup()
        for k in range(1, 11):
            sq = Square(side_length=1.05, stroke_color=STROKE, stroke_width=2, fill_color=PANEL_2, fill_opacity=1)
            self.cells.add(VGroup(sq, self.MNum(k, 0, WHITE, 34).move_to(sq)))
        self.cells.arrange_in_grid(2, 5, buff=.12).move_to([0, 1.4, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.cells, lag_ratio=.08), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(self.M('n', 2.2))
        self.wait_until(.55, t0)
        self.play(*[self.cells[k - 1][0].animate.set_fill(GOLD, .7) for k in (3, 6, 9)], run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[self.cells[k - 1][0].animate.set_fill(CYAN, .45) for k in range(1, 11) if k % 3], run_time=self.rt(.08))
        self.write_board(tx('cả hai không chia hết cho 3', 28, CYAN, bold=True), anim='fade')
        self.wait_until(.6, t0)
        self.write_board(self.M('none', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('chỉ cần 1 thừa số chia hết cho 3', 26, SOFT), anim='fade')

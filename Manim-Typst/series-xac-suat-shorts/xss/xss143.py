"""XSS143 · Đọc bảng hai chiều — trong 20 bạn thích Toán có 12 nữ: 12/20 = 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS143', 'answer': '3/5'}
PROBLEM = ['Lớp $40$ bạn: $24$ nữ, $16$ nam; có $12$ nữ',
           'và $8$ nam thích Toán. Gặp một bạn thích',
           'Toán: xác suất là nữ?']
OPTIONS = ['1/2', '3/5', '3/10']
CORRECT = 1
ANSWER_VALUE = .6
TABLE = [['', 'nữ', 'nam', 'tổng'], ['thích Toán', 12, 8, 20], ['không', 12, 8, 20], ['tổng', 24, 16, 40]]

BEATS = [
    Beat('hook', 'hook', 'Lớp có bốn mươi bạn: hai mươi bốn nữ và mười sáu nam. Mười hai bạn nữ và tám bạn nam thích môn Toán. '
                         'Bạn gặp ngẫu nhiên một bạn thích Toán. Xác suất đó là bạn nữ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần năm, hay ba phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dạng bài này nên lập bảng hai chiều: hàng là thích Toán hay không, cột là nữ hay nam. '
                        'Điền số, rồi cộng hàng, cộng cột.'),
    Beat('s2', 'solve', 'Điều kiện "thích Toán" nghĩa là ta chỉ nhìn đúng một hàng: hàng thích Toán, có hai mươi bạn. '
                        'Trong đó có mười hai bạn nữ.'),
    Beat('s3', 'solve', 'Xác suất bằng mười hai phần hai mươi, tức ba phần năm. Ba phần mười là xác suất vừa nữ vừa thích Toán, '
                        'chưa chia cho điều kiện.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Với bảng hai chiều, điều kiện chính là hàng hoặc cột bạn được phép nhìn!'),
    Beat('outro', 'outro', outro_text(143)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    prob='P("nữ" | "thích Toán") = 12/20 = 3/5',
                    trap='P("nữ" sect "thích Toán") = 12/40 = 3/10')


def validate() -> bool:
    assert F(12, 12 + 8) == F(3, 5) and F(12, 40) == F(3, 10)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS143(ShortScene):
    N = 143

    def hook_visual(self, t0):
        self.board_top = -1.3
        cells = VGroup()
        self.cell = {}
        for i, row in enumerate(TABLE):
            for j, v in enumerate(row):
                w = 2.3 if j == 0 else 1.45
                x = -2.35 if j == 0 else -.4 + 1.55 * (j - 1)
                box = card(w, .78, STROKE, PANEL, radius=.08, stroke_width=2).move_to([x, 2.3 - .86 * i, 0])
                lab = (tx(v, 24, SOFT if i == 0 or j == 0 else GOLD) if isinstance(v, str)
                       else self.MNum(v, 0, CYAN if j == 1 else (CORAL if j == 2 else GOLD), 30)).move_to(box)
                c = VGroup(box, lab)
                self.cell[i, j] = c
                cells.add(c)
        self.table = cells
        self.wait_until(.55, t0)
        self.play(FadeIn(VGroup(*[self.cell[0, j] for j in range(4)], *[self.cell[i, 0] for i in range(1, 4)])),
                  run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        inner = [self.cell[i, j] for i in range(1, 3) for j in range(1, 3)]
        totals = [self.cell[i, j] for i in range(1, 4) for j in range(1, 4) if i == 3 or j == 3]
        self.wait_until(.4, t0)
        self.play(FadeIn(VGroup(*inner), lag_ratio=.2), run_time=self.rt(.15))
        self.play(FadeIn(VGroup(*totals), lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        dim = [self.cell[i, j] for i in (2, 3) for j in range(4)]
        self.play(*[c.animate.set_opacity(.15) for c in dim], run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.play(self.cell[1, 1][0].animate.set_stroke(GOLD, 6), self.cell[1, 3][0].animate.set_stroke(CYAN, 6),
                  run_time=self.rt(.06))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('trap', 1.6), anim='fade')

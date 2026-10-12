"""XSS262 · Ít nhất bao nhiêu bi đỏ? — C(n,2)/C(n+3,2) > 1/2 ⇔ n² − 7n − 6 > 0 ⇔ n ≥ 8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import DOWN, DashedLine, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS262', 'answer': 'n = 8'}
PROBLEM = ['Hộp có $n$ bi đỏ và $3$ bi xanh. Tìm',
           '$n$ nhỏ nhất để xác suất rút $2$ bi',
           'đều đỏ lớn hơn $1/2$.']
OPTIONS = ['n = 6', 'n = 8', 'n = 10']
CORRECT = 1
ANSWER_VALUE = None
VALS = [F(comb(n, 2), comb(n + 3, 2)) for n in range(2, 12)]

BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi xanh và n bi đỏ. Cần ít nhất bao nhiêu bi đỏ để khả năng rút hai bi đều đỏ vượt quá một nửa?'),
    Beat('guess', 'hook', 'Sáu, tám, hay mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xác suất hai đỏ: tổ hợp chập hai của n chia tổ hợp chập hai của n cộng ba, bằng n nhân n trừ một chia n cộng ba nhân n cộng hai.'),
    Beat('s2', 'solve', 'Bất phương trình lớn hơn một phần hai: hai n bình phương trừ hai n lớn hơn n bình phương cộng năm n cộng sáu, '
                        'tức n bình phương trừ bảy n trừ sáu lớn hơn không.'),
    Beat('s3', 'solve', 'Nghiệm dương khoảng bảy phẩy bảy bảy, nên n nhỏ nhất bằng tám. Kiểm tra: n bằng bảy cho hai mốt phần bốn lăm, dưới một nửa; n bằng tám cho hai tám phần năm lăm, vượt một nửa.'),
    Beat('answer', 'solve', 'Đáp án: tám bi đỏ. Bài "nhỏ nhất": lập bất phương trình, giải rồi kiểm tra hai số nguyên kề nhau!'),
    Beat('outro', 'outro', outro_text(262)),
]

FORMULAS = formulas('n = 8', OPTIONS,
                    ineq='(n (n - 1))/((n + 3)(n + 2)) > 1/2 arrow.l.r.double n^2 - 7 n - 6 > 0',
                    check='n = 7: 21/45 < 1/2, quad n = 8: 28/55 > 1/2')


def validate() -> bool:
    assert next(n for n in range(2, 60) if F(comb(n, 2), comb(n + 3, 2)) > F(1, 2)) == 8
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS262(ShortScene):
    N = 262

    def hook_visual(self, t0):
        self.board_top = -1.3
        base, h = -.1, 2.8
        self.bars = VGroup()
        for k, v in enumerate(VALS):
            r = Rectangle(width=.5, height=h * float(v) / .65, stroke_width=0, fill_color=GREEN if v > F(1, 2) else CYAN,
                          fill_opacity=.85)
            r.move_to([-3.0 + .66 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k + 2}$', 20, SOFT).next_to([-3.0 + .66 * k, base, 0], DOWN, buff=.08) for k in range(10)])
        self.line = DashedLine([-3.4, base + h * .5 / .65, 0], [3.4, base + h * .5 / .65, 0], color=GOLD, stroke_width=3)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), FadeIn(self.line), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))
        self.wait_until(.5, t0)

    def beat_s2(self, T):
        self.write_board(self.M('ineq', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        self.play(self.bars[5].animate.set_fill(CORAL, .85), self.bars[6].animate.scale(1.08), run_time=self.rt(.05))
        m = self.M('check', 1.6)
        self.write_board(m)
        self.frame(m)

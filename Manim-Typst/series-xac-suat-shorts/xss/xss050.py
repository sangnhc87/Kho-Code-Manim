"""XSS050 · Có ít nhất một nữ — 6 nam 4 nữ chọn 3: 1 − C(6,3)/C(10,3) = 5/6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS050', 'answer': '5/6'}
PROBLEM = ['Chọn ngẫu nhiên $3$ người từ $6$ nam và',
           '$4$ nữ. Xác suất có ít nhất $1$ nữ?']
OPTIONS = ['2/5', '5/6', '1/2']
CORRECT = 1
ANSWER_VALUE = 5 / 6
PEOPLE = 'TTTTTTGGGG'

BEATS = [
    Beat('hook', 'hook', 'Một nhóm có sáu nam và bốn nữ. Chọn ngẫu nhiên ba người đi thi. '
                         'Xác suất trong ba người có ít nhất một bạn nữ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, năm phần sáu, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chọn ba người từ mười người: tổ hợp chập ba của mười, bằng một trăm hai mươi cách.'),
    Beat('s2', 'solve', 'Ít nhất một nữ gồm một nữ, hai nữ hoặc ba nữ: ba trường hợp. Biến cố đối gọn hơn: '
                        'cả ba đều là nam, tổ hợp chập ba của sáu, bằng hai mươi cách.'),
    Beat('s3', 'solve', 'Xác suất không có nữ bằng hai mươi phần một trăm hai mươi, tức một phần sáu. '
                        'Vậy xác suất có ít nhất một nữ bằng một trừ một phần sáu, bằng năm phần sáu.'),
    Beat('answer', 'solve', 'Đáp án: năm phần sáu. Lại là biến cố đối, vũ khí số một của bài toán ít nhất!'),
    Beat('outro', 'outro', outro_text(50)),
]

FORMULAS = formulas('5/6', OPTIONS,
                    n='n(Omega) = C_10^3 = 120',
                    none='n(overline(A)) = C_6^3 = 20',
                    prob='P(A) = 1 - 20/120 = 5/6')


def validate() -> bool:
    picks = list(combinations(range(10), 3))
    assert comb(10, 3) == 120 and comb(6, 3) == 20
    assert F(sum(any(PEOPLE[i] == 'G' for i in p) for p in picks), 120) == F(5, 6)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS050(ShortScene):
    N = 50

    def hook_visual(self, t0):
        self.g = VGroup(*[token(c, CYAN if c == 'T' else CORAL, .42) for c in PEOPLE]).arrange_in_grid(2, 5, buff=.3)
        self.g.move_to([0, 1.3, 0])
        legend = VGroup(tx('T: nam', 26, CYAN, bold=True), tx('G: nữ', 26, CORAL, bold=True)).arrange(buff=.6) \
            .move_to([0, -.15, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.g, lag_ratio=.08), FadeIn(legend), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(tx('1 nữ, 2 nữ, 3 nữ: dài!', 28, SOFT), anim='fade')
        self.wait_until(.45, t0)
        self.play(*[t.animate.set_opacity(.3) for t in self.g[6:]], run_time=self.rt(.06))
        self.write_board(self.M('none', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[t.animate.set_opacity(1) for t in self.g[6:]], run_time=self.rt(.04))
        self.wait_until(.4, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

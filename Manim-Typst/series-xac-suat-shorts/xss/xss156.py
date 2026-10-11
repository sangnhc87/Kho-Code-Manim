"""XSS156 · Ít nhất hai con trai — 4 dãy có ≥ 2 trai, 1 dãy TTT: 1/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS156', 'answer': '1/4'}
PROBLEM = ['Gia đình có $3$ con, biết có ít nhất $2$ con',
           'trai. Xác suất cả $3$ con đều là trai?']
OPTIONS = ['1/8', '1/4', '1/2']
CORRECT = 1
ANSWER_VALUE = .25
SEQS = [''.join(w) for w in product('TG', repeat=3)]

BEATS = [
    Beat('hook', 'hook', 'Một gia đình có ba con. Bạn biết gia đình đó có ít nhất hai con trai. '
                         'Xác suất cả ba con đều là trai là bao nhiêu? Nhiều người trả lời một phần hai, vì chỉ còn một đứa chưa biết.'),
    Beat('guess', 'hook', 'Một phần tám, một phần tư, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Liệt kê tám khả năng đồng khả năng theo thứ tự sinh. Có ít nhất hai trai: trai trai gái, trai gái trai, '
                        'gái trai trai, và trai trai trai, tất cả bốn khả năng.'),
    Beat('s2', 'solve', 'Trong bốn khả năng đó chỉ một là ba trai. Xác suất bằng một phần tư.'),
    Beat('s3', 'solve', 'Một phần hai sai vì thông tin "ít nhất hai trai" không chỉ ra đứa nào là trai, '
                        'nên đứa "còn lại" không xác định được.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Với điều kiện "ít nhất", hãy liệt kê đầy đủ rồi đếm!'),
    Beat('outro', 'outro', outro_text(156)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    nb='n(B) = C_3^2 + C_3^3 = 4',
                    prob='P(A | B) = 1/4')


def validate() -> bool:
    b = [s for s in SEQS if s.count('T') >= 2]
    assert F(sum(s == 'TTT' for s in b), len(b)) == F(1, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS156(ShortScene):
    N = 156

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.rows = VGroup(*[VGroup(*[token(c, CYAN if c == 'T' else CORAL, .3) for c in s]).arrange(buff=.08) for s in SEQS]) \
            .arrange_in_grid(4, 2, buff=(.9, .2)).move_to([0, 1.25, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.rows, lag_ratio=.1), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.play(*[r.animate.set_opacity(.15) for r, s in zip(self.rows, SEQS) if s.count('T') < 2], run_time=self.rt(.08))
        self.write_board(self.M('nb', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.rows[0].animate.scale(1.2), *[c[0].animate.set_stroke(GOLD, 5) for c in self.rows[0]],
                  run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('$1/2$ sai: không biết đứa nào là trai', 26, CORAL, bold=True), anim='fade')

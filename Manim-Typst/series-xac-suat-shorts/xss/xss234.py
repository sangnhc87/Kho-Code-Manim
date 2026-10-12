"""XSS234 · Ngửa đầu và ít nhất hai ngửa — NNS, NSN, NNN: 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS234', 'answer': '1/3'}
PROBLEM = ['Tung xu $3$ lần, biết lần $1$ ngửa',
           'và có ít nhất $2$ lần ngửa. Xác',
           'suất cả $3$ lần đều ngửa?']
OPTIONS = ['1/4', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3
SEQS = [''.join(w) for w in product('NS', repeat=3)]

BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu ba lần. Biết hai điều: lần đầu ra ngửa, và tổng cộng có ít nhất hai lần ngửa. '
                         'Xác suất cả ba lần đều ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện một, lần đầu ngửa, giữ lại bốn dãy bắt đầu bằng ngửa. Điều kiện hai, ít nhất hai ngửa, loại thêm dãy ngửa sấp sấp.'),
    Beat('s2', 'solve', 'Còn ba dãy: ngửa ngửa sấp, ngửa sấp ngửa, ngửa ngửa ngửa, vẫn đồng khả năng.'),
    Beat('s3', 'solve', 'Xác suất một phần ba. Chỉ với điều kiện "lần đầu ngửa" thì là một phần tư; điều kiện thứ hai làm xác suất tăng lên.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Áp từng điều kiện một, gạch dần các khả năng!'),
    Beat('outro', 'outro', outro_text(234)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    prob='P = 1/3')


def validate() -> bool:
    b = [s for s in SEQS if s[0] == 'N' and s.count('N') >= 2]
    assert F(sum(s == 'NNN' for s in b), len(b)) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS234(ShortScene):
    N = 234

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.rows = VGroup(*[VGroup(*[coin(c, .32) for c in s]).arrange(buff=.08) for s in SEQS]) \
            .arrange_in_grid(4, 2, buff=(.9, .22)).move_to([0, 1.25, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.rows, lag_ratio=.08), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[r.animate.set_opacity(.15) for r, s in zip(self.rows, SEQS) if s[0] != 'N'], run_time=self.rt(.06))
        self.wait_until(.55, t0)
        self.play(*[r.animate.set_opacity(.15) for r, s in zip(self.rows, SEQS) if s == 'NSS'], run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.rows[0].animate.scale(1.2), *[c[0].animate.set_stroke(GOLD, 5) for c in self.rows[0]], run_time=self.rt(.05))

    def beat_s3(self, T):
        m = self.M('prob', 2.4)
        self.write_board(m)
        self.frame(m)

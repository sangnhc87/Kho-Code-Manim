"""XSS314 · Cân rồi có đều? — 12-giác đều: 12·5 − 2·4 = 52 tam giác cân, 4 tam giác đều → 1/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN  # noqa: E402
from xss._polykit import PolyMixin, arcs, is_iso, triangles  # noqa: E402

EPISODE = {'code': 'XSS314', 'answer': '1/13'}
PROBLEM = ['Chọn $3$ đỉnh của đa giác đều $12$ cạnh.',
           'Biết tam giác tạo thành là tam giác cân.',
           'Xác suất nó là tam giác đều?']
OPTIONS = ['1/13', '1/12', '1/11']
CORRECT = 0
ANSWER_VALUE = 1 / 13
N_ = 12
ISO = triangles(N_, is_iso(N_))
EQ = [t for t in ISO if len(set(arcs(t, N_))) == 1]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba đỉnh của đa giác đều mười hai cạnh. Biết tam giác tạo thành là tam giác cân. '
                         'Xác suất nó là tam giác đều bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười ba, một phần mười hai, hay một phần mười một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm tam giác cân theo đỉnh cân: chọn đỉnh cân có mười hai cách, hai đỉnh còn lại đối xứng qua trục, có năm cặp. '
                        'Được sáu mươi, nhưng mỗi tam giác đều bị đếm ba lần.'),
    Beat('s2', 'solve', 'Có bốn tam giác đều, mỗi đỉnh cách nhau bốn bước. Bớt phần đếm thừa: sáu mươi trừ tám, còn năm mươi hai tam giác cân.'),
    Beat('s3', 'solve', 'Trong năm mươi hai tam giác cân đó có đúng bốn tam giác đều. Xác suất bốn phần năm mươi hai, tức một phần mười ba.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười ba. Bẫy hay gặp là quên trừ phần đếm lặp của tam giác đều.'),
    Beat('outro', 'outro', outro_text(314)),
]

FORMULAS = formulas('1/13', OPTIONS,
                    raw='12 dot 5 = 60',
                    iso='60 - 2 dot 4 = 52',
                    prob='P = 4/52 = 1/13')


def validate() -> bool:
    assert len(ISO) == 52 and len(EQ) == 4
    assert F(len(EQ), len(ISO)) == F(1, 13)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS314(PolyMixin, ShortScene):
    N = 314

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(N_)
        self.wait_until(.4, t0)
        self.cur = self.flash([(0, 3, 9), (0, 5, 7), (0, 4, 8)], CYAN, .2)

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash([(0, k, 12 - k) for k in range(1, 6)], CYAN, .3)
        self.wait_until(.55, t0)
        self.write_board(self.M('raw', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash(EQ, GOLD, .25)
        self.wait_until(.6, t0)
        m = self.M('iso', 1.6)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.cur.animate.set_color(GREEN).set_fill(GREEN, .35), run_time=self.rt(.04))
        self.wait_until(.45, t0)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

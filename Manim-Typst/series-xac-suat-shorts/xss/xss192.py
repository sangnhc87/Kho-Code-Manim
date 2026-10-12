"""XSS192 · Nghịch lý Simpson — A tốt hơn ở từng nhóm (93 % > 87 %, 73 % > 69 %) nhưng chung cuộc 78 % < 83 %."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS192', 'answer': 'B (83 % so với 78 %)'}
PROBLEM = ['A khỏi $81\\/87$ ca nhẹ, $192\\/263$ ca nặng;',
           'B khỏi $234\\/270$ và $55\\/80$. Thuốc',
           'nào có tỉ lệ khỏi chung cao hơn?']
OPTIONS = ['"Thuốc A"', '"Thuốc B"', '"Như nhau"']
CORRECT = 1
ANSWER_VALUE = None
DATA = {'A': ((81, 87), (192, 263)), 'B': ((234, 270), (55, 80))}

BEATS = [
    Beat('hook', 'hook', 'Một nghiên cứu sỏi thận thật: thuốc A chữa khỏi tám mươi mốt trên tám mươi bảy ca nhẹ và một trăm chín mươi hai '
                         'trên hai trăm sáu mươi ba ca nặng. Thuốc B khỏi hai trăm ba mươi tư trên hai trăm bảy mươi và năm mươi lăm trên tám mươi. '
                         'Tính chung, thuốc nào tốt hơn?'),
    Beat('guess', 'hook', 'Thuốc A, thuốc B, hay như nhau? Ba, hai, một!'),
    Beat('s1', 'solve', 'So từng nhóm: ca nhẹ, A chín mươi ba phần trăm, B tám mươi bảy. Ca nặng, A bảy mươi ba, B sáu mươi chín. '
                        'A thắng ở cả hai nhóm.'),
    Beat('s2', 'solve', 'Gộp lại: A khỏi hai trăm bảy mươi ba trên ba trăm năm mươi, khoảng bảy mươi tám phần trăm. '
                        'B khỏi hai trăm tám mươi chín trên ba trăm năm mươi, khoảng tám mươi ba phần trăm. B thắng chung cuộc!'),
    Beat('s3', 'solve', 'Bí mật: A được dùng chủ yếu cho ca nặng, vốn khó chữa; B chủ yếu cho ca nhẹ. '
                        'Tỉ lệ chung là trung bình có trọng số, và trọng số của hai thuốc rất khác nhau.'),
    Beat('answer', 'solve', 'Đáp án: tính chung thì B cao hơn, dù A tốt hơn ở từng nhóm. Đây là nghịch lý Simpson, bẫy kinh điển của thống kê!'),
    Beat('outro', 'outro', outro_text(192)),
]

FORMULAS = formulas('"Thuốc B"', OPTIONS,
                    groups='81/87 > 234/270, quad 192/263 > 55/80',
                    total='273/350 approx "0,78" < 289/350 approx "0,83"')


def validate() -> bool:
    (a1, a2), (b1, b2) = DATA['A'], DATA['B']
    assert F(*a1) > F(*b1) and F(*a2) > F(*b2)
    assert F(a1[0] + a2[0], a1[1] + a2[1]) < F(b1[0] + b2[0], b1[1] + b2[1])
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS192(ShortScene):
    N = 192

    def cell(self, text, w, color=SOFT, stroke=STROKE):
        box = card(w, .78, stroke, PANEL, radius=.08, stroke_width=2)
        return VGroup(box, self.TM(text, 24, color).move_to(box))

    def hook_visual(self, t0):
        self.board_top = -1.3
        rows = [['', 'ca nhẹ', 'ca nặng', 'chung'],
                ['A', '$81/87$', '$192/263$', '$273/350$'],
                ['B', '$234/270$', '$55/80$', '$289/350$']]
        self.tab = VGroup()
        for i, r in enumerate(rows):
            line = VGroup(*[self.cell(t, .9 if j == 0 else 1.9, CYAN if i == 1 else (CORAL if i == 2 else SOFT))
                            for j, t in enumerate(r)]).arrange(buff=.08)
            self.tab.add(line)
        self.tab.arrange([0, -1, 0], buff=.08).move_to([0, 1.45, 0])
        self.wait_until(.75, t0)
        self.play(FadeIn(VGroup(*[r[:3] for r in self.tab]), lag_ratio=.1), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.tab[1][1][0].animate.set_stroke(GREEN, 5), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(self.tab[1][2][0].animate.set_stroke(GREEN, 5), run_time=self.rt(.05))
        self.write_board(self.M('groups', 1.7))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(FadeIn(VGroup(self.tab[0][3], self.tab[1][3], self.tab[2][3])), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(self.tab[2][3][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.05))
        m = self.M('total', 1.6)
        self.write_board(m)
        self.frame(m, CORAL)

    def beat_s3(self, T):
        self.write_board(tx('trọng số khác nhau', 28, GOLD, bold=True), anim='fade')

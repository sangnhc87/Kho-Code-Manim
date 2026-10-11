"""XSS021 · Hai con đều trai — cây TT, TG, GT, GG: 1/4 (bẫy 1/3)."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token, tree  # noqa: E402

EPISODE = {'code': 'XSS021', 'answer': '1/4'}
PROBLEM = ['Một gia đình có $2$ con.', 'Xác suất cả hai đều là con trai?']
OPTIONS = ['1/2', '1/3', '1/4']
CORRECT = 2
ANSWER_VALUE = .25
KIDS = [''.join(w) for w in product('TG', repeat=2)]
COLOR = {'T': CYAN, 'G': CORAL}

BEATS = [
    Beat('hook', 'hook', 'Một gia đình có hai con. Coi khả năng sinh trai hay gái là như nhau. '
                         'Xác suất cả hai đều là con trai là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ cây theo thứ tự sinh: con thứ nhất là trai hoặc gái, con thứ hai cũng vậy. '
                        'Được bốn kết quả: trai trai, trai gái, gái trai, gái gái.'),
    Beat('s2', 'solve', 'Chỉ một kết quả là cả hai con trai, nên xác suất bằng một phần tư.'),
    Beat('s3', 'solve', 'Đáp án một phần ba sai vì gộp trai gái và gái trai thành một. '
                        'Anh trai em gái và chị gái em trai là hai gia đình khác nhau!'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Thử thách sau sẽ hỏi lại bài này với một thông tin thêm, '
                            'và đáp án sẽ thay đổi bất ngờ.'),
    Beat('outro', 'outro', outro_text(21)),
]

FORMULAS = formulas('1/4', OPTIONS, n='Omega = {T T; space T G; space G T; space G G}', prob='P("TT") = 1/4')


def validate() -> bool:
    assert Fraction(sum(w == 'TT' for w in KIDS), 4) == Fraction(1, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS021(ShortScene):
    N = 21

    def hook_visual(self, t0):
        self.fam = VGroup(token('?', GOLD, .8), token('?', GOLD, .8)).arrange(buff=1.0).move_to([0, 1.3, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.fam, lag_ratio=.4), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.fam.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.fam)
        root = {'m': tx('gia đình', 24, SOFT), 'kids': []}
        for a in 'TG':
            root['kids'].append({'m': token(a, COLOR[a], .38), 'kids': [{'m': token(b, COLOR[b], .38), 'kids': []}
                                                                        for b in 'TG']})
        _, levels = tree(root, top=(0, 3.2), dy=1.4, width=6.0)
        side = VGroup(tx('con 1', 22, SOFT).move_to([-3.5, 1.8, 0]), tx('con 2', 22, SOFT).move_to([-3.5, .4, 0]))
        leaves = [k['m'] for c in root['kids'] for k in c['kids']]
        self.labels = VGroup(*[tx(w, 28, GOLD, bold=True).next_to(leaf, DOWN, buff=.15) for w, leaf in zip(KIDS, leaves)])
        self.play(FadeIn(levels[0]), run_time=self.rt(.04))
        self.play(FadeIn(levels[1], lag_ratio=.3), FadeIn(side[0]), run_time=self.rt(.12))
        self.play(FadeIn(levels[2], lag_ratio=.2), FadeIn(side[1]), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.labels, lag_ratio=.3), run_time=self.rt(.2))
        self.board_top = -1.0

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.labels[0].animate.scale(1.4), *[lab.animate.set_opacity(.35) for lab in self.labels[1:]],
                  run_time=self.rt(.1))
        self.wait_until(.35, t0)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.labels[1].animate.set_opacity(1).set_color(CORAL), self.labels[2].animate.set_opacity(1)
                  .set_color(CORAL), run_time=self.rt(.08))
        self.write_board(tx('TG và GT là hai kết quả khác nhau', 28, CORAL, bold=True), anim='fade')
        self.wait_until(.6, t0)
        self.write_board(self.M('n', 1.5), anim='fade')

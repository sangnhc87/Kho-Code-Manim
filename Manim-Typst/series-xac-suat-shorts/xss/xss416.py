"""XSS416 · Ba chiếc mũ — thấy 2 mũ cùng màu thì đoán màu ngược lại, khác màu thì bỏ qua: chỉ thua khi cả 3 cùng màu (2/8) → 3/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS416', 'answer': '3/4'}
PROBLEM = ['$3$ người đội mũ đỏ/xanh ngẫu nhiên, thấy',
           'mũ người khác, được đoán hoặc bỏ qua.',
           'Thắng nếu có người đúng và không ai sai.',
           'Chiến thuật tốt nhất thắng với xác suất?']
OPTIONS = ['3/4', '1/2', '7/8']
CORRECT = 0
ANSWER_VALUE = .75


def team_wins(hats):
    guesses = []
    for i in range(3):
        others = [hats[j] for j in range(3) if j != i]
        if others[0] == others[1]:
            guesses.append(hats[i] == 1 - others[0])
    return bool(guesses) and all(guesses)


BEATS = [
    Beat('hook', 'hook', 'Ba người được đội mũ đỏ hoặc xanh ngẫu nhiên. Mỗi người thấy mũ hai người kia nhưng không thấy mũ mình, và cùng lúc đoán hoặc bỏ qua. '
                         'Đội thắng nếu có ít nhất một người đoán đúng và không ai đoán sai. Chiến thuật tốt nhất?'),
    Beat('guess', 'hook', 'Ba phần tư, một phần hai, hay bảy phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Một người đoán bừa thắng một phần hai. Chiến thuật hay hơn: nếu thấy hai mũ cùng màu, đoán màu ngược lại; nếu thấy khác màu, bỏ qua.'),
    Beat('s2', 'solve', 'Có tám cách đội mũ. Sáu cách có đúng hai mũ một màu: người lẻ màu thấy hai mũ giống nhau, đoán ngược lại và đúng; hai người kia bỏ qua.'),
    Beat('s3', 'solve', 'Chỉ hai cách cả ba cùng màu thì cả ba đoán sai. Đội thắng sáu phần tám, tức ba phần tư.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tư. Cái sai được dồn vào ít trường hợp, cái đúng được dàn trải ra nhiều trường hợp.'),
    Beat('outro', 'outro', outro_text(416)),
]

FORMULAS = formulas('3/4', OPTIONS,
                    win='6 "cách thắng", quad 2 "cách thua" ("cùng màu")',
                    prob='P = 6/8 = 3/4')


def validate() -> bool:
    assert F(sum(team_wins(h) for h in product((0, 1), repeat=3)), 8) == F(3, 4)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS416(ShortScene):
    N = 416

    def hook_visual(self, t0):
        self.board_top = -1.4
        rows = VGroup()
        for h in product((0, 1), repeat=3):
            rows.add(VGroup(*[token(' ', CORAL if x else CYAN, .2) for x in h]).arrange(buff=.08))
        self.rows = rows.arrange_in_grid(rows=2, cols=4, buff=(.45, .35)).move_to([0, .8, 0])
        self.wait_until(.6, t0)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.rows, lag_ratio=.1), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        good = [r for r, h in zip(self.rows, product((0, 1), repeat=3)) if len(set(h)) == 2]
        self.wait_until(.4, t0)
        self.play(*[r.animate.scale(1.15) for r in good], run_time=self.rt(.06))

    def beat_s3(self, T):
        t0 = self.now()
        bad = [r for r, h in zip(self.rows, product((0, 1), repeat=3)) if len(set(h)) == 1]
        self.play(*[r.animate.set_opacity(.3) for r in bad], run_time=self.rt(.05))
        self.write_board(self.M('win', 1.2))
        self.wait_until(.6, t0)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

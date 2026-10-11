"""XSS096 · Gieo đến khi ra 6 — P(số lần gieo là chẵn) = (5/6)/(1 + 5/6) = 5/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS096', 'answer': '5/11'}
PROBLEM = ['Gieo xúc xắc cho đến khi ra',
           'mặt $6$ thì dừng. Xác suất số',
           'lần gieo là một số chẵn?']
OPTIONS = ['1/2', '5/11', '6/11']
CORRECT = 1
ANSWER_VALUE = 5 / 11

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc liên tục cho đến khi ra mặt sáu thì dừng. Xác suất số lần gieo là một số chẵn '
                         'bằng bao nhiêu? Chẵn hay lẻ thì chắc cũng một nửa?'),
    Beat('guess', 'hook', 'Một phần hai, năm phần mười một, hay sáu phần mười một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dừng ở lần một: xác suất một phần sáu. Dừng ở lần hai: lần một không ra sáu rồi lần hai ra sáu, '
                        'năm phần sáu nhân một phần sáu. Vậy lần hai luôn kém lần một một hệ số năm phần sáu.'),
    Beat('s2', 'solve', 'Ghép từng cặp lần gieo: lần một với lần hai, lần ba với lần bốn, cứ thế. Trong mỗi cặp, '
                        'khả năng dừng ở lần chẵn chỉ bằng năm phần sáu khả năng dừng ở lần lẻ.'),
    Beat('s3', 'solve', 'Chia một thành hai phần theo tỉ lệ một với năm phần sáu, tức sáu với năm: lẻ được sáu phần mười một, '
                        'chẵn được năm phần mười một. Lần gieo đầu tiên có lợi thế!'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười một. Ai được đi trước luôn có lợi hơn một chút!'),
    Beat('outro', 'outro', outro_text(96)),
]

FORMULAS = formulas('5/11', OPTIONS,
                    first='P(1) = 1/6, quad P(2) = 5/6 dot 1/6',
                    ratio='P("chẵn") : P("lẻ") = 5/6 : 1 = 5 : 6',
                    prob='P("chẵn") = 5/11')


def validate() -> bool:
    even = sum(F(5, 6) ** (k - 1) * F(1, 6) for k in range(2, 400, 2))
    assert abs(float(even) - 5 / 11) < 1e-12 and F(5, 36) / (1 - F(25, 36)) == F(5, 11)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS096(ShortScene):
    N = 96

    def hook_visual(self, t0):
        self.seq = VGroup(*[VGroup(die(v, .85), tx(f'lần {i + 1}', 20, SOFT)).arrange([0, -1, 0], buff=.1)
                            for i, v in enumerate((3, 1, 5, 6))]).arrange(buff=.3).move_to([0, 1.5, 0])
        self.wait_until(.45, t0)
        for s in self.seq:
            self.play(FadeIn(s, shift=[.2, 0, 0]), run_time=self.rt(.07))
        self.play(self.seq[3][0][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('first', 1.8))

    def beat_s2(self, T):
        t0 = self.now()
        pairs = VGroup(tx('(1, 2)', 30, CYAN, bold=True), tx('(3, 4)', 30, CYAN, bold=True), tx('(5, 6) …', 30, CYAN, bold=True)) \
            .arrange(buff=.5).move_to([0, .25, 0])
        self.play(FadeIn(pairs, lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        self.write_board(self.M('ratio', 1.8))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.write_board(tx('đi trước có lợi: lẻ 6/11', 26, CORAL), anim='fade')

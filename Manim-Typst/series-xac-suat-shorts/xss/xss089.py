"""XSS089 · Bốn cặp vợ chồng — xếp hàng 8 người, mọi cặp cạnh nhau: 4!·2⁴/8! = 1/105."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path

from manim import FadeIn, RoundedRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS089', 'answer': '1/105'}
PROBLEM = ['$4$ cặp vợ chồng xếp hàng ngang ngẫu',
           'nhiên. Xác suất mọi cặp đều đứng cạnh',
           'nhau?']
OPTIONS = ['1/16', '1/105', '1/24']
CORRECT = 1
ANSWER_VALUE = 1 / 105
COLORS = (GOLD, CYAN, CORAL, PURPLE)

BEATS = [
    Beat('hook', 'hook', 'Bốn cặp vợ chồng xếp thành một hàng ngang để chụp ảnh, hoàn toàn ngẫu nhiên. '
                         'Xác suất cặp nào cũng đứng cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười sáu, một phần một trăm lẻ năm, hay một phần hai mươi bốn? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tám người xếp hàng có tám giai thừa, bằng bốn mươi nghìn ba trăm hai mươi cách.'),
    Beat('s2', 'solve', 'Gộp mỗi cặp thành một khối: bốn khối xếp được bốn giai thừa bằng hai mươi bốn cách. '
                        'Trong mỗi khối, vợ chồng đổi chỗ được hai cách, bốn khối là hai mũ bốn bằng mười sáu.'),
    Beat('s3', 'solve', 'Số cách thuận lợi: hai mươi bốn nhân mười sáu, bằng ba trăm tám mươi tư. '
                        'Xác suất bằng ba trăm tám mươi tư phần bốn mươi nghìn ba trăm hai mươi, tức một phần một trăm lẻ năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần một trăm lẻ năm, chưa tới một phần trăm. Gộp khối là chìa khóa của dạng "đứng cạnh nhau"!'),
    Beat('outro', 'outro', outro_text(89)),
]

FORMULAS = formulas('1/105', OPTIONS,
                    n='n(Omega) = 8! = 40320',
                    a='n(A) = 4! dot 2^4 = 384',
                    prob='P = 384/40320 = 1/105')


def validate() -> bool:
    ok = 0
    for p in permutations(range(8)):
        pos = {v: i for i, v in enumerate(p)}
        ok += all(abs(pos[2 * k] - pos[2 * k + 1]) == 1 for k in range(4))
    assert F(ok, factorial(8)) == F(1, 105) and factorial(4) * 2 ** 4 == 384
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS089(ShortScene):
    N = 89

    def hook_visual(self, t0):
        order = (0, 5, 2, 7, 1, 4, 6, 3)
        self.line = VGroup(*[token('ab'[i % 2], COLORS[i // 2], .36) for i in order]).arrange(buff=.14).move_to([0, 1.5, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.line, lag_ratio=.12), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.M('n', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        blocks = VGroup()
        for k in range(4):
            pair = VGroup(token('a', COLORS[k], .36), token('b', COLORS[k], .36)).arrange(buff=.05)
            frame = RoundedRectangle(width=pair.width + .2, height=.95, corner_radius=.2, stroke_color=GREEN, stroke_width=4)
            blocks.add(VGroup(frame.move_to(pair), pair))
        blocks.arrange(buff=.2).move_to([0, 1.5, 0])
        self.play(self.line.animate.set_opacity(0), FadeIn(blocks), run_time=self.rt(.1))
        self.remove(self.line)
        self.play(FadeIn(tx('4 khối', 28, GREEN, bold=True).next_to(blocks, [0, -1, 0], buff=.2)), run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.write_board(self.M('a', 2.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('chưa tới 1%', 30, SOFT, bold=True), anim='fade')

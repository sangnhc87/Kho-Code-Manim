"""XSS027 · Đứng đầu hàng — 6 cách xếp A, B, C; A đứng đầu ở 2 cách: 1/3 (tính đối xứng)."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS027', 'answer': '1/3'}
PROBLEM = ['Xếp ngẫu nhiên $3$ bạn A, B, C thành một hàng.', 'Xác suất bạn A đứng đầu hàng?']
OPTIONS = ['1/6', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3
PERMS = [''.join(p) for p in permutations('ABC')]
COLOR = {'A': GOLD, 'B': CYAN, 'C': CORAL}

BEATS = [
    Beat('hook', 'hook', 'Ba bạn A, B, C xếp hàng ngẫu nhiên. Xác suất bạn A đứng đầu hàng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Liệt kê tất cả các cách xếp: ba bạn có ba giai thừa, bằng sáu cách xếp hàng, '
                        'mỗi cách có khả năng như nhau.'),
    Beat('s2', 'solve', 'Bạn A đứng đầu ở hai cách: A B C và A C B. Xác suất bằng hai phần sáu, tức một phần ba.'),
    Beat('s3', 'solve', 'Cách nghĩ đẹp hơn: vị trí đầu hàng là của một trong ba bạn, và không bạn nào được ưu tiên. '
                        'Nên mỗi bạn có cơ hội một phần ba, không cần liệt kê gì cả.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Tính đối xứng là vũ khí bí mật giúp giải nhanh rất nhiều bài xác suất.'),
    Beat('outro', 'outro', outro_text(27)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    n='n(Omega) = 3! = 6',
                    prob='P = 2/6 = 1/3')


def validate() -> bool:
    assert len(PERMS) == 6 and Fraction(sum(p[0] == 'A' for p in PERMS), 6) == Fraction(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS027(ShortScene):
    N = 27

    def row(self, p, r=.33):
        return VGroup(*[token(ch, COLOR[ch], r) for ch in p]).arrange(buff=.12)

    def hook_visual(self, t0):
        self.big = self.row('BCA', .6).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.big, lag_ratio=.3), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.big.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.big)
        self.rows = VGroup(*[self.row(p) for p in PERMS]).arrange_in_grid(3, 2, buff=(.9, .32)).move_to([0, 1.35, 0])
        self.play(FadeIn(self.rows, lag_ratio=.2), run_time=self.rt(.35))
        self.wait_until(.65, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        hits = [i for i, p in enumerate(PERMS) if p[0] == 'A']
        self.play(*[self.rows[i].animate.scale(1.15) for i in hits],
                  *[self.rows[i].animate.set_opacity(.3) for i in range(6) if i not in hits], run_time=self.rt(.12))
        self.wait_until(.5, t0)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(tx('đầu hàng: 3 bạn ngang cơ hội', 28, GREEN, bold=True), anim='fade')

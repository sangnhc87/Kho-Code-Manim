"""XSS049 · Đủ ba màu — 5 đỏ, 4 xanh, 3 vàng, lấy 3: 5·4·3 / C(12,3) = 60/220 = 3/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import SOFT  # noqa: E402
from common.visuals import ball, urn  # noqa: E402

EPISODE = {'code': 'XSS049', 'answer': '3/11'}
PROBLEM = ['Hộp có $5$ bi đỏ, $4$ bi xanh, $3$ bi vàng.', 'Lấy ngẫu nhiên $3$ bi. Xác suất đủ cả ba màu?']
OPTIONS = ['1/3', '3/11', '1/4']
CORRECT = 1
ANSWER_VALUE = 3 / 11
BALLS = 'RRRRRBBBBYYY'

BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đỏ, bốn bi xanh và ba bi vàng. Lấy ngẫu nhiên ba viên. '
                         'Xác suất được đủ cả ba màu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, ba phần mười một, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lấy ba viên từ mười hai viên: tổ hợp chập ba của mười hai, bằng hai trăm hai mươi cách.'),
    Beat('s2', 'solve', 'Đủ ba màu nghĩa là mỗi màu đúng một viên: năm cách chọn viên đỏ, bốn cách chọn viên xanh, '
                        'ba cách chọn viên vàng. Theo quy tắc nhân: sáu mươi cách.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu mươi phần hai trăm hai mươi, rút gọn còn ba phần mười một, '
                        'khoảng hai mươi bảy phần trăm. Một phần ba là bẫy: ba màu không có số bi bằng nhau.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười một. Mỗi màu một viên: nhân số cách của từng màu!'),
    Beat('outro', 'outro', outro_text(49)),
]

FORMULAS = formulas('3/11', OPTIONS,
                    n='n(Omega) = C_12^3 = 220',
                    a='n(A) = 5 dot 4 dot 3 = 60',
                    prob='P(A) = 60/220 = 3/11')


def validate() -> bool:
    picks = list(combinations(range(12), 3))
    assert comb(12, 3) == 220 and F(sum(len({BALLS[i] for i in p}) == 3 for p in picks), 220) == F(3, 11)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS049(ShortScene):
    N = 49

    def hook_visual(self, t0):
        self.u = urn(BALLS, cols=6, r=.36).move_to([0, 1.25, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.u[0]), FadeIn(self.u.balls, lag_ratio=.08), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        trio = VGroup(ball('R', .4), ball('B', .4), ball('Y', .4)).arrange(buff=.3).next_to(self.u, UP, buff=.25)
        self.play(FadeIn(trio, lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.write_board(self.M('a', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('3 màu không có số bi bằng nhau', 26, SOFT), anim='fade')



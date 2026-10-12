"""XSS317 · Bẻ que có điều kiện — điểm bẻ (u; v) đều trên [0;1]²; đoạn trái < 1/2 có xác suất 3/4; tạo tam giác 1/4 (nằm trọn trong điều kiện) → 1/3."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402
from xss._sqkit import Unit  # noqa: E402

EPISODE = {'code': 'XSS317', 'answer': '1/3'}
PROBLEM = ['Bẻ que dài $1$ tại $2$ điểm ngẫu nhiên. Biết',
           'đoạn bên trái ngắn hơn nửa que. Xác suất',
           'ba đoạn tạo thành một tam giác?']
OPTIONS = ['1/4', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3
U = Unit()


def simulate(n=40000, seed=317):
    rnd, c, t = random.Random(seed), 0, 0
    for _ in range(n):
        a, b = sorted((rnd.random(), rnd.random()))
        if a < .5:
            c += 1
            t += max(a, b - a, 1 - b) < .5
    return t / c


BEATS = [
    Beat('hook', 'hook', 'Bẻ một que dài một mét tại hai điểm ngẫu nhiên thành ba đoạn. Biết đoạn bên trái ngắn hơn nửa que. '
                         'Xác suất ba đoạn ghép được thành tam giác là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi u, v là hai điểm bẻ, mỗi cặp là một điểm trong hình vuông đơn vị. Đoạn trái là số nhỏ hơn trong hai số. '
                        'Nó ngắn hơn nửa que trừ khi cả hai số đều lớn hơn một nửa: điều kiện có diện tích ba phần tư.'),
    Beat('s2', 'solve', 'Ba đoạn tạo tam giác khi mọi đoạn đều ngắn hơn một nửa. Vùng đó gồm hai tam giác nhỏ quanh tâm, tổng diện tích một phần tư.'),
    Beat('s3', 'solve', 'Hai tam giác này có đoạn trái ngắn hơn nửa que, nên nằm trọn trong vùng điều kiện. Xác suất một phần tư chia ba phần tư, bằng một phần ba.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Thông tin đoạn trái ngắn chỉ loại vùng không bao giờ tạo tam giác, nên xác suất tăng từ một phần tư lên một phần ba.'),
    Beat('outro', 'outro', outro_text(317)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    cond='P("trái" < 1/2) = 1 - 1/4 = 3/4',
                    tri='P("tam giác") = 1/4',
                    prob='P = (1/4)/(3/4) = 1/3')


def validate() -> bool:
    assert F(1, 4) / F(3, 4) == F(1, 3)
    assert abs(simulate() - 1 / 3) < .02
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS317(ShortScene):
    N = 317

    def hook_visual(self, t0):
        self.board_top = -1.75
        self.sq = U.frame(self, 'u', 'v')
        self.wait_until(.45, t0)
        self.play(FadeIn(self.sq), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.cond = U.region([(0, 0), (1, 0), (1, .5), (.5, .5), (.5, 1), (0, 1)], CYAN, .25, 3)
        self.out = U.region([(.5, .5), (1, .5), (1, 1), (.5, 1)], CORAL, .5)
        self.play(FadeIn(self.cond), FadeIn(self.out), run_time=self.rt(.08))
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        tri = [U.region([(0, .5), (.5, .5), (.5, 1)], GREEN, .75), U.region([(.5, 0), (.5, .5), (1, .5)], GREEN, .75)]
        self.play(*[FadeIn(r) for r in tri], run_time=self.rt(.08))
        self.write_board(self.M('tri', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.35, t0)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

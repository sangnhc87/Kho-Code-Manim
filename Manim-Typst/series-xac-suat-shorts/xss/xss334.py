"""XSS334 · Có vàng thì đủ màu? — 4 đỏ 3 xanh 2 vàng, rút 3; có vàng: 84 − 35 = 49; đủ 3 màu: 4·3·2 = 24 → 24/49."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS334', 'answer': '24/49'}
PROBLEM = ['Hộp $4$ đỏ, $3$ xanh, $2$ vàng. Rút $3$ bi, biết',
           'có ít nhất $1$ bi vàng. Xác suất có đủ',
           'ba màu?']
OPTIONS = ['24/49', '8/21', '1/2']
CORRECT = 0
ANSWER_VALUE = 24 / 49
BALLS = 'RRRRBBBYY'
T = list(combinations(range(9), 3))
COND = [t for t in T if any(BALLS[i] == 'Y' for i in t)]
FULL = [t for t in COND if len({BALLS[i] for i in t}) == 3]

BEATS = [
    Beat('hook', 'hook', 'Hộp có bốn bi đỏ, ba bi xanh, hai bi vàng. Rút ngẫu nhiên ba bi, biết có ít nhất một bi vàng. '
                         'Xác suất ba bi có đủ cả ba màu là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai mươi bốn phần bốn mươi chín, tám phần hai mươi mốt, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có tám mươi tư cách rút ba bi. Không có bi vàng nào: chọn ba trong bảy bi đỏ xanh, ba mươi lăm cách. Điều kiện còn bốn mươi chín.'),
    Beat('s2', 'solve', 'Đủ ba màu thì mỗi màu đúng một bi: bốn nhân ba nhân hai, hai mươi bốn cách. Tất cả đều có bi vàng nên nằm trong điều kiện.'),
    Beat('s3', 'solve', 'Xác suất hai mươi bốn phần bốn mươi chín, gần một nửa. Không có điều kiện thì chỉ hai mươi bốn phần tám mươi tư.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi bốn phần bốn mươi chín. Điều kiện ít nhất một: dùng phần bù để đếm mẫu số.'),
    Beat('outro', 'outro', outro_text(334)),
]

FORMULAS = formulas('24/49', OPTIONS,
                    cond='C_9^3 - C_7^3 = 84 - 35 = 49',
                    full='4 dot 3 dot 2 = 24',
                    prob='P = 24/49')


def validate() -> bool:
    assert len(COND) == 49 and len(FULL) == 24
    assert F(len(FULL), len(COND)) == F(24, 49)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS334(ShortScene):
    N = 334

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn(BALLS, cols=5, r=.3).move_to([0, 2.0, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))
        self.row = ball_row('RBY', y=.4, r=.38, buff=.5)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.row, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        m = self.M('cond', 1.5)
        self.write_board(m)

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.row.animate.scale(1.2), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.write_board(self.M('full', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS318 · An đến sớm — a, b đều trong [0; 1] giờ, gặp nếu |a − b| < 1/4; biết a < 1/4: ∫(a + 1/4) da / (1/4) = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN  # noqa: E402
from xss._sqkit import Unit  # noqa: E402

EPISODE = {'code': 'XSS318', 'answer': '3/8'}
PROBLEM = ['Hai bạn đến ngẫu nhiên trong $1$ giờ, ai',
           'đến trước chờ $15$ phút. Biết An đến',
           'trong $15$ phút đầu. $P("gặp nhau")$?']
OPTIONS = ['7/16', '3/8', '1/4']
CORRECT = 1
ANSWER_VALUE = 3 / 8
U = Unit()
Q = F(1, 4)

BEATS = [
    Beat('hook', 'hook', 'An và Bình hẹn nhau, mỗi người đến ngẫu nhiên trong một giờ, ai đến trước chỉ chờ mười lăm phút. '
                         'Biết An đến trong mười lăm phút đầu. Xác suất hai bạn gặp nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Bảy phần mười sáu, ba phần tám, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Thời điểm đến của An và Bình là một điểm trong hình vuông đơn vị. Gặp nhau khi hai thời điểm lệch dưới một phần tư giờ: dải quanh đường chéo.'),
    Beat('s2', 'solve', 'Điều kiện An đến sớm là dải dọc rộng một phần tư bên trái. Phần gặp nhau trong dải đó là hình thang có hai đáy một phần tư và một phần hai.'),
    Beat('s3', 'solve', 'Diện tích hình thang bằng ba phần ba mươi hai. Chia cho diện tích dải điều kiện một phần tư, được ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Không có điều kiện thì xác suất là bảy phần mười sáu; đến sớm lại làm khả năng gặp giảm, vì nửa cửa sổ chờ rơi ra ngoài giờ hẹn.'),
    Beat('outro', 'outro', outro_text(318)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    meet='abs(a - b) < 1/4',
                    trap='S = (1/4 + 1/2)/2 dot 1/4 = 3/32',
                    prob='P = (3/32)/(1/4) = 3/8')


def validate() -> bool:
    trap = (Q + 2 * Q) / 2 * Q
    assert trap == F(3, 32) and trap / Q == F(3, 8)
    assert 1 - (1 - Q) ** 2 == F(7, 16)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS318(ShortScene):
    N = 318

    def hook_visual(self, t0):
        self.board_top = -1.75
        self.sq = U.frame(self, 'a', 'b')
        self.wait_until(.5, t0)
        self.play(FadeIn(self.sq), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        band = U.region([(0, 0), (.25, 0), (1, .75), (1, 1), (.75, 1), (0, .25)], CYAN, .3, 3)
        self.play(FadeIn(band), run_time=self.rt(.08))
        self.write_board(self.M('meet', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        strip = U.region([(0, 0), (.25, 0), (.25, 1), (0, 1)], GOLD, .2, 4)
        self.play(FadeIn(strip), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.trap = U.region([(0, 0), (.25, 0), (.25, .5), (0, .25)], GREEN, .85)
        self.play(FadeIn(self.trap), run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        self.write_board(self.M('trap', 1.5))
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

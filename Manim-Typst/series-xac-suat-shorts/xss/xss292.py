"""XSS292 · Bao nhiêu bước qua sông? — E(k) = 1 + (E(k−1) + E(k−2))/2, E(0) = E(−1) = 0: 1, 3/2, 9/4, 23/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS292', 'answer': '23/8'}
PROBLEM = ['Tung xu: ngửa thì ếch nhảy $1$ lá, sấp thì',
           'nhảy $2$ lá. Trung bình cần mấy bước để',
           'ếch tới hoặc vượt qua lá số $4$?']
OPTIONS = ['8/3', '23/8', '3']
CORRECT = 1
ANSWER_VALUE = None


def cross(n):
    e = {-1: F(0), 0: F(0)}
    for k in range(1, n + 1):
        e[k] = 1 + (e[k - 1] + e[k - 2]) / 2
    return e


def brute():
    tot = F(0)
    for w in product((1, 2), repeat=4):
        s, n = 0, 0
        for x in w:
            s += x
            n += 1
            if s >= 4:
                break
        tot += F(1, 16) * n
    return tot


BEATS = [
    Beat('hook', 'hook', 'Ếch qua sông: mỗi bước tung đồng xu, ngửa nhảy một lá, sấp nhảy hai lá. Bờ bên kia ở lá số bốn, tới hoặc vượt qua là xong. '
                         'Trung bình ếch cần bao nhiêu bước?'),
    Beat('guess', 'hook', 'Tám phần ba, hai mươi ba phần tám, hay ba bước? Ba, hai, một!'),
    Beat('s1', 'solve', 'Quy hoạch động ngược: gọi E k là số bước trung bình khi còn cách bờ k lá. Mỗi bước tốn một, rồi còn k trừ một hoặc k trừ hai lá.'),
    Beat('s2', 'solve', 'E k bằng một cộng nửa E k trừ một cộng nửa E k trừ hai, với E không và E âm một bằng không, vì đã lên bờ. '
                        'E một bằng một, E hai một phẩy năm, E ba chín phần tư.'),
    Beat('s3', 'solve', 'E bốn bằng một cộng nửa của chín phần tư cộng một phẩy năm, bằng hai mươi ba phần tám, khoảng hai phẩy chín bước.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi ba phần tám. Quy hoạch động cũng tính được kỳ vọng, không chỉ xác suất!'),
    Beat('outro', 'outro', outro_text(292)),
]

FORMULAS = formulas('23/8', OPTIONS,
                    rec='E_k = 1 + 1/2 E_(k-1) + 1/2 E_(k-2), quad E_0 = E_(-1) = 0',
                    vals='E_1 = 1, quad E_2 = 3/2, quad E_3 = 9/4, quad E_4 = 23/8')


def validate() -> bool:
    assert cross(4)[4] == brute() == F(23, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS292(ShortScene):
    N = 292

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = pads(range(5), y=1.7)
        self.row[-1].set_fill(GOLD, .8)
        self.labs = VGroup(*[self.TM(f'${k}$', 26, SOFT).next_to(q, [0, -1, 0], buff=.15) for k, q in enumerate(self.row)])
        self.fr = frog().move_to(self.row[0])
        self.wait_until(.7, t0)
        self.play(FadeIn(self.row), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        for k in (2, 3):
            self.play(self.fr.animate.move_to(self.row[k]), run_time=self.rt(.04))
        self.wait_until(.5, t0)
        self.play(self.fr.animate.move_to(self.row[4]).shift([.6, 0, 0]), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.M('rec', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('vals', 1.5)
        self.write_board(m)
        self.frame(m)

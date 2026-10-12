"""XSS311 · Chờ ba ngửa liên tiếp — trạng thái = số ngửa liên tiếp đang có; E_0 = 14 (= 2 + 4 + 8)."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import RIGHT, Arrow, CurvedArrow, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS311', 'answer': '14'}
PROBLEM = ['Tung đồng xu đến khi có $3$ lần ngửa',
           'liên tiếp. Trung bình cần bao nhiêu',
           'lần tung?']
OPTIONS = ['8', '12', '14']
CORRECT = 2
ANSWER_VALUE = 14


def exact():
    # E_k = 1 + E_(k+1)/2 + E_0/2, E_3 = 0; write E_k = a_k + b_k E_0 and solve backwards
    a, b = F(0), F(0)
    for _ in range(3):
        a, b = 1 + a / 2, b / 2 + F(1, 2)
    return a / (1 - b)


def simulate(n=20000, seed=311):
    rnd, tot = random.Random(seed), 0
    for _ in range(n):
        run = k = 0
        while run < 3:
            k += 1
            run = run + 1 if rnd.random() < .5 else 0
        tot += k
    return tot / n


BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu liên tục cho đến khi được ba lần ngửa liên tiếp thì dừng. '
                         'Trung bình phải tung bao nhiêu lần? Nhiều người đoán tám, vì hai mũ ba bằng tám.'),
    Beat('guess', 'hook', 'Tám lần, mười hai lần, hay mười bốn lần? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trạng thái là số lần ngửa liên tiếp đang có: không, một hoặc hai. Ngửa thì tiến lên một bậc, sấp thì rơi về không.'),
    Beat('s2', 'solve', 'Gọi E k là số lần tung trung bình còn lại. E k bằng một cộng nửa E k cộng một cộng nửa E không, và E ba bằng không.'),
    Beat('s3', 'solve', 'Giải ngược từ E hai lên E không, ta được E không bằng mười bốn. Đẹp hơn nữa: mười bốn bằng hai cộng bốn cộng tám.'),
    Beat('s4', 'solve', 'Mô phỏng hai mươi nghìn lượt chơi cũng cho trung bình khoảng mười bốn lần tung.'),
    Beat('answer', 'solve', 'Đáp án: mười bốn lần, không phải tám. Mỗi cú sấp xóa sạch công sức, nên chuỗi càng dài càng đắt.'),
    Beat('outro', 'outro', outro_text(311)),
]

FORMULAS = formulas('14', OPTIONS,
                    rec='E_k = 1 + 1/2 E_(k+1) + 1/2 E_0, quad E_3 = 0',
                    e0='E_0 = 14 = 2 + 4 + 8')


def validate() -> bool:
    assert exact() == 14
    assert abs(simulate() - 14) < .5
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS311(ShortScene):
    N = 311

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.st = VGroup(*[token(str(k), GOLD if k == 3 else CYAN, .42) for k in range(4)]).arrange(RIGHT, buff=1.0).move_to([0, 1.2, 0])
        self.fw = VGroup(*[Arrow(self.st[k].get_right(), self.st[k + 1].get_left(), buff=.06, color=GREEN, stroke_width=5)
                           for k in range(3)])
        self.back = VGroup(*[CurvedArrow(self.st[k].get_bottom(), self.st[0].get_bottom() + [.12 * k, 0, 0], angle=-1.4 + .2 * k,
                                         color=CORAL, stroke_width=4) for k in (1, 2)])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.st, lag_ratio=.2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.fw, lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.7, t0)
        self.play(FadeIn(self.back), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.M('rec', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        m = self.M('e0', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s4(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(VGroup(self.TM('mô phỏng:', 28, SOFT), self.MNum(simulate(), 2, GREEN, 34)).arrange(RIGHT, buff=.2), anim='fade')

"""XSS426 · Mỗi người một lá át — xếp 52 lá thành 4 chồng 13; xếp lần lượt 4 át: 39/51 · 26/50 · 13/49 = 2197/20825 ≈ 0,105."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import card_back, playing_card  # noqa: E402

EPISODE = {'code': 'XSS426', 'answer': '2197/20825 ≈ 0,105'}
PROBLEM = ['Chia bộ bài $52$ lá cho $4$ người, mỗi người',
           '$13$ lá. Xác suất mỗi người có đúng $1$ át?']
OPTIONS = ['2197/20825 approx "0,105"', 'approx "0,25"', 'approx "0,04"']
CORRECT = 0
ANSWER_VALUE = 2197 / 20825
SEQ = F(39, 51) * F(26, 50) * F(13, 49)


def by_counting():
    good = factorial(4) * comb(48, 12) * comb(36, 12) * comb(24, 12)
    total = comb(52, 13) * comb(39, 13) * comb(26, 13)
    return F(good, total)


BEATS = [
    Beat('hook', 'hook', 'Chia đều bộ bài năm mươi hai lá cho bốn người, mỗi người mười ba lá. Xác suất mỗi người có đúng một lá át là bao nhiêu?'),
    Beat('guess', 'hook', 'Khoảng không phẩy một không năm, không phẩy hai lăm, hay không phẩy không bốn? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo: chỉ theo dõi vị trí bốn lá át trong năm mươi hai chỗ. Lá át thứ nhất ở đâu cũng được.'),
    Beat('s2', 'solve', 'Lá át thứ hai phải rơi vào chồng của ba người kia: ba mươi chín trên năm mươi mốt chỗ còn lại. Lá thứ ba: hai mươi sáu trên năm mươi. Lá thứ tư: mười ba trên bốn mươi chín.'),
    Beat('s3', 'solve', 'Nhân lại được hai nghìn một trăm chín mươi bảy phần hai mươi nghìn tám trăm hai mươi lăm, khoảng mười phẩy năm phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy một không năm. Đặt lần lượt các lá đặc biệt vào chỗ thay vì đếm cả bộ bài.'),
    Beat('outro', 'outro', outro_text(426)),
]

FORMULAS = formulas('2197/20825 approx "0,105"', OPTIONS,
                    seq='P = 39/51 dot 26/50 dot 13/49',
                    prob='P = 2197/20825 approx "0,105"')


def validate() -> bool:
    assert SEQ == by_counting() == F(2197, 20825)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS426(ShortScene):
    N = 426

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.hands = VGroup(*[VGroup(card_back(.7), playing_card('A', s, .7)).arrange(buff=-.35) for s in 'SHDC']).arrange(buff=.45).move_to([0, 1.4, 0])
        self.wait_until(.5, t0)
        self.play(*[FadeIn(h[0]) for h in self.hands], run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(self.hands[0][1]), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        for i, f in enumerate((.1, .4, .7)):
            self.wait_until(f, t0)
            self.play(FadeIn(self.hands[i + 1][1]), run_time=self.rt(.04))
        self.write_board(self.M('seq', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

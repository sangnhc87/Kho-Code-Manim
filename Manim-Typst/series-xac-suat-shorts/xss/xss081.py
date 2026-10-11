"""XSS081 · Lần thứ 3 mới gặp lỗi — 10 sản phẩm, 3 lỗi: 7/10 · 6/9 · 3/8 = 7/40."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import DOWN, FadeIn, RIGHT, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS081', 'answer': '7/40'}
PROBLEM = ['Lô $10$ sản phẩm có $3$ sản phẩm lỗi, kiểm',
           'tra lần lượt. Xác suất lần thứ $3$ mới',
           'gặp sản phẩm lỗi đầu tiên?']
OPTIONS = ['3/10', '7/40', '1/8']
CORRECT = 1
ANSWER_VALUE = 7 / 40

BEATS = [
    Beat('hook', 'hook', 'Lô hàng mười sản phẩm có ba sản phẩm lỗi. Kiểm tra lần lượt từng cái, không trả lại. '
                         'Xác suất đến lần kiểm tra thứ ba mới gặp sản phẩm lỗi đầu tiên là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần mười, bảy phần bốn mươi, hay một phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lần thứ ba mới gặp lỗi nghĩa là: lần một tốt, lần hai tốt, lần ba lỗi. '
                        'Lần một: bảy sản phẩm tốt trong mười, xác suất bảy phần mười.'),
    Beat('s2', 'solve', 'Biết lần một tốt, còn sáu tốt trong chín: sáu phần chín. Biết hai lần đầu tốt, '
                        'còn ba lỗi trong tám: ba phần tám.'),
    Beat('s3', 'solve', 'Nhân dọc chuỗi: bảy phần mười nhân sáu phần chín nhân ba phần tám, bằng bảy phần bốn mươi. '
                        'Mỗi lần kiểm tra, hộp thay đổi, nên mẫu số giảm dần.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần bốn mươi. Chuỗi sự kiện không hoàn lại: nhân các xác suất có điều kiện!'),
    Beat('outro', 'outro', outro_text(81)),
]

FORMULAS = formulas('7/40', OPTIONS, prob='P = 7/10 dot 6/9 dot 3/8 = 7/40')


def validate() -> bool:
    picks = list(combinations(range(10), 3))  # positions of the defective items in the inspection order
    assert F(sum(min(p) == 2 for p in picks), len(picks)) == F(7, 40) == F(7, 10) * F(6, 9) * F(3, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS081(ShortScene):
    N = 81

    def step(self, i, ok, frac_key):
        c = card(1.8, 1.6, GREEN if ok else CORAL, PANEL, radius=.18, stroke_width=4)
        g = VGroup(c, tx('tốt' if ok else 'lỗi', 30, GREEN if ok else CORAL, bold=True).move_to(c.get_center() + [0, .3, 0]),
                   self.TM(f'${frac_key}$', 30, GOLD).move_to(c.get_center() + [0, -.35, 0]))
        lab = tx(f'lần {i}', 24, SOFT).next_to(c, DOWN, buff=.12)
        return VGroup(g, lab)

    def hook_visual(self, t0):
        self.steps = VGroup(self.step(1, True, '7/10'), self.step(2, True, '6/9'), self.step(3, False, '3/8'))
        self.steps.arrange(buff=.35).move_to([0, 1.4, 0])

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.steps[0][1]), FadeIn(self.steps[1][1]), FadeIn(self.steps[2][1]), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.steps[0][0], shift=RIGHT * .3), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.steps[1][0], shift=RIGHT * .3), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.steps[2][0], shift=RIGHT * .3), run_time=self.rt(.08))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('mẫu số giảm dần: 10, 9, 8', 28, SOFT), anim='fade')

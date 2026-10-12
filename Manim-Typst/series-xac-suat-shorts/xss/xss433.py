"""XSS433 · Ước chính phương — 360 = 2³·3²·5: 4·3·2 = 24 ước; chính phương ⇔ số mũ chẵn: 2·2·1 = 4 → 1/6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS433', 'answer': '1/6'}
PROBLEM = ['Chọn ngẫu nhiên một ước dương của $360$.',
           'Xác suất ước đó là số chính phương?']
OPTIONS = ['1/6', '1/4', '1/8']
CORRECT = 0
ANSWER_VALUE = 1 / 6
DIV = [d for d in range(1, 361) if 360 % d == 0]
SQ = [d for d in DIV if isqrt(d) ** 2 == d]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên một ước dương của ba trăm sáu mươi. Xác suất ước đó là một số chính phương?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần tư, hay một phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Phân tích: ba trăm sáu mươi bằng hai mũ ba nhân ba mũ hai nhân năm. Mỗi ước chọn số mũ của hai từ không đến ba, của ba từ không đến hai, của năm không hoặc một: bốn nhân ba nhân hai, hai mươi tư ước.'),
    Beat('s2', 'solve', 'Ước chính phương khi mọi số mũ đều chẵn: số mũ của hai là không hoặc hai, của ba là không hoặc hai, của năm phải là không. Hai nhân hai nhân một, bốn ước: một, bốn, chín, ba mươi sáu.'),
    Beat('s3', 'solve', 'Xác suất bốn phần hai mươi tư, tức một phần sáu.'),
    Beat('answer', 'solve', 'Đáp án: một phần sáu. Đếm ước bằng số mũ: bài số học trở thành bài đếm tổ hợp.'),
    Beat('outro', 'outro', outro_text(433)),
]

FORMULAS = formulas('1/6', OPTIONS,
                    fac='360 = 2^3 dot 3^2 dot 5 => 4 dot 3 dot 2 = 24',
                    sq='2 dot 2 dot 1 = 4: quad 1, 4, 9, 36',
                    prob='P = 4/24 = 1/6')


def validate() -> bool:
    assert len(DIV) == 24 and SQ == [1, 4, 9, 36] and F(len(SQ), len(DIV)) == F(1, 6)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS433(ShortScene):
    N = 433

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.divs = VGroup(*[token(str(d), SOFT, .3, size=18) for d in DIV]).arrange_in_grid(rows=4, cols=6, buff=(.18, .18)).move_to([0, 1.0, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.divs, lag_ratio=.03), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('fac', 1.3))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(*[t[0].animate.set_fill(GOLD) for t, d in zip(self.divs, DIV) if d in SQ], run_time=self.rt(.06))
        self.clear_board(.03)
        self.write_board(self.M('sq', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

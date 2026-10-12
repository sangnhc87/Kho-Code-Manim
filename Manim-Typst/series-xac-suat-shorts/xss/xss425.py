"""XSS425 · Đủ sáu mặt trong sáu lần — 6!/6⁶ = 720/46656 = 5/324 ≈ 1,5 %."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import factorial
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS425', 'answer': '5/324'}
PROBLEM = ['Gieo $6$ con xúc xắc. Xác suất xuất hiện',
           'đủ cả $6$ mặt?']
OPTIONS = ['5/324', '1/6', '1/46656']
CORRECT = 0
ANSWER_VALUE = 5 / 324

BEATS = [
    Beat('hook', 'hook', 'Gieo cùng lúc sáu con xúc xắc. Xác suất sáu con ra đủ cả sáu mặt, từ một đến sáu, là bao nhiêu? Nghe có vẻ không quá hiếm.'),
    Beat('guess', 'hook', 'Năm phần ba trăm hai mươi tư, một phần sáu, hay một phần bốn mươi sáu nghìn sáu trăm năm mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Coi sáu con xúc xắc có màu khác nhau: sáu mũ sáu, bốn mươi sáu nghìn sáu trăm năm mươi sáu kết quả đồng khả năng.'),
    Beat('s2', 'solve', 'Đủ sáu mặt nghĩa là sáu con là một hoán vị của một đến sáu: sáu giai thừa, bảy trăm hai mươi kết quả.'),
    Beat('s3', 'solve', 'Xác suất bảy trăm hai mươi chia bốn mươi sáu nghìn sáu trăm năm mươi sáu, rút gọn năm phần ba trăm hai mươi tư, chỉ khoảng một phẩy năm phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: năm phần ba trăm hai mươi tư. Đủ bộ khó hơn rất nhiều so với cảm giác: trùng mặt mới là điều bình thường.'),
    Beat('outro', 'outro', outro_text(425)),
]

FORMULAS = formulas('5/324', OPTIONS,
                    all='6^6 = 46656',
                    good='6! = 720',
                    prob='P = 720/46656 = 5/324')


def validate() -> bool:
    assert F(factorial(6), 6 ** 6) == F(5, 324)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS425(ShortScene):
    N = 425

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.dice = VGroup(*[die(v, .75) for v in (3, 6, 1, 3, 5, 2)]).arrange(buff=.25).move_to([0, 1.5, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.dice, lag_ratio=.15), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        good = VGroup(*[die(v, .75) for v in (4, 1, 6, 2, 5, 3)]).arrange(buff=.25).move_to([0, 1.5, 0])
        self.play(self.dice.animate.become(good), run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

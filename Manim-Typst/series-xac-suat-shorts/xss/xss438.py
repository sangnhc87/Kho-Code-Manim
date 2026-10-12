"""XSS438 · Bốn xúc xắc sát nhau — max − min ≤ 1: cùng mặt 6, hoặc dùng đúng 2 giá trị liên tiếp {k; k+1}: 5·(2⁴ − 2) = 70 → 76/1296 = 19/324."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS438', 'answer': '19/324'}
PROBLEM = ['Gieo $4$ xúc xắc. Xác suất số lớn nhất và',
           'nhỏ nhất hơn kém nhau không quá $1$?']
OPTIONS = ['19/324', '1/54', '5/162']
CORRECT = 0
ANSWER_VALUE = 19 / 324

BEATS = [
    Beat('hook', 'hook', 'Gieo bốn con xúc xắc. Xác suất số lớn nhất và số nhỏ nhất hơn kém nhau không quá một, tức bốn con sát nhau, là bao nhiêu?'),
    Beat('guess', 'hook', 'Mười chín phần ba trăm hai mươi tư, một phần năm mươi tư, hay năm phần một trăm sáu mươi hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có sáu mũ bốn, một nghìn hai trăm chín mươi sáu kết quả. Trường hợp một: cả bốn cùng mặt, sáu kết quả.'),
    Beat('s2', 'solve', 'Trường hợp hai: chỉ dùng đúng hai giá trị liên tiếp k và k cộng một, có năm cặp. Mỗi con chọn một trong hai giá trị, trừ hai cách toàn một giá trị: mười sáu trừ hai, mười bốn. Năm nhân mười bốn, bảy mươi.'),
    Beat('s3', 'solve', 'Tổng bảy mươi sáu trên một nghìn hai trăm chín mươi sáu, rút gọn mười chín phần ba trăm hai mươi tư.'),
    Beat('answer', 'solve', 'Đáp án: mười chín phần ba trăm hai mươi tư. Tách theo tập giá trị xuất hiện, rồi trừ phần đã đếm.'),
    Beat('outro', 'outro', outro_text(438)),
]

FORMULAS = formulas('19/324', OPTIONS,
                    same='"cùng mặt": 6',
                    two='"hai giá trị kề": 5 dot (2^4 - 2) = 70',
                    prob='P = (6 + 70)/6^4 = 76/1296 = 19/324')


def validate() -> bool:
    good = sum(max(t) - min(t) <= 1 for t in product(range(1, 7), repeat=4))
    assert good == 76 and F(good, 1296) == F(19, 324)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS438(ShortScene):
    N = 438

    def roll(self, vals, frac=.06):
        new = VGroup(*[die(v, .8) for v in vals]).arrange(buff=.35).move_to([0, 1.4, 0])
        if self.dice is None:
            self.play(FadeIn(new, lag_ratio=.15), run_time=self.rt(frac))
        else:
            self.play(self.dice.animate.become(new), run_time=self.rt(frac))
        self.dice = self.dice or new

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.dice = None
        self.wait_until(.45, t0)
        self.roll((2, 5, 3, 6))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.roll((4, 4, 4, 4))
        self.write_board(self.M('same', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.roll((3, 4, 4, 3))
        self.write_board(self.M('two', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

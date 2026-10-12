"""XSS244 · Ba mặt khác nhau có 6? — 120 bộ khác nhau, không có 6: 5·4·3 = 60 → P = 1 − 60/120 = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS244', 'answer': '1/2'}
PROBLEM = ['Gieo $3$ xúc xắc, biết ba mặt khác nhau.', 'Xác suất có ít nhất một mặt $6$?']
OPTIONS = ['91/216', '1/2', '5/9']
CORRECT = 1
ANSWER_VALUE = .5
THREE = list(product(range(1, 7), repeat=3))

BEATS = [
    Beat('hook', 'hook', 'Gieo ba con xúc xắc, biết ba mặt đều khác nhau. Xác suất có ít nhất một mặt sáu là bao nhiêu?'),
    Beat('guess', 'hook', 'Chín mươi mốt phần hai trăm mười sáu, một phần hai, hay năm phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba mặt khác nhau: sáu nhân năm nhân bốn, một trăm hai mươi kết quả. Thực chất là chọn ba số khác nhau trong sáu số.'),
    Beat('s2', 'solve', 'Phần bù: không có mặt sáu, ba số khác nhau lấy từ một đến năm: năm nhân bốn nhân ba, sáu mươi kết quả.'),
    Beat('s3', 'solve', 'Xác suất bằng một trừ sáu mươi phần một trăm hai mươi, đúng một phần hai. Trực giác: chọn ba trong sáu số, '
                        'mỗi số có mặt với xác suất ba phần sáu.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Thử thách tiếp: đảo hai điều kiện thì kết quả thay đổi thế nào?'),
    Beat('outro', 'outro', outro_text(244)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    nb='n(B) = 6 dot 5 dot 4 = 120',
                    comp='P = 1 - (5 dot 4 dot 3)/120 = 1/2')


def validate() -> bool:
    b = [w for w in THREE if len(set(w)) == 3]
    assert len(b) == 120 and F(sum(6 in w for w in b), 120) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS244(ShortScene):
    N = 244

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.dice = VGroup(*[die(v, 1.1) for v in (2, 6, 4)]).arrange(buff=.5).move_to([0, 2.0, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.dice, lag_ratio=.3), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('nb', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.play(self.dice[1][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.04))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('comp', 2.0)
        self.write_board(m)
        self.frame(m)

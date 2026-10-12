"""XSS245 · Có 6 thì khác nhau? — 91 bộ có mặt 6; khác nhau và có 6: 3·5·4 = 60 → 60/91."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS245', 'answer': '60/91'}
PROBLEM = ['Gieo $3$ xúc xắc, biết có ít nhất một mặt',
           '$6$. Xác suất ba mặt đôi một khác nhau?']
OPTIONS = ['5/9', '60/91', '1/2']
CORRECT = 1
ANSWER_VALUE = 60 / 91
THREE = list(product(range(1, 7), repeat=3))

BEATS = [
    Beat('hook', 'hook', 'Đảo điều kiện của thử thách trước: gieo ba xúc xắc, biết có ít nhất một mặt sáu. '
                         'Xác suất ba mặt đôi một khác nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần chín, sáu mươi phần chín mươi mốt, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có ít nhất một mặt sáu: lấy hai trăm mười sáu trừ năm mũ ba, bằng chín mươi mốt kết quả.'),
    Beat('s2', 'solve', 'Ba mặt khác nhau và có một mặt sáu: chọn vị trí của mặt sáu, ba cách; hai vị trí còn lại là hai số khác nhau từ một đến năm, '
                        'năm nhân bốn. Tổng sáu mươi.'),
    Beat('s3', 'solve', 'Xác suất sáu mươi phần chín mươi mốt, khác hẳn một phần hai của chiều ngược lại. Tử số giống nhau, mẫu số khác nhau.'),
    Beat('answer', 'solve', 'Đáp án: sáu mươi phần chín mươi mốt. Đảo điều kiện là đổi mẫu số!'),
    Beat('outro', 'outro', outro_text(245)),
]

FORMULAS = formulas('60/91', OPTIONS,
                    nb='n(B) = 6^3 - 5^3 = 91',
                    nab='n(A sect B) = 3 dot 5 dot 4 = 60',
                    prob='P(A | B) = 60/91')


def validate() -> bool:
    b = [w for w in THREE if 6 in w]
    assert len(b) == 91 and F(sum(len(set(w)) == 3 for w in b), 91) == F(60, 91)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS245(ShortScene):
    N = 245

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.dice = VGroup(*[die(v, 1.1) for v in (6, 3, 5)]).arrange(buff=.5).move_to([0, 2.0, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.dice, lag_ratio=.3), run_time=self.rt(.12))
        self.play(self.dice[0][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.04))

    def beat_s1(self, T):
        self.write_board(self.M('nb', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('nab', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('đảo điều kiện → đổi mẫu số', 26, CORAL, bold=True), anim='fade')

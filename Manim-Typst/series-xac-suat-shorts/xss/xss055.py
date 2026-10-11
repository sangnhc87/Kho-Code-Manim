"""XSS055 · Ba mặt khác nhau — 6·5·4/216 = 120/216 = 5/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, PANEL  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS055', 'answer': '5/9'}
PROBLEM = ['Gieo ba con xúc xắc.', 'Xác suất ba mặt đôi một khác nhau?']
OPTIONS = ['1/2', '5/9', '2/3']
CORRECT = 1
ANSWER_VALUE = 5 / 9

BEATS = [
    Beat('hook', 'hook', 'Gieo ba con xúc xắc. Xác suất ba mặt đôi một khác nhau, không có hai con nào trùng số, là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, năm phần chín, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gieo lần lượt. Con thứ nhất ra mặt nào cũng được: sáu khả năng. '
                        'Con thứ hai phải khác con thứ nhất: còn năm khả năng.'),
    Beat('s2', 'solve', 'Con thứ ba phải khác cả hai con trước: còn bốn khả năng. '
                        'Số kết quả thuận lợi là sáu nhân năm nhân bốn, bằng một trăm hai mươi.'),
    Beat('s3', 'solve', 'Xác suất bằng một trăm hai mươi phần hai trăm mười sáu, rút gọn còn năm phần chín. '
                        'Nghĩa là gần một nửa số lần, sẽ có ít nhất hai con trùng nhau!'),
    Beat('answer', 'solve', 'Đáp án: năm phần chín. Đây là phiên bản thu nhỏ của nghịch lý ngày sinh mà ta sẽ gặp sau!'),
    Beat('outro', 'outro', outro_text(55)),
]

FORMULAS = formulas('5/9', OPTIONS,
                    a='n(A) = 6 dot 5 dot 4 = 120',
                    prob='P = 120/216 = 5/9',
                    rest='1 - 5/9 = 4/9 quad "có trùng"')


def validate() -> bool:
    space = list(product(range(1, 7), repeat=3))
    assert F(sum(len(set(w)) == 3 for w in space), 216) == F(5, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS055(ShortScene):
    N = 55

    def hook_visual(self, t0):
        self.trio = VGroup(*[die(v, 1.3) for v in (1, 4, 6)]).arrange(buff=.5).move_to([0, 1.5, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.trio, lag_ratio=.3), run_time=self.rt(.2))

    def tag(self, i, n):
        c = card(1.0, .75, CYAN, PANEL, radius=.12, stroke_width=3).next_to(self.trio[i], [0, -1, 0], buff=.25)
        return VGroup(c, self.TM(f'${n}$', 34, CYAN, bold=True).move_to(c))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.tag(0, 6)), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.tag(1, 5)), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.tag(2, 4)), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.M('a', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('rest', 1.7), anim='fade')



"""XSS088 · Cần bao nhiêu người? — P(trùng ngày sinh) > 99 % từ 57 người."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import Create, DashedLine, FadeIn, Line, VGroup, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from xss.xss087 import p_same  # noqa: E402

EPISODE = {'code': 'XSS088', 'answer': '57'}
PROBLEM = ['Cần ít nhất bao nhiêu người để xác suất',
           'có hai người trùng ngày sinh vượt $99%$?']
OPTIONS = ['57', '183', '365']
CORRECT = 0
ANSWER_VALUE = None
N99 = next(n for n in range(2, 366) if p_same(n) > .99)

BEATS = [
    Beat('hook', 'hook', 'Hai mươi ba người đã đủ để xác suất trùng ngày sinh vượt một nửa. '
                         'Vậy cần bao nhiêu người để gần như chắc chắn, trên chín mươi chín phần trăm?'),
    Beat('guess', 'hook', 'Năm mươi bảy, một trăm tám mươi ba, hay ba trăm sáu mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Để chắc chắn một trăm phần trăm, cần ba trăm sáu mươi sáu người theo nguyên lý chuồng bồ câu. '
                        'Nhưng chín mươi chín phần trăm thì cần ít hơn rất nhiều.'),
    Beat('s2', 'solve', 'Tính tiếp tích các phân số như thử thách trước, xác suất tăng rất nhanh: ba mươi người khoảng bảy mươi '
                        'phần trăm, bốn mươi người khoảng chín mươi phần trăm, năm mươi người khoảng chín mươi bảy phần trăm.'),
    Beat('s3', 'solve', 'Tới năm mươi bảy người, xác suất vượt chín mươi chín phần trăm. Chỉ khoảng một phần sáu số ngày '
                        'trong năm, mà gần như chắc chắn có hai người trùng ngày sinh!'),
    Beat('answer', 'solve', 'Đáp án: năm mươi bảy người. Một trường học có thể kiểm chứng điều này ngay trong một lớp đông!'),
    Beat('outro', 'outro', outro_text(88)),
]

FORMULAS = formulas('57', OPTIONS,
                    pigeon='366 " người" arrow.r.double P = 1',
                    p57='P(57) approx "0,990" > "0,99"')


def validate() -> bool:
    assert N99 == 57 and p_same(56) < .99 < p_same(57)
    assert round(p_same(30), 2) == .71 and round(p_same(40), 2) == .89 and round(p_same(50), 2) == .97
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS088(ShortScene):
    N = 88

    def hook_visual(self, t0):
        self.board_top = -1.0
        x0, x1, y0, y1 = -2.75, 3.1, -.3, 2.9
        X = lambda n: x0 + (x1 - x0) * n / 70  # noqa: E731
        Y = lambda p: y0 + (y1 - y0) * p  # noqa: E731
        self.X, self.Y = X, Y
        self.axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], color=SOFT, stroke_width=3),
                           Line([x0, y0, 0], [x0, y1, 0], color=SOFT, stroke_width=3))
        self.path = VMobject(stroke_color=CYAN, stroke_width=5)
        self.path.set_points_smoothly([[X(n), Y(p_same(n)), 0] for n in range(1, 71)])
        self.top = DashedLine([x0, Y(.99), 0], [x1, Y(.99), 0], color=CORAL, stroke_width=2)
        self.labs = VGroup(self.TM('$99%$', 22, CORAL).next_to([x0, Y(.99), 0], [-1, 0, 0], buff=.1),
                           self.TM('$70$', 22, SOFT).next_to([x1, y0, 0], [0, -1, 0], buff=.1),
                           tx('số người', 20, SOFT).next_to([X(35), y0, 0], [0, -1, 0], buff=.12))
        self.wait_until(.5, t0)
        self.play(Create(self.axes), FadeIn(self.top), FadeIn(self.labs), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('pigeon', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(Create(self.path), run_time=self.rt(.6), rate_func=lambda u: u)
        self.wait_until(.75, t0)

    def beat_s3(self, T):
        t0 = self.now()
        mark = DashedLine([self.X(57), -.3, 0], [self.X(57), self.Y(p_same(57)), 0], color=GOLD, stroke_width=3)
        lab = self.TM('$57$', 26, GOLD, bold=True).next_to([self.X(57), -.3, 0], [0, -1, 0], buff=.1)
        self.play(Create(mark), FadeIn(lab), run_time=self.rt(.08))
        m = self.M('p57', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('chỉ cần 57 trong 365 ngày!', 28, GOLD, bold=True), anim='fade')

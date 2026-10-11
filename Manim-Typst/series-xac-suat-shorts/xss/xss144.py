"""XSS144 · Học thêm cả hai môn — công thức nhân P(T ∩ L) = P(T)·P(L | T) = 0,6·0,7 = 0,42."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS144', 'answer': '0,42'}
PROBLEM = ['$60%$ học sinh học thêm Toán; trong',
           'số đó $70%$ học thêm Lý. Xác suất',
           'học thêm cả Toán và Lý?']
OPTIONS = ['"0,7"', '"0,42"', '"1,3"']
CORRECT = 1
ANSWER_VALUE = .42

BEATS = [
    Beat('hook', 'hook', 'Sáu mươi phần trăm học sinh học thêm Toán. Trong số những bạn học thêm Toán, bảy mươi phần trăm học thêm cả Lý. '
                         'Chọn ngẫu nhiên một học sinh, xác suất bạn đó học thêm cả hai môn là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bảy, không phẩy bốn hai, hay một phẩy ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chữ "trong số đó" là dấu hiệu của xác suất có điều kiện: bảy mươi phần trăm là xác suất học Lý khi biết đã học Toán, '
                        'không phải tính trên cả trường.'),
    Beat('s2', 'solve', 'Vẽ hình chữ nhật diện tích một: phần học Toán rộng không phẩy sáu. Trong phần đó, tô bảy mươi phần trăm chiều cao.'),
    Beat('s3', 'solve', 'Diện tích phần tô bằng không phẩy sáu nhân không phẩy bảy, bằng không phẩy bốn hai. '
                        'Đây là công thức nhân xác suất: P của A giao B bằng P của A nhân P của B khi biết A.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bốn hai. Không phẩy bảy là bẫy: quên mất điều kiện "trong số đó"!'),
    Beat('outro', 'outro', outro_text(144)),
]

FORMULAS = formulas('"0,42"', OPTIONS,
                    cond='P(L | T) = "0,7"',
                    mult='P(T sect L) = P(T) dot P(L | T) = "0,6" dot "0,7" = "0,42"')


def validate() -> bool:
    assert round(.6 * .7, 2) == .42
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS144(ShortScene):
    N = 144

    def hook_visual(self, t0):
        self.board_top = -1.3
        W, H, x0, y0 = 6.4, 3.0, -3.2, -.2
        self.area = Rectangle(width=W, height=H, stroke_color=STROKE, stroke_width=3).move_to([x0 + W / 2, y0 + H / 2, 0])
        self.math = Rectangle(width=W * .6, height=H, stroke_width=0, fill_color=CYAN, fill_opacity=.35) \
            .move_to([x0 + W * .3, y0 + H / 2, 0])
        self.both = Rectangle(width=W * .6, height=H * .7, stroke_width=0, fill_color=GOLD, fill_opacity=.75) \
            .move_to([x0 + W * .3, y0 + H * .35, 0])
        self.labels = VGroup(self.TM('Toán $"0,6"$', 26, CYAN).next_to(self.math, [0, 1, 0], buff=.1),
                             self.TM('$"0,7"$', 30, '#0B1220').next_to(self.both, [1, 0, 0], buff=-.85),
                             tx('không học Toán', 22, SOFT).move_to([x0 + W * .8, y0 + H / 2, 0]))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.area), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.math), FadeIn(self.labels[0]), FadeIn(self.labels[2]), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.write_board(self.M('cond', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(FadeIn(self.both), FadeIn(self.labels[1]), run_time=self.rt(.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('mult', 1.7)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('"0,7": quên điều kiện', 28, CORAL, bold=True), anim='fade')

"""XSS087 · Nghịch lý ngày sinh — 23 người: 1 − 365·364·…·343/365²³ ≈ 0,507."""
from __future__ import annotations

import sys
from math import comb
from pathlib import Path

from manim import Create, DOWN, DashedLine, FadeIn, Line, VGroup, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS087', 'answer': '≈ 0,507'}
PROBLEM = ['Một lớp có $23$ người. Xác suất có ít nhất', 'hai người trùng ngày sinh?']
OPTIONS = ['approx "0,06"', 'approx "0,507"', 'approx "0,99"']
CORRECT = 1
ANSWER_VALUE = .507


def p_same(n):
    q = 1.0
    for i in range(n):
        q *= (365 - i) / 365
    return 1 - q


BEATS = [
    Beat('hook', 'hook', 'Lớp bạn có hai mươi ba người. Xác suất có ít nhất hai bạn trùng ngày sinh là bao nhiêu? '
                         'Một năm có ba trăm sáu mươi lăm ngày, hai mươi ba người thì chắc ít lắm nhỉ?'),
    Beat('guess', 'hook', 'Khoảng sáu phần trăm, khoảng năm mươi phần trăm, hay chín mươi chín phần trăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dùng biến cố đối: tất cả đều khác ngày sinh. Người thứ nhất tùy ý, người thứ hai còn ba trăm sáu mươi tư '
                        'ngày trong ba trăm sáu mươi lăm, người thứ ba còn ba trăm sáu mươi ba, cứ thế đến người thứ hai mươi ba.'),
    Beat('s2', 'solve', 'Nhân tất cả các phân số đó lại, xác suất mọi người khác ngày sinh chỉ còn khoảng không phẩy bốn chín ba. '
                        'Vậy xác suất có người trùng là khoảng không phẩy năm không bảy, hơn một nửa!'),
    Beat('s3', 'solve', 'Vì sao trực giác sai? Ta nghĩ đến một người cụ thể, nhưng thực ra có tới hai trăm năm mươi ba cặp người '
                        'có thể trùng nhau. Đường cong xác suất vượt một nửa đúng tại hai mươi ba người.'),
    Beat('answer', 'solve', 'Đáp án: khoảng năm mươi phần trăm. Hãy thử đếm ngày sinh trong lớp bạn, rồi bình luận kết quả nhé!'),
    Beat('outro', 'outro', outro_text(87)),
]

FORMULAS = formulas('approx "0,507"', OPTIONS,
                    prod='P(overline(A)) = 365/365 dot 364/365 dot dots dot 343/365 approx "0,493"',
                    prob='P(A) approx 1 - "0,493" = "0,507"',
                    pairs='C_23^2 = 253 " cặp"')


def validate() -> bool:
    assert round(p_same(23), 3) == .507 and p_same(22) < .5 < p_same(23)
    assert comb(23, 2) == 253
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS087(ShortScene):
    N = 87

    def curve(self):
        x0, x1, y0, y1 = -3.3, 3.0, -.3, 2.9
        X = lambda n: x0 + (x1 - x0) * n / 60  # noqa: E731
        Y = lambda p: y0 + (y1 - y0) * p  # noqa: E731
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], color=SOFT, stroke_width=3),
                      Line([x0, y0, 0], [x0, y1, 0], color=SOFT, stroke_width=3))
        pts = [[X(n), Y(p_same(n)), 0] for n in range(1, 61)]
        path = VMobject(stroke_color=CYAN, stroke_width=5)
        path.set_points_smoothly(pts)
        half = DashedLine([x0, Y(.5), 0], [x1, Y(.5), 0], color=SOFT, stroke_width=2)
        mark = DashedLine([X(23), y0, 0], [X(23), Y(.507), 0], color=GOLD, stroke_width=3)
        labs = VGroup(self.TM('$1$', 22, SOFT).next_to([x0, y1, 0], [-1, 0, 0], buff=.1),
                      self.TM('$"0,5"$', 22, SOFT).next_to([x0, Y(.5), 0], [-1, 0, 0], buff=.1),
                      self.TM('$23$', 24, GOLD, bold=True).next_to([X(23), y0, 0], [0, -1, 0], buff=.1),
                      self.TM('$60$', 22, SOFT).next_to([x1, y0, 0], [0, -1, 0], buff=.1),
                      tx('số người', 20, SOFT).next_to([X(42), y0, 0], [0, -1, 0], buff=.12))
        return axes, path, half, mark, labs

    def hook_visual(self, t0):
        self.board_top = -1.0

    def beat_s1(self, T):
        rows = VGroup(*[self.TM(f'người ${k}$: $({366 - k})/365$', 26, SOFT) for k in (2, 3)],
                      tx('…', 30, SOFT), self.TM('người $23$: $343/365$', 26, SOFT)).arrange([0, -1, 0], buff=.15)
        rows.move_to([0, 1.5, 0])
        for r in rows:
            self.play(FadeIn(r, shift=DOWN * .1), run_time=self.rt(.08))
            self.wait(self.rt(.05))
        self.rows = rows

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('prod', 1.2))
        self.wait_until(.55, t0)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.rows.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.rows)
        axes, path, half, mark, labs = self.curve()
        self.play(Create(axes), FadeIn(half), FadeIn(labs), run_time=self.rt(.06))
        self.play(Create(path), run_time=self.rt(.25))
        self.play(Create(mark), run_time=self.rt(.05))
        self.write_board(self.M('pairs', 1.9))
        self.wait_until(.7, t0)
        self.write_board(tx('nhiều cặp hơn bạn tưởng!', 28, CORAL, bold=True), anim='fade')

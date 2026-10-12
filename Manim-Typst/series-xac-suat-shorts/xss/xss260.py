"""XSS260 · Đồng xu lệch bao nhiêu? — 2p(1 − p) = 0,48 ⇒ p = 0,6 hoặc 0,4; p > 1/2 ⇒ p = 0,6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Create, FadeIn, VGroup, VMobject

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS260', 'answer': 'p = 0,6'}
PROBLEM = ['Đồng xu lệch, ra ngửa với xác suất',
           '$p > 1/2$. Tung $2$ lần, xác suất được',
           '$1$ ngửa $1$ sấp là $"0,48"$. Tìm $p$.']
OPTIONS = ['p = "0,4"', 'p = "0,6"', 'p = "0,76"']
CORRECT = 1
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Một đồng xu lệch, ra ngửa với xác suất p lớn hơn một phần hai. Tung hai lần, xác suất được một ngửa một sấp là không phẩy bốn tám. Tìm p.'),
    Beat('guess', 'hook', 'Không phẩy bốn, không phẩy sáu, hay không phẩy bảy sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Một ngửa một sấp có hai thứ tự: ngửa sấp và sấp ngửa, mỗi thứ tự xác suất p nhân một trừ p. Tổng hai p nhân một trừ p.'),
    Beat('s2', 'solve', 'Phương trình bậc hai: p nhân một trừ p bằng không phẩy hai bốn, tức p bình phương trừ p cộng không phẩy hai bốn bằng không. Hai nghiệm: không phẩy sáu và không phẩy bốn.'),
    Beat('s3', 'solve', 'Hai nghiệm đối xứng qua một phần hai, vì đổi vai ngửa và sấp không đổi kết quả. Điều kiện p lớn hơn một phần hai chọn p bằng không phẩy sáu.'),
    Beat('answer', 'solve', 'Đáp án: p bằng không phẩy sáu. Đọc kỹ điều kiện phụ của đề để loại nghiệm!'),
    Beat('outro', 'outro', outro_text(260)),
]

FORMULAS = formulas('p = "0,6"', OPTIONS,
                    eq='2 p (1 - p) = "0,48"',
                    sol='p^2 - p + "0,24" = 0 arrow.l.r.double p in {"0,4"; "0,6"}')


def validate() -> bool:
    roots = [F(k, 100) for k in range(101) if 2 * F(k, 100) * (1 - F(k, 100)) == F(48, 100)]
    assert roots == [F(2, 5), F(3, 5)]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS260(ShortScene):
    N = 260

    def hook_visual(self, t0):
        self.board_top = -1.3
        x0, x1, y0, y1 = -3.0, 3.0, -.2, 2.6
        pts = [[x0 + (x1 - x0) * k / 100, y0 + (y1 - y0) * 2 * (k / 100) * (1 - k / 100) / .5, 0] for k in range(101)]
        self.curve = VMobject(stroke_color=CYAN, stroke_width=5)
        self.curve.set_points_smoothly(pts)
        self.level = VMobject(stroke_color=GOLD, stroke_width=3)
        self.level.set_points_as_corners([[x0, y0 + (y1 - y0) * .48 / .5, 0], [x1, y0 + (y1 - y0) * .48 / .5, 0]])
        self.dots = VGroup(*[coin('N', .22).move_to([x0 + (x1 - x0) * p, y0 + (y1 - y0) * .48 / .5, 0]) for p in (.4, .6)])
        self.lab = VGroup(self.TM('$p$', 24, SOFT).move_to([x1 + .2, y0, 0]), self.TM('$"0,48"$', 22, GOLD).move_to([x0 - .3, y0 + (y1 - y0) * .96, 0]))
        self.wait_until(.6, t0)
        self.play(Create(self.curve), FadeIn(self.lab[0]), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('eq', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(Create(self.level), FadeIn(self.lab[1]), run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.dots), run_time=self.rt(.05))
        self.write_board(self.M('sol', 1.6))

    def beat_s3(self, T):
        self.play(self.dots[0].animate.set_opacity(.2), self.dots[1].animate.scale(1.5), run_time=self.rt(.06))
        self.play(self.dots[0][0].animate.set_stroke(CORAL, 4), run_time=self.rt(.03))

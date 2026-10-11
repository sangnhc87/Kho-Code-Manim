"""XSS062 · Biết có ít nhất một trai — loại GG, còn TT, TG, GT: 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL, SOFT, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS062', 'answer': '1/3'}
PROBLEM = ['Gia đình có $2$ con, biết có ít nhất một con trai.', 'Xác suất cả hai đều là trai?']
OPTIONS = ['1/2', '1/3', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 3
KIDS = [''.join(w) for w in product('TG', repeat=2)]
COLOR = {'T': CYAN, 'G': CORAL}

BEATS = [
    Beat('hook', 'hook', 'Thử thách hai mươi mốt có đáp án một phần tư. Bây giờ thêm một thông tin: gia đình hai con này '
                         'có ít nhất một con trai. Xác suất cả hai đều là trai thay đổi thành bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay vẫn một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn khả năng ban đầu: trai trai, trai gái, gái trai, gái gái, đồng khả năng. '
                        'Biết có ít nhất một trai, ta loại đúng một khả năng: gái gái.'),
    Beat('s2', 'solve', 'Không gian mẫu mới còn ba khả năng như nhau, trong đó chỉ có trai trai là thỏa. '
                        'Xác suất bằng một phần ba.'),
    Beat('s3', 'solve', 'Nhiều người đáp một phần hai vì nghĩ con còn lại là trai hay gái như nhau. '
                        'Nhưng ta không biết con nào là trai, nên "con còn lại" không xác định!'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Thử thách tiếp theo đổi thông tin một chút, và đáp án lại khác!'),
    Beat('outro', 'outro', outro_text(62)),
]

FORMULAS = formulas('1/3', OPTIONS, prob='P("TT" | "có trai") = 1/3')


def validate() -> bool:
    cond = [w for w in KIDS if 'T' in w]
    assert F(sum(w == 'TT' for w in cond), len(cond)) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


def family(w, r=.42):
    c = card(2.2, 1.35, STROKE, PANEL, radius=.2, stroke_width=3)
    kids = VGroup(*[token(ch, COLOR[ch], r) for ch in w]).arrange(buff=.25).move_to(c)
    return VGroup(c, kids)


class XSS062(ShortScene):
    N = 62

    def hook_visual(self, t0):
        self.fams = VGroup(*[family(w) for w in KIDS]).arrange_in_grid(2, 2, buff=(.4, .35)).move_to([0, 1.35, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.fams, lag_ratio=.25), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        gg = self.fams[3]
        self.play(gg.animate.set_opacity(.25), FadeIn(cross(CORAL, 1.0).move_to(gg)), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.fams[0][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.08))
        self.play(FadeIn(tx('1 trong 3 khả năng', 30, GOLD, bold=True).move_to([0, -.45, 0])), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(tx('"con còn lại" không xác định!', 28, SOFT, bold=True), anim='fade')

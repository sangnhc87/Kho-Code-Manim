"""XSS359 · Thang máy năm tầng — 4 người, 5 tầng: 5⁴ = 625; ra ở 4 tầng khác nhau: 5·4·3·2 = 120 → 24/125."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, FadeOut, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, PANEL, SOFT, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS359', 'answer': '24/125'}
PROBLEM = ['$4$ người vào thang máy, mỗi người ra ngẫu',
           'nhiên ở $1$ trong $5$ tầng. Xác suất $4$ người',
           'ra ở $4$ tầng khác nhau?']
OPTIONS = ['24/125', '1/5', '12/125']
CORRECT = 0
ANSWER_VALUE = 24 / 125

BEATS = [
    Beat('hook', 'hook', 'Bốn người cùng vào thang máy của tòa nhà năm tầng phía trên, mỗi người ra ngẫu nhiên ở một tầng. '
                         'Xác suất bốn người ra ở bốn tầng khác nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai mươi bốn phần một trăm hai mươi lăm, một phần năm, hay mười hai phần một trăm hai mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi người có năm lựa chọn độc lập: năm mũ bốn, sáu trăm hai mươi lăm cách.'),
    Beat('s2', 'solve', 'Bốn tầng khác nhau: người đầu năm cách, người sau bốn, rồi ba, rồi hai. Một trăm hai mươi cách.'),
    Beat('s3', 'solve', 'Xác suất một trăm hai mươi phần sáu trăm hai mươi lăm, rút gọn hai mươi bốn phần một trăm hai mươi lăm, khoảng mười chín phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi bốn phần một trăm hai mươi lăm. Chỉnh hợp chia cho lũy thừa: công thức chung của mọi bài khác nhau hết.'),
    Beat('outro', 'outro', outro_text(359)),
]

FORMULAS = formulas('24/125', OPTIONS,
                    all='5^4 = 625',
                    good='A_5^4 = 5 dot 4 dot 3 dot 2 = 120',
                    prob='P = 120/625 = 24/125')


def validate() -> bool:
    good = sum(len(set(t)) == 4 for t in product(range(5), repeat=4))
    assert good == 120 and F(good, 625) == F(24, 125)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS359(ShortScene):
    N = 359

    def put(self, floors, frac=.06):
        new = VGroup()
        for k, f in enumerate(floors):
            new.add(token(str(k + 1), CYAN, .22).move_to(self.fl[f].get_center() + [-.9 + .6 * sum(1 for j in floors[:k] if j == f), 0, 0]))
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.ppl = None
        self.fl = VGroup(*[Rectangle(width=3.6, height=.62, stroke_color=STROKE, stroke_width=3, fill_color=PANEL, fill_opacity=1)
                           for _ in range(5)]).arrange(DOWN, buff=0).move_to([.3, 1.0, 0])
        labs = VGroup(*[self.TM(f'$T_{5 - i}$', 24, SOFT).next_to(f, [-1, 0, 0], buff=.15) for i, f in enumerate(self.fl)])
        self.play(FadeIn(self.fl), FadeIn(labs), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        self.put([1, 3, 1, 4])

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.put([0, 2, 3, 4], .06)
        self.wait_until(.5, t0)
        self.write_board(self.M('good', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

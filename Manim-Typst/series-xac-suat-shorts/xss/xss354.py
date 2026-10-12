"""XSS354 · Ba ghế không kề trên bàn tròn — 10 ghế tròn; ghế 1 được chọn: C(6;2) = 15, không chọn: C(7;3) = 35 → 50/120 = 5/12."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import Circle, FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, PANEL_2, SOFT, STROKE  # noqa: E402
from common.visuals import polygon_pts, token  # noqa: E402

EPISODE = {'code': 'XSS354', 'answer': '5/12'}
PROBLEM = ['Chọn ngẫu nhiên $3$ trong $10$ ghế quanh',
           'bàn tròn. Xác suất không có $2$ ghế nào',
           'kề nhau?']
OPTIONS = ['5/12', '7/24', '1/2']
CORRECT = 0
ANSWER_VALUE = 5 / 12
SETS = list(combinations(range(10), 3))
GOOD = [s for s in SETS if all((b - a) % 10 not in (1, 9) for a, b in combinations(s, 2))]

BEATS = [
    Beat('hook', 'hook', 'Mười ghế quanh một bàn tròn. Chọn ngẫu nhiên ba ghế. Xác suất không có hai ghế nào kề nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần mười hai, bảy phần hai mươi tư, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có một trăm hai mươi cách chọn. Bàn tròn khó hơn dãy thẳng vì ghế mười kề ghế một. Ta chia theo ghế số một.'),
    Beat('s2', 'solve', 'Nếu chọn ghế một: hai ghế bên cạnh bị cấm, còn bảy ghế thẳng hàng từ ba đến chín, chọn hai ghế không kề: tổ hợp chập hai của sáu, mười lăm cách.'),
    Beat('s3', 'solve', 'Nếu không chọn ghế một: chín ghế thẳng hàng từ hai đến mười, chọn ba ghế không kề: tổ hợp chập ba của bảy, ba mươi lăm cách.'),
    Beat('s4', 'solve', 'Tổng năm mươi trên một trăm hai mươi, bằng năm phần mười hai.'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười hai. Cắt vòng tròn tại một điểm để biến về dãy thẳng.'),
    Beat('outro', 'outro', outro_text(354)),
]

FORMULAS = formulas('5/12', OPTIONS,
                    all='C_10^3 = 120',
                    with1='C_6^2 = 15',
                    without1='C_7^3 = 35',
                    prob='P = (15 + 35)/120 = 5/12')


def validate() -> bool:
    assert len(GOOD) == 50 and F(len(GOOD), len(SETS)) == F(5, 12)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS354(ShortScene):
    N = 354

    def pick(self, idx, frac=.06):
        new = VGroup(*[token('', CYAN, .26).move_to(self.pts[i]) for i in idx])
        self.play(*([FadeOut(self.sel)] if self.sel else []), FadeIn(new), run_time=self.rt(frac))
        self.sel = new

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.sel = None
        self.pts = polygon_pts(10, 1.85, (0, 1.0))
        table = Circle(radius=1.25, stroke_color=STROKE, stroke_width=4, fill_color=PANEL_2, fill_opacity=1).move_to([0, 1.0, 0])
        seats = VGroup(*[Circle(radius=.26, stroke_color=SOFT, stroke_width=3).move_to(p) for p in self.pts])
        nums = VGroup(*[self.TM(f'${i + 1}$', 20, SOFT).move_to(p) for i, p in enumerate(self.pts)])
        self.play(FadeIn(table), FadeIn(seats), FadeIn(nums), run_time=self.rt(.06))
        self.seatsg = seats
        self.wait_until(.5, t0)
        self.pick((0, 3, 9))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('all', 1.5))
        self.wait_until(.7, t0)
        self.play(self.seatsg[0].animate.set_stroke(GOLD, 6), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.pick((0, 3, 6), .05)
        self.wait_until(.6, t0)
        self.clear_board(.03)
        self.write_board(self.M('with1', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.pick((2, 5, 8), .05)
        self.wait_until(.6, t0)
        self.write_board(self.M('without1', 1.5))

    def beat_s4(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

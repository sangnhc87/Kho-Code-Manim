"""XSS180 · Chữ số tăng dần — mỗi bộ 3 chữ số khác 0 cho đúng 1 số tăng dần: C(9,3)/900 = 7/75."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS180', 'answer': '7/75'}
PROBLEM = ['Chọn ngẫu nhiên một số tự nhiên',
           'có $3$ chữ số. Xác suất các chữ số',
           'tăng dần từ trái sang phải?']
OPTIONS = ['1/6', '7/75', '2/15']
CORRECT = 1
ANSWER_VALUE = 7 / 75

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên một số có ba chữ số, từ một trăm đến chín trăm chín mươi chín. '
                         'Xác suất các chữ số tăng dần ngặt từ trái sang phải, như một hai năm hay ba bảy chín, là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, bảy phần bảy mươi lăm, hay hai phần mười lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Không gian mẫu có chín trăm số. Số tăng dần thì không thể có chữ số không, vì không không thể đứng đầu, '
                        'và cũng không thể đứng sau một chữ số lớn hơn.'),
    Beat('s2', 'solve', 'Mẹo then chốt: chọn ba chữ số khác nhau từ một đến chín, chỉ có đúng một cách xếp tăng dần. '
                        'Vậy số cách bằng tổ hợp chập ba của chín, tám mươi tư.'),
    Beat('s3', 'solve', 'Xác suất bằng tám mươi tư phần chín trăm, tức bảy phần bảy mươi lăm, khoảng chín phẩy ba phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần bảy mươi lăm. Thứ tự đã bị ép buộc thì đếm bằng tổ hợp, không phải chỉnh hợp!'),
    Beat('outro', 'outro', outro_text(180)),
]

FORMULAS = formulas('7/75', OPTIONS,
                    omega='n(Omega) = 900',
                    good='n(A) = C_9^3 = 84',
                    prob='P = 84/900 = 7/75')


def validate() -> bool:
    good = [n for n in range(100, 1000) if list(str(n)) == sorted(set(str(n)))]
    assert len(good) == 84 == comb(9, 3) and F(84, 900) == F(7, 75)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS180(ShortScene):
    N = 180

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.digits = VGroup(*[VGroup(card(.62, .72, SOFT, PANEL, radius=.1, stroke_width=2), self.MNum(d, 0, SOFT, 30))
                               for d in range(1, 10)]).arrange(buff=.12).move_to([0, 2.3, 0])
        for d in self.digits:
            d[1].move_to(d[0])
        self.slots = VGroup(*[card(1.0, 1.15, GOLD, PANEL, radius=.12, stroke_width=4) for _ in range(3)]) \
            .arrange(buff=.3).move_to([0, .8, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.slots, lag_ratio=.2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(self.M('omega', 2.2))
        self.wait_until(.45, t0)
        zero = tx('0', 36, CORAL, bold=True).next_to(self.slots, [-1, 0, 0], buff=.5)
        self.play(FadeIn(zero), run_time=self.rt(.04))
        self.play(zero.animate.set_opacity(.2), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.digits, lag_ratio=.05), run_time=self.rt(.1))
        picks = [self.digits[i] for i in (6, 1, 4)]
        self.play(*[p[0].animate.set_stroke(CYAN, 5) for p in picks], run_time=self.rt(.05))
        self.wait_until(.45, t0)
        sorted_picks = [self.digits[i] for i in (1, 4, 6)]
        self.play(*[p.copy().animate.move_to(s) for p, s in zip(sorted_picks, self.slots)], run_time=self.rt(.1))
        self.write_board(self.M('good', 2.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

"""XSS015 · Sinh nhật cuối tuần — 2 trong 7 ngày: 2/7 (bẫy tỉ số 2/5)."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PANEL, SOFT, STROKE, WHITE  # noqa: E402

EPISODE = {'code': 'XSS015', 'answer': '2/7'}
PROBLEM = ['Sinh nhật năm nay của bạn rơi vào thứ',
           'Bảy hoặc Chủ nhật với xác suất bao',
           'nhiêu?']
OPTIONS = ['1/7', '2/7', '2/5']
CORRECT = 1
ANSWER_VALUE = 2 / 7
DAYS = ('T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN')

BEATS = [
    Beat('hook', 'hook', 'Sinh nhật năm nay của bạn rơi vào cuối tuần, thứ bảy hoặc chủ nhật, với xác suất bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần bảy, hai phần bảy, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Một tuần có bảy ngày. Khi không có thông tin gì thêm, ta coi sinh nhật rơi vào mỗi thứ '
                        'trong tuần là đồng khả năng.'),
    Beat('s2', 'solve', 'Cuối tuần gồm thứ bảy và chủ nhật: hai kết quả thuận lợi trong bảy. Xác suất bằng hai phần bảy.'),
    Beat('s3', 'solve', 'Hai phần năm là cái bẫy: nó so hai ngày cuối tuần với năm ngày trong tuần, '
                        'tức là một tỉ số, không phải xác suất.'),
    Beat('answer', 'solve', 'Đáp án: hai phần bảy, khoảng hai mươi chín phần trăm. '
                            'Bình luận xem sinh nhật bạn năm nay rơi vào thứ mấy nhé!'),
    Beat('outro', 'outro', outro_text(15)),
]

FORMULAS = formulas('2/7', OPTIONS,
                    n='n(Omega) = 7',
                    prob='P = 2/7 approx "29" %',
                    ratio='2 : 5 quad coral(!=) quad P')


def validate() -> bool:
    assert Fraction(sum(d in ('T7', 'CN') for d in DAYS), len(DAYS)) == Fraction(2, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS015(ShortScene):
    N = 15

    def hook_visual(self, t0):
        self.days = VGroup()
        for d in DAYS:
            c = card(.92, 1.25, STROKE, PANEL, radius=.14, stroke_width=3)
            self.days.add(VGroup(c, tx(d, 30, WHITE, bold=True).move_to(c)))
        self.days.arrange(buff=.1).move_to([0, 1.4, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.days, lag_ratio=.15), run_time=self.rt(.3))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[d[0].animate.set_stroke(SOFT, 4) for d in self.days], run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        we = VGroup(self.days[5], self.days[6])
        self.play(we.animate.shift(UP * .3), *[d[0].animate.set_fill(GOLD, .45) for d in we],
                  VGroup(*self.days[:5]).animate.set_opacity(.35), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('ratio', 1.7), anim='fade')
        self.write_board(tx('tỉ số, không phải xác suất', 28, CORAL, bold=True), anim='fade')

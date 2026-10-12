"""XSS423 · Nghịch lý xe buýt — chu kỳ 10 + 20 = 30 phút; đến bến đều theo thời gian → rơi vào khoảng 20 phút với xác suất 20/30 = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS423', 'answer': '2/3'}
PROBLEM = ['Xe buýt cách nhau $10$ phút hoặc $20$ phút',
           '(xen kẽ). Bạn đến bến ngẫu nhiên. Xác',
           'suất rơi vào khoảng chờ $20$ phút?']
OPTIONS = ['2/3', '1/2', '1/3']
CORRECT = 0
ANSWER_VALUE = 2 / 3
U = .17  # screen units per minute

BEATS = [
    Beat('hook', 'hook', 'Xe buýt chạy xen kẽ: cách nhau mười phút rồi hai mươi phút, cứ thế lặp lại. Một nửa số khoảng là dài. '
                         'Bạn đến bến vào thời điểm ngẫu nhiên. Xác suất bạn rơi vào khoảng hai mươi phút?'),
    Beat('guess', 'hook', 'Hai phần ba, một phần hai, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Một nửa số khoảng là dài, nhưng bạn không chọn khoảng: bạn chọn một thời điểm. Khoảng dài chiếm nhiều thời gian hơn.'),
    Beat('s2', 'solve', 'Mỗi chu kỳ ba mươi phút có mười phút thuộc khoảng ngắn và hai mươi phút thuộc khoảng dài.'),
    Beat('s3', 'solve', 'Xác suất hai mươi phần ba mươi, tức hai phần ba. Thời gian chờ trung bình cũng dài hơn bạn tưởng.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Nghịch lý chờ xe: khoảng dài dễ bị bắt gặp hơn, nên ta luôn thấy mình kém may.'),
    Beat('outro', 'outro', outro_text(423)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    split='30 = 10 + 20',
                    prob='P = 20/30 = 2/3')


def validate() -> bool:
    assert F(20, 30) == F(2, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS423(ShortScene):
    N = 423

    def hook_visual(self, t0):
        self.board_top = -1.3
        x0, segs, t = -3.3, VGroup(), 0
        stops = VGroup()
        for k, d in enumerate((10, 20, 10)):
            a, b = [x0 + U * t, 1.2, 0], [x0 + U * (t + d), 1.2, 0]
            segs.add(Line(a, b, color=CYAN if d == 10 else GOLD, stroke_width=14))
            stops.add(token('B', SOFT, .2).move_to(a))
            t += d
        stops.add(token('B', SOFT, .2).move_to([x0 + U * t, 1.2, 0]))
        labs = VGroup(*[self.TM(f'${d}$', 28, SOFT).next_to(s, DOWN, buff=.25) for d, s in zip((10, 20, 10), segs)])
        self.timeline = VGroup(segs, stops, labs)
        self.wait_until(.4, t0)
        self.play(FadeIn(self.timeline, lag_ratio=.1), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.you = token('Bạn', CORAL, .28).move_to(self.timeline[0][1].get_center() + [0, .55, 0])
        self.play(FadeIn(self.you), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('split', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

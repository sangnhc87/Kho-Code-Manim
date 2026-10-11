"""XSS108 · Hẹn gặp trong một giờ — mỗi người chờ 15 phút: diện tích dải chéo 1 − (3/4)² = 7/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Dot, FadeIn, Polygon, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS108', 'answer': '7/16'}
PROBLEM = ['Hai bạn hẹn nhau, mỗi người đến ngẫu',
           'nhiên trong $1$ giờ và chờ $15$ phút.',
           'Xác suất hai bạn gặp nhau?']
OPTIONS = ['1/4', '7/16', '1/2']
CORRECT = 1
ANSWER_VALUE = 7 / 16

BEATS = [
    Beat('hook', 'hook', 'Hai bạn hẹn gặp nhau trong khoảng từ bảy giờ đến tám giờ. Mỗi người đến vào một thời điểm ngẫu nhiên, '
                         'và chỉ chờ mười lăm phút rồi đi. Xác suất hai bạn gặp được nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, bảy phần mười sáu, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi x, y là số phút sau bảy giờ mà mỗi người đến. Mỗi cặp x, y là một điểm trong hình vuông sáu mươi '
                        'nhân sáu mươi, mọi điểm đồng khả năng.'),
    Beat('s2', 'solve', 'Hai bạn gặp nhau khi hai thời điểm cách nhau không quá mười lăm phút. '
                        'Trên hình vuông, đó là một dải chéo dọc theo đường chéo chính.'),
    Beat('s3', 'solve', 'Phần ngoài dải là hai tam giác vuông, cạnh bốn mươi lăm. Ghép lại thành hình vuông cạnh bốn mươi lăm, '
                        'chiếm ba phần tư bình phương, tức chín phần mười sáu. Phần còn lại là bảy phần mười sáu.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần mười sáu, chưa tới một nửa. Hẹn nhau thì nên chờ lâu hơn mười lăm phút nhé!'),
    Beat('outro', 'outro', outro_text(108)),
]

FORMULAS = formulas('7/16', OPTIONS,
                    cond='abs(x - y) <= 15',
                    out='(45/60)^2 = 9/16',
                    prob='P = 1 - 9/16 = 7/16')


def validate() -> bool:
    assert 1 - F(45, 60) ** 2 == F(7, 16)
    grid = 600
    hit = sum(abs(i - j) <= 150 for i in range(grid) for j in range(grid))
    assert abs(hit / grid ** 2 - 7 / 16) < .003
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS108(ShortScene):
    N = 108

    def hook_visual(self, t0):
        self.board_top = -1.3
        side, cx, cy = 3.7, .2, 1.25
        x0, y0 = cx - side / 2, cy - side / 2
        P = lambda x, y: [x0 + side * x / 60, y0 + side * y / 60, 0]  # noqa: E731
        self.P = P
        self.sq = Square(side_length=side, stroke_color=SOFT, stroke_width=3).move_to([cx, cy, 0])
        self.labs = VGroup(self.TM('$x$', 26, SOFT).next_to(P(30, 0), [0, -1, 0], buff=.1),
                           self.TM('$y$', 26, SOFT).next_to(P(0, 30), [-1, 0, 0], buff=.1),
                           self.TM('$60$', 22, SOFT).next_to(P(60, 0), [0, -1, 0], buff=.1))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.sq), FadeIn(self.labs), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.play(FadeIn(Dot(self.P(12, 40), radius=.09, color=GOLD)), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        P = self.P
        band = Polygon(P(0, 0), P(15, 0), P(60, 45), P(60, 60), P(45, 60), P(0, 15), fill_color=GREEN, fill_opacity=.55,
                       stroke_width=0)
        self.play(FadeIn(band), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.write_board(self.M('cond', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        P = self.P
        tris = VGroup(Polygon(P(15, 0), P(60, 0), P(60, 45), fill_color=CORAL, fill_opacity=.5, stroke_width=0),
                      Polygon(P(0, 15), P(0, 60), P(45, 60), fill_color=CORAL, fill_opacity=.5, stroke_width=0))
        self.play(FadeIn(tris), run_time=self.rt(.08))
        self.clear_board(.03)
        self.write_board(self.M('out', 2.0))
        self.wait_until(.6, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)



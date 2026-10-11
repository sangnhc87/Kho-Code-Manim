"""XSS106 · Bẻ que thành tam giác — mỗi cách bẻ là một điểm trong hình vuông; vùng tạo tam giác có diện tích 1/4."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Dot, FadeIn, Line, Polygon, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS106', 'answer': '1/4'}
PROBLEM = ['Bẻ một que tại $2$ điểm chọn ngẫu',
           'nhiên. Xác suất $3$ đoạn ghép',
           'được thành tam giác?']
OPTIONS = ['1/2', '1/4', '1/3']
CORRECT = 1
ANSWER_VALUE = .25
N, SEED = 2000, 18


def trials():
    r, c, pts, out = random.Random(SEED), 0, [], []
    for k in range(1, N + 1):
        x, y = r.random(), r.random()
        a, b = sorted((x, y))
        ok = max(a, b - a, 1 - b) < .5
        c += ok
        pts.append((x, y, ok))
        out.append(c / k)
    return pts, out


BEATS = [
    Beat('hook', 'hook', 'Bẻ một chiếc que tại hai điểm chọn hoàn toàn ngẫu nhiên, được ba đoạn. '
                         'Xác suất ba đoạn này ghép lại được thành một tam giác là bao nhiêu? Đây là bài xác suất hình học kinh điển.'),
    Beat('guess', 'hook', 'Một phần hai, một phần tư, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba đoạn tạo thành tam giác khi đoạn dài nhất ngắn hơn tổng hai đoạn kia, '
                        'tức mỗi đoạn đều ngắn hơn một nửa chiếc que.'),
    Beat('s2', 'solve', 'Mẹo lớn: gọi hai điểm bẻ là x và y, mỗi số từ không đến một. Mỗi cách bẻ là một điểm trong hình vuông '
                        'đơn vị, và xác suất chính là diện tích.'),
    Beat('s3', 'solve', 'Điều kiện mỗi đoạn nhỏ hơn một nửa cắt ra hai tam giác nhỏ ở giữa hình vuông, '
                        'mỗi tam giác có diện tích một phần tám. Tổng diện tích một phần tư.'),
    Beat('s4', 'solve', 'Kiểm tra bằng mô phỏng: bẻ hai nghìn chiếc que, đánh dấu xanh những lần ghép được tam giác. '
                        'Các chấm xanh lấp đầy đúng hai tam giác, và tỉ lệ dừng lại ở một phần tư.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Biến xác suất thành diện tích là một trong những ý tưởng đẹp nhất của toán học!'),
    Beat('outro', 'outro', outro_text(106)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    cond='"mỗi đoạn" < 1/2',
                    area='S = 2 dot 1/8 = 1/4')


def validate() -> bool:
    _, out = trials()
    assert abs(out[-1] - .25) < .003 and F(2, 8) == F(1, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS106(ShortScene):
    N = 106

    def hook_visual(self, t0):
        self.board_top = -1.35
        stick = Line([-3, 1.8, 0], [3, 1.8, 0], color='#C08A4A', stroke_width=14)
        cuts = VGroup(Line([-1.3, 1.55, 0], [-1.3, 2.05, 0], color=CORAL, stroke_width=6),
                      Line([1.0, 1.55, 0], [1.0, 2.05, 0], color=CORAL, stroke_width=6))
        self.stick = VGroup(stick, cuts)
        self.wait_until(.35, t0)
        self.play(FadeIn(stick), run_time=self.rt(.08))
        self.play(FadeIn(cuts, lag_ratio=.5), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('cond', 2.3))

    def square(self):
        side, cx, cy = 3.6, .2, 1.2
        x0, y0 = cx - side / 2, cy - side / 2
        P = lambda x, y: [x0 + side * x, y0 + side * y, 0]  # noqa: E731
        sq = Square(side_length=side, stroke_color=SOFT, stroke_width=3).move_to([cx, cy, 0])
        labs = VGroup(self.TM('$x$', 26, SOFT).next_to(P(.5, 0), [0, -1, 0], buff=.1),
                      self.TM('$y$', 26, SOFT).next_to(P(0, .5), [-1, 0, 0], buff=.1))
        tri = VGroup(Polygon(P(0, .5), P(.5, .5), P(.5, 1), fill_color=GREEN, fill_opacity=.55, stroke_width=0),
                     Polygon(P(.5, 0), P(.5, .5), P(1, .5), fill_color=GREEN, fill_opacity=.55, stroke_width=0))
        return sq, labs, tri, P

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.stick.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.stick)
        self.sq, labs, self.tri, self.P = self.square()
        self.play(FadeIn(self.sq), FadeIn(labs), run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.play(FadeIn(Dot(self.P(.28, .67), radius=.09, color=GOLD)), run_time=self.rt(.05))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(FadeIn(self.tri, lag_ratio=.5), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        m = self.M('area', 2.3)
        self.write_board(m)
        self.frame(m)

    def beat_s4(self, T):
        self.clear_board(.03)
        pts, out = trials()
        dots = VGroup(*[Dot(self.P(x, y), radius=.025, color=GREEN if ok else CORAL) for x, y, ok in pts[:900]])
        self.play(FadeIn(dots, lag_ratio=.002), run_time=self.rt(.35))
        self.run_sim(out, 'số lần bẻ:', 'tạo tam giác:', .35, y=-1.9)



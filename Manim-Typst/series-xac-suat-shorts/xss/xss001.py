"""XSS001 · Ngẫu nhiên là gì? — một lần tung không đoán được, 1000 lần tung thì có quy luật."""
from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, Create, DashedLine, FadeIn, FadeOut, Line, ValueTracker, VGroup, VMobject, \
    always_redraw, smooth

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT, WHITE  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS001', 'answer': '1/2'}
PROBLEM = ['Tung một đồng xu cân đối.', 'Xác suất ra mặt ngửa bằng bao nhiêu?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5
FLIPS = 1000
SEED = 2026

BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu. Sấp hay ngửa? Không ai đoán chắc được, và đó chính là ngẫu nhiên. '
                         'Vậy xác suất ra mặt ngửa bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Chọn nhanh nào! Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi lần tung chỉ có hai kết quả: sấp hoặc ngửa. Tập hai kết quả này gọi là không gian mẫu. '
                        'Đồng xu cân đối nên hai kết quả có khả năng xảy ra như nhau.'),
    Beat('s2', 'solve', 'Mặt ngửa là một trong hai kết quả đồng khả năng. Xác suất bằng số kết quả thuận lợi chia cho '
                        'số kết quả có thể, tức là một phần hai.'),
    Beat('s3', 'solve', 'Không tin? Ta tung thử một nghìn lần. Lúc đầu tỉ lệ mặt ngửa nhảy lung tung, '
                        'nhưng càng tung nhiều, tỉ lệ càng bám sát một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Từng lần tung là ngẫu nhiên, nhưng lặp lại thật nhiều lần thì '
                            'xuất hiện quy luật. Đó là ý nghĩa của xác suất.'),
    Beat('outro', 'outro', outro_text(1)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    omega='Omega = {S; space N}',
                    rule='P(A) = (n(A))/(n(Omega))',
                    pN='P(N) = 1/2',
                    half='1/2')


def heads_frequency():
    rnd = random.Random(SEED)
    heads, out = 0, []
    for k in range(1, FLIPS + 1):
        heads += rnd.random() < .5
        out.append(heads / k)
    return out


def validate() -> bool:
    omega = ['S', 'N']
    assert Fraction(sum(w == 'N' for w in omega), len(omega)) == Fraction(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    assert abs(heads_frequency()[-1] - .5) < .04  # the simulation really ends near 1/2
    return True


class XSS001(ShortScene):
    N = 1

    def hook_visual(self, t0):
        self.c = coin('N', 1.55).move_to([0, 1.2, 0])
        self.play(FadeIn(self.c, scale=.6), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.c = self.flip(self.c, 'SNSSNSN', self.rt(.55))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.c), run_time=self.rt(.04))
        pair = VGroup(*[VGroup(coin(f, 1.1), tx(name, 30, SOFT)).arrange(DOWN, buff=.2)
                        for f, name in (('S', 'sấp'), ('N', 'ngửa'))]).arrange(RIGHT, buff=1.4).move_to([0, 1.3, 0])
        self.play(FadeIn(pair[0], shift=RIGHT * .3), FadeIn(pair[1], shift=LEFT * .3), run_time=self.rt(.1))
        self.pair = pair
        self.wait_until(.35, t0)
        self.write_board(self.M('omega', 2.3))
        self.wait_until(.7, t0)
        self.write_board(tx('hai kết quả đồng khả năng', 32, CYAN), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.pair[1].animate.scale(1.15), self.pair[0].animate.set_opacity(.35), run_time=self.rt(.08))
        self.clear_board()
        self.write_board(self.M('rule', 2.1))
        self.wait_until(.6, t0)
        m = self.M('pN', 2.5)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.clear_board(.03)
        self.play(FadeOut(self.pair), run_time=self.rt(.03))
        x0, x1, y0, y1 = -3.4, 3.0, -.2, 2.95
        X = lambda k: x0 + (x1 - x0) * k / FLIPS  # noqa: E731
        Y = lambda f: y0 + (y1 - y0) * f  # noqa: E731
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], color=SOFT, stroke_width=3),
                      Line([x0, y0, 0], [x0, y1, 0], color=SOFT, stroke_width=3))
        half = DashedLine([x0, Y(.5), 0], [x1, Y(.5), 0], color=GOLD, stroke_width=3)
        lab = VGroup(self.M('half', 1.3).next_to([x1, Y(.5), 0], UP, buff=.08).shift(LEFT * .3),
                     self.TM('$1$', 26, SOFT).next_to([x0, y1, 0], LEFT, buff=.1),
                     self.TM('$0$', 26, SOFT).next_to([x0, y0, 0], LEFT, buff=.1),
                     self.TM('$1000$', 26, SOFT).next_to([x1, y0, 0], DOWN, buff=.1),
                     tx('số lần tung', 24, SOFT).next_to([X(500), y0, 0], DOWN, buff=.12))
        self.play(Create(axes), Create(half), FadeIn(lab), run_time=self.rt(.07))
        freq = heads_frequency()
        pts = [[X(k + 1), Y(f), 0] for k, f in enumerate(freq)]
        n = ValueTracker(2)

        def curve():
            k = max(2, int(n.get_value()))
            m = VMobject(stroke_color=CYAN, stroke_width=4)
            m.set_points_as_corners(pts[:k])
            return m

        path = always_redraw(curve)
        read = always_redraw(lambda: VGroup(
            VGroup(tx('lần tung:', 32, SOFT), self.MNum(int(n.get_value()), 0, WHITE, 36)).arrange(RIGHT, buff=.2),
            VGroup(tx('tỉ lệ ngửa:', 32, SOFT), self.MNum(freq[max(2, int(n.get_value())) - 1], 3, GREEN, 36))
            .arrange(RIGHT, buff=.2)).arrange(DOWN, aligned_edge=LEFT, buff=.22).move_to([-.3, -2.3, 0]))
        self.add(path, read)
        self.play(n.animate.set_value(FLIPS), run_time=self.rt(.72), rate_func=smooth)
        path.clear_updaters()
        read.clear_updaters()
        self.play(half.animate.set_stroke(width=6), run_time=self.rt(.05))


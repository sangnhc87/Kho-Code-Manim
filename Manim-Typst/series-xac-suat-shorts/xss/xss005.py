"""XSS005 · Bẫy của d'Alembert — "1 sấp 1 ngửa" có xác suất 1/2, không phải 1/3."""
from __future__ import annotations

import random
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import DOWN, RIGHT, UP, FadeIn, ValueTracker, VGroup, always_redraw, smooth

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, PANEL, SOFT, STROKE, WHITE  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS005', 'answer': '1/2 (không phải 1/3)'}
PROBLEM = ['Tung hai đồng xu.', 'Xác suất được một sấp, một ngửa?']
OPTIONS = ['1/3', '1/2', '1/4']
CORRECT = 1
ANSWER_VALUE = .5
TRIALS = 400
SEED = 5


def mixed_frequency():
    rnd = random.Random(SEED)
    hit, out = 0, []
    for k in range(1, TRIALS + 1):
        hit += (rnd.random() < .5) != (rnd.random() < .5)
        out.append(hit / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Tung hai đồng xu. Xác suất được một sấp, một ngửa là bao nhiêu? Lý luận nhanh: '
                         'có ba khả năng, hai sấp, hai ngửa, hoặc một sấp một ngửa, nên đáp án là một phần ba. Đúng không?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lý luận một phần ba sai ở chỗ: ba khả năng đó không có cùng cơ hội xảy ra. '
                        'Ngay cả nhà toán học Pháp Đa-lăm-be cũng từng mắc kiểu sai lầm này.'),
    Beat('s2', 'solve', 'Nhớ lại thử thách trước: hai đồng xu cho bốn kết quả đồng khả năng. '
                        'Một sấp một ngửa chiếm hai trong bốn kết quả: sấp ngửa và ngửa sấp.'),
    Beat('s3', 'solve', 'Vậy xác suất bằng hai phần tư, tức là một phần hai. Kiểm tra bằng thí nghiệm: '
                        'tung hai đồng xu bốn trăm lần, tỉ lệ một sấp một ngửa bám sát một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai, không phải một phần ba. Bài học: chỉ đếm khi các kết quả đồng khả năng!'),
    Beat('outro', 'outro', outro_text(5)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    wrong='1/3 quad coral(times)',
                    prob='P = 2/4 = 1/2')


def validate() -> bool:
    space = list(product('SN', repeat=2))
    assert Fraction(sum(set(w) == {'S', 'N'} for w in space), len(space)) == Fraction(1, 2)
    assert abs(mixed_frequency()[-1] - .5) < .06
    assert OPTIONS[CORRECT] == '1/2'
    return True


class XSS005(ShortScene):
    N = 5

    def hook_visual(self, t0):
        boxes = VGroup()
        for label in ('2 sấp', '2 ngửa', '1 sấp 1 ngửa'):
            c = card(2.2, 1.0, STROKE, PANEL)
            boxes.add(VGroup(c, tx(label, 26, WHITE, bold=True, max_w=2.0).move_to(c)))
        boxes.arrange(RIGHT, buff=.2).move_to([0, 1.6, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(boxes, lag_ratio=.4), run_time=self.rt(.2))
        self.wait_until(.75, t0)
        w = self.M('wrong', 2.0).next_to(boxes, DOWN, buff=.4)
        self.play(FadeIn(w), run_time=self.rt(.05))
        self.boxes, self.wrong = boxes, w

    def beat_s1(self, T):
        t0 = self.now()
        x = cross(CORAL, 1.0).move_to(self.wrong)
        self.play(FadeIn(x, scale=1.5), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.play(FadeIn(tx('không đồng khả năng!', 34, CORAL, bold=True).move_to([-.25, -.9, 0]), shift=UP * .1),
                  run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        pairs = VGroup()
        for a, b in product('SN', repeat=2):
            pair = VGroup(coin(a, .5), coin(b, .5)).arrange(RIGHT, buff=.12)
            pairs.add(VGroup(card(1.6, 1.25, STROKE, PANEL), pair))
            pairs[-1][1].move_to(pairs[-1][0])
        pairs.arrange_in_grid(2, 2, buff=.3).move_to([0, 1.5, 0])
        self.play(FadeIn(pairs, lag_ratio=.25), run_time=self.rt(.15))
        self.pairs = pairs
        self.wait_until(.55, t0)
        self.play(*[pairs[i][0].animate.set_stroke(GOLD, 6) for i in (1, 2)],
                  *[pairs[i].animate.set_opacity(.35) for i in (0, 3)], run_time=self.rt(.08))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.45, t0)
        self.clear_board(.03)
        freq = mixed_frequency()
        n = ValueTracker(1)
        read = always_redraw(lambda: VGroup(
            VGroup(tx('số lần tung:', 30, SOFT), self.MNum(int(n.get_value()), 0, WHITE, 34)).arrange(RIGHT, buff=.2),
            VGroup(tx('tỉ lệ 1 sấp 1 ngửa:', 30, SOFT), self.MNum(freq[int(n.get_value()) - 1], 3, GREEN, 34))
            .arrange(RIGHT, buff=.2)).arrange(DOWN, aligned_edge=RIGHT, buff=.22).move_to([-.25, -1.6, 0]))
        self.add(read)
        self.play(n.animate.set_value(TRIALS), run_time=self.rt(.4), rate_func=smooth)
        read.clear_updaters()


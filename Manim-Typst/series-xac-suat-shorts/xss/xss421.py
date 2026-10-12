"""XSS421 · Bốn điểm trên nửa đường tròn — biến cố E_i: 3 điểm kia nằm trong nửa vòng theo chiều kim đồng hồ từ điểm i; xung khắc, mỗi cái (1/2)³ → 4/8 = 1/2."""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from manim import Arc, Circle, Dot, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, STROKE  # noqa: E402

EPISODE = {'code': 'XSS421', 'answer': '1/2'}
PROBLEM = ['Chọn ngẫu nhiên $4$ điểm trên đường tròn.',
           'Xác suất cả $4$ điểm cùng nằm trên một',
           'nửa đường tròn?']
OPTIONS = ['1/2', '1/4', '1/8']
CORRECT = 0
ANSWER_VALUE = .5
C0 = (0, 1.0)


def simulate(runs=40000, seed=421):
    rnd, ok = random.Random(seed), 0
    for _ in range(runs):
        a = sorted(rnd.random() for _ in range(4))
        gaps = [a[i + 1] - a[i] for i in range(3)] + [1 - a[3] + a[0]]
        ok += max(gaps) >= .5
    return ok / runs


BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên bốn điểm trên một đường tròn. Xác suất cả bốn điểm cùng nằm trên một nửa đường tròn nào đó là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần tư, hay một phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Với mỗi điểm i, xét biến cố: ba điểm còn lại đều nằm trong nửa vòng tròn đi theo chiều kim đồng hồ bắt đầu từ i. Xác suất một phần hai mũ ba.'),
    Beat('s2', 'solve', 'Bốn điểm cùng nằm trên một nửa vòng khi và chỉ khi đúng một trong bốn biến cố đó xảy ra: điểm đầu tiên của cụm. Các biến cố xung khắc.'),
    Beat('s3', 'solve', 'Cộng lại: bốn nhân một phần tám bằng một phần hai. Mô phỏng bốn mươi nghìn lần cũng cho khoảng một nửa.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Tổng quát, n điểm cho n chia hai mũ n trừ một.'),
    Beat('outro', 'outro', outro_text(421)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    ei='P(E_i) = (1/2)^3 = 1/8',
                    prob='P = 4 dot 1/8 = 1/2')


def validate() -> bool:
    assert abs(simulate() - .5) < .01
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS421(ShortScene):
    N = 421

    def hook_visual(self, t0):
        self.board_top = -1.4
        c = [C0[0], C0[1], 0]
        self.circ = Circle(radius=1.8, color=STROKE, stroke_width=4).move_to(c)
        angs = [.3, 1.1, 1.9, 2.6]
        self.pts = VGroup(*[Dot([c[0] + 1.8 * math.cos(a), c[1] + 1.8 * math.sin(a), 0], radius=.12, color=CYAN) for a in angs])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.circ), FadeIn(self.pts, lag_ratio=.2), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        half = Arc(radius=1.8, start_angle=.3, angle=math.pi, arc_center=[C0[0], C0[1], 0], color=GOLD, stroke_width=10)
        self.wait_until(.3, t0)
        self.play(self.pts[0].animate.set_color(CORAL).scale(1.4), FadeIn(half), run_time=self.rt(.08))
        self.write_board(self.M('ei', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.pts[1:].animate.scale(1.25), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

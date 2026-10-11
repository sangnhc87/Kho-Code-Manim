"""XSS115 · Tam giác nhọn trên đường tròn — nhọn ⇔ chứa tâm; 3 đường kính ngẫu nhiên, 8 cách chọn đầu mút, 2 cách chứa tâm: 1/4."""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from manim import Circle, Dot, FadeIn, Line, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT, STROKE, WHITE  # noqa: E402

EPISODE = {'code': 'XSS115', 'answer': '1/4'}
PROBLEM = ['Chọn ngẫu nhiên $3$ điểm trên một',
           'đường tròn. Xác suất tam giác tạo',
           'thành là tam giác nhọn?']
OPTIONS = ['1/2', '1/4', '1/3']
CORRECT = 1
ANSWER_VALUE = .25
N, SEED = 2000, 3
ANG = (100, 25, 230)  # three diameters for the picture (degrees)


def trials():
    r, c, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        t = sorted(r.random() for _ in range(3))
        c += max(t[1] - t[0], t[2] - t[1], 1 - t[2] + t[0]) < .5
        out.append(c / k)
    return out


def contains_centre(angles):
    a = sorted(x % 360 for x in angles)
    gaps = (a[1] - a[0], a[2] - a[1], 360 - a[2] + a[0])
    return max(gaps) < 180


BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba điểm trên một đường tròn rồi nối lại. Xác suất được một tam giác nhọn là bao nhiêu? '
                         'Lời giải dưới đây là một trong những chứng minh đẹp nhất của xác suất hình học.'),
    Beat('guess', 'hook', 'Một phần hai, một phần tư, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tam giác nội tiếp là tam giác nhọn khi và chỉ khi nó chứa tâm đường tròn. '
                        'Nếu tâm nằm ngoài, một góc sẽ chắn cung lớn hơn nửa đường tròn và trở thành góc tù.'),
    Beat('s2', 'solve', 'Mẹo: thay vì chọn ba điểm, chọn ba đường kính ngẫu nhiên, rồi với mỗi đường kính chọn một trong hai đầu mút. '
                        'Có hai mũ ba bằng tám cách chọn, đồng khả năng.'),
    Beat('s3', 'solve', 'Trong tám tam giác đó, đúng hai tam giác chứa tâm: một tam giác và tam giác đối xứng của nó qua tâm. '
                        'Xác suất bằng hai phần tám, tức một phần tư.'),
    Beat('s4', 'solve', 'Mô phỏng hai nghìn lần chọn ba điểm ngẫu nhiên: tỉ lệ tam giác nhọn bám sát một phần tư.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Ba phần tư số tam giác nội tiếp ngẫu nhiên là tam giác tù, ngược hẳn với hình dung thường gặp!'),
    Beat('outro', 'outro', outro_text(115)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    cond='"nhọn" arrow.l.r.double "chứa tâm"',
                    eight='2^3 = 8 " cách", quad 2 " cách chứa tâm"',
                    prob='P = 2/8 = 1/4')


def validate() -> bool:
    picks = [[a + 180 * s for a, s in zip(ANG, signs)] for signs in ((i >> 2 & 1, i >> 1 & 1, i & 1) for i in range(8))]
    assert sum(contains_centre(p) for p in picks) == 2
    assert abs(trials()[-1] - .25) < .003
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS115(ShortScene):
    N = 115

    def P(self, deg):
        return [self.c[0] + self.r * math.cos(math.radians(deg)), self.c[1] + self.r * math.sin(math.radians(deg)), 0]

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.c, self.r = (0, 1.25), 2.0
        self.circle = Circle(radius=self.r, stroke_color=SOFT, stroke_width=4).move_to([*self.c, 0])
        self.centre = Dot([*self.c, 0], radius=.08, color=WHITE)
        tri = Polygon(self.P(80), self.P(150), self.P(300), stroke_color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=.2)
        self.tri = tri
        self.wait_until(.45, t0)
        self.play(FadeIn(self.circle), FadeIn(self.centre), FadeIn(tri), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        obtuse = Polygon(self.P(80), self.P(120), self.P(200), stroke_color=CORAL, stroke_width=5, fill_color=CORAL,
                         fill_opacity=.2)
        self.play(self.tri.animate.set_opacity(0), FadeIn(obtuse), run_time=self.rt(.08))
        self.obtuse = obtuse
        self.write_board(self.M('cond', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.obtuse.animate.set_opacity(0), run_time=self.rt(.03))
        diams = VGroup(*[Line(self.P(a), self.P(a + 180), color=STROKE, stroke_width=3) for a in ANG])
        ends = VGroup(*[Dot(self.P(a + s), radius=.1, color=CYAN) for a in ANG for s in (0, 180)])
        self.play(FadeIn(diams, lag_ratio=.3), FadeIn(ends), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.write_board(self.M('eight', 1.7))

    def beat_s3(self, T):
        t0 = self.now()
        good = [s for s in ((i >> 2 & 1, i >> 1 & 1, i & 1) for i in range(8))
                if contains_centre([a + 180 * b for a, b in zip(ANG, s)])]
        tris = VGroup(*[Polygon(*[self.P(a + 180 * b) for a, b in zip(ANG, s)], stroke_color=GREEN, stroke_width=5,
                                fill_color=GREEN, fill_opacity=.2) for s in good])
        self.play(FadeIn(tris[0]), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(FadeIn(tris[1]), run_time=self.rt(.08))
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

    def beat_s4(self, T):
        self.clear_board(.03)
        self.run_sim(trials(), 'số lần chọn:', 'tam giác nhọn:', .6, y=-1.7)



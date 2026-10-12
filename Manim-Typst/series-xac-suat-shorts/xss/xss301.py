"""XSS301 · Tránh điểm (1; 1) — 8 đường không qua (1;1); trong đó qua (2;2): 4 → 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Cross, Dot, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss._gridkit import Lattice  # noqa: E402
from xss.xss300 import PATHS, visits  # noqa: E402

EPISODE = {'code': 'XSS301', 'answer': '1/2'}
PROBLEM = ['Chọn ngẫu nhiên một đường ngắn nhất từ',
           '$(0; 0)$ tới $(3; 3)$, biết đường đó không',
           'qua $(1; 1)$. Xác suất đường đi qua',
           '$(2; 2)$?']
OPTIONS = ['3/5', '1/2', '1/4']
CORRECT = 1
ANSWER_VALUE = .5
AVOID = [w for w in PATHS if not visits(w, (1, 1))]

BEATS = [
    Beat('hook', 'hook', 'Vẫn lưới ba nhân ba, hai mươi đường đi ngắn nhất. Biết đường được chọn không đi qua điểm một một. '
                         'Xác suất nó đi qua điểm hai hai là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần năm, một phần hai, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện: bỏ mười hai đường qua một một, còn tám đường. Chúng đi men theo hai mép: bắt đầu bằng hai bước phải, hoặc hai bước lên.'),
    Beat('s2', 'solve', 'Trong tám đường đó, đi qua hai hai: từ hai không lên hai hai, hoặc từ không hai sang hai hai, rồi tiếp tới ba ba: bốn đường.'),
    Beat('s3', 'solve', 'Xác suất bốn phần tám, tức một phần hai. Không có điều kiện thì xác suất qua hai hai là ba phần năm: điều kiện kéo nó xuống.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Điều kiện trên đường đi: xóa các đường vi phạm, đếm lại!'),
    Beat('outro', 'outro', outro_text(301)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    nb='n(B) = 20 - 12 = 8',
                    prob='P(A | B) = 4/8 = 1/2')


def validate() -> bool:
    assert len(AVOID) == 8 and F(sum(visits(w, (2, 2)) for w in AVOID), 8) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS301(ShortScene):
    N = 301

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.L = Lattice(3, 3, origin=(-1.5, -.3), step=1.0)
        self.g = self.L.grid()
        self.bad = Cross(Dot(self.L.P(1, 1), radius=.2), stroke_color=CORAL, stroke_width=6)
        self.goal = Dot(self.L.P(2, 2), radius=.14, color=GOLD)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.g), FadeIn(self.bad), FadeIn(self.goal), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.ps = VGroup(*[self.L.path(w, CYAN, 4) for w in AVOID])
        self.play(FadeIn(self.ps, lag_ratio=.1), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.write_board(self.M('nb', 2.1))

    def beat_s2(self, T):
        good = [p for p, w in zip(self.ps, AVOID) if visits(w, (2, 2))]
        other = [p for p, w in zip(self.ps, AVOID) if not visits(w, (2, 2))]
        self.play(*[p.animate.set_stroke(GOLD, 6) for p in good], *[p.animate.set_opacity(.2) for p in other], run_time=self.rt(.08))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

"""XSS303 · Quân vua trên bàn 3 × 3 — góc → ô cạnh (chắc chắn) → tâm (1/3): 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS303', 'answer': '1/3'}
PROBLEM = ['Quân cờ ở góc bàn $3 times 3$, mỗi bước',
           'sang một ô kề cạnh ngẫu nhiên. Xác suất',
           'sau $2$ bước quân cờ ở ô trung tâm?']
OPTIONS = ['1/4', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3


def nb(c):
    i, j = c
    return [(a, b) for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)) if 0 <= a < 3 and 0 <= b < 3]


def dist(steps):
    d = {(0, 0): F(1)}
    for _ in range(steps):
        nx = {}
        for c, p in d.items():
            for n in nb(c):
                nx[n] = nx.get(n, 0) + p / len(nb(c))
        d = nx
    return d


BEATS = [
    Beat('hook', 'hook', 'Một quân cờ đứng ở góc bàn cờ ba nhân ba. Mỗi bước, nó di chuyển sang một ô kề cạnh, chọn ngẫu nhiên. '
                         'Sau hai bước, xác suất quân cờ ở ô trung tâm là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bước một: từ góc chỉ có hai ô kề, đều là ô cạnh. Dù đi đâu, quân cờ chắc chắn đến một ô cạnh.'),
    Beat('s2', 'solve', 'Bước hai: ô cạnh có ba ô kề: hai ô góc và ô trung tâm. Xác suất vào tâm là một phần ba.'),
    Beat('s3', 'solve', 'Vậy đáp án là một phần ba. Lưu ý số ô kề khác nhau ở góc, cạnh, tâm: hai, ba, bốn. Xác suất mỗi nhánh phụ thuộc vị trí hiện tại.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Đi ngẫu nhiên trên bàn cờ: xác suất mỗi bước bằng một chia số ô kề!'),
    Beat('outro', 'outro', outro_text(303)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    prob='P = 1 dot 1/3 = 1/3')


def validate() -> bool:
    assert dist(2)[(1, 1)] == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS303(ShortScene):
    N = 303

    def hook_visual(self, t0):
        self.board_top = -1.25
        s = 1.1
        self.cells = {(i, j): Square(side_length=s, stroke_color=STROKE, stroke_width=3, fill_color=PANEL, fill_opacity=1)
                      .move_to([(j - 1) * s, 1.5 - (i - 1) * s, 0]) for i in range(3) for j in range(3)}
        self.board = VGroup(*self.cells.values())
        self.piece = token('V', GOLD, .35).move_to(self.cells[(0, 0)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.board), FadeIn(self.piece, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[self.cells[c].animate.set_fill(CYAN, .5) for c in ((0, 1), (1, 0))], run_time=self.rt(.05))
        self.wait_until(.55, t0)
        self.play(self.piece.animate.move_to(self.cells[(0, 1)]), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[self.cells[c].animate.set_fill(CYAN, .15) for c in ((0, 1), (1, 0))], run_time=self.rt(.02))
        self.play(*[self.cells[c].animate.set_fill(GOLD if c == (1, 1) else CORAL, .55) for c in ((0, 0), (0, 2), (1, 1))],
                  run_time=self.rt(.06))
        self.wait_until(.5, t0)

    def beat_s3(self, T):
        m = self.M('prob', 2.4)
        self.write_board(m)
        self.frame(m)

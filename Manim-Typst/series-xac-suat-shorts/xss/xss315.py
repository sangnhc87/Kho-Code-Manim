"""XSS315 · Điểm dưới đường chéo — (x; y) đều trong [0;1]², biết x + y < 1 (diện tích 1/2); phần x < 2y có diện tích 1/2 − 1/6 = 1/3 → 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, LEFT, FadeIn, Line, Polygon, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS315', 'answer': '2/3'}
PROBLEM = ['Chọn ngẫu nhiên $x, y$ trong $[0; 1]$.',
           'Biết $x + y < 1$. Xác suất $x < 2y$?']
OPTIONS = ['1/2', '2/3', '3/4']
CORRECT = 1
ANSWER_VALUE = 2 / 3
S, O = 3.4, (-1.7, -1.25)


def P(x, y):
    return [O[0] + S * x, O[1] + S * y, 0]


BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên hai số x và y trong đoạn từ không đến một. Biết tổng x cộng y nhỏ hơn một. '
                         'Xác suất x nhỏ hơn hai lần y là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi cặp x, y là một điểm trong hình vuông đơn vị. Điều kiện x cộng y nhỏ hơn một là tam giác dưới đường chéo, diện tích một phần hai.'),
    Beat('s2', 'solve', 'Đường y bằng x chia hai cắt cạnh huyền tại điểm hai phần ba, một phần ba. Phần bị loại là tam giác nhỏ có đáy một, cao một phần ba, diện tích một phần sáu.'),
    Beat('s3', 'solve', 'Phần thuận lợi có diện tích một phần hai trừ một phần sáu, bằng một phần ba. Chia cho diện tích điều kiện một phần hai, được hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Xác suất có điều kiện trong hình học là tỉ số diện tích bên trong vùng điều kiện.'),
    Beat('outro', 'outro', outro_text(315)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    cond='S_"đk" = 1/2',
                    bad='S_"loại" = 1/2 dot 1 dot 1/3 = 1/6',
                    prob='P = (1/2 - 1/6)/(1/2) = 2/3')


def validate() -> bool:
    good = F(1, 2) - F(1, 2) * F(1, 3)
    assert good / F(1, 2) == F(2, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS315(ShortScene):
    N = 315

    def hook_visual(self, t0):
        self.board_top = -1.75
        sq = Square(S, stroke_color=STROKE, stroke_width=4).move_to(P(.5, .5))
        labs = VGroup(self.TM('$x$', 30, SOFT).next_to(P(1, 0), DOWN, buff=.12), self.TM('$y$', 30, SOFT).next_to(P(0, 1), LEFT, buff=.12),
                      self.TM('$1$', 26, SOFT).next_to(P(1, 0), LEFT + DOWN, buff=.05).shift(DOWN * .05))
        self.sq = VGroup(sq, labs)
        self.play(FadeIn(self.sq), run_time=self.rt(.06))
        self.cond = Polygon(P(0, 0), P(1, 0), P(0, 1), stroke_color=CYAN, stroke_width=4, fill_color=CYAN, fill_opacity=.3)
        self.wait_until(.5, t0)
        self.play(FadeIn(self.cond), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.line = Line(P(0, 0), P(1, .5), color=GOLD, stroke_width=5)
        self.play(FadeIn(self.line), run_time=self.rt(.06))
        self.bad = Polygon(P(0, 0), P(1, 0), P(2 / 3, 1 / 3), stroke_width=0, fill_color=CORAL, fill_opacity=.7)
        self.wait_until(.4, t0)
        self.play(FadeIn(self.bad), run_time=self.rt(.06))
        self.write_board(self.M('bad', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        good = Polygon(P(0, 0), P(2 / 3, 1 / 3), P(0, 1), stroke_width=0, fill_color=GREEN, fill_opacity=.7)
        self.play(FadeIn(good), run_time=self.rt(.06))
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

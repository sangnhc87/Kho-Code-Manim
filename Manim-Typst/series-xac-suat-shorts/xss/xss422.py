"""XSS422 · Que gãy làm đôi — điểm bẻ x đều trên [0;1]; đoạn dài ≥ 2 lần đoạn ngắn ⇔ đoạn ngắn ≤ 1/3 ⇔ x ∈ [0; 1/3] ∪ [2/3; 1] → 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, UP, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS422', 'answer': '2/3'}
PROBLEM = ['Bẻ que tại một điểm ngẫu nhiên. Xác suất',
           'đoạn dài gấp ít nhất $2$ lần đoạn ngắn?']
OPTIONS = ['2/3', '1/3', '1/2']
CORRECT = 0
ANSWER_VALUE = 2 / 3
L0, L1, Y = -3.0, 3.0, 1.2


def X(t):
    return [L0 + (L1 - L0) * t, Y, 0]


BEATS = [
    Beat('hook', 'hook', 'Bẻ một que tại một điểm ngẫu nhiên thành hai đoạn. Xác suất đoạn dài dài gấp ít nhất hai lần đoạn ngắn là bao nhiêu? '
                         'Trực giác thường đoán thấp hơn nhiều.'),
    Beat('guess', 'hook', 'Hai phần ba, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi đoạn ngắn là s. Đoạn dài bằng một trừ s. Điều kiện một trừ s lớn hơn hoặc bằng hai s tương đương s nhỏ hơn hoặc bằng một phần ba.'),
    Beat('s2', 'solve', 'Đoạn ngắn không quá một phần ba khi điểm bẻ nằm trong một phần ba đầu hoặc một phần ba cuối của que.'),
    Beat('s3', 'solve', 'Hai đoạn đó dài tổng cộng hai phần ba. Xác suất hai phần ba: hai lần trong ba lần, một mảnh dài gấp đôi mảnh kia trở lên.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Bẻ ngẫu nhiên hiếm khi cho hai nửa gần bằng nhau.'),
    Beat('outro', 'outro', outro_text(422)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    cond='1 - s >= 2s <=> s <= 1/3',
                    prob='P = 1/3 + 1/3 = 2/3')


def validate() -> bool:
    assert F(1, 3) + F(1, 3) == F(2, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS422(ShortScene):
    N = 422

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.stick = Line(X(0), X(1), color=STROKE, stroke_width=14)
        ticks = VGroup(*[self.TM(f'${s}$', 28, SOFT).next_to(X(v), DOWN, buff=.3) for s, v in (('0', 0), ('1/3', 1 / 3), ('2/3', 2 / 3), ('1', 1))])
        self.ticks = ticks
        self.wait_until(.4, t0)
        self.play(FadeIn(self.stick), run_time=self.rt(.05))
        cut = Line(X(.8) + UP * .4, X(.8) + DOWN * .4, color=CORAL, stroke_width=6)
        self.play(FadeIn(cut), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.ticks), run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.play(FadeIn(Line(X(0), X(1 / 3), color=GREEN, stroke_width=20)), FadeIn(Line(X(2 / 3), X(1), color=GREEN, stroke_width=20)),
                  run_time=self.rt(.08))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

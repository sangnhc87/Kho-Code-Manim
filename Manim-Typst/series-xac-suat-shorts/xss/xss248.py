"""XSS248 · Lần ngược hai bước chọn — P(n = 1 | m = 1) = (1/4)/(25/48) = 12/25."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS248', 'answer': '12/25'}
PROBLEM = ['Chọn ngẫu nhiên $n$ từ $1$ đến $4$,',
           'rồi chọn $m$ từ $1$ đến $n$. Biết',
           '$m = 1$. Xác suất $n = 1$?']
OPTIONS = ['1/4', '12/25', '1/2']
CORRECT = 1
ANSWER_VALUE = 12 / 25
POST = [F(1, n) / F(25, 12) for n in range(1, 5)]

BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: chọn n từ một đến bốn, rồi m từ một đến n. Bạn chỉ thấy m bằng một. '
                         'Xác suất n cũng bằng một là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, mười hai phần hai mươi lăm, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh n bằng một có xác suất một phần tư nhân một, bằng một phần tư. Tổng các nhánh có m bằng một là hai mươi lăm phần bốn mươi tám.'),
    Beat('s2', 'solve', 'Bayes: một phần tư chia hai mươi lăm phần bốn mươi tám, bằng mười hai phần hai mươi lăm, gần một nửa.'),
    Beat('s3', 'solve', 'Hậu nghiệm tỉ lệ với một phần n: mười hai, sáu, bốn, ba phần hai mươi lăm. Số nhỏ được ưu tiên vì nó dễ sinh ra m bằng một.'),
    Beat('answer', 'solve', 'Đáp án: mười hai phần hai mươi lăm. Quan sát kết quả nhỏ là bằng chứng cho phạm vi nhỏ!'),
    Beat('outro', 'outro', outro_text(248)),
]

FORMULAS = formulas('12/25', OPTIONS,
                    bayes='P(n = 1 | m = 1) = (1/4)/(25/48) = 12/25',
                    post='12/25, quad 6/25, quad 4/25, quad 3/25')


def validate() -> bool:
    assert POST == [F(12, 25), F(6, 25), F(4, 25), F(3, 25)] and sum(POST) == 1
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS248(ShortScene):
    N = 248

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.1, 2.8
        self.bars = VGroup()
        for k, v in enumerate(POST):
            r = Rectangle(width=.9, height=h * float(v / POST[0]), stroke_width=0, fill_color=CORAL if k == 0 else CYAN,
                          fill_opacity=.85)
            r.move_to([-2.25 + 1.5 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'$n = {k + 1}$', 22, SOFT).next_to([-2.25 + 1.5 * k, base, 0], DOWN, buff=.08)
                             for k in range(4)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))

    def beat_s2(self, T):
        m = self.M('bayes', 1.8)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        self.clear_board(.03)
        self.write_board(self.M('post', 2.0))

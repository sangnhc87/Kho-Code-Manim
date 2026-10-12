"""XSS419 · Hai hộp diêm — mỗi hộp 2 que; khi phát hiện một hộp rỗng mà hộp kia cũng rỗng ⇔ 4 lần lấy đầu chia đều 2–2: C(4;2)/2⁴ = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

from manim import FadeIn, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS419', 'answer': '3/8'}
PROBLEM = ['Mỗi túi áo có $1$ hộp diêm $2$ que, mỗi lần',
           'lấy que ở túi ngẫu nhiên. Khi thấy một',
           'hộp rỗng: $P("hộp kia cũng rỗng")$?']
OPTIONS = ['3/8', '1/4', '1/2']
CORRECT = 0
ANSWER_VALUE = 3 / 8


@lru_cache(None)
def both_empty(a, b):
    out = F(0)
    for take_a in (True, False):
        mine, other = (a, b) if take_a else (b, a)
        if mine == 0:
            out += F(1, 2) * (other == 0)
        else:
            out += F(1, 2) * (both_empty(a - 1, b) if take_a else both_empty(a, b - 1))
    return out


BEATS = [
    Beat('hook', 'hook', 'Một người có hai hộp diêm ở hai túi áo, mỗi hộp hai que. Mỗi lần cần diêm, anh ta thò tay vào một túi ngẫu nhiên. Đến lúc lần đầu thấy một hộp rỗng. '
                         'Xác suất hộp kia cũng đã rỗng?'),
    Beat('guess', 'hook', 'Ba phần tám, một phần tư, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hộp kia cũng rỗng nghĩa là bốn lần lấy đầu tiên đã dùng hết cả bốn que, mỗi túi đúng hai lần. Lần thứ năm mới phát hiện hộp rỗng.'),
    Beat('s2', 'solve', 'Nếu một túi được chọn ba lần trong bốn lần đầu, lần thứ ba đó đã phát hiện rỗng khi túi kia còn que.'),
    Beat('s3', 'solve', 'Xác suất bốn lần chia đều hai hai: tổ hợp chập hai của bốn trên hai mũ bốn, bằng sáu phần mười sáu, tức ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Đây là bài toán hộp diêm Banach thu nhỏ.'),
    Beat('outro', 'outro', outro_text(419)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    prob='P = (C_4^2)/2^4 = 6/16 = 3/8')


def validate() -> bool:
    assert both_empty(2, 2) == F(3, 8)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS419(ShortScene):
    N = 419

    def hook_visual(self, t0):
        self.board_top = -1.3
        boxes = VGroup()
        for x in (-1.5, 1.5):
            box = Rectangle(width=1.6, height=1.0, stroke_color=SOFT, stroke_width=4).move_to([x, 1.3, 0])
            sticks = VGroup(*[Rectangle(width=.1, height=.7, stroke_width=0, fill_color=GOLD, fill_opacity=1).move_to([x + dx, 1.3, 0])
                              for dx in (-.25, .25)])
            boxes.add(VGroup(box, sticks))
        self.boxes = boxes
        self.wait_until(.45, t0)
        self.play(FadeIn(boxes), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[b[1].animate.set_opacity(.15) for b in self.boxes], run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.boxes[0][0].animate.set_stroke(CORAL, 6), run_time=self.rt(.05))

    def beat_s3(self, T):
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS060 · Hai mặt sát nhau — |a − b| ≤ 1: dải 6 + 10 ô quanh đường chéo → 16/36 = 4/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS060', 'answer': '4/9'}
PROBLEM = ['Gieo hai con xúc xắc. Xác suất hai số',
           'chấm hơn kém nhau không quá $1$?']
OPTIONS = ['1/6', '4/9', '1/3']
CORRECT = 1
ANSWER_VALUE = 4 / 9

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc. Xác suất hai số chấm bằng nhau hoặc hơn kém nhau đúng một là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, bốn phần chín, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trên bảng sáu nhân sáu, hai số bằng nhau là đường chéo chính: sáu ô.'),
    Beat('s2', 'solve', 'Hơn kém nhau đúng một là hai đường chéo nằm sát hai bên, mỗi đường năm ô: mười ô. '
                        'Tổng cộng mười sáu ô tạo thành một dải chéo.'),
    Beat('s3', 'solve', 'Xác suất bằng mười sáu phần ba mươi sáu, rút gọn còn bốn phần chín, gần một nửa. '
                        'Bảng sáu nhân sáu biến bài toán thành bài đếm ô.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần chín. Bài hai xúc xắc nào cũng có thể giải bằng cách tô màu bảng!'),
    Beat('outro', 'outro', outro_text(60)),
]

FORMULAS = formulas('4/9', OPTIONS, count='6 + 5 + 5 = 16', prob='P = 16/36 = 4/9')


def validate() -> bool:
    space = list(product(range(1, 7), repeat=2))
    assert F(sum(abs(a - b) <= 1 for a, b in space), 36) == F(4, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS060(DiceGridMixin, ShortScene):
    N = 60

    def hook_visual(self, t0):
        self.d1 = die(3, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(4, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.04))
        self.remove(self.d1, self.d2)
        self.show_grid(.3)
        self.wait_until(.6, t0)
        self.play(*[self.g.cells[i][i].animate.set_fill(GOLD, .7) for i in range(6)], run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        side = [self.g.cells[j][i] for i in range(6) for j in range(6) if abs(i - j) == 1]
        self.play(*[c.animate.set_fill(CYAN, .55) for c in side], run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.write_board(self.M('count', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('tô màu bảng 6 × 6', 28, GOLD, bold=True), anim='fade')

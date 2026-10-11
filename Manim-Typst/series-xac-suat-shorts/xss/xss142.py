"""XSS142 · Đảo điều kiện — biết tổng ≥ 10 (6 ô), 5 ô có mặt 6: 5/6 ≠ 5/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS142', 'answer': '5/6'}
PROBLEM = ['Gieo $2$ xúc xắc, biết tổng số chấm $>= 10$.', 'Xác suất có ít nhất một mặt $6$?']
OPTIONS = ['5/11', '5/6', '11/36']
CORRECT = 1
ANSWER_VALUE = 5 / 6
TWO = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Thử thách trước: biết có mặt sáu, xác suất tổng từ mười trở lên là năm phần mười một. '
                         'Giờ đảo lại: biết tổng từ mười trở lên, xác suất có mặt sáu là bao nhiêu? Có bằng năm phần mười một không?'),
    Beat('guess', 'hook', 'Năm phần mười một, năm phần sáu, hay mười một phần ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện mới là tổng từ mười trở lên: chỉ còn sáu ô: bốn sáu, năm năm, sáu bốn, năm sáu, sáu năm, sáu sáu.'),
    Beat('s2', 'solve', 'Trong sáu ô này, chỉ năm năm là không có mặt sáu. Còn lại năm ô có mặt sáu.'),
    Beat('s3', 'solve', 'Xác suất bằng năm phần sáu, khác xa năm phần mười một. Tử số giống nhau là năm, '
                        'nhưng mẫu số là biến cố điều kiện, nên đổi điều kiện là đổi cả mẫu.'),
    Beat('answer', 'solve', 'Đáp án: năm phần sáu. Ghi nhớ: P của A khi biết B thường khác P của B khi biết A!'),
    Beat('outro', 'outro', outro_text(142)),
]

FORMULAS = formulas('5/6', OPTIONS,
                    na='n(A) = 6',
                    prob='P(B | A) = 5/6 eq.not P(A | B) = 5/11')


def validate() -> bool:
    a = [w for w in TWO if sum(w) >= 10]
    assert len(a) == 6 and F(sum(6 in w for w in a), 6) == F(5, 6)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS142(DiceGridMixin, ShortScene):
    N = 142

    def hook_visual(self, t0):
        self.wait_until(.5, t0)
        self.show_grid(.2, sums=True)

    def beat_s1(self, T):
        t0 = self.now()
        cells = self.g.cells
        a = [cells[i][j] for i in range(6) for j in range(6) if i + j + 2 >= 10]
        rest = [cells[i][j] for i in range(6) for j in range(6) if i + j + 2 < 10]
        self.wait_until(.3, t0)
        self.play(*[c.animate.set_opacity(.12) for c in rest], *[c.animate.set_fill(CYAN, .5) for c in a],
                  run_time=self.rt(.1))
        self.write_board(self.M('na', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        cells = self.g.cells
        six = [cells[i][j] for i in range(6) for j in range(6) if i + j + 2 >= 10 and (i == 5 or j == 5)]
        self.play(*[c.animate.set_fill(GOLD, .8) for c in six], cells[4][4].animate.set_fill(CORAL, .6),
                  run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(tx('5 trong 6 ô có mặt 6', 30, GOLD, bold=True), anim='fade')

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)

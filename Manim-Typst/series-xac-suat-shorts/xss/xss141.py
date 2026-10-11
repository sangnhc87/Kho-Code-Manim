"""XSS141 · Biết có mặt 6 — thu hẹp không gian mẫu còn 11 ô, trong đó 5 ô có tổng ≥ 10: 5/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS141', 'answer': '5/11'}
PROBLEM = ['Gieo $2$ xúc xắc, biết có ít nhất một mặt',
           '$6$. Xác suất tổng số chấm $>= 10$?']
OPTIONS = ['1/6', '5/11', '5/6']
CORRECT = 1
ANSWER_VALUE = 5 / 11
TWO = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc, bạn được báo: có ít nhất một mặt sáu. '
                         'Biết điều đó, xác suất tổng số chấm từ mười trở lên là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, năm phần mười một, hay năm phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xác suất có điều kiện là thu hẹp không gian mẫu. Trong ba mươi sáu ô, chỉ giữ những ô có ít nhất một mặt sáu: '
                        'hàng sáu và cột sáu, mười một ô.'),
    Beat('s2', 'solve', 'Trong mười một ô đó, ô có tổng từ mười trở lên là: bốn sáu, sáu bốn, năm sáu, sáu năm, sáu sáu, tất cả năm ô.'),
    Beat('s3', 'solve', 'Xác suất bằng năm phần mười một. So với khi chưa biết gì là sáu phần ba mươi sáu: thông tin có mặt sáu làm xác suất tăng gần gấp ba.'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười một. Thử thách tiếp: đảo điều kiện lại thì sao?'),
    Beat('outro', 'outro', outro_text(141)),
]

FORMULAS = formulas('5/11', OPTIONS,
                    nb='n(B) = 6 + 6 - 1 = 11',
                    nab='n(A sect B) = 5',
                    prob='P(A | B) = (n(A sect B))/(n(B)) = 5/11')


def validate() -> bool:
    b = [w for w in TWO if 6 in w]
    assert len(b) == 11 and F(sum(sum(w) >= 10 for w in b), len(b)) == F(5, 11)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS141(DiceGridMixin, ShortScene):
    N = 141

    def hook_visual(self, t0):
        self.wait_until(.45, t0)
        self.show_grid(.2, sums=True)

    def beat_s1(self, T):
        t0 = self.now()
        cells = self.g.cells
        b = [cells[i][j] for i in range(6) for j in range(6) if i == 5 or j == 5]
        rest = [cells[i][j] for i in range(6) for j in range(6) if not (i == 5 or j == 5)]
        self.wait_until(.35, t0)
        self.play(*[c.animate.set_opacity(.12) for c in rest], *[c.animate.set_fill(CYAN, .45) for c in b],
                  run_time=self.rt(.1))
        self.write_board(self.M('nb', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        cells = self.g.cells
        a = [cells[i][j] for i in range(6) for j in range(6) if (i == 5 or j == 5) and i + j + 2 >= 10]
        self.play(*[c.animate.set_fill(GOLD, .8) for c in a], run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('nab', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)



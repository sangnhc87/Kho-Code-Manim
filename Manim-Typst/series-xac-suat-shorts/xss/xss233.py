"""XSS233 · Hai điều kiện cùng lúc — tổng chẵn VÀ có mặt 6: 5 ô; trong đó tổng ≥ 10: 3 ô → 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS233', 'answer': '3/5'}
PROBLEM = ['Gieo $2$ xúc xắc, biết tổng là số',
           'chẵn và có ít nhất một mặt $6$. Xác',
           'suất tổng số chấm $>= 10$?']
OPTIONS = ['1/2', '3/5', '2/3']
CORRECT = 1
ANSWER_VALUE = .6
TWO = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo hai xúc xắc. Bạn được biết hai điều: tổng là số chẵn, và có ít nhất một mặt sáu. '
                         'Xác suất tổng từ mười trở lên là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần năm, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai điều kiện cùng lúc nghĩa là lấy giao: ô vừa có mặt sáu, vừa có tổng chẵn. '
                        'Có mặt sáu là hàng sáu và cột sáu; tổng chẵn thì số còn lại phải chẵn.'),
    Beat('s2', 'solve', 'Còn đúng năm ô: hai sáu, sáu hai, bốn sáu, sáu bốn, sáu sáu. Trong đó tổng từ mười trở lên: bốn sáu, sáu bốn, sáu sáu.'),
    Beat('s3', 'solve', 'Xác suất ba phần năm. Mỗi điều kiện thêm vào lại thu hẹp không gian mẫu thêm một lần.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Đa điều kiện: tìm giao của các điều kiện trước, rồi mới đếm!'),
    Beat('outro', 'outro', outro_text(233)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    nb='n(B_1 sect B_2) = 5',
                    prob='P(A | B_1 sect B_2) = 3/5')


def validate() -> bool:
    b = [w for w in TWO if sum(w) % 2 == 0 and 6 in w]
    assert len(b) == 5 and F(sum(sum(w) >= 10 for w in b), 5) == F(3, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS233(DiceGridMixin, ShortScene):
    N = 233

    def hook_visual(self, t0):
        self.wait_until(.55, t0)
        self.show_grid(.2, sums=True)

    def beat_s1(self, T):
        t0 = self.now()
        c = self.g.cells
        six = [c[i][j] for i in range(6) for j in range(6) if i == 5 or j == 5]
        rest = [c[i][j] for i in range(6) for j in range(6) if not (i == 5 or j == 5)]
        self.play(*[x.animate.set_opacity(.12) for x in rest], run_time=self.rt(.06))
        self.wait_until(.5, t0)
        odd = [c[i][j] for i in range(6) for j in range(6) if (i == 5 or j == 5) and (i + j) % 2 == 1]
        self.play(*[x.animate.set_opacity(.12) for x in odd], run_time=self.rt(.06))
        self.play(*[x.animate.set_fill(CYAN, .5) for x in six if x not in odd], run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        c = self.g.cells
        good = [c[i][j] for i in range(6) for j in range(6) if (i == 5 or j == 5) and (i + j) % 2 == 0 and i + j + 2 >= 10]
        self.write_board(self.M('nb', 2.1))
        self.wait_until(.5, t0)
        self.play(*[x.animate.set_fill(GOLD, .85) for x in good], run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

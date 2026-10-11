"""XSS154 · Biết tổng chẵn — 18 ô tổng chẵn, chỉ 1 ô (6; 6): 1/18."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS154', 'answer': '1/18'}
PROBLEM = ['Gieo $2$ xúc xắc, biết tổng số chấm là số',
           'chẵn. Xác suất cả hai mặt đều là $6$?']
OPTIONS = ['1/36', '1/18', '1/9']
CORRECT = 1
ANSWER_VALUE = 1 / 18
TWO = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc, biết tổng số chấm là số chẵn. Xác suất cả hai mặt đều là sáu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba mươi sáu, một phần mười tám, hay một phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tổng chẵn khi hai số cùng chẵn hoặc cùng lẻ: chín ô cộng chín ô, mười tám ô, đúng một nửa bảng, xếp như bàn cờ.'),
    Beat('s2', 'solve', 'Ô sáu sáu có tổng mười hai, là số chẵn, nên vẫn nằm trong mười tám ô. Nó là ô thuận lợi duy nhất.'),
    Beat('s3', 'solve', 'Xác suất bằng một phần mười tám: điều kiện loại một nửa bảng nên xác suất tăng gấp đôi. '
                        'Công thức: một phần ba mươi sáu chia một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười tám. Nếu biến cố nằm trọn trong điều kiện, chỉ cần chia cho xác suất của điều kiện!'),
    Beat('outro', 'outro', outro_text(154)),
]

FORMULAS = formulas('1/18', OPTIONS,
                    nb='n(B) = 9 + 9 = 18',
                    prob='P(A | B) = (1/36)/(1/2) = 1/18')


def validate() -> bool:
    b = [w for w in TWO if sum(w) % 2 == 0]
    assert len(b) == 18 and F(sum(w == (6, 6) for w in b), 18) == F(1, 18)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS154(DiceGridMixin, ShortScene):
    N = 154

    def hook_visual(self, t0):
        self.wait_until(.5, t0)
        self.show_grid(.2, sums=True)

    def beat_s1(self, T):
        t0 = self.now()
        odd = [self.g.cells[i][j] for i in range(6) for j in range(6) if (i + j) % 2 == 1]
        even = [self.g.cells[i][j] for i in range(6) for j in range(6) if (i + j) % 2 == 0]
        self.wait_until(.3, t0)
        self.play(*[c.animate.set_opacity(.12) for c in odd], *[c.animate.set_fill(CYAN, .4) for c in even],
                  run_time=self.rt(.08))
        self.write_board(self.M('nb', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(self.g.cells[5][5].animate.set_fill(GOLD, .9).scale(1.2), run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

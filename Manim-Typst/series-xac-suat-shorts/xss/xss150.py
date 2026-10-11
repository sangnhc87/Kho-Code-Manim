"""XSS150 · Biết tích chẵn — 27 ô tích chẵn; tổng chẵn khi cả hai chẵn: 9/27 = 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS150', 'answer': '1/3'}
PROBLEM = ['Gieo $2$ xúc xắc, biết tích hai số',
           'chấm là số chẵn. Xác suất tổng',
           'hai số chấm là số chẵn?']
OPTIONS = ['1/2', '1/3', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 3
TWO = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc, bạn được biết tích hai số chấm là số chẵn. Xác suất tổng hai số chấm cũng chẵn là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tích chẵn khi có ít nhất một số chẵn. Bỏ các ô lẻ nhân lẻ, chín ô, còn hai mươi bảy ô.'),
    Beat('s2', 'solve', 'Tổng chẵn khi hai số cùng chẵn hoặc cùng lẻ. Nhưng cùng lẻ đã bị loại, nên chỉ còn cùng chẵn: chín ô.'),
    Beat('s3', 'solve', 'Xác suất bằng chín phần hai mươi bảy, tức một phần ba, khác hẳn một phần hai lúc chưa biết gì. '
                        'Biết tích chẵn đã ngầm loại đi một nửa khả năng tổng chẵn.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Hãy để ý điều kiện loại những ô nào, đôi khi nó loại đúng phần ta cần!'),
    Beat('outro', 'outro', outro_text(150)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    nb='n(B) = 36 - 9 = 27',
                    nab='n(A sect B) = 3 dot 3 = 9',
                    prob='P(A | B) = 9/27 = 1/3')


def validate() -> bool:
    b = [w for w in TWO if w[0] * w[1] % 2 == 0]
    assert len(b) == 27 and F(sum(sum(w) % 2 == 0 for w in b), 27) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS150(DiceGridMixin, ShortScene):
    N = 150

    def hook_visual(self, t0):
        self.wait_until(.5, t0)
        self.show_grid(.2, sums=False)

    def beat_s1(self, T):
        t0 = self.now()
        odd = [self.g.cells[i][j] for i in range(6) for j in range(6) if i % 2 == 0 and j % 2 == 0]
        self.wait_until(.3, t0)
        self.play(*[c.animate.set_opacity(.12) for c in odd], run_time=self.rt(.08))
        self.write_board(self.M('nb', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        even = [self.g.cells[i][j] for i in range(6) for j in range(6) if i % 2 == 1 and j % 2 == 1]
        self.wait_until(.45, t0)
        self.play(*[c.animate.set_fill(GOLD, .8) for c in even], run_time=self.rt(.08))
        self.write_board(self.M('nab', 2.1))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('chẵn + chẵn là cách duy nhất', 26, CYAN), anim='fade')

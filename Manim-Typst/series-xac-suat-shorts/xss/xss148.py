"""XSS148 · Hai mặt khác nhau — bỏ 6 ô đường chéo còn 30 ô, 6 ô tổng 7: 6/30 = 1/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402

EPISODE = {'code': 'XSS148', 'answer': '1/5'}
PROBLEM = ['Gieo $2$ xúc xắc, biết hai mặt khác nhau.', 'Xác suất tổng số chấm bằng $7$?']
OPTIONS = ['1/6', '1/5', '5/36']
CORRECT = 1
ANSWER_VALUE = .2
TWO = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc, bạn được báo hai mặt khác nhau. Xác suất tổng số chấm bằng bảy là bao nhiêu? '
                         'Chưa biết gì thì là một phần sáu.'),
    Beat('guess', 'hook', 'Một phần sáu, một phần năm, hay năm phần ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai mặt khác nhau: bỏ sáu ô trên đường chéo, từ một một đến sáu sáu. Còn lại ba mươi ô.'),
    Beat('s2', 'solve', 'Các ô tổng bảy nằm trên đường chéo phụ, sáu ô, và không ô nào có hai mặt bằng nhau. Cả sáu ô đều được giữ lại.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần ba mươi, tức một phần năm. Điều kiện loại bỏ các ô không thuận lợi nên xác suất tăng.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Điều kiện càng loại nhiều ô không thuận lợi, xác suất càng tăng!'),
    Beat('outro', 'outro', outro_text(148)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    nb='n(B) = 36 - 6 = 30',
                    prob='P(A | B) = 6/30 = 1/5')


def validate() -> bool:
    b = [w for w in TWO if w[0] != w[1]]
    assert F(sum(sum(w) == 7 for w in b), len(b)) == F(1, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS148(DiceGridMixin, ShortScene):
    N = 148

    def hook_visual(self, t0):
        self.wait_until(.5, t0)
        self.show_grid(.2, sums=True)

    def beat_s1(self, T):
        t0 = self.now()
        diag = [self.g.cells[i][i] for i in range(6)]
        self.wait_until(.3, t0)
        self.play(*[c.animate.set_opacity(.12) for c in diag], run_time=self.rt(.08))
        self.write_board(self.M('nb', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        seven = [self.g.cells[i][j] for i in range(6) for j in range(6) if i + j == 5]
        self.wait_until(.25, t0)
        self.play(*[c.animate.set_fill(GOLD, .8) for c in seven], run_time=self.rt(.08))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)



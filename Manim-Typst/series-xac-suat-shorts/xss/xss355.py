"""XSS355 · A trước B trước C — thứ tự tương đối của A, B, C có 3! = 6 khả năng như nhau → 1/6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS355', 'answer': '1/6'}
PROBLEM = ['$5$ học sinh A, B, C, D, E xếp hàng ngẫu',
           'nhiên. Xác suất A đứng trước B và B',
           'đứng trước C?']
OPTIONS = ['1/6', '1/3', '1/10']
CORRECT = 0
ANSWER_VALUE = 1 / 6
COL = {'A': CYAN, 'B': CORAL, 'C': GOLD, 'D': SOFT, 'E': SOFT}

BEATS = [
    Beat('hook', 'hook', 'Năm bạn A, B, C, D, E xếp thành một hàng ngẫu nhiên. Xác suất A đứng trước B, và B đứng trước C là bao nhiêu? '
                         'Không cần đứng sát nhau.'),
    Beat('guess', 'hook', 'Một phần sáu, một phần ba, hay một phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bỏ qua D và E. Chỉ nhìn ba bạn A, B, C: thứ tự tương đối của họ có ba giai thừa, sáu khả năng.'),
    Beat('s2', 'solve', 'Do đối xứng, sáu thứ tự này đồng khả năng. Đúng một thứ tự là A, rồi B, rồi C.'),
    Beat('s3', 'solve', 'Xác suất một phần sáu. Kiểm tra bằng đếm: chọn ba vị trí cho A, B, C là mười cách, xếp D, E hai cách, được hai mươi trên một trăm hai mươi.'),
    Beat('answer', 'solve', 'Đáp án: một phần sáu. Thứ tự tương đối của k người luôn có k giai thừa khả năng như nhau.'),
    Beat('outro', 'outro', outro_text(355)),
]

FORMULAS = formulas('1/6', OPTIONS,
                    rel='3! = 6 "thứ tự"',
                    chk='(C_5^3 dot 2!)/(5!) = 20/120 = 1/6')


def validate() -> bool:
    good = sum(p.index('A') < p.index('B') < p.index('C') for p in permutations('ABCDE'))
    assert F(good, 120) == F(1, 6)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS355(ShortScene):
    N = 355

    def line(self, order, frac=.06):
        new = VGroup(*[token(c, COL[c], .36) for c in order]).arrange(buff=.3).move_to([0, 1.3, 0])
        self.play(*([FadeOut(self.row)] if self.row else []), FadeIn(new), run_time=self.rt(frac))
        self.row = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.row = None
        self.wait_until(.3, t0)
        self.line('DAEBC')

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.play(*[self.row[i].animate.set_opacity(.25) for i, c in enumerate('DAEBC') if c in 'DE'], run_time=self.rt(.05))
        self.write_board(self.M('rel', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.line('CDBAE', .05)
        self.wait_until(.6, t0)
        self.line('ADBEC', .05)

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('chk', 1.6)
        self.write_board(m)
        self.frame(m)

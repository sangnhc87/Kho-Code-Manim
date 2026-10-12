"""XSS342 · Hộp nào cũng đủ màu — 3 đỏ 3 xanh 3 vàng vào 3 hộp × 3 chỗ: 9!/(3!)³ = 1680 cách đặt màu; mỗi hộp là hoán vị của 3 màu: (3!)³ = 216 → 9/70."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path

from manim import FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS342', 'answer': '9/70'}
PROBLEM = ['Chia $9$ bi ($3$ đỏ, $3$ xanh, $3$ vàng) vào $3$',
           'hộp, mỗi hộp $3$ bi. Xác suất hộp nào',
           'cũng đủ $3$ màu?']
OPTIONS = ['9/70', '1/9', '3/28']
CORRECT = 0
ANSWER_VALUE = 9 / 70


def count():
    seqs = set(permutations('RRRBBBYYY'))
    good = sum(all(len(set(s[3 * i:3 * i + 3])) == 3 for i in range(3)) for s in seqs)
    return good, len(seqs)


BEATS = [
    Beat('hook', 'hook', 'Chín bi gồm ba đỏ, ba xanh, ba vàng được chia ngẫu nhiên vào ba hộp, mỗi hộp ba bi. '
                         'Xác suất hộp nào cũng có đủ ba màu là bao nhiêu?'),
    Beat('guess', 'hook', 'Chín phần bảy mươi, một phần chín, hay ba phần hai mươi tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Coi ba hộp là chín chỗ. Số cách đặt màu vào chín chỗ là chín giai thừa chia ba giai thừa mũ ba, bằng một nghìn sáu trăm tám mươi.'),
    Beat('s2', 'solve', 'Hộp nào cũng đủ màu thì ba chỗ trong mỗi hộp là một hoán vị của đỏ, xanh, vàng: ba giai thừa cách cho mỗi hộp, ba hộp là hai trăm mười sáu.'),
    Beat('s3', 'solve', 'Xác suất hai trăm mười sáu phần một nghìn sáu trăm tám mươi, rút gọn chín phần bảy mươi, khoảng mười ba phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: chín phần bảy mươi. Chia đều vào hộp vẫn là bài hoán vị lặp quen thuộc.'),
    Beat('outro', 'outro', outro_text(342)),
]

FORMULAS = formulas('9/70', OPTIONS,
                    all='(9!)/(3! dot 3! dot 3!) = 1680',
                    good='(3!)^3 = 216',
                    prob='P = 216/1680 = 9/70')


def validate() -> bool:
    good, total = count()
    assert total == factorial(9) // 216 == 1680 and good == 216
    assert F(good, total) == F(9, 70)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS342(ShortScene):
    N = 342

    def boxes(self, cols):
        return VGroup(*[urn(cols[3 * i:3 * i + 3], cols=3, r=.27) for i in range(3)]).arrange(buff=.4).move_to([0, 1.3, 0])

    def swap(self, cols, frac=.05):
        new = self.boxes(cols)
        self.play(FadeOut(self.cur), FadeIn(new), run_time=self.rt(frac))
        self.cur = new

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.cur = self.boxes('RRBYBYRYB')
        self.wait_until(.5, t0)
        self.play(FadeIn(self.cur, lag_ratio=.2), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        for f, c in ((.1, 'RBYYRBBYR'), (.4, 'YBRRYBBRY')):
            self.wait_until(f, t0)
            self.swap(c, .05)
        self.write_board(self.M('good', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

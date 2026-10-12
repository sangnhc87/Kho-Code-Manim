"""XSS259 · n đỏ, n xanh — P(cùng màu) = 2C(n,2)/C(2n,2) = (n − 1)/(2n − 1) = 4/9 ⇒ n = 5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS259', 'answer': 'n = 5'}
PROBLEM = ['Hộp có $n$ bi đỏ và $n$ bi xanh. Rút $2$ bi,',
           'xác suất hai bi cùng màu là $4/9$. Tìm $n$.']
OPTIONS = ['n = 4', 'n = 5', 'n = 9']
CORRECT = 1
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Hộp có số bi đỏ bằng số bi xanh, cùng là n. Rút hai bi, xác suất hai bi cùng màu là bốn phần chín. Tìm n.'),
    Beat('guess', 'hook', 'Bốn, năm, hay chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cùng màu: hai lần tổ hợp chập hai của n, bằng n nhân n trừ một. Tổng: tổ hợp chập hai của hai n, bằng n nhân hai n trừ một.'),
    Beat('s2', 'solve', 'Rút gọn n: xác suất cùng màu bằng n trừ một chia hai n trừ một, luôn nhỏ hơn một phần hai một chút.'),
    Beat('s3', 'solve', 'Đặt bằng bốn phần chín: chín n trừ chín bằng tám n trừ bốn, n bằng năm. Kiểm tra: bốn phần chín. Chính xác!'),
    Beat('answer', 'solve', 'Đáp án: n bằng năm. Rút gọn công thức trước khi giải, phương trình sẽ gọn đến bất ngờ!'),
    Beat('outro', 'outro', outro_text(259)),
]

FORMULAS = formulas('n = 5', OPTIONS,
                    fwd='P = (2 C_n^2)/(C_(2 n)^2) = (n - 1)/(2 n - 1)',
                    sol='(n - 1)/(2 n - 1) = 4/9 arrow.r.double n = 5')


def validate() -> bool:
    assert all(F(2 * comb(n, 2), comb(2 * n, 2)) == F(n - 1, 2 * n - 1) for n in range(2, 30))
    assert [n for n in range(1, 60) if F(2 * comb(n, 2), comb(2 * n, 2)) == F(4, 9)] == [5]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS259(ShortScene):
    N = 259

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.u = urn('RRRRRBBBBB', cols=5, r=.32).move_to([0, 1.9, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('fwd', 1.9))

    def beat_s2(self, T):
        self.play(self.u.animate.set_opacity(.4), run_time=self.rt(.04))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)



"""XSS250 · Hai đáp số cho x — 5x/C(5+x,2) = 5/9 ⇔ x² − 9x + 20 = 0 ⇔ x = 4 hoặc 5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS250', 'answer': 'x = 4 hoặc x = 5'}
PROBLEM = ['Hộp có $5$ bi đỏ và $x$ bi xanh.',
           'Rút $2$ bi, xác suất được hai bi',
           'khác màu là $5/9$. Tìm $x$.']
OPTIONS = ['x = 4', 'x = 4 " hoặc " x = 5', 'x = 5']
CORRECT = 1
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đỏ và x bi xanh. Rút hai bi, xác suất được hai bi khác màu là năm phần chín. Tìm x. '
                         'Bài này có một bất ngờ ở cuối!'),
    Beat('guess', 'hook', 'x bằng bốn, x bằng bốn hoặc năm, hay x bằng năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai bi khác màu: năm nhân x cách. Tổng số cách: tổ hợp chập hai của năm cộng x. '
                        'Phương trình: mười x chia tích năm cộng x và bốn cộng x bằng năm phần chín.'),
    Beat('s2', 'solve', 'Nhân chéo và rút gọn: x bình phương trừ chín x cộng hai mươi bằng không. Phương trình bậc hai có hai nghiệm: x bằng bốn và x bằng năm.'),
    Beat('s3', 'solve', 'Cả hai đều thỏa mãn! Với bốn xanh: hai mươi phần ba mươi sáu. Với năm xanh: hai mươi lăm phần bốn mươi lăm. Đều bằng năm phần chín.'),
    Beat('answer', 'solve', 'Đáp án: x bằng bốn hoặc năm. Bài ngược có thể có nhiều đáp số, luôn kiểm tra đủ các nghiệm!'),
    Beat('outro', 'outro', outro_text(250)),
]

FORMULAS = formulas('x = 4 " hoặc " x = 5', OPTIONS,
                    eq='(5 x)/(C_(5 + x)^2) = 5/9',
                    quad='x^2 - 9 x + 20 = 0 arrow.l.r.double x = 4 " hoặc " x = 5',
                    check='20/36 = 25/45 = 5/9')


def validate() -> bool:
    assert [x for x in range(100) if F(5 * x, comb(5 + x, 2)) == F(5, 9)] == [4, 5]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS250(ShortScene):
    N = 250

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.u = urn(['R'] * 5 + ['#475569'] * 4, cols=5, r=.32).move_to([0, 1.9, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        m = self.M('eq', 2.2)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.35, t0)
        self.write_board(self.M('quad', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('check', 1.9))
        self.wait_until(.6, t0)
        self.write_board(tx('hai nghiệm đều đúng!', 28, CORAL, bold=True), anim='fade')

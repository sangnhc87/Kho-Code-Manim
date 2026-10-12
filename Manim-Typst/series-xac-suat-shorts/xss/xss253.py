"""XSS253 · Tỉ lệ bệnh là bao nhiêu? — 0,9x / (0,9x + 0,1(1 − x)) = 1/2 ⇒ 0,9x = 0,1(1 − x) ⇒ x = 0,1."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS253', 'answer': 'x = 0,1'}
PROBLEM = ['Xét nghiệm nhạy $90%$, dương tính giả $10%$.',
           'Người dương tính có $50%$ là bệnh thật.',
           'Tìm tỉ lệ bệnh $x$ trong dân số.']
OPTIONS = ['x = "0,5"', 'x = "0,1"', 'x = "0,01"']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('B', CORAL, 'x', [('+', GOLD, '"0,9"', [])]),
            ('K', GREEN, '1 - x', [('+', GOLD, '"0,1"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Một xét nghiệm phát hiện đúng chín mươi phần trăm người bệnh, nhưng báo nhầm dương tính mười phần trăm người khỏe. '
                         'Thống kê cho thấy người dương tính chỉ có năm mươi phần trăm thật sự bị bệnh. Tỉ lệ bệnh trong dân số là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy năm, không phẩy một, hay không phẩy không một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bayes ngược: đặt x là tỉ lệ bệnh. Hai lá dương tính: bệnh, không phẩy chín x; khỏe, không phẩy một nhân một trừ x.'),
    Beat('s2', 'solve', 'Xác suất bệnh khi dương tính bằng một phần hai nghĩa là hai lá bằng nhau: không phẩy chín x bằng không phẩy một trừ không phẩy một x.'),
    Beat('s3', 'solve', 'Giải: x bằng không phẩy một. Mười phần trăm dân số bị bệnh thì xét nghiệm dương tính đúng một nửa.'),
    Beat('answer', 'solve', 'Đáp án: x bằng không phẩy một. Bayes bằng một phần hai nghĩa là hai nhánh có trọng lượng bằng nhau!'),
    Beat('outro', 'outro', outro_text(253)),
]

FORMULAS = formulas('x = "0,1"', OPTIONS,
                    eq='("0,9" x)/("0,9" x + "0,1" (1 - x)) = 1/2',
                    sol='"0,9" x = "0,1" (1 - x) arrow.r.double x = "0,1"')


def validate() -> bool:
    sols = [F(k, 100) for k in range(1, 100) if F(9, 10) * F(k, 100) / (F(9, 10) * F(k, 100) + F(1, 10) * (1 - F(k, 100))) == F(1, 2)]
    assert sols == [F(1, 10)]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS253(TreeMixin, ShortScene):
    N = 253

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='người dân')
        self.wait_until(.8, t0)
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[n.animate.scale(1.3) for n, _ in self.leaves], run_time=self.rt(.05))
        self.wait_until(.4, t0)
        m = self.M('eq', 1.6)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        m = self.M('sol', 1.6)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('hai nhánh bằng nhau ⇔ $P = 1/2$', 26, SOFT), anim='fade')

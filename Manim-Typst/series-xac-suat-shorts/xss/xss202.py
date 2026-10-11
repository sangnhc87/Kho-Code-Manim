"""XSS202 · Cùng màu thì màu gì? — P(ĐĐ | cùng màu) = (6/30)/(14/30) = 3/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL  # noqa: E402
from xss.xss201 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS202', 'answer': '3/7'}
PROBLEM = ['Hộp I: $3$ đỏ $2$ xanh; hộp II: $2$ đỏ $4$ xanh.',
           'Rút mỗi hộp $1$ bi, biết hai bi cùng màu.',
           'Xác suất cả hai đều đỏ?']
OPTIONS = ['1/2', '3/7', '1/5']
CORRECT = 1
ANSWER_VALUE = 3 / 7

BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: rút mỗi hộp một bi, và bạn được biết hai bi cùng màu. '
                         'Xác suất cả hai bi đều đỏ là bao nhiêu? Hộp một nhiều đỏ, hộp hai nhiều xanh, vậy có phải một phần hai?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần bảy, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện "cùng màu" giữ lại hai lá: đỏ đỏ sáu phần ba mươi, xanh xanh tám phần ba mươi.'),
    Beat('s2', 'solve', 'Xác suất có điều kiện: sáu phần ba mươi chia mười bốn phần ba mươi, bằng ba phần bảy.'),
    Beat('s3', 'solve', 'Xanh xanh nhiều hơn vì hộp hai có tới bốn bi xanh. Ba phần bảy nhỏ hơn một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: ba phần bảy. Một cây, hai câu hỏi: xuôi là toàn phần, ngược là có điều kiện!'),
    Beat('outro', 'outro', outro_text(202)),
]

FORMULAS = formulas('3/7', OPTIONS,
                    prob='P(Đ Đ | "cùng màu") = (6/30)/(14/30) = 3/7')


def validate() -> bool:
    same = [(a, b) for a, b in product('RRRBB', 'RRBBBB') if a == b]
    assert F(sum(a == 'R' for a, _ in same), len(same)) == F(3, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS202(TreeMixin, ShortScene):
    N = 202

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='hộp I')
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[1][0].animate.set_opacity(.15), self.leaves[2][0].animate.set_opacity(.15),
                  self.leaves[0][0].animate.scale(1.3), self.leaves[3][0].animate.scale(1.3), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.TM('$6/30$ và $8/30$', 30))

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('xanh xanh nhiều hơn: $8/30 > 6/30$', 26, CORAL), anim='fade')

"""XSS184 · An rút trước, Bình rút sau — Bayes: 0,6·16/36 / (0,6·16/36 + 0,4·18/36) = 4/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS184', 'answer': '4/7'}
PROBLEM = ['Hộp $6$ đỏ $4$ xanh. An lấy $1$ bi, Bình',
           'lấy tiếp $2$ bi. Biết $2$ bi của Bình cùng',
           'màu. Xác suất An lấy bi đỏ?']
OPTIONS = ['3/5', '4/7', '8/15']
CORRECT = 1
ANSWER_VALUE = 4 / 7
BRANCHES = [('Đ', CORAL, '6/10', [('cùng', GOLD, '16/36', [])]),
            ('X', CYAN, '4/10', [('cùng', GOLD, '18/36', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có sáu bi đỏ và bốn bi xanh. An lấy một bi giấu đi, rồi Bình lấy tiếp hai bi, và hai bi của Bình cùng màu. '
                         'Xác suất An đã lấy bi đỏ là bao nhiêu? Đây là dạng câu trả lời ngắn chặn điểm.'),
    Beat('guess', 'hook', 'Ba phần năm, bốn phần bảy, hay tám phần mười lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh An đỏ: hộp còn năm đỏ bốn xanh. Bình lấy hai bi cùng màu: tổ hợp chập hai của năm cộng tổ hợp chập hai của bốn, '
                        'mười sáu trên ba mươi sáu.'),
    Beat('s2', 'solve', 'Nhánh An xanh: hộp còn sáu đỏ ba xanh: mười lăm cộng ba, mười tám trên ba mươi sáu. '
                        'Nhân với xác suất nhánh: không phẩy sáu và không phẩy bốn.'),
    Beat('s3', 'solve', 'Bayes: không phẩy sáu nhân mười sáu, chia cho không phẩy sáu nhân mười sáu cộng không phẩy bốn nhân mười tám, '
                        'bằng chín phẩy sáu chia mười sáu phẩy tám, tức bốn phần bảy.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy, khoảng không phẩy năm bảy. Rút nhiều bi ở tầng sau thì dùng tổ hợp ngay trên nhánh cây!'),
    Beat('outro', 'outro', outro_text(184)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    red='P("cùng" | Đ) = (C_5^2 + C_4^2)/(C_9^2) = 16/36',
                    blue='P("cùng" | X) = (C_6^2 + C_3^2)/(C_9^2) = 18/36',
                    bayes='P(Đ | "cùng") = ("0,6" dot 16)/("0,6" dot 16 + "0,4" dot 18) = 4/7')


def validate() -> bool:
    balls = ['R'] * 6 + ['B'] * 4
    num = den = 0
    for w in permutations(range(10), 3):
        same = balls[w[1]] == balls[w[2]]
        den += same
        num += same and balls[w[0]] == 'R'
    assert F(num, den) == F(4, 7)
    assert F(comb(5, 2) + comb(4, 2), comb(9, 2)) == F(16, 36)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS184(TreeMixin, ShortScene):
    N = 184

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=5.8, root_label='An lấy', edge_size=28, r=.55)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:3]), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.write_board(self.M('red', 1.7))
        self.play(FadeIn(tx('cùng: hai bi của Bình cùng màu', 22, SOFT).move_to([0, -1.0, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][3:]), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.write_board(self.M('blue', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.5)
        self.write_board(m)
        self.frame(m)

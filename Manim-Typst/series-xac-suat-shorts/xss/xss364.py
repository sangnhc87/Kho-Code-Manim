"""XSS364 · Số ngửa quyết định số bi — k ngửa (¼, ½, ¼), rút k + 1 bi từ 3đ3x; P(≥ 1 đỏ) = ¼·½ + ½·4/5 + ¼·19/20 = 61/80."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402

EPISODE = {'code': 'XSS364', 'answer': '61/80'}
PROBLEM = ['Tung $2$ đồng xu được $k$ mặt ngửa, rồi rút',
           '$k + 1$ bi từ hộp $3$ đỏ $3$ xanh. Xác suất',
           'có ít nhất $1$ bi đỏ?']
OPTIONS = ['61/80', '3/4', '19/20']
CORRECT = 0
ANSWER_VALUE = 61 / 80
PK = [F(1, 4), F(1, 2), F(1, 4)]
ANY = [1 - F(comb(3, k + 1), comb(6, k + 1)) for k in range(3)]
BRANCHES = [('0', CYAN, '1/4', [('Đ', CORAL, '1/2', [])]),
            ('1', CYAN, '1/2', [('Đ', CORAL, '4/5', [])]),
            ('2', CYAN, '1/4', [('Đ', CORAL, '19/20', [])])]

BEATS = [
    Beat('hook', 'hook', 'Tung hai đồng xu được k mặt ngửa, rồi rút k cộng một bi từ hộp ba đỏ ba xanh. '
                         'Xác suất có ít nhất một bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Sáu mươi mốt phần tám mươi, ba phần tư, hay mười chín phần hai mươi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Số ngửa là không, một, hai với xác suất một phần tư, một phần hai, một phần tư. Số bi rút là một, hai hoặc ba.'),
    Beat('s2', 'solve', 'Dùng phần bù: không có bi đỏ nào nghĩa là toàn xanh. Rút một bi: có đỏ với xác suất một phần hai. Hai bi: một trừ ba phần mười lăm, bốn phần năm. Ba bi: một trừ một phần hai mươi, mười chín phần hai mươi.'),
    Beat('s3', 'solve', 'Cộng theo cây: một phần tư nhân một phần hai, cộng một phần hai nhân bốn phần năm, cộng một phần tư nhân mười chín phần hai mươi, bằng sáu mươi mốt phần tám mươi.'),
    Beat('answer', 'solve', 'Đáp án: sáu mươi mốt phần tám mươi. Mỗi nhánh dùng phần bù riêng, rồi gộp bằng xác suất toàn phần.'),
    Beat('outro', 'outro', outro_text(364)),
]

FORMULAS = formulas('61/80', OPTIONS,
                    comp='1 - (C_3^(k+1))/(C_6^(k+1)): quad 1/2, 4/5, 19/20',
                    prob='P = 1/4 dot 1/2 + 1/2 dot 4/5 + 1/4 dot 19/20 = 61/80')


def validate() -> bool:
    assert ANY == [F(1, 2), F(4, 5), F(19, 20)]
    assert sum(p * a for p, a in zip(PK, ANY)) == F(61, 80)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS364(TreeMixin, ShortScene):
    N = 364

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=6.4, r=.34, edge_size=28)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(*[FadeIn(m) for m in self.levels[1]], run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.4, t0)
        self.write_board(self.M('comp', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.4)
        self.write_board(m)
        self.frame(m)

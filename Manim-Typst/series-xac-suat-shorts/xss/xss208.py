"""XSS208 · Xúc xắc chọn hộp, hai bi đỏ — 6 → A (5Đ1X), khác → B (2Đ4X): (1/6·2/3)/(1/6·2/3 + 5/6·1/15) = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS208', 'answer': '2/3'}
PROBLEM = ['Gieo xúc xắc: ra $6$ chọn hộp A ($5$ đỏ $1$',
           'xanh), khác $6$ chọn hộp B ($2$ đỏ $4$ xanh).',
           'Rút $2$ bi đều đỏ. Xác suất hộp A?']
OPTIONS = ['1/6', '2/3', '10/11']
CORRECT = 1
ANSWER_VALUE = 2 / 3
BRANCHES = [('A', GOLD, '1/6', [('ĐĐ', CORAL, '10/15', [])]),
            ('B', PURPLE, '5/6', [('ĐĐ', CORAL, '1/15', [])])]


def rr(box):
    pairs = list(combinations(box, 2))
    return F(sum(a == b == 'R' for a, b in pairs), len(pairs))


BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc: ra sáu thì chọn hộp A có năm đỏ một xanh, không ra sáu thì chọn hộp B có hai đỏ bốn xanh. '
                         'Rút hai bi đều đỏ. Xác suất đã chọn hộp A là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, hai phần ba, hay mười phần mười một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tiên nghiệm: hộp A rất hiếm, chỉ một phần sáu. Nhưng hộp A cho hai đỏ với xác suất tổ hợp chập hai của năm trên mười lăm, '
                        'mười phần mười lăm; hộp B chỉ một phần mười lăm.'),
    Beat('s2', 'solve', 'Hai lá: một phần sáu nhân mười phần mười lăm, bằng mười phần chín mươi; năm phần sáu nhân một phần mười lăm, bằng năm phần chín mươi.'),
    Beat('s3', 'solve', 'Bayes: mười chia mười lăm, bằng hai phần ba. Bằng chứng mạnh gấp mười lần đã lật ngược tiên nghiệm năm chọi một.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Kết quả Bayes là cuộc giằng co giữa tiên nghiệm và sức mạnh của bằng chứng!'),
    Beat('outro', 'outro', outro_text(208)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    lik='P(Đ Đ | A) = (C_5^2)/(C_6^2) = 10/15, quad P(Đ Đ | B) = (C_2^2)/(C_6^2) = 1/15',
                    bayes='P(A | Đ Đ) = (10/90)/(10/90 + 5/90) = 2/3')


def validate() -> bool:
    a, b = rr('RRRRRB'), rr('RRBBBB')
    assert (a, b) == (F(10, 15), F(1, 15))
    assert F(1, 6) * a / (F(1, 6) * a + F(5, 6) * b) == F(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS208(TreeMixin, ShortScene):
    N = 208

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=5.6, root_label='xúc xắc', r=.5)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.write_board(self.M('lik', 1.3))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.play(*[n.animate.scale(1.2) for n, _ in self.leaves], run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.8)
        self.write_board(m)
        self.frame(m)

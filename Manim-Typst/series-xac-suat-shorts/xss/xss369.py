"""XSS369 · Xanh thì thêm hai xanh — 3đ2x; đỏ → bỏ ra (2đ2x), xanh → trả lại + 2 xanh (3đ4x); P(X₁ | X₂) = (2/5·4/7)/(3/5·1/2 + 2/5·4/7) = 16/37."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402

EPISODE = {'code': 'XSS369', 'answer': '16/37'}
PROBLEM = ['Hộp $3$ đỏ $2$ xanh: rút $1$ bi, đỏ thì bỏ',
           'ra ngoài, xanh thì trả lại kèm $2$ xanh.',
           'Lần hai rút được xanh. Xác suất lần một',
           'cũng rút xanh?']
OPTIONS = ['2/5', '16/37', '8/15']
CORRECT = 1
ANSWER_VALUE = 16 / 37
BRANCHES = [('Đ', CORAL, '3/5', [('X', CYAN, '2/4', [])]), ('X', CYAN, '2/5', [('X', CYAN, '4/7', [])])]
A, B = F(3, 5) * F(2, 4), F(2, 5) * F(4, 7)

BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi đỏ, hai bi xanh. Rút một bi: nếu đỏ thì bỏ ra ngoài, nếu xanh thì trả lại kèm thêm hai bi xanh. '
                         'Lần rút thứ hai được bi xanh. Xác suất lần một cũng rút xanh?'),
    Beat('guess', 'hook', 'Hai phần năm, mười sáu phần ba mươi bảy, hay tám phần mười lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lần một đỏ, ba phần năm: hộp còn hai đỏ hai xanh, lần hai xanh với xác suất một phần hai.'),
    Beat('s2', 'solve', 'Lần một xanh, hai phần năm: hộp thành ba đỏ bốn xanh, lần hai xanh với xác suất bốn phần bảy.'),
    Beat('s3', 'solve', 'Hai lá: ba phần mười và tám phần ba mươi lăm. Quy đồng thành hai mươi mốt và mười sáu phần bảy mươi. Bayes: mười sáu phần ba mươi bảy.'),
    Beat('answer', 'solve', 'Đáp án: mười sáu phần ba mươi bảy. Hành động sau thay đổi tùy kết quả trước: cây ghi lại thành phần hộp ở từng nhánh.'),
    Beat('outro', 'outro', outro_text(369)),
]

FORMULAS = formulas('16/37', OPTIONS,
                    leafs='3/5 dot 1/2 = 21/70, quad 2/5 dot 4/7 = 16/70',
                    prob='P(X_1 | X_2) = 16/(21 + 16) = 16/37')


def validate() -> bool:
    assert B / (A + B) == F(16, 37)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS369(TreeMixin, ShortScene):
    N = 369

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.0, r=.4)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), run_time=self.rt(.08))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('leafs', 1.3))
        self.wait_until(.6, t0)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

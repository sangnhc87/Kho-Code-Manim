"""XSS215 · Ba hộp, hai bi khác màu — P(khác | I) = 4/6, II = 3/6, III = 0: P(I | khác) = 4/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE, SOFT  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS215', 'answer': '4/7'}
PROBLEM = ['Hộp I: $2$ đỏ $2$ xanh; II: $3$ đỏ $1$ xanh;',
           'III: $4$ đỏ. Chọn ngẫu nhiên $1$ hộp, rút',
           '$2$ bi khác màu. Xác suất hộp I?']
OPTIONS = ['1/3', '4/7', '2/3']
CORRECT = 1
ANSWER_VALUE = 4 / 7
BOXES = ('RRBB', 'RRRB', 'RRRR')
BRANCHES = [('I', CYAN, '1/3', [('≠', GOLD, '4/6', [])]),
            ('II', PURPLE, '1/3', [('≠', GOLD, '3/6', [])]),
            ('III', CORAL, '1/3', [('≠', GOLD, '0', [])])]


def mixed(box):
    p = list(combinations(box, 2))
    return F(sum(a != b for a, b in p), len(p))


BEATS = [
    Beat('hook', 'hook', 'Ba hộp: hộp một hai đỏ hai xanh, hộp hai ba đỏ một xanh, hộp ba bốn đỏ. Chọn ngẫu nhiên một hộp, rút hai bi, '
                         'được hai bi khác màu. Xác suất đã chọn hộp một là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, bốn phần bảy, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi hộp rút hai bi có sáu cặp. Hộp một: bốn cặp khác màu. Hộp hai: ba cặp. Hộp ba: không cặp nào, vì toàn đỏ.'),
    Beat('s2', 'solve', 'Ba nhánh cùng một phần ba, nên tỉ lệ chỉ phụ thuộc số cặp khác màu: bốn, ba và không.'),
    Beat('s3', 'solve', 'Bayes: bốn chia bốn cộng ba cộng không, bằng bốn phần bảy. Hộp ba bị loại hoàn toàn bởi bằng chứng.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy. Khi các giả thuyết đồng khả năng, Bayes chỉ còn là so sánh khả năng gây ra bằng chứng!'),
    Beat('outro', 'outro', outro_text(215)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    lik='4/6, quad 3/6, quad 0',
                    bayes='P(I | "khác màu") = (4/6)/(4/6 + 3/6 + 0) = 4/7')


def validate() -> bool:
    lik = [mixed(b) for b in BOXES]
    assert lik == [F(4, 6), F(3, 6), 0] and lik[0] / sum(lik) == F(4, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS215(TreeMixin, ShortScene):
    N = 215

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.urns = urn_row([(b, n, SOFT) for b, n in zip(BOXES, ('hộp I', 'hộp II', 'hộp III'))], buff=.45)
        self.wait_until(.65, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('lik', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.urns.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=6.6, root_label='chọn hộp')
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.2))
        self.wait_until(.6, t0)
        self.play(self.leaves[2][0].animate.set_opacity(.15), run_time=self.rt(.04))

    def beat_s3(self, T):
        m = self.M('bayes', 1.6)
        self.write_board(m)
        self.frame(m)

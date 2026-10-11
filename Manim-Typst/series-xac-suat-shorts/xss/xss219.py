"""XSS219 · Chuyển đi rồi chuyển về — I (2Đ1X) → II (1Đ2X) → I, rút từ I: 7/12."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402
from xss._urnkit import transfer_arrow, urn_row  # noqa: E402

EPISODE = {'code': 'XSS219', 'answer': '7/12'}
PROBLEM = ['Hộp I: $2$ đỏ $1$ xanh; II: $1$ đỏ $2$ xanh.',
           'Chuyển $1$ bi I → II, rồi $1$ bi II → I, rồi',
           'rút $1$ bi từ I. Xác suất được đỏ?']
OPTIONS = ['2/3', '7/12', '1/2']
CORRECT = 1
ANSWER_VALUE = 7 / 12
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '2/3', [(*D, '2/4', [(*D, '2/3', [])]), (*X, '2/4', [(*D, '1/3', [])])]),
            (*X, '1/3', [(*D, '1/4', [(*D, '1', [])]), (*X, '3/4', [(*D, '2/3', [])])])]


def chain():
    total = F(0)
    for i, a in enumerate('RRB'):
        box1 = 'RRB'[:i] + 'RRB'[i + 1:]
        box2 = 'RBB' + a
        for j, b in enumerate(box2):
            box1b = box1 + b
            total += F(1, 3) * F(1, 4) * F(box1b.count('R'), 3)
    return total


BEATS = [
    Beat('hook', 'hook', 'Hộp một có hai đỏ một xanh, hộp hai có một đỏ hai xanh. Chuyển một bi từ hộp một sang hộp hai, '
                         'rồi chuyển một bi từ hộp hai về hộp một, rồi rút một bi từ hộp một. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần ba, bảy phần mười hai, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây ba tầng: bi đi, bi về, rồi lần rút. Tầng một: đi đỏ hai phần ba, đi xanh một phần ba. Hộp hai lúc đó có bốn bi.'),
    Beat('s2', 'solve', 'Đi đỏ: hộp hai thành hai đỏ hai xanh; về đỏ thì hộp một lại hai đỏ một xanh, về xanh thì một đỏ hai xanh. '
                        'Đi xanh: hộp hai một đỏ ba xanh; về đỏ thì hộp một ba đỏ, về xanh thì như cũ.'),
    Beat('s3', 'solve', 'Cộng bốn nhánh: hai phần chín cộng một phần chín cộng một phần mười hai cộng một phần sáu, bằng bảy phần mười hai, '
                        'thấp hơn hai phần ba ban đầu: hộp một bị hòa trộn với hộp hai.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần mười hai. Chuyển đi rồi chuyển về thì hộp nguồn bị "pha loãng" về phía hộp kia!'),
    Beat('outro', 'outro', outro_text(219)),
]

FORMULAS = formulas('7/12', OPTIONS,
                    sum='2/3 dot 2/4 dot 2/3 + 2/3 dot 2/4 dot 1/3 + 1/3 dot 1/4 dot 1 + 1/3 dot 3/4 dot 2/3',
                    tot='P = 2/9 + 1/9 + 1/12 + 1/6 = 7/12')


def validate() -> bool:
    assert chain() == F(7, 12)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS219(TreeMixin, ShortScene):
    N = 219

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.urns = urn_row([('RRB', 'hộp I', GOLD), ('RBB', 'hộp II', PURPLE)], y=1.5, buff=1.4)
        self.go = transfer_arrow(self.urns[0], self.urns[1], 'đi')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), FadeIn(self.go), run_time=self.rt(.1))

    def beat_s1(self, T):
        self.play(self.urns.animate.set_opacity(0), self.go.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns, self.go)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.2, width=7.0, root_label='đi → về → rút',
                                                  r=.34, edge_size=26)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.levels[3], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('sum', 1.2))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('tot', 1.8)
        self.write_board(m)
        self.frame(m)



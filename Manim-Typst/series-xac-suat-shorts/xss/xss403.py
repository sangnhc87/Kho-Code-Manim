"""XSS403 · Đỏ thì sang hộp kia — đỏ (2/3) → II thành 2đ2x, rút đỏ 1/2; xanh (1/3) → I còn 2 đỏ, rút đỏ chắc chắn: 1/3 + 1/3 = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from xss._boxswap import BRANCHES, RED_SECOND  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS403', 'answer': '2/3'}
PROBLEM = ['Rút $1$ bi từ hộp I ($2$ đỏ $1$ xanh): đỏ',
           'thì bỏ sang hộp II ($1$ đỏ $2$ xanh) rồi',
           'rút từ II; xanh thì rút tiếp từ I. Xác',
           'suất lần rút thứ hai được đỏ?']
OPTIONS = ['2/3', '1/2', '5/9']
CORRECT = 0
ANSWER_VALUE = 2 / 3

BEATS = [
    Beat('hook', 'hook', 'Hộp một có hai đỏ một xanh, hộp hai có một đỏ hai xanh. Rút một bi từ hộp một: nếu đỏ thì bỏ sang hộp hai rồi rút từ hộp hai; nếu xanh thì để ra ngoài và rút tiếp từ hộp một. '
                         'Xác suất lần rút thứ hai được đỏ?'),
    Beat('guess', 'hook', 'Hai phần ba, một phần hai, hay năm phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh đỏ, hai phần ba: hộp hai thành hai đỏ hai xanh, rút đỏ với một phần hai.'),
    Beat('s2', 'solve', 'Nhánh xanh, một phần ba: bi xanh đã ra ngoài, hộp một chỉ còn hai bi đỏ, chắc chắn rút đỏ.'),
    Beat('s3', 'solve', 'Cộng: hai phần ba nhân một phần hai, cộng một phần ba nhân một, bằng một phần ba cộng một phần ba, tức hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Hành động thứ hai khác nhau tùy nhánh, nhưng cây vẫn tính gọn.'),
    Beat('outro', 'outro', outro_text(403)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    prob='P(Đ_2) = 2/3 dot 1/2 + 1/3 dot 1 = 2/3')


def validate() -> bool:
    assert RED_SECOND == F(2, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS403(TreeMixin, ShortScene):
    N = 403

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.urns = urn_row([('RRB', 'hộp I', None), ('RBB', 'hộp II', None)], y=1.9, r=.24)
        self.play(FadeIn(self.urns), run_time=self.rt(.05))
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, .9), dy=1.3, width=4.6, r=.38, edge_size=26)
        self.tree = VGroup(*self.levels)

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), run_time=self.rt(.08))

    def beat_s3(self, T):
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

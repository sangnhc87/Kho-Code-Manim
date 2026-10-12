"""XSS404 · Lần hai đỏ thì lần một? — P(xanh trước | đỏ sau) = (1/3)/(2/3) = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from xss._boxswap import BLUE_FIRST, BRANCHES, RED_SECOND  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS404', 'answer': '1/2'}
PROBLEM = ['Như bài trước (I: $2$ đỏ $1$ xanh; II: $1$',
           'đỏ $2$ xanh), biết lần rút thứ hai được',
           'đỏ. Xác suất lần một rút xanh?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5

BEATS = [
    Beat('hook', 'hook', 'Tiếp bài trước: rút từ hộp một, đỏ thì bỏ sang hộp hai rồi rút từ hộp hai, xanh thì rút tiếp từ hộp một. Biết lần thứ hai được đỏ. '
                         'Xác suất lần một đã rút xanh?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Từ bài trước: xác suất lần hai đỏ bằng hai phần ba, gồm hai nhánh mỗi nhánh một phần ba.'),
    Beat('s2', 'solve', 'Nhánh lần một xanh đóng góp một phần ba nhân một, đúng một phần ba.'),
    Beat('s3', 'solve', 'Bayes: một phần ba chia hai phần ba, bằng một phần hai. Biết lần hai đỏ, xác suất lần một xanh tăng từ một phần ba lên một nửa.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Nhánh xanh hiếm hơn nhưng lần hai đỏ chắc chắn, nên hai nhánh cân bằng.'),
    Beat('outro', 'outro', outro_text(404)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    prob='P(X_1 | Đ_2) = (1/3 dot 1)/(2/3) = 1/2')


def validate() -> bool:
    assert BLUE_FIRST / RED_SECOND == F(1, 2)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS404(TreeMixin, ShortScene):
    N = 404

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.urns = urn_row([('RRB', 'hộp I', None), ('RBB', 'hộp II', None)], y=1.9, r=.24)
        self.play(FadeIn(self.urns), run_time=self.rt(.05))
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, .9), dy=1.3, width=4.6, r=.38, edge_size=26)
        self.wait_until(.7, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.TM('$P(Đ_2) = 2/3$', 36))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.play(self.leaves[1][0].animate.scale(1.3), run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

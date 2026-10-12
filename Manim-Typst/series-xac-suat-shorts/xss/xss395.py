"""XSS395 · Ngày kia mưa thì mai? — hôm nay mưa; M→M 0,6, T→M 0,2; P(mai M, kia M) = 0,36, P(mai T, kia M) = 0,08 → 9/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS395', 'answer': '9/11'}
PROBLEM = ['Hôm nay mưa. Nếu mưa thì mai mưa $"0,6"$;',
           'nếu tạnh thì mai mưa $"0,2"$. Biết ngày kia',
           'mưa. Xác suất ngày mai mưa?']
OPTIONS = ['9/11', '3/5', '2/3']
CORRECT = 0
ANSWER_VALUE = 9 / 11
MM, TM = F(3, 5) * F(3, 5), F(2, 5) * F(1, 5)
BRANCHES = [('M', CYAN, '"0,6"', [('M', CYAN, '"0,6"', [])]), ('T', GOLD, '"0,4"', [('M', CYAN, '"0,2"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hôm nay trời mưa. Nếu hôm trước mưa thì hôm sau mưa với xác suất không phẩy sáu; nếu tạnh thì hôm sau mưa với không phẩy hai. '
                         'Biết ngày kia mưa. Xác suất ngày mai mưa?'),
    Beat('guess', 'hook', 'Chín phần mười một, ba phần năm, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây hai tầng xuất phát từ hôm nay mưa: ngày mai mưa không phẩy sáu, tạnh không phẩy bốn.'),
    Beat('s2', 'solve', 'Ngày kia mưa: qua ngày mai mưa là không phẩy sáu nhân không phẩy sáu, không phẩy ba sáu; qua ngày mai tạnh là không phẩy bốn nhân không phẩy hai, không phẩy không tám.'),
    Beat('s3', 'solve', 'Bayes: không phẩy ba sáu chia không phẩy bốn bốn, bằng chín phần mười một.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười một. Thông tin tương lai cũng cập nhật được hiện tại: điều kiện chảy ngược thời gian.'),
    Beat('outro', 'outro', outro_text(395)),
]

FORMULAS = formulas('9/11', OPTIONS,
                    leafs='"0,6" dot "0,6" = "0,36", quad "0,4" dot "0,2" = "0,08"',
                    prob='P = ("0,36")/("0,36" + "0,08") = 9/11')


def validate() -> bool:
    assert MM / (MM + TM) == F(9, 11)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS395(TreeMixin, ShortScene):
    N = 395

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.7, width=5.0, r=.42, edge_size=28)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[1]), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.write_board(self.M('leafs', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

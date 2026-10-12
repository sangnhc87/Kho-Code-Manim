"""XSS375 · Nhiệm vụ nào thất bại? — 3 nhiệm vụ đều 1/3, thất bại 0,1; 0,4; 0,7 → P(NV3 | thất bại) = 0,7/1,2 = 7/12."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS375', 'answer': '7/12'}
PROBLEM = ['An bốc thăm $1$ trong $3$ nhiệm vụ, thành',
           'công với xác suất $"0,9"$; $"0,6"$; $"0,3"$. Biết',
           'An thất bại. Xác suất An bốc nhiệm vụ $3$?']
OPTIONS = ['1/3', '7/12', '7/10']
CORRECT = 1
ANSWER_VALUE = 7 / 12
FAIL = [F(1, 10), F(4, 10), F(7, 10)]
BRANCHES = [('1', CYAN, '1/3', [('T', CORAL, '"0,1"', [])]),
            ('2', GOLD, '1/3', [('T', CORAL, '"0,4"', [])]),
            ('3', PURPLE, '1/3', [('T', CORAL, '"0,7"', [])])]

BEATS = [
    Beat('hook', 'hook', 'An bốc thăm một trong ba nhiệm vụ, xác suất thành công lần lượt không phẩy chín, không phẩy sáu, không phẩy ba. '
                         'Biết An thất bại. Xác suất An đã bốc nhiệm vụ ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, bảy phần mười hai, hay bảy phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi nhiệm vụ một phần ba. Xác suất thất bại tương ứng: không phẩy một, không phẩy bốn, không phẩy bảy.'),
    Beat('s2', 'solve', 'Hệ số một phần ba triệt tiêu. Tổng các khả năng thất bại: không phẩy một cộng không phẩy bốn cộng không phẩy bảy, bằng một phẩy hai.'),
    Beat('s3', 'solve', 'Nhiệm vụ ba chiếm không phẩy bảy trên một phẩy hai, tức bảy phần mười hai.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần mười hai. Khi tiên nghiệm đều nhau, hậu nghiệm tỉ lệ thẳng với khả năng.'),
    Beat('outro', 'outro', outro_text(375)),
]

FORMULAS = formulas('7/12', OPTIONS,
                    sum='"0,1" + "0,4" + "0,7" = "1,2"',
                    prob='P(3 | T) = ("0,7")/("1,2") = 7/12')


def validate() -> bool:
    assert FAIL[2] / sum(FAIL) == F(7, 12)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS375(TreeMixin, ShortScene):
    N = 375

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=6.2, r=.38, edge_size=28)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('sum', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

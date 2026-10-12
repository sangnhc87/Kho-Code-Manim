"""XSS373 · Gieo hai lần lấy lớn nhất — ngửa: max của 2 lần = 6 với 11/36; sấp: 1/6; P(ngửa | 6) = 11/(11 + 6) = 11/17."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS373', 'answer': '11/17'}
PROBLEM = ['Tung xu: ngửa thì gieo xúc xắc $2$ lần lấy',
           'số lớn nhất, sấp thì gieo $1$ lần. Kết quả',
           'là $6$. Xác suất đồng xu đã ra ngửa?']
OPTIONS = ['1/2', '11/17', '2/3']
CORRECT = 1
ANSWER_VALUE = 11 / 17
MAX6 = F(sum(max(a, b) == 6 for a in range(1, 7) for b in range(1, 7)), 36)
BRANCHES = [('N', GOLD, '1/2', [('6', CORAL, '11/36', [])]), ('S', SOFT, '1/2', [('6', CORAL, '1/6', [])])]

BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu. Ngửa thì gieo xúc xắc hai lần và lấy số lớn hơn; sấp thì chỉ gieo một lần. Kết quả cuối cùng là sáu. '
                         'Xác suất đồng xu đã ra ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, mười một phần mười bảy, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh ngửa: số lớn nhất bằng sáu khi có ít nhất một lần ra sáu, bằng một trừ hai mươi lăm phần ba mươi sáu, tức mười một phần ba mươi sáu.'),
    Beat('s2', 'solve', 'Nhánh sấp: ra sáu với xác suất một phần sáu, tức sáu phần ba mươi sáu.'),
    Beat('s3', 'solve', 'Hai nhánh đều một phần hai nên triệt tiêu. Bayes: mười một chia mười một cộng sáu, bằng mười một phần mười bảy.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần mười bảy. Gieo hai lần gần gấp đôi cơ hội ra sáu, nên sáu là bằng chứng nghiêng về ngửa.'),
    Beat('outro', 'outro', outro_text(373)),
]

FORMULAS = formulas('11/17', OPTIONS,
                    max6='P(max = 6) = 1 - (5/6)^2 = 11/36',
                    prob='P(N | 6) = (11/36)/(11/36 + 6/36) = 11/17')


def validate() -> bool:
    assert MAX6 == F(11, 36) and MAX6 / (MAX6 + F(1, 6)) == F(11, 17)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS373(TreeMixin, ShortScene):
    N = 373

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.0, r=.4)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('max6', 1.4))

    def beat_s2(self, T):
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), run_time=self.rt(.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

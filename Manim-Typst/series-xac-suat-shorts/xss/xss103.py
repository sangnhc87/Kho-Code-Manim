"""XSS103 · Ba máy sản xuất — Bayes 3 nhánh: P(máy III | lỗi) = 0,006 / 0,017 = 6/17."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE, SOFT  # noqa: E402

EPISODE = {'code': 'XSS103', 'answer': '6/17'}
PROBLEM = ['Máy I, II, III làm $50%$, $30%$, $20%$ sản',
           'phẩm, lỗi $1%$, $2%$, $3%$. Sản phẩm bị lỗi:',
           'xác suất nó do máy III làm?']
OPTIONS = ['"0,2"', '6/17', '1/3']
CORRECT = 1
ANSWER_VALUE = 6 / 17
BRANCHES = [('I', CYAN, '"0,5"', [('L', CORAL, '"0,01"', [])]),
            ('II', PURPLE, '"0,3"', [('L', CORAL, '"0,02"', [])]),
            ('III', GOLD, '"0,2"', [('L', CORAL, '"0,03"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Ba máy cùng sản xuất: máy một làm năm mươi phần trăm sản phẩm, lỗi một phần trăm; máy hai ba mươi phần trăm, '
                         'lỗi hai phần trăm; máy ba hai mươi phần trăm, lỗi ba phần trăm. Một sản phẩm lỗi bị phát hiện. '
                         'Xác suất nó do máy ba làm ra?'),
    Beat('guess', 'hook', 'Không phẩy hai, sáu phần mười bảy, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây ba nhánh, mỗi nhánh dẫn tới kết quả lỗi. Máy một: không phẩy năm nhân không phẩy không một, '
                        'bằng không phẩy không không năm. Máy hai: không phẩy không không sáu. Máy ba: cũng không phẩy không không sáu.'),
    Beat('s2', 'solve', 'Xác suất toàn phần của lỗi: cộng ba nhánh, được không phẩy không một bảy.'),
    Beat('s3', 'solve', 'Bayes: phần của máy ba trong tổng, không phẩy không không sáu chia không phẩy không một bảy, '
                        'bằng sáu phần mười bảy, khoảng ba mươi lăm phần trăm. Máy làm ít nhất lại gây ra hơn một phần ba số lỗi!'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười bảy. Nhiều nguyên nhân thì vẫn công thức cũ: nhánh cần tìm chia tổng các nhánh.'),
    Beat('outro', 'outro', outro_text(103)),
]

FORMULAS = formulas('6/17', OPTIONS,
                    tot='P(L) = "0,005" + "0,006" + "0,006" = "0,017"',
                    bayes='P("III" | L) = ("0,006")/("0,017") = 6/17')


def validate() -> bool:
    parts = [F(5, 10) * F(1, 100), F(3, 10) * F(2, 100), F(2, 10) * F(3, 100)]
    assert parts == [F(5, 1000), F(6, 1000), F(6, 1000)] and sum(parts) == F(17, 1000)
    assert parts[2] / sum(parts) == F(6, 17)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS103(TreeMixin, ShortScene):
    N = 103

    def hook_visual(self, t0):
        self.board_top = -1.1
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.3), dy=1.8, width=6.6, root_label='sản phẩm')

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('tot', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(self.leaves[2][0].animate.scale(1.35), run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('máy làm ít nhất, gây hơn 1/3 số lỗi', 24, SOFT), anim='fade')

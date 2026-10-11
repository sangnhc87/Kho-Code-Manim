"""XSS068 · Phế phẩm từ đâu ra? — toàn phần: 0,6·0,02 + 0,4·0,05 = 0,032."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN, PURPLE, SOFT  # noqa: E402

EPISODE = {'code': 'XSS068', 'answer': '0,032'}
PROBLEM = ['Xưởng I làm $60%$ sản phẩm ($2%$ lỗi),',
           'xưởng II làm $40%$ ($5%$ lỗi). Xác suất',
           'một sản phẩm bị lỗi?']
OPTIONS = ['"0,035"', '"0,032"', '"0,07"']
CORRECT = 1
ANSWER_VALUE = .032
BRANCHES = [('I', CYAN, '"0,6"', [('L', CORAL, '"0,02"', []), ('T', GREEN, '"0,98"', [])]),
            ('II', PURPLE, '"0,4"', [('L', CORAL, '"0,05"', []), ('T', GREEN, '"0,95"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Một nhà máy có hai xưởng. Xưởng một làm sáu mươi phần trăm sản phẩm, tỉ lệ lỗi hai phần trăm. '
                         'Xưởng hai làm bốn mươi phần trăm, tỉ lệ lỗi năm phần trăm. '
                         'Lấy ngẫu nhiên một sản phẩm, xác suất nó bị lỗi là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy không ba lăm, không phẩy không ba hai, hay không phẩy không bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ cây: nhánh đầu là sản phẩm đến từ xưởng nào, nhánh sau là lỗi hay tốt, '
                        'với xác suất có điều kiện của từng xưởng.'),
    Beat('s2', 'solve', 'Lỗi từ xưởng một: không phẩy sáu nhân không phẩy không hai, bằng không phẩy không một hai. '
                        'Lỗi từ xưởng hai: không phẩy bốn nhân không phẩy không năm, bằng không phẩy không hai.'),
    Beat('s3', 'solve', 'Cộng hai nhánh: không phẩy không ba hai. Đó là công thức xác suất toàn phần. '
                        'Lấy trung bình cộng hai tỉ lệ lỗi là sai, vì hai xưởng làm số lượng khác nhau.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy không ba hai, tức ba phẩy hai phần trăm. Toàn phần: cộng tất cả các nhánh dẫn tới kết quả!'),
    Beat('outro', 'outro', outro_text(68)),
]

FORMULAS = formulas('"0,032"', OPTIONS,
                    one='"0,6" dot "0,02" = "0,012"',
                    two='"0,4" dot "0,05" = "0,02"',
                    tot='P(L) = "0,012" + "0,02" = "0,032"')


def validate() -> bool:
    assert F(6, 10) * F(2, 100) + F(4, 10) * F(5, 100) == F(32, 1000)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS068(TreeMixin, ShortScene):
    N = 68

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='sản phẩm')

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.2))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.2))
        legend = tx('L: lỗi   T: tốt', 24, SOFT).next_to(self.levels[2], DOWN, buff=.2)
        self.play(FadeIn(legend), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('one', 2.0))
        self.wait_until(.5, t0)
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('two', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('trung bình cộng 2 tỉ lệ: SAI', 26, CORAL, bold=True), anim='fade')



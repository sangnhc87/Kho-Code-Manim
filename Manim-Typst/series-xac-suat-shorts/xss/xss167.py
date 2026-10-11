"""XSS167 · Tìm ngược tỉ lệ lỗi — 0,6·0,02 + 0,4·x = 0,03 ⇒ x = 0,045 = 4,5 %."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS167', 'answer': '4,5 %'}
PROBLEM = ['Máy A làm $60%$ sản phẩm, lỗi $2%$; tỉ',
           'lệ lỗi chung của nhà máy là $3%$. Tỉ',
           'lệ lỗi của máy B là bao nhiêu?']
OPTIONS = ['"4" %', '"4,5" %', '"5" %']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('A', CYAN, '"0,6"', [('L', CORAL, '"0,02"', [])]),
            ('B', GOLD, '"0,4"', [('L', CORAL, 'x', [])])]

BEATS = [
    Beat('hook', 'hook', 'Nhà máy có hai máy. Máy A làm sáu mươi phần trăm sản phẩm với tỉ lệ lỗi hai phần trăm. '
                         'Thống kê cho thấy tỉ lệ lỗi chung của nhà máy là ba phần trăm. Máy B có tỉ lệ lỗi bao nhiêu?'),
    Beat('guess', 'hook', 'Bốn phần trăm, bốn phẩy năm phần trăm, hay năm phần trăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bài toán ngược: biết kết quả toàn phần, tìm một xác suất trên nhánh. Vẽ cây như thường, '
                        'đặt ẩn x cho tỉ lệ lỗi của máy B.'),
    Beat('s2', 'solve', 'Công thức toàn phần: không phẩy sáu nhân không phẩy không hai, cộng không phẩy bốn nhân x, bằng không phẩy không ba.'),
    Beat('s3', 'solve', 'Không phẩy không một hai cộng không phẩy bốn x bằng không phẩy không ba, nên x bằng không phẩy không một tám chia không phẩy bốn, '
                        'tức không phẩy không bốn lăm, bốn phẩy năm phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: bốn phẩy năm phần trăm. Dạng tìm tham số rất hay gặp trong đề trả lời ngắn!'),
    Beat('outro', 'outro', outro_text(167)),
]

FORMULAS = formulas('"4,5" %', OPTIONS,
                    eq='"0,6" dot "0,02" + "0,4" dot x = "0,03"',
                    sol='x = ("0,03" - "0,012")/("0,4") = "0,045"')


def validate() -> bool:
    x = (F(3, 100) - F(6, 10) * F(2, 100)) / F(4, 10)
    assert x == F(45, 1000)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS167(TreeMixin, ShortScene):
    N = 167

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=5.6, root_label='sản phẩm')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.play(FadeIn(self.TM('L: lỗi', 22, SOFT).move_to([0, -.9, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        m = self.M('eq', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        m = self.M('sol', 2.0)
        self.write_board(m)
        self.frame(m)

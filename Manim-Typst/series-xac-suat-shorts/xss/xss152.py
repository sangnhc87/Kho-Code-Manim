"""XSS152 · Bia đã bị trúng — P(TT | ít nhất một trúng) = 0,48/0,92 = 12/23."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, SOFT  # noqa: E402
from xss.xss151 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS152', 'answer': '12/23'}
PROBLEM = ['A trúng $"0,8"$, B trúng $"0,6"$, mỗi người',
           'bắn $1$ mũi. Biết bia bị trúng. Xác',
           'suất cả hai cùng trúng?']
OPTIONS = ['"0,48"', '12/23', '2/3']
CORRECT = 1
ANSWER_VALUE = 12 / 23

BEATS = [
    Beat('hook', 'hook', 'Vẫn hai cung thủ: A trúng không phẩy tám, B trúng không phẩy sáu. Lần này bạn chỉ biết: bia đã bị trúng. '
                         'Xác suất cả hai người cùng trúng là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bốn tám, mười hai phần hai mươi ba, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', '"Bia bị trúng" nghĩa là có ít nhất một mũi trúng: chỉ loại đúng một lá, trượt trượt, '
                        'với xác suất không phẩy hai nhân không phẩy bốn bằng không phẩy không tám.'),
    Beat('s2', 'solve', 'Xác suất điều kiện bằng một trừ không phẩy không tám, tức không phẩy chín hai. '
                        'Lá cả hai trúng có xác suất không phẩy tám nhân không phẩy sáu, bằng không phẩy bốn tám.'),
    Beat('s3', 'solve', 'Chia: không phẩy bốn tám chia không phẩy chín hai, bằng mười hai phần hai mươi ba, khoảng năm mươi hai phần trăm. '
                        'Không phẩy bốn tám là bẫy: quên chia cho xác suất của điều kiện.'),
    Beat('answer', 'solve', 'Đáp án: mười hai phần hai mươi ba. Mọi xác suất có điều kiện đều phải chia cho xác suất của điều kiện!'),
    Beat('outro', 'outro', outro_text(152)),
]

FORMULAS = formulas('12/23', OPTIONS,
                    cond='P(B) = 1 - "0,2" dot "0,4" = "0,92"',
                    tt='P(T T) = "0,8" dot "0,6" = "0,48"',
                    prob='P = ("0,48")/("0,92") = 12/23')


def validate() -> bool:
    assert F(48, 100) / (1 - F(8, 100)) == F(12, 23)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS152(TreeMixin, ShortScene):
    N = 152

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='A bắn')
        self.wait_until(.55, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[3][0].animate.set_opacity(.15), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(tx('chỉ loại lá X X', 28, SOFT), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('cond', 1.9))
        self.wait_until(.55, t0)
        self.play(self.leaves[0][0].animate.scale(1.35), run_time=self.rt(.05))
        self.write_board(self.M('tt', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.TM('$"0,48"$: quên chia cho điều kiện', 26, CORAL, bold=True), anim='fade')

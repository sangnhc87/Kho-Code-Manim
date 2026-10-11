"""XSS095 · Con trai sinh thứ Ba — bảng 14 × 14 (giới tính, thứ): 27 ô thỏa điều kiện, 13 ô hai trai."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import grid  # noqa: E402

EPISODE = {'code': 'XSS095', 'answer': '13/27'}
PROBLEM = ['Gia đình $2$ con, biết có một con',
           'trai sinh vào thứ Ba. Xác suất',
           'cả hai đều là trai?']
OPTIONS = ['1/3', '13/27', '1/2']
CORRECT = 1
ANSWER_VALUE = 13 / 27
KIDS = list(product('TG', range(7)))  # (giới tính, thứ trong tuần), thứ Ba = 1
TUE = ('T', 1)

BEATS = [
    Beat('hook', 'hook', 'Đây là câu đố khiến cả giới toán học tranh luận. Một gia đình có hai con, biết có một con trai '
                         'sinh vào thứ Ba. Xác suất cả hai đều là trai là bao nhiêu? Ngày sinh thì liên quan gì chứ?'),
    Beat('guess', 'hook', 'Một phần ba, mười ba phần hai mươi bảy, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi đứa trẻ có mười bốn khả năng: trai hoặc gái, nhân bảy ngày trong tuần. '
                        'Hai đứa trẻ cho bảng mười bốn nhân mười bốn, một trăm chín mươi sáu ô đồng khả năng.'),
    Beat('s2', 'solve', 'Điều kiện có một con trai sinh thứ Ba: hàng của nó có mười bốn ô, cột của nó có mười bốn ô, '
                        'trừ một ô trùng, còn hai mươi bảy ô.'),
    Beat('s3', 'solve', 'Trong hai mươi bảy ô đó, ô hai con trai nằm ở phần trai của hàng và cột: bảy cộng bảy trừ một, '
                        'bằng mười ba ô. Xác suất bằng mười ba phần hai mươi bảy, rất gần một phần hai!'),
    Beat('answer', 'solve', 'Đáp án: mười ba phần hai mươi bảy. Thông tin càng cụ thể, như ngày sinh, '
                            'càng giúp phân biệt hai đứa trẻ, và đáp án tiến dần về một phần hai.'),
    Beat('outro', 'outro', outro_text(95)),
]

FORMULAS = formulas('13/27', OPTIONS,
                    cond='n(B) = 14 + 14 - 1 = 27',
                    both='n(A B) = 7 + 7 - 1 = 13',
                    prob='P(A|B) = 13/27')


def validate() -> bool:
    space = list(product(KIDS, repeat=2))
    cond = [w for w in space if TUE in w]
    assert len(space) == 196 and len(cond) == 27
    assert F(sum(a[0] == b[0] == 'T' for a, b in cond), len(cond)) == F(13, 27)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS095(ShortScene):
    N = 95

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.g = grid(14, 14, .31).move_to([.15, .95, 0])
        heads = [tx('trai', 18, CYAN).next_to(self.g.cells[0][3], [0, 1, 0], buff=.1),
                 tx('gái', 18, CORAL).next_to(self.g.cells[0][10], [0, 1, 0], buff=.1),
                 tx('trai', 18, CYAN).rotate(1.5708).next_to(self.g.cells[3][0], [-1, 0, 0], buff=.1),
                 tx('gái', 18, CORAL).rotate(1.5708).next_to(self.g.cells[10][0], [-1, 0, 0], buff=.1)]
        self.heads = heads

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.g, lag_ratio=.002), *[FadeIn(h) for h in self.heads], run_time=self.rt(.3))
        self.wait_until(.6, t0)
        self.write_board(self.TM('$14 times 14 = 196$ ô', 32, SOFT, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        k = 1  # thứ Ba trong nửa "trai"
        cells = {(k, j) for j in range(14)} | {(i, k) for i in range(14)}
        self.play(*[self.g.cells[i][j].animate.set_fill(CYAN, .5) for i, j in cells], run_time=self.rt(.12))
        self.cells = cells
        self.wait_until(.6, t0)
        self.write_board(self.M('cond', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        both = {(i, j) for i, j in self.cells if i < 7 and j < 7}
        self.play(*[self.g.cells[i][j].animate.set_fill(GOLD, .9) for i, j in both], run_time=self.rt(.1))
        self.write_board(self.M('both', 2.0))
        self.wait_until(.55, t0)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

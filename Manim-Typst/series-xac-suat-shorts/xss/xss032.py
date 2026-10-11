"""XSS032 · Lần sau lớn hơn — 6 ô hòa, 30 ô chia đôi: 15/36 = 5/12 (đối xứng)."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS032', 'answer': '5/12'}
PROBLEM = ['Gieo xúc xắc hai lần.', 'Xác suất lần thứ hai lớn hơn lần thứ nhất?']
OPTIONS = ['1/2', '5/12', '1/3']
CORRECT = 1
ANSWER_VALUE = 5 / 12

BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc hai lần. Xác suất lần thứ hai ra số lớn hơn lần thứ nhất là bao nhiêu? '
                         'Lớn hơn hay nhỏ hơn, hai bên công bằng, vậy là một phần hai?'),
    Beat('guess', 'hook', 'Một phần hai, năm phần mười hai, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bảng sáu nhân sáu có ba mươi sáu ô. Sáu ô trên đường chéo là hai lần bằng nhau: '
                        'đây là chỗ một phần hai bị sai.'),
    Beat('s2', 'solve', 'Còn lại ba mươi ô chia đều hai phía của đường chéo nhờ tính đối xứng: '
                        'mười lăm ô lần hai lớn hơn, mười lăm ô lần hai nhỏ hơn.'),
    Beat('s3', 'solve', 'Xác suất bằng mười lăm phần ba mươi sáu, rút gọn còn năm phần mười hai, '
                        'nhỏ hơn một phần hai một chút vì phải nhường phần cho trường hợp hòa.'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười hai. Đừng quên trường hợp bằng nhau!'),
    Beat('outro', 'outro', outro_text(32)),
]

FORMULAS = formulas('5/12', OPTIONS, half='(36 - 6)/2 = 15', prob='P = 15/36 = 5/12')


def validate() -> bool:
    space = list(product(range(1, 7), repeat=2))
    assert Fraction(sum(b > a for a, b in space), 36) == Fraction(5, 12)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS032(DiceGridMixin, ShortScene):
    N = 32

    def hook_visual(self, t0):
        self.d1 = die(2, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(5, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.04))
        self.remove(self.d1, self.d2)
        self.show_grid(.3)
        self.wait_until(.5, t0)
        self.play(*[self.g.cells[i][i].animate.set_fill(SOFT, .6) for i in range(6)], run_time=self.rt(.1))
        self.write_board(tx('6 ô hòa', 30, SOFT, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        above = [self.g.cells[j][i] for i in range(6) for j in range(6) if j > i]
        below = [self.g.cells[j][i] for i in range(6) for j in range(6) if j < i]
        self.play(*[c.animate.set_fill(GOLD, .55) for c in above], run_time=self.rt(.1))
        self.wait_until(.45, t0)
        self.play(*[c.animate.set_fill(CYAN, .4) for c in below], run_time=self.rt(.1))
        self.write_board(self.M('half', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(tx('nhường phần cho trường hợp hòa', 26, SOFT), anim='fade')

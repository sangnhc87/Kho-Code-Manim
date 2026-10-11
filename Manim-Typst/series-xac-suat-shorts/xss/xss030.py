"""XSS030 · Ít nhất một con 6 — hàng 6 và cột 6 của bảng: 11 ô (không phải 12!) → 11/36."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS030', 'answer': '11/36'}
PROBLEM = ['Gieo hai con xúc xắc.', 'Xác suất có ít nhất một mặt $6$?']
OPTIONS = ['1/3', '11/36', '1/36']
CORRECT = 1
ANSWER_VALUE = 11 / 36

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc. Xác suất có ít nhất một mặt sáu là bao nhiêu? '
                         'Mỗi con một phần sáu, cộng lại là một phần ba, đúng không?'),
    Beat('guess', 'hook', 'Một phần ba, mười một phần ba mươi sáu, hay một phần ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tô các ô có con thứ nhất ra sáu: một cột sáu ô. Tô các ô có con thứ hai ra sáu: một hàng sáu ô.'),
    Beat('s2', 'solve', 'Nhưng ô sáu sáu nằm ở cả hàng lẫn cột, bị đếm hai lần! Số ô thực sự là sáu cộng sáu trừ một, '
                        'bằng mười một ô.'),
    Beat('s3', 'solve', 'Xác suất bằng mười một phần ba mươi sáu. Kiểm tra bằng biến cố đối: không có mặt sáu nào '
                        'là năm nhân năm bằng hai mươi lăm ô, và một trừ hai mươi lăm phần ba mươi sáu đúng bằng '
                        'mười một phần ba mươi sáu.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần ba mươi sáu. Cộng xác suất mà quên phần chung là bẫy kinh điển!'),
    Beat('outro', 'outro', outro_text(30)),
]

FORMULAS = formulas('11/36', OPTIONS,
                    count='6 + 6 - 1 = 11',
                    prob='P = 11/36',
                    comp='1 - 25/36 = 11/36')


def validate() -> bool:
    space = list(product(range(1, 7), repeat=2))
    assert Fraction(sum(6 in w for w in space), 36) == Fraction(11, 36) == 1 - Fraction(25, 36)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS030(DiceGridMixin, ShortScene):
    N = 30

    def hook_visual(self, t0):
        self.d1 = die(6, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(2, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.04))
        self.remove(self.d1, self.d2)
        self.show_grid(.25)
        self.play(*[self.g.cells[j][5].animate.set_fill(GOLD, .5) for j in range(6)], run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(*[self.g.cells[5][i].animate.set_fill(CYAN, .5) for i in range(6)], run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.g.cells[5][5].animate.set_fill(CORAL, .9).scale(1.15), run_time=self.rt(.08))
        self.write_board(tx('ô (6; 6) bị đếm 2 lần!', 30, CORAL, bold=True), anim='fade')
        self.wait_until(.55, t0)
        self.write_board(self.M('count', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.45, t0)
        self.write_board(self.M('comp', 1.8), anim='fade')

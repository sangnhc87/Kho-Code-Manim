"""XSS079 · Độc lập bất ngờ — A: lần 1 chẵn, B: tổng chẵn; P(AB) = 9/36 = 1/2 · 1/2 → độc lập."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS079', 'answer': 'Có'}
PROBLEM = ['Gieo hai xúc xắc. $A$: con thứ nhất',
           'ra số chẵn; $B$: tổng là số chẵn.',
           '$A$ và $B$ có độc lập?']
OPTIONS = ['"Có"', '"Không"', '"Không đủ dữ kiện"']
CORRECT = 0
ANSWER_VALUE = None
SPACE = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc. A là con thứ nhất ra số chẵn, B là tổng hai con là số chẵn. '
                         'Tổng phụ thuộc vào con thứ nhất, vậy A và B chắc chắn phụ thuộc nhau? Hãy kiểm tra!'),
    Beat('guess', 'hook', 'Có độc lập, không độc lập, hay không đủ dữ kiện? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trên bảng sáu nhân sáu, A gồm ba cột chẵn: mười tám ô, xác suất một phần hai. '
                        'B gồm các ô có tổng chẵn, xếp như bàn cờ: cũng mười tám ô, xác suất một phần hai.'),
    Beat('s2', 'solve', 'A giao B: con thứ nhất chẵn và tổng chẵn, tức cả hai con cùng chẵn: chín ô, '
                        'xác suất chín phần ba mươi sáu bằng một phần tư.'),
    Beat('s3', 'solve', 'Một phần tư đúng bằng một phần hai nhân một phần hai. Vậy A và B độc lập! '
                        'Biết con thứ nhất chẵn không làm thay đổi cơ hội tổng chẵn, vì con thứ hai vẫn chẵn lẻ như nhau.'),
    Beat('answer', 'solve', 'Đáp án: có, độc lập. Độc lập phải kiểm tra bằng con số, đừng chỉ dựa vào cảm giác!'),
    Beat('outro', 'outro', outro_text(79)),
]

FORMULAS = formulas('"Có"', OPTIONS,
                    pa='P(A) = P(B) = 18/36 = 1/2',
                    pab='P(A B) = 9/36 = 1/4',
                    chk='P(A B) = 1/2 dot 1/2 = P(A) dot P(B)')


def validate() -> bool:
    pa = F(sum(a % 2 == 0 for a, b in SPACE), 36)
    pb = F(sum((a + b) % 2 == 0 for a, b in SPACE), 36)
    pab = F(sum(a % 2 == 0 and (a + b) % 2 == 0 for a, b in SPACE), 36)
    assert pa == pb == F(1, 2) and pab == F(1, 4) == pa * pb
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS079(DiceGridMixin, ShortScene):
    N = 79

    def hook_visual(self, t0):
        self.d1 = die(4, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(2, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.03))
        self.remove(self.d1, self.d2)
        self.show_grid(.2)
        self.play(*[self.g.cells[j][i].animate.set_stroke(CYAN, 5) for i in (1, 3, 5) for j in range(6)],
                  run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.play(*[self.g.cells[j][i].animate.set_fill(CORAL, .35) for i in range(6) for j in range(6) if (i + j) % 2 == 0],
                  run_time=self.rt(.08))
        self.write_board(self.M('pa', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[self.g.cells[j][i].animate.set_fill(GOLD, .85) for i in (1, 3, 5) for j in (1, 3, 5)],
                  run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.write_board(self.M('pab', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('chk', 1.7)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('độc lập!', 34, GOLD, bold=True), anim='fade')

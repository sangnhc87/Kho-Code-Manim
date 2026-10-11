"""XSS058 · Xung khắc có độc lập? — Không: P(AB) = 0 ≠ P(A)·P(B) > 0."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import die_row, venn  # noqa: E402

EPISODE = {'code': 'XSS058', 'answer': 'Không'}
PROBLEM = ['$A$, $B$ xung khắc và cùng có xác suất',
           'dương. $A$ và $B$ có độc lập không?']
OPTIONS = ['"Có"', '"Không"', '"Tùy bài"']
CORRECT = 1
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Hai biến cố xung khắc, tức không thể cùng xảy ra, và đều có xác suất dương. '
                         'Chúng có độc lập không? Rất nhiều bạn nhầm hai khái niệm này!'),
    Beat('guess', 'hook', 'Có, không, hay tùy bài? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ví dụ gieo xúc xắc: A là ra mặt một, B là ra mặt hai. Hai biến cố xung khắc: '
                        'trên biểu đồ Venn, hai vòng tròn tách rời nhau.'),
    Beat('s2', 'solve', 'Xung khắc nghĩa là xác suất A giao B bằng không. Nhưng xác suất A nhân xác suất B bằng '
                        'một phần sáu nhân một phần sáu, lớn hơn không. Hai vế khác nhau, nên không độc lập.'),
    Beat('s3', 'solve', 'Hiểu bằng trực giác: nếu biết A đã xảy ra, ta chắc chắn B không xảy ra. '
                        'Biết A làm thay đổi hẳn khả năng của B, đó là phụ thuộc chặt nhất có thể!'),
    Beat('answer', 'solve', 'Đáp án: không. Xung khắc là không thể cùng xảy ra, độc lập là không ảnh hưởng nhau. '
                            'Hai khái niệm gần như trái ngược!'),
    Beat('outro', 'outro', outro_text(58)),
]

FORMULAS = formulas('"Không"', OPTIONS,
                    excl='P(A B) = 0',
                    prod='P(A) dot P(B) = 1/6 dot 1/6 = 1/36 > 0',
                    neq='P(A B) != P(A) dot P(B)')


def validate() -> bool:
    pa = F(sum(v == 1 for v in range(1, 7)), 6)
    pb = F(sum(v == 2 for v in range(1, 7)), 6)
    pab = F(sum(v == 1 and v == 2 for v in range(1, 7)), 6)
    assert pab == 0 and pa * pb == F(1, 36) and pab != pa * pb
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS058(ShortScene):
    N = 58

    def hook_visual(self, t0):
        self.v = venn(1.05, 2.9, CYAN, CORAL, (0, 1.3))
        labs = VGroup(self.TM('$A$', 36, CYAN, bold=True).move_to(self.v.a), self.TM('$B$', 36, CORAL, bold=True)
                      .move_to(self.v.b))
        self.labs = labs
        self.wait_until(.45, t0)
        self.play(FadeIn(self.v), FadeIn(labs), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        row = die_row((1, 2), .8)
        self.play(FadeIn(row[0].move_to(self.v.a.get_center() + [0, -.5, 0])),
                  FadeIn(row[1].move_to(self.v.b.get_center() + [0, -.5, 0])),
                  self.labs.animate.shift([0, .5, 0]), run_time=self.rt(.1))
        self.wait_until(.55, t0)
        self.play(FadeIn(tx('tách rời: xung khắc', 30, GOLD, bold=True).next_to(self.v, DOWN, buff=.25)),
                  run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('excl', 2.0))
        self.wait_until(.4, t0)
        self.write_board(self.M('prod', 1.7))
        self.wait_until(.75, t0)
        m = self.M('neq', 1.9)
        self.write_board(m)
        self.frame(m, CORAL)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(tx('biết A xảy ra ⇒ B chắc chắn không', 28, CORAL, bold=True), anim='fade')
        self.wait_until(.55, t0)
        self.write_board(tx('xung khắc ≠ độc lập', 34, GOLD, bold=True), anim='fade')



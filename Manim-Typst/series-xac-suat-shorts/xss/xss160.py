"""XSS160 · Hai nhân chứng — cả hai nói "có": (1/2·3/4·4/5)/(… + 1/2·1/4·1/5) = 12/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS160', 'answer': '12/13'}
PROBLEM = ['Sự kiện xảy ra với xác suất $50%$. A nói thật $75%$,',
           'B nói thật $80%$; cả hai cùng nói "có".', 'Xác suất sự kiện thật sự đã xảy ra?']
OPTIONS = ['3/5', '12/13', '4/5']
CORRECT = 1
ANSWER_VALUE = 12 / 13
BRANCHES = [('Có', GREEN, '1/2', [('cc', GREEN, '3/4 dot 4/5', []), ('khác', SOFT, '2/5', [])]),
            ('Ko', CORAL, '1/2', [('cc', GREEN, '1/4 dot 1/5', []), ('khác', SOFT, '19/20', [])])]

BEATS = [
    Beat('hook', 'hook', 'Một sự kiện có thể đã xảy ra hoặc không, mỗi khả năng một phần hai. Nhân chứng A nói thật với xác suất ba phần tư, '
                         'B nói thật bốn phần năm, độc lập. Cả hai cùng nói "có". Xác suất sự kiện thật sự đã xảy ra?'),
    Beat('guess', 'hook', 'Ba phần năm, mười hai phần mười ba, hay bốn phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một là sự thật: có hoặc không. Nếu thật sự có, cả hai cùng nói "có" khi cả hai nói thật: '
                        'ba phần tư nhân bốn phần năm. Nếu không có, cả hai cùng nói "có" khi cả hai nói dối: một phần tư nhân một phần năm.'),
    Beat('s2', 'solve', 'Hai lá phù hợp: một phần hai nhân mười hai phần hai mươi, và một phần hai nhân một phần hai mươi. '
                        'Tỉ lệ giữa chúng là mười hai so với một.'),
    Beat('s3', 'solve', 'Xác suất thật sự có bằng mười hai phần mười ba, khoảng chín mươi hai phần trăm, cao hơn độ tin cậy của từng nhân chứng!'),
    Beat('answer', 'solve', 'Đáp án: mười hai phần mười ba. Hai lời khai độc lập cùng khớp nhau có sức nặng hơn hẳn từng lời khai riêng!'),
    Beat('outro', 'outro', outro_text(160)),
]

FORMULAS = formulas('12/13', OPTIONS,
                    yes='1/2 dot 3/4 dot 4/5 = 12/40',
                    no='1/2 dot 1/4 dot 1/5 = 1/40',
                    prob='P("có" | "cả hai nói có") = 12/(12 + 1) = 12/13')


def validate() -> bool:
    a = F(1, 2) * F(3, 4) * F(4, 5)
    b = F(1, 2) * F(1, 4) * F(1, 5)
    assert a / (a + b) == F(12, 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS160(TreeMixin, ShortScene):
    N = 160

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='sự thật',
                                                  edge_size=26)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('cc: cả hai nói "có"', 24, SOFT).move_to([0, -1.2, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        cc = [n for n, path in self.leaves if path[-1][0] == 'cc']
        other = [n for n, path in self.leaves if path[-1][0] != 'cc']
        self.play(*[n.animate.set_opacity(.15) for n in other], *[n.animate.scale(1.3) for n in cc], run_time=self.rt(.06))
        self.write_board(self.M('yes', 1.9))
        self.wait_until(.45, t0)
        self.write_board(self.M('no', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

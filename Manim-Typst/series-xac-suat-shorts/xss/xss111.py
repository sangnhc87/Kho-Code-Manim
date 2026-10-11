"""XSS111 · Kiểm phiếu — A 3 phiếu, B 2 phiếu: A luôn dẫn trước ở 2/10 thứ tự kiểm = 1/5 = (3 − 2)/(3 + 2)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS111', 'answer': '1/5'}
PROBLEM = ['A được $3$ phiếu, B được $2$ phiếu, kiểm',
           'ngẫu nhiên từng phiếu.',
           '$P("A luôn dẫn trước suốt quá trình")$?']
OPTIONS = ['3/5', '1/5', '2/5']
CORRECT = 1
ANSWER_VALUE = .2
ORDERS = sorted(set(permutations('AAABB')))


def always_ahead(o):
    return all(o[:k].count('A') > o[:k].count('B') for k in range(1, len(o) + 1))


BEATS = [
    Beat('hook', 'hook', 'Cuộc bầu cử có năm phiếu: A được ba phiếu, B được hai phiếu. Kiểm phiếu từng lá theo thứ tự ngẫu nhiên. '
                         'Xác suất A luôn dẫn trước B trong suốt quá trình kiểm là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần năm, một phần năm, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Năm lá phiếu gồm ba A và hai B có tổ hợp chập hai của năm, bằng mười thứ tự kiểm khác nhau, '
                        'đồng khả năng. Liệt kê cả mười.'),
    Beat('s2', 'solve', 'A luôn dẫn trước nghĩa là phiếu đầu tiên phải là A, và sau mỗi lá, số phiếu A luôn nhiều hơn B. '
                        'Kiểm từng dãy: chỉ có hai dãy thỏa mãn, A A A B B và A A B A B.'),
    Beat('s3', 'solve', 'Xác suất bằng hai phần mười, tức một phần năm. Định lý kiểm phiếu cho công thức đẹp: '
                        'hiệu số phiếu chia tổng số phiếu, ba trừ hai chia năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Thắng chung cuộc chưa chắc đã dẫn trước suốt cuộc đua!'),
    Beat('outro', 'outro', outro_text(111)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    n='n(Omega) = C_5^2 = 10',
                    prob='P = 2/10 = 1/5',
                    thm='P = (a - b)/(a + b) = (3 - 2)/(3 + 2) = 1/5')


def validate() -> bool:
    assert len(ORDERS) == 10 and F(sum(map(always_ahead, ORDERS)), 10) == F(1, 5) == F(3 - 2, 3 + 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS111(ShortScene):
    N = 111

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.rows = VGroup(*[VGroup(*[token(ch, CYAN if ch == 'A' else CORAL, .21) for ch in o]).arrange(buff=.06)
                             for o in ORDERS]).arrange_in_grid(5, 2, buff=(.8, .2)).move_to([0, 1.3, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.rows[0], lag_ratio=.2), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows[1:], lag_ratio=.1), run_time=self.rt(.3))
        self.wait_until(.6, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.35, t0)
        self.play(*[r.animate.set_opacity(.2) for r, o in zip(self.rows, ORDERS) if not always_ahead(o)],
                  *[r.animate.scale(1.2) for r, o in zip(self.rows, ORDERS) if always_ahead(o)], run_time=self.rt(.12))
        self.write_board(tx('chỉ 2 thứ tự thỏa mãn', 30, GOLD, bold=True), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(self.M('thm', 1.6), anim='fade')



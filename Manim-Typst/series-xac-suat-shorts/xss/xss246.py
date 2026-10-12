"""XSS246 · Ba phát trúng liên tiếp — biết đúng 3/5 phát trúng: mọi vị trí như nhau, 3 khối liền / C(5,3) = 3/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS246', 'answer': '3/10'}
PROBLEM = ['Bắn $5$ phát (mỗi phát trúng $"0,6"$),',
           'biết trúng đúng $3$ phát. Xác suất',
           '$3$ phát trúng liên tiếp nhau?']
OPTIONS = ['"0,216"', '3/10', '1/2']
CORRECT = 1
ANSWER_VALUE = .3
SEQS = [''.join(w) for w in product('TX', repeat=5) if w.count('T') == 3]

BEATS = [
    Beat('hook', 'hook', 'Xạ thủ bắn năm phát, mỗi phát trúng không phẩy sáu. Biết bạn ấy trúng đúng ba phát. '
                         'Xác suất ba phát trúng nằm liền nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy hai một sáu, ba phần mười, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết trúng đúng ba phát, mọi dãy có ba trúng hai trượt đều có cùng xác suất không phẩy sáu mũ ba nhân không phẩy bốn bình phương. '
                        'Vậy chúng đồng khả năng, và xác suất trúng không phẩy sáu không còn quan trọng.'),
    Beat('s2', 'solve', 'Có tổ hợp chập ba của năm, mười dãy. Ba phát trúng liền nhau: vị trí một hai ba, hai ba bốn, ba bốn năm: ba dãy.'),
    Beat('s3', 'solve', 'Xác suất ba phần mười. Điều kiện về tổng số lần trúng đã xóa sạch ảnh hưởng của p.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười. Biết tổng số thành công thì mọi cách sắp xếp đều đồng khả năng!'),
    Beat('outro', 'outro', outro_text(246)),
]

FORMULAS = formulas('3/10', OPTIONS,
                    same='P(T T T X X) = P(T X T X T) = dots = "0,6"^3 dot "0,4"^2',
                    prob='P = 3/(C_5^3) = 3/10')


def validate() -> bool:
    w = {s: F(3, 5) ** 3 * F(2, 5) ** 2 for s in SEQS}
    assert F(sum(v for s, v in w.items() if 'TTT' in s), sum(w.values())) == F(3, 10)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS246(ShortScene):
    N = 246

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.rows = VGroup(*[VGroup(*[token(c, GREEN if c == 'T' else CORAL, .2, 16) for c in s]).arrange(buff=.05) for s in SEQS]) \
            .arrange_in_grid(5, 2, buff=(.8, .18)).move_to([0, 1.3, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.rows, lag_ratio=.08), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        self.write_board(self.M('same', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.4, t0)
        good = [r for r, s in zip(self.rows, SEQS) if 'TTT' in s]
        self.play(*[r.animate.scale(1.25) for r in good], *[c[0].animate.set_stroke(GOLD, 3) for r in good for c in r],
                  run_time=self.rt(.06))

    def beat_s3(self, T):
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

"""XSS158 · Biết có đúng 3 ngửa — 10 dãy, 6 dãy bắt đầu bằng N: 3/5 (mỗi vị trí như nhau)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, GREEN  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS158', 'answer': '3/5'}
PROBLEM = ['Tung đồng xu $5$ lần, biết có',
           'đúng $3$ lần ngửa. Xác suất lần',
           'tung đầu tiên ra ngửa?']
OPTIONS = ['1/2', '3/5', '3/10']
CORRECT = 1
ANSWER_VALUE = .6
SEQS = [''.join(w) for w in product('NS', repeat=5) if w.count('N') == 3]

BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu năm lần. Bạn được biết có đúng ba lần ngửa. Xác suất lần tung đầu tiên ra ngửa là bao nhiêu? '
                         'Đồng xu không có trí nhớ, vậy chắc là một phần hai?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần năm, hay ba phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết đúng ba ngửa, ta chỉ còn mười dãy, bằng tổ hợp chập ba của năm, và chúng đồng khả năng.'),
    Beat('s2', 'solve', 'Dãy bắt đầu bằng ngửa: hai lần ngửa còn lại xếp vào bốn vị trí sau, tổ hợp chập hai của bốn bằng sáu dãy.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần mười, tức ba phần năm. Trực giác đẹp: ba lần ngửa rải đều trên năm vị trí, '
                        'mỗi vị trí có cơ hội ba phần năm.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Đồng xu không có trí nhớ, nhưng thông tin về tổng số ngửa thì có!'),
    Beat('outro', 'outro', outro_text(158)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    nb='n(B) = C_5^3 = 10',
                    nab='n(A sect B) = C_4^2 = 6',
                    prob='P(A | B) = 6/10 = 3/5')


def validate() -> bool:
    assert len(SEQS) == 10 and F(sum(s[0] == 'N' for s in SEQS), 10) == F(3, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS158(ShortScene):
    N = 158

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.rows = VGroup(*[VGroup(*[coin(c, .23) for c in s]).arrange(buff=.05) for s in SEQS]) \
            .arrange_in_grid(5, 2, buff=(.7, .18)).move_to([0, 1.2, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.rows[:2], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.rows[2:], lag_ratio=.1), run_time=self.rt(.2))
        self.wait_until(.55, t0)
        self.write_board(self.M('nb', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        first = [r for r, s in zip(self.rows, SEQS) if s[0] == 'N']
        self.play(*[r[0][0].animate.set_stroke(GREEN, 6) for r in first], *[r.animate.scale(1.1) for r in first],
                  run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.write_board(self.M('nab', 2.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m, GOLD)

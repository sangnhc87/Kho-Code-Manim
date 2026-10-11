"""XSS128 · Không hai ngửa liền nhau — đếm bằng quy hoạch động a_n = a_(n−1) + a_(n−2): 2, 3, 5, 8; 8/16 = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS128', 'answer': '1/2'}
PROBLEM = ['Tung đồng xu $4$ lần. Xác suất không có', 'hai lần ngửa liên tiếp?']
OPTIONS = ['1/2', '5/16', '3/8']
CORRECT = 0
ANSWER_VALUE = .5
SEQS = [''.join(w) for w in product('SN', repeat=4)]

BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu bốn lần. Xác suất không có hai lần ngửa nào đứng liền nhau là bao nhiêu? '
                         'Có mười sáu dãy, nhưng ta sẽ đếm bằng một mẹo dùng được cho cả trăm lần tung.'),
    Beat('guess', 'hook', 'Một phần hai, năm phần mười sáu, hay ba phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Liệt kê mười sáu dãy và gạch những dãy có hai ngửa liền nhau. Còn lại tám dãy tốt. '
                        'Nhưng nếu tung mười lần, liệt kê sẽ quá dài.'),
    Beat('s2', 'solve', 'Quy hoạch động: gọi a n là số dãy tốt độ dài n. Dãy tốt kết thúc bằng sấp thì phía trước là dãy tốt độ dài '
                        'n trừ một; kết thúc bằng ngửa thì trước nó buộc là sấp, phía trước là dãy tốt độ dài n trừ hai.'),
    Beat('s3', 'solve', 'Vậy a n bằng a n trừ một cộng a n trừ hai: hai, ba, năm, tám, dãy Fibonacci! '
                        'Xác suất bằng tám phần mười sáu, tức một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Gặp điều kiện "không liền nhau", hãy nghĩ ngay tới quy hoạch động và Fibonacci!'),
    Beat('outro', 'outro', outro_text(128)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    rec='a_n = a_(n-1) + a_(n-2)',
                    vals='a_1 = 2, quad a_2 = 3, quad a_3 = 5, quad a_4 = 8',
                    prob='P = 8/16 = 1/2')


def validate() -> bool:
    good = [s for s in SEQS if 'NN' not in s]
    counts = [sum('NN' not in ''.join(w) for w in product('SN', repeat=n)) for n in range(1, 5)]
    assert counts == [2, 3, 5, 8] and F(len(good), 16) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS128(ShortScene):
    N = 128

    def hook_visual(self, t0):
        self.board_top = -1.35
        self.rows = VGroup(*[VGroup(*[coin(c, .2) for c in s]).arrange(buff=.04) for s in SEQS]) \
            .arrange_in_grid(4, 4, buff=(.35, .18))
        self.rows.scale_to_fit_width(min(self.rows.width, 7.2)).move_to([0, 1.3, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.rows, lag_ratio=.04), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        bad = [r for r, s in zip(self.rows, SEQS) if 'NN' in s]
        self.wait_until(.25, t0)
        self.play(*[r.animate.set_opacity(.18) for r in bad], run_time=self.rt(.1))
        good = [r for r, s in zip(self.rows, SEQS) if 'NN' not in s]
        self.play(*[r.animate.scale(1.1) for r in good], run_time=self.rt(.05))
        self.write_board(self.TM('còn lại $8$ dãy tốt', 30, GOLD, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.45, t0)
        m = self.M('rec', 2.2)
        self.write_board(m)
        self.frame(m, CORAL)

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('vals', 1.8))
        self.wait_until(.6, t0)
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

"""XSS306 · Không ba ngửa liền — a_n = a_(n−1) + a_(n−2) + a_(n−3): 2, 4, 7, 13, 24, 44 → 44/64 = 11/16."""
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

EPISODE = {'code': 'XSS306', 'answer': '11/16'}
PROBLEM = ['Tung đồng xu $6$ lần. Xác suất không',
           'có $3$ lần ngửa liên tiếp?']
OPTIONS = ['1/2', '11/16', '13/16']
CORRECT = 1
ANSWER_VALUE = 11 / 16


def count(n):
    return sum('NNN' not in ''.join(w) for w in product('SN', repeat=n))


BEATS = [
    Beat('hook', 'hook', 'Tung một đồng xu sáu lần. Xác suất không có ba lần ngửa nào liên tiếp là bao nhiêu? '
                         'Sáu mươi tư dãy, liệt kê thì mệt, ta dùng quy hoạch động.'),
    Beat('guess', 'hook', 'Một phần hai, mười một phần mười sáu, hay mười ba phần mười sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dãy tốt kết thúc bằng một trong ba đuôi: sấp, sấp ngửa, hoặc sấp ngửa ngửa. Phần đứng trước mỗi đuôi là một dãy tốt ngắn hơn.'),
    Beat('s2', 'solve', 'Vậy a n bằng a n trừ một cộng a n trừ hai cộng a n trừ ba. Bắt đầu a một bằng hai, a hai bằng bốn, a ba bằng bảy; '
                        'tiếp theo mười ba, hai mươi tư, bốn mươi tư.'),
    Beat('s3', 'solve', 'Xác suất bốn mươi tư phần sáu mươi tư, tức mười một phần mười sáu. Nghĩa là gần một phần ba số lần sẽ có chuỗi ba ngửa!'),
    Beat('answer', 'solve', 'Đáp án: mười một phần mười sáu. "Không có k liên tiếp": phân loại theo đuôi, được truy hồi k số hạng!'),
    Beat('outro', 'outro', outro_text(306)),
]

FORMULAS = formulas('11/16', OPTIONS,
                    rec='a_n = a_(n-1) + a_(n-2) + a_(n-3)',
                    vals='2, quad 4, quad 7, quad 13, quad 24, quad 44',
                    prob='P = 44/64 = 11/16')


def validate() -> bool:
    assert [count(n) for n in range(1, 7)] == [2, 4, 7, 13, 24, 44]
    assert F(count(6), 64) == F(11, 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS306(ShortScene):
    N = 306

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.tails = VGroup(VGroup(coin('S', .3)), VGroup(coin('S', .3), coin('N', .3)), VGroup(coin('S', .3), coin('N', .3), coin('N', .3)))
        for t in self.tails:
            t.arrange(buff=.06)
        self.tails.arrange([0, -1, 0], buff=.3, aligned_edge=[1, 0, 0]).move_to([.8, 1.6, 0])
        self.boxes = VGroup(*[self.TM(f'$a_(n-{k})$', 28, GOLD).next_to(t, [-1, 0, 0], buff=.3) for k, t in zip((1, 2, 3), self.tails)])
        self.wait_until(.6, t0)
        self.play(FadeIn(VGroup(coin('N', .3), coin('N', .3), coin('N', .3)).arrange(buff=.06).move_to([0, 2.6, 0]).set_opacity(.5)),
                  run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.tails, lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.boxes, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('rec', 1.8))
        self.wait_until(.5, t0)
        self.write_board(self.M('vals', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m, CORAL)

"""XSS309 · Rắn và thang mini — ô 0 → 4, ngửa +1, sấp +2, ô 3 có rắn đẩy về ô 1: E_1 = 6, E_2 = 4, E_0 = 6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, UP, CurvedArrow, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS309', 'answer': '6'}
PROBLEM = ['Đi từ ô $0$ tới ô $4$: ngửa tiến $1$, sấp',
           'tiến $2$; đáp ô $3$ thì bị rắn đẩy về ô $1$.',
           'Trung bình mấy lượt về đích?']
OPTIONS = ['5', '6', '8']
CORRECT = 1
ANSWER_VALUE = 6


def expected():
    e1, e2 = F(6), F(4)  # E2 = 1 + E1/2,  E1 = 1 + E1/2 + E2/2
    assert e2 == 1 + e1 / 2 and e1 == 1 + e1 / 2 + e2 / 2
    return 1 + e1 / 2 + e2 / 2, e1, e2


BEATS = [
    Beat('hook', 'hook', 'Một bàn rắn và thang mini: đi từ ô không tới ô bốn. Tung xu, ngửa tiến một ô, sấp tiến hai ô. '
                         'Nhưng ô ba có con rắn, đáp vào là bị đẩy về ô một. Trung bình mấy lượt mới về đích?'),
    Beat('guess', 'hook', 'Năm lượt, sáu lượt, hay tám lượt? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi E k là số lượt trung bình còn lại khi đứng ở ô k. Ô ba không bao giờ đứng được, vì rắn đẩy về ô một ngay.'),
    Beat('s2', 'solve', 'Từ ô hai: sấp thì về đích, ngửa thì vào ô ba rồi bị đẩy về ô một. Vậy E hai bằng một cộng nửa E một.'),
    Beat('s3', 'solve', 'Từ ô một: ngửa sang ô hai, sấp vào ô ba rồi quay lại chính ô một. E một bằng một cộng nửa E một cộng nửa E hai. '
                        'Giải ra E một bằng sáu, E hai bằng bốn.'),
    Beat('s4', 'solve', 'Từ ô xuất phát: ngửa tới ô một, sấp tới ô hai. E không bằng một cộng nửa của sáu cộng nửa của bốn, đúng bằng sáu.'),
    Beat('answer', 'solve', 'Đáp án: sáu lượt. Con rắn biến bàn cờ thành vòng lặp, và hệ phương trình kỳ vọng gỡ vòng lặp đó.'),
    Beat('outro', 'outro', outro_text(309)),
]

FORMULAS = formulas('6', OPTIONS,
                    e2='E_2 = 1 + 1/2 E_1',
                    e1='E_1 = 1 + 1/2 E_1 + 1/2 E_2',
                    sol='E_1 = 6, quad E_2 = 4',
                    e0='E_0 = 1 + 1/2 dot 6 + 1/2 dot 4 = 6')


def validate() -> bool:
    e0, e1, e2 = expected()
    assert (e0, e1, e2) == (6, 6, 4)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS309(ShortScene):
    N = 309

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.row = pads(list('01234'), y=1.0, gap=1.4)
        self.nums = VGroup(*[self.TM(f'${k}$', 30, GOLD if k == 4 else SOFT).next_to(p, DOWN, buff=.15)
                             for k, p in enumerate(self.row)])
        self.snake = CurvedArrow(self.row[3].get_top() + UP * .05, self.row[1].get_top() + UP * .05, angle=1.2, color=CORAL, stroke_width=6)
        self.f = frog().move_to(self.row[0])
        self.play(FadeIn(self.row), FadeIn(self.nums), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.snake), run_time=self.rt(.05))
        self.play(FadeIn(self.f, scale=.5), run_time=self.rt(.03))
        for k in (2, 3, 1):
            self.play(self.f.animate.move_to(self.row[k]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.row[3].animate.set_opacity(.3), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.f.animate.move_to(self.row[2]), run_time=self.rt(.05))
        self.wait_until(.55, t0)
        self.write_board(self.M('e2', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(self.f.animate.move_to(self.row[1]), run_time=self.rt(.05))
        self.write_board(self.M('e1', 1.6))
        self.wait_until(.65, t0)
        m = self.M('sol', 1.7)
        self.write_board(m)
        self.frame(m)

    def beat_s4(self, T):
        self.clear_board(.03)
        self.play(self.f.animate.move_to(self.row[0]), run_time=self.rt(.05))
        m = self.M('e0', 1.7)
        self.write_board(m)
        self.frame(m)

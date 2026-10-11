"""XSS097 · Ai ngửa trước thắng — A tung trước: 1/2 + 1/8 + 1/32 + … = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import badge, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS097', 'answer': '2/3'}
PROBLEM = ['A và B lần lượt tung đồng xu,',
           'A tung trước. Ai ra ngửa trước',
           'thì thắng. $P("A thắng")$?']
OPTIONS = ['1/2', '2/3', '3/4']
CORRECT = 1
ANSWER_VALUE = 2 / 3

BEATS = [
    Beat('hook', 'hook', 'A và B thay nhau tung một đồng xu, A tung trước. Ai ra mặt ngửa trước thì thắng. '
                         'Trò chơi có công bằng không? Xác suất A thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'A thắng ngay lượt đầu với xác suất một phần hai. Nếu A ra sấp, B ra sấp, A lại có lượt mới: '
                        'thắng ở lượt ba với xác suất một phần tám, lượt năm một phần ba mươi hai.'),
    Beat('s2', 'solve', 'Mẹo gọn hơn: mỗi vòng hai lượt, A thắng với xác suất một phần hai, B thắng với xác suất một phần tư. '
                        'Nếu cả hai đều sấp, mọi thứ lặp lại từ đầu.'),
    Beat('s3', 'solve', 'Vậy tỉ lệ giữa A và B luôn là một phần hai so với một phần tư, tức hai với một. '
                        'A thắng với xác suất hai phần ba. Tổng một phần hai cộng một phần tám cộng một phần ba mươi hai, '
                        'cứ thế, cũng ra hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Muốn công bằng thì phải bốc thăm xem ai tung trước!'),
    Beat('outro', 'outro', outro_text(97)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    series='P(A) = 1/2 + 1/8 + 1/32 + dots',
                    ratio='P(A) : P(B) = 1/2 : 1/4 = 2 : 1',
                    prob='P(A) = 2/3')


def validate() -> bool:
    s = sum(F(1, 2) * F(1, 4) ** k for k in range(60))
    assert abs(float(s) - 2 / 3) < 1e-15 and F(1, 2) / (F(1, 2) + F(1, 4)) == F(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS097(ShortScene):
    N = 97

    def hook_visual(self, t0):
        self.players = VGroup(VGroup(badge('A', CYAN, 40), coin('N', .7)).arrange([0, -1, 0], buff=.3),
                              VGroup(badge('B', CORAL, 40), coin('S', .7)).arrange([0, -1, 0], buff=.3)) \
            .arrange(buff=2.0).move_to([0, 1.5, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.players, lag_ratio=.3), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('series', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.35, t0)
        self.play(FadeIn(self.TM('mỗi vòng: A $1/2$, B $1/4$', 32, GOLD, bold=True).move_to([0, .1, 0])), run_time=self.rt(.06))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('ratio', 1.9))
        self.wait_until(.35, t0)
        m = self.M('prob', 2.4)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.75, t0)
        self.write_board(tx('đi trước có lợi gấp đôi', 26, SOFT), anim='fade')

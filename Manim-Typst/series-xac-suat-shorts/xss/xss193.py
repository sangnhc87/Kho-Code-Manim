"""XSS193 · Thêm một đồng xu — An n + 1 đồng, Bình n đồng: An nhiều ngửa hơn ⇔ An nhiều sấp hơn không được; đối xứng ⇒ 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS193', 'answer': '1/2'}
PROBLEM = ['An tung $4$ đồng xu, Bình tung',
           '$3$ đồng xu. Xác suất An được nhiều',
           'mặt ngửa hơn Bình?']
OPTIONS = ['1/2', '11/16', '5/8']
CORRECT = 0
ANSWER_VALUE = .5

BEATS = [
    Beat('hook', 'hook', 'An tung bốn đồng xu, Bình tung ba đồng xu. Xác suất An được nhiều mặt ngửa hơn Bình là bao nhiêu? '
                         'Liệt kê thì có một trăm hai mươi tám khả năng, nhưng có một lời giải chỉ mất mười giây.'),
    Beat('guess', 'hook', 'Một phần hai, mười một phần mười sáu, hay năm phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'An có nhiều hơn Bình một đồng xu. Vậy An hoặc có nhiều ngửa hơn Bình, hoặc có nhiều sấp hơn Bình, '
                        'và không thể cả hai cùng xảy ra.'),
    Beat('s2', 'solve', 'Thật vậy: nếu An không hơn Bình cả về ngửa lẫn sấp, thì tổng số đồng của An không vượt số đồng của Bình, vô lý. '
                        'Và nếu hơn cả hai thì An có ít nhất năm đồng, cũng vô lý.'),
    Beat('s3', 'solve', 'Đổi vai ngửa và sấp, bài toán không thay đổi, nên hai khả năng có cùng xác suất. Mỗi khả năng đúng một phần hai!'),
    Beat('answer', 'solve', 'Đáp án: một phần hai, với mọi n. Lý luận đối xứng đánh bại một trăm hai mươi tám phép đếm!'),
    Beat('outro', 'outro', outro_text(193)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    either='"An hơn ngửa" xor "An hơn sấp"',
                    prob='P = 1/2')


def validate() -> bool:
    for n in range(1, 6):
        good = sum(sum(w[:n + 1]) > sum(w[n + 1:]) for w in product((0, 1), repeat=2 * n + 1))
        assert F(good, 2 ** (2 * n + 1)) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS193(ShortScene):
    N = 193

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.an = VGroup(*[coin(f, .45) for f in 'NSNN']).arrange(buff=.12)
        self.binh = VGroup(*[coin(f, .45) for f in 'SNS']).arrange(buff=.12)
        self.rows = VGroup(VGroup(tx('An', 28, CYAN), self.an).arrange(buff=.3),
                           VGroup(tx('Bình', 28, CORAL), self.binh).arrange(buff=.3)).arrange([0, -1, 0], buff=.4,
                                                                                               aligned_edge=[-1, 0, 0])
        self.rows.move_to([0, 1.7, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.rows, lag_ratio=.2), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.an[-1].animate.scale(1.25), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        m = self.M('either', 1.8)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.TM('tổng $4 > 3$: không thể "thua" cả hai', 26, SOFT), anim='fade')

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.4)
        self.write_board(m)
        self.frame(m)

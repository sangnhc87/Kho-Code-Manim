"""XSS046 · Đoán mò cả 4 câu — mỗi câu 1/4, độc lập: (1/4)⁴ = 1/256."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS046', 'answer': '1/256'}
PROBLEM = ['Đoán mò $4$ câu trắc nghiệm, mỗi câu $4$',
           'phương án. Xác suất đúng cả $4$ câu?']
OPTIONS = ['1/16', '1/256', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 256
RIGHT_KEYS = 'BDAC'

BEATS = [
    Beat('hook', 'hook', 'Còn bốn câu trắc nghiệm mà hết giờ, bạn đành khoanh bừa. Mỗi câu có bốn phương án. '
                         'Xác suất bạn khoanh đúng cả bốn câu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười sáu, một phần hai trăm năm mươi sáu, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi câu chỉ có một phương án đúng trong bốn, nên đoán đúng một câu có xác suất một phần tư.'),
    Beat('s2', 'solve', 'Các câu đoán độc lập với nhau, nên đúng cả bốn câu có xác suất bằng một phần tư nhân bốn lần, '
                        'tức một phần tư mũ bốn, bằng một phần hai trăm năm mươi sáu.'),
    Beat('s3', 'solve', 'Nói cách khác, có hai trăm năm mươi sáu cách khoanh, và chỉ đúng một cách trọn vẹn. '
                        'Khoanh bừa gần như không thể ăn trọn điểm!'),
    Beat('answer', 'solve', 'Đáp án: một phần hai trăm năm mươi sáu, chưa tới nửa phần trăm. Học bài vẫn là chiến lược tốt nhất!'),
    Beat('outro', 'outro', outro_text(46)),
]

FORMULAS = formulas('1/256', OPTIONS, one='P("đúng 1 câu") = 1/4', prob='P = (1/4)^4 = 1/256', n='4^4 = 256')


def validate() -> bool:
    ways = list(product('ABCD', repeat=4))
    assert len(ways) == 256 and F(sum(''.join(w) == RIGHT_KEYS for w in ways), 256) == F(1, 4) ** 4
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS046(ShortScene):
    N = 46

    def hook_visual(self, t0):
        self.rows = VGroup()
        for i, key in enumerate(RIGHT_KEYS):
            opts = VGroup(*[token(c, SOFT, .3) for c in 'ABCD']).arrange(buff=.2)
            self.rows.add(VGroup(tx(f'Câu {i + 1}', 26, SOFT, bold=True), opts).arrange(buff=.4))
        self.rows.arrange([0, -1, 0], buff=.28).move_to([0, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.rows, lag_ratio=.2), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        for row, key in zip(self.rows, RIGHT_KEYS):
            self.play(row[1]['ABCD'.index(key)][0].animate.set_fill(GREEN), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.write_board(self.M('one', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.45, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('n', 1.8), anim='fade')
        self.wait_until(.5, t0)
        self.write_board(tx('chỉ 1 cách đúng trọn vẹn', 28, CORAL, bold=True), anim='fade')

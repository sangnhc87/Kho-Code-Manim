"""XSS054 · Ba xúc xắc tổng 10 — 27 bộ trong 216: 1/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS054', 'answer': '1/8'}
PROBLEM = ['Gieo ba con xúc xắc.', 'Xác suất tổng số chấm bằng $10$?']
OPTIONS = ['1/6', '1/8', '1/12']
CORRECT = 1
ANSWER_VALUE = 1 / 8
PARTS10 = [(1, 3, 6), (1, 4, 5), (2, 2, 6), (2, 3, 5), (2, 4, 4), (3, 3, 4)]

BEATS = [
    Beat('hook', 'hook', 'Gieo ba con xúc xắc. Xác suất tổng số chấm bằng mười là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần tám, hay một phần mười hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba con xúc xắc cho sáu mũ ba bằng hai trăm mười sáu kết quả đồng khả năng.'),
    Beat('s2', 'solve', 'Liệt kê các bộ số có tổng mười: một ba sáu, một bốn năm, hai ba năm có sáu hoán vị mỗi bộ. '
                        'Hai hai sáu, hai bốn bốn, ba ba bốn có ba hoán vị mỗi bộ.'),
    Beat('s3', 'solve', 'Tổng cộng ba nhân sáu cộng ba nhân ba, bằng hai mươi bảy kết quả. '
                        'Xác suất bằng hai mươi bảy phần hai trăm mười sáu, đúng bằng một phần tám.'),
    Beat('answer', 'solve', 'Đáp án: một phần tám. Bộ ba số khác nhau có sáu hoán vị, có hai số trùng chỉ có ba!'),
    Beat('outro', 'outro', outro_text(54)),
]

FORMULAS = formulas('1/8', OPTIONS,
                    n='n(Omega) = 6^3 = 216',
                    count='3 dot 6 + 3 dot 3 = 27',
                    prob='P = 27/216 = 1/8')


def validate() -> bool:
    space = list(product(range(1, 7), repeat=3))
    assert F(sum(sum(w) == 10 for w in space), 216) == F(1, 8)
    assert sum(len(set(permutations(p))) for p in PARTS10) == 27
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS054(ShortScene):
    N = 54

    def hook_visual(self, t0):
        self.trio = VGroup(*[die(v, 1.3) for v in (2, 3, 5)]).arrange(buff=.4).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.trio, lag_ratio=.3), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.M('n', 2.3))

    def beat_s2(self, T):
        self.clear_board(.03)
        self.play(self.trio.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.trio)
        rows = VGroup()
        for p in PARTS10:
            k = len(set(permutations(p)))
            rows.add(VGroup(VGroup(*[die(v, .55) for v in p]).arrange(buff=.08),
                            self.TM(f'$times {k}$', 26, GOLD if k == 6 else CYAN)).arrange(buff=.3))
        rows.arrange_in_grid(3, 2, buff=(.6, .25), flow_order='dr').move_to([0, 1.3, 0])
        self.play(FadeIn(rows, lag_ratio=.25), run_time=self.rt(.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('count', 2.0))
        self.wait_until(.5, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)



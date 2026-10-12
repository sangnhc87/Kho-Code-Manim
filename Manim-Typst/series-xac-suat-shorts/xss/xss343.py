"""XSS343 · Màu nào hết trước? — 3 đỏ 2 xanh rút đến khi hết một màu; xanh hết trước ⇔ bi cuối cùng (nếu rút hết) là đỏ: 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, SurroundingRectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import urn  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS343', 'answer': '3/5'}
PROBLEM = ['Hộp $3$ đỏ, $2$ xanh. Rút lần lượt đến khi',
           'hết hẳn một màu. Xác suất màu xanh hết',
           'trước?']
OPTIONS = ['3/5', '2/5', '1/2']
CORRECT = 0
ANSWER_VALUE = .6
ORDERS = set(permutations('RRRBB'))


def blue_first(o):
    r = b = 0
    for c in o:
        r, b = r + (c == 'R'), b + (c == 'B')
        if b == 2:
            return True
        if r == 3:
            return False


BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi đỏ và hai bi xanh. Rút lần lượt không hoàn lại cho đến khi một màu bị rút hết. '
                         'Xác suất màu xanh hết trước là bao nhiêu? Xanh ít hơn, nhưng liệu có chắc hết trước?'),
    Beat('guess', 'hook', 'Ba phần năm, hai phần năm, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo: cứ tưởng tượng rút hết cả năm bi. Màu nào hết trước thì màu còn lại chứa bi cuối cùng.'),
    Beat('s2', 'solve', 'Vậy xanh hết trước khi và chỉ khi bi cuối cùng là đỏ. Mọi vị trí đều như nhau, nên bi cuối đỏ với xác suất ba phần năm.'),
    Beat('s3', 'solve', 'Liệt kê mười thứ tự màu cũng thấy đúng sáu thứ tự kết thúc bằng bi đỏ.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Một câu hỏi về quá trình dừng biến thành câu hỏi về một vị trí duy nhất.'),
    Beat('outro', 'outro', outro_text(343)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    last='"xanh hết trước" <=> "bi cuối là đỏ"',
                    prob='P = 3/5',
                    cnt='6/10 = 3/5')


def validate() -> bool:
    good = sum(blue_first(o) for o in ORDERS)
    assert good == 6 and F(good, len(ORDERS)) == F(3, 5)
    assert all(blue_first(o) == (o[-1] == 'R') for o in ORDERS)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS343(ShortScene):
    N = 343

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn('RRRBB', cols=5, r=.3).move_to([0, 2.1, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))
        self.row = ball_row('BRRBR', y=.6, r=.36, buff=.3)
        self.wait_until(.45, t0)
        self.play(FadeIn(self.row, lag_ratio=.3), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(SurroundingRectangle(self.row[-1], color=GOLD, buff=.08)), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('last', 1.3))
        self.wait_until(.6, t0)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('cnt', 1.4), anim='fade')

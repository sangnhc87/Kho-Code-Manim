"""XSS378 · Dừng ở lần thứ tư — tung đến khi đủ 2 ngửa; dừng ở lần 4 ⇔ đúng 1 ngửa trong 3 lần đầu (NSS, SNS, SSN như nhau) → 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS378', 'answer': '1/3'}
PROBLEM = ['Tung đồng xu đến khi được $2$ lần ngửa.',
           'Biết dừng ở lần thứ $4$. Xác suất lần thứ',
           'nhất là ngửa?']
OPTIONS = ['1/2', '1/3', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 3
STOP4 = [q for q in product('NS', repeat=4) if q[3] == 'N' and q[:3].count('N') == 1]

BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu cho đến khi được hai lần ngửa thì dừng. Biết trò chơi dừng ở lần tung thứ tư. '
                         'Xác suất lần tung thứ nhất là ngửa?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dừng ở lần bốn nghĩa là lần bốn ngửa, và ba lần đầu có đúng một ngửa.'),
    Beat('s2', 'solve', 'Có ba dãy như vậy: ngửa sấp sấp, sấp ngửa sấp, sấp sấp ngửa, rồi ngửa. Cả ba có cùng xác suất một phần mười sáu.'),
    Beat('s3', 'solve', 'Chỉ một dãy bắt đầu bằng ngửa. Xác suất một phần ba, không phải một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Biết thời điểm dừng, vị trí của mặt ngửa còn lại phân bố đều.'),
    Beat('outro', 'outro', outro_text(378)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    cond='"đúng 1 ngửa trong 3 lần đầu, lần 4 ngửa"',
                    prob='P = 1/3')


def validate() -> bool:
    assert len(STOP4) == 3 and F(sum(q[0] == 'N' for q in STOP4), 3) == F(1, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS378(ShortScene):
    N = 378

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.rows = VGroup(*[VGroup(*[coin(c, .38) for c in q]).arrange(buff=.25) for q in STOP4]).arrange(DOWN, buff=.35).move_to([0, 1.2, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.rows[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('cond', 1.2))

    def beat_s2(self, T):
        self.play(FadeIn(self.rows[0]), FadeIn(self.rows[2]), run_time=self.rt(.1))

    def beat_s3(self, T):
        self.play(self.rows[0][0].animate.scale(1.3).set_stroke(GOLD, 6), run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

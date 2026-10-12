"""XSS385 · Tổng vượt 3 — gieo đến khi tổng ≥ 4; dừng ở lần 2 ⇔ lần đầu a ≤ 3 và a + b ≥ 4: số b thỏa 4, 5, 6 với a = 1, 2, 3 → 4/15."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, RIGHT, FadeIn, SurroundingRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS385', 'answer': '4/15'}
PROBLEM = ['Gieo xúc xắc đến khi tổng điểm $>= 4$.',
           'Biết dừng ở lần gieo thứ $2$. Xác suất',
           'lần đầu ra $1$?']
OPTIONS = ['4/15', '1/3', '1/5']
CORRECT = 0
ANSWER_VALUE = 4 / 15
WAYS = {a: sum(a + b >= 4 for b in range(1, 7)) for a in (1, 2, 3)}

BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc liên tục, cộng dồn, dừng khi tổng từ bốn trở lên. Biết trò chơi dừng đúng ở lần gieo thứ hai. '
                         'Xác suất lần đầu ra mặt một?'),
    Beat('guess', 'hook', 'Bốn phần mười lăm, một phần ba, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dừng ở lần hai nghĩa là lần đầu chưa đủ, tức ra một, hai hoặc ba; và tổng hai lần đạt từ bốn trở lên.'),
    Beat('s2', 'solve', 'Lần đầu ra một: lần hai cần từ ba trở lên, bốn cách. Ra hai: cần từ hai trở lên, năm cách. Ra ba: lần hai nào cũng được, sáu cách.'),
    Beat('s3', 'solve', 'Các cặp đều có xác suất một phần ba mươi sáu. Xác suất bốn chia bốn cộng năm cộng sáu, bằng bốn phần mười lăm.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần mười lăm. Điều kiện dừng ở lần hai ưu tiên lần đầu lớn, vì dễ vượt ngưỡng hơn.'),
    Beat('outro', 'outro', outro_text(385)),
]

FORMULAS = formulas('4/15', OPTIONS,
                    cnt='a = 1: 4, quad a = 2: 5, quad a = 3: 6',
                    prob='P = 4/(4 + 5 + 6) = 4/15')


def validate() -> bool:
    assert WAYS == {1: 4, 2: 5, 3: 6} and F(WAYS[1], sum(WAYS.values())) == F(4, 15)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS385(ShortScene):
    N = 385

    def hook_visual(self, t0):
        self.board_top = -1.4
        rows = VGroup()
        for a in (1, 2, 3):
            seconds = VGroup(*[die(b, .42).set_opacity(1 if a + b >= 4 else .2) for b in range(1, 7)]).arrange(RIGHT, buff=.1)
            rows.add(VGroup(die(a, .55, color=GOLD), self.TM('$+$', 30, SOFT), seconds).arrange(RIGHT, buff=.25))
        self.rows = rows.arrange(DOWN, buff=.35, aligned_edge=[-1, 0, 0]).move_to([0, .9, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(VGroup(*[r[0] for r in rows]), lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[FadeIn(r[1:]) for r in self.rows], run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.write_board(self.M('cnt', 1.4))

    def beat_s3(self, T):
        self.play(FadeIn(SurroundingRectangle(self.rows[0], color=GREEN, buff=.08)), run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS415 · Đoán lá đỏ — mọi chiến thuật dừng đều thắng với xác suất 1/2: xác suất lá kế tiếp đỏ bằng tỉ lệ đỏ còn lại = xác suất lá cuối cùng đỏ."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import card_back, playing_card  # noqa: E402

EPISODE = {'code': 'XSS415', 'answer': '1/2'}
PROBLEM = ['Lật dần bộ bài $52$ lá; bạn được hô "đỏ"',
           'đúng một lần trước một lá. Chiến thuật',
           'tốt nhất thắng với xác suất bao nhiêu?']
OPTIONS = ['1/2', '26/51', '3/4']
CORRECT = 0
ANSWER_VALUE = .5


@lru_cache(None)
def best(r, b):
    """Best winning probability with r red and b black cards left (must call before the deck ends)."""
    if r + b == 1:
        return F(r)
    now = F(r, r + b)
    wait = (F(r, r + b) * best(r - 1, b) if r else 0) + (F(b, r + b) * best(r, b - 1) if b else 0)
    return max(now, wait)


BEATS = [
    Beat('hook', 'hook', 'Lật dần từng lá của bộ bài năm mươi hai lá. Trước một lá bất kỳ, bạn được hô đỏ đúng một lần; lá đó đỏ thì thắng. '
                         'Bạn có thể chờ tới lúc đã lộ nhiều lá đen. Chiến thuật tốt nhất thắng với xác suất bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai mươi sáu phần năm mươi mốt, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Giả sử bạn hô ở một thời điểm nào đó. Xác suất lá tiếp theo đỏ bằng tỉ lệ lá đỏ còn lại trong bộ.'),
    Beat('s2', 'solve', 'Nhưng tỉ lệ đó cũng chính là xác suất lá cuối cùng của bộ bài là đỏ! Hô ngay lá kế tiếp hay hô ở lá cuối là như nhau.'),
    Beat('s3', 'solve', 'Mà lá cuối cùng đỏ với xác suất một phần hai, bất kể bạn đã quan sát gì. Mọi chiến thuật đều thắng đúng một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Không có chiến thuật nào đánh bại được một trò chơi công bằng.'),
    Beat('outro', 'outro', outro_text(415)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    next='P("lá kế đỏ") = r/(r + b) = P("lá cuối đỏ")',
                    prob='P = 1/2')


def validate() -> bool:
    assert all(best(r, r) == F(1, 2) for r in range(1, 10))
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS415(ShortScene):
    N = 415

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.shown = [playing_card(r, s, .9) for r, s in (('7', 'S'), ('K', 'C'), ('3', 'S'), ('Q', 'H'))]
        for i, c in enumerate(self.shown):
            c.move_to([-2.4 + 1.1 * i, 1.3, 0])
        self.deck = card_back(.9).move_to([2.3, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.deck), *[FadeIn(c) for c in self.shown], run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.deck.animate.scale(1.15), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('next', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

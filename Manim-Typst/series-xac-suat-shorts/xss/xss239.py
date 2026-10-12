"""XSS239 · Gieo đến khi ra 6: không nhớ — P(T = 4 | T ≥ 3) = P(T = 2) = 5/36."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS239', 'answer': '5/36'}
PROBLEM = ['Gieo xúc xắc đến khi ra mặt $6$. Biết cần',
           'ít nhất $3$ lần. Xác suất cần đúng $4$ lần?']
OPTIONS = ['1/6', '5/36', '125/1296']
CORRECT = 1
ANSWER_VALUE = 5 / 36


def p_eq(k):
    return F(5, 6) ** (k - 1) * F(1, 6)


BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc cho đến khi ra mặt sáu. Bạn được biết phải gieo ít nhất ba lần, tức hai lần đầu đều không ra sáu. '
                         'Xác suất cần đúng bốn lần là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, năm phần ba mươi sáu, hay một trăm hai mươi lăm phần một nghìn hai trăm chín mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tính trực tiếp: P cần đúng bốn lần bằng năm phần sáu mũ ba nhân một phần sáu. P cần ít nhất ba lần bằng năm phần sáu mũ hai.'),
    Beat('s2', 'solve', 'Chia: năm phần sáu mũ ba nhân một phần sáu, chia năm phần sáu mũ hai, bằng năm phần sáu nhân một phần sáu, năm phần ba mươi sáu.'),
    Beat('s3', 'solve', 'Đó chính là xác suất cần đúng hai lần ngay từ đầu! Xúc xắc không nhớ hai lần thất bại trước: '
                        'biết đã thất bại thì mọi thứ bắt đầu lại.'),
    Beat('answer', 'solve', 'Đáp án: năm phần ba mươi sáu. Tính không nhớ: điều kiện "đã thất bại" chỉ làm dời mốc thời gian!'),
    Beat('outro', 'outro', outro_text(239)),
]

FORMULAS = formulas('5/36', OPTIONS,
                    ratio='P(T = 4 | T >= 3) = ((5/6)^3 dot 1/6)/((5/6)^2)',
                    mem='= 5/6 dot 1/6 = P(T = 2) = 5/36')


def validate() -> bool:
    ge3 = 1 - p_eq(1) - p_eq(2)
    assert ge3 == F(5, 6) ** 2 and p_eq(4) / ge3 == p_eq(2) == F(5, 36)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS239(ShortScene):
    N = 239

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.seq = VGroup(*[die(v, .9) for v in (3, 1, 5, 6)]).arrange(buff=.3).move_to([0, 2.0, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.seq, lag_ratio=.3), run_time=self.rt(.15))
        self.play(*[d[0].animate.set_stroke(CORAL, 5) for d in self.seq[:2]], run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.seq[3][0].animate.set_stroke(GREEN, 6), run_time=self.rt(.04))
        self.wait_until(.4, t0)
        self.write_board(self.M('ratio', 1.6))

    def beat_s2(self, T):
        m = self.M('mem', 1.7)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.play(self.seq[:2].animate.set_opacity(.15), run_time=self.rt(.06))
        self.play(self.seq[2:].animate.scale(1.15).set_stroke(GOLD, 2), run_time=self.rt(.05))

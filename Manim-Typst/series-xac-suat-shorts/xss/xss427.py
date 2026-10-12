"""XSS427 · Cùng màu hay khác màu? — lá thứ nhất tùy ý, lá thứ hai khác màu: 26/51 (lớn hơn 1/2 một chút)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import card_back, playing_card  # noqa: E402

EPISODE = {'code': 'XSS427', 'answer': '26/51'}
PROBLEM = ['Rút $2$ lá từ bộ bài $52$ lá. Xác suất hai',
           'lá khác màu?']
OPTIONS = ['26/51', '1/2', '25/51']
CORRECT = 0
ANSWER_VALUE = 26 / 51

BEATS = [
    Beat('hook', 'hook', 'Rút ngẫu nhiên hai lá từ bộ bài năm mươi hai lá: hai mươi sáu đỏ, hai mươi sáu đen. Xác suất hai lá khác màu? '
                         'Cùng màu và khác màu, có phải năm mươi năm mươi?'),
    Beat('guess', 'hook', 'Hai mươi sáu phần năm mươi mốt, một phần hai, hay hai mươi lăm phần năm mươi mốt? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lá thứ nhất là màu gì cũng được. Còn lại năm mươi mốt lá: hai mươi sáu lá khác màu, chỉ hai mươi lăm lá cùng màu.'),
    Beat('s2', 'solve', 'Vậy khác màu với xác suất hai mươi sáu phần năm mươi mốt, nhỉnh hơn một nửa.'),
    Beat('s3', 'solve', 'Kiểm tra bằng tổ hợp: hai mươi sáu nhân hai mươi sáu chia tổ hợp chập hai của năm mươi hai, bằng sáu trăm bảy mươi sáu phần một nghìn ba trăm hai mươi sáu, cũng là hai mươi sáu phần năm mươi mốt.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi sáu phần năm mươi mốt. Lá đã rút không trở lại, nên cán cân nghiêng về khác màu.'),
    Beat('outro', 'outro', outro_text(427)),
]

FORMULAS = formulas('26/51', OPTIONS,
                    second='P = 26/51',
                    chk='(26 dot 26)/(C_52^2) = 676/1326 = 26/51')


def validate() -> bool:
    assert F(26 * 26, comb(52, 2)) == F(26, 51)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS427(ShortScene):
    N = 427

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.deck = card_back(1.0).move_to([-1.6, 1.4, 0])
        self.c1 = playing_card('7', 'H', 1.0).move_to([.2, 1.4, 0])
        self.c2 = playing_card('Q', 'S', 1.0).move_to([1.7, 1.4, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.deck), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.c1), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.c2), run_time=self.rt(.05))

    def beat_s2(self, T):
        m = self.M('second', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('chk', 1.3), anim='fade')

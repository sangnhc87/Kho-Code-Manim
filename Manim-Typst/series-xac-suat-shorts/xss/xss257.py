"""XSS257 · Điều kiện là một phép hợp — P(A | A ∪ B) = P(A)/P(A ∪ B) = 0,5/0,7 = 5/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import unit_square  # noqa: E402

EPISODE = {'code': 'XSS257', 'answer': '5/7'}
PROBLEM = ['Hai biến cố độc lập A, B có $P(A) = "0,5"$;',
           '$P(B) = "0,4"$. Tính $P(A | A union B)$.']
OPTIONS = ['"0,5"', '5/7', '"0,7"']
CORRECT = 1
ANSWER_VALUE = 5 / 7

BEATS = [
    Beat('hook', 'hook', 'Hai biến cố độc lập A và B, xác suất không phẩy năm và không phẩy bốn. '
                         'Biết A hoặc B đã xảy ra. Xác suất A xảy ra là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy năm, năm phần bảy, hay không phẩy bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hình vuông đơn vị: A chiếm cột rộng không phẩy năm, B chiếm hàng cao không phẩy bốn. '
                        'A hợp B là phần được tô, diện tích một trừ không phẩy năm nhân không phẩy sáu, bằng không phẩy bảy.'),
    Beat('s2', 'solve', 'A nằm trọn trong A hợp B, nên A giao với điều kiện chính là A. Xác suất có điều kiện bằng không phẩy năm chia không phẩy bảy.'),
    Beat('s3', 'solve', 'Bằng năm phần bảy. Thông tin "có ít nhất một biến cố xảy ra" làm xác suất của A tăng từ một phần hai lên năm phần bảy.'),
    Beat('answer', 'solve', 'Đáp án: năm phần bảy. Khi điều kiện chứa biến cố, chỉ cần chia cho xác suất điều kiện!'),
    Beat('outro', 'outro', outro_text(257)),
]

FORMULAS = formulas('5/7', OPTIONS,
                    union='P(A union B) = 1 - "0,5" dot "0,6" = "0,7"',
                    prob='P(A | A union B) = (P(A))/(P(A union B)) = ("0,5")/("0,7") = 5/7')


def validate() -> bool:
    union = 1 - F(1, 2) * F(3, 5)
    assert F(1, 2) / union == F(5, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS257(ShortScene):
    N = 257

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.sq = unit_square(.5, .4, 3.6, (0, 1.2))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.sq), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        regs = [self.sq.region(k, GOLD, .6) for k in ('AB', 'Ab', 'aB')]
        self.play(*[FadeIn(r) for r in regs], run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.write_board(self.M('union', 1.8))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.sq.region('AB', CYAN, .8)), FadeIn(self.sq.region('Ab', CYAN, .8)), run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('$1/2$ → $5/7$', 30, CORAL, bold=True), anim='fade')

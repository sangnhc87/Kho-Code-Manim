"""XSS041 · Hai xạ thủ cùng trúng — độc lập: 0,8 · 0,7 = 0,56 (diện tích hình chữ nhật)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from xss.shooters import ShooterSquare  # noqa: E402

EPISODE = {'code': 'XSS041', 'answer': '0,56'}
PROBLEM = ['Hai xạ thủ bắn độc lập, trúng với xác suất', '$"0,8"$ và $"0,7"$. Xác suất cả hai cùng trúng?']
OPTIONS = ['"1,5"', '"0,56"', '"0,75"']
CORRECT = 1
ANSWER_VALUE = .56

BEATS = [
    Beat('hook', 'hook', 'Hai xạ thủ bắn độc lập vào một tấm bia. Người thứ nhất trúng với xác suất không phẩy tám, '
                         'người thứ hai không phẩy bảy. Xác suất cả hai cùng trúng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phẩy năm, không phẩy năm sáu, hay không phẩy bảy lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ một hình vuông có diện tích bằng một. Phần bên trái rộng không phẩy tám là khi người thứ nhất '
                        'trúng. Phần phía trên cao không phẩy bảy là khi người thứ hai trúng.'),
    Beat('s2', 'solve', 'Vì hai người bắn độc lập, cả hai cùng trúng chính là hình chữ nhật góc trên bên trái. '
                        'Diện tích bằng không phẩy tám nhân không phẩy bảy, bằng không phẩy năm sáu.'),
    Beat('s3', 'solve', 'Cộng hai xác suất ra một phẩy năm, lớn hơn một: dấu hiệu chắc chắn của sai lầm. '
                        'Hai biến cố độc lập cùng xảy ra thì ta nhân, không cộng.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy năm sáu. Độc lập và cùng xảy ra: nhân hai xác suất!'),
    Beat('outro', 'outro', outro_text(41)),
]

FORMULAS = formulas('"0,56"', OPTIONS,
                    rule='P(A B) = P(A) dot P(B)',
                    calc='"0,8" dot "0,7" = "0,56"')


def validate() -> bool:
    assert F(8, 10) * F(7, 10) == F(56, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS041(ShooterSquare):
    N = 41

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.sq.region('Ab', '#38CDE6', .25)), FadeIn(self.sq.region('AB', '#38CDE6', .25)),
                  run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.sq.region('aB', CORAL, .25)), FadeIn(self.sq.region('AB', CORAL, .25)), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        ab = self.sq.region('AB', GOLD, .85)
        self.play(FadeIn(ab), run_time=self.rt(.1))
        self.play(FadeIn(self.TM('$"0,56"$', 40, '#0B1221', bold=True).move_to(ab)), run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.write_board(self.M('rule', 2.0))
        m = self.M('calc', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.TM('$"0,8" + "0,7" = "1,5" > 1$', 32, CORAL, bold=True))
        self.wait_until(.5, t0)
        self.write_board(tx('độc lập, cùng xảy ra: NHÂN', 32, GOLD, bold=True), anim='fade')

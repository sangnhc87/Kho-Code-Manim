"""XSS042 · Ít nhất một viên trúng — 1 − 0,2 · 0,3 = 0,94 (góc "cả hai trượt")."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402
from xss.shooters import ShooterSquare  # noqa: E402

EPISODE = {'code': 'XSS042', 'answer': '0,94'}
PROBLEM = ['Hai xạ thủ độc lập trúng với xác suất $"0,8"$ và $"0,7"$.', 'Xác suất có ít nhất một viên trúng?']
OPTIONS = ['"0,56"', '"1,5"', '"0,94"']
CORRECT = 2
ANSWER_VALUE = .94

BEATS = [
    Beat('hook', 'hook', 'Vẫn hai xạ thủ, trúng với xác suất không phẩy tám và không phẩy bảy, bắn độc lập. '
                         'Xác suất bia có ít nhất một vết đạn là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy năm sáu, một phẩy năm, hay không phẩy chín tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ít nhất một viên trúng gồm ba trường hợp: chỉ người một trúng, chỉ người hai trúng, cả hai cùng trúng. '
                        'Tính từng phần thì dài.'),
    Beat('s2', 'solve', 'Biến cố đối gọn hơn nhiều: cả hai cùng trượt. Đó là góc dưới bên phải hình vuông, '
                        'diện tích không phẩy hai nhân không phẩy ba, bằng không phẩy không sáu.'),
    Beat('s3', 'solve', 'Vậy xác suất có ít nhất một viên trúng bằng một trừ không phẩy không sáu, bằng không phẩy chín tư.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín tư. Ít nhất một: tính phần bù, ai cũng trượt.'),
    Beat('outro', 'outro', outro_text(42)),
]

FORMULAS = formulas('"0,94"', OPTIONS,
                    miss='P("cả hai trượt") = "0,2" dot "0,3" = "0,06"',
                    prob='P = 1 - "0,06" = "0,94"')


def validate() -> bool:
    assert 1 - F(2, 10) * F(3, 10) == F(94, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS042(ShooterSquare):
    N = 42

    def beat_s1(self, T):
        t0 = self.now()
        for key in ('Ab', 'aB', 'AB'):
            self.play(FadeIn(self.sq.region(key, GREEN, .45)), run_time=self.rt(.1))
        self.wait_until(.7, t0)
        self.write_board(tx('3 trường hợp: dài!', 30, GREEN, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        ab = self.sq.region('ab', CORAL, .9)
        self.play(FadeIn(ab), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('miss', 1.6))

    def beat_s3(self, T):
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

"""XSS043 · Đúng một viên trúng — 0,8 · 0,3 + 0,2 · 0,7 = 0,38 (hai hình chữ nhật chéo)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss.shooters import ShooterSquare  # noqa: E402

EPISODE = {'code': 'XSS043', 'answer': '0,38'}
PROBLEM = ['Hai xạ thủ độc lập trúng với xác suất $"0,8"$ và $"0,7"$.', 'Xác suất có đúng một viên trúng?']
OPTIONS = ['"0,44"', '"0,38"', '"0,5"']
CORRECT = 1
ANSWER_VALUE = .38

BEATS = [
    Beat('hook', 'hook', 'Hai xạ thủ trúng với xác suất không phẩy tám và không phẩy bảy, bắn độc lập. '
                         'Lần này hỏi: xác suất có đúng một viên trúng là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bốn bốn, không phẩy ba tám, hay không phẩy năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đúng một viên có hai khả năng tách rời nhau. Người một trúng, người hai trượt: '
                        'không phẩy tám nhân không phẩy ba, bằng không phẩy hai bốn.'),
    Beat('s2', 'solve', 'Hoặc người một trượt, người hai trúng: không phẩy hai nhân không phẩy bảy, bằng không phẩy một bốn. '
                        'Hai khả năng xung khắc nên được cộng: không phẩy ba tám.'),
    Beat('s3', 'solve', 'Bẫy không phẩy bốn bốn là một trừ không phẩy năm sáu: nó gồm cả trường hợp cả hai đều trượt. '
                        'Đúng một khác với không phải cả hai!'),
    Beat('answer', 'solve', 'Đáp án: không phẩy ba tám. Chia trường hợp xung khắc, mỗi trường hợp nhân, rồi cộng lại.'),
    Beat('outro', 'outro', outro_text(43)),
]

FORMULAS = formulas('"0,38"', OPTIONS,
                    one='"0,8" dot "0,3" = "0,24"',
                    two='"0,2" dot "0,7" = "0,14"',
                    sum='"0,24" + "0,14" = "0,38"',
                    trap='1 - "0,56" = "0,44" quad coral("gồm cả hai trượt")')


def validate() -> bool:
    assert F(8, 10) * F(3, 10) + F(2, 10) * F(7, 10) == F(38, 100)
    assert 1 - F(56, 100) == F(44, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS043(ShooterSquare):
    N = 43

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.sq.region('Ab', CYAN, .75)), run_time=self.rt(.08))
        self.write_board(self.M('one', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.sq.region('aB', CORAL, .75)), run_time=self.rt(.08))
        self.write_board(self.M('two', 1.9))
        self.wait_until(.6, t0)
        m = self.M('sum', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(FadeIn(self.sq.region('ab', GOLD, .45)), run_time=self.rt(.06))
        self.write_board(self.M('trap', 1.5), anim='fade')
        self.wait_until(.6, t0)
        self.write_board(tx('đúng một ≠ không phải cả hai', 30, GOLD, bold=True), anim='fade')

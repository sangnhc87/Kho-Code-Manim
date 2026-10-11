"""XSS084 · Ai bắn trúng? — biết đúng một viên trúng: P(người I) = 0,24 / 0,38 = 12/19."""
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

EPISODE = {'code': 'XSS084', 'answer': '12/19'}
PROBLEM = ['Hai xạ thủ độc lập trúng với xác suất',
           '$"0,8"$ và $"0,7"$. Biết có đúng một viên trúng.',
           'Xác suất đó là của người I?']
OPTIONS = ['"0,8"', '12/19', '1/2']
CORRECT = 1
ANSWER_VALUE = 12 / 19

BEATS = [
    Beat('hook', 'hook', 'Hai xạ thủ trúng với xác suất không phẩy tám và không phẩy bảy. Sau loạt bắn, '
                         'tấm bia có đúng một vết đạn. Xác suất viên trúng đó là của người thứ nhất bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy tám, mười hai phần mười chín, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết đúng một viên trúng, chỉ còn hai vùng trên hình vuông: người một trúng người hai trượt, '
                        'diện tích không phẩy hai bốn; người một trượt người hai trúng, diện tích không phẩy một bốn.'),
    Beat('s2', 'solve', 'Tổng hai vùng là không phẩy ba tám. Phần của người một: không phẩy hai bốn chia không phẩy ba tám, '
                        'bằng mười hai phần mười chín.'),
    Beat('s3', 'solve', 'Khoảng sáu mươi ba phần trăm: người bắn giỏi hơn có khả năng là chủ nhân vết đạn cao hơn, '
                        'nhưng không chắc chắn như không phẩy tám.'),
    Beat('answer', 'solve', 'Đáp án: mười hai phần mười chín. Có điều kiện: chỉ giữ vùng thỏa điều kiện, rồi lấy tỉ lệ!'),
    Beat('outro', 'outro', outro_text(84)),
]

FORMULAS = formulas('12/19', OPTIONS,
                    tot='P("đúng 1") = "0,24" + "0,14" = "0,38"',
                    prob='P = ("0,24")/("0,38") = 12/19')


def validate() -> bool:
    one = F(8, 10) * F(3, 10)
    assert one / (one + F(2, 10) * F(7, 10)) == F(12, 19)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS084(ShooterSquare):
    N = 84

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.sq.region('Ab', CYAN, .75)), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.sq.region('aB', CORAL, .75)), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('tot', 1.8))
        self.wait_until(.45, t0)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.clear_board(.03)
        self.write_board(tx('khoảng 63%', 34, GOLD, bold=True), anim='fade')
        self.write_board(tx('người giỏi hơn: khả năng cao hơn, nhưng không chắc', 24, CYAN), anim='fade')

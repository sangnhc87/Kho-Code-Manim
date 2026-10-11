"""XSS038 · Thích Toán hoặc Anh — Venn: 25 + 20 − 10 = 35 → 7/8."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import venn  # noqa: E402

EPISODE = {'code': 'XSS038', 'answer': '7/8'}
PROBLEM = ['Lớp $40$ bạn: $25$ thích Toán, $20$ thích Anh, $10$ thích cả hai.',
           'Chọn $1$ bạn. Xác suất bạn đó thích ít nhất một môn?']
OPTIONS = ['9/8', '7/8', '3/4']
CORRECT = 1
ANSWER_VALUE = 7 / 8

BEATS = [
    Beat('hook', 'hook', 'Lớp bốn mươi bạn: hai mươi lăm bạn thích Toán, hai mươi bạn thích Anh, mười bạn thích cả hai. '
                         'Chọn ngẫu nhiên một bạn. Xác suất bạn đó thích ít nhất một trong hai môn là bao nhiêu?'),
    Beat('guess', 'hook', 'Chín phần tám, bảy phần tám, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cộng ngay hai mươi lăm với hai mươi được bốn mươi lăm, nhiều hơn cả lớp! '
                        'Lỗi ở chỗ mười bạn thích cả hai bị đếm hai lần.'),
    Beat('s2', 'solve', 'Vẽ biểu đồ Venn: phần chung có mười bạn, chỉ thích Toán mười lăm bạn, chỉ thích Anh mười bạn. '
                        'Tổng cộng ba mươi lăm bạn thích ít nhất một môn.'),
    Beat('s3', 'solve', 'Đó chính là công thức cộng xác suất: xác suất của A hợp B bằng xác suất A cộng xác suất B '
                        'trừ xác suất A giao B. Ba mươi lăm phần bốn mươi, bằng bảy phần tám.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần tám. Còn năm bạn không thích môn nào, một phần tám còn lại!'),
    Beat('outro', 'outro', outro_text(38)),
]

FORMULAS = formulas('7/8', OPTIONS,
                    count='25 + 20 - 10 = 35',
                    rule='P(A union B) = P(A) + P(B) - P(A B)',
                    prob='P = 35/40 = 7/8')


def validate() -> bool:
    toan, anh, both, n = 25, 20, 10, 40
    assert Fraction(toan + anh - both, n) == Fraction(7, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS038(ShortScene):
    N = 38

    def hook_visual(self, t0):
        self.v = venn(1.5, 1.6, CYAN, CORAL, (0, 1.25))
        labels = VGroup(tx('Toán', 32, CYAN, bold=True).next_to(self.v.a, [-1, 1, 0], buff=-.25),
                        tx('Anh', 32, CORAL, bold=True).next_to(self.v.b, [1, 1, 0], buff=-.25))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.v), FadeIn(labels), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.TM('$25 + 20 = 45 > 40$ ?!', 34, CORAL, bold=True))
        both = self.v.both(GOLD, .7)
        self.wait_until(.6, t0)
        self.play(FadeIn(both), run_time=self.rt(.08))
        self.both = both

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        regions = VGroup(self.v.only_a(), self.v.only_b())
        nums = VGroup(self.MNum(15, 0, CYAN, 44).move_to(self.v.a.get_center() + [-.55, 0, 0]),
                      self.MNum(10, 0, GOLD, 44).move_to(self.v.get_center()),
                      self.MNum(10, 0, CORAL, 44).move_to(self.v.b.get_center() + [.55, 0, 0]))
        self.play(FadeIn(regions), run_time=self.rt(.06))
        for m in nums:
            self.play(FadeIn(m, scale=1.4), run_time=self.rt(.06))
        self.wait_until(.7, t0)
        self.write_board(self.M('count', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('rule', 1.6))
        self.wait_until(.55, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)



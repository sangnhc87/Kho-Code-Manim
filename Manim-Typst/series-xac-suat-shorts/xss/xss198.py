"""XSS198 · Loạt luân lưu — hòa sau 5 lượt: Σ C(5,k)² (3/4)^(2k) (1/4)^(10−2k) ≈ 0,29."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS198', 'answer': '≈ 0,29'}
PROBLEM = ['Mỗi đội sút $5$ quả luân lưu, mỗi quả',
           'vào với xác suất $"0,75"$, độc lập. Xác',
           'suất hai đội hòa sau $5$ lượt?']
OPTIONS = ['approx "0,1"', 'approx "0,29"', 'approx "0,5"']
CORRECT = 1
ANSWER_VALUE = .29
P = [comb(5, k) * F(3, 4) ** k * F(1, 4) ** (5 - k) for k in range(6)]

BEATS = [
    Beat('hook', 'hook', 'Loạt sút luân lưu: mỗi đội sút năm quả, mỗi quả vào lưới với xác suất không phẩy bảy lăm. '
                         'Xác suất hai đội hòa sau năm lượt, phải đá thêm, là bao nhiêu?'),
    Beat('guess', 'hook', 'Khoảng không phẩy một, khoảng không phẩy hai chín, hay khoảng không phẩy năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Số bàn của mỗi đội có phân phối nhị thức với n bằng năm, p bằng không phẩy bảy lăm. '
                        'Hai đội độc lập.'),
    Beat('s2', 'solve', 'Hòa nghĩa là hai đội cùng ghi k bàn, với k từ không đến năm. Xác suất bằng tổng các bình phương P của k.'),
    Beat('s3', 'solve', 'Ghi bốn bàn có xác suất khoảng không phẩy bốn, năm bàn khoảng không phẩy hai bốn, ba bàn khoảng không phẩy hai sáu. '
                        'Cộng các bình phương được khoảng không phẩy hai chín: gần một phần ba loạt luân lưu phải đá thêm!'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy hai chín. Hai đội càng giỏi đều nhau, khả năng hòa càng cao!'),
    Beat('outro', 'outro', outro_text(198)),
]

FORMULAS = formulas('approx "0,29"', OPTIONS,
                    pk='P(X = k) = C_5^k ("0,75")^k ("0,25")^(5 - k)',
                    tie='P("hòa") = sum_(k = 0)^5 P(X = k)^2 approx "0,29"')


def validate() -> bool:
    assert sum(P) == 1 and round(float(sum(p * p for p in P)), 2) == .29
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS198(ShortScene):
    N = 198

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.3, 3.0
        top = float(max(P))
        self.bars = VGroup()
        for k in range(6):
            r = Rectangle(width=.8, height=max(.03, h * float(P[k]) / top), stroke_width=0, fill_color=CYAN, fill_opacity=.85)
            r.move_to([-2.75 + 1.1 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k}$', 22, SOFT).next_to([-2.75 + 1.1 * k, base, 0], DOWN, buff=.08) for k in range(6)])
        self.wait_until(.7, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.2))
        self.write_board(self.M('pk', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[b.animate.set_fill(GOLD, .85) for b in self.bars[3:]], run_time=self.rt(.06))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.45, t0)
        m = self.M('tie', 1.7)
        self.write_board(m)
        self.frame(m)

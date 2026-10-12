"""XSS428 · Tổng ba xúc xắc lớn hơn 10 — đối xứng x ↦ 7 − x: tổng S ↦ 21 − S; S > 10 ⇔ 21 − S ≤ 10 → P(S > 10) = P(S ≤ 10) = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS428', 'answer': '1/2'}
PROBLEM = ['Gieo $3$ xúc xắc. Xác suất tổng số chấm',
           'lớn hơn $10$?']
OPTIONS = ['1/2', '5/12', '7/12']
CORRECT = 0
ANSWER_VALUE = .5
COUNT = {s: sum(sum(t) == s for t in product(range(1, 7), repeat=3)) for s in range(3, 19)}

BEATS = [
    Beat('hook', 'hook', 'Gieo ba con xúc xắc. Xác suất tổng số chấm lớn hơn mười là bao nhiêu? Đừng liệt kê hai trăm mười sáu kết quả!'),
    Beat('guess', 'hook', 'Một phần hai, năm phần mười hai, hay bảy phần mười hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo đối xứng: lật mỗi xúc xắc úp xuống, mặt x thành mặt bảy trừ x. Phép lật biến một kết quả đồng khả năng thành một kết quả đồng khả năng khác.'),
    Beat('s2', 'solve', 'Tổng S trở thành hai mươi mốt trừ S. Vậy tổng lớn hơn mười tương ứng một một với tổng nhỏ hơn hoặc bằng mười.'),
    Beat('s3', 'solve', 'Hai biến cố bù nhau và có cùng số kết quả, nên mỗi biến cố có xác suất một phần hai. Biểu đồ phân phối tổng đối xứng quanh mười phẩy năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Tìm phép biến đổi giữ nguyên xác suất, bài đếm biến mất.'),
    Beat('outro', 'outro', outro_text(428)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    flip='x |-> 7 - x, quad S |-> 21 - S',
                    prob='P(S > 10) = P(S <= 10) = 1/2')


def validate() -> bool:
    assert F(sum(c for s, c in COUNT.items() if s > 10), 216) == F(1, 2)
    assert all(COUNT[s] == COUNT[21 - s] for s in COUNT)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS428(ShortScene):
    N = 428

    def hook_visual(self, t0):
        self.board_top = -1.3
        bars = VGroup()
        for s in range(3, 19):
            r = Rectangle(width=.34, height=.09 * COUNT[s], stroke_width=0, fill_color=GOLD if s > 10 else CYAN, fill_opacity=.9)
            r.move_to([-2.7 + .36 * (s - 3), -.2 + r.height / 2, 0])
            bars.add(r)
        labs = VGroup(*[self.TM(f'${s}$', 18, SOFT).next_to(bars[s - 3], DOWN, buff=.06) for s in range(3, 19, 3)])
        self.bars = VGroup(bars, labs)
        self.wait_until(.5, t0)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.write_board(self.M('flip', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.play(FadeIn(self.bars, lag_ratio=.03), run_time=self.rt(.15))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

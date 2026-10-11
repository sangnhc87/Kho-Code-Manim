"""XSS018 · Tổng nào hay gặp nhất? — biểu đồ tam giác 1, 2, …, 6, …, 1: tổng 7."""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

from manim import DOWN, UP, FadeIn, Line, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS018', 'answer': '7'}
PROBLEM = ['Gieo hai con xúc xắc.', 'Tổng nào có xác suất lớn nhất?']
OPTIONS = ['6', '7', '12']
CORRECT = 1
ANSWER_VALUE = None
COUNTS = {s: sum(a + b == s for a, b in product(range(1, 7), repeat=2)) for s in range(2, 13)}

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc và cộng số chấm. Tổng có thể từ hai đến mười hai. '
                         'Tổng nào xuất hiện nhiều nhất?'),
    Beat('guess', 'hook', 'Sáu, bảy, hay mười hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm số cách tạo ra mỗi tổng trong ba mươi sáu kết quả. '
                        'Tổng hai chỉ có một cách: một một. Tổng mười hai cũng chỉ một cách: sáu sáu.'),
    Beat('s2', 'solve', 'Dựng cột cho từng tổng, ta được một hình tam giác rất đẹp: một, hai, ba, bốn, năm, sáu, '
                        'rồi giảm dần năm, bốn, ba, hai, một.'),
    Beat('s3', 'solve', 'Đỉnh tam giác là tổng bảy với sáu cách, xác suất một phần sáu. '
                        'Mười hai là tổng khó ra nhất, chỉ một phần ba mươi sáu.'),
    Beat('answer', 'solve', 'Đáp án: tổng bảy. Nếu chơi cờ tỷ phú, ô cách bạn bảy bước là ô dễ dừng chân nhất!'),
    Beat('outro', 'outro', outro_text(18)),
]

FORMULAS = formulas('7', OPTIONS, peak='P(7) = 6/36 = 1/6', low='P(12) = 1/36')


def validate() -> bool:
    assert max(COUNTS, key=COUNTS.get) == 7 and COUNTS[7] == 6 and COUNTS[2] == COUNTS[12] == 1
    assert [COUNTS[s] for s in range(2, 13)] == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS018(ShortScene):
    N = 18

    def hook_visual(self, t0):
        self.d1 = die(2, 1.4).move_to([-1.2, 1.4, 0])
        self.d2 = die(5, 1.4).move_to([1.2, 1.4, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.1))

    def chart(self):
        base_y, unit, w = -.35, .55, .5
        bars, labs, nums = VGroup(), VGroup(), VGroup()
        for i, s in enumerate(range(2, 13)):
            x = -3.15 + i * .6
            b = Rectangle(width=w, height=COUNTS[s] * unit, fill_color=CYAN, fill_opacity=.85, stroke_width=0)
            b.move_to([x, base_y, 0], aligned_edge=DOWN)
            bars.add(b)
            labs.add(self.MNum(s, 0, SOFT, 22).next_to([x, base_y, 0], DOWN, buff=.12))
            nums.add(self.MNum(COUNTS[s], 0, GOLD, 22).next_to(b, UP, buff=.06))
        axis = Line([-3.55, base_y, 0], [3.25, base_y, 0], color=SOFT, stroke_width=3)
        return bars, labs, nums, axis

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.04))
        self.remove(self.d1, self.d2)
        self.bars, self.labs, self.nums, self.axis = self.chart()
        self.play(FadeIn(self.axis), FadeIn(self.labs, lag_ratio=.05), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.bars[0], shift=UP * .2), FadeIn(self.nums[0]), run_time=self.rt(.06))
        self.wait_until(.75, t0)
        self.play(FadeIn(self.bars[10], shift=UP * .2), FadeIn(self.nums[10]), run_time=self.rt(.06))

    def beat_s2(self, T):
        for i in range(1, 10):
            self.play(FadeIn(self.bars[i], shift=UP * .2), FadeIn(self.nums[i]), run_time=self.rt(.06))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(self.bars[5].animate.set_fill(GOLD, 1), self.nums[5].animate.scale(1.4), run_time=self.rt(.08))
        self.board_top = -1.25
        m = self.M('peak', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.M('low', 1.6), anim='fade')
        self.write_board(tx('đỉnh tam giác', 26, GOLD), anim='fade')

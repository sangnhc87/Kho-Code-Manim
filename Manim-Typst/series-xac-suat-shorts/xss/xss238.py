"""XSS238 · Không ngửa nào, xúc xắc ra mấy? — P(k = 1 | không ngửa) = (1/12)/(21/128) = 32/63."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS238', 'answer': '32/63'}
PROBLEM = ['Gieo xúc xắc được $k$, rồi tung $k$ đồng',
           'xu. Biết không có mặt ngửa nào. Xác',
           'suất xúc xắc đã ra $1$ chấm?']
OPTIONS = ['1/6', '32/63', '1/2']
CORRECT = 1
ANSWER_VALUE = 32 / 63
POST = [F(1, 2) ** k / F(63, 64) for k in range(1, 7)]

BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: bạn chỉ biết không có đồng xu nào ra ngửa. '
                         'Xác suất xúc xắc đã ra một chấm, tức chỉ tung một đồng xu, là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, ba mươi hai phần sáu mươi ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh k bằng một: một phần sáu nhân một phần hai, bằng một phần mười hai. Tổng tất cả các nhánh là hai mươi mốt phần một trăm hai mươi tám.'),
    Beat('s2', 'solve', 'Bayes: một phần mười hai chia hai mươi mốt phần một trăm hai mươi tám, bằng ba mươi hai phần sáu mươi ba, hơn một nửa!'),
    Beat('s3', 'solve', 'Hậu nghiệm giảm một nửa mỗi khi k tăng một: ba mươi hai, mười sáu, tám, bốn, hai, một phần sáu mươi ba. '
                        'Không ngửa nào là bằng chứng mạnh cho việc tung ít đồng xu.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi hai phần sáu mươi ba. Đa hành động: ngược từ kết quả cuối về hành động đầu tiên!'),
    Beat('outro', 'outro', outro_text(238)),
]

FORMULAS = formulas('32/63', OPTIONS,
                    bayes='P(k = 1 | "không ngửa") = (1/12)/(21/128) = 32/63',
                    post='32/63, quad 16/63, quad 8/63, quad dots, quad 1/63')


def validate() -> bool:
    assert POST[0] == F(32, 63) and sum(POST) == 1
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS238(ShortScene):
    N = 238

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.1, 2.9
        self.bars = VGroup()
        for k in range(6):
            r = Rectangle(width=.7, height=h * float(POST[k] / POST[0]), stroke_width=0,
                          fill_color=CORAL if k == 0 else CYAN, fill_opacity=.85)
            r.move_to([-2.75 + 1.1 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'$k = {k + 1}$', 20, SOFT).next_to([-2.75 + 1.1 * k, base, 0], DOWN, buff=.08)
                             for k in range(6)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))

    def beat_s2(self, T):
        m = self.M('bayes', 1.5)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        self.clear_board(.03)
        self.write_board(self.M('post', 1.8))

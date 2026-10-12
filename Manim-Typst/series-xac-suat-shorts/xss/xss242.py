"""XSS242 · Xu bí ẩn: lần ba — P(N₃ | N₁N₂) = (1/8 + 0,729)/(1/4 + 0,81) = 427/530 ≈ 0,806."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS242', 'answer': '427/530 ≈ 0,806'}
PROBLEM = ['Như thử thách trước (xu chuẩn hoặc',
           'xu lệch $"0,9"$), biết $2$ lần đầu đều ngửa.',
           'Xác suất lần $3$ cũng ngửa?']
OPTIONS = ['53/70', '427/530 approx "0,806"', '"0,9"']
CORRECT = 1
ANSWER_VALUE = 427 / 530
P = (F(1, 2), F(9, 10))


def nxt(n):
    return sum(p ** (n + 1) for p in P) / sum(p ** n for p in P)


BEATS = [
    Beat('hook', 'hook', 'Vẫn đồng xu bí ẩn: chuẩn hoặc lệch chín mươi phần trăm. Lần này hai lần đầu đều ra ngửa. '
                         'Xác suất lần ba cũng ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm mươi ba phần bảy mươi, khoảng không phẩy tám không sáu, hay không phẩy chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba lần ngửa: một phần hai nhân không phẩy một hai lăm cộng một phần hai nhân không phẩy bảy hai chín. '
                        'Hai lần ngửa: một phần hai nhân không phẩy hai lăm cộng một phần hai nhân không phẩy tám mốt.'),
    Beat('s2', 'solve', 'Chia: không phẩy tám năm bốn chia một phẩy không sáu, bằng bốn trăm hai mươi bảy phần năm trăm ba mươi, khoảng không phẩy tám không sáu.'),
    Beat('s3', 'solve', 'Dãy dự đoán: không phẩy bảy, rồi không phẩy bảy sáu, rồi không phẩy tám không sáu, tiến dần về không phẩy chín. '
                        'Càng nhiều lần ngửa, ta càng tin mình đang cầm đồng xu lệch.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy tám không sáu. Mỗi lần quan sát là một lần cập nhật niềm tin!'),
    Beat('outro', 'outro', outro_text(242)),
]

FORMULAS = formulas('427/530 approx "0,806"', OPTIONS,
                    prob='P(N_3 | N_1 N_2) = (1/8 + "0,729")/(1/4 + "0,81") = 427/530',
                    seq='"0,7" arrow.r "0,757" arrow.r "0,806" arrow.r "0,9"')


def validate() -> bool:
    assert nxt(2) == F(427, 530) and nxt(1) == F(53, 70) and nxt(0) == F(7, 10)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS242(ShortScene):
    N = 242

    def hook_visual(self, t0):
        self.board_top = -1.3
        base, h = -.05, 2.8
        vals = [nxt(n) for n in range(6)]
        self.bars = VGroup()
        for k, v in enumerate(vals):
            r = Rectangle(width=.7, height=h * (float(v) - .5) / .4, stroke_width=0,
                          fill_color=GOLD if k == 2 else CYAN, fill_opacity=.85)
            r.move_to([-2.75 + 1.1 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'$n = {k}$', 20, SOFT).next_to([-2.75 + 1.1 * k, base, 0], DOWN, buff=.08)
                             for k in range(6)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), *[GrowFromEdge(b, DOWN) for b in self.bars[:2]], run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('prob', 1.5))

    def beat_s2(self, T):
        self.play(GrowFromEdge(self.bars[2], DOWN), run_time=self.rt(.08))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars[3:]], run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.write_board(self.M('seq', 1.7))



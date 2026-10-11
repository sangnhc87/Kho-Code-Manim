"""XSS190 · Đoán bừa 10 câu — Bernoulli n = 10, p = 1/4: P(X ≥ 5) ≈ 0,078."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS190', 'answer': '≈ 0,078'}
PROBLEM = ['Đề $10$ câu, mỗi câu $4$ phương án; đoán bừa',
           'tất cả. Xác suất đúng ít nhất $5$ câu?']
OPTIONS = ['"0,5"', 'approx "0,078"', 'approx "0,25"']
CORRECT = 1
ANSWER_VALUE = .078
P = [comb(10, k) * F(1, 4) ** k * F(3, 4) ** (10 - k) for k in range(11)]

BEATS = [
    Beat('hook', 'hook', 'Một bạn không học bài, đoán bừa cả mười câu trắc nghiệm, mỗi câu bốn phương án. '
                         'Xác suất bạn ấy đúng từ năm câu trở lên, tức đạt điểm trung bình, là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy năm, khoảng không phẩy không bảy tám, hay khoảng không phẩy hai lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi câu là một phép thử Bernoulli với xác suất đúng một phần tư. Số câu đúng có phân phối nhị thức với n bằng mười.'),
    Beat('s2', 'solve', 'Xác suất đúng k câu bằng tổ hợp chập k của mười, nhân một phần tư mũ k, nhân ba phần tư mũ mười trừ k. '
                        'Biểu đồ dồn hết về phía hai, ba câu đúng.'),
    Beat('s3', 'solve', 'Cộng từ năm đến mười được khoảng không phẩy không bảy tám. Chưa tới tám phần trăm cơ hội đạt trung bình.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy không bảy tám. Đoán bừa gần như chắc chắn trượt, học bài vẫn là chiến thuật tốt nhất!'),
    Beat('outro', 'outro', outro_text(190)),
]

FORMULAS = formulas('approx "0,078"', OPTIONS,
                    pk='P(X = k) = C_10^k (1/4)^k (3/4)^(10 - k)',
                    tot='P(X >= 5) = sum_(k = 5)^10 P(X = k) approx "0,078"')


def validate() -> bool:
    assert sum(P) == 1 and round(float(sum(P[5:])), 3) == .078
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS190(ShortScene):
    N = 190

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.35, 3.1
        top = float(max(P))
        self.bars = VGroup()
        for k in range(11):
            r = Rectangle(width=.5, height=max(.03, h * float(P[k]) / top), stroke_width=0,
                          fill_color=GOLD if k >= 5 else CYAN, fill_opacity=.85)
            r.move_to([-3.0 + .6 * k, base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k}$', 20, SOFT).next_to([-3.0 + .6 * k, base, 0], DOWN, buff=.08) for k in range(11)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('pk', 1.7))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(*[b.animate.set_stroke(CORAL, 4) for b in self.bars[5:]], run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('tot', 1.7)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)

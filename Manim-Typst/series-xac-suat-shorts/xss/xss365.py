"""XSS365 · Có đỏ thì hai xu ngửa? — P(k = 2 | ≥ 1 đỏ) = (1/4 · 19/20)/(61/80) = 19/61."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, SurroundingRectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from xss.xss364 import ANY, BRANCHES, PK  # noqa: E402

EPISODE = {'code': 'XSS365', 'answer': '19/61'}
PROBLEM = ['Tung $2$ xu được $k$ ngửa, rút $k + 1$ bi từ',
           'hộp $3$ đỏ $3$ xanh. Biết có ít nhất $1$ bi',
           'đỏ. Xác suất cả hai xu đều ngửa?']
OPTIONS = ['1/4', '19/61', '19/80']
CORRECT = 1
ANSWER_VALUE = 19 / 61

BEATS = [
    Beat('hook', 'hook', 'Tiếp bài trước: tung hai xu được k ngửa, rút k cộng một bi từ hộp ba đỏ ba xanh. Biết có ít nhất một bi đỏ. '
                         'Xác suất cả hai xu đều ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, mười chín phần sáu mươi mốt, hay mười chín phần tám mươi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẫu số đã có từ bài trước: xác suất có ít nhất một bi đỏ bằng sáu mươi mốt phần tám mươi.'),
    Beat('s2', 'solve', 'Nhánh hai ngửa: một phần tư nhân mười chín phần hai mươi, bằng mười chín phần tám mươi.'),
    Beat('s3', 'solve', 'Chia hai số: mười chín phần sáu mươi mốt, khoảng ba mươi mốt phần trăm, cao hơn một phần tư ban đầu.'),
    Beat('answer', 'solve', 'Đáp án: mười chín phần sáu mươi mốt. Rút nhiều bi thì dễ có đỏ, nên có đỏ là bằng chứng nghiêng về nhiều ngửa.'),
    Beat('outro', 'outro', outro_text(365)),
]

FORMULAS = formulas('19/61', OPTIONS,
                    den='P("có đỏ") = 61/80',
                    num='1/4 dot 19/20 = 19/80',
                    prob='P(k = 2 | "có đỏ") = (19/80)/(61/80) = 19/61')


def validate() -> bool:
    total = sum(p * a for p, a in zip(PK, ANY))
    assert PK[2] * ANY[2] / total == F(19, 61)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS365(TreeMixin, ShortScene):
    N = 365

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=6.4, r=.34, edge_size=28)
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('den', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(SurroundingRectangle(self.leaves[2][0], color=GOLD, buff=.08)), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.write_board(self.M('num', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

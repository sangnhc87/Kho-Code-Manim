"""XSS383 · Số lần rút là số chẵn — r = 2/5, q = 3/5; P(chẵn) = rq/(1 − q²) = 3/8; P(T = 2) = qr = 6/25 → 16/25."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402

EPISODE = {'code': 'XSS383', 'answer': '16/25'}
PROBLEM = ['Rút có hoàn lại từ hộp $2$ đỏ $3$ xanh',
           'đến khi được đỏ. Biết số lần rút là số',
           'chẵn. Xác suất rút đúng $2$ lần?']
OPTIONS = ['16/25', '3/5', '6/25']
CORRECT = 0
ANSWER_VALUE = 16 / 25
R, Q = F(2, 5), F(3, 5)
EVEN = R * Q / (1 - Q ** 2)
BRANCHES = [('Đ', CORAL, '2/5', []),
            ('X', CYAN, '3/5', [('Đ', CORAL, '2/5', []),
                                ('X', CYAN, '3/5', [('Đ', CORAL, '2/5', []), ('X', CYAN, '3/5', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Rút có hoàn lại từ hộp hai đỏ ba xanh cho đến khi được bi đỏ. Biết số lần rút là một số chẵn. '
                         'Xác suất đã rút đúng hai lần là bao nhiêu?'),
    Beat('guess', 'hook', 'Mười sáu phần hai mươi lăm, ba phần năm, hay sáu phần hai mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dừng ở lần k với xác suất ba phần năm mũ k trừ một nhân hai phần năm. Dừng ở lần hai: ba phần năm nhân hai phần năm, sáu phần hai mươi lăm.'),
    Beat('s2', 'solve', 'Các lần chẵn hai, bốn, sáu và cứ thế tạo cấp số nhân công bội chín phần hai mươi lăm. Tổng bằng sáu phần hai mươi lăm chia mười sáu phần hai mươi lăm, tức ba phần tám.'),
    Beat('s3', 'solve', 'Xác suất có điều kiện: sáu phần hai mươi lăm chia ba phần tám, bằng mười sáu phần hai mươi lăm.'),
    Beat('answer', 'solve', 'Đáp án: mười sáu phần hai mươi lăm. Cây dừng vô hạn: dùng tổng cấp số nhân để gom các lá.'),
    Beat('outro', 'outro', outro_text(383)),
]

FORMULAS = formulas('16/25', OPTIONS,
                    t2='P(T = 2) = 3/5 dot 2/5 = 6/25',
                    even='P("chẵn") = (6/25)/(1 - 9/25) = 3/8',
                    prob='P(T = 2 | "chẵn") = (6/25)/(3/8) = 16/25')


def validate() -> bool:
    approx = sum(Q ** (k - 1) * R for k in range(2, 200, 2))
    assert EVEN == F(3, 8) and abs(float(approx - EVEN)) < 1e-12
    assert Q * R / EVEN == F(16, 25)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS383(TreeMixin, ShortScene):
    N = 383

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.15, width=5.4, r=.32, edge_size=24)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[FadeIn(lv) for lv in self.levels[2:]], run_time=self.rt(.12))
        self.wait_until(.55, t0)
        self.write_board(self.M('t2', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('even', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

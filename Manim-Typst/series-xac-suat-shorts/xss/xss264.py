"""XSS264 · Chọn hộp I với xác suất p — 3p/(3p + (1 − p)) = 0,9 ⇒ p = 0,75."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS264', 'answer': 'p = 0,75'}
PROBLEM = ['Hộp I: $3$ đỏ $1$ xanh; II: $1$ đỏ $3$ xanh;',
           'chọn hộp I với xác suất $p$. Rút được',
           'đỏ thì $P("hộp I") = "0,9"$. Tìm $p$.']
OPTIONS = ['p = "0,5"', 'p = "0,75"', 'p = "0,9"']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('I', GOLD, 'p', [('Đ', CORAL, '3/4', [])]),
            ('II', PURPLE, '1 - p', [('Đ', CORAL, '1/4', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp một có ba đỏ một xanh, hộp hai có một đỏ ba xanh. Người chơi chọn hộp một với xác suất p. '
                         'Biết khi rút được đỏ thì chín mươi phần trăm là từ hộp một. Tìm p.'),
    Beat('guess', 'hook', 'Không phẩy năm, không phẩy bảy lăm, hay không phẩy chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai lá "đỏ": hộp một, ba phần tư p; hộp hai, một phần tư nhân một trừ p. Bayes cho hộp một: ba p chia ba p cộng một trừ p.'),
    Beat('s2', 'solve', 'Đặt bằng không phẩy chín: ba p bằng không phẩy chín nhân hai p cộng một, ba p bằng một phẩy tám p cộng không phẩy chín.'),
    Beat('s3', 'solve', 'Một phẩy hai p bằng không phẩy chín, p bằng không phẩy bảy lăm. Muốn hậu nghiệm chín mươi phần trăm thì tiên nghiệm phải ba phần tư.'),
    Beat('answer', 'solve', 'Đáp án: p bằng không phẩy bảy lăm. Bayes ngược: từ hậu nghiệm tìm lại tiên nghiệm!'),
    Beat('outro', 'outro', outro_text(264)),
]

FORMULAS = formulas('p = "0,75"', OPTIONS,
                    bayes='P(I | Đ) = (3 p)/(3 p + (1 - p)) = (3 p)/(2 p + 1)',
                    sol='(3 p)/(2 p + 1) = "0,9" arrow.r.double p = "0,75"')


def validate() -> bool:
    assert [F(k, 100) for k in range(101) if 3 * F(k, 100) / (2 * F(k, 100) + 1) == F(9, 10)] == [F(3, 4)]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS264(TreeMixin, ShortScene):
    N = 264

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='chọn hộp')
        self.wait_until(.8, t0)
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('bayes', 1.6))

    def beat_s2(self, T):
        m = self.M('sol', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('hậu nghiệm $"0,9"$ ⇐ tiên nghiệm $"0,75"$', 26, GOLD), anim='fade')

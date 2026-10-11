"""XSS226 · Bi bị giấu đi — cất 1 bi không xem, rút tiếp: P(đỏ) = 3/5 · 2/4 + 2/5 · 3/4 = 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS226', 'answer': '3/5'}
PROBLEM = ['Hộp $3$ đỏ $2$ xanh. Lấy $1$ bi cất đi',
           'không xem, rồi rút $1$ bi từ hộp.',
           'Xác suất bi rút ra màu đỏ?']
OPTIONS = ['1/2', '3/5', '2/3']
CORRECT = 1
ANSWER_VALUE = .6
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [('?Đ', SOFT, '3/5', [(*D, '2/4', [])]),
            ('?X', SOFT, '2/5', [(*D, '3/4', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có ba đỏ hai xanh. Bạn của bạn lấy một bi cất vào túi mà không ai nhìn thấy. '
                         'Bạn rút một bi từ hộp. Xác suất được bi đỏ có còn là ba phần năm không?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần năm, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhiều người cho rằng hộp đã thay đổi nên xác suất phải khác. Vẽ cây: bi bị giấu là đỏ ba phần năm, xanh hai phần năm.'),
    Beat('s2', 'solve', 'Giấu đỏ: hộp còn hai đỏ hai xanh, rút đỏ hai phần tư. Giấu xanh: còn ba đỏ một xanh, rút đỏ ba phần tư.'),
    Beat('s3', 'solve', 'Toàn phần: ba phần năm nhân hai phần tư cộng hai phần năm nhân ba phần tư, bằng sáu cộng sáu trên hai mươi, đúng ba phần năm!'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Một bi bị giấu không ai biết màu thì không mang thông tin, xác suất giữ nguyên!'),
    Beat('outro', 'outro', outro_text(226)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    tot='P = 3/5 dot 2/4 + 2/5 dot 3/4 = 12/20 = 3/5')


def validate() -> bool:
    seqs = list(permutations('RRRBB', 2))
    assert F(sum(s[1] == 'R' for s in seqs), len(seqs)) == F(3, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS226(TreeMixin, ShortScene):
    N = 226

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='bi bị giấu')
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(*[n.animate.scale(1.25) for n, _ in self.leaves], run_time=self.rt(.04))

    def beat_s3(self, T):
        m = self.M('tot', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)

"""XSS295 · Ếch lười — trái 1/4, phải 1/4, đứng 1/2; về chỗ sau 2 giây: (1/2)² + 2·(1/4)(1/4) = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS295', 'answer': '3/8'}
PROBLEM = ['Mỗi giây ếch nhảy trái ($1/4$), nhảy phải',
           '($1/4$) hoặc đứng yên ($1/2$). Xác suất sau',
           '$2$ giây ếch ở đúng chỗ cũ?']
OPTIONS = ['1/4', '3/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 3 / 8
L, S, R = ('T', CORAL, '1/4'), ('Đ', SOFT, '1/2'), ('P', CYAN, '1/4')
BRANCHES = [(*L, [(*R[:2], R[2], [])]), (*S, [(*S[:2], S[2], [])]), (*R, [(*L[:2], L[2], [])])]

BEATS = [
    Beat('hook', 'hook', 'Một chú ếch lười: mỗi giây nhảy sang trái một phần tư, sang phải một phần tư, còn một nửa thời gian thì đứng yên. '
                         'Sau hai giây, xác suất ếch ở đúng chỗ cũ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, ba phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Về chỗ cũ sau hai giây có ba cách: đứng yên cả hai giây; trái rồi phải; phải rồi trái. Cây chỉ cần ba nhánh đó.'),
    Beat('s2', 'solve', 'Đứng đứng: một phần hai bình phương, một phần tư. Trái phải: một phần tư nhân một phần tư, một phần mười sáu; phải trái cũng vậy.'),
    Beat('s3', 'solve', 'Tổng: bốn phần mười sáu cộng hai phần mười sáu, bằng sáu phần mười sáu, tức ba phần tám. Lưu ý đây đúng bằng xác suất về gốc sau bốn bước của ếch thường!'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Có bước "đứng yên" thì cây ba nhánh mỗi tầng: liệt kê đường quay về!'),
    Beat('outro', 'outro', outro_text(295)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    ways='Đ Đ: 1/4, quad T P: 1/16, quad P T: 1/16',
                    tot='P = 4/16 + 1/16 + 1/16 = 3/8')


def validate() -> bool:
    step = {-1: F(1, 4), 0: F(1, 2), 1: F(1, 4)}
    assert sum(step[a] * step[b] for a, b in product(step, repeat=2) if a + b == 0) == F(3, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS295(TreeMixin, ShortScene):
    N = 295

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=6.0)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[n.animate.scale(1.3) for n, _ in self.leaves], run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.write_board(self.M('ways', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)



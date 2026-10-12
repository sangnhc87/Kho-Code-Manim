"""XSS291 · Ếch quen hướng — cách gốc 3 sau 3 bước ⇔ cả 3 cùng chiều: 2 · 1/2 · (2/3)² = 4/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS291', 'answer': '4/9'}
PROBLEM = ['Bước đầu ếch nhảy $+1$ hoặc $-1$ ($1/2$); từ',
           'bước sau, ếch giữ hướng cũ với xác suất',
           '$2/3$. Xác suất sau $3$ bước cách gốc $3$?']
OPTIONS = ['1/4', '4/9', '1/3']
CORRECT = 1
ANSWER_VALUE = 4 / 9
R, L = ('+', CYAN), ('−', CORAL)
BRANCHES = [(*R, '1/2', [(*R, '2/3', [(*R, '2/3', [])])]),
            (*L, '1/2', [(*L, '2/3', [(*L, '2/3', [])])])]


def prob(w):
    p = F(1, 2)
    for a, b in zip(w, w[1:]):
        p *= F(2, 3) if a == b else F(1, 3)
    return p


BEATS = [
    Beat('hook', 'hook', 'Chú ếch có thói quen: bước đầu chọn trái hoặc phải ngẫu nhiên, nhưng từ bước sau thì giữ nguyên hướng cũ với xác suất hai phần ba. '
                         'Sau ba bước, xác suất ếch cách gốc ba đơn vị là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, bốn phần chín, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Các bước không độc lập: mỗi bước phụ thuộc bước ngay trước. Cách gốc ba sau ba bước nghĩa là ba bước cùng một chiều.'),
    Beat('s2', 'solve', 'Nhánh toàn phải: một phần hai nhân hai phần ba nhân hai phần ba, bằng hai phần chín. Nhánh toàn trái cũng hai phần chín.'),
    Beat('s3', 'solve', 'Tổng bốn phần chín, gần gấp đôi một phần tư của chú ếch không có thói quen. Trí nhớ làm ếch đi xa hơn.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần chín. Khi bước sau phụ thuộc bước trước, ghi xác suất có điều kiện trên từng nhánh!'),
    Beat('outro', 'outro', outro_text(291)),
]

FORMULAS = formulas('4/9', OPTIONS,
                    one='P(+ + +) = 1/2 dot 2/3 dot 2/3 = 2/9',
                    tot='P = 2 dot 2/9 = 4/9 > 1/4')


def validate() -> bool:
    assert sum(prob(w) for w in product('+-', repeat=3) if len(set(w)) == 1) == F(4, 9)
    assert sum(prob(w) for w in product('+-', repeat=3)) == 1
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS291(TreeMixin, ShortScene):
    N = 291

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.15, width=5.6, root_label='bước 1', r=.38)
        self.wait_until(.8, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s2(self, T):
        self.write_board(self.M('one', 1.8))

    def beat_s3(self, T):
        m = self.M('tot', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)

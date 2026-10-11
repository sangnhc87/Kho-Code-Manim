"""XSS121 · Ba phát, trúng đúng hai — cây 3 tầng 8 lá, 3 lá thỏa, mỗi lá 0,6²·0,4: 0,432."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS121', 'answer': '0,432'}
PROBLEM = ['Xạ thủ bắn $3$ phát, mỗi phát trúng',
           'với xác suất $"0,6"$, độc lập. Xác',
           'suất trúng đúng $2$ phát?']
OPTIONS = ['"0,36"', '"0,432"', '"0,648"']
CORRECT = 1
ANSWER_VALUE = .432


def shot(depth):
    if depth == 0:
        return []
    return [('T', GREEN, '"0,6"', shot(depth - 1)), ('X', CORAL, '"0,4"', shot(depth - 1))]


BRANCHES = shot(3)

BEATS = [
    Beat('hook', 'hook', 'Một xạ thủ bắn ba phát, mỗi phát trúng với xác suất không phẩy sáu, các phát độc lập. '
                         'Xác suất anh ấy trúng đúng hai phát là bao nhiêu? Ta vẽ cây ba tầng.'),
    Beat('guess', 'hook', 'Không phẩy ba sáu, không phẩy bốn ba hai, hay không phẩy sáu bốn tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi phát tách thành hai nhánh: trúng không phẩy sáu, trượt không phẩy bốn. '
                        'Ba phát cho cây ba tầng với tám lá, mỗi lá là một kịch bản.'),
    Beat('s2', 'solve', 'Tìm các lá có đúng hai chữ T: trúng trúng trượt, trúng trượt trúng, trượt trúng trúng. '
                        'Nhân dọc mỗi nhánh: không phẩy sáu bình phương nhân không phẩy bốn, bằng không phẩy một bốn bốn.'),
    Beat('s3', 'solve', 'Ba lá cùng xác suất, cộng lại được không phẩy bốn ba hai. '
                        'Số lá chính là tổ hợp chập hai của ba: đây là công thức Bernoulli.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bốn ba hai. Nhân dọc theo nhánh, cộng ngang các lá: hai quy tắc vàng của sơ đồ cây!'),
    Beat('outro', 'outro', outro_text(121)),
]

FORMULAS = formulas('"0,432"', OPTIONS,
                    leaf='P(T T X) = "0,6"^2 dot "0,4" = "0,144"',
                    tot='P = 3 dot "0,144" = "0,432"',
                    bern='C_3^2 dot "0,6"^2 dot "0,4" = "0,432"')


def validate() -> bool:
    p = sum(F(3, 5) ** w.count('T') * F(2, 5) ** w.count('X') for w in product('TX', repeat=3) if w.count('T') == 2)
    assert p == F(54, 125) and float(p) == .432
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS121(TreeMixin, ShortScene):
    N = 121

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.1), dy=1.3, width=7.4, root_label='bắn', r=.3,
                                                  edge_size=24)
        self.wait_until(.55, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[3], lag_ratio=.08), run_time=self.rt(.2))
        self.play(FadeIn(tx('T: trúng   X: trượt', 24, SOFT).move_to([0, -.95, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        good = [n for n, path in self.leaves if [b[0] for b in path].count('T') == 2]
        self.play(*[n.animate.scale(1.35) for n in good], run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.write_board(self.M('leaf', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('tot', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('bern', 1.7), anim='fade')



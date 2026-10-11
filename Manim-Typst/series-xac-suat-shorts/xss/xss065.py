"""XSS065 · Rút liên tiếp 2 đỏ — 5 đỏ 3 xanh, không hoàn lại: 5/8 · 4/7 = 5/14 (cây có trọng số)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import DOWN, FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402
from common.visuals import BALL_COLORS  # noqa: E402

EPISODE = {'code': 'XSS065', 'answer': '5/14'}
PROBLEM = ['Hộp $5$ bi đỏ, $3$ bi xanh. Rút lần',
           'lượt $2$ bi không hoàn lại. Xác',
           'suất cả hai bi đều đỏ?']
OPTIONS = ['25/64', '5/14', '5/8']
CORRECT = 1
ANSWER_VALUE = 5 / 14
BALLS = 'RRRRRBBB'
RED, BLUE = BALL_COLORS['R'], BALL_COLORS['B']
BRANCHES = [('Đ', RED, '5/8', [('Đ', RED, '4/7', []), ('X', BLUE, '3/7', [])]),
            ('X', BLUE, '3/8', [('Đ', RED, '5/7', []), ('X', BLUE, '2/7', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đỏ và ba bi xanh. Rút lần lượt hai viên, rút xong không bỏ lại. '
                         'Xác suất cả hai viên đều đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai mươi lăm phần sáu mươi tư, năm phần mười bốn, hay năm phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ sơ đồ cây có trọng số. Lần một: đỏ với xác suất năm phần tám, xanh ba phần tám.'),
    Beat('s2', 'solve', 'Lần hai phụ thuộc lần một. Nếu lần một ra đỏ, hộp còn bốn đỏ trong bảy viên: '
                        'xác suất đỏ có điều kiện là bốn phần bảy.'),
    Beat('s3', 'solve', 'Công thức nhân xác suất: nhân dọc theo nhánh đỏ đỏ, năm phần tám nhân bốn phần bảy, '
                        'bằng năm phần mười bốn. Hai mươi lăm phần sáu mươi tư là đáp án nếu rút có hoàn lại.'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười bốn. Trên cây xác suất: nhân dọc theo nhánh!'),
    Beat('outro', 'outro', outro_text(65)),
]

FORMULAS = formulas('5/14', OPTIONS,
                    rule='P(A B) = P(A) dot P(B|A)',
                    prob='P = 5/8 dot 4/7 = 5/14')


def validate() -> bool:
    perms = list(permutations(range(8), 2))
    assert F(sum(BALLS[a] == BALLS[b] == 'R' for a, b in perms), len(perms)) == F(5, 14) == F(5, 8) * F(4, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS065(TreeMixin, ShortScene):
    N = 65

    def hook_visual(self, t0):
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='rút')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.2))
        self.play(FadeIn(tx('lần 1', 22, SOFT).move_to([-3.6, 3.2 - 1.6, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.15), FadeIn(tx('lần 2', 22, SOFT).move_to([-3.6, 3.2 - 3.2, 0])),
                  run_time=self.rt(.2))
        self.wait_until(.55, t0)
        self.board_top = -1.0
        self.write_board(self.M('rule', 1.7))

    def beat_s3(self, T):
        t0 = self.now()
        leaf = self.leaves[0][0]
        self.play(leaf.animate.scale(1.3), run_time=self.rt(.05))
        self.play(FadeIn(tx('ĐĐ', 26, GOLD, bold=True).next_to(leaf, DOWN, buff=.1)), run_time=self.rt(.04))
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('25/64: chỉ khi có hoàn lại', 26, CORAL), anim='fade')



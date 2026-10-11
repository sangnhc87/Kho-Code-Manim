"""XSS201 · Mỗi hộp một bi — cùng màu: 3/5·2/6 + 2/5·4/6 = 14/30 = 7/15."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS201', 'answer': '7/15'}
PROBLEM = ['Hộp I: $3$ đỏ $2$ xanh; hộp II: $2$',
           'đỏ $4$ xanh. Rút mỗi hộp $1$ bi. Xác',
           'suất hai bi cùng màu?']
OPTIONS = ['1/2', '7/15', '8/15']
CORRECT = 1
ANSWER_VALUE = 7 / 15
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '3/5', [(*D, '2/6', []), (*X, '4/6', [])]),
            (*X, '2/5', [(*D, '2/6', []), (*X, '4/6', [])])]

BEATS = [
    Beat('hook', 'hook', 'Mở đầu nhánh bốc bi nhiều hộp. Hộp một có ba đỏ hai xanh, hộp hai có hai đỏ bốn xanh. '
                         'Rút mỗi hộp một bi. Xác suất hai bi cùng màu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, bảy phần mười lăm, hay tám phần mười lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai hộp rút độc lập. Cây hai tầng: tầng một là bi từ hộp một, tầng hai là bi từ hộp hai.'),
    Beat('s2', 'solve', 'Cùng màu có hai lá: đỏ đỏ, ba phần năm nhân hai phần sáu bằng sáu phần ba mươi; '
                        'xanh xanh, hai phần năm nhân bốn phần sáu bằng tám phần ba mươi.'),
    Beat('s3', 'solve', 'Cộng lại: mười bốn phần ba mươi, tức bảy phần mười lăm. Nhớ giữ hai lá này, thử thách sau sẽ dùng tới!'),
    Beat('answer', 'solve', 'Đáp án: bảy phần mười lăm. Thử thách tiếp: biết hai bi cùng màu, xác suất cả hai đều đỏ?'),
    Beat('outro', 'outro', outro_text(201)),
]

FORMULAS = formulas('7/15', OPTIONS,
                    rr='3/5 dot 2/6 = 6/30',
                    bb='2/5 dot 4/6 = 8/30',
                    tot='P = 6/30 + 8/30 = 7/15')


def validate() -> bool:
    assert F(sum(a == b for a, b in product('RRRBB', 'RRBBBB')), 30) == F(7, 15)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS201(TreeMixin, ShortScene):
    N = 201

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.urns = urn_row([('RRRBB', 'hộp I', GOLD), ('RRBBBB', 'hộp II', PURPLE)])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='hộp I')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        same = [self.leaves[0][0], self.leaves[3][0]]
        diff = [self.leaves[1][0], self.leaves[2][0]]
        self.play(*[n.animate.set_opacity(.15) for n in diff], *[n.animate.scale(1.3) for n in same], run_time=self.rt(.06))
        self.write_board(self.M('rr', 2.0))
        self.wait_until(.5, t0)
        self.write_board(self.M('bb', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 2.1)
        self.write_board(m)
        self.frame(m)

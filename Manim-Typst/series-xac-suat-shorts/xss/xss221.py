"""XSS221 · Chuyển hai, rút hai — I (3Đ3X) → II (2Đ2X) 2 bi, rút 2 từ II cùng màu: 32/75."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS221', 'answer': '32/75'}
PROBLEM = ['Hộp I: $3$ đỏ $3$ xanh; II: $2$ đỏ $2$ xanh.',
           'Chuyển $2$ bi I → II, rồi rút $2$ bi từ II.',
           'Xác suất hai bi rút ra cùng màu?']
OPTIONS = ['2/5', '32/75', '7/15']
CORRECT = 1
ANSWER_VALUE = 32 / 75
BRANCHES = [('ĐĐ', CORAL, '3/15', [('=', GOLD, '7/15', [])]),
            ('ĐX', PURPLE, '9/15', [('=', GOLD, '6/15', [])]),
            ('XX', CYAN, '3/15', [('=', GOLD, '7/15', [])])]


def same(box):
    p = list(combinations(box, 2))
    return F(sum(a == b for a, b in p), len(p))


BEATS = [
    Beat('hook', 'hook', 'Hộp một có ba đỏ ba xanh, hộp hai có hai đỏ hai xanh. Chuyển hai bi từ hộp một sang hộp hai, '
                         'rồi rút hai bi từ hộp hai. Xác suất hai bi rút ra cùng màu là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, ba mươi hai phần bảy mươi lăm, hay bảy phần mười lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chuyển hai bi có ba khả năng: hai đỏ, một đỏ một xanh, hai xanh. Xác suất: ba phần mười lăm, chín phần mười lăm, ba phần mười lăm.'),
    Beat('s2', 'solve', 'Hộp hai lúc đó có sáu bi. Chuyển hai đỏ: bốn đỏ hai xanh, cùng màu sáu cộng một trên mười lăm, bảy phần mười lăm. '
                        'Chuyển một đỏ một xanh: ba đỏ ba xanh, sáu phần mười lăm. Chuyển hai xanh: đối xứng, bảy phần mười lăm.'),
    Beat('s3', 'solve', 'Toàn phần: ba nhân bảy cộng chín nhân sáu cộng ba nhân bảy, chia hai trăm hai mươi lăm, bằng chín mươi sáu phần hai trăm hai mươi lăm, '
                        'tức ba mươi hai phần bảy mươi lăm.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi hai phần bảy mươi lăm. Chuyển nhiều bi thì tầng một của cây có nhiều nhánh, mỗi nhánh tính bằng tổ hợp!'),
    Beat('outro', 'outro', outro_text(221)),
]

FORMULAS = formulas('32/75', OPTIONS,
                    move='P(Đ Đ) = P(X X) = 3/15',
                    lik='7/15, quad 6/15, quad 7/15',
                    tot='P = (3 dot 7 + 9 dot 6 + 3 dot 7)/225 = 32/75')


def validate() -> bool:
    total = F(0)
    for m in combinations(range(6), 2):
        moved = ''.join('RRRBBB'[i] for i in m)
        total += F(1, comb(6, 2)) * same('RRBB' + moved)
    assert total == F(32, 75)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS221(TreeMixin, ShortScene):
    N = 221

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=6.8, root_label='chuyển 2 bi')
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.45, t0)
        self.write_board(self.M('move', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('lik', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.7)
        self.write_board(m)
        self.frame(m)

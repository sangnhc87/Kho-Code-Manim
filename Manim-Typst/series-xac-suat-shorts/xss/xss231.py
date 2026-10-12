"""XSS231 · Chuyển hai vào hộp toàn xanh — I (4Đ2X) → II (2X) 2 bi, rút II được đỏ: P(chuyển đúng 1 đỏ) = 2/5."""
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

EPISODE = {'code': 'XSS231', 'answer': '2/5'}
PROBLEM = ['Chuyển $2$ bi từ I ($4$ đỏ $2$ xanh) sang II',
           '($2$ xanh), rút $1$ bi từ II được đỏ. Xác',
           'suất đúng $1$ bi đỏ đã được chuyển?']
OPTIONS = ['8/15', '2/5', '1/2']
CORRECT = 1
ANSWER_VALUE = .4
BRANCHES = [('ĐĐ', CORAL, '6/15', [('Đ', GOLD, '2/4', [])]),
            ('ĐX', PURPLE, '8/15', [('Đ', GOLD, '1/4', [])]),
            ('XX', CYAN, '1/15', [('Đ', GOLD, '0', [])])]


def posterior():
    num = den = F(0)
    for m in combinations(range(6), 2):
        moved = ''.join('RRRRBB'[i] for i in m)
        p = F(1, comb(6, 2)) * F(moved.count('R'), 4)
        den += p
        num += p * (moved.count('R') == 1)
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Hộp hai chỉ có hai bi xanh. Chuyển hai bi từ hộp một có bốn đỏ hai xanh sang hộp hai, rồi rút một bi từ hộp hai, được đỏ. '
                         'Xác suất đúng một bi đỏ đã được chuyển là bao nhiêu?'),
    Beat('guess', 'hook', 'Tám phần mười lăm, hai phần năm, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chuyển hai đỏ: sáu phần mười lăm. Một đỏ một xanh: tám phần mười lăm. Hai xanh: một phần mười lăm. Hộp hai lúc đó có bốn bi.'),
    Beat('s2', 'solve', 'Rút đỏ: nhánh hai đỏ hai phần tư, nhánh một đỏ một phần tư, nhánh hai xanh bằng không. '
                        'Nhân lại: mười hai phần sáu mươi và tám phần sáu mươi.'),
    Beat('s3', 'solve', 'Bayes: tám chia mười hai cộng tám, bằng hai phần năm. Dù nhánh một đỏ phổ biến nhất, rút được đỏ lại nghiêng về nhánh hai đỏ.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Hộp nhận "sạch" một màu thì màu kia chỉ có thể đến từ bi được chuyển!'),
    Beat('outro', 'outro', outro_text(231)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    w='6/15 dot 2/4 = 12/60, quad 8/15 dot 1/4 = 8/60',
                    bayes='P("1 đỏ" | Đ) = 8/(12 + 8) = 2/5')


def validate() -> bool:
    assert posterior() == F(2, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS231(TreeMixin, ShortScene):
    N = 231

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=6.8, root_label='chuyển 2 bi')
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.play(self.leaves[2][0].animate.set_opacity(.15), run_time=self.rt(.03))
        self.wait_until(.45, t0)
        self.write_board(self.M('w', 1.6))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m)

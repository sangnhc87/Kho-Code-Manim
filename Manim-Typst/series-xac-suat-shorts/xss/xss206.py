"""XSS206 · Bi thứ hai cùng hộp — biết bi 1 đỏ: P(I) = 4/5, P(II) = 1/5; P(bi 2 đỏ) = 4/5·3/4 + 1/5·0 = 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PURPLE  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS206', 'answer': '3/5'}
PROBLEM = ['Hộp I: $4$ đỏ $1$ xanh; II: $1$ đỏ $4$ xanh.',
           'Tung xu chọn hộp, rút được đỏ; rút tiếp',
           'cùng hộp. Xác suất bi thứ hai cũng đỏ?']
OPTIONS = ['1/2', '3/5', '17/25']
CORRECT = 1
ANSWER_VALUE = .6
BRANCHES = [('I', GOLD, '4/5', [('Đ', CORAL, '3/4', [])]),
            ('II', PURPLE, '1/5', [('Đ', CORAL, '0', [])])]


def second_red():
    num = den = F(0)
    for box in ('RRRRB', 'RBBBB'):
        for a, b in permutations(box, 2):
            pr = F(1, 2) * F(1, 20)
            if a == 'R':
                den += pr
                num += pr * (b == 'R')
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Hộp một có bốn đỏ một xanh, hộp hai có một đỏ bốn xanh. Tung xu chọn hộp, rút một bi được đỏ. '
                         'Rút tiếp bi thứ hai từ cùng hộp, không hoàn lại. Xác suất bi thứ hai cũng đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần năm, hay mười bảy phần hai mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bước một: cập nhật niềm tin. Rút đỏ từ hộp một có xác suất bốn phần năm, từ hộp hai một phần năm. '
                        'Bayes cho hộp một bốn phần năm, hộp hai một phần năm.'),
    Beat('s2', 'solve', 'Bước hai: rút tiếp. Nếu là hộp một, còn ba đỏ một xanh, đỏ ba phần tư. Nếu là hộp hai, bi đỏ duy nhất đã bị rút, đỏ bằng không.'),
    Beat('s3', 'solve', 'Toàn phần: bốn phần năm nhân ba phần tư cộng một phần năm nhân không, bằng ba phần năm.'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Đa hành động có điều kiện: cập nhật bằng Bayes trước, rồi mới tính bước tiếp theo!'),
    Beat('outro', 'outro', outro_text(206)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    upd='P(I | Đ_1) = (1/2 dot 4/5)/(1/2 dot 4/5 + 1/2 dot 1/5) = 4/5',
                    tot='P(Đ_2 | Đ_1) = 4/5 dot 3/4 + 1/5 dot 0 = 3/5')


def validate() -> bool:
    assert second_red() == F(3, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS206(TreeMixin, ShortScene):
    N = 206

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.urns = urn_row([('RRRRB', 'hộp I', GOLD), ('RBBBB', 'hộp II', PURPLE)], y=1.6)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('upd', 1.4))

    def beat_s2(self, T):
        self.clear_board(.03)
        self.play(self.urns.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.6, root_label='biết bi 1 đỏ')
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.2))

    def beat_s3(self, T):
        m = self.M('tot', 1.6)
        self.write_board(m)
        self.frame(m)

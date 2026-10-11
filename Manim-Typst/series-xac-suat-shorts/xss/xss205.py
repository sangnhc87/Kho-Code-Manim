"""XSS205 · Tung xu chọn hộp — I: 4Đ1X, II: 1Đ4X; P(1 đỏ 1 xanh) = 1/2·4/10 + 1/2·4/10 = 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, PURPLE, SOFT  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS205', 'answer': '2/5'}
PROBLEM = ['Hộp I: $4$ đỏ $1$ xanh; hộp II: $1$ đỏ',
           '$4$ xanh. Tung xu chọn hộp, rút $2$ bi.',
           'Xác suất được $1$ đỏ $1$ xanh?']
OPTIONS = ['1/2', '2/5', '4/25']
CORRECT = 1
ANSWER_VALUE = .4
BRANCHES = [('I', GOLD, '1/2', [('ĐX', SOFT, '4/10', [])]),
            ('II', PURPLE, '1/2', [('ĐX', SOFT, '4/10', [])])]


def mixed(box):
    pairs = list(combinations(box, 2))
    return F(sum(a != b for a, b in pairs), len(pairs))


BEATS = [
    Beat('hook', 'hook', 'Hộp một có bốn đỏ một xanh, hộp hai có một đỏ bốn xanh. Tung đồng xu để chọn hộp, rồi rút hai bi từ hộp đó. '
                         'Xác suất được một đỏ một xanh là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần năm, hay bốn phần hai mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai hành động: tung xu chọn hộp, rồi rút hai bi cùng lúc. Trong mỗi hộp, rút hai bi có tổ hợp chập hai của năm, mười cách.'),
    Beat('s2', 'solve', 'Hộp một: một đỏ một xanh có bốn nhân một bằng bốn cách, xác suất bốn phần mười. '
                        'Hộp hai cũng bốn phần mười, do đối xứng.'),
    Beat('s3', 'solve', 'Toàn phần: một phần hai nhân bốn phần mười cộng một phần hai nhân bốn phần mười, bằng hai phần năm.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Thử thách tiếp: rút lần lượt, biết bi đầu đỏ, bi sau đỏ với xác suất bao nhiêu?'),
    Beat('outro', 'outro', outro_text(205)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    each='P("1Đ 1X" | I) = P("1Đ 1X" | I I) = (4 dot 1)/(C_5^2) = 4/10',
                    tot='P = 1/2 dot 4/10 + 1/2 dot 4/10 = 2/5')


def validate() -> bool:
    assert mixed('RRRRB') == mixed('RBBBB') == F(4, 10)
    assert F(1, 2) * mixed('RRRRB') + F(1, 2) * mixed('RBBBB') == F(2, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS205(TreeMixin, ShortScene):
    N = 205

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.urns = urn_row([('RRRRB', 'hộp I', GOLD), ('RBBBB', 'hộp II', PURPLE)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.6, root_label='tung xu')
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.15))
        self.wait_until(.5, t0)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('each', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.8)
        self.write_board(m)
        self.frame(m)

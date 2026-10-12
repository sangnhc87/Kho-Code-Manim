"""XSS254 · Tìm số bi đỏ hộp II — 1/2(2/5 + x/(x + 2)) = 1/2 ⇒ x/(x + 2) = 3/5 ⇒ x = 3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS254', 'answer': 'x = 3'}
PROBLEM = ['Hộp I: $2$ đỏ $3$ xanh; hộp II: $x$ đỏ $2$ xanh.',
           'Chọn ngẫu nhiên $1$ hộp rồi rút $1$ bi, xác',
           'suất được đỏ là $1/2$. Tìm $x$.']
OPTIONS = ['x = 2', 'x = 3', 'x = 4']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('I', GOLD, '1/2', [('Đ', CORAL, '2/5', [])]),
            ('II', PURPLE, '1/2', [('Đ', CORAL, 'x/(x + 2)', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp một có hai đỏ ba xanh, hộp hai có x bi đỏ và hai bi xanh. Chọn ngẫu nhiên một hộp rồi rút một bi, '
                         'xác suất được đỏ đúng một phần hai. Hộp hai có mấy bi đỏ?'),
    Beat('guess', 'hook', 'Hai, ba, hay bốn? Ba, hai, một!'),
    Beat('s1', 'solve', 'Toàn phần với ẩn: một phần hai nhân hai phần năm, cộng một phần hai nhân x chia x cộng hai, bằng một phần hai.'),
    Beat('s2', 'solve', 'Nhân hai vế với hai: hai phần năm cộng x chia x cộng hai bằng một, nên x chia x cộng hai bằng ba phần năm.'),
    Beat('s3', 'solve', 'Năm x bằng ba x cộng sáu, x bằng ba. Hộp hai có ba đỏ hai xanh, đúng là đối xứng với hộp một!'),
    Beat('answer', 'solve', 'Đáp án: x bằng ba. Toàn phần ngược: một ẩn ở một nhánh, giải phương trình bậc nhất!'),
    Beat('outro', 'outro', outro_text(254)),
]

FORMULAS = formulas('x = 3', OPTIONS,
                    eq='1/2 dot 2/5 + 1/2 dot x/(x + 2) = 1/2',
                    sol='x/(x + 2) = 3/5 arrow.r.double x = 3')


def validate() -> bool:
    assert [x for x in range(100) if F(1, 2) * (F(2, 5) + F(x, x + 2)) == F(1, 2)] == [3]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS254(TreeMixin, ShortScene):
    N = 254

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='chọn hộp')
        self.wait_until(.75, t0)
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        m = self.M('eq', 1.7)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('sol', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.TM('$x = 3$: hộp II có $3$ đỏ $2$ xanh', 30, GOLD, bold=True)
        self.write_board(m)
        self.frame(m)

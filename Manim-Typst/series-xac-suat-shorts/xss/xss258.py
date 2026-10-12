"""XSS258 · Nhóm có bao nhiêu bạn? — P(Hà, Lan cạnh nhau) = 2/n = 1/4 ⇒ n = 8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS258', 'answer': 'n = 8'}
PROBLEM = ['$n$ bạn xếp ngẫu nhiên thành hàng',
           'ngang, xác suất Hà và Lan đứng',
           'cạnh nhau là $1/4$. Tìm $n$.']
OPTIONS = ['n = 4', 'n = 8', 'n = 6']
CORRECT = 1
ANSWER_VALUE = None


def adj(n):
    return F(2 * factorial(n - 1), factorial(n))


BEATS = [
    Beat('hook', 'hook', 'Một nhóm n bạn xếp ngẫu nhiên thành hàng ngang. Xác suất hai bạn Hà và Lan đứng cạnh nhau là một phần tư. '
                         'Nhóm có bao nhiêu bạn?'),
    Beat('guess', 'hook', 'Bốn, tám, hay sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xuôi trước: buộc Hà và Lan thành một khối, có n trừ một đối tượng, n trừ một giai thừa cách xếp, nhân hai vì đổi chỗ trong khối.'),
    Beat('s2', 'solve', 'Xác suất bằng hai nhân n trừ một giai thừa chia n giai thừa, gọn lại là hai phần n. Rất đẹp!'),
    Beat('s3', 'solve', 'Hai phần n bằng một phần tư, nên n bằng tám. Kiểm tra với n bằng bốn thì xác suất là một phần hai, quá lớn.'),
    Beat('answer', 'solve', 'Đáp án: tám bạn. Tìm công thức xuôi gọn nhất trước, phương trình ngược sẽ rất dễ!'),
    Beat('outro', 'outro', outro_text(258)),
]

FORMULAS = formulas('n = 8', OPTIONS,
                    fwd='P = (2 (n - 1)!)/(n!) = 2/n',
                    sol='2/n = 1/4 arrow.r.double n = 8')


def validate() -> bool:
    for n in (3, 4, 5):
        pos = list(permutations(range(n)))
        assert F(sum(abs(p.index(0) - p.index(1)) == 1 for p in pos), len(pos)) == adj(n) == F(2, n)
    assert [n for n in range(2, 60) if adj(n) == F(1, 4)] == [8]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS258(ShortScene):
    N = 258

    def hook_visual(self, t0):
        self.board_top = -1.25
        cols = [SOFT] * 8
        cols[3], cols[4] = CYAN, CORAL
        self.row = VGroup(*[token(n, c, .32, 18) for n, c in zip(['', '', '', 'Hà', 'Lan', '', '', ''], cols)]).arrange(buff=.15) \
            .move_to([0, 1.9, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.row, lag_ratio=.1), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.row[3:5].animate.scale(1.25), run_time=self.rt(.05))

    def beat_s2(self, T):
        m = self.M('fwd', 2.0)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        m = self.M('sol', 2.0)
        self.write_board(m)
        self.frame(m)

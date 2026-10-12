"""XSS410 · Hành khách mất vé — người cuối chỉ có thể ngồi ghế của mình hoặc ghế của người đầu, hai ghế đối xứng → 1/2."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss._seatkit import seat, seat_row  # noqa: E402

EPISODE = {'code': 'XSS410', 'answer': '1/2'}
PROBLEM = ['$n$ hành khách lên máy bay $n$ ghế; người',
           'đầu mất vé ngồi bừa, người sau ngồi đúng',
           'ghế nếu còn. $P("người cuối đúng ghế")$?']
OPTIONS = ['1/2', '1/n', '(n - 1)/n']
CORRECT = 0
ANSWER_VALUE = .5


def exact(n):
    """P(last passenger gets own seat): p(n) = 1/n + (1/n) Σ_{k=2}^{n-1} p(n−k+1), and p(2) = 1/2."""
    p = {2: F(1, 2)}
    for m in range(3, n + 1):
        p[m] = F(1, m) + F(1, m) * sum(p[m - k + 1] for k in range(2, m))
    return p[n]


def simulate(n=10, runs=20000, seed=410):
    rnd, ok = random.Random(seed), 0
    for _ in range(runs):
        free = set(range(n))
        free.remove(rnd.randrange(n))
        last = None
        for i in range(1, n):
            if i in free:
                s = i
            else:
                s = rnd.choice(sorted(free))
            free.remove(s)
            last = s
        ok += last == n - 1
    return ok / runs


BEATS = [
    Beat('hook', 'hook', 'Có n hành khách lên máy bay n ghế, ai cũng có vé chỉ định. Người đầu tiên mất vé, ngồi bừa một ghế. Những người sau ngồi đúng ghế của mình nếu còn trống, nếu không thì ngồi bừa. '
                         'Xác suất người cuối cùng ngồi đúng ghế?'),
    Beat('guess', 'hook', 'Một phần hai, một phần n, hay n trừ một phần n? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo: khi người cuối bước lên, ghế còn trống chỉ có thể là ghế của chính họ, hoặc ghế của người đầu tiên. Mọi ghế khác đã có chủ ngồi.'),
    Beat('s2', 'solve', 'Mỗi lần ai đó phải ngồi bừa, ghế người đầu và ghế người cuối có vai trò đối xứng như nhau. Ghế nào bị chọn trước thì quyết định kết cục.'),
    Beat('s3', 'solve', 'Vậy xác suất là một phần hai, với mọi n lớn hơn một. Mô phỏng hai mươi nghìn chuyến bay mười ghế cũng cho khoảng không phẩy năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Cây có hàng nghìn nhánh, nhưng tính đối xứng cho đáp án chỉ trong một dòng.'),
    Beat('outro', 'outro', outro_text(410)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    two='"ghế còn lại" in {"ghế của mình"; "ghế người đầu"}',
                    prob='P = 1/2')


def validate() -> bool:
    assert all(exact(n) == F(1, 2) for n in range(2, 12))
    assert abs(simulate() - .5) < .02
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS410(ShortScene):
    N = 410

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.seats = seat_row(7, y=1.2, w=.7, gap=.14)
        self.play(FadeIn(self.seats), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.p1 = seat([('1', CORAL)], [self.seats[4]])
        self.play(FadeIn(self.p1), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        others = seat([(str(i + 1), CYAN) for i in (1, 2, 3)], [self.seats[i] for i in (1, 2, 3)])
        self.play(FadeIn(others, lag_ratio=.2), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(self.seats[0].animate.set_stroke(GOLD, 6), self.seats[6].animate.set_stroke(GOLD, 6), run_time=self.rt(.06))
        self.write_board(self.M('two', 1.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(VGroup(self.seats[0], self.seats[6]).animate.scale(1.1), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

"""XSS277 · Kiến về đỉnh đối diện — gom theo khoảng cách: E1 = 1 + E0/3 + 2E2/3, E2 = 1 + 2E1/3, E0 = 1 + E1 ⇒ E0 = 10."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import Dot, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, PURPLE, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS277', 'answer': '10'}
PROBLEM = ['Kiến đi ngẫu nhiên trên các cạnh hình',
           'lập phương, mỗi bước sang $1$ đỉnh kề.',
           'Trung bình bao nhiêu bước tới đỉnh đối',
           'diện?']
OPTIONS = ['3', '10', '7']
CORRECT = 1
ANSWER_VALUE = None
COL = {0: SOFT, 1: CYAN, 2: PURPLE, 3: GOLD}
N, SEED = 3000, 2


def exact():
    # unknowns E0, E1, E2 with E3 = 0
    # E0 = 1 + E1; E1 = 1 + E0/3 + 2E2/3; E2 = 1 + 2E1/3
    # substitute E0: E1 = 1 + (1 + E1)/3 + 2(1 + 2E1/3)/3 = 2 + E1/3 + 4E1/9 ⇒ E1 (2/9) = 2 ⇒ E1 = 9
    e1 = F(9)
    e0 = 1 + e1
    e2 = 1 + F(2, 3) * e1
    assert e1 == 1 + e0 / 3 + F(2, 3) * e2
    return e0


def sim():
    r, tot = random.Random(SEED), 0
    for _ in range(N):
        v, n = [0, 0, 0], 0
        while v != [1, 1, 1]:
            v[r.randrange(3)] ^= 1
            n += 1
        tot += n
    return tot / N


BEATS = [
    Beat('hook', 'hook', 'Chú kiến bò ngẫu nhiên trên khung hình lập phương, mỗi bước sang một trong ba đỉnh kề. '
                         'Trung bình bao nhiêu bước thì kiến tới được đỉnh đối diện, xa nhất?'),
    Beat('guess', 'hook', 'Ba bước, mười bước, hay bảy bước? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba bước là đường ngắn nhất, nhưng kiến hay đi lạc. Gom tám đỉnh theo khoảng cách tới đích: ba, hai, một, không cạnh. '
                        'Gọi E k là số bước trung bình còn lại.'),
    Beat('s2', 'solve', 'Từ điểm xuất phát chỉ có thể tới tầng tiếp. Từ tầng giữa: một phần ba lùi về, hai phần ba tiến lên. '
                        'Từ đỉnh sát đích: một phần ba tới đích, hai phần ba lùi lại. Mỗi bước tốn một.'),
    Beat('s3', 'solve', 'Giải hệ ba phương trình được E bằng mười bước. Mô phỏng ba nghìn chú kiến cũng cho trung bình khoảng mười.'),
    Beat('answer', 'solve', 'Đáp án: mười bước. Gom trạng thái giống nhau, đặt ẩn kỳ vọng, rồi giải hệ!'),
    Beat('outro', 'outro', outro_text(277)),
]

FORMULAS = formulas('10', OPTIONS,
                    sys='E_0 = 1 + E_1, quad E_1 = 1 + 1/3 E_0 + 2/3 E_2, quad E_2 = 1 + 2/3 E_1',
                    sol='E_1 = 9 arrow.r.double E_0 = 10')


def validate() -> bool:
    assert exact() == 10 and abs(sim() - 10) < .4
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS277(ShortScene):
    N = 277

    def hook_visual(self, t0):
        self.board_top = -1.3
        P = {v: [-.9 + 1.7 * v[0] + .8 * v[2], .4 + 1.7 * v[1] + .6 * v[2], 0] for v in product((0, 1), repeat=3)}
        edges = VGroup(*[Line(P[a], P[b], color=STROKE, stroke_width=3) for a in P for b in P
                         if a < b and sum(x != y for x, y in zip(a, b)) == 1])
        dots = VGroup(*[Dot(P[v], radius=.14, color=COL[sum(v)]) for v in P])
        self.cube = VGroup(edges, dots)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.cube), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(tx('màu = tầng khoảng cách', 24, SOFT).move_to([0, -.5, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('sys', 1.25))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 2.0)
        self.write_board(m)
        self.frame(m, GREEN)

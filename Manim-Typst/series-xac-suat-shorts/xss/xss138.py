"""XSS138 · Con kiến trên hình lập phương — gom đỉnh theo khoảng cách 0, 1, 2, 3: 1 · 2/3 · 1/3 = 2/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import Dot, FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, PURPLE, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS138', 'answer': '2/9'}
PROBLEM = ['Kiến ở một đỉnh hình lập phương, mỗi',
           'bước bò sang một đỉnh kề ngẫu nhiên. Xác',
           'suất sau $3$ bước kiến ở đỉnh đối diện?']
OPTIONS = ['1/9', '2/9', '1/3']
CORRECT = 1
ANSWER_VALUE = 2 / 9
COL = {'0': SOFT, '1': CYAN, '2': PURPLE, '3': GOLD}
BRANCHES = [('1', CYAN, '1', [('0', SOFT, '1/3', [('1', CYAN, '1', [])]),
                              ('2', PURPLE, '2/3', [('3', GOLD, '1/3', []), ('1', CYAN, '2/3', [])])])]


def walk():
    dist = {(0, 0, 0): F(1)}
    for _ in range(3):
        nxt = {}
        for v, pr in dist.items():
            for i in range(3):
                u = tuple(v[j] ^ (j == i) for j in range(3))
                nxt[u] = nxt.get(u, 0) + pr / 3
        dist = nxt
    return dist[(1, 1, 1)]


BEATS = [
    Beat('hook', 'hook', 'Một chú kiến đứng ở một đỉnh hình lập phương. Mỗi bước, nó bò dọc một cạnh sang một trong ba đỉnh kề, ngẫu nhiên. '
                         'Sau ba bước, xác suất kiến ở đúng đỉnh đối diện là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần chín, hai phần chín, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây đầy đủ có hai mươi bảy nhánh. Mẹo: gom tám đỉnh theo khoảng cách tới điểm xuất phát: '
                        'không, một, hai, ba cạnh. Kiến chỉ cần biết mình đang ở tầng nào.'),
    Beat('s2', 'solve', 'Bước một luôn tới tầng một. Từ tầng một: quay về tầng không một phần ba, lên tầng hai hai phần ba. '
                        'Từ tầng hai: tới đỉnh đối diện một phần ba, lùi về tầng một hai phần ba.'),
    Beat('s3', 'solve', 'Đường duy nhất tới đỉnh đối diện sau ba bước: một nhân hai phần ba nhân một phần ba, bằng hai phần chín.'),
    Beat('answer', 'solve', 'Đáp án: hai phần chín. Gom các trạng thái giống nhau, cây hai mươi bảy nhánh chỉ còn vài nhánh!'),
    Beat('outro', 'outro', outro_text(138)),
]

FORMULAS = formulas('2/9', OPTIONS,
                    prob='P = 1 dot 2/3 dot 1/3 = 2/9')


def validate() -> bool:
    assert walk() == F(2, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS138(TreeMixin, ShortScene):
    N = 138

    def hook_visual(self, t0):
        self.board_top = -1.6
        P = {v: [-.9 + 1.7 * v[0] + .8 * v[2], .3 + 1.7 * v[1] + .6 * v[2], 0] for v in product((0, 1), repeat=3)}
        edges = VGroup(*[Line(P[a], P[b], color=STROKE, stroke_width=3) for a in P for b in P
                         if a < b and sum(x != y for x, y in zip(a, b)) == 1])
        dots = VGroup(*[Dot(P[v], radius=.12, color=COL[str(sum(v))]) for v in P])
        self.cube = VGroup(edges, dots)
        self.wait_until(.5, t0)
        self.play(FadeIn(self.cube), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(*[d.animate.scale(1.6) for d in self.cube[1]], run_time=self.rt(.06))
        self.play(FadeIn(tx('màu = số cạnh tới điểm xuất phát', 24, SOFT).move_to([0, -.4, 0])), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[m.animate.set_opacity(0) for m in self.mobjects if m in (self.cube,)], run_time=self.rt(.03))
        self.remove(self.cube)
        self.clear_stage(.03)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.15, width=5.6, root_label='đỉnh xuất phát',
                                                  r=.38, edge_size=28)
        for i in range(4):
            self.play(FadeIn(self.levels[i], lag_ratio=.3), run_time=self.rt(.08))
            self.wait_until(.2 + .2 * i, t0)

    def beat_s3(self, T):
        t0 = self.now()
        goal = [n for n, path in self.leaves if path[-1][0] == '3']
        self.play(*[n.animate.scale(1.4).set_stroke(GREEN, 5) for n in goal], run_time=self.rt(.06))
        self.wait_until(.3, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)



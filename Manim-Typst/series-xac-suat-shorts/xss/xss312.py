"""XSS312 · Hai robot ngược chiều — A (0;0)→(2;2), B (2;2)→(0;0) cùng tốc độ: chỉ gặp sau 2 bước trên x + y = 2 → (1/6)² + (4/6)² + (1/6)² = 1/2."""
from __future__ import annotations

import itertools
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Dot, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss._gridkit import Lattice  # noqa: E402

EPISODE = {'code': 'XSS312', 'answer': '1/2'}
PROBLEM = ['Robot A đi từ $(0; 0)$ tới $(2; 2)$, B đi',
           'từ $(2; 2)$ về $(0; 0)$, cùng tốc độ, chọn',
           'ngẫu nhiên đường ngắn nhất. $P("gặp")$?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5
PATHS = sorted(set(itertools.permutations('RRUU')))


def at(w, t, start=(0, 0), sign=1):
    x, y = start
    for m in w[:t]:
        x, y = (x + sign, y) if m == 'R' else (x, y + sign)
    return x, y


def meet_prob():
    hits = 0
    for a in PATHS:
        for b in PATHS:
            pos = [(at(a, t), at(b, t, (2, 2), -1)) for t in range(5)]
            same = any(p == q for p, q in pos)
            swap = any(pos[t][0] == pos[t + 1][1] and pos[t][1] == pos[t + 1][0] for t in range(4))
            hits += same or swap
    return F(hits, len(PATHS) ** 2)


BEATS = [
    Beat('hook', 'hook', 'Robot A đi từ gốc tới điểm hai hai, robot B đi ngược lại từ hai hai về gốc. Cùng tốc độ, mỗi robot chọn ngẫu nhiên một đường ngắn nhất. '
                         'Xác suất hai robot gặp nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi robot có sáu đường. Sau hai bước, cả hai đều nằm trên đường chéo x cộng y bằng hai, và chỉ ở đó chúng mới có thể gặp.'),
    Beat('s2', 'solve', 'Sau hai bước, A ở góc dưới phải với xác suất một phần sáu, ở tâm bốn phần sáu, ở góc trên trái một phần sáu. B y hệt, do đối xứng.'),
    Beat('s3', 'solve', 'Hai robot độc lập, nên gặp nhau khi cùng một điểm: một phần ba mươi sáu cộng mười sáu phần ba mươi sáu cộng một phần ba mươi sáu.'),
    Beat('s4', 'solve', 'Tổng là mười tám phần ba mươi sáu, đúng bằng một nửa.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Điểm giữa được ghé nhiều nhất, nên hai robot hay đụng nhau ở tâm.'),
    Beat('outro', 'outro', outro_text(312)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    dist='1/6, quad 4/6, quad 1/6',
                    meet='P = (1/6)^2 + (4/6)^2 + (1/6)^2 = 18/36 = 1/2')


def validate() -> bool:
    assert len(PATHS) == 6 and meet_prob() == F(1, 2)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS312(ShortScene):
    N = 312

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.L = Lattice(2, 2, origin=(-1.3, -.55), step=1.3)
        self.g = self.L.grid()
        self.a = Dot(self.L.P(0, 0), radius=.17, color=CYAN)
        self.b = Dot(self.L.P(2, 2), radius=.17, color=CORAL)
        self.play(FadeIn(self.g), FadeIn(self.a), FadeIn(self.b), run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.L.path('RURU', CYAN, 5)), FadeIn(self.L.path('URRU', CORAL, 5)), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(self.a.animate.move_to(self.L.P(1, 1)), self.b.animate.move_to(self.L.P(1, 1)), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        labs = VGroup(*[self.TM(f'${s}$', 34, GOLD).next_to(self.L.P(*p), [.7, .7, 0], buff=.1)
                        for s, p in (('1/6', (2, 0)), ('4/6', (1, 1)), ('1/6', (0, 2)))])
        self.wait_until(.2, t0)
        self.play(FadeIn(labs, lag_ratio=.3), run_time=self.rt(.12))
        self.write_board(self.M('dist', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.2, t0)
        self.meet = self.M('meet', 1.6)
        self.write_board(self.meet)

    def beat_s4(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.frame(self.meet)

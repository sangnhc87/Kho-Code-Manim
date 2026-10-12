"""XSS300 · Đường ngắn nhất qua (1; 1) — 20 đường RRRUUU; qua (1;1): 2·6 = 12 → 3/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path

from manim import Dot, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402
from xss._gridkit import Lattice  # noqa: E402

EPISODE = {'code': 'XSS300', 'answer': '3/5'}
PROBLEM = ['Chọn ngẫu nhiên một đường đi ngắn nhất',
           'từ $(0; 0)$ tới $(3; 3)$ trên lưới ô vuông.',
           'Xác suất đường đi qua điểm $(1; 1)$?']
OPTIONS = ['1/2', '3/5', '2/5']
CORRECT = 1
ANSWER_VALUE = .6
PATHS = sorted(''.join(p) for p in set(permutations('RRRUUU')))


def visits(w, pt):
    x = y = 0
    if (x, y) == pt:
        return True
    for m in w:
        x, y = (x + 1, y) if m == 'R' else (x, y + 1)
        if (x, y) == pt:
            return True
    return False


BEATS = [
    Beat('hook', 'hook', 'Trên lưới ô vuông, đi từ gốc tới điểm ba ba theo đường ngắn nhất, tức chỉ đi sang phải hoặc lên trên. '
                         'Chọn ngẫu nhiên một trong các đường đó. Xác suất đường đi qua điểm một một?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần năm, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi đường là một dãy ba phải ba lên: tổ hợp chập ba của sáu, hai mươi đường.'),
    Beat('s2', 'solve', 'Qua một một: chặng đầu từ gốc tới một một có hai đường; chặng sau từ một một tới ba ba có tổ hợp chập hai của bốn, sáu đường. Tổng mười hai.'),
    Beat('s3', 'solve', 'Xác suất mười hai phần hai mươi, tức ba phần năm. Lưu ý: đây là chọn đều các đường, khác với kiến đi ngẫu nhiên từng bước!'),
    Beat('answer', 'solve', 'Đáp án: ba phần năm. Đi qua một điểm: nhân số đường của hai chặng!'),
    Beat('outro', 'outro', outro_text(300)),
]

FORMULAS = formulas('3/5', OPTIONS,
                    total='n(Omega) = C_6^3 = 20',
                    via='n(A) = C_2^1 dot C_4^2 = 2 dot 6 = 12',
                    prob='P = 12/20 = 3/5')


def validate() -> bool:
    assert len(PATHS) == 20 and F(sum(visits(w, (1, 1)) for w in PATHS), 20) == F(3, 5) == F(2 * comb(4, 2), 20)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS300(ShortScene):
    N = 300

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.L = Lattice(3, 3, origin=(-1.5, -.3), step=1.0)
        self.g = self.L.grid()
        self.mark = Dot(self.L.P(1, 1), radius=.14, color=GOLD)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.g), FadeIn(self.mark), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        for w in ('RRRUUU', 'URURUR', 'UUURRR'):
            p = self.L.path(w, CYAN, 4)
            self.play(FadeIn(p), run_time=self.rt(.04))
            self.play(p.animate.set_opacity(.25), run_time=self.rt(.03))
        self.wait_until(.6, t0)
        self.write_board(self.M('total', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(VGroup(*[self.L.path(w, GOLD, 5) for w in PATHS if visits(w, (1, 1))])), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        self.clear_board(.03)
        self.write_board(self.M('via', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

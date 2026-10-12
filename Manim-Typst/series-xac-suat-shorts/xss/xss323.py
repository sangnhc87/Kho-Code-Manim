"""XSS323 · Điểm xúc xắc trong hình tròn — (a; b) với a² + b² < 25: 13 điểm; trên y = x: (1;1), (2;2), (3;3) → 3/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Arc, DashedLine, Dot, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT, STROKE  # noqa: E402

EPISODE = {'code': 'XSS323', 'answer': '3/13'}
PROBLEM = ['Gieo $2$ xúc xắc được điểm $(a; b)$. Biết',
           '$a^2 + b^2 < 25$. Xác suất điểm nằm trên',
           'đường thẳng $y = x$?']
OPTIONS = ['3/13', '1/4', '3/16']
CORRECT = 0
ANSWER_VALUE = 3 / 13
IN = [(a, b) for a in range(1, 7) for b in range(1, 7) if a * a + b * b < 25]
DIAG = [p for p in IN if p[0] == p[1]]
G, O = .62, (-2.6, -1.0)


def P(a, b):
    return [O[0] + G * a, O[1] + G * b, 0]


BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc, coi kết quả là điểm a, b trên mặt phẳng. Biết điểm nằm trong hình tròn tâm gốc bán kính năm. '
                         'Xác suất điểm nằm trên đường thẳng y bằng x là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần mười ba, một phần tư, hay ba phần mười sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba mươi sáu điểm của lưới xúc xắc. Đếm theo từng cột a bằng một, hai, ba, bốn: số giá trị b thỏa mãn là bốn, bốn, ba, hai. '
                        'Tổng mười ba điểm trong hình tròn.'),
    Beat('s2', 'solve', 'Trên đường y bằng x chỉ có các điểm một một, hai hai, ba ba. Điểm bốn bốn có tổng bình phương ba mươi hai, nằm ngoài.'),
    Beat('s3', 'solve', 'Vậy xác suất bằng ba phần mười ba.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười ba. Điều kiện thu hẹp ba mươi sáu điểm còn mười ba, ta chỉ đếm trong phần còn lại.'),
    Beat('outro', 'outro', outro_text(323)),
]

FORMULAS = formulas('3/13', OPTIONS,
                    cnt='4 + 4 + 3 + 2 = 13',
                    out='4^2 + 4^2 = 32 > 25',
                    prob='P = 3/13')


def validate() -> bool:
    assert len(IN) == 13 and len(DIAG) == 3
    assert F(len(DIAG), len(IN)) == F(3, 13)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS323(ShortScene):
    N = 323

    def hook_visual(self, t0):
        self.board_top = -1.75
        self.dots = VGroup(*[Dot(P(a, b), radius=.08, color=STROKE) for a in range(1, 7) for b in range(1, 7)])
        self.circ = Arc(radius=5 * G, start_angle=0, angle=1.5708, arc_center=P(0, 0), color=CYAN, stroke_width=5)
        labs = VGroup(*[self.TM(f'${k}$', 22, SOFT).move_to(P(k, 0) + [0, -.3, 0]) for k in range(1, 7)],
                      *[self.TM(f'${k}$', 22, SOFT).move_to(P(0, k) + [-.3, 0, 0]) for k in range(1, 7)])
        self.play(FadeIn(self.dots), FadeIn(labs), run_time=self.rt(.06))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.circ), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(*[d.animate.set_color(CYAN).scale(1.6) for d, (a, b) in
                    zip(self.dots, [(a, b) for a in range(1, 7) for b in range(1, 7)]) if (a, b) in IN], run_time=self.rt(.15))
        m = self.M('cnt', 1.5)
        self.write_board(m)

    def beat_s2(self, T):
        t0 = self.now()
        line = DashedLine(P(0, 0), P(6, 6), color=GOLD, stroke_width=4)
        self.play(FadeIn(line), run_time=self.rt(.06))
        self.play(*[FadeIn(Dot(P(a, a), radius=.17, color=GREEN)) for a in (1, 2, 3)], run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.clear_board(.03)
        self.write_board(self.M('out', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

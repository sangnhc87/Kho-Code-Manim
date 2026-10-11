"""XSS025 · Chọn hai bạn nữ — lớp 30 bạn, 12 nữ: C(12,2)/C(30,2) = 22/145."""
from __future__ import annotations

import sys
from fractions import Fraction
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS025', 'answer': '22/145'}
PROBLEM = ['Lớp có $30$ bạn, trong đó $12$ bạn nữ.', 'Chọn ngẫu nhiên $2$ bạn. Xác suất cả hai là nữ?']
OPTIONS = ['2/5', '4/25', '22/145']
CORRECT = 2
ANSWER_VALUE = 22 / 145

BEATS = [
    Beat('hook', 'hook', 'Lớp có ba mươi bạn, trong đó mười hai bạn nữ. Cô giáo chọn ngẫu nhiên hai bạn lên bảng. '
                         'Xác suất cả hai đều là nữ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, bốn phần hai mươi lăm, hay hai mươi hai phần một trăm bốn mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chọn hai bạn từ ba mươi bạn, không phân biệt thứ tự: tổ hợp chập hai của ba mươi, '
                        'bằng bốn trăm ba mươi lăm cách.'),
    Beat('s2', 'solve', 'Chọn hai bạn trong mười hai bạn nữ: tổ hợp chập hai của mười hai, bằng sáu mươi sáu cách.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu mươi sáu phần bốn trăm ba mươi lăm, rút gọn còn hai mươi hai phần một trăm '
                        'bốn mươi lăm, khoảng mười lăm phần trăm. Bốn phần hai mươi lăm là bẫy: '
                        'nó coi như một bạn được chọn hai lần.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi hai phần một trăm bốn mươi lăm. Chọn không lặp thì dùng tổ hợp!'),
    Beat('outro', 'outro', outro_text(25)),
]

FORMULAS = formulas('22/145', OPTIONS,
                    n='n(Omega) = C_30^2 = 435',
                    a='n(A) = C_12^2 = 66',
                    prob='P(A) = 66/435 = 22/145 approx "15" %',
                    trap='(12/30)^2 = 4/25 quad coral(times)')


def validate() -> bool:
    assert comb(30, 2) == 435 and comb(12, 2) == 66
    assert Fraction(comb(12, 2), comb(30, 2)) == Fraction(22, 145) and round(22 / 145 * 100) == 15
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS025(ShortScene):
    N = 25

    def hook_visual(self, t0):
        self.cls = VGroup(*[token('G' if i < 12 else 'T', CORAL if i < 12 else CYAN, .26) for i in range(30)])
        self.cls.arrange_in_grid(5, 6, buff=.22).move_to([0, 1.3, 0])
        legend = VGroup(tx('G: 12 nữ', 24, CORAL, bold=True), tx('T: 18 nam', 24, CYAN, bold=True)) \
            .arrange(buff=.6).move_to([0, -.25, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.cls, lag_ratio=.03), FadeIn(legend), run_time=self.rt(.3))

    def beat_s1(self, T):
        t0 = self.now()
        self.board_top = -.85
        self.wait_until(.3, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[t[0].animate.set_stroke('#FFFFFF', 4) for t in self.cls[:12]],
                  *[t.animate.set_opacity(.3) for t in self.cls[12:]], run_time=self.rt(.1))
        self.wait_until(.35, t0)
        self.write_board(self.M('a', 2.2))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.M('trap', 1.6), anim='fade')
        self.write_board(tx('không ai được chọn hai lần', 24, SOFT), anim='fade')

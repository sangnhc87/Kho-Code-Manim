"""XSS321 · Đường chéo khối lập phương — 28 cặp đỉnh − 12 cạnh = 16; 12 chéo mặt + 4 chéo khối → 1/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, FadeOut, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss._polykit import CUBE, cube_mob, cube_view, d2  # noqa: E402

EPISODE = {'code': 'XSS321', 'answer': '1/4'}
PROBLEM = ['Chọn $2$ đỉnh của hình lập phương. Biết',
           'đoạn nối chúng không phải là cạnh.',
           'Xác suất đó là đường chéo của khối?']
OPTIONS = ['1/4', '1/3', '1/7']
CORRECT = 0
ANSWER_VALUE = .25
PAIRS = list(combinations(CUBE, 2))
FACE = [p for p in PAIRS if d2(*p) == 2]
SPACE = [p for p in PAIRS if d2(*p) == 3]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên hai đỉnh của một hình lập phương. Biết đoạn nối hai đỉnh không phải là cạnh. '
                         'Xác suất nó là đường chéo xuyên qua khối bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần ba, hay một phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tám đỉnh cho hai mươi tám cặp. Hình lập phương có mười hai cạnh, nên điều kiện còn mười sáu đoạn.'),
    Beat('s2', 'solve', 'Mười sáu đoạn đó gồm hai loại: đường chéo mặt, mỗi mặt hai đường, sáu mặt là mười hai; và đường chéo khối, nối hai đỉnh đối xứng qua tâm, chỉ có bốn.'),
    Beat('s3', 'solve', 'Xác suất bốn phần mười sáu, tức một phần tư. Không có điều kiện thì chỉ là bốn phần hai mươi tám, tức một phần bảy.'),
    Beat('answer', 'solve', 'Đáp án: một phần tư. Loại bỏ mười hai cạnh làm xác suất tăng gần gấp đôi.'),
    Beat('outro', 'outro', outro_text(321)),
]

FORMULAS = formulas('1/4', OPTIONS,
                    cond='C_8^2 - 12 = 16',
                    split='16 = 12 + 4',
                    prob='P = 4/16 = 1/4')


def validate() -> bool:
    assert len(PAIRS) - 12 == 16 and len(FACE) == 12 and len(SPACE) == 4
    assert F(len(SPACE), 16) == F(1, 4)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS321(ShortScene):
    N = 321

    def segs(self, pairs, color, w=5):
        return VGroup(*[Line(cube_view(a), cube_view(b), color=color, stroke_width=w) for a, b in pairs])

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.cube = cube_mob()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.cube), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.cube[0].animate.set_color(CORAL), run_time=self.rt(.06))
        self.write_board(self.M('cond', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.cube[0].animate.set_opacity(.35), run_time=self.rt(.03))
        face = self.segs(FACE, CYAN, 3)
        self.play(FadeIn(face), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.play(FadeOut(face), FadeIn(self.segs(SPACE, GOLD, 6)), run_time=self.rt(.08))
        self.clear_board(.03)
        self.write_board(self.M('split', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.1, t0)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

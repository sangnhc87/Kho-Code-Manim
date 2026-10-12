"""XSS436 · A là tập con của B — mỗi phần tử có 4 trạng thái (∉A∉B, ∉A∈B, ∈A∈B, ∈A∉B), A ⊂ B cấm trạng thái cuối: (3/4)³ = 27/64."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402
from common.visuals import venn  # noqa: E402

EPISODE = {'code': 'XSS436', 'answer': '27/64'}
PROBLEM = ['Chọn ngẫu nhiên $2$ tập con $A, B$ của tập',
           '${1; 2; 3}$ (độc lập). $P(A subset.eq B)$?']
OPTIONS = ['27/64', '1/8', '3/8']
CORRECT = 0
ANSWER_VALUE = 27 / 64
SUBS = [frozenset(s) for r in range(4) for s in combinations((1, 2, 3), r)]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên, độc lập, hai tập con A và B của tập một, hai, ba. Xác suất A là tập con của B?'),
    Beat('guess', 'hook', 'Hai mươi bảy phần sáu mươi tư, một phần tám, hay ba phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Thay vì liệt kê sáu mươi tư cặp tập, xét từng phần tử. Mỗi phần tử có bốn trạng thái như nhau: không thuộc cả hai, chỉ thuộc B, thuộc cả hai, hoặc chỉ thuộc A.'),
    Beat('s2', 'solve', 'A là tập con của B nghĩa là không phần tử nào chỉ thuộc A. Mỗi phần tử tránh trạng thái đó với xác suất ba phần tư, độc lập.'),
    Beat('s3', 'solve', 'Ba phần tử: ba phần tư mũ ba, bằng hai mươi bảy phần sáu mươi tư.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi bảy phần sáu mươi tư. Xét từng phần tử độc lập, bài tập hợp trở thành bài nhân.'),
    Beat('outro', 'outro', outro_text(436)),
]

FORMULAS = formulas('27/64', OPTIONS,
                    state='4 "trạng thái / phần tử", quad "cấm": x in A, x in.not B',
                    prob='P = (3/4)^3 = 27/64')


def validate() -> bool:
    good = sum(a <= b for a in SUBS for b in SUBS)
    assert len(SUBS) == 8 and F(good, 64) == F(27, 64)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS436(ShortScene):
    N = 436

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.v = venn(1.3, 1.3, CORAL, CYAN, center=(0, 1.2))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.v), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.v.animate.set_opacity(.8), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.v.only_a(CORAL, .6)), run_time=self.rt(.06))
        self.write_board(self.M('state', 1.2))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)



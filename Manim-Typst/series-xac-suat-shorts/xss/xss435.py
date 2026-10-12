"""XSS435 · Tập con có tổng chẵn — ghép cặp: thêm/bớt phần tử 1 đổi tính chẵn lẻ của tổng; 32 tập con chia đôi → 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import Arrow, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS435', 'answer': '1/2'}
PROBLEM = ['Chọn ngẫu nhiên một tập con của tập',
           '$A = {1; 2; 3; 4; 5}$. Xác suất tổng các',
           'phần tử là số chẵn?']
OPTIONS = ['1/2', '15/32', '17/32']
CORRECT = 0
ANSWER_VALUE = .5
SUBSETS = [s for r in range(6) for s in combinations(range(1, 6), r)]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên một tập con của tập một, hai, ba, bốn, năm, kể cả tập rỗng. Xác suất tổng các phần tử là số chẵn? '
                         'Tập rỗng có tổng bằng không, là số chẵn.'),
    Beat('guess', 'hook', 'Một phần hai, mười lăm phần ba mươi hai, hay mười bảy phần ba mươi hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có hai mũ năm, ba mươi hai tập con đồng khả năng. Mẹo ghép cặp: với mỗi tập, thêm số một nếu chưa có, bỏ số một nếu đã có.'),
    Beat('s2', 'solve', 'Phép ghép này đổi tổng đi đúng một, nên đổi tổng chẵn thành lẻ và ngược lại. Mỗi tập tổng chẵn có đúng một bạn tổng lẻ.'),
    Beat('s3', 'solve', 'Vậy mười sáu tập tổng chẵn, mười sáu tập tổng lẻ. Xác suất một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Một phép ghép cặp khéo léo thay cho ba mươi hai phép cộng.'),
    Beat('outro', 'outro', outro_text(435)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    pair='S <-> S triangle.t {1}: quad "tổng" plus.minus 1',
                    prob='P = 16/32 = 1/2')


def validate() -> bool:
    assert len(SUBSETS) == 32 and F(sum(sum(s) % 2 == 0 for s in SUBSETS), 32) == F(1, 2)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS435(ShortScene):
    N = 435

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.a = self.TM('${2; 4; 5}$, tổng $11$', 32, CORAL).move_to([-1.6, 1.4, 0])
        self.b = self.TM('${1; 2; 4; 5}$, tổng $12$', 32, CYAN).move_to([1.6, 1.4, 0])
        self.arrow = Arrow(self.a.get_right(), self.b.get_left(), color=GOLD, buff=.1)
        self.ab = VGroup(self.a, self.arrow, self.b).arrange(buff=.25).scale_to_fit_width(7.0).move_to([0, 1.3, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.a), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.55, t0)
        self.play(FadeIn(self.arrow), FadeIn(self.b), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('pair', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

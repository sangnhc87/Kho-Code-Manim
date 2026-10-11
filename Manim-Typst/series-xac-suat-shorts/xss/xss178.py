"""XSS178 · Nữ không đứng cạnh nhau — xếp nam rồi chèn nữ vào 6 khe: 5!·A(6,5)/10! = 1/42."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import factorial, perm
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS178', 'answer': '1/42'}
PROBLEM = ['$5$ nam, $5$ nữ xếp ngẫu nhiên thành',
           'hàng ngang. Xác suất không có hai',
           'bạn nữ nào đứng cạnh nhau?']
OPTIONS = ['1/42', '1/126', '1/21']
CORRECT = 0
ANSWER_VALUE = 1 / 42

BEATS = [
    Beat('hook', 'hook', 'Năm bạn nam và năm bạn nữ xếp ngẫu nhiên thành một hàng ngang. '
                         'Xác suất không có hai bạn nữ nào đứng cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần bốn mươi hai, một phần một trăm hai mươi sáu, hay một phần hai mươi mốt? Ba, hai, một!'),
    Beat('s1', 'solve', 'Kỹ thuật vách ngăn: xếp năm bạn nam trước, năm giai thừa cách. Năm bạn nam tạo ra sáu khe: hai đầu và bốn khe giữa.'),
    Beat('s2', 'solve', 'Mỗi bạn nữ đứng vào một khe khác nhau thì không ai đứng cạnh nhau. Chọn năm khe trong sáu và xếp năm bạn nữ: '
                        'chỉnh hợp chập năm của sáu, bằng bảy trăm hai mươi cách.'),
    Beat('s3', 'solve', 'Xác suất bằng năm giai thừa nhân bảy trăm hai mươi, chia mười giai thừa, tức một phần bốn mươi hai. Rất hiếm!'),
    Beat('answer', 'solve', 'Đáp án: một phần bốn mươi hai. Gặp điều kiện "không đứng cạnh", hãy xếp nhóm kia trước rồi chèn vào khe!'),
    Beat('outro', 'outro', outro_text(178)),
]

FORMULAS = formulas('1/42', OPTIONS,
                    gaps='5! dot A_6^5 = 120 dot 720',
                    prob='P = (5! dot A_6^5)/(10!) = 1/42')


def validate() -> bool:
    seqs = set(permutations('TTTTTGGGGG'))
    assert F(sum('GG' not in ''.join(s) for s in seqs), len(seqs)) == F(1, 42)
    assert F(factorial(5) * perm(6, 5), factorial(10)) == F(1, 42)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS178(ShortScene):
    N = 178

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.boys = VGroup(*[token('T', CYAN, .34) for _ in range(5)]).arrange(buff=.62).move_to([0, 1.8, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.boys, lag_ratio=.15), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        xs = [self.boys[0].get_x() - .65] + [(self.boys[i].get_x() + self.boys[i + 1].get_x()) / 2 for i in range(4)] + \
             [self.boys[-1].get_x() + .65]
        self.gaps = VGroup(*[card(.5, .62, GOLD, PANEL, radius=.1, stroke_width=3).move_to([x, 1.8, 0]) for x in xs])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.gaps, lag_ratio=.15), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        girls = VGroup(*[token('G', CORAL, .26).move_to(self.gaps[i]) for i in (0, 1, 3, 4, 5)])
        self.wait_until(.35, t0)
        self.play(FadeIn(girls, lag_ratio=.15), run_time=self.rt(.15))
        self.write_board(self.M('gaps', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

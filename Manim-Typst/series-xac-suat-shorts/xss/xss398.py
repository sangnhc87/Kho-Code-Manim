"""XSS398 · Tin đồn qua ba người — 2 lần kể, đúng 0,8; C nghe đúng sự thật ⇔ 0 hoặc 2 lần sai: 0,64 + 0,04 = 0,68; tiên nghiệm 1/2 nên P(có | nghe có) = 0,68."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402

EPISODE = {'code': 'XSS398', 'answer': '0,68'}
PROBLEM = ['A kể B, B kể C; mỗi lần kể đúng $"0,8"$, sai',
           'thì đảo nghĩa. Sự thật "có" hay "không" như',
           'nhau. C nghe "có": $P("sự thật là có")$?']
OPTIONS = ['"0,68"', '"0,8"', '"0,64"']
CORRECT = 0
ANSWER_VALUE = .68
C = F(4, 5)
SAME = C * C + (1 - C) ** 2
BRANCHES = [('có', GREEN, '1/2', [('có', GREEN, '"0,68"', [])]), ('không', CORAL, '1/2', [('có', GREEN, '"0,32"', [])])]

BEATS = [
    Beat('hook', 'hook', 'A kể cho B, B kể lại cho C. Mỗi lần kể đúng với xác suất không phẩy tám, kể sai thì đảo nghĩa. Sự thật là có hay không với khả năng như nhau. '
                         'C nghe được là có. Xác suất sự thật đúng là có?'),
    Beat('guess', 'hook', 'Không phẩy sáu tám, không phẩy tám, hay không phẩy sáu bốn? Ba, hai, một!'),
    Beat('s1', 'solve', 'Qua hai lần kể, C nghe đúng sự thật khi không lần nào sai, hoặc sai cả hai lần vì hai lần đảo nghĩa triệt tiêu nhau.'),
    Beat('s2', 'solve', 'Xác suất đó bằng không phẩy tám bình phương cộng không phẩy hai bình phương, tức không phẩy sáu bốn cộng không phẩy không bốn, bằng không phẩy sáu tám.'),
    Beat('s3', 'solve', 'Hai giả thuyết như nhau, nên Bayes cho: không phẩy sáu tám chia không phẩy sáu tám cộng không phẩy ba hai, đúng bằng không phẩy sáu tám.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy sáu tám. Mỗi người trung gian làm tin đồn kém tin cậy hơn.'),
    Beat('outro', 'outro', outro_text(398)),
]

FORMULAS = formulas('"0,68"', OPTIONS,
                    same='P("C nghe đúng") = "0,8"^2 + "0,2"^2 = "0,68"',
                    prob='P = ("0,68")/("0,68" + "0,32") = "0,68"')


def validate() -> bool:
    assert SAME == F(68, 100) and F(1, 2) * SAME / (F(1, 2) * SAME + F(1, 2) * (1 - SAME)) == F(68, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS398(TreeMixin, ShortScene):
    N = 398

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.7, width=5.0, r=.45, edge_size=28)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('same', 1.3))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

"""XSS153 · Người sau trúng thăm — P(người 1 trúng | người 2 trúng) = (6/90)/(27/90) = 2/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS153', 'answer': '2/9'}
PROBLEM = ['$10$ lá thăm có $3$ lá trúng, rút lần',
           'lượt. Biết người thứ $2$ trúng. Xác',
           'suất người thứ $1$ cũng trúng?']
OPTIONS = ['3/10', '2/9', '1/3']
CORRECT = 1
ANSWER_VALUE = 2 / 9
W, L = ('T', GOLD), ('X', SOFT)
BRANCHES = [(*W, '3/10', [(*W, '2/9', []), (*L, '7/9', [])]),
            (*L, '7/10', [(*W, '3/9', []), (*L, '6/9', [])])]

BEATS = [
    Beat('hook', 'hook', 'Mười lá thăm có ba lá trúng thưởng, mười người rút lần lượt. Bạn chỉ biết người thứ hai đã trúng. '
                         'Xác suất người thứ nhất cũng trúng là bao nhiêu? Đây là câu hỏi ngược thời gian.'),
    Beat('guess', 'hook', 'Ba phần mười, hai phần chín, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ cây theo đúng thứ tự rút: người một trúng ba phần mười. Biết người một trúng, người hai trúng hai phần chín; '
                        'biết người một trượt, người hai trúng ba phần chín.'),
    Beat('s2', 'solve', 'Người hai trúng ở hai lá: sáu phần chín mươi và hai mươi mốt phần chín mươi, tổng hai mươi bảy phần chín mươi, '
                        'đúng bằng ba phần mười. Bốc trước hay sau đều công bằng.'),
    Beat('s3', 'solve', 'Xác suất người một trúng khi biết người hai trúng: sáu phần chín mươi chia hai mươi bảy phần chín mươi, '
                        'bằng hai phần chín. Đúng như trực giác: còn hai lá trúng trong chín lá khác.'),
    Beat('answer', 'solve', 'Đáp án: hai phần chín. Thông tin về tương lai cũng làm thay đổi xác suất của quá khứ!'),
    Beat('outro', 'outro', outro_text(153)),
]

FORMULAS = formulas('2/9', OPTIONS,
                    p2='P(T_2) = 3/10 dot 2/9 + 7/10 dot 3/9 = 27/90 = 3/10',
                    prob='P(T_1 | T_2) = (6/90)/(27/90) = 2/9')


def validate() -> bool:
    tickets = ['W'] * 3 + ['L'] * 7
    pairs = list(permutations(range(10), 2))
    b = [p for p in pairs if tickets[p[1]] == 'W']
    assert F(sum(tickets[p[0]] == 'W' for p in b), len(b)) == F(2, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS153(TreeMixin, ShortScene):
    N = 153

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='người 1')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        win2 = [self.leaves[0][0], self.leaves[2][0]]
        lose2 = [self.leaves[1][0], self.leaves[3][0]]
        self.play(*[n.animate.set_opacity(.15) for n in lose2], *[n.animate.scale(1.3) for n in win2], run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.write_board(self.M('p2', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.set_stroke(CORAL, 6), run_time=self.rt(.05))
        self.wait_until(.25, t0)
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

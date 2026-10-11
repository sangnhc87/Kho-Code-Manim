"""XSS132 · Ba người thi tung xu — cây vô hạn: P(A) = (1/2)/(1 − 1/8) = 4/7; tỉ lệ A : B : C = 4 : 2 : 1."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS132', 'answer': '4/7'}
PROBLEM = ['A, B, C lần lượt tung đồng xu, ai ra',
           'ngửa trước thì thắng. Xác suất A thắng?']
OPTIONS = ['1/3', '4/7', '1/2']
CORRECT = 1
ANSWER_VALUE = 4 / 7
S = ('S', SOFT, '1/2')
BRANCHES = [('A', CYAN, '1/2', []),
            (*S, [('B', CORAL, '1/2', []),
                  (*S, [('C', GOLD, '1/2', []), (*S, [])])])]

BEATS = [
    Beat('hook', 'hook', 'Ba bạn A, B, C lần lượt tung một đồng xu, ai ra ngửa trước thì thắng. A tung đầu tiên. '
                         'Chơi công bằng thì mỗi người một phần ba chứ? Xác suất A thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, bốn phần bảy, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ một vòng chơi: A ngửa thì thắng ngay. A sấp thì tới B, B sấp thì tới C. '
                        'Nếu cả ba đều sấp, xác suất một phần tám, mọi thứ lặp lại như lúc đầu.'),
    Beat('s2', 'solve', 'A thắng ở vòng một, hoặc vòng hai, hoặc vòng ba, và cứ thế. Đây là cấp số nhân với công bội một phần tám.'),
    Beat('s3', 'solve', 'Tổng bằng một phần hai chia cho một trừ một phần tám, được bốn phần bảy. '
                        'Tương tự B được hai phần bảy, C chỉ một phần bảy. Đi trước có lợi gấp đôi người sau!'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy. Khi cây lặp lại chính nó, hãy dùng cấp số nhân hoặc phương trình!'),
    Beat('outro', 'outro', outro_text(132)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    series='P(A) = 1/2 + 1/2^4 + 1/2^7 + dots',
                    sum='P(A) = (1/2)/(1 - 1/8) = 4/7',
                    ratio='P(A) : P(B) : P(C) = 4 : 2 : 1')


def validate() -> bool:
    a = sum(F(1, 2) * F(1, 8) ** k for k in range(200))
    assert abs(float(a) - 4 / 7) < 1e-15 and F(1, 2) / (1 - F(1, 8)) == F(4, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS132(TreeMixin, ShortScene):
    N = 132

    def hook_visual(self, t0):
        self.board_top = -1.85
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.05), dy=1.3, width=6.4, root_label='vòng 1', r=.4,
                                                  edge_size=30)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        loop = self.TM('$1/8$: quay lại', 24, GOLD).next_to(self.leaves[-1][0], [1, 0, 0], buff=.15)
        self.play(FadeIn(loop), self.leaves[-1][0].animate.set_stroke(GOLD, 5), run_time=self.rt(.06))
        self.play(FadeIn(tx('S: sấp', 22, SOFT).move_to([-2.6, -1.4, 0])), run_time=self.rt(.03))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3).set_stroke(GREEN, 5), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.write_board(self.M('series', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('sum', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('ratio', 1.8), anim='fade')

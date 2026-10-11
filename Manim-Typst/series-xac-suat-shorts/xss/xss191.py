"""XSS191 · Gối của Lewis Carroll — túi 1 bi (Đ/T), thêm 1 đỏ, rút được đỏ: P(bi còn lại đỏ) = (1/2)/(3/4) = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT, WHITE  # noqa: E402

EPISODE = {'code': 'XSS191', 'answer': '2/3'}
PROBLEM = ['Túi có $1$ bi, đỏ hoặc trắng (như nhau).',
           'Bỏ thêm $1$ bi đỏ, lắc, rút ra được đỏ.',
           'Xác suất bi còn lại là đỏ?']
OPTIONS = ['1/2', '2/3', '3/4']
CORRECT = 1
ANSWER_VALUE = 2 / 3
BRANCHES = [('Đ', CORAL, '1/2', [('rút Đ', GOLD, '1', [])]),
            ('T', SOFT, '1/2', [('rút Đ', GOLD, '1/2', []), ('rút T', WHITE, '1/2', [])])]

BEATS = [
    Beat('hook', 'hook', 'Bài toán của Lewis Carroll, tác giả Alice ở xứ sở thần tiên. Túi có một bi, đỏ hoặc trắng với khả năng như nhau. '
                         'Bỏ thêm một bi đỏ, lắc đều, rút ra một bi đỏ. Xác suất bi còn lại trong túi cũng đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhiều người nghĩ: bi ban đầu đỏ hay trắng, rút đỏ chẳng cho biết gì, vậy là một phần hai. Hãy vẽ cây.'),
    Beat('s2', 'solve', 'Ban đầu đỏ: túi có hai bi đỏ, chắc chắn rút được đỏ. Ban đầu trắng: túi một đỏ một trắng, rút đỏ chỉ một phần hai. '
                        'Hai lá "rút đỏ": một phần hai và một phần tư.'),
    Beat('s3', 'solve', 'Bi còn lại đỏ chính là trường hợp ban đầu đỏ: một phần hai chia ba phần tư, bằng hai phần ba. '
                        'Rút được đỏ là bằng chứng nghiêng về túi có nhiều bi đỏ.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Carroll gọi đây là "bài toán trên gối", nghĩ trước khi ngủ mà không ngủ được!'),
    Beat('outro', 'outro', outro_text(191)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    leaves='1/2 dot 1 = 1/2, quad 1/2 dot 1/2 = 1/4',
                    prob='P = (1/2)/(1/2 + 1/4) = 2/3')


def validate() -> bool:
    worlds = [('R', 'R'), ('R', 'R'), ('R', 'W'), ('W', 'R')]  # (bi rút, bi còn lại), mỗi khả năng 1/4
    drawn_red = [w for w in worlds if w[0] == 'R']
    assert F(sum(w[1] == 'R' for w in drawn_red), len(drawn_red)) == F(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS191(TreeMixin, ShortScene):
    N = 191

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.4, root_label='bi ban đầu',
                                                  r=.48)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.TM('trực giác: $1/2$ ?', 30, SOFT), anim='fade')
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))
        red = [n for n, path in self.leaves if path[-1][0] == 'rút Đ']
        self.wait_until(.55, t0)
        self.play(*[n.animate.scale(1.25) for n in red], self.leaves[-1][0].animate.set_opacity(.15), run_time=self.rt(.05))
        self.write_board(self.M('leaves', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

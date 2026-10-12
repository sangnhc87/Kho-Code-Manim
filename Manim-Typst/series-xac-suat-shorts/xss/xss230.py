"""XSS230 · Bi từ hộp II đỏ không? — P(Đ | II đỏ) = 8/9, P(Đ | II xanh) = 5/9: Bayes 8/(8 + 10) = 4/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS230', 'answer': '4/9'}
PROBLEM = ['Như trên (I: $2$ đỏ $1$ xanh, II: $1$ đỏ $2$',
           'xanh, III: $1$ đỏ), biết bi rút từ III là',
           'đỏ. Xác suất bi lấy từ II là đỏ?']
OPTIONS = ['1/3', '4/9', '1/2']
CORRECT = 1
ANSWER_VALUE = 4 / 9
BRANCHES = [('Đ', CORAL, '1/3', [('Đ', GOLD, '(2 + 2/3)/3', [])]),
            ('X', CYAN, '2/3', [('Đ', GOLD, '(1 + 2/3)/3', [])])]


def posterior():
    num = den = F(0)
    for a in 'RRB':
        for b in 'RBB':
            box = 'R' + a + b
            p = F(1, 9) * F(box.count('R'), 3)
            den += p
            num += p * (b == 'R')
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: bạn rút từ hộp ba được bi đỏ. Xác suất bi lấy từ hộp hai là đỏ là bao nhiêu? '
                         'Trước khi biết thì chỉ một phần ba.'),
    Beat('guess', 'hook', 'Một phần ba, bốn phần chín, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xét bi từ hộp hai. Nếu nó đỏ, hộp ba có bi đỏ sẵn, bi đỏ này, và bi từ hộp một đỏ với hai phần ba: '
                        'xác suất rút đỏ là hai cộng hai phần ba, chia ba, bằng tám phần chín.'),
    Beat('s2', 'solve', 'Nếu bi từ hộp hai xanh: một cộng hai phần ba, chia ba, bằng năm phần chín. '
                        'Hai lá: một phần ba nhân tám phần chín, và hai phần ba nhân năm phần chín.'),
    Beat('s3', 'solve', 'Bayes: tám chia tám cộng mười, bằng bốn phần chín. Niềm tin tăng từ một phần ba lên bốn phần chín.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần chín. Với nhiều nguồn cùng đổ vào, tách riêng nguồn cần hỏi, gom các nguồn còn lại!'),
    Beat('outro', 'outro', outro_text(230)),
]

FORMULAS = formulas('4/9', OPTIONS,
                    lik='P(Đ | "II đỏ") = 8/9, quad P(Đ | "II xanh") = 5/9',
                    bayes='P("II đỏ" | Đ) = (1/3 dot 8/9)/(1/3 dot 8/9 + 2/3 dot 5/9) = 4/9')


def validate() -> bool:
    assert posterior() == F(4, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS230(TreeMixin, ShortScene):
    N = 230

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='bi từ II',
                                                  edge_size=26)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2][:3]), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][3:]), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.write_board(self.M('lik', 1.6))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.5)
        self.write_board(m)
        self.frame(m)

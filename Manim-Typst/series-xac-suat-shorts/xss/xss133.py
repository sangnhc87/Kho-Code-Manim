"""XSS133 · Rút đến khi đủ hai đỏ — dừng ở lần 3: ĐXĐ hoặc XĐĐ, mỗi nhánh 1/6: tổng 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402

EPISODE = {'code': 'XSS133', 'answer': '1/3'}
PROBLEM = ['Hộp $2$ đỏ $2$ xanh, rút lần lượt không',
           'hoàn lại đến khi đủ $2$ bi đỏ. Xác',
           'suất dừng ở lần thứ $3$?']
OPTIONS = ['1/6', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '2/4', [(*D, '1/3', []), (*X, '2/3', [(*D, '1/2', []), (*X, '1/2', [])])]),
            (*X, '2/4', [(*D, '2/3', [(*D, '1/2', []), (*X, '1/2', [])]), (*X, '1/3', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có hai bi đỏ và hai bi xanh. Rút lần lượt, không hoàn lại, cho đến khi có đủ hai bi đỏ thì dừng. '
                         'Xác suất phải dừng đúng ở lần rút thứ ba là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ cây hai tầng đầu. Nhánh đỏ đỏ dừng ngay ở lần hai. Nhánh xanh xanh thì lần ba chắc chắn không đủ. '
                        'Chỉ hai nhánh có một đỏ một xanh mới đi tiếp.'),
    Beat('s2', 'solve', 'Dừng ở lần ba nghĩa là lần ba ra đỏ: đỏ xanh đỏ, hai phần tư nhân hai phần ba nhân một phần hai, '
                        'bằng một phần sáu. Xanh đỏ đỏ cũng bằng một phần sáu.'),
    Beat('s3', 'solve', 'Cộng hai nhánh: một phần ba. Chú ý xác suất trên mỗi nhánh thay đổi vì rút không hoàn lại.'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Với bài "dừng ở lần k", hãy tìm đúng những nhánh mà lần k là lần quyết định!'),
    Beat('outro', 'outro', outro_text(133)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    p1='P(Đ X Đ) = 2/4 dot 2/3 dot 1/2 = 1/6',
                    p2='P(X Đ Đ) = 2/4 dot 2/3 dot 1/2 = 1/6',
                    tot='P = 1/6 + 1/6 = 1/3')


def validate() -> bool:
    seqs = set(permutations('RRBB'))
    assert F(sum(s[:3].count('R') == 2 and s[2] == 'R' for s in seqs), len(seqs)) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS133(TreeMixin, ShortScene):
    N = 133

    def hook_visual(self, t0):
        self.board_top = -1.55
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.05), dy=1.4, width=7.0, root_label='rút', r=.38,
                                                  edge_size=28)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.levels[3], lag_ratio=.2), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        stop3 = [n for n, path in self.leaves if len(path) == 3 and path[-1][0] == 'Đ']
        self.play(*[n.animate.scale(1.35).set_stroke(GREEN, 5) for n in stop3], run_time=self.rt(.06))
        self.write_board(self.M('p1', 1.8))
        self.wait_until(.6, t0)
        self.write_board(self.M('p2', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 2.2)
        self.write_board(m)
        self.frame(m)

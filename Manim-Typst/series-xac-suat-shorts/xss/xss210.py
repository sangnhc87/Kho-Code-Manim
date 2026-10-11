"""XSS210 · Đến khi đủ hai màu — dừng ở lần 3: ĐĐX (1/5) + XXĐ (1/10) = 3/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402

EPISODE = {'code': 'XSS210', 'answer': '3/10'}
PROBLEM = ['Hộp $3$ đỏ $2$ xanh, rút lần lượt không',
           'hoàn lại đến khi có đủ hai màu. Xác',
           'suất cần đúng $3$ lần rút?']
OPTIONS = ['1/5', '3/10', '2/5']
CORRECT = 1
ANSWER_VALUE = .3
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '3/5', [(*D, '2/4', [(*D, '1/3', []), (*X, '2/3', [])]), (*X, '2/4', [])]),
            (*X, '2/5', [(*D, '3/4', []), (*X, '1/4', [(*D, '1', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi đỏ và hai bi xanh. Rút lần lượt, không hoàn lại, cho đến khi trong tay có đủ cả hai màu thì dừng. '
                         'Xác suất phải rút đúng ba lần là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, ba phần mười, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện dừng: lần đầu tiên xuất hiện màu thứ hai. Dừng ở lần ba nghĩa là hai lần đầu cùng màu, lần ba khác màu.'),
    Beat('s2', 'solve', 'Đỏ đỏ xanh: ba phần năm nhân hai phần tư nhân hai phần ba, bằng một phần năm. '
                        'Xanh xanh đỏ: hai phần năm nhân một phần tư nhân một, bằng một phần mười.'),
    Beat('s3', 'solve', 'Cộng lại: ba phần mười. Chú ý nhánh xanh xanh: hết bi xanh, lần ba chắc chắn đỏ.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười. Bài "rút đến khi": vẽ cây dừng sớm, nhánh nào dừng thì cắt!'),
    Beat('outro', 'outro', outro_text(210)),
]

FORMULAS = formulas('3/10', OPTIONS,
                    rrb='Đ Đ X: 3/5 dot 2/4 dot 2/3 = 1/5',
                    bbr='X X Đ: 2/5 dot 1/4 dot 1 = 1/10',
                    tot='P = 1/5 + 1/10 = 3/10')


def validate() -> bool:
    seqs = set(permutations('RRRBB'))
    assert F(sum(s[0] == s[1] != s[2] for s in seqs), len(seqs)) == F(3, 10)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS210(TreeMixin, ShortScene):
    N = 210

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.3, width=6.6, root_label='rút', r=.38,
                                                  edge_size=28)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        stop3 = [n for n, path in self.leaves if len(path) == 3 and path[-1][0] != path[-2][0]]
        self.play(*[n.animate.scale(1.35).set_stroke(GREEN, 5) for n in stop3], run_time=self.rt(.06))
        self.write_board(self.M('rrb', 1.8))
        self.wait_until(.5, t0)
        self.write_board(self.M('bbr', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 2.1)
        self.write_board(m)
        self.frame(m)

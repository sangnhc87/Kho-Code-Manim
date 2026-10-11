"""XSS122 · Trung bình rút mấy lần? — cây dừng sớm 2/5, 3/10, 1/5, 1/10; kỳ vọng 2 = (5 + 1)/(2 + 1)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS122', 'answer': '2'}
PROBLEM = ['Hộp $2$ đỏ $3$ xanh, rút lần lượt không',
           'hoàn lại đến khi được bi đỏ. Trung',
           'bình rút mấy lần?']
OPTIONS = ['"2,5"', '2', '3']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('Đ', CORAL, '2/5', []),
            ('X', CYAN, '3/5', [('Đ', CORAL, '2/4', []),
                                ('X', CYAN, '2/4', [('Đ', CORAL, '2/3', []),
                                                    ('X', CYAN, '1/3', [('Đ', CORAL, '1', [])])])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có hai bi đỏ và ba bi xanh. Rút lần lượt, không hoàn lại, cho đến khi gặp bi đỏ thì dừng. '
                         'Trung bình bạn phải rút bao nhiêu lần?'),
    Beat('guess', 'hook', 'Hai phẩy năm, hai, hay ba lần? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ cây dừng sớm: gặp đỏ là nhánh kết thúc, gặp xanh thì rút tiếp. '
                        'Tối đa bốn lần, vì chỉ có ba bi xanh.'),
    Beat('s2', 'solve', 'Nhân dọc từng nhánh: dừng ở lần một với xác suất hai phần năm, lần hai ba phần mười, '
                        'lần ba một phần năm, lần bốn một phần mười. Cộng lại vừa đúng bằng một.'),
    Beat('s3', 'solve', 'Kỳ vọng: một nhân hai phần năm, cộng hai nhân ba phần mười, cộng ba nhân một phần năm, '
                        'cộng bốn nhân một phần mười, bằng hai. Khớp với công thức năm cộng một chia hai cộng một!'),
    Beat('answer', 'solve', 'Đáp án: trung bình hai lần. Cây dừng sớm cho ta cả xác suất lẫn kỳ vọng!'),
    Beat('outro', 'outro', outro_text(122)),
]

FORMULAS = formulas('2', OPTIONS,
                    probs='2/5, quad 3/10, quad 1/5, quad 1/10',
                    exp='E = 2/5 + 6/10 + 3/5 + 4/10 = 2',
                    gen='E = (5 + 1)/(2 + 1) = 2')


def validate() -> bool:
    seqs = set(permutations('RRBBB'))
    assert F(sum(s.index('R') + 1 for s in seqs), len(seqs)) == 2
    assert F(2, 5) + F(3, 10) + F(1, 5) + F(1, 10) == 1
    assert 1 * F(2, 5) + 2 * F(3, 10) + 3 * F(1, 5) + 4 * F(1, 10) == 2 == F(5 + 1, 2 + 1)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS122(TreeMixin, ShortScene):
    N = 122

    def hook_visual(self, t0):
        self.board_top = -1.65
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=.98, width=6.8, root_label='rút', r=.36,
                                                  edge_size=30)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        for i in range(1, 5):
            self.wait_until(.12 + .17 * i, t0)
            self.play(FadeIn(self.levels[i], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[n.animate.scale(1.25) for n, _ in self.leaves], run_time=self.rt(.06))
        tags = [tx(f'lần {i}', 22, GOLD).next_to(n, [-1, 0, 0], buff=.12) for i, (n, _) in enumerate(self.leaves, 1)]
        self.play(*[FadeIn(t) for t in tags], run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('probs', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('exp', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.65, t0)
        self.write_board(self.M('gen', 1.8), anim='fade')



"""XSS168 · Hai bi đỏ từ hộp nào? — P(RR | I) = 1/10, P(RR | II) = 3/10: P(II | RR) = 3/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS168', 'answer': '3/4'}
PROBLEM = ['Hộp I: $2$ đỏ $3$ xanh; hộp II: $3$ đỏ $2$',
           'xanh. Chọn ngẫu nhiên $1$ hộp, rút $2$',
           'bi đều đỏ. Xác suất hộp II?']
OPTIONS = ['1/2', '3/4', '3/5']
CORRECT = 1
ANSWER_VALUE = .75
BRANCHES = [('I', CYAN, '1/2', [('ĐĐ', CORAL, '1/10', [])]),
            ('II', PURPLE, '1/2', [('ĐĐ', CORAL, '3/10', [])])]


def p_rr(box):
    pairs = list(combinations(box, 2))
    return F(sum(a == b == 'R' for a, b in pairs), len(pairs))


BEATS = [
    Beat('hook', 'hook', 'Hộp một có hai đỏ ba xanh, hộp hai có ba đỏ hai xanh. Chọn ngẫu nhiên một hộp rồi rút hai bi, cả hai đều đỏ. '
                         'Xác suất bạn đã chọn hộp hai là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần tư, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hộp một: rút hai đỏ có tổ hợp chập hai của hai trên tổ hợp chập hai của năm, bằng một phần mười. '
                        'Hộp hai: tổ hợp chập hai của ba trên mười, bằng ba phần mười.'),
    Beat('s2', 'solve', 'Mỗi hộp được chọn với xác suất một phần hai, nên hai lá "đỏ đỏ" có xác suất một phần hai mươi và ba phần hai mươi.'),
    Beat('s3', 'solve', 'Bayes: ba phần hai mươi chia bốn phần hai mươi, bằng ba phần tư. Hộp hai gấp ba lần khả năng tạo ra hai bi đỏ.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tư. Rút hai bi cùng lúc thì tính xác suất bằng tổ hợp, rồi đưa lên cây!'),
    Beat('outro', 'outro', outro_text(168)),
]

FORMULAS = formulas('3/4', OPTIONS,
                    pr='P(Đ Đ | I) = (C_2^2)/(C_5^2) = 1/10, quad P(Đ Đ | I I) = (C_3^2)/(C_5^2) = 3/10',
                    bayes='P(I I | Đ Đ) = (3/20)/(1/20 + 3/20) = 3/4')


def validate() -> bool:
    i, ii = p_rr('RRBBB'), p_rr('RRRBB')
    assert (i, ii) == (F(1, 10), F(3, 10)) and ii / (i + ii) == F(3, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS168(TreeMixin, ShortScene):
    N = 168

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.urns = VGroup(urn('RRBBB', 3, .3), urn('RRRBB', 3, .3)).arrange(buff=1.2).move_to([0, 1.6, 0])
        self.labs = VGroup(tx('hộp I', 24, CYAN).next_to(self.urns[0], [0, -1, 0]),
                           tx('hộp II', 24, PURPLE).next_to(self.urns[1], [0, -1, 0]))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.urns), FadeIn(self.labs), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('pr', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), self.labs.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns, self.labs)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.6, root_label='chọn hộp')
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.2))
        self.wait_until(.6, t0)
        self.play(*[n.animate.scale(1.25) for n, _ in self.leaves], run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)



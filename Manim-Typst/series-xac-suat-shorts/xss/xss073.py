"""XSS073 · Bi đỏ từ hộp nào? — Bayes: P(hộp I | đỏ) = (3/10)/(2/5) = 3/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402
from xss.xss072 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS073', 'answer': '3/4'}
PROBLEM = ['Hộp I: $3$ đỏ, $2$ xanh. Hộp II: $1$ đỏ, $4$ xanh. Chọn một hộp,',
           'rút $1$ bi được bi đỏ. Xác suất bi đó từ hộp I?']
OPTIONS = ['1/2', '3/4', '3/5']
CORRECT = 1
ANSWER_VALUE = .75

BEATS = [
    Beat('hook', 'hook', 'Cùng hai hộp như thử thách trước. Một bạn chọn hộp, rút ra một viên bi đỏ, nhưng không nói hộp nào. '
                         'Xác suất viên đỏ đó đến từ hộp một là bao nhiêu? Hai hộp được chọn như nhau mà!'),
    Beat('guess', 'hook', 'Một phần hai, ba phần tư, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết bi đỏ, chỉ giữ hai nhánh dẫn tới bi đỏ: hộp một rồi đỏ, ba phần mười; '
                        'hộp hai rồi đỏ, một phần mười. Tổng hai phần năm.'),
    Beat('s2', 'solve', 'Phần của hộp một: ba phần mười chia hai phần năm, bằng ba phần tư. Đây là công thức Bayes.'),
    Beat('s3', 'solve', 'Trực giác: hộp một có ba viên đỏ, hộp hai chỉ một viên đỏ. '
                        'Thấy bi đỏ, ta tin hộp một gấp ba lần: ba phần tư so với một phần tư.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tư. Kết quả quan sát được làm nghiêng cán cân về nguyên nhân dễ gây ra nó hơn.'),
    Beat('outro', 'outro', outro_text(73)),
]

FORMULAS = formulas('3/4', OPTIONS,
                    tot='P("đỏ") = 3/10 + 1/10 = 2/5',
                    bayes='P("I" | "đỏ") = (3/10)/(2/5) = 3/4')


def validate() -> bool:
    assert F(1, 2) * F(3, 5) / (F(1, 2) * F(3, 5) + F(1, 2) * F(1, 5)) == F(3, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS073(TreeMixin, ShortScene):
    N = 73

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='chọn hộp')
        self.wait_until(.65, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[1][0].animate.set_opacity(.2), self.leaves[3][0].animate.set_opacity(.2),
                  run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.write_board(self.M('tot', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.35), run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.clear_board(.03)
        m = self.M('bayes', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(tx('3 viên đỏ so với 1 viên đỏ', 30, CYAN, bold=True), anim='fade')
        self.write_board(tx('tin hộp I gấp 3 lần', 28, GOLD), anim='fade')



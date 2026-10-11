"""XSS227 · Bi giấu màu gì? — biết bi rút ra đỏ: P(bi giấu đỏ) = (3/10)/(3/5) = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL  # noqa: E402
from xss.xss226 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS227', 'answer': '1/2'}
PROBLEM = ['Hộp $3$ đỏ $2$ xanh. Lấy $1$ bi cất đi không',
           'xem, rút $1$ bi được đỏ. Xác suất bi',
           'đã cất đi cũng màu đỏ?']
OPTIONS = ['3/5', '1/2', '2/5']
CORRECT = 1
ANSWER_VALUE = .5

BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: bi bị giấu, bạn rút được bi đỏ. Bây giờ xác suất bi bị giấu cũng màu đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần năm, một phần hai, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trên cây: giấu đỏ rồi rút đỏ, ba phần năm nhân hai phần tư bằng ba phần mười; giấu xanh rồi rút đỏ, hai phần năm nhân ba phần tư bằng ba phần mười.'),
    Beat('s2', 'solve', 'Hai lá bằng nhau! Bayes: ba phần mười chia sáu phần mười, bằng một phần hai.'),
    Beat('s3', 'solve', 'Cách nhìn đối xứng: bi giấu và bi rút là hai bi ngẫu nhiên khác nhau. Biết một bi đỏ, bi kia là một trong bốn bi còn lại: hai đỏ hai xanh.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Bi giấu không làm đổi xác suất bi rút, nhưng bi rút lại cho ta thông tin về bi giấu!'),
    Beat('outro', 'outro', outro_text(227)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    leaves='3/5 dot 2/4 = 3/10, quad 2/5 dot 3/4 = 3/10',
                    bayes='P("giấu Đ" | "rút Đ") = (3/10)/(6/10) = 1/2')


def validate() -> bool:
    seqs = [s for s in permutations('RRRBB', 2) if s[1] == 'R']
    assert F(sum(s[0] == 'R' for s in seqs), len(seqs)) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS227(TreeMixin, ShortScene):
    N = 227

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='bi bị giấu')
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[n.animate.scale(1.25) for n, _ in self.leaves], run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.write_board(self.M('leaves', 1.7))

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('còn $2$ đỏ $2$ xanh', 28, CORAL, bold=True), anim='fade')

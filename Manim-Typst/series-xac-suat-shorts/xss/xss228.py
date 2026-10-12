"""XSS228 · Chuyền qua ba hộp — I (2Đ) → II (1Đ1X) → III (1Đ1X), rút III: 2/3·2/3 + 1/3·1/3 = 5/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS228', 'answer': '5/9'}
PROBLEM = ['Hộp I: $2$ đỏ; II và III: mỗi hộp $1$ đỏ',
           '$1$ xanh. Chuyển $1$ bi I → II → III rồi',
           'rút từ III. Xác suất được đỏ?']
OPTIONS = ['1/2', '5/9', '2/3']
CORRECT = 1
ANSWER_VALUE = 5 / 9
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '2/3', [(*D, '2/3', [])]),
            (*X, '1/3', [(*D, '1/3', [])])]


def chain():
    red = F(1)  # bi chuyển từ I chắc chắn đỏ
    red = red * F(2, 3) + (1 - red) * F(1, 3)  # bi chuyển từ II
    return red * F(2, 3) + (1 - red) * F(1, 3)


BEATS = [
    Beat('hook', 'hook', 'Hộp một chỉ có hai bi đỏ. Hộp hai và hộp ba mỗi hộp một đỏ một xanh. Chuyển một bi từ hộp một sang hộp hai, '
                         'rồi một bi từ hộp hai sang hộp ba, rồi rút từ hộp ba. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, năm phần chín, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bước một chắc chắn chuyển đỏ: hộp hai thành hai đỏ một xanh. Bước hai: bi chuyển sang hộp ba là đỏ hai phần ba, xanh một phần ba.'),
    Beat('s2', 'solve', 'Chuyển đỏ: hộp ba hai đỏ một xanh, rút đỏ hai phần ba. Chuyển xanh: hộp ba một đỏ hai xanh, rút đỏ một phần ba.'),
    Beat('s3', 'solve', 'Toàn phần: hai phần ba nhân hai phần ba cộng một phần ba nhân một phần ba, bằng năm phần chín. '
                        'Ảnh hưởng của hộp một yếu dần qua mỗi lần chuyền: một, rồi hai phần ba, rồi năm phần chín.'),
    Beat('answer', 'solve', 'Đáp án: năm phần chín. Chuyền càng xa, thông tin ban đầu càng nhạt dần về một phần hai!'),
    Beat('outro', 'outro', outro_text(228)),
]

FORMULAS = formulas('5/9', OPTIONS,
                    tot='P = 2/3 dot 2/3 + 1/3 dot 1/3 = 5/9',
                    fade='1 arrow.r 2/3 arrow.r 5/9 arrow.r 1/2')


def validate() -> bool:
    assert chain() == F(5, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS228(TreeMixin, ShortScene):
    N = 228

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.urns = urn_row([('RR', 'I', SOFT), ('RB', 'II', SOFT), ('RB', 'III', SOFT)], y=1.4, buff=.6)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(self.urns.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.6, root_label='bi II → III')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('tot', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.M('fade', 1.8), anim='fade')

"""XSS129 · Rút rồi đổi màu — hộp thay đổi theo nhánh: 2/3·1/3 + 1/3·1 = 5/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS129', 'answer': '5/9'}
PROBLEM = ['Hộp $2$ đỏ $1$ xanh. Rút $1$ bi, thay',
           'bằng $1$ bi màu kia, rồi rút tiếp.',
           'Xác suất lần hai được đỏ?']
OPTIONS = ['2/3', '5/9', '4/9']
CORRECT = 1
ANSWER_VALUE = 5 / 9
BRANCHES = [('Đ', CORAL, '2/3', [('Đ', CORAL, '1/3', []), ('X', CYAN, '2/3', [])]),
            ('X', CYAN, '1/3', [('Đ', CORAL, '1', []), ('X', CYAN, '0', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp có hai bi đỏ và một bi xanh. Rút một bi, rồi thay nó bằng một bi màu kia bỏ vào hộp. '
                         'Sau đó rút tiếp. Xác suất lần hai rút được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần ba, năm phần chín, hay bốn phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điểm đặc biệt: sau lần rút đầu, hộp thay đổi khác nhau ở mỗi nhánh. '
                        'Rút đỏ thì hộp còn một đỏ hai xanh; rút xanh thì hộp thành ba đỏ.'),
    Beat('s2', 'solve', 'Nhánh đỏ rồi đỏ: hai phần ba nhân một phần ba, bằng hai phần chín. '
                        'Nhánh xanh rồi đỏ: một phần ba nhân một, bằng một phần ba.'),
    Beat('s3', 'solve', 'Cộng lại: hai phần chín cộng ba phần chín, bằng năm phần chín. '
                        'Xác suất đỏ giảm từ hai phần ba xuống năm phần chín, vì việc đổi màu kéo hộp về thế cân bằng.'),
    Beat('answer', 'solve', 'Đáp án: năm phần chín. Khi hộp thay đổi theo nhánh, hãy ghi trạng thái hộp ngay trên từng nhánh cây!'),
    Beat('outro', 'outro', outro_text(129)),
]

FORMULAS = formulas('5/9', OPTIONS,
                    rr='2/3 dot 1/3 = 2/9',
                    br='1/3 dot 1 = 1/3',
                    tot='P = 2/9 + 3/9 = 5/9')


def validate() -> bool:
    assert F(2, 3) * F(1, 3) + F(1, 3) * 1 == F(5, 9)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS129(TreeMixin, ShortScene):
    N = 129

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.u = urn('RRB', cols=3, r=.36).move_to([0, 1.5, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.u.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.u)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='lần 1')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        states = VGroup(VGroup(urn('RBB', cols=3, r=.17), tx('còn 1 đỏ 2 xanh', 18, SOFT)).arrange(buff=.1),
                        VGroup(urn('RRR', cols=3, r=.17), tx('thành 3 đỏ', 18, SOFT)).arrange(buff=.1))
        for st, (n, _) in zip(states, [(self.levels[1][2], None), (self.levels[1][-1], None)]):
            st.next_to(n, [0, -1, 0], buff=.12)
        self.play(FadeIn(states, lag_ratio=.4), run_time=self.rt(.1))
        self.wait_until(.75, t0)
        self.play(states.animate.set_opacity(0), run_time=self.rt(.03))
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('rr', 2.0))
        self.wait_until(.5, t0)
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('br', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 2.2)
        self.write_board(m)
        self.frame(m)

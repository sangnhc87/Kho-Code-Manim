"""XSS072 · Chọn hộp rồi rút bi — toàn phần: 1/2 · 3/5 + 1/2 · 1/5 = 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, PURPLE  # noqa: E402
from common.visuals import BALL_COLORS, urn  # noqa: E402

EPISODE = {'code': 'XSS072', 'answer': '2/5'}
PROBLEM = ['Hộp I: $3$ đỏ, $2$ xanh. Hộp II: $1$ đỏ, $4$ xanh.', 'Chọn ngẫu nhiên một hộp rồi rút $1$ bi. $P("đỏ")$?']
OPTIONS = ['1/2', '2/5', '4/5']
CORRECT = 1
ANSWER_VALUE = .4
RED, BLUE = BALL_COLORS['R'], BALL_COLORS['B']
BRANCHES = [('I', CYAN, '1/2', [('Đ', RED, '3/5', []), ('X', BLUE, '2/5', [])]),
            ('II', PURPLE, '1/2', [('Đ', RED, '1/5', []), ('X', BLUE, '4/5', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp một có ba bi đỏ, hai bi xanh. Hộp hai có một bi đỏ, bốn bi xanh. '
                         'Chọn ngẫu nhiên một hộp, rồi rút một viên. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần năm, hay bốn phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai bước nối tiếp nhau: chọn hộp, rồi rút bi. Vẽ cây: mỗi hộp được chọn với xác suất một phần hai, '
                        'sau đó xác suất ra đỏ tùy theo hộp.'),
    Beat('s2', 'solve', 'Nhánh hộp một rồi đỏ: một phần hai nhân ba phần năm, bằng ba phần mười. '
                        'Nhánh hộp hai rồi đỏ: một phần hai nhân một phần năm, bằng một phần mười.'),
    Beat('s3', 'solve', 'Cộng hai nhánh: bốn phần mười, tức hai phần năm. Bẫy bốn phần năm là gộp cả hai hộp '
                        'thành một rồi đếm, sai vì mỗi viên bi không có cùng cơ hội được rút.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Xác suất toàn phần: nhân dọc từng nhánh, cộng các nhánh cùng kết quả.'),
    Beat('outro', 'outro', outro_text(72)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    one='1/2 dot 3/5 = 3/10',
                    two='1/2 dot 1/5 = 1/10',
                    tot='P("đỏ") = 3/10 + 1/10 = 2/5')


def validate() -> bool:
    assert F(1, 2) * F(3, 5) + F(1, 2) * F(1, 5) == F(2, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS072(TreeMixin, ShortScene):
    N = 72

    def hook_visual(self, t0):
        self.urns = VGroup(urn('RRRBB', 5, .3), urn('RBBBB', 5, .3)).arrange(buff=.6).move_to([0, 1.4, 0])
        labs = VGroup(tx('hộp I', 26, CYAN, bold=True).next_to(self.urns[0], DOWN, buff=.15),
                      tx('hộp II', 26, PURPLE, bold=True).next_to(self.urns[1], DOWN, buff=.15))
        self.urn_labels = labs
        self.wait_until(.5, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), FadeIn(labs), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), self.urn_labels.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.urns, self.urn_labels)
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='chọn hộp')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('one', 2.0))
        self.wait_until(.5, t0)
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('two', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(tx('gộp 2 hộp rồi đếm: SAI', 26, CORAL, bold=True), anim='fade')



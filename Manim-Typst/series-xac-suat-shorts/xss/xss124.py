"""XSS124 · Thi bằng lái ba lần — xác suất đổi theo nhánh: 1 − 0,4·0,3·0,2 = 0,976."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS124', 'answer': '0,976'}
PROBLEM = ['Thi bằng lái: lần $1$ đậu $"0,6"$; trượt',
           'thì lần $2$ đậu $"0,7"$; trượt nữa thì lần',
           '$3$ đậu $"0,8"$. Xác suất đậu?']
OPTIONS = ['"0,7"', '"0,976"', '"0,336"']
CORRECT = 1
ANSWER_VALUE = .976
BRANCHES = [('Đ', GREEN, '"0,6"', []),
            ('T', CORAL, '"0,4"', [('Đ', GREEN, '"0,7"', []),
                                   ('T', CORAL, '"0,3"', [('Đ', GREEN, '"0,8"', []), ('T', CORAL, '"0,2"', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Thi bằng lái được tối đa ba lần. Lần đầu đậu với xác suất không phẩy sáu. '
                         'Trượt thì rút kinh nghiệm, lần hai đậu không phẩy bảy, lần ba đậu không phẩy tám. '
                         'Xác suất cuối cùng có bằng lái là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bảy, không phẩy chín bảy sáu, hay không phẩy ba ba sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điểm mới của cây này: xác suất trên mỗi tầng thay đổi, vì nó là xác suất có điều kiện, '
                        'biết các lần trước đã trượt.'),
    Beat('s2', 'solve', 'Chỉ có một nhánh không có bằng: trượt, trượt, trượt. Nhân dọc: không phẩy bốn nhân không phẩy ba '
                        'nhân không phẩy hai, bằng không phẩy không hai bốn.'),
    Beat('s3', 'solve', 'Xác suất đậu bằng một trừ không phẩy không hai bốn, được không phẩy chín bảy sáu. '
                        'Bẫy thường gặp: nhân không phẩy sáu, bảy, tám thành không phẩy ba ba sáu, đó là xác suất đậu cả ba lần, vô nghĩa!'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín bảy sáu. Kiên trì thì gần như chắc chắn đậu!'),
    Beat('outro', 'outro', outro_text(124)),
]

FORMULAS = formulas('"0,976"', OPTIONS,
                    fail='P("trượt cả 3") = "0,4" dot "0,3" dot "0,2" = "0,024"',
                    comp='P = 1 - "0,024" = "0,976"')


def validate() -> bool:
    assert round(1 - .4 * .3 * .2, 3) == .976 == round(.6 + .4 * .7 + .4 * .3 * .8, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS124(TreeMixin, ShortScene):
    N = 124

    def hook_visual(self, t0):
        self.board_top = -1.9
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.25, width=6.4, root_label='lần 1', r=.4,
                                                  edge_size=30)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('Đ: đậu   T: trượt', 24, SOFT).move_to([0, -1.5, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[-1][0].animate.scale(1.4), run_time=self.rt(.05))
        self.wait_until(.35, t0)
        self.write_board(self.M('fail', 1.8))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('comp', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(self.TM('$"0,6" dot "0,7" dot "0,8"$: bẫy!', 28, CORAL, bold=True), anim='fade')



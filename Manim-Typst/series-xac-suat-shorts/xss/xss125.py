"""XSS125 · Mưa hai ngày tới — cây 2 bước (chuỗi Markov): 0,6·0,6 + 0,4·0,2 = 0,44."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS125', 'answer': '0,44'}
PROBLEM = ['Hôm nay mưa. Nếu mưa thì hôm sau',
           'mưa $"0,6"$; nếu tạnh thì hôm sau mưa',
           '$"0,2"$. Xác suất ngày kia mưa?']
OPTIONS = ['"0,6"', '"0,44"', '"0,36"']
CORRECT = 1
ANSWER_VALUE = .44
BRANCHES = [('M', CYAN, '"0,6"', [('M', CYAN, '"0,6"', []), ('T', GOLD, '"0,4"', [])]),
            ('T', GOLD, '"0,4"', [('M', CYAN, '"0,2"', []), ('T', GOLD, '"0,8"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Thời tiết có trí nhớ ngắn: hôm nay mưa thì ngày mai mưa với xác suất không phẩy sáu, '
                         'hôm nay tạnh thì mai mưa chỉ không phẩy hai. Hôm nay đang mưa. Xác suất ngày kia mưa là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy sáu, không phẩy bốn bốn, hay không phẩy ba sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một là ngày mai: mưa không phẩy sáu, tạnh không phẩy bốn. '
                        'Tầng hai là ngày kia, xác suất phụ thuộc vào ngày mai ra sao.'),
    Beat('s2', 'solve', 'Hai nhánh dẫn tới ngày kia mưa: mưa rồi mưa, không phẩy sáu nhân không phẩy sáu bằng không phẩy ba sáu; '
                        'tạnh rồi mưa, không phẩy bốn nhân không phẩy hai bằng không phẩy không tám.'),
    Beat('s3', 'solve', 'Cộng lại: không phẩy bốn bốn. Không phẩy ba sáu chỉ là một nhánh, quên nhánh tạnh rồi mưa trở lại.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bốn bốn. Đây là chuỗi Markov, mô hình dùng cho dự báo thời tiết và cả trí tuệ nhân tạo!'),
    Beat('outro', 'outro', outro_text(125)),
]

FORMULAS = formulas('"0,44"', OPTIONS,
                    mm='"0,6" dot "0,6" = "0,36"',
                    tm='"0,4" dot "0,2" = "0,08"',
                    tot='P = "0,36" + "0,08" = "0,44"')


def validate() -> bool:
    assert round(.6 * .6 + .4 * .2, 2) == .44
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS125(TreeMixin, ShortScene):
    N = 125

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.05), dy=1.75, width=6.8, root_label='hôm nay mưa')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('M: mưa   T: tạnh', 24, SOFT).move_to([0, -.95, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('mm', 2.0))
        self.wait_until(.55, t0)
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('tm', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('chỉ "0,36": quên một nhánh', 28, CORAL, bold=True), anim='fade')

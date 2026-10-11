"""XSS077 · Tắc đường vì mưa? — Bayes: P(mưa | tắc) = 0,18/0,32 = 9/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD  # noqa: E402
from xss.xss076 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS077', 'answer': '9/16'}
PROBLEM = ['$P("mưa") = "0,3"$; tắc đường: $"0,6"$ khi mưa, $"0,2"$ khi không.',
           'Hôm nay bị tắc đường. Xác suất trời đã mưa?']
OPTIONS = ['"0,3"', '9/16', '"0,6"']
CORRECT = 1
ANSWER_VALUE = 9 / 16

BEATS = [
    Beat('hook', 'hook', 'Bạn ngồi trong phòng kín, nghe tin đường đang tắc. Biết xác suất mưa là không phẩy ba, '
                         'tắc khi mưa không phẩy sáu, tắc khi khô ráo không phẩy hai. Xác suất bên ngoài đang mưa là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy ba, chín phần mười sáu, hay không phẩy sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết đã tắc đường, chỉ giữ hai nhánh dẫn tới tắc: mưa rồi tắc không phẩy một tám, '
                        'không mưa rồi tắc không phẩy một bốn. Tổng không phẩy ba hai.'),
    Beat('s2', 'solve', 'Bayes: phần của nhánh mưa trong tổng, không phẩy một tám chia không phẩy ba hai, bằng chín phần mười sáu.'),
    Beat('s3', 'solve', 'Trước khi biết tin, xác suất mưa chỉ không phẩy ba. Tin tắc đường đã nâng lên hơn một nửa. '
                        'Bằng chứng mới làm thay đổi niềm tin, đúng như cách bộ não ta suy luận hằng ngày.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười sáu. Từ không phẩy ba lên khoảng không phẩy năm sáu nhờ một manh mối!'),
    Beat('outro', 'outro', outro_text(77)),
]

FORMULAS = formulas('9/16', OPTIONS,
                    tot='P(T) = "0,18" + "0,14" = "0,32"',
                    bayes='P(M | T) = ("0,18")/("0,32") = 9/16')


def validate() -> bool:
    assert F(18, 100) / (F(18, 100) + F(14, 100)) == F(9, 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS077(TreeMixin, ShortScene):
    N = 77

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='hôm nay')
        self.wait_until(.7, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[1][0].animate.set_opacity(.2), self.leaves[3][0].animate.set_opacity(.2), run_time=self.rt(.06))
        self.wait_until(.6, t0)
        self.write_board(self.M('tot', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.35), run_time=self.rt(.05))
        self.wait_until(.25, t0)
        self.clear_board(.03)
        m = self.M('bayes', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.TM('$"0,3" arrow.r 9/16$', 34, GOLD, bold=True), anim='fade')
        self.write_board(tx('một manh mối thay đổi niềm tin', 26, CYAN), anim='fade')



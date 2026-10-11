"""XSS135 · Ra 6 vì tung ngửa? — Bayes trên cây của XSS134: (6/72)/(11/72) = 6/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402
from xss.xss134 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS135', 'answer': '6/11'}
PROBLEM = ['Tung xu: ngửa gieo $1$ xúc xắc, sấp',
           'gieo $2$ xúc xắc. Biết tổng số chấm',
           'bằng $6$. Xác suất đã tung ngửa?']
OPTIONS = ['1/2', '6/11', '5/11']
CORRECT = 1
ANSWER_VALUE = 6 / 11

BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: tung xu, ngửa thì gieo một xúc xắc, sấp thì gieo hai. '
                         'Bạn chỉ được báo kết quả là sáu. Xác suất đồng xu đã ra ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, sáu phần mười một, hay năm phần mười một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trên cây, chỉ hai lá cho kết quả sáu: lá ngửa với xác suất sáu phần bảy mươi hai, '
                        'lá sấp với năm phần bảy mươi hai. Các lá khác bị loại vì trái với điều kiện.'),
    Beat('s2', 'solve', 'Xác suất có điều kiện bằng phần của lá ngửa trong tổng hai lá: '
                        'sáu phần bảy mươi hai chia mười một phần bảy mươi hai, bằng sáu phần mười một.'),
    Beat('s3', 'solve', 'Trước khi biết kết quả, ngửa và sấp như nhau. Biết ra sáu, ngửa hơi được ưu tiên, '
                        'vì một xúc xắc ra sáu dễ hơn hai xúc xắc có tổng sáu.'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười một. Bayes trên cây: giữ lại các lá phù hợp, rồi lấy tỉ lệ!'),
    Beat('outro', 'outro', outro_text(135)),
]

FORMULAS = formulas('6/11', OPTIONS,
                    leaves='6/72 " (ngửa)", quad 5/72 " (sấp)"',
                    bayes='P(N | "tổng 6") = (6/72)/(11/72) = 6/11')


def validate() -> bool:
    assert (F(1, 2) * F(1, 6)) / (F(1, 2) * F(1, 6) + F(1, 2) * F(5, 36)) == F(6, 11)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS135(TreeMixin, ShortScene):
    N = 135

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='tung xu')
        self.wait_until(.55, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        keep = [self.leaves[0][0], self.leaves[2][0]]
        drop = [self.leaves[1][0], self.leaves[3][0]]
        self.play(*[n.animate.set_opacity(.15) for n in drop], *[n.animate.scale(1.3).set_stroke(GREEN, 5) for n in keep],
                  run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('leaves', 1.8))

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(tx('một xúc xắc ra 6 dễ hơn', 28, CORAL, bold=True), anim='fade')

"""XSS105 · Bayes sau khi chuyển bi — biết rút được đỏ: P(đã chuyển 2 đỏ) = (30/120)/(65/120) = 6/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from xss.xss104 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS105', 'answer': '6/13'}
PROBLEM = ['Như thử thách #$104$: chuyển $2$ bi từ hộp',
           'I sang hộp II rồi rút $1$ bi được bi đỏ.',
           '$P("2 bi đã chuyển đều đỏ")$?']
OPTIONS = ['2/5', '6/13', '1/2']
CORRECT = 1
ANSWER_VALUE = 6 / 13

BEATS = [
    Beat('hook', 'hook', 'Quay lại hai hộp ở thử thách trước. Người chơi chuyển hai viên rồi rút được một viên đỏ ở hộp hai. '
                         'Biết điều đó, xác suất hai viên đã chuyển đều màu đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần năm, sáu phần mười ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trước khi rút, xác suất chuyển hai đỏ là sáu phần mười lăm, tức không phẩy bốn. '
                        'Viên đỏ rút được là một bằng chứng mới.'),
    Beat('s2', 'solve', 'Nhánh chuyển hai đỏ rồi rút đỏ: sáu phần mười lăm nhân năm phần tám, bằng ba mươi phần một trăm hai mươi. '
                        'Tổng các nhánh rút đỏ, từ thử thách trước, là sáu mươi lăm phần một trăm hai mươi.'),
    Beat('s3', 'solve', 'Bayes: ba mươi chia sáu mươi lăm, bằng sáu phần mười ba, khoảng không phẩy bốn sáu. '
                        'Viên đỏ làm tăng niềm tin rằng hộp hai đã được thêm nhiều bi đỏ.'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười ba. Đây là cặp câu toàn phần rồi Bayes rất hay gặp trong đề thi tốt nghiệp mới!'),
    Beat('outro', 'outro', outro_text(105)),
]

FORMULAS = formulas('6/13', OPTIONS,
                    prior='P("2 đỏ") = 6/15 = "0,4"',
                    bayes='P("2 đỏ" | "đỏ") = (30/120)/(65/120) = 6/13')


def validate() -> bool:
    box1 = 'RRRRBB'
    num = den = F(0)
    for pick in combinations(range(6), 2):
        reds = sum(box1[i] == 'R' for i in pick)
        p = F(1, comb(6, 2)) * F(3 + reds, 8)
        den += p
        num += p if reds == 2 else 0
    assert num == F(30, 120) and den == F(65, 120) and num / den == F(6, 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS105(TreeMixin, ShortScene):
    N = 105

    def hook_visual(self, t0):
        self.board_top = -1.1
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=6.6, root_label='chuyển 2 bi')
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(self.M('prior', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.35), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        self.write_board(self.TM('tổng nhánh đỏ: $65/120$', 30, SOFT), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('bayes', 1.7)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.TM('$"0,4" arrow.r 6/13 approx "0,46"$', 32, GOLD, bold=True), anim='fade')

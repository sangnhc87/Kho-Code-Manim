"""XSS232 · Đi một vòng trở về — I (3Đ2X) → II (2Đ3X) → I: P(I như cũ) = 3/5·3/6 + 2/5·4/6 = 17/30."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402

EPISODE = {'code': 'XSS232', 'answer': '17/30'}
PROBLEM = ['Hộp I: $3$ đỏ $2$ xanh; II: $2$ đỏ $3$ xanh.',
           'Chuyển $1$ bi I → II, rồi $1$ bi II → I.',
           'Xác suất hộp I trở lại như cũ?']
OPTIONS = ['1/2', '17/30', '3/5']
CORRECT = 1
ANSWER_VALUE = 17 / 30
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '3/5', [(*D, '3/6', []), (*X, '3/6', [])]),
            (*X, '2/5', [(*D, '2/6', []), (*X, '4/6', [])])]


def same():
    tot = F(0)
    for i, a in enumerate('RRRBB'):
        for b in 'RRBBB' + a:
            tot += F(1, 5) * F(1, 6) * (a == b)
    return tot


BEATS = [
    Beat('hook', 'hook', 'Hộp một có ba đỏ hai xanh, hộp hai có hai đỏ ba xanh. Chuyển một bi từ hộp một sang hộp hai, rồi chuyển một bi ngược lại. '
                         'Xác suất hộp một trở lại đúng ba đỏ hai xanh là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, mười bảy phần ba mươi, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hộp một như cũ khi bi về cùng màu với bi đi. Đi đỏ, ba phần năm: hộp hai thành ba đỏ ba xanh, về đỏ ba phần sáu.'),
    Beat('s2', 'solve', 'Đi xanh, hai phần năm: hộp hai thành hai đỏ bốn xanh, về xanh bốn phần sáu.'),
    Beat('s3', 'solve', 'Cộng hai nhánh: ba phần năm nhân ba phần sáu cộng hai phần năm nhân bốn phần sáu, bằng chín cộng tám trên ba mươi, '
                        'tức mười bảy phần ba mươi.'),
    Beat('answer', 'solve', 'Đáp án: mười bảy phần ba mươi. Câu hỏi về "trạng thái" của hộp: chỉ cần bi đi và bi về cùng màu!'),
    Beat('outro', 'outro', outro_text(232)),
]

FORMULAS = formulas('17/30', OPTIONS,
                    tot='P = 3/5 dot 3/6 + 2/5 dot 4/6 = 9/30 + 8/30 = 17/30')


def validate() -> bool:
    assert same() == F(17, 30)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS232(TreeMixin, ShortScene):
    N = 232

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=6.8, root_label='đi, về')
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(self.leaves[0][0].animate.scale(1.3).set_stroke(GREEN, 5), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.play(self.leaves[3][0].animate.scale(1.3).set_stroke(GREEN, 5), run_time=self.rt(.05))
        self.play(*[self.leaves[i][0].animate.set_opacity(.15) for i in (1, 2)], run_time=self.rt(.03))

    def beat_s3(self, T):
        m = self.M('tot', 1.6)
        self.write_board(m)
        self.frame(m)



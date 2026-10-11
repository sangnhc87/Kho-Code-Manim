"""XSS207 · Hoàn lại vẫn phụ thuộc — rút có hoàn lại: P(Đ₂ | Đ₁) = (1/2·16/25 + 1/2·1/25)/(1/2) = 17/25 ≠ 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS207', 'answer': '17/25'}
PROBLEM = ['Như trên (hộp I: $4$ đỏ $1$ xanh; II: $1$',
           'đỏ $4$ xanh) nhưng rút có hoàn lại: lần',
           '$1$ đỏ. Xác suất lần $2$ cũng đỏ?']
OPTIONS = ['1/2', '17/25', '3/5']
CORRECT = 1
ANSWER_VALUE = 17 / 25
BRANCHES = [('I', GOLD, '4/5', [('Đ', CORAL, '4/5', [])]),
            ('II', PURPLE, '1/5', [('Đ', CORAL, '1/5', [])])]

BEATS = [
    Beat('hook', 'hook', 'Vẫn hai hộp đó, chọn hộp bằng đồng xu, nhưng lần này rút có hoàn lại. Lần một rút được đỏ. '
                         'Bỏ bi lại vào hộp, rút lần hai. Có hoàn lại thì hai lần độc lập, vậy đỏ với xác suất một phần hai?'),
    Beat('guess', 'hook', 'Một phần hai, mười bảy phần hai mươi lăm, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bẫy ở đây: có hoàn lại thì độc lập khi biết hộp, nhưng ta không biết hộp. Lần một đỏ khiến ta nghiêng về hộp một, bốn phần năm.'),
    Beat('s2', 'solve', 'Lần hai: hộp một đỏ bốn phần năm, hộp hai đỏ một phần năm. Toàn phần: bốn phần năm nhân bốn phần năm cộng một phần năm nhân một phần năm.'),
    Beat('s3', 'solve', 'Bằng mười sáu phần hai mươi lăm cộng một phần hai mươi lăm, tức mười bảy phần hai mươi lăm, lớn hơn hẳn một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: mười bảy phần hai mươi lăm. Độc lập có điều kiện không có nghĩa là độc lập!'),
    Beat('outro', 'outro', outro_text(207)),
]

FORMULAS = formulas('17/25', OPTIONS,
                    tot='P(Đ_2 | Đ_1) = 4/5 dot 4/5 + 1/5 dot 1/5 = 17/25',
                    trap='17/25 eq.not P(Đ_2) = 1/2')


def validate() -> bool:
    both = F(1, 2) * F(4, 5) ** 2 + F(1, 2) * F(1, 5) ** 2
    assert both / F(1, 2) == F(17, 25)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS207(TreeMixin, ShortScene):
    N = 207

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=5.6, root_label='biết lần 1 đỏ')
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        m = self.M('tot', 1.7)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.M('trap', 1.9), anim='fade')

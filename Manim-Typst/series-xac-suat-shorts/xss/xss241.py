"""XSS241 · Xu bí ẩn: lần hai — xu chuẩn hoặc lệch (0,9): P(N₂ | N₁) = (1/2·1/4 + 1/2·0,81)/(0,7) = 53/70."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS241', 'answer': '53/70'}
PROBLEM = ['Chọn ngẫu nhiên xu chuẩn hoặc xu lệch',
           '(ngửa $"0,9"$), tung $2$ lần. Lần $1$ ra ngửa.',
           'Xác suất lần $2$ cũng ngửa?']
OPTIONS = ['"0,7"', '53/70', '"0,9"']
CORRECT = 1
ANSWER_VALUE = 53 / 70
BRANCHES = [('C', CYAN, '1/2', [('N', GOLD, '1/2', [('N', GOLD, '1/2', [])])]),
            ('L', CORAL, '1/2', [('N', GOLD, '"0,9"', [('N', GOLD, '"0,9"', [])])])]
P = (F(1, 2), F(9, 10))

BEATS = [
    Beat('hook', 'hook', 'Trong túi có một đồng xu chuẩn và một đồng xu lệch ra ngửa chín mươi phần trăm. Chọn ngẫu nhiên một đồng, tung hai lần. '
                         'Lần một ra ngửa. Xác suất lần hai cũng ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bảy, năm mươi ba phần bảy mươi, hay không phẩy chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Khi đã biết đồng xu nào, hai lần tung độc lập. Nhưng ta không biết, nên hai lần tung liên hệ với nhau qua đồng xu. '
                        'Lần một ngửa có xác suất một phần hai nhân không phẩy năm cộng một phần hai nhân không phẩy chín, bằng không phẩy bảy.'),
    Beat('s2', 'solve', 'Hai lần đều ngửa: một phần hai nhân không phẩy hai lăm cộng một phần hai nhân không phẩy tám mốt, bằng không phẩy năm ba.'),
    Beat('s3', 'solve', 'Xác suất có điều kiện: không phẩy năm ba chia không phẩy bảy, bằng năm mươi ba phần bảy mươi, khoảng không phẩy bảy sáu, lớn hơn không phẩy bảy.'),
    Beat('answer', 'solve', 'Đáp án: năm mươi ba phần bảy mươi. Độc lập khi biết đồng xu, nhưng phụ thuộc khi không biết!'),
    Beat('outro', 'outro', outro_text(241)),
]

FORMULAS = formulas('53/70', OPTIONS,
                    one='P(N_1) = 1/2 dot "0,5" + 1/2 dot "0,9" = "0,7"',
                    two='P(N_1 N_2) = 1/2 dot "0,25" + 1/2 dot "0,81" = "0,53"',
                    prob='P(N_2 | N_1) = ("0,53")/("0,7") = 53/70')


def validate() -> bool:
    assert (sum(p * p for p in P) / 2) / (sum(P) / 2) == F(53, 70)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS241(TreeMixin, ShortScene):
    N = 241

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.2, width=5.6, root_label='chọn xu', r=.4,
                                                  edge_size=28)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.write_board(self.M('one', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.3, t0)
        self.write_board(self.M('two', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)

"""XSS393 · Ba đồng xu, tung lại — chuẩn, NN, SS; P(N) = 1/2; P(N, N) = (1/4 + 1 + 0)/3 = 5/12 → P(lần 2 N | lần 1 N) = 5/6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS393', 'answer': '5/6'}
PROBLEM = ['Ba xu: chuẩn, hai mặt ngửa, hai mặt sấp.',
           'Chọn $1$, tung ra ngửa; tung lại đồng đó.',
           'Xác suất lại ra ngửa?']
OPTIONS = ['5/6', '2/3', '3/4']
CORRECT = 0
ANSWER_VALUE = 5 / 6
H = [F(1, 2), F(1), F(0)]
BRANCHES = [('C', CYAN, '1/3', [('N', GOLD, '1/2', [('N', GOLD, '1/2', [])])]),
            ('NN', GOLD, '1/3', [('N', GOLD, '1', [('N', GOLD, '1', [])])]),
            ('SS', SOFT, '1/3', [('N', GOLD, '0', [])])]

BEATS = [
    Beat('hook', 'hook', 'Có ba đồng xu: một đồng chuẩn, một đồng hai mặt đều ngửa, một đồng hai mặt đều sấp. Chọn ngẫu nhiên một đồng, tung ra ngửa. '
                         'Tung lại chính đồng đó. Xác suất lại ra ngửa?'),
    Beat('guess', 'hook', 'Năm phần sáu, hai phần ba, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây ba tầng: chọn đồng, lần tung một, lần tung hai. Đồng hai mặt sấp không bao giờ ra ngửa.'),
    Beat('s2', 'solve', 'Lần một ngửa: một phần ba nhân, một phần hai cộng một cộng không, bằng một phần hai.'),
    Beat('s3', 'solve', 'Hai lần đều ngửa: một phần ba nhân, một phần tư cộng một, bằng năm phần mười hai. Chia cho một phần hai: năm phần sáu.'),
    Beat('answer', 'solve', 'Đáp án: năm phần sáu. Lần ngửa đầu đã nghiêng niềm tin về đồng hai mặt ngửa, nên lần sau dễ ngửa hơn.'),
    Beat('outro', 'outro', outro_text(393)),
]

FORMULAS = formulas('5/6', OPTIONS,
                    one='P(N_1) = 1/3 (1/2 + 1 + 0) = 1/2',
                    two='P(N_1 N_2) = 1/3 (1/4 + 1 + 0) = 5/12',
                    prob='P(N_2 | N_1) = (5/12)/(1/2) = 5/6')


def validate() -> bool:
    one, two = sum(H) / 3, sum(h * h for h in H) / 3
    assert two / one == F(5, 6)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS393(TreeMixin, ShortScene):
    N = 393

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.25, width=6.0, r=.36, edge_size=26)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.2), FadeIn(self.levels[3], lag_ratio=.2), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('one', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('two', 1.4))
        self.wait_until(.6, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

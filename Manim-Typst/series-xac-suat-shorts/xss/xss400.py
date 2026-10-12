"""XSS400 · Ba tù nhân — cai ngục nói tên một người bị xử khác A: A tha (1/3) → nói B với 1/2; C tha (1/3) → nói B chắc chắn → P(A | "B") = 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS400', 'answer': '1/3'}
PROBLEM = ['$3$ tù nhân A, B, C, $1$ người được tha. Cai',
           'ngục (không nói về A) bảo A: "B sẽ bị xử".',
           'Xác suất A được tha?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 0
ANSWER_VALUE = 1 / 3
SAY_B = {'A': F(1, 2), 'B': F(0), 'C': F(1)}
BRANCHES = [('A', CYAN, '1/3', [('"B"', SOFT, '1/2', [])]),
            ('B', GOLD, '1/3', [('"B"', SOFT, '0', [])]),
            ('C', CORAL, '1/3', [('"B"', SOFT, '1', [])])]

BEATS = [
    Beat('hook', 'hook', 'Ba tù nhân A, B, C, một người sẽ được tha. A năn nỉ cai ngục, người biết đáp án nhưng không tiết lộ về A, cho biết tên một người khác bị xử. Cai ngục nói: B sẽ bị xử. '
                         'Bây giờ xác suất A được tha là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nếu A được tha, cai ngục chọn ngẫu nhiên giữa B và C: nói B với một phần hai. Nếu C được tha, cai ngục buộc phải nói B. Nếu B được tha thì không thể nói B.'),
    Beat('s2', 'solve', 'Hai lá còn lại: một phần ba nhân một phần hai bằng một phần sáu, và một phần ba nhân một bằng hai phần sáu.'),
    Beat('s3', 'solve', 'Bayes: một chia một cộng hai, vẫn là một phần ba. Còn C giờ có hai phần ba!'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Đây chính là bài toán Monty Hall, ra đời trước cả trò chơi truyền hình.'),
    Beat('outro', 'outro', outro_text(400)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    leafs='1/3 dot 1/2 = 1/6, quad 1/3 dot 1 = 2/6',
                    prob='P(A | "B") = 1/(1 + 2) = 1/3')


def validate() -> bool:
    tot = sum(F(1, 3) * v for v in SAY_B.values())
    assert F(1, 3) * SAY_B['A'] / tot == F(1, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS400(TreeMixin, ShortScene):
    N = 400

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.7, width=6.0, r=.4, edge_size=28)
        self.wait_until(.8, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.05))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.write_board(self.M('leafs', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

"""XSS224 · Đổi hai lần, về như cũ — xích Markov trên số bi đỏ ở I: P(I có lại 3Đ1X sau 2 lần) = 11/32."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402

EPISODE = {'code': 'XSS224', 'answer': '11/32'}
PROBLEM = ['I: $3$ đỏ $1$ xanh; II: $1$ đỏ $3$ xanh. Đổi',
           '$1$ bi giữa hai hộp, làm $2$ lần. Xác suất',
           'hộp I lại có đúng $3$ đỏ $1$ xanh?']
OPTIONS = ['3/8', '11/32', '9/32']
CORRECT = 1
ANSWER_VALUE = 11 / 32
BRANCHES = [('3', GOLD, '3/8', [('3', GOLD, '3/8', [])]),
            ('2', CYAN, '9/16', [('3', GOLD, '1/4', [])]),
            ('4', CORAL, '1/16', [('3', GOLD, '1', [])])]


def step(r):
    """I has r red of 4 (II has 4 − r red of 4). Returns {new r: prob}."""
    out = {}
    for out_red in (1, 0):
        p_out = F(r, 4) if out_red else F(4 - r, 4)
        for in_red in (1, 0):
            p_in = F(4 - r, 4) if in_red else F(r, 4)
            nr = r - out_red + in_red
            out[nr] = out.get(nr, 0) + p_out * p_in
    return {k: v for k, v in out.items() if v}


def two_steps():
    return sum(p * step(r).get(3, 0) for r, p in step(3).items())


BEATS = [
    Beat('hook', 'hook', 'Vẫn hai hộp: hộp một ba đỏ một xanh, hộp hai một đỏ ba xanh. Đổi ngẫu nhiên một bi giữa hai hộp, làm hai lần. '
                         'Xác suất hộp một lại có đúng ba đỏ một xanh như ban đầu là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tám, mười một phần ba mươi hai, hay chín phần ba mươi hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trạng thái chỉ cần một con số: số bi đỏ trong hộp một. Lần đổi đầu: giữ ba đỏ với xác suất ba phần tám, '
                        'xuống hai đỏ chín phần mười sáu, lên bốn đỏ một phần mười sáu.'),
    Beat('s2', 'solve', 'Lần đổi thứ hai, quay về ba đỏ: từ ba thì ba phần tám; từ hai thì cần xanh ra đỏ vào, hai phần tư nhân hai phần tư bằng một phần tư; '
                        'từ bốn thì chắc chắn.'),
    Beat('s3', 'solve', 'Tổng: ba phần tám nhân ba phần tám, cộng chín phần mười sáu nhân một phần tư, cộng một phần mười sáu, bằng mười một phần ba mươi hai.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần ba mươi hai. Gom trạng thái theo số bi đỏ, cây hai lần đổi chỉ còn ba nhánh!'),
    Beat('outro', 'outro', outro_text(224)),
]

FORMULAS = formulas('11/32', OPTIONS,
                    first='3 arrow.r 3: 3/8, quad 3 arrow.r 2: 9/16, quad 3 arrow.r 4: 1/16',
                    tot='P = 3/8 dot 3/8 + 9/16 dot 1/4 + 1/16 dot 1 = 11/32')


def validate() -> bool:
    assert step(3) == {3: F(3, 8), 2: F(9, 16), 4: F(1, 16)} and two_steps() == F(11, 32)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS224(TreeMixin, ShortScene):
    N = 224

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.85), dy=1.7, width=6.8, root_label='số đỏ ở I: 3')
        self.wait_until(.8, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.write_board(self.M('first', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.play(*[n.animate.scale(1.25).set_stroke(GREEN, 4) for n, _ in self.leaves], run_time=self.rt(.05))

    def beat_s3(self, T):
        m = self.M('tot', 1.6)
        self.write_board(m)
        self.frame(m)

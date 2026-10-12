"""XSS223 · Đổi bi giữa hai hộp — I (3Đ1X) ↔ II (1Đ3X): sau 1 lần đổi, P(rút đỏ từ I) = 5/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE  # noqa: E402
from xss._urnkit import urn_row  # noqa: E402

EPISODE = {'code': 'XSS223', 'answer': '5/8'}
PROBLEM = ['Hộp I: $3$ đỏ $1$ xanh; II: $1$ đỏ $3$ xanh.',
           'Đổi ngẫu nhiên $1$ bi của I lấy $1$ bi của',
           'II, rồi rút từ I. Xác suất đỏ?']
OPTIONS = ['3/4', '5/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 5 / 8
BRANCHES = [('ĐĐ', GOLD, '3/16', [('Đ', CORAL, '3/4', [])]),
            ('ĐX', CYAN, '9/16', [('Đ', CORAL, '2/4', [])]),
            ('XĐ', GREEN, '1/16', [('Đ', CORAL, '4/4', [])]),
            ('XX', PURPLE, '3/16', [('Đ', CORAL, '3/4', [])])]


def after_swap():
    total = F(0)
    for i, a in enumerate('RRRB'):
        for j, b in enumerate('RBBB'):
            box = 'RRRB'[:i] + 'RRRB'[i + 1:] + b
            total += F(1, 16) * F(box.count('R'), 4)
    return total


BEATS = [
    Beat('hook', 'hook', 'Hộp một có ba đỏ một xanh, hộp hai có một đỏ ba xanh. Lấy ngẫu nhiên một bi mỗi hộp rồi đổi chỗ cho nhau. '
                         'Sau đó rút một bi từ hộp một. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tư, năm phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đổi bi là hai hành động cùng lúc: bi đi ra từ hộp một và bi đi vào từ hộp hai. '
                        'Có bốn kiểu đổi, mỗi kiểu là tích hai xác suất.'),
    Beat('s2', 'solve', 'Đỏ đổi đỏ hoặc xanh đổi xanh: hộp một như cũ, đỏ ba phần tư. Đỏ ra xanh vào, chín phần mười sáu, hộp còn hai đỏ. '
                        'Xanh ra đỏ vào, một phần mười sáu, hộp toàn đỏ.'),
    Beat('s3', 'solve', 'Toàn phần: ba phần mười sáu nhân ba phần tư, cộng chín phần mười sáu nhân hai phần tư, '
                        'cộng một phần mười sáu nhân một, cộng ba phần mười sáu nhân ba phần tư, bằng năm phần tám.'),
    Beat('answer', 'solve', 'Đáp án: năm phần tám. Đổi bi giữa hai hộp kéo thành phần của chúng lại gần nhau!'),
    Beat('outro', 'outro', outro_text(223)),
]

FORMULAS = formulas('5/8', OPTIONS,
                    tot='P = 9/64 + 18/64 + 4/64 + 9/64 = 40/64 = 5/8')


def validate() -> bool:
    assert after_swap() == F(5, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS223(TreeMixin, ShortScene):
    N = 223

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.urns = urn_row([('RRRB', 'hộp I', GOLD), ('RBBB', 'hộp II', PURPLE)], y=1.5, buff=1.4)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        a, b = self.urns[0][0].balls[3], self.urns[1][0].balls[0]
        pa, pb = a.get_center(), b.get_center()
        self.wait_until(.4, t0)
        self.play(a.animate.move_to(pb), b.animate.move_to(pa), run_time=self.rt(.15))

    def beat_s2(self, T):
        self.play(self.urns.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=7.2, root_label='đổi bi', r=.42,
                                                  edge_size=26)
        self.play(*[FadeIn(lv, lag_ratio=.2) for lv in self.levels], run_time=self.rt(.25))

    def beat_s3(self, T):
        m = self.M('tot', 1.8)
        self.write_board(m)
        self.frame(m)

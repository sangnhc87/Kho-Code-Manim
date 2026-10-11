"""XSS174 · Chuyền bi qua ba hộp — mỗi lần chuyền giữ nguyên xác suất đỏ 1/2: kết quả 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS174', 'answer': '1/2'}
PROBLEM = ['Ba hộp đều có $1$ đỏ $1$ xanh. Chuyển $1$ bi',
           'từ I sang II, rồi $1$ bi từ II sang III,',
           'rồi rút từ III. Xác suất đỏ?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5
D, X = ('Đ', CORAL), ('X', CYAN)
BRANCHES = [(*D, '1/2', [(*D, '2/3', []), (*X, '1/3', [])]),
            (*X, '1/2', [(*D, '1/3', []), (*X, '2/3', [])])]


def chain(boxes=3):
    red = F(1, 2)
    for _ in range(boxes - 1):
        red = red * F(2, 3) + (1 - red) * F(1, 3)
    return red


BEATS = [
    Beat('hook', 'hook', 'Ba hộp, mỗi hộp một bi đỏ một bi xanh. Chuyển một bi ngẫu nhiên từ hộp một sang hộp hai, '
                         'rồi một bi từ hộp hai sang hộp ba, rồi rút một bi từ hộp ba. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bước đầu: bi chuyển sang hộp hai là đỏ với xác suất một phần hai. Nếu đỏ, hộp hai thành hai đỏ một xanh; '
                        'nếu xanh, thành một đỏ hai xanh.'),
    Beat('s2', 'solve', 'Bi chuyển từ hộp hai sang hộp ba là đỏ với xác suất một phần hai nhân hai phần ba, cộng một phần hai nhân một phần ba, '
                        'vẫn đúng bằng một phần hai!'),
    Beat('s3', 'solve', 'Mỗi lần chuyền, xác suất bi được chuyển là đỏ vẫn giữ một phần hai. Vì vậy rút từ hộp ba cũng được một phần hai, '
                        'dù có chuyền qua mười hộp.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Nhận ra một đại lượng không đổi qua từng bước là chìa khóa của bài chuyển bi nhiều tầng!'),
    Beat('outro', 'outro', outro_text(174)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    step='P("chuyển đỏ") = 1/2 dot 2/3 + 1/2 dot 1/3 = 1/2',
                    inv='1/2 arrow.r 1/2 arrow.r 1/2')


def validate() -> bool:
    assert chain(2) == chain(3) == chain(10) == F(1, 2)
    final = chain(3) * F(2, 3) + (1 - chain(3)) * F(1, 3)
    assert final == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS174(TreeMixin, ShortScene):
    N = 174

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.urns = VGroup(*[urn('RB', 2, .26) for _ in range(3)]).arrange(buff=.35).move_to([0, 1.8, 0])
        self.labs = VGroup(*[tx(n, 24, SOFT).next_to(u, [0, -1, 0]) for n, u in zip(('I', 'II', 'III'), self.urns)])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), FadeIn(self.labs), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), self.labs.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns, self.labs)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='I → II')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('tầng 2: bi chuyển II → III', 22, SOFT).move_to([0, -1.0, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        reds = [n for n, path in self.leaves if path[-1][0] == 'Đ']
        self.play(*[n.animate.scale(1.3) for n in reds], run_time=self.rt(.05))
        self.wait_until(.35, t0)
        m = self.M('step', 1.7)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        self.write_board(self.M('inv', 2.0), anim='fade')

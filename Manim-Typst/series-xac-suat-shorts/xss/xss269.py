"""XSS269 · Người dẫn không biết (Monty Fall) — mở ngẫu nhiên, tình cờ ra dê: P(đổi thắng) = (1/3)/(2/3) = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS269', 'answer': '1/2'}
PROBLEM = ['Monty Hall nhưng người dẫn KHÔNG',
           'biết xe ở đâu, mở ngẫu nhiên $1$ trong',
           '$2$ cửa còn lại và tình cờ ra dê.',
           'Đổi cửa: $P("trúng xe")$?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5
BRANCHES = [('xe', GREEN, '1/3', [('dê', GOLD, '1', [])]),
            ('dê', CORAL, '2/3', [('dê', GOLD, '1/2', []), ('xe', SOFT, '1/2', [])])]


def fall():
    num = den = F(0)
    for car in range(3):
        for opened in (1, 2):
            pr = F(1, 3) * F(1, 2)
            if opened != car:
                den += pr
                num += pr * (car != 0)
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Bài Monty Hall quen thuộc, đổi cửa thắng hai phần ba. Nhưng lần này người dẫn không biết xe ở đâu: '
                         'anh ấy mở ngẫu nhiên một trong hai cửa còn lại, và tình cờ ra dê. Đổi cửa thì xác suất trúng xe là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một: cửa bạn chọn có xe một phần ba, có dê hai phần ba. Tầng hai: người dẫn mở ngẫu nhiên. '
                        'Nếu cửa bạn có xe, anh ấy chắc chắn mở ra dê. Nếu cửa bạn có dê, chỉ một nửa khả năng anh ấy mở ra dê.'),
    Beat('s2', 'solve', 'Điều kiện "mở ra dê": hai lá, một phần ba nhân một, và hai phần ba nhân một phần hai, cũng bằng một phần ba. Hai lá bằng nhau!'),
    Beat('s3', 'solve', 'Đổi cửa thắng khi cửa bạn có dê: một phần ba chia hai phần ba, bằng một phần hai. '
                        'Sự may mắn của người dẫn đã xóa đi lợi thế của việc đổi cửa.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Cùng một quan sát, nhưng cách thông tin được tạo ra quyết định xác suất có điều kiện!'),
    Beat('outro', 'outro', outro_text(269)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    leaves='1/3 dot 1 = 1/3, quad 2/3 dot 1/2 = 1/3',
                    prob='P("đổi thắng" | "mở ra dê") = (1/3)/(2/3) = 1/2')


def validate() -> bool:
    assert fall() == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS269(TreeMixin, ShortScene):
    N = 269

    def hook_visual(self, t0):
        self.board_top = -1.55
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=6.4, root_label='cửa bạn chọn', r=.46)
        self.wait_until(.8, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.03))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.12))
        self.play(FadeIn(tx('tầng 2: cửa người dẫn mở', 22, SOFT).move_to([0, -1.25, 0])), run_time=self.rt(.03))

    def beat_s2(self, T):
        t0 = self.now()
        goats = [self.leaves[0][0], self.leaves[1][0]]
        self.play(*[n.animate.scale(1.3) for n in goats], self.leaves[2][0].animate.set_opacity(.15), run_time=self.rt(.05))
        self.wait_until(.35, t0)
        self.write_board(self.M('leaves', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

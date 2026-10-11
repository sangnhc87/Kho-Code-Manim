"""XSS139 · Tennis: điểm deuce — cây có vòng lặp: P = 0,36 + 0,48·P ⇒ P = 9/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS139', 'answer': '9/13'}
PROBLEM = ['Đang deuce, A thắng mỗi điểm $"0,6"$;',
           'ai hơn đối thủ $2$ điểm thì thắng game.',
           'Xác suất A thắng game?']
OPTIONS = ['"0,6"', '9/13', '"0,36"']
CORRECT = 1
ANSWER_VALUE = 9 / 13
A, B = ('A', CYAN), ('B', CORAL)
BRANCHES = [(*A, '"0,6"', [(*A, '"0,6"', []), (*B, '"0,4"', [])]),
            (*B, '"0,4"', [(*A, '"0,6"', []), (*B, '"0,4"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Quần vợt, tỉ số đang deuce: ai thắng liền hai điểm hơn đối thủ thì thắng game. '
                         'A thắng mỗi điểm với xác suất không phẩy sáu. Xác suất A thắng game là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy sáu, chín phần mười ba, hay không phẩy ba sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xét hai điểm tiếp theo. A A: A thắng game, xác suất không phẩy ba sáu. B B: A thua, không phẩy một sáu. '
                        'A B hoặc B A: quay lại deuce, xác suất không phẩy bốn tám.'),
    Beat('s2', 'solve', 'Cây tự lặp lại chính nó. Gọi P là xác suất A thắng từ deuce: P bằng không phẩy ba sáu cộng không phẩy bốn tám nhân P.'),
    Beat('s3', 'solve', 'Giải ra P bằng không phẩy ba sáu chia không phẩy năm hai, tức chín phần mười ba, khoảng sáu mươi chín phần trăm. '
                        'Luật deuce khuếch đại lợi thế của người giỏi hơn.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười ba. Gặp cây quay về trạng thái cũ, hãy đặt ẩn và lập phương trình!'),
    Beat('outro', 'outro', outro_text(139)),
]

FORMULAS = formulas('9/13', OPTIONS,
                    eq='P = "0,36" + "0,48" dot P',
                    sol='P = ("0,36")/("0,52") = 9/13')


def validate() -> bool:
    p = F(9, 25) / (1 - F(12, 25))
    s = sum(F(12, 25) ** k * F(9, 25) for k in range(300))
    assert p == F(9, 13) and abs(float(s) - 9 / 13) < 1e-12
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS139(TreeMixin, ShortScene):
    N = 139

    def hook_visual(self, t0):
        self.board_top = -1.75
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='deuce')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(self.leaves[0][0].animate.scale(1.35).set_stroke(GREEN, 5), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        back = [self.leaves[1][0], self.leaves[2][0]]
        self.play(*[n.animate.set_stroke(GOLD, 5) for n in back], run_time=self.rt(.05))
        self.play(FadeIn(tx('vàng: về lại deuce', 24, GOLD).move_to([0, -1.3, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        m = self.M('eq', 2.2)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('sol', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.TM('$"0,6"$ mỗi điểm → gần $"0,69"$ mỗi game', 24, SOFT), anim='fade')

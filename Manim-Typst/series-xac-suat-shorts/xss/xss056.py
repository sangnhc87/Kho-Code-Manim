"""XSS056 · Hoàn lại hay không? — 3 đỏ 2 xanh, rút 2: có hoàn lại 9/25, không hoàn lại 3/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path

from manim import DOWN, FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS056', 'answer': '9/25 và 3/10'}
PROBLEM = ['Hộp $3$ bi đỏ, $2$ bi xanh. Rút lần lượt $2$ bi. $P("2 đỏ")$', 'khi CÓ hoàn lại và khi KHÔNG hoàn lại?']
OPTIONS = ['9/25 " và " 3/10', '3/10 " và " 9/25', '9/25 " và " 9/25']
CORRECT = 0
ANSWER_VALUE = None
BALLS = 'RRRBB'

BEATS = [
    Beat('hook', 'hook', 'Hộp có ba bi đỏ, hai bi xanh. Rút lần lượt hai viên. Xác suất được hai viên đỏ là bao nhiêu, '
                         'nếu rút xong bỏ lại vào hộp, và nếu rút xong giữ luôn ở ngoài?'),
    Beat('guess', 'hook', 'Chín phần hai lăm và ba phần mười, ngược lại, hay hai trường hợp bằng nhau? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có hoàn lại: hộp trở về như cũ sau mỗi lần rút. Lần nào cũng ba phần năm cơ hội ra đỏ, '
                        'nên xác suất là ba phần năm nhân ba phần năm, bằng chín phần hai lăm.'),
    Beat('s2', 'solve', 'Không hoàn lại: lần đầu ba phần năm. Đã lấy mất một viên đỏ, hộp còn hai đỏ trong bốn viên, '
                        'lần sau chỉ còn hai phần tư. Nhân lại được ba phần mười.'),
    Beat('s3', 'solve', 'Không hoàn lại cho xác suất nhỏ hơn, vì viên đỏ đầu tiên đã bị lấy đi. '
                        'Đọc kỹ đề: có hoàn lại hay không hoàn lại làm thay đổi đáp án!'),
    Beat('answer', 'solve', 'Đáp án: chín phần hai lăm khi có hoàn lại, ba phần mười khi không hoàn lại.'),
    Beat('outro', 'outro', outro_text(56)),
]

FORMULAS = formulas('9/25 " và " 3/10', OPTIONS,
                    back='3/5 dot 3/5 = 9/25',
                    keep='3/5 dot 2/4 = 3/10',
                    cmp='3/10 < 9/25')


def validate() -> bool:
    labelled = list(range(5))
    red = lambda i: BALLS[i] == 'R'  # noqa: E731
    assert F(sum(red(a) and red(b) for a, b in product(labelled, repeat=2)), 25) == F(9, 25)
    assert F(sum(red(a) and red(b) for a, b in permutations(labelled, 2)), 20) == F(3, 10)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS056(ShortScene):
    N = 56

    def hook_visual(self, t0):
        self.u = urn(BALLS, cols=5, r=.4).move_to([0, 1.5, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.u[0]), FadeIn(self.u.balls, lag_ratio=.15), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(tx('CÓ hoàn lại', 30, CYAN, bold=True).next_to(self.u, DOWN, buff=.3)), run_time=self.rt(.05))
        b = self.u.balls[0]
        self.play(b.animate.shift([0, 1.5, 0]), run_time=self.rt(.08))
        self.play(b.animate.shift([0, -1.5, 0]), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        m = self.M('back', 2.2)
        self.write_board(m)
        self.frame(m, CYAN)

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_stage(.03)
        self.u = urn(BALLS, cols=5, r=.4).move_to([0, 1.5, 0])
        self.add(self.u)
        self.play(FadeIn(tx('KHÔNG hoàn lại', 30, CORAL, bold=True).next_to(self.u, DOWN, buff=.3)), run_time=self.rt(.05))
        self.play(self.u.balls[0].animate.shift([2.6, 1.0, 0]).set_opacity(.6), run_time=self.rt(.1))
        self.wait_until(.55, t0)
        m = self.M('keep', 2.2)
        self.write_board(m)
        self.frame(m, CORAL)

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('cmp', 1.9), anim='fade')
        self.wait_until(.5, t0)
        self.write_board(tx('đọc kỹ: có hoàn lại hay không?', 28, GOLD, bold=True), anim='fade')



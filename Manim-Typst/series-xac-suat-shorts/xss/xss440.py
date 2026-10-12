"""XSS440 · Monty Hall bốn cửa — cửa chọn đầu đúng 1/4; người dẫn (biết xe) mở 2 cửa dê; đổi sang cửa còn lại thắng ⇔ chọn đầu sai: 3/4."""
from __future__ import annotations

import random
import sys
from pathlib import Path

from manim import FadeIn, RoundedRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.kit import tx  # noqa: E402
from common.theme import CYAN, GOLD, GREEN, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS440', 'answer': '3/4'}
PROBLEM = ['$4$ cửa, $1$ cửa có xe. Bạn chọn $1$ cửa,',
           'người dẫn (biết xe) mở $2$ cửa có dê.',
           'Đổi sang cửa còn lại: $P("trúng xe")$?']
OPTIONS = ['3/4', '1/2', '1/4']
CORRECT = 0
ANSWER_VALUE = .75


def simulate(runs=20000, seed=440):
    rnd, win = random.Random(seed), 0
    for _ in range(runs):
        car, pick = rnd.randrange(4), rnd.randrange(4)
        goats = [d for d in range(4) if d not in (car, pick)]
        opened = rnd.sample(goats, 2) if len(goats) == 3 else goats
        other = next(d for d in range(4) if d != pick and d not in opened)
        win += other == car
    return win / runs


BEATS = [
    Beat('hook', 'hook', 'Thử thách cuối cùng! Monty Hall phiên bản bốn cửa: một cửa có xe. Bạn chọn một cửa. Người dẫn, biết xe ở đâu, mở hai trong ba cửa còn lại đều có dê. '
                         'Bạn đổi sang cửa đóng còn lại. Xác suất trúng xe?'),
    Beat('guess', 'hook', 'Ba phần tư, một phần hai, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cửa bạn chọn đầu tiên có xe với xác suất một phần tư. Người dẫn luôn mở được hai cửa dê, nên hành động ấy không làm thay đổi một phần tư đó.'),
    Beat('s2', 'solve', 'Nếu lựa chọn đầu sai, xác suất ba phần tư, xe nằm trong ba cửa kia; người dẫn loại hai cửa dê, cửa còn lại chính là xe.'),
    Beat('s3', 'solve', 'Đổi cửa thắng đúng khi lựa chọn đầu sai: ba phần tư. Mô phỏng hai mươi nghìn lần cũng cho khoảng không phẩy bảy lăm.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tư. Cảm ơn bạn đã đi hết bốn trăm bốn mươi thử thách xác suất! Thông tin là thứ thay đổi xác suất.'),
    Beat('outro', 'outro', outro_text(440)),
]

FORMULAS = formulas('3/4', OPTIONS,
                    first='P("chọn đầu đúng") = 1/4',
                    prob='P("đổi thắng") = 1 - 1/4 = 3/4')


def validate() -> bool:
    assert abs(simulate() - .75) < .01
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS440(ShortScene):
    N = 440

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.doors = VGroup(*[VGroup(RoundedRectangle(width=1.2, height=1.9, corner_radius=.12, stroke_color=SOFT, stroke_width=4,
                                                      fill_color=PANEL, fill_opacity=1),
                                     tx(str(i + 1), 34, SOFT, bold=True)) for i in range(4)]).arrange(buff=.4).move_to([0, 1.2, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.doors, lag_ratio=.15), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.doors[0][0].animate.set_stroke(CYAN, 7), run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.play(*[self.doors[i][0].animate.set_fill(SOFT, .35) for i in (1, 3)],
                  *[self.doors[i][1].animate.become(tx('dê', 30, PANEL, bold=True).move_to(self.doors[i][0])) for i in (1, 3)],
                  run_time=self.rt(.08))
        self.write_board(self.M('first', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.doors[2][0].animate.set_stroke(GOLD, 7), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.play(self.doors[2][0].animate.set_fill(GREEN, .6), run_time=self.rt(.05))
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

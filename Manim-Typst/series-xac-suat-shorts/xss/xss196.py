"""XSS196 · Chọn người giỏi nhất — 3 ứng viên, bỏ qua người đầu: thắng ở 3 trong 6 thứ tự: 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS196', 'answer': '1/2'}
PROBLEM = ['$3$ ứng viên đến lần lượt. Bỏ qua người',
           'đầu, chọn ngay người giỏi hơn người đầu.',
           'Xác suất chọn được người giỏi nhất?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5
ORDERS = list(permutations((1, 2, 3)))  # 3 = giỏi nhất


def pick(order):
    best = order[0]
    return next((x for x in order[1:] if x > best), order[-1])


BEATS = [
    Beat('hook', 'hook', 'Bài toán chọn thư ký: ba ứng viên đến phỏng vấn theo thứ tự ngẫu nhiên. Phỏng vấn xong phải quyết định ngay, '
                         'không gọi lại được. Nếu chọn ngẫu nhiên thì chỉ một phần ba cơ hội có người giỏi nhất. Có chiến thuật tốt hơn không?'),
    Beat('guess', 'hook', 'Chiến thuật "bỏ qua người đầu" cho xác suất một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chiến thuật: chỉ quan sát người đầu tiên để lấy mốc, rồi chọn ngay người đầu tiên giỏi hơn mốc đó. '
                        'Nếu không ai giỏi hơn thì đành lấy người cuối.'),
    Beat('s2', 'solve', 'Liệt kê sáu thứ tự. Thắng khi: hai, ba, một; hai, một, ba; và một, ba, hai. Thua khi người giỏi nhất đến đầu tiên, '
                        'hoặc gặp thứ tự một, hai, ba.'),
    Beat('s3', 'solve', 'Ba trên sáu thứ tự thắng: xác suất một phần hai, tốt hơn hẳn một phần ba. '
                        'Với rất nhiều ứng viên, bỏ qua khoảng ba mươi bảy phần trăm đầu là tối ưu.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Thu thập thông tin trước rồi mới quyết định, ngay cả khi không được quay lại!'),
    Beat('outro', 'outro', outro_text(196)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    win='(2, 3, 1), quad (2, 1, 3), quad (1, 3, 2)',
                    prob='P = 3/6 = 1/2 > 1/3')


def validate() -> bool:
    assert F(sum(pick(o) == 3 for o in ORDERS), 6) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS196(ShortScene):
    N = 196

    def hook_visual(self, t0):
        self.board_top = -1.3
        col = {1: SOFT, 2: CYAN, 3: GOLD}
        self.rows = VGroup(*[VGroup(*[token(str(x), col[x], .26) for x in o]).arrange(buff=.1) for o in ORDERS]) \
            .arrange_in_grid(3, 2, buff=(1.2, .35)).move_to([0, 1.5, 0])
        self.wait_until(.75, t0)
        self.play(FadeIn(self.rows[0]), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.rows[0][0].animate.set_opacity(.35), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.rows[1:], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        for r, o in zip(self.rows, ORDERS):
            win = pick(o) == 3
            self.play(r.animate.set_opacity(1 if win else .2), *([r[o.index(3)][0].animate.set_stroke(GREEN, 5)] if win else []),
                      run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.write_board(self.M('win', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)



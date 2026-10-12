"""XSS344 · Bi cuối cùng bất biến — 5 đỏ 4 xanh; mỗi bước số bi xanh giữ nguyên hoặc giảm 2 → luôn chẵn → bi cuối không thể xanh: đỏ chắc chắn."""
from __future__ import annotations

import random
import sys
from pathlib import Path

from manim import DOWN, FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import SOFT  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS344', 'answer': 'Đỏ (chắc chắn)'}
PROBLEM = ['Hộp $5$ đỏ, $4$ xanh. Mỗi lần lấy $2$ bi: cùng',
           'màu thì bỏ vào $1$ đỏ, khác màu thì bỏ vào',
           '$1$ xanh. Bi cuối cùng màu gì?']
OPTIONS = ['"Xanh (chắc chắn)"', '"Đỏ (chắc chắn)"', '"Tùy may rủi"']
CORRECT = 1
ANSWER_VALUE = 1


def play_out(r, b, rnd):
    while r + b > 1:
        bag = ['R'] * r + ['B'] * b
        x, y = rnd.sample(bag, 2)
        if x == y:
            r, b = (r - 1, b) if x == 'R' else (r + 1, b - 2)
        else:
            r, b = r - 1, b
    return 'R' if r else 'B'


BEATS = [
    Beat('hook', 'hook', 'Hộp có năm bi đỏ, bốn bi xanh. Mỗi lần lấy ra hai bi: cùng màu thì bỏ vào một bi đỏ, khác màu thì bỏ vào một bi xanh. '
                         'Cứ thế đến khi còn một bi. Bi cuối cùng màu gì?'),
    Beat('guess', 'hook', 'Chắc chắn xanh, chắc chắn đỏ, hay tùy may rủi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Theo dõi số bi xanh. Hai đỏ: xanh giữ nguyên. Hai xanh: mất hai xanh, thêm một đỏ. Một đỏ một xanh: mất một đỏ, xanh giữ nguyên.'),
    Beat('s2', 'solve', 'Vậy số bi xanh hoặc giữ nguyên, hoặc giảm hai. Tính chẵn lẻ của nó không bao giờ đổi: bắt đầu bằng bốn, luôn là số chẵn.'),
    Beat('s3', 'solve', 'Nếu bi cuối là xanh thì số bi xanh bằng một, số lẻ: vô lý. Nên bi cuối chắc chắn là đỏ, dù rút thế nào.'),
    Beat('s4', 'solve', 'Mô phỏng một nghìn lần chơi, lần nào bi cuối cũng đỏ. Xác suất bằng một.'),
    Beat('answer', 'solve', 'Đáp án: đỏ, chắc chắn. Khi quá trình rối rắm, hãy tìm đại lượng bất biến.'),
    Beat('outro', 'outro', outro_text(344)),
]

FORMULAS = formulas('"Đỏ (chắc chắn)"', OPTIONS,
                    moves='Delta x in {0; -2}',
                    par='x equiv 0 quad ("mod" 2)',
                    sim='P("đỏ") = 1')


def validate() -> bool:
    rnd = random.Random(344)
    assert all(play_out(5, 4, rnd) == 'R' for _ in range(1000))
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS344(ShortScene):
    N = 344

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.u = urn('RRRRRBBBB', cols=5, r=.3).move_to([0, 1.9, 0])
        self.play(FadeIn(self.u), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        rules = VGroup(*[self.TM(s, 30, SOFT) for s in ('đỏ $+$ đỏ $arrow.r$ xanh giữ nguyên',
                                                       'xanh $+$ xanh $arrow.r$ xanh $-2$',
                                                       'đỏ $+$ xanh $arrow.r$ xanh giữ nguyên')]).arrange(DOWN, buff=.2).move_to([0, .25, 0])
        for i, f in enumerate((.15, .45, .75)):
            self.wait_until(f, t0)
            self.play(FadeIn(rules[i]), run_time=self.rt(.05))
        self.rules = rules

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('moves', 1.5))
        self.wait_until(.5, t0)
        m = self.M('par', 1.5)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeOut(self.rules), run_time=self.rt(.04))
        self.play(FadeIn(self.TM('xanh cuối $= 1$: số lẻ, vô lý', 32, SOFT).move_to([0, .25, 0])), run_time=self.rt(.05))

    def beat_s4(self, T):
        self.clear_board(.03)
        self.write_board(self.M('sim', 1.6))

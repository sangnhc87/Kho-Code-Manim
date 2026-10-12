"""XSS286 · Lá sen bị hỏng — 1 hoặc 2 lá (1/2), lá 3 hỏng: p = 1, 1/2, 3/4, 0, 3/8, 3/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS286', 'answer': '3/16'}
PROBLEM = ['Ếch ở lá $0$, mỗi lần nhảy $1$ hoặc $2$ lá',
           '(mỗi kiểu $1/2$); lá $3$ bị hỏng, đáp vào là',
           'rơi xuống nước. Xác suất ếch đáp lá $5$?']
OPTIONS = ['5/16', '3/16', '1/4']
CORRECT = 1
ANSWER_VALUE = 3 / 16


def land(n, bad=(3,)):
    p = {0: F(1)}
    for k in range(1, n + 1):
        p[k] = 0 if k in bad else (p.get(k - 1, 0) + p.get(k - 2, 0)) / 2
    return p


BEATS = [
    Beat('hook', 'hook', 'Ếch qua sông trên hàng lá sen, mỗi lần nhảy một hoặc hai lá, năm mươi năm mươi. Nhưng lá số ba đã hỏng, đáp vào là rơi xuống nước. '
                         'Xác suất ếch đáp được lá số năm là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần mười sáu, ba phần mười sáu, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Quy hoạch động như cầu thang: p k bằng nửa p k trừ một cộng nửa p k trừ hai. p một một phần hai, p hai ba phần tư.'),
    Beat('s2', 'solve', 'Lá hỏng: ép p ba bằng không, vì ếch đáp vào là dừng cuộc chơi. Lá bốn chỉ có thể tới từ lá hai: ba phần tư chia hai, ba phần tám.'),
    Beat('s3', 'solve', 'Lá năm: nửa p bốn cộng nửa p ba, bằng ba phần mười sáu cộng không, tức ba phần mười sáu. Không có lá hỏng thì sẽ là mười một phần ba mươi hai.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười sáu. Chướng ngại trong quy hoạch động: chỉ cần đặt giá trị ô đó bằng không!'),
    Beat('outro', 'outro', outro_text(286)),
]

FORMULAS = formulas('3/16', OPTIONS,
                    rec='p_k = 1/2 p_(k-1) + 1/2 p_(k-2), quad p_3 = 0',
                    vals='1, quad 1/2, quad 3/4, quad 0, quad 3/8, quad 3/16')


def validate() -> bool:
    brute = F(0)
    for n in range(1, 6):
        for w in product((1, 2), repeat=n):
            pos = [sum(w[:i]) for i in range(1, n + 1)]
            if pos[-1] == 5 and 3 not in pos and all(x < 5 for x in pos[:-1]):
                brute += F(1, 2 ** n)
    assert land(5)[5] == brute == F(3, 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS286(ShortScene):
    N = 286

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = pads(range(6), y=1.7, gap=1.1, r=.4, bad=(3,))
        self.labs = VGroup(*[self.TM(f'${k}$', 24, CORAL if k == 3 else (GOLD if k == 5 else SOFT)).next_to(p, [0, -1, 0], buff=.12)
                             for k, p in enumerate(self.row)])
        self.fr = frog().move_to(self.row[0])
        self.wait_until(.7, t0)
        self.play(FadeIn(self.row, lag_ratio=.1), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('rec', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        for k in (2, 4):
            self.play(self.fr.animate.move_to(self.row[k]), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(self.row[3].animate.set_fill(CORAL, .6), run_time=self.rt(.04))

    def beat_s3(self, T):
        self.clear_board(.03)
        self.play(self.fr.animate.move_to(self.row[5]), run_time=self.rt(.05))
        m = self.M('vals', 1.7)
        self.write_board(m)
        self.frame(m)

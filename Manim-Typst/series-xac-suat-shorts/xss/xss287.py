"""XSS287 · Biết ếch tới lá 4 — P(đáp 2 và 4) = p₂·p₂ = 9/16; P(đáp 4) = 11/16: 9/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS287', 'answer': '9/11'}
PROBLEM = ['Ếch ở lá $0$, mỗi lần nhảy $1$ hoặc $2$ lá',
           '(mỗi kiểu $1/2$). Biết ếch có đáp lá $4$.',
           'Xác suất ếch từng đáp lá $2$?']
OPTIONS = ['3/4', '9/11', '1/2']
CORRECT = 1
ANSWER_VALUE = 9 / 11


def p(n):
    v = [F(1), F(1, 2)]
    while len(v) <= n:
        v.append((v[-1] + v[-2]) / 2)
    return v[n]


def brute():
    num = den = F(0)
    for w in product((1, 2), repeat=4):
        pos = [sum(w[:i]) for i in range(1, 5)]
        pr = F(1, 16)
        if 4 in pos:
            den += pr
            num += pr * (2 in pos)
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Ếch nhảy một hoặc hai lá, năm mươi năm mươi. Bạn biết ếch đã có lúc đáp lá số bốn. '
                         'Xác suất ếch cũng từng đáp lá số hai là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tư, chín phần mười một, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xác suất chạm từng lá: p hai bằng ba phần tư, p bốn bằng mười một phần mười sáu, theo quy hoạch động của bài cầu thang.'),
    Beat('s2', 'solve', 'Đáp cả lá hai và lá bốn: đến lá hai với xác suất ba phần tư, rồi từ lá hai "làm lại" và đến lá bốn, cũng ba phần tư. '
                        'Tích là chín phần mười sáu, nhờ tính không nhớ.'),
    Beat('s3', 'solve', 'Xác suất có điều kiện: chín phần mười sáu chia mười một phần mười sáu, bằng chín phần mười một. Biết đã tới lá bốn thì khả năng từng đứng ở lá hai rất cao.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười một. Ghép quy hoạch động với tính không nhớ để tính xác suất đi qua hai điểm!'),
    Beat('outro', 'outro', outro_text(287)),
]

FORMULAS = formulas('9/11', OPTIONS,
                    both='P(2 " và " 4) = p_2 dot p_2 = 3/4 dot 3/4 = 9/16',
                    prob='P(2 | 4) = (9/16)/(11/16) = 9/11')


def validate() -> bool:
    assert p(2) == F(3, 4) and p(4) == F(11, 16) and brute() == F(9, 11) == p(2) ** 2 / p(4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS287(ShortScene):
    N = 287

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = pads(range(5), y=1.7)
        self.labs = VGroup(*[self.TM(f'${k}$', 26, GOLD if k in (2, 4) else SOFT).next_to(q, [0, -1, 0], buff=.15)
                             for k, q in enumerate(self.row)])
        self.fr = frog().move_to(self.row[0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.row), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.TM('$p_2 = 3/4$ và $p_4 = 11/16$', 30, CYAN))

    def beat_s2(self, T):
        t0 = self.now()
        for k in (2, 4):
            self.play(self.fr.animate.move_to(self.row[k]), run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.clear_board(.03)
        self.write_board(self.M('both', 1.7))

    def beat_s3(self, T):
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

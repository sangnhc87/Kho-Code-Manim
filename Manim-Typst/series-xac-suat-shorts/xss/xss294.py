"""XSS294 · Mấy bước thì lên bờ? — E2 = 1 + E3/2, E3 = 1 + E2/2 ⇒ E2 = 2 = (2 − 1)(4 − 2)."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, GREEN, SOFT  # noqa: E402
from xss._frogkit import frog, pads  # noqa: E402

EPISODE = {'code': 'XSS294', 'answer': '2'}
PROBLEM = ['Như trên: lá $1$ và $4$ là bờ, ếch ở lá $2$,',
           'mỗi bước $plus.minus 1$ ($1/2$). Trung bình',
           'mấy bước thì ếch lên được bờ?']
OPTIONS = ['3/2', '2', '3']
CORRECT = 1
ANSWER_VALUE = None
N, SEED = 3000, 6


def sim():
    r, tot = random.Random(SEED), 0
    for _ in range(N):
        x, n = 2, 0
        while x not in (1, 4):
            x += 1 if r.random() < .5 else -1
            n += 1
        tot += n
    return tot / N


BEATS = [
    Beat('hook', 'hook', 'Vẫn ếch ở lá hai, hai bờ là lá một và lá bốn. Lần này không hỏi bờ nào, mà hỏi: trung bình bao nhiêu bước thì ếch lên được bờ?'),
    Beat('guess', 'hook', 'Một phẩy năm, hai, hay ba bước? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi E hai, E ba là số bước trung bình còn lại. Mỗi bước tốn một. Từ lá hai: nửa lên bờ ngay, nửa sang lá ba.'),
    Beat('s2', 'solve', 'Hệ: E hai bằng một cộng nửa E ba, E ba bằng một cộng nửa E hai. Do đối xứng E hai bằng E ba, nên E bằng một cộng nửa E, E bằng hai.'),
    Beat('s3', 'solve', 'Công thức tổng quát: khoảng cách tới bờ trái nhân khoảng cách tới bờ phải, một nhân hai bằng hai. Mô phỏng ba nghìn chú ếch cũng ra khoảng hai.'),
    Beat('answer', 'solve', 'Đáp án: hai bước. Kỳ vọng thời gian thoát bằng tích hai khoảng cách tới hai bờ!'),
    Beat('outro', 'outro', outro_text(294)),
]

FORMULAS = formulas('2', OPTIONS,
                    sys='E_2 = 1 + 1/2 E_3, quad E_3 = 1 + 1/2 E_2',
                    sol='E_2 = E_3 = 2 = 1 dot 2')


def validate() -> bool:
    e = F(2)
    assert e == 1 + e / 2 and abs(sim() - 2) < .1
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS294(ShortScene):
    N = 294

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = pads(range(1, 5), y=1.7, gap=1.4)
        self.row[0].set_fill(GREEN, .8)
        self.row[-1].set_fill(GREEN, .8)
        self.labs = VGroup(*[self.TM(f'${k}$', 26, SOFT).next_to(q, [0, -1, 0], buff=.15) for k, q in zip(range(1, 5), self.row)])
        self.fr = frog().move_to(self.row[1])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.row), FadeIn(self.labs), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.fr.animate.move_to(self.row[0]), run_time=self.rt(.04))
        self.play(self.fr.animate.move_to(self.row[1]), run_time=self.rt(.04))

    def beat_s2(self, T):
        m = self.M('sys', 1.7)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 2.1)
        self.write_board(m)
        self.frame(m)



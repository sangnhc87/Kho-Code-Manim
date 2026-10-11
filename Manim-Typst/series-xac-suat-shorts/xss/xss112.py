"""XSS112 · Bao lâu ra mặt 6? — kỳ vọng thời gian chờ: E = 1 + (5/6)E ⇒ E = 6."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS112', 'answer': '6'}
PROBLEM = ['Gieo xúc xắc đến khi ra mặt $6$.', 'Trung bình cần bao nhiêu lần gieo?']
OPTIONS = ['"3,5"', '6', '36']
CORRECT = 1
ANSWER_VALUE = None
N, SEED = 1000, 16


def waits():
    r, tot, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        n = 1
        while r.randint(1, 6) != 6:
            n += 1
        tot += n
        out.append(tot / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Gieo một con xúc xắc cho đến khi ra mặt sáu. Có lần ra ngay, có lần phải gieo rất lâu. '
                         'Trung bình bạn cần gieo bao nhiêu lần? Đây là khái niệm kỳ vọng.'),
    Beat('guess', 'hook', 'Ba phẩy năm, sáu, hay ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi E là số lần gieo trung bình. Lần gieo đầu tiên luôn tốn một lần. '
                        'Với xác suất năm phần sáu không ra sáu, ta như bắt đầu lại từ đầu, cần thêm trung bình E lần nữa.'),
    Beat('s2', 'solve', 'Vậy E bằng một cộng năm phần sáu E. Chuyển vế: một phần sáu E bằng một, nên E bằng sáu. '
                        'Tổng quát: chờ một biến cố có xác suất p thì trung bình mất một chia p lần.'),
    Beat('s3', 'solve', 'Mô phỏng một nghìn lượt chơi, đo số lần gieo trung bình: con số bám sát sáu.'),
    Beat('answer', 'solve', 'Đáp án: trung bình sáu lần. Xác suất một phần sáu thì chờ trung bình sáu lần, nghe rất tự nhiên!'),
    Beat('outro', 'outro', outro_text(112)),
]

FORMULAS = formulas('6', OPTIONS,
                    eq='E = 1 + 5/6 E',
                    sol='1/6 E = 1 arrow.r.double E = 6',
                    gen='E = 1/p')


def validate() -> bool:
    e = sum(k * F(5, 6) ** (k - 1) * F(1, 6) for k in range(1, 400))
    assert abs(float(e) - 6) < 1e-9 and abs(waits()[-1] - 6) < .03
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS112(ShortScene):
    N = 112

    def hook_visual(self, t0):
        self.seq = VGroup(*[die(v, .75) for v in (2, 5, 1, 3, 6)]).arrange(buff=.25).move_to([0, 1.6, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.seq, lag_ratio=.3), run_time=self.rt(.25))
        self.play(self.seq[-1][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('eq', 2.3))

    def beat_s2(self, T):
        t0 = self.now()
        m = self.M('sol', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(VGroup(tx('tổng quát:', 26, SOFT), self.M('gen', 1.8)).arrange(buff=.25), anim='fade')

    def beat_s3(self, T):
        self.clear_board(.03)
        self.run_sim(waits(), 'số lượt chơi:', 'trung bình:', .6, y=-1.7, color=GREEN, nd=2)

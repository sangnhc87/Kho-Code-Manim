"""XSS197 · Chờ hai ngửa liên tiếp — trạng thái 0 và 1: E0 = 1 + E1/2 + E0/2, E1 = 1 + E0/2 ⇒ E0 = 6."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN  # noqa: E402
from common.visuals import coin, token  # noqa: E402

EPISODE = {'code': 'XSS197', 'answer': '6'}
PROBLEM = ['Tung đồng xu đến khi có hai lần',
           'ngửa liên tiếp. Trung bình cần',
           'bao nhiêu lần tung?']
OPTIONS = ['4', '6', '8']
CORRECT = 1
ANSWER_VALUE = None
N, SEED = 1000, 3


def waits():
    r, tot, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        n, run = 0, 0
        while run < 2:
            n += 1
            run = run + 1 if r.random() < .5 else 0
        tot += n
        out.append(tot / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu cho đến khi có hai lần ngửa liên tiếp. Trung bình bạn phải tung bao nhiêu lần? '
                         'Xác suất ngửa ngửa là một phần tư, vậy có phải bốn lần?'),
    Beat('guess', 'hook', 'Bốn, sáu, hay tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai trạng thái: chưa có ngửa nào ở cuối, hoặc vừa có một ngửa. Gọi E không và E một là số lần tung trung bình còn lại.'),
    Beat('s2', 'solve', 'Từ trạng thái không: tung một lần, ngửa thì sang trạng thái một, sấp thì ở lại. Từ trạng thái một: ngửa là xong, '
                        'sấp thì về lại trạng thái không, công sức đổ sông đổ biển.'),
    Beat('s3', 'solve', 'Giải hệ: E một bằng một cộng nửa E không, E không bằng một cộng nửa E một cộng nửa E không, ra E không bằng sáu. '
                        'Mô phỏng một nghìn lần cũng bám sát sáu.'),
    Beat('answer', 'solve', 'Đáp án: sáu lần, không phải bốn. Một lần sấp ở giữa làm mất cả lần ngửa trước đó!'),
    Beat('outro', 'outro', outro_text(197)),
]

FORMULAS = formulas('6', OPTIONS,
                    sys='E_0 = 1 + 1/2 E_1 + 1/2 E_0, quad E_1 = 1 + 1/2 E_0',
                    sol='E_0 = 6')


def validate() -> bool:
    e0 = F(6)
    e1 = 1 + e0 / 2
    assert e0 == 1 + e1 / 2 + e0 / 2 and abs(waits()[-1] - 6) < .2
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS197(ShortScene):
    N = 197

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.seq = VGroup(*[coin(f, .38) for f in 'SNSNN']).arrange(buff=.15).move_to([0, 2.3, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.seq, lag_ratio=.25), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.states = VGroup(token('0', CYAN, .45), token('1', GOLD, .45), token('✓', GREEN, .45)).arrange(buff=1.6) \
            .move_to([0, .8, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.states, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        self.write_board(self.M('sys', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('sol', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.clear_board(.03)
        self.run_sim(waits(), 'số lượt:', 'trung bình:', .4, y=-1.8, color=GREEN, nd=2)

"""XSS116 · Vị trí lá át đầu tiên — 4 lá át chia 48 lá còn lại thành 5 nhóm, mỗi nhóm trung bình 48/5: vị trí 53/5."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, GREEN, PANEL, SOFT  # noqa: E402
from common.visuals import card_back, playing_card  # noqa: E402

EPISODE = {'code': 'XSS116', 'answer': '53/5 = 10,6'}
PROBLEM = ['Xáo bộ bài $52$ lá rồi lật dần từng',
           'lá. Trung bình lá át đầu tiên',
           'nằm ở vị trí thứ mấy?']
OPTIONS = ['13', '53/5 = "10,6"', '"9,6"']
CORRECT = 1
ANSWER_VALUE = None
N, SEED = 1000, 7


def first_ace():
    r, tot, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        d = [1] * 4 + [0] * 48
        r.shuffle(d)
        tot += d.index(1) + 1
        out.append(tot / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Xáo kỹ bộ bài năm mươi hai lá rồi lật từng lá một. Bộ bài có bốn lá át. '
                         'Trung bình, lá át đầu tiên xuất hiện ở vị trí thứ mấy?'),
    Beat('guess', 'hook', 'Mười ba, mười phẩy sáu, hay chín phẩy sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo đối xứng: bốn lá át cắt bốn mươi tám lá còn lại thành năm nhóm, trước át thứ nhất, '
                        'giữa các lá át, và sau át cuối cùng. Vì xáo ngẫu nhiên, năm nhóm này có cùng kích thước trung bình.'),
    Beat('s2', 'solve', 'Mỗi nhóm trung bình có bốn mươi tám chia năm, bằng chín phẩy sáu lá. '
                        'Lá át đầu tiên đứng ngay sau nhóm thứ nhất, nên vị trí trung bình là chín phẩy sáu cộng một, '
                        'bằng mười phẩy sáu.'),
    Beat('s3', 'solve', 'Mô phỏng một nghìn lần xáo bài: vị trí trung bình của lá át đầu tiên bám sát mười phẩy sáu.'),
    Beat('answer', 'solve', 'Đáp án: năm mươi ba phần năm, tức mười phẩy sáu. '
                            'Không cần tính một tổng dài, chỉ cần nhìn ra sự đối xứng!'),
    Beat('outro', 'outro', outro_text(116)),
]

FORMULAS = formulas('53/5 = "10,6"', OPTIONS,
                    gap='48/5 = "9,6" " lá mỗi nhóm"',
                    pos='E = "9,6" + 1 = "10,6" = 53/5')


def validate() -> bool:
    exact = sum(k * F(comb(52 - k, 3), comb(52, 4)) for k in range(1, 50))
    assert exact == F(53, 5) and abs(first_ace()[-1] - 10.6) < .05
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS116(ShortScene):
    N = 116

    def hook_visual(self, t0):
        self.board_top = -1.2
        backs = [card_back(.5) for _ in range(10)]
        self.row = VGroup(*backs, playing_card('A', 'S', .5)).arrange(buff=.08).move_to([0, 1.8, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.row, lag_ratio=.08), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.row.animate.set_opacity(.25), run_time=self.rt(.04))
        groups = []
        for i in range(5):
            box = card(1.0, .8, SOFT, PANEL, radius=.12, stroke_width=3)
            groups.append(VGroup(box, self.TM('$?$', 28, SOFT).move_to(box)))
            if i < 4:
                groups.append(playing_card('A', 'SHDC'[i], .55))
        self.scheme = VGroup(*groups).arrange(buff=.1)
        self.scheme.scale_to_fit_width(min(self.scheme.width, 7.4)).move_to([0, .55, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.scheme, lag_ratio=.12), run_time=self.rt(.25))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[g[1].animate.become(self.TM('$"9,6"$', 26, GOLD).move_to(g[0])) for g in self.scheme[::2]],
                  run_time=self.rt(.08))
        self.write_board(self.M('gap', 1.9))
        self.wait_until(.55, t0)
        self.play(self.scheme[1].animate.scale(1.25), run_time=self.rt(.05))
        m = self.M('pos', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.clear_board(.03)
        self.run_sim(first_ace(), 'số lần xáo:', 'vị trí trung bình:', .6, y=-1.8, color=GREEN, nd=2)



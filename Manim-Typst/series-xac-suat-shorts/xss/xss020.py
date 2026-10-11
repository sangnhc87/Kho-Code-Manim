"""XSS020 · Ít nhất một ngửa — ba đồng xu: 1 − P(SSS) = 1 − 1/8 = 7/8."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402
from common.visuals import coin  # noqa: E402
from xss.xss019 import LEAVES, three_coin_tree  # noqa: E402

EPISODE = {'code': 'XSS020', 'answer': '7/8'}
PROBLEM = ['Tung ba đồng xu.', 'Xác suất có ít nhất một mặt ngửa?']
OPTIONS = ['3/8', '1/2', '7/8']
CORRECT = 2
ANSWER_VALUE = 7 / 8

BEATS = [
    Beat('hook', 'hook', 'Tung ba đồng xu. Xác suất có ít nhất một mặt ngửa là bao nhiêu? '
                         'Đếm từng trường hợp thì dài, nhưng có một lối tắt.'),
    Beat('guess', 'hook', 'Ba phần tám, một phần hai, hay bảy phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẫn là cây tám lá. Ít nhất một ngửa gồm các trường hợp có một, hai hoặc ba mặt ngửa: '
                        'đếm trực tiếp khá mất công.'),
    Beat('s2', 'solve', 'Lối tắt: biến cố đối của ít nhất một ngửa là không có mặt ngửa nào, '
                        'tức cả ba đều sấp. Chỉ đúng một lá: sấp sấp sấp.'),
    Beat('s3', 'solve', 'Vậy xác suất bằng một trừ một phần tám, bằng bảy phần tám. '
                        'Gặp chữ ít nhất, hãy nghĩ ngay đến biến cố đối.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần tám. Cứ tám lần tung bộ ba đồng xu, trung bình chỉ một lần không có mặt ngửa.'),
    Beat('outro', 'outro', outro_text(20)),
]

FORMULAS = formulas('7/8', OPTIONS,
                    comp='overline(A) = {S S S}',
                    calc='P(A) = 1 - 1/8 = 7/8')


def validate() -> bool:
    assert Fraction(sum('N' in w for w in LEAVES), 8) == 1 - Fraction(1, 8) == Fraction(7, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS020(ShortScene):
    N = 20

    def hook_visual(self, t0):
        self.coins = VGroup(*[coin(f, .9) for f in 'SSS']).arrange(buff=.35).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.coins, lag_ratio=.3), run_time=self.rt(.2))

    def beat_s1(self, T):
        self.play(self.coins.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.coins)
        self.board_top = -1.25
        self.levels, self.labels = three_coin_tree()
        self.play(*[FadeIn(lv) for lv in self.levels], FadeIn(self.labels), run_time=self.rt(.2))
        self.play(*[self.labels[i].animate.set_color(GREEN) for i, w in enumerate(LEAVES) if 'N' in w],
                  run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[self.labels[i].animate.set_color(CYAN).set_opacity(.4) for i in range(1, 8)],
                  self.labels[0].animate.set_color(CORAL).scale(1.5), run_time=self.rt(.1))
        self.play(FadeIn(cross(CORAL, .5).move_to(self.labels[0])), run_time=self.rt(.04))
        self.wait_until(.5, t0)
        self.write_board(self.M('comp', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('calc', 2.2)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('"ít nhất" → biến cố đối', 28, CYAN, bold=True), anim='fade')

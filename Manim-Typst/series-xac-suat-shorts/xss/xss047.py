"""XSS047 · Đoán mò trúng ít nhất 1 — 1 − (3/4)⁴ = 175/256 ≈ 68 % (bẫy 4 · 1/4 = 1)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS047', 'answer': '175/256'}
PROBLEM = ['Đoán mò $4$ câu trắc nghiệm, mỗi câu $4$',
           'phương án. Xác suất đúng ít nhất $1$ câu?']
OPTIONS = ['1', '175/256', '1/4']
CORRECT = 1
ANSWER_VALUE = 175 / 256
KEYS = 'BDAC'

BEATS = [
    Beat('hook', 'hook', 'Vẫn khoanh bừa bốn câu trắc nghiệm, mỗi câu bốn phương án. '
                         'Lần này chỉ cần đúng ít nhất một câu. Xác suất là bao nhiêu?'),
    Beat('guess', 'hook', 'Chắc chắn bằng một, một trăm bảy mươi lăm phần hai trăm năm mươi sáu, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bẫy kinh điển: mỗi câu một phần tư, bốn câu cộng lại bằng một, chắc chắn đúng ít nhất một câu? '
                        'Sai! Hoàn toàn có thể sai cả bốn câu.'),
    Beat('s2', 'solve', 'Dùng biến cố đối: sai cả bốn câu. Mỗi câu sai với xác suất ba phần tư, '
                        'nên sai hết là ba phần tư mũ bốn, bằng tám mươi mốt phần hai trăm năm mươi sáu.'),
    Beat('s3', 'solve', 'Vậy xác suất đúng ít nhất một câu bằng một trừ tám mươi mốt phần hai trăm năm mươi sáu, '
                        'bằng một trăm bảy mươi lăm phần hai trăm năm mươi sáu, khoảng sáu mươi tám phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: một trăm bảy mươi lăm phần hai trăm năm mươi sáu. Cao, nhưng không bao giờ chắc chắn!'),
    Beat('outro', 'outro', outro_text(47)),
]

FORMULAS = formulas('175/256', OPTIONS,
                    trap='4 dot 1/4 = 1 quad coral(times)',
                    none='P("sai cả 4") = (3/4)^4 = 81/256',
                    prob='P = 1 - 81/256 = 175/256 approx "68" %')


def validate() -> bool:
    ways = list(product('ABCD', repeat=4))
    hit = F(sum(any(w[i] == KEYS[i] for i in range(4)) for w in ways), 256)
    assert hit == F(175, 256) == 1 - F(3, 4) ** 4 and round(175 / 256 * 100) == 68
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS047(ShortScene):
    N = 47

    def hook_visual(self, t0):
        self.rows = VGroup()
        for i in range(4):
            opts = VGroup(*[token(c, SOFT, .3) for c in 'ABCD']).arrange(buff=.2)
            self.rows.add(VGroup(tx(f'Câu {i + 1}', 26, SOFT, bold=True), opts).arrange(buff=.4))
        self.rows.arrange([0, -1, 0], buff=.28).move_to([0, 1.3, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.rows, lag_ratio=.2), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(self.M('trap', 2.0))
        self.wait_until(.55, t0)
        wrong = [row[1][('ABCD'.index(k) + 1) % 4] for row, k in zip(self.rows, KEYS)]
        self.play(*[w[0].animate.set_fill(CORAL) for w in wrong], run_time=self.rt(.1))
        self.write_board(tx('sai cả 4 vẫn có thể xảy ra!', 28, CORAL, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.35, t0)
        self.write_board(self.M('none', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        right = [row[1]['ABCD'.index(k)] for row, k in zip(self.rows, KEYS)]
        self.play(right[2][0].animate.set_fill(GREEN), run_time=self.rt(.06))
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)

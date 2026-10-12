"""XSS268 · Dẫn 2–0 trong loạt 7 ván — A cần thêm 2 thắng trước khi B có 4: Σ C(1+k,k) 0,6² 0,4^k (k ≤ 3) ≈ 0,913."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS268', 'answer': '≈ 0,913'}
PROBLEM = ['Ai thắng $4$ ván trước là vô địch;',
           'A thắng mỗi ván $"0,6"$ và đang dẫn',
           '$2-0$. Xác suất A vô địch?']
OPTIONS = ['"0,6"', 'approx "0,913"', 'approx "0,8"']
CORRECT = 1
ANSWER_VALUE = .913
P, Q = F(3, 5), F(2, 5)
TERMS = [comb(1 + k, k) * P ** 2 * Q ** k for k in range(4)]

BEATS = [
    Beat('hook', 'hook', 'Chung kết bảy ván, ai thắng bốn ván trước vô địch. A thắng mỗi ván với xác suất không phẩy sáu, và đang dẫn hai không. '
                         'Xác suất A vô địch là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy sáu, khoảng không phẩy chín một ba, hay khoảng không phẩy tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điều kiện đang dẫn hai không: A chỉ cần thêm hai ván thắng, trước khi B thắng đủ bốn ván. '
                        'Chia theo số ván B thắng trước khi A thắng ván quyết định: không, một, hai hoặc ba.'),
    Beat('s2', 'solve', 'B thắng k ván: ván cuối là A thắng, k cộng một ván trước có đúng một ván A thắng: k cộng một cách. '
                        'Xác suất k cộng một nhân không phẩy sáu bình phương nhân không phẩy bốn mũ k.'),
    Beat('s3', 'solve', 'Cộng bốn trường hợp: không phẩy ba sáu, không phẩy hai tám tám, không phẩy một bảy hai tám, không phẩy không chín hai một sáu: '
                        'khoảng không phẩy chín một ba.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy chín một ba. Dẫn hai không trong loạt bảy ván gần như nắm chắc chức vô địch!'),
    Beat('outro', 'outro', outro_text(268)),
]

FORMULAS = formulas('approx "0,913"', OPTIONS,
                    term='P_k = (k + 1) dot "0,6"^2 dot "0,4"^k',
                    tot='P = "0,36" + "0,288" + "0,1728" + "0,09216" approx "0,913"')


def validate() -> bool:
    brute = sum(P ** w.count('A') * Q ** w.count('B') for w in map(''.join, product('AB', repeat=5)) if w.count('A') >= 2)
    assert sum(TERMS) == brute and round(float(brute), 3) == .913
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS268(ShortScene):
    N = 268

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.score = VGroup(VGroup(token('A', CYAN, .45), self.TM('$2$', 44, CYAN)).arrange(buff=.25),
                            self.TM('$-$', 44, SOFT),
                            VGroup(self.TM('$0$', 44, CORAL), token('B', CORAL, .45)).arrange(buff=.25)).arrange(buff=.5) \
            .move_to([0, 2.1, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.score, lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.TM('A cần thêm $2$ thắng, B cần $4$', 30, GOLD), anim='fade')

    def beat_s2(self, T):
        self.clear_board(.03)
        self.write_board(self.M('term', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.6)
        self.write_board(m)
        self.frame(m)

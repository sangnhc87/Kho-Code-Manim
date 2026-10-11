"""XSS199 · Giải độc đắc 6/45 — 1/C(45,6) = 1/8 145 060."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS199', 'answer': '1/8 145 060'}
PROBLEM = ['Chọn $6$ số trong $45$ số. Xác suất',
           'bộ số của bạn trùng đủ $6$ số được',
           'quay (giải độc đắc)?']
OPTIONS = ['1/45^6', '1/8145060', '6/45']
CORRECT = 1
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Xổ số kiểu sáu trên bốn mươi lăm: bạn chọn sáu số khác nhau từ một đến bốn mươi lăm. '
                         'Trúng giải độc đắc khi khớp đủ sáu số được quay. Xác suất là bao nhiêu?'),
    Beat('guess', 'hook', 'Một trên bốn mươi lăm mũ sáu, một trên tám triệu một trăm bốn mươi lăm nghìn không trăm sáu mươi, '
                          'hay sáu phần bốn mươi lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Thứ tự không quan trọng, nên số bộ sáu số là tổ hợp chập sáu của bốn mươi lăm, '
                        'bằng tám triệu một trăm bốn mươi lăm nghìn không trăm sáu mươi.'),
    Beat('s2', 'solve', 'Chỉ đúng một bộ trùng khớp. Xác suất một trên hơn tám triệu, tương đương tung đồng xu được hai mươi ba lần ngửa liên tiếp.'),
    Beat('s3', 'solve', 'Nếu mua mỗi tuần một vé, trung bình phải chờ hơn một trăm năm mươi nghìn năm mới trúng một lần.'),
    Beat('answer', 'solve', 'Đáp án: một trên tám triệu một trăm bốn mươi lăm nghìn không trăm sáu mươi. Xác suất giúp ta tỉnh táo trước những giấc mơ đổi đời!'),
    Beat('outro', 'outro', outro_text(199)),
]

FORMULAS = formulas('1/8145060', OPTIONS,
                    n='n(Omega) = C_45^6 = 8145060',
                    coin='2^23 approx 8388608',
                    years='8145060 " tuần" approx 156000 " năm"')


def validate() -> bool:
    assert comb(45, 6) == 8145060 and 2 ** 22 < comb(45, 6) < 2 ** 23
    assert round(comb(45, 6) / 52.18, -3) == 156000
    assert F(1, comb(45, 6)) == F(1, 8145060)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS199(ShortScene):
    N = 199

    def hook_visual(self, t0):
        self.board_top = -1.2
        picks = {7, 13, 22, 28, 36, 41}
        self.nums = VGroup(*[token(str(k), GOLD if k in picks else SOFT, .24, 15) for k in range(1, 46)]) \
            .arrange_in_grid(5, 9, buff=.14).move_to([0, 1.6, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.nums, lag_ratio=.01), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        m = self.M('n', 2.0)
        self.write_board(m)
        self.frame(m, CYAN)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('coin', 1.9), anim='fade')

    def beat_s3(self, T):
        self.clear_board(.03)
        self.write_board(self.M('years', 1.8))
        self.write_board(tx('mỗi tuần một vé', 26, CORAL), anim='fade')

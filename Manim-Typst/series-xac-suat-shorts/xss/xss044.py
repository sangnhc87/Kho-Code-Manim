"""XSS044 · Mạch nối tiếp — 3 linh kiện 0,9 nối tiếp: 0,9³ = 0,729."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402
from common.visuals import circuit  # noqa: E402

EPISODE = {'code': 'XSS044', 'answer': '0,729'}
PROBLEM = ['$3$ linh kiện nối tiếp, mỗi cái hoạt',
           'động với xác suất $"0,9"$ (độc lập).',
           'Xác suất mạch hoạt động?']
OPTIONS = ['"0,9"', '"0,729"', '"2,7"']
CORRECT = 1
ANSWER_VALUE = .729

BEATS = [
    Beat('hook', 'hook', 'Một mạch điện có ba linh kiện mắc nối tiếp. Mỗi linh kiện hoạt động tốt với xác suất không phẩy chín, '
                         'độc lập với nhau. Xác suất cả mạch hoạt động là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy chín, không phẩy bảy hai chín, hay hai phẩy bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mắc nối tiếp nghĩa là dòng điện phải đi qua cả ba linh kiện. Chỉ một cái hỏng là cả mạch tắt.'),
    Beat('s2', 'solve', 'Vậy mạch hoạt động khi cả ba cùng tốt. Các linh kiện độc lập nên ta nhân: '
                        'không phẩy chín mũ ba, bằng không phẩy bảy hai chín.'),
    Beat('s3', 'solve', 'Mỗi linh kiện tốt tới chín mươi phần trăm, nhưng cả mạch chỉ còn khoảng bảy mươi ba phần trăm. '
                        'Càng nhiều khâu nối tiếp, hệ thống càng dễ hỏng.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bảy hai chín. Nối tiếp: tất cả phải cùng tốt, nhân các xác suất.'),
    Beat('outro', 'outro', outro_text(44)),
]

FORMULAS = formulas('"0,729"', OPTIONS, prob='P = "0,9"^3 = "0,729"')


def validate() -> bool:
    assert F(9, 10) ** 3 == F(729, 1000)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS044(ShortScene):
    N = 44

    def hook_visual(self, t0):
        self.c = circuit(3, False, 1.35, .95).move_to([0, 1.3, 0])
        self.tags = VGroup(*[self.TM('$"0,9"$', 32, SOFT).next_to(b, UP, buff=.18) for b in self.c.boxes])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.c), FadeIn(self.tags), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(self.c.boxes[1].animate.set_stroke(CORAL, 6).set_fill(CORAL, .5), run_time=self.rt(.08))
        self.write_board(tx('1 cái hỏng → cả mạch tắt', 30, CORAL, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[b.animate.set_stroke(GREEN, 6).set_fill(GREEN, .45) for b in self.c.boxes], run_time=self.rt(.1))
        self.wait_until(.45, t0)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(tx('nhiều khâu nối tiếp → dễ hỏng hơn', 28, SOFT), anim='fade')

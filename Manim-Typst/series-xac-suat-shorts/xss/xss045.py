"""XSS045 · Mạch song song — 2 linh kiện 0,9 song song: 1 − 0,1² = 0,99."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import RIGHT, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402
from common.visuals import circuit  # noqa: E402

EPISODE = {'code': 'XSS045', 'answer': '0,99'}
PROBLEM = ['$2$ linh kiện mắc song song, mỗi cái',
           'hoạt động với xác suất $"0,9"$ (độc lập).',
           'Xác suất mạch hoạt động?']
OPTIONS = ['"0,81"', '"0,99"', '"0,9"']
CORRECT = 1
ANSWER_VALUE = .99

BEATS = [
    Beat('hook', 'hook', 'Lần này hai linh kiện mắc song song, mỗi cái tốt với xác suất không phẩy chín, độc lập. '
                         'Xác suất mạch hoạt động là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy tám mốt, không phẩy chín chín, hay không phẩy chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mắc song song thì dòng điện có hai đường đi. Chỉ cần một linh kiện tốt là mạch vẫn chạy.'),
    Beat('s2', 'solve', 'Mạch chỉ tắt khi cả hai cùng hỏng: không phẩy một nhân không phẩy một, bằng không phẩy không một. '
                        'Vậy xác suất mạch hoạt động bằng một trừ không phẩy không một, bằng không phẩy chín chín.'),
    Beat('s3', 'solve', 'Không phẩy tám mốt là bẫy: đó là xác suất cả hai cùng tốt, điều kiện của mạch nối tiếp. '
                        'Đây chính là lý do máy bay, bệnh viện luôn có hệ thống dự phòng song song.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín chín. Song song: chỉ hỏng khi tất cả cùng hỏng.'),
    Beat('outro', 'outro', outro_text(45)),
]

FORMULAS = formulas('"0,99"', OPTIONS,
                    off='P("cả hai hỏng") = "0,1"^2 = "0,01"',
                    prob='P = 1 - "0,01" = "0,99"')


def validate() -> bool:
    assert 1 - F(1, 10) ** 2 == F(99, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS045(ShortScene):
    N = 45

    def hook_visual(self, t0):
        self.c = circuit(2, True, 1.2, .7).move_to([0, 1.3, 0])
        self.tags = VGroup(*[self.TM('$"0,9"$', 26, SOFT).next_to(b, RIGHT, buff=.2).shift([0, .35, 0])
                             for b in self.c.boxes])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.c), FadeIn(self.tags), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.c.boxes[0].animate.set_stroke(CORAL, 6).set_fill(CORAL, .5),
                  self.c.boxes[1].animate.set_stroke(GREEN, 6).set_fill(GREEN, .45), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.write_board(tx('1 cái tốt là đủ!', 32, GREEN, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[b.animate.set_stroke(CORAL, 6).set_fill(CORAL, .5) for b in self.c.boxes], run_time=self.rt(.08))
        self.write_board(self.M('off', 1.7))
        self.wait_until(.55, t0)
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.clear_board(.03)
        self.write_board(self.TM('$"0,9"^2 = "0,81"$: nối tiếp', 30, CORAL, bold=True), anim='fade')
        self.write_board(tx('hệ thống dự phòng = song song', 28, SOFT), anim='fade')

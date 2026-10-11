"""XSS177 · Hai đội mạnh cùng bảng — cố định đội mạnh nhất; 3 chỗ còn lại trong bảng / 7 đội: 3/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS177', 'answer': '3/7'}
PROBLEM = ['$8$ đội chia ngẫu nhiên thành $2$ bảng,',
           'mỗi bảng $4$ đội. Xác suất hai đội mạnh',
           'nhất nằm cùng một bảng?']
OPTIONS = ['1/2', '3/7', '1/4']
CORRECT = 1
ANSWER_VALUE = 3 / 7

BEATS = [
    Beat('hook', 'hook', 'Tám đội bóng được bốc thăm chia vào hai bảng, mỗi bảng bốn đội. '
                         'Xác suất hai đội mạnh nhất rơi vào cùng một bảng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần bảy, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cách đếm chuẩn: chọn bốn đội cho bảng A, tổ hợp chập bốn của tám bằng bảy mươi cách. '
                        'Hai đội mạnh cùng bảng A: chọn thêm hai đội từ sáu, mười lăm cách; cùng bảng B cũng mười lăm. Ba mươi trên bảy mươi.'),
    Beat('s2', 'solve', 'Mẹo nhanh hơn: đặt đội mạnh nhất vào một bảng trước. Bảng đó còn ba chỗ trống, '
                        'bảy đội còn lại chia đều cơ hội vào bảy chỗ.'),
    Beat('s3', 'solve', 'Đội mạnh thứ hai rơi vào một trong ba chỗ cùng bảng với xác suất ba phần bảy. Cả hai cách cùng ra ba phần bảy.'),
    Beat('answer', 'solve', 'Đáp án: ba phần bảy. Cố định một đối tượng rồi xét đối tượng còn lại là mẹo làm bài chia nhóm cực nhanh!'),
    Beat('outro', 'outro', outro_text(177)),
]

FORMULAS = formulas('3/7', OPTIONS,
                    count='(2 C_6^2)/(C_8^4) = 30/70 = 3/7',
                    quick='P = 3/7')


def validate() -> bool:
    groups = list(combinations(range(8), 4))
    assert F(sum((0 in g) == (1 in g) for g in groups), len(groups)) == F(3, 7) == F(2 * comb(6, 2), comb(8, 4))
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS177(ShortScene):
    N = 177

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.teams = VGroup(*[token(str(i + 1), CORAL if i < 2 else CYAN, .32) for i in range(8)]).arrange(buff=.2) \
            .move_to([0, 2.6, 0])
        self.boxes = VGroup(*[VGroup(card(3.0, 2.2, SOFT, PANEL, radius=.15, stroke_width=3), tx(n, 24, SOFT))
                              for n in ('bảng A', 'bảng B')]).arrange(buff=.6).move_to([0, .6, 0])
        for b in self.boxes:
            b[1].next_to(b[0], [0, 1, 0], buff=.08)
        self.wait_until(.55, t0)
        self.play(FadeIn(self.teams, lag_ratio=.1), FadeIn(self.boxes), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('count', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        slots = VGroup(*[card(.62, .62, GOLD, PANEL, radius=.3, stroke_width=3) for _ in range(4)]) \
            .arrange_in_grid(2, 2, buff=.25).move_to(self.boxes[0][0])
        self.play(FadeIn(slots), run_time=self.rt(.05))
        self.play(self.teams[0].animate.move_to(slots[0]), run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.play(*[s.animate.set_stroke(GOLD, 6) for s in slots[1:]], run_time=self.rt(.05))
        self.slots = slots

    def beat_s3(self, T):
        t0 = self.now()
        self.play(self.teams[1].animate.move_to(self.slots[2]), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        m = self.M('quick', 2.3)
        self.write_board(m)
        self.frame(m)

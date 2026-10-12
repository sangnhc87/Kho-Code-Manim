"""XSS304 · Quân mã trên bàn 3 × 3 — 8 ô ngoài nối thành vòng 8 bằng nước mã: về gốc sau 4 bước = P(S ≡ 0 mod 8) = 6/16 = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, Line, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, PANEL, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS304', 'answer': '3/8'}
PROBLEM = ['Quân mã ở góc bàn $3 times 3$, mỗi bước',
           'đi một nước mã hợp lệ ngẫu nhiên. Xác',
           'suất sau $4$ bước quân mã về chỗ cũ?']
OPTIONS = ['1/4', '3/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 3 / 8
CELLS = [(i, j) for i in range(3) for j in range(3)]


def knight(c):
    i, j = c
    return [(i + a, j + b) for a, b in ((1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1))
            if 0 <= i + a < 3 and 0 <= j + b < 3]


def dist(steps):
    d = {(0, 0): F(1)}
    for _ in range(steps):
        nx = {}
        for c, p in d.items():
            for n in knight(c):
                nx[n] = nx.get(n, 0) + p / len(knight(c))
        d = nx
    return d


def cycle():
    order, c = [(0, 0)], knight((0, 0))[0]
    while c != (0, 0):
        order.append(c)
        c = [n for n in knight(c) if n != order[-2]][0]
    return order


BEATS = [
    Beat('hook', 'hook', 'Quân mã đứng ở góc bàn cờ ba nhân ba. Mỗi bước nó đi một nước mã hợp lệ, chọn ngẫu nhiên. '
                         'Sau bốn bước, xác suất quân mã quay về ô góc ban đầu là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, ba phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bí mật của bàn ba nhân ba: quân mã không bao giờ vào được ô tâm, và mỗi ô ngoài có đúng hai nước đi. '
                        'Nối các ô bằng nước mã, tám ô ngoài tạo thành một vòng tròn tám ô!'),
    Beat('s2', 'solve', 'Vậy bài toán chính là ếch nhảy trên vòng tám ô, mỗi bước tiến hoặc lùi một nấc. Về gốc sau bốn bước cần tổng các bước chia hết cho tám.'),
    Beat('s3', 'solve', 'Bốn bước chỉ có tổng bằng không là được: hai tiến hai lùi, sáu dãy trên mười sáu, tức ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Vẽ đồ thị các nước đi, bài cờ vua hóa thành bài đi ngẫu nhiên trên vòng tròn!'),
    Beat('outro', 'outro', outro_text(304)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    ring='"8 ô ngoài" = "vòng 8 ô", quad "mỗi bước" plus.minus 1',
                    prob='P = (C_4^2)/2^4 = 6/16 = 3/8')


def validate() -> bool:
    assert knight((1, 1)) == [] and all(len(knight(c)) == 2 for c in CELLS if c != (1, 1))
    assert len(cycle()) == 8 and dist(4)[(0, 0)] == F(3, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS304(ShortScene):
    N = 304

    def hook_visual(self, t0):
        self.board_top = -1.25
        s = 1.1
        self.pos = {c: [(c[1] - 1) * s, 1.5 - (c[0] - 1) * s, 0] for c in CELLS}
        self.board = VGroup(*[Square(side_length=s, stroke_color=STROKE, stroke_width=3, fill_color=PANEL, fill_opacity=1).move_to(self.pos[c])
                              for c in CELLS])
        self.piece = token('M', GOLD, .35).move_to(self.pos[(0, 0)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.board), FadeIn(self.piece, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        order = cycle()
        self.ring = VGroup(*[Line(self.pos[a], self.pos[b], color=CYAN, stroke_width=4) for a, b in zip(order, order[1:] + order[:1])])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.ring, lag_ratio=.12), run_time=self.rt(.2))
        self.bring_to_front(self.piece)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('ring', 1.6))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)

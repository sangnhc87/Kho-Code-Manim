"""XSS285 · Ếch trên ngũ giác — 5 bước ±1 về gốc ⇔ tổng ≡ 0 (mod 5) ⇔ tổng = ±5: 2/32 = 1/16."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import Dot, FadeIn, Polygon, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, STROKE, WHITE  # noqa: E402
from common.visuals import polygon_pts  # noqa: E402
from xss._frogkit import frog  # noqa: E402

EPISODE = {'code': 'XSS285', 'answer': '1/16'}
PROBLEM = ['Ếch ở một đỉnh ngũ giác đều, mỗi bước',
           'nhảy sang một trong hai đỉnh kề. Xác',
           'suất sau $5$ bước ếch về chỗ cũ?']
OPTIONS = ['0', '1/16', '1/5']
CORRECT = 1
ANSWER_VALUE = 1 / 16

BEATS = [
    Beat('hook', 'hook', 'Ếch ở một đỉnh ngũ giác đều, mỗi bước nhảy sang một đỉnh kề. Sau năm bước, xác suất ếch quay về đỉnh ban đầu là bao nhiêu? '
                         'Năm là số lẻ, liệu có về được không?'),
    Beat('guess', 'hook', 'Không, một phần mười sáu, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Khác hình vuông, ngũ giác có số đỉnh lẻ nên không tô màu xen kẽ được: ếch có thể về sau số lẻ bước, bằng cách đi trọn một vòng!'),
    Beat('s2', 'solve', 'Tổng các bước cộng trừ một phải chia hết cho năm. Năm bước thì tổng từ trừ năm đến năm, và là số lẻ, nên chỉ có thể bằng năm hoặc trừ năm.'),
    Beat('s3', 'solve', 'Tức là năm bước cùng một chiều: đi vòng thuận hoặc vòng nghịch, hai dãy trên ba mươi hai, bằng một phần mười sáu.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười sáu. Trên vòng tròn, "về gốc" còn có thể là đi trọn một vòng!'),
    Beat('outro', 'outro', outro_text(285)),
]

FORMULAS = formulas('1/16', OPTIONS,
                    mod='S equiv 0 space "(mod 5)", quad S in {-5; 5}',
                    prob='P = 2/2^5 = 1/16')


def validate() -> bool:
    assert F(sum(sum(w) % 5 == 0 for w in product((1, -1), repeat=5)), 32) == F(1, 16)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS285(ShortScene):
    N = 285

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.pts = polygon_pts(5, 1.6, (0, 1.4))
        self.shape = VGroup(Polygon(*self.pts, stroke_color=STROKE, stroke_width=4), *[Dot(p, radius=.12, color=WHITE) for p in self.pts])
        self.fr = frog(.2).move_to(self.pts[0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.shape), FadeIn(self.fr, scale=2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        for k in (1, 2, 3, 4, 0):
            self.play(self.fr.animate.move_to(self.pts[k]), run_time=self.rt(.05))
        self.wait_until(.6, t0)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('mod', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m, GOLD)



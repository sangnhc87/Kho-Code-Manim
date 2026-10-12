"""XSS353 · Không ai ngồi cạnh ai — 4 trong 10 ghế dãy: không kề ⇔ C(10 − 4 + 1; 4) = C(7;4) = 35 trên C(10;4) = 210 → 1/6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN  # noqa: E402
from xss._seatkit import seat, seat_row  # noqa: E402

EPISODE = {'code': 'XSS353', 'answer': '1/6'}
PROBLEM = ['Dãy $10$ ghế, $4$ người chọn ngẫu nhiên $4$',
           'ghế. Xác suất không có $2$ người nào',
           'ngồi cạnh nhau?']
OPTIONS = ['1/6', '1/5', '2/7']
CORRECT = 0
ANSWER_VALUE = 1 / 6
SETS = list(combinations(range(10), 4))
GOOD = [s for s in SETS if all(s[i + 1] - s[i] > 1 for i in range(3))]

BEATS = [
    Beat('hook', 'hook', 'Một dãy mười ghế, bốn người chọn ngẫu nhiên bốn ghế. Xác suất không có hai người nào ngồi cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, một phần năm, hay hai phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chỉ cần biết tập ghế có người: tổ hợp chập bốn của mười, hai trăm mười cách.'),
    Beat('s2', 'solve', 'Mẹo khe hở: xếp trước sáu ghế trống thành hàng, tạo ra bảy khe kể cả hai đầu. Mỗi người chọn một khe khác nhau thì không ai kề ai: tổ hợp chập bốn của bảy, ba mươi lăm cách.'),
    Beat('s3', 'solve', 'Xác suất ba mươi lăm phần hai trăm mười, tức một phần sáu.'),
    Beat('answer', 'solve', 'Đáp án: một phần sáu. Bài không kề nhau: xếp phần còn lại trước, rồi chèn vào khe.'),
    Beat('outro', 'outro', outro_text(353)),
]

FORMULAS = formulas('1/6', OPTIONS,
                    all='C_10^4 = 210',
                    gap='C_7^4 = 35',
                    prob='P = 35/210 = 1/6')


def validate() -> bool:
    assert len(SETS) == 210 and len(GOOD) == 35
    assert F(len(GOOD), len(SETS)) == F(1, 6)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS353(ShortScene):
    N = 353

    def place(self, idx, frac=.06):
        new = seat([('', CYAN)] * 4, [self.seats[i] for i in idx], r=.22)
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.seats = seat_row(10, y=1.3, w=.6, gap=.1)
        self.play(FadeIn(self.seats), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.place((1, 2, 5, 8))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.place((0, 3, 6, 9), .05)
        self.wait_until(.6, t0)
        self.place((1, 4, 6, 8), .05)
        self.write_board(self.M('gap', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

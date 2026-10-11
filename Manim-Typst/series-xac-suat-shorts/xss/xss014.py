"""XSS014 · Chia hết cho 3 — từ 1 đến 20 chỉ có 6 bội của 3: 3/10 (bẫy 1/3)."""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PANEL_2, STROKE, WHITE  # noqa: E402

EPISODE = {'code': 'XSS014', 'answer': '3/10'}
PROBLEM = ['Chọn ngẫu nhiên một số từ $1$ đến $20$.', 'Xác suất số đó chia hết cho $3$?']
OPTIONS = ['1/3', '3/10', '1/4']
CORRECT = 1
ANSWER_VALUE = .3

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên một số từ một đến hai mươi. Xác suất số đó chia hết cho ba là bao nhiêu? '
                         'Rất nhiều bạn trả lời ngay một phần ba. Có đúng không?'),
    Beat('guess', 'hook', 'Một phần ba, ba phần mười, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Viết hai mươi số thành bảng. Không gian mẫu có hai mươi kết quả đồng khả năng.'),
    Beat('s2', 'solve', 'Các số chia hết cho ba: ba, sáu, chín, mười hai, mười lăm và mười tám. '
                        'Chỉ có sáu số thôi, vì hai mươi không chia hết cho ba.'),
    Beat('s3', 'solve', 'Xác suất bằng sáu phần hai mươi, tức ba phần mười. Đáp án một phần ba chỉ đúng khi '
                        'số lượng số là bội của ba, chẳng hạn chọn từ một đến hai mươi mốt.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười. Đừng đoán theo cảm giác, hãy đếm!'),
    Beat('outro', 'outro', outro_text(14)),
]

FORMULAS = formulas('3/10', OPTIONS,
                    n='n(Omega) = 20',
                    event='A = {3; 6; 9; 12; 15; 18}',
                    prob='P(A) = 6/20 = 3/10',
                    other='1 arrow.r 21: quad 7/21 = 1/3')


def validate() -> bool:
    assert Fraction(sum(k % 3 == 0 for k in range(1, 21)), 20) == Fraction(3, 10)
    assert Fraction(sum(k % 3 == 0 for k in range(1, 22)), 21) == Fraction(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS014(ShortScene):
    N = 14

    def hook_visual(self, t0):
        self.big = tx('?', 160, GOLD, bold=True).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.big, scale=.5), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.big.animate.scale(.1).set_opacity(0), run_time=self.rt(.05))
        self.remove(self.big)
        cells = VGroup()
        for k in range(1, 21):
            sq = Square(side_length=1.05, stroke_color=STROKE, stroke_width=2, fill_color=PANEL_2, fill_opacity=1)
            cells.add(VGroup(sq, self.TM(f'${k}$', 30, WHITE).move_to(sq)))
        cells.arrange_in_grid(4, 5, buff=.1).move_to([0, 1.25, 0])
        self.cells = cells
        self.play(FadeIn(cells, lag_ratio=.05), run_time=self.rt(.35))
        self.wait_until(.7, t0)
        self.write_board(self.M('n', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        for k in range(3, 21, 3):
            self.play(self.cells[k - 1][0].animate.set_fill(GOLD, .55), run_time=self.rt(.05))
        self.wait_until(.6, t0)
        self.play(self.cells[19][0].animate.set_stroke(CORAL, 5), run_time=self.rt(.04))
        self.write_board(self.M('event', 1.7))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.M('other', 1.6), anim='fade')

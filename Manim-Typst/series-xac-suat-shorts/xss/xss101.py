"""XSS101 · Bàn tròn 6 người — nhìn từ A: B ngồi 1 trong 5 ghế còn lại, 2 ghế kề A → 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import Circle, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT, STROKE  # noqa: E402
from common.visuals import polygon_pts, token  # noqa: E402

EPISODE = {'code': 'XSS101', 'answer': '2/5'}
PROBLEM = ['$6$ người ngồi ngẫu nhiên quanh một bàn',
           'tròn. Xác suất A và B ngồi cạnh nhau?']
OPTIONS = ['1/3', '2/5', '1/2']
CORRECT = 1
ANSWER_VALUE = .4

BEATS = [
    Beat('hook', 'hook', 'Sáu người ngồi ngẫu nhiên quanh một chiếc bàn tròn. Xác suất A và B ngồi cạnh nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, hai phần năm, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo bàn tròn: cho A ngồi trước. Bàn tròn không có đầu cuối, nên chỗ của A không quan trọng.'),
    Beat('s2', 'solve', 'Bây giờ B chọn một trong năm ghế còn lại, khả năng như nhau. Có đúng hai ghế sát bên A, '
                        'một bên trái và một bên phải.'),
    Beat('s3', 'solve', 'Xác suất bằng hai phần năm. Kiểm tra bằng đếm: xếp sáu người quanh bàn có năm giai thừa cách, '
                        'gộp A B thành khối còn bốn giai thừa nhân hai, tỉ số đúng bằng hai phần năm.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Với bàn tròn, hãy cố định một người trước!'),
    Beat('outro', 'outro', outro_text(101)),
]

FORMULAS = formulas('2/5', OPTIONS, seat='P = ("2 ghế kề")/("5 ghế") = 2/5', chk='(4! dot 2)/(5!) = 48/120 = 2/5')


def validate() -> bool:
    ok = sum((p.index('A') - p.index('B')) % 6 in (1, 5) for p in permutations('ABCDEF'))
    assert F(ok, 720) == F(2, 5) == F(48, 120)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS101(ShortScene):
    N = 101

    def hook_visual(self, t0):
        self.board_top = -1.4
        pts = polygon_pts(6, 1.9, (0, 1.3))
        self.table = Circle(radius=1.15, stroke_color=STROKE, stroke_width=4, fill_color='#14233B', fill_opacity=1) \
            .move_to([0, 1.3, 0])
        self.seats = VGroup(*[token(' ', SOFT, .38).move_to(p) for p in pts])
        self.pts = pts
        self.wait_until(.35, t0)
        self.play(FadeIn(self.table), FadeIn(self.seats, lag_ratio=.15), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        a = token('A', GOLD, .42).move_to(self.pts[0])
        self.play(FadeIn(a, scale=1.4), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[self.seats[i][0].animate.set_fill(CYAN, .6) for i in range(1, 6)], run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.play(*[self.seats[i][0].animate.set_fill(GREEN, 1) for i in (1, 5)], run_time=self.rt(.08))
        self.write_board(tx('2 ghế kề A trong 5 ghế', 30, GREEN, bold=True), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('seat', 1.8)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.45, t0)
        self.write_board(self.M('chk', 1.6), anim='fade')

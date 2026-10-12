"""XSS319 · Không cạnh nào là cạnh đa giác — 10-giác: n(n−4)(n−5)/6 = 50 tam giác; tù ⇔ có cung ≥ 6 → chỉ kiểu cung (2; 2; 6): 10 tam giác → 1/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402
from xss._polykit import PolyMixin, arcs, is_obtuse, triangles  # noqa: E402

EPISODE = {'code': 'XSS319', 'answer': '1/5'}
PROBLEM = ['Chọn $3$ đỉnh của đa giác đều $10$ cạnh.',
           'Biết tam giác không có cạnh nào là cạnh',
           'của đa giác. Xác suất tam giác tù?']
OPTIONS = ['1/5', '1/4', '2/5']
CORRECT = 0
ANSWER_VALUE = .2
N_ = 10
COND = triangles(N_, lambda t: 1 not in arcs(t, N_))
OBT = [t for t in COND if is_obtuse(N_)(t)]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba đỉnh của đa giác đều mười cạnh. Biết tam giác không có cạnh nào trùng cạnh của đa giác. '
                         'Xác suất nó là tam giác tù bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, một phần tư, hay hai phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba đỉnh chia đường tròn thành ba cung, đo bằng số cạnh. Không có cạnh đa giác nghĩa là mọi cung ít nhất hai. '
                        'Đếm được năm mươi tam giác như vậy.'),
    Beat('s2', 'solve', 'Góc nội tiếp bằng nửa cung chắn, nên tam giác tù khi có một cung lớn hơn nửa vòng, tức ít nhất sáu cạnh.'),
    Beat('s3', 'solve', 'Một cung sáu thì hai cung còn lại phải đúng bằng hai và hai. Kiểu hai, hai, sáu xoay được mười vị trí: mười tam giác tù.'),
    Beat('s4', 'solve', 'Xác suất mười phần năm mươi, tức một phần năm.'),
    Beat('answer', 'solve', 'Đáp án: một phần năm. Đổi tam giác thành bộ ba cung là chìa khóa của mọi bài đỉnh đa giác đều.'),
    Beat('outro', 'outro', outro_text(319)),
]

FORMULAS = formulas('1/5', OPTIONS,
                    cond='(10 dot 6 dot 5)/6 = 50',
                    obt='"cung" >= 6 arrow.r (2; 2; 6)',
                    cnt='10 "tam giác tù"',
                    prob='P = 10/50 = 1/5')


def validate() -> bool:
    assert len(COND) == 50 and len(OBT) == 10
    assert all(sorted(arcs(t, N_)) == [2, 2, 6] for t in OBT)
    assert F(len(OBT), len(COND)) == F(1, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS319(PolyMixin, ShortScene):
    N = 319

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(N_)
        self.wait_until(.45, t0)
        self.cur = self.flash([(0, 3, 6), (1, 4, 8), (0, 2, 5)], CYAN, .2)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.6, t0)
        m = self.M('cond', 1.5)
        self.write_board(m)

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.4, t0)
        self.write_board(self.M('obt', 1.5))

    def beat_s3(self, T):
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash(OBT[:5], CORAL, .4)
        self.write_board(self.M('cnt', 1.4), anim='fade')

    def beat_s4(self, T):
        self.clear_board(.03)
        self.play(self.cur.animate.set_color(GREEN).set_fill(GREEN, .35), run_time=self.rt(.06))
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

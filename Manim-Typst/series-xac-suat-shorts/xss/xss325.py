"""XSS325 · Tứ giác chứa tâm — bát giác: 70 tứ giác, 32 có khoảng trống ≥ 4 (không chứa tâm) → 38; hình chữ nhật = cặp 2 đường kính: C(4;2) = 6 → 3/19."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402
from xss._polykit import PolyMixin  # noqa: E402

EPISODE = {'code': 'XSS325', 'answer': '3/19'}
PROBLEM = ['Chọn $4$ đỉnh của bát giác đều. Biết tứ',
           'giác tạo thành chứa tâm ở bên trong.',
           'Xác suất đó là hình chữ nhật?']
OPTIONS = ['3/19', '3/35', '1/6']
CORRECT = 0
ANSWER_VALUE = 3 / 19
N_ = 8


def gaps(q):
    return [q[1] - q[0], q[2] - q[1], q[3] - q[2], N_ - q[3] + q[0]]


QUADS = list(combinations(range(N_), 4))
INSIDE = [q for q in QUADS if max(gaps(q)) < N_ // 2]
RECT = [q for q in INSIDE if gaps(q)[0] == gaps(q)[2] and gaps(q)[1] == gaps(q)[3]]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên bốn đỉnh của một bát giác đều. Biết tứ giác tạo thành chứa tâm ở bên trong. '
                         'Xác suất nó là hình chữ nhật bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần mười chín, ba phần ba mươi lăm, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Có bảy mươi tứ giác. Tứ giác không chứa tâm khi bốn đỉnh dồn vào nửa vòng, tức có một khoảng trống từ bốn cạnh trở lên.'),
    Beat('s2', 'solve', 'Đếm chúng: chọn đỉnh đứng ngay sau khoảng trống lớn, tám cách; ba đỉnh còn lại nằm trong bốn đỉnh kế tiếp, bốn cách. '
                        'Ba mươi hai tứ giác bị loại, còn ba mươi tám.'),
    Beat('s3', 'solve', 'Tứ giác nội tiếp là hình chữ nhật khi hai đường chéo đều là đường kính. Bát giác có bốn đường kính, chọn hai: sáu hình chữ nhật, và chúng đều chứa tâm.'),
    Beat('s4', 'solve', 'Xác suất sáu phần ba mươi tám, tức ba phần mười chín.'),
    Beat('answer', 'solve', 'Đáp án: ba phần mười chín. Đếm phần bù qua khoảng trống lớn nhất là mẹo quen thuộc cho bài chứa tâm.'),
    Beat('outro', 'outro', outro_text(325)),
]

FORMULAS = formulas('3/19', OPTIONS,
                    bad='8 dot C_4^3 = 32',
                    cond='C_8^4 - 32 = 38',
                    rect='C_4^2 = 6',
                    prob='P = 6/38 = 3/19')


def validate() -> bool:
    assert len(QUADS) == 70 and len(INSIDE) == 38 and len(RECT) == 6
    assert F(len(RECT), len(INSIDE)) == F(3, 19)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS325(PolyMixin, ShortScene):
    N = 325

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(N_)
        self.wait_until(.45, t0)
        self.cur = self.flash([(0, 2, 3, 6), (0, 1, 4, 5)], CYAN, .15)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash([(0, 1, 2, 3), (1, 2, 4, 5)], CORAL, .15)

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('bad', 1.5))
        self.wait_until(.6, t0)
        m = self.M('cond', 1.5)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash(RECT[:4], GREEN, .3)
        self.wait_until(.6, t0)
        self.write_board(self.M('rect', 1.5))

    def beat_s4(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

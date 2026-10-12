"""XSS328 · Góc 150 độ — 12-giác: tù ⇔ cung lớn nhất k ≥ 7, mỗi k có (11 − k) cách chia phần còn lại × 12 = 120; góc 150° ⇔ cung (1; 1; 10): 12 → 1/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from xss._polykit import PolyMixin, arcs, is_obtuse, triangles  # noqa: E402

EPISODE = {'code': 'XSS328', 'answer': '1/10'}
PROBLEM = ['Chọn $3$ đỉnh của đa giác đều $12$ cạnh.',
           'Biết được tam giác tù. Xác suất tam giác',
           'có một góc bằng $150 degree$?']
OPTIONS = ['1/10', '1/12', '1/6']
CORRECT = 0
ANSWER_VALUE = .1
N_ = 12
OBT = triangles(N_, is_obtuse(N_))
A150 = [t for t in OBT if 10 in arcs(t, N_)]

BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên ba đỉnh của đa giác đều mười hai cạnh. Biết tam giác tạo thành là tam giác tù. '
                         'Xác suất nó có một góc đúng một trăm năm mươi độ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười, một phần mười hai, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi cạnh của mười hai giác chắn cung ba mươi độ, nên góc nội tiếp chắn k cạnh bằng mười lăm nhân k độ. '
                        'Tam giác tù khi cung lớn nhất có từ bảy cạnh trở lên.'),
    Beat('s2', 'solve', 'Cung lớn bảy, tám, chín, mười thì phần còn lại chia thành hai cung có bốn, ba, hai, một cách. Tổng mười, nhân mười hai vị trí xoay: một trăm hai mươi tam giác tù.'),
    Beat('s3', 'solve', 'Góc một trăm năm mươi độ chắn cung mười cạnh, hai cung kia mỗi cung một cạnh: mười hai tam giác. Xác suất mười hai phần một trăm hai mươi, tức một phần mười.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười. Trong đa giác đều, mọi góc đều là bội của một góc nhỏ, nên bài góc trở thành bài đếm cung.'),
    Beat('outro', 'outro', outro_text(328)),
]

FORMULAS = formulas('1/10', OPTIONS,
                    ang='hat(A) = 15 degree dot k',
                    obt='12 dot (4 + 3 + 2 + 1) = 120',
                    a150='150 degree <-> (1; 1; 10): 12',
                    prob='P = 12/120 = 1/10')


def validate() -> bool:
    assert len(OBT) == 120 and len(A150) == 12
    assert F(len(A150), len(OBT)) == F(1, 10)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS328(PolyMixin, ShortScene):
    N = 328

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.show_ngon(N_)
        self.wait_until(.45, t0)
        self.cur = self.flash([(0, 1, 5), (0, 3, 4)], CYAN, .12)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('ang', 1.5))
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash([(0, 1, 5), (0, 1, 4)], CORAL, .12)

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash([(0, 1, 5), (0, 2, 5), (0, 1, 4), (0, 1, 3)], GOLD, .3)
        self.wait_until(.55, t0)
        self.clear_board(.03)
        self.write_board(self.M('obt', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(FadeOut(self.cur), run_time=self.rt(.03))
        self.cur = self.flash(A150[:3], GREEN, .15)
        self.write_board(self.M('a150', 1.4))
        self.wait_until(.6, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

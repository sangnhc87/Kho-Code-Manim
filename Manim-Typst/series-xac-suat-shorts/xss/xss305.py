"""XSS305 · Hai vũng nước — đường ngắn nhất (0;0) → (3;3) tránh (1;2) và (2;1): chỉ còn 2 đường men mép → 2/20 = 1/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Circle, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN  # noqa: E402
from xss._gridkit import Lattice  # noqa: E402
from xss.xss300 import PATHS, visits  # noqa: E402

EPISODE = {'code': 'XSS305', 'answer': '1/10'}
PROBLEM = ['Chọn ngẫu nhiên đường ngắn nhất từ',
           '$(0; 0)$ tới $(3; 3)$. Có hai vũng nước ở',
           '$(1; 2)$ và $(2; 1)$. Xác suất đường đi khô',
           'ráo?']
OPTIONS = ['1/5', '1/10', '1/4']
CORRECT = 1
ANSWER_VALUE = .1
DRY = [w for w in PATHS if not visits(w, (1, 2)) and not visits(w, (2, 1))]
A = [w for w in PATHS if visits(w, (1, 2))]
B = [w for w in PATHS if visits(w, (2, 1))]

BEATS = [
    Beat('hook', 'hook', 'Đi từ gốc tới điểm ba ba theo đường ngắn nhất trên lưới, chọn ngẫu nhiên một đường. Hai giao lộ một hai và hai một đang có vũng nước. '
                         'Xác suất đường được chọn tránh được cả hai vũng?'),
    Beat('guess', 'hook', 'Một phần năm, một phần mười, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bao hàm loại trừ: đường qua một hai có ba nhân ba bằng chín đường; qua hai một cũng chín đường. Một đường không thể qua cả hai, vì chúng cùng tổng tọa độ.'),
    Beat('s2', 'solve', 'Số đường ướt: chín cộng chín bằng mười tám. Đường khô: hai mươi trừ mười tám bằng hai: đi men mép dưới rồi lên, hoặc men mép trái rồi sang.'),
    Beat('s3', 'solve', 'Xác suất hai phần hai mươi, tức một phần mười. Hai vũng nước nhỏ chặn gần hết các đường!'),
    Beat('answer', 'solve', 'Đáp án: một phần mười. Vật cản trên lưới: đếm đường qua vật cản rồi trừ, nhớ xét phần giao!'),
    Beat('outro', 'outro', outro_text(305)),
]

FORMULAS = formulas('1/10', OPTIONS,
                    wet='n(A) = n(B) = 3 dot 3 = 9, quad n(A sect B) = 0',
                    prob='P = (20 - 9 - 9)/20 = 2/20 = 1/10')


def validate() -> bool:
    assert (len(A), len(B), len(DRY)) == (9, 9, 2) and not set(A) & set(B)
    assert F(len(DRY), 20) == F(1, 10)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS305(ShortScene):
    N = 305

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.L = Lattice(3, 3, origin=(-1.5, -.3), step=1.0)
        self.g = self.L.grid()
        self.pools = VGroup(*[Circle(radius=.28, fill_color=CYAN, fill_opacity=.6, stroke_width=0).move_to(self.L.P(*p)) for p in ((1, 2), (2, 1))])
        self.wait_until(.65, t0)
        self.play(FadeIn(self.g), FadeIn(self.pools), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('wet', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(FadeIn(VGroup(*[self.L.path(w, GREEN, 6) for w in DRY]), lag_ratio=.4), run_time=self.rt(.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m, GOLD)

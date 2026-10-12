"""XSS345 · Nam nữ xen kẽ — 3 nam 3 nữ vào dãy 6 ghế: C(6;3) = 20 cách xếp giới tính, xen kẽ 2 (NNữ… hoặc Nữ N…) → 1/10."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, FadeOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402
from xss._seatkit import seat, seat_row  # noqa: E402

EPISODE = {'code': 'XSS345', 'answer': '1/10'}
PROBLEM = ['$3$ nam, $3$ nữ ngồi ngẫu nhiên vào dãy $6$',
           'ghế. Xác suất nam nữ ngồi xen kẽ?']
OPTIONS = ['1/10', '1/20', '1/5']
CORRECT = 0
ANSWER_VALUE = .1
P_ = {'M': ('Na', CYAN), 'F': ('Nữ', CORAL)}

BEATS = [
    Beat('hook', 'hook', 'Ba bạn nam và ba bạn nữ ngồi ngẫu nhiên vào một dãy sáu ghế. Xác suất nam nữ ngồi xen kẽ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần mười, một phần hai mươi, hay một phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chỉ cần quan tâm ghế nào là nam, ghế nào là nữ. Chọn ba ghế cho nam: tổ hợp chập ba của sáu, hai mươi cách đồng khả năng.'),
    Beat('s2', 'solve', 'Xen kẽ chỉ có hai kiểu: nam ngồi đầu, hoặc nữ ngồi đầu.'),
    Beat('s3', 'solve', 'Xác suất hai phần hai mươi, tức một phần mười. Đếm theo hoán vị cũng ra: hai nhân ba giai thừa nhân ba giai thừa chia sáu giai thừa.'),
    Beat('answer', 'solve', 'Đáp án: một phần mười. Khi chỉ quan tâm nhóm, hãy đếm cách chia chỗ cho nhóm.'),
    Beat('outro', 'outro', outro_text(345)),
]

FORMULAS = formulas('1/10', OPTIONS,
                    all='C_6^3 = 20',
                    alt='2 "kiểu xen kẽ"',
                    prob='P = 2/20 = (2 dot 3! dot 3!)/(6!) = 1/10')


def validate() -> bool:
    orders = set(permutations('MMMFFF'))
    good = sum(all(o[i] != o[i + 1] for i in range(5)) for o in orders)
    assert len(orders) == 20 and good == 2 and F(good, 20) == F(1, 10)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS345(ShortScene):
    N = 345

    def place(self, pattern, frac=.06):
        new = seat([P_[c] for c in pattern], self.seats)
        self.play(*([FadeOut(self.ppl)] if self.ppl else []), FadeIn(new), run_time=self.rt(frac))
        self.ppl = new

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.ppl = None
        self.seats = seat_row(6, y=1.3)
        self.play(FadeIn(self.seats), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.place('MFFMMF')

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.place('FMMFMF', .05)
        self.wait_until(.6, t0)
        self.write_board(self.M('all', 1.5))

    def beat_s2(self, T):
        t0 = self.now()
        self.place('MFMFMF', .05)
        self.wait_until(.5, t0)
        self.place('FMFMFM', .05)
        self.write_board(self.M('alt', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

"""XSS229 · Hai hộp đổ vào một — 1 bi từ I (2Đ1X), 1 bi từ II (1Đ2X) vào III (1Đ): P(đỏ) = (1 + 2/3 + 1/3)/3 = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from xss._urnkit import transfer_arrow, urn_row  # noqa: E402

EPISODE = {'code': 'XSS229', 'answer': '2/3'}
PROBLEM = ['Lấy $1$ bi từ I ($2$ đỏ $1$ xanh) và $1$ bi từ',
           'II ($1$ đỏ $2$ xanh) bỏ vào III (đang có $1$',
           'đỏ). Rút $1$ bi từ III. Xác suất đỏ?']
OPTIONS = ['1/2', '2/3', '5/9']
CORRECT = 1
ANSWER_VALUE = 2 / 3


def direct():
    tot = F(0)
    for a in 'RRB':
        for b in 'RBB':
            box = 'R' + a + b
            tot += F(1, 9) * F(box.count('R'), 3)
    return tot


BEATS = [
    Beat('hook', 'hook', 'Hộp ba đang có một bi đỏ. Lấy một bi từ hộp một có hai đỏ một xanh, và một bi từ hộp hai có một đỏ hai xanh, '
                         'bỏ cả vào hộp ba. Rút một bi từ hộp ba. Xác suất được đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay năm phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hộp ba có ba bi: bi đỏ sẵn có, bi từ hộp một, bi từ hộp hai. Rút ngẫu nhiên nghĩa là mỗi bi trong ba bi có cơ hội một phần ba.'),
    Beat('s2', 'solve', 'Mẹo tuyến tính: xác suất đỏ bằng trung bình xác suất từng bi là đỏ: một, hai phần ba, và một phần ba.'),
    Beat('s3', 'solve', 'Trung bình: một cộng hai phần ba cộng một phần ba, chia ba, bằng hai phần ba. Không cần vẽ cây chín nhánh!'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Rút một bi trong hỗn hợp: lấy trung bình xác suất đỏ của từng bi thành phần!'),
    Beat('outro', 'outro', outro_text(229)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    each='1, quad 2/3, quad 1/3',
                    avg='P = 1/3 (1 + 2/3 + 1/3) = 2/3')


def validate() -> bool:
    assert direct() == F(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS229(ShortScene):
    N = 229

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.urns = urn_row([('RRB', 'I', SOFT), ('RBB', 'II', SOFT), ('R', 'III', GOLD)], y=1.3, buff=.6)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        a1 = transfer_arrow(self.urns[0], self.urns[2])
        a2 = transfer_arrow(self.urns[1], self.urns[2])
        self.play(FadeIn(a1), FadeIn(a2), run_time=self.rt(.08))
        self.wait_until(.5, t0)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('each', 2.1))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('avg', 2.0)
        self.write_board(m)
        self.frame(m)

"""XSS249 · Hộp có bao nhiêu bi? — C(3,2)/C(n,2) = 1/5 ⇒ C(n,2) = 15 ⇒ n = 6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402
from common.visuals import urn  # noqa: E402

EPISODE = {'code': 'XSS249', 'answer': 'n = 6'}
PROBLEM = ['Hộp có $n$ bi, trong đó $3$ bi đỏ. Rút $2$ bi,',
           'xác suất được $2$ bi đỏ là $1/5$. Tìm $n$.']
OPTIONS = ['n = 5', 'n = 6', 'n = 15']
CORRECT = 1
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Mở đầu nhánh bài toán chứa tham số, đi ngược từ xác suất về đề bài. Hộp có n bi, trong đó ba bi đỏ. '
                         'Rút hai bi, xác suất được hai bi đỏ là một phần năm. Hộp có bao nhiêu bi?'),
    Beat('guess', 'hook', 'Năm bi, sáu bi, hay mười lăm bi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Viết xuôi như bình thường: số cách chọn hai bi đỏ là tổ hợp chập hai của ba, bằng ba. Số cách chọn hai bi bất kỳ là tổ hợp chập hai của n.'),
    Beat('s2', 'solve', 'Phương trình: ba chia tổ hợp chập hai của n bằng một phần năm, nên tổ hợp chập hai của n bằng mười lăm, tức n nhân n trừ một bằng ba mươi.'),
    Beat('s3', 'solve', 'Nghiệm n bằng sáu, loại nghiệm âm. Kiểm tra lại: tổ hợp chập hai của sáu bằng mười lăm, ba phần mười lăm bằng một phần năm. Chính xác!'),
    Beat('answer', 'solve', 'Đáp án: sáu bi. Bài ngược: viết công thức xuôi với ẩn, đặt bằng giá trị cho trước, rồi giải phương trình!'),
    Beat('outro', 'outro', outro_text(249)),
]

FORMULAS = formulas('n = 6', OPTIONS,
                    eq='(C_3^2)/(C_n^2) = 1/5 arrow.l.r.double C_n^2 = 15',
                    sol='(n (n - 1))/2 = 15 arrow.l.r.double n = 6')


def validate() -> bool:
    assert [n for n in range(3, 100) if F(comb(3, 2), comb(n, 2)) == F(1, 5)] == [6]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS249(ShortScene):
    N = 249

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.u = urn(['R', 'R', 'R', '#475569', '#475569', '#475569'], cols=3, r=.36).move_to([0, 1.9, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.TM('$P = (C_3^2)/(C_n^2) = 3/(C_n^2)$', 32))

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('eq', 2.0)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        m = self.M('sol', 2.0)
        self.write_board(m)
        self.frame(m)

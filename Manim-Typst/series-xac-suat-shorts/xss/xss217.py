"""XSS217 · Chuyển một, rút hai — I (3Đ2X) → II (2Đ2X), rút 2 từ II: 3/5·3/10 + 2/5·1/10 = 11/50."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402
from xss._urnkit import transfer_arrow, urn_row  # noqa: E402

EPISODE = {'code': 'XSS217', 'answer': '11/50'}
PROBLEM = ['Hộp I: $3$ đỏ $2$ xanh; II: $2$ đỏ $2$ xanh.',
           'Chuyển $1$ bi từ I sang II, rồi rút $2$ bi',
           'từ II. Xác suất được $2$ bi đỏ?']
OPTIONS = ['1/6', '11/50', '3/10']
CORRECT = 1
ANSWER_VALUE = 11 / 50
BRANCHES = [('Đ', CORAL, '3/5', [('ĐĐ', GOLD, '3/10', [])]),
            ('X', CYAN, '2/5', [('ĐĐ', GOLD, '1/10', [])])]


def rr(box):
    p = list(combinations(box, 2))
    return F(sum(a == b == 'R' for a, b in p), len(p))


BEATS = [
    Beat('hook', 'hook', 'Mở đầu nhánh chuyển bi. Hộp một có ba đỏ hai xanh, hộp hai có hai đỏ hai xanh. Chuyển ngẫu nhiên một bi từ hộp một sang hộp hai, '
                         'rồi rút hai bi từ hộp hai. Xác suất được hai bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần sáu, mười một phần năm mươi, hay ba phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bước chuyển là tầng một của cây: bi chuyển là đỏ ba phần năm, xanh hai phần năm. Mỗi nhánh tạo ra một hộp hai khác nhau.'),
    Beat('s2', 'solve', 'Chuyển đỏ: hộp hai có ba đỏ hai xanh, rút hai đỏ ba phần mười. Chuyển xanh: hộp hai có hai đỏ ba xanh, rút hai đỏ một phần mười.'),
    Beat('s3', 'solve', 'Toàn phần: ba phần năm nhân ba phần mười cộng hai phần năm nhân một phần mười, bằng chín cộng hai trên năm mươi, mười một phần năm mươi.'),
    Beat('answer', 'solve', 'Đáp án: mười một phần năm mươi. Bài chuyển bi: tầng một là bi được chuyển, tầng hai là lần rút!'),
    Beat('outro', 'outro', outro_text(217)),
]

FORMULAS = formulas('11/50', OPTIONS,
                    lik='P(Đ Đ | "chuyển Đ") = (C_3^2)/(C_5^2) = 3/10',
                    lik2='P(Đ Đ | "chuyển X") = (C_2^2)/(C_5^2) = 1/10',
                    tot='P = 3/5 dot 3/10 + 2/5 dot 1/10 = 11/50')


def validate() -> bool:
    assert (rr('RRRBB'), rr('RRBBB')) == (F(3, 10), F(1, 10))
    assert F(3, 5) * F(3, 10) + F(2, 5) * F(1, 10) == F(11, 50)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS217(TreeMixin, ShortScene):
    N = 217

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.urns = urn_row([('RRRBB', 'hộp I', GOLD), ('RRBB', 'hộp II', PURPLE)], y=1.15)
        self.arrow = transfer_arrow(self.urns[0], self.urns[1], 'chuyển 1 bi')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), run_time=self.rt(.08))
        self.play(FadeIn(self.arrow), run_time=self.rt(.05))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), self.arrow.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns, self.arrow)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.75, width=5.6, root_label='bi chuyển')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.5, t0)

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.4, t0)
        self.write_board(self.M('lik', 1.6))
        self.write_board(self.M('lik2', 1.6))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.8)
        self.write_board(m)
        self.frame(m)

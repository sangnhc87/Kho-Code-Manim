"""XSS411 · Trùng sinh nhật với bạn — 22 người khác, mỗi người khác ngày bạn với 364/365: 1 − (364/365)²² ≈ 0,059 (khác hẳn nghịch lý ngày sinh ≈ 0,507)."""
from __future__ import annotations

import sys
from math import prod
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402
from common.visuals import polygon_pts, token  # noqa: E402

EPISODE = {'code': 'XSS411', 'answer': '≈ 0,059'}
PROBLEM = ['Lớp có $23$ người, kể cả bạn. Xác suất có',
           'người trùng ngày sinh với chính bạn?']
OPTIONS = ['approx "0,059"', 'approx "0,507"', 'approx "0,029"']
CORRECT = 0
ANSWER_VALUE = .059
P_ME = 1 - (364 / 365) ** 22
P_ANY = 1 - prod((365 - k) / 365 for k in range(23))

BEATS = [
    Beat('hook', 'hook', 'Nghịch lý ngày sinh nói lớp hai mươi ba người có hơn năm mươi phần trăm khả năng có hai bạn trùng ngày sinh. '
                         'Vậy xác suất có người trùng ngày sinh với chính bạn là bao nhiêu?'),
    Beat('guess', 'hook', 'Khoảng không phẩy không năm chín, không phẩy năm không bảy, hay không phẩy không hai chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai mươi hai người còn lại, mỗi người khác ngày sinh với bạn với xác suất ba trăm sáu mươi tư phần ba trăm sáu mươi lăm, độc lập.'),
    Beat('s2', 'solve', 'Không ai trùng với bạn: ba trăm sáu mươi tư phần ba trăm sáu mươi lăm mũ hai mươi hai, khoảng không phẩy chín bốn một.'),
    Beat('s3', 'solve', 'Vậy có người trùng với bạn chỉ khoảng không phẩy không năm chín, gần sáu phần trăm. Nghịch lý ngày sinh cao vì xét mọi cặp, tới hai trăm năm mươi ba cặp.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy không năm chín. Câu hỏi khác một chữ, xác suất khác gần mười lần.'),
    Beat('outro', 'outro', outro_text(411)),
]

FORMULAS = formulas('approx "0,059"', OPTIONS,
                    none='(364/365)^22 approx "0,941"',
                    prob='P = 1 - (364/365)^22 approx "0,059"',
                    pairs='C_23^2 = 253 "cặp"')


def validate() -> bool:
    assert abs(P_ME - .0586) < .001 and abs(P_ANY - .5073) < .001
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS411(ShortScene):
    N = 411

    def hook_visual(self, t0):
        self.board_top = -1.4
        pts = polygon_pts(23, 2.0, (0, .95))
        self.ppl = token('Bạn', CORAL, .36).move_to(pts[0])
        self.ring = [token(' ', CYAN, .18).move_to(p) for p in pts[1:]]
        self.wait_until(.35, t0)
        self.play(FadeIn(self.ppl), *[FadeIn(r) for r in self.ring], run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.ppl.animate.scale(1.2), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('none', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.4)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.M('pairs', 1.3), anim='fade')

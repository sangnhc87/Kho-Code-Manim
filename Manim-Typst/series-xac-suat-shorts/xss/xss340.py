"""XSS340 · Tổng chẵn thì cùng lẻ? — rút lần lượt 2 bi từ 1..9; tổng chẵn ⇔ cùng tính chẵn lẻ: 5·4 + 4·3 = 32; cùng lẻ 20 → 5/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS340', 'answer': '5/8'}
PROBLEM = ['Rút lần lượt $2$ bi từ $9$ bi số $1$ đến $9$.',
           'Biết tổng hai số chẵn. Xác suất cả hai',
           'số đều lẻ?']
OPTIONS = ['5/8', '5/9', '1/2']
CORRECT = 0
ANSWER_VALUE = 5 / 8
PAIRS = [(a, b) for a in range(1, 10) for b in range(1, 10) if a != b and (a + b) % 2 == 0]

BEATS = [
    Beat('hook', 'hook', 'Chín bi đánh số từ một đến chín. Rút lần lượt hai bi không hoàn lại. Biết tổng hai số là số chẵn. '
                         'Xác suất cả hai số đều lẻ bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần tám, năm phần chín, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tổng chẵn khi hai số cùng lẻ hoặc cùng chẵn. Có năm số lẻ và bốn số chẵn.'),
    Beat('s2', 'solve', 'Rút lần lượt hai số lẻ: năm nhân bốn, hai mươi cách. Hai số chẵn: bốn nhân ba, mười hai cách. Điều kiện có ba mươi hai cách.'),
    Beat('s3', 'solve', 'Xác suất cả hai lẻ: hai mươi phần ba mươi hai, bằng năm phần tám.'),
    Beat('answer', 'solve', 'Đáp án: năm phần tám. Nhóm đông hơn được ưu thế theo bình phương, nên nghiêng về số lẻ.'),
    Beat('outro', 'outro', outro_text(340)),
]

FORMULAS = formulas('5/8', OPTIONS,
                    odd='"lẻ, lẻ": 5 dot 4 = 20',
                    even='"chẵn, chẵn": 4 dot 3 = 12',
                    prob='P = 20/(20 + 12) = 5/8')


def validate() -> bool:
    assert len(PAIRS) == 32 and F(sum(a % 2 for a, _ in PAIRS), len(PAIRS)) == F(5, 8)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS340(ShortScene):
    N = 340

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.pool = ball_row('RBRBRBRBR', y=1.9, r=.32, buff=.1, labels=list(range(1, 10)))
        self.play(FadeIn(self.pool, lag_ratio=.08), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        odd = ball_row('RRRRR', r=.3, buff=.1, labels=[1, 3, 5, 7, 9])
        even = ball_row('BBBB', r=.3, buff=.1, labels=[2, 4, 6, 8])
        self.groups = VGroup(odd, even).arrange(DOWN, buff=.3).move_to([0, .45, 0])
        self.play(FadeIn(self.groups, lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('odd', 1.4))
        self.wait_until(.45, t0)
        self.write_board(self.M('even', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

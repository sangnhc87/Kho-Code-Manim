"""XSS409 · Xúc xắc không bắc cầu — A {2,4,9}, B {1,6,8}, C {3,5,7} (mỗi số 2 mặt): A > B, B > C, C > A đều 5/9."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, RIGHT, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS409', 'answer': '5/9'}
PROBLEM = ['Ba xúc xắc A: $2, 2, 4, 4, 9, 9$;',
           'B: $1, 1, 6, 6, 8, 8$; C: $3, 3, 5, 5, 7, 7$',
           'A thắng B $5/9$, B thắng C $5/9$. Xác suất',
           'C thắng A?']
OPTIONS = ['5/9', '4/9', '1/2']
CORRECT = 0
ANSWER_VALUE = 5 / 9
DICE = {'A': (2, 4, 9), 'B': (1, 6, 8), 'C': (3, 5, 7)}


def beats(x, y):
    return F(sum(a > b for a in DICE[x] for b in DICE[y]), 9)


BEATS = [
    Beat('hook', 'hook', 'Ba con xúc xắc lạ. A có các mặt hai, bốn, chín; B có một, sáu, tám; C có ba, năm, bảy, mỗi số xuất hiện hai lần. '
                         'A thắng B với năm phần chín, B thắng C với năm phần chín. Vậy C thắng A với xác suất bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần chín, bốn phần chín, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi số xuất hiện hai lần nên chỉ cần so ba giá trị của C với ba giá trị của A: chín cặp đồng khả năng.'),
    Beat('s2', 'solve', 'C ra ba thắng A ra hai. C ra năm thắng hai và bốn. C ra bảy thắng hai và bốn. Tổng năm cặp.'),
    Beat('s3', 'solve', 'Vậy C thắng A với năm phần chín! A mạnh hơn B, B mạnh hơn C, nhưng C lại mạnh hơn A, như oẳn tù tì.'),
    Beat('answer', 'solve', 'Đáp án: năm phần chín. Quan hệ mạnh hơn trong xác suất không có tính bắc cầu.'),
    Beat('outro', 'outro', outro_text(409)),
]

FORMULAS = formulas('5/9', OPTIONS,
                    pairs='C > A: (3;2), (5;2), (5;4), (7;2), (7;4)',
                    prob='P(C > A) = 5/9')


def validate() -> bool:
    assert beats('A', 'B') == beats('B', 'C') == beats('C', 'A') == F(5, 9)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS409(ShortScene):
    N = 409

    def hook_visual(self, t0):
        self.board_top = -1.4
        rows = VGroup()
        for name, col in (('A', CYAN), ('B', GOLD), ('C', CORAL)):
            rows.add(VGroup(token(name, col, .34), *[token(str(v), SOFT, .3) for v in DICE[name]]).arrange(RIGHT, buff=.25))
        self.rows = rows.arrange(DOWN, buff=.3).move_to([0, 1.2, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.rows, lag_ratio=.25), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.rows[1].animate.set_opacity(.25), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        for i, f in enumerate((.1, .35, .65)):
            self.wait_until(f, t0)
            self.play(self.rows[2][i + 1][0].animate.set_fill(GREEN), run_time=self.rt(.04))
        self.write_board(self.M('pairs', 1.2))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

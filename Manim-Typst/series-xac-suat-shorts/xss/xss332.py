"""XSS332 · Tổng chia hết cho 3 — số dư: 0 {3;6;9}, 1 {1;4;7;10}, 2 {2;5;8}; cùng dư 1 + 4 + 1, mỗi dư một số 3·4·3 = 36 → 42/120 = 7/20."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import SOFT  # noqa: E402
from common.kit import tx  # noqa: E402
from xss._urnkit import ball_row  # noqa: E402

EPISODE = {'code': 'XSS332', 'answer': '7/20'}
PROBLEM = ['Rút $3$ bi từ $10$ bi đánh số $1$ đến $10$.',
           'Xác suất tổng ba số chia hết cho $3$?']
OPTIONS = ['1/3', '7/20', '3/10']
CORRECT = 1
ANSWER_VALUE = 7 / 20
GROUPS = [[3, 6, 9], [1, 4, 7, 10], [2, 5, 8]]

BEATS = [
    Beat('hook', 'hook', 'Mười viên bi đánh số từ một đến mười. Rút ngẫu nhiên ba viên. Xác suất tổng ba số chia hết cho ba là bao nhiêu? '
                         'Nhiều bạn đoán ngay một phần ba.'),
    Beat('guess', 'hook', 'Một phần ba, bảy phần hai mươi, hay ba phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chia bi theo số dư khi chia cho ba: dư không có ba bi, dư một có bốn bi, dư hai có ba bi. Nhóm không đều nên không phải một phần ba.'),
    Beat('s2', 'solve', 'Tổng chia hết cho ba khi ba số cùng một nhóm dư, hoặc mỗi nhóm một số. Cùng nhóm: một cộng bốn cộng một, sáu bộ. Mỗi nhóm một số: ba nhân bốn nhân ba, ba mươi sáu bộ.'),
    Beat('s3', 'solve', 'Tổng bốn mươi hai trên một trăm hai mươi bộ, rút gọn được bảy phần hai mươi.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần hai mươi. Bài chia hết luôn bắt đầu bằng phân nhóm theo số dư.'),
    Beat('outro', 'outro', outro_text(332)),
]

FORMULAS = formulas('7/20', OPTIONS,
                    same='C_3^3 + C_4^3 + C_3^3 = 6',
                    mix='3 dot 4 dot 3 = 36',
                    prob='P = (6 + 36)/C_10^3 = 42/120 = 7/20')


def validate() -> bool:
    good = sum(sum(t) % 3 == 0 for t in combinations(range(1, 11), 3))
    assert good == 42 and F(good, 120) == F(7, 20)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS332(ShortScene):
    N = 332

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.all = ball_row('RBYRBYRBYR', y=1.9, r=.3, buff=.08, labels=list(range(1, 11)))
        self.play(FadeIn(self.all, lag_ratio=.1), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        rows = VGroup()
        for g, c, name in zip(GROUPS, ('R', 'B', 'Y'), ('dư 0', 'dư 1', 'dư 2')):
            rows.add(VGroup(tx(name, 28, SOFT), ball_row(c * len(g), r=.28, buff=.1, labels=g)).arrange(buff=.4))
        rows.arrange(DOWN, buff=.25, aligned_edge=[-1, 0, 0]).move_to([0, .35, 0])
        self.play(FadeIn(rows, lag_ratio=.3), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('same', 1.4))
        self.wait_until(.75, t0)
        self.write_board(self.M('mix', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

"""XSS437 · Số này chia hết số kia — a | b: a = 1..6 cho 6, 3, 2, 1, 1, 1 giá trị b → 14/36 = 7/18."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GREEN  # noqa: E402

EPISODE = {'code': 'XSS437', 'answer': '7/18'}
PROBLEM = ['Gieo $2$ xúc xắc được $a, b$. Xác suất $a$ là',
           'ước của $b$?']
OPTIONS = ['7/18', '1/3', '1/2']
CORRECT = 0
ANSWER_VALUE = 7 / 18
CNT = {a: sum(b % a == 0 for b in range(1, 7)) for a in range(1, 7)}

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc, được hai số a và b. Xác suất a là ước của b, tức b chia hết cho a?'),
    Beat('guess', 'hook', 'Bảy phần mười tám, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm theo a. a bằng một: mọi b, sáu cách. a bằng hai: b là hai, bốn, sáu, ba cách. a bằng ba: ba hoặc sáu, hai cách.'),
    Beat('s2', 'solve', 'a bằng bốn, năm, sáu: chỉ có b bằng chính a, mỗi trường hợp một cách.'),
    Beat('s3', 'solve', 'Tổng mười bốn ô trên ba mươi sáu, rút gọn bảy phần mười tám.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần mười tám. Bảng ba mươi sáu ô và đếm theo hàng: nhanh và không sót.'),
    Beat('outro', 'outro', outro_text(437)),
]

FORMULAS = formulas('7/18', OPTIONS,
                    cnt='6 + 3 + 2 + 1 + 1 + 1 = 14',
                    prob='P = 14/36 = 7/18')


def validate() -> bool:
    assert sum(CNT.values()) == 14 and F(14, 36) == F(7, 18)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS437(DiceGridMixin, ShortScene):
    N = 437

    def hook_visual(self, t0):
        self.wait_until(.45, t0)
        self.show_grid(.1, center=(.1, .55), scale=.85)

    def beat_s1(self, T):
        t0 = self.now()
        c = self.g.cells
        for a, f in ((1, .1), (2, .35), (3, .65)):
            self.wait_until(f, t0)
            self.light([c[b - 1][a - 1] for b in range(1, 7) if b % a == 0], GREEN, .03)

    def beat_s2(self, T):
        c = self.g.cells
        self.light([c[a - 1][a - 1] for a in (4, 5, 6)], GREEN, .04)
        self.write_board(self.M('cnt', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

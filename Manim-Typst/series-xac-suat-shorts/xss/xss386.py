"""XSS386 · Dừng ở +2 hay −2? — ngửa 2/3 (+1), sấp −1; dừng sau đúng 4 lần ⇔ 2 lần đầu khác nhau, 2 lần sau giống nhau: (2/3)² : (1/3)² = 4 : 1 → 4/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS386', 'answer': '4/5'}
PROBLEM = ['Ngửa ($2/3$) được $+1$ điểm, sấp được $-1$;',
           'dừng khi đạt $+2$ hoặc $-2$. Biết dừng sau',
           'đúng $4$ lần. Xác suất dừng ở $+2$?']
OPTIONS = ['4/5', '2/3', '8/9']
CORRECT = 0
ANSWER_VALUE = .8
P = F(2, 3)
BRANCHES = [('0', SOFT, '4/9', [('+2', CYAN, '4/9', []), ('0', SOFT, '4/9', []), ('−2', CORAL, '1/9', [])])]


def ends():
    out = {2: F(0), -2: F(0)}
    for s in product((1, -1), repeat=4):
        pos, ok = 0, True
        for i, x in enumerate(s):
            pos += x
            if abs(pos) == 2 and i < 3:
                ok = False
                break
        if ok and abs(pos) == 2:
            pr = F(1)
            for x in s:
                pr *= P if x == 1 else 1 - P
            out[pos] += pr
    return out


BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu lệch: ngửa với xác suất hai phần ba được cộng một điểm, sấp bị trừ một điểm. Dừng khi đạt cộng hai hoặc trừ hai. '
                         'Biết trò chơi dừng sau đúng bốn lần tung. Xác suất dừng ở cộng hai?'),
    Beat('guess', 'hook', 'Bốn phần năm, hai phần ba, hay tám phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chưa dừng sau hai lần nghĩa là điểm quay về không: một ngửa một sấp, xác suất hai nhân hai phần ba nhân một phần ba, bốn phần chín.'),
    Beat('s2', 'solve', 'Từ điểm không, hai lần tiếp theo phải giống nhau để dừng ở lần bốn: hai ngửa lên cộng hai với bốn phần chín, hai sấp xuống trừ hai với một phần chín.'),
    Beat('s3', 'solve', 'Phần đầu như nhau nên triệt tiêu. Tỉ lệ bốn so với một: dừng ở cộng hai với xác suất bốn phần năm.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần năm. Với điều kiện dừng, cắt cây tại điểm hồi về rồi so hai nhánh kết thúc.'),
    Beat('outro', 'outro', outro_text(386)),
]

FORMULAS = formulas('4/5', OPTIONS,
                    back='P("về 0 sau 2 lần") = 2 dot 2/3 dot 1/3 = 4/9',
                    prob='P(+2 | T = 4) = (4/9)/(4/9 + 1/9) = 4/5')


def validate() -> bool:
    e = ends()
    assert e[2] / (e[2] + e[-2]) == F(4, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS386(TreeMixin, ShortScene):
    N = 386

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.6, width=5.4, r=.4)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1]), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.write_board(self.M('back', 1.4))

    def beat_s2(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

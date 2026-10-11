"""XSS225 · Đồng xu quyết định số bi — ngửa chuyển 1, sấp chuyển 2 từ I (3Đ1X) sang II (1Đ1X): 29/48."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS225', 'answer': '29/48'}
PROBLEM = ['Ngửa: chuyển $1$ bi, sấp: chuyển $2$ bi từ',
           'hộp I ($3$ đỏ $1$ xanh) sang hộp II ($1$ đỏ $1$',
           'xanh); rồi rút $1$ bi từ II. Xác suất đỏ?']
OPTIONS = ['5/8', '29/48', '7/12']
CORRECT = 1
ANSWER_VALUE = 29 / 48
BRANCHES = [('N', GOLD, '1/2', [('Đ', CORAL, '3/4', [('Đ', CORAL, '2/3', [])]), ('X', CYAN, '1/4', [('Đ', CORAL, '1/3', [])])]),
            ('S', PURPLE, '1/2', [('ĐĐ', CORAL, '3/6', [('Đ', CORAL, '3/4', [])]), ('ĐX', CYAN, '3/6', [('Đ', CORAL, '2/4', [])])])]


def p_red(k):
    tot = F(0)
    for m in combinations(range(4), k):
        box = 'RB' + ''.join('RRRB'[i] for i in m)
        tot += F(1, comb(4, k)) * F(box.count('R'), len(box))
    return tot


BEATS = [
    Beat('hook', 'hook', 'Ba hành động liên tiếp: tung đồng xu, ngửa thì chuyển một bi, sấp thì chuyển hai bi từ hộp một có ba đỏ một xanh '
                         'sang hộp hai có một đỏ một xanh. Rồi rút một bi từ hộp hai. Xác suất được đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần tám, hai mươi chín phần bốn mươi tám, hay bảy phần mười hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nhánh ngửa: chuyển đỏ ba phần tư, hộp hai thành hai đỏ một xanh; chuyển xanh một phần tư, thành một đỏ hai xanh. '
                        'Xác suất rút đỏ: ba phần tư nhân hai phần ba cộng một phần tư nhân một phần ba, bằng bảy phần mười hai.'),
    Beat('s2', 'solve', 'Nhánh sấp: chuyển hai đỏ một nửa, hộp hai ba đỏ một xanh; chuyển một đỏ một xanh một nửa, hai đỏ hai xanh. '
                        'Xác suất rút đỏ: một phần hai nhân ba phần tư cộng một phần hai nhân một phần hai, bằng năm phần tám.'),
    Beat('s3', 'solve', 'Toàn phần theo đồng xu: một phần hai nhân bảy phần mười hai cộng một phần hai nhân năm phần tám, bằng hai mươi chín phần bốn mươi tám.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi chín phần bốn mươi tám. Cây ba tầng: tính từng nhánh lớn trước, rồi mới gộp!'),
    Beat('outro', 'outro', outro_text(225)),
]

FORMULAS = formulas('29/48', OPTIONS,
                    head='P(Đ | N) = 3/4 dot 2/3 + 1/4 dot 1/3 = 7/12',
                    tail='P(Đ | S) = 1/2 dot 3/4 + 1/2 dot 2/4 = 5/8',
                    tot='P = 1/2 dot 7/12 + 1/2 dot 5/8 = 29/48')


def validate() -> bool:
    assert (p_red(1), p_red(2)) == (F(7, 12), F(5, 8)) and (p_red(1) + p_red(2)) / 2 == F(29, 48)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS225(TreeMixin, ShortScene):
    N = 225

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.2, width=7.2, root_label='tung xu', r=.38,
                                                  edge_size=24)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2], lag_ratio=.2), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[3][:len(self.levels[3]) // 2], lag_ratio=.2), run_time=self.rt(.1))
        self.write_board(self.M('head', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:], lag_ratio=.2), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[3][len(self.levels[3]) // 2:], lag_ratio=.2), run_time=self.rt(.1))
        self.write_board(self.M('tail', 1.6))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.7)
        self.write_board(m)
        self.frame(m)

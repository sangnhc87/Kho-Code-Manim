"""XSS407 · Sinh đến khi có con trai (tối đa 3) — E[trai] = 1/2 + 1/4 + 1/8 = 7/8, E[con] = 1/2 + 2/4 + 3/4 = 7/4 → tỉ lệ 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402

EPISODE = {'code': 'XSS407', 'answer': '1/2'}
PROBLEM = ['Mỗi gia đình sinh đến khi có con trai,',
           'tối đa $3$ con. Tỉ lệ con trai trong toàn',
           'bộ trẻ em của rất nhiều gia đình?']
OPTIONS = ['1/2', '7/12', '2/3']
CORRECT = 0
ANSWER_VALUE = .5
FAM = [('T', 1, 1, F(1, 2)), ('GT', 2, 1, F(1, 4)), ('GGT', 3, 1, F(1, 8)), ('GGG', 3, 0, F(1, 8))]
BRANCHES = [('T', CYAN, '1/2', []),
            ('G', CORAL, '1/2', [('T', CYAN, '1/2', []), ('G', CORAL, '1/2', [('T', CYAN, '1/2', []), ('G', CORAL, '1/2', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Mỗi gia đình sinh con cho đến khi có một con trai thì dừng, nhưng tối đa ba con. Xét rất nhiều gia đình. '
                         'Tỉ lệ con trai trong toàn bộ trẻ em là bao nhiêu? Chính sách này có làm lệch tỉ lệ không?'),
    Beat('guess', 'hook', 'Một phần hai, bảy phần mười hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây dừng có bốn lá: trai ngay, xác suất một phần hai; gái rồi trai, một phần tư; gái gái trai, một phần tám; ba gái, một phần tám.'),
    Beat('s2', 'solve', 'Số con trai trung bình mỗi nhà: một phần hai cộng một phần tư cộng một phần tám, bằng bảy phần tám. Số con trung bình: một nhân một phần hai cộng hai nhân một phần tư cộng ba nhân một phần tư, bằng bảy phần tư.'),
    Beat('s3', 'solve', 'Tỉ lệ con trai: bảy phần tám chia bảy phần tư, đúng một phần hai!'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Mỗi lần sinh vẫn là một nửa trai, quy tắc dừng không thể thay đổi tỉ lệ đó.'),
    Beat('outro', 'outro', outro_text(407)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    boys='E("trai") = 1/2 + 1/4 + 1/8 = 7/8',
                    kids='E("con") = 1 dot 1/2 + 2 dot 1/4 + 3 dot 1/4 = 7/4',
                    prob='(7/8)/(7/4) = 1/2')


def validate() -> bool:
    eb = sum(b * p for _, _, b, p in FAM)
    ek = sum(k * p for _, k, _, p in FAM)
    assert (eb, ek) == (F(7, 8), F(7, 4)) and eb / ek == F(1, 2)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS407(TreeMixin, ShortScene):
    N = 407

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.15, width=5.4, r=.34, edge_size=24)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        self.play(*[FadeIn(lv) for lv in self.levels[2:]], run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('boys', 1.3))
        self.wait_until(.5, t0)
        self.write_board(self.M('kids', 1.2))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

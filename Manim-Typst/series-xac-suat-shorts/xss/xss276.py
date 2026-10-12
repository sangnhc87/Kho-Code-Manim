"""XSS276 · Ba người, cùng tháng sinh — phần bù: 1 − 12·11·10/12³ = 17/72."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402

EPISODE = {'code': 'XSS276', 'answer': '17/72'}
PROBLEM = ['Ba người, tháng sinh của mỗi người ngẫu',
           'nhiên trong $12$ tháng. Xác suất có ít',
           'nhất $2$ người sinh cùng tháng?']
OPTIONS = ['1/4', '17/72', '1/6']
CORRECT = 1
ANSWER_VALUE = 17 / 72
BRANCHES = [('≠', GREEN, '11/12', [('≠', GREEN, '10/12', []), ('=', CORAL, '2/12', [])]),
            ('=', CORAL, '1/12', [])]

BEATS = [
    Beat('hook', 'hook', 'Ba người bạn, mỗi người sinh vào một tháng ngẫu nhiên. Xác suất có ít nhất hai người sinh cùng tháng là bao nhiêu? '
                         'Đây là phiên bản mini của nghịch lý ngày sinh.'),
    Beat('guess', 'hook', 'Một phần tư, mười bảy phần bảy mươi hai, hay một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ cây theo từng người, chỉ theo dõi "khác hết" hay "đã trùng". Người hai khác tháng người một: mười một phần mười hai.'),
    Beat('s2', 'solve', 'Người ba khác cả hai người trước: mười phần mười hai. Nhánh duy nhất không trùng: mười một phần mười hai nhân mười phần mười hai.'),
    Beat('s3', 'solve', 'Phần bù: một trừ một trăm mười phần một trăm bốn mươi tư, bằng ba mươi tư phần một trăm bốn mươi tư, tức mười bảy phần bảy mươi hai, khoảng hai mươi ba phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: mười bảy phần bảy mươi hai. Cây "khác hết" chỉ có một nhánh, phần bù là lối tắt!'),
    Beat('outro', 'outro', outro_text(276)),
]

FORMULAS = formulas('17/72', OPTIONS,
                    diff='P("khác hết") = 11/12 dot 10/12 = 110/144',
                    comp='P = 1 - 110/144 = 34/144 = 17/72')


def validate() -> bool:
    ws = list(product(range(12), repeat=3))
    assert F(sum(len(set(w)) < 3 for w in ws), len(ws)) == F(17, 72)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS276(TreeMixin, ShortScene):
    N = 276

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.6, width=5.6, root_label='người 2, rồi 3', r=.42)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.03))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.04))
        self.wait_until(.45, t0)
        self.write_board(self.M('diff', 1.9))

    def beat_s3(self, T):
        m = self.M('comp', 1.9)
        self.write_board(m)
        self.frame(m)



"""XSS104 · Chuyển hai bi — I: 4Đ 2X, II: 3Đ 3X; chuyển 2 bi I → II rồi rút 1 ở II: 13/24."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, PURPLE  # noqa: E402
from common.visuals import BALL_COLORS, urn  # noqa: E402

EPISODE = {'code': 'XSS104', 'answer': '13/24'}
PROBLEM = ['Hộp I: $4$ đỏ, $2$ xanh. Hộp II: $3$ đỏ,',
           '$3$ xanh. Chuyển $2$ bi từ I sang II,',
           'rồi rút $1$ bi ở hộp II. $P("đỏ")$?']
OPTIONS = ['1/2', '13/24', '7/12']
CORRECT = 1
ANSWER_VALUE = 13 / 24
RED, BLUE = BALL_COLORS['R'], BALL_COLORS['B']
BRANCHES = [('ĐĐ', RED, '6/15', [('Đ', RED, '5/8', [])]),
            ('ĐX', PURPLE, '8/15', [('Đ', RED, '4/8', [])]),
            ('XX', BLUE, '1/15', [('Đ', RED, '3/8', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp một có bốn đỏ hai xanh, hộp hai có ba đỏ ba xanh. Lấy ngẫu nhiên hai viên ở hộp một bỏ sang hộp hai, '
                         'rồi rút một viên ở hộp hai. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, mười ba phần hai mươi bốn, hay bảy phần mười hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai viên chuyển sang có ba khả năng. Hai đỏ: tổ hợp chập hai của bốn trên tổ hợp chập hai của sáu, '
                        'sáu phần mười lăm. Một đỏ một xanh: tám phần mười lăm. Hai xanh: một phần mười lăm.'),
    Beat('s2', 'solve', 'Hộp hai lúc đó có tám viên. Chuyển hai đỏ thì có năm đỏ: rút đỏ năm phần tám. '
                        'Chuyển một đỏ một xanh: bốn phần tám. Chuyển hai xanh: ba phần tám.'),
    Beat('s3', 'solve', 'Toàn phần: sáu phần mười lăm nhân năm phần tám, cộng tám phần mười lăm nhân bốn phần tám, '
                        'cộng một phần mười lăm nhân ba phần tám, bằng sáu mươi lăm phần một trăm hai mươi, tức mười ba phần hai mươi bốn.'),
    Beat('answer', 'solve', 'Đáp án: mười ba phần hai mươi bốn. Bài chuyển nhiều bi: liệt kê mọi khả năng của bước chuyển!'),
    Beat('outro', 'outro', outro_text(104)),
]

FORMULAS = formulas('13/24', OPTIONS,
                    moves='C_4^2/C_6^2 = 6/15, quad (4 dot 2)/C_6^2 = 8/15, quad C_2^2/C_6^2 = 1/15',
                    tot='P = 6/15 dot 5/8 + 8/15 dot 4/8 + 1/15 dot 3/8 = 65/120 = 13/24')


def validate() -> bool:
    box1 = 'RRRRBB'
    total = F(0)
    for pick in combinations(range(6), 2):
        reds = sum(box1[i] == 'R' for i in pick)
        total += F(1, comb(6, 2)) * F(3 + reds, 8)
    assert total == F(13, 24) and F(comb(4, 2), 15) == F(6, 15)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS104(TreeMixin, ShortScene):
    N = 104

    def hook_visual(self, t0):
        self.urns = VGroup(urn('RRRRBB', 3, .3), urn('RRRBBB', 3, .3)).arrange(buff=1.0).move_to([0, 1.5, 0])
        labs = VGroup(tx('hộp I', 26, CYAN, bold=True).next_to(self.urns[0], DOWN, buff=.15),
                      tx('hộp II', 26, PURPLE, bold=True).next_to(self.urns[1], DOWN, buff=.15))
        self.labs = labs
        self.wait_until(.45, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), FadeIn(labs), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), self.labs.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.urns, self.labs)
        self.board_top = -1.1
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.3), dy=1.8, width=6.6, root_label='chuyển 2 bi')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.write_board(self.M('moves', 1.3))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.25, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.2))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('tot', 1.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.7, t0)
        self.write_board(tx('liệt kê mọi khả năng của bước chuyển', 24, GOLD), anim='fade')

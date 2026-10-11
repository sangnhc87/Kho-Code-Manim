"""XSS220 · Truy ngược hai lần chuyển — từ cây XSS219: P(đi đỏ | rút đỏ) = (2/9 + 1/9)/(7/12) = 4/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402
from xss.xss219 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS220', 'answer': '4/7'}
PROBLEM = ['Như thử thách trước (đi I → II, về II',
           '→ I, rút từ I), biết bi rút từ I là đỏ.',
           'Xác suất bi "đi" lúc đầu là đỏ?']
OPTIONS = ['2/3', '4/7', '1/2']
CORRECT = 1
ANSWER_VALUE = 4 / 7


def posterior():
    num = den = F(0)
    for i, a in enumerate('RRB'):
        box1 = 'RRB'[:i] + 'RRB'[i + 1:]
        for b in 'RBB' + a:
            p = F(1, 3) * F(1, 4) * F((box1 + b).count('R'), 3)
            den += p
            num += p * (a == 'R')
    return num / den


BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: chuyển một bi đi, một bi về, rồi rút từ hộp một được bi đỏ. '
                         'Xác suất bi chuyển đi lúc đầu là bi đỏ là bao nhiêu? Ta phải truy ngược qua hai lần chuyển.'),
    Beat('guess', 'hook', 'Hai phần ba, bốn phần bảy, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trên cây ba tầng, bốn lá "rút đỏ" có xác suất: hai phần chín, một phần chín ở nhánh đi đỏ; '
                        'một phần mười hai, một phần sáu ở nhánh đi xanh. Tổng bảy phần mười hai.'),
    Beat('s2', 'solve', 'Nhánh đi đỏ gom lại: hai phần chín cộng một phần chín, bằng một phần ba.'),
    Beat('s3', 'solve', 'Bayes: một phần ba chia bảy phần mười hai, bằng bốn phần bảy. Thấp hơn hai phần ba ban đầu: '
                        'rút đỏ chẳng phải bằng chứng mạnh cho đi đỏ, vì đi xanh có thể được bù bằng về đỏ.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy. Truy ngược nhiều bước: gom tất cả các lá cùng nguồn gốc rồi lấy tỉ lệ!'),
    Beat('outro', 'outro', outro_text(220)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    red='P("đi Đ" sect "rút Đ") = 2/9 + 1/9 = 1/3',
                    bayes='P("đi Đ" | "rút Đ") = (1/3)/(7/12) = 4/7')


def validate() -> bool:
    assert posterior() == F(4, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS220(TreeMixin, ShortScene):
    N = 220

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.2, width=7.0, root_label='đi → về → rút',
                                                  r=.34, edge_size=26)
        self.wait_until(.7, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[n.animate.scale(1.25) for n, _ in self.leaves], run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.write_board(self.TM('$2/9$, $1/9$, $1/12$, $1/6$: tổng $7/12$', 26))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[self.leaves[i][0].animate.set_stroke(GREEN, 5) for i in (0, 1)], run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.write_board(self.M('red', 1.8))

    def beat_s3(self, T):
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m, CORAL)

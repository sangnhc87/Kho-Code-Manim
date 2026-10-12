"""XSS222 · Hai bi chuyển đều đỏ? — biết rút 2 đỏ từ II: P(chuyển ĐĐ) = (3/15·6/15)/(48/225) = 3/8."""
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

EPISODE = {'code': 'XSS222', 'answer': '3/8'}
PROBLEM = ['Như trên (chuyển $2$ bi I: $3$ đỏ $3$ xanh →',
           'II: $2$ đỏ $2$ xanh), biết $2$ bi rút từ II',
           'đều đỏ. Xác suất $2$ bi đã chuyển đều đỏ?']
OPTIONS = ['1/5', '3/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 3 / 8
BRANCHES = [('ĐĐ', CORAL, '3/15', [('ĐĐ', GOLD, '6/15', [])]),
            ('ĐX', PURPLE, '9/15', [('ĐĐ', GOLD, '3/15', [])]),
            ('XX', CYAN, '3/15', [('ĐĐ', GOLD, '1/15', [])])]


def rr(box):
    p = list(combinations(box, 2))
    return F(sum(a == b == 'R' for a, b in p), len(p))


BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: lần này bạn chỉ thấy hai bi rút từ hộp hai đều đỏ. '
                         'Xác suất hai bi đã chuyển từ hộp một đều là đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, ba phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Rút hai đỏ từ hộp hai: nếu chuyển hai đỏ, hộp có bốn đỏ, xác suất sáu phần mười lăm; chuyển một đỏ một xanh, ba phần mười lăm; '
                        'chuyển hai xanh, một phần mười lăm.'),
    Beat('s2', 'solve', 'Nhân với nhánh: ba nhân sáu bằng mười tám, chín nhân ba bằng hai mươi bảy, ba nhân một bằng ba, cùng mẫu hai trăm hai mươi lăm.'),
    Beat('s3', 'solve', 'Bayes: mười tám chia mười tám cộng hai mươi bảy cộng ba, bằng mười tám phần bốn mươi tám, tức ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Nhánh giữa vẫn đóng góp nhiều nhất vì nó phổ biến nhất ngay từ đầu!'),
    Beat('outro', 'outro', outro_text(222)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    w='3 dot 6 = 18, quad 9 dot 3 = 27, quad 3 dot 1 = 3',
                    bayes='P("chuyển Đ Đ" | "rút Đ Đ") = 18/(18 + 27 + 3) = 3/8')


def validate() -> bool:
    num = den = F(0)
    for m in combinations(range(6), 2):
        moved = ''.join('RRRBBB'[i] for i in m)
        p = F(1, comb(6, 2)) * rr('RRBB' + moved)
        den += p
        num += p * (moved == 'RR')
    assert num / den == F(3, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS222(TreeMixin, ShortScene):
    N = 222

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=6.8, root_label='chuyển 2 bi',
                                                  r=.5)
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv, lag_ratio=.2) for lv in self.levels[:2]], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.play(*[n.animate.scale(1.15) for n, _ in self.leaves], run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('w', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.6)
        self.write_board(m)
        self.frame(m)

"""XSS067 · Nhìn ngược thời gian — biết bi thứ 2 đỏ: P(bi 1 đỏ | bi 2 đỏ) = (5/14)/(5/8) = 4/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, SOFT  # noqa: E402
from xss.xss065 import BALLS, BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS067', 'answer': '4/7'}
PROBLEM = ['Hộp $5$ đỏ, $3$ xanh, rút lần lượt $2$ bi không hoàn lại.', 'Biết bi thứ hai đỏ. Xác suất bi thứ nhất đỏ?']
OPTIONS = ['5/8', '4/7', '5/14']
CORRECT = 1
ANSWER_VALUE = 4 / 7

BEATS = [
    Beat('hook', 'hook', 'Bạn rút hai viên bi lần lượt, giấu viên thứ nhất trong tay, chỉ cho xem viên thứ hai: màu đỏ. '
                         'Xác suất viên trong tay cũng màu đỏ là bao nhiêu? Đây là câu hỏi ngược thời gian!'),
    Beat('guess', 'hook', 'Năm phần tám, bốn phần bảy, hay năm phần mười bốn? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trên cây, chỉ giữ các nhánh có viên thứ hai đỏ: đỏ đỏ với hai mươi phần năm mươi sáu, '
                        'và xanh đỏ với mười lăm phần năm mươi sáu. Tổng là năm phần tám.'),
    Beat('s2', 'solve', 'Trong các nhánh đó, viên thứ nhất đỏ chỉ ở nhánh đỏ đỏ. Xác suất có điều kiện bằng '
                        'hai mươi phần năm mươi sáu chia ba mươi lăm phần năm mươi sáu, bằng bốn phần bảy.'),
    Beat('s3', 'solve', 'Trực giác: biết viên thứ hai đỏ, coi như viên đỏ đó đã ra khỏi hộp. Bảy viên còn lại có bốn đỏ, '
                        'nên viên thứ nhất đỏ với xác suất bốn phần bảy. Đây là tinh thần của công thức Bayes.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy. Thông tin về tương lai vẫn làm thay đổi xác suất của quá khứ!'),
    Beat('outro', 'outro', outro_text(67)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    keep='P(B) = 20/56 + 15/56 = 35/56',
                    bayes='P(A|B) = (20/56)/(35/56) = 4/7')


def validate() -> bool:
    perms = [p for p in permutations(range(8), 2) if BALLS[p[1]] == 'R']
    assert F(sum(BALLS[a] == 'R' for a, _ in perms), len(perms)) == F(4, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS067(TreeMixin, ShortScene):
    N = 67

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='rút')
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[1][0].animate.set_opacity(.2), self.leaves[3][0].animate.set_opacity(.2),
                  run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.write_board(self.M('keep', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.35), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.clear_board(.03)
        m = self.M('bayes', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(tx('còn 7 viên, 4 đỏ', 30, CYAN, bold=True), anim='fade')
        self.write_board(tx('tinh thần công thức Bayes', 24, SOFT), anim='fade')

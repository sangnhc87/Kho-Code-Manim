"""XSS274 · Chuột trong mê cung — E = 1/3·2 + 1/3(3 + E) + 1/3(5 + E) ⇒ E = 10 phút."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402

EPISODE = {'code': 'XSS274', 'answer': '10 phút'}
PROBLEM = ['Chuột chọn ngẫu nhiên $1$ trong $3$ cửa:',
           'cửa $1$ ra ngoài sau $2$ phút, cửa $2$,',
           '$3$ quay lại chỗ cũ sau $3$ và $5$ phút.',
           'Trung bình bao lâu ra?']
OPTIONS = ['"3,33" " phút"', '10 " phút"', '6 " phút"']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('ra', GREEN, '1/3', []), ('↺', CYAN, '1/3', []), ('↺', CORAL, '1/3', [])]
N, SEED = 2000, 4


def sim():
    r, tot = random.Random(SEED), 0
    for _ in range(N):
        t = 0
        while True:
            d = r.randrange(3)
            if d == 0:
                t += 2
                break
            t += 3 if d == 1 else 5
        tot += t
    return tot / N


BEATS = [
    Beat('hook', 'hook', 'Một chú chuột trong mê cung có ba cửa. Cửa một dẫn ra ngoài sau hai phút. Cửa hai và ba là đường vòng, đưa chuột trở lại chỗ cũ sau ba phút và năm phút. '
                         'Chuột không có trí nhớ, mỗi lần chọn ngẫu nhiên. Trung bình bao lâu thì ra?'),
    Beat('guess', 'hook', 'Ba phẩy ba ba phút, mười phút, hay sáu phút? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi E là thời gian trung bình để ra. Ba nhánh: cửa một mất đúng hai phút; cửa hai mất ba phút rồi bắt đầu lại, thêm E; cửa ba mất năm phút rồi thêm E.'),
    Beat('s2', 'solve', 'Phương trình: E bằng một phần ba nhân hai, cộng một phần ba nhân ba cộng E, cộng một phần ba nhân năm cộng E.'),
    Beat('s3', 'solve', 'Rút gọn: một phần ba E bằng mười phần ba, nên E bằng mười phút. Mô phỏng hai nghìn con chuột cũng cho khoảng mười phút.'),
    Beat('answer', 'solve', 'Đáp án: mười phút. Cây có nhánh quay về gốc: kỳ vọng thỏa mãn một phương trình tuyến tính!'),
    Beat('outro', 'outro', outro_text(274)),
]

FORMULAS = formulas('10 " phút"', OPTIONS,
                    eq='E = 1/3 dot 2 + 1/3 (3 + E) + 1/3 (5 + E)',
                    sol='1/3 E = 10/3 arrow.r.double E = 10')


def validate() -> bool:
    e = (F(2) + 3 + 5) / 3 / (1 - F(2, 3))
    assert e == 10 and abs(sim() - 10) < .5
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS274(TreeMixin, ShortScene):
    N = 274

    def hook_visual(self, t0):
        self.board_top = -1.35
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.75, width=6.4, root_label='chọn cửa', r=.46)
        self.wait_until(.8, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        tags = [tx(t, 24, c).next_to(n, [0, -1, 0], buff=.15) for (n, _), t, c in
                zip(self.leaves, ('2 phút', '3 phút + E', '5 phút + E'), (GREEN, CYAN, CORAL))]
        self.wait_until(.3, t0)
        for tg in tags:
            self.play(FadeIn(tg), run_time=self.rt(.04))

    def beat_s2(self, T):
        m = self.M('eq', 1.6)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 2.0)
        self.write_board(m)
        self.frame(m)



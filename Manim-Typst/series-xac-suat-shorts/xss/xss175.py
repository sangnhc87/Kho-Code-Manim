"""XSS175 · Ba đồng xu bí ẩn — P(NN)/P(N) = (29/48)/(3/4) = 29/36."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS175', 'answer': '29/36'}
PROBLEM = ['Ba xu: chuẩn, lệch (ngửa $3/4$), hai mặt',
           'ngửa. Chọn $1$ đồng, tung ra ngửa. Xác',
           'suất lần tung tiếp theo cũng ngửa?']
OPTIONS = ['3/4', '29/36', '5/6']
CORRECT = 1
ANSWER_VALUE = 29 / 36
P = [F(1, 2), F(3, 4), F(1)]
BRANCHES = [('C', CYAN, '1/3', [('N', GOLD, '1/2', [])]),
            ('L', PURPLE, '1/3', [('N', GOLD, '3/4', [])]),
            ('2N', CORAL, '1/3', [('N', GOLD, '1', [])])]

BEATS = [
    Beat('hook', 'hook', 'Ba đồng xu: một đồng chuẩn, một đồng lệch ra ngửa ba phần tư, một đồng hai mặt ngửa. '
                         'Chọn ngẫu nhiên một đồng, tung được ngửa. Tung lại đồng đó, xác suất lại ra ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tư, hai mươi chín phần ba mươi sáu, hay năm phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lần tung đầu ra ngửa với xác suất một phần ba nhân tổng một phần hai, ba phần tư và một, bằng ba phần tư.'),
    Beat('s2', 'solve', 'Hai lần đều ngửa: một phần ba nhân tổng các bình phương: một phần tư, chín phần mười sáu và một, '
                        'bằng hai mươi chín phần bốn mươi tám.'),
    Beat('s3', 'solve', 'Xác suất có điều kiện: hai mươi chín phần bốn mươi tám chia ba phần tư, bằng hai mươi chín phần ba mươi sáu. '
                        'Lớn hơn ba phần tư vì lần ngửa đầu khiến ta nghiêng về đồng xu thiên ngửa.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi chín phần ba mươi sáu. Khi chưa biết đồng xu nào, các lần tung không còn độc lập!'),
    Beat('outro', 'outro', outro_text(175)),
]

FORMULAS = formulas('29/36', OPTIONS,
                    one='P(N_1) = 1/3 (1/2 + 3/4 + 1) = 3/4',
                    two='P(N_1 N_2) = 1/3 (1/4 + 9/16 + 1) = 29/48',
                    prob='P(N_2 | N_1) = (29/48)/(3/4) = 29/36')


def validate() -> bool:
    one = sum(P) / 3
    two = sum(p * p for p in P) / 3
    assert (one, two, two / one) == (F(3, 4), F(29, 48), F(29, 36))
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS175(TreeMixin, ShortScene):
    N = 175

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.coins = VGroup(VGroup(coin('N', .45), coin('S', .45)).arrange(buff=.08),
                            VGroup(coin('N', .45), coin('S', .45)).arrange(buff=.08),
                            VGroup(coin('N', .45), coin('N', .45)).arrange(buff=.08)).arrange(buff=.6).move_to([0, 1.6, 0])
        self.labs = VGroup(*[tx(n, 22, c).next_to(g, [0, -1, 0]) for n, c, g in
                             zip(('chuẩn', 'lệch', 'hai mặt ngửa'), (CYAN, PURPLE, CORAL), self.coins)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.coins, lag_ratio=.3), FadeIn(self.labs), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.coins.animate.set_opacity(0), self.labs.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.coins, self.labs)
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.7, width=6.6, root_label='chọn xu')
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.2))
        self.wait_until(.5, t0)
        self.write_board(self.M('one', 1.8))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('two', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)



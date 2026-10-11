"""XSS004 · Không gian mẫu — tung hai đồng xu: 4 kết quả (sơ đồ cây, quy tắc nhân)."""
from __future__ import annotations

import sys
from pathlib import Path
from itertools import product

from manim import DOWN, UP, FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import coin, tree  # noqa: E402

EPISODE = {'code': 'XSS004', 'answer': '4'}
PROBLEM = ['Tung hai đồng xu cùng lúc.', 'Có bao nhiêu kết quả có thể xảy ra?']
OPTIONS = ['2', '3', '4']
CORRECT = 2
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Tung hai đồng xu cùng lúc. Có bao nhiêu kết quả có thể xảy ra? '
                         'Nghe rất dễ, nhưng rất nhiều người trả lời sai.'),
    Beat('guess', 'hook', 'Hai, ba, hay bốn kết quả? Chọn nhanh! Ba, hai, một!'),
    Beat('s1', 'solve', 'Hãy đánh số hai đồng xu: xu một và xu hai. Xu một có hai khả năng: sấp hoặc ngửa.'),
    Beat('s2', 'solve', 'Với mỗi khả năng của xu một, xu hai lại có hai khả năng. Sơ đồ cây mọc ra bốn nhánh: '
                        'sấp sấp, sấp ngửa, ngửa sấp và ngửa ngửa.'),
    Beat('s3', 'solve', 'Sấp ngửa và ngửa sấp là hai kết quả khác nhau, vì hai đồng xu là hai vật khác nhau. '
                        'Theo quy tắc nhân, hai nhân hai bằng bốn.'),
    Beat('answer', 'solve', 'Đáp án: bốn kết quả. Hãy nhớ kỹ điều này, vì thử thách tiếp theo sẽ cần đến nó!'),
    Beat('outro', 'outro', outro_text(4)),
]

FORMULAS = formulas('4', OPTIONS,
                    omega='Omega = {S S; space S N; space N S; space N N}',
                    rule='n(Omega) = 2 dot 2 = 4')


def validate() -> bool:
    assert len(list(product('SN', repeat=2))) == 4
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


def node(face):
    return coin(face, .5)


class XSS004(ShortScene):
    N = 4

    def hook_visual(self, t0):
        self.c1 = coin('N', 1.1).move_to([-1.5, 1.3, 0])
        self.c2 = coin('S', 1.1).move_to([1.5, 1.3, 0])
        self.play(FadeIn(self.c1, scale=.6), FadeIn(self.c2, scale=.6), run_time=self.rt(.06))
        self.wait_until(.35, t0)
        self.c1 = self.flip(self.c1, 'SNS', self.rt(.3))
        self.c2 = self.flip(self.c2, 'NSN', self.rt(.3))

    def build_tree(self):
        root = {'m': tx('bắt đầu', 24, SOFT), 'kids': []}
        for f in 'SN':
            kids = [{'m': node(g), 'kids': []} for g in 'SN']
            root['kids'].append({'m': node(f), 'kids': kids})
        g, levels = tree(root, top=(-.1, 3.3), dy=1.5, width=6.4)
        leaves = VGroup(*[tx(a + b, 30, GOLD, bold=True) for a in 'SN' for b in 'SN'])
        for lab, leaf in zip(leaves, [k['m'] for c in root['kids'] for k in c['kids']]):
            lab.next_to(leaf, DOWN, buff=.15)
        side = VGroup(tx('xu 1', 24, CYAN, bold=True).move_to([-3.55, 3.3 - 1.5, 0]),
                      tx('xu 2', 24, CYAN, bold=True).move_to([-3.55, 3.3 - 3.0, 0]))
        return levels, leaves, side

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.c1), FadeOut(self.c2), run_time=self.rt(.05))
        self.levels, self.leaves, self.side = self.build_tree()
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), FadeIn(self.side[0]), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.2, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), FadeIn(self.side[1]), run_time=self.rt(.2))
        self.wait_until(.55, t0)
        for lab in self.leaves:
            self.play(FadeIn(lab, shift=UP * .1), run_time=self.rt(.07))

    def beat_s3(self, T):
        t0 = self.now()
        self.board_top = -1.05
        self.play(self.leaves[1].animate.scale(1.3), self.leaves[2].animate.scale(1.3), run_time=self.rt(.06))
        self.play(self.leaves[1].animate.scale(1 / 1.3), self.leaves[2].animate.scale(1 / 1.3), run_time=self.rt(.06))
        self.write_board(self.M('omega', 1.6))
        self.wait_until(.6, t0)
        m = self.M('rule', 2.0)
        self.write_board(m)
        self.frame(m)


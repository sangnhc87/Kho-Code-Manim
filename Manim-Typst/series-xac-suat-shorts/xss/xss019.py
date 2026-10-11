"""XSS019 · Đúng 2 mặt ngửa — ba đồng xu: cây 8 lá, 3 lá thuận lợi → 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from common.visuals import coin, tree  # noqa: E402

EPISODE = {'code': 'XSS019', 'answer': '3/8'}
PROBLEM = ['Tung ba đồng xu.', 'Xác suất có đúng $2$ mặt ngửa?']
OPTIONS = ['1/3', '3/8', '1/2']
CORRECT = 1
ANSWER_VALUE = 3 / 8
LEAVES = [''.join(w) for w in product('SN', repeat=3)]

BEATS = [
    Beat('hook', 'hook', 'Tung ba đồng xu cùng lúc. Xác suất có đúng hai mặt ngửa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, ba phần tám, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẽ sơ đồ cây: mỗi đồng xu tách mỗi nhánh thành hai. Ba đồng xu cho hai nhân hai nhân hai, '
                        'bằng tám kết quả đồng khả năng.'),
    Beat('s2', 'solve', 'Tìm các lá có đúng hai chữ N: sấp ngửa ngửa, ngửa sấp ngửa, ngửa ngửa sấp. '
                        'Có ba lá, vì mặt sấp duy nhất có thể nằm ở ba vị trí.'),
    Beat('s3', 'solve', 'Xác suất bằng ba phần tám. Đáp án một phần ba là bẫy quen thuộc: đếm số mặt ngửa từ không '
                        'đến ba rồi coi chúng đồng khả năng, trong khi thực tế không phải vậy.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Sơ đồ cây không bao giờ đếm sai!'),
    Beat('outro', 'outro', outro_text(19)),
]

FORMULAS = formulas('3/8', OPTIONS, n='n(Omega) = 2^3 = 8', prob='P = 3/8')


def validate() -> bool:
    assert Fraction(sum(w.count('N') == 2 for w in LEAVES), 8) == Fraction(3, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


def three_coin_tree():
    root = {'m': tx('bắt đầu', 22, SOFT), 'kids': []}
    for a in 'SN':
        mid = []
        for b in 'SN':
            mid.append({'m': coin(b, .27), 'kids': [{'m': coin(c, .27), 'kids': []} for c in 'SN']})
        root['kids'].append({'m': coin(a, .3), 'kids': mid})
    g, levels = tree(root, top=(0, 3.35), dy=1.08, width=6.9)
    leaves = [k['m'] for c in root['kids'] for m in c['kids'] for k in m['kids']]
    labels = VGroup(*[tx(w, 20, SOFT, bold=True).next_to(leaf, DOWN, buff=.12) for w, leaf in zip(LEAVES, leaves)])
    return levels, labels


class XSS019(ShortScene):
    N = 19

    def hook_visual(self, t0):
        self.coins = VGroup(*[coin(f, .9) for f in 'NSN']).arrange(buff=.35).move_to([0, 1.3, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.coins, lag_ratio=.3), run_time=self.rt(.2))

    def beat_s1(self, T):
        self.play(self.coins.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.coins)
        self.board_top = -1.25
        self.levels, self.labels = three_coin_tree()
        for lv in self.levels:
            self.play(FadeIn(lv, lag_ratio=.1), run_time=self.rt(.1))
        self.play(FadeIn(self.labels, lag_ratio=.05), run_time=self.rt(.1))
        self.write_board(self.M('n', 2.0))

    def beat_s2(self, T):
        self.clear_board(.03)
        for i, w in enumerate(LEAVES):
            if w.count('N') == 2:
                self.play(self.labels[i].animate.set_color(GOLD), run_time=self.rt(.08))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('prob', 2.4)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.45, t0)
        self.write_board(tx('0, 1, 2, 3 mặt ngửa không đồng khả năng', 24, SOFT), anim='fade')

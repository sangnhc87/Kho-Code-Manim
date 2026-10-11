"""XSS090 · Thư bỏ nhầm phong bì — 4 lá thư: 9 hoán vị không điểm cố định / 24 = 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL  # noqa: E402

EPISODE = {'code': 'XSS090', 'answer': '3/8'}
PROBLEM = ['Bỏ ngẫu nhiên $4$ lá thư vào $4$ phong',
           'bì đã ghi địa chỉ. Xác suất KHÔNG',
           'lá nào đúng địa chỉ?']
OPTIONS = ['1/4', '3/8', '1/24']
CORRECT = 1
ANSWER_VALUE = 3 / 8
DER = [p for p in permutations(range(4)) if all(p[i] != i for i in range(4))]

BEATS = [
    Beat('hook', 'hook', 'Một thư ký đãng trí bỏ bốn lá thư vào bốn phong bì đã ghi sẵn địa chỉ, hoàn toàn ngẫu nhiên. '
                         'Xác suất không lá thư nào đến đúng người là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, ba phần tám, hay một phần hai mươi bốn? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn lá thư vào bốn phong bì có bốn giai thừa bằng hai mươi bốn cách. '
                        'Ta cần đếm các cách mà không lá nào nằm đúng chỗ, gọi là hoán vị không có điểm cố định.'),
    Beat('s2', 'solve', 'Dùng bao hàm loại trừ: lấy hai mươi bốn, trừ các cách có ít nhất một lá đúng, '
                        'cộng lại phần trừ trùng, cứ thế xen kẽ. Kết quả còn đúng chín cách.'),
    Beat('s3', 'solve', 'Chín cách đó hiện trên màn hình, không lá nào trùng màu với phong bì của mình. '
                        'Xác suất bằng chín phần hai mươi bốn, tức ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Thử thách sau: nếu có thật nhiều lá thư thì sao? Một con số rất nổi tiếng sẽ xuất hiện!'),
    Beat('outro', 'outro', outro_text(90)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    n='n(Omega) = 4! = 24',
                    ie='D_4 = 24 - 4 dot 6 + 6 dot 2 - 4 dot 1 + 1 = 9',
                    prob='P = 9/24 = 3/8')


def validate() -> bool:
    assert len(DER) == 9 and F(len(DER), factorial(4)) == F(3, 8)
    assert 24 - 4 * 6 + 6 * 2 - 4 * 1 + 1 == 9
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


COL = (GOLD, CYAN, CORAL, GREEN)


class XSS090(ShortScene):
    N = 90

    def hook_visual(self, t0):
        envs = VGroup()
        for i in range(4):
            c = card(1.3, .9, COL[i], PANEL, radius=.1, stroke_width=4)
            envs.add(VGroup(c, self.TM(f'${i + 1}$', 30, COL[i], bold=True).move_to(c)))
        self.envs = envs.arrange(buff=.3).move_to([0, 1.6, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(envs, lag_ratio=.2), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(self.M('n', 2.2))
        self.wait_until(.5, t0)
        self.write_board(tx('không lá nào đúng chỗ', 30, CORAL, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.25, t0)
        m = self.M('ie', 1.5)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.envs.animate.set_opacity(0), run_time=self.rt(.03))
        self.remove(self.envs)
        rows = VGroup()
        for p in DER:
            cells = VGroup()
            for i, letter in enumerate(p):
                c = card(.42, .42, COL[i], PANEL, radius=.06, stroke_width=2)
                cells.add(VGroup(c, self.MNum(letter + 1, 0, COL[letter], 20).move_to(c)))
            rows.add(cells.arrange(buff=.05))
        rows.arrange_in_grid(3, 3, buff=(.35, .2)).move_to([0, 1.4, 0])
        self.play(FadeIn(rows, lag_ratio=.1), run_time=self.rt(.25))
        self.wait_until(.6, t0)
        m = self.M('prob', 2.2)
        self.write_board(m)
        self.frame(m)



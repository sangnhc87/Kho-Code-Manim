"""XSS086 · Monty Hall — đổi cửa thắng 2/3 (liệt kê 3 trường hợp + mô phỏng 1000 ván)."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, RIGHT, UP, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import badge, card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS086', 'answer': '2/3'}
PROBLEM = ['$3$ cửa, sau $1$ cửa là ô tô. Bạn chọn',
           'cửa $1$, người dẫn mở một cửa có dê.',
           'ĐỔI cửa thì xác suất thắng xe?']
OPTIONS = ['1/2', '2/3', '1/3']
CORRECT = 1
ANSWER_VALUE = 2 / 3
GAMES, SEED = 1000, 39


def switch_wins():
    r, w, out = random.Random(SEED), 0, []
    for k in range(1, GAMES + 1):
        w += r.randrange(3) != 0  # you picked door 0; switching wins exactly when the car is elsewhere
        out.append(w / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Bài toán gây tranh cãi nhất lịch sử xác suất. Ba cánh cửa, sau một cửa là ô tô, hai cửa còn lại là dê. '
                         'Bạn chọn cửa số một. Người dẫn chương trình, biết rõ xe ở đâu, mở một cửa khác có dê, '
                         'rồi hỏi bạn có muốn đổi cửa không. Đổi thì xác suất thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lúc bạn chọn, cửa số một có một phần ba cơ hội có xe. Hai cửa còn lại, gộp chung, có hai phần ba.'),
    Beat('s2', 'solve', 'Người dẫn luôn mở được một cửa có dê trong hai cửa còn lại, nên hành động đó không cho thêm thông tin '
                        'về cửa của bạn. Cửa của bạn vẫn một phần ba, và cả hai phần ba dồn sang cửa còn đóng.'),
    Beat('s3', 'solve', 'Liệt kê ba khả năng vị trí xe. Xe ở cửa một: giữ thì thắng, đổi thì thua. '
                        'Xe ở cửa hai hoặc cửa ba: người dẫn buộc phải mở cửa dê còn lại, đổi thì thắng. Đổi thắng hai trên ba.'),
    Beat('s4', 'solve', 'Vẫn chưa tin? Mô phỏng một nghìn ván, luôn đổi cửa: tỉ lệ thắng bám sát hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Luôn đổi cửa! Nhà toán học lừng danh Paul Erdős ban đầu cũng không tin, '
                            'cho đến khi được xem mô phỏng.'),
    Beat('outro', 'outro', outro_text(86)),
]

FORMULAS = formulas('2/3', OPTIONS,
                    keep='P("giữ") = 1/3',
                    switch='P("đổi") = 1 - 1/3 = 2/3')


def validate() -> bool:
    assert F(sum(car != 0 for car in range(3)), 3) == F(2, 3)
    assert abs(switch_wins()[-1] - 2 / 3) < .005
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS086(ShortScene):
    N = 86

    def door(self, n, w=1.7, h=2.4):
        c = card(w, h, GOLD, PANEL, radius=.15, stroke_width=4)
        return VGroup(c, self.TM(f'${n}$', 48, GOLD, bold=True).move_to(c))

    def hook_visual(self, t0):
        self.doors = VGroup(*[self.door(n) for n in (1, 2, 3)]).arrange(buff=.4).move_to([0, 1.5, 0])
        self.wait_until(.3, t0)
        self.play(FadeIn(self.doors, lag_ratio=.25), run_time=self.rt(.12))
        self.wait_until(.48, t0)
        self.play(self.doors[0][0].animate.set_stroke(CYAN, 7), run_time=self.rt(.04))
        self.play(FadeIn(tx('bạn chọn', 24, CYAN, bold=True).next_to(self.doors[0], DOWN, buff=.15)), run_time=self.rt(.03))
        self.wait_until(.7, t0)
        goat = badge('DÊ', SOFT, 26).move_to(self.doors[2])
        self.play(self.doors[2][1].animate.set_opacity(0), FadeIn(goat), run_time=self.rt(.06))
        self.goat = goat

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(VGroup(tx('cửa 1:', 30, CYAN, bold=True), self.M('keep', 1.8)).arrange(RIGHT, buff=.25),
                         anim='fade')
        self.wait_until(.45, t0)
        self.write_board(self.TM('cửa $2$ và $3$: $2/3$', 32, GOLD, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.5, t0)
        arrow = tx('2/3 dồn về đây', 26, GOLD, bold=True).next_to(self.doors[1], UP, buff=.15)
        self.play(self.doors[1][0].animate.set_stroke(GOLD, 7), FadeIn(arrow), run_time=self.rt(.08))
        self.write_board(self.M('switch', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        rows = VGroup()
        for car, keep, swap in ((1, 'thắng', 'thua'), (2, 'thua', 'thắng'), (3, 'thua', 'thắng')):
            rows.add(VGroup(self.TM(f'xe ở cửa ${car}$:', 26, SOFT), tx(f'giữ {keep}', 26, GREEN if keep == 'thắng' else CORAL),
                            tx(f'đổi {swap}', 26, GREEN if swap == 'thắng' else CORAL, bold=True)).arrange(buff=.35))
        rows.arrange(DOWN, buff=.18)
        self.write_board(rows, anim='fade', frac=.25)

    def beat_s4(self, T):
        self.clear_board(.03)
        self.run_sim(switch_wins(), 'số ván:', 'đổi cửa thắng:', .7, y=-1.6)

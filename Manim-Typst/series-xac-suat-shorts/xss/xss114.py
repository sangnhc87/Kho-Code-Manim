"""XSS114 · Trò chơi Penney — "sấp – ngửa" trước "ngửa – ngửa" với xác suất 3/4 (chỉ thua khi 2 lần đầu đều ngửa)."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN  # noqa: E402
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS114', 'answer': '3/4'}
PROBLEM = ['Tung đồng xu liên tục. Cặp "sấp – ngửa"',
           '(SN) hay cặp "ngửa – ngửa" (NN) xuất',
           'hiện trước? $P("SN trước")$?']
OPTIONS = ['1/2', '3/4', '2/3']
CORRECT = 1
ANSWER_VALUE = .75
N, SEED = 2000, 7


def games():
    r, c, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        prev = r.random() < .5
        while True:
            cur = r.random() < .5  # True = ngửa
            if prev and cur:
                w = 0
                break
            if not prev and cur:
                w = 1
                break
            prev = cur
        c += w
        out.append(c / k)
    return out


def sn_first(seq):
    for a, b in zip(seq, seq[1:]):
        if (a, b) == ('S', 'N'):
            return True
        if (a, b) == ('N', 'N'):
            return False
    return None


BEATS = [
    Beat('hook', 'hook', 'Hai bạn cá cược: tung đồng xu liên tục, một bạn chọn cặp sấp ngửa, bạn kia chọn cặp ngửa ngửa. '
                         'Cặp nào xuất hiện trước thì thắng. Mỗi cặp đều có xác suất một phần tư, vậy công bằng chứ?'),
    Beat('guess', 'hook', 'Một phần hai, ba phần tư, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Để ý điều này: ngay khi một mặt sấp xuất hiện, ngửa ngửa không thể đến trước sấp ngửa nữa. '
                        'Vì muốn có hai ngửa liên tiếp, trước đó phải có một ngửa đứng ngay sau mặt sấp, tạo thành sấp ngửa trước.'),
    Beat('s2', 'solve', 'Vậy ngửa ngửa chỉ thắng khi hai lần tung đầu tiên đều ra ngửa, xác suất một phần tư. '
                        'Mọi trường hợp còn lại, sấp ngửa thắng: ba phần tư.'),
    Beat('s3', 'solve', 'Mô phỏng hai nghìn ván xác nhận: sấp ngửa thắng khoảng bảy mươi lăm phần trăm. '
                        'Hai cặp cùng xác suất xuất hiện, nhưng thứ tự xuất hiện lại không công bằng!'),
    Beat('answer', 'solve', 'Đáp án: ba phần tư. Đây là trò chơi Penney, nơi trực giác "cùng xác suất thì công bằng" bị đánh bại.'),
    Beat('outro', 'outro', outro_text(114)),
]

FORMULAS = formulas('3/4', OPTIONS,
                    lose='P("NN thắng") = P(N N " ở hai lần đầu") = 1/4',
                    win='P("SN thắng") = 1 - 1/4 = 3/4')


def validate() -> bool:
    seqs = [''.join(w) for w in product('SN', repeat=12)]
    res = [sn_first(s) for s in seqs]
    decided = [r for r in res if r is not None]
    assert abs(sum(decided) / len(seqs) - .75) < .001 and abs(games()[-1] - .75) < .003
    assert all(r is True for s, r in zip(seqs, res) if 'S' in s[:2] and r is not None)
    assert F(1, 4) == F(1, 2) ** 2
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS114(ShortScene):
    N = 114

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.seq = VGroup(*[coin(f, .45) for f in 'NSSN']).arrange(buff=.15).move_to([0, 1.8, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.seq, lag_ratio=.3), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.seq[1][0].animate.set_stroke(CYAN, 6), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(self.seq[2][0].animate.set_stroke(GREEN, 6), self.seq[3][0].animate.set_stroke(GREEN, 6), run_time=self.rt(.06))
        self.play(FadeIn(tx('có mặt sấp ⇒ SN chắc chắn thắng', 26, GREEN, bold=True).move_to([0, .6, 0])),
                  run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('lose', 1.5))
        self.wait_until(.5, t0)
        m = self.M('win', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.run_sim(games(), 'số ván:', 'SN thắng:', .45, y=-1.7)
        self.wait_until(.7, t0)
        self.write_board(tx('cùng xác suất ≠ công bằng', 28, CORAL, bold=True), anim='fade')



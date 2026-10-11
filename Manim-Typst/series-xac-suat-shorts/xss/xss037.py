"""XSS037 · Cược của de Méré (2) — đôi 6 trong 24 lần gieo hai xúc xắc: 1 − (35/36)²⁴ ≈ 0,491 < 1/2."""
from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS037', 'answer': '≈ 0,491 (thua!)'}
PROBLEM = ['Gieo hai con xúc xắc $24$ lần.', 'Xác suất có ít nhất một lần đôi $6$?']
OPTIONS = ['approx "0,518"', 'approx "0,491"', '2/3']
CORRECT = 1
ANSWER_VALUE = 1 - (35 / 36) ** 24
GAMES, SEED = 2000, 7


def wins():
    r, w, out = random.Random(SEED), 0, []
    for k in range(1, GAMES + 1):
        w += any(r.randint(1, 6) == 6 and r.randint(1, 6) == 6 for _ in range(24))
        out.append(w / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Thắng ván cược trước, de Méré nghĩ ra ván mới: gieo hai con xúc xắc hai mươi bốn lần, '
                         'cược có ít nhất một lần đôi sáu. Đôi sáu khó gấp sáu lần, nhưng gieo nhiều gấp sáu lần, '
                         'vậy vẫn có lợi? Ông bắt đầu thua!'),
    Beat('guess', 'hook', 'Khoảng không phẩy năm một tám, không phẩy bốn chín một, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biến cố đối: không lần nào ra đôi sáu. Mỗi lần gieo hai con, xác suất không phải đôi sáu là '
                        'ba mươi lăm phần ba mươi sáu.'),
    Beat('s2', 'solve', 'Hai mươi bốn lần độc lập: ba mươi lăm phần ba mươi sáu mũ hai mươi bốn, khoảng không phẩy năm '
                        'không chín. Xác suất thắng bằng một trừ số đó, khoảng không phẩy bốn chín một.'),
    Beat('s3', 'solve', 'Dưới một nửa! Mô phỏng hai nghìn ván xác nhận ông thua về lâu dài. Câu đố này được gửi tới '
                        'Pascal, và thư từ giữa Pascal với Fermat năm một sáu năm tư đã khai sinh lý thuyết xác suất.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy bốn chín một. Trực giác "nhân tỉ lệ" không dùng được cho xác suất!'),
    Beat('outro', 'outro', outro_text(37)),
]

FORMULAS = formulas('approx "0,491"', OPTIONS,
                    one='P("không đôi 6") = 35/36',
                    none='(35/36)^24 approx "0,509"',
                    prob='P = 1 - (35/36)^24 approx "0,491" < 1/2')


def validate() -> bool:
    p = 1 - Fraction(35, 36) ** 24
    assert round(float(p), 3) == .491 and round(float(Fraction(35, 36) ** 24), 3) == .509
    assert wins()[-1] < .5 and abs(wins()[-1] - float(p)) < .005
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS037(ShortScene):
    N = 37

    def hook_visual(self, t0):
        self.pair = VGroup(die(6, 1.4), die(6, 1.4)).arrange(buff=.5).move_to([0, 1.3, 0])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.pair, lag_ratio=.3), run_time=self.rt(.15))
        self.play(FadeIn(tx('× 24 lần', 40, GOLD, bold=True).next_to(self.pair, [0, -1, 0], buff=.3)),
                  run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('one', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('none', 1.9))
        self.wait_until(.55, t0)
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m, CORAL)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.02)
        self.run_sim(wins(), 'số ván:', 'tỉ lệ thắng:', .3, y=-1.6, color=CORAL)
        self.wait_until(.6, t0)
        self.write_board(tx('Pascal – Fermat, 1654', 28, SOFT, bold=True), anim='fade')

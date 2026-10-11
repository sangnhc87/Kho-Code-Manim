"""XSS120 · Nguyên tố cùng nhau — không cùng chia hết cho p với xác suất 1 − 1/p²; nhân qua mọi số nguyên tố: 6/π²."""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from manim import FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN, PANEL  # noqa: E402

EPISODE = {'code': 'XSS120', 'answer': '6/π² ≈ 0,608'}
PROBLEM = ['Chọn ngẫu nhiên hai số nguyên dương.', 'Xác suất chúng nguyên tố cùng nhau?']
OPTIONS = ['1/2', '6/pi^2 approx "0,608"', '3/4']
CORRECT = 1
ANSWER_VALUE = 6 / math.pi ** 2
N, SEED, G = 2000, 11, 24


def trials():
    r, c, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        c += math.gcd(r.randint(1, 10 ** 6), r.randint(1, 10 ** 6)) == 1
        out.append(c / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Chọn ngẫu nhiên hai số nguyên dương. Xác suất chúng nguyên tố cùng nhau, tức ước chung lớn nhất bằng một, '
                         'là bao nhiêu? Câu trả lời chứa số pi, dù chẳng có hình tròn nào!'),
    Beat('guess', 'hook', 'Một phần hai, sáu chia pi bình phương, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Trên lưới các cặp số, ô sáng là cặp nguyên tố cùng nhau. Hai số cùng chẵn với xác suất một phần tư, '
                        'cùng chia hết cho ba với xác suất một phần chín, và với số nguyên tố p là một trên p bình phương.'),
    Beat('s2', 'solve', 'Nguyên tố cùng nhau nghĩa là không cùng chia hết cho bất kỳ số nguyên tố nào. '
                        'Nhân các xác suất một trừ một trên p bình phương qua mọi số nguyên tố. '
                        'Euler chứng minh tích này bằng sáu chia pi bình phương.'),
    Beat('s3', 'solve', 'Mô phỏng hai nghìn cặp số ngẫu nhiên đến một triệu: tỉ lệ nguyên tố cùng nhau bám sát không phẩy sáu không tám.'),
    Beat('answer', 'solve', 'Đáp án: sáu chia pi bình phương, khoảng không phẩy sáu không tám. '
                            'Đây là thử thách mở rộng, nơi số học, xác suất và số pi gặp nhau!'),
    Beat('outro', 'outro', outro_text(120)),
]

FORMULAS = formulas('6/pi^2 approx "0,608"', OPTIONS,
                    p2='P(2 | a, space 2 | b) = 1/4, quad P(p | a, space p | b) = 1/p^2',
                    prod='P = (1 - 1/2^2)(1 - 1/3^2)(1 - 1/5^2) dots',
                    euler='P = 6/pi^2 approx "0,608"')


def validate() -> bool:
    primes = [p for p in range(2, 20000) if all(p % q for q in range(2, int(p ** .5) + 1))]
    prod = math.prod(1 - 1 / p ** 2 for p in primes)
    assert abs(prod - 6 / math.pi ** 2) < 1e-4
    assert abs(trials()[-1] - 6 / math.pi ** 2) < .003
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS120(ShortScene):
    N = 120

    def hook_visual(self, t0):
        self.board_top = -1.3
        s = .2
        self.cells = VGroup()
        for i in range(G):
            for j in range(G):
                ok = math.gcd(i + 1, j + 1) == 1
                self.cells.add(Square(side_length=s * .9, stroke_width=0, fill_color=CYAN if ok else PANEL,
                                      fill_opacity=.9 if ok else 1).move_to([(j - G / 2 + .5) * s, 1.15 - (i - G / 2 + .5) * s, 0]))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.cells, lag_ratio=.002), run_time=self.rt(.25))

    def beat_s1(self, T):
        t0 = self.now()
        even = [c for k, c in enumerate(self.cells) if (k // G + 1) % 2 == 0 and (k % G + 1) % 2 == 0]
        self.play(*[c.animate.set_fill(CORAL, .9) for c in even], run_time=self.rt(.08))
        self.wait_until(.4, t0)
        self.write_board(self.M('p2', 1.6))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('prod', 1.7))
        self.wait_until(.6, t0)
        m = self.M('euler', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.clear_board(.03)
        self.run_sim(trials(), 'số cặp:', 'nguyên tố cùng nhau:', .6, y=-1.9, color=GREEN)

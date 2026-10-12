"""XSS308 · Tổng dồn chạm đúng 6 — p_k = (p_(k−1) + … + p_(k−6))/6, p_k = (7/6)^(k−1)/6 với k ≤ 6: p_6 = 7⁵/6⁶ = 16807/46656."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS308', 'answer': '16807/46656 ≈ 0,36'}
PROBLEM = ['Gieo xúc xắc nhiều lần, cộng dồn',
           'số chấm. Xác suất tổng cộng dồn',
           'có lúc bằng đúng $6$?']
OPTIONS = ['1/6', '16807/46656 approx "0,36"', '2/7']
CORRECT = 1
ANSWER_VALUE = 16807 / 46656


def touch(n):
    p = [F(1)]
    for k in range(1, n + 1):
        p.append(sum(p[k - s] for s in range(1, 7) if k - s >= 0) / 6)
    return p


BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc liên tục và cộng dồn số chấm: ba, rồi bảy, rồi chín, và cứ thế. Xác suất tổng cộng dồn có lúc bằng đúng sáu là bao nhiêu? '
                         'Ra mặt sáu ngay lần đầu chỉ là một trong nhiều cách.'),
    Beat('guess', 'hook', 'Một phần sáu, khoảng không phẩy ba sáu, hay hai phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Như ếch nhảy, nhưng bước nhảy từ một đến sáu. p k bằng trung bình sáu giá trị p ngay trước: p một một phần sáu, p hai bảy phần ba mươi sáu.'),
    Beat('s2', 'solve', 'Với k từ một đến sáu, mỗi lần p nhân thêm bảy phần sáu: p k bằng một phần sáu nhân bảy phần sáu mũ k trừ một. '
                        'Nên p sáu bằng bảy mũ năm chia sáu mũ sáu.'),
    Beat('s3', 'solve', 'Bằng mười sáu nghìn tám trăm lẻ bảy phần bốn mươi sáu nghìn sáu trăm năm mươi sáu, khoảng ba mươi sáu phần trăm. '
                        'Với tổng rất lớn, xác suất tiến về hai phần bảy, nghịch đảo của mặt trung bình ba phẩy năm.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy ba sáu. Quy hoạch động đẹp đến mức cho ra công thức lũy thừa!'),
    Beat('outro', 'outro', outro_text(308)),
]

FORMULAS = formulas('16807/46656 approx "0,36"', OPTIONS,
                    rec='p_k = 1/6 (p_(k-1) + dots + p_(k-6))',
                    pk='p_k = 1/6 (7/6)^(k-1) quad (k <= 6)',
                    p6='p_6 = 7^5/6^6 = 16807/46656')


def validate() -> bool:
    p = touch(6)
    assert all(p[k] == F(1, 6) * F(7, 6) ** (k - 1) for k in range(1, 7))
    assert p[6] == F(16807, 46656)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS308(ShortScene):
    N = 308

    def hook_visual(self, t0):
        self.board_top = -1.25
        base, h = -.1, 2.8
        p = touch(12)
        self.bars = VGroup()
        for k in range(1, 13):
            r = Rectangle(width=.42, height=h * float(p[k]) / .4, stroke_width=0, fill_color=GOLD if k == 6 else CYAN, fill_opacity=.85)
            r.move_to([-3.1 + .56 * (k - 1), base + r.height / 2, 0])
            self.bars.add(r)
        self.axis = VGroup(*[self.TM(f'${k}$', 18, SOFT).next_to([-3.1 + .56 * (k - 1), base, 0], DOWN, buff=.06) for k in range(1, 13)])
        self.wait_until(.7, t0)
        self.play(FadeIn(self.axis), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('rec', 1.7))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[GrowFromEdge(b, DOWN) for b in self.bars], run_time=self.rt(.15))
        self.wait_until(.4, t0)
        self.clear_board(.03)
        self.write_board(self.M('pk', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('p6', 1.9)
        self.write_board(m)
        self.frame(m)

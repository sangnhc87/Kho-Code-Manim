"""XSS176 · Phương trình có nghiệm — b² ≥ 4c đếm theo từng b: 0 + 1 + 2 + 4 + 6 + 6 = 19 ô: 19/36."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD  # noqa: E402

EPISODE = {'code': 'XSS176', 'answer': '19/36'}
PROBLEM = ['Gieo xúc xắc $2$ lần được $b$ rồi',
           '$c$. Xác suất phương trình',
           '$x^2 + b x + c = 0$ có nghiệm?']
OPTIONS = ['1/2', '19/36', '17/36']
CORRECT = 1
ANSWER_VALUE = 19 / 36
TWO = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc hai lần, lần đầu được b, lần sau được c. Xác suất phương trình x bình phương cộng b x cộng c bằng không '
                         'có nghiệm là bao nhiêu? Câu này rất hay xuất hiện ở phần vận dụng.'),
    Beat('guess', 'hook', 'Một phần hai, mười chín phần ba mươi sáu, hay mười bảy phần ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Phương trình có nghiệm khi đenta không âm: b bình phương lớn hơn hoặc bằng bốn c. '
                        'Đếm theo từng giá trị của b.'),
    Beat('s2', 'solve', 'b bằng một: không có c nào. b bằng hai: c bằng một. b bằng ba: c bằng một, hai. b bằng bốn: c từ một đến bốn. '
                        'b bằng năm và sáu: cả sáu giá trị của c.'),
    Beat('s3', 'solve', 'Tổng: không cộng một cộng hai cộng bốn cộng sáu cộng sáu bằng mười chín ô. Xác suất mười chín phần ba mươi sáu.'),
    Beat('answer', 'solve', 'Đáp án: mười chín phần ba mươi sáu. Đếm theo từng cột của bảng là cách không sót, không trùng!'),
    Beat('outro', 'outro', outro_text(176)),
]

FORMULAS = formulas('19/36', OPTIONS,
                    cond='Delta = b^2 - 4 c >= 0 arrow.l.r.double c <= b^2/4',
                    cnt='0 + 1 + 2 + 4 + 6 + 6 = 19',
                    prob='P = 19/36')


def validate() -> bool:
    assert F(sum(b * b >= 4 * c for b, c in TWO), 36) == F(19, 36)
    assert [sum(b * b >= 4 * c for c in range(1, 7)) for b in range(1, 7)] == [0, 1, 2, 4, 6, 6]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS176(DiceGridMixin, ShortScene):
    N = 176

    def hook_visual(self, t0):
        self.wait_until(.55, t0)
        self.show_grid(.2, sums=False)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('cond', 1.8))

    def beat_s2(self, T):
        t0 = self.now()
        for b in range(1, 7):
            cells = [self.g.cells[c - 1][b - 1] for c in range(1, 7) if b * b >= 4 * c]
            self.wait_until(.08 + .14 * (b - 1), t0)
            if cells:
                self.play(*[c.animate.set_fill(GOLD, .75) for c in cells], run_time=self.rt(.04))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('cnt', 2.0))
        self.wait_until(.5, t0)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

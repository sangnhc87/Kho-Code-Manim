"""XSS098 · Tổng 7 hay tổng 8 về trước? — chỉ hai tổng này quyết định: 6/(6 + 5) = 6/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS098', 'answer': '6/11'}
PROBLEM = ['Gieo liên tục hai con xúc xắc. Xác suất',
           'tổng $7$ xuất hiện trước tổng $8$?']
OPTIONS = ['1/2', '6/11', '5/11']
CORRECT = 1
ANSWER_VALUE = 6 / 11
SPACE = list(product(range(1, 7), repeat=2))

BEATS = [
    Beat('hook', 'hook', 'Gieo liên tục hai con xúc xắc, mỗi lần cộng số chấm. Tổng bảy và tổng tám, tổng nào xuất hiện trước? '
                         'Xác suất tổng bảy về trước là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, sáu phần mười một, hay năm phần mười một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Những lần gieo ra tổng khác bảy và tám chẳng quyết định gì, chỉ là gieo lại. '
                        'Trò chơi kết thúc ngay lần đầu tiên ra một trong hai tổng đó.'),
    Beat('s2', 'solve', 'Trên bảng sáu nhân sáu: tổng bảy có sáu ô, tổng tám có năm ô. Mười một ô quyết định, đồng khả năng.'),
    Beat('s3', 'solve', 'Biết lần quyết định rơi vào mười một ô đó, xác suất là tổng bảy bằng sáu phần mười một. '
                        'Đây là xác suất có điều kiện đội lốt một trò chơi vô hạn bước!'),
    Beat('answer', 'solve', 'Đáp án: sáu phần mười một. Bỏ qua những gì không quan trọng, bài toán vô hạn hóa đơn giản.'),
    Beat('outro', 'outro', outro_text(98)),
]

FORMULAS = formulas('6/11', OPTIONS,
                    cnt='n(7) = 6, quad n(8) = 5',
                    prob='P = 6/(6 + 5) = 6/11')


def validate() -> bool:
    n7 = sum(sum(w) == 7 for w in SPACE)
    n8 = sum(sum(w) == 8 for w in SPACE)
    p7, p8 = F(n7, 36), F(n8, 36)
    series = sum((1 - p7 - p8) ** k * p7 for k in range(400))
    assert F(n7, n7 + n8) == F(6, 11) and abs(float(series) - 6 / 11) < 1e-12
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS098(DiceGridMixin, ShortScene):
    N = 98

    def hook_visual(self, t0):
        self.d1 = die(3, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(4, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(tx('tổng khác 7, 8: gieo lại', 32, CYAN, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[m.animate.set_opacity(0) for m in (self.d1, self.d2)], run_time=self.rt(.03))
        self.remove(self.d1, self.d2)
        self.show_grid(.2, sums=True)
        seven = [self.g.cells[6 - a][a - 1] for a in range(1, 7)]
        eight = [self.g.cells[8 - a - 1][a - 1] for a in range(2, 7)]
        rest = [c for row in self.g.cells for c in row if c not in seven and c not in eight]
        self.play(*[c.animate.set_fill(GOLD, .75) for c in seven], *[c.animate.set_fill(CORAL, .6) for c in eight],
                  *[c.animate.set_opacity(.15) for c in rest], run_time=self.rt(.12))
        self.wait_until(.65, t0)
        self.write_board(self.M('cnt', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)

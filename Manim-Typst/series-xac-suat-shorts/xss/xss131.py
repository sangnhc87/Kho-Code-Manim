"""XSS131 · Oẳn tù tì ba người — 27 kết quả; hòa khi cả ba giống nhau (3) hoặc đủ ba kiểu (6): 9/27 = 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS131', 'answer': '1/3'}
PROBLEM = ['Ba người oẳn tù tì (kéo, búa, bao)',
           'một lượt. Xác suất hòa (cả ba giống',
           'nhau hoặc đủ ba kiểu)?']
OPTIONS = ['1/9', '1/3', '2/9']
CORRECT = 1
ANSWER_VALUE = 1 / 3
OUTS = list(product('KBO', repeat=3))
COL = {'K': CYAN, 'B': CORAL, 'O': GOLD}

BEATS = [
    Beat('hook', 'hook', 'Ba bạn chơi oẳn tù tì: kéo, búa, bao. Ván hòa khi cả ba ra giống nhau, hoặc khi ra đủ cả ba kiểu, '
                         'vì khi đó ai cũng thắng một người và thua một người. Xác suất hòa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần chín, một phần ba, hay hai phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây ba tầng, mỗi tầng ba nhánh, cho ba mũ ba bằng hai mươi bảy kết quả đồng khả năng. '
                        'Thay vì vẽ cây, ta xếp hai mươi bảy bộ ba thành một bảng.'),
    Beat('s2', 'solve', 'Cả ba giống nhau: ba bộ. Đủ ba kiểu: mỗi cách xếp kéo, búa, bao cho ba người, ba giai thừa bằng sáu bộ.'),
    Beat('s3', 'solve', 'Tổng cộng chín kết quả hòa trên hai mươi bảy, bằng một phần ba. Nghĩa là cứ ba lượt thì có một lượt phải chơi lại!'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Đông người chơi oẳn tù tì thì rất hay hòa, bây giờ bạn đã biết vì sao!'),
    Beat('outro', 'outro', outro_text(131)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    n='n(Omega) = 3^3 = 27',
                    cnt='3 " (giống nhau)" + 3! " (đủ ba kiểu)" = 9',
                    prob='P = 9/27 = 1/3')


def validate() -> bool:
    assert F(sum(len(set(w)) != 2 for w in OUTS), 27) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS131(ShortScene):
    N = 131

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.cells = VGroup(*[VGroup(*[token(c, COL[c], .17, 16) for c in w]).arrange(buff=.03) for w in OUTS]) \
            .arrange_in_grid(9, 3, buff=(.45, .12)).move_to([0, 1.15, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.cells[:3], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.cells[3:], lag_ratio=.03), run_time=self.rt(.3))
        self.wait_until(.6, t0)
        self.write_board(self.M('n', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        same = [c for c, w in zip(self.cells, OUTS) if len(set(w)) == 1]
        diff = [c for c, w in zip(self.cells, OUTS) if len(set(w)) == 3]
        rest = [c for c, w in zip(self.cells, OUTS) if len(set(w)) == 2]
        self.play(*[c.animate.set_opacity(.15) for c in rest], run_time=self.rt(.06))
        self.play(*[c.animate.scale(1.15) for c in same], run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.play(*[c.animate.scale(1.15) for c in diff], *[c[0].animate.set_stroke(GREEN, 3) for c in diff],
                  run_time=self.rt(.06))
        self.write_board(self.M('cnt', 1.7))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)

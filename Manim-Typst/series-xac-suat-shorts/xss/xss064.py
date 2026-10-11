"""XSS064 · P(A|B) khác P(B|A) — bảng hai chiều: P(kính | nam) = 0,4 nhưng P(nam | kính) = 0,6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL_2, SOFT, STROKE, WHITE  # noqa: E402

EPISODE = {'code': 'XSS064', 'answer': '0,4 và 0,6'}
PROBLEM = ['$100$ học sinh: $60$ nam ($24$ đeo kính),',
           '$40$ nữ ($16$ đeo kính). Tính $P("kính" | "nam")$',
           'và $P("nam" | "kính")$.']
OPTIONS = ['"0,4" " và " "0,6"', '"0,6" " và " "0,4"', '"0,24" " và " "0,24"']
CORRECT = 0
ANSWER_VALUE = None
TABLE = {('nam', 'kính'): 24, ('nam', 'không'): 36, ('nữ', 'kính'): 16, ('nữ', 'không'): 24}

BEATS = [
    Beat('hook', 'hook', 'Một trường có sáu mươi học sinh nam, hai mươi tư bạn đeo kính, và bốn mươi học sinh nữ, '
                         'mười sáu bạn đeo kính. Xác suất đeo kính khi biết là nam, và xác suất là nam khi biết đeo kính, '
                         'có bằng nhau không?'),
    Beat('guess', 'hook', 'Không phẩy bốn và không phẩy sáu, ngược lại, hay bằng nhau? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xếp số liệu vào bảng hai chiều: hàng là nam và nữ, cột là đeo kính và không đeo kính.'),
    Beat('s2', 'solve', 'Biết là nam: chỉ nhìn hàng nam có sáu mươi bạn, trong đó hai mươi tư bạn đeo kính. '
                        'Xác suất bằng không phẩy bốn.'),
    Beat('s3', 'solve', 'Biết đeo kính: chỉ nhìn cột đeo kính có bốn mươi bạn, trong đó hai mươi tư bạn nam. '
                        'Xác suất bằng không phẩy sáu. Cùng con số hai mươi tư, nhưng chia cho hai cái khác nhau!'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bốn và không phẩy sáu. Đảo điều kiện là đổi mẫu số, đừng bao giờ nhầm!'),
    Beat('outro', 'outro', outro_text(64)),
]

FORMULAS = formulas('"0,4" " và " "0,6"', OPTIONS,
                    row='P("kính" | "nam") = 24/60 = "0,4"',
                    col='P("nam" | "kính") = 24/40 = "0,6"')


def validate() -> bool:
    nam = TABLE[('nam', 'kính')] + TABLE[('nam', 'không')]
    kinh = TABLE[('nam', 'kính')] + TABLE[('nữ', 'kính')]
    assert nam == 60 and kinh == 40 and sum(TABLE.values()) == 100
    assert F(24, nam) == F(2, 5) and F(24, kinh) == F(3, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS064(ShortScene):
    N = 64

    def hook_visual(self, t0):
        w, h = 1.85, .85
        cells = {}
        grid = VGroup()
        heads = [('', 'kính', 'không', 'tổng'), ('nam', 24, 36, 60), ('nữ', 16, 24, 40), ('tổng', 40, 60, 100)]
        for i, row in enumerate(heads):
            for j, val in enumerate(row):
                box = Rectangle(width=w, height=h, stroke_color=STROKE, stroke_width=2,
                                fill_color=PANEL_2, fill_opacity=1 if i and j else 0)
                box.move_to([(j - 1.5) * w, 2.3 - i * h, 0])
                lab = self.MNum(val, 0, WHITE if i < 3 and j < 3 else SOFT, 32) if isinstance(val, int) else \
                    tx(val, 26, SOFT, bold=True)
                cells[(i, j)] = VGroup(box, lab.move_to(box))
                grid.add(cells[(i, j)])
        self.cells = cells
        self.grid = grid
        self.wait_until(.6, t0)
        self.play(FadeIn(grid, lag_ratio=.03), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(*[self.cells[(i, j)][0].animate.set_stroke(SOFT, 3) for i in (1, 2) for j in (1, 2)], run_time=self.rt(.1))

    def beat_s2(self, T):
        t0 = self.now()
        row = VGroup(*[self.cells[(1, j)] for j in range(4)])
        frame = Rectangle(width=row.width + .1, height=row.height + .1, stroke_color=CYAN, stroke_width=6).move_to(row)
        self.play(FadeIn(frame), self.cells[(1, 1)][0].animate.set_fill(GOLD, .55), run_time=self.rt(.1))
        self.frame_row = frame
        self.wait_until(.5, t0)
        m = self.M('row', 1.9)
        self.write_board(m)
        self.frame(m, CYAN)

    def beat_s3(self, T):
        t0 = self.now()
        col = VGroup(*[self.cells[(i, 1)] for i in range(4)])
        frame = Rectangle(width=col.width + .1, height=col.height + .1, stroke_color=CORAL, stroke_width=6).move_to(col)
        self.play(FadeIn(frame), self.frame_row.animate.set_opacity(.3), run_time=self.rt(.1))
        self.wait_until(.45, t0)
        m = self.M('col', 1.9)
        self.write_board(m)
        self.frame(m, CORAL)

"""XSS118 · Galilei và ba xúc xắc — tổng 9 và tổng 10 đều có 6 cách phân tích, nhưng đếm thứ tự: 25 so với 27."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import DOWN, LEFT, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PANEL, SOFT  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS118', 'answer': 'Tổng 10 (27/216 so với 25/216)'}
PROBLEM = ['Gieo ba con xúc xắc.', 'Tổng $9$ hay tổng $10$ dễ xuất hiện hơn?']
OPTIONS = ['"Tổng 9"', '"Tổng 10"', '"Như nhau"']
CORRECT = 1
ANSWER_VALUE = None
THREE = list(product(range(1, 7), repeat=3))
PARTS9 = [(1, 2, 6), (1, 3, 5), (1, 4, 4), (2, 2, 5), (2, 3, 4), (3, 3, 3)]
PARTS10 = [(1, 3, 6), (1, 4, 5), (2, 2, 6), (2, 3, 5), (2, 4, 4), (3, 3, 4)]


def ways(t):
    return len(set(p for p in product(t, repeat=3) if sorted(p) == sorted(t)))


BEATS = [
    Beat('hook', 'hook', 'Thế kỷ mười bảy, các tay chơi xúc xắc ở Ý thắc mắc: gieo ba con xúc xắc, tổng chín và tổng mười '
                         'đều có sáu cách phân tích, vậy mà tổng mười lại ra nhiều hơn. Họ mang câu hỏi đến nhà khoa học Galilei.'),
    Beat('guess', 'hook', 'Tổng chín, tổng mười, hay như nhau? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đúng là mỗi tổng có sáu cách phân tích. Nhưng ba con xúc xắc là ba vật khác nhau, '
                        'nên phải đếm cả thứ tự. Ba số khác nhau cho sáu hoán vị, có hai số trùng cho ba, ba số trùng chỉ một.'),
    Beat('s2', 'solve', 'Tổng chín: sáu cộng sáu cộng ba cộng ba cộng sáu cộng một, bằng hai mươi lăm. '
                        'Tổng mười: sáu cộng sáu cộng ba cộng sáu cộng ba cộng ba, bằng hai mươi bảy. '
                        'Bộ ba ba ba của tổng chín chỉ có một cách, đó là chỗ thua thiệt.'),
    Beat('s3', 'solve', 'Trên hai trăm mười sáu kết quả đồng khả năng: tổng mười có xác suất hai mươi bảy phần hai trăm mười sáu, '
                        'lớn hơn hai mươi lăm phần hai trăm mười sáu của tổng chín.'),
    Beat('answer', 'solve', 'Đáp án: tổng mười. Bài học từ Galilei: đếm kết quả đồng khả năng, đừng đếm cách phân tích!'),
    Beat('outro', 'outro', outro_text(118)),
]

FORMULAS = formulas('"Tổng 10"', OPTIONS,
                    n9='n_9 = 6 + 6 + 3 + 3 + 6 + 1 = 25',
                    n10='n_10 = 6 + 6 + 3 + 6 + 3 + 3 = 27',
                    cmp='27/216 > 25/216')


def validate() -> bool:
    assert [sum(ways(t) for t in ps) for ps in (PARTS9, PARTS10)] == [25, 27]
    assert F(sum(sum(w) == 10 for w in THREE), 216) == F(27, 216)
    assert F(sum(sum(w) == 9 for w in THREE), 216) == F(25, 216)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS118(ShortScene):
    N = 118

    def column(self, parts, total, color):
        head = tx(f'tổng {total}', 30, color, bold=True)
        rows = VGroup(*[self.TM(f'${a} + {b} + {c}$', 26, SOFT) for a, b, c in parts]).arrange(DOWN, buff=.11)
        box = card(3.3, 3.55, color, PANEL, radius=.18, stroke_width=3)
        return VGroup(box, VGroup(head, rows).arrange(DOWN, buff=.18).move_to(box))

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.dice = VGroup(*[die(v, 1.1) for v in (3, 3, 4)]).arrange(buff=.4).move_to([0, 1.5, 0])
        self.wait_until(.25, t0)
        self.play(FadeIn(self.dice, lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.55, t0)
        self.play(self.dice.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.dice)
        self.cols = VGroup(self.column(PARTS9, 9, CYAN), self.column(PARTS10, 10, CORAL)).arrange(buff=.4) \
            .move_to([0, 1.65, 0])
        self.play(FadeIn(self.cols, lag_ratio=.3), run_time=self.rt(.12))

    def add_counts(self, col, parts, color):
        tags = VGroup(*[self.TM(f'$times {ways(t)}$', 26, color).next_to(r, [1, 0, 0], buff=.15)
                        for r, t in zip(col[1][1], parts)])
        self.play(*[r.animate.shift(LEFT * .35) for r in col[1][1]], run_time=self.rt(.04))
        for r, tg in zip(col[1][1], tags):
            tg.next_to(r, [1, 0, 0], buff=.15)
        self.play(FadeIn(tags, lag_ratio=.15), run_time=self.rt(.1))
        return tags

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.add_counts(self.cols[0], PARTS9, GOLD)

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('n9', 1.8))
        self.wait_until(.35, t0)
        self.add_counts(self.cols[1], PARTS10, GOLD)
        self.write_board(self.M('n10', 1.8))
        self.wait_until(.75, t0)
        self.play(self.cols[0][1][1][5].animate.set_color(CORAL), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('cmp', 2.3)
        self.write_board(m)
        self.frame(m)

"""XSS094 · Hộp của Bertrand — VV, BB, VB; rút được vàng: P(đồng còn lại vàng) = 2/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PANEL, SOFT, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS094', 'answer': '2/3'}
PROBLEM = ['$3$ hộp: hai đồng vàng; hai đồng bạc; một',
           'vàng một bạc. Chọn hộp, rút $1$ đồng được',
           'vàng. $P("đồng còn lại cũng vàng")$?']
OPTIONS = ['1/2', '2/3', '1/3']
CORRECT = 1
ANSWER_VALUE = 2 / 3
SILVER = '#C7D2DE'
BOXES = ('VV', 'BB', 'VB')

BEATS = [
    Beat('hook', 'hook', 'Nghịch lý của Bertrand: ba chiếc hộp, một hộp hai đồng vàng, một hộp hai đồng bạc, '
                         'một hộp một vàng một bạc. Chọn ngẫu nhiên một hộp, rút ra một đồng: màu vàng. '
                         'Xác suất đồng còn lại trong hộp cũng là vàng bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần ba, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lập luận phổ biến: rút được vàng thì loại hộp bạc bạc, còn hai hộp, nên một phần hai. '
                        'Nghe hợp lý nhưng sai!'),
    Beat('s2', 'solve', 'Hãy đếm theo từng đồng tiền. Có tất cả ba đồng vàng, mỗi đồng có cơ hội như nhau được rút ra. '
                        'Hai trong số đó nằm trong hộp vàng vàng.'),
    Beat('s3', 'solve', 'Nếu rút trúng một trong hai đồng của hộp vàng vàng, đồng còn lại cũng vàng. '
                        'Chỉ khi rút đồng vàng của hộp vàng bạc thì đồng còn lại là bạc. Xác suất bằng hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: hai phần ba. Hộp vàng vàng có gấp đôi cơ hội tạo ra đồng vàng, nên được tin gấp đôi.'),
    Beat('outro', 'outro', outro_text(94)),
]

FORMULAS = formulas('2/3', OPTIONS, prob='P = 2/3 quad ("2 trong 3 đồng vàng")')


def validate() -> bool:
    draws = [(box, i) for box in BOXES for i in range(2)]
    gold = [(b, i) for b, i in draws if b[i] == 'V']
    assert len(gold) == 3 and F(sum(b[1 - i] == 'V' for b, i in gold), 3) == F(2, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS094(ShortScene):
    N = 94

    def hook_visual(self, t0):
        self.boxes = VGroup()
        for b in BOXES:
            c = card(2.0, 1.4, STROKE, PANEL, radius=.2, stroke_width=3)
            coins = VGroup(*[token(' ', GOLD if ch == 'V' else SILVER, .38) for ch in b]).arrange(buff=.2).move_to(c)
            self.boxes.add(VGroup(c, coins))
        self.boxes.arrange(buff=.3).move_to([0, 1.5, 0])
        names = VGroup(*[tx(n, 22, SOFT).next_to(bx, DOWN, buff=.12) for n, bx in zip(('vàng – vàng', 'bạc – bạc', 'vàng – bạc'),
                                                                                     self.boxes)])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.boxes, lag_ratio=.3), FadeIn(names), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.boxes[1].animate.set_opacity(.25), FadeIn(cross(CORAL, .9).move_to(self.boxes[1])), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.write_board(self.TM('còn $2$ hộp $arrow.r 1/2$ ?', 32, CORAL, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        golds = [self.boxes[0][1][0], self.boxes[0][1][1], self.boxes[2][1][0]]
        for i, g in enumerate(golds):
            self.play(g.animate.scale(1.3), run_time=self.rt(.05))
            self.play(FadeIn(self.MNum(i + 1, 0, '#0B1221', 26).move_to(g)), run_time=self.rt(.03))
        self.wait_until(.6, t0)
        self.write_board(tx('3 đồng vàng, đồng khả năng', 30, GOLD, bold=True), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(self.boxes[0][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        m = self.M('prob', 2.0)
        self.write_board(m)
        self.frame(m)

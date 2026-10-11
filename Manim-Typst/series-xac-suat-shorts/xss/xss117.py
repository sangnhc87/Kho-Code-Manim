"""XSS117 · Xét nghiệm bao nhiêu lần? — mỗi lần dương tính nhân tỉ số bệnh/khỏe lên 0,99/0,05 = 19,8; cần 4 lần."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, UP, DashedLine, FadeIn, GrowFromEdge, Rectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS117', 'answer': '4'}
PROBLEM = ['Bệnh $1%$; xét nghiệm nhạy $99%$, dương tính', 'giả $5%$. Cần mấy lần dương tính liên tiếp',
           'để $P("bệnh") > 99%$?']
OPTIONS = ['2', '3', '4']
CORRECT = 2
ANSWER_VALUE = None
LR = F(99, 100) / F(5, 100)


def posterior(k):
    odds = F(1, 99) * LR ** k
    return odds / (1 + odds)


BEATS = [
    Beat('hook', 'hook', 'Một bệnh gặp ở một phần trăm dân số. Xét nghiệm phát hiện đúng chín mươi chín phần trăm người bệnh, '
                         'nhưng báo nhầm dương tính năm phần trăm người khỏe. Cần bao nhiêu lần dương tính liên tiếp '
                         'thì mới chắc trên chín mươi chín phần trăm là có bệnh?'),
    Beat('guess', 'hook', 'Hai lần, ba lần, hay bốn lần? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dùng tỉ số cược: xác suất bệnh chia xác suất khỏe. Ban đầu tỉ số là một trên chín mươi chín. '
                        'Mỗi lần dương tính, Bayes nhân tỉ số này với không phẩy chín chín chia không phẩy không năm, '
                        'bằng mười chín phẩy tám.'),
    Beat('s2', 'solve', 'Muốn xác suất bệnh vượt chín mươi chín phần trăm thì tỉ số phải vượt chín mươi chín. '
                        'Sau ba lần, tỉ số mới khoảng bảy mươi tám, xác suất chừng chín mươi tám phẩy bảy phần trăm, chưa đủ.'),
    Beat('s3', 'solve', 'Lần thứ tư đưa tỉ số lên hơn một nghìn năm trăm, xác suất vượt chín mươi chín phẩy chín phần trăm. '
                        'Nhìn các cột: lần một chỉ mười bảy phần trăm, rồi tám mươi, chín mươi tám phẩy bảy, và chín chín phẩy chín.'),
    Beat('answer', 'solve', 'Đáp án: bốn lần. Một kết quả dương tính chưa nói được gì nhiều, '
                            'nhưng bằng chứng lặp lại thì nhân lên rất nhanh!'),
    Beat('outro', 'outro', outro_text(117)),
]

FORMULAS = formulas('4', OPTIONS,
                    odds='O_0 = ("0,01")/("0,99") = 1/99',
                    lr='"0,99"/"0,05" = "19,8"',
                    cond='P > "0,99" arrow.l.r.double O > 99',
                    k3='O_3 = 1/99 dot "19,8"^3 approx "78,4" < 99',
                    k4='O_4 = 1/99 dot "19,8"^4 approx 1552 > 99')


def validate() -> bool:
    assert posterior(3) < F(99, 100) < posterior(4)
    assert abs(float(posterior(1)) - 1 / 6) < .001
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS117(ShortScene):
    N = 117

    def hook_visual(self, t0):
        self.board_top = -1.3
        base, top = -.6, 2.6
        self.bars = VGroup()
        self.labels = VGroup()
        for k in range(1, 5):
            p = float(posterior(k))
            x = -2.7 + (k - 1) * 1.8
            b = Rectangle(width=1.0, height=(top - base) * p, stroke_width=0,
                          fill_color=GREEN if p > .99 else (GOLD if p > .5 else CORAL), fill_opacity=.85)
            b.move_to([x, base + b.height / 2, 0])
            self.bars.add(b)
            self.labels.add(VGroup(VGroup(self.MNum(p * 100, 1, SOFT, 26), tx('%', 22, SOFT)).arrange(buff=.05)
                                   .next_to(b, UP, buff=.08),
                                   self.TM(f'$k = {k}$', 24, SOFT).next_to([x, base, 0], DOWN, buff=.12)))
        self.line = DashedLine([-3.4, base + (top - base) * .99, 0], [3.4, base + (top - base) * .99, 0],
                               color=CYAN, stroke_width=3)
        self.wait_until(.6, t0)
        self.play(FadeIn(self.line), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.write_board(self.M('odds', 1.9))
        self.wait_until(.55, t0)
        m = self.M('lr', 2.0)
        self.write_board(m)
        self.frame(m, CYAN)

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('cond', 1.9))
        self.wait_until(.45, t0)
        for i in range(3):
            self.play(GrowFromEdge(self.bars[i], DOWN), FadeIn(self.labels[i]), run_time=self.rt(.06))
        self.write_board(self.M('k3', 1.7))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(GrowFromEdge(self.bars[3], DOWN), FadeIn(self.labels[3]), run_time=self.rt(.08))
        m = self.M('k4', 1.7)
        self.write_board(m)
        self.frame(m, GREEN)
        self.wait_until(.5, t0)

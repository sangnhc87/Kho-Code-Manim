"""XSS033 · Đoán mật khẩu — 10³ = 1000 mật khẩu: 1/1000."""
from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS033', 'answer': '1/1000'}
PROBLEM = ['Ổ khóa có mật khẩu $3$ chữ số ($000$ – $999$).', 'Đoán một lần, xác suất mở được khóa?']
OPTIONS = ['1/27', '1/720', '1/1000']
CORRECT = 2
ANSWER_VALUE = .001

BEATS = [
    Beat('hook', 'hook', 'Một ổ khóa vali có mật khẩu ba chữ số, từ không không không đến chín chín chín. '
                         'Đoán bừa một lần, xác suất mở được khóa là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai mươi bảy, một phần bảy trăm hai mươi, hay một phần một nghìn? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mỗi bánh xe có mười chữ số, từ không đến chín, và các chữ số được phép lặp lại. '
                        'Theo quy tắc nhân: mười nhân mười nhân mười bằng một nghìn mật khẩu.'),
    Beat('s2', 'solve', 'Chỉ một mật khẩu đúng, nên xác suất bằng một phần một nghìn. Bảy trăm hai mươi là bẫy: '
                        'đó là số mật khẩu có ba chữ số khác nhau, nhưng mật khẩu thật được lặp chữ số.'),
    Beat('s3', 'solve', 'Thêm một chữ số nữa, xác suất giảm mười lần, còn một phần mười nghìn. '
                        'Đó là lý do mật khẩu càng dài càng an toàn.'),
    Beat('answer', 'solve', 'Đáp án: một phần một nghìn. Mỗi chữ số thêm vào giúp bạn an toàn gấp mười lần!'),
    Beat('outro', 'outro', outro_text(33)),
]

FORMULAS = formulas('1/1000', OPTIONS,
                    n='n(Omega) = 10 dot 10 dot 10 = 1000',
                    trap='10 dot 9 dot 8 = 720 quad coral("khác nhau")',
                    four='10^4 arrow.r 1/10000')


def validate() -> bool:
    assert len(list(product(range(10), repeat=3))) == 1000 and Fraction(1, 1000) == Fraction(1, 10 ** 3)
    assert 10 * 9 * 8 == 720
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS033(ShortScene):
    N = 33

    def wheels(self, digits):
        g = VGroup()
        for d in digits:
            c = card(1.3, 2.0, GOLD, PANEL, radius=.2, stroke_width=4)
            g.add(VGroup(c, self.MNum(d, 0, GOLD, 70).move_to(c)))
        return g.arrange(buff=.25).move_to([0, 1.3, 0])

    def hook_visual(self, t0):
        self.lock = self.wheels((0, 0, 0))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.lock, lag_ratio=.25), run_time=self.rt(.15))
        for digits in ((3, 8, 1), (7, 2, 9), (4, 4, 0)):
            new = self.wheels(digits)
            self.play(*[FadeIn(n) for n in new], *[m.animate.set_opacity(0) for m in self.lock], run_time=self.rt(.06))
            self.remove(self.lock)
            self.lock = new

    def beat_s1(self, T):
        t0 = self.now()
        tens = VGroup(*[self.TM('$10$ cách', 26, SOFT).next_to(w, [0, -1, 0], buff=.2) for w in self.lock])
        self.play(FadeIn(tens, lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.board_top = -1.0
        m = self.M('n', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.clear_board(.03)
        self.write_board(self.M('trap', 1.7), anim='fade')
        self.write_board(tx('mật khẩu được lặp chữ số!', 26, CORAL, bold=True), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.15, t0)
        self.write_board(self.M('four', 2.0))
        self.write_board(tx('dài hơn 1 chữ số → an toàn gấp 10 lần', 26, SOFT), anim='fade')



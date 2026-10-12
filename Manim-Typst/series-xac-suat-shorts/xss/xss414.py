"""XSS414 · Chuỗi dài là bình thường — dãy 20 lần không có 4 mặt giống liền: a_n = a_(n−1) + a_(n−2) + a_(n−3), a₁..₃ = 2, 4, 8 → a₂₀ = 242830; P = 1 − 242830/2²⁰ ≈ 0,768."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS414', 'answer': '≈ 0,768'}
PROBLEM = ['Tung đồng xu $20$ lần. Xác suất có ít nhất',
           '$4$ lần liên tiếp cùng một mặt?']
OPTIONS = ['approx "0,768"', 'approx "0,25"', 'approx "0,5"']
CORRECT = 0
ANSWER_VALUE = .768
SEQ = 'NSSNNSNNNNSNSSNSNSSN'


def no_run(n):
    a = [0, 2, 4, 8]
    for k in range(4, n + 1):
        a.append(a[k - 1] + a[k - 2] + a[k - 3])
    return a[n]


BEATS = [
    Beat('hook', 'hook', 'Nhờ hai bạn bịa ra hai mươi lần tung xu, và một bạn tung thật. Giáo viên thường đoán đúng ngay bạn nào tung thật. '
                         'Bí mật: xác suất có ít nhất bốn lần liên tiếp cùng mặt trong hai mươi lần tung là bao nhiêu?'),
    Beat('guess', 'hook', 'Khoảng không phẩy bảy sáu tám, không phẩy hai lăm, hay không phẩy năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đếm các dãy không có chuỗi bốn. Mỗi dãy tốt kết thúc bằng một chuỗi dài một, hai hoặc ba; bỏ chuỗi cuối đi ta được một dãy tốt ngắn hơn.'),
    Beat('s2', 'solve', 'Nên a n bằng a n trừ một cộng a n trừ hai cộng a n trừ ba, bắt đầu từ hai, bốn, tám. Tính đến n bằng hai mươi được hai trăm bốn mươi hai nghìn tám trăm ba mươi.'),
    Beat('s3', 'solve', 'Chia cho hai mũ hai mươi, khoảng không phẩy hai ba hai. Vậy xác suất có chuỗi bốn khoảng không phẩy bảy sáu tám.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy bảy sáu tám. Người bịa thường né chuỗi dài, nhưng ngẫu nhiên thật thì chuỗi dài rất thường gặp.'),
    Beat('outro', 'outro', outro_text(414)),
]

FORMULAS = formulas('approx "0,768"', OPTIONS,
                    rec='a_n = a_(n-1) + a_(n-2) + a_(n-3), quad 2, 4, 8, 14, 26, dots',
                    a20='a_20 = 242830',
                    prob='P = 1 - 242830/2^20 approx "0,768"')


def validate() -> bool:
    assert no_run(4) == 14 and no_run(20) == 242830
    assert abs(1 - 242830 / 2 ** 20 - .768) < .001
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS414(ShortScene):
    N = 414

    def hook_visual(self, t0):
        self.board_top = -1.3
        rows = VGroup(*[VGroup(*[coin(c, .2) for c in SEQ[i:i + 10]]).arrange(buff=.08) for i in (0, 10)])
        self.coins = rows.arrange([0, -1, 0], buff=.25).move_to([0, 1.5, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.coins, lag_ratio=.05), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(*[self.coins[0][i].animate.scale(1.3) for i in range(6, 10)], run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('rec', 1.25))
        self.wait_until(.6, t0)
        self.write_board(self.M('a20', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

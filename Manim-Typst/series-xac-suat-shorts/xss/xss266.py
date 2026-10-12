"""XSS266 · Trò craps — thắng ngay 8/36; điểm c: P(lặp c trước 7) = n(c)/(n(c) + 6): tổng 244/495 ≈ 0,493."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, DiceGridMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN  # noqa: E402

EPISODE = {'code': 'XSS266', 'answer': '244/495 ≈ 0,493'}
PROBLEM = ['Gieo $2$ xúc xắc: $7, 11$ thắng; $2, 3, 12$',
           'thua; khác thì gieo tiếp đến khi',
           'lặp lại số đó (thắng) hoặc ra $7$',
           '(thua). $P("thắng")$?']
OPTIONS = ['1/2', '244/495 approx "0,493"', '"0,47"']
CORRECT = 1
ANSWER_VALUE = 244 / 495
TWO = list(product(range(1, 7), repeat=2))


def n(s):
    return sum(sum(w) == s for w in TWO)


WIN = F(n(7) + n(11), 36) + sum(F(n(c), 36) * F(n(c), n(c) + n(7)) for c in (4, 5, 6, 8, 9, 10))

BEATS = [
    Beat('hook', 'hook', 'Trò craps nổi tiếng: gieo hai xúc xắc. Ra bảy hoặc mười một thì thắng ngay; ra hai, ba, mười hai thì thua ngay. '
                         'Ra số khác, số đó thành "điểm": gieo tiếp, lặp lại điểm trước thì thắng, ra bảy trước thì thua. Xác suất thắng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, khoảng không phẩy bốn chín ba, hay không phẩy bốn bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Thắng ngay: tổng bảy sáu ô, tổng mười một hai ô, tám phần ba mươi sáu. Điểm là c: các lần gieo khác c và bảy chỉ là gieo lại.'),
    Beat('s2', 'solve', 'Như thử thách tổng bảy hay tổng tám: xác suất lặp c trước bảy bằng số ô của c chia số ô của c cộng sáu. '
                        'Ví dụ điểm bốn: ba phần chín.'),
    Beat('s3', 'solve', 'Cộng thắng ngay với sáu nhánh điểm: hai trăm bốn mươi tư phần bốn trăm chín mươi lăm, khoảng bốn chín phẩy ba phần trăm. '
                        'Nhà cái có lợi thế nhỏ nhưng chắc chắn.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy bốn chín ba. Cây vô hạn được thu gọn nhờ xác suất có điều kiện ở mỗi nhánh điểm!'),
    Beat('outro', 'outro', outro_text(266)),
]

FORMULAS = formulas('244/495 approx "0,493"', OPTIONS,
                    now='P("thắng ngay") = (6 + 2)/36 = 8/36',
                    point='P("lặp " c " trước 7") = (n(c))/(n(c) + 6)',
                    tot='P = 8/36 + sum_c (n(c))/36 dot (n(c))/(n(c) + 6) = 244/495')


def validate() -> bool:
    assert WIN == F(244, 495)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS266(DiceGridMixin, ShortScene):
    N = 266

    def hook_visual(self, t0):
        self.wait_until(.75, t0)
        self.show_grid(.12, sums=True, center=(.1, .1))

    def beat_s1(self, T):
        t0 = self.now()
        c = self.g.cells
        win = [c[i][j] for i in range(6) for j in range(6) if i + j + 2 in (7, 11)]
        lose = [c[i][j] for i in range(6) for j in range(6) if i + j + 2 in (2, 3, 12)]
        self.play(*[x.animate.set_fill(GREEN, .7) for x in win], *[x.animate.set_fill(CORAL, .7) for x in lose], run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.write_board(self.M('now', 2.0))

    def beat_s2(self, T):
        t0 = self.now()
        c = self.g.cells
        four = [c[i][j] for i in range(6) for j in range(6) if i + j + 2 == 4]
        self.play(*[x.animate.set_fill(GOLD, .8) for x in four], run_time=self.rt(.05))
        self.wait_until(.3, t0)
        self.clear_board(.03)
        self.write_board(self.M('point', 1.9))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.4)
        self.write_board(m)
        self.frame(m)



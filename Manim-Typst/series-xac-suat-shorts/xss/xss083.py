"""XSS083 · Từ P(A|B) ra P(A ∪ B) — P(AB) = 0,4 · 0,3 = 0,12; P(A ∪ B) = 0,5 + 0,4 − 0,12 = 0,78."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import venn  # noqa: E402

EPISODE = {'code': 'XSS083', 'answer': '0,78'}
PROBLEM = ['$P(A) = "0,5"$, $P(B) = "0,4"$, $P(A|B) = "0,3"$.', 'Tính $P(A union B)$.']
OPTIONS = ['"0,9"', '"0,78"', '"0,12"']
CORRECT = 1
ANSWER_VALUE = .78

BEATS = [
    Beat('hook', 'hook', 'Cho xác suất A bằng không phẩy năm, xác suất B bằng không phẩy bốn, '
                         'và xác suất A khi biết B bằng không phẩy ba. Tính xác suất A hợp B. Dạng này rất hay gặp trong đề thi!'),
    Beat('guess', 'hook', 'Không phẩy chín, không phẩy bảy tám, hay không phẩy một hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Muốn dùng công thức cộng, cần phần chung A giao B. Từ công thức nhân: '
                        'xác suất A giao B bằng xác suất B nhân xác suất A khi biết B.'),
    Beat('s2', 'solve', 'Không phẩy bốn nhân không phẩy ba, bằng không phẩy một hai. Đây là diện tích phần giao nhau.'),
    Beat('s3', 'solve', 'Công thức cộng: không phẩy năm cộng không phẩy bốn trừ không phẩy một hai, bằng không phẩy bảy tám. '
                        'Hai công thức nối nhau: nhân để tìm giao, cộng để tìm hợp.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bảy tám. Có xác suất có điều kiện, hãy nghĩ ngay tới công thức nhân!'),
    Beat('outro', 'outro', outro_text(83)),
]

FORMULAS = formulas('"0,78"', OPTIONS,
                    mult='P(A B) = P(B) dot P(A|B) = "0,4" dot "0,3" = "0,12"',
                    add='P(A union B) = "0,5" + "0,4" - "0,12" = "0,78"')


def validate() -> bool:
    ab = F(4, 10) * F(3, 10)
    assert ab == F(12, 100) and F(5, 10) + F(4, 10) - ab == F(78, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS083(ShortScene):
    N = 83

    def hook_visual(self, t0):
        self.v = venn(1.45, 1.5, CYAN, CORAL, (0, 1.3))
        labs = VGroup(self.TM('$A$', 36, CYAN, bold=True).move_to(self.v.a.get_center() + [-.75, .9, 0]),
                      self.TM('$B$', 36, CORAL, bold=True).move_to(self.v.b.get_center() + [.75, .9, 0]))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.v), FadeIn(labs), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.v.both(GOLD, .7)), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(tx('cần phần giao A ∩ B', 30, GOLD, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.15, t0)
        self.write_board(self.M('mult', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        m = self.M('add', 1.5)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.65, t0)
        self.write_board(tx('nhân → giao, cộng → hợp', 28, SOFT), anim='fade')

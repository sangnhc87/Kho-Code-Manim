"""XSS078 · Lọc thư rác — Bayes: 0,4·0,3 / (0,4·0,3 + 0,6·0,03) = 20/23 ≈ 0,87."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import CountTreeMixin, PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS078', 'answer': '20/23 ≈ 0,87'}
PROBLEM = ['$40%$ thư là thư rác. Chữ "khuyến mãi"',
           'có trong $30%$ thư rác và $3%$ thư thường.',
           'Thư có chữ đó: $P("rác")$?']
OPTIONS = ['"0,3"', '"0,4"', '20/23 approx "0,87"']
CORRECT = 2
ANSWER_VALUE = 20 / 23

BEATS = [
    Beat('hook', 'hook', 'Hộp thư của bạn có bốn mươi phần trăm là thư rác. Chữ "khuyến mãi" xuất hiện trong ba mươi phần trăm '
                         'thư rác, nhưng chỉ trong ba phần trăm thư thường. Một thư mới có chữ "khuyến mãi". Xác suất nó là thư rác?'),
    Beat('guess', 'hook', 'Không phẩy ba, không phẩy bốn, hay khoảng không phẩy tám bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tưởng tượng một nghìn bức thư: bốn trăm thư rác và sáu trăm thư thường.'),
    Beat('s2', 'solve', 'Trong bốn trăm thư rác, ba mươi phần trăm có chữ khuyến mãi: một trăm hai mươi thư. '
                        'Trong sáu trăm thư thường, ba phần trăm: mười tám thư.'),
    Beat('s3', 'solve', 'Một trăm ba mươi tám thư có chữ khuyến mãi, một trăm hai mươi trong đó là rác. '
                        'Xác suất bằng một trăm hai mươi phần một trăm ba mươi tám, tức hai mươi phần hai mươi ba, khoảng tám mươi bảy phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi phần hai mươi ba. Các bộ lọc thư rác đầu tiên hoạt động đúng theo công thức Bayes này!'),
    Beat('outro', 'outro', outro_text(78)),
]

FORMULAS = formulas('20/23 approx "0,87"', OPTIONS,
                    tot='120 + 18 = 138',
                    bayes='P("rác" | "KM") = 120/138 = 20/23')


def validate() -> bool:
    p = F(4, 10) * F(3, 10) / (F(4, 10) * F(3, 10) + F(6, 10) * F(3, 100))
    assert p == F(20, 23) and round(float(p), 2) == .87
    assert 400 * F(3, 10) == 120 and 600 * F(3, 100) == 18
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS078(CountTreeMixin, ShortScene):
    N = 78

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.levels, self.nodes = self.count_tree(1000, [
            (400, CORAL, 'thư rác', [(120, GOLD, 'có KM', []), (280, SOFT, 'không', [])]),
            (600, CYAN, 'thư thường', [(18, GOLD, 'có KM', []), (582, SOFT, 'không', [])])],
            top=3.25, dy=1.55, width=6.9)

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.25))

    def beat_s2(self, T):
        t0 = self.now()
        half = len(self.levels[2]) // 2
        self.play(FadeIn(self.levels[2][:half]), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2][half:]), run_time=self.rt(.12))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('tot', 2.1))
        self.wait_until(.45, t0)
        self.clear_board(.03)
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m)
        self.write_board(tx('khoảng 87%', 30, CORAL, bold=True), anim='fade')

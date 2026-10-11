"""XSS070 · Dương tính có chắc bệnh? — 10 000 người: 99 dương tính thật / 594 dương tính = 1/6."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import CountTreeMixin, PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS070', 'answer': '1/6 ≈ 0,17'}
PROBLEM = ['Bệnh gặp ở $1%$ dân số. Xét nghiệm đúng',
           'với $99%$ người bệnh, báo nhầm dương tính',
           '$5%$ người khỏe. Dương tính thì $P("bệnh")$?']
OPTIONS = ['"0,99"', '"0,95"', '1/6 approx "0,17"']
CORRECT = 2
ANSWER_VALUE = 1 / 6

BEATS = [
    Beat('hook', 'hook', 'Một bệnh gặp ở một phần trăm dân số. Xét nghiệm phát hiện đúng chín mươi chín phần trăm người bệnh, '
                         'nhưng cũng báo nhầm dương tính cho năm phần trăm người khỏe. Bạn nhận kết quả dương tính. '
                         'Xác suất bạn thật sự mắc bệnh là bao nhiêu?'),
    Beat('guess', 'hook', 'Chín mươi chín phần trăm, chín mươi lăm phần trăm, hay chỉ khoảng một phần sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hãy tưởng tượng mười nghìn người cùng đi xét nghiệm. Một phần trăm, tức một trăm người, mắc bệnh. '
                        'Chín nghìn chín trăm người còn lại khỏe mạnh.'),
    Beat('s2', 'solve', 'Trong một trăm người bệnh, chín mươi chín người có kết quả dương tính. '
                        'Trong chín nghìn chín trăm người khỏe, năm phần trăm, tức bốn trăm chín mươi lăm người, '
                        'cũng bị báo dương tính nhầm.'),
    Beat('s3', 'solve', 'Tổng cộng năm trăm chín mươi tư người dương tính, nhưng chỉ chín mươi chín người thật sự có bệnh. '
                        'Xác suất bằng chín mươi chín phần năm trăm chín mươi tư, đúng bằng một phần sáu!'),
    Beat('answer', 'solve', 'Đáp án: một phần sáu, chỉ khoảng mười bảy phần trăm. Bệnh càng hiếm, '
                            'một lần dương tính càng cần xét nghiệm lại. Đây chính là công thức Bayes.'),
    Beat('outro', 'outro', outro_text(70)),
]

FORMULAS = formulas('1/6 approx "0,17"', OPTIONS,
                    pos='99 + 495 = 594',
                    bayes='P("bệnh" | +) = 99/594 = 1/6')


def validate() -> bool:
    sick, healthy = 100, 9900
    tp, fp = sick * F(99, 100), healthy * F(5, 100)
    assert (tp, fp) == (99, 495) and tp / (tp + fp) == F(1, 6)
    bayes = F(1, 100) * F(99, 100) / (F(1, 100) * F(99, 100) + F(99, 100) * F(5, 100))
    assert bayes == F(1, 6)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS070(CountTreeMixin, ShortScene):
    N = 70

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.levels, self.nodes = self.count_tree(10000, [
            (100, CORAL, 'bệnh', [(99, CORAL, 'dương tính', []), (1, SOFT, 'âm tính', [])]),
            (9900, GREEN, 'khỏe', [(495, GOLD, 'dương tính', []), (9405, SOFT, 'âm tính', [])])],
            top=3.25, dy=1.55, width=6.9)

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), run_time=self.rt(.12))
        self.wait_until(.35, t0)
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), run_time=self.rt(.12))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('pos', 2.1))
        self.wait_until(.5, t0)
        self.clear_board(.03)
        m = self.M('bayes', 2.0)
        self.write_board(m)
        self.frame(m)
        self.write_board(tx('chỉ khoảng 17%!', 30, CORAL, bold=True), anim='fade')

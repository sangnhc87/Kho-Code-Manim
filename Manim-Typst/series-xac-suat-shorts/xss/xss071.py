"""XSS071 · Xét nghiệm lần hai — từ 1/6, thêm một lần dương tính độc lập: ≈ 0,80."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS071', 'answer': '≈ 0,80'}
PROBLEM = ['Như thử thách #$070$: sau lần $1$ dương tính, $P("bệnh") = 1/6$.',
           'Xét nghiệm lần $2$ (độc lập) cũng dương tính. $P("bệnh")$?']
OPTIONS = ['"0,99"', 'approx "0,80"', '1/3']
CORRECT = 1
ANSWER_VALUE = .8
BRANCHES = [('B', CORAL, '1/6', [('+', GOLD, '"0,99"', [])]), ('K', GREEN, '5/6', [('+', GOLD, '"0,05"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Ở thử thách bảy mươi, sau một lần dương tính, xác suất mắc bệnh chỉ là một phần sáu. '
                         'Bạn đi xét nghiệm lần hai, độc lập, và lại dương tính. Bây giờ xác suất mắc bệnh là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy chín chín, khoảng không phẩy tám, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điểm mấu chốt: niềm tin mới bắt đầu từ kết quả cũ. Trước lần hai, xác suất bệnh là một phần sáu, '
                        'khỏe là năm phần sáu.'),
    Beat('s2', 'solve', 'Nhánh bệnh rồi dương tính: một phần sáu nhân không phẩy chín chín, khoảng không phẩy một sáu lăm. '
                        'Nhánh khỏe rồi dương tính nhầm: năm phần sáu nhân không phẩy không năm, khoảng không phẩy không bốn hai.'),
    Beat('s3', 'solve', 'Bayes: không phẩy một sáu lăm chia cho tổng hai nhánh, được khoảng không phẩy tám. '
                        'Một lần dương tính chưa nói lên nhiều, hai lần thì đáng lo thật sự.'),
    Beat('answer', 'solve', 'Đáp án: khoảng tám mươi phần trăm. Mỗi bằng chứng mới cập nhật lại niềm tin, đó là tư duy Bayes!'),
    Beat('outro', 'outro', outro_text(71)),
]

FORMULAS = formulas('approx "0,80"', OPTIONS,
                    s='1/6 dot "0,99" = "0,165"',
                    h='5/6 dot "0,05" approx "0,042"',
                    bayes='P = ("0,165")/("0,165" + "0,042") approx "0,80"')


def validate() -> bool:
    p = F(1, 6) * F(99, 100) / (F(1, 6) * F(99, 100) + F(5, 6) * F(5, 100))
    assert round(float(p), 2) == .80 and F(1, 6) * F(99, 100) == F(165, 1000)
    assert round(float(F(5, 6) * F(5, 100)), 3) == .042
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS071(TreeMixin, ShortScene):
    N = 71

    def hook_visual(self, t0):
        self.board_top = -.9
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.1), dy=1.6, width=5.0, root_label='sau lần 1')

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.2))
        self.play(FadeIn(tx('B: bệnh   K: khỏe', 24, SOFT).move_to([0, -.45, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))
        self.write_board(self.M('s', 1.9))
        self.wait_until(.55, t0)
        self.write_board(self.M('h', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('bayes', 1.8)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(tx('bằng chứng mới → cập nhật niềm tin', 26, GOLD, bold=True), anim='fade')

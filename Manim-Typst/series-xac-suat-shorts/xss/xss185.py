"""XSS185 · Gặp một bạn nam — Bayes: 0,45·0,6 / (0,45·0,6 + 0,55·0,3) = 18/29 ≈ 0,62."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS185', 'answer': '18/29 ≈ 0,62'}
PROBLEM = ['$45%$ học sinh thích bóng đá; trong số đó',
           '$60%$ là nam, nhóm còn lại $30%$ là nam. Gặp',
           'một bạn nam: xác suất thích bóng đá?']
OPTIONS = ['"0,45"', '18/29 approx "0,62"', '"0,6"']
CORRECT = 1
ANSWER_VALUE = 18 / 29
BRANCHES = [('BĐ', GOLD, '"0,45"', [('T', CYAN, '"0,6"', []), ('G', CORAL, '"0,4"', [])]),
            ('ko', SOFT, '"0,55"', [('T', CYAN, '"0,3"', []), ('G', CORAL, '"0,7"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Bốn mươi lăm phần trăm học sinh thích bóng đá. Trong nhóm thích bóng đá, sáu mươi phần trăm là nam; '
                         'nhóm còn lại chỉ ba mươi phần trăm là nam. Bạn gặp ngẫu nhiên một bạn nam. Xác suất bạn ấy thích bóng đá?'),
    Beat('guess', 'hook', 'Không phẩy bốn lăm, khoảng không phẩy sáu hai, hay không phẩy sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một là thích hay không thích bóng đá, tầng hai là nam hay nữ. Hai lá "nam" là hai đường dẫn tới thông tin ta biết.'),
    Beat('s2', 'solve', 'Thích bóng đá và nam: không phẩy bốn lăm nhân không phẩy sáu bằng không phẩy hai bảy. '
                        'Không thích và nam: không phẩy năm lăm nhân không phẩy ba bằng không phẩy một sáu lăm.'),
    Beat('s3', 'solve', 'Bayes: không phẩy hai bảy chia không phẩy bốn ba lăm, bằng mười tám phần hai mươi chín, '
                        'làm tròn đến hàng phần trăm là không phẩy sáu hai.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy sáu hai. Đề trả lời ngắn thường yêu cầu làm tròn, nhớ giữ phân số tới bước cuối!'),
    Beat('outro', 'outro', outro_text(185)),
]

FORMULAS = formulas('18/29 approx "0,62"', OPTIONS,
                    leaves='"0,45" dot "0,6" = "0,27", quad "0,55" dot "0,3" = "0,165"',
                    bayes='P("BĐ" | "nam") = ("0,27")/("0,435") = 18/29 approx "0,62"')


def validate() -> bool:
    assert F(27, 100) / (F(27, 100) + F(165, 1000)) == F(18, 29) and round(18 / 29, 2) == .62
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS185(TreeMixin, ShortScene):
    N = 185

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.7, width=6.8, root_label='học sinh')
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.35, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('BĐ: thích bóng đá   ko: không   T: nam   G: nữ', 20, SOFT).move_to([0, -1.2, 0])), run_time=self.rt(.04))
        boys = [n for n, path in self.leaves if path[-1][0] == 'T']
        girls = [n for n, path in self.leaves if path[-1][0] == 'G']
        self.play(*[n.animate.set_opacity(.15) for n in girls], *[n.animate.scale(1.3) for n in boys], run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('leaves', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.5)
        self.write_board(m)
        self.frame(m)

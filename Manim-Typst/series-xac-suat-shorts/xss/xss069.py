"""XSS069 · Truy nguồn phế phẩm — Bayes: P(II | lỗi) = 0,02 / 0,032 = 0,625."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, PURPLE, SOFT  # noqa: E402
from xss.xss068 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS069', 'answer': '0,625'}
PROBLEM = ['Xưởng I: $60%$ sản phẩm, $2%$ lỗi; xưởng II: $40%$, $5%$ lỗi.',
           'Biết sản phẩm bị lỗi. Xác suất nó từ xưởng II?']
OPTIONS = ['"0,4"', '"0,625"', '"0,05"']
CORRECT = 1
ANSWER_VALUE = .625

BEATS = [
    Beat('hook', 'hook', 'Cùng nhà máy hai xưởng như thử thách trước. Khách hàng gửi trả một sản phẩm lỗi. '
                         'Xác suất sản phẩm đó do xưởng hai làm ra là bao nhiêu? Xưởng hai chỉ làm bốn mươi phần trăm thôi mà!'),
    Beat('guess', 'hook', 'Không phẩy bốn, không phẩy sáu hai lăm, hay không phẩy không năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết sản phẩm lỗi, ta chỉ giữ hai nhánh lỗi: lỗi từ xưởng một không phẩy không một hai, '
                        'lỗi từ xưởng hai không phẩy không hai. Tổng là không phẩy không ba hai.'),
    Beat('s2', 'solve', 'Phần của xưởng hai trong tổng đó: không phẩy không hai chia không phẩy không ba hai, '
                        'bằng không phẩy sáu hai lăm. Đây là công thức Bayes.'),
    Beat('s3', 'solve', 'Xưởng hai làm ít hàng hơn, nhưng tỉ lệ lỗi cao gấp hai phẩy năm lần, '
                        'nên chiếm hơn sáu mươi phần trăm số hàng lỗi. Bayes giúp truy ngược nguyên nhân từ kết quả.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy sáu hai lăm. Bayes: lấy nhánh cần tìm chia cho tổng các nhánh cùng kết quả.'),
    Beat('outro', 'outro', outro_text(69)),
]

FORMULAS = formulas('"0,625"', OPTIONS,
                    tot='P(L) = "0,012" + "0,02" = "0,032"',
                    bayes='P("II" | L) = ("0,02")/("0,032") = "0,625"')


def validate() -> bool:
    lo = F(6, 10) * F(2, 100) + F(4, 10) * F(5, 100)
    assert F(4, 10) * F(5, 100) / lo == F(5, 8)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS069(TreeMixin, ShortScene):
    N = 69

    def hook_visual(self, t0):
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='sản phẩm')
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[1][0].animate.set_opacity(.2), self.leaves[3][0].animate.set_opacity(.2),
                  self.leaves[0][0].animate.scale(1.3), self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.write_board(self.M('tot', 1.9))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[2][0][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.clear_board(.03)
        m = self.M('bayes', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.write_board(tx('tỉ lệ lỗi cao gấp 2,5 lần', 28, PURPLE, bold=True), anim='fade')
        self.write_board(tx('Bayes: từ kết quả truy ngược nguyên nhân', 24, SOFT), anim='fade')

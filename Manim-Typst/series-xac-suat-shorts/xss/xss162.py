"""XSS162 · Muộn vì xe buýt? — Bayes: 0,04/0,07 = 4/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD  # noqa: E402
from xss.xss161 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS162', 'answer': '4/7'}
PROBLEM = ['$40%$ đi buýt (muộn $10%$), $60%$ tự đi',
           '(muộn $5%$). Biết một bạn đi muộn.',
           'Xác suất bạn đó đi xe buýt?']
OPTIONS = ['"0,4"', '4/7', '1/2']
CORRECT = 1
ANSWER_VALUE = 4 / 7

BEATS = [
    Beat('hook', 'hook', 'Vẫn trường học đó: bốn mươi phần trăm đi xe buýt và muộn mười phần trăm, sáu mươi phần trăm tự đi và muộn năm phần trăm. '
                         'Thầy giám thị bắt được một bạn đi muộn. Xác suất bạn ấy đi xe buýt là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bốn, bốn phần bảy, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Biết đi muộn, ta chỉ giữ lại hai lá "muộn": nhánh xe buýt không phẩy không bốn và nhánh tự đi không phẩy không ba. '
                        'Tổng là không phẩy không bảy, xác suất toàn phần ở thử thách trước.'),
    Beat('s2', 'solve', 'Công thức Bayes: phần của nhánh xe buýt trên tổng, không phẩy không bốn chia không phẩy không bảy, bằng bốn phần bảy.'),
    Beat('s3', 'solve', 'Trước khi biết, khả năng đi buýt là bốn mươi phần trăm. Biết bạn đi muộn, nó tăng lên khoảng năm mươi bảy phần trăm, '
                        'vì xe buýt hay gây muộn hơn.'),
    Beat('answer', 'solve', 'Đáp án: bốn phần bảy. Toàn phần đi xuôi từ nguyên nhân tới kết quả, Bayes đi ngược từ kết quả về nguyên nhân!'),
    Beat('outro', 'outro', outro_text(162)),
]

FORMULAS = formulas('4/7', OPTIONS,
                    bayes='P(B u | M) = ("0,04")/("0,07") = 4/7')


def validate() -> bool:
    assert F(4, 100) / F(7, 100) == F(4, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS162(TreeMixin, ShortScene):
    N = 162

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='học sinh')
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.leaves[1][0].animate.set_opacity(.15), self.leaves[3][0].animate.set_opacity(.15),
                  self.leaves[0][0].animate.scale(1.3), self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.TM('$"0,04"$ và $"0,03"$, tổng $"0,07"$', 28, GOLD), anim='fade')

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('$40%$ → $57%$', 30, CORAL, bold=True), anim='fade')



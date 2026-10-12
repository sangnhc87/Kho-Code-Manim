"""XSS263 · Đài báo nhầm bao nhiêu? — 0,27/(0,27 + 0,7x) = 0,72 ⇒ x = 0,15."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS263', 'answer': '0,15'}
PROBLEM = ['Mưa $30%$ số ngày; trời mưa thì đài báo',
           'mưa $90%$. Biết $P("mưa" | "báo mưa") = "0,72"$.',
           'Tìm tỉ lệ báo mưa khi trời tạnh.']
OPTIONS = ['"0,1"', '"0,15"', '"0,28"']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('M', CYAN, '"0,3"', [('bm', GOLD, '"0,9"', [])]),
            ('T', CORAL, '"0,7"', [('bm', GOLD, 'x', [])])]

BEATS = [
    Beat('hook', 'hook', 'Ba mươi phần trăm số ngày có mưa. Trời mưa thì đài báo trước có mưa chín mươi phần trăm. '
                         'Thống kê: khi đài báo mưa thì bảy mươi hai phần trăm trời mưa thật. Đài báo mưa nhầm vào ngày tạnh bao nhiêu phần trăm?'),
    Beat('guess', 'hook', 'Không phẩy một, không phẩy một lăm, hay không phẩy hai tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đặt x là tỉ lệ báo mưa khi trời tạnh. Hai lá "báo mưa": mưa thật, không phẩy hai bảy; trời tạnh, không phẩy bảy x.'),
    Beat('s2', 'solve', 'Bayes: không phẩy hai bảy chia không phẩy hai bảy cộng không phẩy bảy x bằng không phẩy bảy hai. '
                        'Nghịch đảo: một cộng không phẩy bảy x chia không phẩy hai bảy bằng một trên không phẩy bảy hai.'),
    Beat('s3', 'solve', 'Giải ra không phẩy bảy x bằng không phẩy một không năm, x bằng không phẩy một lăm, tức mười lăm phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy một lăm. Bayes ngược tìm tỉ lệ sai: đặt ẩn ở nhánh còn thiếu!'),
    Beat('outro', 'outro', outro_text(263)),
]

FORMULAS = formulas('"0,15"', OPTIONS,
                    eq='("0,27")/("0,27" + "0,7" x) = "0,72"',
                    sol='"0,7" x = "0,27"/"0,72" - "0,27" = "0,105" arrow.r.double x = "0,15"')


def validate() -> bool:
    sols = [F(k, 100) for k in range(101) if F(27, 100) / (F(27, 100) + F(7, 10) * F(k, 100)) == F(72, 100)]
    assert sols == [F(3, 20)]
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS263(TreeMixin, ShortScene):
    N = 263

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='thời tiết')
        self.wait_until(.8, t0)
        self.play(*[FadeIn(lv, lag_ratio=.3) for lv in self.levels], run_time=self.rt(.1))

    def beat_s1(self, T):
        self.play(*[n.animate.scale(1.3) for n, _ in self.leaves], run_time=self.rt(.05))

    def beat_s2(self, T):
        m = self.M('eq', 1.9)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        m = self.M('sol', 1.3)
        self.write_board(m)
        self.frame(m)

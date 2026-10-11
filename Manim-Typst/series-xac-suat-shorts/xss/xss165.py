"""XSS165 · Dự báo có mưa — 0,2·0,9 / (0,2·0,9 + 0,8·0,3) = 0,18/0,42 = 3/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS165', 'answer': '3/7'}
PROBLEM = ['Ngày mưa $20%$. Trời mưa thì đài báo',
           'mưa $90%$, trời tạnh vẫn báo mưa $30%$.',
           'Đài báo mưa: xác suất mưa?']
OPTIONS = ['"0,9"', '3/7', '"0,2"']
CORRECT = 1
ANSWER_VALUE = 3 / 7
BRANCHES = [('M', CYAN, '"0,2"', [('bm', GOLD, '"0,9"', []), ('bt', SOFT, '"0,1"', [])]),
            ('T', CORAL, '"0,8"', [('bm', GOLD, '"0,3"', []), ('bt', SOFT, '"0,7"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Ở một thành phố, hai mươi phần trăm số ngày có mưa. Hôm trời mưa, đài báo trước có mưa chín mươi phần trăm; '
                         'hôm trời tạnh, đài vẫn báo mưa ba mươi phần trăm. Đài vừa báo mưa. Xác suất ngày mai mưa thật?'),
    Beat('guess', 'hook', 'Không phẩy chín, ba phần bảy, hay không phẩy hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây: tầng một là thời tiết thật, tầng hai là đài báo gì. Lá "báo mưa" xuất hiện ở cả hai nhánh.'),
    Beat('s2', 'solve', 'Mưa và báo mưa: không phẩy hai nhân không phẩy chín bằng không phẩy một tám. '
                        'Tạnh mà vẫn báo mưa: không phẩy tám nhân không phẩy ba bằng không phẩy hai bốn, còn lớn hơn!'),
    Beat('s3', 'solve', 'Bayes: không phẩy một tám chia không phẩy bốn hai, bằng ba phần bảy, chưa tới năm mươi phần trăm. '
                        'Lý do: ngày tạnh nhiều gấp bốn ngày mưa.'),
    Beat('answer', 'solve', 'Đáp án: ba phần bảy. Một dự báo "khá chính xác" vẫn có thể sai nhiều khi sự kiện hiếm!'),
    Beat('outro', 'outro', outro_text(165)),
]

FORMULAS = formulas('3/7', OPTIONS,
                    rain='"0,2" dot "0,9" = "0,18"',
                    dry='"0,8" dot "0,3" = "0,24"',
                    bayes='P(M | "báo mưa") = ("0,18")/("0,18" + "0,24") = 3/7')


def validate() -> bool:
    assert F(18, 100) / (F(18, 100) + F(24, 100)) == F(3, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS165(TreeMixin, ShortScene):
    N = 165

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='thời tiết')
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('M: mưa   T: tạnh   bm: báo mưa   bt: báo tạnh', 20, SOFT).move_to([0, -1.15, 0])),
                  run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        bm = [n for n, path in self.leaves if path[-1][0] == 'bm']
        other = [n for n, path in self.leaves if path[-1][0] != 'bm']
        self.play(*[n.animate.set_opacity(.15) for n in other], *[n.animate.scale(1.3) for n in bm], run_time=self.rt(.06))
        self.write_board(self.M('rain', 2.0))
        self.wait_until(.5, t0)
        self.write_board(self.M('dry', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.7)
        self.write_board(m)
        self.frame(m)

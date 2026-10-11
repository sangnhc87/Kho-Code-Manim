"""XSS164 · Biết hay đoán mò? — 0,6 / (0,6 + 0,4·1/4) = 6/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS164', 'answer': '6/7'}
PROBLEM = ['Học sinh biết đáp án với xác suất $"0,6"$,',
           'không biết thì đoán $1$ trong $4$. Trả lời',
           'đúng: xác suất thật sự biết?']
OPTIONS = ['"0,6"', '6/7', '"0,7"']
CORRECT = 1
ANSWER_VALUE = 6 / 7
BRANCHES = [('B', GREEN, '"0,6"', [('Đ', GOLD, '1', [])]),
            ('Ko', CORAL, '"0,4"', [('Đ', GOLD, '1/4', []), ('S', SOFT, '3/4', [])])]

BEATS = [
    Beat('hook', 'hook', 'Câu trắc nghiệm bốn phương án. Một học sinh biết đáp án với xác suất không phẩy sáu, '
                         'không biết thì đoán bừa. Bạn ấy trả lời đúng. Xác suất bạn ấy thật sự biết là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy sáu, sáu phần bảy, hay không phẩy bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây hai nhánh: biết, thì chắc chắn đúng; không biết, thì đúng với xác suất một phần tư.'),
    Beat('s2', 'solve', 'Hai lá "đúng": biết rồi đúng, không phẩy sáu; đoán mò mà đúng, không phẩy bốn nhân một phần tư bằng không phẩy một. '
                        'Xác suất trả lời đúng là không phẩy bảy.'),
    Beat('s3', 'solve', 'Bayes: không phẩy sáu chia không phẩy bảy, bằng sáu phần bảy. Vẫn còn một phần bảy khả năng câu đúng đó chỉ là may mắn!'),
    Beat('answer', 'solve', 'Đáp án: sáu phần bảy. Vì vậy đề thi trắc nghiệm luôn cần nhiều câu, để may mắn không quyết định điểm số!'),
    Beat('outro', 'outro', outro_text(164)),
]

FORMULAS = formulas('6/7', OPTIONS,
                    tot='P("đúng") = "0,6" + "0,4" dot 1/4 = "0,7"',
                    bayes='P("biết" | "đúng") = ("0,6")/("0,7") = 6/7')


def validate() -> bool:
    assert F(3, 5) / (F(3, 5) + F(2, 5) * F(1, 4)) == F(6, 7)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS164(TreeMixin, ShortScene):
    N = 164

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.4, root_label='học sinh')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.12))
        self.play(FadeIn(tx('B: biết   Ko: không biết   Đ: đúng   S: sai', 20, SOFT).move_to([0, -1.15, 0])),
                  run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        right = [n for n, path in self.leaves if path[-1][0] == 'Đ']
        self.play(*[n.animate.scale(1.3) for n in right], self.leaves[2][0].animate.set_opacity(.15), run_time=self.rt(.06))
        self.wait_until(.5, t0)
        self.write_board(self.M('tot', 1.8))

    def beat_s3(self, T):
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m)



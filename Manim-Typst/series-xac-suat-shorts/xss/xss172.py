"""XSS172 · Súng tốt hay súng thường? — 3/5·0,9 / (3/5·0,9 + 2/5·0,6) = 0,54/0,78 = 9/13."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS172', 'answer': '9/13'}
PROBLEM = ['Có $3$ súng tốt (trúng $"0,9"$) và $2$ súng',
           'thường (trúng $"0,6"$). Chọn $1$ súng bắn,',
           'trúng. Xác suất súng tốt?']
OPTIONS = ['3/5', '9/13', '"0,9"']
CORRECT = 1
ANSWER_VALUE = 9 / 13
BRANCHES = [('tốt', CYAN, '3/5', [('T', GREEN, '"0,9"', []), ('X', SOFT, '"0,1"', [])]),
            ('th', GOLD, '2/5', [('T', GREEN, '"0,6"', []), ('X', SOFT, '"0,4"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Kho có năm khẩu súng: ba khẩu tốt bắn trúng với xác suất không phẩy chín, hai khẩu thường chỉ không phẩy sáu. '
                         'Xạ thủ chọn ngẫu nhiên một khẩu, bắn một phát và trúng. Xác suất đó là súng tốt?'),
    Beat('guess', 'hook', 'Ba phần năm, chín phần mười ba, hay không phẩy chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây: chọn súng tốt ba phần năm, súng thường hai phần năm; rồi trúng hay trượt.'),
    Beat('s2', 'solve', 'Hai lá "trúng": súng tốt, ba phần năm nhân không phẩy chín bằng không phẩy năm bốn; '
                        'súng thường, hai phần năm nhân không phẩy sáu bằng không phẩy hai bốn. Tổng không phẩy bảy tám.'),
    Beat('s3', 'solve', 'Bayes: không phẩy năm bốn chia không phẩy bảy tám bằng chín phần mười ba. '
                        'Phát trúng làm niềm tin vào súng tốt tăng từ sáu mươi lên khoảng sáu mươi chín phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười ba. Thử thách tiếp theo: dùng lại khẩu súng đó bắn phát thứ hai thì sao?'),
    Beat('outro', 'outro', outro_text(172)),
]

FORMULAS = formulas('9/13', OPTIONS,
                    leaves='3/5 dot "0,9" = "0,54", quad 2/5 dot "0,6" = "0,24"',
                    bayes='P("tốt" | T) = ("0,54")/("0,78") = 9/13')


def validate() -> bool:
    assert F(54, 100) / F(78, 100) == F(9, 13)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS172(TreeMixin, ShortScene):
    N = 172

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='chọn súng')
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.2))
        self.play(FadeIn(tx('th: thường   T: trúng   X: trượt', 22, SOFT).move_to([0, -1.2, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        hit = [n for n, path in self.leaves if path[-1][0] == 'T']
        miss = [n for n, path in self.leaves if path[-1][0] == 'X']
        self.play(*[n.animate.set_opacity(.15) for n in miss], *[n.animate.scale(1.3) for n in hit], run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.write_board(self.M('leaves', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('bayes', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.TM('$60%$ → $69%$', 28, CORAL, bold=True), anim='fade')

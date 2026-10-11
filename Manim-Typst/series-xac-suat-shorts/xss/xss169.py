"""XSS169 · Tín hiệu bị nhiễu — gửi 1 (0,3), lật 10 %: P(gửi 1 | nhận 1) = 0,27/0,34 = 27/34."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS169', 'answer': '27/34'}
PROBLEM = ['Gửi bit $1$ với xác suất $"0,3"$, bit $0$ với',
           '$"0,7"$; mỗi bit bị lật với xác suất $"0,1"$.',
           'Nhận được $1$: xác suất đã gửi $1$?']
OPTIONS = ['"0,9"', '27/34', '"0,3"']
CORRECT = 1
ANSWER_VALUE = 27 / 34
BRANCHES = [('1', GOLD, '"0,3"', [('1', GOLD, '"0,9"', []), ('0', SOFT, '"0,1"', [])]),
            ('0', CYAN, '"0,7"', [('1', GOLD, '"0,1"', []), ('0', SOFT, '"0,9"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Một thiết bị gửi bit một với xác suất không phẩy ba, bit không với xác suất không phẩy bảy. '
                         'Đường truyền nhiễu làm lật bit với xác suất mười phần trăm. Máy nhận được bit một. '
                         'Xác suất bit gửi đi thật sự là một?'),
    Beat('guess', 'hook', 'Không phẩy chín, hai mươi bảy phần ba mươi tư, hay không phẩy ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây: tầng một là bit gửi, tầng hai là bit nhận. Bit được giữ nguyên chín mươi phần trăm, bị lật mười phần trăm.'),
    Beat('s2', 'solve', 'Nhận một có hai đường: gửi một, giữ nguyên, không phẩy hai bảy; gửi không mà bị lật, không phẩy không bảy.'),
    Beat('s3', 'solve', 'Bayes: không phẩy hai bảy chia không phẩy ba bốn, bằng hai mươi bảy phần ba mươi tư, khoảng bảy mươi chín phần trăm. '
                        'Đường truyền đúng chín mươi phần trăm, nhưng bit một hiếm hơn nên độ tin cậy giảm.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi bảy phần ba mươi tư. Thử thách tiếp: gửi mỗi bit hai lần thì sao?'),
    Beat('outro', 'outro', outro_text(169)),
]

FORMULAS = formulas('27/34', OPTIONS,
                    paths='"0,3" dot "0,9" = "0,27", quad "0,7" dot "0,1" = "0,07"',
                    bayes='P(1 | "nhận" 1) = ("0,27")/("0,34") = 27/34')


def validate() -> bool:
    assert F(27, 100) / (F(27, 100) + F(7, 100)) == F(27, 34)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS169(TreeMixin, ShortScene):
    N = 169

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='bit gửi')
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('tầng 2: bit nhận', 22, SOFT).move_to([0, -1.2, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        ones = [n for n, path in self.leaves if path[-1][0] == '1']
        zeros = [n for n, path in self.leaves if path[-1][0] == '0']
        self.play(*[n.animate.set_opacity(.15) for n in zeros], *[n.animate.scale(1.3) for n in ones], run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.write_board(self.M('paths', 1.6))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('bayes', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('bit 1 hiếm hơn → kém tin cậy hơn', 24, CORAL), anim='fade')

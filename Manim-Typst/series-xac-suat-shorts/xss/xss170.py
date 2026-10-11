"""XSS170 · Gửi lặp hai lần — nhận "1 1": 0,3·0,81 / (0,3·0,81 + 0,7·0,01) = 243/250 = 0,972."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS170', 'answer': '243/250 = 0,972'}
PROBLEM = ['Như thử thách trước, nhưng mỗi bit được',
           'gửi $2$ lần (mỗi lần lật $"0,1"$, độc lập);',
           'nhận "$1$ $1$". Xác suất đã gửi $1$?']
OPTIONS = ['27/34', '243/250 = "0,972"', '"0,81"']
CORRECT = 1
ANSWER_VALUE = .972
BRANCHES = [('1', GOLD, '"0,3"', [('11', GREEN, '"0,9"^2', []), ('khác', SOFT, '"0,19"', [])]),
            ('0', CYAN, '"0,7"', [('11', GREEN, '"0,1"^2', []), ('khác', SOFT, '"0,99"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Cải tiến: mỗi bit được gửi hai lần, mỗi lần bị lật độc lập với xác suất mười phần trăm. Máy nhận được một rồi một. '
                         'Bây giờ xác suất bit gửi đi là một tăng lên bao nhiêu?'),
    Beat('guess', 'hook', 'Hai mươi bảy phần ba mươi tư, hai trăm bốn mươi ba phần hai trăm năm mươi, hay không phẩy tám mốt? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gửi một: nhận một một khi cả hai lần đều giữ nguyên, không phẩy chín bình phương bằng không phẩy tám mốt. '
                        'Gửi không: nhận một một khi cả hai lần đều bị lật, chỉ không phẩy không một.'),
    Beat('s2', 'solve', 'Hai lá phù hợp: không phẩy ba nhân không phẩy tám mốt bằng không phẩy hai bốn ba; '
                        'không phẩy bảy nhân không phẩy không một bằng không phẩy không không bảy.'),
    Beat('s3', 'solve', 'Bayes: không phẩy hai bốn ba chia không phẩy hai năm, bằng không phẩy chín bảy hai. '
                        'Chỉ lặp lại một lần, độ tin cậy nhảy từ bảy mươi chín lên chín mươi bảy phần trăm!'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín bảy hai. Đây là ý tưởng của mã sửa lỗi trong mọi thiết bị điện tử!'),
    Beat('outro', 'outro', outro_text(170)),
]

FORMULAS = formulas('243/250 = "0,972"', OPTIONS,
                    paths='"0,3" dot "0,81" = "0,243", quad "0,7" dot "0,01" = "0,007"',
                    bayes='P = ("0,243")/("0,243" + "0,007") = 243/250 = "0,972"')


def validate() -> bool:
    assert F(3, 10) * F(81, 100) / (F(3, 10) * F(81, 100) + F(7, 10) * F(1, 100)) == F(243, 250)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS170(TreeMixin, ShortScene):
    N = 170

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='bit gửi',
                                                  edge_size=28)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('11: nhận "1 1"', 22, SOFT).move_to([0, -1.2, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        good = [n for n, path in self.leaves if path[-1][0] == '11']
        bad = [n for n, path in self.leaves if path[-1][0] != '11']
        self.play(*[n.animate.set_opacity(.15) for n in bad], *[n.animate.scale(1.3) for n in good], run_time=self.rt(.06))
        self.wait_until(.4, t0)
        self.write_board(self.M('paths', 1.5))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('bayes', 1.6)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.TM('$79%$ → $97%$ nhờ gửi lặp', 26, GREEN, bold=True), anim='fade')

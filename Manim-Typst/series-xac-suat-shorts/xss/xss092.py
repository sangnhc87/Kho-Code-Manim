"""XSS092 · Chia tiền cược (Pascal – Fermat 1654) — A cần 1 ván, B cần 2: P(A thắng) = 1 − 1/4 = 3/4."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import badge, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, SOFT, WHITE  # noqa: E402

EPISODE = {'code': 'XSS092', 'answer': '3/4'}
PROBLEM = ['Ai thắng $3$ ván trước được cả thưởng.',
           'Đang $2 - 1$ cho A thì phải dừng.',
           'Chia thưởng theo $P("A thắng")$ thế nào?']
OPTIONS = ['2/3', '3/4', '1/2']
CORRECT = 1
ANSWER_VALUE = .75
BRANCHES = [('A', CYAN, '1/2', []), ('B', CORAL, '1/2', [('A', CYAN, '1/2', []), ('B', CORAL, '1/2', [])])]

BEATS = [
    Beat('hook', 'hook', 'Năm một sáu năm tư, một con bạc hỏi Pascal: hai người chơi, ai thắng ba ván trước được cả tiền thưởng. '
                         'Đang hai một cho người A thì phải dừng. Chia tiền thế nào cho công bằng?'),
    Beat('guess', 'hook', 'Chia theo tỉ số hai một, tức A được hai phần ba? Hay ba phần tư? Hay chia đôi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ý tưởng của Pascal và Fermat: nhìn về tương lai, không nhìn về quá khứ. '
                        'A chỉ cần thắng thêm một ván, còn B cần thắng hai ván liên tiếp.'),
    Beat('s2', 'solve', 'Ván tới, A thắng với xác suất một phần hai là xong. Nếu B thắng, ván sau A lại có một phần hai. '
                        'B chỉ thắng chung cuộc khi thắng cả hai ván: một phần hai nhân một phần hai, bằng một phần tư.'),
    Beat('s3', 'solve', 'Vậy A thắng chung cuộc với xác suất ba phần tư. Công bằng là chia tiền theo tỉ lệ ba một, '
                        'không phải hai một như tỉ số hiện tại.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tư. Thư từ giữa Pascal và Fermat về bài toán này đã khai sinh ra lý thuyết xác suất!'),
    Beat('outro', 'outro', outro_text(92)),
]

FORMULAS = formulas('3/4', OPTIONS,
                    b='P("B thắng") = 1/2 dot 1/2 = 1/4',
                    a='P("A thắng") = 1 - 1/4 = 3/4',
                    split='"chia" quad 3 : 1')


def validate() -> bool:
    futures = list(product('AB', repeat=2))  # play out both remaining games even if decided earlier
    assert F(sum('A' in w for w in futures), 4) == F(3, 4)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS092(TreeMixin, ShortScene):
    N = 92

    def hook_visual(self, t0):
        self.score = VGroup(badge('A', CYAN, 40), self.TM('$2 - 1$', 60, WHITE, bold=True), badge('B', CORAL, 40)) \
            .arrange(buff=.5).move_to([0, 1.6, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.score, lag_ratio=.3), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        need = VGroup(tx('A cần 1 ván', 30, CYAN, bold=True), tx('B cần 2 ván', 30, CORAL, bold=True)).arrange(buff=.8) \
            .move_to([0, .4, 0])
        self.play(FadeIn(need, lag_ratio=.4), run_time=self.rt(.12))
        self.need = need

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.score.animate.set_opacity(0), self.need.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.score, self.need)
        self.board_top = -1.0
        levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.7, width=5.6, root_label='ván tới')
        self.play(*[FadeIn(lv, lag_ratio=.2) for lv in levels], run_time=self.rt(.2))
        self.wait_until(.6, t0)
        self.play(self.leaves[-1][0].animate.scale(1.35), run_time=self.rt(.05))
        self.write_board(self.M('b', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('a', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.5, t0)
        self.write_board(self.M('split', 1.8), anim='fade')
        self.write_board(tx('Pascal – Fermat, 1654', 24, SOFT), anim='fade')



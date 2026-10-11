"""XSS085 · Đồng xu hai mặt ngửa — 2 xu thường + 1 xu hai mặt ngửa; ra ngửa: P(xu đặc biệt) = 1/2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, SOFT  # noqa: E402
from common.visuals import COIN_FACE, coin  # noqa: E402

EPISODE = {'code': 'XSS085', 'answer': '1/2'}
PROBLEM = ['Có $2$ đồng xu thường và $1$ đồng xu hai',
           'mặt đều ngửa. Chọn $1$ đồng, tung được',
           'ngửa. $P("đồng hai mặt ngửa")$?']
OPTIONS = ['1/3', '1/2', '2/3']
CORRECT = 1
ANSWER_VALUE = .5
GOLDC = COIN_FACE['N'][0]
BRANCHES = [('2N', CORAL, '1/3', [('N', GOLDC, '1', [])]),
            ('T', SOFT, '2/3', [('N', GOLDC, '1/2', []), ('S', SOFT, '1/2', [])])]

BEATS = [
    Beat('hook', 'hook', 'Trong túi có hai đồng xu bình thường và một đồng xu gian, hai mặt đều là ngửa. '
                         'Rút ngẫu nhiên một đồng, tung lên được mặt ngửa. Xác suất đó là đồng xu gian bằng bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần ba, một phần hai, hay hai phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây xác suất: rút được đồng gian với xác suất một phần ba, chắc chắn ra ngửa. '
                        'Rút đồng thường với xác suất hai phần ba, ra ngửa với xác suất một phần hai.'),
    Beat('s2', 'solve', 'Hai nhánh ra ngửa: đồng gian một phần ba, đồng thường hai phần ba nhân một phần hai, '
                        'cũng bằng một phần ba. Tổng xác suất ra ngửa là hai phần ba.'),
    Beat('s3', 'solve', 'Bayes: một phần ba chia hai phần ba, bằng một phần hai. Mặt ngửa là một bằng chứng '
                        'nghiêng về đồng gian, đẩy xác suất từ một phần ba lên một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Nếu tung thêm lần nữa vẫn ngửa, nghi ngờ còn tăng tiếp!'),
    Beat('outro', 'outro', outro_text(85)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    tot='P(N) = 1/3 dot 1 + 2/3 dot 1/2 = 2/3',
                    bayes='P("gian" | N) = (1/3)/(2/3) = 1/2')


def validate() -> bool:
    coins = ['NN', 'SN', 'SN']
    faces = [(c, f) for c in coins for f in c]  # each coin, each face equally likely
    heads = [cf for cf in faces if cf[1] == 'N']
    assert F(sum(c == 'NN' for c, _ in heads), len(heads)) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS085(TreeMixin, ShortScene):
    N = 85

    def hook_visual(self, t0):
        self.bag = VGroup(VGroup(coin('N', .65), tx('thường', 22, SOFT)).arrange(DOWN, buff=.12),
                          VGroup(coin('N', .65), tx('thường', 22, SOFT)).arrange(DOWN, buff=.12),
                          VGroup(coin('N', .65), tx('2 mặt ngửa', 22, CORAL, bold=True)).arrange(DOWN, buff=.12))
        self.bag.arrange(buff=.5).move_to([0, 1.4, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.bag, lag_ratio=.3), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.bag.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.bag)
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=5.8, root_label='rút xu')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[2][0].animate.set_opacity(.2), self.leaves[0][0].animate.scale(1.3),
                  self.leaves[1][0].animate.scale(1.3), run_time=self.rt(.08))
        self.wait_until(.6, t0)
        self.write_board(self.M('tot', 1.8))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('bayes', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.TM('$1/3 arrow.r 1/2$', 34, GOLD, bold=True), anim='fade')

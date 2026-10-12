"""XSS265 · Xu lệch hóa công bằng (von Neumann) — mỗi cặp quyết định với xác suất 2pq = 0,42: trung bình 1/0,42 = 50/21."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS265', 'answer': '50/21 ≈ 2,38'}
PROBLEM = ['Xu lệch ra ngửa $"0,7"$. Tung từng cặp: NS',
           'thì A thắng, SN thì B thắng, NN hoặc SS',
           'thì tung lại. Trung bình cần mấy cặp?']
OPTIONS = ['2', '50/21 approx "2,38"', '"3,33"']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('NS', CYAN, '"0,21"', []), ('SN', CORAL, '"0,21"', []), ('lại', SOFT, '"0,58"', [])]

BEATS = [
    Beat('hook', 'hook', 'Bạn chỉ có một đồng xu lệch, ra ngửa bảy mươi phần trăm. Làm sao chơi công bằng? Nhà toán học von Neumann bày cách: '
                         'tung từng cặp, ngửa sấp thì A thắng, sấp ngửa thì B thắng, còn lại tung lại. Trung bình cần mấy cặp?'),
    Beat('guess', 'hook', 'Hai cặp, khoảng hai phẩy ba tám cặp, hay ba phẩy ba ba cặp? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vì sao công bằng? Ngửa sấp có xác suất không phẩy bảy nhân không phẩy ba, sấp ngửa là không phẩy ba nhân không phẩy bảy: '
                        'bằng nhau, đều không phẩy hai mốt, dù đồng xu lệch!'),
    Beat('s2', 'solve', 'Mỗi cặp kết thúc trò chơi với xác suất không phẩy bốn hai, tung lại với xác suất không phẩy năm tám. '
                        'Cây lặp lại chính nó.'),
    Beat('s3', 'solve', 'Chờ một sự kiện có xác suất p thì trung bình mất một chia p lần: một chia không phẩy bốn hai, bằng năm mươi phần hai mươi mốt, '
                        'khoảng hai phẩy ba tám cặp.'),
    Beat('answer', 'solve', 'Đáp án: khoảng hai phẩy ba tám cặp. Xác suất có điều kiện biến đồng xu lệch thành trọng tài công bằng!'),
    Beat('outro', 'outro', outro_text(265)),
]

FORMULAS = formulas('50/21 approx "2,38"', OPTIONS,
                    fair='P(N S) = P(S N) = "0,7" dot "0,3" = "0,21"',
                    exp='E = 1/("0,42") = 50/21 approx "2,38"')


def validate() -> bool:
    p = F(7, 10)
    assert p * (1 - p) == (1 - p) * p == F(21, 100)
    e = sum(k * F(58, 100) ** (k - 1) * F(42, 100) for k in range(1, 400))
    assert abs(float(e) - 50 / 21) < 1e-9
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS265(TreeMixin, ShortScene):
    N = 265

    def hook_visual(self, t0):
        self.board_top = -1.35
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.85), dy=1.75, width=6.4, root_label='một cặp', r=.48)
        self.wait_until(.8, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        m = self.M('fair', 1.7)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s2(self, T):
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.play(FadeIn(tx('↺ về lại đầu cây', 24, SOFT).next_to(self.leaves[2][0], [0, -1, 0], buff=.15)), run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('exp', 2.0)
        self.write_board(m)
        self.frame(m)

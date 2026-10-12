"""XSS408 · Có hòa thì sao? — bỏ ván hòa: A thắng mỗi ván quyết định 5/8; thắng 2 trước thua 2: w²(1 + 2l) = 25/64 · 14/8 = 175/256."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN  # noqa: E402

EPISODE = {'code': 'XSS408', 'answer': '175/256'}
PROBLEM = ['Mỗi ván A thắng $"0,5"$, hòa $"0,2"$, thua $"0,3"$;',
           'dừng khi A thắng $2$ ván hoặc thua $2$ ván.',
           'Xác suất A thắng chung cuộc?']
OPTIONS = ['175/256', '25/64', '5/8']
CORRECT = 0
ANSWER_VALUE = 175 / 256
W = F(5, 10) / F(8, 10)
BRANCHES = [('T', CYAN, '5/8', [('T', CYAN, '5/8', []), ('Th', CORAL, '3/8', [('T', CYAN, '5/8', [])])]),
            ('Th', CORAL, '3/8', [('T', CYAN, '5/8', [('T', CYAN, '5/8', [])])])]


def dp(w=0, l=0):
    """Exact, draws included: x = 0,5·x(w+1) + 0,2·x + 0,3·x(l+1)  ⇒  x = (0,5·x(w+1) + 0,3·x(l+1))/0,8."""
    if w == 2:
        return F(1)
    if l == 2:
        return F(0)
    return (F(1, 2) * dp(w + 1, l) + F(3, 10) * dp(w, l + 1)) / F(4, 5)


BEATS = [
    Beat('hook', 'hook', 'Mỗi ván, A thắng với xác suất không phẩy năm, hòa không phẩy hai, thua không phẩy ba. Trận đấu dừng khi A thắng hai ván hoặc thua hai ván. '
                         'Xác suất A thắng chung cuộc?'),
    Beat('guess', 'hook', 'Một trăm bảy mươi lăm phần hai trăm năm mươi sáu, hai mươi lăm phần sáu mươi tư, hay năm phần tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ván hòa không thay đổi gì, chỉ kéo dài trận. Bỏ qua ván hòa, mỗi ván có kết quả thì A thắng với xác suất không phẩy năm chia không phẩy tám, tức năm phần tám.'),
    Beat('s2', 'solve', 'Cây gọn: A thắng hai ván đầu, hoặc thắng một thua một theo hai thứ tự rồi thắng ván thứ ba.'),
    Beat('s3', 'solve', 'Xác suất: năm phần tám bình phương nhân một cộng hai nhân ba phần tám, bằng hai mươi lăm phần sáu mươi tư nhân mười bốn phần tám, tức một trăm bảy mươi lăm phần hai trăm năm mươi sáu.'),
    Beat('answer', 'solve', 'Đáp án: một trăm bảy mươi lăm phần hai trăm năm mươi sáu. Kết quả không ảnh hưởng thì cắt khỏi cây bằng xác suất có điều kiện.'),
    Beat('outro', 'outro', outro_text(408)),
]

FORMULAS = formulas('175/256', OPTIONS,
                    w='P(T | "không hòa") = ("0,5")/("0,8") = 5/8',
                    prob='P = (5/8)^2 (1 + 2 dot 3/8) = 175/256')


def validate() -> bool:
    l = 1 - W
    assert W == F(5, 8) and W ** 2 * (1 + 2 * l) == F(175, 256)
    assert dp() == F(175, 256)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS408(TreeMixin, ShortScene):
    N = 408

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.15, width=5.2, r=.34, edge_size=24)
        self.wait_until(.75, t0)

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('w', 1.4))

    def beat_s2(self, T):
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.2))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

"""XSS011 · 36 kết quả — hai xúc xắc: bảng 6 × 6 (bẫy 21: (2; 5) khác (5; 2))."""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

from manim import FadeIn, FadeOut, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import dice_grid, die  # noqa: E402

EPISODE = {'code': 'XSS011', 'answer': '36'}
PROBLEM = ['Gieo hai con xúc xắc.', 'Không gian mẫu có bao nhiêu phần tử?']
OPTIONS = ['12', '21', '36']
CORRECT = 2
ANSWER_VALUE = None

BEATS = [
    Beat('hook', 'hook', 'Gieo hai con xúc xắc cùng lúc. Có bao nhiêu kết quả có thể xảy ra? '
                         'Đếm sai ở đây thì mọi bài hai xúc xắc phía sau đều sai theo.'),
    Beat('guess', 'hook', 'Mười hai, hai mươi mốt, hay ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Xúc xắc thứ nhất có sáu mặt. Với mỗi mặt của nó, xúc xắc thứ hai lại có sáu mặt. '
                        'Xếp thành bảng: sáu cột cho con thứ nhất, sáu hàng cho con thứ hai.'),
    Beat('s2', 'solve', 'Mỗi ô là một kết quả. Ô này là con thứ nhất ra hai, con thứ hai ra năm. '
                        'Bảng có sáu nhân sáu, bằng ba mươi sáu ô.'),
    Beat('s3', 'solve', 'Bẫy hai mươi mốt: nhiều bạn coi hai năm và năm hai là một. Nhưng hai con xúc xắc là hai vật '
                        'khác nhau, giống hai đồng xu ở thử thách số bốn, nên đây là hai ô khác nhau.'),
    Beat('answer', 'solve', 'Đáp án: ba mươi sáu kết quả đồng khả năng. Bảng sáu nhân sáu này sẽ theo bạn suốt series!'),
    Beat('outro', 'outro', outro_text(11)),
]

FORMULAS = formulas('36', OPTIONS,
                    n='n(Omega) = 6 dot 6 = 36',
                    neq='(2; 5) != (5; 2)')


def validate() -> bool:
    assert len(list(product(range(1, 7), repeat=2))) == 36
    assert len({tuple(sorted(w)) for w in product(range(1, 7), repeat=2)}) == 21  # the trap
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS011(ShortScene):
    N = 11

    def hook_visual(self, t0):
        self.board_top = -1.65
        self.d1 = die(2, 1.5).move_to([-1.2, 1.3, 0])
        self.d2 = die(5, 1.5).move_to([1.2, 1.3, 0])
        self.wait_until(.25, t0)
        self.play(FadeIn(self.d1, scale=.6), FadeIn(self.d2, scale=.6), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeOut(self.d1), FadeOut(self.d2), run_time=self.rt(.04))
        self.g = dice_grid(.66, .5).move_to([.1, 1.0, 0])
        self.play(FadeIn(self.g.top, lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(self.g.left, lag_ratio=.15), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.g[0], lag_ratio=.02), run_time=self.rt(.25))

    def beat_s2(self, T):
        t0 = self.now()
        cell = self.g.cells[4][1]
        lab = self.TM('$(2; 5)$', 15, GOLD).move_to(cell)
        self.play(cell.animate.set_fill(GOLD, .35), FadeIn(lab), run_time=self.rt(.1))
        self.labels = [lab]
        self.wait_until(.55, t0)
        m = self.M('n', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        cell = self.g.cells[1][4]
        lab = self.TM('$(5; 2)$', 15, CYAN).move_to(cell)
        self.play(cell.animate.set_fill(CYAN, .35), FadeIn(lab), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.write_board(self.M('neq', 2.0))
        self.write_board(VGroup(tx('21 là bẫy', 30, CORAL, bold=True), tx('(bỏ mất thứ tự)', 26, SOFT))
                         .arrange(buff=.2), anim='fade')

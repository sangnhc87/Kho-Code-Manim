"""XSS166 · Ba nhà cung cấp — toàn phần ba nhánh: 0,45·0,98 + 0,35·0,96 + 0,2·0,95 = 0,967."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS166', 'answer': '0,967'}
PROBLEM = ['Bóng đèn đến từ 3 nơi: $45%$, $35%$,',
           '$20%$; tỉ lệ đạt chuẩn $98%$, $96%$, $95%$.',
           'Xác suất đèn đạt chuẩn?']
OPTIONS = ['"0,963"', '"0,967"', '"0,98"']
CORRECT = 1
ANSWER_VALUE = .967
BRANCHES = [('I', CYAN, '"0,45"', [('Đ', GREEN, '"0,98"', [])]),
            ('II', PURPLE, '"0,35"', [('Đ', GREEN, '"0,96"', [])]),
            ('III', GOLD, '"0,2"', [('Đ', GREEN, '"0,95"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Một cửa hàng nhập bóng đèn từ ba nhà cung cấp: bốn mươi lăm, ba mươi lăm và hai mươi phần trăm. '
                         'Tỉ lệ đạt chuẩn lần lượt chín mươi tám, chín mươi sáu và chín mươi lăm phần trăm. '
                         'Lấy ngẫu nhiên một bóng, xác suất nó đạt chuẩn là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy chín sáu ba, không phẩy chín sáu bảy, hay không phẩy chín tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Ba nhà cung cấp là ba giả thuyết, tạo ba nhánh. Ta chỉ cần vẽ nhánh con "đạt chuẩn" của mỗi nhánh.'),
    Beat('s2', 'solve', 'Nhân dọc: không phẩy bốn lăm nhân không phẩy chín tám bằng không phẩy bốn bốn một; '
                        'không phẩy ba lăm nhân không phẩy chín sáu bằng không phẩy ba ba sáu; không phẩy hai nhân không phẩy chín lăm bằng không phẩy một chín.'),
    Beat('s3', 'solve', 'Cộng ba nhánh được không phẩy chín sáu bảy. Không phẩy chín sáu ba là trung bình cộng ba tỉ lệ, sai vì bỏ qua thị phần.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín sáu bảy. Xác suất toàn phần là trung bình có trọng số, trọng số chính là xác suất các nhánh!'),
    Beat('outro', 'outro', outro_text(166)),
]

FORMULAS = formulas('"0,967"', OPTIONS,
                    parts='"0,441" + "0,336" + "0,19"',
                    tot='P = "0,45" dot "0,98" + "0,35" dot "0,96" + "0,2" dot "0,95" = "0,967"')


def validate() -> bool:
    assert round(.45 * .98 + .35 * .96 + .2 * .95, 3) == .967 and round((.98 + .96 + .95) / 3, 3) == .963
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS166(TreeMixin, ShortScene):
    N = 166

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=7.4, root_label='nhà cung cấp')
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        for i in range(3):
            self.wait_until(.1 + .28 * i, t0)
            self.play(self.leaves[i][0].animate.scale(1.3), run_time=self.rt(.04))
        self.write_board(self.M('parts', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 1.5)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(self.TM('trung bình $"0,963"$: sai', 26, CORAL, bold=True), anim='fade')

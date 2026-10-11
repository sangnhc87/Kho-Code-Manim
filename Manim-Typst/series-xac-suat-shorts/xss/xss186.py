"""XSS186 · Trúng đủ hai phát thì dừng — phát 4 trúng, 3 phát đầu trúng đúng 1: C(3,1)·0,6·0,4²·0,6 = 0,1728."""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, PANEL, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS186', 'answer': '0,1728'}
PROBLEM = ['Xạ thủ bắn đến khi trúng đủ $2$ phát',
           'thì dừng, mỗi phát trúng $"0,6"$. Xác',
           'suất dừng ở phát thứ $4$?']
OPTIONS = ['"0,0576"', '"0,1728"', '"0,3456"']
CORRECT = 1
ANSWER_VALUE = .1728
SEQS = ['TXXT', 'XTXT', 'XXTT']

BEATS = [
    Beat('hook', 'hook', 'Một xạ thủ bắn liên tục, mỗi phát trúng với xác suất không phẩy sáu, và dừng ngay khi trúng đủ hai phát. '
                         'Xác suất anh ấy dừng đúng ở phát thứ tư là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy không năm bảy sáu, không phẩy một bảy hai tám, hay không phẩy ba bốn năm sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Dừng ở phát thứ tư nghĩa là phát thứ tư trúng, và đó là phát trúng thứ hai. '
                        'Vậy ba phát đầu có đúng một phát trúng.'),
    Beat('s2', 'solve', 'Phát trúng đó có thể ở vị trí một, hai hoặc ba: ba dãy. Mỗi dãy có hai phát trúng hai phát trượt, '
                        'xác suất không phẩy sáu bình phương nhân không phẩy bốn bình phương, bằng không phẩy không năm bảy sáu.'),
    Beat('s3', 'solve', 'Nhân ba: không phẩy một bảy hai tám. Bẫy thường gặp là quên điều kiện phát cuối phải trúng, '
                        'rồi đếm sáu dãy thay vì ba.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy một bảy hai tám. Với bài "dừng ở lần k", luôn chốt lần k trước!'),
    Beat('outro', 'outro', outro_text(186)),
]

FORMULAS = formulas('"0,1728"', OPTIONS,
                    one='"0,6"^2 dot "0,4"^2 = "0,0576"',
                    tot='P = C_3^1 dot "0,6" dot "0,4"^2 dot "0,6" = "0,1728"')


def validate() -> bool:
    p = sum(.6 ** w.count('T') * .4 ** w.count('X') for w in map(''.join, product('TX', repeat=4))
            if w[3] == 'T' and w[:3].count('T') == 1)
    assert abs(p - .1728) < 1e-12 and len(SEQS) == 3
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS186(ShortScene):
    N = 186

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.slots = VGroup(*[card(1.0, 1.0, SOFT, PANEL, radius=.5, stroke_width=3) for _ in range(4)]) \
            .arrange(buff=.35).move_to([0, 2.2, 0])
        self.labs = VGroup(*[self.TM(f'${k}$', 24, SOFT).next_to(s, [0, 1, 0], buff=.08) for k, s in enumerate(self.slots, 1)])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.slots, lag_ratio=.2), FadeIn(self.labs), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        last = token('T', GREEN, .4).move_to(self.slots[3])
        self.play(FadeIn(last, scale=1.5), self.slots[3].animate.set_stroke(GOLD, 6), run_time=self.rt(.08))
        self.wait_until(.55, t0)
        self.play(*[s.animate.set_stroke(GOLD, 4) for s in self.slots[:3]], run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        rows = VGroup(*[VGroup(*[token(c, GREEN if c == 'T' else CORAL, .26) for c in s]).arrange(buff=.12) for s in SEQS]) \
            .arrange(buff=.5).move_to([0, .7, 0])
        self.play(FadeIn(rows, lag_ratio=.25), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.write_board(self.M('one', 2.0))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.7)
        self.write_board(m)
        self.frame(m)

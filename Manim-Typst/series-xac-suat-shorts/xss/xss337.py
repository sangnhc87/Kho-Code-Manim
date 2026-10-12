"""XSS337 · Hộp bí ẩn ba bi — số đỏ k = 0..3 như nhau, rút có hoàn lại 2 lần đều đỏ: hợp lý (k/3)² = 0, 1/9, 4/9, 1 → P(k = 3) = 1/(14/9) = 9/14."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, SurroundingRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, SOFT  # noqa: E402
from xss._mystery import POST, urns_row  # noqa: E402

EPISODE = {'code': 'XSS337', 'answer': '9/14'}
PROBLEM = ['Hộp $3$ bi, số bi đỏ $0, 1, 2, 3$ như nhau.',
           'Rút có hoàn lại $2$ lần, đều đỏ. Xác suất',
           'cả $3$ bi trong hộp đều đỏ?']
OPTIONS = ['9/14', '3/4', '1/2']
CORRECT = 0
ANSWER_VALUE = 9 / 14

BEATS = [
    Beat('hook', 'hook', 'Một hộp kín có ba bi, số bi đỏ có thể là không, một, hai hoặc ba, khả năng như nhau. '
                         'Rút có hoàn lại hai lần, cả hai lần đều đỏ. Xác suất cả ba bi trong hộp đều đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Chín phần mười bốn, ba phần tư, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bốn giả thuyết, mỗi cái một phần tư. Nếu hộp có k bi đỏ, xác suất rút hai lần đều đỏ là k phần ba bình phương: không, một phần chín, bốn phần chín, và một.'),
    Beat('s2', 'solve', 'Phần tư chung triệt tiêu trong công thức Bayes. Tổng các khả năng bằng mười bốn phần chín.'),
    Beat('s3', 'solve', 'Giả thuyết ba bi đỏ đóng góp một. Vậy xác suất hậu nghiệm bằng một chia mười bốn phần chín, tức chín phần mười bốn.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười bốn. Hai lần đỏ liên tiếp đẩy niềm tin từ một phần tư lên gần hai phần ba.'),
    Beat('outro', 'outro', outro_text(337)),
]

FORMULAS = formulas('9/14', OPTIONS,
                    lik='(k/3)^2: 0, 1/9, 4/9, 1',
                    tot='0 + 1/9 + 4/9 + 1 = 14/9',
                    post='P(k = 3) = 1/(14/9) = 9/14')


def validate() -> bool:
    assert POST[3] == F(9, 14)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS337(ShortScene):
    N = 337

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.urns = urns_row(1.75)
        self.ks = VGroup(*[self.TM(f'$k = {k}$', 26, SOFT).next_to(u, DOWN, buff=.15) for k, u in enumerate(self.urns)])
        self.wait_until(.35, t0)
        self.play(FadeIn(self.urns, lag_ratio=.2), FadeIn(self.ks), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        liks = VGroup(*[self.TM(f'${s}$', 30, GOLD).next_to(k, DOWN, buff=.2) for s, k in zip(('0', '1/9', '4/9', '1'), self.ks)])
        self.play(FadeIn(liks, lag_ratio=.3), run_time=self.rt(.12))
        self.write_board(self.M('lik', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.wait_until(.3, t0)
        self.write_board(self.M('tot', 1.5))

    def beat_s3(self, T):
        self.play(FadeIn(SurroundingRectangle(self.urns[3], color=GOLD, buff=.1)), run_time=self.rt(.05))
        m = self.M('post', 1.6)
        self.write_board(m)
        self.frame(m)

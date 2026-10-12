"""XSS338 · Lần thứ ba cũng đỏ? — hậu nghiệm 0, 1/14, 4/14, 9/14 (k = 0..3); P(đỏ lần 3) = Σ p_k · k/3 = 6/7."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, GREEN, SOFT  # noqa: E402
from xss._mystery import NEXT_RED, POST, urns_row  # noqa: E402

EPISODE = {'code': 'XSS338', 'answer': '6/7'}
PROBLEM = ['Hộp $3$ bi, số bi đỏ $0, 1, 2, 3$ như nhau.',
           'Đã rút có hoàn lại $2$ lần đều đỏ. Xác',
           'suất lần rút thứ ba cũng đỏ?']
OPTIONS = ['6/7', '9/14', '5/7']
CORRECT = 0
ANSWER_VALUE = 6 / 7

BEATS = [
    Beat('hook', 'hook', 'Tiếp tục hộp bí ẩn ba bi, số bi đỏ không đến ba như nhau. Đã rút có hoàn lại hai lần, đều đỏ. '
                         'Xác suất lần rút thứ ba cũng đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Sáu phần bảy, chín phần mười bốn, hay năm phần bảy? Ba, hai, một!'),
    Beat('s1', 'solve', 'Sau hai lần đỏ, niềm tin về hộp đã cập nhật: không có đỏ là không, một đỏ là một phần mười bốn, hai đỏ là bốn phần mười bốn, ba đỏ là chín phần mười bốn.'),
    Beat('s2', 'solve', 'Với mỗi hộp, lần ba đỏ với xác suất k phần ba. Lấy trung bình theo niềm tin mới: một phần mười bốn nhân một phần ba, cộng bốn phần mười bốn nhân hai phần ba, cộng chín phần mười bốn nhân một.'),
    Beat('s3', 'solve', 'Bằng ba mươi sáu phần bốn mươi hai, tức sáu phần bảy.'),
    Beat('answer', 'solve', 'Đáp án: sáu phần bảy. Dự đoán lần sau là trung bình theo xác suất hậu nghiệm, không phải theo xác suất ban đầu.'),
    Beat('outro', 'outro', outro_text(338)),
]

FORMULAS = formulas('6/7', OPTIONS,
                    post='0, quad 1/14, quad 4/14, quad 9/14',
                    mix='1/14 dot 1/3 + 4/14 dot 2/3 + 9/14 dot 1',
                    prob='P = 36/42 = 6/7')


def validate() -> bool:
    assert POST == [0, F(1, 14), F(4, 14), F(9, 14)] and NEXT_RED == F(6, 7)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS338(ShortScene):
    N = 338

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.urns = urns_row(1.75)
        self.ks = VGroup(*[self.TM(f'$k = {k}$', 26, SOFT).next_to(u, DOWN, buff=.15) for k, u in enumerate(self.urns)])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.urns, lag_ratio=.2), FadeIn(self.ks), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        ps = VGroup(*[self.TM(f'${s}$', 30, GOLD).next_to(k, DOWN, buff=.2) for s, k in zip(('0', '1/14', '4/14', '9/14'), self.ks)])
        self.wait_until(.35, t0)
        self.play(FadeIn(ps, lag_ratio=.3), run_time=self.rt(.15))
        self.write_board(self.M('post', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        nxt = VGroup(*[self.TM(f'${s}$', 28, GREEN).next_to(u, [0, 1, 0], buff=.12) for s, u in zip(('0', '1/3', '2/3', '1'), self.urns)])
        self.play(FadeIn(nxt, lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.4, t0)
        self.write_board(self.M('mix', 1.3))

    def beat_s3(self, T):
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

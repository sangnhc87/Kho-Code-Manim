"""XSS397 · Ba trạm trung chuyển — đúng ⇔ số lần lật chẵn (0 hoặc 2): 0,9³ + 3·0,9·0,1² = 0,729 + 0,027 = 0,756."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from manim import Arrow, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS397', 'answer': '0,756'}
PROBLEM = ['Tín hiệu $0$/$1$ qua $3$ trạm, mỗi trạm lật',
           'bit với xác suất $"0,1"$, độc lập. Xác suất',
           'tín hiệu nhận được đúng?']
OPTIONS = ['"0,756"', '"0,729"', '"0,9"']
CORRECT = 0
ANSWER_VALUE = .756
P = F(1, 10)


def correct():
    tot = F(0)
    for s in product((0, 1), repeat=3):
        pr = F(1)
        for x in s:
            pr *= P if x else 1 - P
        tot += pr * (sum(s) % 2 == 0)
    return tot


BEATS = [
    Beat('hook', 'hook', 'Một bit tín hiệu không hoặc một đi qua ba trạm trung chuyển. Mỗi trạm lật bit với xác suất không phẩy một, độc lập. '
                         'Xác suất tín hiệu đến nơi vẫn đúng?'),
    Beat('guess', 'hook', 'Không phẩy bảy năm sáu, không phẩy bảy hai chín, hay không phẩy chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Lật hai lần thì bit trở về như cũ! Tín hiệu đúng khi số lần lật là số chẵn: không lần, hoặc hai lần.'),
    Beat('s2', 'solve', 'Không lần lật: không phẩy chín mũ ba, không phẩy bảy hai chín. Đúng hai lần lật: ba cách chọn trạm, nhân không phẩy chín nhân không phẩy một bình phương, không phẩy không hai bảy.'),
    Beat('s3', 'solve', 'Cộng lại: không phẩy bảy năm sáu. Đáp án không phẩy bảy hai chín là bẫy, quên mất hai lần lỗi tự sửa nhau.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy bảy năm sáu. Trên cây nhiều tầng, nhiều đường khác nhau có thể dẫn về cùng một kết quả.'),
    Beat('outro', 'outro', outro_text(397)),
]

FORMULAS = formulas('"0,756"', OPTIONS,
                    zero='"0,9"^3 = "0,729"',
                    two='C_3^2 dot "0,9" dot "0,1"^2 = "0,027"',
                    prob='P = "0,729" + "0,027" = "0,756"')


def validate() -> bool:
    assert correct() == F(756, 1000)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS397(ShortScene):
    N = 397

    def hook_visual(self, t0):
        self.board_top = -1.3
        nodes = VGroup(token('1', CYAN, .38), *[token(f'T{i}', SOFT, .38) for i in (1, 2, 3)], token('?', GOLD, .38)).arrange(buff=.75).move_to([0, 1.3, 0])
        arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=.05, color=SOFT, stroke_width=4) for i in range(4)])
        self.chain = VGroup(nodes, arrows)
        self.wait_until(.45, t0)
        self.play(FadeIn(self.chain, lag_ratio=.1), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(self.chain[0][1].animate.set_fill(GOLD), self.chain[0][3].animate.set_fill(GOLD), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('zero', 1.4))
        self.wait_until(.5, t0)
        self.write_board(self.M('two', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

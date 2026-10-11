"""XSS063 · Biết con cả là trai — còn TT, TG: 1/2 (so sánh với XSS062)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import cross, tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT  # noqa: E402
from xss.xss062 import KIDS, family  # noqa: E402

EPISODE = {'code': 'XSS063', 'answer': '1/2'}
PROBLEM = ['Gia đình có $2$ con, biết CON CẢ là con trai.', 'Xác suất cả hai đều là trai?']
OPTIONS = ['1/2', '1/3', '1/4']
CORRECT = 0
ANSWER_VALUE = .5

BEATS = [
    Beat('hook', 'hook', 'Thử thách trước, biết có ít nhất một con trai, đáp án là một phần ba. '
                         'Lần này thông tin cụ thể hơn: con cả là con trai. Xác suất cả hai là trai bây giờ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, một phần ba, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Vẫn bốn khả năng theo thứ tự con cả, con út. Biết con cả là trai, ta loại cả gái trai lẫn gái gái.'),
    Beat('s2', 'solve', 'Chỉ còn trai trai và trai gái, hai khả năng như nhau. Xác suất cả hai là trai bằng một phần hai.'),
    Beat('s3', 'solve', 'Vì sao khác thử thách trước? Lần này ta biết chính xác con nào là trai, '
                        'nên con út thật sự là trai hay gái như nhau. Thông tin càng cụ thể, kết quả càng khác.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Một chữ "con cả" thay đổi hẳn đáp án, đó là sức mạnh của điều kiện!'),
    Beat('outro', 'outro', outro_text(63)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    prob='P("TT" | "con cả trai") = 1/2',
                    cmp='P("TT" | "có trai") = 1/3')


def validate() -> bool:
    cond = [w for w in KIDS if w[0] == 'T']
    assert F(sum(w == 'TT' for w in cond), len(cond)) == F(1, 2)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS063(ShortScene):
    N = 63

    def hook_visual(self, t0):
        self.fams = VGroup(*[family(w) for w in KIDS]).arrange_in_grid(2, 2, buff=(.4, .35)).move_to([0, 1.35, 0])
        heads = VGroup(tx('cả  út', 22, SOFT).next_to(self.fams[0], [0, 1, 0], buff=.08),
                       tx('cả  út', 22, SOFT).next_to(self.fams[1], [0, 1, 0], buff=.08))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.fams, lag_ratio=.25), FadeIn(heads), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        for i in (2, 3):
            self.play(self.fams[i].animate.set_opacity(.25), FadeIn(cross(CORAL, 1.0).move_to(self.fams[i])),
                      run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.fams[0][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('cmp', 1.7), anim='fade')
        self.wait_until(.55, t0)
        self.write_board(tx('thông tin cụ thể hơn → đáp án khác', 26, CYAN, bold=True), anim='fade')

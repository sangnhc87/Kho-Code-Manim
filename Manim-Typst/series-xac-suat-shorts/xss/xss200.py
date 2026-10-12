"""XSS200 · Monty Hall 100 cửa — giữ cửa đầu: 1/100; đổi: 99/100."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, PANEL, SOFT  # noqa: E402

EPISODE = {'code': 'XSS200', 'answer': '99/100'}
PROBLEM = ['$100$ cửa, $1$ cửa có xe. Bạn chọn $1$ cửa,',
           'người dẫn (biết) mở $98$ cửa có dê. Đổi',
           'sang cửa còn lại: xác suất trúng xe?']
OPTIONS = ['1/2', '99/100', '1/100']
CORRECT = 1
ANSWER_VALUE = .99

BEATS = [
    Beat('hook', 'hook', 'Thử thách số hai trăm: Monty Hall phiên bản một trăm cửa. Một cửa có xe hơi. Bạn chọn một cửa. '
                         'Người dẫn biết xe ở đâu, mở chín mươi tám cửa đều có dê. Bạn có nên đổi sang cửa còn lại không?'),
    Beat('guess', 'hook', 'Đổi cửa trúng với xác suất một phần hai, chín mươi chín phần trăm, hay một phần trăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cửa bạn chọn đúng ngay từ đầu với xác suất một phần trăm. Người dẫn mở cửa nào cũng không làm thay đổi điều đó, '
                        'vì anh ấy luôn mở được cửa dê.'),
    Beat('s2', 'solve', 'Chín mươi chín phần trăm còn lại nằm ở nhóm chín mươi chín cửa bạn không chọn. Người dẫn loại bỏ chín mươi tám cửa sai '
                        'trong nhóm đó, dồn toàn bộ chín mươi chín phần trăm vào cửa cuối cùng.'),
    Beat('s3', 'solve', 'Vậy đổi cửa thắng với xác suất chín mươi chín phần trăm. Với ba cửa, cùng lý luận cho hai phần ba.'),
    Beat('answer', 'solve', 'Đáp án: chín mươi chín phần trăm. Cảm ơn bạn đã đi cùng hai trăm thử thách. Phần tiếp theo còn nhiều bất ngờ hơn!'),
    Beat('outro', 'outro', outro_text(200)),
]

FORMULAS = formulas('99/100', OPTIONS,
                    keep='P("giữ") = 1/100',
                    swap='P("đổi") = 1 - 1/100 = 99/100')


def validate() -> bool:
    keep = F(1, 100)
    assert 1 - keep == F(99, 100)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS200(ShortScene):
    N = 200

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.doors = VGroup(*[card(.42, .4, SOFT, PANEL, radius=.05, stroke_width=1.5) for _ in range(100)]) \
            .arrange_in_grid(10, 10, buff=.07).move_to([0, 1.05, 0])
        self.wait_until(.6, t0)
        self.play(FadeIn(self.doors, lag_ratio=.003), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.doors[0].animate.set_stroke(GOLD, 5).set_fill(GOLD, .4), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.write_board(self.M('keep', 2.1))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[d.animate.set_opacity(.12) for i, d in enumerate(self.doors) if i not in (0, 57)], run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.play(self.doors[57].animate.set_stroke(GREEN, 6).set_fill(GREEN, .4).scale(1.4), run_time=self.rt(.06))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('swap', 2.1)
        self.write_board(m)
        self.frame(m, CORAL)

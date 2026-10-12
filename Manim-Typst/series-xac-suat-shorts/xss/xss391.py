"""XSS391 · Ba lần thất bại rồi — các lần thử độc lập (không có trí nhớ): P(thành công trong 2 lần tới) = 1 − 0,8² = 0,36."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS391', 'answer': '0,36'}
PROBLEM = ['Mỗi lần thử thành công với xác suất $"0,2"$,',
           'độc lập. Biết $3$ lần đầu đều thất bại.',
           'Xác suất thành công trong $2$ lần tới?']
OPTIONS = ['"0,36"', '"0,2"', '"0,488"']
CORRECT = 0
ANSWER_VALUE = .36
P = F(1, 5)

BEATS = [
    Beat('hook', 'hook', 'Mỗi lần thử thành công với xác suất không phẩy hai, các lần độc lập. Ba lần đầu đều thất bại. '
                         'Xác suất thành công trong hai lần tiếp theo là bao nhiêu? Đã thua nhiều thì sắp thắng chăng?'),
    Beat('guess', 'hook', 'Không phẩy ba sáu, không phẩy hai, hay không phẩy bốn tám tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Theo định nghĩa: xác suất có điều kiện bằng xác suất ba lần đầu thất bại rồi có thành công trong lần bốn hoặc năm, chia xác suất ba lần đầu thất bại.'),
    Beat('s2', 'solve', 'Vì độc lập, phần không phẩy tám mũ ba triệt tiêu. Chỉ còn xác suất có thành công trong hai lần: một trừ không phẩy tám bình phương.'),
    Beat('s3', 'solve', 'Bằng một trừ không phẩy sáu tư, tức không phẩy ba sáu. Quá khứ không làm thay đổi tương lai.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy ba sáu. Ảo tưởng con bạc: thua nhiều lần không làm lần sau dễ thắng hơn.'),
    Beat('outro', 'outro', outro_text(391)),
]

FORMULAS = formulas('"0,36"', OPTIONS,
                    defn='P = ("0,8"^3 dot (1 - "0,8"^2))/("0,8"^3)',
                    prob='P = 1 - "0,8"^2 = "0,36"')


def validate() -> bool:
    q = 1 - P
    assert (q ** 3 * (1 - q ** 2)) / q ** 3 == F(36, 100)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS391(ShortScene):
    N = 391

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.row = VGroup(*[token('X' if i < 3 else '?', CORAL if i < 3 else SOFT, .42) for i in range(5)]).arrange(buff=.3).move_to([0, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.row, lag_ratio=.2), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('defn', 1.4))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.row[:3].animate.set_opacity(.25), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.play(*[self.row[i][0].animate.set_fill(GREEN, 1) for i in (3, 4)], run_time=self.rt(.05))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

"""XSS110 · Con bạc phá sản — trò chơi công bằng: kỳ vọng tiền giữ nguyên, 2 = 5p + 0(1 − p) ⇒ p = 2/5."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS110', 'answer': '2/5'}
PROBLEM = ['Có $2$ đồng, mỗi ván thắng hoặc thua $1$',
           'đồng (xác suất $1/2$). Dừng khi có $5$ đồng',
           'hoặc hết tiền. $P("đạt 5 đồng")$?']
OPTIONS = ['1/2', '2/5', '1/4']
CORRECT = 1
ANSWER_VALUE = .4
N, SEED = 1000, 10


def games():
    r, c, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        m = 2
        while 0 < m < 5:
            m += 1 if r.random() < .5 else -1
        c += m == 5
        out.append(c / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Bạn có hai đồng. Mỗi ván tung đồng xu: thắng được một đồng, thua mất một đồng. '
                         'Bạn chơi đến khi có năm đồng thì nghỉ, hoặc cho đến khi cháy túi. Xác suất bạn đạt năm đồng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần năm, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Liệt kê mọi đường đi thì vô tận, vì có thể lên xuống mãi. Ta cần một ý tưởng thông minh hơn.'),
    Beat('s2', 'solve', 'Trò chơi công bằng: mỗi ván, trung bình bạn không lời không lỗ. Vậy về trung bình, '
                        'số tiền lúc kết thúc phải bằng đúng số tiền ban đầu, là hai đồng.'),
    Beat('s3', 'solve', 'Lúc kết thúc chỉ có hai khả năng: năm đồng với xác suất p, hoặc không đồng. '
                        'Trung bình bằng năm p, và phải bằng hai. Suy ra p bằng hai phần năm.'),
    Beat('s4', 'solve', 'Mô phỏng một nghìn người chơi, mỗi người bắt đầu với hai đồng: khoảng bốn mươi phần trăm đạt năm đồng, '
                        'còn lại đều cháy túi.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm. Ý tưởng "kỳ vọng không đổi" giải được bài toán tưởng như vô hạn bước!'),
    Beat('outro', 'outro', outro_text(110)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    fair='E("tiền cuối") = E("tiền đầu") = 2',
                    eq='5 p + 0 dot (1 - p) = 2 arrow.r.double p = 2/5')


def validate() -> bool:
    # exact: P_i satisfies P_i = (P_{i-1} + P_{i+1})/2, P_0 = 0, P_5 = 1 → P_i = i/5
    p = [F(i, 5) for i in range(6)]
    assert all(p[i] == (p[i - 1] + p[i + 1]) / 2 for i in range(1, 5)) and p[2] == F(2, 5)
    assert abs(games()[-1] - .4) < .003
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS110(ShortScene):
    N = 110

    def hook_visual(self, t0):
        self.board_top = -1.2
        xs = [-3.0 + 1.2 * k for k in range(6)]
        self.line = Line([xs[0], 1.4, 0], [xs[-1], 1.4, 0], color=SOFT, stroke_width=4)
        self.ticks = VGroup(*[VGroup(Line([x, 1.25, 0], [x, 1.55, 0], color=SOFT, stroke_width=3),
                                     self.MNum(k, 0, CORAL if k == 0 else GREEN if k == 5 else SOFT, 30)
                                     .move_to([x, .9, 0])) for k, x in enumerate(xs)])
        self.xs = xs
        self.me = token('$', GOLD, .35).move_to([xs[2], 2.0, 0])
        labels = VGroup(tx('cháy túi', 22, CORAL, bold=True).move_to([xs[0], .45, 0]),
                        tx('nghỉ chơi', 22, GREEN, bold=True).move_to([xs[5], .45, 0]))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.line), FadeIn(self.ticks), FadeIn(labels), FadeIn(self.me), run_time=self.rt(.12))

    def beat_s1(self, T):
        path = [3, 2, 3, 4, 3, 2, 1, 2]
        for k in path:
            self.play(self.me.animate.move_to([self.xs[k], 2.0, 0]), run_time=self.rt(.07))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('fair', 1.9))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        m = self.M('eq', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s4(self, T):
        self.clear_board(.03)
        self.run_sim(games(), 'số người chơi:', 'đạt 5 đồng:', .6, y=-1.75)



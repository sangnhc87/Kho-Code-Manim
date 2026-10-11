"""XSS109 · Đo số π bằng xác suất — điểm ngẫu nhiên trong hình vuông rơi vào hình tròn nội tiếp: π/4."""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from manim import Circle, Dot, FadeIn, Square, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS109', 'answer': 'π/4 ≈ 0,785'}
PROBLEM = ['Chọn ngẫu nhiên một điểm trong',
           'hình vuông. Xác suất điểm đó nằm',
           'trong hình tròn nội tiếp?']
OPTIONS = ['1/2', 'pi/4 approx "0,785"', '3/4']
CORRECT = 1
ANSWER_VALUE = math.pi / 4
N, SEED = 2000, 13


def shots():
    r, c, pts, out = random.Random(SEED), 0, [], []
    for k in range(1, N + 1):
        x, y = r.random() * 2 - 1, r.random() * 2 - 1
        inside = x * x + y * y < 1
        c += inside
        pts.append((x, y, inside))
        out.append(c / k)
    return pts, out


BEATS = [
    Beat('hook', 'hook', 'Một hình vuông có một hình tròn vừa khít bên trong. Ném ngẫu nhiên một hạt cát vào hình vuông. '
                         'Xác suất hạt cát rơi vào hình tròn là bao nhiêu? Và làm sao dùng nó để đo số pi?'),
    Beat('guess', 'hook', 'Một phần hai, pi phần bốn, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Điểm rơi đều trên hình vuông, nên xác suất bằng tỉ số diện tích. Hình tròn bán kính r có diện tích pi r bình '
                        'phương, hình vuông cạnh hai r có diện tích bốn r bình phương.'),
    Beat('s2', 'solve', 'Tỉ số bằng pi phần bốn, khoảng không phẩy bảy tám năm, không phụ thuộc kích thước.'),
    Beat('s3', 'solve', 'Làm ngược lại: ném hai nghìn hạt cát, đếm tỉ lệ rơi vào hình tròn, rồi nhân bốn. '
                        'Ta ước lượng được số pi, càng ném nhiều càng chính xác.'),
    Beat('answer', 'solve', 'Đáp án: pi phần bốn. Đây gọi là phương pháp Monte Carlo, được dùng hằng ngày trong vật lý, tài chính và trí tuệ nhân tạo.'),
    Beat('outro', 'outro', outro_text(109)),
]

FORMULAS = formulas('pi/4 approx "0,785"', OPTIONS,
                    ratio='P = (pi r^2)/((2r)^2) = pi/4',
                    est='pi approx 4 f')


def validate() -> bool:
    _, out = shots()
    assert abs(out[-1] - math.pi / 4) < .002 and abs(4 * out[-1] - math.pi) < .01
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS109(ShortScene):
    N = 109

    def hook_visual(self, t0):
        self.board_top = -1.35
        self.side, self.c = 3.8, (0, 1.2)
        self.sq = Square(side_length=self.side, stroke_color=SOFT, stroke_width=3).move_to([*self.c, 0])
        self.circ = Circle(radius=self.side / 2, stroke_color=CYAN, stroke_width=4).move_to([*self.c, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.sq), FadeIn(self.circ), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.circ.animate.set_fill(CYAN, .25), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.M('ratio', 1.9))

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('answer', 2.0)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        pts, out = shots()
        h = self.side / 2
        dots = VGroup(*[Dot([self.c[0] + h * x, self.c[1] + h * y, 0], radius=.025, color=GREEN if ok else CORAL)
                        for x, y, ok in pts[:900]])
        self.play(FadeIn(dots, lag_ratio=.002), run_time=self.rt(.3))
        self.run_sim(out, 'số hạt cát:', 'trong hình tròn:', .3, y=-1.75)
        self.wait_until(.75, t0)
        self.write_board(VGroup(self.M('est', 1.6), self.TM('$= "' + f'{4 * out[-1]:.2f}'.replace('.', ',') + '"$', 30, GOLD, bold=True))
                         .arrange(buff=.2), anim='fade')

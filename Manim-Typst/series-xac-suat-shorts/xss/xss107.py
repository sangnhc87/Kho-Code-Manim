"""XSS107 · Cây kim của Buffon — kim dài bằng khoảng cách vạch: P(cắt vạch) = 2/π ≈ 0,637, từ đó đo được π."""
from __future__ import annotations

import math
import random
import sys
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402

EPISODE = {'code': 'XSS107', 'answer': '2/π ≈ 0,637'}
PROBLEM = ['Thả ngẫu nhiên một cây kim lên sàn kẻ',
           'vạch song song, kim dài bằng khoảng cách',
           'hai vạch. $P("kim cắt vạch")$?']
OPTIONS = ['1/2', '2/pi approx "0,637"', '1/pi']
CORRECT = 1
ANSWER_VALUE = 2 / math.pi
N, SEED = 2000, 16
GAP = 1.0


def drops():
    r, c, out, needles = random.Random(SEED), 0, [], []
    for k in range(1, N + 1):
        y, t = r.random() * GAP / 2, r.random() * math.pi
        hit = y <= GAP / 2 * math.sin(t)
        c += hit
        out.append(c / k)
        if k <= 60:
            needles.append((r.random(), y if r.random() < .5 else -y, t, hit))
    return needles, out


BEATS = [
    Beat('hook', 'hook', 'Năm một bảy bảy, bá tước Buffon thả những cây kim xuống sàn gỗ kẻ vạch song song. '
                         'Cây kim dài đúng bằng khoảng cách giữa hai vạch. Xác suất cây kim cắt một vạch là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, hai chia pi, hay một chia pi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai con số quyết định: khoảng cách từ tâm cây kim tới vạch gần nhất, và góc nghiêng của kim. '
                        'Kim cắt vạch khi khoảng cách đó nhỏ hơn nửa chiều dài kim nhân sin của góc.'),
    Beat('s2', 'solve', 'Kim nằm ngang thì sin bằng không, gần như không bao giờ cắt. Kim dựng đứng thì cắt nhiều nhất. '
                        'Lấy trung bình của sin theo mọi góc, ta được hai chia pi.'),
    Beat('s3', 'solve', 'Vậy xác suất bằng hai chia pi, khoảng không phẩy sáu ba bảy. Số pi xuất hiện từ những cây kim và vạch thẳng, '
                        'không hề có đường tròn nào!'),
    Beat('s4', 'solve', 'Làm ngược lại: thả hai nghìn cây kim, đếm tỉ lệ cắt vạch, rồi lấy hai chia tỉ lệ đó, ta đo được số pi '
                        'bằng xác suất.'),
    Beat('answer', 'solve', 'Đáp án: hai chia pi. Đây là thí nghiệm Monte Carlo đầu tiên trong lịch sử, hơn hai trăm năm trước máy tính!'),
    Beat('outro', 'outro', outro_text(107)),
]

FORMULAS = formulas('2/pi approx "0,637"', OPTIONS,
                    cond='"cắt" arrow.l.r.double d <= 1/2 sin theta',
                    avg='P = 2/pi approx "0,637"',
                    est='pi approx 2/f')


def validate() -> bool:
    _, out = drops()
    assert abs(out[-1] - 2 / math.pi) < .002 and abs(2 / out[-1] - math.pi) < .01
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS107(ShortScene):
    N = 107

    def floor(self):
        ys = [2.9 - 1.0 * k for k in range(4)]
        lines = VGroup(*[Line([-3.6, y, 0], [3.6, y, 0], color=SOFT, stroke_width=3) for y in ys])
        return lines, ys

    def hook_visual(self, t0):
        self.board_top = -1.35
        self.lines, ys = self.floor()
        needles, _ = drops()
        self.needle_mobs = VGroup()
        for i, (u, dy, t, hit) in enumerate(needles):
            cx = -3.2 + 6.4 * u
            cy = ys[i % 3] - .5 + dy
            dx, dyy = .5 * math.cos(t), .5 * math.sin(t)
            self.needle_mobs.add(Line([cx - dx, cy - dyy, 0], [cx + dx, cy + dyy, 0], color=GOLD if hit else CYAN,
                                      stroke_width=4))
        self.wait_until(.4, t0)
        self.play(FadeIn(self.lines), run_time=self.rt(.06))
        self.play(FadeIn(self.needle_mobs[:8], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.write_board(self.M('cond', 2.0))

    def beat_s2(self, T):
        self.play(FadeIn(self.needle_mobs[8:], lag_ratio=.05), run_time=self.rt(.4))
        self.write_board(tx('vàng: cắt vạch   xanh: không cắt', 24, SOFT), anim='fade')

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('avg', 2.3)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.7, t0)

    def beat_s4(self, T):
        t0 = self.now()
        self.clear_board(.03)
        _, out = drops()
        self.run_sim(out, 'số cây kim:', 'tỉ lệ cắt:', .45, y=-1.75)
        self.wait_until(.6, t0)
        self.write_board(VGroup(self.M('est', 1.6), self.TM('$approx "3,14"$', 30, GOLD, bold=True)).arrange(buff=.25),
                         anim='fade')



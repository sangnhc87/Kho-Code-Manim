"""XSS413 · Đếm cá trong hồ — bắt lại: tỉ lệ có dấu 8/40 ≈ 50/N → N ≈ 50·40/8 = 250 (ước lượng Lincoln–Petersen)."""
from __future__ import annotations

import random
import sys
from pathlib import Path

from manim import Dot, Ellipse, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, PANEL_2, STROKE  # noqa: E402

EPISODE = {'code': 'XSS413', 'answer': '250'}
PROBLEM = ['Đánh dấu $50$ con cá rồi thả lại hồ. Lần',
           'sau bắt $40$ con thấy $8$ con có dấu. Ước',
           'lượng số cá trong hồ?']
OPTIONS = ['250', '200', '320']
CORRECT = 0
ANSWER_VALUE = 250

BEATS = [
    Beat('hook', 'hook', 'Làm sao đếm cá trong một cái hồ? Người ta bắt năm mươi con, đánh dấu rồi thả lại. Lần sau bắt bốn mươi con, thấy tám con có dấu. '
                         'Trong hồ có khoảng bao nhiêu con cá?'),
    Beat('guess', 'hook', 'Hai trăm năm mươi, hai trăm, hay ba trăm hai mươi? Ba, hai, một!'),
    Beat('s1', 'solve', 'Nếu cá trộn đều, xác suất một con bắt được có dấu bằng năm mươi chia N, với N là số cá trong hồ.'),
    Beat('s2', 'solve', 'Mẻ thứ hai cho tỉ lệ thực nghiệm tám trên bốn mươi, tức một phần năm. Cho hai tỉ lệ bằng nhau: năm mươi trên N bằng một phần năm.'),
    Beat('s3', 'solve', 'Suy ra N khoảng hai trăm năm mươi con. Đây là phương pháp bắt và thả lại mà các nhà sinh thái học vẫn dùng.'),
    Beat('answer', 'solve', 'Đáp án: khoảng hai trăm năm mươi con. Xác suất biến một mẻ lưới nhỏ thành phép đếm cả hồ.'),
    Beat('outro', 'outro', outro_text(413)),
]

FORMULAS = formulas('250', OPTIONS,
                    ratio='50/N approx 8/40 = 1/5',
                    prob='N approx (50 dot 40)/8 = 250')


def validate() -> bool:
    assert 50 * 40 // 8 == 250
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS413(ShortScene):
    N = 413

    def hook_visual(self, t0):
        self.board_top = -1.3
        pond = Ellipse(width=6.4, height=3.2, stroke_color=STROKE, stroke_width=4, fill_color=PANEL_2, fill_opacity=1).move_to([0, .95, 0])
        rnd = random.Random(413)
        fish = VGroup()
        for k in range(60):
            while True:
                x, y = rnd.uniform(-3, 3), rnd.uniform(-1.4, 1.4)
                if (x / 3) ** 2 + (y / 1.45) ** 2 < .85:
                    break
            fish.add(Dot([x, y + .95, 0], radius=.07, color=CORAL if k < 12 else CYAN))
        self.pond, self.fish = pond, fish
        self.wait_until(.35, t0)
        self.play(FadeIn(pond), FadeIn(fish, lag_ratio=.01), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.play(*[f.animate.scale(1.6) for f in self.fish[:12]], run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('ratio', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)

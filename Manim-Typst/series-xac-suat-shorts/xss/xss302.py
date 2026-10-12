"""XSS302 · Robot rẽ ngẫu nhiên — mỗi ngã rẽ 1/2, chạm mép đi thẳng: qua (3;0) ⇔ RRR: 1/8 (chọn đều đường: 1/20)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import Dot, FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402
from xss._gridkit import Lattice  # noqa: E402

EPISODE = {'code': 'XSS302', 'answer': '1/8'}
PROBLEM = ['Robot đi từ $(0; 0)$ tới $(3; 3)$, ở mỗi ngã',
           'rẽ chọn sang phải hoặc lên ($1/2$), chạm',
           'mép thì đi thẳng. $P("qua góc " (3; 0))$?']
OPTIONS = ['1/20', '1/8', '1/4']
CORRECT = 1
ANSWER_VALUE = 1 / 8


BEATS = [
    Beat('hook', 'hook', 'Một robot đi từ gốc tới ba ba, chỉ sang phải hoặc lên trên. Ở mỗi ngã rẽ, robot tung đồng xu chọn hướng; '
                         'khi đã chạm mép trên hoặc mép phải thì đi thẳng. Xác suất robot đi qua góc ba không là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai mươi, một phần tám, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Qua góc ba không nghĩa là ba bước đầu đều sang phải. Mỗi bước là một ngã rẽ thật, xác suất một phần hai: một phần tám.'),
    Beat('s2', 'solve', 'Nếu chọn đều một trong hai mươi đường ngắn nhất thì chỉ được một phần hai mươi! Hai cách "ngẫu nhiên" cho hai đáp số khác nhau.'),
    Beat('s3', 'solve', 'Lý do: robot tung xu cho các đường men mép ít lần hơn, nên các đường đó có xác suất lớn hơn. Các đường không còn đồng khả năng.'),
    Beat('answer', 'solve', 'Đáp án: một phần tám. Luôn hỏi: ngẫu nhiên theo kiểu nào? Mô hình khác nhau cho xác suất khác nhau!'),
    Beat('outro', 'outro', outro_text(302)),
]

FORMULAS = formulas('1/8', OPTIONS,
                    robot='P = (1/2)^3 = 1/8',
                    uniform='"chọn đều đường": 1/(C_6^3) = 1/20')


def robot_paths():
    """Distinct robot paths with their probabilities."""
    out = {}

    def go(x, y, path, pr):
        if (x, y) == (3, 3):
            out[path] = out.get(path, 0) + pr
            return
        if x == 3:
            go(x, y + 1, path + 'U', pr)
        elif y == 3:
            go(x + 1, y, path + 'R', pr)
        else:
            go(x + 1, y, path + 'R', pr / 2)
            go(x, y + 1, path + 'U', pr / 2)
    go(0, 0, '', F(1))
    return out


def validate() -> bool:
    paths = robot_paths()
    assert len(paths) == 20 and sum(paths.values()) == 1
    assert paths['RRRUUU'] == F(1, 8)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS302(ShortScene):
    N = 302

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.L = Lattice(3, 3, origin=(-1.5, -.3), step=1.0)
        self.g = self.L.grid()
        self.corner = Dot(self.L.P(3, 0), radius=.15, color=GOLD)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.g), FadeIn(self.corner), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        p = self.L.path('RRRUUU', GOLD, 6)
        self.play(FadeIn(p), run_time=self.rt(.08))
        self.wait_until(.5, t0)
        self.write_board(self.M('robot', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('uniform', 1.8))

    def beat_s3(self, T):
        self.clear_board(.03)
        self.write_board(tx('đường men mép: ít lần tung xu hơn', 26, CYAN), anim='fade')
        self.write_board(tx('→ không đồng khả năng', 28, CORAL, bold=True), anim='fade')

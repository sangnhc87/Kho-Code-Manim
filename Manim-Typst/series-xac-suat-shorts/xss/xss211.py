"""XSS211 · Hai bi xanh liền nhau — 2 vị trí xanh trong 6: 5 cặp kề / C(6,2) = 15: 1/3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import card  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, PANEL, SOFT  # noqa: E402
from common.visuals import ball, urn  # noqa: E402

EPISODE = {'code': 'XSS211', 'answer': '1/3'}
PROBLEM = ['Hộp $4$ đỏ $2$ xanh, rút lần lượt đến hết.', 'Xác suất hai bi xanh được rút liền nhau?']
OPTIONS = ['1/5', '1/3', '1/2']
CORRECT = 1
ANSWER_VALUE = 1 / 3

BEATS = [
    Beat('hook', 'hook', 'Hộp có bốn bi đỏ và hai bi xanh. Rút lần lượt từng bi cho đến hết. '
                         'Xác suất hai bi xanh được rút liền nhau là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần năm, một phần ba, hay một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Rút đến hết là xếp sáu bi thành hàng ngẫu nhiên. Chỉ cần quan tâm vị trí của hai bi xanh: '
                        'tổ hợp chập hai của sáu, mười lăm cặp vị trí đồng khả năng.'),
    Beat('s2', 'solve', 'Hai vị trí liền nhau: một hai, hai ba, ba bốn, bốn năm, năm sáu: năm cặp.'),
    Beat('s3', 'solve', 'Xác suất năm phần mười lăm, tức một phần ba. Không cần vẽ cây sáu tầng!'),
    Beat('answer', 'solve', 'Đáp án: một phần ba. Rút đến hết thì chỉ chọn vị trí cho nhóm ít bi nhất!'),
    Beat('outro', 'outro', outro_text(211)),
]

FORMULAS = formulas('1/3', OPTIONS,
                    omega='n(Omega) = C_6^2 = 15',
                    prob='P = 5/15 = 1/3')


def validate() -> bool:
    seqs = set(permutations('RRRRBB'))
    assert F(sum('BB' in ''.join(s) for s in seqs), len(seqs)) == F(1, 3)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS211(ShortScene):
    N = 211

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.u = urn('RRRRBB', cols=3, r=.34).move_to([0, 2.2, 0])
        self.slots = VGroup(*[card(.8, .8, SOFT, PANEL, radius=.4, stroke_width=2) for _ in range(6)]).arrange(buff=.2) \
            .move_to([0, .6, 0])
        self.wait_until(.55, t0)
        self.play(FadeIn(self.u), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.slots, lag_ratio=.1), run_time=self.rt(.1))
        self.wait_until(.5, t0)
        self.write_board(self.M('omega', 2.2))

    def beat_s2(self, T):
        t0 = self.now()
        for i in range(5):
            pair = VGroup(ball('B', .3).move_to(self.slots[i]), ball('B', .3).move_to(self.slots[i + 1]))
            self.play(FadeIn(pair), run_time=self.rt(.04))
            self.wait_until(.1 + .17 * (i + 1), t0)
            self.play(pair.animate.set_opacity(0), run_time=self.rt(.02))
        self.play(*[s.animate.set_stroke(GOLD, 4) for s in self.slots], run_time=self.rt(.03))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 2.3)
        self.write_board(m)
        self.frame(m)



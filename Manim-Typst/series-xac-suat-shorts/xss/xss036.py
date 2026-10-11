"""XSS036 · Cược của de Méré (1) — ít nhất một mặt 6 trong 4 lần gieo: 1 − (5/6)⁴ ≈ 0,518."""
from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS036', 'answer': '671/1296 ≈ 0,518'}
PROBLEM = ['Gieo một con xúc xắc $4$ lần.', 'Xác suất có ít nhất một mặt $6$?']
OPTIONS = ['2/3', '671/1296 approx "0,518"', '1/2']
CORRECT = 1
ANSWER_VALUE = 671 / 1296
GAMES, SEED = 2000, 19


def wins():
    r, w, out = random.Random(SEED), 0, []
    for k in range(1, GAMES + 1):
        w += any(r.randint(1, 6) == 6 for _ in range(4))
        out.append(w / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Pháp, thế kỷ mười bảy. Nhà quý tộc de Méré hay đặt cược: gieo một con xúc xắc bốn lần, '
                         'sẽ có ít nhất một mặt sáu. Ông thắng nhiều hơn thua. Xác suất thắng của ông là bao nhiêu?'),
    Beat('guess', 'hook', 'Hai phần ba, khoảng không phẩy năm một tám, hay đúng một phần hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cách nghĩ sai: mỗi lần một phần sáu, bốn lần là bốn phần sáu, bằng hai phần ba. '
                        'Nếu đúng thì gieo sáu lần sẽ chắc chắn ra mặt sáu, điều đó vô lý!'),
    Beat('s2', 'solve', 'Dùng biến cố đối: không lần nào ra sáu. Mỗi lần có năm phần sáu không ra sáu, các lần độc lập, '
                        'nên xác suất bằng năm phần sáu mũ bốn, bằng sáu trăm hai mươi lăm phần một nghìn hai trăm chín sáu.'),
    Beat('s3', 'solve', 'Vậy xác suất thắng bằng một trừ số đó, bằng sáu trăm bảy mươi mốt phần một nghìn hai trăm chín sáu, '
                        'khoảng không phẩy năm một tám. Mô phỏng hai nghìn ván cũng ra đúng như vậy.'),
    Beat('answer', 'solve', 'Đáp án: khoảng năm mươi mốt phẩy tám phần trăm. Hơn một nửa một chút, '
                            'đủ để de Méré thắng về lâu dài!'),
    Beat('outro', 'outro', outro_text(36)),
]

FORMULAS = formulas('671/1296 approx "0,518"', OPTIONS,
                    wrong='4 dot 1/6 = 2/3 quad coral(times)',
                    none='P(overline(A)) = (5/6)^4 = 625/1296',
                    prob='P(A) = 1 - 625/1296 = 671/1296')


def validate() -> bool:
    p = 1 - Fraction(5, 6) ** 4
    assert p == Fraction(671, 1296) and round(float(p), 3) == .518
    assert abs(wins()[-1] - float(p)) < .005 and wins()[-1] > .5
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS036(ShortScene):
    N = 36

    def hook_visual(self, t0):
        self.dice = VGroup(*[die(v, 1.05) for v in (2, 5, 6, 3)]).arrange(buff=.3).move_to([0, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.dice, lag_ratio=.3), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        w = self.M('wrong', 2.0)
        self.write_board(w)
        self.wait_until(.6, t0)
        self.write_board(tx('gieo 6 lần chắc chắn ra 6? Vô lý!', 28, CORAL, bold=True), anim='fade')

    def beat_s2(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.play(*[d[0].animate.set_stroke(GREEN, 5) for d in self.dice], run_time=self.rt(.06))
        self.write_board(tx('không lần nào ra 6', 30, GREEN, bold=True), anim='fade')
        self.wait_until(.4, t0)
        self.write_board(self.M('none', 1.8))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.7)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.clear_board(.02)
        self.run_sim(wins(), 'số ván:', 'tỉ lệ thắng:', .35, y=-1.6)



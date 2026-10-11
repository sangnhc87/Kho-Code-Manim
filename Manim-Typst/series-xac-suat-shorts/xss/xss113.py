"""XSS113 · Sưu tầm đủ 6 mặt — chờ mặt mới thứ k mất trung bình 6/(7 − k) lần: tổng 14,7."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import GOLD, GREEN  # noqa: E402
from common.visuals import die  # noqa: E402

EPISODE = {'code': 'XSS113', 'answer': '14,7'}
PROBLEM = ['Gieo xúc xắc cho đến khi thấy đủ cả $6$',
           'mặt. Trung bình cần bao nhiêu lần gieo?']
OPTIONS = ['6', '"14,7"', '36']
CORRECT = 1
ANSWER_VALUE = None
N, SEED = 1000, 16


def collect():
    r, tot, out = random.Random(SEED), 0, []
    for k in range(1, N + 1):
        seen, n = set(), 0
        while len(seen) < 6:
            seen.add(r.randint(1, 6))
            n += 1
        tot += n
        out.append(tot / k)
    return out


BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc cho đến khi đã thấy đủ cả sáu mặt. Giống như sưu tầm đủ bộ thẻ trong các gói bim bim. '
                         'Trung bình cần gieo bao nhiêu lần?'),
    Beat('guess', 'hook', 'Sáu lần, mười bốn phẩy bảy, hay ba mươi sáu? Ba, hai, một!'),
    Beat('s1', 'solve', 'Chia thành từng chặng. Mặt đầu tiên luôn mới: một lần. Khi đã có một mặt, mỗi lần gieo ra mặt mới '
                        'với xác suất năm phần sáu, nên chờ trung bình sáu phần năm lần.'),
    Beat('s2', 'solve', 'Cứ thế: chặng ba chờ sáu phần bốn, chặng bốn sáu phần ba, chặng năm sáu phần hai, '
                        'và mặt cuối cùng rất khó, chờ trung bình sáu lần.'),
    Beat('s3', 'solve', 'Cộng các chặng: một cộng một phẩy hai cộng một phẩy năm cộng hai cộng ba cộng sáu, '
                        'bằng mười bốn phẩy bảy lần. Mặt cuối cùng chiếm gần một nửa thời gian!'),
    Beat('s4', 'solve', 'Mô phỏng một nghìn lượt sưu tầm: số lần gieo trung bình bám sát mười bốn phẩy bảy.'),
    Beat('answer', 'solve', 'Đáp án: mười bốn phẩy bảy. Đó là lý do món thẻ cuối cùng trong bộ sưu tập luôn khó kiếm nhất!'),
    Beat('outro', 'outro', outro_text(113)),
]

FORMULAS = formulas('"14,7"', OPTIONS,
                    sum='E = 6/6 + 6/5 + 6/4 + 6/3 + 6/2 + 6/1',
                    val='E = 1 + "1,2" + "1,5" + 2 + 3 + 6 = "14,7"')


def validate() -> bool:
    assert sum(F(6, k) for k in range(1, 7)) == F(147, 10)
    assert abs(collect()[-1] - 14.7) < .05
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS113(ShortScene):
    N = 113

    def hook_visual(self, t0):
        self.board_top = -1.2
        self.faces = VGroup(*[die(v, .8) for v in range(1, 7)]).arrange(buff=.2).move_to([0, 1.8, 0])
        for d in self.faces:
            d.set_opacity(.2)
        self.wait_until(.4, t0)
        self.play(FadeIn(self.faces), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.faces[2].animate.set_opacity(1), run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.play(self.faces[4].animate.set_opacity(1), run_time=self.rt(.06))
        self.play(FadeIn(self.TM('chặng $2$: $6/5$', 28, GOLD).move_to([0, .6, 0])), run_time=self.rt(.05))

    def beat_s2(self, T):
        t0 = self.now()
        for i, k in enumerate((0, 5, 1)):
            self.wait_until(.15 + .22 * i, t0)
            self.play(self.faces[k].animate.set_opacity(1), run_time=self.rt(.05))
        self.wait_until(.8, t0)
        self.play(self.faces[3].animate.set_opacity(1), self.faces[3][0].animate.set_stroke(GOLD, 6), run_time=self.rt(.05))

    def beat_s3(self, T):
        t0 = self.now()
        self.write_board(self.M('sum', 1.5))
        self.wait_until(.45, t0)
        m = self.M('val', 1.5)
        self.write_board(m)
        self.frame(m)

    def beat_s4(self, T):
        self.clear_board(.03)
        self.run_sim(collect(), 'số lượt:', 'trung bình:', .6, y=-1.7, color=GREEN, nd=2)



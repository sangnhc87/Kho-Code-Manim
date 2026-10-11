"""XSS053 · Cùng nhóm — chia 6 bạn thành 2 nhóm 3: nhóm của A còn 2 chỗ cho 5 bạn → 2/5."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from manim import FadeIn, RoundedRectangle, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS053', 'answer': '2/5'}
PROBLEM = ['Chia ngẫu nhiên $6$ bạn thành $2$ nhóm, mỗi',
           'nhóm $3$ bạn. Xác suất A và B cùng nhóm?']
OPTIONS = ['1/2', '2/5', '1/3']
CORRECT = 1
ANSWER_VALUE = .4

BEATS = [
    Beat('hook', 'hook', 'Cô giáo chia ngẫu nhiên sáu bạn thành hai nhóm, mỗi nhóm ba bạn. A và B là đôi bạn thân. '
                         'Xác suất hai bạn được chung nhóm là bao nhiêu? Hai nhóm thì chắc một phần hai?'),
    Beat('guess', 'hook', 'Một phần hai, hai phần năm, hay một phần ba? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mẹo nhìn từ phía bạn A. Dù A ở nhóm nào, nhóm của A còn đúng hai chỗ trống, '
                        'và năm bạn còn lại có cơ hội như nhau để vào hai chỗ đó.'),
    Beat('s2', 'solve', 'Vậy xác suất B được vào một trong hai chỗ ấy là hai phần năm. '
                        'Không cần đếm cách chia nhóm phức tạp!'),
    Beat('s3', 'solve', 'Kiểm tra bằng cách đếm: chọn hai bạn đi cùng A từ năm bạn có mười cách, '
                        'trong đó có B ở bốn cách. Bốn phần mười, đúng bằng hai phần năm.'),
    Beat('answer', 'solve', 'Đáp án: hai phần năm, không phải một phần hai. Hãy đứng ở vị trí của một người để nhìn bài toán!'),
    Beat('outro', 'outro', outro_text(53)),
]

FORMULAS = formulas('2/5', OPTIONS,
                    seat='P = ("2 chỗ")/("5 bạn") = 2/5',
                    check='C_4^1/C_5^2 = 4/10 = 2/5')


def validate() -> bool:
    mates = list(combinations('BCDEF', 2))
    assert len(mates) == 10 and F(sum('B' in m for m in mates), 10) == F(2, 5)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS053(ShortScene):
    N = 53

    def hook_visual(self, t0):
        self.board_top = -1.05
        self.people = VGroup(*[token(c, GOLD if c in 'AB' else CYAN, .45) for c in 'ABCDEF']).arrange(buff=.25)
        self.people.move_to([0, 1.3, 0])
        self.wait_until(.5, t0)
        self.play(FadeIn(self.people, lag_ratio=.15), run_time=self.rt(.2))

    def beat_s1(self, T):
        t0 = self.now()
        grp = RoundedRectangle(width=3.6, height=1.4, corner_radius=.3, stroke_color=GREEN, stroke_width=5) \
            .move_to([-1.6, 2.0, 0])
        a = self.people[0]
        holes = VGroup(*[RoundedRectangle(width=.85, height=.85, corner_radius=.42, stroke_color=SOFT, stroke_width=3)
                         for _ in range(2)]).arrange(buff=.2).move_to(grp.get_center() + [.55, 0, 0])
        others = VGroup(*self.people[1:])
        self.play(FadeIn(grp), a.animate.move_to(grp.get_center() + [-1.1, 0, 0]),
                  others.animate.arrange(buff=.25).move_to([.6, .2, 0]), run_time=self.rt(.12))
        self.play(FadeIn(holes), run_time=self.rt(.05))
        self.play(FadeIn(tx('2 chỗ trống', 26, GREEN, bold=True).next_to(grp, [1, 0, 0], buff=.2)), run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.play(FadeIn(tx('5 bạn còn lại', 26, CYAN, bold=True).next_to(others, [0, -1, 0], buff=.2)),
                  run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        m = self.M('seat', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.write_board(self.M('check', 1.8), anim='fade')

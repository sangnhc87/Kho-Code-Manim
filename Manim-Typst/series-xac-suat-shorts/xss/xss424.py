"""XSS424 · Lớp 30 người, tháng sinh — 30 người, 12 tháng: nguyên lý Dirichlet ⇒ chắc chắn có 2 người cùng tháng (thậm chí ít nhất 3 người)."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS424', 'answer': '1 (chắc chắn)'}
PROBLEM = ['Lớp có $30$ học sinh. Xác suất có ít nhất',
           '$2$ bạn sinh cùng tháng?']
OPTIONS = ['1 ("chắc chắn")', 'approx "0,7"', 'approx "0,95"']
CORRECT = 0
ANSWER_VALUE = 1

BEATS = [
    Beat('hook', 'hook', 'Lớp có ba mươi học sinh. Xác suất có ít nhất hai bạn sinh cùng một tháng là bao nhiêu? Đừng vội tính!'),
    Beat('guess', 'hook', 'Chắc chắn, khoảng không phẩy bảy, hay khoảng không phẩy chín lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Một năm chỉ có mười hai tháng. Nếu mọi bạn sinh khác tháng nhau, lớp có nhiều nhất mười hai người.'),
    Beat('s2', 'solve', 'Ba mươi người lớn hơn mười hai, nên chắc chắn có hai bạn trùng tháng. Thậm chí có tháng có ít nhất ba bạn, vì mười hai nhân hai bằng hai mươi tư nhỏ hơn ba mươi.'),
    Beat('s3', 'solve', 'Xác suất bằng một: biến cố chắc chắn. Không cần công thức, chỉ cần nguyên lý chuồng bồ câu.'),
    Beat('answer', 'solve', 'Đáp án: một, chắc chắn. Trước khi tính xác suất, hãy kiểm tra xem biến cố có tất yếu không!'),
    Beat('outro', 'outro', outro_text(424)),
]

FORMULAS = formulas('1 ("chắc chắn")', OPTIONS,
                    pig='30 > 12 => "có 2 bạn cùng tháng"',
                    three='30 > 2 dot 12 => "có tháng" >= 3 "bạn"')


def validate() -> bool:
    assert 30 > 12 and 30 > 2 * 12
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS424(ShortScene):
    N = 424

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.months = VGroup(*[token(str(m), SOFT, .3) for m in range(1, 13)]).arrange_in_grid(rows=2, cols=6, buff=(.25, .35)).move_to([0, 1.3, 0])
        self.wait_until(.45, t0)
        self.play(FadeIn(self.months, lag_ratio=.05), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.play(*[m[0].animate.set_fill(CYAN) for m in self.months], run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(*[m[0].animate.set_fill(GOLD) for m in self.months], run_time=self.rt(.06))
        self.write_board(self.M('pig', 1.3))
        self.wait_until(.6, t0)
        self.write_board(self.M('three', 1.3))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(self.months.animate.scale(1.05), run_time=self.rt(.04))

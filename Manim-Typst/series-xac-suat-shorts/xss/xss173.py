"""XSS173 · Bắn tiếp phát hai — dự đoán sau cập nhật: 9/13·0,9 + 4/13·0,6 = 21/26."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, GREEN  # noqa: E402

EPISODE = {'code': 'XSS173', 'answer': '21/26'}
PROBLEM = ['Như thử thách trước: phát đầu đã trúng.',
           'Dùng lại khẩu súng đó bắn phát thứ',
           'hai. Xác suất lại trúng?']
OPTIONS = ['"0,78"', '21/26', '"0,81"']
CORRECT = 1
ANSWER_VALUE = 21 / 26
BRANCHES = [('tốt', CYAN, '9/13', [('T', GREEN, '"0,9"', [])]),
            ('th', GOLD, '4/13', [('T', GREEN, '"0,6"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: xạ thủ đã bắn trúng phát đầu. Giờ dùng lại đúng khẩu súng đó bắn phát thứ hai. '
                         'Xác suất lại trúng là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bảy tám, hai mươi mốt phần hai mươi sáu, hay không phẩy tám một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Sau phát trúng đầu tiên, ta đã cập nhật niềm tin: súng tốt chín phần mười ba, súng thường bốn phần mười ba. '
                        'Đây là cây mới cho phát thứ hai.'),
    Beat('s2', 'solve', 'Toàn phần với xác suất đã cập nhật: chín phần mười ba nhân không phẩy chín, cộng bốn phần mười ba nhân không phẩy sáu, '
                        'bằng hai mươi mốt phần hai mươi sáu.'),
    Beat('s3', 'solve', 'Khoảng không phẩy tám không tám, cao hơn không phẩy bảy tám của phát đầu. '
                        'Hai phát không độc lập: phát trúng đầu là bằng chứng súng tốt, nên phát sau dễ trúng hơn.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi mốt phần hai mươi sáu. Bayes rồi toàn phần: cập nhật niềm tin, sau đó dự đoán!'),
    Beat('outro', 'outro', outro_text(173)),
]

FORMULAS = formulas('21/26', OPTIONS,
                    tot='P = 9/13 dot "0,9" + 4/13 dot "0,6" = 21/26',
                    cmp='21/26 approx "0,808" > "0,78"')


def validate() -> bool:
    assert F(9, 13) * F(9, 10) + F(4, 13) * F(6, 10) == F(21, 26)
    both = F(3, 5) * F(81, 100) + F(2, 5) * F(36, 100)
    assert both / F(78, 100) == F(21, 26)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS173(TreeMixin, ShortScene):
    N = 173

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=5.6, root_label='sau phát 1')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.4, t0)
        m = self.M('tot', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.M('cmp', 1.9), anim='fade')



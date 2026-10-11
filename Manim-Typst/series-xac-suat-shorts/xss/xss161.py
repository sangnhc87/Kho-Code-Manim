"""XSS161 · Đi học muộn — toàn phần: 0,4·0,1 + 0,6·0,05 = 0,07."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS161', 'answer': '0,07'}
PROBLEM = ['$40%$ học sinh đi xe buýt; đi muộn',
           '$10%$ nếu đi buýt, $5%$ nếu tự đi. Xác',
           'suất một bạn đi học muộn?']
OPTIONS = ['"0,15"', '"0,07"', '"0,075"']
CORRECT = 1
ANSWER_VALUE = .07
BRANCHES = [('Bu', CYAN, '"0,4"', [('M', CORAL, '"0,1"', []), ('Đ', GREEN, '"0,9"', [])]),
            ('Tự', GOLD, '"0,6"', [('M', CORAL, '"0,05"', []), ('Đ', GREEN, '"0,95"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Bốn mươi phần trăm học sinh đi xe buýt. Đi xe buýt thì đi học muộn mười phần trăm, tự đi thì chỉ năm phần trăm. '
                         'Chọn ngẫu nhiên một bạn, xác suất bạn đó đi muộn là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy một lăm, không phẩy không bảy, hay không phẩy không bảy lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Đi muộn có hai nguyên nhân: đi xe buýt hoặc tự đi. Mỗi nguyên nhân là một nhánh của cây, '
                        'nhánh con là muộn hay đúng giờ.'),
    Beat('s2', 'solve', 'Nhánh xe buýt rồi muộn: không phẩy bốn nhân không phẩy một bằng không phẩy không bốn. '
                        'Nhánh tự đi rồi muộn: không phẩy sáu nhân không phẩy không năm bằng không phẩy không ba.'),
    Beat('s3', 'solve', 'Công thức xác suất toàn phần: cộng hai nhánh, được không phẩy không bảy. '
                        'Không phẩy không bảy lăm là lấy trung bình hai tỉ lệ, sai vì hai nhóm không đông như nhau.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy không bảy. Thử thách tiếp theo: biết một bạn đi muộn, bạn ấy có đi xe buýt không?'),
    Beat('outro', 'outro', outro_text(161)),
]

FORMULAS = formulas('"0,07"', OPTIONS,
                    bus='"0,4" dot "0,1" = "0,04"',
                    walk='"0,6" dot "0,05" = "0,03"',
                    tot='P(M) = "0,04" + "0,03" = "0,07"')


def validate() -> bool:
    assert round(.4 * .1 + .6 * .05, 2) == .07
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS161(TreeMixin, ShortScene):
    N = 161

    def hook_visual(self, t0):
        self.board_top = -1.65
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=6.8, root_label='học sinh')
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(tx('Bu: xe buýt   Tự: tự đi   M: muộn   Đ: đúng giờ', 20, SOFT).move_to([0, -1.2, 0])),
                  run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('bus', 2.0))
        self.wait_until(.5, t0)
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('walk', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 2.1)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.55, t0)
        self.write_board(self.TM('trung bình $"0,075"$: sai', 26, CORAL, bold=True), anim='fade')

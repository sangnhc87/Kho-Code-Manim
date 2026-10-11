"""XSS074 · Chuyển một bi — I: 3Đ 2X, II: 2Đ 2X; chuyển 1 bi I → II rồi rút ở II: 3/5·3/5 + 2/5·2/5 = 13/25."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import DOWN, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, PURPLE  # noqa: E402
from common.visuals import BALL_COLORS, urn  # noqa: E402

EPISODE = {'code': 'XSS074', 'answer': '13/25'}
PROBLEM = ['Hộp I: $3$ đỏ, $2$ xanh. Hộp II: $2$ đỏ, $2$',
           'xanh. Chuyển $1$ bi từ hộp I sang hộp II,',
           'rồi rút $1$ bi ở hộp II. $P("đỏ")$?']
OPTIONS = ['1/2', '13/25', '3/5']
CORRECT = 1
ANSWER_VALUE = 13 / 25
RED, BLUE = BALL_COLORS['R'], BALL_COLORS['B']
BRANCHES = [('Đ', RED, '3/5', [('Đ', RED, '3/5', []), ('X', BLUE, '2/5', [])]),
            ('X', BLUE, '2/5', [('Đ', RED, '2/5', []), ('X', BLUE, '3/5', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hộp một có ba đỏ hai xanh, hộp hai có hai đỏ hai xanh. Lấy ngẫu nhiên một viên ở hộp một '
                         'bỏ sang hộp hai, rồi rút một viên ở hộp hai. Xác suất được bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần hai, mười ba phần hai mươi lăm, hay ba phần năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Bước một quyết định hộp hai trông như thế nào. Chuyển bi đỏ, xác suất ba phần năm, '
                        'hộp hai thành ba đỏ hai xanh. Chuyển bi xanh, xác suất hai phần năm, hộp hai thành hai đỏ ba xanh.'),
    Beat('s2', 'solve', 'Nhánh chuyển đỏ rồi rút đỏ: ba phần năm nhân ba phần năm, bằng chín phần hai mươi lăm. '
                        'Nhánh chuyển xanh rồi rút đỏ: hai phần năm nhân hai phần năm, bằng bốn phần hai mươi lăm.'),
    Beat('s3', 'solve', 'Cộng lại: mười ba phần hai mươi lăm, nhỉnh hơn một nửa, vì hộp một nhiều bi đỏ hơn nên dễ chuyển '
                        'sang một viên đỏ. Dạng bài chuyển bi rất hay gặp trong đề thi mới.'),
    Beat('answer', 'solve', 'Đáp án: mười ba phần hai mươi lăm. Bài nhiều bước: mỗi bước một tầng của cây!'),
    Beat('outro', 'outro', outro_text(74)),
]

FORMULAS = formulas('13/25', OPTIONS,
                    rr='3/5 dot 3/5 = 9/25',
                    br='2/5 dot 2/5 = 4/25',
                    tot='P("đỏ") = 9/25 + 4/25 = 13/25')


def validate() -> bool:
    total = F(0)
    for moved in 'RRRBB':
        box2 = 'RRBB' + moved
        total += F(1, 5) * F(box2.count('R'), 5)
    assert total == F(13, 25)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS074(TreeMixin, ShortScene):
    N = 74

    def hook_visual(self, t0):
        self.urns = VGroup(urn('RRRBB', 5, .3), urn('RRBB', 4, .3)).arrange(buff=.7).move_to([0, 1.4, 0])
        labs = VGroup(tx('hộp I', 26, CYAN, bold=True).next_to(self.urns[0], DOWN, buff=.15),
                      tx('hộp II', 26, PURPLE, bold=True).next_to(self.urns[1], DOWN, buff=.15))
        self.labs = labs
        self.wait_until(.45, t0)
        self.play(FadeIn(self.urns, lag_ratio=.3), FadeIn(labs), run_time=self.rt(.15))
        moving = self.urns[0].balls[0]
        self.play(moving.animate.move_to(self.urns[1].get_top() + [0, .35, 0]), run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.urns.animate.set_opacity(0), self.labs.animate.set_opacity(0), run_time=self.rt(.04))
        self.remove(self.urns, self.labs)
        self.board_top = -1.0
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.2), dy=1.6, width=6.2, root_label='chuyển')
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.15))
        self.wait_until(.55, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(self.leaves[0][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('rr', 2.0))
        self.wait_until(.5, t0)
        self.play(self.leaves[2][0].animate.scale(1.3), run_time=self.rt(.05))
        self.write_board(self.M('br', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('tot', 2.0)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('mỗi bước = một tầng của cây', 26, GOLD, bold=True), anim='fade')



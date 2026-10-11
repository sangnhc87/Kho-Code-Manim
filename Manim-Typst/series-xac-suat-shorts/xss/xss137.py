"""XSS137 · Phong độ ảnh hưởng — cây 3 tầng, xác suất phụ thuộc trận trước: 0,105 + 0,06 + 0,14 = 0,305."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS137', 'answer': '0,305'}
PROBLEM = ['Trận $1$ thắng $"0,5"$; thắng trận trước thì',
           'trận sau thắng $"0,7"$, thua thì $"0,4"$.',
           'Xác suất thắng đúng $2$ trong $3$ trận?']
OPTIONS = ['"0,375"', '"0,305"', '"0,245"']
CORRECT = 1
ANSWER_VALUE = .305


def after(result, depth):
    if depth == 0:
        return []
    pw = '"0,7"' if result == 'T' else '"0,4"'
    pl = '"0,3"' if result == 'T' else '"0,6"'
    return [('T', CYAN, pw, after('T', depth - 1)), ('B', CORAL, pl, after('B', depth - 1))]


BRANCHES = [('T', CYAN, '"0,5"', after('T', 2)), ('B', CORAL, '"0,5"', after('B', 2))]

BEATS = [
    Beat('hook', 'hook', 'Một đội bóng chịu ảnh hưởng tâm lý: thắng trận trước thì trận sau thắng với xác suất không phẩy bảy, '
                         'thua trận trước thì chỉ không phẩy bốn. Trận đầu thắng không phẩy năm. '
                         'Xác suất thắng đúng hai trong ba trận là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy ba bảy lăm, không phẩy ba không năm, hay không phẩy hai bốn lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Các trận không độc lập, nên không dùng được công thức Bernoulli. Vẽ cây ba tầng, '
                        'xác suất trên mỗi nhánh phụ thuộc vào kết quả ngay trước nó.'),
    Beat('s2', 'solve', 'Ba lá có đúng hai trận thắng: thắng thắng thua, không phẩy một không năm; thắng thua thắng, không phẩy không sáu; '
                        'thua thắng thắng, không phẩy một bốn.'),
    Beat('s3', 'solve', 'Cộng lại: không phẩy ba không năm. Không phẩy ba bảy lăm là đáp án sai nếu coi các trận độc lập với xác suất một phần hai.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy ba không năm. Khi các lần thử phụ thuộc nhau, sơ đồ cây là công cụ an toàn nhất!'),
    Beat('outro', 'outro', outro_text(137)),
]

FORMULAS = formulas('"0,305"', OPTIONS,
                    ttb='T T B: "0,5" dot "0,7" dot "0,3" = "0,105"',
                    tbt='T B T: "0,5" dot "0,3" dot "0,4" = "0,06"',
                    btt='B T T: "0,5" dot "0,4" dot "0,7" = "0,14"',
                    tot='P = "0,105" + "0,06" + "0,14" = "0,305"')


def validate() -> bool:
    assert round(.5 * .7 * .3 + .5 * .3 * .4 + .5 * .4 * .7, 3) == .305
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS137(TreeMixin, ShortScene):
    N = 137

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.2, width=7.4, root_label='trận 1', r=.3,
                                                  edge_size=22)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.35, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(FadeIn(self.levels[3], lag_ratio=.08), run_time=self.rt(.2))
        self.play(FadeIn(tx('T: thắng   B: thua', 22, SOFT).move_to([0, -1.2, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        two = [n for n, path in self.leaves if [b[0] for b in path].count('T') == 2]
        self.play(*[n.animate.scale(1.4).set_stroke(GREEN, 4) for n in two], run_time=self.rt(.05))
        self.wait_until(.12, t0)
        self.write_board(self.M('ttb', 1.5))
        self.wait_until(.4, t0)
        self.write_board(self.M('tbt', 1.5))
        self.wait_until(.68, t0)
        self.write_board(self.M('btt', 1.5))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('tot', 1.9)
        self.write_board(m)
        self.frame(m)

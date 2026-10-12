"""XSS255 · Tham số sau khi chuyển bi — 3/4·(a + 1)/(a + 3) + 1/4·a/(a + 3) = 5/8 ⇒ a = 3."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD  # noqa: E402

EPISODE = {'code': 'XSS255', 'answer': 'a = 3'}
PROBLEM = ['Chuyển $1$ bi từ hộp I ($3$ đỏ $1$ xanh) sang',
           'hộp II ($a$ đỏ $2$ xanh), rồi rút từ II:',
           'xác suất đỏ là $5/8$. Tìm $a$.']
OPTIONS = ['a = 2', 'a = 3', 'a = 5']
CORRECT = 1
ANSWER_VALUE = None
BRANCHES = [('Đ', CORAL, '3/4', [('Đ', GOLD, '(a + 1)/(a + 3)', [])]),
            ('X', CYAN, '1/4', [('Đ', GOLD, 'a/(a + 3)', [])])]

BEATS = [
    Beat('hook', 'hook', 'Chuyển một bi từ hộp một có ba đỏ một xanh sang hộp hai có a bi đỏ và hai bi xanh. Rút một bi từ hộp hai, '
                         'xác suất được đỏ là năm phần tám. Hộp hai lúc đầu có mấy bi đỏ?'),
    Beat('guess', 'hook', 'Hai, ba, hay năm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Sau khi chuyển, hộp hai có a cộng ba bi. Chuyển đỏ: a cộng một bi đỏ. Chuyển xanh: vẫn a bi đỏ.'),
    Beat('s2', 'solve', 'Toàn phần: ba phần tư nhân a cộng một chia a cộng ba, cộng một phần tư nhân a chia a cộng ba, bằng bốn a cộng ba chia bốn lần a cộng ba.'),
    Beat('s3', 'solve', 'Đặt bằng năm phần tám: tám lần bốn a cộng ba bằng hai mươi lần a cộng ba, ba mươi hai a cộng hai mươi tư bằng hai mươi a cộng sáu mươi, a bằng ba.'),
    Beat('answer', 'solve', 'Đáp án: a bằng ba. Chuyển bi có tham số: gộp các nhánh cùng mẫu rồi giải!'),
    Beat('outro', 'outro', outro_text(255)),
]

FORMULAS = formulas('a = 3', OPTIONS,
                    tot='3/4 dot (a + 1)/(a + 3) + 1/4 dot a/(a + 3) = (4 a + 3)/(4 (a + 3))',
                    sol='(4 a + 3)/(4 (a + 3)) = 5/8 arrow.r.double a = 3')


def validate() -> bool:
    assert [a for a in range(100) if F(3, 4) * F(a + 1, a + 3) + F(1, 4) * F(a, a + 3) == F(5, 8)] == [3]
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS255(TreeMixin, ShortScene):
    N = 255

    def hook_visual(self, t0):
        self.board_top = -1.45
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.95), dy=1.75, width=5.6, root_label='bi chuyển',
                                                  edge_size=26)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.15))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('tot', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 1.6)
        self.write_board(m)
        self.frame(m)

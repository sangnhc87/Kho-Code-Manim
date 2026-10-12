"""XSS363 · Chẵn hộp I, lẻ hộp II — I (3đ2x), II (1đ4x), rút 2 bi; P(R1R2) = ½·3/10 + 0 = 3/20, P(R2) = ½·3/5 + ½·1/5 = 2/5 → 3/8."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS363', 'answer': '3/8'}
PROBLEM = ['Xúc xắc chẵn: hộp I ($3$ đỏ $2$ xanh), lẻ:',
           'hộp II ($1$ đỏ $4$ xanh); rút lần lượt $2$ bi.',
           'Biết bi thứ hai đỏ. $P("bi đầu đỏ")$?']
OPTIONS = ['3/8', '1/2', '3/10']
CORRECT = 0
ANSWER_VALUE = 3 / 8
BRANCHES = [('I', GOLD, '1/2', [('Đ', CORAL, '3/5', [('Đ', CORAL, '1/2', [])]), ('X', CYAN, '2/5', [('Đ', CORAL, '3/4', [])])]),
            ('II', PURPLE, '1/2', [('Đ', CORAL, '1/5', [('Đ', CORAL, '0', [])]), ('X', CYAN, '4/5', [('Đ', CORAL, '1/4', [])])])]


def leaves():
    out = {}
    for box, (r, b) in (('I', (3, 2)), ('II', (1, 4))):
        n = r + b
        out[box, 'RR'] = F(1, 2) * F(r, n) * F(r - 1, n - 1)
        out[box, 'BR'] = F(1, 2) * F(b, n) * F(r, n - 1)
    return out


BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc: chẵn thì rút từ hộp một gồm ba đỏ hai xanh, lẻ thì rút từ hộp hai gồm một đỏ bốn xanh. Rút lần lượt hai bi. '
                         'Biết bi thứ hai đỏ, xác suất bi thứ nhất cũng đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần tám, một phần hai, hay ba phần mười? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây ba tầng: chọn hộp, bi thứ nhất, bi thứ hai. Có bốn lá kết thúc bằng bi thứ hai đỏ.'),
    Beat('s2', 'solve', 'Hộp một: đỏ đỏ là ba phần mười, xanh đỏ cũng ba phần mười. Hộp hai: đỏ đỏ bằng không vì chỉ một bi đỏ, xanh đỏ là một phần năm. Mỗi cái nhân một phần hai.'),
    Beat('s3', 'solve', 'Bi thứ hai đỏ: ba phần hai mươi cộng ba phần hai mươi cộng một phần mười, bằng hai phần năm. Cả hai đỏ: ba phần hai mươi. Chia ra ba phần tám.'),
    Beat('answer', 'solve', 'Đáp án: ba phần tám. Điều kiện ở lần rút sau vẫn xử lý được bằng cách gom lá trên cây.'),
    Beat('outro', 'outro', outro_text(363)),
]

FORMULAS = formulas('3/8', OPTIONS,
                    leafs='"I": 3/10, 3/10; quad "II": 0, 1/5',
                    den='P(Đ_2) = 1/2 (3/10 + 3/10) + 1/2 (0 + 1/5) = 2/5',
                    prob='P(Đ_1 | Đ_2) = (3/20)/(2/5) = 3/8')


def validate() -> bool:
    lv = leaves()
    num = lv['I', 'RR'] + lv['II', 'RR']
    den = num + lv['I', 'BR'] + lv['II', 'BR']
    assert den == F(2, 5) and num / den == F(3, 8)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS363(TreeMixin, ShortScene):
    N = 363

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.3, width=6.8, r=.3, edge_size=24)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2], lag_ratio=.2), FadeIn(self.levels[3], lag_ratio=.2), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('leafs', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        self.write_board(self.M('den', 1.3))
        self.wait_until(.6, t0)
        m = self.M('prob', 1.5)
        self.write_board(m)
        self.frame(m)

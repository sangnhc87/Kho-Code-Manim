"""XSS367 · Chọn hộp, chuyển, rồi rút — 1–4: I → II rồi rút II; 5–6: II → I rồi rút I: 2/3(2/3·1/2 + 1/3·1/4) + 1/3(1/3·3/4 + 2/3·1/2) = 17/36."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, PURPLE  # noqa: E402

EPISODE = {'code': 'XSS367', 'answer': '17/36'}
PROBLEM = ['Xúc xắc $1$–$4$: chuyển $1$ bi từ I ($2$ đỏ $1$',
           'xanh) sang II ($1$ đỏ $2$ xanh); $5$–$6$: chuyển',
           'ngược lại. Rút $1$ bi từ hộp nhận. $P(Đ)$?']
OPTIONS = ['1/2', '17/36', '4/9']
CORRECT = 1
ANSWER_VALUE = 17 / 36
BRANCHES = [('I→II', GOLD, '2/3', [('Đ', CORAL, '2/3', [('Đ', CORAL, '1/2', [])]), ('X', CYAN, '1/3', [('Đ', CORAL, '1/4', [])])]),
            ('II→I', PURPLE, '1/3', [('Đ', CORAL, '1/3', [('Đ', CORAL, '3/4', [])]), ('X', CYAN, '2/3', [('Đ', CORAL, '1/2', [])])])]


def total():
    a = F(2, 3) * (F(2, 3) * F(2, 4) + F(1, 3) * F(1, 4))
    b = F(1, 3) * (F(1, 3) * F(3, 4) + F(2, 3) * F(2, 4))
    return a, b


BEATS = [
    Beat('hook', 'hook', 'Gieo xúc xắc. Ra một đến bốn: chuyển một bi từ hộp một, hai đỏ một xanh, sang hộp hai, một đỏ hai xanh. Ra năm, sáu: chuyển ngược lại. '
                         'Sau đó rút một bi từ hộp vừa nhận. Xác suất bi đỏ?'),
    Beat('guess', 'hook', 'Một phần hai, mười bảy phần ba mươi sáu, hay bốn phần chín? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây ba tầng: chiều chuyển, màu bi chuyển, màu bi rút. Chiều một sang hai có xác suất hai phần ba.'),
    Beat('s2', 'solve', 'Chuyển đỏ sang hộp hai: hộp thành hai đỏ hai xanh, rút đỏ một phần hai. Chuyển xanh: một đỏ ba xanh, một phần tư. Nhánh này cho hai phần ba nhân năm phần mười hai.'),
    Beat('s3', 'solve', 'Chiều ngược lại, hộp một nhận bi: nhận đỏ thì ba phần tư, nhận xanh thì một phần hai. Nhánh này cho một phần ba nhân bảy phần mười hai.'),
    Beat('s4', 'solve', 'Cộng: mười phần ba mươi sáu cộng bảy phần ba mươi sáu, bằng mười bảy phần ba mươi sáu.'),
    Beat('answer', 'solve', 'Đáp án: mười bảy phần ba mươi sáu. Ba hành động nối nhau, cây ba tầng xử lý gọn gàng.'),
    Beat('outro', 'outro', outro_text(367)),
]

FORMULAS = formulas('17/36', OPTIONS,
                    a='2/3 (2/3 dot 1/2 + 1/3 dot 1/4) = 10/36',
                    b='1/3 (1/3 dot 3/4 + 2/3 dot 1/2) = 7/36',
                    prob='P(Đ) = 10/36 + 7/36 = 17/36')


def validate() -> bool:
    a, b = total()
    assert (a, b) == (F(10, 36), F(7, 36)) and a + b == F(17, 36)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS367(TreeMixin, ShortScene):
    N = 367

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.7), dy=1.3, width=6.8, r=.32, edge_size=24)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.play(FadeIn(self.levels[1]), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][:len(self.levels[2]) // 2]), FadeIn(self.levels[3][:len(self.levels[3]) // 2]), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.write_board(self.M('a', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2][len(self.levels[2]) // 2:]), FadeIn(self.levels[3][len(self.levels[3]) // 2:]), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.write_board(self.M('b', 1.4))

    def beat_s4(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.6)
        self.write_board(m)
        self.frame(m)

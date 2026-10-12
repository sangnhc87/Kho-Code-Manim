"""XSS394 · Hai xét nghiệm trái ngược — bệnh 2 %; A+: 0,9 / 0,1; B−: 0,2 / 0,95: 0,02·0,9·0,2 = 0,0036 vs 0,98·0,1·0,95 = 0,0931 → 36/967."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402

EPISODE = {'code': 'XSS394', 'answer': '36/967 ≈ 0,037'}
PROBLEM = ['Bệnh $2 %$. Test A: nhạy $"0,9"$, dương giả',
           '$"0,1"$; test B: nhạy $"0,8"$, dương giả $"0,05"$.',
           'A dương, B âm. Xác suất người đó bệnh?']
OPTIONS = ['36/967 approx "0,037"', '"0,18"', '"0,02"']
CORRECT = 0
ANSWER_VALUE = 36 / 967
D = F(2, 100)
SICK = D * F(9, 10) * F(2, 10)
WELL = (1 - D) * F(1, 10) * F(95, 100)
BRANCHES = [('B', CORAL, '"0,02"', [('A+', GOLD, '"0,9"', [('B−', GREEN, '"0,2"', [])])]),
            ('K', CYAN, '"0,98"', [('A+', GOLD, '"0,1"', [('B−', GREEN, '"0,95"', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Một bệnh có tỉ lệ hai phần trăm. Xét nghiệm A có độ nhạy không phẩy chín, dương tính giả không phẩy một. Xét nghiệm B nhạy không phẩy tám, dương giả không phẩy không năm. '
                         'Một người có A dương nhưng B âm. Xác suất người đó bệnh?'),
    Beat('guess', 'hook', 'Khoảng không phẩy không ba bảy, không phẩy một tám, hay không phẩy không hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây ba tầng: có bệnh hay không, kết quả A, kết quả B. Hai xét nghiệm độc lập khi biết tình trạng bệnh.'),
    Beat('s2', 'solve', 'Nhánh bệnh: không phẩy không hai nhân không phẩy chín nhân không phẩy hai, vì B âm khi bệnh với xác suất một trừ không phẩy tám. Bằng không phẩy không không ba sáu.'),
    Beat('s3', 'solve', 'Nhánh khỏe: không phẩy chín tám nhân không phẩy một nhân không phẩy chín lăm, bằng không phẩy không chín ba một.'),
    Beat('s4', 'solve', 'Bayes: ba mươi sáu chia ba mươi sáu cộng chín trăm ba mươi mốt, bằng ba mươi sáu phần chín trăm sáu mươi bảy, khoảng ba phẩy bảy phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: khoảng không phẩy không ba bảy. Kết quả âm của xét nghiệm B gần như xóa sạch cảnh báo của A.'),
    Beat('outro', 'outro', outro_text(394)),
]

FORMULAS = formulas('36/967 approx "0,037"', OPTIONS,
                    sick='"0,02" dot "0,9" dot "0,2" = "0,0036"',
                    well='"0,98" dot "0,1" dot "0,95" = "0,0931"',
                    prob='P = ("0,0036")/("0,0036" + "0,0931") = 36/967')


def validate() -> bool:
    assert SICK / (SICK + WELL) == F(36, 967)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS394(TreeMixin, ShortScene):
    N = 394

    def hook_visual(self, t0):
        self.board_top = -1.6
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.25, width=5.0, r=.36, edge_size=26)
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1]), run_time=self.rt(.05))

    def beat_s1(self, T):
        self.play(FadeIn(self.levels[2]), FadeIn(self.levels[3]), run_time=self.rt(.2))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.5, t0)
        self.write_board(self.M('sick', 1.4))

    def beat_s3(self, T):
        t0 = self.now()
        self.wait_until(.4, t0)
        self.write_board(self.M('well', 1.4))

    def beat_s4(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.4)
        self.write_board(m)
        self.frame(m)

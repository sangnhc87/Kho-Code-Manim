"""XSS218 · Bi chuyển màu gì? — Bayes trên cây XSS217: (9/50)/(11/50) = 9/11."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL  # noqa: E402
from xss.xss217 import BRANCHES  # noqa: E402

EPISODE = {'code': 'XSS218', 'answer': '9/11'}
PROBLEM = ['Như trên (chuyển $1$ bi từ I: $3$ đỏ $2$ xanh',
           'sang II: $2$ đỏ $2$ xanh), biết $2$ bi rút từ',
           'II đều đỏ. Xác suất bi chuyển là đỏ?']
OPTIONS = ['3/5', '9/11', '3/4']
CORRECT = 1
ANSWER_VALUE = 9 / 11

BEATS = [
    Beat('hook', 'hook', 'Tiếp thử thách trước: bạn không thấy bi nào được chuyển, chỉ thấy hai bi rút từ hộp hai đều đỏ. '
                         'Xác suất bi đã chuyển sang là bi đỏ là bao nhiêu?'),
    Beat('guess', 'hook', 'Ba phần năm, chín phần mười một, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hai lá "hai đỏ" trên cây: chuyển đỏ rồi hai đỏ, chín phần năm mươi; chuyển xanh rồi hai đỏ, hai phần năm mươi.'),
    Beat('s2', 'solve', 'Bayes: chín phần năm mươi chia mười một phần năm mươi, bằng chín phần mười một.'),
    Beat('s3', 'solve', 'Trước khi rút, bi chuyển là đỏ với xác suất ba phần năm. Thấy hai đỏ, niềm tin tăng lên khoảng tám mươi hai phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: chín phần mười một. Kết quả ở hộp sau là bằng chứng về bi đã chuyển ở bước trước!'),
    Beat('outro', 'outro', outro_text(218)),
]

FORMULAS = formulas('9/11', OPTIONS,
                    bayes='P("chuyển Đ" | Đ Đ) = (9/50)/(9/50 + 2/50) = 9/11')


def validate() -> bool:
    assert F(9, 50) / F(11, 50) == F(9, 11)
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS218(TreeMixin, ShortScene):
    N = 218

    def hook_visual(self, t0):
        self.board_top = -1.4
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.0), dy=1.75, width=5.6, root_label='bi chuyển')
        self.wait_until(.6, t0)
        self.play(*[FadeIn(lv) for lv in self.levels], run_time=self.rt(.12))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(*[n.animate.scale(1.25) for n, _ in self.leaves], run_time=self.rt(.05))
        self.wait_until(.4, t0)
        self.write_board(self.TM('$9/50$ và $2/50$', 30))

    def beat_s2(self, T):
        self.clear_board(.03)
        m = self.M('bayes', 1.8)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        self.write_board(self.TM('$3/5$ → $9/11$', 30, CORAL, bold=True), anim='fade')

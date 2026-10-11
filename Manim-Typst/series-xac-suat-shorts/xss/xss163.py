"""XSS163 · Nhân chứng taxi (Kahneman) — trong 100 xe: 12 xanh dương bị nói đúng, 17 xanh lá bị nói nhầm: 12/29."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, CountTreeMixin, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS163', 'answer': '12/29 ≈ 0,41'}
PROBLEM = ['$85%$ taxi màu xanh lá, $15%$ xanh dương.',
           'Nhân chứng nhận đúng màu $80%$, khai',
           '"xanh dương". Xác suất đúng?']
OPTIONS = ['"0,8"', '12/29 approx "0,41"', '"0,15"']
CORRECT = 1
ANSWER_VALUE = 12 / 29

BEATS = [
    Beat('hook', 'hook', 'Một taxi gây tai nạn rồi bỏ chạy. Thành phố có tám mươi lăm phần trăm taxi xanh lá, mười lăm phần trăm xanh dương. '
                         'Nhân chứng nhận đúng màu tám mươi phần trăm, và khai đó là xe xanh dương. Xác suất xe thật sự xanh dương?'),
    Beat('guess', 'hook', 'Không phẩy tám, khoảng không phẩy bốn một, hay không phẩy một lăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hình dung một trăm chiếc taxi: mười lăm xe xanh dương, tám mươi lăm xe xanh lá. '
                        'Nhân chứng nói đúng màu tám mươi phần trăm.'),
    Beat('s2', 'solve', 'Xe xanh dương được khai đúng là xanh dương: mười hai xe. Xe xanh lá bị khai nhầm thành xanh dương: '
                        'hai mươi phần trăm của tám mươi lăm, bằng mười bảy xe!'),
    Beat('s3', 'solve', 'Có hai mươi chín lần khai "xanh dương", chỉ mười hai lần đúng: xác suất mười hai phần hai mươi chín, '
                        'khoảng bốn mươi mốt phần trăm. Xe xanh lá quá đông nên lời khai nhầm lấn át lời khai đúng.'),
    Beat('answer', 'solve', 'Đáp án: mười hai phần hai mươi chín. Đây là "bỏ quên tỉ lệ nền", lỗi mà cả tòa án cũng từng mắc!'),
    Beat('outro', 'outro', outro_text(163)),
]

FORMULAS = formulas('12/29 approx "0,41"', OPTIONS,
                    cnt='12 " đúng", quad 17 " nhầm"',
                    prob='P = 12/(12 + 17) = 12/29 approx "0,41"')


def validate() -> bool:
    assert F(15 * 80, 15 * 80 + 85 * 20) == F(12, 29)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS163(CountTreeMixin, ShortScene):
    N = 163

    def hook_visual(self, t0):
        self.board_top = -1.25
        self.levels, self.nodes = self.count_tree(100, [
            (15, CYAN, 'xanh dương', [(12, CYAN, 'nói XD', []), (3, SOFT, 'nói XL', [])]),
            (85, GREEN, 'xanh lá', [(17, CORAL, 'nói XD', []), (68, SOFT, 'nói XL', [])])],
            top=2.9, dy=1.55, width=6.9)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.25, t0)
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.15), run_time=self.rt(.15))
        self.play(self.nodes[1].animate.scale(1.25), run_time=self.rt(.05))
        self.wait_until(.45, t0)
        self.play(self.nodes[4].animate.scale(1.25), run_time=self.rt(.05))
        self.play(FadeIn(tx('XD: xanh dương   XL: xanh lá', 22, SOFT).move_to([0, -.9, 0])), run_time=self.rt(.04))
        self.write_board(self.M('cnt', 2.0))

    def beat_s3(self, T):
        t0 = self.now()
        self.clear_board(.03)
        m = self.M('prob', 1.9)
        self.write_board(m)
        self.frame(m)
        self.wait_until(.6, t0)
        self.write_board(tx('bỏ quên tỉ lệ nền', 28, GOLD, bold=True), anim='fade')

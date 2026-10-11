"""XSS123 · Ném rổ tối đa ba lần — chỉ một nhánh thất bại: 1 − 0,3³ = 0,973."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS123', 'answer': '0,973'}
PROBLEM = ['Ném rổ đến khi vào thì dừng, tối',
           'đa $3$ lần, mỗi lần vào với xác suất',
           '$"0,7"$. Xác suất ném vào?']
OPTIONS = ['"0,7"', '"0,973"', '"0,91"']
CORRECT = 1
ANSWER_VALUE = .973
BRANCHES = [('V', GREEN, '"0,7"', []),
            ('T', CORAL, '"0,3"', [('V', GREEN, '"0,7"', []),
                                   ('T', CORAL, '"0,3"', [('V', GREEN, '"0,7"', []), ('T', CORAL, '"0,3"', [])])])]

BEATS = [
    Beat('hook', 'hook', 'Bạn được ném rổ tối đa ba lần, vào là dừng. Mỗi lần ném vào với xác suất không phẩy bảy. '
                         'Xác suất cuối cùng bạn ném vào rổ là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy bảy, không phẩy chín bảy ba, hay không phẩy chín một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Cây dừng sớm: ném vào thì nhánh kết thúc, trượt thì ném tiếp. '
                        'Có ba nhánh thành công nhưng chỉ đúng một nhánh thất bại: trượt cả ba lần.'),
    Beat('s2', 'solve', 'Nhánh thất bại có xác suất không phẩy ba mũ ba, bằng không phẩy không hai bảy. '
                        'Lấy biến cố đối: một trừ không phẩy không hai bảy, bằng không phẩy chín bảy ba.'),
    Beat('s3', 'solve', 'Kiểm tra bằng cách cộng ba nhánh thành công: không phẩy bảy, cộng không phẩy hai mốt, '
                        'cộng không phẩy không sáu ba. Cùng ra không phẩy chín bảy ba. Không phẩy chín một là đáp án nếu chỉ ném hai lần.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín bảy ba. Khi cây có nhiều nhánh tốt mà ít nhánh xấu, hãy tính nhánh xấu rồi lấy phần bù!'),
    Beat('outro', 'outro', outro_text(123)),
]

FORMULAS = formulas('"0,973"', OPTIONS,
                    miss='P("trượt cả 3") = "0,3"^3 = "0,027"',
                    comp='P = 1 - "0,027" = "0,973"',
                    sum='"0,7" + "0,21" + "0,063" = "0,973"')


def validate() -> bool:
    assert round(1 - .3 ** 3, 3) == .973 == round(.7 + .3 * .7 + .09 * .7, 3)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS123(TreeMixin, ShortScene):
    N = 123

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 3.05), dy=1.25, width=6.4, root_label='ném', r=.4,
                                                  edge_size=30)
        self.wait_until(.55, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.1))
        self.play(FadeIn(tx('V: vào   T: trượt', 24, SOFT).move_to([0, -1.15, 0])), run_time=self.rt(.04))
        self.wait_until(.6, t0)
        self.play(self.leaves[-1][0].animate.scale(1.4), run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.write_board(self.M('miss', 1.9))
        self.wait_until(.5, t0)
        m = self.M('comp', 2.1)
        self.write_board(m)
        self.frame(m)

    def beat_s3(self, T):
        t0 = self.now()
        self.play(*[n.animate.scale(1.3) for n, _ in self.leaves[:-1]], run_time=self.rt(.06))
        self.wait_until(.3, t0)
        self.write_board(self.M('sum', 1.8), anim='fade')

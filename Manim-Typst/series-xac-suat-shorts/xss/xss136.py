"""XSS136 · Máy dự phòng — 0,9 + 0,1·0,8·0,9 = 0,972."""
from __future__ import annotations

import sys
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS136', 'answer': '0,972'}
PROBLEM = ['Máy chính hỏng với xác suất $"0,1"$; khi đó',
           'máy phụ khởi động được $"0,8"$ và chạy tốt',
           '$"0,9"$. Xác suất hệ thống vẫn chạy?']
OPTIONS = ['"0,9"', '"0,972"', '"0,98"']
CORRECT = 1
ANSWER_VALUE = .972
OK, NO = ('✓', GREEN), ('✗', CORAL)
BRANCHES = [(*OK, '"0,9"', []),
            (*NO, '"0,1"', [(*OK, '"0,8"', [(*OK, '"0,9"', []), (*NO, '"0,1"', [])]), (*NO, '"0,2"', [])])]

BEATS = [
    Beat('hook', 'hook', 'Bệnh viện có máy phát điện chính, hỏng với xác suất không phẩy một. Khi máy chính hỏng, '
                         'máy phụ khởi động được với xác suất không phẩy tám, và nếu khởi động thì chạy tốt không phẩy chín. '
                         'Xác suất bệnh viện vẫn có điện là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy chín, không phẩy chín bảy hai, hay không phẩy chín tám? Ba, hai, một!'),
    Beat('s1', 'solve', 'Tầng một: máy chính chạy hay hỏng. Chỉ nhánh hỏng mới mở tiếp: máy phụ có khởi động không, '
                        'rồi có chạy tốt không. Đây là cây không đối xứng.'),
    Beat('s2', 'solve', 'Hai lá có điện: máy chính chạy, không phẩy chín; hoặc hỏng rồi máy phụ khởi động và chạy tốt, '
                        'không phẩy một nhân không phẩy tám nhân không phẩy chín, bằng không phẩy không bảy hai.'),
    Beat('s3', 'solve', 'Cộng lại: không phẩy chín bảy hai. Máy phụ giảm khả năng mất điện từ mười phần trăm xuống còn hai phẩy tám phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy chín bảy hai. Dự phòng chính là lý do các hệ thống quan trọng luôn có hai lớp!'),
    Beat('outro', 'outro', outro_text(136)),
]

FORMULAS = formulas('"0,972"', OPTIONS,
                    b2='"0,1" dot "0,8" dot "0,9" = "0,072"',
                    tot='P = "0,9" + "0,072" = "0,972"')


def validate() -> bool:
    assert round(.9 + .1 * .8 * .9, 3) == .972
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS136(TreeMixin, ShortScene):
    N = 136

    def hook_visual(self, t0):
        self.board_top = -1.8
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.25, width=6.4, root_label='máy chính', r=.38,
                                                  edge_size=28)
        self.wait_until(.7, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.04))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.35, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.3), run_time=self.rt(.1))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.levels[3], lag_ratio=.3), run_time=self.rt(.1))
        self.play(FadeIn(tx('✓: có điện   ✗: mất điện', 24, SOFT).move_to([0, -1.45, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        good = [n for n, path in self.leaves if path[-1][0] == '✓']
        self.play(*[n.animate.scale(1.35) for n in good], run_time=self.rt(.06))
        self.wait_until(.45, t0)
        self.write_board(self.M('b2', 1.9))

    def beat_s3(self, T):
        m = self.M('tot', 2.1)
        self.write_board(m)
        self.frame(m)

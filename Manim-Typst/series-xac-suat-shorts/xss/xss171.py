"""XSS171 · Câu hỏi nhạy cảm (randomized response) — 0,5·p + 0,5·1 = 0,6 ⇒ p = 0,2."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import tx  # noqa: E402
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN, SOFT  # noqa: E402

EPISODE = {'code': 'XSS171', 'answer': '20 %'}
PROBLEM = ['Mỗi bạn tung xu bí mật: ngửa thì trả lời',
           'thật "có quay cóp không?", sấp thì nói "có".',
           '$60%$ nói "có". Tỉ lệ thật sự quay cóp?']
OPTIONS = ['"10" %', '"20" %', '"60" %']
CORRECT = 1
ANSWER_VALUE = .2
BRANCHES = [('N', GOLD, '1/2', [('có', CORAL, 'p', []), ('ko', GREEN, '1 - p', [])]),
            ('S', CYAN, '1/2', [('có', CORAL, '1', [])])]

BEATS = [
    Beat('hook', 'hook', 'Hỏi thẳng "bạn có quay cóp không" thì ai cũng nói không. Nhà thống kê dùng mẹo: mỗi bạn tung xu bí mật. '
                         'Ngửa thì trả lời thật, sấp thì cứ nói "có". Kết quả: sáu mươi phần trăm nói "có". Tỉ lệ thật sự quay cóp là bao nhiêu?'),
    Beat('guess', 'hook', 'Mười phần trăm, hai mươi phần trăm, hay sáu mươi phần trăm? Ba, hai, một!'),
    Beat('s1', 'solve', 'Không ai biết một bạn nói "có" vì thật hay vì đồng xu, nên các bạn yên tâm trả lời. '
                        'Gọi p là tỉ lệ thật sự quay cóp, vẽ cây theo kết quả đồng xu.'),
    Beat('s2', 'solve', 'Xác suất nói "có" theo công thức toàn phần: một phần hai nhân p, cộng một phần hai nhân một. '
                        'Đặt bằng không phẩy sáu.'),
    Beat('s3', 'solve', 'Giải ra: một phần hai p bằng không phẩy một, nên p bằng không phẩy hai, tức hai mươi phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: hai mươi phần trăm. Xác suất toàn phần giúp khảo sát câu hỏi nhạy cảm mà vẫn giữ bí mật cho từng người!'),
    Beat('outro', 'outro', outro_text(171)),
]

FORMULAS = formulas('"20" %', OPTIONS,
                    eq='1/2 dot p + 1/2 dot 1 = "0,6"',
                    sol='p = 2 dot ("0,6" - "0,5") = "0,2"')


def validate() -> bool:
    p = (F(3, 5) - F(1, 2)) * 2
    assert p == F(1, 5)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS171(TreeMixin, ShortScene):
    N = 171

    def hook_visual(self, t0):
        self.board_top = -1.55
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.8), dy=1.6, width=6.4, root_label='tung xu bí mật')
        self.wait_until(.75, t0)
        self.play(FadeIn(self.levels[0]), FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.06))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.15))
        self.play(FadeIn(tx('N: trả lời thật   S: luôn nói "có"', 22, SOFT).move_to([0, -1.15, 0])), run_time=self.rt(.04))

    def beat_s2(self, T):
        t0 = self.now()
        yes = [n for n, path in self.leaves if path[-1][0] == 'có']
        self.play(*[n.animate.scale(1.3) for n in yes], run_time=self.rt(.05))
        self.wait_until(.45, t0)
        m = self.M('eq', 2.0)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        m = self.M('sol', 2.0)
        self.write_board(m)
        self.frame(m)

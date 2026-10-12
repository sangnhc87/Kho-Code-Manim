"""XSS270 · Dòng họ tuyệt chủng — q = 1/4 + q/4 + q²/2 ⇒ 2q² − 3q + 1 = 0 ⇒ q = 1/2 (nghiệm nhỏ nhất)."""
from __future__ import annotations

import random
import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, TreeMixin, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, GREEN  # noqa: E402

EPISODE = {'code': 'XSS270', 'answer': '1/2'}
PROBLEM = ['Mỗi cá thể sinh $0$, $1$ hoặc $2$ con với xác',
           'suất $1/4$, $1/4$, $1/2$. Xác suất dòng họ',
           'của một cá thể bị tuyệt chủng?']
OPTIONS = ['1/4', '1/2', '1']
CORRECT = 1
ANSWER_VALUE = .5
BRANCHES = [('0', CORAL, '1/4', []),
            ('1', CYAN, '1/4', [('q', GOLD, '', [])]),
            ('2', GREEN, '1/2', [('q', GOLD, '', []), ('q', GOLD, '', [])])]
N, SEED = 4000, 5


def sim():
    r, dead = random.Random(SEED), 0
    for _ in range(N):
        pop = 1
        for _ in range(60):
            if pop == 0 or pop > 200:
                break
            nxt = 0
            for _ in range(pop):
                u = r.random()
                nxt += 0 if u < .25 else (1 if u < .5 else 2)
            pop = nxt
        dead += pop == 0
    return dead / N


BEATS = [
    Beat('hook', 'hook', 'Một loài sinh vật: mỗi cá thể sinh không con với xác suất một phần tư, một con một phần tư, hai con một phần hai. '
                         'Trung bình mỗi cá thể có một phẩy hai lăm con, dòng họ đang tăng. Vậy xác suất dòng họ tuyệt chủng là bao nhiêu?'),
    Beat('guess', 'hook', 'Một phần tư, một phần hai, hay một? Ba, hai, một!'),
    Beat('s1', 'solve', 'Gọi q là xác suất dòng họ của một cá thể tuyệt chủng. Mẹo then chốt: mỗi đứa con bắt đầu một dòng họ y hệt, độc lập, '
                        'cũng tuyệt chủng với xác suất q.'),
    Beat('s2', 'solve', 'Cây một tầng: không con thì tuyệt chủng ngay; một con thì xác suất q; hai con thì cả hai dòng phải tuyệt, q bình phương. '
                        'Vậy q bằng một phần tư cộng một phần tư q cộng một phần hai q bình phương.'),
    Beat('s3', 'solve', 'Phương trình hai q bình phương trừ ba q cộng một bằng không, nghiệm một phần hai và một. '
                        'Xác suất tuyệt chủng là nghiệm nhỏ nhất: một phần hai. Mô phỏng bốn nghìn dòng họ cũng cho khoảng năm mươi phần trăm.'),
    Beat('answer', 'solve', 'Đáp án: một phần hai. Cây tự đồng dạng: mỗi nhánh con giống hệt cây mẹ, một phương trình là đủ!'),
    Beat('outro', 'outro', outro_text(270)),
]

FORMULAS = formulas('1/2', OPTIONS,
                    eq='q = 1/4 + 1/4 q + 1/2 q^2',
                    sol='2 q^2 - 3 q + 1 = 0 arrow.l.r.double q in {1/2; 1} arrow.r.double q = 1/2')


def validate() -> bool:
    q = F(1, 2)
    assert q == F(1, 4) + q / 4 + q * q / 2 and abs(sim() - .5) < .03
    assert OPTIONS[CORRECT] == EPISODE['answer']
    return True


class XSS270(TreeMixin, ShortScene):
    N = 270

    def hook_visual(self, t0):
        self.board_top = -1.5
        self.levels, self.leaves = self.prob_tree(BRANCHES, top=(0, 2.9), dy=1.6, width=6.6, root_label='một cá thể', r=.42)
        self.wait_until(.85, t0)
        self.play(FadeIn(self.levels[0]), run_time=self.rt(.03))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.levels[1], lag_ratio=.3), run_time=self.rt(.12))
        self.wait_until(.5, t0)
        self.play(FadeIn(self.levels[2], lag_ratio=.2), run_time=self.rt(.12))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.45, t0)
        m = self.M('eq', 2.0)
        self.write_board(m)
        self.frame(m, GOLD)

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('sol', 1.4)
        self.write_board(m)
        self.frame(m)

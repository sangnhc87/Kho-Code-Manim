"""XSS273 · Nhánh đấu loại trực tiếp — C thắng D (1/2) rồi thắng chung kết: 1/2·(0,6·0,4 + 0,4·0,5) = 0,22."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

from manim import FadeIn, Line, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CORAL, CYAN, GOLD, SOFT, STROKE  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS273', 'answer': '0,22'}
PROBLEM = ['A gặp B, C gặp D, hai đội thắng vào',
           'chung kết. A thắng ai cũng với xác suất',
           '$"0,6"$; các trận khác $1/2$. $P("C vô địch")$?']
OPTIONS = ['"0,25"', '"0,22"', '"0,2"']
CORRECT = 1
ANSWER_VALUE = .22
P_A = F(3, 5)


def champion(team):
    def beat(x, y):
        return P_A if x == 'A' else (1 - P_A if y == 'A' else F(1, 2))
    semi = {'A': beat('A', 'B'), 'B': beat('B', 'A'), 'C': F(1, 2), 'D': F(1, 2)}
    other = ('C', 'D') if team in 'AB' else ('A', 'B')
    return semi[team] * sum(semi[o] * beat(team, o) for o in other)


BEATS = [
    Beat('hook', 'hook', 'Giải đấu bốn đội loại trực tiếp: A gặp B, C gặp D, hai đội thắng vào chung kết. A mạnh, thắng ai cũng với xác suất không phẩy sáu; '
                         'các trận khác năm mươi năm mươi. Xác suất đội C vô địch là bao nhiêu?'),
    Beat('guess', 'hook', 'Không phẩy hai lăm, không phẩy hai hai, hay không phẩy hai? Ba, hai, một!'),
    Beat('s1', 'solve', 'C phải thắng D trước: một phần hai. Đối thủ chung kết là A với xác suất không phẩy sáu, hoặc B với xác suất không phẩy bốn.'),
    Beat('s2', 'solve', 'Gặp A, C thắng không phẩy bốn; gặp B, C thắng một phần hai. Toàn phần trong chung kết: không phẩy sáu nhân không phẩy bốn cộng không phẩy bốn nhân không phẩy năm, bằng không phẩy bốn bốn.'),
    Beat('s3', 'solve', 'Nhân với vòng bán kết: một phần hai nhân không phẩy bốn bốn, bằng không phẩy hai hai. A vô địch không phẩy ba sáu, bốn đội cộng lại đúng bằng một.'),
    Beat('answer', 'solve', 'Đáp án: không phẩy hai hai. Nhánh đấu chính là sơ đồ cây: đối thủ ở vòng sau phụ thuộc kết quả nhánh bên kia!'),
    Beat('outro', 'outro', outro_text(273)),
]

FORMULAS = formulas('"0,22"', OPTIONS,
                    final='P("C thắng CK") = "0,6" dot "0,4" + "0,4" dot "0,5" = "0,44"',
                    tot='P = 1/2 dot "0,44" = "0,22"')


def validate() -> bool:
    assert champion('C') == F(11, 50) and sum(champion(t) for t in 'ABCD') == 1 and champion('A') == F(9, 25)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS273(ShortScene):
    N = 273

    def hook_visual(self, t0):
        self.board_top = -1.3
        pos = {'A': (-2.6, 2.7), 'B': (-2.6, 1.3), 'C': (2.6, 2.7), 'D': (2.6, 1.3)}
        self.teams = VGroup(*[token(k, GOLD if k == 'A' else (CYAN if k == 'C' else SOFT), .38).move_to([*v, 0]) for k, v in pos.items()])
        lines = VGroup(Line([-2.2, 2.7, 0], [-1.5, 2.7, 0]), Line([-2.2, 1.3, 0], [-1.5, 1.3, 0]), Line([-1.5, 2.7, 0], [-1.5, 1.3, 0]),
                       Line([-1.5, 2.0, 0], [-.4, 2.0, 0]),
                       Line([2.2, 2.7, 0], [1.5, 2.7, 0]), Line([2.2, 1.3, 0], [1.5, 1.3, 0]), Line([1.5, 2.7, 0], [1.5, 1.3, 0]),
                       Line([1.5, 2.0, 0], [.4, 2.0, 0]))
        lines.set_stroke(STROKE, 4)
        self.bracket = VGroup(lines, token('?', CORAL, .35).move_to([0, 2.0, 0]))
        self.wait_until(.8, t0)
        self.play(FadeIn(self.teams), FadeIn(self.bracket), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(self.teams[2].animate.scale(1.2), self.teams[3].animate.set_opacity(.2), run_time=self.rt(.05))
        self.wait_until(.5, t0)
        self.write_board(self.TM('đối thủ: A ($"0,6"$) hoặc B ($"0,4"$)', 28, SOFT))

    def beat_s2(self, T):
        self.clear_board(.03)
        self.write_board(self.M('final', 1.6))

    def beat_s3(self, T):
        m = self.M('tot', 2.0)
        self.write_board(m)
        self.frame(m)

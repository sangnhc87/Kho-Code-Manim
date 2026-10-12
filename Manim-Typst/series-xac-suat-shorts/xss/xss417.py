"""XSS417 · Bốn tù nhân, bốn hộp — theo vòng: ai cũng thấy tên ⇔ hoán vị không có chu trình dài > 2: 1 + 6 + 3 = 10 trên 4! = 24 → 5/12 (đoán bừa: 1/16)."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

from manim import Arrow, FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.theme import CYAN, GOLD, SOFT  # noqa: E402
from common.visuals import token  # noqa: E402

EPISODE = {'code': 'XSS417', 'answer': '5/12'}
PROBLEM = ['$4$ tù nhân, $4$ hộp chứa tên ngẫu nhiên;',
           'mỗi người mở $2$ hộp tìm tên mình. Đi theo',
           'vòng: $P("ai cũng tìm thấy")$?']
OPTIONS = ['5/12', '1/16', '1/4']
CORRECT = 0
ANSWER_VALUE = 5 / 12


def longest_cycle(p):
    seen, best = set(), 0
    for s in range(len(p)):
        n, x = 0, s
        while x not in seen:
            seen.add(x)
            x = p[x]
            n += 1
        best = max(best, n)
    return best


GOOD = [p for p in permutations(range(4)) if longest_cycle(p) <= 2]

BEATS = [
    Beat('hook', 'hook', 'Bốn tù nhân, bốn hộp đánh số, trong mỗi hộp là tên một người, xếp ngẫu nhiên. Lần lượt từng người được mở hai hộp để tìm tên mình. Tất cả đều phải thành công. '
                         'Chiến thuật đi theo vòng cho xác suất bao nhiêu?'),
    Beat('guess', 'hook', 'Năm phần mười hai, một phần mười sáu, hay một phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Mở bừa thì mỗi người một phần hai, cả bốn chỉ một phần mười sáu. Chiến thuật vòng: mở hộp số của mình, thấy tên ai thì mở tiếp hộp số của người đó.'),
    Beat('s2', 'solve', 'Đi theo vòng, mỗi người lần theo chu trình chứa mình. Người đó thành công khi chu trình dài không quá hai. Mọi người đều thành công khi không có chu trình nào dài hơn hai.'),
    Beat('s3', 'solve', 'Đếm hoán vị của bốn như vậy: giữ nguyên một cách, đổi một cặp sáu cách, đổi hai cặp ba cách. Mười trên hai mươi tư, bằng năm phần mười hai.'),
    Beat('answer', 'solve', 'Đáp án: năm phần mười hai, gấp gần bảy lần đoán bừa. Các số phận được buộc chặt với nhau qua chu trình.'),
    Beat('outro', 'outro', outro_text(417)),
]

FORMULAS = formulas('5/12', OPTIONS,
                    rand='(1/2)^4 = 1/16',
                    cnt='1 + 6 + 3 = 10',
                    prob='P = 10/(4!) = 5/12')


def validate() -> bool:
    assert len(GOOD) == 10 and F(len(GOOD), 24) == F(5, 12)
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS417(ShortScene):
    N = 417

    def hook_visual(self, t0):
        self.board_top = -1.3
        boxes = VGroup(*[token(str(i + 1), SOFT, .4) for i in range(4)]).arrange(buff=.7).move_to([0, 1.5, 0])
        names = VGroup(*[token(n, CYAN, .26).next_to(b, [0, -1, 0], buff=.2) for n, b in zip('3142', boxes)])
        self.boxes, self.names = boxes, names
        self.wait_until(.5, t0)
        self.play(FadeIn(boxes, lag_ratio=.2), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('rand', 1.4))
        self.wait_until(.6, t0)
        self.play(FadeIn(self.names, lag_ratio=.2), run_time=self.rt(.08))

    def beat_s2(self, T):
        t0 = self.now()
        cyc = VGroup(*[Arrow(self.boxes[a].get_top(), self.boxes[b].get_top(), path_arc=-1.2, color=GOLD, buff=.05, stroke_width=4)
                       for a, b in ((0, 2), (2, 3), (3, 1), (1, 0))])
        self.wait_until(.2, t0)
        self.play(FadeIn(cyc, lag_ratio=.4), run_time=self.rt(.15))

    def beat_s3(self, T):
        self.clear_board(.03)
        self.write_board(self.M('cnt', 1.4))
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)

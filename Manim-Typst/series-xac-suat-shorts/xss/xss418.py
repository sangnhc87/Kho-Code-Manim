"""XSS418 · Penney ba đồng xu — NNN thắng chỉ khi 3 lần đầu là NNN (1/8); nếu có S trước đó thì SNN luôn xuất hiện trước → 7/8."""
from __future__ import annotations

import random
import sys
from pathlib import Path

from manim import FadeIn, VGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.short import PARTS, Beat, ShortScene, formulas, outro_text  # noqa: E402,F401
from common.visuals import coin  # noqa: E402

EPISODE = {'code': 'XSS418', 'answer': '7/8'}
PROBLEM = ['Tung đồng xu liên tục. Xác suất "sấp ngửa',
           'ngửa" xuất hiện trước "ngửa ngửa ngửa"?']
OPTIONS = ['7/8', '1/2', '3/4']
CORRECT = 0
ANSWER_VALUE = 7 / 8


def simulate(runs=20000, seed=418):
    rnd, win = random.Random(seed), 0
    for _ in range(runs):
        s = ''
        while True:
            s += 'N' if rnd.random() < .5 else 'S'
            if s.endswith('SNN'):
                win += 1
                break
            if s.endswith('NNN'):
                break
    return win / runs


BEATS = [
    Beat('hook', 'hook', 'Tung đồng xu liên tục. Bạn chọn dãy sấp ngửa ngửa, đối thủ chọn ngửa ngửa ngửa. Dãy nào xuất hiện trước thì thắng. '
                         'Xác suất bạn thắng là bao nhiêu? Hai dãy dài bằng nhau mà!'),
    Beat('guess', 'hook', 'Bảy phần tám, một phần hai, hay ba phần tư? Ba, hai, một!'),
    Beat('s1', 'solve', 'Hãy xem lúc ngửa ngửa ngửa lần đầu xuất hiện. Nếu trước nó có ít nhất một mặt sấp, thì ngay trước ba ngửa ấy là sấp ngửa ngửa, đã xuất hiện sớm hơn.'),
    Beat('s2', 'solve', 'Vậy đối thủ chỉ thắng khi ba lần tung đầu tiên đều là ngửa: xác suất một phần tám.'),
    Beat('s3', 'solve', 'Bạn thắng với xác suất bảy phần tám. Mô phỏng hai mươi nghìn ván cũng cho khoảng không phẩy tám bảy năm.'),
    Beat('answer', 'solve', 'Đáp án: bảy phần tám. Trò chơi Penney: với mọi dãy đối thủ chọn, luôn có dãy khác thắng nó.'),
    Beat('outro', 'outro', outro_text(418)),
]

FORMULAS = formulas('7/8', OPTIONS,
                    lose='P("thua") = P(N N N "ngay đầu") = 1/8',
                    prob='P = 1 - 1/8 = 7/8')


def validate() -> bool:
    assert abs(simulate() - .875) < .01
    assert OPTIONS[CORRECT] == FORMULAS['answer']
    return True


class XSS418(ShortScene):
    N = 418

    def hook_visual(self, t0):
        self.board_top = -1.3
        self.picks = VGroup(VGroup(*[coin(c, .32) for c in 'SNN']).arrange(buff=.1),
                            VGroup(*[coin(c, .32) for c in 'NNN']).arrange(buff=.1)).arrange(buff=1.6).move_to([0, 2.0, 0])
        self.seq = VGroup(*[coin(c, .24) for c in 'NSNSSNN']).arrange(buff=.08).move_to([0, .6, 0])
        self.wait_until(.4, t0)
        self.play(FadeIn(self.picks, lag_ratio=.3), run_time=self.rt(.08))

    def beat_s1(self, T):
        t0 = self.now()
        self.play(FadeIn(self.seq, lag_ratio=.15), run_time=self.rt(.15))
        self.wait_until(.6, t0)
        self.play(*[c.animate.scale(1.35) for c in self.seq[4:]], run_time=self.rt(.06))

    def beat_s2(self, T):
        t0 = self.now()
        self.wait_until(.3, t0)
        self.write_board(self.M('lose', 1.4))

    def beat_s3(self, T):
        self.clear_board(.03)
        m = self.M('prob', 1.8)
        self.write_board(m)
        self.frame(m)



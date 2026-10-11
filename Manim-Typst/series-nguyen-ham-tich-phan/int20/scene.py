"""INT20 – Tổng ôn tích phân: mini-đề 10 câu theo 3 dạng câu hỏi.

    python scripts/build_typst.py --ep int20
    python scripts/prepare_voice.py --ep int20 --voice off|on
    manim --disable_caching -ql -r 854,480 --fps 24 int20/scene.py INT20
    python scripts/finalize.py --ep int20

One method per narration beat (int20/lesson.py); shared screens come from
common/blocks.py. Every answer shown is checked in lesson.validate().
"""
from __future__ import annotations

import sys
from pathlib import Path

from manim import DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, LaggedStart, VGroup, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.kit import badge, card, tx  # noqa: E402
from common.lesson_scene import LessonScene  # noqa: E402
from common.theme import CORAL, CYAN, GOLD, GREEN, PURPLE, SOFT, WHITE  # noqa: E402


class INT20(LessonScene):
    EP = 'int20'

    # ------------------------------------------------------------ helpers
    def tool_cards(self, t0, title, color, rows, fracs):
        """Summary table: one card per tool (name + formula)."""
        self.clear_stage(.04)
        self.play(FadeIn(tx(title, 26, color, bold=True).move_to([0, 2.6, 0])), run_time=self.rt(.04))
        for i, ((name, key), frac) in enumerate(zip(rows, fracs)):
            c = card(12.4, 1.45, color).move_to([0, 1.5 - 1.65 * i, 0])
            n = tx(name, 24, WHITE, bold=True).move_to(c.get_left() + RIGHT * 1.9)
            m = self.M(key, 1.15, max_w=8.6).move_to(c.get_center() + RIGHT * 1.6)
            self.wait_until(frac, t0)
            self.play(FadeIn(VGroup(c, n), shift=UP * .15), Write(m), run_time=self.rt(.08))

    def mc(self, n, q, opts, k, sol, fracs=(.2, .3, .55)):
        """Câu trắc nghiệm: đề, 4 phương án, tạm dừng, rồi khoanh đáp án đúng kèm lời giải."""
        t0 = self.now()
        lesson_entry = self.lesson.MC[n - 1]
        assert lesson_entry == (q, opts, k, sol), (n, lesson_entry)
        self.clear_stage(.04)
        self.mc_question(t0, n, [self.M(q, 1.4)], [self.M(o, 1.4) for o in opts], fracs=fracs[:2])
        self.wait_until(fracs[2], t0)
        self.play(*self.mc_mark(k, self.M(sol, 1.3)), run_time=self.rt(.1))

    def short(self, t0, n, task, sol, value, extra=None, fracs=(.12, .6, .82)):
        self.clear_stage(.05)
        tag = VGroup(badge(f'CÂU {n}', PURPLE, 20), tx('trả lời ngắn – Phần III', 19, SOFT)).arrange(RIGHT, buff=.3)
        rows = [tag]
        if extra is not None:
            rows.append(extra)
        m_task, m_sol = self.M(task, 1.45), self.M(sol, 1.2)
        sheet = self.answer_sheet(value)
        self.centre(*rows, m_task, m_sol, sheet, top=2.6, gap=.55)
        self.play(*[FadeIn(r) for r in rows], run_time=self.rt(.05))
        self.wait_until(fracs[0], t0)
        self.play(Write(m_task), run_time=self.rt(.1))
        self.wait_until(fracs[1], t0)
        self.play(Write(m_sol), run_time=self.rt(.14))
        self.wait_until(fracs[2], t0)
        self.play(FadeIn(sheet), run_time=self.rt(.05))

    # ================================================================ MỞ ĐẦU
    def beat_h1(self, T):
        t0 = self.now()
        blocks = VGroup()
        for i, (num, label, col) in enumerate((('6', 'trắc nghiệm', CYAN), ('1', 'đúng / sai (4 ý)', CORAL),
                                               ('3', 'trả lời ngắn', PURPLE))):
            c = card(3.7, 3.0, col).move_to([-4.1 + 4.1 * i, .3, 0])
            blocks.add(VGroup(c, tx(num, 72, col, bold=True).move_to(c.get_center() + UP * .35),
                              tx(label, 24, WHITE).move_to(c.get_bottom() + UP * .55)))
        self.play(LaggedStart(*[FadeIn(b, shift=UP * .2) for b in blocks], lag_ratio=.5), run_time=self.rt(.4))
        self.wait_until(.75, t0)
        self.play(FadeIn(tx('Em làm được bao nhiêu câu?', 32, GOLD, bold=True).move_to([0, -2.3, 0])),
                  run_time=self.rt(.07))

    def beat_h2(self, T):
        self.clear_stage(.06)
        self.title_card()

    def beat_h3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.goal_cards([('Bảng tổng hợp', 'Mọi công cụ của phần tích phân'),
                         ('Tự làm trước', 'Tạm dừng ở mỗi câu'),
                         ('Tự chấm điểm', 'Biết phần nào cần ôn lại')], t0, fracs=(.05, .35, .65))

    # ================================================================ BẢNG TỔNG HỢP
    def beat_c1(self, T):
        self.tool_cards(self.now(), 'NHÓM 1 · CÔNG CỤ TÍNH', CYAN,
                        (('Newton–Leibniz', 'tool1'), ('Cộng khoảng', 'tool2'), ('Trị tuyệt đối', 'tool3')),
                        (.05, .35, .62))

    def beat_c2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('NHÓM 2 · KỸ THUẬT BIẾN ĐỔI', 26, GOLD, bold=True).move_to([0, 2.6, 0])),
                  run_time=self.rt(.04))
        rows = (('Đổi biến', 'tech1'), ('Từng phần', 'tech2'), ('Đối xứng', 'tech3'))
        for i, ((name, key), frac) in enumerate(zip(rows, (.05, .25, .55))):
            c = card(12.4, 1.3, GOLD).move_to([0, 1.55 - 1.45 * i, 0])
            n = tx(name, 24, WHITE, bold=True).move_to(c.get_left() + RIGHT * 1.9)
            m = self.M(key, 1.1, max_w=8.6).move_to(c.get_center() + RIGHT * 1.6)
            self.wait_until(frac, t0)
            self.play(FadeIn(VGroup(c, n), shift=UP * .15), Write(m), run_time=self.rt(.08))
        self.wait_until(.8, t0)
        self.play(FadeIn(tx("Hàm ẩn: f'/h(f) = g(x) → tích phân hai vế", 24, SOFT).move_to([0, -2.7, 0])),
                  run_time=self.rt(.05))

    def beat_c3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        top = VGroup(tx('NHÓM 3 · ỨNG DỤNG', 24, GREEN, bold=True), self.M('app1', 1.3)).arrange(RIGHT, buff=.6) \
            .move_to([0, 2.3, 0])
        self.play(FadeIn(top[0]), Write(top[1]), run_time=self.rt(.08))
        self.wait_until(.3, t0)
        for i, (title, tip, col, frac) in enumerate((
                ('Trắc nghiệm', 'loại trừ + bấm máy kiểm tra', CYAN, .32),
                ('Đúng / Sai', 'xét từng ý độc lập', CORAL, .5),
                ('Trả lời ngắn', 'làm tròn đúng, ghi phiếu đúng', PURPLE, .66))):
            c = card(3.9, 2.6, col).move_to([-4.2 + 4.2 * i, -.6, 0])
            g = VGroup(c, tx(title, 26, col, bold=True).move_to(c.get_top() + DOWN * .6),
                       tx(tip, 20, WHITE, max_w=3.5).move_to(c.get_center() + DOWN * .25))
            self.wait_until(frac, t0)
            self.play(FadeIn(g, shift=UP * .2), run_time=self.rt(.06))

    def beat_c4(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('5 BẪY THƯỜNG GẶP', 26, CORAL, bold=True).move_to([0, 2.6, 0])), run_time=self.rt(.04))
        traps = ('quên chia hệ số: nguyên hàm của e^(2x)', 'đưa trị tuyệt đối ra ngoài tích phân',
                 'đổi biến mà quên đổi cận', 'chọn u ngược thứ tự khi từng phần', 'sai dấu: nguyên hàm của e^(−x)')
        for i, (trap, frac) in enumerate(zip(traps, (.12, .35, .5, .62, .76))):
            r = VGroup(tx(f'{i + 1}', 30, CORAL, bold=True), tx(trap, 26, WHITE)).arrange(RIGHT, buff=.4) \
                .move_to([-5.2, 1.6 - .95 * i, 0], aligned_edge=LEFT)
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.05))

    # ================================================================ TRẮC NGHIỆM
    def beat_q1(self, T):
        self.mc(1, 'q1', ('o_4', 'o_6', 'o_8', 'o_2'), 0, 'q1_s', fracs=(.12, .22, .45))

    def beat_q2(self, T):
        self.mc(2, 'q2', ('o_4', 'o_13', 'o_16', 'o_10'), 2, 'q2_s', fracs=(.25, .35, .55))

    def beat_q3(self, T):
        self.mc(3, 'q3', ('o_e1', 'o_e2', 'o_e3', 'o_e4'), 1, 'q3_s', fracs=(.12, .2, .4))

    def beat_q4(self, T):
        self.mc(4, 'q4', ('o_0', 'o_2', 'o_1', 'o_half'), 2, 'q4_s', fracs=(.12, .2, .45))

    def beat_q5(self, T):
        self.mc(5, 'q5', ('o_83', 'o_76', 'o_1', 'o_73'), 3, 'q5_s', fracs=(.15, .25, .5))

    def beat_q6(self, T):
        self.mc(6, 'q6', ('o_e', 'o_1', 'o_em1', 'o_0'), 1, 'q6_s', fracs=(.12, .2, .45))

    # ================================================================ ĐÚNG/SAI & TRẢ LỜI NGẮN
    def beat_x1(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        l1 = VGroup(tx('Câu 7. Chất điểm có', 24, WHITE), self.M('tf_given', 1.3)).arrange(RIGHT, buff=.25)
        l2 = tx('Xét các mệnh đề sau:', 24, WHITE)
        items = tuple(self.M(k, 1.35) for k in ('tf_a', 'tf_b', 'tf_c', 'tf_d'))
        self.tf_question(t0, [l1, l2], items, fracs=(.4, .72))

    def beat_x2(self, T):
        t0 = self.now()
        self.play(FadeOut(self.tf_pause), self.tf_mark(0, True), run_time=self.rt(.08))
        self.wait_until(.45, t0)
        self.play(self.tf_mark(1, True), run_time=self.rt(.08))

    def beat_x3(self, T):
        t0 = self.now()
        sol = VGroup(tx('c, d)', 22, SOFT), self.M('tf_calc', .9)).arrange(RIGHT, buff=.25) \
            .move_to([0, -2.68, 0]).to_edge(LEFT, buff=.9)
        self.play(FadeIn(sol), self.tf_mark(2, False), run_time=self.rt(.1))
        self.wait_until(.7, t0)
        self.play(self.tf_mark(3, True), run_time=self.rt(.08))
        self.play(FadeIn(self.tf_key('ĐĐSĐ'), shift=LEFT * .1), run_time=self.rt(.05))

    def beat_x4(self, T):
        t0 = self.now()
        self.clear_stage(.05)
        head = badge('CÁCH GHI PHIẾU TRẢ LỜI NGẮN', PURPLE, 20)
        rule = tx('4 ô · dấu phẩy và dấu trừ mỗi thứ chiếm 1 ô', 26, WHITE)
        ex = self.answer_sheet('-1,5')
        tip = tx('Làm tròn theo yêu cầu của đề rồi mới ghi', 25, GOLD, bold=True)
        self.centre(head, rule, ex, tip, top=2.2, gap=.75)
        self.play(FadeIn(head), FadeIn(rule), run_time=self.rt(.08))
        self.wait_until(.35, t0)
        self.play(FadeIn(ex), run_time=self.rt(.06))
        self.wait_until(.65, t0)
        self.play(FadeIn(tip, shift=UP * .1), run_time=self.rt(.05))

    def beat_s1(self, T):
        self.short(self.now(), 8, 's1', 's1_s', '0,57', tx('(làm tròn đến hàng phần trăm)', 22, SOFT),
                   fracs=(.05, .35, .8))

    def beat_s2(self, T):
        self.short(self.now(), 9, 's2', 's2_s', '2,67', tx('(làm tròn đến hàng phần trăm)', 22, SOFT),
                   fracs=(.05, .45, .85))

    def beat_s3(self, T):
        self.short(self.now(), 10, 's3', 's3_s', '50', tx('Ô tô đang chạy 20 m/s thì phanh, vận tốc sau đó:', 23, WHITE),
                   fracs=(.05, .45, .85))

    # ================================================================ TỔNG KẾT
    def beat_o1(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(badge('ĐÁP ÁN MINI-ĐỀ', GOLD, 22).move_to([0, 2.6, 0])), run_time=self.rt(.04))
        keys = [('1', 'A'), ('2', 'C'), ('3', 'B'), ('4', 'C'), ('5', 'D'), ('6', 'B'),
                ('7', 'ĐĐSĐ'), ('8', '0,57'), ('9', '2,67'), ('10', '50')]
        cells = VGroup()
        for i, (n, a) in enumerate(keys):
            col = CYAN if i < 6 else (CORAL if i == 6 else PURPLE)
            c = card(2.25, 1.55, col).move_to([-4.9 + 2.45 * (i % 5), 1.1 - 1.85 * (i // 5), 0])
            cells.add(VGroup(c, tx(f'Câu {n}', 19, SOFT).move_to(c.get_top() + DOWN * .35),
                             tx(a, 30, col, bold=True).move_to(c.get_center() + DOWN * .15)))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .1) for c in cells[:6]], lag_ratio=.4), run_time=self.rt(.35))
        self.wait_until(.5, t0)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * .1) for c in cells[6:]], lag_ratio=.5), run_time=self.rt(.35))

    def beat_o2(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.play(FadeIn(tx('SAI CÂU NÀO → XEM LẠI TẬP NÀO', 26, GOLD, bold=True).move_to([0, 2.6, 0])),
                  run_time=self.rt(.04))
        rows = (('Câu 3, 8', 'INT12 · INT17'), ('Câu 4, 7', 'INT14 · INT15'), ('Câu 5', 'INT16'), ('Câu 9', 'INT18'))
        for i, ((q, ep), frac) in enumerate(zip(rows, (.08, .3, .55, .7))):
            r = VGroup(tx(q, 28, WHITE, bold=True), tx('→', 28, SOFT), tx(ep, 28, CYAN, bold=True)) \
                .arrange(RIGHT, buff=.5).move_to([0, 1.5 - 1.0 * i, 0])
            self.wait_until(frac, t0)
            self.play(FadeIn(r, shift=RIGHT * .2), run_time=self.rt(.05))

    def beat_o3(self, T):
        t0 = self.now()
        self.clear_stage(.04)
        self.next_card(t0, [tx('Phần C · Ứng dụng tích phân', 28, GOLD, bold=True), self.M('next1', 1.3)])


class INT20_SMOKE(INT20):
    smoke = True

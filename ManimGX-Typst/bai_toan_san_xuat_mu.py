import json
from pathlib import Path
import manimgx as m

# ==============================================================================
# BÀI TOÁN TỐI ƯU SẢN XUẤT - HỆ BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN (TOÁN 10)
# Engine: ManimGX (Rust + GPU/Lavapipe core + Native Typst) + AI Voiceover
# Bản quyền nội dung: Thầy Nguyễn Văn Sang (vi-VN-NamMinhNeural)
# ==============================================================================

BG = "#08111F"
PANEL = "#0E1D34"
INK = "#EDF4FF"
MUTED = "#8EA7C2"
BLUE = "#38BDF8"
CYAN = "#38E0CF"
GOLD = "#FFD700"
GREEN = "#4ADE80"
RED = "#FF6B6B"
ORANGE = "#FB923C"

m.config.background_color = BG

ROOT = Path(__file__).resolve().parent
TIMINGS_FILE = ROOT / "narration_timings.json"

DEFAULT_TIMINGS = {
    "seg_01_intro": {"duration": 6.5, "path": str(ROOT / "audio_cache" / "seg_01_intro.mp3")},
    "seg_02_model": {"duration": 11.0, "path": str(ROOT / "audio_cache" / "seg_02_model.mp3")},
    "seg_03_time_prop_a": {"duration": 8.0, "path": str(ROOT / "audio_cache" / "seg_03_time_prop_a.mp3")},
    "seg_04_system_prop_b": {"duration": 10.5, "path": str(ROOT / "audio_cache" / "seg_04_system_prop_b.mp3")},
    "seg_05_geometry": {"duration": 11.5, "path": str(ROOT / "audio_cache" / "seg_05_geometry.mp3")},
    "seg_06_profit_prop_cd": {"duration": 13.5, "path": str(ROOT / "audio_cache" / "seg_06_profit_prop_cd.mp3")},
    "seg_07_summary": {"duration": 7.0, "path": str(ROOT / "audio_cache" / "seg_07_summary.mp3")},
}


class BaiToanSanXuatMuScene(m.Scene):
    def construct(self) -> None:
        if TIMINGS_FILE.exists():
            timings = json.loads(TIMINGS_FILE.read_text(encoding="utf-8"))
        else:
            timings = DEFAULT_TIMINGS

        timeline = []
        cur_t = 0.0

        def track(key: str):
            nonlocal cur_t
            audio_info = timings.get(key, DEFAULT_TIMINGS[key])
            timeline.append({
                "key": key,
                "start": cur_t,
                "audio_path": audio_info.get("path", str(ROOT / "audio_cache" / f"{key}.mp3")),
                "duration": audio_info["duration"],
            })
            return audio_info["duration"]

        def advance(dt: float):
            nonlocal cur_t
            cur_t += dt

        # ======================================================================
        # ĐOẠN 1: HEADER & FOOTER CỐ ĐỊNH (GIỚI THIỆU BÀI TOÁN)
        # ======================================================================
        d1 = track("seg_01_intro")

        header_title = m.Text(
            "BÀI TOÁN TỐI ƯU SẢN XUẤT MŨ",
            font_size=28,
            color=GOLD,
            weight=m.BOLD,
        )
        header_sub = m.Text(
            "Hệ Bất Phương Trình Bậc Nhất Hai Ẩn • Toán 10",
            font_size=17,
            color=BLUE,
        )
        header = m.VGroup(header_title, header_sub).arrange(m.DOWN, buff=0.08).to_edge(m.UP, buff=0.20)

        footer = m.Text(
            "Bài giảng Toán THPT • Thầy Nguyễn Văn Sang",
            font_size=15,
            color=MUTED,
        ).to_edge(m.DOWN, buff=0.20)

        self.play(m.FadeIn(header), m.FadeIn(footer), run_time=0.8)
        advance(0.8)

        w1 = max(0.2, d1 - 0.8 + 0.3)
        self.wait(w1)
        advance(w1)

        # ======================================================================
        # ĐOẠN 2: THIẾT LẬP MÔ HÌNH TOÁN HỌC (ĐẶT ẨN & NĂNG SUẤT)
        # ======================================================================
        d2 = track("seg_02_model")

        card_intro = m.RoundedRectangle(
            width=12.6,
            height=5.2,
            corner_radius=0.2,
            fill_color=PANEL,
            fill_opacity=0.92,
            stroke_color=BLUE,
            stroke_width=1.5,
        ).move_to([0, -0.1, 0])

        t_intro_title = m.Text("1. THIẾT LẬP MÔ HÌNH TOÁN HỌC", font_size=21, color=GOLD, weight=m.BOLD)
        t_row1 = m.Text("• Gọi x, y là số mũ kiểu I và kiểu II cần sản xuất trong một ngày (x, y ≥ 0).", font_size=17, color=INK)
        t_row2 = m.Text("• Năng suất: Làm 1 mũ II mất 1/60 giờ; làm 1 mũ I mất gấp đôi là 2/60 = 1/30 giờ.", font_size=17, color=CYAN)

        intro_top = m.VGroup(t_intro_title, t_row1, t_row2).arrange(m.DOWN, buff=0.22, aligned_edge=m.LEFT).move_to(card_intro.get_top() + [0, -1.0, 0])

        self.play(m.FadeIn(card_intro), m.LaggedStart(*[m.FadeIn(r) for r in intro_top], lag_ratio=0.2), run_time=1.5)
        advance(1.5)

        w2 = max(0.2, d2 - 1.5 + 0.3)
        self.wait(w2)
        advance(w2)

        # ======================================================================
        # ĐOẠN 3: TÍNH THỜI GIAN SẢN XUẤT & XÉT MỆNH ĐỀ a
        # ======================================================================
        d3 = track("seg_03_time_prop_a")

        t_row3 = m.Text("• Tổng thời gian để làm x mũ kiểu I và y mũ kiểu II là: (2x + y)/60 (giờ).", font_size=17, color=INK).next_to(t_row2, m.DOWN, buff=0.22, aligned_edge=m.LEFT)

        box_a = m.RoundedRectangle(width=11.6, height=0.6, corner_radius=0.12, fill_color="#071224", fill_opacity=1.0, stroke_color=RED, stroke_width=1.2).next_to(t_row3, m.DOWN, buff=0.18, aligned_edge=m.LEFT)
        txt_a = m.Text("a) Thời gian làm mũ là (2x - y)/60 giờ  ➔  SAI (Công thức đúng là (2x + y)/60)", font_size=15, color=RED).move_to(box_a.get_center())
        grp_a = m.VGroup(box_a, txt_a)

        self.play(m.FadeIn(t_row3), m.FadeIn(grp_a), run_time=1.2)
        advance(1.2)

        w3 = max(0.2, d3 - 1.2 + 0.3)
        self.wait(w3)
        advance(w3)

        # ======================================================================
        # ĐOẠN 4: QUỸ THỜI GIAN 8H, GIỚI HẠN THỊ TRƯỜNG & XÉT MỆNH ĐỀ b
        # ======================================================================
        d4 = track("seg_04_system_prop_b")

        t_row4 = m.Text("• Quỹ thời gian 8 giờ: (2x + y)/60 ≤ 8  ⇔  2x + y ≤ 480. Nhu cầu: 0 ≤ x ≤ 200, 0 ≤ y ≤ 240.", font_size=16, color=ORANGE).next_to(box_a, m.DOWN, buff=0.18, aligned_edge=m.LEFT)

        box_b = m.RoundedRectangle(width=11.6, height=0.6, corner_radius=0.12, fill_color="#071224", fill_opacity=1.0, stroke_color=GREEN, stroke_width=1.2).next_to(t_row4, m.DOWN, buff=0.18, aligned_edge=m.LEFT)
        txt_b = m.Text("b) Hệ BPT mô tả các điều kiện: { 0 ≤ x ≤ 200; 0 ≤ y ≤ 240; 2x + y ≤ 480 }  ➔  ĐÚNG", font_size=15, color=GREEN).move_to(box_b.get_center())
        grp_b = m.VGroup(box_b, txt_b)

        self.play(m.FadeIn(t_row4), m.FadeIn(grp_b), run_time=1.2)
        advance(1.2)

        w4 = max(0.2, d4 - 1.2 + 0.3)
        self.wait(w4)
        advance(w4)

        # Chuyển cảnh sang hình học
        self.play(
            m.FadeOut(card_intro),
            m.FadeOut(intro_top),
            m.FadeOut(t_row3),
            m.FadeOut(grp_a),
            m.FadeOut(t_row4),
            m.FadeOut(grp_b),
            run_time=0.5,
        )
        advance(0.5)

        # ======================================================================
        # ĐOẠN 5: BIỂU DIỄN HÌNH HỌC TRÊN HỆ TRỤC OXY
        # ======================================================================
        d5 = track("seg_05_geometry")

        axes = m.Axes(
            x_range=[0, 260, 50],
            y_range=[0, 300, 50],
            x_length=4.8,
            y_length=4.4,
            axis_config={"color": MUTED, "stroke_width": 1.2, "font_size": 20},
        ).move_to([-3.7, -0.15, 0])
        axes.add_coordinates()

        lbl_x = m.Text("x (Mũ I)", font_size=15, color=BLUE).next_to(axes.x_axis.get_end(), m.DR, buff=0.06)
        lbl_y = m.Text("y (Mũ II)", font_size=15, color=BLUE).next_to(axes.y_axis.get_end(), m.UL, buff=0.06)

        p_O = axes.c2p(0, 0)
        p_A = axes.c2p(200, 0)
        p_B = axes.c2p(200, 80)
        p_C = axes.c2p(120, 240)
        p_D = axes.c2p(0, 240)

        line_x200 = m.Line(axes.c2p(200, 0), axes.c2p(200, 270), color=ORANGE, stroke_width=1.8)
        lbl_line_x = m.MathTex(r"x = 200", font_size=15, color=ORANGE).next_to(line_x200.get_top(), m.UR, buff=0.05)

        line_y240 = m.Line(axes.c2p(0, 240), axes.c2p(240, 240), color=GOLD, stroke_width=1.8)
        lbl_line_y = m.MathTex(r"y = 240", font_size=15, color=GOLD).next_to(axes.c2p(60, 240), m.UP, buff=0.06)

        line_time = m.Line(axes.c2p(90, 300), axes.c2p(245, -10), color=CYAN, stroke_width=1.8)
        lbl_line_time = m.MathTex(r"2x + y = 480", font_size=15, color=CYAN).next_to(axes.c2p(165, 150), m.UR, buff=0.06)

        region = m.Polygon(
            p_O, p_A, p_B, p_C, p_D,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.32,
            stroke_width=2.0,
        )

        dots = m.VGroup(
            m.Dot(p_O, color=GOLD, radius=0.05),
            m.Dot(p_A, color=GOLD, radius=0.05),
            m.Dot(p_B, color=GOLD, radius=0.05),
            m.Dot(p_C, color=RED, radius=0.08),
            m.Dot(p_D, color=GOLD, radius=0.05),
        )

        lbl_O = m.MathTex(r"O", font_size=14, color=GOLD).next_to(p_O, m.DL, buff=0.06)
        lbl_A = m.MathTex(r"A(200, 0)", font_size=13, color=GOLD).next_to(p_A, m.UR, buff=0.05)
        lbl_B = m.MathTex(r"B(200, 80)", font_size=13, color=GOLD).next_to(p_B, m.RIGHT, buff=0.06)
        lbl_C = m.MathTex(r"C(120, 240)", font_size=16, color=GOLD).next_to(p_C, m.UP, buff=0.08)
        lbl_D = m.MathTex(r"D(0, 240)", font_size=13, color=GOLD).next_to(p_D, m.RIGHT, buff=0.06)
        labels_pts = m.VGroup(lbl_O, lbl_A, lbl_B, lbl_C, lbl_D)

        self.play(m.Create(axes), m.Write(lbl_x), m.Write(lbl_y), run_time=1.0)
        self.play(
            m.Create(line_x200), m.Write(lbl_line_x),
            m.Create(line_y240), m.Write(lbl_line_y),
            m.Create(line_time), m.Write(lbl_line_time),
            run_time=1.0,
        )
        self.play(m.FadeIn(region), m.FadeIn(dots), m.FadeIn(labels_pts), run_time=1.0)
        advance(3.0)

        w5 = max(0.2, d5 - 3.0 + 0.3)
        self.wait(w5)
        advance(w5)

        # ======================================================================
        # ĐOẠN 6: KHẢO SÁT HÀM TIỀN LÃI & XÉT MỆNH ĐỀ c, d
        # ======================================================================
        d6 = track("seg_06_profit_prop_cd")

        panel_right = m.RoundedRectangle(
            width=6.0,
            height=5.2,
            corner_radius=0.2,
            fill_color=PANEL,
            fill_opacity=0.92,
            stroke_color=MUTED,
            stroke_width=1.5,
        ).move_to([3.5, -0.1, 0])

        right_title = m.Text("2. KHẢO SÁT HÀM MỤC TIÊU", font_size=19, color=GOLD, weight=m.BOLD)
        right_func = m.MathTex(r"F(x, y) = 24x + 15y \quad (\text{nghìn đồng})", font_size=18, color=INK)

        val_O = m.MathTex(r"\bullet \; F(0, 0) = 0", font_size=17, color=INK)
        val_A = m.MathTex(r"\bullet \; F(200, 0) = 24(200) + 15(0) = 4.800", font_size=17, color=INK)
        val_B = m.MathTex(r"\bullet \; F(200, 80) = 24(200) + 15(80) = 6.000", font_size=17, color=INK)
        val_C = m.MathTex(r"\bullet \; F(120, 240) = 24(120) + 15(240) = 6.480 \; \mathbf{(MAX)}", font_size=18, color=GOLD)
        val_D = m.MathTex(r"\bullet \; F(0, 240) = 24(0) + 15(240) = 3.600", font_size=17, color=INK)

        eval_c = m.Text("c) Sản xuất 120 mũ I, 240 mũ II lãi cao nhất: ĐÚNG", font_size=14, color=GREEN)
        eval_d = m.Text("d) Số tiền lãi cao nhất là 6.480.000 đồng: ĐÚNG", font_size=14, color=GREEN)

        calc_group = m.VGroup(
            right_title,
            right_func,
            val_O,
            val_A,
            val_B,
            val_C,
            val_D,
            eval_c,
            eval_d,
        ).arrange(m.DOWN, buff=0.18, aligned_edge=m.LEFT).move_to(panel_right.get_center())

        self.play(m.FadeIn(panel_right), m.LaggedStart(*[m.FadeIn(item) for item in calc_group], lag_ratio=0.12), run_time=1.5)
        self.play(m.Circumscribe(val_C, color=GOLD), m.Indicate(dots[3], color=RED, scale_factor=1.5), run_time=1.2)
        advance(2.7)

        w6 = max(0.2, d6 - 2.7 + 0.3)
        self.wait(w6)
        advance(w6)

        # Chuyển cảnh sang bảng tổng kết
        self.play(
            m.FadeOut(axes), m.FadeOut(lbl_x), m.FadeOut(lbl_y),
            m.FadeOut(line_x200), m.FadeOut(lbl_line_x),
            m.FadeOut(line_y240), m.FadeOut(lbl_line_y),
            m.FadeOut(line_time), m.FadeOut(lbl_line_time),
            m.FadeOut(region), m.FadeOut(dots), m.FadeOut(labels_pts),
            m.FadeOut(panel_right), m.FadeOut(calc_group),
            run_time=0.5,
        )
        advance(0.5)

        # ======================================================================
        # ĐOẠN 7: BẢNG KẾT LUẬN & ĐÁP ÁN TỔNG KẾT
        # ======================================================================
        d7 = track("seg_07_summary")

        card_summary = m.RoundedRectangle(
            width=12.2,
            height=5.2,
            corner_radius=0.2,
            fill_color=PANEL,
            fill_opacity=0.95,
            stroke_color=GOLD,
            stroke_width=2.0,
        ).move_to([0, -0.1, 0])

        sum_title = m.Text("KẾT LUẬN & BẢNG ĐÁP ÁN ĐÚNG / SAI", font_size=23, color=GOLD, weight=m.BOLD)

        t_sa = m.Text("a) Thời gian làm x mũ I và y mũ II là (2x - y)/60 giờ.", font_size=17, color=INK)
        tag_sa = m.Text("[SAI]", font_size=17, color=RED, weight=m.BOLD)
        row_a = m.VGroup(t_sa, tag_sa).arrange(m.RIGHT, buff=0.4)

        t_sb = m.Text("b) Hệ bất phương trình mô tả các điều kiện của bài toán.", font_size=17, color=INK)
        tag_sb = m.Text("[ĐÚNG]", font_size=17, color=GREEN, weight=m.BOLD)
        row_b = m.VGroup(t_sb, tag_sb).arrange(m.RIGHT, buff=0.4)

        t_sc = m.Text("c) Cần sản xuất 120 chiếc mũ kiểu I và 240 chiếc mũ kiểu II.", font_size=17, color=INK)
        tag_sc = m.Text("[ĐÚNG]", font_size=17, color=GREEN, weight=m.BOLD)
        row_c = m.VGroup(t_sc, tag_sc).arrange(m.RIGHT, buff=0.4)

        t_sd = m.Text("d) Số tiền lãi cao nhất thu được trong ngày là 6.480.000 đồng.", font_size=17, color=INK)
        tag_sd = m.Text("[ĐÚNG]", font_size=17, color=GREEN, weight=m.BOLD)
        row_d = m.VGroup(t_sd, tag_sd).arrange(m.RIGHT, buff=0.4)

        final_box = m.RoundedRectangle(width=8.8, height=0.8, corner_radius=0.15, fill_color="#102544", fill_opacity=1.0, stroke_color=CYAN, stroke_width=1.5)
        final_text = m.Text("ĐÁP ÁN:   a) S   —   b) Đ   —   c) Đ   —   d) Đ", font_size=21, color=GOLD, weight=m.BOLD).move_to(final_box.get_center())
        final_row = m.VGroup(final_box, final_text)

        summary_content = m.VGroup(
            sum_title,
            row_a,
            row_b,
            row_c,
            row_d,
            final_row,
        ).arrange(m.DOWN, buff=0.25).move_to(card_summary.get_center())

        self.play(m.FadeIn(card_summary), m.LaggedStart(*[m.FadeIn(elem) for elem in summary_content], lag_ratio=0.15), run_time=1.2)
        self.play(m.Circumscribe(final_box, color=GOLD), run_time=1.0)
        advance(2.2)

        w7 = max(0.5, d7 - 2.2 + 1.5)
        self.wait(w7)
        advance(w7)

        # Lưu lại timeline để mux_audio sử dụng
        timeline_path = ROOT / "scene_timeline.json"
        timeline_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")

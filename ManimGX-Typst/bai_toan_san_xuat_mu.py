import manimgx as m

# ==============================================================================
# BÀI TOÁN TỐI ƯU SẢN XUẤT - HỆ BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN (TOÁN 10)
# Engine: ManimGX (Rust + GPU/Lavapipe core + Native Typst typesetting)
# Bản quyền nội dung: Thầy Nguyễn Văn Sang
# ==============================================================================

# Palette màu cao cấp
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
WHITE = "#FFFFFF"

m.config.background_color = BG


class BaiToanSanXuatMuScene(m.Scene):
    def construct(self) -> None:
        # ======================================================================
        # HEADER & FOOTER CỐ ĐỊNH
        # ======================================================================
        header_title = m.Text(
            "BÀI TOÁN TỐI ƯU SẢN XUẤT MŨ",
            font_size=30,
            color=GOLD,
            weight=m.BOLD,
        )
        header_sub = m.Text(
            "Hệ Bất Phương Trình Bậc Nhất Hai Ẩn • Toán 10",
            font_size=18,
            color=BLUE,
        )
        header = m.VGroup(header_title, header_sub).arrange(m.DOWN, buff=0.08).to_edge(m.UP, buff=0.22)

        footer = m.Text(
            "Bài giảng Toán THPT • Thầy Nguyễn Văn Sang",
            font_size=16,
            color=MUTED,
        ).to_edge(m.DOWN, buff=0.22)

        self.play(m.FadeIn(header), m.FadeIn(footer), run_time=0.8)
        self.wait(0.5)

        # ======================================================================
        # PHẦN 1: TÓM TẮT ĐỀ BÀI & CÁC MỆNH ĐỀ CẦN XÉT
        # ======================================================================
        card_intro = m.RoundedRectangle(
            width=12.6,
            height=5.2,
            corner_radius=0.2,
            fill_color=PANEL,
            fill_opacity=0.9,
            stroke_color=BLUE,
            stroke_width=1.5,
        ).move_to([0, -0.1, 0])

        t_intro_title = m.Text("1. THIẾT LẬP MÔ HÌNH TOÁN HỌC", font_size=22, color=GOLD, weight=m.BOLD)

        t_row1 = m.Text("• Gọi x, y lần lượt là số mũ kiểu I và kiểu II cần sản xuất trong một ngày (x, y ≥ 0).", font_size=18, color=INK)
        t_row2 = m.Text("• Năng suất: Làm 1 mũ II mất 1/60 giờ; làm 1 mũ I mất gấp đôi là 2/60 = 1/30 giờ.", font_size=18, color=CYAN)
        t_row3 = m.Text("• Quỹ thời gian: Phân xưởng làm 8 giờ/ngày  ⇒  Tổng thời gian: (2x + y)/60 ≤ 8  ⇔  2x + y ≤ 480.", font_size=18, color=INK)
        t_row4 = m.Text("• Nhu cầu thị trường tối đa: 0 ≤ x ≤ 200 và 0 ≤ y ≤ 240.", font_size=18, color=ORANGE)
        t_row5 = m.Text("• Tiền lãi thu được (nghìn đồng): F(x, y) = 24x + 15y.", font_size=18, color=GREEN)

        intro_content = m.VGroup(
            t_intro_title,
            t_row1,
            t_row2,
            t_row3,
            t_row4,
            t_row5,
        ).arrange(m.DOWN, buff=0.22, aligned_edge=m.LEFT).move_to(card_intro.get_center())

        self.play(m.FadeIn(card_intro), m.LaggedStart(*[m.FadeIn(r) for r in intro_content], lag_ratio=0.15), run_time=1.2)
        self.wait(1.5)

        # Đánh giá nhanh mệnh đề a & b
        box_ab = m.RoundedRectangle(width=11.8, height=1.3, corner_radius=0.15, fill_color="#071224", fill_opacity=0.95, stroke_color=CYAN, stroke_width=1.5).move_to([0, -1.8, 0])
        txt_a = m.Text("a) Thời gian làm mũ là (2x - y)/60 giờ  ➔  SAI (Phải là phép cộng: (2x + y)/60)", font_size=16, color=RED)
        txt_b = m.Text("b) Hệ BPT mô tả các điều kiện: { 0 ≤ x ≤ 200; 0 ≤ y ≤ 240; 2x + y ≤ 480 }  ➔  ĐÚNG", font_size=16, color=GREEN)
        ab_group = m.VGroup(txt_a, txt_b).arrange(m.DOWN, buff=0.15, aligned_edge=m.LEFT).move_to(box_ab.get_center())

        self.play(m.FadeIn(box_ab), m.FadeIn(ab_group), run_time=0.8)
        self.wait(1.5)

        # Chuyển cảnh sang mô hình hình học
        self.play(
            m.FadeOut(card_intro),
            m.FadeOut(intro_content),
            m.FadeOut(box_ab),
            m.FadeOut(ab_group),
            run_time=0.6,
        )

        # ======================================================================
        # PHẦN 2: MIỀN NGHIỆM HÌNH HỌC TRÊN HỆ TRỤC OXY
        # ======================================================================
        # Cột trái: Trục Oxy và Miền nghiệm ngũ giác OABCD
        # Đặt tâm axes tại x = -3.2, y = -0.1
        axes = m.Axes(
            x_range=[0, 260, 50],
            y_range=[0, 300, 50],
            x_length=5.6,
            y_length=4.8,
            axis_config={"color": MUTED, "stroke_width": 1.5},
        ).move_to([-3.4, -0.1, 0])
        axes.add_coordinates()

        lbl_x = m.Text("x (Mũ I)", font_size=16, color=BLUE).next_to(axes.x_axis.get_end(), m.DR, buff=0.08)
        lbl_y = m.Text("y (Mũ II)", font_size=16, color=BLUE).next_to(axes.y_axis.get_end(), m.UL, buff=0.08)

        # Các điểm đỉnh miền nghiệm
        p_O = axes.c2p(0, 0)
        p_A = axes.c2p(200, 0)
        p_B = axes.c2p(200, 80)
        p_C = axes.c2p(120, 240)
        p_D = axes.c2p(0, 240)

        # Các đường ranh giới
        line_x200 = m.Line(axes.c2p(200, 0), axes.c2p(200, 280), color=ORANGE, stroke_width=2)
        lbl_line_x = m.MathTex(r"x = 200", font_size=18, color=ORANGE).next_to(line_x200.get_top(), m.UP, buff=0.08)

        line_y240 = m.Line(axes.c2p(0, 240), axes.c2p(250, 240), color=GOLD, stroke_width=2)
        lbl_line_y = m.MathTex(r"y = 240", font_size=18, color=GOLD).next_to(line_y240.get_right(), m.RIGHT, buff=0.08)

        line_time = m.Line(axes.c2p(100, 280), axes.c2p(245, -10), color=CYAN, stroke_width=2)
        lbl_line_time = m.MathTex(r"2x + y = 480", font_size=18, color=CYAN).next_to(axes.c2p(160, 160), m.UR, buff=0.08)

        # Miền nghiệm đa giác OABCD
        region = m.Polygon(
            p_O, p_A, p_B, p_C, p_D,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.35,
            stroke_width=2.5,
        )

        dots = m.VGroup(
            m.Dot(p_O, color=GOLD, radius=0.06),
            m.Dot(p_A, color=GOLD, radius=0.06),
            m.Dot(p_B, color=GOLD, radius=0.06),
            m.Dot(p_C, color=RED, radius=0.09), # Đỉnh cực đại
            m.Dot(p_D, color=GOLD, radius=0.06),
        )

        lbl_O = m.MathTex(r"O(0, 0)", font_size=15, color=GOLD).next_to(p_O, m.DL, buff=0.08)
        lbl_A = m.MathTex(r"A(200, 0)", font_size=15, color=GOLD).next_to(p_A, m.DOWN, buff=0.1)
        lbl_B = m.MathTex(r"B(200, 80)", font_size=15, color=GOLD).next_to(p_B, m.RIGHT, buff=0.08)
        lbl_C = m.MathTex(r"C(120, 240)", font_size=18, color=RED).next_to(p_C, m.UP, buff=0.1)
        lbl_D = m.MathTex(r"D(0, 240)", font_size=15, color=GOLD).next_to(p_D, m.LEFT, buff=0.08)
        labels_pts = m.VGroup(lbl_O, lbl_A, lbl_B, lbl_C, lbl_D)

        # ======================================================================
        # CỘT PHẢI: TÍNH TOÁN LỢI NHUẬN TẠI CÁC ĐỈNH
        # ======================================================================
        panel_right = m.RoundedRectangle(
            width=6.6,
            height=5.2,
            corner_radius=0.2,
            fill_color=PANEL,
            fill_opacity=0.9,
            stroke_color=MUTED,
            stroke_width=1.5,
        ).move_to([3.4, -0.1, 0])

        right_title = m.Text("2. KHẢO SÁT HÀM MỤC TIÊU", font_size=20, color=GOLD, weight=m.BOLD)
        right_func = m.MathTex(r"F(x, y) = 24x + 15y \quad (\text{nghìn đồng})", font_size=20, color=INK)

        val_O = m.MathTex(r"\bullet \; F(0, 0) = 0", font_size=18, color=INK)
        val_A = m.MathTex(r"\bullet \; F(200, 0) = 24(200) + 15(0) = 4.800", font_size=18, color=INK)
        val_B = m.MathTex(r"\bullet \; F(200, 80) = 24(200) + 15(80) = 6.000", font_size=18, color=INK)
        val_C = m.MathTex(r"\bullet \; F(120, 240) = 24(120) + 15(240) = 6.480 \; \mathbf{(MAX)}", font_size=19, color=GOLD)
        val_D = m.MathTex(r"\bullet \; F(0, 240) = 24(0) + 15(240) = 3.600", font_size=18, color=INK)

        eval_c = m.Text("c) Sản xuất 120 mũ I, 240 mũ II lãi cao nhất: ĐÚNG", font_size=15, color=GREEN)
        eval_d = m.Text("d) Số tiền lãi cao nhất là 6.480.000 đồng: ĐÚNG", font_size=15, color=GREEN)

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

        # Hiệu ứng vẽ đồ thị cột trái
        self.play(m.Create(axes), m.Write(lbl_x), m.Write(lbl_y), run_time=1.0)
        self.play(
            m.Create(line_x200), m.Write(lbl_line_x),
            m.Create(line_y240), m.Write(lbl_line_y),
            m.Create(line_time), m.Write(lbl_line_time),
            run_time=1.0,
        )
        self.play(m.FadeIn(region), m.FadeIn(dots), m.FadeIn(labels_pts), run_time=1.0)
        self.wait(0.5)

        # Hiển thị tính toán cột phải
        self.play(m.FadeIn(panel_right), m.LaggedStart(*[m.FadeIn(item) for item in calc_group], lag_ratio=0.12), run_time=1.2)
        self.play(m.Circumscribe(val_C, color=GOLD), m.Indicate(dots[3], color=RED, scale_factor=1.5), run_time=1.0)
        self.wait(1.8)

        # ======================================================================
        # PHẦN 3: BẢNG ĐÁP ÁN TỔNG KẾT (FINAL SUMMARY TABLE)
        # ======================================================================
        self.play(
            m.FadeOut(axes), m.FadeOut(lbl_x), m.FadeOut(lbl_y),
            m.FadeOut(line_x200), m.FadeOut(lbl_line_x),
            m.FadeOut(line_y240), m.FadeOut(lbl_line_y),
            m.FadeOut(line_time), m.FadeOut(lbl_line_time),
            m.FadeOut(region), m.FadeOut(dots), m.FadeOut(labels_pts),
            m.FadeOut(panel_right), m.FadeOut(calc_group),
            run_time=0.6,
        )

        card_summary = m.RoundedRectangle(
            width=12.2,
            height=5.2,
            corner_radius=0.2,
            fill_color=PANEL,
            fill_opacity=0.95,
            stroke_color=GOLD,
            stroke_width=2.0,
        ).move_to([0, -0.1, 0])

        sum_title = m.Text("KẾT LUẬN & ĐÁP ÁN CHI TIẾT", font_size=24, color=GOLD, weight=m.BOLD)

        t_sa = m.Text("a) Thời gian làm x mũ I và y mũ II là (2x - y)/60 giờ.", font_size=18, color=INK)
        tag_sa = m.Text("[SAI]", font_size=18, color=RED, weight=m.BOLD)
        row_a = m.VGroup(t_sa, tag_sa).arrange(m.RIGHT, buff=0.4)

        t_sb = m.Text("b) Hệ bất phương trình mô tả các điều kiện của bài toán.", font_size=18, color=INK)
        tag_sb = m.Text("[ĐÚNG]", font_size=18, color=GREEN, weight=m.BOLD)
        row_b = m.VGroup(t_sb, tag_sb).arrange(m.RIGHT, buff=0.4)

        t_sc = m.Text("c) Cần sản xuất 120 chiếc mũ kiểu I và 240 chiếc mũ kiểu II.", font_size=18, color=INK)
        tag_sc = m.Text("[ĐÚNG]", font_size=18, color=GREEN, weight=m.BOLD)
        row_c = m.VGroup(t_sc, tag_sc).arrange(m.RIGHT, buff=0.4)

        t_sd = m.Text("d) Số tiền lãi cao nhất thu được trong ngày là 6.480.000 đồng.", font_size=18, color=INK)
        tag_sd = m.Text("[ĐÚNG]", font_size=18, color=GREEN, weight=m.BOLD)
        row_d = m.VGroup(t_sd, tag_sd).arrange(m.RIGHT, buff=0.4)

        final_box = m.RoundedRectangle(width=9.0, height=0.8, corner_radius=0.15, fill_color="#102544", fill_opacity=1.0, stroke_color=CYAN, stroke_width=1.5)
        final_text = m.Text("ĐÁP ÁN:   a) S   —   b) Đ   —   c) Đ   —   d) Đ", font_size=22, color=GOLD, weight=m.BOLD).move_to(final_box.get_center())
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
        self.wait(2.5)

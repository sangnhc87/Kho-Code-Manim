import os, sys, json, math, hashlib, asyncio, subprocess, textwrap
from pathlib import Path

# ======================================================================
# CẤU HÌNH HỆ THỐNG & BẢN QUYỀN NỘI DUNG
# ======================================================================
TEN_THAY    = "Thầy Nguyễn Văn Sang"
GIONG_DOC   = "vi-VN-NamMinhNeural"
TOC_DO_DOC  = "-5%"
FPS         = 24

ROOT = Path.cwd()
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TIMING_FILE = ROOT / "timing.json"
SCRIPT = ROOT / "temp_scene_12_2_01.py"

def probe_duration(wav_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(wav_path)]
    return float(subprocess.check_output(cmd, encoding="utf-8").strip())

def run_log(cmd, log_file=None):
    print("RUN:", " ".join(cmd))
    subprocess.run(cmd)

# BƯỚC 1: Cài đặt (Colab)
if Path("/content").exists():
    marker = Path("/content/env_ok.txt")
    if not marker.exists():
        print("Cài đặt môi trường...")
        run_log(["sudo", "apt-get", "update", "-y"])
        run_log(["sudo", "apt-get", "install", "-y", "ffmpeg", "libcairo2-dev", "libpango1.0-dev", "texlive-latex-base", "texlive-latex-extra", "texlive-fonts-recommended", "texlive-science", "dvisvgm"])
        run_log([sys.executable, "-m", "pip", "install", "-q", "manim==0.19.0", "edge-tts", "nest_asyncio"])
        marker.write_text("OK")

SLIDES = [
    {
        "title": "1. HỆ TỌA ĐỘ TRONG KHÔNG GIAN OXYZ",
        "lines": [
            r"Hệ trục Oxyz gồm 3 trục vuông góc từng đôi một.",
            r"Trục hoành $Ox$, trục tung $Oy$, trục cao $Oz$.",
            r"Các vectơ đơn vị: $\vec{i}, \vec{j}, \vec{k}$ (độ dài bằng $1$).",
            r"$\vec{i} = (1; 0; 0)$",
            r"$\vec{j} = (0; 1; 0)$",
            r"$\vec{k} = (0; 0; 1)$",
            r"Vectơ $\vec{u} = x\vec{i} + y\vec{j} + z\vec{k} \implies \vec{u} = (x; y; z)$"
        ],
        "narration": (
            "Chào các em. Chào mừng các em đến với chuyên đề Hình học không gian Oxyz. "
            "Bài đầu tiên chúng ta sẽ tìm hiểu về hệ tọa độ và các phép toán vectơ. "
            "Hệ tọa độ Oxyz được tạo thành từ 3 trục vuông góc với nhau từng đôi một tại gốc O. "
            "Đó là trục hoành Ox, trục tung Oy và trục cao Oz. "
            "Trên mỗi trục, ta định nghĩa các vectơ đơn vị lần lượt là i, j, và k có độ dài bằng 1. "
            "Bất kỳ vectơ u nào trong không gian cũng có thể phân tích thành tổng x lần vectơ i, y lần vectơ j, "
            "và z lần vectơ k. Khi đó bộ số x, y, z chính là tọa độ của vectơ u."
        ),
        "scene_type": "oxyz_intro"
    },
    {
        "title": "2. TÍCH VÔ HƯỚNG CỦA HAI VECTƠ",
        "lines": [
            r"Cho $\vec{a} = (x_1; y_1; z_1)$ và $\vec{b} = (x_2; y_2; z_2)$.",
            r"Định nghĩa đại số:",
            r"$\boxed{ \vec{a} \cdot \vec{b} = x_1 x_2 + y_1 y_2 + z_1 z_2 }$",
            r"Bản chất hình học:",
            r"$\boxed{ \vec{a} \cdot \vec{b} = |\vec{a}| \cdot |\vec{b}| \cdot \cos(\vec{a}, \vec{b}) }$",
            r"Ứng dụng 1: Tính góc giữa hai vectơ.",
            r"Ứng dụng 2: Kiểm tra vuông góc $\implies \vec{a} \perp \vec{b} \iff \vec{a} \cdot \vec{b} = 0$"
        ],
        "narration": (
            "Phép toán cực kỳ quan trọng đầu tiên là Tích vô hướng. Giả sử ta có hai vectơ a và b. "
            "Theo công thức tọa độ, tích vô hướng của chúng bằng tổng các tích của tọa độ tương ứng: "
            "hoành nhân hoành, cộng tung nhân tung, cộng cao nhân cao. "
            "Về bản chất hình học, nó chính là tích độ dài của hai vectơ nhân với cosin góc xen giữa. "
            "Từ đây ta suy ra hai ứng dụng sống còn: thứ nhất, tính góc giữa hai vectơ bằng cách chia tích vô hướng "
            "cho tích độ dài; thứ hai, kiểm tra điều kiện vuông góc. Hai vectơ vuông góc khi và chỉ khi "
            "tích vô hướng của chúng bằng 0."
        ),
        "scene_type": "dot_product"
    },
    {
        "title": "3. TÍCH CÓ HƯỚNG CỦA HAI VECTƠ",
        "lines": [
            r"Ký hiệu: $[\vec{a}, \vec{b}]$ hoặc $\vec{a} \times \vec{b}$",
            r"Là MỘT VECTƠ mới, vuông góc với cả $\vec{a}$ và $\vec{b}$.",
            r"Công thức (Định thức xen kẽ):",
            r"$\displaystyle [\vec{a}, \vec{b}] = \left( \begin{vmatrix} y_1 & z_1 \\ y_2 & z_2 \end{vmatrix}; \begin{vmatrix} z_1 & x_1 \\ z_2 & x_2 \end{vmatrix}; \begin{vmatrix} x_1 & y_1 \\ x_2 & y_2 \end{vmatrix} \right)$",
            r"Độ dài: $\big|[\vec{a}, \vec{b}]\big| = |\vec{a}| \cdot |\vec{b}| \cdot \sin(\vec{a}, \vec{b})$",
            r"Độ dài vectơ này chính là Diện tích hình bình hành tạo bởi $\vec{a}$ và $\vec{b}$."
        ],
        "narration": (
            "Tiếp theo là Tích có hướng, một phép toán đặc biệt sinh ra một vectơ hoàn toàn mới. "
            "Đặc tính quan trọng nhất của vectơ mới này là nó vuông góc đồng thời với cả hai vectơ a và b ban đầu. "
            "Tọa độ của tích có hướng được tính bằng định thức xen kẽ như trên màn hình. "
            "Về độ lớn, độ dài của vectơ tích có hướng được tính bằng tích độ dài hai vectơ nhân với sin góc xen giữa. "
            "Đáng chú ý, độ dài này chính bằng diện tích hình bình hành được tạo bởi hai vectơ đó. "
            "Chiều của vectơ kết quả tuân theo quy tắc bàn tay phải."
        ),
        "scene_type": "cross_product"
    },
    {
        "title": "4. ỨNG DỤNG HÌNH HỌC CỦA TÍCH CÓ HƯỚNG",
        "lines": [
            r"1. Diện tích tam giác $ABC$:",
            r"$\displaystyle S_{\triangle ABC} = \frac{1}{2} \Big| [\overrightarrow{AB}, \overrightarrow{AC}] \Big|$",
            r"2. Thể tích khối hộp $ABCD.A'B'C'D'$:",
            r"$\displaystyle V_{\text{Hộp}} = \Big| [\overrightarrow{AB}, \overrightarrow{AD}] \cdot \overrightarrow{AA'} \Big|$",
            r"3. Thể tích khối tứ diện $ABCD$:",
            r"$\displaystyle V_{\text{Tứ diện}} = \frac{1}{6} \Big| [\overrightarrow{AB}, \overrightarrow{AC}] \cdot \overrightarrow{AD} \Big|$"
        ],
        "narration": (
            "Nhờ những đặc tính tuyệt vời của tích có hướng, ta áp dụng để giải quyết nhanh "
            "các bài toán hình học không gian. "
            "Thứ nhất, diện tích tam giác ABC bằng một nửa độ dài vectơ tích có hướng của AB và AC. "
            "Thứ hai, thể tích khối hộp bằng trị tuyệt đối của tích hỗn tạp ba vectơ chung đỉnh. "
            "Cuối cùng, đối với khối tứ diện, thể tích của nó bằng một phần sáu trị tuyệt đối "
            "của tích hỗn tạp ba vectơ cạnh bên. Các công cụ tọa độ này sẽ giúp chúng ta tính toán "
            "thể tích cực kỳ nhanh gọn mà không cần vẽ đường cao."
        ),
        "scene_type": "applications"
    }
]

print("BƯỚC 2: Tổng hợp giọng đọc (1 tệp duy nhất / trang)...")
try: import nest_asyncio; nest_asyncio.apply()
except: pass
import edge_tts

async def make_mp3(text, dest):
    comm = edge_tts.Communicate(text=text, voice=GIONG_DOC, rate=TOC_DO_DOC)
    await comm.save(str(dest))

for index, slide in enumerate(SLIDES):
    text = slide["narration"]
    wav = AUDIO_DIR / f"voice_{index}.wav"
    if not wav.exists():
        mp3 = AUDIO_DIR / f"temp_{index}.mp3"
        asyncio.run(make_mp3(text, mp3))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-ar", "44100", "-ac", "2", str(wav)])
        mp3.unlink(missing_ok=True)
    slide["duration"] = probe_duration(wav)
    print(f"  -> Slide {index+1}: {slide['duration']:.2f}s")

TIMING_FILE.write_text(json.dumps({"slides": SLIDES, "ten_thay": TEN_THAY}, ensure_ascii=False))

SOURCE = r"""
from manim import *
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
timing = json.loads((HERE / "timing.json").read_text(encoding="utf-8"))
SLIDES = timing["slides"]

TMPL = TexTemplate()
TMPL.add_to_preamble(r'\usepackage{amsmath}\usepackage{amssymb}\usepackage{xcolor}')

BG     = "#0b1120"
PANEL  = "#0e1d34"
INK    = "#EDF4FF"
MUTED  = "#7A9ABF"
BLUE_C = "#38BDF8"
CYAN_C = "#3ADEC8"
GOLD   = "#FFD700"
GREEN_C= "#4ADE80"
RED_C  = "#FF6B6B"

class OxyzVectors(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        
        # Footer
        footer = Text(timing["ten_thay"], font="Arial", font_size=20, color=MUTED)
        footer.to_edge(DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(footer)

        axes = ThreeDAxes(
            x_range=[-1, 4, 1], y_range=[-1, 4, 1], z_range=[-1, 4, 1],
            x_length=5, y_length=5, z_length=5,
            axis_config={"color": MUTED, "stroke_width": 2}
        )
        axes_labels = axes.get_axis_labels(
            MathTex("x", color=INK).scale(0.8),
            MathTex("y", color=INK).scale(0.8),
            MathTex("z", color=INK).scale(0.8)
        )
        
        for idx, slide in enumerate(SLIDES):
            audio_path = str(HERE / "audio_cache" / f"voice_{idx}.wav")
            dur = slide["duration"]
            
            # --- TẠO GIAO DIỆN 2D (Cố định trên màn hình) ---
            page_text = Text(f"Trang {idx+1}/{len(SLIDES)}", font="Arial", font_size=20, color=MUTED)
            page_text.to_corner(DR, buff=0.2)
            self.add_fixed_in_frame_mobjects(page_text)

            title = Text(slide["title"], font="Arial", font_size=32, color=GOLD, weight="BOLD")
            title.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
            self.add_fixed_in_frame_mobjects(title)
            
            lines_group = VGroup()
            for line in slide["lines"]:
                if "boxed" in line:
                    mob = MathTex(line, font_size=36, color=GREEN_C, tex_template=TMPL)
                else:
                    mob = MathTex(line, font_size=32, color=INK, tex_template=TMPL)
                lines_group.add(mob)
            
            lines_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            lines_group.to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
            self.add_fixed_in_frame_mobjects(lines_group)
            
            # --- ĐỒ HỌA 3D BÊN DƯỚI ---
            scene_3d = VGroup()
            
            if slide["scene_type"] == "oxyz_intro":
                scene_3d.add(axes, axes_labels)
                self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
                
                i_vec = Arrow3D(start=ORIGIN, end=axes.c2p(1, 0, 0), color=RED_C)
                j_vec = Arrow3D(start=ORIGIN, end=axes.c2p(0, 1, 0), color=GREEN_C)
                k_vec = Arrow3D(start=ORIGIN, end=axes.c2p(0, 0, 1), color=BLUE_C)
                
                i_lbl = MathTex(r"\vec{i}", color=RED_C).next_to(i_vec.get_end(), DOWN)
                j_lbl = MathTex(r"\vec{j}", color=GREEN_C).next_to(j_vec.get_end(), RIGHT)
                k_lbl = MathTex(r"\vec{k}", color=BLUE_C).next_to(k_vec.get_end(), LEFT)
                self.add_fixed_orientation_mobjects(i_lbl, j_lbl, k_lbl)
                
                u_vec = Arrow3D(start=ORIGIN, end=axes.c2p(2, 3, 2), color=CYAN_C)
                u_lbl = MathTex(r"\vec{u}", color=CYAN_C).next_to(u_vec.get_end(), UP)
                self.add_fixed_orientation_mobjects(u_lbl)
                
                scene_3d.add(i_vec, j_vec, k_vec, i_lbl, j_lbl, k_lbl, u_vec, u_lbl)
            
            elif slide["scene_type"] == "dot_product":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=60 * DEGREES, theta=-30 * DEGREES)
                
                v1 = Arrow3D(start=ORIGIN, end=axes.c2p(3, 0, 0), color=RED_C)
                v2 = Arrow3D(start=ORIGIN, end=axes.c2p(2, 2, 0), color=GREEN_C)
                
                l1 = MathTex(r"\vec{a}", color=RED_C).next_to(v1.get_end(), DOWN)
                l2 = MathTex(r"\vec{b}", color=GREEN_C).next_to(v2.get_end(), UP)
                self.add_fixed_orientation_mobjects(l1, l2)
                
                # Angle arc
                arc = Arc(radius=0.8, start_angle=0, angle=PI/4, color=GOLD)
                # Align arc to axes
                arc.apply_matrix(axes.get_basis_matrix())
                
                scene_3d.add(v1, v2, l1, l2, arc)
                
            elif slide["scene_type"] == "cross_product":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)
                
                v1 = Arrow3D(start=ORIGIN, end=axes.c2p(2, -1, 0), color=RED_C)
                v2 = Arrow3D(start=ORIGIN, end=axes.c2p(1, 2, 0), color=GREEN_C)
                # Cross product of (2, -1, 0) and (1, 2, 0) is (0, 0, 5)
                v3 = Arrow3D(start=ORIGIN, end=axes.c2p(0, 0, 3), color=CYAN_C) # scale down for visual
                
                plg = Polygon(ORIGIN, axes.c2p(2, -1, 0), axes.c2p(3, 1, 0), axes.c2p(1, 2, 0), fill_opacity=0.3, fill_color=GOLD, stroke_width=0)
                
                l1 = MathTex(r"\vec{a}", color=RED_C).next_to(v1.get_end(), DOWN)
                l2 = MathTex(r"\vec{b}", color=GREEN_C).next_to(v2.get_end(), UP)
                l3 = MathTex(r"[\vec{a}, \vec{b}]", color=CYAN_C).next_to(v3.get_end(), LEFT)
                self.add_fixed_orientation_mobjects(l1, l2, l3)
                
                scene_3d.add(plg, v1, v2, v3, l1, l2, l3)
                
            elif slide["scene_type"] == "applications":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
                
                # Tetra
                A = axes.c2p(1, 1, 3)
                B = axes.c2p(3, 0, 0)
                C = axes.c2p(0, 3, 0)
                D = ORIGIN
                
                tetra = VGroup(
                    Line3D(A, B, color=BLUE_C), Line3D(B, C, color=BLUE_C), Line3D(C, A, color=BLUE_C),
                    Line3D(A, D, color=BLUE_C), Line3D(B, D, color=BLUE_C), Line3D(C, D, color=BLUE_C)
                )
                lbl_a = MathTex("A", color=INK).next_to(A, UP)
                lbl_b = MathTex("B", color=INK).next_to(B, RIGHT)
                lbl_c = MathTex("C", color=INK).next_to(C, LEFT)
                lbl_d = MathTex("D", color=INK).next_to(D, DOWN)
                self.add_fixed_orientation_mobjects(lbl_a, lbl_b, lbl_c, lbl_d)
                
                scene_3d.add(tetra, lbl_a, lbl_b, lbl_c, lbl_d)

            # --- RENDER VÀ ĐỒNG BỘ ÂM THANH ---
            # Chỉ hiện title trước, sau đó phát âm thanh và hiện từ từ
            self.play(FadeIn(title))
            self.add_sound(audio_path)
            
            # Tính thời gian reveal
            reveal_time = dur * 0.8
            time_per_line = reveal_time / len(lines_group)
            
            # Hiện hình ảnh 3D lúc đầu
            self.play(FadeIn(scene_3d), run_time=1.5)
            
            for i, mob in enumerate(lines_group):
                self.play(FadeIn(mob, shift=UP*0.2), run_time=1)
                self.wait(time_per_line - 1 if time_per_line > 1 else 0)
                
            # Chờ âm thanh chạy hết
            self.wait(dur * 0.2 + 0.5)
            
            # Xóa để sang slide mới
            self.play(FadeOut(title), FadeOut(lines_group), FadeOut(scene_3d), FadeOut(page_text), run_time=1)

"""

SCRIPT.write_text(SOURCE, encoding="utf-8")

print("BƯỚC 3: Render video Manim 3D...")
MEDIA_DIR = ROOT / "media"
# Use -qm (Medium quality) for fast rendering in dev, but GitHub actions will use this script
run_log([sys.executable, "-m", "manim", "-ql", "--fps", str(FPS), "--media_dir", str(MEDIA_DIR), "-o", "HeToaDoOxyz_Vecto", str(SCRIPT), "OxyzVectors"])

candidates = list(MEDIA_DIR.rglob("HeToaDoOxyz_Vecto.mp4"))
if not candidates:
    print("Lỗi render Manim.")
else:
    print(f"Xong! Video lưu tại: {candidates[0]}")
    # Cleanup temp script
    SCRIPT.unlink(missing_ok=True)

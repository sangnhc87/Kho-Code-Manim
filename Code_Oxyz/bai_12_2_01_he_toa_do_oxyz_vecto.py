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

# Cấu trúc nội dung sư phạm sâu sắc và chi tiết
SLIDES = [
    {
        "title": "1. SỰ HÌNH THÀNH HỆ TRỤC OXYZ",
        "lines": [
            r"Từ hình học phẳng Oxy 2 chiều, ta thêm chiều thứ 3: Chiều Sâu.",
            r"Hệ Oxyz gồm 3 trục vuông góc từng đôi một tại gốc tọa độ $O$.",
            r"$\bullet$ Trục hoành $Ox$, Trục tung $Oy$, Trục cao $Oz$.",
            r"$\bullet$ 3 mặt phẳng tọa độ: $(Oxy), (Oyz), (Ozx)$ chia không gian thành 8 góc phần tám.",
            r"Trên mỗi trục, định nghĩa các vectơ đơn vị $\vec{i}, \vec{j}, \vec{k}$ có độ dài bằng $1$."
        ],
        "narration": (
            "Chào các em. Chào mừng các em đến với chuyên đề Tọa độ không gian Oxyz. "
            "Để bước từ hình học phẳng hai chiều Oxy lên không gian ba chiều, chúng ta cần bổ sung thêm một chiều nữa, đó là chiều cao hay chiều sâu. "
            "Hệ tọa độ Oxyz được tạo thành từ ba trục phân biệt vuông góc với nhau từng đôi một tại gốc tọa độ O. "
            "Đó là trục hoành O x, trục tung O y và trục cao O z. "
            "Ba trục này tạo thành ba mặt phẳng tọa độ O x y, O y z và O z x vuông góc với nhau, chia không gian thành 8 góc phần tám. "
            "Để định lượng hóa không gian này, trên mỗi trục, ta đặt các vectơ đơn vị lần lượt là i, j, và k. "
            "Mỗi vectơ này đều có độ dài chuẩn bằng một đơn vị."
        ),
        "scene_type": "oxyz_intro"
    },
    {
        "title": "2. TỌA ĐỘ VECTƠ VÀ TỌA ĐỘ ĐIỂM",
        "lines": [
            r"Mọi vectơ trong không gian đều được phân tích duy nhất theo hệ cơ sở:",
            r"$\boxed{\vec{u} = x\vec{i} + y\vec{j} + z\vec{k} \implies \vec{u} = (x; y; z)}$",
            r"Đối với một điểm $M$ bất kỳ trong không gian:",
            r"Tọa độ của điểm $M$ chính là tọa độ của vectơ vị trí $\overrightarrow{OM}$.",
            r"$\overrightarrow{OM} = (x; y; z) \implies M(x; y; z)$"
        ],
        "narration": (
            "Nhờ hệ cơ sở gồm ba vectơ đơn vị i, j, k, không gian hình học đã được đại số hóa hoàn toàn. "
            "Theo định lý phân tích vectơ, mọi vectơ u bất kỳ trong không gian đều được phân tích duy nhất "
            "thành tổng của x lần vectơ i, cộng y lần vectơ j, cộng z lần vectơ k. "
            "Bộ ba số x, y, z đó được gọi là tọa độ của vectơ u. "
            "Và để xác định tọa độ của một điểm M bất kỳ, ta chỉ cần gắn nó với gốc tọa độ O để tạo thành vectơ vị trí O M. "
            "Tọa độ của vectơ O M chính là tọa độ của điểm M."
        ),
        "scene_type": "vector_point"
    },
    {
        "title": "3. TÍCH VÔ HƯỚNG - BẢN CHẤT HÌNH HỌC",
        "lines": [
            r"Cho $\vec{a} = (x_1; y_1; z_1)$ và $\vec{b} = (x_2; y_2; z_2)$.",
            r"Về mặt đại số:",
            r"$\boxed{ \vec{a} \cdot \vec{b} = x_1 x_2 + y_1 y_2 + z_1 z_2 }$",
            r"Về mặt hình học (Bản chất cực kỳ quan trọng):",
            r"$\boxed{ \vec{a} \cdot \vec{b} = |\vec{a}| \cdot |\vec{b}| \cdot \cos(\vec{a}, \vec{b}) }$",
            r"Đại lượng này vô hướng (là một con số, không phải vectơ)."
        ],
        "narration": (
            "Phép toán cốt lõi đầu tiên là Tích vô hướng. Tại sao gọi là tích vô hướng? "
            "Bởi vì kết quả của phép nhân hai vectơ này sinh ra một con số, không có phương chiều. "
            "Về mặt đại số, ta tính rất dễ dàng bằng tổng các tích tọa độ: hoành nhân hoành, cộng tung nhân tung, cộng cao nhân cao. "
            "Nhưng bản chất hình học của nó mới thực sự sâu sắc. Tích vô hướng đo lường mức độ đồng hướng của hai vectơ. "
            "Nó bằng độ dài vectơ a, nhân độ dài vectơ b, nhân với cosin của góc xen giữa. "
            "Nếu hai vectơ cùng chiều, cosin bằng một, tích vô hướng lớn nhất. Nếu chúng vuông góc, cosin bằng không, tích vô hướng triệt tiêu."
        ),
        "scene_type": "dot_product"
    },
    {
        "title": "4. ỨNG DỤNG SỐNG CÒN CỦA TÍCH VÔ HƯỚNG",
        "lines": [
            r"Từ công thức bản chất, ta rút ra 2 ứng dụng nền tảng:",
            r"$\bullet$ Tính góc giữa hai vectơ:",
            r"$\displaystyle \cos(\vec{a}, \vec{b}) = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}| \cdot |\vec{b}|} = \frac{x_1 x_2 + y_1 y_2 + z_1 z_2}{\sqrt{x_1^2+y_1^2+z_1^2} \sqrt{x_2^2+y_2^2+z_2^2}}$",
            r"$\bullet$ Điều kiện vuông góc (Xương sống của Oxyz):",
            r"$\boxed{ \vec{a} \perp \vec{b} \iff \vec{a} \cdot \vec{b} = 0 \iff x_1 x_2 + y_1 y_2 + z_1 z_2 = 0 }$"
        ],
        "narration": (
            "Từ bản chất hình học đó, tích vô hướng trở thành công cụ tối thượng để giải quyết góc và sự vuông góc. "
            "Ứng dụng thứ nhất là tính góc. Cosin của góc giữa hai vectơ bằng tích vô hướng chia cho tích độ dài. "
            "Bạn chỉ cần ráp tọa độ vào công thức đại số là lập tức tính được góc trong không gian mà không cần kẻ vẽ phụ. "
            "Ứng dụng thứ hai, và cũng là xương sống của mọi bài toán Oxyz, đó là kiểm tra điều kiện vuông góc. "
            "Hai vectơ vuông góc với nhau khi và chỉ khi tích vô hướng của chúng bằng 0. "
            "Chỉ bằng một phương trình đại số đơn giản, ta kiểm soát được cả sự vuông góc của hình học không gian."
        ),
        "scene_type": "dot_applications"
    },
    {
        "title": "5. TÍCH CÓ HƯỚNG - VŨ KHÍ BÍ MẬT CỦA OXYZ",
        "lines": [
            r"Ký hiệu: $[\vec{a}, \vec{b}]$ hoặc $\vec{a} \times \vec{b}$. Kết quả là MỘT VECTƠ mới.",
            r"Công thức tọa độ (Định thức xen kẽ vòng quanh):",
            r"$\displaystyle [\vec{a}, \vec{b}] = \left( \begin{vmatrix} y_1 & z_1 \\ y_2 & z_2 \end{vmatrix}; \begin{vmatrix} z_1 & x_1 \\ z_2 & x_2 \end{vmatrix}; \begin{vmatrix} x_1 & y_1 \\ x_2 & y_2 \end{vmatrix} \right)$",
            r"Đặc tính 1 (Phương chiều): Vectơ mới vuông góc với cả $\vec{a}$ và $\vec{b}$.",
            r"$\implies [\vec{a}, \vec{b}] \perp \vec{a}$ và $[\vec{a}, \vec{b}] \perp \vec{b}$. Tuân theo quy tắc bàn tay phải."
        ],
        "narration": (
            "Nếu tích vô hướng trả về một con số, thì tích có hướng lại là vũ khí độc quyền của không gian ba chiều Oxyz. "
            "Nó nhận vào hai vectơ, và đẻ ra một vectơ thứ ba hoàn toàn mới. "
            "Công thức tọa độ của nó là một bộ ba định thức cấp hai được viết theo chu trình vòng quanh x y z để tránh nhầm dấu. "
            "Về mặt hình học, vectơ sinh ra mang một sứ mệnh đặc biệt: nó bắt buộc phải vuông góc đồng thời với cả hai vectơ ban đầu. "
            "Nói cách khác, nó chính là vectơ pháp tuyến của mặt phẳng chứa hai vectơ a và b. "
            "Về mặt định hướng, nó vươn lên theo quy tắc bàn tay phải."
        ),
        "scene_type": "cross_product"
    },
    {
        "title": "6. Ý NGHĨA ĐỘ LỚN CỦA TÍCH CÓ HƯỚNG",
        "lines": [
            r"Đặc tính 2 (Độ lớn): Liên quan đến diện tích.",
            r"$\big|[\vec{a}, \vec{b}]\big| = |\vec{a}| \cdot |\vec{b}| \cdot \sin(\vec{a}, \vec{b})$",
            r"So sánh với tích vô hướng dùng $\cos$, tích có hướng dùng $\sin$.",
            r"Về mặt hình học, độ dài của tích có hướng bằng chính Diện tích hình bình hành tạo bởi $\vec{a}$ và $\vec{b}$.",
            r"$\boxed{ S_{\text{Hình bình hành}} = \big|[\vec{a}, \vec{b}]\big| }$"
        ],
        "narration": (
            "Còn về độ lớn, độ dài của vectơ tích có hướng được định nghĩa bằng tích độ dài hai vectơ ban đầu, nhưng nhân với sin của góc xen giữa. "
            "Các em hãy nhớ, vô hướng thì dùng cosin, có hướng thì dùng sin. "
            "Điều kỳ diệu nằm ở chỗ, theo công thức hình học phẳng, cạnh nhân cạnh nhân sin góc xen giữa chính là diện tích hình bình hành. "
            "Vậy bản chất độ lớn của vectơ tích có hướng chính là diện tích của hình bình hành được căng bởi hai vectơ a và b. "
            "Đây là một cầu nối tuyệt đẹp giữa Đại số tọa độ và Hình học diện tích."
        ),
        "scene_type": "cross_magnitude"
    },
    {
        "title": "7. ỨNG DỤNG TÍCH CÓ HƯỚNG TRONG DIỆN TÍCH TỌA ĐỘ",
        "lines": [
            r"Từ ý nghĩa hình bình hành, ta chia đôi để tính diện tích tam giác:",
            r"$\boxed{ S_{\triangle ABC} = \frac{1}{2} \Big| [\overrightarrow{AB}, \overrightarrow{AC}] \Big| }$",
            r"Ứng dụng 2: Điều kiện đồng phẳng của ba vectơ.",
            r"Ba vectơ $\vec{a}, \vec{b}, \vec{c}$ đồng phẳng khi và chỉ khi:",
            r"$\boxed{ [\vec{a}, \vec{b}] \cdot \vec{c} = 0 }$"
        ],
        "narration": (
            "Dựa vào ý nghĩa diện tích đó, ta có công thức ứng dụng cực mạnh để tính diện tích tam giác trong không gian. "
            "Diện tích tam giác A B C đơn giản bằng một nửa độ dài vectơ tích có hướng của hai cạnh A B và A C. "
            "Thêm một ứng dụng sắc bén nữa: điều kiện đồng phẳng. "
            "Tích có hướng của a và b tạo ra một vectơ vuông góc với mặt phẳng chứa a và b. "
            "Nếu vectơ c nằm trong cùng mặt phẳng đó, thì c phải vuông góc với vectơ tích có hướng kia. "
            "Nên tích vô hướng của chúng sẽ bằng 0. Đây chính là điều kiện đồng phẳng của ba vectơ."
        ),
        "scene_type": "cross_applications"
    },
    {
        "title": "8. TÍCH HỖN TẠP & BÀI TOÁN THỂ TÍCH",
        "lines": [
            r"Biểu thức $[\vec{a}, \vec{b}] \cdot \vec{c}$ được gọi là TÍCH HỖN TẠP.",
            r"Thể tích khối hộp $ABCD.A'B'C'D'$ căng bởi 3 vectơ xuất phát từ cùng một đỉnh:",
            r"$\boxed{ V_{\text{Hộp}} = \Big| [\overrightarrow{AB}, \overrightarrow{AD}] \cdot \overrightarrow{AA'} \Big| }$",
            r"Thể tích khối tứ diện $ABCD$ (bằng $\frac{1}{6}$ thể tích khối hộp tương ứng):",
            r"$\boxed{ V_{\text{Tứ diện}} = \frac{1}{6} \Big| [\overrightarrow{AB}, \overrightarrow{AC}] \cdot \overrightarrow{AD} \Big| }$"
        ],
        "narration": (
            "Và cuối cùng, khi ta lấy tích có hướng của hai vectơ, rồi mang kết quả đó nhân vô hướng với vectơ thứ ba, ta gọi đó là Tích hỗn tạp. "
            "Trị tuyệt đối của tích hỗn tạp mang một ý nghĩa hình học vĩ đại: nó chính là Thể tích của khối hộp được căng bởi ba vectơ đó. "
            "Vì tích có hướng cho ta diện tích đáy, còn tích vô hướng với vectơ thứ ba sẽ bóc tách ra thành phần chiều cao. "
            "Khối tứ diện có thể tích bằng một phần sáu khối hộp. Nên thể tích tứ diện A B C D bằng một phần sáu "
            "trị tuyệt đối tích hỗn tạp của ba vectơ cạnh xuất phát từ đỉnh A. "
            "Nắm vững các công cụ này, bài toán Oxyz sẽ trở nên vô cùng đơn giản."
        ),
        "scene_type": "mixed_product"
    }
]

print("BƯỚC 1: Xử lý âm thanh AI...")
try:
    import edge_tts, nest_asyncio
    nest_asyncio.apply()
except:
    pass

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

print("BƯỚC 2: Sinh mã nguồn Manim chuyên sâu...")
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
ORANGE = "#FB923C"

class OxyzVectorsDetailed(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        
        # Footer branding
        footer = Text(timing["ten_thay"], font="Arial", font_size=20, color=MUTED)
        footer.to_edge(DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(footer)

        axes = ThreeDAxes(
            x_range=[-2, 5, 1], y_range=[-2, 5, 1], z_range=[-2, 5, 1],
            x_length=6, y_length=6, z_length=6,
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
            
            # --- UI PANEL ---
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
            
            # --- 3D SCENE CONTENT ---
            scene_3d = VGroup()
            
            if slide["scene_type"] == "oxyz_intro":
                scene_3d.add(axes, axes_labels)
                self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
                
                # Planes
                xy_plane = Polygon(axes.c2p(0,0,0), axes.c2p(4,0,0), axes.c2p(4,4,0), axes.c2p(0,4,0), fill_color=BLUE_C, fill_opacity=0.1, stroke_width=0)
                yz_plane = Polygon(axes.c2p(0,0,0), axes.c2p(0,4,0), axes.c2p(0,4,4), axes.c2p(0,0,4), fill_color=RED_C, fill_opacity=0.1, stroke_width=0)
                zx_plane = Polygon(axes.c2p(0,0,0), axes.c2p(4,0,0), axes.c2p(4,0,4), axes.c2p(0,0,4), fill_color=GREEN_C, fill_opacity=0.1, stroke_width=0)
                
                i_vec = Arrow3D(start=ORIGIN, end=axes.c2p(1, 0, 0), color=RED_C)
                j_vec = Arrow3D(start=ORIGIN, end=axes.c2p(0, 1, 0), color=GREEN_C)
                k_vec = Arrow3D(start=ORIGIN, end=axes.c2p(0, 0, 1), color=BLUE_C)
                
                i_lbl = MathTex(r"\vec{i}", color=RED_C).next_to(i_vec.get_end(), DOWN)
                j_lbl = MathTex(r"\vec{j}", color=GREEN_C).next_to(j_vec.get_end(), RIGHT)
                k_lbl = MathTex(r"\vec{k}", color=BLUE_C).next_to(k_vec.get_end(), LEFT)
                self.add_fixed_orientation_mobjects(i_lbl, j_lbl, k_lbl)
                
                scene_3d.add(xy_plane, yz_plane, zx_plane, i_vec, j_vec, k_vec, i_lbl, j_lbl, k_lbl)
            
            elif slide["scene_type"] == "vector_point":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=60 * DEGREES, theta=-30 * DEGREES)
                
                M = axes.c2p(3, 4, 3)
                u_vec = Arrow3D(start=ORIGIN, end=M, color=CYAN_C)
                
                # Projections
                Mx = axes.c2p(3, 0, 0)
                My = axes.c2p(0, 4, 0)
                Mz = axes.c2p(0, 0, 3)
                Mxy = axes.c2p(3, 4, 0)
                
                d1 = DashedLine(M, Mxy, color=MUTED)
                d2 = DashedLine(Mxy, Mx, color=MUTED)
                d3 = DashedLine(Mxy, My, color=MUTED)
                d4 = DashedLine(M, Mz, color=MUTED)
                
                dot_M = Dot3D(M, color=GOLD, radius=0.1)
                lbl_M = MathTex("M(x, y, z)", color=GOLD).next_to(M, UP)
                self.add_fixed_orientation_mobjects(lbl_M)
                
                scene_3d.add(u_vec, d1, d2, d3, d4, dot_M, lbl_M)

            elif slide["scene_type"] == "dot_product":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=75 * DEGREES, theta=-20 * DEGREES)
                
                v1 = Arrow3D(start=ORIGIN, end=axes.c2p(4, 0, 0), color=RED_C)
                v2 = Arrow3D(start=ORIGIN, end=axes.c2p(3, 3, 0), color=GREEN_C)
                
                l1 = MathTex(r"\vec{a}", color=RED_C).next_to(v1.get_end(), DOWN)
                l2 = MathTex(r"\vec{b}", color=GREEN_C).next_to(v2.get_end(), UP)
                self.add_fixed_orientation_mobjects(l1, l2)
                
                # Show projection
                proj_pt = axes.c2p(3, 0, 0)
                d_proj = DashedLine(axes.c2p(3, 3, 0), proj_pt, color=YELLOW)
                
                # Angle arc
                arc = Arc(radius=1.0, start_angle=0, angle=PI/4, color=GOLD)
                arc.apply_matrix(axes.get_basis_matrix())
                lbl_angle = MathTex(r"\alpha", color=GOLD).move_to(axes.c2p(1.2, 0.5, 0))
                self.add_fixed_orientation_mobjects(lbl_angle)
                
                scene_3d.add(v1, v2, l1, l2, d_proj, arc, lbl_angle)
                
            elif slide["scene_type"] == "dot_applications":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
                
                # Show perpendicular vectors
                v1 = Arrow3D(start=ORIGIN, end=axes.c2p(3, 0, 0), color=RED_C)
                v2 = Arrow3D(start=ORIGIN, end=axes.c2p(0, 3, 0), color=GREEN_C)
                
                sq = VGroup(
                    Line3D(axes.c2p(0.5,0,0), axes.c2p(0.5,0.5,0), color=GOLD),
                    Line3D(axes.c2p(0.5,0.5,0), axes.c2p(0,0.5,0), color=GOLD)
                )
                
                l1 = MathTex(r"\vec{a}", color=RED_C).next_to(v1.get_end(), DOWN)
                l2 = MathTex(r"\vec{b}", color=GREEN_C).next_to(v2.get_end(), LEFT)
                self.add_fixed_orientation_mobjects(l1, l2)
                
                scene_3d.add(v1, v2, sq, l1, l2)

            elif slide["scene_type"] == "cross_product":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)
                
                v1 = Arrow3D(start=ORIGIN, end=axes.c2p(3, 0, 0), color=RED_C)
                v2 = Arrow3D(start=ORIGIN, end=axes.c2p(1.5, 3, 0), color=GREEN_C)
                # Cross product is (0, 0, 9)
                v3 = Arrow3D(start=ORIGIN, end=axes.c2p(0, 0, 4), color=CYAN_C) 
                
                l1 = MathTex(r"\vec{a}", color=RED_C).next_to(v1.get_end(), DOWN)
                l2 = MathTex(r"\vec{b}", color=GREEN_C).next_to(v2.get_end(), LEFT)
                l3 = MathTex(r"[\vec{a}, \vec{b}]", color=CYAN_C).next_to(v3.get_end(), RIGHT)
                self.add_fixed_orientation_mobjects(l1, l2, l3)
                
                # Right angle indicators
                ra1 = VGroup(Line3D(axes.c2p(0.5,0,0), axes.c2p(0.5,0,0.5), color=GOLD), Line3D(axes.c2p(0.5,0,0.5), axes.c2p(0,0,0.5), color=GOLD))
                ra2 = VGroup(Line3D(axes.c2p(0.25,0.5,0), axes.c2p(0.25,0.5,0.5), color=GOLD), Line3D(axes.c2p(0.25,0.5,0.5), axes.c2p(0,0,0.5), color=GOLD))
                
                scene_3d.add(v1, v2, v3, l1, l2, l3, ra1, ra2)
                
            elif slide["scene_type"] == "cross_magnitude":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
                
                v1 = Arrow3D(start=ORIGIN, end=axes.c2p(4, 0, 0), color=RED_C)
                v2 = Arrow3D(start=ORIGIN, end=axes.c2p(2, 3, 0), color=GREEN_C)
                
                # Parallelogram
                plg = Polygon(ORIGIN, axes.c2p(4, 0, 0), axes.c2p(6, 3, 0), axes.c2p(2, 3, 0), fill_opacity=0.4, fill_color=YELLOW, stroke_width=2, stroke_color=YELLOW)
                
                l1 = MathTex(r"\vec{a}", color=RED_C).next_to(v1.get_end(), DOWN)
                l2 = MathTex(r"\vec{b}", color=GREEN_C).next_to(v2.get_end(), LEFT)
                lbl_S = MathTex("S", color=INK).move_to(axes.c2p(3, 1.5, 0.1))
                self.add_fixed_orientation_mobjects(l1, l2, lbl_S)
                
                scene_3d.add(v1, v2, plg, l1, l2, lbl_S)

            elif slide["scene_type"] == "cross_applications":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
                
                A = axes.c2p(1, 1, 1)
                B = axes.c2p(4, 1, 1)
                C = axes.c2p(2, 4, 1)
                
                tri = Polygon(A, B, C, fill_opacity=0.4, fill_color=BLUE_C, stroke_width=2, stroke_color=BLUE_C)
                
                lbl_A = MathTex("A", color=INK).next_to(A, DOWN)
                lbl_B = MathTex("B", color=INK).next_to(B, DOWN)
                lbl_C = MathTex("C", color=INK).next_to(C, UP)
                self.add_fixed_orientation_mobjects(lbl_A, lbl_B, lbl_C)
                
                vec_AB = Arrow3D(start=A, end=B, color=RED_C)
                vec_AC = Arrow3D(start=A, end=C, color=GREEN_C)
                
                scene_3d.add(tri, lbl_A, lbl_B, lbl_C, vec_AB, vec_AC)

            elif slide["scene_type"] == "mixed_product":
                scene_3d.add(axes)
                self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)
                
                # Parallelepiped
                O_pt = ORIGIN
                v1_pt = axes.c2p(3, 0, 0)
                v2_pt = axes.c2p(1, 3, 0)
                v3_pt = axes.c2p(0, 1, 3)
                
                p1 = Polygon(O_pt, v1_pt, axes.c2p(4,3,0), v2_pt, fill_opacity=0.3, fill_color=ORANGE, stroke_width=2)
                p2 = Polygon(v3_pt, axes.c2p(3,1,3), axes.c2p(4,4,3), axes.c2p(1,4,3), fill_opacity=0.3, fill_color=ORANGE, stroke_width=2)
                
                edges = VGroup(
                    Line3D(O_pt, v3_pt, color=INK),
                    Line3D(v1_pt, axes.c2p(3,1,3), color=INK),
                    Line3D(v2_pt, axes.c2p(1,4,3), color=INK),
                    Line3D(axes.c2p(4,3,0), axes.c2p(4,4,3), color=INK)
                )
                
                v_a = Arrow3D(start=O_pt, end=v1_pt, color=RED_C)
                v_b = Arrow3D(start=O_pt, end=v2_pt, color=GREEN_C)
                v_c = Arrow3D(start=O_pt, end=v3_pt, color=CYAN_C)
                
                l_a = MathTex(r"\vec{a}", color=RED_C).next_to(v_a.get_end(), DOWN)
                l_b = MathTex(r"\vec{b}", color=GREEN_C).next_to(v_b.get_end(), LEFT)
                l_c = MathTex(r"\vec{c}", color=CYAN_C).next_to(v_c.get_end(), UP)
                self.add_fixed_orientation_mobjects(l_a, l_b, l_c)
                
                scene_3d.add(p1, p2, edges, v_a, v_b, v_c, l_a, l_b, l_c)


            # --- RENDER VÀ ĐỒNG BỘ ÂM THANH ---
            self.play(FadeIn(title))
            self.add_sound(audio_path)
            
            reveal_time = dur * 0.8
            time_per_line = reveal_time / len(lines_group)
            
            # Animate 3D Scene based on type
            if slide["scene_type"] == "cross_product":
                # Only show a, b first, then cross product
                v3 = scene_3d[2]; l3 = scene_3d[5]
                scene_3d.remove(v3, l3)
                self.play(FadeIn(scene_3d), run_time=1.5)
                # Show cross product later
                self.play(GrowArrow(v3), Write(l3), run_time=1)
                scene_3d.add(v3, l3)
            else:
                self.play(FadeIn(scene_3d), run_time=1.5)
            
            # Text lines reveal
            for i, mob in enumerate(lines_group):
                self.play(FadeIn(mob, shift=UP*0.2), run_time=1)
                self.wait(time_per_line - 1 if time_per_line > 1 else 0)
                
            self.wait(dur * 0.2 + 0.5)
            self.play(FadeOut(title), FadeOut(lines_group), FadeOut(scene_3d), FadeOut(page_text), run_time=1)

        # Outro màn hình kết thúc
        outro_title = Text("CHUYÊN ĐỀ OXYZ - BÀI GIẢNG MANIM ĐỘT PHÁ", font="Arial", font_size=40, color=GOLD, weight="BOLD")
        outro_sub = Text("Sản xuất bởi Thầy Nguyễn Văn Sang", font="Arial", font_size=28, color=INK)
        outro_grp = VGroup(outro_title, outro_sub).arrange(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(outro_grp)
        self.play(FadeIn(outro_grp))
        self.wait(3)

"""

SCRIPT.write_text(SOURCE, encoding="utf-8")

print("BƯỚC 3: Render video Manim 3D chuyên sâu...")
MEDIA_DIR = ROOT / "media"
run_log([sys.executable, "-m", "manim", "-ql", "--fps", str(FPS), "--media_dir", str(MEDIA_DIR), "-o", "HeToaDoOxyz_Vecto", str(SCRIPT), "OxyzVectorsDetailed"])

candidates = list(MEDIA_DIR.rglob("HeToaDoOxyz_Vecto.mp4"))
if not candidates:
    print("Lỗi render Manim.")
else:
    print(f"Xong! Video lưu tại: {candidates[0]}")
    SCRIPT.unlink(missing_ok=True)

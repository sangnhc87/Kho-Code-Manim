# ======================================================================
# GOOGLE COLAB — 1-CELL PIPELINE
# CHỦ ĐỀ: TỐC ĐỘ NƯỚC DÂNG (BÀI TOÁN THỰC TẾ TRONG KHÔNG GIAN 3D)
# LƯU Ý: Khắc phục hoàn toàn lỗi âm thanh rời rạc (1 file audio dài/slide)
# Sử dụng ThreeDScene để vẽ 3D chuẩn xác, có nước dâng thực tế.
# ======================================================================

import os, sys, json, math, time, asyncio, hashlib, subprocess
from pathlib import Path
import numpy as np

TEN_THAY    = "Thầy Nguyễn Văn Sang"
GIONG_DOC   = "vi-VN-NamMinhNeural"
TOC_DO_DOC  = "+0%"
RESOLUTION  = "1280,720"
FPS         = 30

if Path("/content").exists():
    ROOT = Path("/content/NuocDang3D")
else:
    ROOT = Path.cwd() / "NuocDang3D_out"

ROOT.mkdir(parents=True, exist_ok=True)
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TIMING_FILE = ROOT / "timing.json"
SCRIPT = ROOT / "manim_scene.py"

os.environ["DEBIAN_FRONTEND"] = "noninteractive"
os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"

def run_log(command, logfile=None):
    if logfile:
        with Path(logfile).open("w", encoding="utf-8") as f:
            res = subprocess.run([str(x) for x in command], stdout=f, stderr=subprocess.STDOUT, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Lỗi lệnh. Xem log: {logfile}")
    else:
        subprocess.run([str(x) for x in command], check=True)

def probe_duration(path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                            capture_output=True, text=True, check=True)
    val = float(result.stdout.strip())
    return val

print("BƯỚC 1: Kiểm tra môi trường...")
marker = ROOT / "env_ok.txt"
if Path("/content").exists() and not marker.exists():
    print("  -> Đang cài đặt thư viện...")
    run_log(["apt-get", "update", "-qq"], ROOT / "apt.log")
    run_log(["apt-get", "install", "-y", "-qq", "ffmpeg", "texlive", "texlive-latex-extra", "texlive-fonts-extra", "texlive-science"], ROOT / "apt.log")
    run_log([sys.executable, "-m", "pip", "install", "-q", "manim==0.19.0", "edge-tts", "nest_asyncio"], ROOT / "pip.log")
    marker.write_text("OK")

SLIDES = [
    {
        "title": "BÀI TOÁN 1: BỂ NƯỚC HÌNH TRỤ ĐỨNG",
        "lines": [
            r"Cho một bể nước hình trụ đứng có bán kính đáy $R$ không đổi.",
            r"Nước được bơm vào bể với lưu lượng không đổi $v \ (\text{m}^3/\text{s})$.",
            r"Hãy tìm tốc độ nước dâng $h'(t)$ trong bể."
        ],
        "narration": (
            "Chào các em. Hôm nay chúng ta sẽ giải quyết bài toán thực tế về tốc độ nước dâng "
            "thông qua ứng dụng của đạo hàm. Bài toán đầu tiên: Cho một bể nước hình trụ đứng "
            "có bán kính đáy e rờ lớn không đổi. Nước được bơm liên tục vào bể với lưu lượng "
            "v không đổi. Yêu cầu của bài toán là tìm tốc độ nước dâng, tức là đạo hàm của "
            "chiều cao h theo thời gian."
        ),
        "scene_type": "cylinder_intro"
    },
    {
        "title": "LỜI GIẢI CHI TIẾT: BỂ HÌNH TRỤ ĐỨNG",
        "lines": [
            r"Gọi $h(t)$ là chiều cao mực nước tại thời điểm $t$.",
            r"Thể tích nước trong bể: $V(t) = \text{Diện tích đáy} \times \text{Chiều cao}$",
            r"$\implies V(t) = \pi R^2 \cdot h(t)$",
            r"Lấy đạo hàm hai vế theo thời gian $t$:",
            r"$\implies V'(t) = \pi R^2 \cdot h'(t)$",
            r"Vì lưu lượng bơm không đổi nên $V'(t) = v$.",
            r"$\implies v = \pi R^2 \cdot h'(t) \implies \boxed{h'(t) = \frac{v}{\pi R^2}}$",
            r"$\implies$ Tốc độ nước dâng trong bể hình trụ là một hằng số."
        ],
        "narration": (
            "Để giải bài toán này, ta gọi h là chiều cao mực nước tại thời điểm t. "
            "Thể tích khối nước hình trụ bằng diện tích đáy nhân với chiều cao, tức là "
            "V bằng Pi nhân e rờ bình phương nhân h. Lấy đạo hàm hai vế theo thời gian, "
            "ta có V phẩy bằng Pi nhân e rờ bình phương nhân h phẩy. Khối lượng nước bơm vào "
            "đều đặn nên V phẩy chính là lưu lượng v. Rút h phẩy ra, ta được kết quả cuối cùng: "
            "tốc độ nước dâng bằng v chia cho Pi e rờ bình phương. Đây là một hằng số."
        ),
        "scene_type": "cylinder_math"
    },
    {
        "title": "BÀI TOÁN 2: BỂ NƯỚC HÌNH NÓN (ĐỈNH HƯỚNG XUỐNG)",
        "lines": [
            r"Cho bể nước hình nón có bán kính đáy lớn $R$, chiều cao $H$.",
            r"Nước được bơm vào với lưu lượng $v$ không đổi.",
            r"Mực nước hiện tại là $h$. Tính tốc độ nước dâng $h'(t)$."
        ],
        "narration": (
            "Tiếp theo, chúng ta đến với một mô hình phức tạp hơn: Bể nước hình nón lộn ngược "
            "như phễu, có bán kính miệng là e rờ và chiều cao tổng là H. Nước vẫn được bơm vào "
            "với lưu lượng v. Tại thời điểm mực nước đạt độ cao h, tốc độ dâng của nước là bao nhiêu? "
            "Rõ ràng vì bình càng lên cao càng phình to, nước sẽ dâng chậm dần."
        ),
        "scene_type": "cone_intro"
    },
    {
        "title": "LỜI GIẢI CHI TIẾT: BỂ HÌNH NÓN",
        "lines": [
            r"Tại độ cao $h$, bán kính mặt nước là $r$. Theo định lý Thales:",
            r"$\displaystyle \frac{r}{R} = \frac{h}{H} \implies r = \frac{R}{H} h$",
            r"Thể tích nước: $\displaystyle V = \frac{1}{3} \pi r^2 h = \frac{1}{3} \pi \left(\frac{R}{H} h\right)^2 h = \frac{\pi R^2}{3 H^2} h^3$",
            r"Đạo hàm hai vế theo $t$:",
            r"$\displaystyle V'(t) = \frac{\pi R^2}{3 H^2} \cdot 3 h^2 \cdot h'(t) = \frac{\pi R^2}{H^2} h^2 \cdot h'(t)$",
            r"$\displaystyle \implies v = \frac{\pi R^2}{H^2} h^2 \cdot h'(t) \implies \boxed{h'(t) = \frac{v H^2}{\pi R^2 h^2}}$"
        ],
        "narration": (
            "Gọi r nhỏ là bán kính mặt nước. Áp dụng định lý Ta-lét, tỉ số r trên e rờ bằng h trên H. "
            "Rút r ra ta được r bằng e rờ nhân h chia H. Thể tích khối nón nước bằng một phần ba Pi "
            "nhân r bình nhân h. Thay r vào và thu gọn, ta có V bằng Pi e rờ bình chia cho ba H bình, "
            "tất cả nhân với h mũ ba. Đạo hàm hai vế, h mũ ba đạo hàm thành ba h bình nhân h phẩy. "
            "Triệt tiêu số ba, ta được phương trình liên hệ. Từ đó dễ dàng tìm được tốc độ nước dâng "
            "h phẩy tỉ lệ nghịch với bình phương chiều cao h."
        ),
        "scene_type": "cone_math"
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

class WaterTanks3D(ThreeDScene):
    def construct(self):
        # Thiết lập ánh sáng và môi trường 3D
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        
        for idx, slide in enumerate(SLIDES):
            audio_path = str(HERE / "audio_cache" / f"voice_{idx}.wav")
            dur = slide["duration"]
            
            # --- TẠO GIAO DIỆN 2D (Cố định trên màn hình) ---
            title = Text(slide["title"], font="Arial", font_size=32, color=YELLOW, weight="BOLD")
            title.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
            self.add_fixed_in_frame_mobjects(title)
            
            lines_group = VGroup()
            for line in slide["lines"]:
                if "boxed" in line:
                    mob = MathTex(line, font_size=38, color=GREEN, tex_template=TMPL)
                else:
                    mob = MathTex(line, font_size=32, color=WHITE, tex_template=TMPL)
                lines_group.add(mob)
            
            lines_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            # Nếu có hình 3D (intro), đặt text sang trái, hình 3D bên phải.
            if "intro" in slide["scene_type"]:
                lines_group.to_edge(LEFT, buff=0.4).shift(DOWN * 0.5)
            else:
                lines_group.to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
                
            self.add_fixed_in_frame_mobjects(lines_group)
            
            # --- ĐỒ HỌA 3D BÊN DƯỚI ---
            scene_3d = VGroup()
            water = None
            tank = None
            if slide["scene_type"] == "cylinder_intro":
                tank = Cylinder(radius=1.5, height=4, direction=Z_AXIS, color=WHITE, fill_opacity=0.1, stroke_width=2)
                tank.shift(RIGHT * 3 + DOWN * 1)
                water = Cylinder(radius=1.48, height=0.1, direction=Z_AXIS, color=BLUE, fill_opacity=0.7)
                water.move_to(tank.get_bottom() + UP*0.05)
                scene_3d.add(tank, water)
                
            elif slide["scene_type"] == "cone_intro":
                tank = Cone(base_radius=2, height=4, direction=-Z_AXIS, color=WHITE, fill_opacity=0.1)
                tank.shift(RIGHT * 3 + UP * 1) # Đỉnh nón quay xuống
                # Nước trong nón
                water = Cone(base_radius=0.1, height=0.2, direction=-Z_AXIS, color=BLUE, fill_opacity=0.8)
                water.move_to(tank.get_bottom() + UP*0.1)
                scene_3d.add(tank, water)
            
            if scene_3d:
                self.play(FadeIn(title), FadeIn(tank), run_time=1)
            else:
                self.play(FadeIn(title), run_time=1)
                
            self.add_sound(audio_path)
            
            # Tính thời gian hiện text
            reveal_time = dur * 0.8
            time_per_line = reveal_time / len(lines_group)
            
            for i, mob in enumerate(lines_group):
                anim_group = [FadeIn(mob, shift=UP*0.2)]
                
                # Nếu có nước, cho nước dâng dần theo từng line
                if water is not None:
                    if slide["scene_type"] == "cylinder_intro":
                        new_h = 4 * ((i+1)/len(lines_group))
                        if new_h < 0.1: new_h = 0.1
                        new_water = Cylinder(radius=1.48, height=new_h, direction=Z_AXIS, color=BLUE, fill_opacity=0.7)
                        new_water.move_to(tank.get_bottom() + UP*(new_h/2))
                        anim_group.append(Transform(water, new_water))
                    elif slide["scene_type"] == "cone_intro":
                        ratio = ((i+1)/len(lines_group))
                        new_h = 4 * ratio
                        if new_h < 0.2: new_h = 0.2
                        new_r = 2 * ratio
                        if new_r < 0.1: new_r = 0.1
                        new_water = Cone(base_radius=new_r, height=new_h, direction=-Z_AXIS, color=BLUE, fill_opacity=0.8)
                        new_water.move_to(tank.get_bottom() + UP*(new_h/2))
                        anim_group.append(Transform(water, new_water))
                        
                self.play(*anim_group, run_time=1.5)
                self.wait(time_per_line - 1.5 if time_per_line > 1.5 else 0)
                
            # Đợi cho hết audio
            self.wait(dur * 0.2)
            
            # Xóa để sang slide kế tiếp
            self.play(FadeOut(title), FadeOut(lines_group), FadeOut(scene_3d), run_time=1)

"""

SCRIPT.write_text(SOURCE, encoding="utf-8")

print("BƯỚC 3: Render video Manim 3D...")
MEDIA_DIR = ROOT / "media"
run_log([sys.executable, "-m", "manim", "-qm", "--fps", str(FPS), "--media_dir", str(MEDIA_DIR), "-o", "TocDoNuocDang_3D", str(SCRIPT), "WaterTanks3D"])

candidates = list(MEDIA_DIR.rglob("TocDoNuocDang_3D.mp4"))
if not candidates: raise RuntimeError("Lỗi render Manim.")
print(f"Xong! Video lưu tại: {candidates[0]}")

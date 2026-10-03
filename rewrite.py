import re

with open("duong_tiem_can_toan_12.py", "r", encoding="utf-8") as f:
    text = f.read()

# Extract SLIDES
slides_match = re.search(r'(SLIDES\s*=\s*\[.*?\])\n\n# ===', text, re.DOTALL)
if not slides_match:
    print("Cannot find SLIDES!")
    exit(1)
slides = slides_match.group(1)

out = open("duong_tiem_can_toan_12.py", "w", encoding="utf-8")

part1 = """# ======================================================================
# GOOGLE COLAB — DÁN TOÀN BỘ VÀO MỘT Ô RỒI CHẠY (1-CELL PIPELINE)
# 20 BÀI HỌC & BÀI TẬP: ĐƯỜNG TIỆM CẬN CỦA ĐỒ THỊ HÀM SỐ (TOÁN 12)
# Giọng Nam tiếng Việt · Footer: Thầy Nguyễn Văn Sang
# 100% CÔNG THỨC TOÁN, SỐ LIỆU, BIẾN SỐ CHUẨN MÃ LATEX (MathTex)
# ======================================================================

import os, sys, json, math, time, asyncio, hashlib, subprocess, textwrap, shutil
from pathlib import Path
import numpy as np

# ======================== 1. CẤU HÌNH BẮT BUỘC ========================
TEN_THAY    = "Thầy Nguyễn Văn Sang"
GIONG_DOC   = "vi-VN-NamMinhNeural"
TOC_DO_DOC  = "-5%"

RESOLUTION  = "1280,720"
FPS         = 24

if Path("/content").exists():
    ROOT = Path("/content/duong_tiem_can_toan_12")
else:
    ROOT = (
        (Path(__file__).resolve().parent / "duong_tiem_can_toan_12_out")
        if "__file__" in globals()
        else (Path.cwd() / "duong_tiem_can_toan_12_out")
    )

ROOT.mkdir(parents=True, exist_ok=True)
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TIMING_FILE = ROOT / "timing.json"
SCRIPT = ROOT / "duong_tiem_can_scene.py"

os.environ["DEBIAN_FRONTEND"]               = "noninteractive"
os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"

def run_log(command, logfile=None):
    if logfile:
        logfile = Path(logfile)
        with logfile.open("w", encoding="utf-8") as f:
            res = subprocess.run([str(x) for x in command], stdout=f, stderr=subprocess.STDOUT, text=True)
        if res.returncode != 0:
            print(logfile.read_text(encoding="utf-8", errors="replace")[-10000:])
            raise RuntimeError(f"Lệnh thất bại: {' '.join(str(c) for c in command)}")
    else:
        subprocess.run([str(x) for x in command], check=True)

def probe_duration(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path)
        ],
        capture_output=True,
        text=True,
        check=True
    )
    val = float(result.stdout.strip())
    if not math.isfinite(val) or val <= 0:
        raise RuntimeError(f"Tệp âm thanh không hợp lệ: {path}")
    return val

# ======================== 2. CÀI ĐẶT MÔI TRƯỜNG =======================
print("BƯỚC 1/4: Kiểm tra và cài đặt môi trường (Manim, LaTeX, Font tiếng Việt, TTS)...")

marker = ROOT / "env_ok_v6.txt"
if Path("/content").exists() and not marker.exists():
    print("  -> Đang cài đặt gói hệ thống và thư viện LaTeX...")
    run_log(["apt-get", "update", "-qq"], ROOT / "apt_update.log")
    run_log([
        "apt-get", "install", "-y", "-qq",
        "ffmpeg", "pkg-config", "libcairo2-dev", "libpango1.0-dev",
        "fonts-dejavu-core", "fonts-noto-core",
        "texlive", "texlive-latex-extra", "texlive-fonts-extra",
        "texlive-latex-recommended", "texlive-science", "tipa", "dvisvgm"
    ], ROOT / "apt_install.log")
    
    print("  -> Đang cài đặt Manim và Edge-TTS...")
    run_log([
        sys.executable, "-m", "pip", "install", "-q",
        "manim==0.19.0", "edge-tts>=7.0.0,<8", "nest_asyncio", "ipywidgets"
    ], ROOT / "pip_install.log")
    marker.write_text("OK", encoding="utf-8")
    print("  -> Cài đặt hoàn tất thành công.")
else:
    print("  -> Môi trường đã sẵn sàng.")

# ======================== DỮ LIỆU BÀI HỌC ========================
"""

out.write(part1)
out.write(slides)

part2 = """

# ======================== 3. TỔNG HỢP ÂM THANH =======================
print("\\nBƯỚC 2/4: Tổng hợp giọng đọc NamMinhNeural và đo đạc thời lượng...")

try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

import edge_tts

async def make_mp3(text, destination):
    comm = edge_tts.Communicate(text=text, voice=GIONG_DOC, rate=TOC_DO_DOC)
    await comm.save(str(destination))

lengths = []
for index, slide in enumerate(SLIDES):
    text = slide["narration"]
    key = hashlib.md5((GIONG_DOC + TOC_DO_DOC + text).encode("utf-8")).hexdigest()
    mp3 = AUDIO_DIR / f"{key}.mp3"
    wav = AUDIO_DIR / f"voice_{index:02d}.wav"

    if not wav.exists():
        if not mp3.exists() or mp3.stat().st_size < 1024:
            for attempt in range(3):
                try:
                    try:
                        asyncio.run(make_mp3(text, mp3))
                    except RuntimeError:
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(make_mp3(text, mp3))
                    if mp3.exists() and mp3.stat().st_size >= 1024:
                        break
                except Exception as e:
                    print(f"  [TTS] Thử lại lần {attempt+1} cho trang {index+1}: {e}")
                    time.sleep(1.5)
        subprocess.run([
            "ffmpeg", "-y", "-v", "error",
            "-i", str(mp3),
            "-ar", "44100", "-ac", "2",
            str(wav)
        ], check=True)

    dur = probe_duration(wav)
    lengths.append(dur)
    if (index + 1) % 5 == 0 or (index + 1) == len(SLIDES):
        print(f"  -> Đã tạo giọng đọc: {index + 1}/{len(SLIDES)} trang.")

TIMING_FILE.write_text(json.dumps({
    "durations": lengths,
    "slides": SLIDES,
    "voice": GIONG_DOC,
    "rate": TOC_DO_DOC,
    "ten_thay": TEN_THAY
}, ensure_ascii=False, indent=2), encoding="utf-8")
print("Hoàn tất chuẩn bị âm thanh.")

# ======================== 4. MÃ NGUỒN CẢNH MANIM =====================

"""

out.write(part2)

out.write("SOURCE = r'''\n")
out.write("from manim import *\n")
out.write("import json\n")
out.write("import math\n")
out.write("import numpy as np\n")
out.write("from pathlib import Path\n")
out.write("\n")
out.write("HERE = Path(__file__).resolve().parent\n")
out.write("AUDIO_DIR = HERE / \"audio_cache\"\n")
out.write("TIMING_FILE = HERE / \"timing.json\"\n")
out.write("\n")
out.write("timing = json.loads(TIMING_FILE.read_text(encoding=\"utf-8\"))\n")
out.write("SLIDES = timing[\"slides\"]\n")
out.write("DURATIONS = timing[\"durations\"]\n")
out.write("TEN_THAY = timing[\"ten_thay\"]\n")
out.write("\n")
out.write("ENTER_TIME       = 0.55\n")
out.write("AFTER_AUDIO_TIME = 0.30\n")
out.write("EXIT_TIME        = 0.30\n")
out.write("\n")
out.write("FONT   = \"DejaVu Sans\"\n")
out.write("BG     = \"#0b1120\"\n")
out.write("PANEL  = \"#0e1d34\"\n")
out.write("FG     = \"#EDF4FF\"\n")
out.write("INK    = \"#EDF4FF\"\n")
out.write("MUTED  = \"#7A9ABF\"\n")
out.write("ACCENT = \"#38BDF8\"\n")
out.write("CYAN   = \"#3ADEC8\"\n")
out.write("GREEN  = \"#4ADE80\"\n")
out.write("YELLOW = \"#FBBF24\"\n")
out.write("GOLD   = \"#FFD700\"\n")
out.write("RED    = \"#FF6B6B\"\n")
out.write("PINK   = \"#F472B6\"\n")
out.write("\n")
out.write("config.background_color = BG\n")
out.write("\n")
out.write("TMPL = TexTemplate()\n")
out.write("TMPL.add_to_preamble(r\"\"\"\n")
out.write("\\usepackage{amsmath}\n")
out.write("\\usepackage{amssymb}\n")
out.write("\\usepackage{xcolor}\n")
out.write("\\usepackage{bm}\n")
out.write("\"\"\")\n")

# Now we append the rest of the file which is identical
part3 = """
def make_line_element(content, size=24, color=FG, max_width=None):
    if "$" not in content:
        mob = Text(content, font=FONT, font_size=size, color=color, line_spacing=0.85)
        if max_width and mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob

    parts = content.split("$")
    items = []
    for idx, part in enumerate(parts):
        if not part:
            continue
        if idx % 2 == 0:
            txt_mob = Text(part, font=FONT, font_size=size, color=color)
            items.append(txt_mob)
        else:
            is_boxed = r"\\boxed" in part
            math_color = GOLD if is_boxed else (ACCENT if any(k in part for k in ["=", r"\\lim", r"\\to", r"\\implies"]) else INK)
            math_mob = MathTex(part, font_size=size + 3, color=math_color, tex_template=TMPL)
            items.append(math_mob)

    if not items:
        return VMobject()

    group = VGroup()
    for i, it in enumerate(items):
        if i == 0:
            group.add(it)
        else:
            prev = items[i - 1]
            buff = 0.05 if (isinstance(it, Text) and it.text and it.text[0] in ".,;:)") else 0.11
            it.next_to(prev, RIGHT, buff=buff)
            it.shift(DOWN * (it.get_bottom()[1] - prev.get_bottom()[1]))
            group.add(it)

    if max_width and group.width > max_width:
        group.scale_to_fit_width(max_width)
    return group

def make_body(lines, has_graph):
    font_size = 23 if has_graph else 26
    max_width = 6.25 if has_graph else 12.8
    items = []
    for idx, line in enumerate(lines):
        line_color = FG
        if idx == 0:
            line_color = ACCENT
        elif idx == len(lines) - 1:
            line_color = GREEN
        items.append(make_line_element(line, size=font_size, color=line_color, max_width=max_width))

    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.20 if has_graph else 0.24)
    if body.height > 5.50:
        body.scale_to_fit_height(5.50)
    body.to_edge(LEFT, buff=0.45)
    body.shift(UP * (2.55 - body.get_top()[1]))
    return body

def evaluate_function(name, x):
    if name == "inverse": return 1.0 / x
    if name == "rational_21": return (2.0 * x + 1.0) / (x - 1.0)
    if name == "inverse_sqrt": return 1.0 / np.sqrt(x)
    if name == "two_horizontal": return x / np.sqrt(x * x + 1.0)
    if name == "slant_simple": return x + 1.0 / x
    if name == "slant_shift": return x + 1.0 + 1.0 / (x + 1.0)
    if name == "cross_horizontal": return x / (x * x + 1.0)
    raise ValueError(f"Chưa khai báo hàm: {name}")

def line_rectangle_intersections(a, b, c, bounds):
    xmin, xmax, ymin, ymax = bounds
    eps = 1e-8
    candidates = []
    if abs(b) > eps:
        for x in (xmin, xmax):
            y = (c - a * x) / b
            if ymin - eps <= y <= ymax + eps:
                candidates.append((float(x), float(y)))
    if abs(a) > eps:
        for y in (ymin, ymax):
            x = (c - b * y) / a
            if xmin - eps <= x <= xmax + eps:
                candidates.append((float(x), float(y)))

    unique = []
    for pt in candidates:
        if not any(math.hypot(pt[0] - o[0], pt[1] - o[1]) < eps for o in unique):
            unique.append(pt)
    if len(unique) < 2: return None
    pairs = [(p, q) for i, p in enumerate(unique) for q in unique[i + 1:]]
    return max(pairs, key=lambda pr: (pr[0][0] - pr[1][0])**2 + (pr[0][1] - pr[1][1])**2)

def build_graph(spec):
    xmin, xmax, ymin, ymax = spec["range"]
    x_step = 2 if xmax - xmin > 10 else 1
    y_step = 2 if ymax - ymin > 10 else 1

    axes = Axes(
        x_range=[xmin, xmax, x_step],
        y_range=[ymin, ymax, y_step],
        x_length=5.3,
        y_length=4.6,
        axis_config={
            "color": "#94A3B8",
            "stroke_width": 1.6,
            "include_ticks": True,
            "include_numbers": False,
            "tip_width": 0.12,
            "tip_height": 0.12
        }
    ).move_to([3.75, -0.05, 0])

    graph = VGroup()
    grid = VGroup()
    first_x = math.ceil(xmin / x_step) * x_step
    first_y = math.ceil(ymin / y_step) * y_step

    for x in np.arange(first_x, xmax + 0.001, x_step):
        grid.add(Line(axes.c2p(x, ymin), axes.c2p(x, ymax), color="#1E293B", stroke_width=0.7))
    for y in np.arange(first_y, ymax + 0.001, y_step):
        grid.add(Line(axes.c2p(xmin, y), axes.c2p(xmax, y), color="#1E293B", stroke_width=0.7))
    graph.add(grid, axes)

    tick_labels = VGroup()
    for x in np.arange(first_x, xmax + 0.001, x_step):
        if abs(x) > 1e-8 and xmin < x < xmax:
            lbl = MathTex(f"{x:g}", font_size=16, color=MUTED, tex_template=TMPL).next_to(axes.c2p(x, 0), DOWN, buff=0.08)
            tick_labels.add(lbl)
    for y in np.arange(first_y, ymax + 0.001, y_step):
        if abs(y) > 1e-8 and ymin < y < ymax:
            lbl = MathTex(f"{y:g}", font_size=16, color=MUTED, tex_template=TMPL).next_to(axes.c2p(0, y), LEFT, buff=0.08)
            tick_labels.add(lbl)
    graph.add(tick_labels)

    x_lbl = MathTex("x", font_size=20, color=MUTED, tex_template=TMPL).next_to(axes.c2p(xmax, 0), RIGHT, buff=0.06)
    y_lbl = MathTex("y", font_size=20, color=MUTED, tex_template=TMPL).next_to(axes.c2p(0, ymax), UP, buff=0.06)
    o_lbl = MathTex("O", font_size=18, color=MUTED, tex_template=TMPL).next_to(axes.c2p(0, 0), DL, buff=0.06)
    graph.add(x_lbl, y_lbl, o_lbl)

    legend_items = []
    for index, asymp in enumerate(spec.get("asymptotes", [])):
        kind = asymp[0]
        color = GOLD if index % 2 == 0 else PINK
        if kind == "v":
            val, label_str = asymp[1:]
            ends = line_rectangle_intersections(1, 0, val, spec["range"])
        elif kind == "h":
            val, label_str = asymp[1:]
            ends = line_rectangle_intersections(0, 1, val, spec["range"])
        else:
            a, b, label_str = asymp[1:]
            ends = line_rectangle_intersections(-a, 1, b, spec["range"])

        if ends is not None:
            p, q = ends
            graph.add(DashedLine(
                axes.c2p(*p), axes.c2p(*q),
                dash_length=0.12, dashed_ratio=0.55,
                stroke_width=2.8, color=color
            ))

        clean_tex = label_str.strip("$")
        legend_items.append(MathTex(clean_tex, font_size=22, color=color, tex_template=TMPL))

    for left, right in spec["intervals"]:
        left = max(left, xmin)
        right = min(right, xmax)
        if left >= right: continue
        xs = np.linspace(left, right, 1800)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            ys = evaluate_function(spec["func"], xs)
        valid = np.isfinite(ys) & (ys >= ymin) & (ys <= ymax)
        indices = np.flatnonzero(valid)
        if len(indices) < 2: continue
        breaks = np.where(np.diff(indices) > 1)[0] + 1
        for run in np.split(indices, breaks):
            if len(run) < 2: continue
            pts = [axes.c2p(float(xs[i]), float(ys[i])) for i in run]
            curve = VMobject().set_points_as_corners(pts)
            curve.set_stroke(color=CYAN, width=3.2)
            graph.add(curve)

    for x, y, label_content in spec.get("points", []):
        pt = Dot(axes.c2p(x, y), radius=0.065, color=GOLD)
        clean_lbl = label_content.strip("$")
        lbl = MathTex(clean_lbl, font_size=20, color=GOLD, tex_template=TMPL).next_to(pt, UR, buff=0.08)
        lbl.add_background_rectangle(color=BG, opacity=0.85, buff=0.04)
        graph.add(pt, lbl)

    if legend_items:
        legend = VGroup(*legend_items).arrange(RIGHT, buff=0.35)
        if legend.width > 5.4: legend.scale_to_fit_width(5.4)
        legend.move_to([3.75, 2.70, 0])
        graph.add(legend)

    if spec.get("caption"):
        cap = make_line_element(spec["caption"], size=20, color=GREEN, max_width=5.6).move_to([3.75, -2.95, 0])
        graph.add(cap)

    return graph


class DuongTiemCanToan12(Scene):
    def construct(self):
        footer_bg = Rectangle(
            width=config.frame_width, height=0.55,
            stroke_width=0, fill_color="#070c18", fill_opacity=1
        ).to_edge(DOWN, buff=0).set_z_index(100)

        footer_rule = Line(
            [-config.frame_width / 2, -3.45, 0],
            [config.frame_width / 2, -3.45, 0],
            stroke_width=1.5, color=ACCENT
        ).set_z_index(101)

        footer_name = Text(TEN_THAY, font=FONT, font_size=20, color=FG, weight="BOLD"
                           ).move_to([0, -3.72, 0]).set_z_index(102)

        footer_subj = Text("TOÁN 12 • ĐƯỜNG TIỆM CẬN", font=FONT, font_size=15, color=MUTED
                           ).to_edge(LEFT, buff=0.35)
        footer_subj.set_y(-3.72).set_z_index(102)

        self.add(footer_bg, footer_rule, footer_name, footer_subj)

        for index, slide in enumerate(SLIDES):
            title = make_line_element(slide["title"], size=30, color=ACCENT, max_width=12.6).move_to([0, 3.32, 0])
            header_rule = Line([-6.65, 2.92, 0], [6.65, 2.92, 0], stroke_width=1.2, color="#2A3D5C")

            counter = Text(f"{index + 1:02d} / {len(SLIDES):02d}", font=FONT, font_size=16, color=MUTED
                           ).to_edge(RIGHT, buff=0.35)
            counter.set_y(-3.72).set_z_index(103)

            has_graph = "graph" in slide
            body = make_body(slide["lines"], has_graph)
            content = VGroup(title, header_rule, body)

            if has_graph:
                divider = Line([0.15, -2.75, 0], [0.15, 2.65, 0], stroke_width=1, color="#23354E")
                content.add(divider, build_graph(slide["graph"]))

            self.add(counter)
            self.play(FadeIn(content, shift=UP * 0.08), run_time=ENTER_TIME)

            audio_path = AUDIO_DIR / f"voice_{index:02d}.wav"
            if audio_path.exists():
                self.add_sound(str(audio_path))

            track = Line(LEFT * 6.60 + DOWN * 3.25, RIGHT * 6.60 + DOWN * 3.25, color="#1B283A", stroke_width=3)
            progress = Line(LEFT * 6.60 + DOWN * 3.25, RIGHT * 6.60 + DOWN * 3.25, color=ACCENT, stroke_width=3)

            self.add(track)
            self.play(Create(progress), run_time=DURATIONS[index], rate_func=linear)
            self.wait(AFTER_AUDIO_TIME)

            self.play(
                FadeOut(content, shift=UP * 0.05),
                FadeOut(track), FadeOut(progress), FadeOut(counter),
                run_time=EXIT_TIME
            )
'''
"""

out.write(part3)

part4 = """
SCRIPT.write_text(SOURCE, encoding="utf-8")

# ======================== 5. RENDER VIDEO MANIM =====================

print(f"\\nBƯỚC 3/4: Render video Manim ({RESOLUTION} @ {FPS}fps)...")
MEDIA_DIR = ROOT / "media"

run_log([
    sys.executable, "-m", "manim",
    "-qm" if RESOLUTION == "1280,720" else "-qh",
    "--fps", str(FPS),
    "--disable_caching",
    "--media_dir", str(MEDIA_DIR),
    "-o", "Duong_Tiem_Can_Thay_Nguyen_Van_Sang",
    str(SCRIPT),
    "DuongTiemCanToan12"
])

candidates = [
    p for p in MEDIA_DIR.rglob("Duong_Tiem_Can_Thay_Nguyen_Van_Sang.mp4")
    if "partial_movie_files" not in str(p)
]

if not candidates:
    raise FileNotFoundError("Chưa tìm thấy video thành phẩm. Vui lòng kiểm tra log lỗi Manim.")

VIDEO_PATH = max(candidates, key=lambda p: p.stat().st_mtime)
dur_sec = probe_duration(VIDEO_PATH)
mins = int(dur_sec // 60)
secs = dur_sec - mins * 60

print(f"\\nBƯỚC 4/4: HOÀN TẤT BÀI GIẢNG!")
print(f"• Đường dẫn video: {VIDEO_PATH}")
print(f"• Thời lượng: {mins:02d}:{secs:05.2f}")
print(f"• Dung lượng: {VIDEO_PATH.stat().st_size / 1024**2:.1f} MB")
print(f"• Bản quyền: {TEN_THAY}")

# ======================== 6. NÚT TẢI XUỐNG COLAB =====================

try:
    from IPython.display import display
    import ipywidgets as widgets
    from google.colab import files

    btn_video = widgets.Button(
        description="Tải video MP4",
        button_style="success",
        layout=widgets.Layout(width="200px")
    )
    btn_source = widgets.Button(
        description="Tải mã nguồn .py",
        button_style="info",
        layout=widgets.Layout(width="200px")
    )

    btn_video.on_click(lambda _: files.download(str(VIDEO_PATH)))
    btn_source.on_click(lambda _: files.download(str(SCRIPT)))

    display(widgets.HBox([btn_video, btn_source]))
    print("Bắt đầu tải video về máy...")
    files.download(str(VIDEO_PATH))
except Exception:
    pass
"""

out.write(part4)
out.close()

print("Rewrite successful")


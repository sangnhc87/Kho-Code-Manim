from manim import *
from pathlib import Path
import asyncio, hashlib, json, math, os, subprocess, sys, textwrap, time

# ==========================================================
# SYSTEM CONFIG
# ==========================================================
TEN_THAY = "Thầy Nguyễn Văn Sang"
GIONG_DOC = "vi-VN-NamMinhNeural"
TOC_DO_DOC = "-5%"
PITCH = "+0Hz"

FINAL_WIDTH = 1920
FINAL_HEIGHT = 1080
FINAL_FPS = 30

config.pixel_width = FINAL_WIDTH
config.pixel_height = FINAL_HEIGHT
config.frame_rate = FINAL_FPS
config.background_color = "#0B1120"

ROOT = Path.cwd()
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR = ROOT / "media"

# ==========================================================
# COLORS
# ==========================================================
BG = "#0B1120"
PANEL = "#0E1D34"
INK = "#EDF4FF"
MUTED = "#7A9ABF"
BLUE = "#38BDF8"
CYAN = "#3ADEC8"
GOLD = "#FFD700"
GREEN = "#4ADE80"
RED = "#FF6B6B"
ORANGE = "#FB923C"

# ==========================================================
# TEX
# ==========================================================
TMPL = TexTemplate()
TMPL.add_to_preamble(r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{xcolor}
""")


def mtx(s, size=38, color=INK):
    return MathTex(s, font_size=size, color=color, tex_template=TMPL)


def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


def fit_width(mob, width=12.4):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def make_panel(width=12.2, height=5.4):
    return RoundedRectangle(
        width=width, height=height, corner_radius=0.18,
        fill_color=PANEL, fill_opacity=0.90,
        stroke_color=MUTED, stroke_opacity=0.22, stroke_width=1.5,
    )


def title_block(title, subtitle=None):
    t = fit_width(txt(title, 38, INK, BOLD), 12.0).to_edge(UP, buff=0.25)
    if subtitle:
        s = fit_width(txt(subtitle, 23, MUTED), 11.5).next_to(t, DOWN, buff=0.10)
        return VGroup(t, s)
    return VGroup(t)


def footer(page_text=""):
    left = txt(TEN_THAY, 19, MUTED)
    right = txt(page_text, 19, MUTED)
    left.to_edge(DOWN, buff=0.18).to_edge(LEFT, buff=0.38)
    right.to_edge(DOWN, buff=0.18).to_edge(RIGHT, buff=0.38)
    return VGroup(left, right)


def bullet(text, color=INK, size=28, dot_color=BLUE):
    d = Dot(radius=0.055, color=dot_color)
    t = txt(text, size, color)
    return VGroup(d, t).arrange(RIGHT, buff=0.18, aligned_edge=UP)


def label_point(axes, x, y, name, color=CYAN, direction=UR):
    d = Dot(axes.c2p(x, y), radius=0.055, color=color)
    lab = mtx(name, 28, color).next_to(d, direction, buff=0.08)
    return VGroup(d, lab)

# ==========================================================
# TTS + MASTER AUDIO
# ==========================================================
def _audio_key(text):
    payload = json.dumps({
        "text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC,
        "pitch": PITCH, "engine": "edge-tts"
    }, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)


def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError(f"Audio không hợp lệ: {path}")
    subprocess.run([
        "ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"
    ], check=True)


async def _edge_save(text: str, out_path: str):
    import edge_tts
    communicate = edge_tts.Communicate(
        text=text, voice=GIONG_DOC, rate=TOC_DO_DOC, pitch=PITCH
    )
    await communicate.save(out_path)


def create_audio(text: str) -> Path:
    out = AUDIO_DIR / f"{_audio_key(text)}.mp3"
    if out.exists():
        try:
            validate_audio(out)
            return out
        except Exception:
            out.unlink(missing_ok=True)

    last_err = None
    for attempt in range(1, 4):
        try:
            code = (
                "import asyncio\n"
                "from pathlib import Path\n"
                "import edge_tts\n"
                f"text={text!r}\n"
                f"out={str(out)!r}\n"
                f"voice={GIONG_DOC!r}\n"
                f"rate={TOC_DO_DOC!r}\n"
                f"pitch={PITCH!r}\n"
                "async def main():\n"
                "    c=edge_tts.Communicate(text=text,voice=voice,rate=rate,pitch=pitch)\n"
                "    await c.save(out)\n"
                "asyncio.run(main())\n"
            )
            subprocess.run([sys.executable, "-c", code], check=True)
            validate_audio(out)
            return out
        except Exception as e:
            last_err = e
            out.unlink(missing_ok=True)
            time.sleep(1.5 * attempt)
    raise RuntimeError(f"Edge TTS thất bại sau 3 lần: {last_err}")


def build_master_audio(events, video_duration, out_wav: Path):
    # events: list[(start_time, audio_path)]
    if not events:
        raise RuntimeError("Không có narration nào để ghép.")

    inputs = []
    filters = []
    mix_labels = []
    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]adelay={ms}|{ms},aresample=48000[a{i}]")
        mix_labels.append(f"[a{i}]")

    filter_complex = ";".join(filters) + ";" + "".join(mix_labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    cmd = ["ffmpeg", "-y", "-v", "error", *inputs,
           "-filter_complex", filter_complex, "-map", "[m]",
           "-ar", "48000", "-ac", "2", "-t", f"{video_duration:.3f}", str(out_wav)]
    subprocess.run(cmd, check=True)


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)
    ], check=True)

# ==========================================================
# SCENE
# ==========================================================
class SangLesson(Scene):
    def setup(self):
        self.audio_events = []
        self.page = 1

    # ---------- narration ----------
    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def narrate_while(self, text, animation, min_hold=0.2):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        rt = min(max(0.8, dur * 0.62), 4.0)
        self.play(animation, run_time=rt)
        if dur > rt:
            self.wait(dur - rt + min_hold)
        else:
            self.wait(min_hold)
        return dur

    # ---------- common ----------
    def clear_stage(self, keep_footer=False):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.45)

    def add_header_footer(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, lines, voice, progress):
        self.clear_stage()
        self.add_header_footer(title, "ĐỀ BÀI", progress)
        p = make_panel(12.3, 5.25).shift(DOWN*0.12)
        self.play(FadeIn(p), run_time=0.5)
        line_mobs = VGroup()
        for i, line in enumerate(lines):
            t = fit_width(txt(line, 28 if i == 0 else 26, INK if i == 0 else "#D8E7FF", BOLD if i == 0 else NORMAL), 11.2)
            line_mobs.add(t)
        line_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        line_mobs.move_to(p.get_center()).shift(UP*0.08)
        for mob in line_mobs:
            self.play(FadeIn(mob, shift=UP*0.08), run_time=0.35)
        self.narrate(voice, 2.0)
        self.wait(0.3)
        return VGroup(p, line_mobs)

    # ---------- intro ----------
    def intro(self):
        self.clear_stage()
        main = fit_width(txt("HỆ BẤT PHƯƠNG TRÌNH BẬC NHẤT HAI ẨN", 48, INK, BOLD), 12.2)
        sub = txt("Từ một bất phương trình đến miền nghiệm của cả hệ", 29, CYAN)
        brand = txt(TEN_THAY, 24, MUTED)
        g = VGroup(main, sub, brand).arrange(DOWN, buff=0.28).move_to(ORIGIN)
        self.play(FadeIn(main, shift=UP*0.2), run_time=0.9)
        self.play(Write(sub), run_time=0.9)
        self.play(FadeIn(brand), run_time=0.5)
        self.narrate(
            "Chào các em! Hôm nay, chúng ta bắt đầu bài học về hệ bất phương trình bậc nhất hai ẩn. "
            "Mục tiêu quan trọng nhất không phải là ghi nhớ máy móc cách tô miền, mà là hiểu vì sao mỗi bất phương trình cho một nửa mặt phẳng, "
            "và vì sao miền nghiệm của cả hệ chính là phần giao của tất cả các miền đó.", 2.0)
        self.play(FadeOut(g), run_time=0.5)

        self.add_header_footer("Hôm nay chúng ta sẽ học gì?", "4 ý cốt lõi", "Phần mở đầu")
        items = VGroup(
            bullet("Hiểu miền nghiệm của một bất phương trình bậc nhất hai ẩn."),
            bullet("Biết chọn đúng nửa mặt phẳng bằng điểm thử."),
            bullet("Biết tìm giao các miền để giải một hệ bất phương trình."),
            bullet("Đọc được ý nghĩa hình học của miền nghiệm."),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).shift(DOWN*0.25)
        for b in items:
            self.play(FadeIn(b, shift=RIGHT*0.15), run_time=0.4)
        self.narrate(
            "Sau bài học, các em sẽ làm được bốn việc. Một là đọc được một bất phương trình dưới dạng nửa mặt phẳng. "
            "Hai là chọn đúng phía cần tô. Ba là tìm phần giao khi có nhiều bất phương trình. Và bốn là giải thích được vì sao một điểm thuộc hoặc không thuộc miền nghiệm.", 2.0)

    # ---------- foundation ----------
    def foundation(self):
        self.clear_stage()
        self.add_header_footer("Bản chất hình học", "Một bất phương trình → một nửa mặt phẳng", "Kiến thức nền")
        panel = make_panel(11.9, 4.9).shift(DOWN*0.15)
        general = mtx(r"ax+by\le c\qquad (a,b)\ne(0,0)", 42, GOLD)
        boundary = mtx(r"ax+by=c", 42, BLUE)
        desc1 = txt("Đường biên", 27, BLUE, BOLD)
        desc2 = txt("chia mặt phẳng thành hai nửa", 27, INK)
        row = VGroup(desc1, desc2).arrange(RIGHT, buff=0.18)
        group = VGroup(general, boundary, row).arrange(DOWN, buff=0.40).move_to(panel)
        self.play(FadeIn(panel), Write(general), run_time=0.9)
        self.narrate("Một bất phương trình bậc nhất hai ẩn có dạng a x cộng b y nhỏ hơn hoặc bằng c, với a và b không đồng thời bằng không.", 1.3)
        self.play(Write(boundary), FadeIn(row), run_time=0.8)
        self.narrate("Khi thay dấu bất phương trình bằng dấu bằng, ta được một đường thẳng. Đường thẳng này là đường biên và chia mặt phẳng thành hai nửa. Một nửa thỏa bất phương trình, nửa còn lại không thỏa.", 1.8)

        self.clear_stage()
        self.add_header_footer("Đường biên có được lấy không?", "Nhìn dấu là biết", "Kiến thức nền")
        solid = Line(LEFT*2.1, RIGHT*2.1, color=GREEN, stroke_width=5)
        dashed = DashedLine(LEFT*2.1, RIGHT*2.1, color=ORANGE, stroke_width=4, dash_length=0.15)
        s1 = VGroup(mtx(r"\le,\ \ge", 38, GREEN), txt("→ nét liền, lấy đường biên", 27, INK)).arrange(RIGHT,buff=0.35)
        s2 = VGroup(mtx(r"<,\ >", 38, ORANGE), txt("→ nét đứt, không lấy đường biên", 27, INK)).arrange(RIGHT,buff=0.35)
        g1 = VGroup(solid, s1).arrange(DOWN,buff=0.22)
        g2 = VGroup(dashed, s2).arrange(DOWN,buff=0.22)
        both = VGroup(g1,g2).arrange(DOWN,buff=0.65).shift(DOWN*0.1)
        self.play(Create(solid), FadeIn(s1), run_time=0.7)
        self.narrate("Nếu dấu có kèm dấu bằng, nghĩa là nhỏ hơn hoặc bằng hay lớn hơn hoặc bằng, các điểm trên đường biên cũng là nghiệm, nên ta vẽ nét liền.", 1.6)
        self.play(Create(dashed), FadeIn(s2), run_time=0.7)
        self.narrate("Nếu dấu là nhỏ hơn hoặc lớn hơn nghiêm ngặt, các điểm trên đường biên không phải nghiệm, nên ta biểu diễn đường biên bằng nét đứt.", 1.5)

        self.clear_stage()
        self.add_header_footer("Vì sao dùng điểm thử?", "Một điểm đại diện cho cả một phía", "Kiến thức nền")
        axes = Axes(x_range=[-3,5,1], y_range=[-3,5,1], x_length=6.5, y_length=5.2,
                    axis_config={"color":MUTED,"include_numbers":False})
        axes.shift(LEFT*2.2+DOWN*0.2)
        line = axes.plot(lambda x: 2-x, x_range=[-3,5], color=BLUE, stroke_width=4)
        o = Dot(axes.c2p(0,0),color=CYAN)
        ol = mtx(r"O(0,0)",28,CYAN).next_to(o,DR,buff=0.08)
        expl = VGroup(
            mtx(r"x+y\le2", 38, GOLD),
            mtx(r"0+0\le2", 34, GREEN),
            txt("Đúng → lấy phía chứa O", 26, GREEN, BOLD)
        ).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.45)
        self.play(Create(axes),Create(line),FadeIn(o),FadeIn(ol),run_time=0.9)
        self.play(FadeIn(expl),run_time=0.6)
        self.narrate("Để biết chọn phía nào, ta chỉ cần thử một điểm không nằm trên đường biên. Điểm O thường rất tiện. Nếu thay vào được mệnh đề đúng, ta lấy phía chứa O. Nếu sai, ta lấy phía còn lại.", 1.8)

    # ---------- concept 1 ----------
    def one_inequality(self):
        self.show_problem(
            "Ví dụ 1 – Một bất phương trình",
            [
                "Xét bất phương trình  x + 2y ≤ 6.",
                "a) Vẽ miền nghiệm trên mặt phẳng tọa độ.",
                "b) Kiểm tra các điểm O(0;0), A(2;1), B(4;2)."
            ],
            "Ví dụ đầu tiên rất cơ bản. Ta xét bất phương trình x cộng hai y nhỏ hơn hoặc bằng sáu. "
            "Nhiệm của nó không phải là một điểm, mà là cả một miền trên mặt phẳng. Ta sẽ tìm miền đó và kiểm tra ba điểm cụ thể.",
            "Ví dụ 1/3"
        )
        self.clear_stage()
        self.add_header_footer("Ví dụ 1 – Bước 1", "Vẽ đường biên", "Ví dụ 1/3")

        axes = Axes(x_range=[-1,7,1], y_range=[-1,5,1], x_length=7.2, y_length=5.0,
                    axis_config={"color":MUTED,"stroke_width":2,"include_numbers":True,"font_size":24})
        axes.shift(LEFT*2.4 + DOWN*0.25)
        eq = mtx(r"x+2y=6", 40, GOLD).to_edge(RIGHT, buff=0.6).shift(UP*1.6)
        pts = VGroup(mtx(r"(0,3)", 30, CYAN), mtx(r"(6,0)", 30, CYAN)).arrange(DOWN, buff=0.25)
        pts.next_to(eq, DOWN, buff=0.35)
        line = axes.plot(lambda x:(6-x)/2, x_range=[-1,7], color=BLUE, stroke_width=4)
        p1 = Dot(axes.c2p(0,3), color=CYAN); p2=Dot(axes.c2p(6,0), color=CYAN)
        self.play(Create(axes), run_time=1.0)
        self.narrate_while("Trước hết, thay dấu nhỏ hơn hoặc bằng bằng dấu bằng. Ta được đường biên x cộng hai y bằng sáu.", Write(eq))
        self.play(Create(line), FadeIn(p1), FadeIn(p2), FadeIn(pts), run_time=1.2)
        self.narrate("Để vẽ đường thẳng này, ta có thể lấy hai giao điểm với hai trục: không phẩy ba và sáu phẩy không.", 1.5)

        test_box = make_panel(4.4,2.1).to_edge(RIGHT,buff=0.35).shift(DOWN*1.1)
        test_title = txt("Chọn điểm thử O(0;0)", 27, CYAN, BOLD)
        test_eq = mtx(r"0+2\cdot0=0\le6", 34, GREEN)
        test_group = VGroup(test_title, test_eq).arrange(DOWN,buff=0.28).move_to(test_box)
        self.play(FadeIn(test_box), FadeIn(test_group), run_time=0.6)
        self.narrate("Bây giờ ta chọn điểm O, tọa độ không không. Thay vào vế trái, ta được không nhỏ hơn hoặc bằng sáu, là mệnh đề đúng. Vì vậy miền nghiệm nằm về phía có chứa điểm O.",2.0)

        poly_pts = [axes.c2p(-1,-1), axes.c2p(7,-1), axes.c2p(7,-0.5), axes.c2p(-1,3.5)]
        # More accurate clipped quadrilateral under line in shown box
        region = Polygon(axes.c2p(-1,-1), axes.c2p(7,-1), axes.c2p(7,-0.5), axes.c2p(-1,3.5),
                         fill_color=GREEN, fill_opacity=0.20, stroke_opacity=0)
        self.play(FadeIn(region), run_time=0.8)
        self.narrate("Phần màu xanh là nửa mặt phẳng thỏa mãn bất phương trình. Đường biên được lấy vì dấu là nhỏ hơn hoặc bằng.",1.5)

        # check points
        self.clear_stage()
        self.add_header_footer("Ví dụ 1 – Bước 2", "Kiểm tra điểm bằng thế trực tiếp", "Ví dụ 1/3")
        rows = VGroup(
            VGroup(mtx(r"O(0,0):",32,CYAN), mtx(r"0\le6",32,GREEN), txt("→ thuộc miền nghiệm",25,GREEN)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"A(2,1):",32,CYAN), mtx(r"2+2=4\le6",32,GREEN), txt("→ thuộc miền nghiệm",25,GREEN)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"B(4,2):",32,CYAN), mtx(r"4+4=8>6",32,RED), txt("→ không thuộc",25,RED)).arrange(RIGHT,buff=0.25),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.55).shift(UP*0.2)
        for r in rows:
            self.play(FadeIn(r,shift=RIGHT*0.2),run_time=0.5)
        self.narrate("Ta kiểm tra trực tiếp. Điểm O và điểm A cho mệnh đề đúng nên thuộc miền nghiệm. Điểm B cho tám lớn hơn sáu, nên không thuộc miền nghiệm. Đây là cách kiểm tra chắc chắn nhất khi em phân vân một điểm có nằm trong miền đã tô hay không.",2.2)

    # ---------- concept 2 system ----------
    def system_two(self):
        self.show_problem(
            "Ví dụ 2 – Hệ hai bất phương trình",
            [
                "Giải hệ:",
                "x + y ≤ 5",
                "x − y ≥ 1",
                "và biểu diễn miền nghiệm trên mặt phẳng tọa độ."
            ],
            "Sang ví dụ hai, ta có một hệ gồm hai bất phương trình. Mỗi bất phương trình cho một nửa mặt phẳng. Miền nghiệm của hệ là phần giao của hai nửa mặt phẳng đó.",
            "Ví dụ 2/3"
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Từng miền một → lấy phần giao", "Ví dụ 2/3")
        axes = Axes(x_range=[-1,7,1], y_range=[-3,6,1], x_length=7.0, y_length=5.5,
                    axis_config={"color":MUTED,"include_numbers":True,"font_size":23})
        axes.shift(LEFT*2.5+DOWN*0.2)
        l1 = axes.plot(lambda x:5-x, x_range=[-1,7], color=BLUE, stroke_width=4)
        l2 = axes.plot(lambda x:x-1, x_range=[-1,7], color=ORANGE, stroke_width=4)
        e1 = mtx(r"x+y\le5",34,BLUE); e2=mtx(r"x-y\ge1",34,ORANGE)
        side = VGroup(e1,e2).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.55).shift(UP*1.4)
        self.play(Create(axes), FadeIn(side), run_time=1.0)
        self.play(Create(l1), run_time=0.8)
        self.narrate("Bất phương trình thứ nhất có đường biên x cộng y bằng năm. Điểm O thỏa mãn không nhỏ hơn hoặc bằng năm, nên ta chọn phía chứa O.",1.7)
        reg1 = Polygon(axes.c2p(-1,-3), axes.c2p(7,-3), axes.c2p(7,-2), axes.c2p(-1,6), fill_color=BLUE, fill_opacity=0.15, stroke_opacity=0)
        self.play(FadeIn(reg1), run_time=0.6)
        self.play(Create(l2), run_time=0.8)
        self.narrate("Bất phương trình thứ hai là x trừ y lớn hơn hoặc bằng một. Điểm O không thỏa mãn, nên lần này ta chọn phía không chứa O.",1.7)
        # Region satisfying y <= x-1 AND y <= 5-x in shown domain
        inter = Polygon(axes.c2p(-1,-3), axes.c2p(7,-3), axes.c2p(7,-2), axes.c2p(3,2), axes.c2p(-1,-2),
                        fill_color=GREEN, fill_opacity=0.28, stroke_color=GREEN, stroke_width=2)
        self.play(FadeIn(inter), run_time=0.8)
        p = label_point(axes,3,2,"I",GOLD,UR)
        self.play(FadeIn(p), run_time=0.4)
        self.narrate("Phần màu xanh lá là phần giao của hai miền. Hai đường biên cắt nhau tại I có tọa độ ba phẩy hai, vì giải hệ x cộng y bằng năm và x trừ y bằng một. Mọi điểm trong phần giao này đều đồng thời thỏa mãn cả hai bất phương trình.",2.2)

        # explain boundary inclusion
        box=make_panel(4.4,1.8).to_edge(RIGHT,buff=0.35).shift(DOWN*1.25)
        g=VGroup(txt("Dấu ≤ hoặc ≥",26,GOLD,BOLD),txt("→ lấy cả đường biên",25,INK)).arrange(DOWN,buff=0.2).move_to(box)
        self.play(FadeIn(box),FadeIn(g),run_time=0.5)
        self.narrate("Các em chú ý: vì cả hai dấu đều có dấu bằng, nên hai đường thẳng biên đều thuộc miền nghiệm.",1.2)

    # ---------- system 3 + x,y >=0 ----------
    def system_three(self):
        self.show_problem(
            "Ví dụ 3 – Hệ nhiều điều kiện",
            [
                "Tìm miền nghiệm của hệ:",
                "2x + y ≤ 8",
                "x + 2y ≤ 8",
                "x ≥ 0,  y ≥ 0."
            ],
            "Ví dụ ba gần với các bài toán thực tế và quy hoạch tuyến tính. Ngoài hai bất phương trình chính, ta còn có điều kiện x không âm và y không âm. Vì vậy miền nghiệm bị giới hạn trong góc phần tư thứ nhất.",
            "Ví dụ 3/3"
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Hệ 4 điều kiện", "Ví dụ 3/3")
        axes=Axes(x_range=[-1,7,1],y_range=[-1,7,1],x_length=6.8,y_length=5.6,
                  axis_config={"color":MUTED,"include_numbers":True,"font_size":23})
        axes.shift(LEFT*2.3+DOWN*0.15)
        l1=axes.plot(lambda x:8-2*x,x_range=[0,4],color=BLUE,stroke_width=4)
        l2=axes.plot(lambda x:(8-x)/2,x_range=[0,7],color=ORANGE,stroke_width=4)
        formulas=VGroup(mtx(r"2x+y\le8",32,BLUE),mtx(r"x+2y\le8",32,ORANGE),mtx(r"x\ge0,\ y\ge0",32,GREEN)).arrange(DOWN,buff=0.22)
        formulas.to_edge(RIGHT,buff=0.5).shift(UP*1.3)
        self.play(Create(axes),FadeIn(formulas),run_time=1.0)
        self.play(Create(l1),Create(l2),run_time=1.0)
        self.narrate("Ta vẽ hai đường biên. Đường màu xanh là hai x cộng y bằng tám. Đường màu cam là x cộng hai y bằng tám.",1.5)

        vertices=[(0,0),(4,0),(8/3,8/3),(0,4)]
        poly=Polygon(*[axes.c2p(x,y) for x,y in vertices],fill_color=GREEN,fill_opacity=0.28,stroke_color=GREEN,stroke_width=3)
        self.play(FadeIn(poly),run_time=0.8)
        labs=VGroup(
            label_point(axes,0,0,"O",CYAN,DL),
            label_point(axes,4,0,"A",CYAN,DR),
            label_point(axes,8/3,8/3,"B",GOLD,UR),
            label_point(axes,0,4,"C",CYAN,UL),
        )
        self.play(FadeIn(labs),run_time=0.7)
        self.narrate("Điều kiện x không âm và y không âm giữ ta trong góc phần tư thứ nhất. Phần giao cuối cùng là tứ giác O A B C.",1.4)

        # intersection derivation
        box=make_panel(4.8,2.8).to_edge(RIGHT,buff=0.25).shift(DOWN*1.25)
        calc=VGroup(
            txt("Tìm giao điểm B",27,CYAN,BOLD),
            mtx(r"\begin{cases}2x+y=8\\x+2y=8\end{cases}",30,INK),
            mtx(r"x=y=\frac83",32,GOLD),
        ).arrange(DOWN,buff=0.20).move_to(box)
        self.play(FadeIn(box),FadeIn(calc),run_time=0.7)
        self.narrate("Đỉnh B là giao của hai đường biên. Giải hệ hai x cộng y bằng tám và x cộng hai y bằng tám, ta được x bằng y bằng tám phần ba.",1.6)

        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Kiểm tra một điểm trong và một điểm ngoài", "Ví dụ 3/3")
        rows=VGroup(
            VGroup(mtx(r"M(2,2)",32,CYAN),mtx(r"2\cdot2+2=6\le8",30,GREEN),mtx(r"2+2\cdot2=6\le8",30,GREEN)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"N(4,3)",32,CYAN),mtx(r"2\cdot4+3=11>8",30,RED),txt("→ loại ngay",25,RED)).arrange(RIGHT,buff=0.25),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.65).shift(UP*0.2)
        for r in rows:self.play(FadeIn(r,shift=RIGHT*0.2),run_time=0.5)
        self.narrate("Điểm M hai hai thỏa cả hai bất phương trình chính và hai điều kiện không âm, nên thuộc miền nghiệm. Điểm N bốn ba đã vi phạm bất phương trình đầu tiên, nên ta có thể loại ngay mà không cần kiểm tra tiếp.",1.8)

    # ---------- pitfalls ----------
    def pitfalls(self):
        self.clear_stage(); self.add_header_footer("Những lỗi rất dễ mắc", "Hãy tránh 5 lỗi này", "Tổng kết")
        items=VGroup(
            bullet("Tô theo cảm tính mà không thử một điểm.",RED,27,RED),
            bullet("Quên đổi bất phương trình thành phương trình đường biên.",INK,27,ORANGE),
            bullet("Quên phân biệt <, > với ≤, ≥ khi vẽ đường biên.",INK,27,GOLD),
            bullet("Chỉ tô từng miền mà quên lấy phần giao của cả hệ.",INK,27,CYAN),
            bullet("Quên điều kiện x ≥ 0, y ≥ 0 trong bài toán thực tế.",INK,27,GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.36).shift(DOWN*0.1)
        for i,b in enumerate(items): self.play(FadeIn(b,shift=RIGHT*0.15),run_time=0.35)
        self.narrate("Có năm lỗi các em cần tránh. Một, tô theo cảm tính. Hai, quên vẽ đường biên. Ba, quên xem đường biên có được lấy hay không. Bốn, quên lấy phần giao. Và năm, trong bài toán thực tế, quên điều kiện các đại lượng thường không âm.",2.0)

    def recipe(self):
        self.clear_stage(); self.add_header_footer("Quy trình 5 bước", "Dùng cho mọi hệ bất phương trình bậc nhất hai ẩn", "Tổng kết")
        steps=VGroup(
            VGroup(txt("1",30,GOLD,BOLD),txt("Vẽ từng đường biên bằng cách thay bất phương trình bởi phương trình.",27,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("2",30,GOLD,BOLD),txt("Chọn một điểm thử không nằm trên đường biên.",27,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("3",30,GOLD,BOLD),txt("Thế điểm thử để chọn đúng nửa mặt phẳng.",27,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("4",30,GOLD,BOLD),txt("Lặp lại với tất cả các bất phương trình.",27,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("5",30,GOLD,BOLD),txt("Lấy phần giao và kiểm tra các đường biên có được lấy hay không.",27,INK)).arrange(RIGHT,buff=0.25),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.35).shift(DOWN*0.1)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.18),run_time=0.35)
        self.narrate("Các em có thể dùng quy trình năm bước này cho hầu hết các bài. Vẽ đường biên, chọn điểm thử, xác định nửa mặt phẳng, lặp lại với từng điều kiện, rồi lấy phần giao cuối cùng.",1.8)

    def practice(self):
        self.show_problem(
            "Bài tự luyện",
            [
                "Biểu diễn miền nghiệm của hệ:",
                "x + y ≤ 6",
                "2x + y ≥ 4",
                "x ≥ 0,  y ≥ 0.",
                "Hãy dự đoán hình dạng miền nghiệm trước khi vẽ."
            ],
            "Trước khi kết thúc, các em hãy thử tự làm bài này. Vẽ hai đường biên x cộng y bằng sáu và hai x cộng y bằng bốn. Kết hợp với điều kiện x và y không âm. Hãy tạm dừng video và dự đoán hình dạng miền nghiệm trước khi xem gợi ý.",
            "Bài tự luyện"
        )
        self.clear_stage(); self.add_header_footer("Gợi ý bài tự luyện", "Đừng xem quá sớm", "Bài tự luyện")
        hints=VGroup(
            bullet("Đường 1: x + y = 6 → qua (0;6), (6;0).",INK,27,BLUE),
            bullet("Đường 2: 2x + y = 4 → qua (0;4), (2;0).",INK,27,ORANGE),
            bullet("Miền cần tìm nằm trong góc phần tư thứ nhất.",INK,27,GREEN),
            bullet("Một điều kiện lấy phía dưới, một điều kiện lấy phía trên.",INK,27,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.4).shift(DOWN*0.1)
        for h in hints:self.play(FadeIn(h,shift=RIGHT*0.2),run_time=0.35)
        self.narrate("Gợi ý: một đường đi qua không sáu và sáu không. Đường còn lại đi qua không bốn và hai không. Miền nghiệm nằm trong góc phần tư thứ nhất, phía dưới đường thứ nhất nhưng phía trên đường thứ hai.",1.8)

    def outro(self):
        self.clear_stage()
        t=txt("CHỐT LẠI",44,GOLD,BOLD)
        a=txt("Mỗi bất phương trình → một nửa mặt phẳng",31,INK)
        b=txt("Cả hệ → phần giao của các nửa mặt phẳng",31,CYAN,BOLD)
        c=txt("Hiểu hình học trước, thao tác sẽ trở nên rất nhẹ.",28,MUTED)
        brand=txt(TEN_THAY,23,MUTED)
        g=VGroup(t,a,b,c,brand).arrange(DOWN,buff=0.28).move_to(ORIGIN)
        self.play(FadeIn(t),run_time=0.5)
        self.play(Write(a),Write(b),run_time=1.2)
        self.play(FadeIn(c),FadeIn(brand),run_time=0.6)
        self.narrate("Điều quan trọng nhất của bài hôm nay là: mỗi bất phương trình cho một nửa mặt phẳng, còn hệ bất phương trình cho phần giao của các nửa mặt phẳng đó. Khi em hiểu được bức tranh hình học này, mọi thao tác tô miền sẽ trở nên rõ ràng và có lý do.",2.0)

    def construct(self):
        self.intro()
        self.foundation()
        self.one_inequality()
        self.system_two()
        self.system_three()
        self.pitfalls()
        self.recipe()
        self.practice()
        self.outro()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "he_bat_phuong_trinh_bac_nhat_hai_an_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Không tìm thấy video Manim cuối: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    print("\n============================================================")
    print(f"VIDEO HOÀN CHỈNH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


if __name__ == "__main__":
    render_full()

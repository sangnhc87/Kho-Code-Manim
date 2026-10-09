from manim import *
from pathlib import Path
import hashlib, json, math, subprocess, sys, time

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
PURPLE = "#C084FC"

# ==========================================================
# LATEX / TEXT HELPERS
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


def fit_width(mob, width=12.2):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def make_panel(width=12.2, height=5.4):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        fill_color=PANEL,
        fill_opacity=0.90,
        stroke_color=MUTED,
        stroke_opacity=0.22,
        stroke_width=1.5,
    )


def title_block(title, subtitle=None):
    t = fit_width(txt(title, 38, INK, BOLD), 12.0).to_edge(UP, buff=0.25)
    if subtitle:
        s = fit_width(txt(subtitle, 23, MUTED), 11.6).next_to(t, DOWN, buff=0.10)
        return VGroup(t, s)
    return VGroup(t)


def footer(page_text=""):
    left = txt(TEN_THAY, 19, MUTED)
    right = txt(page_text, 19, MUTED)
    left.to_edge(DOWN, buff=0.18).to_edge(LEFT, buff=0.38)
    right.to_edge(DOWN, buff=0.18).to_edge(RIGHT, buff=0.38)
    return VGroup(left, right)


def bullet(text, color=INK, size=27, dot_color=BLUE):
    d = Dot(radius=0.055, color=dot_color)
    t = txt(text, size, color)
    return VGroup(d, t).arrange(RIGHT, buff=0.18, aligned_edge=UP)

# ==========================================================
# EXACT COUNTING HELPERS
# ==========================================================
def disk_count_sq(n):
    """Number of integer (x,y) with x^2+y^2 <= n, n >= 0 integer."""
    if n < 0:
        return 0
    a = math.isqrt(n)
    total = 0
    for x in range(-a, a + 1):
        total += 2 * math.isqrt(n - x*x) + 1
    return total


def sphere_count(R):
    return sum(disk_count_sq(R*R - z*z) for z in range(-R, R + 1))


def layer_count(R, z):
    return disk_count_sq(R*R - z*z)


def sphere_surface_count(R):
    total = 0
    rr = R * R
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            rem = rr - x*x - y*y
            if rem < 0:
                continue
            z = math.isqrt(rem)
            if z*z == rem:
                total += 1 if z == 0 else 2
    return total

# ==========================================================
# TTS + MASTER AUDIO
# ==========================================================
def _audio_key(text):
    payload = json.dumps(
        {"text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC, "pitch": PITCH, "engine": "edge-tts"},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ]
    return float(subprocess.check_output(cmd, text=True).strip())


def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError(f"Audio khong hop le: {path}")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], check=True)


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
    raise RuntimeError(f"Edge TTS that bai sau 3 lan: {last_err}")


def build_master_audio(events, video_duration, out_wav: Path):
    if not events:
        raise RuntimeError("Khong co narration nao de ghep.")
    inputs = []
    filters = []
    labels = []
    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]adelay={ms}|{ms},aresample=48000[a{i}]")
        labels.append(f"[a{i}]")
    filter_complex = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    cmd = [
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", filter_complex, "-map", "[m]",
        "-ar", "48000", "-ac", "2", "-t", f"{video_duration:.3f}", str(out_wav),
    ]
    subprocess.run(cmd, check=True)


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out),
    ], check=True)

# ==========================================================
# LESSON
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []

    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def narrate_while(self, text, animation, min_hold=0.25, max_anim=4.5):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        rt = min(max(0.9, dur * 0.55), max_anim)
        self.play(animation, run_time=rt)
        self.wait(max(min_hold, dur - rt + min_hold))
        return dur

    def clear_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.42)

    def add_header_footer(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, lines, voice, progress):
        self.clear_stage()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_header_footer(title, "ĐỀ BÀI", progress)
        p = make_panel(12.35, 5.15).shift(DOWN * 0.10)
        self.play(FadeIn(p), run_time=0.5)
        line_mobs = VGroup()
        for i, line in enumerate(lines):
            if isinstance(line, Mobject):
                mob = line
            else:
                mob = fit_width(txt(line, 28 if i == 0 else 26, INK if i == 0 else "#D8E7FF", BOLD if i == 0 else NORMAL), 11.2)
            line_mobs.add(mob)
        line_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(p.get_center()).shift(UP * 0.06)
        for mob in line_mobs:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.30)
        self.narrate(voice, 2.0)

    # ------------------------------------------------------
    # INTRO
    # ------------------------------------------------------
    def intro(self):
        self.clear_stage()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        g = VGroup(
            txt("ĐẾM SỐ ĐIỂM NGUYÊN", 48, GOLD, BOLD),
            txt("TRONG QUẢ CẦU TÂM O, BÁN KÍNH R", 35, INK, BOLD),
            mtx(r"x^2+y^2+z^2\le R^2,\qquad R\in\mathbb N^*", 41, CYAN),
            txt("Từ lát cắt 2D → công thức 3D → ứng dụng", 27, MUTED),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.28)
        fit_width(g, 12.0)
        self.play(FadeIn(g[0], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(g[1]), Write(g[2]), run_time=1.2)
        self.play(FadeIn(g[3]), FadeIn(g[4]), run_time=0.6)
        self.narrate(
            "Chào các em. Hôm nay chúng ta tiếp tục bài toán đếm điểm nguyên, nhưng nâng từ mặt phẳng lên không gian. Ta sẽ đếm tất cả các điểm có ba tọa độ nguyên nằm trong hoặc trên một quả cầu tâm O, bán kính R. Điều hay nhất của bài này là ta không cần phát minh một phương pháp hoàn toàn mới. Chỉ cần cắt quả cầu thành từng lát ngang, mỗi lát lại trở về đúng bài đếm điểm nguyên trong đường tròn mà các em vừa học.",
            2.5,
        )

    # ------------------------------------------------------
    # GENERAL PROBLEM
    # ------------------------------------------------------
    def general_problem(self):
        self.show_problem(
            "Bài toán tổng quát",
            [
                "Cho quả cầu tâm O trùng gốc tọa độ, bán kính R là số tự nhiên dương.",
                mtx(r"(S):\ x^2+y^2+z^2\le R^2", 40, GOLD),
                mtx(r"(x,y,z)\in\mathbb Z^3", 36, CYAN),
                "Hỏi có bao nhiêu điểm nguyên nằm trong hoặc trên quả cầu?",
            ],
            "Ta phát biểu bài toán thật rõ. Một điểm M có tọa độ x, y, z đều nguyên. Điểm đó được tính nếu x bình phương cộng y bình phương cộng z bình phương không vượt quá R bình phương. Dấu nhỏ hơn hoặc bằng có nghĩa là ta tính cả các điểm nằm đúng trên mặt cầu.",
            "Phần 1/9",
        )

        self.clear_stage()
        self.add_header_footer("Ý tưởng chủ đạo", "Cắt quả cầu theo từng mặt phẳng z = k", "Phần 1/9")
        a = mtx(r"z=k", 40, BLUE)
        b = mtx(r"x^2+y^2+k^2\le R^2", 39, INK)
        c = mtx(r"x^2+y^2\le R^2-k^2", 42, CYAN)
        d = mtx(r"r_k=\sqrt{R^2-k^2}", 42, GOLD)
        arr = VGroup(a, b, c, d).arrange(DOWN, buff=0.36).shift(UP * 0.3)
        for mob in arr:
            self.play(Write(mob), run_time=0.65)
        note = txt("Mỗi lớp z = k là một đĩa tròn 2D.", 30, GREEN, BOLD).next_to(arr, DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=0.5)
        self.narrate(
            "Ta cố định z bằng một số nguyên k. Khi ấy bài toán ba chiều trở thành x bình phương cộng y bình phương nhỏ hơn hoặc bằng R bình phương trừ k bình phương. Đây chính là một đĩa tròn trên mặt phẳng z bằng k, có bán kính căn R bình phương trừ k bình phương. Vậy bài toán quả cầu được tách thành nhiều bài toán đường tròn hai chiều.",
            2.0,
        )

    # ------------------------------------------------------
    # 3D VISUAL IDEA R=3
    # ------------------------------------------------------
    def slicing_3d(self):
        self.clear_stage()
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.86)
        fixed_title = title_block("Nhìn quả cầu bằng các lát cắt", "Minh họa với R = 3")
        fixed_footer = footer("Phần 2/9")
        self.add_fixed_in_frame_mobjects(fixed_title, fixed_footer)

        axes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1], z_range=[-3.5, 3.5, 1],
            x_length=6.3, y_length=6.3, z_length=6.3,
            axis_config={"color": MUTED, "stroke_width": 2},
        ).shift(DOWN * 0.35)
        sphere = Sphere(radius=2.7, resolution=(16, 28))
        sphere.set_fill(BLUE, opacity=0.10).set_stroke(BLUE, width=1.0, opacity=0.28)
        sphere.move_to(axes.c2p(0, 0, 0))
        self.play(Create(axes), FadeIn(sphere), run_time=1.3)
        self.begin_ambient_camera_rotation(rate=0.055)
        self.narrate(
            "Đây là quả cầu bán kính ba nhìn trong không gian. Các điểm nguyên không nằm liên tục như vật chất trong quả cầu; chúng nằm tại các nút của lưới không gian. Để đếm dễ hơn, ta không nhìn toàn bộ một lúc mà sẽ đi lần lượt theo các lớp z bằng âm ba, âm hai, âm một, không, một, hai và ba.",
            2.0,
        )
        self.stop_ambient_camera_rotation()

        colors = [PURPLE, ORANGE, CYAN, GOLD, CYAN, ORANGE, PURPLE]
        layers = VGroup()
        for idx, z in enumerate(range(-3, 4)):
            rr = 9 - z*z
            r = math.sqrt(rr)
            circ = ParametricFunction(
                lambda t, z=z, r=r: axes.c2p(r*math.cos(t), r*math.sin(t), z),
                t_range=[0, TAU], color=colors[idx], stroke_width=4,
            )
            layers.add(circ)
        self.play(LaggedStart(*[Create(c) for c in layers], lag_ratio=0.14), run_time=3.0)
        self.narrate(
            "Mỗi vòng màu là biên của một lát cắt. Lát giữa z bằng không có bán kính ba và lớn nhất. Càng đi lên hoặc đi xuống, bán kính lát cắt nhỏ dần. Ở z bằng cộng hoặc trừ ba, lát cắt co lại chỉ còn đúng điểm nằm trên trục z.",
            1.9,
        )

        self.play(FadeOut(sphere), run_time=0.5)
        pts = VGroup()
        for z in range(-3, 4):
            rr = 9 - z*z
            lim = math.isqrt(rr)
            col = colors[z + 3]
            for x in range(-lim, lim + 1):
                yy = math.isqrt(rr - x*x)
                for y in range(-yy, yy + 1):
                    pts.add(Dot3D(axes.c2p(x, y, z), radius=0.038, color=col))
        self.play(LaggedStart(*[FadeIn(p, scale=1.35) for p in pts], lag_ratio=0.004), run_time=3.0)
        self.begin_ambient_camera_rotation(rate=-0.045)
        self.narrate(
            "Bây giờ ta đặt các điểm nguyên thật sự vào từng lát. Tổng cộng với R bằng ba có một trăm hai mươi ba điểm. Nhưng đừng cố đếm trực tiếp bằng mắt. Điều quan trọng là mỗi màu tương ứng với một lớp z, và số điểm của lớp đó chính là số điểm nguyên của một đĩa tròn hai chiều.",
            2.0,
        )
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(pts), FadeOut(layers), FadeOut(axes), run_time=0.6)
        self.remove_fixed_in_frame_mobjects(fixed_title, fixed_footer)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

    # ------------------------------------------------------
    # DISK COUNT FUNCTION
    # ------------------------------------------------------
    def disk_function(self):
        self.clear_stage()
        self.add_header_footer("Nhắc lại bài toán 2D", "Đếm điểm nguyên trong một đĩa tròn", "Phần 3/9")
        p = make_panel(12.1, 5.0).shift(DOWN * 0.05)
        self.play(FadeIn(p), run_time=0.5)
        e1 = mtx(r"D(n)=\#\{(x,y)\in\mathbb Z^2:x^2+y^2\le n\}", 37, BLUE)
        e2 = mtx(r"-\lfloor\sqrt n\rfloor\le x\le\lfloor\sqrt n\rfloor", 35, INK)
        e3 = mtx(r"|y|\le\sqrt{n-x^2}", 38, CYAN)
        e4 = mtx(r"2\left\lfloor\sqrt{n-x^2}\right\rfloor+1", 39, GREEN)
        e5 = mtx(r"\boxed{D(n)=\sum_{x=-\lfloor\sqrt n\rfloor}^{\lfloor\sqrt n\rfloor}\left(2\left\lfloor\sqrt{n-x^2}\right\rfloor+1\right)}", 37, GOLD)
        g = VGroup(e1, e2, e3, e4, e5).arrange(DOWN, buff=0.30).move_to(p)
        fit_width(g, 11.2)
        for mob in g:
            self.play(Write(mob), run_time=0.68)
        self.narrate(
            "Để tránh viết lặp lại một công thức rất dài, ta ký hiệu D của n là số điểm nguyên x y thỏa x bình phương cộng y bình phương không vượt quá n. Với mỗi x nguyên, số giá trị y là hai lần phần nguyên của căn n trừ x bình phương, rồi cộng một. Cộng theo tất cả các cột x, ta có công thức chính xác cho D của n.",
            2.1,
        )

        callout = VGroup(
            txt("Lưu ý:", 27, ORANGE, BOLD),
            txt("bán kính lát cắt có thể không nguyên; nhưng", 27, INK),
            mtx(r"n=R^2-k^2\in\mathbb Z", 35, GOLD),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.72)
        fit_width(callout, 11.6)
        self.play(FadeIn(callout), run_time=0.5)
        self.narrate(
            "Một chi tiết rất quan trọng: bán kính của lát cắt, căn R bình phương trừ k bình phương, thường không phải số nguyên. Nhưng bình phương bán kính là R bình phương trừ k bình phương, luôn là số nguyên. Vì vậy dùng D của n là cách viết vừa chính xác vừa gọn.",
            1.7,
        )

    # ------------------------------------------------------
    # GENERAL SPHERE FORMULA
    # ------------------------------------------------------
    def general_formula(self):
        self.clear_stage()
        self.add_header_footer("Công thức tổng quát cho quả cầu", "Cộng các lát z = k", "Phần 4/9")
        a = mtx(r"-R\le z\le R,\qquad z\in\mathbb Z", 38, CYAN)
        b = mtx(r"L_z=D(R^2-z^2)", 42, BLUE)
        c = mtx(r"\boxed{S(R)=\sum_{z=-R}^{R}D(R^2-z^2)}", 46, GOLD)
        g = VGroup(a, b, c).arrange(DOWN, buff=0.55).shift(UP * 0.45)
        for mob in g:
            self.play(Write(mob), run_time=0.8)
        self.narrate(
            "Tọa độ z chỉ có thể chạy từ âm R đến R. Ở mỗi lớp z, số điểm nguyên đúng bằng D của R bình phương trừ z bình phương. Vì các lớp khác nhau không trùng điểm, tổng số điểm trong quả cầu chỉ là tổng số điểm của tất cả các lớp. Ta ký hiệu kết quả đó là S của R.",
            1.9,
        )

        nested = mtx(
            r"S(R)=\sum_{z=-R}^{R}\ \sum_{x=-\lfloor\sqrt{R^2-z^2}\rfloor}^{\lfloor\sqrt{R^2-z^2}\rfloor}\left(2\left\lfloor\sqrt{R^2-z^2-x^2}\right\rfloor+1\right)",
            31, GREEN,
        ).shift(DOWN * 1.7)
        fit_width(nested, 12.0)
        self.play(Write(nested), run_time=1.3)
        self.narrate(
            "Nếu thay luôn công thức của D vào, ta thu được một tổng kép hoàn toàn chính xác. Nhìn có vẻ dài, nhưng ý nghĩa rất đơn giản: chọn một lớp z, rồi trong lớp đó chọn từng cột x và đếm các giá trị y nguyên. Công thức dài chỉ là cách viết gọn của hai bước đếm liên tiếp.",
            2.0,
        )

    # ------------------------------------------------------
    # EXAMPLE R=2
    # ------------------------------------------------------
    def example_r2(self):
        self.show_problem(
            "Ví dụ 1 – Quả cầu bán kính 2",
            [
                "Đếm số điểm nguyên thỏa:",
                mtx(r"x^2+y^2+z^2\le4", 42, GOLD),
                mtx(r"(x,y,z)\in\mathbb Z^3", 35, CYAN),
                "Giải bằng phương pháp lát cắt theo z.",
            ],
            "Ví dụ đầu tiên có bán kính bằng hai. Ta không đếm ba chiều trực tiếp. Ta xét lần lượt năm lớp z bằng âm hai, âm một, không, một và hai. Mỗi lớp là một đĩa tròn hai chiều.",
            "Phần 5/9",
        )
        self.clear_stage()
        self.add_header_footer("Ví dụ R = 2", "Đếm từng lớp thật chậm", "Phần 5/9")
        rows = VGroup(
            mtx(r"z=0:\quad x^2+y^2\le4\Rightarrow D(4)=13", 34, INK),
            mtx(r"z=\pm1:\quad x^2+y^2\le3\Rightarrow D(3)=9", 34, CYAN),
            mtx(r"z=\pm2:\quad x^2+y^2\le0\Rightarrow D(0)=1", 34, PURPLE),
            mtx(r"S(2)=13+2\cdot9+2\cdot1", 40, BLUE),
            mtx(r"\boxed{S(2)=33}", 48, GOLD),
        ).arrange(DOWN, buff=0.34).shift(UP * 0.10)
        fit_width(rows, 11.5)
        for mob in rows:
            self.play(Write(mob), run_time=0.72)
        self.narrate(
            "Ở lớp giữa z bằng không, ta có đĩa bán kính hai nên có mười ba điểm, đúng kết quả của bài trước. Ở z bằng cộng hoặc trừ một, điều kiện còn x bình phương cộng y bình phương không vượt quá ba. Chín điểm của hình vuông nhỏ từ âm một đến một đều thỏa. Ở z bằng cộng hoặc trừ hai chỉ còn x bằng y bằng không, nên mỗi lớp có một điểm. Tổng là mười ba cộng hai lần chín cộng hai lần một, bằng ba mươi ba.",
            2.3,
        )

    # ------------------------------------------------------
    # EXAMPLE R=3 DETAILED
    # ------------------------------------------------------
    def example_r3(self):
        self.show_problem(
            "Ví dụ 2 – Quả cầu bán kính 3",
            [
                "Đếm số điểm nguyên thỏa:",
                mtx(r"x^2+y^2+z^2\le9", 42, GOLD),
                "Lập bảng số điểm theo từng lớp z và cộng đối xứng.",
            ],
            "Bây giờ ta làm ví dụ trung tâm với bán kính bằng ba. Đây chính là quả cầu ba chiều các em đã nhìn thấy lúc đầu. Ta sẽ tính chính xác số điểm của từng lát, rồi cộng lại bằng đối xứng qua mặt phẳng z bằng không.",
            "Phần 6/9",
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ R = 3", "Bảng các lớp theo |z|", "Phần 6/9")
        header = VGroup(mtx(r"|z|", 31, GOLD), mtx(r"R^2-z^2", 31, GOLD), mtx(r"D(R^2-z^2)", 31, GOLD)).arrange(RIGHT, buff=1.20).shift(UP * 2.15)
        fit_width(header, 10.7)
        self.play(FadeIn(header), run_time=0.5)
        data = [(0, 9, 29), (1, 8, 25), (2, 5, 21), (3, 0, 1)]
        table = VGroup()
        for z, n, c in data:
            row = VGroup(mtx(str(z), 31, INK), mtx(str(n), 31, CYAN), mtx(str(c), 31, GREEN)).arrange(RIGHT, buff=2.35)
            table.add(row)
        table.arrange(DOWN, buff=0.38).shift(DOWN * 0.05)
        for row in table:
            self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.36)
        self.narrate(
            "Ta chỉ cần xét trị tuyệt đối của z vì các lớp phía trên và phía dưới đối xứng. Với z bằng không, n bằng chín và lớp giữa có hai mươi chín điểm. Với độ cao một, n bằng tám và có hai mươi lăm điểm. Với độ cao hai, n bằng năm và có hai mươi mốt điểm. Với độ cao ba, n bằng không nên chỉ còn đúng một điểm trên trục z.",
            2.2,
        )

        result = VGroup(
            mtx(r"S(3)=D(9)+2D(8)+2D(5)+2D(0)", 38, BLUE),
            mtx(r"=29+2(25+21+1)", 42, CYAN),
            mtx(r"=29+94", 42, CYAN),
            mtx(r"\boxed{S(3)=123}", 50, GOLD),
        ).arrange(DOWN, buff=0.36).shift(DOWN * 1.55)
        fit_width(result, 11.4)
        for mob in result:
            self.play(Write(mob), run_time=0.65)
        self.narrate(
            "Lớp z bằng không xuất hiện một lần. Các lớp z bằng một, hai và ba đều có lớp đối xứng ở phía âm, nên nhân đôi. Ta được hai mươi chín cộng hai lần tổng hai mươi lăm, hai mươi mốt và một. Kết quả là một trăm hai mươi ba điểm nguyên.",
            1.8,
        )

    # ------------------------------------------------------
    # EXAMPLE R=5 APPLICATION
    # ------------------------------------------------------
    def example_r5(self):
        self.show_problem(
            "Ví dụ 3 – Áp dụng với R = 5",
            [
                "Đếm số điểm nguyên trong hoặc trên quả cầu:",
                mtx(r"x^2+y^2+z^2\le25", 42, GOLD),
                "Dùng kết quả đếm theo lớp, không liệt kê 515 điểm.",
            ],
            "Với bán kính năm, việc vẽ từng điểm sẽ rất rối. Ta dùng đúng công thức lớp. Điều quan trọng là biết tổ chức tính toán, chứ không phải liệt kê năm trăm mười lăm điểm bằng tay.",
            "Phần 7/9",
        )
        self.clear_stage()
        self.add_header_footer("Ví dụ R = 5", "Các lớp từ tâm ra ngoài", "Phần 7/9")
        rows = VGroup(
            mtx(r"D(25)=81", 33, GOLD),
            mtx(r"D(24)=69", 33, CYAN),
            mtx(r"D(21)=69", 33, CYAN),
            mtx(r"D(16)=49", 33, CYAN),
            mtx(r"D(9)=29", 33, CYAN),
            mtx(r"D(0)=1", 33, CYAN),
        ).arrange(RIGHT, buff=0.46).shift(UP * 1.25)
        fit_width(rows, 11.8)
        self.play(FadeIn(rows), run_time=0.9)
        calc = VGroup(
            mtx(r"S(5)=81+2(69+69+49+29+1)", 40, BLUE),
            mtx(r"=81+434", 42, CYAN),
            mtx(r"\boxed{S(5)=515}", 50, GOLD),
        ).arrange(DOWN, buff=0.38).shift(DOWN * 0.65)
        for mob in calc:
            self.play(Write(mob), run_time=0.72)
        self.narrate(
            "Lớp giữa z bằng không chính là đĩa bán kính năm nên có tám mươi mốt điểm. Các lớp độ cao một và hai đều có sáu mươi chín điểm; độ cao ba có bốn mươi chín; độ cao bốn có hai mươi chín; và độ cao năm chỉ có một điểm. Cộng lớp giữa với hai lần các lớp dương, ta được năm trăm mười lăm điểm nguyên.",
            2.0,
        )

    # ------------------------------------------------------
    # VOLUME COMPARISON + SURFACE
    # ------------------------------------------------------
    def deeper(self):
        self.clear_stage()
        self.add_header_footer("Đừng nhầm với thể tích", "Đếm rời rạc khác đo liên tục", "Phần 8/9")
        g = VGroup(
            mtx(r"S(5)=515", 45, GOLD),
            mtx(r"V=\frac43\pi R^3=\frac{500}{3}\pi\approx523.60", 42, ORANGE),
            mtx(r"515\ne523.60", 40, RED),
            txt("Thể tích chỉ cho một ước lượng, không phải số điểm nguyên chính xác.", 27, MUTED),
        ).arrange(DOWN, buff=0.40)
        fit_width(g, 11.6)
        for mob in g:
            self.play(FadeIn(mob) if isinstance(mob, Text) else Write(mob), run_time=0.68)
        self.narrate(
            "Cũng giống bài đường tròn, ta không được lấy thể tích quả cầu để thay cho số điểm nguyên. Với R bằng năm, số điểm chính xác là năm trăm mười lăm, còn thể tích là năm trăm phần ba nhân pi, xấp xỉ năm trăm hai mươi ba phẩy sáu. Hai đại lượng khá gần nhưng bản chất khác nhau: một bên đếm các nút rời rạc, một bên đo thể tích liên tục.",
            2.0,
        )

        self.clear_stage()
        self.add_header_footer("Mở rộng – Điểm trên mặt cầu", "Phân biệt \u201ctrong quả cầu\u201d và \u201ctrên mặt cầu\u201d", "Phần 8/9")
        a = mtx(r"x^2+y^2+z^2=25", 42, BLUE)
        b = mtx(r"25=5^2+0^2+0^2", 36, CYAN)
        c = mtx(r"25=4^2+3^2+0^2", 36, CYAN)
        d = mtx(r"B(5)=6+24=30", 42, GOLD)
        e = mtx(r"I(5)=515-30=485", 43, GREEN)
        group = VGroup(a, b, c, d, e).arrange(DOWN, buff=0.34)
        for mob in group:
            self.play(Write(mob), run_time=0.68)
        self.narrate(
            "Nếu đề chỉ hỏi các điểm nằm đúng trên mặt cầu bán kính năm, ta thay dấu nhỏ hơn hoặc bằng bằng dấu bằng. Hai kiểu biểu diễn hai mươi lăm bởi tổng ba bình phương cơ bản là năm bình phương cộng không cộng không, và bốn bình phương cộng ba bình phương cộng không. Kiểu thứ nhất tạo sáu điểm trên ba trục. Kiểu thứ hai, sau khi hoán vị tọa độ và chọn dấu, tạo hai mươi bốn điểm. Tổng cộng có ba mươi điểm trên mặt cầu. Vì vậy số điểm nằm nghiêm ngặt bên trong là năm trăm mười lăm trừ ba mươi, bằng bốn trăm tám mươi lăm.",
            2.4,
        )

    # ------------------------------------------------------
    # REAL APPLICATION + SUMMARY
    # ------------------------------------------------------
    def summary(self):
        self.clear_stage()
        self.add_header_footer("Mô hình thực tế", "Các nút cảm biến trong vùng phủ sóng 3D", "Phần 9/9")
        p = make_panel(12.1, 4.9).shift(DOWN * 0.08)
        self.play(FadeIn(p), run_time=0.45)
        lines = VGroup(
            txt("Các cảm biến được đặt tại các nút lưới không gian cách nhau 1 m.", 27, INK),
            txt("Trạm O kích hoạt mọi nút cách O không quá 3 m.", 27, INK),
            mtx(r"x^2+y^2+z^2\le9", 39, CYAN),
            VGroup(mtx(r"\boxed{123}", 44, GOLD), txt("nút cảm biến được kích hoạt", 27, GOLD, BOLD)).arrange(RIGHT, buff=0.20),
        ).arrange(DOWN, buff=0.36).move_to(p)
        fit_width(lines, 11.2)
        for mob in lines:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.38)
        self.narrate(
            "Một mô hình thực tế dễ hình dung là các cảm biến đặt tại các nút của lưới ba chiều, mỗi nút cách nhau một mét theo ba phương. Nếu trạm trung tâm chỉ kích hoạt các nút cách O không quá ba mét, bài toán đúng là đếm điểm nguyên trong quả cầu bán kính ba. Kết quả một trăm hai mươi ba chính là số cảm biến được kích hoạt.",
            1.9,
        )

        self.clear_stage()
        self.add_header_footer("Chốt lại phương pháp", "Từ 3D về 2D", "Tổng kết")
        steps = VGroup(
            VGroup(txt("1", 30, GOLD, BOLD), mtx(r"x^2+y^2+z^2\le R^2", 32, CYAN)).arrange(RIGHT, buff=0.20),
            VGroup(txt("2", 30, GOLD, BOLD), txt("Cố định", 25, INK), mtx(r"z=k", 32, BLUE), txt("để được", 25, INK), mtx(r"x^2+y^2\le R^2-k^2", 32, INK)).arrange(RIGHT, buff=0.18),
            VGroup(txt("3", 30, GOLD, BOLD), mtx(r"L_k=D(R^2-k^2)", 34, GREEN)).arrange(RIGHT, buff=0.20),
            VGroup(txt("4", 30, GOLD, BOLD), mtx(r"S(R)=\sum_{k=-R}^{R}L_k", 34, GOLD)).arrange(RIGHT, buff=0.20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        fit_width(steps, 11.5)
        for row in steps:
            self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.42)
        self.narrate(
            "Toàn bộ phương pháp chỉ có bốn bước. Viết điều kiện quả cầu. Cố định một tọa độ z để biến bài ba chiều thành một đĩa tròn hai chiều. Dùng công thức D để đếm điểm của lát đó. Cuối cùng cộng tất cả các lát từ âm R đến R. Nếu hiểu ý tưởng lát cắt, công thức tổng quát sẽ trở nên rất tự nhiên.",
            1.9,
        )

        self.clear_stage()
        title = txt("BÀI TẬP TỰ LUYỆN", 43, GOLD, BOLD)
        q1 = mtx(r"S(1)=?", 46, CYAN)
        q2 = mtx(r"S(4)=?", 46, CYAN)
        hint = txt("Hãy lập bảng theo |z| trước khi cộng.", 27, INK)
        group = VGroup(title, q1, q2, hint).arrange(DOWN, buff=0.34).shift(UP * 0.35)
        self.play(FadeIn(group), run_time=0.8)
        self.narrate(
            "Các em hãy tự luyện với R bằng một và R bằng bốn. Hãy lập bảng theo trị tuyệt đối của z, tính số điểm trên từng lát, rồi mới cộng. Dừng video ở đây nếu các em muốn tự làm trước.",
            1.6,
        )
        ans = mtx(r"\boxed{S(1)=7,\qquad S(4)=257}", 46, GREEN).shift(DOWN * 1.65)
        self.play(Write(ans), run_time=0.9)
        self.narrate(
            "Đáp số là bảy điểm với bán kính một và hai trăm năm mươi bảy điểm với bán kính bốn. Nếu các em ra đúng hai kết quả này, nghĩa là đã nắm chắc kỹ thuật lát cắt và cộng lớp.",
            1.4,
        )

        self.clear_stage()
        f = mtx(r"\boxed{S(R)=\sum_{z=-R}^{R}D(R^2-z^2)}", 47, GOLD)
        sub = txt("Một bài toán 3D được giải bằng nhiều bài toán 2D.", 30, INK, BOLD)
        brand = txt(TEN_THAY, 22, MUTED)
        end = VGroup(f, sub, brand).arrange(DOWN, buff=0.45)
        fit_width(end, 11.8)
        self.play(Write(f), run_time=1.0)
        self.play(FadeIn(sub), FadeIn(brand), run_time=0.6)
        self.narrate(
            "Ý tưởng đẹp nhất của bài hôm nay là giảm chiều: một quả cầu ba chiều được chia thành các đĩa tròn hai chiều. Ta giải từng lát bằng kiến thức cũ rồi cộng lại. Đây là một tư duy rất quan trọng trong toán học: chia một đối tượng phức tạp thành những phần đơn giản mà ta đã biết cách xử lý.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.general_problem()
        self.slicing_3d()
        self.disk_function()
        self.general_formula()
        self.example_r2()
        self.example_r3()
        self.example_r5()
        self.deeper()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "dem_diem_nguyen_qua_cau_R_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    # Math sanity checks before a long render.
    expected = {1: 7, 2: 33, 3: 123, 4: 257, 5: 515}
    for R, value in expected.items():
        got = sphere_count(R)
        if got != value:
            raise RuntimeError(f"Math check failed for R={R}: got {got}, expected {value}")
    if sphere_surface_count(5) != 30:
        raise RuntimeError("Math check failed for sphere surface R=5")

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Math checks: OK")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_sphere_lattice.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    # Verify both video and audio streams exist.
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
        "-of", "default=noprint_wrappers=1:nokey=1", str(final_path),
    ], text=True)
    if "video" not in probe or "audio" not in probe:
        raise RuntimeError("Final MP4 khong du video/audio stream")

    print("\n============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


if __name__ == "__main__":
    render_full()
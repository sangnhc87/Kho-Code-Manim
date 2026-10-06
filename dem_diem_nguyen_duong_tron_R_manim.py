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


def count_points(R):
    return sum(2 * math.isqrt(R * R - x * x) + 1 for x in range(-R, R + 1))


def ymax(R, x):
    return math.isqrt(R * R - x * x)

# ==========================================================
# TTS + MASTER AUDIO
# ==========================================================
def _audio_key(text):
    payload = json.dumps(
        {
            "text": text,
            "voice": GIONG_DOC,
            "rate": TOC_DO_DOC,
            "pitch": PITCH,
            "engine": "edge-tts",
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    out = subprocess.check_output(cmd, text=True).strip()
    return float(out)


def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError(f"Audio khong hop le: {path}")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
        check=True,
    )


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
    mix_labels = []
    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]adelay={ms}|{ms},aresample=48000[a{i}]")
        mix_labels.append(f"[a{i}]")

    filter_complex = (
        ";".join(filters)
        + ";"
        + "".join(mix_labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        *inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        "[m]",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-t",
        f"{video_duration:.3f}",
        str(out_wav),
    ]
    subprocess.run(cmd, check=True)


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out),
        ],
        check=True,
    )

# ==========================================================
# MAIN LESSON
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []

    # ---------- narration ----------
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
        if dur > rt:
            self.wait(dur - rt + min_hold)
        else:
            self.wait(min_hold)
        return dur

    # ---------- common ----------
    def clear_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.45)

    def add_header_footer(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, lines, voice, progress):
        self.clear_stage()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add_header_footer(title, "ĐỀ BÀI", progress)
        p = make_panel(12.35, 5.15).shift(DOWN * 0.10)
        self.play(FadeIn(p), run_time=0.5)
        line_mobs = VGroup()
        for i, line in enumerate(lines):
            if isinstance(line, Mobject):
                mob = line
            else:
                mob = fit_width(
                    txt(line, 28 if i == 0 else 26, INK if i == 0 else "#D8E7FF", BOLD if i == 0 else NORMAL),
                    11.2,
                )
            line_mobs.add(mob)
        line_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        line_mobs.move_to(p.get_center()).shift(UP * 0.06)
        for mob in line_mobs:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.32)
        self.narrate(voice, 2.0)
        return VGroup(p, line_mobs)

    # ---------- drawing helpers ----------
    def lattice_axes(self, R, length=6.1, shift=LEFT * 3.0):
        ax = Axes(
            x_range=[-R - 0.5, R + 0.5, 1],
            y_range=[-R - 0.5, R + 0.5, 1],
            x_length=length,
            y_length=length,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 28), mtx("y", 28))
        return ax, labels

    def circle_on_axes(self, ax, R, color=BLUE):
        return ParametricFunction(
            lambda t: ax.c2p(R * math.cos(t), R * math.sin(t)),
            t_range=[0, TAU],
            color=color,
            stroke_width=4,
        )

    def integer_points(self, ax, R, color=CYAN, radius=0.045):
        pts = []
        for x in range(-R, R + 1):
            for y in range(-R, R + 1):
                if x * x + y * y <= R * R:
                    pts.append(Dot(ax.c2p(x, y), radius=radius, color=color))
        return VGroup(*pts)

    # ======================================================
    # 1. INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        t1 = txt("ĐẾM SỐ ĐIỂM NGUYÊN", 48, GOLD, BOLD)
        t2 = txt("TRONG ĐƯỜNG TRÒN TÂM O, BÁN KÍNH R", 36, INK, BOLD)
        f = mtx(r"x^2+y^2\le R^2,\qquad R\in\mathbb N^*", 42, CYAN)
        s = txt("Từ đếm trực quan → công thức tổng quát → ứng dụng", 27, MUTED)
        brand = txt(TEN_THAY, 22, MUTED)
        g = VGroup(t1, t2, f, s, brand).arrange(DOWN, buff=0.28).move_to(ORIGIN)
        self.play(FadeIn(t1, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(t2), Write(f), run_time=1.2)
        self.play(FadeIn(s), FadeIn(brand), run_time=0.5)
        self.narrate(
            "Chào các em. Hôm nay chúng ta sẽ cùng giải một bài toán rất đẹp: đếm số điểm có cả hai tọa độ nguyên nằm trong hoặc trên một đường tròn tâm O, bán kính R là số tự nhiên. Thầy sẽ không đưa công thức ngay. Chúng ta sẽ bắt đầu bằng việc nhìn hình, đếm thật chậm, rồi tự xây dựng công thức tổng quát. Sau đó các em sẽ áp dụng công thức vào những bài cụ thể và hiểu vì sao diện tích pi R bình phương chỉ là một giá trị gần đúng, chứ không phải số điểm nguyên chính xác.",
            2.5,
        )

    # ======================================================
    # 2. GENERAL PROBLEM
    # ======================================================
    def general_problem(self):
        self.show_problem(
            "Bài toán tổng quát",
            [
                "Cho đường tròn tâm O trùng gốc tọa độ, bán kính R là số tự nhiên dương.",
                mtx(r"(C):\ x^2+y^2=R^2", 36, BLUE),
                mtx(r"(x,y)\in\mathbb Z^2", 36, CYAN),
                "Hỏi có bao nhiêu điểm nguyên nằm trong hoặc trên đường tròn?",
                mtx(r"x^2+y^2\le R^2", 38, GOLD),
            ],
            "Ta phát biểu bài toán thật rõ. Đường tròn có tâm là gốc tọa độ O, bán kính R là một số tự nhiên dương. Ta cần đếm tất cả các điểm M có tọa độ x và y đều là số nguyên, sao cho x bình phương cộng y bình phương nhỏ hơn hoặc bằng R bình phương. Dấu nhỏ hơn hoặc bằng rất quan trọng, vì các điểm nằm đúng trên đường tròn cũng được tính.",
            "Phần 1/8",
        )

        self.clear_stage()
        self.add_header_footer("Ba điều cần nhìn thấy", "Trước khi đếm", "Phần 1/8")
        items = VGroup(
            VGroup(mtx(r"x\in\mathbb Z", 34, CYAN), txt("→ chỉ xét các cột có hoành độ nguyên", 27, INK)).arrange(RIGHT, buff=0.25),
            VGroup(mtx(r"y\in\mathbb Z", 34, CYAN), txt("→ trên mỗi cột chỉ lấy tung độ nguyên", 27, INK)).arrange(RIGHT, buff=0.25),
            VGroup(mtx(r"x^2+y^2\le R^2", 34, GOLD), txt("→ điểm phải nằm trong đĩa tròn", 27, INK)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).shift(DOWN * 0.1)
        for row in items:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.45)
        self.narrate(
            "Có ba ý các em phải giữ thật chắc. Một, x chỉ nhận giá trị nguyên. Hai, y cũng chỉ nhận giá trị nguyên. Ba, cặp x y phải thỏa bất đẳng thức của đĩa tròn. Vì vậy thay vì nhìn cả mặt phẳng cùng một lúc, ta sẽ chia bài toán thành từng cột thẳng đứng có hoành độ nguyên. Đây là ý tưởng quan trọng nhất của cả video.",
            2.0,
        )

    # ======================================================
    # 3. WARM-UP R=2
    # ======================================================
    def warmup_r2(self):
        self.clear_stage()
        self.add_header_footer("Khởi động với R = 2", "Đếm bằng mắt trước khi dùng công thức", "Phần 2/8")
        ax, labels = self.lattice_axes(2, length=5.8, shift=LEFT * 3.2)
        circle = self.circle_on_axes(ax, 2)
        grid_dots = VGroup(*[
            Dot(ax.c2p(x, y), radius=0.025, color=MUTED).set_opacity(0.5)
            for x in range(-2, 3) for y in range(-2, 3)
        ])
        pts = self.integer_points(ax, 2, CYAN, 0.06)
        eq = mtx(r"x^2+y^2\le4", 39, GOLD).shift(RIGHT * 3.4 + UP * 2.0)
        count = mtx(r"N(2)=?", 46, INK).next_to(eq, DOWN, buff=0.35)
        self.play(Create(ax), FadeIn(labels), run_time=0.8)
        self.play(Create(circle), FadeIn(grid_dots), Write(eq), run_time=1.0)
        self.narrate(
            "Ta bắt đầu với bán kính bằng hai. Khi đó điều kiện trở thành x bình phương cộng y bình phương nhỏ hơn hoặc bằng bốn. Trên hình, mỗi chấm nhỏ là một vị trí có tọa độ nguyên. Việc của chúng ta là chọn đúng những chấm nằm trong hoặc nằm trên đường tròn.",
            1.8,
        )
        self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.04), run_time=2.0)
        self.play(Write(count), run_time=0.5)

        rows = VGroup(
            VGroup(mtx(r"x=-2:\ y=0", 31, INK), txt("→ 1 điểm", 24, GREEN)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"x=-1:\ y=-1,0,1", 31, INK), txt("→ 3 điểm", 24, GREEN)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"x=0:\ y=-2,-1,0,1,2", 31, INK), txt("→ 5 điểm", 24, GREEN)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"x=1", 31, INK), txt("→ 3 điểm", 24, GREEN)).arrange(RIGHT, buff=0.22),
            VGroup(mtx(r"x=2", 31, INK), txt("→ 1 điểm", 24, GREEN)).arrange(RIGHT, buff=0.22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(RIGHT * 3.3 + DOWN * 0.45)
        fit_width(rows, 6.0)
        self.play(FadeIn(rows, shift=RIGHT * 0.12), run_time=0.8)
        ans = mtx(r"\boxed{N(2)=1+3+5+3+1=13}", 38, GOLD).to_edge(DOWN, buff=0.65).shift(RIGHT * 2.2)
        self.play(Write(ans), run_time=1.0)
        self.narrate(
            "Bây giờ đếm theo từng cột. Ở x bằng âm hai chỉ có y bằng không, nên được một điểm. Ở x bằng âm một có ba điểm. Ở x bằng không có năm điểm. Sau đó do đối xứng, x bằng một có ba điểm và x bằng hai có một điểm. Tổng cộng là mười ba điểm. Cách đếm theo cột này chính là chiếc cầu dẫn tới công thức tổng quát.",
            2.2,
        )

    # ======================================================
    # 4. DERIVE ONE COLUMN
    # ======================================================
    def derive_column(self):
        self.clear_stage()
        self.add_header_footer("Một cột có bao nhiêu điểm?", "Cố định hoành độ x = k", "Phần 3/8")
        panel = make_panel(11.8, 5.0).shift(DOWN * 0.05)
        self.play(FadeIn(panel), run_time=0.5)

        e1 = mtx(r"k^2+y^2\le R^2", 43, INK)
        e2 = mtx(r"y^2\le R^2-k^2", 43, INK)
        e3 = mtx(r"-\sqrt{R^2-k^2}\le y\le\sqrt{R^2-k^2}", 40, CYAN)
        e4 = mtx(r"m_k=\left\lfloor\sqrt{R^2-k^2}\right\rfloor", 41, ORANGE)
        e5 = mtx(r"y=-m_k,-m_k+1,\ldots,0,\ldots,m_k", 37, INK)
        e6 = mtx(r"\boxed{c_k=2m_k+1=2\left\lfloor\sqrt{R^2-k^2}\right\rfloor+1}", 39, GOLD)
        grp = VGroup(e1, e2, e3, e4, e5, e6).arrange(DOWN, buff=0.28).move_to(panel)
        fit_width(grp, 10.8)

        self.play(Write(e1), run_time=0.7)
        self.narrate(
            "Ta cố định một hoành độ nguyên x bằng k. Khi đó k bình phương cộng y bình phương nhỏ hơn hoặc bằng R bình phương. Chuyển vế, ta được y bình phương nhỏ hơn hoặc bằng R bình phương trừ k bình phương.",
            1.6,
        )
        self.play(TransformMatchingTex(e1.copy(), e2), run_time=0.8)
        self.play(Write(e3), run_time=0.9)
        self.narrate(
            "Suy ra y nằm từ âm căn R bình phương trừ k bình phương đến dương căn R bình phương trừ k bình phương. Nhưng y phải là số nguyên. Vì vậy số nguyên lớn nhất mà độ lớn của y có thể đạt tới chính là phần nguyên của căn đó.",
            1.8,
        )
        self.play(Write(e4), run_time=0.8)
        self.play(Write(e5), run_time=0.8)
        self.narrate(
            "Gọi m k là phần nguyên của căn R bình phương trừ k bình phương. Khi đó y chạy từ âm m k đến dương m k. Ta có m k số âm, một số không, và m k số dương. Vì vậy tổng số điểm trên cột x bằng k là hai m k cộng một.",
            1.8,
        )
        self.play(Write(e6), run_time=1.0)
        self.narrate(
            "Đây là công thức quan trọng nhất của bài: số điểm nguyên trên cột x bằng k bằng hai lần phần nguyên của căn R bình phương trừ k bình phương, rồi cộng một.",
            1.4,
        )

    # ======================================================
    # 5. GENERAL FORMULA
    # ======================================================
    def general_formula(self):
        self.clear_stage()
        self.add_header_footer("Công thức tổng quát chính xác", "Cộng tất cả các cột nguyên", "Phần 4/8")
        f1 = mtx(r"-R\le x\le R,\qquad x\in\mathbb Z", 38, CYAN)
        f2 = mtx(r"c_x=2\left\lfloor\sqrt{R^2-x^2}\right\rfloor+1", 40, INK)
        f3 = mtx(r"\boxed{N(R)=\sum_{x=-R}^{R}\left(2\left\lfloor\sqrt{R^2-x^2}\right\rfloor+1\right)}", 42, GOLD)
        g = VGroup(f1, f2, f3).arrange(DOWN, buff=0.55).shift(UP * 0.3)
        fit_width(g, 12.0)
        self.play(Write(f1), run_time=0.8)
        self.play(Write(f2), run_time=0.8)
        self.narrate(
            "Hoành độ x chỉ có thể chạy từ âm R đến R, bởi vì nếu độ lớn của x lớn hơn R thì riêng x bình phương đã vượt quá R bình phương. Với mỗi x nguyên, ta đã biết chính xác số điểm trên cột đó. Vì vậy chỉ cần cộng số điểm của tất cả các cột.",
            1.8,
        )
        self.play(Write(f3), run_time=1.2)
        self.narrate(
            "Ta thu được công thức tổng quát chính xác. Công thức có một tổng hữu hạn và hàm phần nguyên. Với mỗi bán kính nguyên R, công thức này cho đúng số điểm nguyên nằm trong hoặc trên đường tròn.",
            1.8,
        )

        note = VGroup(
            txt("Không nhầm với diện tích hình tròn:", 28, MUTED),
            mtx(r"\pi R^2", 39, ORANGE),
            txt("là diện tích liên tục, không phải số điểm nguyên.", 27, MUTED),
        ).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.72)
        fit_width(note, 11.8)
        self.play(FadeIn(note), run_time=0.5)
        self.narrate(
            "Các em đặc biệt không được lấy pi R bình phương rồi coi đó là số điểm. Pi R bình phương là diện tích của miền liên tục. Còn ở đây chúng ta đang đếm các điểm rời rạc có tọa độ nguyên. Hai đại lượng có liên hệ gần đúng khi R lớn, nhưng không giống nhau.",
            1.8,
        )

    # ======================================================
    # 6. SYMMETRY FORMULA
    # ======================================================
    def symmetry_formula(self):
        self.clear_stage()
        self.add_header_footer("Khai thác đối xứng", "Đếm một phần tư rồi nhân 4", "Phần 5/8")
        ax, labels = self.lattice_axes(5, length=5.8, shift=LEFT * 3.2)
        circle = self.circle_on_axes(ax, 5)
        axes_points = VGroup()
        quad_points = VGroup()
        for x in range(-5, 6):
            for y in range(-5, 6):
                if x*x + y*y <= 25:
                    if x == 0 or y == 0:
                        axes_points.add(Dot(ax.c2p(x, y), radius=0.04, color=GOLD))
                    elif x > 0 and y > 0:
                        quad_points.add(Dot(ax.c2p(x, y), radius=0.045, color=CYAN))
        self.play(Create(ax), FadeIn(labels), Create(circle), run_time=1.0)
        self.play(FadeIn(axes_points), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(p) for p in quad_points], lag_ratio=0.03), run_time=1.5)

        formulas = VGroup(
            mtx(r"1", 34, INK),
            mtx(r"+\ 4R", 34, GOLD),
            mtx(r"+\ 4\sum_{x=1}^{R-1}\left\lfloor\sqrt{R^2-x^2}\right\rfloor", 34, CYAN),
        ).arrange(RIGHT, buff=0.12).shift(RIGHT * 3.15 + UP * 1.5)
        caption = VGroup(
            txt("gốc O", 24, INK),
            txt("các điểm trên 4 nửa trục", 24, GOLD),
            txt("4 góc phần tư", 24, CYAN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(formulas, DOWN, buff=0.35)
        boxed = mtx(r"\boxed{N(R)=1+4R+4\sum_{x=1}^{R-1}\left\lfloor\sqrt{R^2-x^2}\right\rfloor}", 37, GOLD).shift(RIGHT * 2.9 + DOWN * 1.7)
        fit_width(boxed, 6.3)
        self.play(Write(formulas), FadeIn(caption), run_time=1.0)
        self.narrate(
            "Do đường tròn tâm O đối xứng qua hai trục tọa độ, ta có một cách viết gọn hơn. Điểm O được tính một lần. Trên bốn nửa trục có tổng cộng bốn R điểm khác O. Còn trong góc phần tư thứ nhất, với x chạy từ một đến R trừ một, số tung độ nguyên dương là phần nguyên của căn R bình phương trừ x bình phương. Bốn góc phần tư có số điểm như nhau.",
            2.0,
        )
        self.play(Write(boxed), run_time=1.2)
        self.narrate(
            "Vì vậy ta có công thức đối xứng: một cộng bốn R, cộng bốn lần tổng phần nguyên trong góc phần tư thứ nhất. Hai công thức là hoàn toàn tương đương. Khi tính tay, dạng đối xứng thường ngắn hơn.",
            1.8,
        )

    # ======================================================
    # 7. DETAILED EXAMPLE R=5
    # ======================================================
    def example_r5(self):
        self.show_problem(
            "Ví dụ áp dụng: R = 5",
            [
                "Đếm số điểm nguyên nằm trong hoặc trên đường tròn:",
                mtx(r"x^2+y^2\le25", 40, GOLD),
                mtx(r"(x,y)\in\mathbb Z^2", 36, CYAN),
                "Giải bằng phương pháp đếm theo cột và kiểm tra bằng đối xứng.",
            ],
            "Bây giờ ta áp dụng thật chậm với bán kính bằng năm. Ta cần đếm các điểm nguyên thỏa x bình phương cộng y bình phương nhỏ hơn hoặc bằng hai mươi lăm. Thầy sẽ làm theo hai cách: trước hết đếm theo cột, sau đó kiểm tra lại bằng công thức đối xứng.",
            "Phần 6/8",
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ R = 5", "Bước 1: lập bảng theo |x|", "Phần 6/8")
        headers = VGroup(
            mtx(r"|x|", 30, GOLD),
            mtx(r"\left\lfloor\sqrt{25-x^2}\right\rfloor", 30, GOLD),
            mtx(r"c_x=2m+1", 30, GOLD),
        ).arrange(RIGHT, buff=0.9).shift(UP * 2.15)
        fit_width(headers, 10.6)
        self.play(FadeIn(headers), run_time=0.5)

        data = [(0,5,11),(1,4,9),(2,4,9),(3,4,9),(4,3,7),(5,0,1)]
        rows = VGroup()
        for x,m,c in data:
            row = VGroup(
                mtx(str(x), 30, INK),
                mtx(str(m), 30, CYAN),
                mtx(str(c), 30, GREEN),
            ).arrange(RIGHT, buff=2.25)
            rows.add(row)
        rows.arrange(DOWN, buff=0.24).shift(DOWN * 0.15)
        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.12), run_time=0.32)
        self.narrate(
            "Ta chỉ cần xét trị tuyệt đối của x từ không đến năm. Với x bằng không, căn hai mươi lăm bằng năm, nên có mười một giá trị y từ âm năm đến năm. Với x bằng một, phần nguyên của căn hai mươi bốn là bốn, nên có chín điểm. x bằng hai cũng có chín điểm. x bằng ba có căn mười sáu bằng bốn, nên vẫn có chín điểm. x bằng bốn cho ba, nên có bảy điểm. Và x bằng năm chỉ còn y bằng không, tức một điểm.",
            2.2,
        )

        self.clear_stage()
        self.add_header_footer("Ví dụ R = 5", "Bước 2: cộng các cột đối xứng", "Phần 6/8")
        e1 = mtx(r"N(5)=c_0+2(c_1+c_2+c_3+c_4+c_5)", 40, INK)
        e2 = mtx(r"=11+2(9+9+9+7+1)", 40, CYAN)
        e3 = mtx(r"=11+70", 42, CYAN)
        e4 = mtx(r"\boxed{N(5)=81}", 48, GOLD)
        grp = VGroup(e1,e2,e3,e4).arrange(DOWN,buff=0.42).shift(UP*0.15)
        for e in grp:
            self.play(Write(e), run_time=0.65)
        self.narrate(
            "Bây giờ cộng. Cột x bằng không chỉ xuất hiện một lần. Các cột x bằng một đến năm có cột đối xứng ở phía âm, nên ta nhân đôi. Mười một cộng hai lần tổng chín cộng chín cộng chín cộng bảy cộng một bằng tám mươi mốt. Vậy có đúng tám mươi mốt điểm nguyên.",
            1.8,
        )

        check = mtx(r"1+4\cdot5+4(4+4+4+3)=81", 38, GREEN).next_to(e4, DOWN, buff=0.45)
        self.play(Write(check), run_time=0.8)
        self.narrate(
            "Kiểm tra bằng công thức đối xứng: một điểm ở gốc, hai mươi điểm trên bốn nửa trục, và trong một góc phần tư có bốn cộng bốn cộng bốn cộng ba bằng mười lăm điểm. Nhân bốn rồi cộng lại, ta vẫn được tám mươi mốt. Hai cách khớp nhau.",
            1.8,
        )

    # ======================================================
    # 8. 3D VISUALIZATION
    # ======================================================
    def visualization_3d(self):
        self.clear_stage()
        self.set_camera_orientation(phi=62 * DEGREES, theta=-45 * DEGREES, zoom=0.9)

        fixed_title = title_block("Trực quan 3D", "Biến mỗi cột điểm thành một cột chiều cao")
        fixed_footer = footer("Phần 7/8")
        self.add_fixed_in_frame_mobjects(fixed_title, fixed_footer)

        ax3 = ThreeDAxes(
            x_range=[-5,5,1],
            y_range=[-5,5,1],
            z_range=[0,12,2],
            x_length=7.0,
            y_length=7.0,
            z_length=4.8,
            axis_config={"color": MUTED, "stroke_width": 2},
        ).shift(DOWN * 0.4)
        circle3 = ParametricFunction(
            lambda t: ax3.c2p(5*math.cos(t),5*math.sin(t),0),
            t_range=[0,TAU],
            color=BLUE,
            stroke_width=4,
        )
        pts3 = VGroup()
        for x in range(-5,6):
            for y in range(-5,6):
                if x*x+y*y <= 25:
                    pts3.add(Dot3D(ax3.c2p(x,y,0), radius=0.035, color=CYAN))

        self.play(Create(ax3), Create(circle3), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(p, scale=1.4) for p in pts3], lag_ratio=0.006), run_time=2.2)
        self.begin_ambient_camera_rotation(rate=0.06)
        self.narrate(
            "Bây giờ ta đổi góc nhìn sang ba chiều để thấy cấu trúc của phép đếm. Tám mươi mốt điểm vẫn nằm trên mặt phẳng z bằng không. Khi camera nghiêng xuống, ta nhìn thấy rất rõ các điểm được xếp thành những cột thẳng đứng theo từng giá trị x. Cột ở giữa cao nhất, rồi số điểm giảm dần khi tiến ra gần biên đường tròn.",
            2.0,
        )
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(pts3), FadeOut(circle3), run_time=0.7)

        bars = VGroup()
        for x in range(-5,6):
            c = 2*ymax(5,x)+1
            h_scene = c * (4.8/12.0)
            bar = Prism(dimensions=[0.43,0.65,h_scene])
            bar.set_fill(CYAN if x != 0 else GOLD, opacity=0.78)
            bar.set_stroke(INK, width=0.6, opacity=0.35)
            bar.move_to(ax3.c2p(x,0,c/2))
            bars.add(bar)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), run_time=2.5)

        formula = mtx(r"N(5)=\sum_{x=-5}^{5}c_x=81", 38, GOLD).to_edge(DOWN, buff=0.75)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula), run_time=0.8)
        self.begin_ambient_camera_rotation(rate=-0.05)
        self.narrate(
            "Ta có thể thay mỗi cột điểm bằng một thanh ba chiều có chiều cao đúng bằng số điểm trên cột đó. Khi ấy bài toán đếm tám mươi mốt điểm trở thành việc cộng chiều cao của mười một thanh, từ x bằng âm năm đến x bằng năm. Đây không phải là một cách giải mới, mà là một hình ảnh ba chiều giúp chúng ta nhìn thấy công thức tổng theo cột một cách trực quan hơn.",
            2.2,
        )
        self.stop_ambient_camera_rotation()

        # Return to 2D camera
        self.play(FadeOut(bars), FadeOut(ax3), run_time=0.6)
        self.remove_fixed_in_frame_mobjects(fixed_title, fixed_footer, formula)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

    # ======================================================
    # 9. APPLICATIONS + AREA COMPARISON
    # ======================================================
    def applications(self):
        self.clear_stage()
        self.add_header_footer("Ứng dụng 1: mạng cảm biến", "Một mô hình đếm điểm nguyên thực tế", "Phần 8/8")
        p = make_panel(12.2,5.1).shift(DOWN*0.1)
        self.play(FadeIn(p),run_time=0.5)
        lines = VGroup(
            txt("Một khu thử nghiệm đặt cảm biến tại các nút lưới cách nhau 1 m.",27,INK),
            txt("Chỉ các nút cách trạm O không quá 5 m được kích hoạt.",27,INK),
            mtx(r"x^2+y^2\le25,\qquad (x,y)\in\mathbb Z^2",38,CYAN),
            VGroup(mtx(r"\boxed{81}",40,GOLD), txt("cảm biến được kích hoạt",26,GOLD,BOLD)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,buff=0.38).move_to(p)
        fit_width(lines,11.1)
        for m in lines:self.play(FadeIn(m,shift=UP*0.08),run_time=0.4)
        self.narrate(
            "Một ứng dụng rất tự nhiên là mạng cảm biến đặt trên lưới vuông, mỗi nút cách nhau một mét. Nếu trạm trung tâm chỉ kích hoạt những cảm biến cách O không quá năm mét, thì mỗi cảm biến tương ứng với một điểm nguyên trong đĩa bán kính năm. Vì vậy kết quả tám mươi mốt có thể được hiểu ngay là tám mươi mốt cảm biến được kích hoạt.",
            1.8,
        )

        self.clear_stage()
        self.add_header_footer("Ứng dụng 2: so sánh với diện tích", "Vì sao πR² chỉ là gần đúng?", "Phần 8/8")
        a1=mtx(r"N(5)=81",44,GOLD)
        a2=mtx(r"\pi\cdot5^2=25\pi\approx78.54",42,ORANGE)
        a3=mtx(r"81-25\pi\approx2.46",40,CYAN)
        a4=txt("Số điểm nguyên là đại lượng rời rạc; diện tích là đại lượng liên tục.",28,MUTED)
        g=VGroup(a1,a2,a3,a4).arrange(DOWN,buff=0.42).shift(UP*0.1)
        for m in g:self.play(FadeIn(m) if isinstance(m,Text) else Write(m),run_time=0.65)
        self.narrate(
            "Với R bằng năm, số điểm chính xác là tám mươi mốt. Trong khi diện tích hình tròn là hai mươi lăm pi, xấp xỉ bảy mươi tám phẩy năm tư. Hai số khá gần nhau nhưng không bằng nhau. Khi R tăng lớn, số điểm nguyên thường gần pi R bình phương, nhưng sai lệch ở vùng biên vẫn tồn tại. Bài toán nghiên cứu sâu sai lệch này chính là một bài toán nổi tiếng trong toán học, thường được gọi là bài toán đường tròn Gauss.",
            2.2,
        )

        self.clear_stage()
        self.add_header_footer("Mở rộng: điểm trên biên và điểm bên trong", "R = 5", "Phần 8/8")
        b1=mtx(r"x^2+y^2=25",40,BLUE)
        b2=mtx(r"(\pm5,0),(0,\pm5),(\pm3,\pm4),(\pm4,\pm3)",36,CYAN)
        b3=mtx(r"B(5)=12",42,GOLD)
        b4=mtx(r"I(5)=N(5)-B(5)=81-12=69",42,GREEN)
        bg=VGroup(b1,b2,b3,b4).arrange(DOWN,buff=0.42)
        fit_width(bg,11.5)
        for m in bg:self.play(Write(m),run_time=0.7)
        self.narrate(
            "Ta còn có thể tách riêng các điểm nằm đúng trên đường tròn. Với R bằng năm, phương trình x bình phương cộng y bình phương bằng hai mươi lăm có các nghiệm nguyên tạo bởi bộ ba bốn năm và các điểm trên hai trục. Tổng cộng có mười hai điểm biên. Vì toàn bộ đĩa có tám mươi mốt điểm, nên số điểm nằm nghiêm ngặt bên trong là sáu mươi chín.",
            1.9,
        )

    # ======================================================
    # 10. SUMMARY
    # ======================================================
    def summary(self):
        self.clear_stage()
        self.add_header_footer("Chốt lại phương pháp", "4 bước để đếm điểm nguyên trong đường tròn", "Tổng kết")
        steps = VGroup(
            VGroup(txt("1",30,GOLD,BOLD), mtx(r"x^2+y^2\le R^2",32,CYAN), txt("và xác định",25,INK), mtx(r"-R\le x\le R",32,INK)).arrange(RIGHT,buff=0.18),
            VGroup(txt("2",30,GOLD,BOLD), txt("Cố định",25,INK), mtx(r"x=k",32,CYAN), txt("rồi tìm",25,INK), mtx(r"|y|\le\sqrt{R^2-k^2}",32,INK)).arrange(RIGHT,buff=0.18),
            VGroup(txt("3",30,GOLD,BOLD), txt("Số điểm trên cột:",25,INK), mtx(r"2\lfloor\sqrt{R^2-k^2}\rfloor+1",32,GREEN)).arrange(RIGHT,buff=0.18),
            VGroup(txt("4",30,GOLD,BOLD), txt("Cộng các cột hoặc dùng đối xứng.",25,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.42).shift(DOWN*0.15)
        fit_width(steps,11.6)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.42)
        self.narrate(
            "Các em chỉ cần nhớ bốn bước. Một, viết điều kiện của đĩa tròn và xác định x chạy từ âm R đến R. Hai, cố định một hoành độ x bằng k. Ba, dùng hàm phần nguyên để đếm chính xác số giá trị y trên cột đó. Bốn, cộng tất cả các cột, hoặc khai thác đối xứng để giảm khối lượng tính toán. Nếu hiểu được bốn bước này, công thức tổng quát sẽ không còn là thứ phải học thuộc.",
            2.0,
        )

        self.clear_stage()
        t=txt("BÀI TẬP TỰ LUYỆN",42,GOLD,BOLD)
        q1=mtx(r"N(3)=?",48,CYAN)
        q2=mtx(r"N(4)=?",48,CYAN)
        q3=txt("Hãy tính bằng công thức cột, rồi kiểm tra bằng đối xứng.",27,INK)
        ans=mtx(r"N(3)=29,\qquad N(4)=49",42,GREEN)
        g=VGroup(t,q1,q2,q3).arrange(DOWN,buff=0.34).shift(UP*0.3)
        self.play(FadeIn(g),run_time=0.8)
        self.narrate(
            "Trước khi kết thúc, các em hãy tự tính N của ba và N của bốn. Hãy tạm dừng video, lập bảng theo từng cột, sau đó kiểm tra lại bằng đối xứng. Khi đã làm xong, các em có thể đối chiếu đáp số.",
            1.6,
        )
        self.play(Write(ans),run_time=1.0)
        self.narrate(
            "Đáp số là N của ba bằng hai mươi chín và N của bốn bằng bốn mươi chín. Nếu các em ra đúng hai kết quả này, nghĩa là đã nắm rất chắc phương pháp.",
            1.3,
        )

        self.clear_stage()
        main = mtx(r"\boxed{N(R)=\sum_{x=-R}^{R}\left(2\left\lfloor\sqrt{R^2-x^2}\right\rfloor+1\right)}", 41, GOLD)
        sub = txt("Đừng học thuộc trước khi hiểu cách đếm từng cột.",29,INK,BOLD)
        brand=txt(TEN_THAY,22,MUTED)
        gg=VGroup(main,sub,brand).arrange(DOWN,buff=0.45)
        fit_width(gg,12.0)
        self.play(Write(main),run_time=1.2)
        self.play(FadeIn(sub),FadeIn(brand),run_time=0.6)
        self.narrate(
            "Công thức cuối cùng rất đẹp, nhưng điều quan trọng hơn công thức là ý tưởng: chia đĩa tròn thành các cột nguyên, đếm từng cột, rồi cộng lại. Khi hiểu ý tưởng đó, các em có thể tự xây dựng lại công thức bất cứ lúc nào. Hẹn gặp các em ở bài tiếp theo.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.general_problem()
        self.warmup_r2()
        self.derive_column()
        self.general_formula()
        self.symmetry_formula()
        self.example_r5()
        self.visualization_3d()
        self.applications()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "dem_diem_nguyen_duong_tron_R_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_circle_lattice.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    print("\n============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


if __name__ == "__main__":
    render_full()

from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time

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


def make_panel(width=12.2, height=5.3):
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
        s = fit_width(txt(subtitle, 23, MUTED), 11.7).next_to(t, DOWN, buff=0.10)
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
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ]
    return float(subprocess.check_output(cmd, text=True).strip())


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

    inputs, filters, labels = [], [], []
    for i, (start, path) in enumerate(events):
        inputs += ["-i", str(path)]
        ms = max(0, int(round(start * 1000)))
        filters.append(f"[{i}:a]adelay={ms}|{ms},aresample=48000[a{i}]")
        labels.append(f"[a{i}]")

    filter_complex = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[m]", "-ar", "48000", "-ac", "2",
        "-t", f"{video_duration:.3f}", str(out_wav)
    ], check=True)


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(out)
    ], check=True)

# ==========================================================
# LESSON
# ==========================================================
class SangLesson(Scene):
    def setup(self):
        self.audio_events = []

    # ---------- audio ----------
    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    # ---------- layout ----------
    def clear_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.42)

    def add_header_footer(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, content, voice, progress):
        self.clear_stage()
        self.add_header_footer(title, "ĐỀ BÀI", progress)
        panel = make_panel(12.3, 5.15).shift(DOWN * 0.08)
        self.play(FadeIn(panel), run_time=0.45)
        group = VGroup()
        for item in content:
            if isinstance(item, Mobject):
                mob = item
            else:
                mob = fit_width(txt(item, 27, INK), 11.1)
            group.add(mob)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(panel)
        fit_width(group, 11.15)
        for mob in group:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.30)
        self.narrate(voice, 2.0)
        return VGroup(panel, group)

    def make_axes(self, xr=(-5, 6, 1), yr=(-5, 8, 1), xlen=6.7, ylen=5.2, shift=LEFT*2.55):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 22},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 27), mtx("y", 27))
        return ax, labels

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        t1 = txt("6 VIÊN NGỌC CỦA HÀM SỐ", 47, GOLD, BOLD)
        t2 = txt("BÀI TOÁN KHÓ NHÌN — LỜI GIẢI LẠI RẤT NGẮN", 32, INK, BOLD)
        f = VGroup(
            txt("Cấu trúc", 29, BLUE, BOLD),
            mtx(r"\Longrightarrow", 38, MUTED),
            txt("lời giải gọn", 29, GOLD, BOLD),
        ).arrange(RIGHT, buff=0.30)
        note = txt("Tiếp tuyến • đối xứng • hàm ngược • đơn điệu • cực trị", 27, CYAN)
        brand = txt(TEN_THAY, 22, MUTED)
        g = VGroup(t1, t2, f, note, brand).arrange(DOWN, buff=0.28)
        self.play(FadeIn(t1, shift=UP*0.2), run_time=0.6)
        self.play(FadeIn(t2), Write(f), run_time=1.0)
        self.play(FadeIn(note), FadeIn(brand), run_time=0.5)
        self.narrate(
            "Chào các em. Video hôm nay không phải một chương lý thuyết thông thường. Thầy chọn sáu bài toán có vẻ khá khó, thậm chí hơi lạ khi mới nhìn, nhưng khi nhận ra đúng cấu trúc thì lời giải chỉ còn vài dòng. Mục tiêu quan trọng nhất là học cách nhìn: khi nào nên dùng trung điểm, khi nào nên đổi tâm, khi nào tiếp tuyến ẩn một bất biến, và khi nào một phương trình lồng hàm có thể sụp xuống thành một phương trình rất đơn giản.",
            2.3,
        )

        self.clear_stage(); self.add_header_footer("Tinh thần của chuyên đề", "Đừng lao vào tính trước khi nhìn cấu trúc", "Mở đầu")
        rows = VGroup(
            bullet("Bài dài chưa chắc cần lời giải dài.", INK, 27, BLUE),
            bullet("Một phép biến đổi đúng có thể lộ ra đối xứng ngay lập tức.", INK, 27, CYAN),
            bullet("Một tiếp tuyến đôi khi mang theo trung điểm và diện tích bất biến.", INK, 27, GREEN),
            bullet("Đơn điệu có thể loại cả một tầng hàm hợp.", INK, 27, ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT*0.12), run_time=0.36)
        self.narrate(
            "Các em hãy để ý một điều. Những lời giải đẹp thường không cố tính tất cả. Chúng tìm ra đại lượng trung tâm rồi bỏ qua phần thừa. Vì thế trong mỗi bài, thầy sẽ cố tình cho các em nhìn thấy cách làm dài trước, sau đó chỉ ra một cấu trúc giúp rút gọn mạnh. Đó chính là thứ đáng mang theo sau khi xem video.",
            1.8,
        )

    # ======================================================
    # GEM 1 - QUADRATIC CHORD
    # ======================================================
    def gem1_quadratic_chord(self):
        self.show_problem(
            "Viên ngọc 1 – Dây cung và đạo hàm",
            [
                mtx(r"f(x)=ax^2+bx+c,\qquad a\ne0", 40, GOLD),
                "Hai điểm A, B bất kỳ trên parabol có hoành độ x₁, x₂.",
                "Có một điểm đặc biệt mà tiếp tuyến song song với dây AB. Tìm điểm đó.",
            ],
            "Cho một parabol bất kỳ và hai điểm A, B trên đồ thị. Theo định lý giá trị trung bình, ta biết đâu đó giữa A và B có một tiếp tuyến song song với dây AB. Nhưng với parabol, điều kỳ lạ là ta biết chính xác điểm ấy mà không cần giải phương trình phức tạp.",
            "Viên ngọc 1/6",
        )

        self.clear_stage(); self.add_header_footer("Viên ngọc 1", "Độ dốc dây cung bằng đạo hàm tại trung điểm hoành độ", "Viên ngọc 1/6")
        deriv = VGroup(
            mtx(r"k_{AB}=\frac{f(x_2)-f(x_1)}{x_2-x_1}", 37, INK),
            mtx(r"=\frac{a(x_2^2-x_1^2)+b(x_2-x_1)}{x_2-x_1}", 35, CYAN),
            mtx(r"=a(x_1+x_2)+b", 39, GREEN),
            mtx(r"x_M=\frac{x_1+x_2}{2}", 37, BLUE),
            mtx(r"f'(x_M)=2a\cdot\frac{x_1+x_2}{2}+b", 35, CYAN),
            mtx(r"\boxed{k_{AB}=f'\!\left(\frac{x_1+x_2}{2}\right)}", 43, GOLD),
        ).arrange(DOWN, buff=0.26).shift(LEFT*2.7)
        fit_width(deriv, 7.4)
        side = VGroup(
            txt("Không cần tìm điểm ξ bằng định lý tồn tại.", 24, MUTED),
            txt("Với parabol, ξ chính là trung điểm", 24, INK),
            mtx(r"\xi=\frac{x_1+x_2}{2}", 36, GOLD),
        ).arrange(DOWN, buff=0.22).to_edge(RIGHT, buff=0.45)
        self.play(FadeIn(deriv), FadeIn(side), run_time=1.0)
        self.narrate(
            "Ta tính hệ số góc của dây A B. Hiệu hai bình phương tách được thành x hai trừ x một nhân x hai cộng x một, nên sau khi rút gọn, hệ số góc bằng a nhân x một cộng x hai rồi cộng b. Bây giờ lấy trung điểm hoành độ, x M bằng trung bình cộng của x một và x hai. Đạo hàm tại đó cũng đúng bằng a nhân x một cộng x hai cộng b. Vậy với mọi parabol, tiếp tuyến tại điểm có hoành độ là trung bình cộng của hai đầu dây luôn song song với dây ấy.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Nhìn trên hình", "Một định lý giá trị trung bình chính xác", "Viên ngọc 1/6")
        ax, labels = self.make_axes(xr=(-2,6,1), yr=(-2,12,2), xlen=7.2, ylen=5.1, shift=LEFT*2.4)
        graph = ax.plot(lambda x: x*x - 2*x + 3, x_range=[-1.2,4.6], color=BLUE, stroke_width=4)
        x1, x2 = 0, 4
        p1 = ax.c2p(x1, 3)
        p2 = ax.c2p(x2, 11)
        A = Dot(p1, radius=0.075, color=CYAN)
        B = Dot(p2, radius=0.075, color=CYAN)
        chord = Line(p1, p2, color=CYAN, stroke_width=3.4)
        xm = 2
        ym = 3
        M = Dot(ax.c2p(xm, ym), radius=0.08, color=GOLD)
        tangent = ax.plot(lambda x: 2*x - 1, x_range=[-0.2,4.3], color=GOLD, stroke_width=3.6)
        side2 = VGroup(
            mtx(r"x_1=0,\quad x_2=4", 32, INK),
            mtx(r"x_M=2", 34, GOLD),
            mtx(r"k_{AB}=2=f'(2)", 36, GREEN),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.55)
        self.play(Create(ax), FadeIn(labels), Create(graph), run_time=0.9)
        self.play(FadeIn(A), FadeIn(B), Create(chord), run_time=0.7)
        self.play(FadeIn(M, scale=1.5), Create(tangent), FadeIn(side2), run_time=0.8)
        self.narrate(
            "Ví dụ với f bằng x bình phương trừ hai x cộng ba, lấy hai đầu dây có hoành độ không và bốn. Trung điểm hoành độ là hai. Dây A B có hệ số góc bằng hai, và đúng tại x bằng hai, đạo hàm cũng bằng hai. Đây là một tính chất cực gọn nhưng dùng rất tốt trong các bài tiếp tuyến và chứng minh song song.",
            1.7,
        )

    # ======================================================
    # GEM 2 - CUBIC CENTER
    # ======================================================
    def gem2_cubic_center(self):
        self.show_problem(
            "Viên ngọc 2 – Mọi đồ thị bậc ba đều có tâm",
            [
                mtx(r"f(x)=ax^3+bx^2+cx+d,\qquad a\ne0", 38, GOLD),
                "Không cần vẽ, hãy tìm tâm đối xứng của đồ thị.",
            ],
            "Một đồ thị bậc ba nhìn rất khác nhau khi các hệ số thay đổi. Nhưng có một tính chất đẹp: mọi đồ thị của hàm đa thức bậc ba đều có một tâm đối xứng. Và tâm ấy chính là điểm uốn. Ta sẽ chứng minh bằng một phép đổi biến rất ngắn.",
            "Viên ngọc 2/6",
        )

        self.clear_stage(); self.add_header_footer("Viên ngọc 2", "Dịch gốc tọa độ để làm mất hạng tử bậc hai", "Viên ngọc 2/6")
        g = VGroup(
            mtx(r"x_0=-\frac{b}{3a},\qquad y_0=f(x_0)", 40, GOLD),
            mtx(r"x=x_0+t", 36, BLUE),
            mtx(r"f(x_0+t)=y_0+At^3+Bt", 39, CYAN),
            mtx(r"f(x_0-t)=y_0-At^3-Bt", 39, CYAN),
            mtx(r"f(x_0+t)+f(x_0-t)=2y_0", 41, GREEN),
            mtx(r"\boxed{I\left(-\frac{b}{3a},\ f\!\left(-\frac{b}{3a}\right)\right)}", 43, GOLD),
        ).arrange(DOWN, buff=0.30)
        fit_width(g, 11.4)
        for e in g:
            self.play(Write(e), run_time=0.55)
        self.narrate(
            "Ta lấy x không bằng âm b chia ba a. Đây là hoành độ điểm uốn. Đặt x bằng x không cộng t. Điều đặc biệt xảy ra là hạng tử t bình phương biến mất hoàn toàn, nên biểu thức chỉ còn y không cộng A t lập phương cộng B t. Nếu thay t bởi âm t, hai phần lẻ đổi dấu. Cộng hai giá trị lại chỉ còn hai y không. Điều đó nói rằng hai điểm ứng với t và âm t đối xứng nhau qua I. Vì thế mọi hàm bậc ba đều có tâm đối xứng tại điểm uốn.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ cực gọn", "Nhìn hệ số x² là tìm ra tâm", "Viên ngọc 2/6")
        ax, labels = self.make_axes(xr=(-2,4,1), yr=(-8,8,2), xlen=7.0, ylen=5.2, shift=LEFT*2.5)
        graph = ax.plot(lambda x: x**3 - 3*x*x + 2, x_range=[-1.2,3.2], color=BLUE, stroke_width=4)
        I = Dot(ax.c2p(1,0), radius=0.09, color=GOLD)
        side = VGroup(
            mtx(r"f(x)=x^3-3x^2+2", 34, INK),
            mtx(r"x_I=-\frac{-3}{3}=1", 35, CYAN),
            mtx(r"y_I=f(1)=0", 35, CYAN),
            mtx(r"\boxed{I(1,0)}", 42, GOLD),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.45)
        self.play(Create(ax), FadeIn(labels), Create(graph), run_time=1.0)
        self.play(FadeIn(I, scale=1.5), FadeIn(side), run_time=0.8)
        self.narrate(
            "Chẳng hạn f bằng x lập phương trừ ba x bình phương cộng hai. Chỉ nhìn hệ số, hoành độ tâm bằng một. Thay vào hàm được tung độ bằng không. Vậy tâm là I một không. Một bài tìm tâm tưởng phải biến đổi đồ thị khá nhiều, thực ra chỉ cần đúng hai phép tính.",
            1.5,
        )

    # ======================================================
    # GEM 3 - RECTANGULAR HYPERBOLA AREA
    # ======================================================
    def gem3_hyperbola_rectangle(self):
        self.show_problem(
            "Viên ngọc 3 – Hình chữ nhật có diện tích không đổi",
            [
                mtx(r"(H):\ y=b+\frac{k}{x-a},\qquad k\ne0", 41, GOLD),
                "M chạy trên (H). Kẻ qua M hai đường song song với các tiệm cận.",
                "Diện tích hình chữ nhật tạo bởi M và hai tiệm cận bằng bao nhiêu?",
            ],
            "Bài toán thứ ba trông hoàn toàn hình học. Một điểm M chạy trên hyperbol, hai cạnh của hình chữ nhật thay đổi liên tục. Thế nhưng diện tích của hình chữ nhật lại đứng yên. Lời giải chỉ là một dòng nếu ta viết đúng phương trình.",
            "Viên ngọc 3/6",
        )

        self.clear_stage(); self.add_header_footer("Viên ngọc 3", "Phương trình hyperbol chính là công thức diện tích", "Viên ngọc 3/6")
        g = VGroup(
            mtx(r"y-b=\frac{k}{x-a}", 40, INK),
            mtx(r"(x-a)(y-b)=k", 42, CYAN),
            mtx(r"S=|x-a|\,|y-b|", 40, BLUE),
            mtx(r"\boxed{S=|k|}", 48, GOLD),
        ).arrange(DOWN, buff=0.42).shift(LEFT*2.7)
        side = VGroup(
            txt("Hai cạnh thay đổi", 26, INK),
            mtx(r"|x-a|,\quad |y-b|", 34, CYAN),
            txt("nhưng tích của chúng không đổi.", 25, GREEN),
        ).arrange(DOWN, buff=0.24).to_edge(RIGHT, buff=0.6)
        self.play(FadeIn(g), FadeIn(side), run_time=0.9)
        self.narrate(
            "Hai tiệm cận là x bằng a và y bằng b. Khoảng cách theo phương ngang từ M đến tiệm cận đứng là trị tuyệt đối x trừ a. Khoảng cách theo phương dọc là trị tuyệt đối y trừ b. Nhưng phương trình hyperbol cho ngay tích x trừ a nhân y trừ b bằng k. Vì vậy diện tích hình chữ nhật luôn bằng trị tuyệt đối của k, hoàn toàn không phụ thuộc vị trí M.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ", "M chạy nhưng diện tích luôn bằng 6", "Viên ngọc 3/6")
        ax, labels = self.make_axes(xr=(-2,7,1), yr=(-2,8,1), xlen=7.2, ylen=5.2, shift=LEFT*2.4)
        graph1 = ax.plot(lambda x: 2 + 6/(x-1), x_range=[1.8,6.6], color=BLUE, stroke_width=4)
        graph2 = ax.plot(lambda x: 2 + 6/(x-1), x_range=[-1.6,0.2], color=BLUE, stroke_width=4)
        v_asym = DashedLine(ax.c2p(1,-2), ax.c2p(1,8), color=ORANGE, dash_length=0.12)
        h_asym = DashedLine(ax.c2p(-2,2), ax.c2p(7,2), color=ORANGE, dash_length=0.12)
        x0 = 3
        y0 = 5
        M = Dot(ax.c2p(x0,y0), radius=0.08, color=GOLD)
        rect = Polygon(ax.c2p(1,2), ax.c2p(x0,2), ax.c2p(x0,y0), ax.c2p(1,y0), color=GREEN, fill_color=GREEN, fill_opacity=0.16)
        side2 = VGroup(mtx(r"(x-1)(y-2)=6", 36, CYAN), mtx(r"S=2\cdot3=6", 40, GOLD)).arrange(DOWN,buff=0.35).to_edge(RIGHT,buff=0.55)
        self.play(Create(ax), FadeIn(labels), Create(v_asym), Create(h_asym), run_time=0.8)
        self.play(Create(graph1), Create(graph2), run_time=0.8)
        self.play(FadeIn(M), FadeIn(rect), FadeIn(side2), run_time=0.8)
        self.narrate(
            "Với y bằng hai cộng sáu chia x trừ một, hai tiệm cận là x bằng một và y bằng hai. Chọn M ba năm, hai cạnh hình chữ nhật lần lượt bằng hai và ba, diện tích bằng sáu. Nếu M chạy sang vị trí khác, một cạnh dài ra thì cạnh kia ngắn lại đúng tỷ lệ để tích vẫn bằng sáu.",
            1.7,
        )

    # ======================================================
    # GEM 4 - TANGENT TO y=k/x
    # ======================================================
    def gem4_tangent_hyperbola(self):
        self.show_problem(
            "Viên ngọc 4 – Một tiếp tuyến, hai điều bất ngờ",
            [
                mtx(r"(H):\ y=\frac{k}{x},\qquad k>0", 43, GOLD),
                mtx(r"M\left(t,\frac{k}{t}\right),\qquad t>0", 38, CYAN),
                "Tiếp tuyến tại M cắt Ox, Oy lần lượt tại A, B.",
                "Chứng minh M là trung điểm AB và diện tích tam giác OAB không đổi.",
            ],
            "Đây là một bài rất đẹp. M chạy trên hyperbol y bằng k trên x. Tiếp tuyến tại M cắt hai trục tọa độ. Hai giao điểm A và B thay đổi theo M, nhưng điểm tiếp xúc luôn là trung điểm của A B. Chưa hết, diện tích tam giác O A B cũng là một hằng số.",
            "Viên ngọc 4/6",
        )

        self.clear_stage(); self.add_header_footer("Viên ngọc 4", "Tất cả nằm trong phương trình tiếp tuyến", "Viên ngọc 4/6")
        deriv = VGroup(
            mtx(r"f'(t)=-\frac{k}{t^2}", 37, BLUE),
            mtx(r"y-\frac{k}{t}=-\frac{k}{t^2}(x-t)", 38, INK),
            mtx(r"y=-\frac{k}{t^2}x+\frac{2k}{t}", 39, CYAN),
            mtx(r"A(2t,0),\qquad B\left(0,\frac{2k}{t}\right)", 38, GREEN),
            mtx(r"\frac{A+B}{2}=\left(t,\frac{k}{t}\right)=M", 37, GOLD),
            mtx(r"S_{OAB}=\frac12\cdot2t\cdot\frac{2k}{t}=\boxed{2k}", 40, GOLD),
        ).arrange(DOWN, buff=0.27)
        fit_width(deriv, 11.5)
        for e in deriv:
            self.play(Write(e), run_time=0.52)
        self.narrate(
            "Đạo hàm tại t là âm k chia t bình phương. Viết phương trình tiếp tuyến rồi rút gọn, ta đọc ngay được hai giao điểm: A có hoành độ hai t, B có tung độ hai k chia t. Trung điểm của A B là t và k chia t, đúng bằng M. Đồng thời diện tích tam giác vuông O A B bằng một nửa nhân hai t nhân hai k chia t, nên bằng hai k. Cả hai kết luận đều rơi ra từ cùng một phương trình tiếp tuyến.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Nhìn trên hình", "M là trung điểm của đoạn chắn bởi hai trục", "Viên ngọc 4/6")
        ax, labels = self.make_axes(xr=(-1,7,1), yr=(-1,7,1), xlen=6.7, ylen=5.3, shift=LEFT*2.45)
        graph = ax.plot(lambda x: 4/x, x_range=[0.65,6.5], color=BLUE, stroke_width=4)
        t = 2
        k = 4
        M = Dot(ax.c2p(2,2), radius=0.085, color=GOLD)
        A = Dot(ax.c2p(4,0), radius=0.07, color=CYAN)
        B = Dot(ax.c2p(0,4), radius=0.07, color=CYAN)
        tangent = Line(ax.c2p(0,4), ax.c2p(4,0), color=GOLD, stroke_width=3.6)
        tri = Polygon(ax.c2p(0,0), ax.c2p(4,0), ax.c2p(0,4), fill_color=GREEN, fill_opacity=0.12, stroke_color=GREEN)
        side = VGroup(mtx(r"k=4,\quad t=2", 32, INK), mtx(r"M(2,2)", 34, GOLD), mtx(r"A(4,0),\ B(0,4)", 33, CYAN), mtx(r"S_{OAB}=8", 39, GREEN)).arrange(DOWN,buff=0.27).to_edge(RIGHT,buff=0.5)
        self.play(Create(ax), FadeIn(labels), Create(graph), run_time=0.8)
        self.play(FadeIn(tri), Create(tangent), FadeIn(A), FadeIn(B), FadeIn(M,scale=1.4), FadeIn(side), run_time=0.9)
        self.narrate(
            "Với k bằng bốn và t bằng hai, M là hai hai. Tiếp tuyến cắt hai trục tại bốn không và không bốn, nên M đúng là trung điểm. Tam giác O A B có diện tích tám, bằng hai k. Khi M trượt dọc hyperbol, tam giác thay hình đổi dạng nhưng diện tích vẫn luôn bằng tám.",
            1.7,
        )

    # ======================================================
    # GEM 5 - EXPONENTIAL TANGENT
    # ======================================================
    def gem5_exponential_tangent(self):
        self.show_problem(
            "Viên ngọc 5 – Tiếp tuyến hàm mũ luôn lùi một khoảng cố định",
            [
                mtx(r"f(x)=a^x,\qquad a>0,\ a\ne1", 42, GOLD),
                mtx(r"M(t,a^t)", 37, CYAN),
                "Tiếp tuyến tại M cắt Ox tại H. Tính khoảng cách theo phương ngang giữa M và H.",
            ],
            "Bài thứ năm nhìn như một bài tiếp tuyến có tham số t. Nhưng kết quả rất lạ: điểm tiếp xúc chạy đến đâu thì giao điểm của tiếp tuyến với trục hoành cũng chạy theo, luôn cách hoành độ tiếp xúc đúng một khoảng cố định. Khoảng ấy chỉ phụ thuộc cơ số a, không phụ thuộc t.",
            "Viên ngọc 5/6",
        )

        self.clear_stage(); self.add_header_footer("Viên ngọc 5", "Khoảng cách không phụ thuộc điểm tiếp xúc", "Viên ngọc 5/6")
        deriv = VGroup(
            mtx(r"f'(t)=a^t\ln a", 38, BLUE),
            mtx(r"y-a^t=a^t\ln a\,(x-t)", 38, INK),
            mtx(r"y=a^t\bigl[1+\ln a\,(x-t)\bigr]", 37, CYAN),
            mtx(r"y=0\Longrightarrow x_H=t-\frac{1}{\ln a}", 40, GREEN),
            mtx(r"\boxed{|t-x_H|=\frac{1}{|\ln a|}}", 44, GOLD),
            mtx(r"a=e\Longrightarrow |t-x_H|=1", 38, GOLD),
        ).arrange(DOWN, buff=0.29)
        fit_width(deriv, 11.4)
        for e in deriv:
            self.play(Write(e), run_time=0.52)
        self.narrate(
            "Đạo hàm của a mũ x tại t bằng a mũ t nhân lô ga tự nhiên của a. Viết tiếp tuyến rồi cho y bằng không, hệ số a mũ t triệt tiêu hoàn toàn. Ta được hoành độ H bằng t trừ một chia lô ga tự nhiên của a. Vì vậy khoảng cách theo phương ngang giữa H và điểm tiếp xúc luôn bằng một chia trị tuyệt đối lô ga tự nhiên của a. Đặc biệt với hàm e mũ x, khoảng cách ấy luôn đúng bằng một.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Trường hợp đẹp nhất: y = e^x", "Tiếp tuyến luôn cắt Ox tại t - 1", "Viên ngọc 5/6")
        ax, labels = self.make_axes(xr=(-4,4,1), yr=(-1,9,1), xlen=7.0, ylen=5.2, shift=LEFT*2.45)
        graph = ax.plot(lambda x: math.exp(x), x_range=[-3.5,2.05], color=BLUE, stroke_width=4)
        tvals = [-1,0,1]
        colors = [PURPLE, GREEN, ORANGE]
        lines = VGroup(); pts = VGroup(); hs = VGroup()
        for t0,col in zip(tvals,colors):
            y0 = math.exp(t0)
            line = ax.plot(lambda x,t0=t0,y0=y0: y0*(x-t0+1), x_range=[t0-1.3,t0+1.25], color=col, stroke_width=2.8)
            lines.add(line)
            pts.add(Dot(ax.c2p(t0,y0),radius=0.065,color=col))
            hs.add(Dot(ax.c2p(t0-1,0),radius=0.055,color=GOLD))
        side=VGroup(mtx(r"t=-1\Rightarrow x_H=-2",31,PURPLE),mtx(r"t=0\Rightarrow x_H=-1",31,GREEN),mtx(r"t=1\Rightarrow x_H=0",31,ORANGE),mtx(r"t-x_H=1",38,GOLD)).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.45)
        self.play(Create(ax),FadeIn(labels),Create(graph),run_time=0.8)
        for l,p,h in zip(lines,pts,hs): self.play(Create(l),FadeIn(p),FadeIn(h),run_time=0.42)
        self.play(FadeIn(side),run_time=0.6)
        self.narrate(
            "Trên đồ thị e mũ x, ta vẽ ba tiếp tuyến tại t bằng âm một, không và một. Các giao điểm với trục hoành lần lượt có hoành độ âm hai, âm một và không. Mỗi lần điểm tiếp xúc dịch sang phải một đơn vị, giao điểm cũng dịch sang phải một đơn vị, và khoảng cách ngang giữa chúng luôn bằng một.",
            1.7,
        )

    # ======================================================
    # GEM 6 - COMPOSITION MONOTONE
    # ======================================================
    def gem6_composition(self):
        self.show_problem(
            "Viên ngọc 6 – Phương trình lồng hàm tưởng rất khó",
            [
                "Cho f là hàm số đồng biến nghiêm ngặt trên R.",
                mtx(r"f(f(x))=x", 47, GOLD),
                "Chứng minh phương trình này tương đương với f(x)=x.",
            ],
            "Bài cuối cùng là một mẹo tư duy rất mạnh. Phương trình f của f của x bằng x thường làm học sinh nghĩ phải khai triển một biểu thức cực lớn. Nhưng nếu f đồng biến nghiêm ngặt, ta không cần khai triển gì cả. Chỉ cần so sánh f của x với x.",
            "Viên ngọc 6/6",
        )

        self.clear_stage(); self.add_header_footer("Viên ngọc 6", "Đơn điệu phá tan lớp hàm hợp", "Viên ngọc 6/6")
        case1 = VGroup(
            mtx(r"f(x)>x", 38, RED),
            mtx(r"f(f(x))>f(x)>x", 38, RED),
            mtx(r"\bot,\qquad f(f(x))=x", 35, RED),
        ).arrange(DOWN,buff=0.22)
        case2 = VGroup(
            mtx(r"f(x)<x", 38, ORANGE),
            mtx(r"f(f(x))<f(x)<x", 38, ORANGE),
            mtx(r"\bot,\qquad f(f(x))=x", 35, ORANGE),
        ).arrange(DOWN,buff=0.22)
        cases = VGroup(case1, case2).arrange(RIGHT,buff=1.1).shift(UP*0.5)
        ans = mtx(r"\boxed{f(f(x))=x\iff f(x)=x}", 47, GOLD).shift(DOWN*1.55)
        self.play(FadeIn(cases),run_time=0.8)
        self.narrate(
            "Giả sử f của x lớn hơn x. Vì f đồng biến, áp dụng f vào hai vế sẽ cho f của f của x lớn hơn f của x, do đó còn lớn hơn x. Nhưng đề bài nói f của f của x bằng x, mâu thuẫn. Tương tự, nếu f của x nhỏ hơn x, tính đồng biến cho f của f của x nhỏ hơn f của x và nhỏ hơn x, cũng mâu thuẫn. Vậy chỉ còn khả năng f của x bằng x.",
            2.0,
        )
        self.play(Write(ans),run_time=0.8)

        self.clear_stage(); self.add_header_footer("Áp dụng", "Một phương trình bậc chín biến thành bậc ba", "Viên ngọc 6/6")
        q = VGroup(
            mtx(r"f(x)=x^3+x-1", 41, GOLD),
            mtx(r"f'(x)=3x^2+1>0", 37, GREEN),
            mtx(r"f(f(x))=x", 40, INK),
            mtx(r"\Longleftrightarrow f(x)=x", 40, CYAN),
            mtx(r"x^3+x-1=x", 38, INK),
            mtx(r"x^3=1", 40, INK),
            mtx(r"\boxed{x=1}", 48, GOLD),
        ).arrange(DOWN,buff=0.25)
        fit_width(q,10.4)
        for e in q: self.play(Write(e),run_time=0.46)
        self.narrate(
            "Áp dụng với f bằng x lập phương cộng x trừ một. Đạo hàm bằng ba x bình phương cộng một, luôn dương, nên f đồng biến nghiêm ngặt. Nếu khai triển f của f của x, ta sẽ gặp một đa thức bậc chín rất khó chịu. Nhưng định lý vừa chứng minh cho phép thay ngay bằng f của x bằng x. Khi đó x lập phương cộng x trừ một bằng x, suy ra x lập phương bằng một và nghiệm duy nhất là x bằng một. Đây là ví dụ điển hình của một bài nhìn rất khó nhưng lời giải đúng chỉ vài dòng.",
            2.2,
        )

    # ======================================================
    # BONUS - TWO PARABOLA TANGENTS
    # ======================================================
    def bonus_parabola_tangents(self):
        self.clear_stage(); self.add_header_footer("Phần thưởng – Một tính chất nữa của parabol", "Giao hai tiếp tuyến biết ngay hoành độ", "Bonus")
        p = VGroup(
            mtx(r"(P):\ y=x^2", 39, GOLD),
            mtx(r"A(p,p^2),\qquad B(q,q^2)", 36, CYAN),
            mtx(r"d_A:\ y=2px-p^2", 36, INK),
            mtx(r"d_B:\ y=2qx-q^2", 36, INK),
            mtx(r"2px-p^2=2qx-q^2", 35, BLUE),
            mtx(r"(p-q)\bigl(2x-(p+q)\bigr)=0", 35, CYAN),
            mtx(r"\boxed{x_T=\frac{p+q}{2}}", 43, GOLD),
        ).arrange(DOWN,buff=0.23).shift(LEFT*2.5)
        fit_width(p,7.5)
        side=VGroup(
            txt("Giao hai tiếp tuyến nằm trên",25,INK),
            txt("đường thẳng đứng qua trung điểm",25,CYAN),
            txt("của hai điểm tiếp xúc.",25,CYAN),
        ).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.6)
        self.play(FadeIn(p),FadeIn(side),run_time=0.9)
        self.narrate(
            "Thầy tặng thêm một tính chất rất đẹp. Với parabol y bằng x bình phương, tiếp tuyến tại hoành độ p có phương trình hai p x trừ p bình phương. Tiếp tuyến tại q tương tự. Cho hai phương trình bằng nhau, ta tách ngay được nhân tử p trừ q, và hoành độ giao điểm bằng trung bình cộng p cộng q chia hai. Nghĩa là giao của hai tiếp tuyến luôn nằm trên đường thẳng đứng đi qua trung điểm của hai điểm tiếp xúc. Một phép biến đổi rất ngắn nhưng hình học lại rất đẹp.",
            2.0,
        )

    # ======================================================
    # SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_stage(); self.add_header_footer("Bản đồ nhận dạng lời giải đẹp", "Mỗi cấu trúc gợi một động tác", "Tổng kết")
        rows = VGroup(
            VGroup(mtx(r"ax^2+bx+c",31,BLUE),txt("→ nghĩ đến trung điểm hoành độ của dây",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"ax^3+bx^2+cx+d",31,CYAN),txt("→ dịch về điểm uốn để lộ tính lẻ",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"y=b+\frac{k}{x-a}",31,GREEN),txt("→ nhân hai độ lệch tới tiệm cận",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"y=\frac{k}{x}",31,ORANGE),txt("→ phương trình tiếp tuyến cho trung điểm + diện tích",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"y=a^x",31,PURPLE),txt("→ cho y=0 trong tiếp tuyến để thấy khoảng cố định",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"f(f(x))=x",31,GOLD),txt("→ nếu f tăng nghiêm ngặt, so sánh f(x) với x",24,INK)).arrange(RIGHT,buff=0.20),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30)
        fit_width(rows,11.9)
        for r in rows: self.play(FadeIn(r,shift=RIGHT*0.10),run_time=0.34)
        self.narrate(
            "Ta chốt lại bằng một bản đồ nhận dạng. Gặp parabol và dây cung, hãy nghĩ đến trung điểm hoành độ. Gặp bậc ba, hãy nghĩ đến điểm uốn và phép dịch tâm. Gặp hyperbol chữ nhật, hãy nhân hai độ lệch tới các tiệm cận. Gặp tiếp tuyến của k trên x, hãy đọc hai đoạn chắn trên trục. Gặp hàm mũ, hãy thử cho y bằng không trong phương trình tiếp tuyến. Và gặp hàm hợp cùng điều kiện đơn điệu, đừng khai triển vội; hãy thử so sánh f của x với x.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Bài thử thách cuối", "Nhìn ra cấu trúc trước khi tính", "Tổng kết")
        q = VGroup(
            txt("Cho f đồng biến nghiêm ngặt và", 27, INK),
            mtx(r"f(f(f(x)))=x", 46, GOLD),
            txt("Chứng minh rằng", 27, INK),
            mtx(r"f(x)=x", 43, CYAN),
        ).arrange(DOWN,buff=0.32).shift(UP*0.65)
        self.play(FadeIn(q),run_time=0.7)
        self.narrate(
            "Bài thử thách: nếu f đồng biến nghiêm ngặt và f lồng ba lần của x bằng x, ta có thể kết luận f của x bằng x hay không? Hãy dừng video và thử dùng đúng tư duy so sánh vừa học, không khai triển và cũng không cần biết công thức cụ thể của f.",
            1.5,
        )
        sol = VGroup(
            mtx(r"f(x)>x\Rightarrow f(f(x))>f(x)>x", 35, RED),
            mtx(r"\Rightarrow f(f(f(x)))>f(f(x))>x", 34, RED),
            txt("mâu thuẫn", 25, RED, BOLD),
            mtx(r"f(x)<x", 35, ORANGE),
            txt("tương tự cũng mâu thuẫn", 25, ORANGE, BOLD),
            mtx(r"\boxed{f(x)=x}", 46, GOLD),
        ).arrange(DOWN,buff=0.20).shift(DOWN*0.85)
        self.play(FadeIn(sol),run_time=0.9)
        self.narrate(
            "Nếu f của x lớn hơn x, vì f tăng, ta có f hai lần của x lớn hơn f của x, rồi f ba lần của x lại lớn hơn f hai lần của x. Như vậy f ba lần của x lớn hơn x, trái giả thiết. Trường hợp f của x nhỏ hơn x cũng mâu thuẫn tương tự. Vì thế f của x bắt buộc bằng x. Ý tưởng không đổi, dù số lớp hàm hợp tăng lên.",
            1.9,
        )

    def outro(self):
        self.clear_stage()
        main=txt("VẺ ĐẸP CỦA HÀM SỐ",44,GOLD,BOLD)
        formula=VGroup(
            txt("Bài khó",29,INK),
            mtx(r"+",36,MUTED),
            txt("đúng cấu trúc",29,CYAN),
            mtx(r"\Longrightarrow",38,BLUE),
            txt("lời giải ngắn",29,GOLD,BOLD),
        ).arrange(RIGHT,buff=0.20)
        sub=txt("Đừng tính nhiều hơn những gì cấu trúc thực sự yêu cầu.",28,CYAN)
        brand=txt(TEN_THAY,22,MUTED)
        g=VGroup(main,formula,sub,brand).arrange(DOWN,buff=0.38)
        fit_width(g,12.0)
        self.play(FadeIn(g),run_time=1.0)
        self.narrate(
            "Sáu bài hôm nay rất khác nhau, nhưng đều có chung một tinh thần: lời giải ngắn xuất hiện khi ta nhìn đúng cấu trúc. Toán phổ thông có rất nhiều bài như vậy. Điều đáng học không chỉ là kết quả cuối, mà là khoảnh khắc ta nhận ra thứ gì nên được giữ lại và thứ gì có thể bỏ qua. Hẹn gặp các em ở video tiếp theo với những bài toán đẹp và bất ngờ hơn nữa.",
            2.0,
        )

    def construct(self):
        self.intro()
        self.gem1_quadratic_chord()
        self.gem2_cubic_center()
        self.gem3_hyperbola_rectangle()
        self.gem4_tangent_hyperbola()
        self.gem5_exponential_tangent()
        self.gem6_composition()
        self.bonus_parabola_tangents()
        self.synthesis()
        self.outro()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "tinh_chat_dep_la_ham_so_1080p"
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
    master_wav = ROOT / "master_narration_tinh_chat_dep.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate",
        "-show_entries", "format=duration,size",
        "-of", "json", str(final_path)
    ], check=True)

    print("\n============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


if __name__ == "__main__":
    render_full()

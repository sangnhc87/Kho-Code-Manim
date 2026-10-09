from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time
import numpy as np

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

    def narrate_play(self, text, *animations, min_time=1.0, rate_func=linear):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.play(*animations, run_time=max(dur, min_time), rate_func=rate_func)
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
        self.add_header_footer(title, "BÀI TOÁN", progress)
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
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.28)
        self.narrate(voice, 1.8)

    def make_axes(self, xr=(-5, 6, 1), yr=(-5, 8, 1), xlen=6.7, ylen=5.2, shift=LEFT*2.7):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 21},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 27), mtx("y", 27))
        return ax, labels

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("NHỮNG VIÊN NGỌC CỦA HÀM SỐ – PHẦN 2", 45, GOLD, BOLD),
            txt("Bài nhìn khó, hình chuyển động đẹp, lời giải lại rất ngắn", 29, CYAN),
            VGroup(txt("Nhìn cấu trúc", 27, INK), Arrow(LEFT*0.35, RIGHT*0.35, color=CYAN, stroke_width=3), txt("lời giải gọn", 27, INK)).arrange(RIGHT, buff=0.18),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.32)
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.7)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), run_time=1.0)
        self.narrate(
            "Chào các em. Ở phần hai này, thầy chọn sáu tính chất rất đẹp của hàm số. Điều đặc biệt là ta sẽ không chỉ nhìn công thức. Mỗi bài đều có điểm chuyển động thật trên đồ thị, các đường thẳng và tiếp tuyến chạy theo, để các em nhìn thấy quy luật trước khi chứng minh. Nhiều bài trông khá khó, nhưng khi nhận đúng cấu trúc thì lời giải chỉ còn vài dòng.",
            2.0,
        )

    # ======================================================
    # GEM 1: LOGISTIC CENTRAL SYMMETRY
    # ======================================================
    def gem1_logistic(self):
        self.show_problem(
            "Viên ngọc 1 – Một tâm đối xứng ẩn",
            [
                mtx(r"f(x)=\frac{1}{1+e^{-x}}", 43, GOLD),
                "Lấy hai điểm ứng với hai hoành độ đối nhau.",
                mtx(r"A(t,f(t)),\qquad B(-t,f(-t))", 38, CYAN),
                "Trung điểm của AB có gì đặc biệt?",
            ],
            "Ta bắt đầu bằng hàm logistic. Đồ thị có dạng chữ S và tưởng như không có tính chất hình học đơn giản. Nhưng hãy lấy hai điểm có hoành độ đối nhau là t và âm t, rồi quan sát trung điểm của đoạn nối hai điểm đó.",
            "1/6",
        )

        self.clear_stage(); self.add_header_footer("Viên ngọc 1", "Hai điểm chạy, trung điểm đứng yên", "1/6")
        ax, labels = self.make_axes(xr=(-5,5,1), yr=(-0.2,1.2,0.2), xlen=7.0, ylen=4.8, shift=LEFT*2.6)
        curve = ax.plot(lambda x: 1/(1+math.exp(-x)), x_range=[-5,5], color=BLUE, stroke_width=4)
        t = ValueTracker(0.8)
        A = always_redraw(lambda: Dot(ax.c2p(t.get_value(), 1/(1+math.exp(-t.get_value()))), radius=0.075, color=GOLD))
        B = always_redraw(lambda: Dot(ax.c2p(-t.get_value(), 1/(1+math.exp(t.get_value()))), radius=0.075, color=GREEN))
        seg = always_redraw(lambda: Line(A.get_center(), B.get_center(), color=CYAN, stroke_width=3))
        I = Dot(ax.c2p(0,0.5), radius=0.08, color=RED)
        ilab = mtx(r"I\left(0,\frac12\right)", 28, RED).next_to(I, RIGHT, buff=0.12)
        formula = VGroup(
            mtx(r"f(-x)=\frac{1}{1+e^x}", 34, INK),
            mtx(r"f(x)+f(-x)=1", 38, CYAN),
            mtx(r"M_{AB}=\left(0,\frac12\right)", 40, GOLD),
        ).arrange(DOWN, buff=0.34).to_edge(RIGHT, buff=0.45).shift(UP*0.4)
        self.play(Create(ax), FadeIn(labels), Create(curve), run_time=1.0)
        self.play(FadeIn(A), FadeIn(B), Create(seg), FadeIn(I), FadeIn(ilab), FadeIn(formula), run_time=1.0)
        self.narrate_play(
            "Khi t tăng, hai điểm A và B chạy về hai phía của đồ thị. Nhưng đoạn A B luôn đi qua đúng một điểm cố định. Đó là điểm có hoành độ không và tung độ một phần hai.",
            t.animate.set_value(4.0), min_time=4.0,
        )
        self.narrate_play(
            "Cho t chạy ngược lại, hiện tượng vẫn không đổi. Lý do đại số cực ngắn: f của x cộng f của âm x luôn bằng một. Vì hai hoành độ cũng có tổng bằng không, nên trung điểm của A B luôn là I không, một phần hai.",
            t.animate.set_value(0.45), min_time=4.0,
        )
        box = VGroup(mtx(r"\boxed{I\left(0,\frac12\right)}", 35, GOLD), txt("là tâm đối xứng", 24, GOLD, BOLD)).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.65).shift(RIGHT*2.0)
        self.play(Write(box), run_time=0.7)
        self.narrate("Một tiêu chuẩn rất đáng nhớ là: nếu f của a cộng t cộng f của a trừ t luôn bằng hai b, thì đồ thị nhận I a b làm tâm đối xứng.", 1.5)

    # ======================================================
    # GEM 2: x + 1/x
    # ======================================================
    def gem2_reciprocal(self):
        self.show_problem(
            "Viên ngọc 2 – Hai giao điểm luôn nghịch đảo",
            [
                mtx(r"f(x)=x+\frac1x,\qquad x>0", 42, GOLD),
                mtx(r"y=m,\qquad m>2", 38, CYAN),
                "Đường thẳng ngang cắt đồ thị tại A và B.",
                "Có đại lượng nào của hai hoành độ luôn không đổi?",
            ],
            "Bây giờ xét hàm x cộng một trên x. Một đường thẳng ngang y bằng m lớn hơn hai thường cắt đồ thị tại hai điểm. Khi đường thẳng chạy lên xuống, hai giao điểm cũng chạy, nhưng tích hai hoành độ lại không thay đổi.",
            "2/6",
        )
        self.clear_stage(); self.add_header_footer("Viên ngọc 2", "Đường ngang chuyển động – tích hoành độ bất biến", "2/6")
        ax, labels = self.make_axes(xr=(0,5.5,0.5), yr=(0,6,1), xlen=6.8, ylen=5.2, shift=LEFT*2.65)
        curve = ax.plot(lambda x: x + 1/x, x_range=[0.18,5.2], color=BLUE, stroke_width=4)
        m = ValueTracker(2.25)
        def roots():
            mm = m.get_value()
            d = math.sqrt(max(mm*mm-4, 0))
            return (mm-d)/2, (mm+d)/2
        hline = always_redraw(lambda: Line(ax.c2p(0,m.get_value()), ax.c2p(5.25,m.get_value()), color=ORANGE, stroke_width=3))
        A = always_redraw(lambda: Dot(ax.c2p(roots()[0], m.get_value()), radius=0.075, color=GOLD))
        B = always_redraw(lambda: Dot(ax.c2p(roots()[1], m.get_value()), radius=0.075, color=GREEN))
        labA = always_redraw(lambda: mtx(r"A", 26, GOLD).next_to(A, UL, buff=0.08))
        labB = always_redraw(lambda: mtx(r"B", 26, GREEN).next_to(B, UR, buff=0.08))
        deriv = VGroup(
            mtx(r"x+\frac1x=m", 35, INK),
            mtx(r"x^2-mx+1=0", 37, CYAN),
            mtx(r"x_1x_2=1", 43, GOLD),
            mtx(r"\boxed{x_2=\frac1{x_1}}", 38, GREEN),
        ).arrange(DOWN, buff=0.32).to_edge(RIGHT, buff=0.55).shift(UP*0.35)
        self.play(Create(ax), FadeIn(labels), Create(curve), FadeIn(deriv), run_time=1.1)
        self.play(Create(hline), FadeIn(A), FadeIn(B), FadeIn(labA), FadeIn(labB), run_time=0.8)
        self.narrate_play(
            "Kéo đường y bằng m lên cao. Điểm bên trái chạy rất nhanh về gần trục tung, còn điểm bên phải chạy xa sang phải. Nhìn bằng mắt tưởng hai chuyển động không liên quan, nhưng tích hai hoành độ luôn bằng một.",
            m.animate.set_value(5.0), min_time=4.5,
        )
        self.narrate_play(
            "Lời giải chỉ có hai dòng. Phương trình giao điểm trở thành x bình phương trừ m x cộng một bằng không. Theo Viète, tích hai nghiệm bằng một. Vì vậy hai hoành độ luôn nghịch đảo của nhau.",
            m.animate.set_value(2.35), min_time=4.2,
        )
        note = txt("Hình thay đổi mạnh, nhưng tích nghiệm không đổi.", 26, MUTED).to_edge(DOWN, buff=0.65).shift(RIGHT*2.0)
        self.play(FadeIn(note), run_time=0.5)

    # ======================================================
    # GEM 3: CUBIC CENTROID
    # ======================================================
    def gem3_cubic_centroid(self):
        self.show_problem(
            "Viên ngọc 3 – Ba giao điểm và một điểm trung bình rất ngoan",
            [
                mtx(r"y=x^3-3x", 44, GOLD),
                mtx(r"y=m,\qquad -2<m<2", 38, CYAN),
                "Đường ngang cắt đồ thị tại ba điểm A, B, C.",
                "Điểm trung bình của ba giao điểm chạy trên đường nào?",
            ],
            "Đây là một bài rất đẹp của hàm bậc ba. Khi đường ngang y bằng m nằm giữa âm hai và hai, nó cắt đồ thị tại ba điểm. Ba điểm đều chuyển động, nhưng điểm trung bình của ba vị trí đó lại bị khóa trên một đường thẳng rất đơn giản.",
            "3/6",
        )
        self.clear_stage(); self.add_header_footer("Viên ngọc 3", "Ba điểm chạy – điểm trung bình chỉ đi trên trục Oy", "3/6")
        ax, labels = self.make_axes(xr=(-2.6,2.6,0.5), yr=(-3,3,1), xlen=7.0, ylen=5.3, shift=LEFT*2.55)
        curve = ax.plot(lambda x: x**3-3*x, x_range=[-2.2,2.2], color=BLUE, stroke_width=4)
        m = ValueTracker(-1.6)
        def real_roots():
            rr = np.roots([1.0,0.0,-3.0,-m.get_value()])
            vals = sorted([float(r.real) for r in rr if abs(r.imag) < 1e-7])
            if len(vals) != 3:
                return [-1.0,0.0,1.0]
            return vals
        hline = always_redraw(lambda: Line(ax.c2p(-2.5,m.get_value()), ax.c2p(2.5,m.get_value()), color=ORANGE, stroke_width=3))
        pts = always_redraw(lambda: VGroup(*[Dot(ax.c2p(x,m.get_value()), radius=0.072, color=c) for x,c in zip(real_roots(),[GOLD,CYAN,GREEN])]))
        span = always_redraw(lambda: Line(ax.c2p(real_roots()[0],m.get_value()), ax.c2p(real_roots()[-1],m.get_value()), color=MUTED, stroke_width=2))
        G = always_redraw(lambda: Dot(ax.c2p(0,m.get_value()), radius=0.085, color=RED))
        glab = always_redraw(lambda: mtx(r"G", 26, RED).next_to(G, RIGHT, buff=0.08))
        deriv = VGroup(
            mtx(r"x^3-3x-m=0", 36, INK),
            mtx(r"x_1+x_2+x_3=0", 40, CYAN),
            mtx(r"x_G=\frac{x_1+x_2+x_3}{3}=0", 36, GOLD),
            mtx(r"\boxed{G(0,m)}", 43, GREEN),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.40).shift(UP*0.3)
        self.play(Create(ax), FadeIn(labels), Create(curve), FadeIn(deriv), run_time=1.0)
        self.play(Create(hline), FadeIn(pts), Create(span), FadeIn(G), FadeIn(glab), run_time=0.8)
        self.narrate_play(
            "Cho m tăng từ gần âm hai lên gần hai. Ba giao điểm chạy rất khác nhau trên đồ thị, nhưng chấm đỏ là điểm trung bình của ba giao điểm chỉ trượt thẳng trên trục O y. Nó không bao giờ rời trục này.",
            m.animate.set_value(1.65), min_time=5.0,
        )
        self.narrate_play(
            "Vì ba hoành độ là ba nghiệm của phương trình x mũ ba trừ ba x trừ m bằng không, hệ số của x bình phương bằng không. Theo Viète, tổng ba nghiệm bằng không. Do đó hoành độ điểm trung bình luôn bằng không, còn tung độ của cả ba điểm đều bằng m.",
            m.animate.set_value(-0.8), min_time=4.5,
        )
        self.narrate("Điều đẹp ở đây là một dữ kiện đại số rất nhỏ, hệ số x bình phương bằng không, lại biến thành một quỹ tích hình học rất rõ ràng của điểm trung bình ba giao điểm.", 1.5)

    # ======================================================
    # GEM 4: PARABOLA TANGENTS
    # ======================================================
    def gem4_parabola_tangents(self):
        self.show_problem(
            "Viên ngọc 4 – Hai tiếp tuyến tiết lộ một đường thẳng ẩn",
            [
                mtx(r"(P):\ y=x^2", 43, GOLD),
                mtx(r"A(a,a^2),\qquad B(b,b^2)", 37, CYAN),
                "Hai tiếp tuyến tại A, B cắt nhau tại T.",
                "Gọi M là trung điểm của AB. Quan hệ giữa M và T?",
            ],
            "Lấy hai điểm bất kỳ trên parabol y bằng x bình phương. Dựng hai tiếp tuyến tại đó và gọi giao điểm là T. Đồng thời lấy trung điểm M của dây A B. Khi hai điểm A và B chạy độc lập, có một quan hệ hình học luôn đúng.",
            "4/6",
        )
        self.clear_stage(); self.add_header_footer("Viên ngọc 4", "A và B chạy, M và T luôn thẳng đứng", "4/6")
        ax, labels = self.make_axes(xr=(-3.5,3.5,0.5), yr=(-4,10,2), xlen=7.0, ylen=5.4, shift=LEFT*2.55)
        curve = ax.plot(lambda x: x*x, x_range=[-3.1,3.1], color=BLUE, stroke_width=4)
        a = ValueTracker(-2.2); b = ValueTracker(1.4)
        A = always_redraw(lambda: Dot(ax.c2p(a.get_value(),a.get_value()**2), radius=0.072, color=GOLD))
        B = always_redraw(lambda: Dot(ax.c2p(b.get_value(),b.get_value()**2), radius=0.072, color=GREEN))
        chord = always_redraw(lambda: Line(A.get_center(), B.get_center(), color=MUTED, stroke_width=2.5))
        ta = always_redraw(lambda: ax.plot(lambda x: 2*a.get_value()*x-a.get_value()**2, x_range=[-3.2,3.2], color=ORANGE, stroke_width=2.8))
        tb = always_redraw(lambda: ax.plot(lambda x: 2*b.get_value()*x-b.get_value()**2, x_range=[-3.2,3.2], color=PURPLE, stroke_width=2.8))
        T = always_redraw(lambda: Dot(ax.c2p((a.get_value()+b.get_value())/2, a.get_value()*b.get_value()), radius=0.08, color=RED))
        M = always_redraw(lambda: Dot(ax.c2p((a.get_value()+b.get_value())/2, (a.get_value()**2+b.get_value()**2)/2), radius=0.08, color=CYAN))
        vertical = always_redraw(lambda: DashedLine(T.get_center(), M.get_center(), color=CYAN, dash_length=0.12))
        labels_dyn = always_redraw(lambda: VGroup(
            mtx(r"A",24,GOLD).next_to(A,UL,buff=0.06),
            mtx(r"B",24,GREEN).next_to(B,UR,buff=0.06),
            mtx(r"T",24,RED).next_to(T,DOWN,buff=0.06),
            mtx(r"M",24,CYAN).next_to(M,UP,buff=0.06),
        ))
        deriv = VGroup(
            mtx(r"t_a:\ y=2ax-a^2", 31, ORANGE),
            mtx(r"t_b:\ y=2bx-b^2", 31, PURPLE),
            mtx(r"T\left(\frac{a+b}{2},ab\right)", 35, RED),
            mtx(r"M\left(\frac{a+b}{2},\frac{a^2+b^2}{2}\right)", 33, CYAN),
            mtx(r"\boxed{x_T=x_M=\frac{a+b}{2}}", 35, GOLD),
        ).arrange(DOWN,buff=0.24).to_edge(RIGHT,buff=0.28).shift(UP*0.2)
        self.play(Create(ax), FadeIn(labels), Create(curve), FadeIn(deriv), run_time=1.0)
        self.play(FadeIn(A), FadeIn(B), Create(chord), Create(ta), Create(tb), FadeIn(T), FadeIn(M), Create(vertical), FadeIn(labels_dyn), run_time=1.0)
        self.narrate_play(
            "Bây giờ cho A chạy sang phải, còn B vẫn đứng yên. Giao điểm hai tiếp tuyến T và trung điểm M đều chạy, nhưng đường nét đứt nối M với T luôn thẳng đứng.",
            a.animate.set_value(-0.7), min_time=4.5,
        )
        self.narrate_play(
            "Tiếp tục cho B chạy ra xa. Tính chất vẫn giữ nguyên. Từ hai phương trình tiếp tuyến, ta tìm được hoành độ T bằng trung bình cộng a và b. Trung điểm M của A B hiển nhiên cũng có đúng hoành độ đó.",
            b.animate.set_value(2.6), min_time=4.5,
        )
        gap = mtx(r"MT=\frac{(a-b)^2}{2}", 38, GREEN).to_edge(DOWN,buff=0.65).shift(RIGHT*2.1)
        self.play(Write(gap), run_time=0.7)
        self.narrate("Thậm chí khoảng cách thẳng đứng giữa M và T còn có công thức rất đẹp: M T bằng một nửa bình phương hiệu a trừ b.", 1.4)

    # ======================================================
    # GEM 5: INVERSE AREA IDENTITY
    # ======================================================
    def gem5_inverse_area(self):
        self.show_problem(
            "Viên ngọc 5 – Một hình chữ nhật bị chia đúng thành hai tích phân",
            [
                mtx(r"f(x)=x^2,\qquad x\ge0", 42, GOLD),
                mtx(r"f^{-1}(x)=\sqrt{x}", 39, CYAN),
                mtx(r"a>0", 36, INK),
                "Tìm một đẳng thức diện tích nối f và hàm ngược của f.",
            ],
            "Đây là một bài hình học tích phân rất đẹp. Với hàm x bình phương trên nửa trục dương, hàm ngược là căn x. Ta sẽ cho điểm A chạy trên parabol, dựng hình chữ nhật có góc đối diện là A, rồi nhìn hai miền mà đường cong chia ra.",
            "5/6",
        )
        self.clear_stage(); self.add_header_footer("Viên ngọc 5", "Diện tích của hàm và hàm ngược bổ sung nhau", "5/6")
        ax, labels = self.make_axes(xr=(0,3,0.5), yr=(0,5.5,1), xlen=6.6, ylen=5.2, shift=LEFT*2.7)
        a = ValueTracker(1.35)
        curve_full = ax.plot(lambda x: x*x, x_range=[0,2.35], color=BLUE, stroke_width=4)
        A = always_redraw(lambda: Dot(ax.c2p(a.get_value(),a.get_value()**2), radius=0.08, color=GOLD))
        rect = always_redraw(lambda: Polygon(
            ax.c2p(0,0), ax.c2p(a.get_value(),0), ax.c2p(a.get_value(),a.get_value()**2), ax.c2p(0,a.get_value()**2),
            stroke_color=MUTED, stroke_width=2.2, fill_opacity=0
        ))
        def lower_region():
            aa=a.get_value(); xs=np.linspace(0,aa,45)
            pts=[ax.c2p(0,0)] + [ax.c2p(x,x*x) for x in xs] + [ax.c2p(aa,0)]
            poly=Polygon(*pts, stroke_opacity=0, fill_color=BLUE, fill_opacity=0.24)
            return poly
        def upper_region():
            aa=a.get_value(); xs=np.linspace(0,aa,45)
            pts=[ax.c2p(0,aa*aa),ax.c2p(aa,aa*aa)] + [ax.c2p(x,x*x) for x in xs[::-1]]
            poly=Polygon(*pts, stroke_opacity=0, fill_color=GREEN, fill_opacity=0.24)
            return poly
        low=always_redraw(lower_region); up=always_redraw(upper_region)
        guides = always_redraw(lambda: VGroup(
            DashedLine(ax.c2p(a.get_value(),0), A.get_center(), color=GOLD, dash_length=0.1),
            DashedLine(ax.c2p(0,a.get_value()**2), A.get_center(), color=GOLD, dash_length=0.1),
        ))
        formula = VGroup(
            mtx(r"\int_0^a x^2\,dx", 34, BLUE),
            mtx(r"+\int_0^{a^2}\sqrt{x}\,dx", 34, GREEN),
            mtx(r"=a\cdot a^2=a^3", 38, GOLD),
        ).arrange(DOWN,buff=0.32).to_edge(RIGHT,buff=0.5).shift(UP*0.65)
        check = VGroup(
            mtx(r"\frac{a^3}{3}+\frac{2a^3}{3}=a^3", 36, CYAN),
            mtx(r"\boxed{\int_0^a f+\int_0^{f(a)}f^{-1}=a f(a)}", 32, GOLD),
        ).arrange(DOWN,buff=0.32).to_edge(RIGHT,buff=0.30).shift(DOWN*1.25)
        self.play(Create(ax), FadeIn(labels), Create(curve_full), FadeIn(formula), FadeIn(check), run_time=1.1)
        self.play(FadeIn(low), FadeIn(up), Create(rect), FadeIn(A), FadeIn(guides), run_time=0.9)
        self.narrate_play(
            "Khi điểm A chạy lên parabol, hình chữ nhật thay đổi liên tục. Miền xanh dương là diện tích dưới đồ thị x bình phương. Miền xanh lá là phần còn lại, và nếu cắt theo phương ngang thì nó chính là tích phân của hàm ngược căn x.",
            a.animate.set_value(2.2), min_time=5.0,
        )
        self.narrate_play(
            "Hai miền luôn ghép vừa khít thành hình chữ nhật có chiều rộng a và chiều cao a bình phương. Vì thế tổng hai tích phân bằng a nhân f của a. Với f bằng x bình phương, ta được một phần ba a mũ ba cộng hai phần ba a mũ ba bằng đúng a mũ ba.",
            a.animate.set_value(1.55), min_time=4.5,
        )
        self.narrate("Đẳng thức này đúng rộng hơn cho các hàm một một, liên tục và tăng thích hợp. Đây là một công thức đẹp nối hình học, tích phân và hàm ngược.", 1.5)

    # ======================================================
    # GEM 6: x^x MINIMUM
    # ======================================================
    def gem6_x_pow_x(self):
        self.show_problem(
            "Viên ngọc 6 – Hàm số kỳ lạ x mũ x",
            [
                mtx(r"f(x)=x^x,\qquad x>0", 44, GOLD),
                "Đồ thị giảm rồi tăng dù cả cơ số và số mũ đều là x.",
                "Tìm giá trị nhỏ nhất bằng một cách thật gọn.",
            ],
            "Viên ngọc cuối là hàm x mũ x. Đây là một hàm rất lạ: khi x tăng từ gần không, hàm ban đầu lại giảm, rồi mới tăng rất nhanh. Ta sẽ cho một điểm chạy trên đồ thị để đoán vị trí thấp nhất, sau đó chứng minh bằng đạo hàm logarit.",
            "6/6",
        )
        self.clear_stage(); self.add_header_footer("Viên ngọc 6", "Điểm thấp nhất xuất hiện tại 1/e", "6/6")
        ax, labels = self.make_axes(xr=(0,3.1,0.5), yr=(0,6,1), xlen=6.8, ylen=5.2, shift=LEFT*2.65)
        curve = ax.plot(lambda x: x**x, x_range=[0.06,2.45], color=BLUE, stroke_width=4)
        x = ValueTracker(0.12)
        P = always_redraw(lambda: Dot(ax.c2p(x.get_value(), x.get_value()**x.get_value()), radius=0.08, color=GOLD))
        plab = always_redraw(lambda: mtx(r"P",24,GOLD).next_to(P,UR,buff=0.06))
        xmin=1/math.e; ymin=math.exp(-1/math.e)
        Q=Dot(ax.c2p(xmin,ymin), radius=0.085, color=RED)
        qlab=mtx(r"Q",24,RED).next_to(Q,DOWN,buff=0.07)
        deriv = VGroup(
            mtx(r"y=x^x", 34, INK),
            mtx(r"\ln y=x\ln x", 35, CYAN),
            mtx(r"\frac{y'}y=\ln x+1", 35, CYAN),
            mtx(r"y'=x^x(\ln x+1)", 37, GOLD),
            mtx(r"y'=0\iff x=\frac1e", 38, GREEN),
            mtx(r"\boxed{y_{\min}=e^{-1/e}}", 38, GOLD),
        ).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.40).shift(UP*0.15)
        self.play(Create(ax), FadeIn(labels), Create(curve), FadeIn(P), FadeIn(plab), FadeIn(deriv), FadeIn(Q), FadeIn(qlab), run_time=1.1)
        self.narrate_play(
            "Cho P chạy từ rất gần không sang phải. Các em sẽ thấy P đi xuống trước, chạm vùng thấp nhất, rồi mới bật lên và tăng nhanh. Điểm đỏ đánh dấu vị trí một trên e.",
            x.animate.set_value(2.3), min_time=5.0,
        )
        self.narrate_play(
            "Để đạo hàm x mũ x, ta không cần công thức phức tạp. Đặt y bằng x mũ x, lấy logarit hai vế: log y bằng x log x. Đạo hàm suy ra y phẩy trên y bằng log x cộng một. Vì x mũ x luôn dương, y phẩy bằng không đúng khi log x bằng âm một, tức x bằng một trên e.",
            x.animate.set_value(xmin), min_time=5.2,
        )
        self.narrate("Thay vào hàm, giá trị nhỏ nhất là e mũ âm một trên e. Một kết quả khá bất ngờ, nhưng lời giải chỉ cần đúng một phép lấy logarit.", 1.4)

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_stage(); self.add_header_footer("Bản đồ săn tính chất đẹp", "Đừng lao vào biến đổi trước khi nhìn cấu trúc", "Tổng kết")
        items = VGroup(
            VGroup(mtx(r"f(x)+f(-x)=K",31,BLUE), txt("→ nghĩ đến tâm đối xứng",25,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"x_1x_2=\mathrm{const}",31,CYAN), txt("→ nghĩ đến Viète và cặp nghịch đảo",25,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"x_1+x_2+x_3=0",31,GREEN), txt("→ nghĩ đến trung bình tọa độ",25,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"t_a,\ t_b",31,ORANGE), txt("→ thử tìm giao điểm hai tiếp tuyến",25,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"f^{-1}",31,PURPLE), txt("→ thử nhìn hình đối xứng và diện tích",25,INK)).arrange(RIGHT,buff=0.25),
            VGroup(mtx(r"x^x",31,GOLD), txt("→ logarit hóa trước khi đạo hàm",25,INK)).arrange(RIGHT,buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).shift(DOWN*0.1)
        fit_width(items, 11.7)
        for row in items:
            self.play(FadeIn(row, shift=RIGHT*0.12), run_time=0.34)
        self.narrate(
            "Điểm chung của sáu bài hôm nay là: không nên biến đổi máy móc ngay. Hãy nhìn xem có đối xứng, tổng nghiệm, tích nghiệm, trung điểm, hàm ngược hay phép logarit nào đang ẩn phía sau. Một cấu trúc đúng có thể rút một bài dài thành vài dòng.",
            1.8,
        )

        self.clear_stage()
        g=VGroup(
            txt("NHÌN HÌNH – ĐOÁN QUY LUẬT – CHỨNG MINH GỌN", 39, GOLD, BOLD),
            VGroup(txt("Đồ thị động", 26, CYAN), Arrow(LEFT*0.3,RIGHT*0.3,color=CYAN,stroke_width=3), txt("bất biến",26,GOLD,BOLD), Arrow(LEFT*0.3,RIGHT*0.3,color=CYAN,stroke_width=3), txt("lời giải đẹp",26,CYAN)).arrange(RIGHT,buff=0.16),
            txt("Thầy Nguyễn Văn Sang", 22, MUTED),
        ).arrange(DOWN,buff=0.38)
        self.play(FadeIn(g[0]), Write(g[1]), FadeIn(g[2]), run_time=1.0)
        self.narrate("Các em hãy tập thói quen dùng hình để phát hiện điều không đổi, rồi dùng đại số để chứng minh. Đó là một trong những cách học hàm số thú vị và sâu nhất ở phổ thông. Hẹn gặp các em ở phần tiếp theo của series những viên ngọc Toán học.", 1.8)

    def construct(self):
        self.intro()
        self.gem1_logistic()
        self.gem2_reciprocal()
        self.gem3_cubic_centroid()
        self.gem4_parabola_tangents()
        self.gem5_inverse_area()
        self.gem6_x_pow_x()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "tinh_chat_dep_la_ham_so_phan_2_1080p"
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
    master_wav = ROOT / "master_narration_tinh_chat_dep_phan_2.wav"
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

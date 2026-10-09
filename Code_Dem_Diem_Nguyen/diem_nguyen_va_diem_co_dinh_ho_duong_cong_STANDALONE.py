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

    def narrate_while(self, text, animation, min_hold=0.25, max_anim=4.2):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        rt = min(max(0.9, dur * 0.50), max_anim)
        self.play(animation, run_time=rt)
        if dur > rt:
            self.wait(dur - rt + min_hold)
        else:
            self.wait(min_hold)
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
        for m in group:
            self.play(FadeIn(m, shift=UP * 0.08), run_time=0.30)
        self.narrate(voice, 2.0)
        return VGroup(panel, group)

    def make_axes(self, xr=(-5, 6, 1), yr=(-5, 8, 1), xlen=6.6, ylen=5.2, shift=LEFT*2.6):
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
        t1 = txt("ĐIỂM NGUYÊN TRÊN ĐỒ THỊ", 46, GOLD, BOLD)
        t2 = txt("VÀ ĐIỂM CỐ ĐỊNH CỦA HỌ ĐƯỜNG CONG", 36, INK, BOLD)
        f = VGroup(
            mtx(r"(x,y)\in\mathbb Z^2", 39, CYAN),
            mtx(r"F(x,y,m)=0\quad\forall m", 39, BLUE),
        ).arrange(RIGHT, buff=0.65)
        sub = txt("Số học trên đồ thị  ↔  tham số trong họ đường cong", 27, MUTED)
        brand = txt(TEN_THAY, 22, MUTED)
        g = VGroup(t1, t2, f, sub, brand).arrange(DOWN, buff=0.28).move_to(ORIGIN)
        self.play(FadeIn(t1, shift=UP*0.2), run_time=0.6)
        self.play(FadeIn(t2), Write(f), run_time=1.0)
        self.play(FadeIn(sub), FadeIn(brand), run_time=0.5)
        self.narrate(
            "Chào các em. Hôm nay chúng ta học hai dạng bài rất đẹp và có liên hệ với nhau. Dạng thứ nhất là tìm hoặc đếm những điểm trên đồ thị hàm số mà cả hoành độ và tung độ đều là số nguyên. Dạng thứ hai là tìm những điểm cố định mà mọi đường cong trong một họ phụ thuộc tham số m đều đi qua. Thầy sẽ đi từ ví dụ rất đơn giản, rồi mới nâng dần đến hàm hữu tỉ và các họ đường thẳng, parabol, đường tròn. Mục tiêu là hiểu bản chất chứ không học mẹo rời rạc.",
            2.5,
        )

    # ======================================================
    # PART A - INTEGER POINTS
    # ======================================================
    def integer_point_definition(self):
        self.clear_stage()
        self.add_header_footer("Phần A – Điểm có tọa độ nguyên", "Điều kiện cốt lõi", "Phần A/2")
        g = VGroup(
            mtx(r"M(x,y)\in\mathbb Z^2", 44, GOLD),
            mtx(r"y=f(x)", 42, BLUE),
            mtx(r"\Longrightarrow\quad x\in\mathbb Z,\quad f(x)\in\mathbb Z", 42, CYAN),
        ).arrange(DOWN, buff=0.45).shift(UP*0.35)
        self.play(Write(g[0]), run_time=0.6)
        self.play(Write(g[1]), Write(g[2]), run_time=0.9)
        self.narrate(
            "Một điểm M có tọa độ nguyên khi cả x và y đều là số nguyên. Nếu M nằm trên đồ thị y bằng f của x, thì ta phải có x nguyên và đồng thời f của x cũng nguyên. Đây là câu hỏi số học nằm bên trong một bài hình học về đồ thị. Đặc biệt, nếu đồ thị trải dài vô hạn thì số điểm nguyên có thể là vô hạn; muốn đếm hữu hạn, đề thường giới hạn một đoạn hoặc hàm số có cấu trúc đặc biệt khiến chỉ có hữu hạn x phù hợp.",
            2.1,
        )
        note = VGroup(
            txt("Câu hỏi luôn là:", 27, MUTED),
            VGroup(txt("Khi", 27, INK), mtx(r"x\in\mathbb Z", 34, CYAN), txt("thì khi nào",27,INK), mtx(r"f(x)\in\mathbb Z",34,GOLD), txt("?",27,INK)).arrange(RIGHT,buff=0.14),
        ).arrange(DOWN,buff=0.25).shift(DOWN*1.25)
        self.play(FadeIn(note), run_time=0.6)

    def ex1_line_segment(self):
        self.show_problem(
            "Ví dụ 1 – Đếm điểm nguyên trên một đoạn đồ thị",
            [
                mtx(r"y=\frac{x}{2}+1", 42, GOLD),
                mtx(r"-4\le x\le6", 38, CYAN),
                "Đếm các điểm có tọa độ nguyên trên đoạn đồ thị này.",
            ],
            "Ví dụ đầu tiên rất nhẹ. Ta xét đồ thị y bằng x chia hai cộng một, nhưng chỉ trên đoạn từ x bằng âm bốn đến x bằng sáu. Vì x phải nguyên và y cũng phải nguyên, ta cần tìm những giá trị nguyên của x làm x chia hai là số nguyên.",
            "Ví dụ 1/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 1", "Điều kiện chẵn – lẻ", "Ví dụ 1/6")
        ax, labels = self.make_axes(xr=(-5,7,1), yr=(-2,6,1), xlen=7.2, ylen=5.1, shift=LEFT*2.5)
        graph = ax.plot(lambda x: x/2+1, x_range=[-4,6], color=BLUE, stroke_width=4)
        pts_data = [(-4,-1),(-2,0),(0,1),(2,2),(4,3),(6,4)]
        pts = VGroup(*[Dot(ax.c2p(x,y), radius=0.065, color=GOLD) for x,y in pts_data])
        side = VGroup(
            mtx(r"x\in\mathbb Z", 34, CYAN),
            mtx(r"\frac{x}{2}+1\in\mathbb Z", 34, INK),
            mtx(r"\Longleftrightarrow\ x\equiv0\pmod 2", 35, GOLD),
            mtx(r"x=-4,-2,0,2,4,6", 33, GREEN),
            mtx(r"\boxed{N=6}", 42, GOLD),
        ).arrange(DOWN, buff=0.26).to_edge(RIGHT, buff=0.35)
        self.play(Create(ax), FadeIn(labels), Create(graph), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.12), run_time=1.5)
        self.play(FadeIn(side), run_time=0.8)
        self.narrate(
            "Vì cộng một không làm thay đổi tính nguyên, điều kiện chỉ còn x chia hai phải nguyên. Nghĩa là x phải chẵn. Trong đoạn từ âm bốn đến sáu, các giá trị chẵn là âm bốn, âm hai, không, hai, bốn và sáu. Mỗi giá trị cho đúng một điểm trên đồ thị. Vậy có sáu điểm nguyên. Đây là dạng dễ nhất: dùng điều kiện chia hết hoặc chẵn lẻ.",
            2.0,
        )

    def rational_general_idea(self):
        self.clear_stage(); self.add_header_footer("Hàm hữu tỉ – Ý tưởng mạnh", "Chia đa thức để lộ điều kiện chia hết", "Phần A/2")
        g = VGroup(
            mtx(r"y=\frac{P(x)}{x-a}", 43, GOLD),
            mtx(r"P(x)=(x-a)Q(x)+P(a)", 40, BLUE),
            mtx(r"\frac{P(x)}{x-a}=Q(x)+\frac{P(a)}{x-a}", 40, CYAN),
            mtx(r"x\in\mathbb Z\ \Longrightarrow\ Q(x)\in\mathbb Z", 36, INK),
            mtx(r"y\in\mathbb Z\ \Longleftrightarrow\ x-a\mid P(a)", 43, GOLD),
        ).arrange(DOWN, buff=0.34).shift(UP*0.10)
        fit_width(g, 11.8)
        for mob in g:
            self.play(Write(mob), run_time=0.6)
        self.narrate(
            "Với hàm hữu tỉ có mẫu x trừ a, ta có một mẹo rất mạnh. Dùng phép chia đa thức, ta viết P của x bằng x trừ a nhân Q của x cộng P của a. Vì vậy y bằng Q của x cộng P của a chia x trừ a. Nếu P có hệ số nguyên và x là số nguyên, Q của x cũng nguyên. Do đó y nguyên khi và chỉ khi x trừ a là một ước của số nguyên P của a. Bài toán hình học đã biến thành bài toán tìm ước số.",
            2.2,
        )
        note = VGroup(
            txt("Nếu",26,INK), mtx(r"P(a)\ne0",34,ORANGE), txt("→ chỉ có hữu hạn ước → thường chỉ có hữu hạn điểm nguyên.",26,INK)
        ).arrange(RIGHT,buff=0.15).to_edge(DOWN,buff=0.75)
        fit_width(note, 11.7)
        self.play(FadeIn(note), run_time=0.5)

    def ex2_rational(self):
        self.show_problem(
            "Ví dụ 2 – Tìm toàn bộ điểm nguyên trên đồ thị hữu tỉ",
            [
                mtx(r"y=\frac{x^2+1}{x-1}", 44, GOLD),
                mtx(r"x\ne1", 34, RED),
                "Tìm tất cả các điểm có tọa độ nguyên trên đồ thị.",
            ],
            "Ta xét y bằng x bình phương cộng một chia cho x trừ một. Đề không giới hạn x, nhưng nhờ phép chia đa thức, số điểm nguyên vẫn hữu hạn. Ta sẽ biến biểu thức thành phần nguyên cộng một phân số nhỏ rồi dùng điều kiện chia hết.",
            "Ví dụ 2/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Từ đồ thị sang ước số", "Ví dụ 2/6")
        deriv = VGroup(
            mtx(r"x^2+1=(x-1)(x+1)+2", 38, BLUE),
            mtx(r"y=x+1+\frac{2}{x-1}", 42, CYAN),
            mtx(r"y\in\mathbb Z\Longleftrightarrow x-1\mid2", 40, GOLD),
            mtx(r"x-1\in\{-2,-1,1,2\}", 36, INK),
            mtx(r"x\in\{-1,0,2,3\}", 38, GREEN),
        ).arrange(DOWN,buff=0.30).shift(LEFT*2.6+UP*0.15)
        table = VGroup(
            mtx(r"(-1,-1)", 31, GOLD),
            mtx(r"(0,-1)", 31, GOLD),
            mtx(r"(2,5)", 31, GOLD),
            mtx(r"(3,5)", 31, GOLD),
            mtx(r"\boxed{N=4}", 40, GOLD),
        ).arrange(DOWN,buff=0.26).to_edge(RIGHT,buff=0.75)
        self.play(FadeIn(deriv), run_time=1.0)
        self.play(FadeIn(table), run_time=0.8)
        self.narrate(
            "Ta chia x bình phương cộng một cho x trừ một, được x cộng một và dư hai. Vậy y bằng x cộng một cộng hai chia x trừ một. Với x nguyên, x cộng một chắc chắn nguyên, nên y nguyên đúng khi hai chia x trừ một là số nguyên. Tức x trừ một phải là ước của hai: âm hai, âm một, một hoặc hai. Suy ra x bằng âm một, không, hai hoặc ba. Thay lại ta được bốn điểm nguyên: âm một âm một, không âm một, hai năm và ba năm.",
            2.3,
        )

        # graph illustration
        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Nhìn lại bốn điểm trên đồ thị", "Ví dụ 2/6")
        ax, labels = self.make_axes(xr=(-4,5,1), yr=(-5,8,1), xlen=6.7, ylen=5.2, shift=LEFT*2.5)
        g1 = ax.plot(lambda x:(x*x+1)/(x-1), x_range=[-4,0.90], color=BLUE, stroke_width=3.5)
        g2 = ax.plot(lambda x:(x*x+1)/(x-1), x_range=[1.10,4.5], color=BLUE, stroke_width=3.5)
        asym = DashedLine(ax.c2p(1,-5), ax.c2p(1,8), color=MUTED, dash_length=0.12)
        coords=[(-1,-1),(0,-1),(2,5),(3,5)]
        pts=VGroup(*[Dot(ax.c2p(x,y),radius=0.075,color=GOLD) for x,y in coords])
        labs=VGroup(*[mtx(rf"({x},{y})",25,GOLD).next_to(ax.c2p(x,y),UR,buff=0.06) for x,y in coords])
        side=VGroup(
            txt("Chỉ 4 điểm vàng có",26,INK),
            mtx(r"x,y\in\mathbb Z",36,CYAN),
            txt("trên toàn bộ đồ thị.",26,INK),
        ).arrange(DOWN,buff=0.20).to_edge(RIGHT,buff=0.45)
        self.play(Create(ax),FadeIn(labels),Create(g1),Create(g2),Create(asym),run_time=1.2)
        self.play(LaggedStart(*[FadeIn(p,scale=1.5) for p in pts],lag_ratio=0.15),FadeIn(labs),FadeIn(side),run_time=1.4)
        self.narrate(
            "Trên hình, đồ thị có vô số điểm thực, nhưng chỉ có bốn điểm vàng mà cả hai tọa độ đều nguyên. Đây là lý do ta không nên dò bằng mắt. Cấu trúc chia hết mới là công cụ chính xác và mạnh hơn nhiều.",
            1.5,
        )

    def partA_summary(self):
        self.clear_stage(); self.add_header_footer("Chốt phần A", "Ba câu hỏi trước khi đếm", "Phần A/2")
        steps=VGroup(
            bullet("1. Miền của x có bị giới hạn không?",INK,27,BLUE),
            bullet("2. Với x nguyên, điều kiện nào làm f(x) nguyên?",INK,27,CYAN),
            bullet("3. Có thể biến điều kiện thành chia hết, chẵn – lẻ hay ước số không?",INK,27,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.45).shift(UP*0.35)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.4)
        theorem=mtx(r"\frac{P(x)}{x-a}\in\mathbb Z\Longleftrightarrow x-a\mid P(a)",40,GREEN).shift(DOWN*1.25)
        fit_width(theorem,11.0)
        self.play(Write(theorem),run_time=0.8)
        self.narrate(
            "Kết thúc phần A, các em hãy luôn hỏi ba câu. Miền x có bị giới hạn hay không. Với x nguyên, điều kiện nào làm f của x nguyên. Và điều kiện đó có thể đưa về chia hết, chẵn lẻ hay tìm ước số không. Riêng dạng P của x chia x trừ a, công thức x trừ a chia hết P của a là một công cụ rất mạnh.",
            1.8,
        )

    # ======================================================
    # PART B - FIXED POINTS
    # ======================================================
    def fixed_definition(self):
        self.clear_stage(); self.add_header_footer("Phần B – Điểm cố định của họ đường cong", "Một điểm thuộc mọi thành viên của họ", "Phần B/2")
        g=VGroup(
            mtx(r"F(x,y,m)=0",44,BLUE),
            txt("Điểm cố định M phải thỏa phương trình",27,INK),
            mtx(r"\forall m",44,GOLD),
            mtx(r"F(x_M,y_M,m)\equiv0",42,CYAN),
        ).arrange(DOWN,buff=0.35).shift(UP*0.15)
        self.play(FadeIn(g[1]),Write(g[0]),Write(g[2]),Write(g[3]),run_time=1.2)
        self.narrate(
            "Bây giờ sang điểm cố định của một họ đường cong. Ta có một phương trình chứa tham số m. Một điểm M được gọi là điểm cố định nếu M nằm trên mọi đường cong của họ, bất kể m nhận giá trị nào. Nói cách khác, sau khi thay tọa độ của M vào phương trình, đẳng thức phải đúng với mọi m. Từ khóa quan trọng nhất là với mọi m.",
            2.0,
        )
        rule=VGroup(
            mtx(r"A(x,y)+mB(x,y)=0\quad\forall m",38,INK),
            mtx(r"\Longleftrightarrow\begin{cases}A(x,y)=0\\B(x,y)=0\end{cases}",42,GOLD),
        ).arrange(DOWN,buff=0.35).shift(DOWN*1.45)
        self.play(Write(rule),run_time=1.0)
        self.narrate(
            "Nếu phương trình có dạng A cộng m nhân B bằng không, muốn đúng với mọi m thì cả phần không chứa m và hệ số của m đều phải bằng không. Vì vậy bài điểm cố định thường biến thành một hệ phương trình không còn tham số.",
            1.5,
        )

    def ex3_lines(self):
        self.show_problem(
            "Ví dụ 3 – Họ đường thẳng",
            [
                mtx(r"d_m:\ y=(m+1)x+2m-1",42,GOLD),
                mtx(r"m\in\mathbb R",34,CYAN),
                "Tìm điểm cố định mà mọi đường thẳng của họ đều đi qua.",
            ],
            "Ta xét họ đường thẳng y bằng m cộng một nhân x cộng hai m trừ một. Mỗi giá trị m cho một đường thẳng khác nhau. Ta cần tìm điểm chung của tất cả các đường này, chứ không chỉ giao điểm của hai đường bất kỳ.",
            "Ví dụ 3/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Tách phần chứa m", "Ví dụ 3/6")
        deriv=VGroup(
            mtx(r"y=(m+1)x+2m-1",39,INK),
            mtx(r"y=x-1+m(x+2)",42,BLUE),
            mtx(r"y-(x-1)=m(x+2)",40,CYAN),
            mtx(r"\forall m\Rightarrow x+2=0",40,GOLD),
            mtx(r"x=-2,\qquad y=-3",42,GREEN),
            mtx(r"\boxed{M(-2,-3)}",46,GOLD),
        ).arrange(DOWN,buff=0.28).shift(LEFT*2.4)
        fit_width(deriv,7.2)
        self.play(FadeIn(deriv),run_time=1.0)
        self.narrate(
            "Ta gom các hạng tử theo m. Phương trình trở thành y bằng x trừ một cộng m nhân x cộng hai. Muốn cùng một điểm tồn tại với mọi m, hệ số của m phải bằng không, nên x cộng hai bằng không. Suy ra x bằng âm hai. Thay vào phần còn lại, y bằng x trừ một bằng âm ba. Vậy điểm cố định là M âm hai âm ba.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Nhìn họ đường thẳng cùng đi qua một điểm", "Ví dụ 3/6")
        ax,labels=self.make_axes(xr=(-5,4,1),yr=(-7,6,1),xlen=6.8,ylen=5.3,shift=LEFT*2.4)
        lines=VGroup()
        for mm,col in [(-2,PURPLE),(-1,CYAN),(0,BLUE),(1,GREEN),(2,ORANGE)]:
            lines.add(ax.plot(lambda x,mm=mm:(mm+1)*x+2*mm-1,x_range=[-5,4],color=col,stroke_width=3))
        p=Dot(ax.c2p(-2,-3),radius=0.09,color=GOLD)
        plab=mtx(r"M(-2,-3)",28,GOLD).next_to(p,UR,buff=0.08)
        self.play(Create(ax),FadeIn(labels),run_time=0.7)
        for ln in lines:self.play(Create(ln),run_time=0.32)
        self.play(FadeIn(p,scale=1.6),FadeIn(plab),run_time=0.6)
        self.narrate(
            "Trên hình, năm giá trị m tạo năm đường thẳng khác nhau, nhưng tất cả đều đi qua đúng điểm vàng M âm hai âm ba. Đây chính là ý nghĩa hình học của điểm cố định.",
            1.4,
        )

    def ex4_parabolas(self):
        self.show_problem(
            "Ví dụ 4 – Họ parabol",
            [
                mtx(r"(P_m):\ y=x^2+2x+3+m(x-1)",41,GOLD),
                "Tìm điểm cố định của họ parabol.",
            ],
            "Bây giờ thay đường thẳng bằng parabol. Họ parabol có phương trình y bằng x bình phương cộng hai x cộng ba cộng m nhân x trừ một. Dù hình dạng vẫn là parabol, tham số m làm vị trí và độ nghiêng thay đổi. Ta vẫn dùng đúng nguyên tắc: phương trình phải đúng với mọi m.",
            "Ví dụ 4/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 4", "Hệ số của m phải bằng 0", "Ví dụ 4/6")
        g=VGroup(
            mtx(r"y=x^2+2x+3+m(x-1)",39,INK),
            mtx(r"\forall m\Rightarrow x-1=0",40,GOLD),
            mtx(r"x=1",39,CYAN),
            mtx(r"y=1+2+3=6",40,GREEN),
            mtx(r"\boxed{M(1,6)}",46,GOLD),
        ).arrange(DOWN,buff=0.34).shift(LEFT*2.6)
        self.play(FadeIn(g),run_time=0.9)
        self.narrate(
            "Hệ số của m là x trừ một. Muốn điểm không phụ thuộc m, ta bắt buộc có x bằng một. Khi đó toàn bộ phần chứa m biến mất. Thay x bằng một vào phần còn lại, ta được y bằng sáu. Vậy mọi parabol trong họ đều đi qua điểm M một sáu.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ 4", "Nhiều parabol – một điểm chung", "Ví dụ 4/6")
        ax=Axes(x_range=[-4,4,1],y_range=[-5,13,2],x_length=6.5,y_length=5.3,tips=False,
                axis_config={"color":MUTED,"stroke_width":2,"include_numbers":True,"font_size":21}).shift(LEFT*2.4)
        labels=ax.get_axis_labels(mtx("x",27),mtx("y",27))
        curves=VGroup()
        for mm,col in [(-2,PURPLE),(-1,CYAN),(0,BLUE),(1,GREEN),(2,ORANGE)]:
            curves.add(ax.plot(lambda x,mm=mm:x*x+2*x+3+mm*(x-1),x_range=[-3.7,3.2],color=col,stroke_width=3))
        p=Dot(ax.c2p(1,6),radius=0.09,color=GOLD)
        lab=mtx(r"M(1,6)",28,GOLD).next_to(p,UR,buff=0.08)
        self.play(Create(ax),FadeIn(labels),run_time=0.7)
        for c in curves:self.play(Create(c),run_time=0.33)
        self.play(FadeIn(p,scale=1.6),FadeIn(lab),run_time=0.6)
        self.narrate(
            "Các parabol khác nhau khá rõ, nhưng tất cả đều xuyên qua cùng điểm M một sáu. Khi nhìn hình, các em hãy nhớ rằng điểm cố định không có nghĩa là đỉnh cố định hay trục đối xứng cố định; nó chỉ là điểm nằm trên mọi thành viên của họ.",
            1.5,
        )

    def ex5_circles(self):
        self.show_problem(
            "Ví dụ 5 – Họ đường tròn có hai điểm cố định",
            [
                mtx(r"(C_m):\ x^2+y^2-4+2m(x-y)=0",40,GOLD),
                "Tìm tất cả các điểm cố định của họ đường tròn.",
            ],
            "Ví dụ năm thú vị hơn vì họ đường tròn có thể có hai điểm cố định. Phương trình là x bình phương cộng y bình phương trừ bốn cộng hai m nhân x trừ y bằng không. Ta sẽ tách phần không chứa m và phần chứa m.",
            "Ví dụ 5/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 5", "Giải hệ hệ số theo m", "Ví dụ 5/6")
        sys1=mtx(r"\begin{cases}x^2+y^2-4=0\\x-y=0\end{cases}",48,GOLD)
        arr=mtx(r"x=y\Rightarrow2x^2=4\Rightarrow x=\pm\sqrt2",40,CYAN)
        ans=mtx(r"\boxed{M_1(\sqrt2,\sqrt2),\quad M_2(-\sqrt2,-\sqrt2)}",39,GREEN)
        g=VGroup(sys1,arr,ans).arrange(DOWN,buff=0.48).shift(UP*0.15)
        fit_width(g,11.4)
        self.play(Write(sys1),run_time=0.8)
        self.play(Write(arr),run_time=0.8)
        self.play(Write(ans),run_time=1.0)
        self.narrate(
            "Muốn đúng với mọi m, ta cần đồng thời x bình phương cộng y bình phương trừ bốn bằng không và x trừ y bằng không. Từ x bằng y, thay vào phương trình đường tròn tâm O bán kính hai, ta được hai x bình phương bằng bốn. Suy ra x bằng cộng hoặc trừ căn hai. Vậy họ có hai điểm cố định: căn hai căn hai và âm căn hai âm căn hai.",
            2.0,
        )
        note=VGroup(txt("Hai điểm cố định này",26,INK),mtx(r"\notin\mathbb Z^2",36,RED),txt("nên không phải điểm nguyên.",26,INK)).arrange(RIGHT,buff=0.14).shift(DOWN*1.7)
        self.play(FadeIn(note),run_time=0.5)
        self.narrate(
            "Một liên hệ đẹp với phần A: hai điểm cố định này không có tọa độ nguyên vì căn hai không nguyên. Điểm cố định và điểm nguyên là hai tính chất hoàn toàn khác nhau; đôi khi một điểm có cả hai tính chất, đôi khi không.",
            1.5,
        )

        # circle visualization
        self.clear_stage(); self.add_header_footer("Ví dụ 5", "Các đường tròn cùng đi qua hai điểm", "Ví dụ 5/6")
        ax,labels=self.make_axes(xr=(-5,5,1),yr=(-5,5,1),xlen=6.4,ylen=5.3,shift=LEFT*2.4)
        circles=VGroup()
        for mm,col in [(-1.5,PURPLE),(-0.75,CYAN),(0,BLUE),(0.75,GREEN),(1.5,ORANGE)]:
            center=(-mm,mm); rad=math.sqrt(4+2*mm*mm)
            cir=ParametricFunction(lambda t,c=center,r=rad:ax.c2p(c[0]+r*math.cos(t),c[1]+r*math.sin(t)),t_range=[0,TAU],color=col,stroke_width=3)
            circles.add(cir)
        s2=math.sqrt(2)
        p1=Dot(ax.c2p(s2,s2),radius=0.08,color=GOLD); p2=Dot(ax.c2p(-s2,-s2),radius=0.08,color=GOLD)
        l1=mtx(r"M_1",27,GOLD).next_to(p1,UR,buff=0.06); l2=mtx(r"M_2",27,GOLD).next_to(p2,DL,buff=0.06)
        self.play(Create(ax),FadeIn(labels),run_time=0.7)
        for c in circles:self.play(Create(c),run_time=0.32)
        self.play(FadeIn(p1),FadeIn(p2),FadeIn(l1),FadeIn(l2),run_time=0.5)
        self.narrate(
            "Trên hình, các đường tròn có tâm và bán kính khác nhau, nhưng chúng luôn cùng đi qua hai điểm vàng. Một họ đường cong hoàn toàn có thể có nhiều hơn một điểm cố định.",
            1.4,
        )

    def ex6_quadratic_parameter(self):
        self.show_problem(
            "Ví dụ 6 – Khi phương trình chứa cả m và m²",
            [
                mtx(r"y=x^2+m(x-1)+m^2(x+1)",39,GOLD),
                "Họ đường cong có điểm cố định hay không?",
            ],
            "Ví dụ cuối nâng cao thêm một bước. Phương trình chứa cả m và m bình phương. Khi đó không chỉ một hệ số mà tất cả các hệ số theo từng lũy thừa của m đều phải bằng không. Đây là nguyên tắc tổng quát cần nhớ.",
            "Ví dụ 6/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 6", "Đồng nhất thức theo m", "Ví dụ 6/6")
        g=VGroup(
            mtx(r"y-x^2=m(x-1)+m^2(x+1)",38,INK),
            mtx(r"\forall m\Rightarrow\begin{cases}x-1=0\\x+1=0\end{cases}",43,GOLD),
        ).arrange(DOWN,buff=0.45).shift(UP*0.25)
        no=VGroup(mtx(r"\varnothing",46,RED),txt("Không có điểm cố định",30,RED,BOLD)).arrange(RIGHT,buff=0.25)
        g.add(no)
        self.play(FadeIn(g),run_time=1.0)
        self.narrate(
            "Muốn phương trình đúng với mọi m, hệ số của m phải bằng không và hệ số của m bình phương cũng phải bằng không. Ta cần đồng thời x bằng một và x bằng âm một, điều này không thể xảy ra. Vì vậy họ đường cong này không có điểm cố định. Khi có nhiều lũy thừa của m, các em phải cho tất cả hệ số bằng không, không được chỉ xét hệ số của m.",
            2.0,
        )

    def general_rule(self):
        self.clear_stage(); self.add_header_footer("Công thức tổng quát cho điểm cố định", "So hệ số theo m", "Tổng kết")
        g=VGroup(
            mtx(r"F(x,y,m)=A_0(x,y)+A_1(x,y)m+\cdots+A_n(x,y)m^n",36,BLUE),
            mtx(r"F(x,y,m)\equiv0\quad\forall m",39,GOLD),
            mtx(r"\Longleftrightarrow\quad A_0=A_1=\cdots=A_n=0",42,GREEN),
        ).arrange(DOWN,buff=0.50).shift(UP*0.25)
        fit_width(g,11.8)
        for m in g:self.play(Write(m),run_time=0.75)
        self.narrate(
            "Nguyên tắc tổng quát là thế này. Nếu phương trình của họ là một đa thức theo m, muốn một điểm thuộc mọi đường cong thì sau khi thay tọa độ điểm đó vào, biểu thức theo m phải bằng không với mọi m. Một đa thức bằng không với mọi m khi và chỉ khi tất cả các hệ số của nó bằng không. Vì vậy ta lập hệ: A không bằng không, A một bằng không, và tiếp tục như vậy cho đến A n bằng không.",
            2.0,
        )

    def mistakes_and_challenge(self):
        self.clear_stage(); self.add_header_footer("Những lỗi rất hay gặp", "Đừng nhầm hai dạng bài", "Tổng kết")
        errs=VGroup(
            bullet("Điểm nguyên: quên kiểm tra cả x và y đều nguyên.",RED,26,RED),
            bullet("Hàm hữu tỉ: thử vài x rồi kết luận, thay vì dùng chia hết.",RED,26,ORANGE),
            bullet("Điểm cố định: chỉ giao hai đường cong rồi tưởng đã đủ.",RED,26,RED),
            bullet("Phương trình có m²: chỉ cho hệ số của m bằng 0.",RED,26,ORANGE),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.38).shift(UP*0.2)
        for e in errs:self.play(FadeIn(e,shift=RIGHT*0.12),run_time=0.36)
        self.narrate(
            "Có bốn lỗi thầy muốn các em tránh. Điểm nguyên thì phải kiểm tra cả hai tọa độ. Hàm hữu tỉ không nên dò vài giá trị x rồi đoán. Điểm cố định không phải đơn giản là giao điểm của hai thành viên bất kỳ, trừ khi ta đã chứng minh điều đó đủ. Và nếu phương trình có m bình phương hoặc bậc cao hơn, phải xét tất cả các hệ số theo m.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài thử thách cuối", "Kết nối hai phần", "Tự luyện")
        q=VGroup(
            mtx(r"d_m:\ y=(m+1)x+2m-1",40,GOLD),
            txt("1. Tìm điểm cố định của họ.",27,INK),
            txt("2. Điểm đó có phải điểm nguyên không?",27,INK),
            txt("3. Giải thích vì sao mọi đường thẳng đều đi qua điểm đó.",27,CYAN),
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate(
            "Bài thử thách cuối video quay lại họ đường thẳng ban đầu. Hãy tự tìm điểm cố định, kiểm tra xem điểm đó có tọa độ nguyên hay không, rồi giải thích bằng hệ số của m. Các em hãy dừng video vài giây trước khi xem đáp án.",
            1.7,
        )
        self.wait(1.0)
        ans=VGroup(
            mtx(r"M(-2,-3)",42,GOLD),
            mtx(r"M\in\mathbb Z^2",40,GREEN),
            mtx(r"x+2=0",36,CYAN),
        ).arrange(DOWN,buff=0.28).shift(DOWN*1.55)
        self.play(FadeIn(ans),run_time=0.7)
        self.narrate(
            "Đáp án là M âm hai âm ba. Đây vừa là điểm cố định của cả họ, vừa là một điểm có tọa độ nguyên. Lý do là tại x bằng âm hai, hệ số của m bằng không nên tung độ không còn phụ thuộc m nữa.",
            1.5,
        )

    def outro(self):
        self.clear_stage()
        g=VGroup(
            txt("CHỐT LẠI",44,GOLD,BOLD),
            VGroup(mtx(r"x\in\mathbb Z",34,CYAN),txt("+",28,MUTED),mtx(r"f(x)\in\mathbb Z",34,CYAN),txt("→ điểm nguyên",27,INK)).arrange(RIGHT,buff=0.14),
            VGroup(mtx(r"F(x,y,m)\equiv0\ \forall m",34,BLUE),txt("→ điểm cố định",27,INK)).arrange(RIGHT,buff=0.18),
            txt("Một bên là số học của tọa độ, một bên là tính bất biến theo tham số.",27,MUTED),
            txt(TEN_THAY,22,MUTED),
        ).arrange(DOWN,buff=0.32)
        fit_width(g,12.0)
        self.play(FadeIn(g),run_time=1.0)
        self.narrate(
            "Chốt lại, bài điểm nguyên hỏi khi nào tọa độ của một điểm trên đồ thị thuộc tập số nguyên. Bài điểm cố định hỏi khi nào một điểm không thay đổi dù tham số m thay đổi. Một bên là số học của tọa độ, một bên là tính bất biến theo tham số. Khi hiểu đúng bản chất này, các dạng bài tưởng rời rạc sẽ trở nên rất hệ thống. Hẹn gặp các em ở video tiếp theo.",
            2.0,
        )

    def construct(self):
        self.intro()
        self.integer_point_definition()
        self.ex1_line_segment()
        self.rational_general_idea()
        self.ex2_rational()
        self.partA_summary()
        self.fixed_definition()
        self.ex3_lines()
        self.ex4_parabolas()
        self.ex5_circles()
        self.ex6_quadratic_parameter()
        self.general_rule()
        self.mistakes_and_challenge()
        self.outro()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "diem_nguyen_va_diem_co_dinh_1080p"
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
    master_wav = ROOT / "master_narration_integer_fixed.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    # final verification
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

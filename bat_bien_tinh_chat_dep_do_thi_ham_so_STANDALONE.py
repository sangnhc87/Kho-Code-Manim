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
        t1 = txt("BẤT BIẾN TRÊN ĐỒ THỊ HÀM SỐ", 46, GOLD, BOLD)
        t2 = txt("NHỮNG TÍNH CHẤT ĐẸP ẨN SAU THAM SỐ", 34, INK, BOLD)
        f = VGroup(
            VGroup(txt("Tham số", 28, INK), mtx(r"m", 36, BLUE), txt("thay đổi", 28, INK)).arrange(RIGHT, buff=0.14),
            mtx(r"\Longrightarrow", 38, MUTED),
            txt("vẫn có cấu trúc bất biến", 28, GOLD, BOLD),
        ).arrange(RIGHT, buff=0.30)
        sub = txt("Điểm – trung điểm – tâm đối xứng – tiếp tuyến – diện tích", 27, CYAN)
        brand = txt(TEN_THAY, 22, MUTED)
        g = VGroup(t1, t2, f, sub, brand).arrange(DOWN, buff=0.28).move_to(ORIGIN)
        self.play(FadeIn(t1, shift=UP*0.2), run_time=0.6)
        self.play(FadeIn(t2), FadeIn(f), run_time=1.0)
        self.play(FadeIn(sub), FadeIn(brand), run_time=0.5)
        self.narrate(
            "Chào các em. Trong các bài toán có tham số, ta thường bị cuốn vào câu hỏi đồ thị thay đổi như thế nào. Nhưng có một cách nhìn sâu hơn: khi tham số thay đổi, có những đại lượng hoặc cấu trúc vẫn hoàn toàn không đổi. Đó là bất biến. Một điểm có thể đứng yên trong khi cả họ đường cong chuyển động. Một trung điểm có thể cố định dù hai giao điểm chạy qua chạy lại. Một tâm đối xứng, một tiếp tuyến, thậm chí một diện tích có thể bất biến. Video này sẽ giúp các em nhận ra những cấu trúc đẹp ấy bằng cả hình học và đại số.",
            2.5,
        )

    def invariant_idea(self):
        self.clear_stage(); self.add_header_footer("Bất biến là gì?", "Tách cái thay đổi khỏi cái không đổi", "Phần 1/7")
        g = VGroup(
            VGroup(txt("Tham số",27,INK), mtx(r"m",38,BLUE), txt("thay đổi",27,INK)).arrange(RIGHT,buff=0.18),
            mtx(r"\Downarrow",36,MUTED),
            VGroup(txt("Đồ thị",27,INK), mtx(r"C_m",38,CYAN), txt("thay đổi",27,INK)).arrange(RIGHT,buff=0.18),
            mtx(r"\Downarrow",36,MUTED),
            VGroup(txt("Nhưng có thể",27,INK), mtx(r"I,\ d,\ T,\ S",38,GOLD), txt("không đổi",27,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,buff=0.25).shift(LEFT*2.9)
        keys = VGroup(
            VGroup(mtx(r"I",34,GOLD),txt("điểm / trung điểm / tâm",25,INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"d",34,GOLD),txt("đường thẳng / trục / tiệm cận",25,INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"T",34,GOLD),txt("tiếp tuyến chung",25,INK)).arrange(RIGHT,buff=0.22),
            VGroup(mtx(r"S",34,GOLD),txt("diện tích hoặc tích phân",25,INK)).arrange(RIGHT,buff=0.22),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.35).to_edge(RIGHT,buff=0.55)
        self.play(FadeIn(g),FadeIn(keys),run_time=0.9)
        self.narrate(
            "Ta gọi một đối tượng là bất biến nếu nó không phụ thuộc vào tham số, dù bản thân đồ thị có thay đổi. Khi gặp một họ hàm số, các em nên tập thói quen hỏi: có điểm nào không chuyển động không; có đường nào luôn giữ nguyên không; có tâm đối xứng hay trung điểm nào cố định không; có tiếp tuyến nào mà mọi đồ thị cùng tiếp xúc không; hoặc có một tổng, tích phân hay diện tích nào mà phần phụ thuộc m tự triệt tiêu không. Đó là tư duy săn bất biến.",
            2.0,
        )

    # ======================================================
    # EXAMPLE 1 - HORIZONTAL TRANSLATION
    # ======================================================
    def ex1_minimum(self):
        self.show_problem(
            "Ví dụ 1 – Giá trị nhỏ nhất bất biến",
            [
                mtx(r"(P_m):\ y=(x-m)^2+1", 43, GOLD),
                mtx(r"m\in\mathbb R", 34, CYAN),
                "Khi m thay đổi, đại lượng nào của parabol vẫn giữ nguyên?",
            ],
            "Ta bắt đầu bằng một họ parabol rất trực quan: y bằng x trừ m tất cả bình phương cộng một. Tham số m chỉ làm parabol trượt sang trái hoặc sang phải. Hãy nhìn xem trong sự chuyển động đó có điều gì tuyệt đối không thay đổi.",
            "Ví dụ 1/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 1", "Tịnh tiến ngang nhưng độ cao đáy không đổi", "Ví dụ 1/6")
        ax,labels=self.make_axes(xr=(-5,6,1),yr=(-1,8,1),xlen=7.3,ylen=5.2,shift=LEFT*2.5)
        ms=[-2,0,2,4]
        cols=[PURPLE,BLUE,GREEN,ORANGE]
        curves=VGroup()
        vertices=VGroup()
        for mm,col in zip(ms,cols):
            curves.add(ax.plot(lambda x,mm=mm:(x-mm)**2+1,x_range=[mm-2.3,mm+2.3],color=col,stroke_width=3.2))
            vertices.add(Dot(ax.c2p(mm,1),radius=0.075,color=GOLD))
        base_line=DashedLine(ax.c2p(-5,1),ax.c2p(6,1),color=GOLD,dash_length=0.12)
        side=VGroup(
            mtx(r"V_m(m,1)",36,GOLD),
            mtx(r"y_{\min}=1",40,GREEN),
            mtx(r"V_m\in d:\ y=1",36,CYAN),
        ).arrange(DOWN,buff=0.34).to_edge(RIGHT,buff=0.55)
        self.play(Create(ax),FadeIn(labels),Create(base_line),run_time=0.8)
        for c,v in zip(curves,vertices):
            self.play(Create(c),FadeIn(v,scale=1.5),run_time=0.42)
        self.play(FadeIn(side),run_time=0.7)
        self.narrate(
            "Viết ở dạng bình phương hoàn chỉnh, ta thấy ngay đỉnh của parabol là V m có tọa độ m, một. Khi m thay đổi, hoành độ đỉnh thay đổi, nhưng tung độ đỉnh luôn bằng một. Vì bình phương luôn không âm, giá trị nhỏ nhất của hàm số luôn bằng một. Như vậy có hai cách nói cùng một bất biến: giá trị nhỏ nhất là một, và toàn bộ các đỉnh chạy trên đường thẳng cố định y bằng một. Đây là bất biến sinh ra từ phép tịnh tiến ngang.",
            2.0,
        )
        rule=VGroup(
            txt("Mẫu nhận biết:",26,GOLD,BOLD),
            mtx(r"f_m(x)=g(x-m)+c",38,BLUE),
            txt("hình dạng giữ nguyên, đồ thị chỉ trượt theo phương ngang.",25,INK),
        ).arrange(DOWN,buff=0.22).to_edge(DOWN,buff=0.55)
        self.play(FadeIn(rule),run_time=0.6)

    # ======================================================
    # EXAMPLE 2 - FIXED MIDPOINT OF ROOTS
    # ======================================================
    def ex2_midpoint(self):
        self.show_problem(
            "Ví dụ 2 – Trung điểm hai giao điểm luôn cố định",
            [
                mtx(r"(P_m):\ y=x^2-4x+m", 43, GOLD),
                "Giả sử parabol cắt trục Ox tại A và B.",
                "Chứng minh trung điểm của AB không phụ thuộc m.",
            ],
            "Ví dụ hai sâu hơn. Hai giao điểm A và B với trục hoành sẽ thay đổi khi m thay đổi. Nhưng đề yêu cầu ta tìm một thứ không thay đổi: trung điểm của đoạn A B. Đây là lúc định lý Viète cho ta một lời giải rất gọn.",
            "Ví dụ 2/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Hai đầu mút chạy, trung điểm đứng yên", "Ví dụ 2/6")
        deriv=VGroup(
            mtx(r"x^2-4x+m=0",39,INK),
            mtx(r"x_1+x_2=4",42,BLUE),
            mtx(r"x_I=\frac{x_1+x_2}{2}=2",42,GOLD),
            mtx(r"\boxed{I(2,0)}",46,GOLD),
            mtx(r"\Delta=16-4m\ge0\Longleftrightarrow m\le4",34,CYAN),
        ).arrange(DOWN,buff=0.31).shift(LEFT*2.7)
        side=VGroup(
            txt("Điều kiện có A, B thực:",24,MUTED),
            mtx(r"m\le4",38,CYAN),
            txt("Tại m = 4:",24,MUTED),
            txt("A và B nhập lại thành I.",24,INK),
        ).arrange(DOWN,buff=0.20).to_edge(RIGHT,buff=0.65)
        self.play(FadeIn(deriv),FadeIn(side),run_time=0.9)
        self.narrate(
            "Giao điểm với trục hoành là nghiệm của phương trình x bình phương trừ bốn x cộng m bằng không. Theo Viète, tổng hai nghiệm luôn bằng bốn, hoàn toàn không chứa m. Vì vậy hoành độ trung điểm bằng nửa tổng hai nghiệm, tức bằng hai. Tung độ của A và B đều bằng không nên trung điểm cố định là I hai không. Ta cũng phải nói rõ điều kiện: hai giao điểm thực tồn tại khi m nhỏ hơn hoặc bằng bốn. Tại m bằng bốn, hai điểm nhập lại đúng tại I.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ 2", "Quan sát nhiều parabol cùng lúc", "Ví dụ 2/6")
        ax,labels=self.make_axes(xr=(-1,5,1),yr=(-7,7,1),xlen=6.8,ylen=5.25,shift=LEFT*2.5)
        ms=[-3,0,3,4]
        cols=[PURPLE,BLUE,GREEN,ORANGE]
        curves=VGroup()
        chords=VGroup()
        for mm,col in zip(ms,cols):
            curves.add(ax.plot(lambda x,mm=mm:x*x-4*x+mm,x_range=[-0.5,4.5],color=col,stroke_width=3))
            d=16-4*mm
            if d>=0:
                r1=(4-math.sqrt(d))/2
                r2=(4+math.sqrt(d))/2
                if abs(r2-r1) < 1e-9:
                    chords.add(Dot(ax.c2p(2,0), radius=0.07, color=col))
                else:
                    chords.add(Line(ax.c2p(r1,0),ax.c2p(r2,0),color=col,stroke_width=5).set_opacity(0.7))
        I=Dot(ax.c2p(2,0),radius=0.10,color=GOLD)
        Ilab=mtx(r"I(2,0)",29,GOLD).next_to(I,UR,buff=0.08)
        self.play(Create(ax),FadeIn(labels),run_time=0.7)
        for c,ch in zip(curves,chords):
            self.play(Create(c),Create(ch),run_time=0.36)
        self.play(FadeIn(I,scale=1.6),FadeIn(Ilab),run_time=0.5)
        self.narrate(
            "Trên hình, mỗi màu cho một parabol và một đoạn A B khác nhau. Khi m tăng, hai giao điểm tiến dần vào nhau. Nhưng điểm vàng I hai không luôn là trung điểm của mọi đoạn A B. Hình học đang minh họa đúng điều Viète đã chứng minh đại số.",
            1.6,
        )

    # ======================================================
    # EXAMPLE 3 - HOMOGRAPHIC CENTER
    # ======================================================
    def ex3_homographic(self):
        self.show_problem(
            "Ví dụ 3 – Tâm đối xứng cố định của họ hàm phân thức",
            [
                mtx(r"(H_m):\ y=\frac{2x+m}{x-1}", 43, GOLD),
                mtx(r"m\ne-2",34,CYAN),
                "Chứng minh mọi đồ thị đều có cùng một tâm đối xứng.",
            ],
            "Ta chuyển sang một họ hàm phân thức bậc nhất trên bậc nhất. Nhìn trực tiếp biểu thức chưa thấy bất biến. Nhưng chỉ cần chia tử cho mẫu, hai tiệm cận sẽ xuất hiện ngay, và giao điểm của chúng chính là tâm đối xứng.",
            "Ví dụ 3/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Chia để lộ hai tiệm cận bất biến", "Ví dụ 3/6")
        deriv=VGroup(
            mtx(r"\frac{2x+m}{x-1}=2+\frac{m+2}{x-1}",40,BLUE),
            mtx(r"x=1",40,CYAN),
            mtx(r"y=2",40,GREEN),
            mtx(r"\boxed{I(1,2)}",46,GOLD),
        ).arrange(DOWN,buff=0.34).shift(LEFT*2.8)
        explain=VGroup(
            txt("Hai tiệm cận",25,INK),
            txt("không phụ thuộc m.",25,GOLD,BOLD),
            txt("Giao điểm của chúng",25,INK),
            txt("là tâm đối xứng.",25,INK),
        ).arrange(DOWN,buff=0.20).to_edge(RIGHT,buff=0.85)
        self.play(FadeIn(deriv),FadeIn(explain),run_time=0.9)
        self.narrate(
            "Ta viết hàm số thành hai cộng m cộng hai chia x trừ một. Tiệm cận đứng luôn là x bằng một, còn tiệm cận ngang luôn là y bằng hai. Cả hai đều không chứa m. Đồ thị dạng y bằng hai cộng một hằng số chia x trừ một là một hyperbol nhận giao điểm hai tiệm cận làm tâm đối xứng. Vì vậy mọi đồ thị trong họ đều có chung tâm I một hai. Trường hợp m bằng âm hai bị suy biến thành đường thẳng y bằng hai với một điểm khuyết, nên ta tách riêng.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ 3", "Nhiều hyperbol – một tâm duy nhất", "Ví dụ 3/6")
        ax,labels=self.make_axes(xr=(-5,6,1),yr=(-7,9,1),xlen=7.0,ylen=5.25,shift=LEFT*2.5)
        vx=DashedLine(ax.c2p(1,-7),ax.c2p(1,9),color=CYAN,dash_length=0.12)
        hy=DashedLine(ax.c2p(-5,2),ax.c2p(6,2),color=GREEN,dash_length=0.12)
        curves=VGroup()
        for mm,col in [(-6,PURPLE),(-4,BLUE),(0,GREEN),(3,ORANGE)]:
            curves.add(ax.plot(lambda x,mm=mm:(2*x+mm)/(x-1),x_range=[-5,0.78],color=col,stroke_width=2.8))
            curves.add(ax.plot(lambda x,mm=mm:(2*x+mm)/(x-1),x_range=[1.22,6],color=col,stroke_width=2.8))
        I=Dot(ax.c2p(1,2),radius=0.10,color=GOLD)
        lab=mtx(r"I(1,2)",29,GOLD).next_to(I,UR,buff=0.08)
        self.play(Create(ax),FadeIn(labels),Create(vx),Create(hy),run_time=0.8)
        self.play(LaggedStart(*[Create(c) for c in curves],lag_ratio=0.08),run_time=2.2)
        self.play(FadeIn(I,scale=1.6),FadeIn(lab),run_time=0.5)
        self.narrate(
            "Các hyperbol đổi độ mở và đổi vị trí các nhánh khi m thay đổi, nhưng hai đường tiệm cận không nhúc nhích. Vì thế tâm đối xứng I cũng đứng yên. Đây là một ví dụ rất đẹp: bất biến không nhất thiết là một điểm nằm trên đồ thị; nó có thể là một đặc trưng hình học của đồ thị.",
            1.7,
        )

    # ======================================================
    # EXAMPLE 4 - CUBIC FIXED CENTER
    # ======================================================
    def ex4_cubic(self):
        self.show_problem(
            "Ví dụ 4 – Tâm đối xứng cố định của họ hàm bậc ba",
            [
                mtx(r"(C_m):\ y=x^3-3x^2+mx+2-m", 41, GOLD),
                "Chứng minh mọi đồ thị trong họ đều nhận cùng một điểm làm tâm đối xứng.",
            ],
            "Bài bậc ba thường làm học sinh ngại vì biểu thức dài. Nhưng nếu ta đoán đúng tâm và đổi biến quanh tâm đó, cấu trúc trở nên rất trong sáng. Ở đây hệ số của x bình phương gợi cho ta hoành độ đặc biệt x bằng một.",
            "Ví dụ 4/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 4", "Đổi biến quanh điểm nghi ngờ là tâm", "Ví dụ 4/6")
        deriv=VGroup(
            mtx(r"x=1+t",38,CYAN),
            mtx(r"f_m(1+t)=t^3+(m-3)t",40,BLUE),
            mtx(r"f_m(1-t)=-t^3-(m-3)t",40,BLUE),
            mtx(r"f_m(1+t)+f_m(1-t)=0",42,GREEN),
            mtx(r"\boxed{I(1,0)}",47,GOLD),
        ).arrange(DOWN,buff=0.31).shift(LEFT*2.4)
        rule=VGroup(
            txt("Điều kiện tâm đối xứng",24,MUTED),
            mtx(r"f(a+t)+f(a-t)=2b",35,GOLD),
            mtx(r"I(a,b)",34,CYAN),
        ).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.55)
        self.play(FadeIn(deriv),FadeIn(rule),run_time=0.9)
        self.narrate(
            "Đặt x bằng một cộng t. Sau khi rút gọn, mọi hạng tử bậc hai và hằng số biến mất, còn lại t mũ ba cộng m trừ ba nhân t. Đây là một hàm lẻ theo t. Thay t bởi âm t thì giá trị đổi dấu. Vì vậy f của một cộng t cộng f của một trừ t luôn bằng không. Theo tiêu chuẩn đối xứng tâm, mọi đồ thị đều nhận I một không làm tâm. Điều đẹp ở đây là tham số m vẫn còn trong biểu thức, nhưng nó nằm trong một hạng lẻ nên không phá vỡ đối xứng.",
            2.3,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ 4", "Các đường bậc ba cùng quay quanh I", "Ví dụ 4/6")
        ax,labels=self.make_axes(xr=(-2,4,1),yr=(-10,10,2),xlen=6.7,ylen=5.2,shift=LEFT*2.5)
        curves=VGroup()
        for mm,col in [(-1,PURPLE),(1,BLUE),(3,GREEN),(5,ORANGE)]:
            curves.add(ax.plot(lambda x,mm=mm:x**3-3*x*x+mm*x+2-mm,x_range=[-1.2,3.2],color=col,stroke_width=3))
        I=Dot(ax.c2p(1,0),radius=0.10,color=GOLD)
        lab=mtx(r"I(1,0)",29,GOLD).next_to(I,UR,buff=0.08)
        self.play(Create(ax),FadeIn(labels),run_time=0.7)
        self.play(LaggedStart(*[Create(c) for c in curves],lag_ratio=0.16),run_time=2.0)
        self.play(FadeIn(I,scale=1.6),FadeIn(lab),run_time=0.5)
        self.narrate(
            "Trên hình, hình dạng của các đường bậc ba khác nhau khá rõ, nhưng tất cả đều có cùng tâm đối xứng I một không. Nếu ta lấy hai điểm trên cùng một đồ thị có hoành độ cách một một khoảng t về hai phía, hai điểm ấy sẽ đối xứng nhau qua I.",
            1.6,
        )

    # ======================================================
    # EXAMPLE 5 - COMMON TANGENT
    # ======================================================
    def ex5_tangent(self):
        self.show_problem(
            "Ví dụ 5 – Một tiếp tuyến chung bất biến",
            [
                mtx(r"f_m(x)=x^2+m(x-1)^2", 43, GOLD),
                "Chứng minh mọi đồ thị đi qua cùng một điểm và có cùng tiếp tuyến tại điểm đó.",
            ],
            "Đây là một bất biến mạnh hơn điểm cố định. Không chỉ mọi đồ thị cùng đi qua một điểm, mà tại điểm đó chúng còn có cùng hướng tiếp xúc. Để chứng minh, ta phải kiểm tra đồng thời giá trị hàm và đạo hàm.",
            "Ví dụ 5/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 5", "Bất biến cấp 0 và cấp 1", "Ví dụ 5/6")
        deriv=VGroup(
            mtx(r"f_m(1)=1",42,GREEN),
            mtx(r"f'_m(x)=2x+2m(x-1)",39,BLUE),
            mtx(r"f'_m(1)=2",42,GREEN),
            mtx(r"A(1,1)",39,GOLD),
            mtx(r"y-1=2(x-1)",39,CYAN),
            mtx(r"\boxed{y=2x-1}",45,GOLD),
        ).arrange(DOWN,buff=0.25).shift(LEFT*2.4)
        side=VGroup(
            VGroup(mtx(r"f_m(1)",31,GREEN),txt("không phụ thuộc m",23,INK)).arrange(RIGHT,buff=0.16),
            VGroup(mtx(r"f'_m(1)",31,GREEN),txt("không phụ thuộc m",23,INK)).arrange(RIGHT,buff=0.16),
            txt("→ cùng điểm, cùng hệ số góc",24,GOLD,BOLD),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.35)
        self.play(FadeIn(deriv),FadeIn(side),run_time=0.9)
        self.narrate(
            "Thay x bằng một, hạng m nhân x trừ một bình phương bằng không, nên mọi đồ thị đều đi qua A một một. Bây giờ lấy đạo hàm: f phẩy bằng hai x cộng hai m nhân x trừ một. Tại x bằng một, phần chứa m lại bằng không, nên hệ số góc tiếp tuyến luôn bằng hai. Vậy mọi đồ thị không chỉ đi qua A mà còn có chung tiếp tuyến y bằng hai x trừ một. Ta có thể gọi f tại một là bất biến cấp không, còn f phẩy tại một là bất biến cấp một.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ 5", "Các đồ thị chạm cùng một đường thẳng", "Ví dụ 5/6")
        ax,labels=self.make_axes(xr=(-2,4,1),yr=(-3,10,1),xlen=6.8,ylen=5.3,shift=LEFT*2.5)
        curves=VGroup()
        for mm,col in [(-0.5,PURPLE),(0,BLUE),(0.8,GREEN),(2,ORANGE)]:
            curves.add(ax.plot(lambda x,mm=mm:x*x+mm*(x-1)**2,x_range=[-1.7,3.2],color=col,stroke_width=3))
        tan=ax.plot(lambda x:2*x-1,x_range=[-1,3.5],color=GOLD,stroke_width=4)
        A=Dot(ax.c2p(1,1),radius=0.10,color=GOLD)
        lab=mtx(r"A(1,1)",29,GOLD).next_to(A,UR,buff=0.08)
        self.play(Create(ax),FadeIn(labels),run_time=0.7)
        self.play(LaggedStart(*[Create(c) for c in curves],lag_ratio=0.13),run_time=1.8)
        self.play(Create(tan),FadeIn(A,scale=1.6),FadeIn(lab),run_time=0.8)
        self.narrate(
            "Nhìn hình, các đường cong tách xa nhau ở hai phía, nhưng khi đến A một một, chúng cùng chạm vào đường thẳng màu vàng với đúng một hướng. Đây là một kiểu bất biến rất mạnh và thường xuất hiện khi phần chứa tham số có nhân tử bình phương x trừ a.",
            1.6,
        )

        self.clear_stage(); self.add_header_footer("Mẫu tổng quát", "Vì sao nhân tử bình phương tạo tiếp tuyến chung?", "Ví dụ 5/6")
        gen=VGroup(
            mtx(r"f_m(x)=g(x)+(x-a)^2H(x,m)",40,GOLD),
            mtx(r"f_m(a)=g(a)",40,GREEN),
            mtx(r"f'_m(a)=g'(a)",40,GREEN),
            txt("Giá trị và đạo hàm bậc nhất đều không còn m.",26,CYAN),
        ).arrange(DOWN,buff=0.38)
        fit_width(gen,11.6)
        self.play(FadeIn(gen),run_time=0.9)
        self.narrate(
            "Mẫu tổng quát là f m bằng g cộng x trừ a bình phương nhân một biểu thức bất kỳ có thể chứa m. Tại x bằng a, cả phần thêm vào và đạo hàm bậc nhất của phần thêm vào đều bằng không. Vì vậy mọi đồ thị có chung điểm g của a và chung tiếp tuyến có hệ số góc g phẩy của a. Đây là một kết quả rất đáng nhớ vì nó giúp ta nhìn ra tiếp tuyến chung mà không cần tính riêng cho từng m.",
            2.0,
        )

    # ======================================================
    # EXAMPLE 6 - INVARIANT AREA
    # ======================================================
    def ex6_area(self):
        self.show_problem(
            "Ví dụ 6 – Diện tích dưới đồ thị vẫn không đổi",
            [
                mtx(r"f_m(x)=x^2+1+m\left(x-\frac12\right)", 40, GOLD),
                mtx(r"0\le x\le1,\qquad -1\le m\le1", 34, CYAN),
                "Chứng minh diện tích giới hạn bởi đồ thị, trục Ox và hai đường x = 0, x = 1 là bất biến.",
            ],
            "Ví dụ cuối cùng cho thấy bất biến không chỉ là điểm hay đường. Trên đoạn từ không đến một và với m nằm từ âm một đến một, đồ thị luôn nằm phía trên trục hoành. Ta sẽ chứng minh diện tích dưới đồ thị luôn bằng cùng một số, dù đường cong thay đổi.",
            "Ví dụ 6/6",
        )
        self.clear_stage(); self.add_header_footer("Ví dụ 6", "Phần phụ thuộc m tự triệt tiêu khi tích phân", "Ví dụ 6/6")
        deriv=VGroup(
            mtx(r"S_m=\int_0^1\left[x^2+1+m\left(x-\frac12\right)\right]dx",38,INK),
            mtx(r"=\int_0^1(x^2+1)dx+m\int_0^1\left(x-\frac12\right)dx",37,BLUE),
            mtx(r"=\frac13+1+m\left(\frac12-\frac12\right)",39,CYAN),
            mtx(r"\boxed{S_m=\frac43}",48,GOLD),
        ).arrange(DOWN,buff=0.38).shift(LEFT*2.35)
        side=VGroup(
            txt("Chìa khóa:",25,GOLD,BOLD),
            mtx(r"\int_0^1\left(x-\frac12\right)dx=0",36,GREEN),
            txt("phần chứa m có tổng đại số bằng 0.",24,INK),
        ).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.35)
        self.play(FadeIn(deriv),FadeIn(side),run_time=0.9)
        self.narrate(
            "Ta viết diện tích thành tích phân từ không đến một. Tách phần không chứa m và phần chứa m. Tích phân của x bình phương cộng một bằng một phần ba cộng một. Còn tích phân của x trừ một phần hai trên đoạn từ không đến một bằng không, vì phần âm bên trái và phần dương bên phải triệt tiêu nhau. Do đó toàn bộ phần nhân m biến mất. Kết quả luôn là bốn phần ba. Đây là bất biến do cơ chế bù trừ.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Ví dụ 6", "Hình dạng khác nhau nhưng cùng diện tích", "Ví dụ 6/6")
        ax=Axes(x_range=[0,1.1,0.2],y_range=[0,3.2,0.5],x_length=6.6,y_length=4.9,tips=False,
                axis_config={"color":MUTED,"stroke_width":2,"include_numbers":True,"font_size":22}).shift(LEFT*2.5+DOWN*0.1)
        labels=ax.get_axis_labels(mtx("x",27),mtx("y",27))
        graphs=[]
        areas=[]
        for mm,col in [(-1,PURPLE),(0,BLUE),(1,GREEN)]:
            gr=ax.plot(lambda x,mm=mm:x*x+1+mm*(x-0.5),x_range=[0,1],color=col,stroke_width=3.2)
            ar=ax.get_area(gr,x_range=[0,1],color=col,opacity=0.10)
            graphs.append(gr); areas.append(ar)
        side=VGroup(
            mtx(r"m=-1",31,PURPLE),
            mtx(r"m=0",31,BLUE),
            mtx(r"m=1",31,GREEN),
            mtx(r"S=\frac43",43,GOLD),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.85)
        self.play(Create(ax),FadeIn(labels),run_time=0.7)
        for gr,ar in zip(graphs,areas):
            self.play(FadeIn(ar),Create(gr),run_time=0.55)
        self.play(FadeIn(side),run_time=0.5)
        self.narrate(
            "Ba đường cong trên hình rõ ràng không trùng nhau. Có vùng được đẩy lên, có vùng bị kéo xuống. Nhưng lượng tăng ở một phía đúng bằng lượng giảm ở phía còn lại, nên tổng diện tích vẫn bằng bốn phần ba. Đây là một hình ảnh rất quan trọng: bất biến thường xuất hiện khi một phần thay đổi được cân bằng bởi một phần thay đổi ngược chiều.",
            1.8,
        )

    # ======================================================
    # SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_stage(); self.add_header_footer("Bản đồ săn bất biến", "Nhìn cấu trúc trước khi tính toán", "Tổng kết")
        rows=VGroup(
            VGroup(mtx(r"(x-m)^2+c",31,BLUE),txt("→ tịnh tiến; giá trị cực trị có thể cố định",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"x_1+x_2=C",31,CYAN),txt("→ trung điểm nghiệm cố định",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"\frac{ax+b}{cx+d}",31,GREEN),txt("→ giao hai tiệm cận là tâm đối xứng",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"f(a+t)+f(a-t)=2b",31,ORANGE),txt("→ tâm đối xứng",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"(x-a)^2H(x,m)",31,PURPLE),txt("→ dễ sinh điểm và tiếp tuyến chung",24,INK)).arrange(RIGHT,buff=0.20),
            VGroup(mtx(r"\int_a^b h(x)dx=0",31,GOLD),txt("→ phần chứa tham số có thể triệt tiêu",24,INK)).arrange(RIGHT,buff=0.20),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.31).shift(DOWN*0.05)
        fit_width(rows,11.9)
        for r in rows:self.play(FadeIn(r,shift=RIGHT*0.10),run_time=0.34)
        self.narrate(
            "Ta có thể gom cả video thành sáu dấu hiệu. Dạng bình phương có tham số thường gợi phép tịnh tiến. Tổng nghiệm cố định gợi trung điểm cố định. Hàm phân thức bậc nhất trên bậc nhất gợi tâm là giao hai tiệm cận. Điều kiện f của a cộng t cộng f của a trừ t bằng hai b nhận diện tâm đối xứng. Nhân tử x trừ a bình phương thường tạo điểm và tiếp tuyến chung. Và trong tích phân, nếu phần chứa tham số có tích phân bằng không thì đại lượng tổng có thể bất biến.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Bài thử thách", "Tìm bất biến mà không cần vẽ trước", "Tổng kết")
        q=VGroup(
            mtx(r"f_m(x)=x^2+2x+m(x+1)^2",42,GOLD),
            txt("Tìm điểm chung và tiếp tuyến chung của mọi đồ thị.",27,INK),
        ).arrange(DOWN,buff=0.35).shift(UP*1.2)
        self.play(FadeIn(q),run_time=0.7)
        self.narrate(
            "Bài thử thách cuối video. Với f m bằng x bình phương cộng hai x cộng m nhân x cộng một bình phương, hãy tìm điểm chung và tiếp tuyến chung của mọi đồ thị. Các em hãy dừng video và thử dùng đúng mẫu vừa học.",
            1.5,
        )
        sol=VGroup(
            mtx(r"a=-1",34,CYAN),
            mtx(r"f_m(-1)=-1",38,GREEN),
            mtx(r"f'_m(x)=2x+2+2m(x+1)",36,BLUE),
            mtx(r"f'_m(-1)=0",38,GREEN),
            mtx(r"\boxed{A(-1,-1),\qquad y=-1}",44,GOLD),
        ).arrange(DOWN,buff=0.25).shift(DOWN*0.75)
        self.play(FadeIn(sol),run_time=0.9)
        self.narrate(
            "Thay x bằng âm một, phần chứa m biến mất và ta được y bằng âm một. Đạo hàm tại âm một cũng bằng không với mọi m. Vì vậy điểm chung là A âm một âm một và tiếp tuyến chung là đường thẳng ngang y bằng âm một. Nếu các em tự làm ra kết quả này, nghĩa là đã nắm được tư duy bất biến chứ không chỉ thuộc công thức.",
            1.8,
        )

    def outro(self):
        self.clear_stage()
        main=txt("CHỐT LẠI",44,GOLD,BOLD)
        f=VGroup(
            txt("Tham số thay đổi", 29, INK),
            mtx(r"\not\Rightarrow", 40, BLUE),
            txt("mọi thứ đều thay đổi", 29, INK),
        ).arrange(RIGHT, buff=0.22)
        sub=txt("Hãy tìm cấu trúc đứng yên bên trong sự chuyển động.",29,CYAN)
        brand=txt(TEN_THAY,22,MUTED)
        g=VGroup(main,f,sub,brand).arrange(DOWN,buff=0.38)
        fit_width(g,12.0)
        self.play(FadeIn(main),Write(f),FadeIn(sub),FadeIn(brand),run_time=1.2)
        self.narrate(
            "Điều quan trọng nhất của chuyên đề hôm nay là thay đổi câu hỏi. Đừng chỉ hỏi đồ thị chạy đi đâu khi m thay đổi. Hãy hỏi trong sự chuyển động ấy, cái gì vẫn đứng yên. Khi các em nhìn thấy bất biến, những bài tham số dài và rối thường trở nên rất ngắn, đồng thời các em hiểu được một vẻ đẹp sâu hơn của đồ thị hàm số. Hẹn gặp các em ở video tiếp theo.",
            2.0,
        )

    def construct(self):
        self.intro()
        self.invariant_idea()
        self.ex1_minimum()
        self.ex2_midpoint()
        self.ex3_homographic()
        self.ex4_cubic()
        self.ex5_tangent()
        self.ex6_area()
        self.synthesis()
        self.outro()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "bat_bien_tinh_chat_dep_do_thi_ham_so_1080p"
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
    master_wav = ROOT / "master_narration_invariants.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    # Final verification: video + audio streams must exist.
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

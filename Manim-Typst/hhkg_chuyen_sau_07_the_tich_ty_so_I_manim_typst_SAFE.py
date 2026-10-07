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
# HHKG CHUYEN SAU 07 - THE TICH & TY SO THE TICH I - MANIM + TYPST SAFE
# Standalone 100% for GitHub Actions
#
# Visual grammar for the whole HHKG series:
#   - visible polyhedron edges: solid
#   - hidden polyhedron edges: dashed neutral
#   - auxiliary / projection lines: dashed accent
#   - fixed teaching camera inside each geometry scene
#   - mathematics only in MathTypst; prose in Text
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
config.background_color = "#08111F"

ROOT = Path.cwd()
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR = ROOT / "media"

# ==========================================================
# PREMIUM PALETTE
# ==========================================================
BG = "#08111F"
PANEL = "#0D1B2E"
PANEL_2 = "#10233C"
INK = "#F3F7FF"
MUTED = "#8EA7C2"
GRID = "#25415E"
BLUE = "#43C6F9"
CYAN = "#38E0CF"
GOLD = "#FFD84D"
GREEN = "#5CE58A"
RED = "#FF7373"
ORANGE = "#FF9B54"
PURPLE = "#B995FF"
EDGE = "#E7F0FF"
DIM = "#58718C"

# ==========================================================
# TYPOGRAPHY
# ==========================================================
def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


_FORBIDDEN_TYPST_WORDS = {"sect", "intersect", "angle"}


def validate_typst_expr(s):
    """Fail early on known-invalid Typst math tokens used in this series."""
    words = set(s.replace("(", " " ).replace(")", " " ).replace(",", " " ).split())
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(
            f"Forbidden Typst math token(s) {bad} in {s!r}. "
            "Use 'inter' for intersection and 'hat(...)' for plane angles."
        )
    if "/" in s:
        raise ValueError(
            f"Slash fraction is forbidden in HHKG MathTypst: {s!r}. Use frac(..., ...)."
        )
    return s


def mty(s, size=38, color=INK):
    """Math only. Text prose must use txt()."""
    s = validate_typst_expr(s)
    try:
        return MathTypst(s, font_size=size, color=color)
    except Exception as exc:
        raise RuntimeError(f"MathTypst failed for expression: {s!r}") from exc


def fit_width(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def fit_height(mob, height):
    if mob.height > height:
        mob.scale_to_fit_height(height)
    return mob


# ==========================================================
# AUDIO + MASTER TRACK
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
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
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
        except Exception as exc:
            last_err = exc
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

    filter_complex = (
        ";".join(filters)
        + ";"
        + "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", *inputs,
            "-filter_complex", filter_complex,
            "-map", "[m]",
            "-ar", "48000",
            "-ac", "2",
            "-t", f"{video_duration:.3f}",
            str(out_wav),
        ],
        check=True,
    )


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(video),
            "-i", str(audio),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(out),
        ],
        check=True,
    )


# ==========================================================
# 3D GEOMETRY
# ==========================================================
GEO_SCALE = 0.80
GEO_SHIFT = np.array([-1.78, -0.02, -0.08])
VIEW_PHI = 68 * DEGREES
VIEW_THETA = -54 * DEGREES
VIEW_ZOOM = 0.97


def L(x, y, z):
    """Logical geometry -> scene geometry."""
    return GEO_SCALE * np.array([float(x), float(y), float(z)]) + GEO_SHIFT


def solid(a, b, color=EDGE, width=4.0, opacity=0.94):
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def hidden_edge(a, b, color=DIM, width=2.7, opacity=0.70, dash=0.11):
    return DashedLine(
        a, b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def aux(a, b, color=CYAN, width=3.7, opacity=0.90, dash=0.11):
    return DashedLine(
        a, b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def face(*points, color=BLUE, opacity=0.10, stroke=BLUE, stroke_width=0.0):
    return Polygon(
        *points,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=stroke_width,
        stroke_opacity=0.0 if stroke_width == 0 else 0.55,
    )


def right_angle_3d(vertex, u, v, size=0.30, color=GOLD, width=4.5):
    u = np.array(u, dtype=float)
    v = np.array(v, dtype=float)
    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)
    p1 = vertex + size * u
    p2 = vertex + size * (u + v)
    p3 = vertex + size * v
    return VGroup(
        solid(p1, p2, color=color, width=width),
        solid(p2, p3, color=color, width=width),
    )


def arc_basis(center, e1, e2, angle, radius=0.52, color=GOLD, width=6):
    e1 = np.array(e1, dtype=float)
    e2 = np.array(e2, dtype=float)
    e1 /= np.linalg.norm(e1)
    e2 /= np.linalg.norm(e2)
    return ParametricFunction(
        lambda t: center + radius * (math.cos(t) * e1 + math.sin(t) * e2),
        t_range=[0, angle],
        color=color,
        stroke_width=width,
    )


# ==========================================================
# SCENE
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)

    # ------------------------------------------------------
    # AUDIO
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # FIXED MASTER UI
    # ------------------------------------------------------
    def clear_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.30)
        self.clear()

    def add_header(self, title, subtitle, progress):
        series = txt("HHKG CHUYÊN SÂU · 07", 15, BLUE, BOLD)
        series.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.30)
        title_m = fit_width(txt(title, 29, INK, BOLD), 8.9)
        title_m.next_to(series, DOWN, buff=0.045, aligned_edge=LEFT)
        sub_m = fit_width(txt(subtitle, 17, MUTED), 8.9)
        sub_m.next_to(title_m, DOWN, buff=0.045, aligned_edge=LEFT)
        accent = Line(series.get_left()+DOWN*0.13, series.get_left()+RIGHT*0.62+DOWN*0.13,
                      color=GOLD, stroke_width=3.2)
        prog = txt(progress, 15, MUTED, BOLD)
        prog.to_edge(UP, buff=0.20).to_edge(RIGHT, buff=0.32)
        rule = Line(LEFT*6.82, RIGHT*6.82, color=GRID, stroke_width=0.9,
                    stroke_opacity=0.42).shift(UP*2.78)
        divider = Line(np.array([1.50,-2.83,0]), np.array([1.50,2.64,0]),
                       color=GRID, stroke_width=1.0, stroke_opacity=0.42)
        teacher = txt(TEN_THAY, 15, MUTED)
        teacher.to_edge(DOWN, buff=0.10).to_edge(LEFT, buff=0.30)
        hud = VGroup(series,title_m,sub_m,accent,prog,rule,divider,teacher)
        self.add_fixed_in_frame_mobjects(hud)
        return hud

    def card(self, kicker, title, items, accent=GOLD, height=5.25, auto_add=True):
        bg = Rectangle(width=5.12,height=height,fill_color=PANEL,fill_opacity=0.90,
                       stroke_color=GRID,stroke_width=0.9,stroke_opacity=0.36).move_to(RIGHT*4.28+DOWN*0.03)
        spine = Line(bg.get_corner(UL)+RIGHT*0.12+DOWN*0.18,
                     bg.get_corner(DL)+RIGHT*0.12+UP*0.18,
                     color=accent,stroke_width=3.8,stroke_opacity=0.95)
        k = txt(kicker.upper(),14,accent,BOLD)
        k.move_to(bg.get_corner(UL)+RIGHT*0.36+DOWN*0.30,aligned_edge=LEFT)
        t = fit_width(txt(title,23,INK,BOLD),4.30)
        t.next_to(k,DOWN,buff=0.10,aligned_edge=LEFT)
        body = VGroup()
        for item in items:
            kind = item[0]
            if kind == "text":
                _,s,size,color,weight = item; mob = txt(s,size,color,weight)
            elif kind == "math":
                _,expr,size,color = item; mob = mty(expr,size,color)
            elif kind == "sep":
                mob = Line(LEFT*2.00,RIGHT*2.00,color=GRID,stroke_width=0.9,stroke_opacity=0.55)
            elif kind == "obj":
                mob = item[1]
            else:
                raise ValueError(kind)
            body.add(fit_width(mob,4.28))
        body.arrange(DOWN,aligned_edge=LEFT,buff=0.18)
        body.next_to(t,DOWN,buff=0.22,aligned_edge=LEFT)
        fit_height(body,height-1.45)
        group = VGroup(bg,spine,k,t,body)
        if auto_add:
            self.add_fixed_in_frame_mobjects(group)
        return group

    def takeaway(self, text_s):
        label = fit_width(txt(text_s,16,CYAN,BOLD),7.15)
        label.move_to(LEFT*2.55+DOWN*2.52)
        self.add_fixed_in_frame_mobjects(label)
        return label

    def add_label(self, name, pt, color=GOLD, off=(0.10,-0.10,0.05), size=22):
        lab = mty(name,size,color).move_to(pt+np.array(off,dtype=float))
        self.add_fixed_orientation_mobjects(lab)
        return lab

    # ------------------------------------------------------
    # MODELS
    # ------------------------------------------------------
    def right_square_pyramid(self, dim=False):
        A=L(-2.0,-1.8,0); B=L(2.0,-1.8,0); C=L(2.0,2.0,0); D=L(-2.0,2.0,0); S=L(-2.0,-1.8,3.0)
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(solid(A,B,vc,vw,vo),solid(B,C,vc,vw,vo),solid(S,A,vc,vw,vo),solid(S,B,vc,vw,vo),solid(S,C,vc,vw,vo))
        hidden=VGroup(hidden_edge(C,D,DIM,2.6,0.68),hidden_edge(D,A,DIM,2.6,0.68),hidden_edge(S,D,DIM,2.6,0.68))
        base=face(A,B,C,D,color=BLUE,opacity=0.09,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def tetrahedron(self, dim=False):
        S=L(-0.5,-0.5,3.4); A=L(-2.3,-1.8,0); B=L(2.2,-1.8,0); C=L(0.7,2.0,0)
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(solid(S,A,vc,vw,vo),solid(S,B,vc,vw,vo),solid(S,C,vc,vw,vo),solid(A,B,vc,vw,vo),solid(A,C,vc,vw,vo))
        hidden=VGroup(hidden_edge(B,C,DIM,2.6,0.68))
        base=face(A,B,C,color=BLUE,opacity=0.08,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C]],Dot3D(S,radius=0.06,color=RED))
        return {"S":S,"A":A,"B":B,"C":C,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def centered_square_pyramid(self):
        A=L(-2.2,-2.0,0); B=L(2.2,-2.0,0); C=L(2.2,2.0,0); D=L(-2.2,2.0,0); S=L(0,0,3.8)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.08,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        title=txt("HHKG CHUYÊN SÂU 07",46,GOLD,BOLD)
        sub=txt("THỂ TÍCH & TỶ SỐ THỂ TÍCH I",35,INK,BOLD)
        line=txt("Cùng đáy · cùng chiều cao · đổi đỉnh · đồng dạng · chóp cụt",24,CYAN,BOLD)
        note=txt("Tính tỷ số trước khi tính số tuyệt đối",23,MUTED)
        brand=txt(TEN_THAY,20,MUTED)
        g=VGroup(title,sub,line,note,brand).arrange(DOWN,buff=0.28)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g,shift=UP*0.10),run_time=1.0)
        self.narrate(
            "Từ video bảy, series chuyển sang chặng thể tích. Đây là phần rất dễ bị biến thành một bộ sưu tập công thức, nhưng cách học hiệu quả hơn là nhìn xem hai khối đang chia sẻ điều gì: cùng đáy, cùng chiều cao, cùng một mặt phẳng đáy, hay cùng một tâm đồng dạng. Khi nhận ra cấu trúc chung, nhiều bài thể tích không cần tính từng khối riêng. Ta chỉ tính một tỷ số, hoặc thậm chí không cần biết chiều cao thật của khối. Video này xây nền cho toàn bộ chặng C, từ công thức cơ bản tới định lý tích ba tỷ số và chóp cụt.",2.2)

    # ======================================================
    # METHOD MAP
    # ======================================================
    def method_map(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ phương pháp", "Một bài thể tích nên hỏi gì trước khi bấm số?", "2/9")
        left=VGroup(
            txt("1 · Cùng đáy?",24,GOLD,BOLD),
            txt("→ so chiều cao",20,INK),
            txt("2 · Cùng chiều cao?",24,GOLD,BOLD),
            txt("→ so diện tích đáy",20,INK),
            txt("3 · Điểm nằm trên cạnh?",24,GOLD,BOLD),
            txt("→ tỷ số khoảng cách tuyến tính",20,INK),
            txt("4 · Khối đồng dạng?",24,GOLD,BOLD),
            txt("→ diện tích k², thể tích k³",20,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.18).move_to(LEFT*2.45+UP*0.05)
        right=VGroup(
            mty("V = frac(1, 3) S h",34,CYAN),
            mty("frac(V_1, V_2) = frac(S_1 h_1, S_2 h_2)",30,INK),
            mty("S_1 = S_2 -> frac(V_1, V_2) = frac(h_1, h_2)",27,GREEN),
            mty("h_1 = h_2 -> frac(V_1, V_2) = frac(S_1, S_2)",27,GREEN),
            mty("k -> k^2 -> k^3",34,GOLD),
        ).arrange(DOWN,buff=0.30).move_to(RIGHT*3.6+UP*0.05)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left),FadeIn(right),run_time=0.9)
        self.narrate(
            "Trước khi tính, hãy đặt bốn câu hỏi. Hai khối có cùng đáy không? Nếu có, tỷ số thể tích chỉ còn là tỷ số chiều cao. Hai khối có cùng chiều cao không? Nếu có, ta chỉ so diện tích đáy. Có điểm nào chạy trên một cạnh hoặc chia cạnh theo tỷ số không? Khi đó khoảng cách tới một mặt phẳng thường biến thiên tuyến tính theo đúng tỷ số trên cạnh. Cuối cùng, nếu hai khối đồng dạng tỷ số k thì diện tích đổi theo k bình phương còn thể tích đổi theo k lập phương. Bốn câu hỏi này quan trọng hơn việc thuộc thêm một công thức riêng lẻ.",2.0)

    # ======================================================
    # 1. BASIC VOLUME
    # ======================================================
    def basic_volume(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 1 · Công thức gốc", "Chóp vuông S.ABCD, AB = 4, SA = 3", "3/9")
        G=self.right_square_pyramid(); self.add(G["base"],G["edges"],G["dots"])
        for n in ["A","B","C","D","S"]: self.add_label(n,G[n],RED if n=="S" else GOLD)
        sa=solid(G["S"],G["A"],GOLD,6.0,1.0); self.play(Create(sa),run_time=0.6)
        self.card("NỀN TẢNG","Đáy và chiều cao phải tương ứng",[
            ("math","S_(A B C D) = 4^2 = 16",29,CYAN),
            ("math","h = S A = 3",29,GREEN),
            ("math","V = frac(1, 3) S_(A B C D) h",30,INK),
            ("math","V = frac(1, 3) times 16 times 3",29,INK),
            ("math","V = 16",36,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Ta bắt đầu bằng công thức gốc. Hình chóp S.ABCD có đáy là hình vuông cạnh bốn và SA vuông góc với đáy, SA bằng ba. Diện tích đáy là mười sáu, chiều cao tương ứng là ba, nên thể tích bằng một phần ba nhân mười sáu nhân ba, bằng mười sáu. Điểm cần nhấn mạnh không phải phép nhân, mà là cặp đáy và chiều cao phải đi cùng nhau. Nếu đổi mặt đáy sang một mặt bên, chiều cao cũng phải đổi theo. Rất nhiều sai lầm thể tích bắt đầu từ việc lấy diện tích của một mặt nhưng dùng chiều cao ứng với mặt khác.",1.9)
        self.narrate(
            "Trong những bài tiếp theo, ta sẽ cố tình tránh tính diện tích và chiều cao tuyệt đối khi không cần thiết. Công thức một phần ba S h sẽ được dùng chủ yếu ở dạng tỷ số. Khi hai khối chia sẻ cùng S hoặc cùng h, một phần lớn dữ kiện tự triệt tiêu. Đó mới là sức mạnh thật sự của công thức thể tích trong các bài phân hóa.",1.6)
        self.takeaway("Thể tích: chọn đúng cặp đáy–chiều cao trước, rồi mới thay số")

    # ======================================================
    # 2. SAME BASE / SAME HEIGHT
    # ======================================================
    def same_base_same_height(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-50*DEGREES,zoom=0.98)
        self.add_header("Bài 2 · Cùng đáy, cùng chiều cao", "Hai đỉnh khác vị trí nhưng nằm trên cùng mặt phẳng song song đáy", "4/9")
        A=L(-2.3,-1.7,0); B=L(2.0,-1.7,0); C=L(0.4,1.8,0)
        S=L(-1.3,-0.2,3.0); T=L(1.6,0.8,3.0)
        base=face(A,B,C,color=BLUE,opacity=0.12,stroke_width=0)
        p1=VGroup(solid(S,A,EDGE,3.4,0.72),solid(S,B,EDGE,3.4,0.72),solid(S,C,EDGE,3.4,0.72))
        p2=VGroup(solid(T,A,PURPLE,3.4,0.72),solid(T,B,PURPLE,3.4,0.72),solid(T,C,PURPLE,3.4,0.72))
        level=aux(L(-2.5,-0.8,3.0),L(2.5,1.2,3.0),ORANGE,3.4,0.7)
        self.add(base,p1,p2,level,Dot3D(S,radius=0.06,color=RED),Dot3D(T,radius=0.06,color=PURPLE))
        for n,p in [("A",A),("B",B),("C",C),("S",S),("T",T)]: self.add_label(n,p,RED if n=="S" else PURPLE if n=="T" else GOLD)
        self.card("TỶ SỐ","Cùng đáy ABC, cùng khoảng cách tới (ABC)",[
            ("math","S_1 = S_2 = S_(A B C)",28,CYAN),
            ("math","h_1 = h_2",30,GREEN),
            ("math","frac(V_(S A B C), V_(T A B C)) = 1",29,INK),
            ("math","V_(S A B C) = V_(T A B C)",32,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Hai tứ diện S.ABC và T.ABC có cùng đáy ABC. Giả sử S và T nằm trên cùng một mặt phẳng song song với ABC. Khi đó khoảng cách từ S và T tới mặt đáy bằng nhau. Công thức thể tích cho hai khối có cùng diện tích đáy và cùng chiều cao, nên thể tích bằng nhau dù hai đỉnh nằm ở hai vị trí rất khác nhau trong không gian. Đây là nguyên lý đổi đỉnh: ta có thể trượt đỉnh trên một mặt phẳng song song với đáy mà thể tích không đổi.",1.9)
        self.narrate(
            "Nguyên lý này cực hữu ích trong bài có đỉnh nằm ở vị trí khó. Thay vì dựng chiều cao từ đỉnh đó, ta tìm một điểm khác nằm cùng mặt phẳng song song với đáy nhưng tạo ra một khối dễ tính hơn. Điều phải chứng minh không phải hai cạnh bên bằng nhau, mà là hai đỉnh có cùng khoảng cách tới mặt phẳng đáy. Trong lời giải ngắn, chỉ cần nêu cùng đáy và hai đỉnh thuộc một mặt phẳng song song đáy là đủ để kết luận hai thể tích bằng nhau.",1.8)
        self.takeaway("Đổi đỉnh: đỉnh trượt trên mặt phẳng song song đáy → thể tích không đổi")

    # ======================================================
    # 3. ONE-EDGE RATIO + CHANGE BASE
    # ======================================================
    def one_edge_ratio(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-52*DEGREES,zoom=0.98)
        self.add_header("Bài 3 · Một điểm chia cạnh", "M thuộc SA — tỷ số trên cạnh trở thành tỷ số thể tích", "5/9")
        G=self.tetrahedron(); self.add(G["base"],G["edges"],G["dots"])
        for n in ["S","A","B","C"]: self.add_label(n,G[n],RED if n=="S" else GOLD)
        lam=0.62; M=G["S"]+lam*(G["A"]-G["S"])
        self.add(Dot3D(M,radius=0.065,color=ORANGE)); self.add_label("M",M,ORANGE)
        subface=face(G["S"],M,G["B"],G["C"],color=PURPLE,opacity=0.18,stroke_width=0)
        sm=solid(G["S"],M,ORANGE,6.0,1.0); self.play(FadeIn(subface),Create(sm),run_time=0.8)
        self.card("ĐỊNH LÝ NHỎ","M nằm trên SA",[
            ("math","frac(S M, S A) = lambda",30,ORANGE),
            ("math","frac(h_M, h_A) = lambda",25,CYAN),
            ("math","frac(V_(S M B C), V_(S A B C)) = lambda",28,GREEN),
            ("math","frac(V_(S M B C), V_(S A B C)) = frac(S M, S A)",27,GOLD),
        ],accent=ORANGE)
        self.narrate(
            "Trong tứ diện SABC, lấy M trên cạnh SA. Hai tứ diện SMBC và SABC có chung đáy SBC. Vì S nằm ngay trên mặt phẳng SBC, khoảng cách từ một điểm trên đoạn SA tới mặt phẳng SBC tăng tuyến tính từ không tại S tới khoảng cách của A. Do đó nếu SM trên SA bằng lambda thì chiều cao của M so với mặt SBC cũng bằng lambda lần chiều cao của A. Tỷ số thể tích vì thế đúng bằng SM trên SA.",1.9)
        self.narrate(
            "Đây là mẫu nhận dạng rất mạnh: một điểm chia cạnh của tứ diện thường biến ngay thành một tỷ số thể tích. Ta không cần biết diện tích tam giác SBC, cũng không cần biết góc giữa SA và mặt SBC. Tất cả những đại lượng khó đó triệt tiêu khi lấy tỷ số. Ở bước tiếp theo, ta sẽ áp dụng nguyên lý một cạnh này ba lần liên tiếp để có công thức tích ba tỷ số.",1.7)
        self.takeaway("Điểm chia cạnh → nghĩ tới thể tích trước khi nghĩ tới khoảng cách tuyệt đối")

    # ======================================================
    # 4. PRODUCT OF THREE RATIOS
    # ======================================================
    def product_theorem(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-52*DEGREES,zoom=0.98)
        self.add_header("Bài 4 · Định lý tích ba tỷ số", "M∈SA, N∈SB, P∈SC", "6/9")
        G=self.tetrahedron(); self.add(G["base"],G["edges"],G["dots"])
        for n in ["S","A","B","C"]: self.add_label(n,G[n],RED if n=="S" else GOLD)
        lm,ln,lp=2/3,3/4,1/2
        M=G["S"]+lm*(G["A"]-G["S"]); N=G["S"]+ln*(G["B"]-G["S"]); Pp=G["S"]+lp*(G["C"]-G["S"])
        small=face(M,N,Pp,color=GOLD,opacity=0.25,stroke=GOLD,stroke_width=2.4)
        self.add(small,*[Dot3D(q,radius=0.06,color=GOLD) for q in [M,N,Pp]])
        for n,p in [("M",M),("N",N),("P",Pp)]: self.add_label(n,p,GOLD)
        self.card("ĐỊNH LÝ","Ba điểm trên ba cạnh xuất phát từ S",[
            ("math","frac(V_(S M N P), V_(S A B C)) = frac(S M, S A) frac(S N, S B) frac(S P, S C)",23,CYAN),
            ("math","frac(V_(S M N P), V_(S A B C)) = frac(2, 3) frac(3, 4) frac(1, 2)",24,INK),
            ("math","frac(V_(S M N P), V_(S A B C)) = frac(1, 4)",29,GOLD),
            ("math","frac(V_R, V_(S A B C)) = frac(3, 4)",27,GREEN),
        ],accent=GOLD)
        self.narrate(
            "Bây giờ lấy M trên SA, N trên SB và P trên SC. Khi ba điểm cùng xuất phát từ đỉnh S, tỷ số thể tích của tứ diện nhỏ SMNP với tứ diện lớn SABC bằng tích của ba tỷ số cạnh: SM trên SA, SN trên SB và SP trên SC. Có thể hiểu công thức này bằng cách thay từng đỉnh một; mỗi lần thay một điểm trên cạnh, thể tích nhân thêm đúng tỷ số tuyến tính tương ứng. Không cần ba tỷ số bằng nhau và không cần mặt MNP song song với ABC.",2.0)
        self.narrate(
            "Ví dụ SM trên SA bằng hai phần ba, SN trên SB bằng ba phần tư, SP trên SC bằng một phần hai. Tích ba tỷ số bằng một phần tư. Do đó khối nhỏ chiếm đúng một phần tư thể tích tứ diện ban đầu; phần còn lại chiếm ba phần tư. Đây là công thức cực nhanh trong trắc nghiệm và trả lời ngắn. Tuy nhiên phải nhớ điều kiện cấu trúc: ba điểm đều nằm trên ba cạnh cùng phát ra từ một đỉnh chung. Nếu các điểm nằm rải rác trên các cạnh khác nhau, không được máy móc nhân ba tỷ số.",2.0)
        self.takeaway("Ba cạnh cùng xuất phát từ một đỉnh → tỷ số thể tích = tích ba tỷ số cạnh")

    # ======================================================
    # 5. SIMILAR SECTION - DYNAMIC K
    # ======================================================
    def similar_section_dynamic(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 5 · Thiết diện song song đáy", "Tỷ số dài k → diện tích k² → thể tích k³", "7/9")
        G=self.centered_square_pyramid(); self.add(G["base"],G["edges"],G["dots"])
        for n in ["A","B","C","D","S"]: self.add_label(n,G[n],RED if n=="S" else GOLD)
        k=ValueTracker(0.30)
        verts=[G["A"],G["B"],G["C"],G["D"]]; S=G["S"]
        def pts(): return [S+k.get_value()*(v-S) for v in verts]
        sec=always_redraw(lambda: face(*pts(),color=GOLD,opacity=0.30,stroke=GOLD,stroke_width=2.2))
        dots=always_redraw(lambda: VGroup(*[Dot3D(q,radius=0.052,color=GOLD) for q in pts()]))
        self.add(sec,dots)
        read=always_redraw(lambda: VGroup(
            txt(f"k = {k.get_value():.2f}",17,ORANGE,BOLD),
            txt(f"k² = {k.get_value()**2:.3f}",17,CYAN,BOLD),
            txt(f"k³ = {k.get_value()**3:.3f}",17,GOLD,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.06).move_to(RIGHT*4.22+DOWN*1.95))
        self.add_fixed_in_frame_mobjects(read)
        self.card("ĐỒNG DẠNG","MNPQ song song ABCD",[
            ("math","frac(S M, S A) = frac(S N, S B) = k",25,CYAN),
            ("math","frac(S_(M N P Q), S_(A B C D)) = k^2",27,GREEN),
            ("math","frac(V_(S M N P Q), V_(S A B C D)) = k^3",27,GOLD),
            ("math","frac(V_F, V_L) = 1 - k^3",26,INK),
        ],accent=GOLD)
        self.narrate_play(
            "Khi một mặt phẳng cắt bốn cạnh bên của hình chóp theo cùng tỷ số k tính từ đỉnh S, thiết diện song song với đáy và hình chóp nhỏ đồng dạng với hình chóp lớn. Tỷ số các độ dài là k, nên tỷ số diện tích là k bình phương và tỷ số thể tích là k lập phương. Hãy quan sát khi mặt cắt di chuyển: k tăng đều nhưng thể tích phần chóp nhỏ tăng nhanh hơn nhiều vì phụ thuộc lũy thừa ba.",
            k.animate.set_value(0.80),min_time=5.0)
        self.narrate_play(
            "Đưa k về một phần hai. Khi thiết diện đi qua trung điểm bốn cạnh bên, diện tích thiết diện chỉ bằng một phần tư diện tích đáy, còn thể tích chóp nhỏ bằng một phần tám thể tích toàn khối. Phần chóp cụt bên dưới vì thế chiếm bảy phần tám. Đây là chỗ học sinh rất hay nhầm giữa một phần hai, một phần tư và một phần tám. Hãy nhớ ba tầng: độ dài bậc một, diện tích bậc hai, thể tích bậc ba.",
            k.animate.set_value(0.50),min_time=4.5)
        self.takeaway("Đồng dạng không gian: k cho chiều dài, k² cho diện tích, k³ cho thể tích")

    # ======================================================
    # 6. FRUSTUM - TWO METHODS
    # ======================================================
    def frustum_two_methods(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 6 · Chóp cụt", "Đáy lớn cạnh 6, đáy nhỏ cạnh 2, chiều cao chóp cụt 6", "8/9")
        A=L(-2.4,-2.0,0); B=L(2.4,-2.0,0); C=L(2.4,2.0,0); D=L(-2.4,2.0,0); S=L(0,0,3.6)
        k=1/3
        M=S+k*(A-S); N=S+k*(B-S); Pp=S+k*(C-S); Q=S+k*(D-S)
        base=face(A,B,C,D,color=BLUE,opacity=0.10,stroke_width=0)
        top=face(M,N,Pp,Q,color=GOLD,opacity=0.30,stroke=GOLD,stroke_width=2.2)
        sides=VGroup(face(A,B,N,M,color=PURPLE,opacity=0.08,stroke_width=0),face(B,C,Pp,N,color=PURPLE,opacity=0.08,stroke_width=0),face(C,D,Q,Pp,color=PURPLE,opacity=0.05,stroke_width=0),face(D,A,M,Q,color=PURPLE,opacity=0.05,stroke_width=0))
        edges=VGroup(solid(A,B),solid(B,C),hidden_edge(C,D),hidden_edge(D,A),solid(A,M),solid(B,N),solid(C,Pp),hidden_edge(D,Q),solid(M,N,GOLD,4.5),solid(N,Pp,GOLD,4.5),hidden_edge(Pp,Q,GOLD,3.0),hidden_edge(Q,M,GOLD,3.0))
        self.add(base,sides,top,edges)
        for n,p in [("A",A),("B",B),("C",C),("D",D),("M",M),("N",N),("P",Pp),("Q",Q)]: self.add_label(n,p,GOLD)
        self.card("HAI CÁCH","Khôi phục chóp lớn rồi trừ, hoặc dùng công thức chóp cụt",[
            ("math","V_l = frac(1, 3) times 36 times 9 = 108",27,CYAN),
            ("math","frac(V_s, V_l) = (frac(1, 3))^3 = frac(1, 27)",25,INK),
            ("math","V_s = 4",29,GREEN),
            ("math","V_c = 108 - 4 = 104",31,GOLD),
            ("sep",),
            ("math","V_c = frac(h, 3) times (S_1 + S_2 + sqrt(S_1 S_2))",23,PURPLE),
            ("math","V_c = 104",31,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Xét một chóp cụt vuông có đáy lớn là hình vuông cạnh sáu, đáy nhỏ cạnh hai và chiều cao chóp cụt bằng sáu. Cách thứ nhất là khôi phục chóp lớn ban đầu. Vì tỷ số cạnh đáy nhỏ trên đáy lớn bằng một phần ba, chóp nhỏ bị cắt đi đồng dạng với chóp lớn theo tỷ số một phần ba. Chiều cao chóp nhỏ vì thế bằng ba, còn chiều cao chóp lớn bằng chín.",1.9)
        self.narrate(
            "Thể tích chóp lớn bằng một phần ba nhân ba mươi sáu nhân chín, bằng một trăm lẻ tám. Chóp nhỏ chiếm một phần hai mươi bảy nên có thể tích bốn. Chóp cụt còn lại bằng một trăm lẻ bốn. Ta cũng có thể kiểm tra bằng công thức chóp cụt: h trên ba nhân tổng hai diện tích đáy và căn bậc hai tích hai diện tích ấy. Với h bằng sáu, hai diện tích là ba mươi sáu và bốn, kết quả vẫn là một trăm lẻ bốn. Hai cách cho cùng đáp số nhưng cách đồng dạng thường giải thích cấu trúc tốt hơn.",2.0)
        self.takeaway("Chóp cụt: ưu tiên khôi phục chóp lớn nếu tỷ số đồng dạng đẹp")

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Tổng kết Video 07", "Từ công thức gốc đến tỷ số lập phương", "9/9")
        left=VGroup(
            txt("6 mẫu nhận dạng",26,GOLD,BOLD),
            txt("• Cùng đáy → so chiều cao",20,INK),
            txt("• Cùng chiều cao → so diện tích đáy",20,INK),
            txt("• Đổi đỉnh trên mặt song song → V không đổi",20,INK),
            txt("• Điểm chia cạnh → tỷ số V tuyến tính",20,INK),
            txt("• Ba cạnh cùng đỉnh → tích ba tỷ số",20,INK),
            txt("• Đồng dạng → k² cho S, k³ cho V",20,INK),
            txt("• Chóp cụt → khôi phục chóp lớn rồi trừ",20,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.21).move_to(LEFT*2.25+UP*0.02)
        right=VGroup(
            mty("V = frac(1, 3) S h",30,CYAN),
            mty("frac(V_1, V_2) = frac(h_1, h_2)",28,INK),
            mty("frac(V_1, V_2) = frac(S_1, S_2)",28,INK),
            mty("frac(V_(S M N P), V_(S A B C)) = frac(S M, S A) frac(S N, S B) frac(S P, S C)",22,GREEN),
            mty("k -> k^2 -> k^3",32,GOLD),
            mty("V_F = (1-k^3) V_L",27,PURPLE),
        ).arrange(DOWN,buff=0.28).move_to(RIGHT*3.65+UP*0.04)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left),FadeIn(right),run_time=0.9)
        self.narrate(
            "Video bảy đã xây bộ khung cơ bản cho tỷ số thể tích. Một bài tốt không bắt đầu bằng việc tính từng thể tích, mà bắt đầu bằng việc tìm phần dữ kiện chung để triệt tiêu. Cùng đáy thì so chiều cao, cùng chiều cao thì so diện tích đáy, điểm chia cạnh tạo tỷ số tuyến tính, còn đồng dạng đưa ta từ k lên k bình phương và k lập phương. Khi ba điểm nằm trên ba cạnh cùng xuất phát từ một đỉnh, tích ba tỷ số là công cụ cực nhanh. Với chóp cụt, khôi phục chóp lớn thường giúp nhìn ra đồng dạng rõ hơn công thức trực tiếp.",2.0)
        self.narrate(
            "Video tám sẽ đi sâu hơn: nhiều điểm chia cạnh đồng thời, chia một tứ diện thành nhiều phần, đổi đỉnh liên tiếp, tỷ số thể tích có tham số, bài đúng sai dễ mắc bẫy và những cấu hình mà tỷ số cần được ghép qua hai hoặc ba khối trung gian. Mục tiêu của cả chặng C là nhìn thấy quan hệ thể tích trước khi nhìn thấy con số.",1.6)

    def construct(self):
        self.intro()
        self.method_map()
        self.basic_volume()
        self.same_base_same_height()
        self.one_edge_ratio()
        self.product_theorem()
        self.similar_section_dynamic()
        self.frustum_two_methods()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir=str(MEDIA_DIR)
    config.output_file="hhkg_chuyen_sau_07_the_tich_ty_so_I_typst_SAFE_1080p"
    config.format="mp4"
    config.write_to_movie=True
    config.disable_caching=False
    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 07")
    scene=SangLesson(); scene.render()
    video_path=Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")
    duration=probe_duration(video_path)
    master_wav=ROOT/"master_narration_hhkg_07.wav"
    build_master_audio(scene.audio_events,duration,master_wav)
    final_path=video_path.with_name(video_path.stem+"_WITH_AUDIO.mp4")
    mux_audio(video_path,master_wav,final_path)
    validate_audio(master_wav)
    print("\n============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path

if __name__ == "__main__":
    render_full()

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
# HHKG CHUYEN SAU 09 - THE TICH TU KHOANG CACH VA GOC - MANIM + TYPST SAFE
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
        series = txt("HHKG CHUYÊN SÂU · 09", 15, BLUE, BOLD)
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


    # ------------------------------------------------------
    # EXTRA MODELS FOR VIDEO 09
    # ------------------------------------------------------
    def oblique_tetrahedron(self, dim=False):
        # Exact visual angle AD with base plane: 30 degrees.
        A = L(-2.3, -1.8, 0.0)
        B = L( 2.2, -1.8, 0.0)
        C = L(-2.3,  2.0, 0.0)
        H = L( 0.1, -0.1, 0.0)
        D = L( 0.1, -0.1, 1.7)
        vc = DIM if dim else EDGE
        vo = 0.42 if dim else 0.94
        vw = 2.4 if dim else 3.7
        visible = VGroup(
            solid(A, B, vc, vw, vo), solid(A, C, vc, vw, vo),
            solid(A, D, vc, vw, vo), solid(B, D, vc, vw, vo), solid(C, D, vc, vw, vo),
        )
        hidden = VGroup(hidden_edge(B, C, DIM, 2.6, 0.68))
        base = face(A, B, C, color=BLUE, opacity=0.09)
        dots = VGroup(
            Dot3D(A, radius=0.05, color=GOLD), Dot3D(B, radius=0.05, color=GOLD),
            Dot3D(C, radius=0.05, color=GOLD), Dot3D(D, radius=0.06, color=RED),
            Dot3D(H, radius=0.045, color=CYAN),
        )
        return {"A":A,"B":B,"C":C,"D":D,"H":H,"edges":VGroup(visible, hidden),"base":base,"dots":dots}

    def edge_dihedral_tetrahedron(self, beta_deg=60):
        # AB is the common edge. HC and HS form the normal section at H.
        A = L(-3.0, 0.0, 0.0)
        B = L( 3.0, 0.0, 0.0)
        H = L( 0.0, 0.0, 0.0)
        C = L( 0.0, 4.0, 0.0)
        beta = beta_deg * DEGREES
        S = L(0.0, 5.0*math.cos(beta), 5.0*math.sin(beta))
        base = face(A, B, C, color=BLUE, opacity=0.10)
        side = face(A, B, S, color=PURPLE, opacity=0.14)
        edges = VGroup(
            solid(A,B,GOLD,5.1,1.0), solid(A,C,EDGE,3.5,0.90), solid(B,C,EDGE,3.5,0.90),
            solid(A,S,EDGE,3.5,0.90), solid(B,S,EDGE,3.5,0.90),
            hidden_edge(C,S,DIM,2.5,0.62),
        )
        dots = VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,H]], Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"H":H,"S":S,"base":base,"side":side,"edges":edges,"dots":dots}

    def square_pyramid_4(self, dim=False):
        A=L(-2,-2,0); B=L(2,-2,0); C=L(2,2,0); D=L(-2,2,0); S=L(-2,-2,3)
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(solid(A,B,vc,vw,vo),solid(B,C,vc,vw,vo),solid(S,A,vc,vw,vo),solid(S,B,vc,vw,vo),solid(S,C,vc,vw,vo))
        hidden=VGroup(hidden_edge(C,D,DIM,2.6,0.68),hidden_edge(D,A,DIM,2.6,0.68),hidden_edge(S,D,DIM,2.6,0.68))
        base=face(A,B,C,D,color=BLUE,opacity=0.08)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]], Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        title = txt("HHKG CHUYÊN SÂU 09", 46, GOLD, BOLD)
        sub = txt("THỂ TÍCH TỪ KHOẢNG CÁCH VÀ GÓC", 34, INK, BOLD)
        line = txt("Góc → chiều cao → thể tích → khoảng cách → bài ngược", 23, CYAN, BOLD)
        note = txt("Dùng thể tích như chiếc cầu nối nhiều đại lượng không gian", 22, MUTED)
        brand = txt(TEN_THAY, 20, MUTED)
        g = VGroup(title, sub, line, note, brand).arrange(DOWN, buff=0.28)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g, shift=UP*0.10), run_time=1.0)
        self.narrate(
            "Video chín khép lại chặng thể tích bằng một ý rất quan trọng: thể tích không chỉ là đại lượng cần tính ở cuối bài. "
            "Nó còn là chiếc cầu nối góc, khoảng cách và diện tích. Nếu biết góc giữa một cạnh và mặt phẳng, ta lấy được chiều cao rồi suy ra thể tích. "
            "Nếu biết thể tích và diện tích một mặt, ta suy ngược ra khoảng cách đến mặt ấy. Với góc nhị diện, mặt cắt vuông góc cạnh chung biến chiều cao thành một thành phần lượng giác. "
            "Ta còn dùng diện tích hình chiếu để nối góc giữa hai mặt với diện tích thật. Mục tiêu của video là nhìn ba chương góc, khoảng cách, thể tích như một hệ thống duy nhất.",
            2.0,
        )

    # ======================================================
    # METHOD MAP
    # ======================================================
    def method_map(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_header("Bản đồ liên kết", "Một chuỗi suy luận dùng được cho rất nhiều bài HHKG", "2/11")
        left = VGroup(
            txt("1. Góc đường–mặt cho thành phần vuông góc", 22, INK, BOLD),
            txt("2. Thành phần vuông góc chính là chiều cao", 22, INK, BOLD),
            txt("3. Chiều cao + diện tích đáy → thể tích", 22, INK, BOLD),
            txt("4. Đổi đáy → thể tích cho một khoảng cách mới", 22, INK, BOLD),
            txt("5. Góc nhị diện → xét mặt cắt vuông góc cạnh chung", 22, INK, BOLD),
            txt("6. Hình chiếu diện tích → nối hai mặt phẳng", 22, INK, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(LEFT*2.25+UP*0.08)
        right = VGroup(
            mty("h = l sin alpha", 28, CYAN),
            mty("V = frac(1, 3) S h", 28, GREEN),
            mty("h = frac(3 V, S)", 28, GOLD),
            mty("S_0 = S cos beta", 28, PURPLE),
        ).arrange(DOWN, buff=0.38).move_to(RIGHT*3.60+UP*0.10)
        self.add_fixed_in_frame_mobjects(left, right)
        self.play(FadeIn(left), FadeIn(right), run_time=0.9)
        self.narrate(
            "Có một chuỗi suy luận nên thuộc bằng tư duy chứ không học thuộc máy móc. Một đoạn dài l tạo với mặt phẳng góc alpha thì thành phần vuông góc của nó là l nhân sin alpha. "
            "Đó chính là chiều cao nếu một đầu đoạn nằm trên mặt phẳng. Từ chiều cao ta có thể tích. Nhưng thể tích của cùng một khối không phụ thuộc cách ta chọn đáy. "
            "Đổi sang một mặt khác làm đáy, ta có thể giải ngược một khoảng cách hoàn toàn mới bằng ba V chia diện tích mặt ấy. Với hai mặt phẳng, diện tích hình chiếu lại cho hệ số cos của góc giữa chúng. "
            "Video này sẽ luyện cả chiều thuận, chiều ngược và cách ghép nhiều mắt xích trong một bài.",
            2.1,
        )

    # ======================================================
    # 1. LINE-PLANE ANGLE -> VOLUME
    # ======================================================
    def angle_to_volume(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 1 · Góc đường–mặt → thể tích", "S_ABC = 24, AD = 10, góc giữa AD và đáy bằng 30°", "3/11")
        G = self.oblique_tetrahedron()
        self.add(G["base"], G["edges"], G["dots"])
        for n in ["A","B","C","D","H"]:
            self.add_label(n, G[n], RED if n=="D" else (CYAN if n=="H" else GOLD))
        dh = aux(G["D"], G["H"], GREEN, 4.7, 0.95)
        ah = aux(G["A"], G["H"], CYAN, 4.0, 0.88)
        mark = right_angle_3d(G["H"], G["A"]-G["H"], G["D"]-G["H"], size=0.24, color=GOLD)
        ad_dir = (G["A"]-G["H"]); ad_dir = ad_dir/np.linalg.norm(ad_dir)
        dh_dir = (G["D"]-G["H"]); dh_dir = dh_dir/np.linalg.norm(dh_dir)
        # Angle at A between AD and its projection AH.
        e1=(G["H"]-G["A"]); e1=e1/np.linalg.norm(e1)
        e2=(G["D"]-G["A"]); e2=e2/np.linalg.norm(e2)
        ang=math.acos(np.clip(np.dot(e1,e2),-1,1))
        arc=arc_basis(G["A"], e1, (e2-np.dot(e2,e1)*e1), ang, radius=0.40, color=GOLD)
        self.play(Create(ah), Create(dh), Create(mark), Create(arc), run_time=0.9)
        self.card("ĐỔI GÓC THÀNH CHIỀU CAO", "Không cần dựng thêm tam giác phụ phức tạp", [
            ("text", "Góc(AD, (ABC)) = 30°", 19, CYAN, BOLD),
            ("math", "D H = A D sin alpha", 28, GREEN),
            ("math", "D H = 10 times frac(1, 2) = 5", 27, GOLD),
            ("math", "V_(D A B C) = frac(1, 3) S_(A B C) D H", 25, INK),
            ("math", "V_(D A B C) = frac(1, 3) times 24 times 5 = 40", 27, GOLD),
        ], accent=CYAN)
        self.narrate(
            "Cho tứ diện DABC có diện tích đáy ABC bằng hai mươi bốn, cạnh AD dài mười và tạo với mặt phẳng ABC góc ba mươi độ. H là hình chiếu vuông góc của D xuống đáy. "
            "Góc giữa AD và mặt phẳng chính là góc giữa AD và hình chiếu AH. Vì tam giác ADH vuông tại H, chiều cao DH bằng AD nhân sin alpha. Với sin ba mươi độ bằng một phần hai, DH bằng năm.",
            1.8,
        )
        self.narrate(
            "Từ đây thể tích gần như tự động: một phần ba nhân diện tích đáy hai mươi bốn nhân chiều cao năm, được bốn mươi. Điều cần nhớ không phải con số bốn mươi mà là công thức tổng quát: nếu một cạnh dài l đi từ điểm trên đáy lên đỉnh và tạo với đáy góc alpha, thì chiều cao bằng l sin alpha. "
            "Vì thế V bằng một phần ba S l sin alpha. Góc đường–mặt thực chất đang mã hóa chiều cao của khối.",
            2.0,
        )
        self.takeaway("Góc đường–mặt → lấy thành phần vuông góc l·sin α → có chiều cao")

    # ======================================================
    # 2. VOLUME -> LINE-PLANE ANGLE
    # ======================================================
    def reverse_line_plane_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 2 · Bài ngược", "Biết V = 40, S_ABC = 24, AD = 10 — tìm góc giữa AD và đáy", "4/11")
        G = self.oblique_tetrahedron()
        self.add(G["base"], G["edges"], G["dots"])
        for n in ["A","B","C","D","H"]:
            self.add_label(n, G[n], RED if n=="D" else (CYAN if n=="H" else GOLD))
        self.add(aux(G["D"],G["H"],GREEN,4.7,0.95), aux(G["A"],G["H"],CYAN,4.0,0.88))
        self.card("ĐI NGƯỢC", "Thể tích cho chiều cao, chiều cao cho sin góc", [
            ("math", "D H = frac(3 V, S_(A B C))", 28, CYAN),
            ("math", "D H = frac(3 times 40, 24) = 5", 27, GOLD),
            ("math", "sin alpha = frac(D H, A D)", 28, GREEN),
            ("math", "sin alpha = frac(5, 10) = frac(1, 2)", 29, GOLD),
            ("text", "Suy ra α = 30°", 20, PURPLE, BOLD),
        ], accent=GREEN)
        self.narrate(
            "Bài hai đảo toàn bộ quá trình. Vẫn tứ diện ấy nhưng lần này không cho góc. Ta biết thể tích bằng bốn mươi, diện tích đáy bằng hai mươi bốn và AD bằng mười. "
            "Từ V bằng một phần ba S nhân h, giải ngược chiều cao DH bằng ba V chia S, tức bằng năm. Sau đó trong tam giác vuông ADH, sin alpha bằng DH trên AD, bằng một phần hai.",
            1.9,
        )
        self.narrate(
            "Vì alpha là góc nhọn giữa đường thẳng và mặt phẳng, sin alpha bằng một phần hai cho alpha bằng ba mươi độ. Dạng bài này rất hay xuất hiện theo kiểu dữ kiện gián tiếp: đề không cho chiều cao, cũng không cho góc, mà cho thể tích. "
            "Hãy nghĩ thể tích như một phương trình chứa chiều cao. Giải phương trình ấy trước rồi mới quay về lượng giác. Đây là mẫu nhận dạng đầu tiên của video: V có thể dùng để khôi phục góc đường–mặt.",
            2.0,
        )
        self.takeaway("Bài ngược: V → h = 3V/S → sin α = h/l")

    # ======================================================
    # 3. DIHEDRAL ANGLE -> VOLUME
    # ======================================================
    def dihedral_to_volume(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES, theta=-60*DEGREES, zoom=0.94)
        self.add_header("Bài 3 · Góc nhị diện → thể tích", "AB = 6, CH = 4, SH = 5, góc nhị diện theo AB bằng 60°", "5/11")
        G = self.edge_dihedral_tetrahedron(60)
        self.add(G["base"], G["side"], G["edges"], G["dots"])
        for n in ["A","B","C","H","S"]:
            self.add_label(n,G[n],RED if n=="S" else (CYAN if n=="H" else GOLD),off=(0.08,0.06,0.06))
        hc=solid(G["H"],G["C"],CYAN,5.0,1.0); hs=solid(G["H"],G["S"],GREEN,5.0,1.0)
        m1=right_angle_3d(G["H"],G["B"]-G["H"],G["C"]-G["H"],size=0.24,color=CYAN)
        m2=right_angle_3d(G["H"],G["B"]-G["H"],G["S"]-G["H"],size=0.24,color=GREEN)
        e1=(G["C"]-G["H"]); e1=e1/np.linalg.norm(e1)
        e2=(G["S"]-G["H"]); e2=e2/np.linalg.norm(e2)
        beta=math.acos(np.clip(np.dot(e1,e2),-1,1))
        normal_comp=e2-np.dot(e2,e1)*e1
        arc=arc_basis(G["H"],e1,normal_comp,beta,radius=0.42,color=GOLD)
        self.play(Create(hc),Create(hs),Create(m1),Create(m2),Create(arc),run_time=1.0)
        self.card("MẶT CẮT VUÔNG GÓC AB", "Góc nhị diện biến thành góc CHS", [
            ("math", "beta = hat(C H S, size: #145%)", 27, GOLD),
            ("math", "h = S H sin beta", 28, GREEN),
            ("math", "S_(A B C) = frac(1, 2) A B times C H", 25, CYAN),
            ("math", "V = frac(1, 6) A B times C H times S H times sin beta", 22, INK),
            ("math", "V = 10 sqrt(3)", 31, GOLD),
        ], accent=PURPLE)
        self.narrate(
            "Bài ba nối góc nhị diện với thể tích. Hai mặt ABC và ABS có cạnh chung AB. Tại H trên AB, ta có HC vuông góc AB trong mặt đáy và HS vuông góc AB trong mặt bên. Vì vậy góc CHS chính là góc nhị diện beta. "
            "Trong mặt cắt vuông góc AB, thành phần của SH vuông góc với mặt ABC bằng SH nhân sin beta. Đó chính là chiều cao của S xuống đáy ABC.",
            2.0,
        )
        self.narrate(
            "Diện tích tam giác ABC bằng một phần hai AB nhân CH. Ghép với chiều cao SH sin beta, ta được một công thức rất đẹp: V bằng một phần sáu AB nhân CH nhân SH nhân sin beta. "
            "Với AB bằng sáu, CH bằng bốn, SH bằng năm và beta bằng sáu mươi độ, thể tích bằng mười căn ba. Công thức này đặc biệt hữu ích khi đề cho hai khoảng cách vuông góc với cùng một cạnh và cho góc nhị diện giữa hai mặt.",
            2.1,
        )
        self.takeaway("Góc nhị diện → mặt cắt vuông góc cạnh chung → chiều cao chứa sin β")

    # ======================================================
    # 4. VOLUME -> DIHEDRAL ANGLE
    # ======================================================
    def reverse_dihedral(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES, theta=-60*DEGREES, zoom=0.94)
        self.add_header("Bài 4 · Bài ngược góc nhị diện", "AB = 6, CH = 4, SH = 5, V = 10 — tìm β", "6/11")
        G = self.edge_dihedral_tetrahedron(30)
        self.add(G["base"],G["side"],G["edges"],G["dots"])
        for n in ["A","B","C","H","S"]:
            self.add_label(n,G[n],RED if n=="S" else (CYAN if n=="H" else GOLD),off=(0.08,0.06,0.06))
        self.add(solid(G["H"],G["C"],CYAN,5.0),solid(G["H"],G["S"],GREEN,5.0))
        self.card("GIẢI NGƯỢC SIN β", "Thể tích xác định góc giữa hai mặt", [
            ("math", "V = frac(1, 6) A B times C H times S H times sin beta", 22, CYAN),
            ("math", "10 = frac(1, 6) times 6 times 4 times 5 times sin beta", 22, INK),
            ("math", "sin beta = frac(1, 2)", 29, GOLD),
            ("text", "Vì β là góc nhị diện nhọn nên β = 30°", 18, PURPLE, BOLD),
        ], accent=GOLD)
        self.narrate(
            "Ta đảo tiếp công thức vừa có. Giữ AB bằng sáu, CH bằng bốn, SH bằng năm nhưng chỉ biết thể tích bằng mười. Thay vào công thức một phần sáu AB CH SH sin beta, mọi độ dài đã biết và ẩn duy nhất là sin beta. "
            "Ta thu được mười bằng hai mươi nhân sin beta, nên sin beta bằng một phần hai.",
            1.7,
        )
        self.narrate(
            "Nếu bài đang xét góc nhị diện nhọn, beta bằng ba mươi độ. Điểm đáng chú ý là ta không phải dựng chiều cao từ S xuống mặt ABC một cách trực tiếp. Mặt cắt vuông góc cạnh chung đã biến góc nhị diện thành thành phần vuông góc của SH, còn thể tích đóng vai trò phương trình để giải góc. "
            "Đây là một dạng bài ngược khá mạnh: dữ kiện thể tích có thể quyết định cả góc giữa hai mặt phẳng.",
            2.0,
        )
        self.takeaway("V + ba độ dài trong mặt cắt chuẩn → giải sin β → suy ra góc nhị diện")

    # ======================================================
    # 5. AREA PROJECTION + DIHEDRAL
    # ======================================================
    def projection_area(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-52*DEGREES, zoom=0.96)
        self.add_header("Bài 5 · Diện tích hình chiếu", "Mặt (SBC) chiếu vuông góc xuống đáy thành tam giác ABC", "7/11")
        G=self.square_pyramid_4()
        self.add(G["base"],G["edges"],G["dots"])
        for n in ["A","B","C","D","S"]:
            self.add_label(n,G[n],RED if n=="S" else GOLD)
        side=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.22)
        proj=face(G["A"],G["B"],G["C"],color=CYAN,opacity=0.24)
        sa=aux(G["S"],G["A"],GREEN,4.0,0.90)
        self.play(FadeIn(side),FadeIn(proj),Create(sa),run_time=0.9)
        self.card("CÔNG THỨC HÌNH CHIẾU", "Diện tích giảm theo cos góc giữa hai mặt", [
            ("math", "S_0 = S cos beta", 30, CYAN),
            ("math", "S_(A B C) = 8", 27, GREEN),
            ("math", "S_(S B C) = 10", 27, PURPLE),
            ("math", "cos beta = frac(S_(A B C), S_(S B C))", 25, INK),
            ("math", "cos beta = frac(8, 10) = frac(4, 5)", 29, GOLD),
        ], accent=CYAN)
        self.narrate(
            "Một liên kết ít được khai thác đúng mức là diện tích hình chiếu. Trong hình chóp vuông S.ABCD, khi chiếu vuông góc mặt tam giác SBC xuống đáy, S rơi xuống A còn B và C giữ nguyên, nên hình chiếu chính là tam giác ABC. "
            "Nếu beta là góc giữa mặt SBC và mặt đáy, diện tích hình chiếu S không bằng diện tích thật, mà bằng diện tích thật nhân cos beta.",
            1.9,
        )
        self.narrate(
            "Ở cấu hình cạnh đáy bốn và SA bằng ba, tam giác ABC vuông có diện tích tám. Tam giác SBC vuông tại B, với BC bằng bốn và SB bằng năm, nên diện tích bằng mười. Vì vậy cos beta bằng tám phần mười, tức bốn phần năm. "
            "Công thức S không bằng S cos beta là cách rất nhanh để đổi qua lại giữa diện tích thật, diện tích hình chiếu và góc giữa hai mặt. Nó sẽ còn xuất hiện trong bài thiết diện và hình chiếu ở các video sau.",
            2.0,
        )
        self.takeaway("Hình chiếu vuông góc của một miền phẳng: S₀ = S·cos β")

    # ======================================================
    # 6. VOLUME -> DISTANCE TO A DIFFERENT FACE
    # ======================================================
    def distance_from_volume(self):
        self.clear_all()
        self.set_camera_orientation(phi=69*DEGREES, theta=-54*DEGREES, zoom=0.96)
        self.add_header("Bài 6 · Đổi đáy để tìm khoảng cách", "Tính d(D, (SBC)) mà không dựng chân vuông góc", "8/11")
        G=self.square_pyramid_4()
        self.add(G["base"],G["edges"],G["dots"])
        for n in ["A","B","C","D","S"]:
            self.add_label(n,G[n],RED if n=="S" else GOLD)
        side=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.24)
        self.add(side)
        # Exact perpendicular foot H of D on plane (SBC).
        n = np.cross(G["B"]-G["S"], G["C"]-G["S"])
        H = G["D"] - n * (np.dot(G["D"]-G["S"], n) / np.dot(n, n))
        dh=aux(G["D"],H,GOLD,4.6,0.95)
        mark=right_angle_3d(H, G["D"]-H, G["C"]-G["B"], size=0.22, color=GOLD)
        self.add(dh,mark,Dot3D(H,radius=0.045,color=GOLD))
        self.add_label("H",H,GOLD,off=(0.08,0.05,0.06),size=20)
        self.card("THỂ TÍCH LÀ BẤT BIẾN", "Cùng một tứ diện, đổi mặt SBC thành đáy", [
            ("math", "V_(S B C D) = 8", 28, CYAN),
            ("math", "S_(S B C) = 10", 28, PURPLE),
            ("math", "V_(S B C D) = frac(1, 3) S_(S B C) h_D", 24, INK),
            ("math", "h_D = frac(3 V, S_(S B C))", 27, GREEN),
            ("math", "h_D = frac(24, 10) = frac(12, 5)", 30, GOLD),
        ], accent=GOLD)
        self.narrate(
            "Bài sáu cho thấy vì sao thể tích là chiếc cầu rất mạnh. Ta cần khoảng cách từ D đến mặt SBC. Dựng trực tiếp chân H trong không gian không hề dễ. Nhưng tứ diện SBCD đã có thể tích bằng tám: đáy BCD chiếm một nửa hình vuông ABCD và cùng chiều cao SA nên nó chiếm một nửa thể tích hình chóp, tức tám. "
            "Từ bài trước, diện tích mặt SBC bằng mười.",
            1.9,
        )
        self.narrate(
            "Bây giờ đổi vai trò: xem SBC là đáy của tứ diện SBCD. Chiều cao tương ứng chính là khoảng cách cần tìm từ D tới mặt SBC. Ta có tám bằng một phần ba nhân mười nhân hD, nên hD bằng mười hai phần năm. "
            "Mẫu nhận dạng rất quan trọng là: khi khoảng cách đến mặt phẳng khó dựng, hãy hỏi xem khối chứa điểm ấy có thể tích đã biết hoặc dễ tính hay không. Nếu có, ba V chia diện tích mặt thường kết thúc bài ngay.",
            2.0,
        )
        self.takeaway("Khoảng cách khó dựng → đổi mặt cần đo thành đáy → h = 3V/S")

    # ======================================================
    # 7. MOVING POINT: VOLUME IS LINEAR IN DISTANCE
    # ======================================================
    def dynamic_point_volume(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 7 · Điểm động trên cạnh xiên", "M chạy trên AD — thể tích MABC thay đổi thế nào?", "9/11")
        G=self.oblique_tetrahedron()
        self.add(G["base"],G["edges"],G["dots"])
        for n in ["A","B","C","D"]:
            self.add_label(n,G[n],RED if n=="D" else GOLD)
        u=ValueTracker(0.10)
        def mp(): return G["A"]+u.get_value()*(G["D"]-G["A"])
        M=always_redraw(lambda: Dot3D(mp(),radius=0.060,color=GOLD))
        am=always_redraw(lambda: solid(G["A"],mp(),GOLD,5.0,1.0))
        mh=always_redraw(lambda: aux(mp(), np.array([mp()[0],mp()[1],G["A"][2]]), GREEN,3.8,0.88))
        tetra_faces=always_redraw(lambda: VGroup(
            face(mp(),G["A"],G["B"],color=GOLD,opacity=0.08),
            face(mp(),G["A"],G["C"],color=GOLD,opacity=0.08),
            face(mp(),G["B"],G["C"],color=GOLD,opacity=0.14),
        ))
        self.add(tetra_faces,am,mh,M)
        read=always_redraw(lambda: VGroup(
            txt(f"u = {u.get_value():.2f}",18,ORANGE,BOLD),
            txt(f"V/Vmax = {u.get_value():.2f}",18,GOLD,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.07).move_to(RIGHT*4.18+DOWN*2.02))
        self.add_fixed_in_frame_mobjects(read)
        self.card("TUYẾN TÍNH", "AM/AD = u nên khoảng cách và thể tích cùng tỷ lệ u", [
            ("math", "frac(A M, A D) = u", 28, CYAN),
            ("math", "h_M = u h_D", 28, GREEN),
            ("math", "frac(V_(M A B C), V_(D A B C)) = u", 25, INK),
            ("math", "V_(D A B C) = 40", 27, PURPLE),
            ("math", "V_(M A B C) = 40 u", 31, GOLD),
        ], accent=ORANGE)
        self.narrate_play(
            "Cho M chạy từ A tới D và đặt AM trên AD bằng u. Vì A nằm trên mặt ABC, khoảng cách từ điểm M trên đường AD tới mặt ABC tăng tuyến tính theo vị trí trên đoạn AD. Cụ thể, chiều cao từ M chỉ bằng u lần chiều cao từ D. "
            "Hai tứ diện MABC và DABC có chung đáy ABC, nên tỷ số thể tích đúng bằng tỷ số chiều cao, tức bằng u. Quan sát khi M đi lên, thể tích phần vàng tăng đều từ gần không đến toàn bộ khối.",
            u.animate.set_value(0.90), min_time=5.2,
        )
        self.narrate_play(
            "Vì thể tích lớn nhất của DABC là bốn mươi, ta có V của MABC bằng bốn mươi u. Đây là một kết quả rất hữu ích cho bài điểm động: nếu điểm chạy trên một đường cắt mặt đáy tại A, thì khoảng cách đến mặt và thể tích chung đáy biến thiên tuyến tính theo tham số chia đoạn. "
            "Không cần tọa độ, không cần đạo hàm. Chỉ khi có thêm một đại lượng phi tuyến khác thì bài cực trị mới thật sự xuất hiện.",
            u.animate.set_value(0.50), min_time=4.2,
        )
        self.takeaway("Điểm chạy trên đường cắt mặt tại A → khoảng cách và thể tích chung đáy biến thiên tuyến tính")

    # ======================================================
    # 8. CAPSTONE CHAIN: ANGLE -> V -> NEW DISTANCE
    # ======================================================
    def synthesis_chain(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bài 8 · Chuỗi tổng hợp", "Từ một góc đường–mặt suy ra khoảng cách đến một mặt khác", "10/11")
        G=self.oblique_tetrahedron()
        P=G["D"]
        self.add(G["base"],G["edges"],G["dots"])
        for n,p in [("A",G["A"]),("B",G["B"]),("C",G["C"]),("P",P)]:
            self.add_label(n,p,RED if n=="P" else GOLD)
        target=face(P,G["B"],G["C"],color=PURPLE,opacity=0.22)
        self.add(target)
        self.card("MỘT CHUỖI 3 MẮT XÍCH", "Góc → chiều cao → V → khoảng cách mới", [
            ("text", "S(ABC)=18,  PA=12,  góc(PA,(ABC))=30°", 17, CYAN, BOLD),
            ("text", "S(PBC)=15", 18, PURPLE, BOLD),
            ("math", "h_P = 12 times frac(1, 2) = 6", 27, GREEN),
            ("math", "V_(P A B C) = frac(1, 3) times 18 times 6 = 36", 25, GOLD),
            ("math", "h_A = frac(3 times 36, 15) = frac(36, 5)", 26, GOLD),
        ], accent=PURPLE)
        self.narrate(
            "Bài tổng hợp cuối cùng nối toàn bộ video trong một chuỗi. Cho tứ diện PABC, diện tích ABC bằng mười tám, PA bằng mười hai và góc giữa PA với mặt ABC bằng ba mươi độ. Đồng thời diện tích mặt PBC bằng mười lăm. Hỏi khoảng cách từ A đến mặt PBC. "
            "Ta chưa hề biết chân vuông góc từ A xuống PBC và cũng không cần dựng nó.",
            1.8,
        )
        self.narrate(
            "Mắt xích thứ nhất: góc đường–mặt cho chiều cao từ P xuống ABC bằng mười hai nhân một phần hai, tức sáu. Mắt xích thứ hai: thể tích tứ diện bằng một phần ba nhân mười tám nhân sáu, được ba mươi sáu. Mắt xích thứ ba: đổi mặt PBC thành đáy. "
            "Khoảng cách từ A đến mặt ấy bằng ba lần thể tích chia diện tích PBC, tức một trăm lẻ tám chia mười lăm, bằng ba mươi sáu phần năm. Một bài tưởng cần hai phép dựng vuông góc trong không gian lại được giải bằng một chuỗi đại lượng rất mạch lạc.",
            2.1,
        )
        self.takeaway("Chuỗi mạnh: góc → h₁ → V → đổi đáy → h₂")

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Tổng kết Video 09", "Khép lại Chặng C — góc, khoảng cách và thể tích là một hệ thống", "11/11")
        left=VGroup(
            txt("7 mẫu nhận dạng cần mang sang các chương sau",25,GOLD,BOLD),
            txt("• Góc đường–mặt → h = l·sin α",19,INK),
            txt("• Biết V → h = 3V/S → tìm lại góc",19,INK),
            txt("• Góc nhị diện → mặt cắt vuông góc cạnh chung",19,INK),
            txt("• S hình chiếu = S thật · cos β",19,INK),
            txt("• Khoảng cách khó dựng → đổi đáy bằng thể tích",19,INK),
            txt("• Điểm động trên đường cắt mặt → V tuyến tính",19,INK),
            txt("• Chuỗi tổng hợp: góc → V → khoảng cách mới",19,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.19).move_to(LEFT*2.25+UP*0.02)
        right=VGroup(
            mty("h = l sin alpha",26,CYAN),
            mty("V = frac(1, 3) S h",26,GREEN),
            mty("h = frac(3 V, S)",26,GOLD),
            mty("S_0 = S cos beta",26,PURPLE),
            mty("V = frac(1, 6) a p q sin beta",23,ORANGE),
        ).arrange(DOWN,buff=0.30).move_to(RIGHT*3.65+UP*0.05)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left),FadeIn(right),run_time=0.9)
        self.narrate(
            "Video chín đã hoàn thành chặng C của series. Ta bắt đầu từ công thức thể tích quen thuộc nhưng dùng nó theo cả hai chiều. Góc đường–mặt cho chiều cao, thể tích cho lại chiều cao, góc nhị diện cho thành phần vuông góc qua mặt cắt chuẩn, diện tích hình chiếu cho cos góc giữa hai mặt, và đổi đáy cho phép biến thể tích thành một khoảng cách rất khó dựng. "
            "Với điểm động, thể tích chung đáy còn cho ta một quy luật tuyến tính gần như ngay lập tức.",
            2.0,
        )
        self.narrate(
            "Từ video mười, series chuyển sang Chặng D: thiết diện. Đây là phần cần hình 3D đặc biệt chuẩn, vì sai một giao tuyến là toàn bộ hình cắt sai. Ta sẽ bắt đầu bằng cách dựng thiết diện đúng theo ba nguyên tắc: tìm hai điểm chung để dựng giao tuyến, tận dụng hai mặt phẳng song song, và đi liên tục qua các mặt của đa diện. "
            "Sau đó mới nâng lên diện tích thiết diện, tỷ số, điểm động và cực trị. Hệ thống góc, khoảng cách, thể tích vừa học sẽ trở thành công cụ tính toán cho chính các thiết diện ấy.",
            1.9,
        )

    def construct(self):
        self.intro()
        self.method_map()
        self.angle_to_volume()
        self.reverse_line_plane_angle()
        self.dihedral_to_volume()
        self.reverse_dihedral()
        self.projection_area()
        self.distance_from_volume()
        self.dynamic_point_volume()
        self.synthesis_chain()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_09_the_tich_tu_khoang_cach_va_goc_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 09")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_09.wav"
    build_master_audio(scene.audio_events, duration, master_wav)

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

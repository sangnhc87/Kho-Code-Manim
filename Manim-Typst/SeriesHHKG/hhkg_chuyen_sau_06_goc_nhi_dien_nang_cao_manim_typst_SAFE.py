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
# HHKG CHUYEN SAU 05 - MANIM + TYPST - MASTER TEMPLATE
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

    def narrate_camera(self, text, **kwargs):
        return self.narrate(text, min_visual_time=1.8)

    # ------------------------------------------------------
    # FIXED MASTER UI
    # ------------------------------------------------------
    def clear_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.30)
        self.clear()

    def add_header(self, title, subtitle, progress):
        series = txt("HHKG CHUYÊN SÂU · 06", 15, BLUE, BOLD)
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
        hud=VGroup(series,title_m,sub_m,accent,prog,rule,divider,teacher)
        self.add_fixed_in_frame_mobjects(hud)
        return hud

    def card(self, kicker, title, items, accent=GOLD, height=5.25, auto_add=True):
        bg=Rectangle(width=5.12,height=height,fill_color=PANEL,fill_opacity=0.90,
                     stroke_color=GRID,stroke_width=0.9,stroke_opacity=0.36).move_to(RIGHT*4.28+DOWN*0.03)
        spine=Line(bg.get_corner(UL)+RIGHT*0.12+DOWN*0.18,
                   bg.get_corner(DL)+RIGHT*0.12+UP*0.18,
                   color=accent,stroke_width=3.8,stroke_opacity=0.95)
        k=txt(kicker.upper(),14,accent,BOLD)
        k.move_to(bg.get_corner(UL)+RIGHT*0.36+DOWN*0.30,aligned_edge=LEFT)
        t=fit_width(txt(title,23,INK,BOLD),4.30)
        t.next_to(k,DOWN,buff=0.10,aligned_edge=LEFT)
        body=VGroup()
        for item in items:
            kind=item[0]
            if kind=="text":
                _,s,size,color,weight=item; mob=txt(s,size,color,weight)
            elif kind=="math":
                _,expr,size,color=item; mob=mty(expr,size,color)
            elif kind=="sep":
                mob=Line(LEFT*2.00,RIGHT*2.00,color=GRID,stroke_width=0.9,stroke_opacity=0.55)
            elif kind=="obj":
                mob=item[1]
            else:
                raise ValueError(kind)
            body.add(fit_width(mob,4.28))
        body.arrange(DOWN,aligned_edge=LEFT,buff=0.18)
        body.next_to(t,DOWN,buff=0.22,aligned_edge=LEFT)
        fit_height(body,height-1.45)
        group=VGroup(bg,spine,k,t,body)
        if auto_add:
            self.add_fixed_in_frame_mobjects(group)
        return group

    def takeaway(self, text_s):
        label=fit_width(txt(text_s,16,CYAN,BOLD),7.15)
        label.move_to(LEFT*2.55+DOWN*2.52)
        self.add_fixed_in_frame_mobjects(label)
        return label

    def add_label(self, name, pt, color=GOLD, off=(0.10,-0.10,0.05), size=22):
        lab=mty(name,size,color).move_to(pt+np.array(off,dtype=float))
        self.add_fixed_orientation_mobjects(lab)
        return lab

    # ------------------------------------------------------
    # MODELS
    # ------------------------------------------------------
    def oblique_prism(self, dim=False):
        # Right triangular base ABC; lateral vector (0,1,2) makes an oblique prism.
        A=L(-2.2,-1.8,0); B=L(2.2,-1.8,0); C=L(-2.2,1.5,0)
        v=GEO_SCALE*np.array([0.0,1.0,2.0])
        A1=A+v; B1=B+v; C1=C+v
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        hc="#405A73" if dim else DIM; ho=0.42 if dim else 0.70; hw=2.1 if dim else 2.6
        visible=VGroup(
            solid(A,B,vc,vw,vo), solid(A,C,vc,vw,vo), solid(A,A1,vc,vw,vo),
            solid(B,B1,vc,vw,vo), solid(A1,B1,vc,vw,vo), solid(A1,C1,vc,vw,vo),
        )
        hidden=VGroup(
            hidden_edge(B,C,hc,hw,ho), hidden_edge(B1,C1,hc,hw,ho), hidden_edge(C,C1,hc,hw,ho)
        )
        base=face(A,B,C,color=BLUE,opacity=0.07,stroke_width=0)
        side=face(A,B,B1,A1,color=PURPLE,opacity=0.12,stroke_width=0)
        top=face(A1,B1,C1,color=CYAN,opacity=0.035,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,A1,B1,C1]])
        return {"A":A,"B":B,"C":C,"A1":A1,"B1":B1,"C1":C1,
                "edges":VGroup(visible,hidden),"base":base,"side":side,"top":top,"dots":dots}

    def right_tri_pyramid(self, a=4.0, h=3.0, dim=False):
        # Similar drawing with the correct h/a ratio.
        draw_a = 4.0
        draw_h = draw_a * float(h) / float(a)
        A=L(-2.0,-1.6,0); B=L(2.0,-1.6,0); C=L(-2.0,2.4,0); S=L(-2.0,-1.6,draw_h)
        M=(B+C)/2
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(solid(A,B,vc,vw,vo),solid(A,C,vc,vw,vo),solid(S,A,vc,vw,vo),solid(S,B,vc,vw,vo),solid(S,C,vc,vw,vo))
        hidden=VGroup(hidden_edge(B,C,DIM,2.6,0.68))
        base=face(A,B,C,color=BLUE,opacity=0.08,stroke_width=0)
        side=face(S,B,C,color=PURPLE,opacity=0.16,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,M]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"S":S,"M":M,"edges":VGroup(visible,hidden),"base":base,"side":side,"dots":dots}

    def rectangular_pyramid(self, a=3.0, b=5.0, h=4.0, dim=False):
        # Preserve the proportions a:b:h while fitting the teaching viewport.
        m=max(float(a),float(b),float(h))
        dx=4.2*float(a)/m; dy=4.2*float(b)/m; dz=4.2*float(h)/m
        A=L(-dx/2,-dy/2,0); B=L(dx/2,-dy/2,0); C=L(dx/2,dy/2,0); D=L(-dx/2,dy/2,0); S=L(-dx/2,-dy/2,dz)
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(solid(A,B,vc,vw,vo),solid(B,C,vc,vw,vo),solid(S,A,vc,vw,vo),solid(S,B,vc,vw,vo),solid(S,C,vc,vw,vo))
        hidden=VGroup(hidden_edge(C,D,DIM,2.6,0.68),hidden_edge(D,A,DIM,2.6,0.68),hidden_edge(S,D,DIM,2.6,0.68))
        base=face(A,B,C,D,color=BLUE,opacity=0.08,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def cube(self, dim=False):
        a=3.0
        A=L(-1.8,-1.8,0); B=L(1.8,-1.8,0); C=L(1.8,1.8,0); D=L(-1.8,1.8,0)
        z=GEO_SCALE*a
        A1=A+np.array([0,0,z]); B1=B+np.array([0,0,z]); C1=C+np.array([0,0,z]); D1=D+np.array([0,0,z])
        vc=DIM if dim else EDGE; vo=0.42 if dim else 0.94; vw=2.4 if dim else 3.7
        visible=VGroup(
            solid(A,B,vc,vw,vo),solid(B,C,vc,vw,vo),solid(A,A1,vc,vw,vo),solid(B,B1,vc,vw,vo),
            solid(C,C1,vc,vw,vo),solid(A1,B1,vc,vw,vo),solid(B1,C1,vc,vw,vo),solid(C1,D1,vc,vw,vo)
        )
        hidden=VGroup(hidden_edge(C,D,DIM,2.6,0.68),hidden_edge(D,A,DIM,2.6,0.68),hidden_edge(D,D1,DIM,2.6,0.68),hidden_edge(D1,A1,DIM,2.6,0.68))
        base=face(A,B,C,D,color=BLUE,opacity=0.06,stroke_width=0)
        dots=VGroup(*[Dot3D(p,radius=0.048,color=GOLD) for p in [A,B,C,D,A1,B1,C1,D1]])
        return {"A":A,"B":B,"C":C,"D":D,"A1":A1,"B1":B1,"C1":C1,"D1":D1,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        title=txt("HHKG CHUYÊN SÂU 06",46,GOLD,BOLD)
        sub=txt("GÓC NHỊ DIỆN NÂNG CAO & BÀI NGƯỢC",34,INK,BOLD)
        line=txt("Cạnh chung khó thấy · lăng trụ xiên · chóp tam giác · tham số · cực trị",24,CYAN,BOLD)
        note=txt("Một góc không gian tốt luôn bắt đầu từ một mặt cắt đúng",23,MUTED)
        brand=txt(TEN_THAY,20,MUTED)
        g=VGroup(title,sub,line,note,brand).arrange(DOWN,buff=0.28)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g,shift=UP*0.10),run_time=0.9)
        self.narrate(
            "Ở video trước, chúng ta đã xây nền tảng của góc nhị diện bằng mặt cắt vuông góc cạnh chung. Video này đi sâu hơn. Cạnh chung có thể là một đường chéo khó nhìn, khối có thể là lăng trụ xiên hoặc chóp tam giác, đề có thể cho trước góc để bắt ta tìm chiều cao hay cạnh đáy, thậm chí điểm động làm góc thay đổi. Dù hình có phức tạp đến đâu, chiến lược vẫn nhất quán: tìm cạnh chung, dựng trong mỗi mặt một đường cùng vuông góc với cạnh đó, rồi đưa bài toán trở về một tam giác phẳng đủ dữ kiện.",2.0)

    # ======================================================
    # METHOD MAP
    # ======================================================
    def method_map(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ phương pháp", "Bốn câu hỏi trước khi tính", "1/9")
        blocks=VGroup(
            VGroup(txt("1",24,GOLD,BOLD),txt("Cạnh chung là đường nào?",24,INK,BOLD)).arrange(RIGHT,buff=0.18),
            VGroup(txt("2",24,GOLD,BOLD),txt("Trong mặt thứ nhất, đường nào vuông góc cạnh chung?",23,INK)).arrange(RIGHT,buff=0.18),
            VGroup(txt("3",24,GOLD,BOLD),txt("Trong mặt thứ hai, đường nào vuông góc cạnh chung?",23,INK)).arrange(RIGHT,buff=0.18),
            VGroup(txt("4",24,GOLD,BOLD),txt("Tam giác phẳng nào chứa góc cần tìm?",23,CYAN,BOLD)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.43).move_to(LEFT*2.2+UP*0.2)
        formula=VGroup(
            mty("(P) inter (Q) = d",31,GOLD),
            mty("a perp d",29,CYAN),
            mty("b perp d",29,GREEN),
            mty("phi = hat(a b, size: #145%)",31,GOLD),
        ).arrange(DOWN,buff=0.30).move_to(RIGHT*3.7+UP*0.2)
        self.add_fixed_in_frame_mobjects(blocks,formula)
        self.play(FadeIn(blocks),FadeIn(formula),run_time=0.9)
        self.narrate(
            "Trước khi vào các cấu hình khó, thầy chốt lại bốn câu hỏi. Một, hai mặt phẳng cắt nhau theo đường nào. Hai, trong mặt thứ nhất có đường nào vuông góc cạnh chung. Ba, trong mặt thứ hai có đường nào cũng vuông góc cạnh chung tại cùng một điểm. Bốn, hai đường ấy tạo ra tam giác phẳng nào. Chỉ sau bốn bước này ta mới dùng lượng giác. Làm ngược thứ tự, tức nhìn hình rồi đoán góc, là nguyên nhân lớn nhất khiến bài nhị diện trở nên rối. Một mẹo kiểm tra rất hữu ích là: nếu hai tia mà em chọn không cùng xuất phát từ một điểm trên cạnh chung, thì gần như chắc chắn em chưa dựng đúng góc nhị diện.",2.0)

    # ======================================================
    # 1. OBLIQUE PRISM
    # ======================================================
    def oblique_prism_example(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 1 · Lăng trụ xiên", "Góc giữa mặt bên ABB'A' và mặt đáy ABC", "2/9")
        G=self.oblique_prism(); self.add(G["base"],G["side"],G["top"],G["edges"],G["dots"])
        for name in ["A","B","C","A1","B1","C1"]:
            self.add_label(name.replace("1","'"),G[name],RED if name=="A1" else GOLD)
        ab=solid(G["A"],G["B"],GOLD,6.1,1.0)
        ac=solid(G["A"],G["C"],CYAN,5.0,1.0)
        aa1=solid(G["A"],G["A1"],GREEN,5.0,1.0)
        mark1=right_angle_3d(G["A"],G["B"]-G["A"],G["C"]-G["A"],size=0.26,color=CYAN)
        mark2=right_angle_3d(G["A"],G["B"]-G["A"],G["A1"]-G["A"],size=0.30,color=GREEN)
        u=(G["C"]-G["A"])/np.linalg.norm(G["C"]-G["A"]); v=(G["A1"]-G["A"])/np.linalg.norm(G["A1"]-G["A"])
        ang=math.acos(float(np.clip(np.dot(u,v),-1,1))); arc=arc_basis(G["A"],u,v,ang,radius=0.44)
        self.play(Create(ab),Create(ac),Create(aa1),FadeIn(mark1),FadeIn(mark2),Create(arc),run_time=1.0)
        self.card("LỜI GIẢI","Cạnh bên xiên nhưng mặt cắt vẫn rất sạch",[
            ("math","(A B B' A') inter (A B C) = A B",27,GOLD),
            ("math","A C perp A B",28,CYAN),
            ("math","A A' perp A B",28,GREEN),
            ("math","phi = hat(C A A', size: #145%)",30,GOLD),
            ("math","tan phi = frac(2, 1) = 2",31,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Ta bắt đầu bằng một lăng trụ xiên. Mặt bên ABB phẩy A phẩy và mặt đáy ABC có cạnh chung AB. Vì đáy ABC vuông tại A nên AC vuông góc AB. Cạnh bên AA phẩy của lăng trụ này không vuông góc mặt đáy, nhưng nó được chọn sao cho cũng vuông góc AB. Do đó mặt cắt vuông góc cạnh chung xuất hiện ngay tại A, và góc nhị diện chính là góc CAA phẩy.",1.9)
        self.narrate(
            "Trong mặt cắt ấy, thành phần ngang của AA phẩy theo hướng AC bằng một đơn vị, còn thành phần đứng bằng hai đơn vị. Vì vậy tang phi bằng hai trên một, tức bằng hai. Điểm đáng học không phải con số hai, mà là việc một lăng trụ xiên vẫn xử lý hoàn toàn giống chóp: cạnh chung trước, mặt cắt sau, rồi mới lượng giác. Nếu cạnh bên xiên theo một hướng khác, ta cũng không được lấy góc giữa cạnh bên và đáy thay cho góc nhị diện; chỉ hai đường cùng vuông góc cạnh chung mới đại diện đúng cho hai mặt.",1.8)
        self.takeaway("Lăng trụ xiên không đổi định nghĩa: cạnh chung vẫn là chìa khóa")

    # ======================================================
    # 2. TRIANGULAR PYRAMID GENERAL FORMULA
    # ======================================================
    def triangular_pyramid_formula(self):
        self.clear_all(); self.set_camera_orientation(phi=69*DEGREES,theta=-52*DEGREES,zoom=0.98)
        self.add_header("Bài 2 · Chóp đáy tam giác", "AB = AC = a, góc BAC vuông, SA = h", "3/9")
        G=self.right_tri_pyramid(); self.add(G["base"],G["side"],G["edges"],G["dots"])
        for name in ["A","B","C","S","M"]: self.add_label(name,G[name],RED if name=="S" else GOLD)
        bc=hidden_edge(G["B"],G["C"],GOLD,3.2,0.92)
        am=aux(G["A"],G["M"],CYAN,4.1,0.95)
        sm=solid(G["S"],G["M"],GREEN,5.0,1.0)
        mark1=right_angle_3d(G["M"],G["B"]-G["M"],G["A"]-G["M"],size=0.25,color=CYAN)
        mark2=right_angle_3d(G["M"],G["B"]-G["M"],G["S"]-G["M"],size=0.28,color=GREEN)
        u=(G["A"]-G["M"])/np.linalg.norm(G["A"]-G["M"]); v=(G["S"]-G["M"])/np.linalg.norm(G["S"]-G["M"])
        ang=math.acos(float(np.clip(np.dot(u,v),-1,1))); arc=arc_basis(G["M"],u,v,ang,radius=0.42)
        self.play(Create(bc),Create(am),Create(sm),FadeIn(mark1),FadeIn(mark2),Create(arc),run_time=1.0)
        self.card("CÔNG THỨC","Một mẫu tổng quát rất đáng nhớ",[
            ("math","B M = M C = frac(B C, 2)",26,MUTED),
            ("math","A M = frac(a, sqrt(2))",29,CYAN),
            ("math","B C perp (S A M)",28,GREEN),
            ("math","phi = hat(A M S, size: #145%)",30,GOLD),
            ("math","tan phi = frac(h, frac(a, sqrt(2)))",28,INK),
            ("math","tan phi = frac(sqrt(2) h, a)",32,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Xét chóp S.ABC có SA vuông góc đáy, tam giác ABC vuông cân tại A với AB bằng AC bằng a. Ta cần góc nhị diện giữa mặt SBC và đáy ABC theo cạnh BC. Vì tam giác ABC vuông cân, trung điểm M của cạnh huyền BC cho AM vuông góc BC và AM bằng a trên căn hai. Đồng thời SA cũng vuông góc BC. Vì vậy BC vuông góc mặt phẳng SAM, kéo theo SM vuông góc BC.",2.0)
        self.narrate(
            "Góc nhị diện cần tìm là góc AMS. Tam giác SAM vuông tại A, nên tang phi bằng SA trên AM. Thay SA bằng h và AM bằng a trên căn hai, ta được tang phi bằng căn hai h trên a. Đây là công thức tổng quát cho cả một họ chóp tam giác vuông cân. Khi đề thay số, ta chỉ việc thế vào thay vì dựng lại từ đầu.",1.9)
        self.takeaway("Chóp tam giác vuông cân: trung điểm cạnh huyền tạo mặt cắt chuẩn")

    # ======================================================
    # 3. INVERSE PROBLEM
    # ======================================================
    def inverse_problem(self):
        self.clear_all(); self.set_camera_orientation(phi=69*DEGREES,theta=-52*DEGREES,zoom=0.98)
        self.add_header("Bài 3 · Bài ngược", "Biết góc nhị diện, tìm chiều cao", "4/9")
        G=self.right_tri_pyramid(a=6.0,h=3*math.sqrt(6)); self.add(G["base"],G["side"],G["edges"],G["dots"])
        for name in ["A","B","C","S","M"]: self.add_label(name,G[name],RED if name=="S" else GOLD)
        am=aux(G["A"],G["M"],CYAN,4.1,0.95); sm=solid(G["S"],G["M"],GREEN,5.0,1.0); sa=solid(G["S"],G["A"],ORANGE,5.0,1.0)
        self.play(Create(am),Create(sm),Create(sa),run_time=0.8)
        self.card("ĐỀ BÀI","AB = AC = 6, góc nhị diện bằng 60°",[
            ("math","A M = frac(6, sqrt(2)) = 3 sqrt(2)",28,CYAN),
            ("math","tan 60 degree = frac(S A, A M)",29,INK),
            ("math","sqrt(3) = frac(h, 3 sqrt(2))",29,INK),
            ("math","h = 3 sqrt(6)",34,GOLD),
        ],accent=ORANGE)
        self.narrate(
            "Bây giờ đảo chiều bài toán. Đáy vẫn là tam giác vuông cân tại A nhưng cạnh góc vuông bằng sáu. Góc nhị diện theo BC được cho bằng sáu mươi độ, còn chiều cao SA chưa biết. Mặt cắt vẫn là tam giác SAM, nên AM bằng ba căn hai. Chúng ta không phải dựng thêm bất cứ đường nào mới.",1.7)
        self.narrate(
            "Từ tang sáu mươi độ bằng SA trên AM, ta có căn ba bằng h chia ba căn hai. Suy ra h bằng ba căn sáu. Bài ngược kiểu này xuất hiện rất nhiều: đề cho góc để hỏi chiều cao, cạnh đáy hoặc một khoảng cách. Kỹ năng quan trọng là giữ được cùng một mặt cắt chuẩn và giải ngược quan hệ lượng giác đã có. Khi đề thay tang bằng sin hay cos, ta cũng nên chọn đúng tỷ số phù hợp với những cạnh đã biết, thay vì cố đưa tất cả về tang một cách máy móc.",1.9)
        self.takeaway("Bài ngược: đừng dựng lại — giải ngược ngay trên mặt cắt đã chuẩn hóa")

    # ======================================================
    # 4. COMPARE TWO DIHEDRAL ANGLES
    # ======================================================
    def compare_angles(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 4 · So sánh hai góc nhị diện", "Chóp vuông đáy chữ nhật", "5/9")
        G=self.rectangular_pyramid(); self.add(G["base"],G["edges"],G["dots"])
        for name in ["A","B","C","D","S"]: self.add_label(name,G[name],RED if name=="S" else GOLD)
        ba=solid(G["B"],G["A"],CYAN,4.7,1.0); bs=solid(G["B"],G["S"],GREEN,4.7,1.0)
        da=hidden_edge(G["D"],G["A"],CYAN,3.2,0.92); ds=hidden_edge(G["D"],G["S"],GREEN,3.2,0.92)
        self.play(Create(ba),Create(bs),Create(da),Create(ds),run_time=1.0)
        self.card("SO SÁNH","Không cần tính số đo hai góc",[
            ("math","tan beta_1 = frac(h, a)",29,GOLD),
            ("math","tan beta_2 = frac(h, b)",29,GOLD),
            ("math","a < b",28,CYAN),
            ("math","frac(h, a) > frac(h, b)",29,GREEN),
            ("math","beta_1 > beta_2",32,GOLD),
        ],accent=CYAN)
        self.narrate(
            "Xét chóp S.ABCD có SA vuông góc đáy chữ nhật, AB bằng a, AD bằng b. Góc nhị diện của mặt SBC với đáy theo cạnh BC được đọc trong tam giác SAB, nên tang của nó bằng h trên a. Tương tự, góc nhị diện của mặt SCD với đáy theo cạnh CD được đọc trong tam giác SAD, nên tang bằng h trên b.",1.9)
        self.narrate(
            "Nếu a nhỏ hơn b, thì h trên a lớn hơn h trên b. Vì cả hai góc đều nhọn, tang lớn hơn kéo theo góc lớn hơn. Vậy mặt bên dựa trên cạnh ngắn hơn của đáy sẽ dốc hơn. Bài so sánh góc thường không cần tính số đo góc; chỉ cần đưa về hai tỷ số lượng giác cùng loại rồi so sánh. Đây cũng là cách xử lý tốt các câu đúng sai: thay vì bấm hai góc gần nhau trên máy tính, hãy so sánh trực tiếp những đại lượng quyết định chúng.",1.9)
        self.takeaway("So sánh nhị diện: đưa về cùng hàm lượng giác, tránh bấm máy góc")

    # ======================================================
    # 5. CUBE WITH HARD-TO-SEE COMMON EDGE
    # ======================================================
    def cube_hidden_edge(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 5 · Cạnh chung khó thấy", "Mặt A'BC và mặt đáy trong hình lập phương", "6/9")
        G=self.cube(); self.add(G["base"],G["edges"],G["dots"])
        for name in ["A","B","C","D","A1","B1","C1","D1"]: self.add_label(name.replace("1","'"),G[name])
        plane=face(G["A1"],G["B"],G["C"],color=PURPLE,opacity=0.19,stroke_width=0)
        bc=solid(G["B"],G["C"],GOLD,6.0,1.0); ba=solid(G["B"],G["A"],CYAN,4.9,1.0); ba1=solid(G["B"],G["A1"],GREEN,4.9,1.0)
        self.play(FadeIn(plane),Create(bc),Create(ba),Create(ba1),run_time=1.0)
        self.card("LỜI GIẢI","Cạnh chung BC bị che bởi nhiều đường",[
            ("math","(A' B C) inter (A B C D) = B C",27,GOLD),
            ("math","B A perp B C",28,CYAN),
            ("math","B A' perp B C",28,GREEN),
            ("math","beta = hat(A B A', size: #145%)",30,GOLD),
            ("math","tan beta = frac(A A', A B) = 1",29,INK),
            ("math","beta = 45 degree",32,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Trong hình lập phương, xét mặt phẳng A phẩy B C và mặt đáy. Vì hình có rất nhiều cạnh và đường chéo, cạnh chung BC dễ bị bỏ qua. Nhưng khi đã xác định được giao tuyến BC, ta chỉ cần chọn BA trong đáy và BA phẩy trong mặt A phẩy B C. Cả hai cùng vuông góc BC tại B.",1.8)
        self.narrate(
            "Góc nhị diện là góc ABA phẩy. Tam giác ABA phẩy vuông cân vì AB bằng AA phẩy, nên tang beta bằng một và beta bằng bốn mươi lăm độ. Bài này nhắc chúng ta rằng một cấu hình trông dày đặc không có nghĩa lời giải phải dài; cạnh chung đúng có thể làm toàn bộ hình thu gọn về một tam giác vuông rất quen thuộc. Trong câu đúng sai, nếu ai đó chọn góc giữa A phẩy B và một đường chéo bất kỳ của đáy, em phải kiểm tra ngay đường đó có thật sự vuông góc BC hay không.",1.8)
        self.takeaway("Hình dày đặc: xác định giao tuyến trước, mọi thứ còn lại sẽ nhẹ đi")

    # ======================================================
    # 6. MOVING POINT + EXTREMA ON SEGMENT
    # ======================================================
    def moving_point(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.98)
        self.add_header("Bài 6 · Điểm động", "M chạy trên CC' — góc nhị diện của (ABM) với đáy", "7/9")
        G=self.cube(); self.add(G["base"],G["edges"],G["dots"])
        for name in ["A","B","C","D","A1","B1","C1","D1"]: self.add_label(name.replace("1","'"),G[name])
        u=ValueTracker(0.08)
        C=G["C"]; C1=G["C1"]; B=G["B"]
        def Mpt(): return C + u.get_value()*(C1-C)
        Mdot=always_redraw(lambda: Dot3D(Mpt(),radius=0.06,color=RED))
        bm=always_redraw(lambda: solid(B,Mpt(),GREEN,5.0,1.0))
        cm=always_redraw(lambda: solid(C,Mpt(),ORANGE,4.0,0.95))
        bc=solid(B,C,CYAN,5.0,1.0)
        mlab=always_redraw(lambda: mty("M",22,RED).move_to(Mpt()+np.array([0.11,0.04,0.10])))
        self.add(Mdot,bm,cm,bc); self.add_fixed_orientation_mobjects(mlab)
        readout=always_redraw(lambda: VGroup(
            txt(f"u = {u.get_value():.2f}",17,ORANGE,BOLD),
            txt(f"tan θ = {u.get_value():.2f}",17,GOLD,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.07).move_to(RIGHT*4.25+DOWN*1.95))
        self.add_fixed_in_frame_mobjects(readout)
        self.card("ĐIỂM ĐỘNG","Đặt CM = u·a, 0 ≤ u ≤ 1",[
            ("math","B C perp A B",27,CYAN),
            ("math","B M perp A B",27,GREEN),
            ("math","theta = hat(C B M, size: #145%)",29,GOLD),
            ("math","tan theta = frac(C M, B C) = u",30,GOLD),
            ("math","0 <= theta <= 45 degree",29,INK),
            ("math","theta_2 = 45 degree",31,GOLD),
        ],accent=RED)
        self.narrate_play(
            "Cho M chạy trên cạnh đứng CC phẩy của hình lập phương. Hai mặt đang xét là ABM và mặt đáy, cạnh chung là AB. Trong đáy, BC vuông góc AB. Trong mặt ABM, BM cũng vuông góc AB vì BM chỉ có thành phần theo BC và theo phương thẳng đứng. Vậy góc nhị diện chính là góc CBM. Đặt CM bằng u lần cạnh khối lập phương, ta có tang theta bằng u.",
            u.animate.set_value(1.0),min_time=5.0)
        self.narrate_play(
            "Vì u chạy từ không đến một, tang theta tăng từ không đến một, nên góc theta tăng liên tục từ không đến bốn mươi lăm độ. Do đó góc lớn nhất đạt tại M bằng C phẩy và bằng bốn mươi lăm độ; góc nhỏ nhất đạt tại M bằng C và bằng không. Nếu đề hỏi khi theta bằng ba mươi độ, ta chỉ giải u bằng tang ba mươi độ, tức một trên căn ba.",
            u.animate.set_value(1/math.sqrt(3)),min_time=4.5)
        self.takeaway("Điểm động: trước khi đạo hàm, thử biểu diễn tan/cos theo tham số thật đơn giản")

    # ======================================================
    # 7. PRACTICAL INVERSE DESIGN
    # ======================================================
    def practical_design(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-52*DEGREES,zoom=0.98)
        self.add_header("Bài 7 · Thiết kế thực tế", "Mái dốc biết góc, tìm chiều cao đỉnh", "8/9")
        A=L(-2.7,-1.7,0); B=L(2.7,-1.7,0); C=L(2.7,2.2,0); D=L(-2.7,2.2,0)
        M=(A+B)/2; N=(C+D)/2; S=N+np.array([0,0,GEO_SCALE*2.3])
        ground=face(A,B,C,D,color=BLUE,opacity=0.10,stroke_width=0)
        roof=face(A,B,S,color=PURPLE,opacity=0.20,stroke_width=0)
        edge=solid(A,B,GOLD,6.0,1.0); mn=aux(M,N,CYAN,4.0,0.95); ms=solid(M,S,GREEN,5.0,1.0); ns=solid(N,S,ORANGE,4.2,0.95)
        self.add(ground,roof,edge,mn,ms,ns)
        for name,pt in [("M",M),("N",N),("S",S)]: self.add_label(name,pt,RED if name=="S" else GOLD)
        self.card("MÔ HÌNH","Nửa bề rộng mái là 4 m, góc dốc 35°",[
            ("math","M N = 4",29,CYAN),
            ("math","alpha = 35 degree",29,GOLD),
            ("math","tan alpha = frac(N S, M N)",29,INK),
            ("math","N S = 4 tan 35 degree",29,INK),
            ("math","N S approx 2.80",33,GOLD),
        ],accent=ORANGE)
        self.narrate(
            "Một mô hình thực tế rất điển hình là mái dốc. Mép mái AB đóng vai trò cạnh chung giữa mái và mặt phẳng ngang. Mặt cắt vuông góc cạnh chung đi qua trung điểm M của mép và đỉnh S của mái. Nếu nửa bề rộng công trình là bốn mét và góc dốc yêu cầu ba mươi lăm độ, chiều cao mái được tìm trực tiếp bằng tang của góc nhị diện.",1.9)
        self.narrate(
            "Ta có tang alpha bằng chiều cao NS chia bốn. Suy ra NS bằng bốn nhân tang ba mươi lăm độ, xấp xỉ hai phẩy tám mét. Đây chính là bài ngược trong bối cảnh kỹ thuật: yêu cầu góc nhị diện trước, rồi suy ra kích thước cần thiết của cấu kiện. Khi gặp mô hình thực tế, điều khó nhất vẫn là nhận ra mặt cắt vuông góc cạnh chung. Sau khi đã có tam giác thiết kế, việc thay đổi bề rộng mái hoặc thay đổi tiêu chuẩn góc dốc chỉ còn là thay tham số trong cùng một công thức, rất thuận lợi cho việc so sánh nhiều phương án.",1.8)
        self.takeaway("Mô hình thực tế: góc nhị diện thường chuyển thành tam giác thiết kế 2D")

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Tổng kết Video 06", "Từ cạnh chung khó thấy đến bài ngược và điểm động", "9/9")
        left=VGroup(
            txt("7 mẫu nhận dạng",26,GOLD,BOLD),
            txt("• Lăng trụ xiên: vẫn dựng hai đường ⟂ cạnh chung",20,INK),
            txt("• Chóp tam giác: tìm trung điểm / đường cao đáy",20,INK),
            txt("• Bài ngược: giải ngược trên cùng mặt cắt",20,INK),
            txt("• So sánh: đưa về cùng tan hoặc cos",20,INK),
            txt("• Cạnh chung khó thấy: tìm giao tuyến trước",20,INK),
            txt("• Điểm động: biểu diễn góc theo tham số",20,INK),
            txt("• Thực tế: mặt cắt 3D → tam giác thiết kế 2D",20,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).move_to(LEFT*2.35+UP*0.05)
        right=VGroup(
            mty("tan phi = frac(sqrt(2) h, a)",29,CYAN),
            mty("h = frac(a tan phi, sqrt(2))",29,GREEN),
            mty("tan beta_1 = frac(h, a)",28,INK),
            mty("tan beta_2 = frac(h, b)",28,INK),
            mty("tan theta = u",31,GOLD),
            mty("theta_2 = 45 degree",30,GOLD),
        ).arrange(DOWN,buff=0.28).move_to(RIGHT*3.6+UP*0.1)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left),FadeIn(right),run_time=0.9)
        self.narrate(
            "Video này mở rộng góc nhị diện theo ba hướng. Thứ nhất, hình phức tạp hơn nhưng định nghĩa không đổi: cạnh chung, hai đường vuông góc, một góc phẳng. Thứ hai, bài toán có thể đi ngược: biết góc để tìm chiều cao hay cạnh. Thứ ba, góc có thể phụ thuộc tham số hoặc điểm động; khi đó ta nên biểu diễn một hàm lượng giác đơn giản như tang theo tham số trước khi nghĩ tới đạo hàm. Từ video sau, series chuyển sang chặng C: thể tích và tỷ số thể tích, nơi các kỹ thuật đổi đỉnh, cùng đáy, cùng chiều cao và đồng dạng sẽ được hệ thống hóa sâu hơn.",2.1)

    def construct(self):
        self.intro()
        self.method_map()
        self.oblique_prism_example()
        self.triangular_pyramid_formula()
        self.inverse_problem()
        self.compare_angles()
        self.cube_hidden_edge()
        self.moving_point()
        self.practical_design()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir=str(MEDIA_DIR)
    config.output_file="hhkg_chuyen_sau_06_goc_nhi_dien_nang_cao_typst_SAFE_1080p"
    config.format="mp4"
    config.write_to_movie=True
    config.disable_caching=False
    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 06")
    scene=SangLesson(); scene.render()
    video_path=Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")
    duration=probe_duration(video_path)
    master_wav=ROOT/"master_narration_hhkg_06.wav"
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

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
# HHKG CHUYEN SAU 11 - THIET DIEN II: DIEN TICH VA TY SO
# Manim Community + MathTypst SAFE | Standalone 100%
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
# PALETTE
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
# TYPOGRAPHY + TYPST SAFETY
# ==========================================================
def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


_FORBIDDEN_TYPST_WORDS = {"sect", "intersect", "angle"}


def validate_typst_expr(s):
    words = set(s.replace("(", " ").replace(")", " ").replace(",", " ").split())
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(
            f"Forbidden Typst math token(s) {bad} in {s!r}. "
            "Use inter for intersection and hat(...) for plane angles."
        )
    if "/" in s:
        raise ValueError(
            f"Slash fraction forbidden in HHKG MathTypst: {s!r}. Use frac(..., ...)."
        )
    return s


def mty(s, size=38, color=INK):
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
        {"text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC, "pitch": PITCH, "engine": "edge-tts"},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        text=True,
    ).strip()
    return float(out)


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
    fc = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[m]", "-ar", "48000", "-ac", "2", "-t", f"{video_duration:.3f}", str(out_wav)],
        check=True,
    )


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)],
        check=True,
    )

# ==========================================================
# 3D VISUAL GRAMMAR
# ==========================================================
GEO_SCALE = 0.80
GEO_SHIFT = np.array([-1.78, -0.04, -0.08])
VIEW_PHI = 68 * DEGREES
VIEW_THETA = -54 * DEGREES
VIEW_ZOOM = 0.97


def L(x, y, z):
    return GEO_SCALE * np.array([float(x), float(y), float(z)]) + GEO_SHIFT


def solid(a, b, color=EDGE, width=4.0, opacity=0.94):
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def hidden_edge(a, b, color=DIM, width=2.7, opacity=0.70, dash=0.11):
    return DashedLine(a, b, color=color, stroke_width=width, stroke_opacity=opacity, dash_length=dash, dashed_ratio=0.56)


def aux(a, b, color=CYAN, width=3.7, opacity=0.92, dash=0.11):
    return DashedLine(a, b, color=color, stroke_width=width, stroke_opacity=opacity, dash_length=dash, dashed_ratio=0.56)


def face(*points, color=BLUE, opacity=0.10, stroke=BLUE, stroke_width=0.0):
    return Polygon(*points, fill_color=color, fill_opacity=opacity, stroke_color=stroke,
                   stroke_width=stroke_width, stroke_opacity=0.0 if stroke_width == 0 else 0.55)


def right_angle_3d(vertex, u, v, size=0.28, color=GOLD, width=4.2):
    u = np.array(u, dtype=float); v = np.array(v, dtype=float)
    u /= np.linalg.norm(u); v /= np.linalg.norm(v)
    p1 = vertex + size * u
    p2 = vertex + size * (u + v)
    p3 = vertex + size * v
    return VGroup(solid(p1, p2, color, width), solid(p2, p3, color, width))


def angle_arc_3d(vertex, ray1, ray2, radius=0.42, color=GOLD, width=5.5):
    """Geometrically correct 3D angle marker.

    The old arc helper assumed an orthonormal basis and could draw a wrong angle
    on screen. This version constructs the minor arc from the two actual rays,
    in the plane spanned by those rays. The endpoints of the arc are exactly on
    the two rays before camera projection.
    """
    u = np.array(ray1, dtype=float)
    v = np.array(ray2, dtype=float)
    u /= np.linalg.norm(u)
    v /= np.linalg.norm(v)
    dot = float(np.clip(np.dot(u, v), -1.0, 1.0))
    theta = math.acos(dot)
    w = v - dot * u
    nw = np.linalg.norm(w)
    if nw < 1e-9:
        raise ValueError("Angle rays are collinear; cannot draw a unique angle arc.")
    w /= nw
    return ParametricFunction(
        lambda t: vertex + radius * (math.cos(t) * u + math.sin(t) * w),
        t_range=[0, theta], color=color, stroke_width=width,
    )


def plane_normal(a, b, c):
    n = np.cross(b - a, c - a)
    norm = np.linalg.norm(n)
    if norm < 1e-9:
        raise ValueError("Three points do not determine a plane.")
    return n / norm


def line_plane_intersection(p, q, a, b, c):
    n = plane_normal(a, b, c)
    d = q - p
    den = float(np.dot(n, d))
    if abs(den) < 1e-9:
        return None
    t = float(np.dot(n, a - p) / den)
    return p + t * d, t


def segment_plane_intersection(p, q, plane_point, normal, tol=1e-8):
    dp = float(np.dot(normal, p - plane_point))
    dq = float(np.dot(normal, q - plane_point))
    if abs(dp) < tol and abs(dq) < tol:
        return None
    den = dp - dq
    if abs(den) < tol:
        return None
    t = dp / den
    if -tol <= t <= 1 + tol:
        return p + t * (q - p), float(t)
    return None


def unique_points(points, tol=1e-6):
    out = []
    for p in points:
        if not any(np.linalg.norm(p - q) < tol for q in out):
            out.append(p)
    return out


def order_points_in_plane(points, normal):
    pts = unique_points(points)
    ctr = np.mean(pts, axis=0)
    e1 = pts[0] - ctr
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(normal, e1)
    e2 /= np.linalg.norm(e2)
    vals = []
    for p in pts:
        d = p - ctr
        vals.append((math.atan2(np.dot(d, e2), np.dot(d, e1)), p))
    vals.sort(key=lambda x: x[0])
    return [p for _, p in vals]


def section_from_edges(edge_map, p1, p2, p3):
    n = plane_normal(p1, p2, p3)
    hits = []
    hit_by_edge = {}
    for name, (a, b) in edge_map.items():
        h = segment_plane_intersection(a, b, p1, n)
        if h is not None:
            point, t = h
            if -1e-7 <= t <= 1 + 1e-7:
                hits.append(point)
                hit_by_edge[name] = point
    ordered = order_points_in_plane(hits, n)
    return ordered, hit_by_edge, n


def plane_patch(center, normal, width=4.8, height=4.0, color=PURPLE, opacity=0.10):
    n = np.array(normal, dtype=float); n /= np.linalg.norm(n)
    seed = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(seed, n)) > 0.90:
        seed = np.array([1.0, 0.0, 0.0])
    u = np.cross(n, seed); u /= np.linalg.norm(u)
    v = np.cross(n, u); v /= np.linalg.norm(v)
    p1 = center - width/2*u - height/2*v
    p2 = center + width/2*u - height/2*v
    p3 = center + width/2*u + height/2*v
    p4 = center - width/2*u + height/2*v
    return face(p1, p2, p3, p4, color=color, opacity=opacity)

# ==========================================================
# SCENE
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)

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

    # ---------- fixed UI ----------
    def clear_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.30)
        self.clear()

    def add_header(self, title, subtitle, progress):
        series = txt("HHKG CHUYÊN SÂU · 11", 15, BLUE, BOLD)
        series.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.30)
        title_m = fit_width(txt(title, 29, INK, BOLD), 8.9)
        title_m.next_to(series, DOWN, buff=0.045, aligned_edge=LEFT)
        sub_m = fit_width(txt(subtitle, 17, MUTED), 8.9)
        sub_m.next_to(title_m, DOWN, buff=0.045, aligned_edge=LEFT)
        accent = Line(series.get_left()+DOWN*0.13, series.get_left()+RIGHT*0.62+DOWN*0.13,
                      color=GOLD, stroke_width=3.2)
        prog = txt(progress, 15, MUTED, BOLD)
        prog.to_edge(UP, buff=0.20).to_edge(RIGHT, buff=0.32)
        rule = Line(LEFT*6.82, RIGHT*6.82, color=GRID, stroke_width=0.9, stroke_opacity=0.42).shift(UP*2.78)
        divider = Line(np.array([1.50,-2.83,0]), np.array([1.50,2.64,0]), color=GRID, stroke_width=1.0, stroke_opacity=0.42)
        teacher = txt(TEN_THAY, 15, MUTED)
        teacher.to_edge(DOWN, buff=0.10).to_edge(LEFT, buff=0.30)
        hud = VGroup(series, title_m, sub_m, accent, prog, rule, divider, teacher)
        self.add_fixed_in_frame_mobjects(hud)
        return hud

    def card(self, kicker, title, items, accent=GOLD, height=5.25, auto_add=True):
        bg = Rectangle(width=5.12, height=height, fill_color=PANEL, fill_opacity=0.90,
                       stroke_color=GRID, stroke_width=0.9, stroke_opacity=0.36).move_to(RIGHT*4.28+DOWN*0.03)
        spine = Line(bg.get_corner(UL)+RIGHT*0.12+DOWN*0.18,
                     bg.get_corner(DL)+RIGHT*0.12+UP*0.18,
                     color=accent, stroke_width=3.8, stroke_opacity=0.95)
        k = txt(kicker.upper(), 14, accent, BOLD)
        k.move_to(bg.get_corner(UL)+RIGHT*0.36+DOWN*0.30, aligned_edge=LEFT)
        t = fit_width(txt(title, 23, INK, BOLD), 4.30)
        t.next_to(k, DOWN, buff=0.10, aligned_edge=LEFT)
        body = VGroup()
        for item in items:
            kind = item[0]
            if kind == "text":
                _, s, size, color, weight = item; mob = txt(s, size, color, weight)
            elif kind == "math":
                _, expr, size, color = item; mob = mty(expr, size, color)
            elif kind == "sep":
                mob = Line(LEFT*2.00, RIGHT*2.00, color=GRID, stroke_width=0.9, stroke_opacity=0.55)
            elif kind == "obj":
                mob = item[1]
            else:
                raise ValueError(kind)
            body.add(fit_width(mob, 4.28))
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        body.next_to(t, DOWN, buff=0.22, aligned_edge=LEFT)
        fit_height(body, height-1.45)
        group = VGroup(bg, spine, k, t, body)
        if auto_add:
            self.add_fixed_in_frame_mobjects(group)
        return group

    def takeaway(self, s):
        label = fit_width(txt(s, 16, CYAN, BOLD), 7.15)
        label.move_to(LEFT*2.55 + DOWN*2.52)
        self.add_fixed_in_frame_mobjects(label)
        return label

    def add_label(self, name, pt, color=GOLD, off=(0.10,-0.10,0.05), size=22):
        lab = mty(name, size, color).move_to(pt + np.array(off, dtype=float))
        self.add_fixed_orientation_mobjects(lab)
        return lab

    def label_many(self, data):
        return VGroup(*[self.add_label(*item) for item in data])

    # ---------- models ----------
    def tetrahedron(self):
        S=L(-0.3,-0.2,3.5); A=L(-2.3,-1.8,0); B=L(2.2,-1.8,0); C=L(0.9,2.0,0)
        visible=VGroup(solid(S,A),solid(S,B),solid(S,C),solid(A,B),solid(A,C))
        hidden=VGroup(hidden_edge(B,C))
        base=face(A,B,C,color=BLUE,opacity=0.07)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C]],Dot3D(S,radius=0.06,color=RED))
        edges={"SA":(S,A),"SB":(S,B),"SC":(S,C),"AB":(A,B),"AC":(A,C),"BC":(B,C)}
        return {"S":S,"A":A,"B":B,"C":C,"edges":VGroup(visible,hidden),"base":base,"dots":dots,"edge_map":edges}

    def square_pyramid(self):
        # centered apex: good for generic section construction
        A=L(-2.1,-1.8,0); B=L(2.1,-1.8,0); C=L(2.1,1.9,0); D=L(-2.1,1.9,0); S=L(0,0,3.8)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.07)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        edges={"SA":(S,A),"SB":(S,B),"SC":(S,C),"SD":(S,D),"AB":(A,B),"BC":(B,C),"CD":(C,D),"DA":(D,A)}
        return {"S":S,"A":A,"B":B,"C":C,"D":D,"edges":VGroup(visible,hidden),"base":base,"dots":dots,"edge_map":edges}

    def cube(self):
        a=1.72
        A=L(-a,-a,-a); B=L(a,-a,-a); C=L(a,a,-a); D=L(-a,a,-a)
        A1=L(-a,-a,a); B1=L(a,-a,a); C1=L(a,a,a); D1=L(-a,a,a)
        # for the fixed camera: front/right/top edges emphasized, far-left/back edges dashed
        visible=VGroup(
            solid(A,B),solid(B,C),solid(B,B1),solid(A,A1),solid(A1,B1),
            solid(B1,C1),solid(C,C1),solid(C1,D1),solid(A1,D1)
        )
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(D,D1))
        faces=VGroup(
            face(A,B,C,D,color=BLUE,opacity=0.035),
            face(A1,B1,C1,D1,color=PURPLE,opacity=0.035)
        )
        dots=VGroup(*[Dot3D(p,radius=0.04,color=GOLD) for p in [A,B,C,D,A1,B1,C1,D1]])
        edges={
            "AB":(A,B),"BC":(B,C),"CD":(C,D),"DA":(D,A),
            "A1B1":(A1,B1),"B1C1":(B1,C1),"C1D1":(C1,D1),"D1A1":(D1,A1),
            "AA1":(A,A1),"BB1":(B,B1),"CC1":(C,C1),"DD1":(D,D1),
        }
        return {"A":A,"B":B,"C":C,"D":D,"A1":A1,"B1":B1,"C1":C1,"D1":D1,
                "edges":VGroup(visible,hidden),"faces":faces,"dots":dots,"edge_map":edges,"a":a}


    def regular_square_pyramid(self):
        A=L(-2.0,-2.0,0); B=L(2.0,-2.0,0); C=L(2.0,2.0,0); D=L(-2.0,2.0,0); S=L(0,0,3.0)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.065)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        edges={"SA":(S,A),"SB":(S,B),"SC":(S,C),"SD":(S,D),"AB":(A,B),"BC":(B,C),"CD":(C,D),"DA":(D,A)}
        return {"S":S,"A":A,"B":B,"C":C,"D":D,"edges":VGroup(visible,hidden),"base":base,"dots":dots,"edge_map":edges}

    def add_pyramid_labels(self, G):
        return self.label_many([
            ("S",G["S"],RED,(-0.13,-0.04,0.13),21),
            ("A",G["A"],GOLD,(-0.16,-0.12,0.00),20),
            ("B",G["B"],GOLD,(0.13,-0.10,0.00),20),
            ("C",G["C"],GOLD,(0.12,0.10,0.00),20),
            ("D",G["D"],GOLD,(-0.15,0.10,0.00),20),
        ])

    def add_cube_labels(self, G):
        return self.label_many([
            ("A",G["A"],GOLD,(-0.14,-0.11,0),18),("B",G["B"],GOLD,(0.12,-0.10,0),18),
            ("C",G["C"],GOLD,(0.12,0.09,0),18),("D",G["D"],GOLD,(-0.15,0.10,0),18),
            ("A'",G["A1"],GOLD,(-0.15,-0.08,0.06),18),("B'",G["B1"],GOLD,(0.12,-0.07,0.06),18),
            ("C'",G["C1"],GOLD,(0.12,0.08,0.06),18),("D'",G["D1"],GOLD,(-0.15,0.09,0.06),18),
        ])

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        series=txt("HHKG CHUYÊN SÂU · 11",18,BLUE,BOLD)
        title=txt("THIẾT DIỆN II",48,GOLD,BOLD)
        sub=txt("DIỆN TÍCH & TỶ SỐ",38,INK,BOLD)
        line=txt("Đồng dạng · hình thang · hình chữ nhật · lục giác",24,CYAN,BOLD)
        note=txt("Dựng đúng ở Video 10 — tính gọn ở Video 11",22,MUTED)
        brand=txt(TEN_THAY,18,MUTED)
        g=VGroup(series,title,sub,line,note,brand).arrange(DOWN,buff=0.24)
        self.play(FadeIn(series),FadeIn(title,shift=UP*0.15),run_time=0.8)
        self.play(FadeIn(sub),FadeIn(line),FadeIn(note),FadeIn(brand),run_time=1.0)
        self.narrate(
            "Ở video mười, ta chỉ tập trung dựng thiết diện: đi qua từng mặt, tìm đúng giao tuyến và không đoán trước đa giác cắt. Video mười một giữ nguyên kỷ luật ấy nhưng đi thêm một bước: tính diện tích. Điều khó không nằm ở công thức diện tích tam giác, hình thang hay lục giác; điều khó là biến một hình cắt ba chiều thành một hình phẳng có đủ độ dài, chiều cao và tỷ số. Vì vậy mỗi bài hôm nay đều bắt đầu bằng cấu trúc của thiết diện, sau đó mới tính.",
            2.0,
        )

    # ======================================================
    # 1. TOOLKIT
    # ======================================================
    def toolkit(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-50*DEGREES,zoom=0.96)
        self.add_header("Bản đồ tính diện tích thiết diện", "Ba câu hỏi trước khi bấm công thức", "1/7")
        G=self.regular_square_pyramid(); self.add(G["base"],G["edges"],G["dots"]); self.add_pyramid_labels(G)
        k=0.56
        M=G["S"]+k*(G["A"]-G["S"]); N=G["S"]+k*(G["B"]-G["S"]); P=G["S"]+k*(G["C"]-G["S"]); Q=G["S"]+k*(G["D"]-G["S"])
        sec=face(M,N,P,Q,color=GOLD,opacity=0.20)
        outline=VGroup(solid(M,N,GOLD,5.5),solid(N,P,GOLD,5.5),solid(P,Q,GOLD,5.5),solid(Q,M,GOLD,5.5))
        self.play(FadeIn(sec),Create(outline),run_time=0.9)
        self.card("Chiến lược", "Đừng tính diện tích quá sớm", [
            ("text","1. Thiết diện là hình gì?",18,INK,BOLD),
            ("text","2. Có đồng dạng, song song hay đối xứng không?",18,INK,BOLD),
            ("text","3. Cần cạnh, đường cao hay chỉ cần tỷ số?",18,INK,BOLD),
            ("sep",),
            ("math","frac(S_(M N P Q), S_(A B C D)) = k^2",28,GOLD),
            ("text","Nếu tính được tỷ số trước, thường không cần tính từng cạnh.",16,MUTED,NORMAL),
        ],accent=CYAN)
        self.narrate(
            "Có ba câu hỏi nên đặt trước mọi bài diện tích thiết diện. Một, thiết diện là hình gì: tam giác, hình thang, hình bình hành, hình chữ nhật hay lục giác. Hai, cấu hình có đồng dạng, song song hoặc đối xứng nào giúp ta tránh tính từng cạnh hay không. Ba, nếu phải tính trực tiếp thì hình phẳng ấy cần những đại lượng nào: đáy, chiều cao, đường chéo hay bán kính ngoại tiếp. Càng trả lời được bằng tỷ số, lời giải càng ngắn và ít sai.",
            2.0,
        )
        self.takeaway("Dựng đúng hình → nhận dạng cấu trúc → ưu tiên tỷ số → cuối cùng mới tính độ dài tuyệt đối.")
        self.narrate(
            "Ví dụ ngay trên hình, mặt cắt song song đáy tạo ra một hình vuông đồng dạng với đáy. Khi tỷ số dài từ đỉnh bằng k, ta không cần đo cạnh của hình vuông mới; tỷ số diện tích lập tức là k bình phương. Đây sẽ là kỹ thuật đầu tiên và cũng là sợi dây nối diện tích thiết diện với phần thể tích ở các video trước.",
            1.7,
        )

    # ======================================================
    # 2. PARALLEL SECTION - DYNAMIC
    # ======================================================
    def parallel_section_dynamic(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-50*DEGREES,zoom=0.96)
        self.add_header("Bài 1 · Thiết diện song song đáy", "Tỷ số dài k → tỷ số diện tích k²", "2/7")
        G=self.regular_square_pyramid(); self.add(G["base"],G["edges"],G["dots"]); self.add_pyramid_labels(G)
        tracker=ValueTracker(0.28)
        def pts():
            k=tracker.get_value(); S=G["S"]
            return [S+k*(G[n]-S) for n in ["A","B","C","D"]]
        section=always_redraw(lambda: Polygon(*pts(),fill_color=GOLD,fill_opacity=0.20,stroke_color=GOLD,stroke_width=4.5))
        dots=always_redraw(lambda: VGroup(*[Dot3D(p,radius=0.045,color=GOLD) for p in pts()]))
        self.add(section,dots)
        moving_labels=[]
        for idx,name in enumerate(["M","N","P","Q"]):
            lab=mty(name,17,GOLD)
            lab.add_updater(lambda mob, i=idx: mob.move_to(pts()[i] + np.array([0.10,0.06,0.08])))
            self.add_fixed_orientation_mobjects(lab)
            moving_labels.append(lab)
        k_num=DecimalNumber(tracker.get_value(),num_decimal_places=2,font_size=26,color=CYAN)
        k_num.add_updater(lambda m: m.set_value(tracker.get_value()))
        k2_num=DecimalNumber(tracker.get_value()**2,num_decimal_places=2,font_size=26,color=GOLD)
        k2_num.add_updater(lambda m: m.set_value(tracker.get_value()**2))
        live=VGroup(txt("k =",18,CYAN,BOLD),k_num,txt("k² =",18,GOLD,BOLD),k2_num).arrange(RIGHT,buff=0.12).move_to(LEFT*2.65+DOWN*2.22)
        self.add_fixed_in_frame_mobjects(live)
        self.card("Đề bài", "M, N, P, Q cùng chia bốn cạnh bên theo tỷ số k", [
            ("math","frac(S M, S A) = frac(S N, S B) = k",25,CYAN),
            ("math","frac(S P, S C) = frac(S Q, S D) = k",25,CYAN),
            ("math","(M N P Q) parallel (A B C D)",26,GREEN),
            ("sep",),
            ("math","frac(S_(M N P Q), S_(A B C D)) = k^2",29,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Nếu bốn điểm M, N, P, Q chia bốn cạnh bên theo cùng tỷ số k tính từ đỉnh S, mặt MNPQ song song với đáy. Hai hình vuông đồng dạng theo tỷ số dài k. Vì diện tích biến đổi theo bình phương tỷ số đồng dạng, ta có diện tích thiết diện chia diện tích đáy bằng k bình phương. Quy tắc này đúng với mọi hình chóp, không riêng đáy vuông: chỉ cần mặt cắt song song đáy.",
            2.0,
        )
        self.play(tracker.animate.set_value(0.78),run_time=4.2,rate_func=linear)
        self.play(tracker.animate.set_value(0.45),run_time=2.0,rate_func=smooth)
        self.narrate(
            "Khi k tăng tuyến tính từ gần đỉnh xuống gần đáy, cạnh của thiết diện tăng tuyến tính, nhưng diện tích tăng theo k bình phương. Quan sát hai con số trên màn hình: k và k bình phương không tăng cùng tốc độ. Đây là trực giác rất quan trọng. Nếu một mặt cắt ở nửa chiều cao của hình chóp tính từ đỉnh, diện tích của nó chỉ bằng một phần tư đáy chứ không phải một nửa.",
            2.0,
        )
        self.play(tracker.animate.set_value(0.60),run_time=1.0)
        self.narrate(
            "Đặc biệt khi k bằng ba phần năm, tỷ số diện tích bằng chín phần hai mươi lăm. Ta sẽ dùng đúng số này ngay ở bài ngược tiếp theo để đi từ diện tích trở lại vị trí của mặt cắt, rồi nối tiếp sang tỷ số thể tích.",
            1.4,
        )

    # ======================================================
    # 3. REVERSE RATIO + LINK TO VOLUME
    # ======================================================
    def reverse_ratio(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-50*DEGREES,zoom=0.96)
        self.add_header("Bài 2 · Bài ngược từ diện tích", "Biết tỷ số diện tích → tìm vị trí mặt cắt → suy ra thể tích", "3/7")
        G=self.regular_square_pyramid(); self.add(G["base"],G["edges"],G["dots"]); self.add_pyramid_labels(G)
        k=3/5
        M=G["S"]+k*(G["A"]-G["S"]); N=G["S"]+k*(G["B"]-G["S"]); P=G["S"]+k*(G["C"]-G["S"]); Q=G["S"]+k*(G["D"]-G["S"])
        sec=face(M,N,P,Q,color=GOLD,opacity=0.23)
        self.play(FadeIn(sec),run_time=0.7)
        self.card("Bài ngược", "Diện tích thiết diện bằng 9/25 diện tích đáy", [
            ("math","frac(S_(M N P Q), S_(A B C D)) = frac(9, 25)",27,CYAN),
            ("math","k^2 = frac(9, 25)",28,INK),
            ("math","k = frac(3, 5)",31,GOLD),
            ("sep",),
            ("math","frac(V_(S M N P Q), V_(S A B C D)) = k^3",25,GREEN),
            ("math","k^3 = frac(27, 125)",31,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Giả sử đề không cho vị trí M, N, P, Q mà chỉ cho diện tích thiết diện bằng chín phần hai mươi lăm diện tích đáy. Vì mặt cắt song song đáy, tỷ số diện tích là k bình phương. K dương nên k bằng ba phần năm. Như vậy chỉ từ diện tích, ta đã tìm được vị trí tương đối của mặt cắt trên cả bốn cạnh bên.",
            2.0,
        )
        S=G["S"]; O=(G["A"]+G["B"]+G["C"]+G["D"])/4
        Osec=(M+N+P+Q)/4
        so=solid(S,O,GREEN,4.8,0.95); sosec=solid(S,Osec,GOLD,6.0,1.0)
        self.play(Create(so),Create(sosec),run_time=0.8)
        self.narrate(
            "Nếu chiều cao toàn hình chóp là H, khoảng cách từ S đến mặt cắt bằng ba phần năm H, còn khoảng cách từ mặt cắt xuống đáy bằng hai phần năm H. Và vì hai hình chóp đồng dạng, tỷ số thể tích chóp nhỏ so với chóp lớn bằng k lập phương, tức hai mươi bảy phần một trăm hai mươi lăm. Đây là cầu nối rất đẹp: diện tích cho k bình phương, thể tích cho k lập phương.",
            2.0,
        )
        self.takeaway("Mặt cắt song song đáy: diện tích → căn bậc hai để ra k; thể tích → lũy thừa ba của cùng k.")

    # ======================================================
    # 4. TRAPEZOID SECTION
    # ======================================================
    def trapezoid_section(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-52*DEGREES,zoom=0.96)
        self.add_header("Bài 3 · Thiết diện hình thang", "Không lấy chiều cao hình chóp làm chiều cao hình thang", "4/7")
        G=self.regular_square_pyramid(); self.add(G["base"],G["edges"],G["dots"]); self.add_pyramid_labels(G)
        S,A,B,C,D=G["S"],G["A"],G["B"],G["C"],G["D"]
        M=(S+A)/2; N=(S+B)/2
        I=(M+N)/2; J=(C+D)/2
        K=np.array([I[0],I[1],J[2]])
        sec=face(M,N,C,D,color=GOLD,opacity=0.20)
        outline=VGroup(solid(M,N,GOLD,5.8),solid(N,C,GOLD,5.8),hidden_edge(C,D,GOLD,4.2,0.95),solid(D,M,GOLD,5.8))
        pts=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [M,N,I,J,K]])
        self.play(FadeIn(sec),Create(outline),FadeIn(pts),run_time=1.0)
        self.label_many([
            ("M",M,GOLD,(-0.12,-0.08,0.08),18),("N",N,GOLD,(0.12,-0.07,0.07),18),
            ("I",I,CYAN,(-0.12,-0.04,0.08),18),("J",J,CYAN,(0.12,0.07,0.03),18),("K",K,CYAN,(-0.14,0.02,0.03),18),
        ])
        ij=solid(I,J,CYAN,5.2); ik=aux(I,K,GREEN,3.6); kj=aux(K,J,GREEN,3.6)
        self.play(Create(ij),Create(ik),Create(kj),run_time=0.9)
        self.card("Dữ kiện", "Đáy vuông cạnh 4, chiều cao SO = 3; M, N là trung điểm", [
            ("math","M N = 2",27,CYAN),
            ("math","C D = 4",27,CYAN),
            ("math","I K = frac(3, 2)",27,INK),
            ("math","K J = 3",27,INK),
            ("math","I J = frac(3 sqrt(5), 2)",29,GREEN),
            ("math","S_(M N C D) = frac(9 sqrt(5), 2)",30,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Bây giờ một thiết diện không song song đáy. Trong hình chóp đều đáy vuông cạnh bốn, chiều cao ba, M và N là trung điểm của SA và SB. Mặt phẳng qua M, N và cạnh CD tạo thiết diện MNCD. Vì MN song song AB và AB song song CD, MNCD là hình thang với hai đáy dài hai và bốn. Nhưng chiều cao của hình thang không phải chiều cao ba của hình chóp.",
            2.0,
        )
        self.narrate(
            "Gọi I và J là trung điểm của MN và CD. Đường IJ nằm ngay trong mặt phẳng thiết diện và vuông góc với hai đáy song song, nên IJ mới là chiều cao hình thang. Hạ IK vuông góc đáy. Vì M, N ở trung điểm cạnh bên, độ cao của I bằng ba phần hai. Trong mặt đáy, KJ bằng ba. Tam giác IKJ vuông cho IJ bằng căn của chín cộng chín phần tư, tức ba căn năm trên hai.",
            2.0,
        )
        self.narrate(
            "Diện tích hình thang bằng tổng hai đáy chia hai nhân chiều cao: hai cộng bốn, chia hai, nhân ba căn năm trên hai. Kết quả là chín căn năm trên hai. Mẫu nhận dạng ở đây rất quan trọng: khi thiết diện là hình thang nằm xiên trong không gian, chiều cao phải được đo trong chính mặt phẳng thiết diện, không được lấy một đoạn thẳng đứng chỉ vì nó trông giống chiều cao.",
            2.0,
        )
        self.takeaway("Chiều cao của đa giác thiết diện luôn nằm trong mặt phẳng thiết diện.")

    # ======================================================
    # 5. CUBE DIAGONAL RECTANGLE
    # ======================================================
    def cube_diagonal_rectangle(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.96)
        self.add_header("Bài 4 · Thiết diện chéo của hình lập phương", "Một hình chữ nhật có diện tích lớn hơn mặt bên", "5/7")
        G=self.cube(); self.add(G["faces"],G["edges"],G["dots"]); self.add_cube_labels(G)
        A,C,C1,A1=G["A"],G["C"],G["C1"],G["A1"]
        sec=face(A,C,C1,A1,color=PURPLE,opacity=0.22)
        outline=VGroup(aux(A,C,CYAN,5.0,1.0),solid(C,C1,GOLD,5.5),solid(C1,A1,GOLD,5.5),solid(A1,A,GOLD,5.5))
        self.play(FadeIn(sec),Create(outline),run_time=0.9)
        self.card("Thiết diện", "Mặt phẳng (ACC'A')", [
            ("math","A C = a sqrt(2)",29,CYAN),
            ("math","A A' = a",29,CYAN),
            ("math","A C perp A A'",27,GREEN),
            ("math","S_(A C C' A') = a^2 sqrt(2)",31,GOLD),
            ("sep",),
            ("math","frac(S_(A C C' A'), a^2) = sqrt(2)",28,INK),
        ],accent=PURPLE)
        self.narrate(
            "Trong hình lập phương cạnh a, mặt phẳng đi qua đường chéo AC của đáy và hai cạnh đứng AA phẩy, CC phẩy tạo thiết diện ACC phẩy A phẩy. Vì cạnh đứng vuông góc đáy nên AA phẩy vuông góc AC. Thiết diện là hình chữ nhật, một cạnh bằng a, cạnh còn lại là đường chéo đáy a căn hai. Diện tích vì thế bằng a bình phương căn hai.",
            2.0,
        )
        self.narrate(
            "Điều đáng chú ý là diện tích thiết diện này lớn hơn diện tích một mặt vuông của lập phương theo tỷ số căn hai. Thiết diện không nhất thiết nhỏ hơn một mặt của khối; nó phụ thuộc hướng cắt. Đây là lý do ta không nên suy luận diện tích bằng trực giác hình vẽ. Hãy đưa đa giác cắt về đúng hình phẳng rồi tính bằng độ dài thật của các cạnh nằm trong mặt phẳng ấy.",
            2.0,
        )

    # ======================================================
    # 6. REGULAR HEXAGON IN CUBE
    # ======================================================
    def cube_regular_hexagon(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.96)
        self.add_header("Bài 5 · Lục giác đều trong hình lập phương", "Sáu trung điểm — sáu tam giác đều quanh tâm", "6/7")
        G=self.cube(); self.add(G["faces"],G["edges"],G["dots"]); self.add_cube_labels(G)
        M=(G["B"]+G["C"])/2
        N=(G["C"]+G["D"])/2
        P=(G["D"]+G["D1"])/2
        Q=(G["D1"]+G["A1"])/2
        R=(G["A1"]+G["B1"])/2
        T=(G["B"]+G["B1"])/2
        pts=[M,N,P,Q,R,T]
        O=(G["A"]+G["C1"])/2
        sec=Polygon(*pts,fill_color=GOLD,fill_opacity=0.20,stroke_color=GOLD,stroke_width=4.5)
        pdots=VGroup(*[Dot3D(x,radius=0.048,color=GOLD) for x in pts],Dot3D(O,radius=0.05,color=CYAN))
        self.play(FadeIn(sec),FadeIn(pdots),run_time=0.8)
        self.label_many([
            ("M",M,GOLD,(0.12,-0.05,0.05),17),("N",N,GOLD,(0.08,0.10,0.04),17),
            ("P",P,GOLD,(-0.14,0.08,0.05),17),("Q",Q,GOLD,(-0.14,0.03,0.06),17),
            ("R",R,GOLD,(-0.04,-0.10,0.06),17),("T",T,GOLD,(0.12,-0.08,0.05),17),
            ("O",O,CYAN,(0.10,0.03,0.08),17),
        ])
        radii=VGroup(*[solid(O,x,CYAN,3.2,0.80) for x in pts])
        self.play(Create(radii),run_time=1.0)
        self.card("Cấu trúc", "M, N, P, Q, R, T là trung điểm sáu cạnh", [
            ("math","M N = frac(a, sqrt(2))",28,CYAN),
            ("math","O M = M N",28,GREEN),
            ("text","Sáu tam giác quanh O đều là tam giác đều.",16,MUTED,NORMAL),
            ("math","S_(M N P Q R T) = 6 times frac(sqrt(3), 4) times frac(a^2, 2)",24,INK),
            ("math","S_(M N P Q R T) = frac(3 sqrt(3), 4) a^2",31,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Bài đẹp nhất của video: mặt phẳng qua sáu trung điểm thích hợp của sáu cạnh hình lập phương tạo một lục giác đều. Gọi O là tâm lập phương. Hai trung điểm liên tiếp, chẳng hạn M của BC và N của CD, cách nhau bằng đường chéo của một hình vuông cạnh a trên hai theo hai phương vuông góc, nên MN bằng a trên căn hai.",
            2.0,
        )
        self.narrate(
            "Mặt khác, OM cũng bằng a trên căn hai. Tương tự với cả sáu đỉnh, nên O nối với sáu đỉnh chia lục giác thành sáu tam giác đều cạnh a trên căn hai. Diện tích mỗi tam giác bằng căn ba trên bốn nhân a bình phương trên hai. Nhân sáu, ta được diện tích thiết diện bằng ba căn ba trên bốn nhân a bình phương.",
            2.0,
        )
        # emphasize one equilateral triangle
        tri=Polygon(O,M,N,fill_color=CYAN,fill_opacity=0.20,stroke_color=CYAN,stroke_width=4)
        self.play(FadeIn(tri),run_time=0.55)
        self.narrate(
            "Cách chia từ tâm mạnh hơn việc cố tính trực tiếp chiều cao của lục giác. Nó biến một đa giác sáu cạnh trong không gian thành sáu tam giác phẳng giống hệt nhau. Đây là mẫu tư duy nên nhớ: với thiết diện có đối xứng cao, hãy tìm tâm đối xứng rồi chia nhỏ thành các hình cơ bản trước khi dùng công thức diện tích.",
            1.8,
        )
        self.takeaway("Đối xứng cao → tìm tâm → chia thiết diện thành các tam giác bằng nhau.")

    # ======================================================
    # 7. SYNTHESIS + ERRORS
    # ======================================================
    def synthesis(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ phương pháp", "Từ hình cắt đến diện tích", "7/7")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Song song đáy",20,INK),txt("→ đồng dạng, k²",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Bài ngược",20,INK),txt("→ căn tỷ số diện tích",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Hình thang xiên",20,INK),txt("→ tìm chiều cao trong mặt cắt",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Hình hộp",20,INK),txt("→ nhận dạng hình chữ nhật",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Đối xứng cao",20,INK),txt("→ chia nhỏ từ tâm",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30).shift(LEFT*2.75+UP*0.22)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Sai lầm", "Bốn lỗi cần tránh", [
            ("text","Lấy chiều cao khối làm chiều cao đa giác cắt.",17,RED,BOLD),
            ("text","Thấy mặt cắt song song đáy nhưng quên bình phương tỷ số.",17,RED,BOLD),
            ("text","Dùng diện tích hình chiếu thay cho diện tích thật của thiết diện.",17,RED,BOLD),
            ("text","Gặp lục giác rồi cố tính sáu cạnh thay vì dùng đối xứng.",17,RED,BOLD),
            ("sep",),
            ("math","S_0 = S cos beta",28,CYAN),
            ("text","Diện tích hình chiếu chỉ bằng diện tích thật nhân cos của góc hai mặt.",15,MUTED,NORMAL),
        ],accent=RED)
        self.play(FadeIn(left,shift=RIGHT*0.12),run_time=0.7)
        self.narrate(
            "Tóm lại, diện tích thiết diện có năm cửa vào. Mặt cắt song song đáy thì dùng đồng dạng và bình phương tỷ số. Bài ngược thì lấy căn bậc hai của tỷ số diện tích để trở về tỷ số dài. Hình thang xiên phải dựng đúng chiều cao nằm trong mặt cắt. Hình hộp thường cho những hình chữ nhật hoặc hình bình hành dễ nhận dạng. Còn cấu hình đối xứng cao như lục giác trong lập phương thì nên chia từ tâm.",
            2.0,
        )
        self.narrate(
            "Bốn lỗi lớn cũng rất rõ. Một, lấy chiều cao của khối thay cho chiều cao của đa giác cắt. Hai, quên rằng diện tích đổi theo bình phương chứ không theo tỷ số dài. Ba, nhầm diện tích hình chiếu với diện tích thật; nếu hai mặt tạo góc beta thì diện tích hình chiếu bằng diện tích thật nhân cos beta. Bốn, gặp đa giác nhiều cạnh nhưng không khai thác đối xứng nên lời giải trở nên dài không cần thiết.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 12",17,BLUE,BOLD),
            txt("THIẾT DIỆN III · ĐIỂM ĐỘNG & CỰC TRỊ",25,GOLD,BOLD),
            txt("Mặt cắt biến dạng · diện tích theo tham số · cực trị · cấu hình khó",18,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box)
        self.play(FadeIn(next_box),run_time=0.55)
        self.narrate(
            "Video mười hai sẽ là phần khó nhất của chặng thiết diện. Mặt phẳng cắt sẽ chuyển động, hình cắt thay đổi theo tham số, có lúc đổi từ tam giác sang tứ giác hoặc lục giác. Ta sẽ lập công thức diện tích theo vị trí điểm động rồi tìm cực trị. Khi đó kỹ năng dựng của video mười và kỹ năng tính của video mười một sẽ được ghép lại trong cùng một bài.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.toolkit()
        self.parallel_section_dynamic()
        self.reverse_ratio()
        self.trapezoid_section()
        self.cube_diagonal_rectangle()
        self.cube_regular_hexagon()
        self.synthesis()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_11_thiet_dien_II_dien_tich_ty_so_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 11")
    print("Angle markers: geometrically exact 3D ray-to-ray arcs")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_11.wav"
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

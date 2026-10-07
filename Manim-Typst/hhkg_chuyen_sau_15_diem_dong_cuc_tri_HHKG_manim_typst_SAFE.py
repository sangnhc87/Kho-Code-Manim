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
# HHKG CHUYEN SAU 15 - DIEM DONG & CUC TRI HHKG
# Manim Community + MathTypst SAFE | Standalone 100%
# Muc tieu: 12-15 phut; bat bien, khoang cach, goc, trai phang, the tich.
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

# ==========================================================
# EXTRA DYNAMIC GEOMETRY FOR VIDEO 12
# ==========================================================
def regular_tetra_raw(scale=1.55):
    """Regular tetrahedron with opposite edges AD and BC parallel to z-level sections."""
    raw = {
        "A": np.array([ 1.0,  1.0,  1.0]),
        "D": np.array([-1.0, -1.0,  1.0]),
        "B": np.array([ 1.0, -1.0, -1.0]),
        "C": np.array([-1.0,  1.0, -1.0]),
    }
    return {k: L(*(scale*v)) for k, v in raw.items()}


def cube_unit_map(x, y, z, side_display=3.05):
    """Map normalized unit-cube coordinates to the geometry area on screen."""
    v = side_display * (np.array([x, y, z], dtype=float) - 0.5)
    return GEO_SCALE * v + GEO_SHIFT


def cube_unit_vertices(side_display=3.05):
    P = lambda x,y,z: cube_unit_map(x,y,z,side_display)
    return {
        "A":P(0,0,0), "B":P(1,0,0), "C":P(1,1,0), "D":P(0,1,0),
        "A1":P(0,0,1), "B1":P(1,0,1), "C1":P(1,1,1), "D1":P(0,1,1),
    }


def cube_section_normalized(t):
    """Ordered polygon of x+y+z=t inside [0,1]^3, 0<t<3."""
    verts = [
        np.array([0.,0.,0.]), np.array([1.,0.,0.]), np.array([1.,1.,0.]), np.array([0.,1.,0.]),
        np.array([0.,0.,1.]), np.array([1.,0.,1.]), np.array([1.,1.,1.]), np.array([0.,1.,1.]),
    ]
    edge_ids = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    pts=[]
    for i,j in edge_ids:
        p,q=verts[i],verts[j]
        fp=float(np.sum(p)-t); fq=float(np.sum(q)-t)
        if abs(fp)<1e-9:
            pts.append(p.copy())
        if abs(fq)<1e-9:
            pts.append(q.copy())
        if fp*fq < -1e-12:
            u=fp/(fp-fq)
            pts.append(p+u*(q-p))
    pts=unique_points(pts,1e-7)
    if len(pts)<3:
        return []
    return order_points_in_plane(pts, np.array([1.,1.,1.]))


def cube_section_area_factor(t):
    """Area divided by a^2 for plane x+y+z=t a in a cube of side a."""
    if t <= 1:
        return math.sqrt(3)/2 * t*t
    if t <= 2:
        return math.sqrt(3)/2 * (-2*t*t + 6*t - 3)
    return math.sqrt(3)/2 * (3-t)*(3-t)


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
        series = txt("HHKG CHUYÊN SÂU · 15", 15, BLUE, BOLD)
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
        hud = VGroup(series, title_m, sub_m, accent, prog, rule, divider, teacher)
        self.add_fixed_in_frame_mobjects(hud)
        return hud

    def card(self, kicker, title, items, accent=GOLD, height=5.25, auto_add=True):
        bg = Rectangle(width=5.12, height=height, fill_color=PANEL, fill_opacity=0.90,
                       stroke_color=GRID, stroke_width=0.9, stroke_opacity=0.36)
        bg.move_to(RIGHT*4.28+DOWN*0.03)
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
                _, s, size, color, weight = item
                mob = txt(s, size, color, weight)
            elif kind == "math":
                _, expr, size, color = item
                mob = mty(expr, size, color)
            elif kind == "sep":
                mob = Line(LEFT*2.00, RIGHT*2.00, color=GRID,
                           stroke_width=0.9, stroke_opacity=0.55)
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
        label.move_to(LEFT*2.55+DOWN*2.52)
        self.add_fixed_in_frame_mobjects(label)
        return label

    def add_label(self, name, pt, color=GOLD, off=(0.10,-0.10,0.05), size=22):
        lab = mty(name, size, color).move_to(pt+np.array(off, dtype=float))
        self.add_fixed_orientation_mobjects(lab)
        return lab

    def label_many(self, data):
        return VGroup(*[self.add_label(*item) for item in data])

    # ---------- geometry models ----------
    def right_pyramid(self):
        A=L(-2,-2,0); B=L(2,-2,0); C=L(2,2,0); D=L(-2,2,0); S=L(-2,-2,3)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.055)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def tri_rect_tetra(self):
        O=L(-1.2,-1.2,0); A=L(0.8,-1.2,0); B=L(-1.2,0.8,0); C=L(-1.2,-1.2,1.0)
        edges=VGroup(
            solid(O,A,CYAN,4.5), solid(O,B,CYAN,4.5), solid(O,C,GREEN,4.8),
            solid(A,B,EDGE,4.2), solid(A,C,EDGE,3.8), hidden_edge(B,C,DIM,2.8)
        )
        faces=VGroup(face(O,A,B,color=BLUE,opacity=0.065), face(O,A,C,color=GREEN,opacity=0.025))
        dots=VGroup(*[Dot3D(p,radius=0.055,color=GOLD) for p in [O,A,B]],Dot3D(C,radius=0.06,color=RED))
        return {"O":O,"A":A,"B":B,"C":C,"edges":edges,"faces":faces,"dots":dots}

    def centered_pyramid(self):
        A=L(-2,-2,0); B=L(2,-2,0); C=L(2,2,0); D=L(-2,2,0)
        O=L(0,0,0); S=L(0,0,3)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.055)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D,O]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"O":O,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def cube_model(self):
        G=cube_unit_vertices(side_display=3.05)
        A,B,C,D,A1,B1,C1,D1=[G[k] for k in ["A","B","C","D","A1","B1","C1","D1"]]
        visible=VGroup(solid(A,B),solid(B,C),solid(B,B1),solid(A,A1),solid(A1,B1),
                       solid(B1,C1),solid(C,C1),solid(C1,D1),solid(A1,D1))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(D,D1))
        faces=VGroup(face(A,B,B1,A1,color=BLUE,opacity=0.040),
                     face(B,C,C1,B1,color=PURPLE,opacity=0.035))
        dots=VGroup(*[Dot3D(p,radius=0.04,color=GOLD) for p in [A,B,C,D,A1,B1,C1,D1]])
        return {**G,"edges":VGroup(visible,hidden),"faces":faces,"dots":dots}

    # ======================================================
    # 1. INTRO + TOOLKIT
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Điểm động & cực trị HHKG",
                        "Đừng lập hàm trước khi biết đại lượng nào thật sự thay đổi",
                        "1/7")
        left=VGroup(
            txt("BƯỚC 1",16,GOLD,BOLD),txt("Kiểm tra bất biến",22,INK,BOLD),
            txt("BƯỚC 2",16,GOLD,BOLD),txt("Chọn tham số hình học",22,INK,BOLD),
            txt("BƯỚC 3",16,GOLD,BOLD),txt("Tối ưu đại lượng đơn giản hơn",22,INK,BOLD),
            txt("BƯỚC 4",16,GOLD,BOLD),txt("Kiểm tra miền và điểm đạt",22,INK,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.18).shift(LEFT*2.65+UP*0.15)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Tư duy lõi","Năm công cụ sẽ dùng",[
            ("text","Bất biến trước, cực trị sau.",17,CYAN,BOLD),
            ("math","d^2",28,GOLD),
            ("text","Tối ưu bình phương khoảng cách.",16,MUTED,NORMAL),
            ("math","tan alpha",28,GOLD),
            ("text","Tối ưu tang thay vì tối ưu góc.",16,MUTED,NORMAL),
            ("math","V_1 V_2",28,GOLD),
            ("text","Chuẩn hóa bằng tỷ số trước khi đạo hàm.",16,MUTED,NORMAL),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.8)
        self.narrate(
            "Từ video mười lăm, ta bước vào chặng điểm động và cực trị hình học không gian. Một lỗi rất phổ biến là thấy điểm M chạy thì lập tức đặt x, viết công thức dài rồi đạo hàm. Cách đó đôi khi đúng nhưng thường bỏ qua cấu trúc hình học. Trước hết phải hỏi: đại lượng cần tìm có thật sự thay đổi không, hay nó là một bất biến bị che bởi chuyển động của điểm?",
            2.0,
        )
        self.narrate(
            "Nếu đại lượng có thay đổi, ta chọn tham số sao cho hình học đơn giản nhất. Khoảng cách thường nên tối ưu bình phương khoảng cách. Góc nên chuyển sang sin, cos hoặc tang nếu các hàm ấy đơn điệu trên miền đang xét. Với bài thể tích, nên chuẩn hóa về tỷ số thể tích trước. Còn bài đường đi trên mặt đa diện nhiều khi không cần đạo hàm, chỉ cần trải phẳng đúng các mặt.",
            2.0,
        )

    # ======================================================
    # 2. INVARIANT TRAP
    # ======================================================
    def invariant_trap(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Bẫy bất biến","M chạy trên AD nhưng khoảng cách đến (SBC) không đổi","2/7")
        G=self.right_pyramid()
        self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("S",G["S"],RED,(-0.14,-0.10,0.12),19),("A",G["A"],GOLD,(-0.15,-0.12,0),18),
            ("B",G["B"],GOLD,(0.12,-0.12,0),18),("C",G["C"],GOLD,(0.12,0.10,0),18),
            ("D",G["D"],GOLD,(-0.15,0.10,0),18),
        ])
        plane=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.18)
        self.add(plane)

        t=ValueTracker(0.08)
        def raw_M():
            y=-2+4*t.get_value()
            return L(-2,y,0)
        def raw_H():
            y=-2+4*t.get_value()
            return L(-14/25,y,48/25)

        M=always_redraw(lambda: Dot3D(raw_M(),radius=0.065,color=GOLD))
        H=always_redraw(lambda: Dot3D(raw_H(),radius=0.048,color=CYAN))
        MH=always_redraw(lambda: solid(raw_M(),raw_H(),GOLD,5.3,1.0))
        self.add(M,H,MH)

        self.card("Nhận dạng","Song song làm mất biến",[
            ("math","A D parallel B C",28,CYAN),
            ("text","BC nằm trong mặt phẳng (SBC).",16,MUTED,NORMAL),
            ("math","A D parallel (S B C)",29,GREEN),
            ("math","d(M,(S B C)) = d(A,(S B C))",27,INK),
            ("math","d(A,(S B C)) = frac(12, 5)",31,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Ta trở lại hình chóp quen thuộc: đáy ABCD là hình vuông cạnh bốn, SA bằng ba và vuông góc với đáy. Điểm M chạy trên cạnh AD. Câu hỏi tưởng như là một bài điểm động: khoảng cách từ M đến mặt phẳng SBC nhỏ nhất khi nào? Nhưng AD song song BC, còn BC nằm trong mặt phẳng SBC. Vì AD không nằm trên mặt phẳng ấy, suy ra AD song song với mặt phẳng SBC.",
            2.0,
        )
        self.play(t.animate.set_value(0.92),run_time=3.0,rate_func=linear)
        self.play(t.animate.set_value(0.30),run_time=2.0,rate_func=linear)
        self.narrate(
            "Quan sát đoạn vuông góc màu vàng khi M chạy: nó chỉ trượt song song, độ dài không đổi. Mọi điểm trên một đường thẳng song song với một mặt phẳng đều cách mặt phẳng ấy một khoảng như nhau. Vì vậy không hề có bài cực trị ở đây. Khoảng cách luôn bằng khoảng cách từ A đến mặt SBC, kết quả đã biết là mười hai phần năm.",
            2.0,
        )
        self.takeaway("Bài điểm động đầu tiên cần kiểm tra: đại lượng có phải bất biến không?")
        self.narrate(
            "Đây là thói quen tiết kiệm rất nhiều thời gian: trước khi đặt tham số, kiểm tra song song, vuông góc, đồng dạng và các tỷ số cố định. Nếu cấu trúc đã khóa đại lượng, việc lập hàm chỉ làm lời giải dài hơn mà không thêm giá trị toán học.",
            1.7,
        )

    # ======================================================
    # 3. MIN DISTANCE IN A TRI-RECTANGULAR TETRAHEDRON
    # ======================================================
    def min_distance(self):
        self.clear_all()
        self.set_camera_orientation(phi=70*DEGREES,theta=-48*DEGREES,zoom=1.00)
        self.add_header("Bài 2 · Khoảng cách nhỏ nhất","Tối ưu CM bằng cách tối ưu hình chiếu OM","3/7")
        G=self.tri_rect_tetra()
        self.add(G["faces"],G["edges"],G["dots"])
        self.label_many([
            ("O",G["O"],GOLD,(-0.16,-0.12,-0.02),18),("A",G["A"],GOLD,(0.12,-0.10,0),18),
            ("B",G["B"],GOLD,(-0.15,0.10,0),18),("C",G["C"],RED,(-0.13,-0.06,0.12),19),
        ])
        # right-angle marks at O
        self.add(right_angle_3d(G["O"],G["A"]-G["O"],G["B"]-G["O"],0.20,CYAN,3.6))
        self.add(right_angle_3d(G["O"],G["A"]-G["O"],G["C"]-G["O"],0.20,GREEN,3.6))

        t=ValueTracker(0.08)
        def Mp():
            return (1-t.get_value())*G["A"]+t.get_value()*G["B"]
        H=(G["A"]+G["B"])/2
        M=always_redraw(lambda: Dot3D(Mp(),radius=0.065,color=GOLD))
        CM=always_redraw(lambda: solid(G["C"],Mp(),GOLD,5.0,1.0))
        OM=always_redraw(lambda: aux(G["O"],Mp(),CYAN,3.5,0.95))
        Hdot=Dot3D(H,radius=0.052,color=GREEN)
        OH=aux(G["O"],H,GREEN,4.0,1.0)
        markH=right_angle_3d(H,G["A"]-H,G["O"]-H,0.18,GREEN,3.6)
        self.add(M,CM,OM,Hdot,OH,markH)
        self.add_label("H",H,GREEN,(0.02,0.10,0.04),18)

        self.card("Dữ kiện","Ba cạnh tại O đôi một vuông góc",[
            ("math","O A = O B = 2",28,CYAN),
            ("math","O C = 1",28,GREEN),
            ("math","C O perp (A O B)",28,INK),
            ("math","C M^2 = C O^2 + O M^2",29,GOLD),
            ("math","O H perp A B",28,GREEN),
            ("math","C H = sqrt(3)",32,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Xét tứ diện vuông tại O: OA và OB cùng bằng hai, OC bằng một, ba cạnh OA, OB, OC đôi một vuông góc. Điểm M chạy trên AB. Ta cần tìm giá trị nhỏ nhất của CM. Nếu viết CM theo một tham số trên AB, ta sẽ nhận một biểu thức bậc hai. Nhưng hình học cho một đường ngắn hơn.",
            2.0,
        )
        self.play(t.animate.set_value(0.88),run_time=2.8,rate_func=linear)
        self.play(t.animate.set_value(0.50),run_time=2.2,rate_func=smooth)
        self.narrate(
            "Vì CO vuông góc với mặt phẳng AOB, nên CO vuông góc OM với mọi vị trí của M. Do đó CM bình phương bằng CO bình phương cộng OM bình phương. CO là hằng số, vậy muốn CM nhỏ nhất chỉ cần làm OM nhỏ nhất. Trong mặt phẳng tam giác AOB, điểm gần O nhất trên AB chính là chân đường vuông góc H.",
            2.0,
        )
        self.narrate(
            "Tam giác AOB vuông cân tại O, OA bằng OB bằng hai. Vì thế chân H đồng thời là trung điểm AB và OH bằng căn hai. Suy ra CH bình phương bằng một cộng hai bằng ba, nên khoảng cách nhỏ nhất là căn ba. Điểm đạt cực trị xuất hiện từ một phép chiếu vuông góc, không phải từ đạo hàm.",
            2.0,
        )
        self.takeaway("Khoảng cách 3D → tách thành hằng số vuông góc + bài khoảng cách phẳng.")

    # ======================================================
    # 4. MAX ANGLE IN A SQUARE PYRAMID
    # ======================================================
    def max_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI,theta=-54*DEGREES,zoom=VIEW_ZOOM)
        self.add_header("Bài 3 · Góc lớn nhất","M chạy trên AB; tối ưu góc giữa SM và mặt đáy","4/7")
        G=self.centered_pyramid()
        self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("S",G["S"],RED,(-0.10,-0.06,0.13),19),("A",G["A"],GOLD,(-0.14,-0.12,0),18),
            ("B",G["B"],GOLD,(0.12,-0.12,0),18),("C",G["C"],GOLD,(0.12,0.10,0),18),
            ("D",G["D"],GOLD,(-0.14,0.10,0),18),("O",G["O"],GREEN,(0.08,0.08,0.05),18),
        ])
        N=(G["A"]+G["B"])/2
        self.add(Dot3D(N,radius=0.045,color=GREEN))
        self.add_label("N",N,GREEN,(0.02,-0.12,0.03),18)
        self.add(aux(G["S"],G["O"],GREEN,4.0,1.0))
        self.add(aux(G["O"],N,CYAN,3.4,0.9))

        t=ValueTracker(0.10)
        def Mp():
            return (1-t.get_value())*G["A"]+t.get_value()*G["B"]
        M=always_redraw(lambda: Dot3D(Mp(),radius=0.065,color=GOLD))
        SM=always_redraw(lambda: solid(G["S"],Mp(),GOLD,5.2,1.0))
        OM=always_redraw(lambda: aux(G["O"],Mp(),CYAN,4.0,0.96))
        arc=always_redraw(lambda: angle_arc_3d(
            Mp(),G["O"]-Mp(),G["S"]-Mp(),radius=0.28,color=GOLD,width=5.0
        ))
        alpha_label=mty("alpha",18,GOLD)
        self.add_fixed_orientation_mobjects(alpha_label)
        def update_alpha(mob):
            M0=Mp()
            u=G["O"]-M0; u=u/np.linalg.norm(u)
            v=G["S"]-M0; v=v/np.linalg.norm(v)
            b=u+v
            if np.linalg.norm(b)<1e-8:
                b=u
            b=b/np.linalg.norm(b)
            mob.move_to(M0+0.42*b+np.array([0,0,0.03]))
        alpha_label.add_updater(update_alpha)
        self.add(M,SM,OM,arc)

        self.card("Hình chiếu","Không tối ưu góc trực tiếp",[
            ("math","alpha = hat(O M S, size: #155%)",28,GOLD),
            ("math","O N = 2",27,CYAN),
            ("math","O M = sqrt(4+x^2)",28,INK),
            ("math","tan alpha = frac(3, sqrt(4+x^2))",29,GOLD),
            ("math","x = 0 => M = N",27,GREEN),
            ("math","tan alpha = frac(3, 2)",31,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Cho hình chóp có đáy ABCD là hình vuông cạnh bốn, SO vuông góc đáy và SO bằng ba. Điểm M chạy trên AB. Ta tìm góc lớn nhất giữa SM và mặt phẳng đáy. Hình chiếu của S là O, còn M đã nằm trên đáy, nên hình chiếu của SM xuống đáy là OM. Vì vậy góc cần tối ưu chính là góc OMS; cung vàng trên hình luôn được dựng từ đúng hai tia MO và MS.",
            2.0,
        )
        self.play(t.animate.set_value(0.90),run_time=3.0,rate_func=linear)
        self.play(t.animate.set_value(0.50),run_time=2.0,rate_func=smooth)
        self.narrate(
            "Trong tam giác vuông SOM, tang alpha bằng SO chia OM. SO cố định bằng ba, nên alpha lớn nhất khi OM nhỏ nhất. Gọi N là trung điểm AB. Vì O là tâm hình vuông, ON vuông góc AB và ON bằng hai. Nếu đặt x bằng MN thì OM bằng căn của bốn cộng x bình phương.",
            2.0,
        )
        self.narrate(
            "Do đó tang alpha bằng ba chia căn của bốn cộng x bình phương. Mẫu số nhỏ nhất khi x bằng không, tức M trùng N. Khi ấy tang alpha bằng ba phần hai. Ta không cần lấy đạo hàm của hàm arctang; tính đơn điệu của tang trên khoảng góc nhọn đã biến bài góc thành bài khoảng cách từ tâm O đến cạnh AB.",
            2.0,
        )
        self.takeaway("Tối ưu góc nhọn → thường tối ưu sin, cos hoặc tan trước.")

    # ======================================================
    # 5. SHORTEST PATH ON A CUBE BY UNFOLDING
    # ======================================================
    def cube_unfolding(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 4 · Đường đi ngắn nhất","AM + MC' với M chạy trên cạnh BB' của lập phương","5/7")
        G=self.cube_model()
        self.add(G["faces"],G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.14,-0.10,0),17),("B",G["B"],GOLD,(0.10,-0.10,0),17),
            ("B'",G["B1"],GOLD,(0.10,-0.05,0.10),17),("C'",G["C1"],GOLD,(0.10,0.08,0.08),17),
        ])

        t=ValueTracker(0.15)
        def Mp():
            return (1-t.get_value())*G["B"]+t.get_value()*G["B1"]
        M=always_redraw(lambda: Dot3D(Mp(),radius=0.065,color=GOLD))
        AM=always_redraw(lambda: solid(G["A"],Mp(),CYAN,5.0,1.0))
        MC=always_redraw(lambda: solid(Mp(),G["C1"],GOLD,5.0,1.0))
        self.add(M,AM,MC)
        self.card("Mấu chốt","Hai đoạn nằm trên hai mặt kề nhau",[
            ("text","Trải hai mặt quanh cạnh BB'.",17,CYAN,BOLD),
            ("math","A M + M C' >= A X",29,GOLD),
            ("math","A X = a sqrt(5)",31,GOLD),
            ("math","B M = frac(a, 2)",30,GREEN),
            ("text","Dấu bằng khi A, M, X thẳng hàng.",16,MUTED,NORMAL),
        ],accent=CYAN)
        self.narrate(
            "Trong lập phương cạnh a, M chạy trên cạnh BB phẩy. Ta cần tìm giá trị nhỏ nhất của tổng AM cộng MC phẩy. Hai đoạn này không cùng nằm trên một mặt của lập phương: AM nằm trên mặt ABB phẩy A phẩy, còn MC phẩy nằm trên mặt BCC phẩy B phẩy. Đây là tín hiệu rất điển hình của phương pháp trải phẳng.",
            2.0,
        )
        self.play(t.animate.set_value(0.85),run_time=2.8,rate_func=linear)
        self.play(t.animate.set_value(0.50),run_time=1.8,rate_func=smooth)
        self.narrate(
            "Nếu cố viết căn thức theo BM rồi đạo hàm, ta vẫn giải được nhưng không thấy bản chất. Hãy giữ mặt ABB phẩy A phẩy và xoay mặt BCC phẩy B phẩy quanh cạnh chung BB phẩy ra cùng một mặt phẳng. Ảnh của C phẩy sau khi trải gọi là X. Khi ấy độ dài MC phẩy được bảo toàn thành MX.",
            2.0,
        )

        # switch to a clean 2D unfolding
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bài 4 · Trải phẳng hai mặt","Đường gấp khúc trở thành một đoạn thẳng","5/7")
        B=np.array([-2.55,-1.20,0]); B1=np.array([-2.55,1.20,0])
        A=np.array([-4.95,-1.20,0]); A1=np.array([-4.95,1.20,0])
        C=np.array([-0.15,-1.20,0]); X=np.array([-0.15,1.20,0])
        M2=np.array([-2.55,0.00,0])
        left_square=Polygon(A,B,B1,A1,fill_color=BLUE,fill_opacity=0.08,stroke_color=EDGE,stroke_width=3.2)
        right_square=Polygon(B,C,X,B1,fill_color=PURPLE,fill_opacity=0.08,stroke_color=EDGE,stroke_width=3.2)
        shared=Line(B,B1,color=GOLD,stroke_width=4.5)
        straight=Line(A,X,color=GREEN,stroke_width=5.0)
        dotM=Dot(M2,radius=0.075,color=GOLD)
        self.add_fixed_in_frame_mobjects(left_square,right_square,shared,straight,dotM)
        for s,p,off in [
            ("A",A,LEFT*0.15+DOWN*0.15),("B",B,RIGHT*0.10+DOWN*0.16),
            ("B'",B1,RIGHT*0.10+UP*0.12),("X",X,RIGHT*0.12+UP*0.12),
            ("M",M2,RIGHT*0.12),
        ]:
            lab=mty(s,18,GOLD).move_to(p+off)
            self.add_fixed_in_frame_mobjects(lab)
        self.card("Tam giác phẳng","Không cần đạo hàm",[
            ("math","A M + M X >= A X",28,INK),
            ("math","A X^2 = (2a)^2 + a^2",28,CYAN),
            ("math","A X = a sqrt(5)",32,GOLD),
            ("math","B M = frac(a, 2)",31,GREEN),
        ],accent=GREEN)
        self.play(Create(straight),run_time=0.8)
        self.narrate(
            "Sau khi trải, hai hình vuông tạo thành một hình chữ nhật kích thước hai a nhân a. M vẫn phải nằm trên đường chung BB phẩy. Tổng AM cộng MX luôn lớn hơn hoặc bằng đoạn thẳng AX. Đường AX cắt BB phẩy đúng tại trung điểm M, nên dấu bằng đạt được. Theo định lý Pythagore, AX bằng a căn năm.",
            2.0,
        )
        self.narrate(
            "Vậy tổng nhỏ nhất là a căn năm và M là trung điểm BB phẩy. Đây là một mẫu rất mạnh: tổng các quãng đường trên những mặt kề của đa diện thường nên trải phẳng trước. Khi trải đúng, bài cực trị không gian có thể biến thành bất đẳng thức tam giác đơn giản trong mặt phẳng.",
            2.0,
        )

    # ======================================================
    # 6. VOLUME PRODUCT WITH A MOVING PARALLEL SECTION
    # ======================================================
    def volume_product(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI,theta=-54*DEGREES,zoom=VIEW_ZOOM)
        self.add_header("Bài 5 · Tích hai thể tích","Mặt cắt song song đáy chạy trên hình chóp","6/7")
        G=self.centered_pyramid()
        self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("S",G["S"],RED,(-0.10,-0.06,0.13),19),("A",G["A"],GOLD,(-0.14,-0.12,0),17),
            ("B",G["B"],GOLD,(0.12,-0.12,0),17),("C",G["C"],GOLD,(0.12,0.10,0),17),
            ("D",G["D"],GOLD,(-0.14,0.10,0),17),("O",G["O"],GREEN,(0.08,0.08,0.04),17),
        ])
        self.add(aux(G["S"],G["O"],GREEN,3.8,0.90))

        u=ValueTracker(0.22)
        def sec_point(P):
            return G["S"] + u.get_value()*(P-G["S"])
        section=always_redraw(lambda: face(
            sec_point(G["A"]),sec_point(G["B"]),sec_point(G["C"]),sec_point(G["D"]),
            color=GOLD,opacity=0.25,stroke=GOLD,stroke_width=2.8
        ))
        sec_edges=always_redraw(lambda: VGroup(
            solid(sec_point(G["A"]),sec_point(G["B"]),GOLD,4.2,1.0),
            solid(sec_point(G["B"]),sec_point(G["C"]),GOLD,4.2,1.0),
            solid(sec_point(G["C"]),sec_point(G["D"]),GOLD,4.2,1.0),
            solid(sec_point(G["D"]),sec_point(G["A"]),GOLD,4.2,1.0),
        ))
        M=always_redraw(lambda: Dot3D(G["S"]+u.get_value()*(G["O"]-G["S"]),radius=0.055,color=GREEN))
        self.add(section,sec_edges,M)

        self.card("Chuẩn hóa","Đặt u là tỷ số dài từ đỉnh S",[
            ("math","u = frac(S M, S O)",28,CYAN),
            ("math","V_1 = u^3 V",29,GOLD),
            ("math","V_2 = (1-u^3) V",28,INK),
            ("math","V_1 V_2 = V^2 u^3(1-u^3)",27,GOLD),
            ("math","y = u^3",27,GREEN),
            ("math","y(1-y) <= frac(1, 4)",29,GREEN),
            ("math","u = (frac(1, 2))^(frac(1, 3))",27,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Bài cuối cùng nối điểm động với tỷ số thể tích. Trong hình chóp S.ABCD, điểm M chạy trên SO. Qua M dựng mặt phẳng song song đáy, cắt bốn cạnh bên tạo một hình chóp nhỏ phía trên và một chóp cụt phía dưới. Đặt u bằng SM chia SO. Do đồng dạng, mọi tỷ số dài của chóp nhỏ so với chóp lớn đều bằng u.",
            2.0,
        )
        self.play(u.animate.set_value(0.92),run_time=3.0,rate_func=linear)
        self.play(u.animate.set_value(0.55),run_time=2.0,rate_func=linear)
        self.narrate(
            "Vì thể tích biến theo lập phương tỷ số đồng dạng, thể tích phần trên bằng u mũ ba nhân V. Phần dưới bằng một trừ u mũ ba nhân V. Nếu cần làm lớn nhất tích hai thể tích, ta không nên đạo hàm biểu thức chứa u mũ ba ngay. Hãy đặt y bằng u mũ ba; khi M chạy từ S đến O thì y chạy từ không đến một.",
            2.0,
        )
        u_star=(0.5)**(1/3)
        self.play(u.animate.set_value(u_star),run_time=2.1,rate_func=smooth)
        self.narrate(
            "Tích sau khi chuẩn hóa chỉ còn y nhân một trừ y. Ta có y nhân một trừ y không vượt quá một phần tư, dấu bằng khi y bằng một phần hai. Vì vậy u bằng căn bậc ba của một phần hai. Điều đáng chú ý là tại cực trị, hai thể tích bằng nhau, nhưng mặt cắt không nằm ở trung điểm chiều cao; nó nằm gần đáy hơn vì thể tích thay đổi theo lập phương.",
            2.0,
        )
        self.takeaway("Chuẩn hóa theo tỷ số trước: cực trị thường lộ ra cấu trúc đơn giản hơn.")

    # ======================================================
    # 7. SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ cực trị HHKG","Chọn đúng đại lượng để tối ưu","7/7")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Bất biến",20,INK),txt("→ dừng trước khi lập hàm",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Khoảng cách",20,INK),txt("→ tối ưu bình phương / hình chiếu",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Góc",20,INK),txt("→ sin, cos, tan đơn điệu",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Đường đi",20,INK),txt("→ trải phẳng mặt đa diện",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Thể tích",20,INK),txt("→ chuẩn hóa tỷ số trước",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.28).shift(LEFT*2.72+UP*0.18)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Năm kết quả","Một video — năm kiểu cực trị",[
            ("math","d(M,(S B C)) = frac(12, 5)",27,GOLD),
            ("math","C H = sqrt(3)",29,GOLD),
            ("math","tan alpha = frac(3, 2)",29,GOLD),
            ("math","A M + M C' >= a sqrt(5)",27,GOLD),
            ("math","V_1 V_2 <= frac(V^2, 4)",28,GOLD),
            ("sep",),
            ("text","Hình học tốt thường làm hàm số ngắn đi.",16,MUTED,NORMAL),
        ],accent=GREEN)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.8)
        self.narrate(
            "Năm bài của video cho năm chiến lược khác nhau. Một điểm chạy nhưng khoảng cách có thể bất biến. Một khoảng cách không gian có thể tách thành một thành phần cố định và một khoảng cách phẳng. Một góc có thể tối ưu qua tang. Một tổng độ dài trên đa diện có thể trải phẳng. Và một bài thể tích có thể chuẩn hóa thành y nhân một trừ y.",
            2.0,
        )
        self.narrate(
            "Điểm chung là không có một công thức cực trị duy nhất cho hình học không gian. Chất lượng lời giải nằm ở bước chọn mô hình trước khi tính. Nếu hình học đã cho một phép chiếu, một đối xứng, một mặt phẳng song song hay một phép trải phẳng, hãy khai thác chúng trước. Đạo hàm chỉ nên xuất hiện sau khi biểu thức đã được rút về dạng thực sự cần thiết.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 16",17,BLUE,BOLD),
            txt("OXYZ NHƯ NGÔN NGỮ THỨ HAI",25,GOLD,BOLD),
            txt("Tọa độ hóa đúng lúc · vector pháp tuyến · khoảng cách · góc · kiểm chứng hình học",18,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box)
        self.play(FadeIn(next_box),run_time=0.55)
        self.narrate(
            "Video mười sáu sẽ đưa Oxyz vào như một ngôn ngữ thứ hai, không phải để thay hình học thuần túy. Ta sẽ học cách đặt hệ trục sao cho tọa độ ngắn, khi nào vector pháp tuyến giúp giải nhanh, khi nào tích vô hướng thay cho một chứng minh vuông góc, và quan trọng nhất là cách dùng tọa độ để kiểm chứng một cấu hình khó mà vẫn giữ được ý tưởng hình học.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.invariant_trap()
        self.min_distance()
        self.max_angle()
        self.cube_unfolding()
        self.volume_product()
        self.synthesis()


# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_15_diem_dong_cuc_tri_HHKG_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 15")
    print("Dynamic themes: invariant, minimum distance, maximum angle, unfolding, volume product")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_15.wav"
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

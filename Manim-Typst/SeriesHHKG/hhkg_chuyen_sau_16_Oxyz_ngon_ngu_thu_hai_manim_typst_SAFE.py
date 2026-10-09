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


# ==========================================================
# HHKG 16 - OXYZ HELPERS
# ==========================================================
def phys(x, y, z):
    """Map physical Oxyz coordinates to the current 3D drawing frame."""
    return L(x, y, z)

def foot_to_plane_physical(p, n, c):
    """Foot of physical point p to plane n.x + c = 0."""
    p = np.array(p, dtype=float)
    n = np.array(n, dtype=float)
    f = float(np.dot(n, p) + c)
    return p - (f / float(np.dot(n, n))) * n


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
        series = txt("HHKG CHUYÊN SÂU · 16", 15, BLUE, BOLD)
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

    # ---------- geometry ----------
    def pyramid_xyz(self):
        A=phys(0,0,0); B=phys(4,0,0); C=phys(4,4,0); D=phys(0,4,0); S=phys(0,0,3)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.055)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def cube_xyz(self, a=3.0):
        A=phys(0,0,0); B=phys(a,0,0); C=phys(a,a,0); D=phys(0,a,0)
        A1=phys(0,0,a); B1=phys(a,0,a); C1=phys(a,a,a); D1=phys(0,a,a)
        visible=VGroup(solid(A,B),solid(B,C),solid(A,A1),solid(B,B1),solid(C,C1),
                       solid(A1,B1),solid(B1,C1),solid(C1,D1),solid(A1,D1))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(D,D1))
        faces=VGroup(face(A,B,B1,A1,color=BLUE,opacity=0.035),
                     face(B,C,C1,B1,color=PURPLE,opacity=0.030))
        dots=VGroup(*[Dot3D(p,radius=0.043,color=GOLD) for p in [A,B,C,D,A1,B1,C1,D1]])
        return {"A":A,"B":B,"C":C,"D":D,"A1":A1,"B1":B1,"C1":C1,"D1":D1,
                "edges":VGroup(visible,hidden),"faces":faces,"dots":dots,"a":a}

    def draw_axes_at_A(self, A):
        ex=solid(A, A+np.array([1.2,0,0]), RED, 4.2, 1.0)
        ey=solid(A, A+np.array([0,1.2,0]), GREEN, 4.2, 1.0)
        ez=solid(A, A+np.array([0,0,1.2]), BLUE, 4.2, 1.0)
        self.add(ex,ey,ez)
        self.add_label("x", ex.get_end(), RED, (0.08,0,0), 18)
        self.add_label("y", ey.get_end(), GREEN, (0,0.08,0), 18)
        self.add_label("z", ez.get_end(), BLUE, (0,0,0.08), 18)
        return VGroup(ex,ey,ez)

    # ======================================================
    # 1. INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Oxyz như ngôn ngữ thứ hai",
                        "Đặt trục để rút ngắn lời giải, không thay thế tư duy hình học",
                        "1/7")
        left=VGroup(
            txt("1",17,GOLD,BOLD),txt("Gốc tại điểm có nhiều vuông góc",21,INK,BOLD),
            txt("2",17,GOLD,BOLD),txt("Trục theo cạnh / đường cao tự nhiên",21,INK,BOLD),
            txt("3",17,GOLD,BOLD),txt("Chỉ viết phương trình cần thiết",21,INK,BOLD),
            txt("4",17,GOLD,BOLD),txt("Kiểm chứng lại bằng hình học",21,INK,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.18).shift(LEFT*2.72+UP*0.12)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Nguyên tắc","Tọa độ tốt phải làm bài ngắn đi",[
            ("math","A=(0,0,0)",28,CYAN),
            ("math","B=(4,0,0)",28,INK),
            ("math","D=(0,4,0)",28,INK),
            ("math","S=(0,0,3)",28,GOLD),
            ("sep",),
            ("text","Một hệ trục tốt thường biến dữ kiện vuông góc thành số 0.",16,MUTED,NORMAL),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.8)
        self.narrate(
            "Oxyz không nên được dùng như một chiếc búa cho mọi bài hình học không gian. Nếu đặt hệ trục xấu, ta có thể biến một lời giải hình học ba dòng thành một trang đại số. Nhưng nếu đặt đúng gốc và đúng hướng trục, những quan hệ vuông góc, song song và đối xứng sẽ biến thành các tọa độ bằng không; khi ấy phương trình mặt phẳng, khoảng cách và góc có thể xuất hiện rất tự nhiên.",
            2.0,
        )
        self.narrate(
            "Trong video này ta sẽ dùng cùng một nguyên tắc: tọa độ phải phục vụ cấu trúc hình. Ta bắt đầu bằng một hình chóp vuông để thấy vì sao nên đặt gốc tại chân đường cao; sau đó dùng tích có hướng cho hai đường chéo nhau, dùng pháp tuyến cho góc giữa hai mặt, và kết thúc bằng một bài điểm động nơi phương trình khoảng cách tuyến tính hơn rất nhiều so với cách dựng hình trực tiếp.",
            2.0,
        )

    # ======================================================
    # 2. COORDINATE PLACEMENT + POINT-PLANE DISTANCE
    # ======================================================
    def point_plane_distance(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Đặt trục đúng","Hình chóp vuông: khoảng cách D đến (SBC)","2/7")
        G=self.pyramid_xyz()
        self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.14,-0.12,0),18),("B",G["B"],GOLD,(0.12,-0.12,0),18),
            ("C",G["C"],GOLD,(0.12,0.10,0),18),("D",G["D"],GOLD,(-0.16,0.10,0),18),
            ("S",G["S"],RED,(-0.12,-0.06,0.13),19),
        ])
        self.draw_axes_at_A(G["A"])
        plane=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.18,stroke=PURPLE,stroke_width=2.2)
        self.add(plane)

        card1 = self.card("Chọn hệ trục","Gốc A, ba trục theo AB, AD, AS",[
            ("math","A=(0,0,0)",27,CYAN),
            ("math","B=(4,0,0)",27,INK),
            ("math","C=(4,4,0)",27,INK),
            ("math","D=(0,4,0)",27,INK),
            ("math","S=(0,0,3)",27,GOLD),
            ("sep",),
            ("math","(S B C): 3x+4z-12=0",28,GREEN),
        ],accent=PURPLE)
        self.narrate(
            "Ta xét lại hình chóp S.ABCD có đáy là hình vuông cạnh bốn, SA bằng ba và vuông góc đáy. Đây là cấu hình lý tưởng cho tọa độ: đặt A làm gốc, trục x theo AB, trục y theo AD và trục z theo AS. Mọi tọa độ đều rất ngắn; đặc biệt đáy có z bằng không, còn đường cao SA nằm ngay trên trục z.",
            2.0,
        )
        self.narrate(
            "Mặt phẳng SBC đi qua ba điểm S, B, C. Từ hai vectơ nằm trong mặt, ta có thể tìm một vectơ pháp tuyến tỷ lệ với bộ ba ba, không, bốn. Vì vậy phương trình mặt phẳng là ba x cộng bốn z trừ mười hai bằng không. Điểm đáng chú ý là biến y biến mất; điều đó phản ánh đúng hình học rằng mặt SBC song song với phương AD.",
            2.0,
        )

        Dp=np.array([0.,4.,0.]); n=np.array([3.,0.,4.])
        Hp=foot_to_plane_physical(Dp,n,-12.0)
        H=phys(*Hp)
        dh=solid(G["D"],H,GOLD,6.0,1.0)
        hdot=Dot3D(H,radius=0.055,color=GOLD)
        self.add(dh,hdot)
        self.add_label("H",H,GOLD,(0.08,0.07,0.04),17)
        normal_dir=n/np.linalg.norm(n)
        nline=solid(G["B"],G["B"]+0.95*normal_dir,GREEN,4.5,1.0)
        self.add(nline)

        self.play(FadeOut(card1), run_time=0.35)
        self.remove(card1)
        self.card("Khoảng cách","Công thức điểm – mặt phẳng",[
            ("math","n=(3,0,4)",28,GREEN),
            ("math","sqrt(3^2+4^2)=5",28,INK),
            ("math","d(D,(S B C)) = frac(12,5)",34,GOLD),
            ("math","H=(frac(36,25),4,frac(48,25))",25,CYAN),
        ],accent=GOLD)
        self.narrate(
            "Khoảng cách từ D đến mặt SBC giờ chỉ còn là khoảng cách từ điểm đến mặt phẳng. Thay tọa độ D vào vế trái, ta được độ lệch tuyệt đối bằng mười hai; độ dài pháp tuyến là năm. Suy ra khoảng cách bằng mười hai phần năm. Nếu cần chân đường vuông góc, công thức chiếu theo pháp tuyến còn cho H có tọa độ ba mươi sáu phần hai mươi lăm, bốn, bốn mươi tám phần hai mươi lăm.",
            2.0,
        )
        self.narrate(
            "Có một phép kiểm tra rất đáng làm. Vì phương trình mặt SBC không chứa y, nếu ta tịnh tiến một điểm theo phương AD thì giá trị ba x cộng bốn z trừ mười hai không đổi. Điều đó giải thích ngay vì sao mọi điểm trên AD có cùng khoảng cách tới mặt SBC, đúng với tính chất song song đã gặp ở Video hai và Video mười lăm. Một phương trình tọa độ tốt không chỉ cho con số; nó còn phải phản ánh được một quan hệ hình học đã biết.",
            1.8,
        )
        self.takeaway("Tọa độ tốt biến dựng chân vuông góc khó thành một phép chiếu theo pháp tuyến.")

    # ======================================================
    # 3. LINE-PLANE ANGLE: GEOMETRY AND COORDINATES AGREE
    # ======================================================
    def line_plane_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 2 · Góc đường – mặt","Hai ngôn ngữ cho cùng một góc","3/7")
        G=self.pyramid_xyz()
        self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.14,-0.12,0),18),("C",G["C"],GOLD,(0.12,0.10,0),18),
            ("S",G["S"],RED,(-0.12,-0.06,0.13),19),
        ])
        sc=solid(G["S"],G["C"],GOLD,6.0,1.0)
        ac=aux(G["A"],G["C"],CYAN,4.3,0.95)
        self.add(sc,ac)
        arc=angle_arc_3d(G["C"],G["S"]-G["C"],G["A"]-G["C"],radius=0.40,color=GOLD,width=5.5)
        self.add(arc)
        al=mty("alpha",20,GOLD).move_to(G["C"]+0.42*((G["S"]-G["C"])/np.linalg.norm(G["S"]-G["C"])+(G["A"]-G["C"])/np.linalg.norm(G["A"]-G["C"])))
        self.add_fixed_orientation_mobjects(al)

        self.card("Hình học + Oxyz","Hình chiếu vẫn là AC",[
            ("math","alpha = hat(S C A, size: #155%)",27,GOLD),
            ("math","u=(4,4,-3)",27,CYAN),
            ("math","n_0=(0,0,1)",27,GREEN),
            ("math","sin alpha = frac(3, sqrt(41))",29,INK),
            ("math","tan alpha = frac(3, 4 sqrt(2))",30,GOLD),
        ],accent=CYAN)
        self.narrate(
            "Bây giờ xét góc giữa SC và mặt đáy. Trên hình, ký hiệu góc phải được đặt đúng tại C giữa hai tia CS và CA, vì AC là hình chiếu vuông góc của SC xuống đáy. Vì vậy góc phẳng đại diện là góc SCA. Cung vàng trên hình được dựng từ chính hai tia này trong không gian, không phải một cung trang trí theo màn hình.",
            2.0,
        )
        self.narrate(
            "Trong Oxyz, vectơ chỉ phương của SC có thể lấy là bốn, bốn, âm ba; pháp tuyến của đáy là không, không, một. Thành phần theo pháp tuyến có độ lớn ba, còn độ dài vectơ SC là căn bốn mươi mốt. Vì vậy sin alpha bằng ba trên căn bốn mươi mốt. Nếu quay về tam giác SAC, ta lại có tang alpha bằng ba trên bốn căn hai. Hai ngôn ngữ cho cùng một góc và có thể dùng để kiểm tra lẫn nhau.",
            2.0,
        )
        self.takeaway("Tọa độ không thay thế hình chiếu: nó chỉ mã hóa hình chiếu bằng vectơ và pháp tuyến.")

    # ======================================================
    # 4. DISTANCE BETWEEN SKEW LINES
    # ======================================================
    def skew_lines(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES,theta=-49*DEGREES,zoom=0.98)
        self.add_header("Bài 3 · Hai đường chéo nhau","Khoảng cách AC' và BD trong hình lập phương","4/7")
        G=self.cube_xyz(3.0)
        self.add(G["faces"],G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.13,-0.12,0),17),("B",G["B"],GOLD,(0.12,-0.12,0),17),
            ("C",G["C"],GOLD,(0.12,0.10,0),17),("D",G["D"],GOLD,(-0.14,0.10,0),17),
            ("C'",G["C1"],RED,(0.12,0.10,0.08),17),
        ])
        line1=solid(G["A"],G["C1"],GOLD,6.0,1.0)
        line2=solid(G["B"],G["D"],CYAN,6.0,1.0)
        self.add(line1,line2)

        a=3.0
        Pp=np.array([a/3,a/3,a/3]); Qp=np.array([a/2,a/2,0])
        P=phys(*Pp); Q=phys(*Qp)
        pq=solid(P,Q,GREEN,6.0,1.0)
        self.add(pq,Dot3D(P,radius=0.052,color=GREEN),Dot3D(Q,radius=0.052,color=GREEN))
        self.add_label("P",P,GREEN,(-0.12,0.06,0.06),17)
        self.add_label("Q",Q,GREEN,(0.08,-0.06,0.04),17)

        self.card("Tích có hướng","Một pháp tuyến chung cho hai hướng",[
            ("math","u=(1,1,1)",27,GOLD),
            ("math","v=(-1,1,0)",27,CYAN),
            ("math","n=u times v=(-1,-1,2)",27,GREEN),
            ("math","P=(frac(a,3),frac(a,3),frac(a,3))",23,INK),
            ("math","Q=(frac(a,2),frac(a,2),0)",23,INK),
            ("math","d(A C',B D)=frac(a, sqrt(6))",29,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Trong hình lập phương cạnh a, xét hai đường AC phẩy và BD. Chúng không cắt nhau và cũng không song song. Nếu giải thuần hình học, việc dựng đường vuông góc chung không quá hiển nhiên. Oxyz lại rất hợp với bài này: đặt A tại gốc, các cạnh của lập phương theo ba trục, rồi lấy vectơ chỉ phương u của AC phẩy là một, một, một và v của BD là âm một, một, không.",
            2.0,
        )
        self.narrate(
            "Tích có hướng u nhân v cho vectơ n bằng âm một, âm một, hai. Vectơ này vuông góc với cả hai đường. Từ công thức khoảng cách giữa hai đường chéo nhau, hoặc giải hệ điều kiện vuông góc, ta được hai chân P và Q. P chia đường AC phẩy theo tỷ số một phần ba, còn Q là trung điểm BD. Đoạn PQ chính là đường vuông góc chung.",
            2.0,
        )
        self.narrate(
            "Độ dài PQ bằng a trên căn sáu. Kết quả này cho thấy tọa độ mạnh ở chỗ nào: nó không bắt ta đoán trước vị trí đường vuông góc chung. Nhưng sau khi tìm ra P và Q, ta vẫn nên quay lại hình để hiểu rằng PQ thật sự vuông góc với cả AC phẩy lẫn BD. Đại số tìm điểm; hình học xác nhận cấu trúc.",
            2.0,
        )

    # ======================================================
    # 5. ANGLE BETWEEN PLANES VIA NORMALS
    # ======================================================
    def plane_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=67*DEGREES,theta=-50*DEGREES,zoom=0.98)
        self.add_header("Bài 4 · Góc giữa hai mặt","Mặt chéo (ACD') và mặt đáy","5/7")
        G=self.cube_xyz(3.0)
        self.add(G["faces"],G["edges"],G["dots"])
        A,C,D,D1=G["A"],G["C"],G["D"],G["D1"]
        plane=face(A,C,D1,color=PURPLE,opacity=0.19,stroke=PURPLE,stroke_width=2.4)
        self.add(plane)
        O=(A+C)/2
        self.add(Dot3D(O,radius=0.05,color=GREEN))
        self.add_label("O",O,GREEN,(0.05,-0.08,0.03),17)
        self.label_many([
            ("A",A,GOLD,(-0.13,-0.12,0),17),("C",C,GOLD,(0.12,0.10,0),17),
            ("D",D,GOLD,(-0.14,0.10,0),17),("D'",D1,RED,(-0.14,0.10,0.08),17),
        ])
        od=solid(O,D,CYAN,5.2,1.0); od1=solid(O,D1,GOLD,5.2,1.0)
        self.add(od,od1)
        arc=angle_arc_3d(O,D-O,D1-O,radius=0.36,color=GOLD,width=5.4)
        self.add(arc)
        beta=mty("beta",19,GOLD).move_to(O+0.38*((D-O)/np.linalg.norm(D-O)+(D1-O)/np.linalg.norm(D1-O)))
        self.add_fixed_orientation_mobjects(beta)

        self.card("Pháp tuyến","Góc trên hình là DOD'",[
            ("math","(A C D') inter (A B C D)=A C",24,CYAN),
            ("math","beta = hat(D O D', size: #155%)",26,GOLD),
            ("math","n_0=(0,0,1)",26,GREEN),
            ("math","n_1=(1,-1,1)",26,PURPLE),
            ("math","cos beta = frac(1, sqrt(3))",29,INK),
            ("math","tan beta = sqrt(2)",31,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Xét mặt chéo ACD phẩy và mặt đáy. Giao tuyến của chúng là AC. Trên hình, O là trung điểm AC. Trong đáy, OD vuông góc AC; trong tam giác cân AD phẩy C, OD phẩy cũng vuông góc AC. Vì vậy góc giữa hai mặt chính là góc DOD phẩy, và cung góc được đặt đúng tại O giữa hai tia OD và OD phẩy.",
            2.0,
        )
        self.narrate(
            "Tọa độ cho một lời giải rất ngắn. Pháp tuyến của đáy là không, không, một. Từ hai vectơ AC và AD phẩy, ta có thể lấy pháp tuyến của mặt ACD phẩy là một, âm một, một. Góc nhọn giữa hai pháp tuyến có cos bằng một trên căn ba; đó cũng là góc nhọn giữa hai mặt. Từ đây suy ra tang beta bằng căn hai, đúng với lời giải mặt cắt vuông góc ở các video trước.",
            2.0,
        )
        self.takeaway("Góc hai mặt: hình học chọn đúng góc phẳng; Oxyz kiểm tra nhanh bằng hai pháp tuyến.")

    # ======================================================
    # 6. MOVING POINT: EQUAL DISTANCES TO TWO PLANES
    # ======================================================
    def moving_point(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 5 · Điểm động","M trên SA và cách đều hai mặt phẳng","6/7")
        G=self.pyramid_xyz()
        self.add(G["base"],G["edges"],G["dots"])
        plane=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.13,stroke=PURPLE,stroke_width=2.1)
        self.add(plane)
        self.label_many([
            ("A",G["A"],GOLD,(-0.14,-0.12,0),18),("S",G["S"],RED,(-0.12,-0.06,0.13),19),
            ("B",G["B"],GOLD,(0.12,-0.12,0),17),("C",G["C"],GOLD,(0.12,0.10,0),17),
        ])
        t=ValueTracker(0.35)
        M=always_redraw(lambda: Dot3D(phys(0,0,t.get_value()),radius=0.058,color=GOLD))
        d_base=always_redraw(lambda: solid(phys(0,0,0),phys(0,0,t.get_value()),CYAN,5.0,0.95))
        def foot_side():
            mp=np.array([0.,0.,t.get_value()])
            hp=foot_to_plane_physical(mp,np.array([3.,0.,4.]),-12.0)
            return phys(*hp)
        d_side=always_redraw(lambda: solid(phys(0,0,t.get_value()),foot_side(),GREEN,5.0,0.95))
        H=always_redraw(lambda: Dot3D(foot_side(),radius=0.048,color=GREEN))
        self.add(M,d_base,d_side,H)

        self.card("Tham số","Đặt M=(0,0,t), 0 <= t <= 3",[
            ("math","d(M,(A B C D))=t",27,CYAN),
            ("math","d(M,(S B C))=frac(12-4t,5)",27,GREEN),
            ("math","t=frac(12-4t,5)",29,INK),
            ("math","9t=12",29,INK),
            ("math","t=frac(4,3)",34,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Bài cuối cùng cho M chạy trên SA và yêu cầu tìm vị trí để M cách đều mặt đáy và mặt SBC. Nếu dựng hai chân vuông góc trực tiếp, hình khá rối. Trong hệ trục hiện tại, M có tọa độ không, không, t với t chạy từ không đến ba. Khoảng cách từ M đến đáy z bằng không chính là t.",
            2.0,
        )
        self.play(t.animate.set_value(2.75),run_time=3.0,rate_func=linear)
        self.play(t.animate.set_value(0.75),run_time=2.0,rate_func=linear)
        self.narrate(
            "Khoảng cách từ M tới mặt SBC có phương trình ba x cộng bốn z trừ mười hai bằng không, nên bằng mười hai trừ bốn t, tất cả chia năm. Một khoảng cách tăng tuyến tính, khoảng cách kia giảm tuyến tính. Điều kiện cách đều vì thế chỉ còn một phương trình bậc nhất: t bằng mười hai trừ bốn t chia năm.",
            2.0,
        )
        self.play(t.animate.set_value(4/3),run_time=2.0,rate_func=smooth)
        self.narrate(
            "Giải ra chín t bằng mười hai, tức t bằng bốn phần ba. Đây là ví dụ điển hình cho lúc Oxyz thực sự đáng dùng: bài toán động ba chiều biến thành hai hàm khoảng cách tuyến tính. Sau khi có kết quả, ta vẫn nhìn lại hình để thấy M nằm gần A hơn trung điểm SA, hoàn toàn phù hợp vì mặt SBC nghiêng về phía M.",
            2.0,
        )
        self.narrate(
            "Một chi tiết kỹ thuật cần nhớ là công thức khoảng cách luôn có giá trị tuyệt đối. Ở bài này ta được phép bỏ dấu tuyệt đối vì đã khóa miền không nhỏ hơn không và không lớn hơn ba, nên bốn t trừ mười hai không dương trên cả đoạn SA. Nếu điểm M chạy vượt qua S hoặc chạy trên một đường khác, biểu thức khoảng cách có thể phải tách miền. Kiểm tra miền tham số trước khi bỏ dấu tuyệt đối là một thói quen rất quan trọng trong các bài Oxyz có điểm động.",
            1.8,
        )

    # ======================================================
    # 7. SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ Oxyz trong HHKG","Khi nào tọa độ thật sự đáng dùng?","7/7")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Đặt trục",20,INK),txt("→ theo vuông góc và đối xứng",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Mặt phẳng",20,INK),txt("→ pháp tuyến ngắn",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Hai đường chéo",20,INK),txt("→ tích có hướng",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Góc hai mặt",20,INK),txt("→ hai pháp tuyến + góc phẳng",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Điểm động",20,INK),txt("→ tọa độ tham số",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.28).shift(LEFT*2.70+UP*0.18)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Năm kết quả","Một hệ trục tốt — năm lời giải ngắn",[
            ("math","d(D,(S B C))=frac(12,5)",27,GOLD),
            ("math","sin alpha = frac(3,sqrt(41))",27,GOLD),
            ("math","d(A C',B D)=frac(a,sqrt(6))",26,GOLD),
            ("math","tan beta=sqrt(2)",28,GOLD),
            ("math","t=frac(4,3)",30,GOLD),
            ("sep",),
            ("text","Nếu tọa độ làm biểu thức dài hơn hình học, hãy quay lại hình.",16,MUTED,NORMAL),
        ],accent=GREEN)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.8)
        self.narrate(
            "Năm bài cho thấy Oxyz mạnh nhất khi nó tôn trọng cấu trúc của hình. Đặt gốc tại chân đường cao giúp phương trình mặt phẳng ngắn. Pháp tuyến biến khoảng cách điểm tới mặt thành một phép thế số. Tích có hướng tìm được đường vuông góc chung của hai đường chéo nhau. Hai pháp tuyến kiểm tra góc giữa hai mặt, còn tọa độ tham số biến bài điểm động thành phương trình một ẩn.",
            2.0,
        )
        self.narrate(
            "Nhưng tọa độ chỉ là ngôn ngữ thứ hai. Trên hình, góc đường với mặt vẫn phải gắn với hình chiếu thật; góc hai mặt vẫn phải có cạnh chung và góc phẳng đúng; đường vuông góc chung vẫn phải được hiểu sau khi tìm ra bằng đại số. Một lời giải tốt thường đi hai chiều: hình học chọn mô hình, tọa độ tính nhanh, rồi hình học kiểm chứng ý nghĩa của kết quả.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 17",17,BLUE,BOLD),
            txt("ĐÚNG/SAI HHKG · PHÂN HÓA CAO",24,GOLD,BOLD),
            txt("Nhận diện mệnh đề · phản ví dụ · kiểm chứng bằng hình học và Oxyz",18,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box)
        self.play(FadeIn(next_box),run_time=0.55)
        self.narrate(
            "Video mười bảy sẽ chuyển sang dạng Đúng Sai phân hóa cao. Ta sẽ luyện cách kiểm tra từng mệnh đề bằng đúng công cụ vừa xây dựng trong cả series: hình chiếu, khoảng cách, góc, thể tích, thiết diện và khi cần thì dùng Oxyz như một cách kiểm chứng nhanh. Mục tiêu là nhận ra mệnh đề sai bằng cấu trúc hoặc phản ví dụ, thay vì lao vào tính toàn bộ bài.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.point_plane_distance()
        self.line_plane_angle()
        self.skew_lines()
        self.plane_angle()
        self.moving_point()
        self.synthesis()


def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_16_Oxyz_ngon_ngu_thu_hai_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 16")
    print("Themes: coordinate placement, point-plane distance, line-plane angle, skew lines, plane angle, moving point")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_16.wav"
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

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
# HHKG CHUYEN SAU 19 - CAU HINH LA, LOI GIAI DEP
# Manim Community + MathTypst SAFE | Standalone 100%
# Muc tieu: 12-15 phut; 5 cau hinh la, loi giai ngan nhung du chung minh va kiem tra hinh hoc.
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
# GENERAL DYNAMIC GEOMETRY HELPERS
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
# OXYZ / METRIC HELPERS
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




# ==========================================================
# LIGHTWEIGHT SOLIDS OF REVOLUTION FOR SHORT-ANSWER PROBLEMS
# ==========================================================
def low_surface(func, u_range, v_range, color=BLUE, opacity=0.08, resolution=(10, 24)):
    surf = Surface(func, u_range=u_range, v_range=v_range, resolution=resolution)
    surf.set_fill(color, opacity=opacity)
    surf.set_stroke(color, width=0.35, opacity=0.18)
    return surf


def sphere_surface(center, radius, color=BLUE, opacity=0.065):
    c = np.array(center, dtype=float)
    return low_surface(
        lambda u, v: c + radius*np.array([math.sin(u)*math.cos(v), math.sin(u)*math.sin(v), math.cos(u)]),
        [0, PI], [0, TAU], color=color, opacity=opacity, resolution=(12, 24)
    )


def cylinder_surface(center, radius, height, color=CYAN, opacity=0.09):
    c = np.array(center, dtype=float)
    return low_surface(
        lambda u, v: c + np.array([radius*math.cos(v), radius*math.sin(v), (u-0.5)*height]),
        [0, 1], [0, TAU], color=color, opacity=opacity, resolution=(5, 24)
    )


def horizontal_rim(center, radius, color=EDGE, width=3.0, hidden_color=DIM):
    c = np.array(center, dtype=float)
    th = VIEW_THETA
    front = ParametricFunction(
        lambda t: c + radius*np.array([math.cos(t), math.sin(t), 0.0]),
        t_range=[th-PI/2, th+PI/2], color=color, stroke_width=width,
    )
    back_curve = ParametricFunction(
        lambda t: c + radius*np.array([math.cos(t), math.sin(t), 0.0]),
        t_range=[th+PI/2, th+3*PI/2], color=hidden_color, stroke_width=max(2.0, width-0.6),
    )
    back = DashedVMobject(back_curve, num_dashes=16, dashed_ratio=0.52)
    back.set_opacity(0.72)
    return VGroup(front, back)


def meridian_circle(center, radius, color=BLUE, width=2.0, opacity=0.58):
    c = np.array(center, dtype=float)
    curve = ParametricFunction(
        lambda t: c + radius*np.array([math.cos(t), 0.0, math.sin(t)]),
        t_range=[0, TAU], color=color, stroke_width=width,
    )
    curve.set_opacity(opacity)
    return curve


def project_point_to_plane(p, a, b, c):
    n = plane_normal(a, b, c)
    return p - float(np.dot(p-a, n))*n


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
        series = txt("HHKG CHUYÊN SÂU · 19", 15, BLUE, BOLD)
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

    def fade_card(self, group):
        self.play(FadeOut(group), run_time=0.26)

    # ---------- geometry constructors ----------
    def rectangular_pyramid(self, a=6, b=8, h=12, scale=0.32):
        P = lambda x,y,z: L(scale*x, scale*y, scale*z)
        A=P(0,0,0); B=P(a,0,0); C=P(a,b,0); D=P(0,b,0); S=P(0,0,h)
        base=face(A,B,C,D,color=BLUE,opacity=0.055)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"base":base,"edges":VGroup(visible,hidden),"dots":dots}

    def square_pyramid(self, a=6, h=8, scale=0.38):
        P = lambda x,y,z: L(scale*x, scale*y, scale*z)
        A=P(0,0,0); B=P(a,0,0); C=P(a,a,0); D=P(0,a,0); S=P(0,0,h)
        base=face(A,B,C,D,color=BLUE,opacity=0.055)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"base":base,"edges":VGroup(visible,hidden),"dots":dots,
                "scale":scale}

    def regular_tetra(self):
        P = regular_tetra_raw(scale=1.40)
        A,B,C,D=P["A"],P["B"],P["C"],P["D"]
        edges=VGroup(solid(A,B),solid(A,C),solid(A,D),solid(B,C),hidden_edge(B,D),hidden_edge(C,D))
        dots=VGroup(*[Dot3D(P[k],radius=0.052,color=GOLD) for k in ["A","B","C","D"]])
        return {**P,"edges":edges,"dots":dots}

    def normalized_cube(self, side_display=3.10):
        P = cube_unit_vertices(side_display)
        visible=VGroup(
            solid(P["A"],P["B"]), solid(P["B"],P["C"]), solid(P["A"],P["A1"]),
            solid(P["B"],P["B1"]), solid(P["C"],P["C1"]), solid(P["A1"],P["B1"]),
            solid(P["B1"],P["C1"]), solid(P["C1"],P["D1"]), solid(P["A1"],P["D1"])
        )
        hidden=VGroup(hidden_edge(P["C"],P["D"]),hidden_edge(P["D"],P["A"]),hidden_edge(P["D"],P["D1"]))
        dots=VGroup(*[Dot3D(P[k],radius=0.045,color=GOLD) for k in ["A","B","C","D","A1","B1","C1","D1"]])
        return {**P,"edges":VGroup(visible,hidden),"dots":dots}


    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_header("Cấu hình lạ · lời giải đẹp", "Ít tính hơn — nhìn cấu trúc sâu hơn", "1/7")
        left = VGroup(
            VGroup(txt("1",18,GOLD,BOLD), txt("Tìm khối quen thuộc đang ẩn trong hình",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD), txt("Ưu tiên trung điểm, tâm, đối xứng và thể tích",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD), txt("Đường phụ phải có nhiệm vụ hình học rõ ràng",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD), txt("Sau một phát hiện đúng, lời giải phải ngắn đi",20,INK)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).shift(LEFT*2.72+UP*0.12)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Tinh thần", "Không dùng kỹ thuật chỉ để làm bài dài hơn", [
            ("math", "perp, parallel, inter", 27, CYAN),
            ("math", "S, V, d, rho", 27, INK),
            ("sep",),
            ("text", "Mỗi bài chỉ giữ lại một phát hiện quyết định.",16,MUTED,NORMAL),
            ("text", "Nếu đường phụ không làm xuất hiện cấu trúc mới, bỏ nó.",16,MUTED,NORMAL),
        ], accent=GOLD)
        self.play(FadeIn(left, shift=RIGHT*0.10), run_time=0.70)
        self.narrate(
            "Video mười chín không cố gom thêm thật nhiều dạng. Thầy chọn năm cấu hình mà khi nhìn lần đầu rất dễ sa vào tọa độ dài hoặc dựng phụ lan man. Mục tiêu là tìm đúng cấu trúc ẩn: một tứ diện đều nằm trong lập phương, một bát diện đều tạo bởi tâm các mặt, một tứ diện vuông ba chiều, một bất biến thể tích và một mặt cầu tiếp xúc sáu cạnh.",
            2.0,
        )
        self.narrate(
            "Tiêu chuẩn của một lời giải đẹp trong video này rất nghiêm. Sau khi phát hiện đúng ý, số dòng tính toán phải giảm rõ rệt; hình phụ phải giải thích được vì sao nó xuất hiện; và kết quả phải kiểm tra được bằng đối xứng, thể tích hoặc một quan hệ vuông góc. Ta không dùng kỹ thuật khó chỉ để làm bài trông cao cấp hơn.",
            1.9,
        )

    # ======================================================
    # Q1. HIDDEN REGULAR TETRAHEDRON IN A CUBE
    # ======================================================
    def q1_hidden_regular_tetra(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Tứ diện đều ẩn trong lập phương", "Bốn đỉnh so le tạo một khối chuẩn", "2/7")
        G = self.normalized_cube(side_display=3.05)
        self.add(G["edges"], G["dots"])
        B,D,A1,C1 = G["B"],G["D"],G["A1"],G["C1"]
        tetra_edges = VGroup(
            solid(B,D,CYAN,4.6), solid(B,A1,CYAN,4.6), solid(D,A1,CYAN,4.6),
            solid(C1,B,GOLD,4.8), solid(C1,D,GOLD,4.8), solid(C1,A1,GOLD,4.8),
        )
        base = face(B,D,A1,color=PURPLE,opacity=0.15)
        self.play(FadeIn(base), Create(tetra_edges), run_time=0.9)
        for name,pt,off in [
            ("B",B,(-0.12,-0.12,0)),("D",D,(-0.16,0.06,0.02)),("A'",A1,(-0.16,0.10,0.05)),("C'",C1,(0.10,0.10,0.06))
        ]:
            self.add_label(name,pt,GOLD,off,19)
        q = self.card("Quan sát", "Lập phương cạnh a", [
            ("text", "Chứng minh BDA'C' là tứ diện đều.",16,MUTED,NORMAL),
            ("text", "Từ đó tính d(C', (BDA')).",16,MUTED,NORMAL),
        ], accent=PURPLE)
        self.narrate(
            "Trong lập phương cạnh a, chọn bốn đỉnh so le B, D, A phẩy và C phẩy. Nếu nhìn chúng như bốn điểm rời rạc, bài khá khó chịu. Nhưng hãy kiểm tra đúng một độ dài. Mỗi đoạn nối hai đỉnh trong bốn điểm này đều là đường chéo của một mặt vuông, vì vậy tất cả sáu cạnh đều bằng a căn hai. Tức là bên trong lập phương đang ẩn một tứ diện đều.",
            2.0,
        )
        self.narrate(
            "Điểm đáng học không phải là thuộc lòng bộ bốn đỉnh B, D, A phẩy, C phẩy. Cách phát hiện là nhìn tính chẵn lẻ của các tọa độ đỉnh: hai đỉnh được chọn luôn khác nhau ở đúng hai phương của lập phương, nên đoạn nối chúng là đường chéo một mặt. Khi sáu đoạn đều rơi vào đúng loại đường chéo đó, ta lập tức có sáu cạnh bằng nhau và nhận ra tứ diện đều.",
            1.8,
        )
        self.fade_card(q)
        H=(B+D+A1)/3
        self.add_label("H",H,GREEN,(0.07,0.02,0.05),18)
        height=solid(C1,H,GREEN,5.4)
        mark=right_angle_3d(H,C1-H,B-H,size=0.16,color=GOLD,width=3.2)
        self.play(Create(height),Create(mark),run_time=0.55)
        self.card("Lời giải", "Dùng ngay đường cao tứ diện đều", [
            ("math", "s=a sqrt(2)", 28, CYAN),
            ("math", "C' H=s sqrt(frac(2,3))", 27, INK),
            ("math", "C' H=frac(2 a,sqrt(3))", 31, GREEN),
            ("math", "d(C',(B D A'))=frac(2 a,sqrt(3))", 31, GOLD),
        ], accent=GREEN)
        self.narrate(
            "Gọi H là tâm tam giác đều BDA phẩy. Trong tứ diện đều cạnh s, đường cao bằng s căn hai phần ba. Ở đây s bằng a căn hai, nên C phẩy H bằng hai a trên căn ba. Vì C phẩy H vuông góc mặt BDA phẩy, đây chính là khoảng cách cần tìm. Không cần lập phương trình mặt phẳng của ba điểm và cũng không cần giải hệ tọa độ.",
            2.0,
        )
        self.takeaway("Mẫu đẹp: thấy các đường chéo mặt bằng nhau → thử tìm một tứ diện đều ẩn trong lập phương.")

    # ======================================================
    # Q2. HIDDEN REGULAR OCTAHEDRON FROM FACE CENTERS
    # ======================================================
    def q2_hidden_octahedron(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 2 · Bát diện đều ẩn trong lập phương", "Sáu tâm mặt tạo một khối đối ngẫu rất đẹp", "3/7")
        G=self.normalized_cube(side_display=3.05); self.add(G["edges"],G["dots"])
        P=lambda x,y,z: cube_unit_map(x,y,z,3.05)
        U=P(.5,.5,1); Lw=P(.5,.5,0)
        E=P(0,.5,.5); F=P(.5,0,.5); R=P(1,.5,.5); H=P(.5,1,.5)
        pts=[U,Lw,E,F,R,H]
        oct_edges=VGroup()
        for i in range(len(pts)):
            for j in range(i+1,len(pts)):
                d=np.linalg.norm(pts[i]-pts[j])
                target=np.linalg.norm(E-F)
                if abs(d-target)<1e-6:
                    oct_edges.add(solid(pts[i],pts[j],CYAN,3.6,0.90))
        eq_square=VGroup(solid(E,F,GOLD,4.2),solid(F,R,GOLD,4.2),solid(R,H,GOLD,4.2),solid(H,E,GOLD,4.2))
        self.play(Create(oct_edges),Create(eq_square),run_time=0.95)
        for name,pt,off in [
            ("U",U,(0.05,0.06,0.08)),("L",Lw,(0.05,-0.10,-0.02)),("E",E,(-0.12,0.02,0.03)),
            ("F",F,(0.04,-0.12,0.02)),("R",R,(0.08,0.02,0.03)),("H",H,(0.04,0.10,0.03))
        ]:
            self.add_label(name,pt,GOLD,off,17)
        q = self.card("Phát hiện", "Nối tâm của sáu mặt", [
            ("math", "E F=frac(a,sqrt(2))", 28, CYAN),
            ("text", "Mọi cạnh tương tự đều bằng nhau.",16,MUTED,NORMAL),
            ("math", "U L=a", 28, INK),
            ("math", "E R=F H=a", 27, INK),
        ], accent=PURPLE)
        self.narrate(
            "Bây giờ lấy tâm của cả sáu mặt lập phương. Hai tâm của hai mặt kề nhau cách nhau a trên căn hai, nên khi nối các tâm kề nhau ta được một bát diện đều. Để tính thể tích, không cần nhớ công thức bát diện. Bốn tâm của các mặt bên nằm trên mặt phẳng trung tâm và tạo thành một hình vuông; hai tâm của mặt trên và mặt dưới là hai đỉnh đối xứng.",
            2.1,
        )
        self.narrate(
            "Có một kiểm tra hình rất nhanh. Mặt phẳng qua bốn tâm mặt bên đi qua tâm lập phương và song song với hai đáy. Trong mặt phẳng ấy, hai đường nối các tâm của hai cặp mặt đối diện vuông góc và đều dài a. Vì vậy tứ giác giữa chắc chắn là hình vuông có hai đường chéo a. Cách nhìn này đáng tin hơn việc cố đo cạnh trên hình phối cảnh 3D.",
            1.8,
        )
        self.fade_card(q)
        self.card("Tính thể tích", "Hai chóp vuông bằng nhau", [
            ("math", "d_1=d_2=a", 26, CYAN),
            ("math", "S_Q=frac(a^2,2)", 29, INK),
            ("math", "h=frac(a,2)", 29, INK),
            ("math", "V_O=2 times frac(1,3) times frac(a^2,2) times frac(a,2)", 25, GREEN),
            ("math", "V_O=frac(a^3,6)", 34, GOLD),
        ], accent=GREEN)
        self.narrate(
            "Hình vuông giữa có hai đường chéo chính là khoảng cách giữa hai cặp tâm mặt đối diện, đều bằng a; vì thế diện tích của nó bằng a bình phương chia hai. Mỗi nửa bát diện là một chóp có chiều cao a chia hai. Nhân hai lần một phần ba diện tích đáy nhân chiều cao, ta được thể tích bát diện bằng a lập phương chia sáu. Một khối lạ xuất hiện, nhưng phép tính chỉ còn hai chóp vuông quen thuộc.",
            2.1,
        )
        self.takeaway("Mẫu đẹp: tâm các mặt của lập phương → bát diện đều; chọn mặt phẳng trung tâm để chia thành hai chóp.")

    # ======================================================
    # Q3. TRI-RECTANGULAR TETRAHEDRON: TWO GEMS
    # ======================================================
    def q3_tri_rectangular_tetra(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 3 · Tứ diện vuông ba chiều", "Một cấu hình — hai công thức rất ngắn", "4/7")
        scale=0.55
        P=lambda x,y,z: L(scale*x,scale*y,scale*z)
        O=P(0,0,0); A=P(4,0,0); B=P(0,3,0); C=P(0,0,5)
        edges=VGroup(solid(O,A),solid(O,B),solid(O,C,GREEN,4.5),solid(A,B),solid(A,C),solid(B,C))
        opp=face(A,B,C,color=PURPLE,opacity=0.13)
        self.add(opp,edges)
        for name,pt,off in [("O",O,(-0.14,-0.12,0)),("A",A,(0.10,-0.10,0)),("B",B,(-0.14,0.08,0)),("C",C,(-0.12,0.02,0.10))]:
            self.add_label(name,pt,GOLD,off,19)
        H=project_point_to_plane(O,A,B,C)
        self.add_label("H",H,GREEN,(0.06,0.02,0.05),17)
        oh=solid(O,H,GOLD,5.0)
        mark_h=right_angle_3d(H,O-H,A-H,size=0.15,color=GOLD,width=3.0)
        self.play(Create(oh),Create(mark_h),run_time=0.45)
        q = self.card("Giả thiết", "OA, OB, OC đôi một vuông góc", [
            ("math", "O A=a, O B=b, O C=c", 27, CYAN),
            ("math", "V=frac(a b c,6)", 29, INK),
            ("math", "S_(A B C)=frac(1,2) sqrt(a^2 b^2+a^2 c^2+b^2 c^2)", 24, INK),
            ("math", "d=frac(a b c,sqrt(a^2 b^2+a^2 c^2+b^2 c^2))", 25, GOLD),
        ], accent=PURPLE)
        self.narrate(
            "Xét tứ diện OABC có ba cạnh OA, OB, OC đôi một vuông góc. Khoảng cách từ O tới mặt ABC nhìn rất khó dựng trực tiếp. Nhưng thể tích lại biết ngay: một phần sáu a b c. Diện tích tam giác ABC có thể tính từ tích có hướng hoặc từ ba cạnh, và rút gọn thành một nửa căn của a bình b bình cộng a bình c bình cộng b bình c bình.",
            2.2,
        )
        self.narrate(
            "Đổi mặt ABC làm đáy, ta có V bằng một phần ba diện tích ABC nhân d. Sau đúng một phép rút gọn, khoảng cách d bằng a b c chia căn của tổng ba tích bình phương. Viết nghịch đảo bình phương còn đẹp hơn: một trên d bình bằng một trên a bình cộng một trên b bình cộng một trên c bình. Đây là phiên bản ba chiều của một hệ thức rất quen trong tam giác vuông.",
            2.2,
        )
        self.narrate(
            "Một trường hợp kiểm tra rất đẹp là a bằng b bằng c. Khi ấy ba cạnh từ O bằng nhau, mặt ABC trở thành tam giác đều cạnh a căn hai và công thức trên cho d bằng a trên căn ba. Kết quả hoàn toàn khớp với đối xứng của cấu hình. Kiểm tra một trường hợp cân đối như vậy là cách tốt để phát hiện nhầm hệ số trước khi dùng công thức tổng quát.",
            1.8,
        )
        self.fade_card(q)
        # Second gem: distance between opposite edges AB and OC.
        # Use the actual foot from O to AB in the displayed right triangle OAB.
        v=B-A
        t=float(np.dot(O-A,v)/np.dot(v,v))
        M=A+t*v
        self.add_label("M",M,GREEN,(0.06,0.02,0.04),17)
        om=solid(O,M,CYAN,5.0)
        mark1=right_angle_3d(M,O-M,B-A,size=0.15,color=GOLD,width=3.0)
        mark2=right_angle_3d(O,C-O,M-O,size=0.15,color=GOLD,width=3.0)
        self.play(Create(om),Create(mark1),Create(mark2),run_time=0.55)
        self.card("Viên ngọc thứ hai", "Khoảng cách hai cạnh đối AB và OC", [
            ("math", "O M perp A B", 27, CYAN),
            ("math", "O C perp (O A B)", 27, INK),
            ("math", "O M perp O C", 27, INK),
            ("math", "d(A B,O C)=O M", 29, GREEN),
            ("math", "O M=frac(a b,sqrt(a^2+b^2))", 29, GOLD),
        ], accent=GREEN)
        self.narrate(
            "Cấu hình này còn giấu một kết quả thứ hai. Hạ OM vuông góc AB trong tam giác vuông OAB. Vì OC vuông góc cả mặt OAB, nên OC cũng vuông góc OM. Vậy OM đồng thời vuông góc AB và OC: nó là đường vuông góc chung của hai cạnh đối. Từ công thức đường cao trong tam giác vuông, OM bằng a b chia căn a bình cộng b bình. Đáng chú ý, độ dài c của OC hoàn toàn biến mất.",
            2.2,
        )
        self.takeaway("Một cấu hình tốt có thể cho nhiều kết quả: hãy tận dụng quan hệ vuông góc của cả mặt phẳng, không chỉ từng đường.")

    # ======================================================
    # Q4. INVARIANT SUM OF DISTANCES IN A REGULAR TETRAHEDRON
    # ======================================================
    def q4_invariant_regular_tetra(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 4 · Một bất biến trong tứ diện đều", "Điểm chạy — tổng bốn khoảng cách vẫn không đổi", "5/7")
        G=self.regular_tetra(); self.add(G["edges"],G["dots"])
        for name in ["A","B","C","D"]:
            off={"A":(0.10,0.08,0.08),"B":(0.10,-0.10,-0.04),"C":(-0.15,0.08,-0.04),"D":(-0.15,-0.08,0.08)}[name]
            self.add_label(name,G[name],GOLD,off,18)
        A,B,C,D=G["A"],G["B"],G["C"],G["D"]
        P0=0.40*A+0.20*B+0.20*C+0.20*D
        P1=0.18*A+0.34*B+0.23*C+0.25*D
        u=ValueTracker(0.0)
        cur=lambda: (1-u.get_value())*P0+u.get_value()*P1
        moving=always_redraw(lambda: Dot3D(cur(),radius=0.060,color=RED))
        faces=[(B,C,D),(A,C,D),(A,B,D),(A,B,C)]
        colors=[GOLD,CYAN,GREEN,ORANGE]
        segs=[]
        for f,col in zip(faces,colors):
            segs.append(always_redraw(lambda f=f,col=col: solid(cur(),project_point_to_plane(cur(),*f),col,3.8,0.92)))
        self.add(moving,*segs)
        self.card("Bất biến", "P nằm tùy ý bên trong tứ diện đều cạnh a", [
            ("math", "V=frac(1,3) S (d_1+d_2+d_3+d_4)", 26, CYAN),
            ("math", "V=frac(1,3) S h", 28, INK),
            ("math", "d_1+d_2+d_3+d_4=h", 29, GREEN),
            ("math", "h=frac(a sqrt(6),3)", 31, GOLD),
        ], accent=PURPLE)
        self.narrate(
            "Cho P chạy tùy ý bên trong một tứ diện đều cạnh a. Gọi bốn khoảng cách từ P tới bốn mặt là d một, d hai, d ba, d bốn. Trên hình, bốn đoạn vuông góc thay đổi liên tục khi P di chuyển. Nếu cố tính từng khoảng cách, bài sẽ rất dài. Nhưng bốn tam giác đáy thực ra là bốn mặt của cùng một tứ diện đều, nên chúng có cùng diện tích S.",
            2.1,
        )
        self.play(u.animate.set_value(1.0),run_time=2.1,rate_func=there_and_back)
        self.narrate(
            "Nếu P tiến rất gần một mặt, một trong bốn khoảng cách tiến về không nhưng ba khoảng cách còn lại tự tăng để bù lại. Nếu P nằm ở tâm tứ diện, bốn khoảng cách bằng nhau và mỗi khoảng cách bằng một phần tư đường cao. Hai trạng thái rất khác nhau nhưng cùng thỏa một tổng cố định. Chính sự kiểm tra ở các vị trí đặc biệt này làm bất biến trở nên dễ tin hơn trước khi ta chứng minh bằng thể tích.",
            1.9,
        )
        self.narrate(
            "Bốn tứ diện nhỏ có chung đỉnh P và bốn đáy là bốn mặt của tứ diện lớn. Tổng thể tích của chúng bằng thể tích ban đầu, nên V bằng một phần ba S nhân tổng bốn khoảng cách. Mặt khác V cũng bằng một phần ba S nhân đường cao h của tứ diện đều. Vì vậy d một cộng d hai cộng d ba cộng d bốn luôn bằng h, bằng a căn sáu chia ba, bất kể P ở đâu bên trong.",
            2.2,
        )
        self.takeaway("Mẫu bất biến: nếu các đáy con có cùng diện tích, hãy cộng thể tích trước khi tính từng khoảng cách.")

    # ======================================================
    # Q5. SPHERE TANGENT TO ALL SIX EDGES OF A REGULAR TETRAHEDRON
    # ======================================================
    def q5_midsphere_regular_tetra(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 5 · Mặt cầu tiếp xúc sáu cạnh", "Một mặt cầu ít được nhắc tới nhưng cấu trúc rất đẹp", "6/7")
        G=self.regular_tetra(); A,B,C,D=G["A"],G["B"],G["C"],G["D"]
        self.add(G["edges"],G["dots"])
        for name in ["A","B","C","D"]:
            off={"A":(0.10,0.08,0.08),"B":(0.10,-0.10,-0.04),"C":(-0.15,0.08,-0.04),"D":(-0.15,-0.08,0.08)}[name]
            self.add_label(name,G[name],GOLD,off,18)
        M=(A+B)/2; N=(C+D)/2; Gc=(M+N)/2
        self.add_label("M",M,GREEN,(0.06,0.02,0.04),17); self.add_label("N",N,GREEN,(-0.10,0.02,0.04),17); self.add_label("G",Gc,RED,(0.08,0.03,0.05),17)
        mn=solid(M,N,GOLD,5.0)
        mark_m=right_angle_3d(M,N-M,B-A,size=0.14,color=GOLD,width=3.0)
        mark_n=right_angle_3d(N,M-N,D-C,size=0.14,color=GOLD,width=3.0)
        self.play(Create(mn),Create(mark_m),Create(mark_n),run_time=0.6)
        radius=float(np.linalg.norm(Gc-M))
        sph=sphere_surface(Gc,radius,color=PURPLE,opacity=0.075)
        self.play(FadeIn(sph),run_time=0.65)
        self.card("Cấu trúc", "M, N là trung điểm hai cạnh đối", [
            ("math", "M N perp A B", 27, CYAN),
            ("math", "M N perp C D", 27, CYAN),
            ("math", "M N=frac(a,sqrt(2))", 29, INK),
            ("math", "G M=frac(1,2) M N", 28, GREEN),
            ("math", "rho=frac(a sqrt(2),4)", 32, GOLD),
        ], accent=PURPLE)
        self.narrate(
            "Trong tứ diện đều, lấy M và N là trung điểm của hai cạnh đối AB và CD. Ta đã biết MN là đường vuông góc chung của hai cạnh đối và có độ dài a trên căn hai. Do đối xứng, tâm G của tứ diện nằm đúng tại trung điểm MN. Vì vậy khoảng cách từ G tới cạnh AB chính là GM, bằng một nửa MN, tức a căn hai chia bốn.",
            2.1,
        )
        self.narrate(
            "Bây giờ dựng mặt cầu tâm G bán kính rho bằng GM. Nó tiếp xúc AB tại M. Nhưng trong tứ diện đều, sáu cạnh hoàn toàn tương đương qua các phép đối xứng của khối, nên khoảng cách từ G tới cả sáu cạnh đều bằng nhau. Mặt cầu này vì thế tiếp xúc cả sáu cạnh. Ta không cần tìm sáu tiếp điểm; chỉ cần chứng minh một tiếp điểm rồi dùng đối xứng của tứ diện đều.",
            2.1,
        )
        self.narrate(
            "Cần phân biệt mặt cầu này với hai mặt cầu quen thuộc hơn. Nó không tiếp xúc bốn mặt như mặt cầu nội tiếp và cũng không đi qua bốn đỉnh như mặt cầu ngoại tiếp. Điều kiện của nó nằm ở sáu cạnh. Vì thế bán kính a căn hai chia bốn xuất hiện từ khoảng cách tâm đến một cạnh, chứ không từ đường cao đến một mặt hay khoảng cách tới một đỉnh.",
            1.9,
        )
        self.takeaway("Mẫu đẹp: trung điểm hai cạnh đối + đối xứng của tứ diện đều → mặt cầu tiếp xúc sáu cạnh.")

    # ======================================================
    # SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ cấu hình lạ", "Năm bài — năm cách làm hình khó trở nên quen", "7/7")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Đỉnh so le trong lập phương → tứ diện đều ẩn",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Tâm sáu mặt → bát diện đều, chia thành hai chóp",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Ba cạnh vuông tại một đỉnh → dùng mặt phẳng vuông góc",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Điểm động trong tứ diện đều → cộng thể tích để tìm bất biến",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Hai trung điểm cạnh đối → đường vuông góc chung và mặt cầu",19,INK)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.24).shift(LEFT*2.68+UP*0.08)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Kết quả đẹp", "Năm công thức đáng nhớ nhưng phải hiểu cấu trúc", [
            ("math", "frac(2 a,sqrt(3))", 28, GOLD),
            ("math", "frac(a^3,6)", 28, GOLD),
            ("math", "frac(1,d^2)=frac(1,a^2)+frac(1,b^2)+frac(1,c^2)", 24, GOLD),
            ("math", "d_1+d_2+d_3+d_4=frac(a sqrt(6),3)", 23, GOLD),
            ("math", "rho=frac(a sqrt(2),4)", 28, GOLD),
        ], accent=GREEN)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.70)
        self.narrate(
            "Năm cấu hình hôm nay nhìn rất khác nhau, nhưng cùng một triết lý. Đầu tiên hãy hỏi xem trong hình có một khối chuẩn nào đang ẩn hay không. Nếu không, hãy nhìn các tâm, trung điểm, mặt phẳng vuông góc và đối xứng. Với khoảng cách hoặc điểm động, thể tích thường giúp bỏ qua việc dựng chân vuông góc. Với khối đều, một quan hệ đúng ở một cạnh thường được nhân lên nhờ đối xứng.",
            2.1,
        )
        self.narrate(
            "Điều thầy muốn các em mang sang bài lạ không phải năm công thức trên màn hình, mà là thói quen làm cho cấu hình lạ trở về một cấu hình quen. Khi lời giải bỗng ngắn đi sau một đường phụ hoặc một phép chia khối, đó thường là dấu hiệu ta đã nhìn đúng. Video hai mươi sẽ gom toàn bộ mười chín video thành một bản đồ phương pháp HHKG THPT hoàn chỉnh.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 20 · CAPSTONE",17,BLUE,BOLD),
            txt("BẢN ĐỒ PHƯƠNG PHÁP HHKG THPT",24,GOLD,BOLD),
            txt("Khoảng cách · góc · thể tích · thiết diện · khối tròn · cực trị · Oxyz",17,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box)
        self.play(FadeIn(next_box),run_time=0.55)

    def construct(self):
        self.intro()
        self.q1_hidden_regular_tetra()
        self.q2_hidden_octahedron()
        self.q3_tri_rectangular_tetra()
        self.q4_invariant_regular_tetra()
        self.q5_midsphere_regular_tetra()
        self.synthesis()


def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_19_cau_hinh_la_loi_giai_dep_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 19")
    print("Themes: hidden regular tetrahedron, hidden octahedron, tri-rectangular tetrahedron, invariant distances, midsphere")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_19.wav"
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

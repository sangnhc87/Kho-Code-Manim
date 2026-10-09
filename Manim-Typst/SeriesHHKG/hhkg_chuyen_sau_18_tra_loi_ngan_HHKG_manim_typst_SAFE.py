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
# HHKG CHUYEN SAU 18 - TRA LOI NGAN HHKG
# Manim Community + MathTypst SAFE | Standalone 100%
# Muc tieu: 12-15 phut; 6 bai tra loi ngan, da dang cong cu, giai gon nhung du chung minh.
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
        series = txt("HHKG CHUYÊN SÂU · 18", 15, BLUE, BOLD)
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
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Trả lời ngắn HHKG","Tự nhận diện cấu hình — tính vừa đủ — chốt đáp số sạch","1/8")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Đọc dữ kiện và khoanh đại lượng cần trả lời",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Chọn một cấu trúc mạnh nhất",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Tính đến đúng mức cần thiết",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Kiểm tra đơn vị, miền giá trị và độ lớn",20,INK)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.28).shift(LEFT*2.70+UP*0.10)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Chiến lược","Không có đáp án gợi ý — phải tự chọn đường đi",[
            ("math","d, S, V, sin, tan",27,CYAN),
            ("math","perp, parallel, inter",27,INK),
            ("sep",),
            ("text","Mỗi câu chỉ giữ lại cấu trúc quyết định đáp số.",16,MUTED,NORMAL),
            ("text","Nếu có hai cách ngắn, dùng cách thứ hai để kiểm tra.",16,MUTED,NORMAL),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.70)
        self.narrate(
            "Dạng trả lời ngắn khó hơn đúng sai ở một điểm: đề không cho ta bốn mệnh đề để lần theo. Ta phải tự nhận diện cấu hình, tự chọn công cụ và tự kiểm soát đáp số. Nhưng điều đó không có nghĩa lời giải phải dài. Một bài tốt thường có đúng một cấu trúc mạnh nhất: đổi đáy thể tích, trung điểm đối xứng, mặt cắt qua trục, Oxyz ngắn hoặc trải phẳng.",
            2.0,
        )
        self.narrate(
            "Video mười tám gồm sáu câu ngắn nhưng phủ sáu kiểu tư duy khác nhau: khoảng cách điểm tới mặt, khoảng cách hai đường chéo nhau, diện tích thiết diện, cực trị khối tròn, điểm động cách đều hai mặt và đường đi ngắn nhất trên bề mặt khối. Mỗi câu đều có một bước kiểm tra để tránh ra một con số đẹp nhưng sai hình học.",
            2.0,
        )

    # ======================================================
    # Q1. POINT-PLANE DISTANCE VIA VOLUME
    # ======================================================
    def q1_distance_volume(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Câu 1 · Khoảng cách điểm–mặt","Đổi đáy tứ diện để tránh dựng chân vuông góc khó","2/8")
        G=self.rectangular_pyramid()
        self.add(G["base"],G["edges"],G["dots"])
        for name,pt,off in [
            ("A",G["A"],(-0.16,-0.12,0.0)),("B",G["B"],(0.12,-0.12,0.0)),
            ("C",G["C"],(0.12,0.10,0.0)),("D",G["D"],(-0.18,0.10,0.0)),("S",G["S"],(-0.14,-0.08,0.14))]:
            self.add_label(name,pt,GOLD if name!="S" else RED,off,20)
        plane=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.16)
        self.play(FadeIn(plane),run_time=0.55)
        q=self.card("Câu hỏi","Tính chính xác khoảng cách từ D đến (SBC)",[
            ("math","A B=6, A D=8",28,INK),
            ("math","S A=12",28,INK),
            ("math","S A perp (A B C D)",27,CYAN),
            ("sep",),
            ("math","d(D,(S B C))",33,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Câu một. Hình chóp S.ABCD có đáy là hình chữ nhật, AB bằng sáu, AD bằng tám, SA bằng mười hai và vuông góc với đáy. Hãy tính chính xác khoảng cách từ D đến mặt phẳng SBC. Nếu dựng trực tiếp chân vuông góc từ D xuống mặt nghiêng, ta sẽ mất nhiều công. Hãy thử xem mặt SBC có thể trở thành đáy của một tứ diện hay không.",
            1.8,
        )
        self.fade_card(q)
        H=project_point_to_plane(G["D"],G["S"],G["B"],G["C"])
        dh=solid(G["D"],H,GOLD,5.8)
        hdot=Dot3D(H,radius=0.055,color=GOLD)
        mark=right_angle_3d(H,G["D"]-H,G["C"]-G["B"],size=0.17,color=GOLD,width=3.3)
        self.play(Create(dh),FadeIn(hdot),Create(mark),run_time=0.65)
        self.card("Lời giải","Một thể tích — hai cách chọn đáy",[
            ("math","S_(B C D)=24",27,CYAN),
            ("math","V_(S B C D)=frac(1,3) times 24 times 12=96",25,INK),
            ("math","S B=6 sqrt(5), B C=8",26,INK),
            ("math","S_(S B C)=24 sqrt(5)",27,GREEN),
            ("math","d=frac(3 times 96,24 sqrt(5))",27,INK),
            ("math","d=frac(12 sqrt(5),5)",34,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Tam giác BCD có diện tích hai mươi bốn, còn S cách mặt đáy mười hai, nên thể tích tứ diện SBCD bằng chín mươi sáu. Bây giờ đổi mặt SBC làm đáy. SB là căn của sáu bình cộng mười hai bình, tức sáu căn năm; BC bằng tám và vuông góc SB, nên diện tích tam giác SBC bằng hai mươi bốn căn năm. Từ V bằng một phần ba nhân diện tích đáy mới nhân khoảng cách cần tìm, ta được d bằng mười hai căn năm chia năm.",
            2.2,
        )
        self.takeaway("Đáp số: 12√5/5. Khi chân vuông góc khó dựng, thử đổi đáy thể tích trước.")
        self.narrate(
            "Ta kiểm tra nhanh đáp số. Mười hai căn năm chia năm xấp xỉ năm phẩy ba bảy, nhỏ hơn các độ dài lớn trên mặt SBC như SB bằng sáu căn năm. Điều đó hợp lý vì khoảng cách vuông góc phải là đường ngắn nhất từ D tới mặt. Nếu ở bước cuối ta thu được một giá trị lớn hơn hẳn các kích thước của hình, đó là tín hiệu phải kiểm tra lại diện tích đáy mới hoặc hệ số một phần ba của thể tích.",
            1.5,
        )

    # ======================================================
    # Q2. SKEW DISTANCE IN REGULAR TETRAHEDRON
    # ======================================================
    def q2_regular_tetra(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=-48*DEGREES,zoom=VIEW_ZOOM)
        self.add_header("Câu 2 · Hai đường chéo nhau","Tứ diện đều — trung điểm biến bài 3D thành một tam giác vuông","3/8")
        G=self.regular_tetra(); self.add(G["edges"],G["dots"])
        for name in ["A","B","C","D"]:
            self.add_label(name,G[name],GOLD,(0.10,-0.08,0.08),20)
        ab=solid(G["A"],G["B"],GOLD,6.0)
        cd=hidden_edge(G["C"],G["D"],CYAN,5.2,0.95,0.10)
        self.play(Create(ab),Create(cd),run_time=0.55)
        q=self.card("Câu hỏi","Tứ diện đều ABCD cạnh 6",[
            ("text","Tính khoảng cách giữa hai cạnh đối AB và CD.",17,MUTED,NORMAL),
            ("math","d(A B,C D)",34,GOLD),
        ],accent=CYAN)
        self.narrate(
            "Câu hai. Tứ diện đều ABCD cạnh sáu. Tính khoảng cách giữa hai cạnh đối AB và CD. Hai đường này chéo nhau, nhưng tứ diện đều có đối xứng rất mạnh. Hãy nghĩ tới hai trung điểm của hai cạnh đối, thay vì dựng một đường vuông góc chung từ một điểm bất kỳ.",
            1.7,
        )
        self.fade_card(q)
        M=(G["A"]+G["B"])/2; N=(G["C"]+G["D"])/2
        mn=solid(M,N,GREEN,6.0)
        self.play(FadeIn(Dot3D(M,radius=0.055,color=GREEN)),FadeIn(Dot3D(N,radius=0.055,color=GREEN)),Create(mn),run_time=0.60)
        self.add_label("M",M,GREEN,(-0.10,-0.08,0.08),18); self.add_label("N",N,GREEN,(0.10,0.08,0.08),18)
        self.card("Lời giải","M, N là trung điểm của AB và CD",[
            ("math","M N perp A B",26,CYAN),
            ("math","M N perp C D",26,CYAN),
            ("math","M C=3 sqrt(3)",27,INK),
            ("math","C N=3",27,INK),
            ("math","M N^2=27-9=18",27,INK),
            ("math","M N=3 sqrt(2)",34,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Gọi M, N lần lượt là trung điểm AB và CD. Vì N cách đều A và B, đường MN vuông góc AB; tương tự, vì M cách đều C và D, MN vuông góc CD. Vậy MN chính là đường vuông góc chung. Trong tam giác đều ABC cạnh sáu, MC là đường trung tuyến nên bằng ba căn ba. CN bằng ba. Tam giác MCN vuông tại N, do đó MN bình bằng hai mươi bảy trừ chín, bằng mười tám. Khoảng cách cần tìm là ba căn hai.",
            2.1,
        )
        self.takeaway("Đáp số: 3√2. Với tứ diện đều, hai trung điểm của hai cạnh đối là cấu hình phải thử đầu tiên.")

    # ======================================================
    # Q3. CENTRAL REGULAR HEXAGON IN A CUBE
    # ======================================================
    def q3_cube_hexagon(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Câu 3 · Thiết diện đối xứng","Lục giác đều qua sáu trung điểm của hình lập phương cạnh 6","4/8")
        G=self.normalized_cube(); self.add(G["edges"],G["dots"])
        for name,key,off in [
            ("A","A",(-0.15,-0.12,0)),("B","B",(0.10,-0.12,0)),("C","C",(0.12,0.10,0)),("D","D",(-0.18,0.10,0)),
            ("A'","A1",(-0.17,-0.10,0.08)),("C'","C1",(0.10,0.10,0.08))]:
            self.add_label(name,G[key],GOLD,off,18)
        pts_norm=cube_section_normalized(1.5)
        pts=[cube_unit_map(*p,side_display=3.10) for p in pts_norm]
        sec=Polygon(*pts,fill_color=GOLD,fill_opacity=0.22,stroke_color=GOLD,stroke_width=4.0)
        self.play(FadeIn(sec),run_time=0.65)
        O=np.mean(np.array(pts),axis=0)
        spokes=VGroup(*[solid(O,p,CYAN,2.6,0.75) for p in pts])
        self.play(Create(spokes),run_time=0.55)
        q=self.card("Câu hỏi","Mặt phẳng qua sáu trung điểm tạo lục giác đều",[
            ("math","a=6",28,INK),
            ("text","Tính diện tích thiết diện.",17,MUTED,NORMAL),
            ("math","S_H",34,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Câu ba. Trong hình lập phương cạnh sáu, mặt phẳng đi qua sáu trung điểm thích hợp của sáu cạnh tạo thành một lục giác đều qua tâm khối. Hãy tính diện tích lục giác. Điểm mấu chốt không phải tọa độ của cả sáu đỉnh, mà là độ dài một cạnh và phép chia lục giác thành sáu tam giác đều.",
            1.8,
        )
        self.fade_card(q)
        self.card("Lời giải","Cắt lục giác thành sáu tam giác đều",[
            ("math","s=frac(6,sqrt(2))=3 sqrt(2)",27,CYAN),
            ("math","S_H=6 times frac(sqrt(3),4) times s^2",27,INK),
            ("math","s^2=18",27,INK),
            ("math","S_H=27 sqrt(3)",35,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Hai đỉnh liên tiếp của thiết diện là trung điểm của hai cạnh vuông góc trên cùng một mặt vuông cạnh sáu. Vì thế cạnh lục giác bằng nửa đường chéo của hình vuông, tức sáu trên căn hai, hay ba căn hai. Nối tâm lục giác tới sáu đỉnh ta được sáu tam giác đều cạnh ba căn hai. Mỗi tam giác có diện tích căn ba trên bốn nhân mười tám. Nhân sáu, diện tích thiết diện bằng hai mươi bảy căn ba.",
            2.0,
        )
        self.takeaway("Đáp số: 27√3. Cấu hình đối xứng mạnh thường biến đa giác lớn thành vài tam giác chuẩn.")

    # ======================================================
    # Q4. MAXIMUM CYLINDER IN A SPHERE
    # ======================================================
    def q4_cylinder_sphere(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Câu 4 · Cực trị khối tròn","Hình trụ nội tiếp mặt cầu bán kính 6 — tìm chiều cao tối ưu","5/8")
        O=np.array([-2.62,-0.02,0.0]); Rd=1.52
        hd=2*Rd/math.sqrt(3); rd=Rd*math.sqrt(2/3)
        sph=sphere_surface(O,Rd,BLUE,0.06); mer=meridian_circle(O,Rd,BLUE,2.1,0.60)
        cyl=cylinder_surface(O,rd,hd,CYAN,0.09)
        rims=VGroup(horizontal_rim(O+UP*hd/2,rd,CYAN,2.8),horizontal_rim(O+DOWN*hd/2,rd,CYAN,2.8))
        rect=VGroup(
            solid(O+LEFT*rd+DOWN*hd/2,O+LEFT*rd+UP*hd/2,GOLD,3.2),
            solid(O+RIGHT*rd+DOWN*hd/2,O+RIGHT*rd+UP*hd/2,GOLD,3.2),
            solid(O+LEFT*rd+UP*hd/2,O+RIGHT*rd+UP*hd/2,GOLD,2.8),
            solid(O+LEFT*rd+DOWN*hd/2,O+RIGHT*rd+DOWN*hd/2,GOLD,2.8),
        )
        self.play(FadeIn(sph),Create(mer),FadeIn(cyl),Create(rims),Create(rect),run_time=1.0)
        q=self.card("Câu hỏi","Mặt cầu bán kính 6",[
            ("text","Một hình trụ nội tiếp có thể tích lớn nhất.",17,MUTED,NORMAL),
            ("text","Tính chiều cao h của hình trụ.",17,MUTED,NORMAL),
            ("math","h",34,GOLD),
        ],accent=CYAN)
        self.narrate(
            "Câu bốn. Một hình trụ nội tiếp mặt cầu bán kính sáu. Trong tất cả các hình trụ như vậy, hãy tìm chiều cao của hình trụ có thể tích lớn nhất. Đây là bài cực trị ba chiều nhưng chỉ cần mặt cắt qua trục. Nửa chiều cao, bán kính đáy trụ và bán kính cầu tạo thành một tam giác vuông.",
            1.7,
        )
        self.fade_card(q)
        self.card("Lời giải","Mặt cắt trục đưa bài toán về một biến",[
            ("math","r^2+frac(h^2,4)=36",28,CYAN),
            ("math","V=pi (36-frac(h^2,4)) h",27,INK),
            ("math","V'=pi (36-frac(3 h^2,4))",27,INK),
            ("math","h^2=48",28,GREEN),
            ("math","h=4 sqrt(3)",35,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Từ tam giác vuông, r bình cộng h bình trên bốn bằng ba mươi sáu. Thay r bình vào thể tích pi r bình h, ta được V bằng pi nhân ba mươi sáu trừ h bình trên bốn, rồi nhân h. Đạo hàm bằng pi nhân ba mươi sáu trừ ba h bình trên bốn. Trong miền dương, cực đại xảy ra khi h bình bằng bốn mươi tám. Vì h dương, chiều cao cần tìm là bốn căn ba.",
            2.0,
        )
        self.takeaway("Đáp số: 4√3. Khối tròn cực trị: mặt cắt trục trước, đạo hàm sau.")
        self.narrate(
            "Có hai kiểm tra ngắn. Thứ nhất, bốn căn ba nhỏ hơn đường kính mười hai nên hình trụ thực sự nằm trong cầu. Thứ hai, tại hai biên suy biến h tiến về không hoặc h tiến về mười hai, thể tích đều tiến về không, nên nghiệm nội miền do đạo hàm tìm được phù hợp với một cực đại. Với bài trả lời ngắn, những kiểm tra miền như vậy rất quan trọng vì ta không có phương án lựa chọn để phát hiện một nghiệm ngoại lai.",
            1.5,
        )

    # ======================================================
    # Q5. MOVING POINT EQUIDISTANT FROM TWO PLANES
    # ======================================================
    def q5_moving_equal_distance(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Câu 5 · Điểm động cách đều hai mặt","Kết hợp Oxyz ngắn với animation kiểm tra trực quan","6/8")
        G=self.square_pyramid(); self.add(G["base"],G["edges"],G["dots"])
        for name,pt,off in [
            ("A",G["A"],(-0.16,-0.12,0)),("B",G["B"],(0.12,-0.12,0)),("C",G["C"],(0.12,0.10,0)),
            ("D",G["D"],(-0.18,0.10,0)),("S",G["S"],(-0.14,-0.08,0.14))]:
            self.add_label(name,pt,GOLD if name!="S" else RED,off,19)
        plane=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.15); self.add(plane)
        q=self.card("Câu hỏi","M chạy trên SA",[
            ("math","A B=6, S A=8",28,INK),
            ("math","S A perp (A B C D)",27,CYAN),
            ("text","Tìm AM để M cách đều đáy và mặt (SBC).",16,MUTED,NORMAL),
            ("math","A M",34,GOLD),
        ],accent=PURPLE)
        self.narrate(
            "Câu năm. Hình chóp S.ABCD có đáy vuông cạnh sáu, SA bằng tám và vuông góc đáy. Điểm M chạy trên SA. Tìm AM để M cách đều mặt đáy và mặt SBC. Vì M đã nằm trên đường cao SA, khoảng cách tới đáy rất đơn giản. Phần còn lại nên dùng một hệ trục ngắn để khoảng cách tới mặt nghiêng trở thành biểu thức bậc nhất theo t.",
            1.8,
        )
        self.fade_card(q)
        t=ValueTracker(0.8)
        A,S=G["A"],G["S"]
        M=lambda: A+(t.get_value()/8.0)*(S-A)
        moving=always_redraw(lambda: Dot3D(M(),radius=0.060,color=GOLD))
        base_dist=always_redraw(lambda: solid(A,M(),GREEN,5.0))
        plane_dist=always_redraw(lambda: solid(M(),project_point_to_plane(M(),G["S"],G["B"],G["C"]),GOLD,5.0))
        self.add(moving,base_dist,plane_dist)
        self.play(t.animate.set_value(6.6),run_time=2.0,rate_func=there_and_back)
        self.play(t.animate.set_value(3.0),run_time=0.8)
        self.add_label("M",M(),GOLD,(0.12,0.0,0.08),18)
        H3=project_point_to_plane(M(),G["S"],G["B"],G["C"])
        mark_base=right_angle_3d(G["A"],M()-G["A"],G["B"]-G["A"],size=0.15,color=GREEN,width=3.1)
        mark_plane=right_angle_3d(H3,M()-H3,G["C"]-G["B"],size=0.15,color=GOLD,width=3.1)
        self.play(Create(mark_base),Create(mark_plane),run_time=0.40)
        self.card("Lời giải","Đặt A(0,0,0), M(0,0,t)",[
            ("math","4 x+3 z-24=0",27,CYAN),
            ("math","d_1=t",28,INK),
            ("math","d_2=frac(24-3 t,5)",28,INK),
            ("math","t=frac(24-3 t,5)",28,GREEN),
            ("math","t=3",35,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Đặt A làm gốc, AB theo trục x và SA theo trục z. Khi đó mặt SBC có phương trình bốn x cộng ba z trừ hai mươi bốn bằng không. Nếu M có tọa độ không, không, t thì khoảng cách từ M xuống đáy bằng t. Khoảng cách từ M đến mặt SBC bằng hai mươi bốn trừ ba t chia năm. Cho hai khoảng cách bằng nhau, ta được t bằng ba. Trên hình, khi M dừng ở vị trí này, hai đoạn khoảng cách có cùng độ dài.",
            2.1,
        )
        self.takeaway("Đáp số: AM = 3. Điểm động + mặt nghiêng: Oxyz thường biến bài toán thành phương trình bậc nhất.")

    # ======================================================
    # Q6. SHORTEST SURFACE PATH ON A CUBE
    # ======================================================
    def q6_unfold_cube(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Câu 6 · Đường đi ngắn nhất trên bề mặt","Trải hai mặt kề thành một hình chữ nhật","7/8")
        G=self.normalized_cube(side_display=2.85); self.add(G["edges"],G["dots"])
        A=G["A"]; B=G["B"]; B1=G["B1"]; C1=G["C1"]
        M=0.35*B+0.65*B1
        path=VGroup(solid(A,M,GOLD,5.2),solid(M,C1,GREEN,5.2))
        self.play(Create(path),run_time=0.6)
        self.add_label("A",A,GOLD,(-0.14,-0.12,0),18); self.add_label("M",M,GOLD,(0.10,0.02,0.08),18); self.add_label("C'",C1,GOLD,(0.10,0.10,0.08),18)
        q=self.card("Câu hỏi","Lập phương cạnh 4, M thuộc BB'",[
            ("text","Tìm giá trị nhỏ nhất của AM + MC'.",17,MUTED,NORMAL),
            ("math","L_m",34,GOLD),
        ],accent=ORANGE)
        self.narrate(
            "Câu cuối. Lập phương cạnh bốn. Điểm M chạy trên cạnh BB phẩy. Hãy tìm giá trị nhỏ nhất của tổng AM cộng MC phẩy, với hai đoạn nằm trên hai mặt kề nhau của khối. Nếu lập hàm theo BM, ta sẽ có hai căn thức. Cách hình học đẹp hơn là mở hai mặt kề ra cùng một mặt phẳng.",
            1.7,
        )
        self.fade_card(q)

        # Switch to a clean 2D unfolding while keeping the mathematical story continuous.
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Câu 6 · Trải phẳng","Đường gấp khúc trở thành một đoạn thẳng","7/8")
        x0=-5.0; y0=-1.15; s=0.60
        A2=np.array([x0,y0,0]); B2=np.array([x0+4*s,y0,0]); B12=np.array([x0+4*s,y0+4*s,0]); X=np.array([x0+8*s,y0+4*s,0])
        rect=Rectangle(width=8*s,height=4*s,stroke_color=BLUE,stroke_width=2.6,fill_color=BLUE,fill_opacity=0.035)
        rect.move_to((A2+X)/2)
        fold=DashedLine(B2,B12,color=CYAN,stroke_width=3.0,dash_length=0.10)
        diag=Line(A2,X,color=GOLD,stroke_width=5.0)
        M2=(B2+B12)/2
        self.add(rect,fold); self.play(Create(diag),run_time=0.65)
        for name,pt,off in [("A",A2,(-0.15,-0.12,0)),("M",M2,(0.08,0.10,0)),("X",X,(0.08,0.10,0))]:
            lab=mty(name,20,GOLD).move_to(pt+np.array(off)); self.add_fixed_in_frame_mobjects(lab)
        self.card("Lời giải","C' mở ra điểm X trên mặt phẳng",[
            ("math","A M+M C'=A M+M X",26,CYAN),
            ("math","A M+M X >= A X",27,INK),
            ("math","A X=sqrt((2 a)^2+a^2)",27,INK),
            ("math","A X=a sqrt(5)",29,GREEN),
            ("math","a=4",27,INK),
            ("math","L_m=4 sqrt(5)",35,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Sau khi trải hai mặt kề quanh cạnh BB phẩy, điểm C phẩy biến thành điểm X. Khi đó tổng AM cộng MC phẩy bằng AM cộng MX trong cùng một mặt phẳng. Theo bất đẳng thức tam giác, tổng này không nhỏ hơn AX, và đạt đúng AX khi A, M, X thẳng hàng. Hai hình vuông cạnh a tạo thành hình chữ nhật kích thước hai a nhân a, nên AX bằng a căn năm. Với a bằng bốn, giá trị nhỏ nhất là bốn căn năm. Đường thẳng AX cắt nếp gấp tại trung điểm BB phẩy.",
            2.2,
        )
        self.takeaway("Đáp số: 4√5. Đường đi trên nhiều mặt phẳng → thử trải phẳng trước khi đạo hàm.")

    # ======================================================
    # SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ trả lời ngắn","Sáu câu — sáu cấu trúc quyết định đáp số","8/8")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Khoảng cách khó dựng → đổi đáy thể tích",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Tứ diện đều → trung điểm và đối xứng",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Thiết diện đối xứng → chia thành hình chuẩn",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Khối tròn cực trị → mặt cắt trục",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Điểm động + mặt nghiêng → Oxyz ngắn",19,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("6",18,GOLD,BOLD),txt("Đường đi bề mặt → trải phẳng",19,INK)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).shift(LEFT*2.67+UP*0.06)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Đáp số","Sáu câu của Video 18",[
            ("math","frac(12 sqrt(5),5)",27,GOLD),
            ("math","3 sqrt(2)",27,GOLD),
            ("math","27 sqrt(3)",27,GOLD),
            ("math","4 sqrt(3)",27,GOLD),
            ("math","3",27,GOLD),
            ("math","4 sqrt(5)",27,GOLD),
        ],accent=GREEN)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.70)
        self.narrate(
            "Sáu câu trả lời ngắn vừa rồi không dùng cùng một kỹ thuật. Câu một đổi đáy thể tích. Câu hai khai thác trung điểm trong tứ diện đều. Câu ba dùng đối xứng của thiết diện. Câu bốn đưa khối tròn về mặt cắt trục. Câu năm dùng Oxyz vì khoảng cách tới mặt nghiêng trở thành bậc nhất. Câu sáu trải phẳng để biến đường gấp khúc thành đoạn thẳng. Điều quan trọng là chọn được đúng ngôn ngữ trước khi tính.",
            2.1,
        )
        self.narrate(
            "Trong bài trả lời ngắn, đáp số không có phương án lựa chọn để cứu ta. Vì vậy sau khi tính xong, hãy dành vài giây kiểm tra: khoảng cách có nhỏ hơn các cạnh liên quan không, diện tích có đúng thứ nguyên bình phương không, cực trị có nằm trong miền hình học không, và kết quả có phù hợp với đối xứng của hình hay không. Những kiểm tra này thường phát hiện lỗi nhanh hơn việc làm lại cả bài.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 19",17,BLUE,BOLD),
            txt("CẤU HÌNH LẠ · LỜI GIẢI ĐẸP",24,GOLD,BOLD),
            txt("Nhìn tưởng Oxyz dài — nhưng một đường phụ đúng có thể giải quyết cả bài",18,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box)
        self.play(FadeIn(next_box),run_time=0.55)
        self.narrate(
            "Video mười chín sẽ dành cho những cấu hình lạ nhưng lời giải đẹp: điểm phụ không hiển nhiên, phép chiếu bất ngờ, đối xứng ẩn, đổi đỉnh thể tích và các bài nhìn hình rất khó nhưng sau khi dựng đúng một đường thì lời giải chỉ còn vài dòng. Đây sẽ là chặng cuối trước video hai mươi tổng kết toàn bộ bản đồ phương pháp HHKG.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.q1_distance_volume()
        self.q2_regular_tetra()
        self.q3_cube_hexagon()
        self.q4_cylinder_sphere()
        self.q5_moving_equal_distance()
        self.q6_unfold_cube()
        self.synthesis()


def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_18_tra_loi_ngan_HHKG_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 18")
    print("Themes: short answer, point-plane distance, skew lines, section area, solids optimization, moving point, unfolding")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_18.wav"
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

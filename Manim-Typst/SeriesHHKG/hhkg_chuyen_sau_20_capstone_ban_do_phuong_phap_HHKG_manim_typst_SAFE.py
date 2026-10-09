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
# HHKG CHUYEN SAU 20 - CAPSTONE BAN DO PHUONG PHAP HHKG THPT
# Manim Community + MathTypst SAFE | Standalone 100%
# Muc tieu: 15-18 phut; capstone he thong hoa quyet dinh phuong phap va 5 bai mau lien ket 19 video truoc.
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
        series = txt("HHKG CHUYÊN SÂU · 20", 15, BLUE, BOLD)
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
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        tag = txt("HHKG CHUYÊN SÂU · 20", 18, BLUE, BOLD)
        title = txt("CAPSTONE — BẢN ĐỒ PHƯƠNG PHÁP HHKG THPT", 39, INK, BOLD)
        sub = txt("Không bắt đầu bằng công thức — bắt đầu bằng câu hỏi đúng", 25, CYAN, BOLD)
        rule = Line(LEFT*4.8, RIGHT*4.8, color=GOLD, stroke_width=3.2)
        brand = txt(TEN_THAY, 18, MUTED)
        g = VGroup(tag, title, sub, rule, brand).arrange(DOWN, buff=0.27)
        fit_width(g, 12.0)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g, shift=UP*0.12), run_time=0.8)
        self.narrate(
            "Đây là video thứ hai mươi, cũng là capstone của toàn bộ series hình học không gian chuyên sâu. Thay vì thêm một tập công thức mới, ta sẽ gom những gì đã học thành một bản đồ ra quyết định. Khi gặp một bài lạ, câu hỏi quan trọng không phải là công thức nào có thể dùng, mà là cấu trúc nào đang ẩn trong hình. Khoảng cách có thể đổi sang thể tích. Góc phải tìm hình chiếu hoặc mặt cắt vuông góc. Thiết diện phải đi qua từng mặt. Điểm động phải kiểm tra bất biến trước khi lập hàm. Và Oxyz chỉ xuất hiện khi nó thực sự làm lời giải ngắn hơn.",
            2.2,
        )
        self.narrate(
            "Trong video này, thầy không cố nhắc lại toàn bộ mười chín video trước. Ta sẽ làm một việc hữu ích hơn: xây một cây quyết định, rồi dùng năm bài mẫu để thử cây đó. Mỗi bài sẽ bắt đầu bằng bước chẩn đoán, sau đó mới dựng phụ, tính toán và kiểm tra đáp số. Nếu các em nhớ được thứ tự tư duy này, một cấu hình mới sẽ bớt đáng sợ rất nhiều, vì ta biết mình phải hỏi gì trước khi cầm bút tính.",
            1.8,
        )

    def decision_map(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_header("Bản đồ ra quyết định", "Sáu cửa vào của một bài HHKG", "01/08")

        root = VGroup(
            RoundedRectangle(width=3.0, height=0.70, corner_radius=0.12, fill_color=PANEL_2, fill_opacity=0.96, stroke_color=GOLD, stroke_width=2.0),
            txt("BÀI TOÁN ĐANG HỎI GÌ?", 19, GOLD, BOLD),
        )
        root[1].move_to(root[0])
        root.move_to(LEFT*2.6+UP*1.95)

        specs = [
            ("KHOẢNG CÁCH", "song song? mặt phụ? thể tích?", BLUE),
            ("GÓC", "hình chiếu? cạnh chung?", CYAN),
            ("THIẾT DIỆN", "đi qua mặt nào trước?", GREEN),
            ("THỂ TÍCH", "cùng đáy? cùng cao? tỷ số?", ORANGE),
            ("ĐIỂM ĐỘNG", "bất biến? miền? hàm nào?", PURPLE),
            ("OXYZ / TRẢI PHẲNG", "có ngắn hơn hình học không?", RED),
        ]
        boxes = VGroup()
        positions = [LEFT*4.55+UP*0.65, LEFT*1.55+UP*0.65, LEFT*4.55+DOWN*0.65, LEFT*1.55+DOWN*0.65, LEFT*4.55+DOWN*1.95, LEFT*1.55+DOWN*1.95]
        for (name, desc, col), pos in zip(specs, positions):
            bg = RoundedRectangle(width=2.55, height=0.90, corner_radius=0.10, fill_color=PANEL, fill_opacity=0.94, stroke_color=col, stroke_width=1.5)
            a = txt(name, 17, col, BOLD)
            b = fit_width(txt(desc, 13, MUTED), 2.25)
            gg = VGroup(bg, a, b)
            a.move_to(bg.get_center()+UP*0.15)
            b.move_to(bg.get_center()+DOWN*0.18)
            gg.move_to(pos)
            boxes.add(gg)

        arrows = VGroup()
        for gg in boxes:
            arrows.add(Arrow(root.get_bottom(), gg[0].get_top(), buff=0.08, color=GRID, stroke_width=1.7, max_tip_length_to_length_ratio=0.09))

        card = self.card("Nguyên tắc", "Không tính trước khi chẩn đoán", [
            ("text", "1. Gọi đúng loại bài", 19, INK, BOLD),
            ("text", "2. Tìm cấu trúc rút gọn", 19, INK, BOLD),
            ("text", "3. Chọn ngôn ngữ ngắn nhất", 19, INK, BOLD),
            ("sep",),
            ("text", "Hình học trước — đại số sau", 19, GOLD, BOLD),
        ], accent=GOLD, height=4.2)

        self.add_fixed_in_frame_mobjects(root, arrows, boxes)
        self.play(FadeIn(root), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), LaggedStart(*[FadeIn(b, shift=UP*0.08) for b in boxes], lag_ratio=0.08), run_time=1.7)
        self.narrate(
            "Cây quyết định bắt đầu bằng đúng một câu: bài đang hỏi đại lượng nào. Nếu là khoảng cách, kiểm tra song song, mặt phẳng phụ và khả năng đổi sang thể tích. Nếu là góc, tìm hình chiếu hoặc cạnh chung của hai mặt. Nếu là thiết diện, đi theo từng mặt của đa diện và chỉ nối hai điểm khi chúng thật sự cùng nằm trên một mặt. Với thể tích, ưu tiên tỷ số trước số tuyệt đối. Với điểm động, kiểm tra bất biến trước khi lập hàm. Còn Oxyz và trải phẳng là ngôn ngữ thứ hai, chỉ dùng khi làm cấu trúc sáng hơn.",
            2.1,
        )
        self.narrate(
            "Một lỗi rất phổ biến là nhìn thấy dữ kiện số rồi tính ngay. Cách đó khiến bài hình học không gian biến thành một mê cung. Thứ tự tốt hơn là: gọi tên bài toán, tìm cấu trúc giảm chiều, rồi mới chọn công thức. Giảm chiều nghĩa là biến ba chiều thành một tam giác phẳng, một mặt cắt, một tỷ số, một đoạn vuông góc chung hoặc một phương trình tọa độ ngắn. Từ đây, ta sẽ thử cây quyết định trên năm tình huống tiêu biểu.",
            1.9,
        )

    def case_distance(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Cửa 1 — Khoảng cách", "Nếu chân vuông góc khó dựng, thử đổi đáy thể tích", "02/08")
        G = self.square_pyramid(a=4, h=3, scale=0.56)
        self.add(G["base"], G["edges"], G["dots"])
        for name in ["A","B","C","D","S"]:
            self.add_label(name, G[name], RED if name=="S" else GOLD)

        sbc = face(G["S"], G["B"], G["C"], color=PURPLE, opacity=0.20)
        H = project_point_to_plane(G["D"], G["S"], G["B"], G["C"])
        dh = solid(G["D"], H, GOLD, 6.0, 1.0)
        mark = right_angle_3d(H, G["D"]-H, G["B"]-H, size=0.22, color=GOLD)
        self.play(FadeIn(sbc), Create(dh), FadeIn(Dot3D(H, radius=0.05, color=GOLD)), Create(mark), run_time=0.9)

        card = self.card("Chẩn đoán", "Tính d(D,(SBC))", [
            ("text", "Chân H khó thấy → không săn H", 17, MUTED, NORMAL),
            ("math", "V_(S B C D)=8", 29, CYAN),
            ("math", "S_(S B C)=10", 29, GREEN),
            ("math", "8=frac(1,3) times 10 times d", 27, INK),
            ("math", "d=frac(12,5)", 37, GOLD),
        ], accent=BLUE, height=4.75)
        self.narrate(
            "Bài thứ nhất quay về cấu hình quen thuộc: đáy ABCD là hình vuông cạnh bốn, SA bằng ba và vuông góc đáy. Cần tính khoảng cách từ D tới mặt SBC. Cây quyết định nói: đây là khoảng cách điểm đến mặt; nếu chân H khó dựng thì thử đổi mặt SBC thành đáy của một tứ diện. Ta vẫn vẽ DH để hiểu ý nghĩa hình học, nhưng lời giải không phụ thuộc vào việc tìm tọa độ hay vị trí chính xác của H.",
            1.8,
        )
        self.narrate(
            "Tứ diện SBCD chiếm một nửa hình chóp SABCD nên có thể tích bằng tám. Tam giác SBC vuông tại B, vì SB vuông BC, với SB bằng năm và BC bằng bốn nên diện tích bằng mười. Dùng SBC làm đáy, chiều cao tương ứng chính là d từ D tới mặt SBC. Ta có tám bằng một phần ba nhân mười nhân d, suy ra d bằng mười hai phần năm. Mẫu nhận dạng ở đây là: khoảng cách khó dựng, nhưng mặt cần đo lại có diện tích dễ tính, hãy nghĩ đến thể tích.",
            2.0,
        )
        self.takeaway("Khoảng cách khó dựng → đổi mặt cần đo thành đáy thể tích")

    def case_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Cửa 2 — Góc", "Góc nhị diện bắt đầu từ cạnh chung, không bắt đầu từ công thức", "03/08")
        G = self.square_pyramid(a=4, h=3, scale=0.56)
        self.add(G["base"], G["edges"], G["dots"])
        for name in ["A","B","C","S"]:
            self.add_label(name, G[name], RED if name=="S" else GOLD)
        sbc = face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.18)
        self.add(sbc)
        bc = solid(G["B"],G["C"],GOLD,7.0)
        ba = solid(G["B"],G["A"],CYAN,5.0)
        bs = solid(G["B"],G["S"],GREEN,5.0)
        m1 = right_angle_3d(G["B"], G["C"]-G["B"], G["A"]-G["B"], size=0.22, color=CYAN)
        m2 = right_angle_3d(G["B"], G["C"]-G["B"], G["S"]-G["B"], size=0.27, color=GREEN)
        arc = angle_arc_3d(G["B"], G["A"]-G["B"], G["S"]-G["B"], radius=0.47, color=GOLD, width=6.0)
        self.play(Create(bc), Create(ba), Create(bs), Create(m1), Create(m2), Create(arc), run_time=1.0)

        card = self.card("Chẩn đoán", "Nhị diện (SBC) và đáy theo BC", [
            ("math", "B A perp B C", 27, CYAN),
            ("math", "B S perp B C", 27, GREEN),
            ("math", "beta=hat(A B S, size: #155%)", 28, GOLD),
            ("math", "tan beta=frac(S A,A B)", 29, INK),
            ("math", "tan beta=frac(3,4)", 36, GOLD),
        ], accent=CYAN, height=4.8)
        self.narrate(
            "Bài thứ hai là góc nhị diện giữa mặt SBC và mặt đáy theo cạnh BC. Cây quyết định bắt buộc ta xác định cạnh chung trước. Sau đó, tại cùng một điểm B trên cạnh chung, chọn trong mỗi mặt một đường vuông góc BC. Trong đáy đó là BA. Trong mặt SBC đó là BS, vì BC vuông cả BA và SA nên BC vuông với mặt SAB, suy ra BC vuông BS. Chỉ tới lúc này ta mới được đồng nhất góc nhị diện với góc phẳng ABS.",
            2.0,
        )
        self.narrate(
            "Trên hình, cung vàng được dựng từ chính hai tia BA và BS trong không gian, nên hai đầu cung nằm đúng trên hai tia trước khi camera chiếu xuống màn hình. Tam giác SAB là tam giác vuông ba bốn năm, vì vậy tang beta bằng SA trên AB, bằng ba phần bốn. Mẫu nhận dạng: góc nhị diện không phải là góc giữa hai đường tùy ý nằm trên hai mặt. Nó là góc của một mặt cắt vuông góc cạnh chung.",
            1.9,
        )
        self.takeaway("Nhị diện → cạnh chung → hai đường cùng vuông góc cạnh chung → góc phẳng")

    def case_section(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Cửa 3 — Thiết diện", "Đa giác phải được dựng theo từng mặt của khối", "04/08")
        C = self.normalized_cube(side_display=3.20)
        self.add(C["edges"], C["dots"])
        for name,key in [("A","A"),("B","B"),("C","C"),("D","D"),("A'","A1"),("B'","B1"),("C'","C1"),("D'","D1")]:
            self.add_label(name,C[key],size=19,off=(0.08,-0.08,0.05))

        pts_u = cube_section_normalized(1.5)
        pts = [cube_unit_map(*p, side_display=3.20) for p in pts_u]
        poly = Polygon(*pts, fill_color=GOLD, fill_opacity=0.24, stroke_color=GOLD, stroke_width=4.2)
        dots = VGroup(*[Dot3D(p,radius=0.052,color=GOLD) for p in pts])
        edges = VGroup(*[solid(pts[i],pts[(i+1)%len(pts)],GOLD,5.0) for i in range(len(pts))])
        self.play(LaggedStart(*[FadeIn(d) for d in dots],lag_ratio=0.08), LaggedStart(*[Create(e) for e in edges],lag_ratio=0.12), FadeIn(poly), run_time=1.6)

        card = self.card("Chẩn đoán", "Mặt x+y+z=frac(3,2) a", [
            ("text", "Cắt đúng 6 cạnh của lập phương", 17, MUTED, NORMAL),
            ("text", "→ thiết diện là lục giác", 18, INK, BOLD),
            ("math", "S=frac(3 sqrt(3),4) a^2", 31, GOLD),
            ("sep",),
            ("text", "Đừng đoán đa giác từ hình phối cảnh", 17, CYAN, BOLD),
        ], accent=GREEN, height=4.45)
        self.narrate(
            "Bài thứ ba là thiết diện của lập phương bởi mặt x cộng y cộng z bằng ba phần hai a. Nếu nhìn phối cảnh rồi đoán, ta rất dễ bỏ sót một đỉnh. Cây quyết định cho thiết diện yêu cầu ta đi theo từng mặt: tìm các cạnh bị mặt phẳng cắt, đánh dấu giao điểm, rồi nối các điểm chỉ khi chúng cùng nằm trên một mặt của khối. Với tham số ba phần hai, mặt phẳng cắt đúng sáu cạnh và đa giác khép kín là một lục giác.",
            1.9,
        )
        self.narrate(
            "Do mặt phẳng đi qua tâm lập phương và vuông góc với đường chéo không gian, sáu giao điểm đối xứng nhau; trong trường hợp đặc biệt này thiết diện là lục giác đều. Diện tích bằng ba căn ba trên bốn a bình phương. Điều quan trọng hơn đáp số là quy tắc kiểm tra: với mỗi cạnh của thiết diện, ta phải chỉ ra được nó nằm trên mặt nào của đa diện. Nếu không trả lời được câu đó, đoạn nối ấy chưa có cơ sở hình học.",
            1.9,
        )
        self.takeaway("Thiết diện → tìm giao điểm theo mặt → nối đúng mặt → khép kín → mới tính")

    def case_dynamic(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Cửa 4 — Điểm động & cực trị", "Kiểm tra bất biến trước, đạo hàm sau cùng", "05/08")
        G = self.square_pyramid(a=4, h=6, scale=0.43)
        self.add(G["base"],G["edges"],G["dots"])
        for name in ["A","B","C","D","S"]:
            self.add_label(name,G[name],RED if name=="S" else GOLD,size=20)

        u=ValueTracker(0.28)
        def section_pts():
            k=u.get_value()
            S=G["S"]
            return [S+k*(G[q]-S) for q in ["A","B","C","D"]]
        sec=always_redraw(lambda: Polygon(*section_pts(),fill_color=GOLD,fill_opacity=0.23,stroke_color=GOLD,stroke_width=3.6))
        self.add(sec)
        self.play(u.animate.set_value(0.80),run_time=2.0,rate_func=there_and_back)

        card = self.card("Chẩn đoán", "Tối đa tích hai thể tích", [
            ("math", "u=frac(S M,S A)", 28, CYAN),
            ("math", "V_1=u^3 V", 29, INK),
            ("math", "V_2=(1-u^3) V", 29, INK),
            ("math", "y=u^3", 30, GREEN),
            ("math", "y(1-y) <= frac(1,4)", 31, GOLD),
            ("math", "u=(frac(1,2))^(frac(1,3))", 31, GOLD),
        ], accent=PURPLE, height=5.05)
        self.narrate(
            "Bài thứ tư là điểm động. Một mặt phẳng song song đáy cắt các cạnh bên theo cùng tỷ số u tính từ đỉnh S. Trước khi đạo hàm, cây quyết định hỏi hai việc. Thứ nhất, đại lượng có bất biến không. Ở đây không, vì mặt cắt thật sự thay đổi. Thứ hai, có thể thay biến để nhìn cấu trúc đơn giản hơn không. Chóp nhỏ đồng dạng tỷ số u nên thể tích của nó là u lập phương V, còn phần dưới là một trừ u lập phương nhân V.",
            1.9,
        )
        self.narrate(
            "Cần tối đa tích hai thể tích, ta không cần đạo hàm một biểu thức bậc sáu. Đặt y bằng u lập phương. Bài toán trở thành tối đa y nhân một trừ y trên đoạn từ không đến một. Tích đạt lớn nhất một phần tư khi y bằng một phần hai. Vì vậy u bằng căn bậc ba của một phần hai. Mẫu nhận dạng: với điểm động, hãy thử bất biến, đơn điệu, đối xứng hoặc đổi biến trước; đạo hàm là công cụ cuối cùng chứ không phải phản xạ đầu tiên.",
            2.0,
        )
        self.takeaway("Điểm động → bất biến? miền? biến nào tự nhiên? → rồi mới cực trị")

    def case_oxyz(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Cửa 5 — Oxyz", "Dùng tọa độ khi nó biến cấu hình khó nhìn thành phép tính ngắn", "06/08")
        C=self.normalized_cube(side_display=3.25)
        self.add(C["edges"],C["dots"])
        for name,key in [("A","A"),("B","B"),("C","C"),("D","D"),("A'","A1"),("C'","C1")]:
            self.add_label(name,C[key],size=20,off=(0.08,-0.08,0.05))
        ac1=solid(C["A"],C["C1"],GOLD,6.0)
        bd=aux(C["B"],C["D"],CYAN,5.0)
        P=cube_unit_map(1/3,1/3,1/3,side_display=3.25)
        Q=cube_unit_map(1/2,1/2,0,side_display=3.25)
        pq=solid(P,Q,GREEN,6.0)
        self.play(Create(ac1),Create(bd),Create(pq),FadeIn(Dot3D(P,radius=0.052,color=GREEN)),FadeIn(Dot3D(Q,radius=0.052,color=GREEN)),run_time=1.0)

        card=self.card("Chẩn đoán","d(AC',BD) trong lập phương",[
            ("math","u=(1,1,1)",27,CYAN),
            ("math","v=(-1,1,0)",27,CYAN),
            ("math","n=(-1,-1,2)",27,GREEN),
            ("math","P=(frac(1,3),frac(1,3),frac(1,3)) a",24,INK),
            ("math","Q=(frac(1,2),frac(1,2),0) a",24,INK),
            ("math","P Q=frac(a,sqrt(6))",34,GOLD),
        ],accent=RED,height=5.05)
        self.narrate(
            "Bài thứ năm là khoảng cách giữa AC phẩy và BD trong lập phương. Có thể giải hình học, nhưng Oxyz ở đây rất sạch. Đặt cạnh bằng a, chọn các trục theo ba cạnh của lập phương. Vectơ chỉ phương của AC phẩy là một một một, của BD là âm một một không. Tích có hướng cho một vectơ vuông góc chung âm một âm một hai. Từ điều kiện đoạn PQ vuông góc cả hai đường, ta tìm được P trên AC phẩy và Q trên BD như trên hình.",
            1.9,
        )
        self.narrate(
            "Độ dài PQ bằng a trên căn sáu. Đây là lúc Oxyz đáng dùng: hai đường chéo nhau, chân vuông góc chung khó nhìn, nhưng tọa độ của các đỉnh lại cực kỳ tự nhiên. Ngược lại, nếu bài đã có một tam giác vuông đẹp hoặc một mặt cắt vuông góc cạnh chung, ép Oxyz vào sẽ chỉ làm lời giải dài hơn. Quy tắc không phải là thích hình học hay thích tọa độ; quy tắc là chọn ngôn ngữ tạo ít biến phụ nhất và ít phép tính vô ích nhất.",
            2.0,
        )
        self.takeaway("Oxyz tốt khi tọa độ tự nhiên + quan hệ khó nhìn → phép tính ngắn")

    def exam_strategy(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Trong phòng thi — chọn công cụ trong 20 giây", "Sáu câu hỏi trước khi triển khai lời giải", "07/08")

        left = VGroup(
            txt("1. Đề hỏi đại lượng nào?",21,BLUE,BOLD),
            txt("2. Có song song / vuông góc / đối xứng?",19,INK),
            txt("3. Có mặt cắt phẳng đẹp không?",19,INK),
            txt("4. Có tỷ số thay cho số tuyệt đối?",19,INK),
            txt("5. Đại lượng động có thật sự thay đổi?",19,INK),
            txt("6. Oxyz / trải phẳng có ngắn hơn?",19,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.32).move_to(LEFT*2.65+UP*0.10)
        self.add_fixed_in_frame_mobjects(left)

        card=self.card("Bản đồ nhanh","Dấu hiệu → công cụ",[
            ("text","chân vuông góc khó → thể tích",17,CYAN,BOLD),
            ("text","nhị diện → mặt cắt vuông góc",17,CYAN,BOLD),
            ("text","cùng tỷ số → đồng dạng, k², k³",17,CYAN,BOLD),
            ("text","đường đi trên mặt → trải phẳng",17,CYAN,BOLD),
            ("text","hai đường chéo nhau → Oxyz hoặc mặt phụ",17,CYAN,BOLD),
            ("text","điểm động → bất biến trước",17,CYAN,BOLD),
        ],accent=GOLD,height=4.95)
        self.play(LaggedStart(*[FadeIn(x,shift=RIGHT*0.08) for x in left],lag_ratio=0.08),run_time=1.0)
        self.narrate(
            "Trong phòng thi, các em không cần nhớ một cây quyết định dài. Chỉ cần sáu câu hỏi trong khoảng hai mươi giây. Đề hỏi đại lượng gì. Có quan hệ song song, vuông góc hoặc đối xứng nào chưa khai thác. Có thể cắt hình bằng một mặt phẳng để đưa về hai chiều không. Có thể dùng tỷ số thay cho tính tuyệt đối không. Nếu có điểm động, đại lượng có thật sự thay đổi không. Và cuối cùng, Oxyz hoặc trải phẳng có làm lời giải ngắn hơn hình học thuần túy không.",
            1.9,
        )
        self.narrate(
            "Khi đã chọn được công cụ, lời giải nên đi theo một chuỗi ngắn: nêu quan hệ hình học, chứng minh đủ để hợp thức hóa công cụ, tính toán, rồi kiểm tra độ hợp lý. Đừng bỏ qua bước chứng minh chỉ vì hình vẽ trông có vẻ vuông góc hoặc song song. Và cũng đừng chứng minh quá nhiều thứ đề không cần. Một lời giải tốt không phải lời giải dài nhất; nó là lời giải mà mỗi dòng đều đẩy bài toán tiến gần đáp số hoặc xác nhận một điều kiện cần thiết.",
            1.9,
        )

    def synthesis(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Capstone — hệ thống đã khép kín", "20 video, một bản đồ tư duy thống nhất", "08/08")
        branches = VGroup(
            VGroup(txt("KHOẢNG CÁCH",18,BLUE,BOLD),txt("mặt phụ · thể tích · vuông góc chung",15,MUTED)).arrange(DOWN,buff=0.08),
            VGroup(txt("GÓC",18,CYAN,BOLD),txt("hình chiếu · cạnh chung · mặt cắt",15,MUTED)).arrange(DOWN,buff=0.08),
            VGroup(txt("THIẾT DIỆN",18,GREEN,BOLD),txt("đi theo mặt · song song · khép kín",15,MUTED)).arrange(DOWN,buff=0.08),
            VGroup(txt("THỂ TÍCH",18,ORANGE,BOLD),txt("đổi đỉnh · tỷ số · đồng dạng",15,MUTED)).arrange(DOWN,buff=0.08),
            VGroup(txt("ĐIỂM ĐỘNG",18,PURPLE,BOLD),txt("bất biến · miền · cực trị",15,MUTED)).arrange(DOWN,buff=0.08),
            VGroup(txt("OXYZ / TRẢI PHẲNG",18,RED,BOLD),txt("ngôn ngữ thứ hai khi thật sự ngắn",15,MUTED)).arrange(DOWN,buff=0.08),
        ).arrange_in_grid(rows=3,cols=2,buff=(0.85,0.50)).move_to(LEFT*2.6+UP*0.05)
        self.add_fixed_in_frame_mobjects(branches)
        card=self.card("Chốt series","Một câu cần nhớ",[
            ("text","Đừng hỏi: công thức nào?",19,MUTED,NORMAL),
            ("text","Hãy hỏi: cấu trúc nào?",23,GOLD,BOLD),
            ("sep",),
            ("text","Nhìn đúng cấu hình",18,CYAN,BOLD),
            ("text","→ chọn đúng mặt phẳng",18,CYAN,BOLD),
            ("text","→ lời giải tự ngắn lại",18,CYAN,BOLD),
        ],accent=GOLD,height=4.50)
        self.play(LaggedStart(*[FadeIn(b,shift=UP*0.08) for b in branches],lag_ratio=0.08),run_time=1.2)
        self.narrate(
            "Sau hai mươi video, hệ thống có thể thu về sáu nhánh: khoảng cách, góc, thiết diện, thể tích, điểm động và ngôn ngữ thay thế như Oxyz hoặc trải phẳng. Nhưng sâu hơn nữa, sáu nhánh này dùng chung một tư tưởng: hãy tìm cấu trúc làm bài toán giảm chiều. Một đường chiếu biến góc không gian thành góc phẳng. Một mặt cắt biến nhị diện thành tam giác. Một lần đổi đáy biến khoảng cách thành thể tích. Một phép trải phẳng biến đường gấp khúc thành đường thẳng. Một hệ trục tốt biến cấu hình khó nhìn thành vài vectơ ngắn.",
            2.1,
        )
        self.narrate(
            "Điều thầy mong các em giữ lại không phải hai mươi video riêng lẻ, mà là thói quen hỏi đúng câu trước khi tính. Nếu gặp bài lạ, đừng hoảng vì hình mới. Hãy hỏi nó thuộc nhánh nào, cấu trúc nào quen thuộc đang ẩn phía dưới, và cách nào chứng minh được với ít bước nhất. Khi nhìn đúng cấu hình, hình học không gian không còn là một kho mẹo rời rạc; nó trở thành một hệ thống có thể suy luận, kiểm tra và mở rộng.",
            2.0,
        )

        self.clear_all()
        end=VGroup(
            txt("HHKG CHUYÊN SÂU · 20/20",44,GOLD,BOLD),
            txt("BẢN ĐỒ ĐÃ KHÉP KÍN",31,INK,BOLD),
            txt("Nhìn cấu hình → chọn công cụ → chứng minh → tính → kiểm tra",23,CYAN,BOLD),
            txt(TEN_THAY,19,MUTED),
        ).arrange(DOWN,buff=0.27)
        fit_width(end,11.8)
        self.add_fixed_in_frame_mobjects(end)
        self.play(FadeIn(end),run_time=0.9)
        self.narrate(
            "Series hai mươi video đến đây đã hoàn chỉnh. Các em có thể quay lại từng chặng theo đúng nhu cầu: khoảng cách, góc, thể tích, thiết diện, khối tròn, điểm động, Oxyz hay luyện thi. Hãy dùng video capstone này như một bản đồ: khi quên một kỹ thuật, xác định nhánh trước rồi trở lại video chuyên sâu tương ứng. Chúc các em học hình học không gian ngày càng chắc, gọn và có lý do cho từng bước mình viết.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.decision_map()
        self.case_distance()
        self.case_angle()
        self.case_section()
        self.case_dynamic()
        self.case_oxyz()
        self.exam_strategy()
        self.synthesis()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_20_capstone_ban_do_phuong_phap_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim Community + native Typst (MathTypst) SAFE")
    print("Video 20/20: Capstone ban do phuong phap HHKG THPT")

    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_20.wav"
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

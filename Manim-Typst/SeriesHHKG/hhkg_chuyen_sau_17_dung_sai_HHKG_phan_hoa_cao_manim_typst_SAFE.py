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
# HHKG CHUYEN SAU 17 - DUNG/SAI HHKG PHAN HOA CAO
# Manim Community + MathTypst SAFE | Standalone 100%
# Muc tieu: 12-15 phut; 4 bo dung/sai tong hop, uu tien kiem chung ngan va phan vi du.
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
        series = txt("HHKG CHUYÊN SÂU · 17", 15, BLUE, BOLD)
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

    def angle_label(self, symbol, vertex, ray1, ray2, radius=0.58):
        u=np.array(ray1,dtype=float); v=np.array(ray2,dtype=float)
        u/=np.linalg.norm(u); v/=np.linalg.norm(v)
        d=u+v
        if np.linalg.norm(d)<1e-8:
            d=u
        else:
            d/=np.linalg.norm(d)
        lab=mty(symbol,18,GOLD).move_to(vertex+radius*d)
        self.add_fixed_orientation_mobjects(lab)
        return lab

    def tf_board(self, title, statements, accent=GOLD):
        bg = Rectangle(width=5.12, height=5.25, fill_color=PANEL, fill_opacity=0.91,
                       stroke_color=GRID, stroke_width=0.9, stroke_opacity=0.36)
        bg.move_to(RIGHT*4.28+DOWN*0.03)
        spine = Line(bg.get_corner(UL)+RIGHT*0.12+DOWN*0.18,
                     bg.get_corner(DL)+RIGHT*0.12+UP*0.18,
                     color=accent, stroke_width=3.8)
        head = txt(title, 21, INK, BOLD)
        head.move_to(bg.get_corner(UL)+RIGHT*0.34+DOWN*0.34, aligned_edge=LEFT)
        rows = VGroup()
        for label, expr in statements:
            lab = txt(label, 15, MUTED, BOLD)
            eq = fit_width(mty(expr, 22, INK), 3.45)
            row = VGroup(lab, eq).arrange(RIGHT, buff=0.11)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        rows.next_to(head, DOWN, buff=0.34, aligned_edge=LEFT)
        fit_height(rows, 4.18)
        group = VGroup(bg, spine, head, rows)
        self.add_fixed_in_frame_mobjects(group)
        return {"group":group, "rows":rows, "marks":[]}

    def reveal(self, board, idx, correct, note=None):
        row = board["rows"][idx]
        mark = txt("ĐÚNG" if correct else "SAI", 13, GREEN if correct else RED, BOLD)
        mark.move_to(np.array([6.18, row.get_center()[1], 0]))
        self.add_fixed_in_frame_mobjects(mark)
        self.play(FadeIn(mark, shift=LEFT*0.06), run_time=0.28)
        board["marks"].append(mark)
        if note:
            self.takeaway(note)
        return mark

    # ---------- geometry ----------
    def cube(self, a=3.0):
        A=phys(0,0,0); B=phys(a,0,0); C=phys(a,a,0); D=phys(0,a,0)
        A1=phys(0,0,a); B1=phys(a,0,a); C1=phys(a,a,a); D1=phys(0,a,a)
        visible=VGroup(solid(A,B),solid(B,C),solid(A,A1),solid(B,B1),solid(C,C1),
                       solid(A1,B1),solid(B1,C1),solid(C1,D1),solid(A1,D1))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(D,D1))
        dots=VGroup(*[Dot3D(p,radius=0.043,color=GOLD) for p in [A,B,C,D,A1,B1,C1,D1]])
        return {"A":A,"B":B,"C":C,"D":D,"A1":A1,"B1":B1,"C1":C1,"D1":D1,
                "edges":VGroup(visible,hidden),"dots":dots,"a":a}

    def pyramid(self):
        A=phys(0,0,0); B=phys(4,0,0); C=phys(4,4,0); D=phys(0,4,0); S=phys(0,0,3)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.055)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def tetra(self):
        P = regular_tetra_raw(scale=1.40)
        A,B,C,D=P["A"],P["B"],P["C"],P["D"]
        # Wireframe with a deliberately subdued back pair under the fixed camera.
        edges=VGroup(
            solid(A,B), solid(A,C), solid(A,D), solid(B,C),
            hidden_edge(B,D), hidden_edge(C,D)
        )
        dots=VGroup(*[Dot3D(P[k],radius=0.052,color=GOLD) for k in ["A","B","C","D"]])
        return {**P,"edges":edges,"dots":dots}

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_header("Đúng/Sai HHKG · Phân hóa cao",
                        "Không tính hết bài — chỉ kiểm chứng đúng lượng thông tin cần thiết",
                        "1/6")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Gọi đúng loại mệnh đề",21,INK,BOLD)).arrange(RIGHT,buff=0.15),
            VGroup(txt("2",18,GOLD,BOLD),txt("Tìm bất biến / song song / vuông góc",21,INK,BOLD)).arrange(RIGHT,buff=0.15),
            VGroup(txt("3",18,GOLD,BOLD),txt("Thử phản ví dụ hoặc giá trị biên",21,INK,BOLD)).arrange(RIGHT,buff=0.15),
            VGroup(txt("4",18,GOLD,BOLD),txt("Chỉ tính đến khi đủ kết luận",21,INK,BOLD)).arrange(RIGHT,buff=0.15),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.28).shift(LEFT*2.72+UP*0.12)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Chiến lược","Đúng/Sai là bài kiểm chứng, không phải bài tự luận",[
            ("math","perp, parallel, inter",27,CYAN),
            ("math","d, sin, tan, V, S",27,INK),
            ("sep",),
            ("text","Một mệnh đề sai chỉ cần một mâu thuẫn chắc chắn.",16,MUTED,NORMAL),
            ("text","Một mệnh đề đúng phải có chứng minh đủ mạnh.",16,MUTED,NORMAL),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.75)
        self.narrate(
            "Dạng đúng sai hình học không gian dễ khiến ta sa vào việc giải lại toàn bộ bài. Cách làm hiệu quả hơn là coi mỗi mệnh đề như một bài kiểm chứng độc lập. Trước hết xác định nó thuộc nhóm nào: vuông góc, song song, khoảng cách, góc, thể tích hay thiết diện. Sau đó tìm cấu trúc mạnh nhất có thể quyết định nhanh, chẳng hạn hình chiếu, mặt cắt vuông góc, tỷ số đồng dạng, hoặc một hệ trục ngắn.",
            2.0,
        )
        self.narrate(
            "Video này gồm bốn bộ mệnh đề trên bốn cấu hình quen nhưng đủ độ phân hóa: lập phương, tứ diện đều, hình chóp vuông và thiết diện song song đáy. Ta sẽ không tính thừa. Mỗi khi có thể bác bỏ bằng một hệ thức ngắn, một giá trị biên hoặc một kết quả cấu trúc, ta dừng ngay. Mục tiêu là xây phản xạ chọn công cụ, không phải ghi nhớ đáp án.",
            2.0,
        )

    # ======================================================
    # SET 1: CUBE
    # ======================================================
    def cube_set(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bộ 1 · Hình lập phương","Một cấu hình, bốn mệnh đề về vuông góc — khoảng cách — góc","2/6")
        G=self.cube(3.0); self.add(G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.12,-0.10,0),17),("B",G["B"],GOLD,(0.10,-0.10,0),17),
            ("C",G["C"],GOLD,(0.10,0.10,0),17),("D",G["D"],GOLD,(-0.15,0.10,0),17),
            ("A'",G["A1"],GOLD,(-0.14,-0.04,0.10),17),("B'",G["B1"],GOLD,(0.09,-0.05,0.10),17),
            ("C'",G["C1"],GOLD,(0.10,0.08,0.10),17),("D'",G["D1"],GOLD,(-0.14,0.08,0.10),17),
        ])
        board=self.tf_board("BỘ 1 · CẠNH a",[
            ("A.","A C' perp B D"),
            ("B.","d(A C', B D)=frac(a,sqrt(6))"),
            ("C.","tan alpha = frac(1,sqrt(2))"),
            ("D.","beta=frac(pi,3)"),
        ],accent=BLUE)

        ac1=solid(G["A"],G["C1"],GOLD,6.1,1.0)
        bd=hidden_edge(G["B"],G["D"],CYAN,4.8,0.95,0.12)
        self.play(Create(ac1),Create(bd),run_time=0.65)
        self.narrate(
            "Mệnh đề A hỏi AC phẩy có vuông góc BD hay không. Không cần dựng góc giữa hai đường chéo nhau. Ta chỉ cần so hướng. Vectơ chỉ phương của AC phẩy có thể lấy là một, một, một; còn BD là âm một, một, không. Tích vô hướng bằng không. Vì vậy hai hướng vuông góc, và mệnh đề A đúng.",
            1.6,
        )
        self.reveal(board,0,True)

        a=3.0
        P=phys(a/3,a/3,a/3); Q=phys(a/2,a/2,0)
        pq=solid(P,Q,GREEN,6.0,1.0); dp=Dot3D(P,radius=0.05,color=GREEN); dq=Dot3D(Q,radius=0.05,color=GREEN)
        self.play(Create(pq),FadeIn(dp),FadeIn(dq),run_time=0.55)
        self.narrate(
            "Mệnh đề B là khoảng cách giữa hai đường chéo nhau. Đoạn vuông góc chung nối P trên AC phẩy với Q trên BD. Tọa độ chuẩn hóa cho P bằng một phần ba, một phần ba, một phần ba lần a; Q bằng một phần hai, một phần hai, không lần a. Hiệu hai điểm có độ dài a trên căn sáu. Vì vậy mệnh đề B cũng đúng.",
            1.7,
        )
        self.reveal(board,1,True)

        ac=aux(G["A"],G["C"],CYAN,4.4,0.95)
        arc=angle_arc_3d(G["A"],G["C"]-G["A"],G["C1"]-G["A"],radius=0.38,color=GOLD,width=5.2)
        self.angle_label("alpha",G["A"],G["C"]-G["A"],G["C1"]-G["A"],0.60)
        self.play(Create(ac),Create(arc),run_time=0.5)
        self.narrate(
            "Mệnh đề C xét góc alpha giữa AC phẩy và mặt đáy. Hình chiếu của AC phẩy xuống đáy là AC, nên trên hình góc phẳng đúng là góc C A C phẩy. Tam giác ACC phẩy vuông có AC bằng a căn hai và CC phẩy bằng a, do đó tang alpha bằng một trên căn hai. Mệnh đề C đúng. Chú ý cung góc được đặt đúng tại A giữa hai tia AC và AC phẩy.",
            1.8,
        )
        self.reveal(board,2,True)

        O=(G["A"]+G["C"])/2
        plane=face(G["A"],G["C"],G["D1"],color=PURPLE,opacity=0.15,stroke=PURPLE,stroke_width=2.0)
        od=solid(O,G["D"],CYAN,4.4,0.95); od1=solid(O,G["D1"],PURPLE,4.8,0.95)
        arc2=angle_arc_3d(O,G["D"]-O,G["D1"]-O,radius=0.34,color=GOLD,width=5.2)
        self.angle_label("beta",O,G["D"]-O,G["D1"]-O,0.56)
        self.play(FadeIn(plane),Create(od),Create(od1),Create(arc2),run_time=0.65)
        self.narrate(
            "Mệnh đề D nói góc giữa mặt ACD phẩy và đáy bằng sáu mươi độ. Đây là chỗ dễ bị hình vẽ đánh lừa. Góc phẳng đúng là D O D phẩy, với O là trung điểm AC. Ta có OD bằng a trên căn hai và DD phẩy bằng a, nên tang beta bằng căn hai. Vì tang sáu mươi độ là căn ba, beta không thể bằng sáu mươi độ. Mệnh đề D sai.",
            1.8,
        )
        self.reveal(board,3,False)
        self.takeaway("Đúng/Sai về góc: dựng đúng hình chiếu hoặc mặt cắt trước, đừng ước lượng bằng mắt.")

    # ======================================================
    # SET 2: REGULAR TETRAHEDRON
    # ======================================================
    def tetra_set(self):
        self.clear_all()
        self.set_camera_orientation(phi=70*DEGREES, theta=-42*DEGREES, zoom=1.0)
        self.add_header("Bộ 2 · Tứ diện đều","Cạnh đối — đường vuông góc chung — khối tám mặt trung tâm","3/6")
        G=self.tetra(); self.add(G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(0.10,0.10,0.10),17),("B",G["B"],GOLD,(0.10,-0.10,-0.05),17),
            ("C",G["C"],GOLD,(-0.14,0.10,-0.05),17),("D",G["D"],GOLD,(-0.14,-0.10,0.10),17),
        ])
        board=self.tf_board("BỘ 2 · TỨ DIỆN ĐỀU CẠNH a",[
            ("A.","A B perp C D"),
            ("B.","d(A B,C D)=frac(a,sqrt(2))"),
            ("C.","M N=frac(a,2)"),
            ("D.","V_O=frac(1,2)V"),
        ],accent=PURPLE)

        ab=solid(G["A"],G["B"],GOLD,6.0,1.0); cd=hidden_edge(G["C"],G["D"],CYAN,5.0,0.98,0.12)
        self.play(Create(ab),Create(cd),run_time=0.55)
        self.narrate(
            "Trong tứ diện đều, mệnh đề A nói hai cạnh đối AB và CD vuông góc. Ta có thể kiểm tra bằng đối xứng hoặc bằng một hệ tọa độ đối xứng rất ngắn. Với mô hình các đỉnh cộng trừ một, hướng AB tỉ lệ với không, âm một, âm một; hướng CD tỉ lệ với không, âm một, một. Tích vô hướng bằng không. Vì vậy A đúng.",
            1.6,
        )
        self.reveal(board,0,True)

        M=(G["A"]+G["B"])/2; N=(G["C"]+G["D"])/2
        mn=solid(M,N,GREEN,6.2,1.0); dm=Dot3D(M,radius=0.052,color=GREEN); dn=Dot3D(N,radius=0.052,color=GREEN)
        self.play(Create(mn),FadeIn(dm),FadeIn(dn),run_time=0.55)
        self.add_label("M",M,GREEN,(0.05,0.08,0.05),16); self.add_label("N",N,GREEN,(-0.10,-0.08,0.05),16)
        self.narrate(
            "Gọi M, N là trung điểm của hai cạnh đối. Đoạn MN vuông góc cả AB lẫn CD nên chính là đường vuông góc chung. Trong một mặt phẳng phù hợp, hoặc từ tọa độ đối xứng, ta được MN bằng a trên căn hai. Vì vậy mệnh đề B đúng. Đồng thời mệnh đề C nói MN bằng a trên hai là sai; chỉ cần so hai giá trị đã đủ kết luận, không cần làm thêm.",
            1.8,
        )
        self.reveal(board,1,True); self.reveal(board,2,False)

        mids={
            "AB":M,
            "AC":(G["A"]+G["C"])/2,
            "AD":(G["A"]+G["D"])/2,
            "BC":(G["B"]+G["C"])/2,
            "BD":(G["B"]+G["D"])/2,
            "CD":N,
        }
        opp={frozenset(["AB","CD"]),frozenset(["AC","BD"]),frozenset(["AD","BC"])}
        oct_edges=VGroup()
        keys=list(mids)
        for i in range(len(keys)):
            for j in range(i+1,len(keys)):
                if frozenset([keys[i],keys[j]]) in opp:
                    continue
                oct_edges.add(solid(mids[keys[i]],mids[keys[j]],GOLD,3.5,0.84))
        self.play(Create(oct_edges),run_time=0.9)
        self.narrate(
            "Mệnh đề D xét khối tám mặt nối sáu trung điểm. Cách nhanh nhất không phải tính thể tích khối tám mặt trực tiếp. Bốn tứ diện ở bốn đỉnh đều đồng dạng với tứ diện ban đầu theo tỷ số một phần hai, nên mỗi khối có thể tích một phần tám V. Bốn khối góc chiếm đúng một phần hai V; phần còn lại, tức khối tám mặt trung tâm, cũng bằng một phần hai V. Mệnh đề D đúng.",
            2.0,
        )
        self.reveal(board,3,True)
        self.takeaway("Tứ diện đều: khai thác đối xứng và đồng dạng trước khi lao vào tọa độ dài.")

    # ======================================================
    # SET 3: RIGHT PYRAMID
    # ======================================================
    def pyramid_set(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bộ 3 · Hình chóp vuông","Khoảng cách — góc nhị diện — góc đường mặt — bất biến","4/6")
        G=self.pyramid(); self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.14,-0.12,0),17),("B",G["B"],GOLD,(0.10,-0.12,0),17),
            ("C",G["C"],GOLD,(0.10,0.10,0),17),("D",G["D"],GOLD,(-0.14,0.10,0),17),
            ("S",G["S"],RED,(-0.12,-0.06,0.12),18),
        ])
        plane=face(G["S"],G["B"],G["C"],color=PURPLE,opacity=0.14,stroke=PURPLE,stroke_width=2.0)
        self.add(plane)
        board=self.tf_board("BỘ 3 · AB=4, SA=3",[
            ("A.","d(D,(S B C))=frac(12,5)"),
            ("B.","tan beta = frac(3,4)"),
            ("C.","tan alpha = frac(3,4)"),
            ("D.","d(M,(S B C))=frac(12,5)"),
        ],accent=GOLD)

        H_phys=foot_to_plane_physical(np.array([0.,4.,0.]),np.array([3.,0.,4.]),-12.0)
        H=phys(*H_phys)
        dh=solid(G["D"],H,GREEN,6.0,1.0); hd=Dot3D(H,radius=0.05,color=GREEN)
        self.play(Create(dh),FadeIn(hd),run_time=0.5)
        self.narrate(
            "Mệnh đề A là khoảng cách từ D tới mặt SBC. Ta có thể dùng thể tích hoặc phương trình mặt phẳng; cả hai cho mười hai phần năm. Trên hình, H là chân chiếu thật của D lên mặt SBC. Vì vậy A đúng. Ở dạng đúng sai, khi đã có một kết quả chắc chắn từ công thức ngắn, không cần dựng tiếp tọa độ của H nếu đề không hỏi.",
            1.6,
        )
        self.reveal(board,0,True)

        ba=solid(G["B"],G["A"],CYAN,5.0,0.95); bs=solid(G["B"],G["S"],GREEN,5.0,0.95)
        arc=angle_arc_3d(G["B"],G["A"]-G["B"],G["S"]-G["B"],radius=0.40,color=GOLD,width=5.4)
        self.angle_label("beta",G["B"],G["A"]-G["B"],G["S"]-G["B"],0.62)
        self.play(Create(ba),Create(bs),Create(arc),run_time=0.55)
        self.narrate(
            "Mệnh đề B nói tang góc nhị diện giữa mặt SBC và đáy theo cạnh BC bằng ba phần bốn. Vì BA và BS cùng vuông góc BC, góc phẳng của nhị diện là góc A B S. Tam giác SAB là tam giác vuông ba, bốn, năm nên tang beta bằng SA trên AB, tức ba phần bốn. B đúng.",
            1.7,
        )
        self.reveal(board,1,True)

        ac=aux(G["A"],G["C"],CYAN,4.3,0.95); sc=solid(G["S"],G["C"],GOLD,5.6,1.0)
        arc2=angle_arc_3d(G["C"],G["A"]-G["C"],G["S"]-G["C"],radius=0.42,color=GOLD,width=5.2)
        self.angle_label("alpha",G["C"],G["A"]-G["C"],G["S"]-G["C"],0.63)
        self.play(Create(ac),Create(sc),Create(arc2),run_time=0.55)
        self.narrate(
            "Mệnh đề C rất giống B nhưng không được bê nguyên tỷ số ba phần bốn. Góc giữa SC và đáy dùng hình chiếu AC, không dùng AB. Vì AC bằng bốn căn hai, tang alpha phải bằng ba trên bốn căn hai. Do đó mệnh đề C sai. Đây là kiểu bẫy đổi đúng một cạnh trong tam giác vuông nhưng giữ nguyên con số cũ.",
            1.7,
        )
        self.reveal(board,2,False)

        u=ValueTracker(0.15)
        M=always_redraw(lambda: Dot3D(phys(0,4*u.get_value(),0),radius=0.055,color=ORANGE))
        def foot_m():
            p=np.array([0.,4*u.get_value(),0.])
            h=foot_to_plane_physical(p,np.array([3.,0.,4.]),-12.0)
            return phys(*h)
        mh=always_redraw(lambda: solid(phys(0,4*u.get_value(),0),foot_m(),ORANGE,5.0,0.95))
        self.add(M,mh)
        self.play(u.animate.set_value(0.85),run_time=2.2,rate_func=linear)
        self.play(u.animate.set_value(0.35),run_time=1.4,rate_func=linear)
        self.narrate(
            "Mệnh đề D cho M chạy trên AD và khẳng định khoảng cách từ M tới mặt SBC luôn bằng mười hai phần năm. Vì AD song song BC, mà BC nằm trong mặt SBC, nên AD song song với mặt SBC. Mọi điểm trên đường thẳng AD có cùng khoảng cách tới mặt phẳng đó. Animation cho thấy chân vuông góc trượt theo nhưng độ dài đoạn vuông góc không đổi. D đúng.",
            1.9,
        )
        self.reveal(board,3,True)
        self.takeaway("Một điểm chạy chưa chắc tạo đại lượng động: hãy kiểm tra song song và bất biến trước.")

    # ======================================================
    # SET 4: PARALLEL SECTION
    # ======================================================
    def section_set(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bộ 4 · Thiết diện song song đáy","Bẫy bậc một — bậc hai — bậc ba","5/6")
        G=self.pyramid(); self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.14,-0.12,0),16),("B",G["B"],GOLD,(0.10,-0.12,0),16),
            ("C",G["C"],GOLD,(0.10,0.10,0),16),("D",G["D"],GOLD,(-0.14,0.10,0),16),
            ("S",G["S"],RED,(-0.12,-0.06,0.12),17),
        ])
        board=self.tf_board("BỘ 4 · CÙNG TỶ SỐ k",[
            ("A.","(M N P Q) parallel (A B C D)"),
            ("B.","frac(S_(M N P Q),S_(A B C D))=k"),
            ("C.","frac(V_(S M N P Q),V_(S A B C D))=k^3"),
            ("D.","k=frac(1,2), frac(V_f,V)=frac(3,4)"),
        ],accent=GREEN)

        k=ValueTracker(0.34)
        def sec_pts():
            kk=k.get_value(); S=G["S"]
            return [S+kk*(G[x]-S) for x in ["A","B","C","D"]]
        section=always_redraw(lambda: face(*sec_pts(),color=GOLD,opacity=0.26,stroke=GOLD,stroke_width=2.4))
        sec_edges=always_redraw(lambda: VGroup(*[solid(sec_pts()[i],sec_pts()[(i+1)%4],GOLD,4.8,1.0) for i in range(4)]))
        self.add(section,sec_edges)
        self.play(k.animate.set_value(0.72),run_time=2.2,rate_func=linear)
        self.play(k.animate.set_value(0.50),run_time=1.2,rate_func=smooth)
        self.narrate(
            "Bộ cuối cùng dùng bốn điểm M, N, P, Q trên các cạnh SA, SB, SC, SD với cùng tỷ số k tính từ S. Vì bốn cạnh đều bị cắt theo cùng tỷ số, thiết diện MNPQ song song đáy ABCD. Mệnh đề A đúng. Animation cho thấy mặt cắt luôn giữ cùng hướng với đáy khi k thay đổi.",
            1.7,
        )
        self.reveal(board,0,True)

        self.narrate(
            "Mệnh đề B là bẫy bậc. Tỷ số độ dài bằng k, nhưng diện tích của hai hình đồng dạng phải theo bình phương tỷ số dài. Do đó diện tích MNPQ trên diện tích ABCD bằng k bình phương, không phải k. B sai. Chỉ cần nhận diện đồng dạng là đủ; không cần tính bất kỳ cạnh cụ thể nào.",
            1.6,
        )
        self.reveal(board,1,False)

        self.narrate(
            "Mệnh đề C chuyển sang thể tích. Hai hình chóp S.MNPQ và S.ABCD đồng dạng theo tỷ số k, nên tỷ số thể tích bằng k mũ ba. C đúng. Đây là chuỗi cần thuộc về cấu trúc chứ không phải thuộc lòng riêng lẻ: độ dài bậc một, diện tích bậc hai, thể tích bậc ba.",
            1.6,
        )
        self.reveal(board,2,True)

        self.narrate(
            "Mệnh đề D cho k bằng một phần hai và nói phần chóp cụt còn lại chiếm ba phần tư thể tích. Ta thử ngay giá trị đặc biệt: chóp nhỏ phía trên chiếm một phần hai mũ ba, tức một phần tám. Phần còn lại phải là bảy phần tám, không phải ba phần tư. D sai. Đây là ví dụ điển hình của chiến lược thay giá trị đơn giản để bác bỏ mệnh đề rất nhanh.",
            1.7,
        )
        self.reveal(board,3,False)
        self.takeaway("Thiết diện đồng dạng: k — k² — k³. Sai một bậc là sai cả mệnh đề.")

    # ======================================================
    # SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_header("Bản đồ kiểm chứng Đúng/Sai","Năm câu hỏi để giảm tính toán và tăng độ chắc chắn","6/6")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Có hình chiếu / mặt cắt chuẩn không?",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Có bất biến hoặc song song không?",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Có thể thử giá trị biên / đặc biệt không?",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Có đối xứng / đồng dạng không?",20,INK)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Oxyz có làm lời giải ngắn hơn không?",20,INK)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.27).shift(LEFT*2.70+UP*0.16)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Kết quả","Bốn bộ — mười sáu mệnh đề",[
            ("text","Bộ 1",15,MUTED,BOLD),("text","Đ · Đ · Đ · S",22,GOLD,BOLD),
            ("text","Bộ 2",15,MUTED,BOLD),("text","Đ · Đ · S · Đ",22,GOLD,BOLD),
            ("text","Bộ 3",15,MUTED,BOLD),("text","Đ · Đ · S · Đ",22,GOLD,BOLD),
            ("text","Bộ 4",15,MUTED,BOLD),("text","Đ · S · Đ · S",22,GOLD,BOLD),
        ],accent=GREEN)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.75)
        self.narrate(
            "Qua mười sáu mệnh đề, ta đã dùng gần như toàn bộ kho công cụ của series mà không phải giải dài. Lập phương cần vectơ ngắn và hình chiếu đúng. Tứ diện đều ưu tiên đối xứng, trung điểm và đồng dạng. Hình chóp vuông cho thấy hai mệnh đề nhìn gần giống nhau có thể dùng hai tam giác hoàn toàn khác nhau. Thiết diện song song đáy nhắc ta phân biệt bậc một, bậc hai và bậc ba.",
            2.0,
        )
        self.narrate(
            "Khi làm đúng sai, mệnh đề sai thường được phát hiện nhanh nhất bằng một mâu thuẫn cấu trúc, một giá trị đặc biệt hoặc một đại lượng có thứ nguyên không phù hợp. Mệnh đề đúng thì cần một lập luận đủ mạnh: song song thật, vuông góc thật, hình chiếu đúng, hoặc một công thức đã được dựng từ cấu hình. Đừng dùng hình vẽ như bằng chứng; hình chỉ giúp chọn đường suy luận.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 18",17,BLUE,BOLD),
            txt("TRẢ LỜI NGẮN HHKG · TỪ CẤU HÌNH ĐẾN ĐÁP SỐ",24,GOLD,BOLD),
            txt("Ít dòng — đủ chứng minh — kiểm soát sai số và đơn vị",18,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box)
        self.play(FadeIn(next_box),run_time=0.55)
        self.narrate(
            "Video mười tám sẽ chuyển sang dạng trả lời ngắn. Khi không còn bốn mệnh đề gợi ý, ta phải tự nhận diện cấu hình và tự chọn đại lượng cần tính, nhưng vẫn giữ nguyên triết lý: dựng vừa đủ, tính vừa đủ và kiểm tra đáp số bằng đơn vị, miền giá trị hoặc một cách giải thứ hai khi cần.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.cube_set()
        self.tetra_set()
        self.pyramid_set()
        self.section_set()
        self.synthesis()


def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_17_dung_sai_HHKG_phan_hoa_cao_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 17")
    print("Themes: true-false strategy, cube, regular tetrahedron, right pyramid, parallel section")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_17.wav"
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

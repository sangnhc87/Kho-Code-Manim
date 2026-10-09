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
# HHKG CHUYEN SAU 12 - THIET DIEN III: DIEM DONG, THAM SO, CUC TRI
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
        self.audio_events=[]
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)

    # ---------- audio ----------
    def narrate(self,text,min_visual_time=1.0):
        audio=create_audio(text); dur=probe_duration(audio)
        self.audio_events.append((self.time,audio)); self.wait(max(dur,min_visual_time)); return dur

    def narrate_play(self,text,*animations,min_time=1.0,rate_func=linear):
        audio=create_audio(text); dur=probe_duration(audio)
        self.audio_events.append((self.time,audio))
        self.play(*animations,run_time=max(dur,min_time),rate_func=rate_func); return dur

    # ---------- fixed UI ----------
    def clear_all(self):
        mobs=list(self.mobjects)
        if mobs: self.play(*[FadeOut(m) for m in mobs],run_time=0.30)
        self.clear()

    def add_header(self,title,subtitle,progress):
        series=txt("HHKG CHUYÊN SÂU · 12",15,BLUE,BOLD)
        series.to_edge(UP,buff=0.16).to_edge(LEFT,buff=0.30)
        title_m=fit_width(txt(title,29,INK,BOLD),8.9); title_m.next_to(series,DOWN,buff=0.045,aligned_edge=LEFT)
        sub_m=fit_width(txt(subtitle,17,MUTED),8.9); sub_m.next_to(title_m,DOWN,buff=0.045,aligned_edge=LEFT)
        accent=Line(series.get_left()+DOWN*0.13,series.get_left()+RIGHT*0.62+DOWN*0.13,color=GOLD,stroke_width=3.2)
        prog=txt(progress,15,MUTED,BOLD); prog.to_edge(UP,buff=0.20).to_edge(RIGHT,buff=0.32)
        rule=Line(LEFT*6.82,RIGHT*6.82,color=GRID,stroke_width=0.9,stroke_opacity=0.42).shift(UP*2.78)
        divider=Line(np.array([1.50,-2.83,0]),np.array([1.50,2.64,0]),color=GRID,stroke_width=1.0,stroke_opacity=0.42)
        teacher=txt(TEN_THAY,15,MUTED); teacher.to_edge(DOWN,buff=0.10).to_edge(LEFT,buff=0.30)
        hud=VGroup(series,title_m,sub_m,accent,prog,rule,divider,teacher)
        self.add_fixed_in_frame_mobjects(hud); return hud

    def card(self,kicker,title,items,accent=GOLD,height=5.25,auto_add=True):
        bg=Rectangle(width=5.12,height=height,fill_color=PANEL,fill_opacity=0.90,stroke_color=GRID,stroke_width=0.9,stroke_opacity=0.36).move_to(RIGHT*4.28+DOWN*0.03)
        spine=Line(bg.get_corner(UL)+RIGHT*0.12+DOWN*0.18,bg.get_corner(DL)+RIGHT*0.12+UP*0.18,color=accent,stroke_width=3.8,stroke_opacity=0.95)
        k=txt(kicker.upper(),14,accent,BOLD); k.move_to(bg.get_corner(UL)+RIGHT*0.36+DOWN*0.30,aligned_edge=LEFT)
        t=fit_width(txt(title,23,INK,BOLD),4.30); t.next_to(k,DOWN,buff=0.10,aligned_edge=LEFT)
        body=VGroup()
        for item in items:
            kind=item[0]
            if kind=="text": _,s,size,color,weight=item; mob=txt(s,size,color,weight)
            elif kind=="math": _,expr,size,color=item; mob=mty(expr,size,color)
            elif kind=="sep": mob=Line(LEFT*2.00,RIGHT*2.00,color=GRID,stroke_width=0.9,stroke_opacity=0.55)
            elif kind=="obj": mob=item[1]
            else: raise ValueError(kind)
            body.add(fit_width(mob,4.28))
        body.arrange(DOWN,aligned_edge=LEFT,buff=0.18); body.next_to(t,DOWN,buff=0.22,aligned_edge=LEFT); fit_height(body,height-1.45)
        group=VGroup(bg,spine,k,t,body)
        if auto_add: self.add_fixed_in_frame_mobjects(group)
        return group

    def takeaway(self,s):
        label=fit_width(txt(s,16,CYAN,BOLD),7.15); label.move_to(LEFT*2.55+DOWN*2.52)
        self.add_fixed_in_frame_mobjects(label); return label

    def add_label(self,name,pt,color=GOLD,off=(0.10,-0.10,0.05),size=22):
        lab=mty(name,size,color).move_to(pt+np.array(off,dtype=float)); self.add_fixed_orientation_mobjects(lab); return lab

    def label_many(self,data):
        return VGroup(*[self.add_label(*item) for item in data])

    # ---------- models ----------
    def regular_tetra(self):
        G=regular_tetra_raw()
        A,B,C,D=G["A"],G["B"],G["C"],G["D"]
        # fixed camera: one back edge is dashed; all section lines have their own highlight style
        edges=VGroup(solid(A,B),solid(A,C),solid(A,D),solid(D,B),solid(D,C),hidden_edge(B,C))
        faces=VGroup(face(A,B,C,color=BLUE,opacity=0.035),face(A,D,C,color=PURPLE,opacity=0.025))
        dots=VGroup(*[Dot3D(G[x],radius=0.05,color=GOLD) for x in ["A","B","C","D"]])
        return {**G,"edges":edges,"faces":faces,"dots":dots}

    def square_pyramid(self):
        A=L(-2,-2,0); B=L(2,-2,0); C=L(2,2,0); D=L(-2,2,0); S=L(0,0,3.2)
        visible=VGroup(solid(A,B),solid(B,C),solid(S,A),solid(S,B),solid(S,C))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(S,D))
        base=face(A,B,C,D,color=BLUE,opacity=0.06)
        dots=VGroup(*[Dot3D(p,radius=0.05,color=GOLD) for p in [A,B,C,D]],Dot3D(S,radius=0.06,color=RED))
        return {"A":A,"B":B,"C":C,"D":D,"S":S,"edges":VGroup(visible,hidden),"base":base,"dots":dots}

    def cube_dynamic(self):
        G=cube_unit_vertices()
        A,B,C,D,A1,B1,C1,D1=[G[k] for k in ["A","B","C","D","A1","B1","C1","D1"]]
        visible=VGroup(solid(A,B),solid(B,C),solid(B,B1),solid(A,A1),solid(A1,B1),solid(B1,C1),solid(C,C1),solid(C1,D1),solid(A1,D1))
        hidden=VGroup(hidden_edge(C,D),hidden_edge(D,A),hidden_edge(D,D1))
        faces=VGroup(face(A,B,C,D,color=BLUE,opacity=0.025),face(A1,B1,C1,D1,color=PURPLE,opacity=0.025))
        dots=VGroup(*[Dot3D(p,radius=0.04,color=GOLD) for p in [A,B,C,D,A1,B1,C1,D1]])
        return {**G,"edges":VGroup(visible,hidden),"faces":faces,"dots":dots}

    def add_tetra_labels(self,G):
        return self.label_many([
            ("A",G["A"],GOLD,(0.11,0.10,0.08),18),("B",G["B"],GOLD,(0.13,-0.08,-0.03),18),
            ("C",G["C"],GOLD,(-0.14,0.08,-0.03),18),("D",G["D"],GOLD,(-0.16,-0.08,0.08),18),
        ])

    def add_pyramid_labels(self,G):
        return self.label_many([
            ("S",G["S"],RED,(-0.10,-0.03,0.12),20),("A",G["A"],GOLD,(-0.15,-0.10,0),18),
            ("B",G["B"],GOLD,(0.12,-0.10,0),18),("C",G["C"],GOLD,(0.12,0.10,0),18),("D",G["D"],GOLD,(-0.15,0.10,0),18),
        ])

    # ======================================================
    # 1. INTRO
    # ======================================================
    def intro(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        title=txt("HHKG CHUYÊN SÂU 12",45,GOLD,BOLD)
        sub=txt("THIẾT DIỆN III · ĐIỂM ĐỘNG, THAM SỐ & CỰC TRỊ",31,INK,BOLD)
        line=txt("Khi mặt phẳng cắt chuyển động, hình cắt có thể đổi cả số cạnh",22,CYAN,BOLD)
        note=txt("Dựng đúng → lập hàm → xét từng miền → tìm cực trị",22,MUTED)
        brand=txt(TEN_THAY,18,MUTED)
        g=VGroup(title,sub,line,note,brand).arrange(DOWN,buff=0.28)
        self.play(FadeIn(title,shift=UP*0.15),FadeIn(sub),run_time=0.9); self.play(FadeIn(line),FadeIn(note),FadeIn(brand),run_time=0.8)
        self.narrate(
            "Video mười hai khép lại chặng thiết diện bằng phần khó nhất: mặt phẳng cắt chuyển động. Khi tham số thay đổi, không chỉ độ dài và diện tích đổi theo; chính hình dạng thiết diện có thể đổi từ tam giác sang lục giác rồi trở lại tam giác. Vì thế ta phải làm ba việc theo đúng thứ tự: xác định kiểu thiết diện trên từng khoảng của tham số, lập công thức diện tích tương ứng, rồi mới tìm cực trị. Đây là chỗ hình học không gian gặp tư duy hàm số rất rõ ràng.",
            2.0,
        )

    # ======================================================
    # 2. TOOLKIT
    # ======================================================
    def toolkit(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ xử lý thiết diện động","Không lập một công thức duy nhất khi hình cắt đã đổi kiểu","1/6")
        left=VGroup(
            txt("BƯỚC 1",15,GOLD,BOLD),txt("Tìm các mốc tham số làm mặt cắt đi qua đỉnh/cạnh",20,INK,BOLD),
            txt("BƯỚC 2",15,GOLD,BOLD),txt("Chia miền: mỗi miền giữ nguyên số đỉnh thiết diện",20,INK,BOLD),
            txt("BƯỚC 3",15,GOLD,BOLD),txt("Lập S(t), V(t), chu vi... theo từng miền",20,INK,BOLD),
            txt("BƯỚC 4",15,GOLD,BOLD),txt("Tìm cực trị và kiểm tra tại các mốc chuyển kiểu",20,INK,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.18).shift(LEFT*2.65+UP*0.10)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Nguyên tắc","Một tham số — nhiều công thức",[
            ("math","0 < t < 1",28,CYAN),
            ("math","1 < t < 2",28,CYAN),
            ("math","2 < t < 3",28,CYAN),
            ("sep",),
            ("text","Nếu số cạnh của thiết diện đổi, công thức diện tích cũng phải đổi.",16,MUTED,NORMAL),
        ],accent=BLUE)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.7)
        self.narrate(
            "Quy tắc đầu tiên của bài tham số là tìm các mốc hình học, không phải đạo hàm ngay. Mốc xuất hiện khi mặt phẳng cắt đi qua một đỉnh hoặc khi một giao điểm chuyển từ cạnh này sang cạnh khác. Giữa hai mốc liên tiếp, số đỉnh của thiết diện thường ổn định và ta mới có một công thức diện tích duy nhất. Khi qua mốc, phải dựng lại hình cắt và lập công thức mới.",
            2.0,
        )
        self.narrate(
            "Vì vậy, nếu thấy đề có một tham số t điều khiển mặt phẳng, hãy tự hỏi trước: với t nhỏ thiết diện là gì, ở t bằng một giá trị đặc biệt mặt phẳng đi qua đỉnh nào, và sau mốc đó đa giác cắt có thêm hay mất cạnh hay không. Chỉ riêng việc chia đúng miền đã quyết định hơn nửa lời giải.",
            1.8,
        )

    # ======================================================
    # 3. REGULAR TETRAHEDRON: MOVING RECTANGLE
    # ======================================================
    def tetra_moving_rectangle(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-47*DEGREES,zoom=0.96)
        self.add_header("Bài 1 · Tứ diện đều và thiết diện chữ nhật","Mặt cắt song song hai cạnh đối — cực trị diện tích","2/6")
        G=self.regular_tetra(); self.add(G["faces"],G["edges"],G["dots"]); self.add_tetra_labels(G)
        A,B,C,D=G["A"],G["B"],G["C"],G["D"]
        lam=ValueTracker(0.22)

        def pts():
            u=lam.get_value()
            M=A+u*(B-A); N=A+u*(C-A); P=D+u*(C-D); Q=D+u*(B-D)
            return M,N,P,Q
        sec=always_redraw(lambda: Polygon(*pts(),fill_color=GOLD,fill_opacity=0.22,stroke_color=GOLD,stroke_width=4.5))
        sdots=always_redraw(lambda: VGroup(*[Dot3D(x,radius=0.048,color=GOLD) for x in pts()]))
        self.add(sec,sdots)
        lam_num=always_redraw(lambda: txt(f"{lam.get_value():.2f}", 19, GOLD, BOLD))
        area_num=always_redraw(lambda: txt(f"{lam.get_value()*(1-lam.get_value()):.3f}", 19, CYAN, BOLD))
        read=VGroup(txt("λ =",19,MUTED,BOLD),lam_num,txt("   S/a² =",19,MUTED,BOLD),area_num).arrange(RIGHT,buff=0.10).move_to(LEFT*2.55+DOWN*2.38)
        self.add_fixed_in_frame_mobjects(read)
        self.card("Cấu trúc","MNPQ là hình chữ nhật",[
            ("math","M N parallel B C",27,CYAN),
            ("math","N P parallel A D",27,CYAN),
            ("math","B C perp A D",27,GREEN),
            ("math","M N = lambda a",29,INK),
            ("math","N P = (1-lambda) a",29,INK),
            ("math","S(lambda) = a^2 lambda (1-lambda)",29,GOLD),
        ],accent=GOLD)
        self.narrate(
            "Xét tứ diện đều ABCD cạnh a. Mặt phẳng cắt bốn cạnh AB, AC, DC, DB tại M, N, P, Q sao cho AM trên AB và AN trên AC cùng bằng lambda lần cạnh tương ứng; tương tự DP trên DC và DQ trên DB cũng cùng tỷ số lambda. Trong tam giác ABC, MN song song BC và dài lambda a. Trong tam giác ACD, NP song song AD và dài một trừ lambda nhân a.",
            2.0,
        )
        self.narrate(
            "Hai cạnh đối AD và BC của tứ diện đều vuông góc nhau. Vì vậy MN vuông góc NP, và thiết diện MNPQ là hình chữ nhật. Đây là một cấu hình rất đẹp: một mặt cắt của tứ diện đều không chỉ là tứ giác mà còn có cấu trúc vuông góc rõ ràng. Diện tích bằng a bình phương nhân lambda nhân một trừ lambda.",
            2.0,
        )
        self.play(lam.animate.set_value(0.50),run_time=2.6,rate_func=smooth)
        self.narrate(
            "Cho lambda chạy từ gần đỉnh A về giữa các cạnh. Một cạnh của hình chữ nhật tăng, cạnh kia giảm. Tại lambda bằng một phần hai, hai cạnh bằng nhau và hình chữ nhật trở thành hình vuông cạnh a trên hai. Ta có lambda nhân một trừ lambda bằng một phần tư trừ bình phương của lambda trừ một phần hai, nên diện tích lớn nhất đúng tại vị trí giữa.",
            2.0,
        )
        self.card("Cực trị","Hoàn thành bình phương",[
            ("math","S(lambda) = a^2 lambda (1-lambda)",28,INK),
            ("math","S(lambda) = frac(a^2, 4) - a^2 (lambda-frac(1, 2))^2",25,CYAN),
            ("math","lambda = frac(1, 2)",31,GOLD),
            ("math","S = frac(a^2, 4)",33,GOLD),
            ("text","Tại cực trị: thiết diện là hình vuông.",16,MUTED,NORMAL),
        ],accent=CYAN)
        self.play(lam.animate.set_value(0.82),run_time=2.0,rate_func=smooth); self.play(lam.animate.set_value(0.50),run_time=1.7,rate_func=smooth)
        self.narrate(
            "Điều nên nhớ không phải chỉ là đáp số a bình phương trên bốn. Mẫu nhận dạng ở đây là: khi diện tích có dạng tích của hai đại lượng bù nhau, x nhân một trừ x, cực trị thường xuất hiện ở trạng thái cân bằng x bằng một phần hai. Hình học xác nhận điều đó bằng việc hình chữ nhật trở thành hình vuông.",
            1.8,
        )
        self.takeaway("Tứ diện đều + mặt cắt song song hai cạnh đối → chữ nhật; cực đại khi thành hình vuông.")

    # ======================================================
    # 4. INSCRIBED PRISM IN A SQUARE PYRAMID
    # ======================================================
    def pyramid_inscribed_prism(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-52*DEGREES,zoom=0.96)
        self.add_header("Bài 2 · Hình hộp nội tiếp hình chóp","Thiết diện song song đáy tạo bài toán cực trị thể tích","3/6")
        G=self.square_pyramid(); self.add(G["base"],G["edges"],G["dots"]); self.add_pyramid_labels(G)
        A,B,C,D,S=[G[x] for x in ["A","B","C","D","S"]]
        k=ValueTracker(0.35)
        def top_pts():
            u=k.get_value()
            return [S+u*(X-S) for X in [A,B,C,D]]
        top=always_redraw(lambda: Polygon(*top_pts(),fill_color=GOLD,fill_opacity=0.22,stroke_color=GOLD,stroke_width=4.2))
        pillars=always_redraw(lambda: VGroup(*[solid(X,np.array([X[0],X[1],A[2]]),CYAN,3.3,0.78) for X in top_pts()]))
        self.add(top,pillars)
        k_num=always_redraw(lambda: txt(f"{k.get_value():.2f}", 19, GOLD, BOLD))
        v_num=always_redraw(lambda: txt(f"{48*k.get_value()**2*(1-k.get_value()):.2f}", 19, CYAN, BOLD))
        read=VGroup(txt("k =",19,MUTED,BOLD),k_num,txt("  V =",19,MUTED,BOLD),v_num).arrange(RIGHT,buff=0.10).move_to(LEFT*2.60+DOWN*2.40)
        self.add_fixed_in_frame_mobjects(read)
        self.card("Mô hình","Chóp đáy vuông cạnh 4, cao 3",[
            ("math","S_(M N P Q) = 16 k^2",29,CYAN),
            ("math","h = 3(1-k)",29,CYAN),
            ("math","V(k) = 48 k^2 (1-k)",31,GOLD),
            ("sep",),
            ("math","V'(k) = 48 k (2-3k)",28,INK),
            ("math","k = frac(2, 3)",31,GREEN),
        ],accent=ORANGE)
        self.narrate(
            "Xét hình chóp đều đáy vuông cạnh bốn, chiều cao ba. Một mặt phẳng song song đáy cắt bốn cạnh bên theo cùng tỷ số k tính từ đỉnh. Thiết diện là hình vuông có diện tích mười sáu k bình phương. Từ thiết diện đó hạ bốn cạnh vuông góc xuống đáy, ta được một hình hộp chữ nhật nội tiếp hình chóp, có mặt trên chính là thiết diện.",
            2.0,
        )
        self.narrate(
            "Khoảng cách từ thiết diện xuống đáy bằng ba nhân một trừ k. Vì vậy thể tích hình hộp là bốn mươi tám k bình phương nhân một trừ k. Đây là một ví dụ đẹp cho việc thiết diện không chỉ là hình cắt để tính diện tích; nó còn có thể đóng vai trò mặt trên của một khối nội tiếp, biến bài hình học thành bài cực trị hàm số.",
            2.0,
        )
        self.play(k.animate.set_value(2/3),run_time=2.8,rate_func=smooth)
        self.narrate(
            "Đạo hàm cho V phẩy bằng bốn mươi tám k nhân hai trừ ba k. Trong khoảng từ không đến một, điểm cực đại nội là k bằng hai phần ba. Lúc đó mặt trên của hình hộp không nằm ở nửa chiều cao mà nằm thấp hơn: nó cách đỉnh hai phần ba quãng đường xuống đáy, để cân bằng giữa diện tích mặt trên và chiều cao của hình hộp.",
            2.0,
        )
        self.play(k.animate.set_value(0.90),run_time=1.6); self.play(k.animate.set_value(0.25),run_time=1.6); self.play(k.animate.set_value(2/3),run_time=1.5)
        self.takeaway("Cực trị khối nội tiếp: diện tích tăng theo k² nhưng chiều cao giảm theo 1−k.")

    # ======================================================
    # 5. CUBE MOVING PLANE: TRIANGLE -> HEXAGON -> TRIANGLE
    # ======================================================
    def cube_moving_plane(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-52*DEGREES,zoom=0.96)
        self.add_header("Bài 3 · Mặt phẳng chạy qua hình lập phương","Tam giác → lục giác → tam giác","4/6")
        G=self.cube_dynamic(); self.add(G["faces"],G["edges"],G["dots"])
        t=ValueTracker(0.35)
        def section_display():
            pts=cube_section_normalized(t.get_value())
            return [cube_unit_map(*p) for p in pts]
        sec=always_redraw(lambda: Polygon(*section_display(),fill_color=GOLD,fill_opacity=0.24,stroke_color=GOLD,stroke_width=4.4))
        pdots=always_redraw(lambda: VGroup(*[Dot3D(x,radius=0.042,color=GOLD) for x in section_display()]))
        self.add(sec,pdots)
        t_num=always_redraw(lambda: txt(f"{t.get_value():.2f}", 18, GOLD, BOLD))
        n_num=always_redraw(lambda: txt(f"{len(cube_section_normalized(t.get_value()))}", 18, CYAN, BOLD))
        a_num=always_redraw(lambda: txt(f"{cube_section_area_factor(t.get_value()):.3f}", 18, GREEN, BOLD))
        read=VGroup(txt("t =",18,MUTED,BOLD),t_num,txt("  số đỉnh =",18,MUTED,BOLD),n_num,txt("  S/a² =",18,MUTED,BOLD),a_num).arrange(RIGHT,buff=0.08).move_to(LEFT*2.50+DOWN*2.38)
        self.add_fixed_in_frame_mobjects(read)
        self.card("Mặt phẳng","x + y + z = t a",[
            ("math","0 < t < 1",27,CYAN),
            ("text","Thiết diện là tam giác đều.",16,MUTED,NORMAL),
            ("math","1 < t < 2",27,CYAN),
            ("text","Thiết diện là lục giác.",16,MUTED,NORMAL),
            ("math","2 < t < 3",27,CYAN),
            ("text","Thiết diện trở lại tam giác đều.",16,MUTED,NORMAL),
        ],accent=GOLD)
        self.narrate(
            "Bây giờ là cấu hình mạnh nhất của chặng thiết diện. Trong hình lập phương cạnh a, xét họ mặt phẳng x cộng y cộng z bằng t a, với t chạy từ không đến ba. Ta chưa cần dùng tọa độ để giải những video trước, nhưng ở đây phương trình chỉ đóng vai trò điều khiển một mặt phẳng song song với chính nó. Điều quan trọng là nhìn xem mặt phẳng đang cắt những cạnh nào của lập phương.",
            2.0,
        )
        self.narrate(
            "Khi t nhỏ hơn một, mặt phẳng chỉ cắt ba cạnh xuất phát từ một đỉnh, nên thiết diện là tam giác đều. Đến t bằng một, mặt phẳng đi qua ba đỉnh của khối: đây là mốc chuyển kiểu. Sau mốc đó, mỗi mặt của lập phương có thể đóng góp một đoạn cắt và thiết diện mở thành lục giác.",
            2.0,
        )
        self.play(t.animate.set_value(0.98),run_time=2.5,rate_func=linear)
        self.play(t.animate.set_value(1.35),run_time=2.0,rate_func=linear)
        self.narrate(
            "Quan sát lúc t vừa vượt một: ba đỉnh cũ không còn nằm trên cạnh như trước, đồng thời ba giao điểm mới xuất hiện trên ba cạnh phía đối diện. Số cạnh nhảy từ ba lên sáu. Đây chính là lý do một công thức diện tích không thể dùng cho cả khoảng từ không đến ba.",
            1.8,
        )
        self.play(t.animate.set_value(1.50),run_time=1.5,rate_func=smooth)
        self.narrate(
            "Tại t bằng ba phần hai, mặt phẳng đi qua tâm lập phương. Nhờ đối xứng tâm, sáu giao điểm nằm hoàn toàn cân đối và thiết diện trở thành lục giác đều. Đây cũng là ứng viên tự nhiên cho diện tích lớn nhất, nhưng ta vẫn cần công thức để chứng minh.",
            1.8,
        )
        self.play(t.animate.set_value(2.02),run_time=2.0,rate_func=linear); self.play(t.animate.set_value(2.65),run_time=2.0,rate_func=linear)
        self.narrate(
            "Khi t vượt hai, lục giác co lại thành tam giác đều ở phía đỉnh đối diện. Toàn bộ chuyển động đối xứng qua t bằng ba phần hai: thiết diện tại t và tại ba trừ t có cùng diện tích. Nhìn được đối xứng này sẽ giúp ta kiểm tra công thức và cực trị rất nhanh.",
            1.8,
        )

    # ======================================================
    # 6. CUBE PIECEWISE AREA + EXTREMUM
    # ======================================================
    def cube_piecewise_area(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bài 3 · Công thức diện tích theo từng miền","Một hàm từng đoạn xuất hiện từ chính sự đổi kiểu thiết diện","5/6")
        left=VGroup(
            txt("0 < t < 1",17,GOLD,BOLD),mty("S(t) = frac(sqrt(3), 2) a^2 t^2",27,INK),
            txt("1 < t < 2",17,GOLD,BOLD),mty("S(t) = frac(sqrt(3), 2) a^2 (-2 t^2 + 6 t - 3)",25,INK),
            txt("2 < t < 3",17,GOLD,BOLD),mty("S(t) = frac(sqrt(3), 2) a^2 (3-t)^2",27,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.22).shift(LEFT*2.65+UP*0.20)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Cực trị","Miền giữa quyết định cực đại",[
            ("math","-2 t^2 + 6 t - 3",28,CYAN),
            ("math","= frac(3, 2) - 2(t-frac(3, 2))^2",25,CYAN),
            ("math","t = frac(3, 2)",31,GOLD),
            ("math","S = frac(3 sqrt(3), 4) a^2",32,GOLD),
            ("text","Đúng lúc thiết diện là lục giác đều qua tâm.",16,MUTED,NORMAL),
        ],accent=GREEN)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.7)
        self.narrate(
            "Ta lập công thức theo ba miền. Với không nhỏ hơn t nhỏ hơn một, tam giác đều có cạnh căn hai nhân t a, nên diện tích bằng căn ba trên hai nhân a bình phương t bình phương. Miền cuối đối xứng, chỉ cần thay t bởi ba trừ t. Phần đáng chú ý là miền giữa, khi thiết diện là lục giác.",
            2.0,
        )
        self.narrate(
            "Diện tích miền giữa rút gọn thành căn ba trên hai nhân a bình phương nhân âm hai t bình phương cộng sáu t trừ ba. Hoàn thành bình phương, biểu thức trong ngoặc bằng ba phần hai trừ hai lần bình phương của t trừ ba phần hai. Vì vậy diện tích lớn nhất tại t bằng ba phần hai.",
            2.0,
        )
        self.narrate(
            "Thế t bằng ba phần hai, ta được diện tích cực đại bằng ba căn ba trên bốn nhân a bình phương. Đây chính là diện tích lục giác đều ở video mười một. Như vậy một kết quả tưởng rời rạc về lục giác trung điểm thực ra là trạng thái cực đại của cả một họ thiết diện chuyển động xuyên qua hình lập phương.",
            2.0,
        )
        self.narrate(
            "Bài này cho một mẫu rất sâu: khi đa giác cắt đổi loại, hàm hình học trở thành hàm từng đoạn. Muốn cực trị toàn cục, phải xét cực trị bên trong từng đoạn và cả các mốc chuyển kiểu. Không được đạo hàm một công thức rồi áp dụng cho toàn miền nếu công thức đó chỉ đúng cho một kiểu thiết diện.",
            1.8,
        )

    # ======================================================
    # 7. SYNTHESIS
    # ======================================================
    def synthesis(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ phương pháp","Thiết diện động: dựng hình trước, hàm số sau","6/6")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Tìm mốc",20,INK),txt("→ mặt cắt qua đỉnh/cạnh",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Chia miền",20,INK),txt("→ giữ nguyên kiểu đa giác",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Lập hàm",20,INK),txt("→ độ dài, diện tích, thể tích",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Cực trị",20,INK),txt("→ xét cả điểm trong và mốc",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Đọc hình",20,INK),txt("→ cực trị thường đi cùng đối xứng",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30).shift(LEFT*2.70+UP*0.22)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Ba kết quả đẹp","Chốt chặng thiết diện",[
            ("math","S_1 <= frac(a^2, 4)",28,GOLD),
            ("math","V_2 = 48 k^2(1-k)",27,GOLD),
            ("math","k = frac(2, 3)",29,GREEN),
            ("math","S_3 <= frac(3 sqrt(3), 4) a^2",26,GOLD),
            ("math","t = frac(3, 2)",29,GREEN),
            ("sep",),
            ("text","Đối xứng trên hình thường báo trước vị trí cực trị.",16,MUTED,NORMAL),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.10),run_time=0.7)
        self.narrate(
            "Chặng thiết diện kết thúc bằng ba bức tranh. Trong tứ diện đều, mặt cắt song song hai cạnh đối là hình chữ nhật và đạt diện tích lớn nhất khi trở thành hình vuông. Trong hình chóp, thiết diện song song đáy làm mặt trên của hình hộp nội tiếp, và thể tích lớn nhất tại tỷ số hai phần ba. Trong lập phương, một họ mặt phẳng song song tạo chuỗi tam giác, lục giác, tam giác, với cực đại đúng tại lục giác đều qua tâm.",
            2.0,
        )
        self.narrate(
            "Điểm chung của cả ba bài là cực trị hình học thường xuất hiện tại trạng thái cân bằng hoặc đối xứng cao. Nhưng đối xứng chỉ giúp dự đoán, còn chứng minh phải đến từ công thức đúng trên miền đúng. Hãy luôn dựng mặt cắt trước, xác định xem hình có đổi kiểu hay không, rồi mới lập hàm. Đây là nguyên tắc sẽ tiếp tục xuất hiện ở các video điểm động và cực trị sau này.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 13",17,BLUE,BOLD),
            txt("NÓN · TRỤ · CẦU · CHÓP CỤT",25,GOLD,BOLD),
            txt("Mặt cắt tròn · tiếp xúc · thể tích · cấu hình ghép khối",18,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box); self.play(FadeIn(next_box),run_time=0.55)
        self.narrate(
            "Video mười ba sẽ mở chặng mới về khối tròn và các mô hình ba chiều. Ta sẽ không chỉ nhắc lại công thức nón, trụ, cầu, mà tập trung vào mặt cắt qua trục, mặt cắt vuông góc trục, quan hệ tiếp xúc, khối nội tiếp ngoại tiếp và các bài ghép nhiều khối. Mục tiêu vẫn là nhìn cấu hình trước rồi mới chọn công thức.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.toolkit()
        self.tetra_moving_rectangle()
        self.pyramid_inscribed_prism()
        self.cube_moving_plane()
        self.cube_piecewise_area()
        self.synthesis()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir=str(MEDIA_DIR)
    config.output_file="hhkg_chuyen_sau_12_thiet_dien_III_diem_dong_cuc_tri_typst_SAFE_1080p"
    config.format="mp4"; config.write_to_movie=True; config.disable_caching=False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 12")
    print("Dynamic sections: regular tetrahedron, pyramid prism, cube piecewise plane")
    scene=SangLesson(); scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists(): raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")
    video_duration=probe_duration(video_path)
    master_wav=ROOT/"master_narration_hhkg_12.wav"
    build_master_audio(scene.audio_events,video_duration,master_wav)
    final_path=video_path.with_name(video_path.stem+"_WITH_AUDIO.mp4")
    mux_audio(video_path,master_wav,final_path); validate_audio(master_wav)
    print("\n============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path

if __name__ == "__main__":
    render_full()

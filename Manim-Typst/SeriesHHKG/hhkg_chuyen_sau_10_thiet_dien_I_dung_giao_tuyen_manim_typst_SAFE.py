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
# HHKG CHUYEN SAU 10 - THIET DIEN I: DUNG DUNG GIAO TUYEN
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
        series = txt("HHKG CHUYÊN SÂU · 10", 15, BLUE, BOLD)
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

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        series=txt("HHKG CHUYÊN SÂU · 10",18,BLUE,BOLD)
        title=txt("THIẾT DIỆN I",48,GOLD,BOLD)
        sub=txt("DỰNG ĐÚNG GIAO TUYẾN",38,INK,BOLD)
        line=txt("Đi qua từng mặt · nối đúng cạnh · dùng điểm phụ khi cần",24,CYAN,BOLD)
        note=txt("Không đoán hình cắt — để mặt phẳng tự dẫn đường",22,MUTED)
        brand=txt(TEN_THAY,18,MUTED)
        g=VGroup(series,title,sub,line,note,brand).arrange(DOWN,buff=0.24)
        self.play(FadeIn(series),FadeIn(title,shift=UP*0.15),run_time=0.8)
        self.play(FadeIn(sub),FadeIn(line),FadeIn(note),FadeIn(brand),run_time=1.0)
        self.narrate(
            "Từ video mười, ta bước sang thiết diện. Đây là phần mà một hình vẽ sai có thể làm hỏng cả lời giải, nên thầy sẽ không cho sẵn đa giác cắt rồi mới tính. Ta sẽ dựng mặt phẳng cắt từng bước: nó gặp mặt nào trước, trên mặt ấy ta đã biết hai điểm nào, giao tuyến nào là thật, giao điểm nào chỉ là điểm phụ nằm ngoài khối. Khi quy trình dựng đã chắc, diện tích và tỷ số ở các video sau sẽ nhẹ hơn rất nhiều.",
            2.0,
        )

    # ======================================================
    # PRINCIPLES
    # ======================================================
    def principles(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-50*DEGREES,zoom=0.96)
        self.add_header("Nguyên tắc dựng thiết diện", "Mặt phẳng cắt đi qua từng mặt của đa diện", "1/6")
        G=self.tetrahedron(); self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("S",G["S"],RED,(-0.13,-0.05,0.13),21),("A",G["A"],GOLD,(-0.15,-0.13,0),21),
            ("B",G["B"],GOLD,(0.12,-0.10,0),21),("C",G["C"],GOLD,(0.12,0.10,0),21),
        ])
        M=G["S"]+0.48*(G["A"]-G["S"]); N=G["S"]+0.66*(G["B"]-G["S"]); P=G["S"]+0.58*(G["C"]-G["S"])
        points=VGroup(*[Dot3D(x,radius=0.055,color=GOLD) for x in [M,N,P]])
        self.add(points)
        self.label_many([("M",M,GOLD,(-0.16,-0.08,0.08),19),("N",N,GOLD,(0.12,-0.08,0.08),19),("P",P,GOLD,(0.12,0.10,0.05),19)])
        card=self.card("Nền tảng", "Ba nguyên tắc phải nhớ", [
            ("text","1. Hai điểm cùng nằm trên một mặt → nối chúng.",18,INK,NORMAL),
            ("text","2. Sang mặt kề qua điểm chung của hai giao tuyến.",18,INK,NORMAL),
            ("text","3. Hai mặt song song → hai giao tuyến song song.",18,INK,NORMAL),
            ("sep",),
            ("text","Điểm phụ có thể nằm ngoài đa diện; đoạn thiết diện thì không.",17,CYAN,BOLD),
        ],accent=CYAN)
        self.narrate(
            "Có ba nguyên tắc gốc. Một, trên cùng một mặt của đa diện, nếu mặt phẳng cắt đã có hai điểm thì nối hai điểm ấy, đó là một đoạn giao tuyến thật. Hai, muốn đi sang mặt kề, ta đi qua cạnh chung của hai mặt. Ba, nếu đa diện có hai mặt song song, các giao tuyến của cùng một mặt phẳng cắt với hai mặt song song ấy cũng song song. Và nhớ một điều rất quan trọng: điểm phụ có thể nằm ngoài khối, nhưng thiết diện chỉ gồm phần nằm bên trong khối.",
            2.0,
        )
        mn=solid(M,N,CYAN,6.0,1); mp=solid(M,P,CYAN,6.0,1); np_=solid(N,P,CYAN,6.0,1)
        self.narrate_play("Trong mặt SAB, M và N cùng nằm trên mặt ấy nên ta có đoạn MN. Trong mặt SAC, M và P cho đoạn MP. Sang mặt SBC, N và P cho đoạn NP. Ba đoạn khép kín thành thiết diện MNP. Không có bước nào là nối theo cảm giác; mỗi đoạn đều phải thuộc một mặt của tứ diện.",Create(mn),Create(mp),Create(np_),min_time=2.0)
        sec=face(M,N,P,color=GOLD,opacity=0.22)
        self.play(FadeIn(sec),run_time=0.55)
        self.takeaway("Muốn nối hai điểm, trước hết phải chỉ ra chúng cùng nằm trên một mặt của đa diện.")
        self.narrate("Đây là bài đơn giản nhất nhưng nó chứa đúng tinh thần của toàn chương: giao tuyến được dựng mặt theo mặt. Khi số mặt tăng lên, ta vẫn giữ quy trình này chứ không đổi bản chất.",1.5)

    # ======================================================
    # EXAMPLE 1: TETRAHEDRON
    # ======================================================
    def tetra_section(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-52*DEGREES,zoom=0.97)
        self.add_header("Bài 1 · Tứ diện", "Ba điểm trên ba cạnh xuất phát từ cùng một đỉnh", "2/7")
        G=self.tetrahedron(); self.add(G["base"],G["edges"],G["dots"])
        self.label_many([("S",G["S"],RED,(-0.12,-0.05,0.13),21),("A",G["A"],GOLD,(-0.15,-0.12,0),21),("B",G["B"],GOLD,(0.12,-0.10,0),21),("C",G["C"],GOLD,(0.10,0.11,0),21)])
        M=G["S"]+0.42*(G["A"]-G["S"]); N=G["S"]+0.68*(G["B"]-G["S"]); P=G["S"]+0.54*(G["C"]-G["S"])
        dots=VGroup(*[Dot3D(x,radius=0.055,color=GOLD) for x in [M,N,P]])
        self.play(FadeIn(dots),run_time=0.45)
        self.label_many([("M",M,GOLD,(-0.14,-0.07,0.07),19),("N",N,GOLD,(0.11,-0.07,0.07),19),("P",P,GOLD,(0.11,0.10,0.05),19)])
        card1=self.card("Đề bài", "Dựng thiết diện qua M, N, P", [
            ("math","M in S A",29,CYAN),("math","N in S B",29,CYAN),("math","P in S C",29,CYAN),
            ("text","Ba tỷ số không bằng nhau.",18,MUTED,NORMAL),
            ("text","Vì vậy không được kết luận thiết diện song song đáy.",17,RED,BOLD),
        ],accent=GOLD)
        self.narrate(
            "Bài một vẫn là tứ diện nhưng thầy cố ý chọn M, N, P ở ba vị trí khác nhau. Ba tỷ số từ S đến các điểm không bằng nhau, nên thiết diện không song song với đáy. Điều này giúp tách hai ý: dựng thiết diện là chuyện xác định giao tuyến; song song với đáy chỉ là một trường hợp đặc biệt khi các tỷ số bằng nhau.",
            2.0,
        )
        seg1=solid(M,N,CYAN,6.3); seg2=solid(N,P,CYAN,6.3); seg3=solid(P,M,CYAN,6.3)
        self.play(Create(seg1),run_time=0.55); self.play(Create(seg2),run_time=0.55); self.play(Create(seg3),run_time=0.55)
        sec=face(M,N,P,color=GOLD,opacity=0.23)
        self.play(FadeIn(sec),run_time=0.5)
        old=[m for m in self.mobjects if False]
        self.play(FadeOut(card1),run_time=0.25)
        card2=self.card("Lời giải", "Mỗi cạnh thiết diện nằm trên một mặt", [
            ("math","(M N P) inter (S A B) = M N",26,CYAN),
            ("math","(M N P) inter (S B C) = N P",26,CYAN),
            ("math","(M N P) inter (S C A) = P M",26,CYAN),
            ("sep",),
            ("text","Thiết diện: MNP",20,GOLD,BOLD),
        ],accent=GREEN)
        self.narrate(
            "Ta đọc thiết diện theo ba mặt bên. Với mặt SAB, giao tuyến là MN. Với mặt SBC, giao tuyến là NP. Với mặt SCA, giao tuyến là PM. Ba đoạn đóng lại thành tam giác MNP. Đây là cách trình bày chuẩn: không chỉ ghi đáp án MNP mà phải nói được mỗi cạnh của thiết diện xuất phát từ mặt nào.",
            2.0,
        )
        self.takeaway("Thiết diện là một đa giác; mỗi cạnh của nó phải là giao tuyến với một mặt của khối.")

    # ======================================================
    # EXAMPLE 2: PARALLEL SECTION OF A PYRAMID
    # ======================================================
    def parallel_section(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.96)
        self.add_header("Bài 2 · Thiết diện song song đáy", "Từ tỷ số bằng nhau đến bốn giao tuyến song song", "3/7")
        G=self.square_pyramid(); self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("S",G["S"],RED,(-0.08,-0.03,0.15),21),("A",G["A"],GOLD,(-0.14,-0.12,0),20),
            ("B",G["B"],GOLD,(0.12,-0.12,0),20),("C",G["C"],GOLD,(0.12,0.10,0),20),("D",G["D"],GOLD,(-0.16,0.10,0),20),
        ])
        k=0.56
        M=G["S"]+k*(G["A"]-G["S"]); N=G["S"]+k*(G["B"]-G["S"])
        P=G["S"]+k*(G["C"]-G["S"]); Q=G["S"]+k*(G["D"]-G["S"])
        dots=VGroup(*[Dot3D(x,radius=0.055,color=GOLD) for x in [M,N,P,Q]])
        self.play(FadeIn(dots),run_time=0.45)
        for name,x,off in [("M",M,(-0.14,-0.08,0.08)),("N",N,(0.12,-0.08,0.06)),("P",P,(0.12,0.08,0.05)),("Q",Q,(-0.14,0.08,0.05))]:
            self.add_label(name,x,GOLD,off,19)
        card1=self.card("Đề bài", "Bốn điểm chia các cạnh bên cùng tỷ số", [
            ("math","frac(S M, S A) = frac(S N, S B) = k",25,CYAN),
            ("math","frac(S P, S C) = frac(S Q, S D) = k",25,CYAN),
            ("text","Dựng thiết diện qua M, N, P, Q.",18,INK,NORMAL),
            ("sep",),
            ("text","Không cần tìm điểm phụ ngoài khối.",17,MUTED,NORMAL),
        ],accent=GOLD)
        self.narrate(
            "Trước khi sang bài có điểm phụ, ta xét một cấu hình rất quan trọng: bốn điểm M, N, P, Q chia bốn cạnh bên theo cùng một tỷ số tính từ S. Trong tam giác SAB, định lý Ta-lét cho MN song song AB. Tương tự, NP song song BC, PQ song song CD và QM song song DA. Vì bốn đoạn ghép kín và lần lượt nằm trên bốn mặt bên, thiết diện là tứ giác MNPQ.",
            2.0,
        )
        mn=solid(M,N,CYAN,6.0); np_=solid(N,P,CYAN,6.0); pq=solid(P,Q,CYAN,6.0); qm=solid(Q,M,CYAN,6.0)
        self.play(Create(mn),run_time=0.42); self.play(Create(np_),run_time=0.42); self.play(Create(pq),run_time=0.42); self.play(Create(qm),run_time=0.42)
        sec=face(M,N,P,Q,color=GOLD,opacity=0.22)
        self.play(FadeIn(sec),run_time=0.45)
        self.play(FadeOut(card1),run_time=0.25)
        card2=self.card("Kết luận", "Tứ giác cắt song song với đáy", [
            ("math","M N parallel A B",26,GREEN),
            ("math","N P parallel B C",26,GREEN),
            ("math","P Q parallel C D",26,GREEN),
            ("math","Q M parallel D A",26,GREEN),
            ("sep",),
            ("math","(M N P Q) parallel (A B C D)",26,GOLD),
        ],accent=GREEN)
        self.narrate(
            "Bốn cặp song song cho ta mạnh hơn việc nhận ra hình dạng. Chúng chứng minh mặt phẳng MNPQ song song với mặt đáy ABCD. Ở video bảy ta đã dùng cấu hình này để suy ra tỷ số diện tích bằng k bình phương và tỷ số thể tích bằng k lập phương. Ở đây ta nhìn ngược lại: trước khi có các công thức tỷ số ấy, điều nền tảng vẫn là dựng đúng bốn giao tuyến trên bốn mặt bên. Đây cũng là mẫu nhận dạng nhanh nhất của thiết diện song song đáy.",
            2.0,
        )
        self.takeaway("Cùng tỷ số trên các cạnh bên → dùng Ta-lét trên từng mặt → thiết diện song song đáy.")

    # ======================================================
    # EXAMPLE 2: PYRAMID + EXTERNAL AUXILIARY POINT
    # ======================================================
    def pyramid_external_point(self):
        self.clear_all(); self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.96)
        self.add_header("Bài 2 · Hình chóp", "Điểm phụ nằm ngoài đa diện — thiết diện là ngũ giác", "4/7")
        G=self.square_pyramid(); self.add(G["base"],G["edges"],G["dots"])
        self.label_many([
            ("S",G["S"],RED,(-0.08,-0.03,0.15),21),("A",G["A"],GOLD,(-0.14,-0.12,0),20),
            ("B",G["B"],GOLD,(0.12,-0.12,0),20),("C",G["C"],GOLD,(0.12,0.10,0),20),("D",G["D"],GOLD,(-0.16,0.10,0),20),
        ])
        # Unequal ratios ensure MN is not parallel AB. P lies on CD.
        M=G["S"]+0.45*(G["A"]-G["S"])
        N=G["S"]+0.75*(G["B"]-G["S"])
        P=0.50*(G["C"]+G["D"])
        section_pts,hits,norm=section_from_edges(G["edge_map"],M,N,P)
        Q=hits["BC"]; R=hits["SD"]
        dots=VGroup(*[Dot3D(x,radius=0.055,color=GOLD) for x in [M,N,P]])
        self.play(FadeIn(dots),run_time=0.4)
        self.label_many([("M",M,GOLD,(-0.14,-0.08,0.08),19),("N",N,GOLD,(0.12,-0.08,0.06),19),("P",P,GOLD,(0.10,0.12,0),19)])
        card1=self.card("Đề bài", "Dựng thiết diện qua M, N, P", [
            ("math","M in S A",28,CYAN),("math","N in S B",28,CYAN),("math","P in C D",28,CYAN),
            ("text","MN không song song AB.",18,MUTED,NORMAL),
            ("text","Cần tìm giao tuyến của mặt cắt với đáy.",18,GOLD,BOLD),
        ],accent=GOLD)
        self.narrate(
            "Đây là cấu hình quan trọng hơn. M nằm trên SA, N nằm trên SB, P nằm trên CD và MN không song song AB. Ta biết ngay MN trên mặt SAB, nhưng P không cùng nằm với M hay N trên một mặt bên thích hợp. Muốn tiếp tục, ta phải tìm giao tuyến của mặt phẳng cắt với mặt đáy ABCD. Đây chính là lúc điểm phụ ngoài đa diện xuất hiện.",
            2.0,
        )
        mn=solid(M,N,CYAN,6.0)
        self.play(Create(mn),run_time=0.55)
        # I = extension MN intersect base plane; mathematically it falls on extension of AB beyond B.
        hit=line_plane_intersection(M,N,G["A"],G["B"],G["D"])
        if hit is None: raise RuntimeError("MN unexpectedly parallel to base plane")
        I,_=hit
        ext=aux(M,I,ORANGE,3.6,0.85)
        idot=Dot3D(I,radius=0.052,color=ORANGE)
        self.play(Create(ext),FadeIn(idot),run_time=0.75)
        self.add_label("I",I,ORANGE,(0.11,-0.08,0.05),19)
        self.narrate(
            "Kéo dài MN. Vì MN nằm trong mặt phẳng cắt, còn AB nằm trong mặt đáy, giao điểm I của hai đường kéo dài thuộc đồng thời cả hai mặt phẳng. I có thể nằm ngoài cạnh AB, thậm chí ngoài hẳn hình chóp; điều đó hoàn toàn hợp lệ vì I chỉ là điểm phụ. Bây giờ I và P cùng thuộc mặt phẳng cắt và cùng thuộc mặt đáy, nên IP chính là giao tuyến của mặt phẳng cắt với đáy.",
            2.0,
        )
        ip=aux(I,P,GREEN,4.2,0.92)
        self.play(Create(ip),run_time=0.65)
        # Reveal Q = IP ∩ BC, while P already lies on CD.
        qdot=Dot3D(Q,radius=0.055,color=GREEN)
        self.play(FadeIn(qdot),run_time=0.35); self.add_label("Q",Q,GREEN,(0.12,-0.05,0.03),19)
        self.narrate(
            "Đường IP đi vào hình vuông đáy tại Q trên BC rồi đi ra tại P trên CD. Vì vậy đoạn QP mới là cạnh thật của thiết diện trong đáy; phần IQ nằm ngoài khối chỉ là đường dựng phụ. Ta đã có NQ trên mặt SBC. Từ P, thiết diện sang mặt SCD và cắt cạnh SD tại R. Cuối cùng RM nằm trên mặt SDA và đa giác khép kín.",
            2.0,
        )
        rdot=Dot3D(R,radius=0.055,color=GREEN); self.play(FadeIn(rdot),run_time=0.35); self.add_label("R",R,GREEN,(-0.14,0.08,0.06),19)
        nq=solid(N,Q,CYAN,6.0); qp=solid(Q,P,CYAN,6.0); pr=solid(P,R,CYAN,6.0); rm=solid(R,M,CYAN,6.0)
        self.play(Create(nq),run_time=0.45); self.play(Create(qp),run_time=0.45); self.play(Create(pr),run_time=0.45); self.play(Create(rm),run_time=0.45)
        sec=Polygon(M,N,Q,P,R,fill_color=GOLD,fill_opacity=0.22,stroke_width=0)
        self.play(FadeIn(sec),run_time=0.55)
        self.play(FadeOut(card1),run_time=0.25)
        card2=self.card("Lời giải", "Từ điểm phụ I đến ngũ giác thiết diện", [
            ("math","I = M N inter A B",27,ORANGE),
            ("math","I P = (M N P) inter (A B C D)",25,GREEN),
            ("math","Q = I P inter B C",27,GREEN),
            ("math","R in S D",27,CYAN),
            ("sep",),
            ("text","Thiết diện: MNQPR",20,GOLD,BOLD),
        ],accent=GREEN)
        self.narrate(
            "Thiết diện là ngũ giác MNQPR. Điểm I không phải đỉnh thiết diện vì nó nằm ngoài đa diện. Đây là lỗi rất hay gặp: học sinh tìm được điểm phụ rồi đưa luôn nó vào đa giác cắt. Hãy phân biệt rõ hai lớp hình: đường dựng có thể kéo dài vô hạn; thiết diện chỉ lấy phần của mặt phẳng nằm bên trong khối.",
            2.0,
        )
        self.takeaway("Điểm phụ ngoài khối để tìm giao tuyến; chỉ các giao điểm trên cạnh của đa diện mới là đỉnh thiết diện.")
        self.narrate(
            "Ta có thể tự kiểm tra ngũ giác vừa dựng bằng cách đọc ngược một vòng. MN nằm trên mặt SAB; NQ nằm trên mặt SBC; QP nằm trong đáy ABCD; PR nằm trên mặt SCD; RM nằm trên mặt SDA. Hai cạnh liên tiếp luôn gặp nhau trên một cạnh của hình chóp, và sau năm bước ta trở lại M. Cách kiểm tra vòng kín này rất hữu ích trong bài thi: nếu có một đoạn mà em không chỉ ra được mặt chứa nó, hoặc hai đoạn liên tiếp không gặp nhau trên cạnh chung của hai mặt, hình dựng gần như chắc chắn có lỗi.",
            2.0,
        )

    # ======================================================
    # EXAMPLE 3: CUBE HEXAGON
    # ======================================================
    def cube_hexagon(self):
        self.clear_all(); self.set_camera_orientation(phi=67*DEGREES,theta=-50*DEGREES,zoom=0.97)
        self.add_header("Bài 3 · Hình lập phương", "Ba cặp mặt song song tạo thiết diện lục giác", "5/7")
        G=self.cube(); self.add(G["faces"],G["edges"],G["dots"])
        self.label_many([
            ("A",G["A"],GOLD,(-0.15,-0.10,0),18),("B",G["B"],GOLD,(0.10,-0.10,0),18),
            ("C",G["C"],GOLD,(0.11,0.08,0),18),("D",G["D"],GOLD,(-0.15,0.08,0),18),
            ("A'",G["A1"],GOLD,(-0.16,-0.10,0.05),18),("B'",G["B1"],GOLD,(0.10,-0.09,0.05),18),
            ("C'",G["C1"],GOLD,(0.10,0.09,0.05),18),("D'",G["D1"],GOLD,(-0.16,0.09,0.05),18),
        ])
        a=G["a"]
        # Exact six midpoints of the plane x+y+z=0 in logical cube coordinates.
        M=0.5*(G["B"]+G["C"])      # BC
        N=0.5*(G["B"]+G["B1"])     # BB'
        P=0.5*(G["A1"]+G["B1"])    # A'B'
        Q=0.5*(G["D1"]+G["A1"])    # D'A'
        R=0.5*(G["D"]+G["D1"])     # DD'
        T=0.5*(G["C"]+G["D"])      # CD
        pts=[M,N,P,Q,R,T]
        dots=VGroup(*[Dot3D(x,radius=0.052,color=GOLD) for x in pts])
        self.play(FadeIn(dots),run_time=0.55)
        for name,x,off in [("M",M,(0.11,0.02,0.05)),("N",N,(0.12,-0.05,0.05)),("P",P,(0.08,-0.10,0.05)),
                           ("Q",Q,(-0.15,-0.02,0.05)),("R",R,(-0.15,0.06,0.05)),("T",T,(0.05,0.11,0.05))]:
            self.add_label(name,x,GOLD,off,18)
        card1=self.card("Đề bài", "Mặt phẳng qua 3 trung điểm liên tiếp", [
            ("text","M là trung điểm BC",18,INK,NORMAL),
            ("text","N là trung điểm BB'",18,INK,NORMAL),
            ("text","P là trung điểm A'B'",18,INK,NORMAL),
            ("sep",),
            ("text","Dựng tiếp thiết diện mà không đoán trước hình lục giác.",17,CYAN,BOLD),
        ],accent=GOLD)
        self.narrate(
            "Trong hình lập phương, ta lấy M là trung điểm BC, N là trung điểm BB phẩy, P là trung điểm A phẩy B phẩy. Ba điểm xác định mặt phẳng cắt. Trên mặt BCC phẩy B phẩy, ta có MN. Trên mặt ABB phẩy A phẩy, ta có NP. Từ đây ta chưa biết ngay ba đỉnh còn lại, nhưng hình lập phương cho ta một công cụ rất mạnh: ba cặp mặt đối song song.",
            2.0,
        )
        mn=solid(M,N,CYAN,6.0); np_=solid(N,P,CYAN,6.0)
        self.play(Create(mn),Create(np_),run_time=0.9)
        self.play(FadeOut(card1),run_time=0.25)
        card2=self.card("Dựng tiếp", "Dùng các mặt đối song song", [
            ("math","(B C C' B') parallel (A D D' A')",24,CYAN),
            ("math","M N parallel Q R",27,GREEN),
            ("math","N P parallel R T",27,GREEN),
            ("math","P Q parallel T M",27,GREEN),
            ("sep",),
            ("text","Các giao tuyến trên hai mặt song song phải song song.",17,MUTED,NORMAL),
        ],accent=GREEN)
        qr=solid(Q,R,CYAN,6.0); rt=solid(R,T,CYAN,6.0); pq=solid(P,Q,CYAN,6.0); tm=solid(T,M,CYAN,6.0)
        self.play(Create(qr),run_time=0.45); self.play(Create(rt),run_time=0.45); self.play(Create(pq),run_time=0.45); self.play(Create(tm),run_time=0.45)
        sec=Polygon(*pts,fill_color=GOLD,fill_opacity=0.20,stroke_width=0)
        self.play(FadeIn(sec),run_time=0.55)
        self.narrate(
            "Mặt đối với BCC phẩy B phẩy là ADD phẩy A phẩy, nên giao tuyến QR phải song song MN. Tương tự, RT song song NP, còn PQ song song TM. Khi đi hết sáu mặt, mặt phẳng cắt khép lại thành lục giác MNPQRT. Trong cấu hình trung điểm này, sáu cạnh còn bằng nhau nên thực tế ta được một lục giác đều. Tuy nhiên ở video mười, điều quan trọng không phải diện tích mà là dựng được đúng sáu cạnh bằng quy tắc giao tuyến.",
            2.0,
        )
        self.takeaway("Khối có các mặt đối song song: hãy dùng tính song song của các giao tuyến để dựng nhanh phần còn lại.")
        self.narrate(
            "Một cách kiểm chứng khác là nhìn sáu đỉnh của thiết diện: mỗi đỉnh nằm đúng trên một cạnh của lập phương, và mặt phẳng cắt lần lượt đi qua sáu mặt khác nhau trước khi quay về điểm đầu. Đặc biệt, ba cặp cạnh đối của lục giác song song từng đôi vì chúng nằm trên ba cặp mặt đối song song của lập phương. Sang video mười một, chính cấu trúc này sẽ cho phép ta tính diện tích rất nhanh bằng cách chia lục giác thành các tam giác đều hoặc lấy diện tích hình vuông chiếu, nhưng hôm nay ta dừng ở phần dựng để không trộn hai kỹ năng vào nhau.",
            2.0,
        )

    # ======================================================
    # ALGORITHM + COMMON ERRORS
    # ======================================================
    def errors_and_algorithm(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Thuật toán dựng thiết diện", "Bốn câu hỏi trước khi nối bất kỳ hai điểm nào", "6/7")
        left=VGroup(
            txt("01",19,GOLD,BOLD),txt("Điểm đã biết nằm trên mặt nào?",22,INK,BOLD),
            txt("02",19,GOLD,BOLD),txt("Trên mặt ấy đã có đủ hai điểm chưa?",22,INK,BOLD),
            txt("03",19,GOLD,BOLD),txt("Nếu chưa: dùng cạnh chung, song song hay điểm phụ?",22,INK,BOLD),
            txt("04",19,GOLD,BOLD),txt("Đa giác đã khép kín và chỉ nằm trong khối chưa?",22,INK,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).shift(LEFT*2.7+UP*0.15)
        self.add_fixed_in_frame_mobjects(left)
        right=self.card("Sai lầm", "Bốn lỗi làm hỏng thiết diện", [
            ("text","Nối hai điểm dù chúng không cùng nằm trên một mặt.",17,RED,BOLD),
            ("text","Thấy ba điểm rồi kết luận ngay thiết diện là tam giác.",17,RED,BOLD),
            ("text","Đưa điểm phụ ngoài khối vào đa giác thiết diện.",17,RED,BOLD),
            ("text","Bỏ qua tính song song của các mặt đối.",17,RED,BOLD),
            ("sep",),
            ("text","Mỗi cạnh thiết diện phải trả lời được: nó nằm trên mặt nào?",17,CYAN,BOLD),
        ],accent=RED)
        self.play(FadeIn(left,shift=RIGHT*0.12),run_time=0.7)
        self.narrate(
            "Thầy đề nghị dùng một thuật toán bốn câu hỏi. Một, điểm ta đang có nằm trên mặt nào của đa diện. Hai, trên mặt ấy đã đủ hai điểm để nối chưa. Ba, nếu chưa đủ thì ta tìm điểm mới bằng cạnh chung, tính song song hay kéo dài để tạo điểm phụ. Bốn, sau khi đi qua các mặt, đa giác đã khép kín chưa và mọi đỉnh của nó có thật sự nằm trên cạnh của đa diện không. Thuật toán này nghe chậm nhưng khi quen sẽ nhanh hơn rất nhiều so với vẽ theo cảm giác rồi sửa sai.",
            2.0,
        )
        # Visual wrong-vs-right mini diagram in 2D fixed frame.
        p1=np.array([-4.8,-1.7,0]); p2=np.array([-2.9,-1.1,0]); p3=np.array([-3.6,0.7,0]); p4=np.array([-5.2,0.5,0])
        quad=Polygon(p1,p2,p3,p4,color=DIM,stroke_width=2,fill_opacity=0)
        a=Dot(p4,color=GOLD); b=Dot(p2,color=GOLD)
        wrong=DashedLine(p4,p2,color=RED,stroke_width=5,dash_length=0.10)
        cross=VGroup(Line(LEFT*0.14+DOWN*0.14,RIGHT*0.14+UP*0.14,color=RED,stroke_width=6),Line(LEFT*0.14+UP*0.14,RIGHT*0.14+DOWN*0.14,color=RED,stroke_width=6)).move_to((p4+p2)/2)
        mini=VGroup(quad,a,b,wrong,cross)
        self.add_fixed_in_frame_mobjects(mini)
        self.play(Create(wrong),FadeIn(cross),run_time=0.6)
        self.narrate(
            "Lỗi phổ biến nhất là thấy hai điểm thuộc mặt phẳng cắt rồi nối ngay, dù đoạn nối không nằm trên một mặt của đa diện. Trong không gian, hai điểm xác định một đường thẳng, nhưng đường ấy chưa chắc là giao tuyến với một mặt của khối. Mỗi lần nối, hãy tự hỏi: đoạn này đang nằm trên mặt tam giác hay tứ giác nào của đa diện? Nếu không chỉ ra được, chưa được phép coi đó là cạnh thiết diện.",
            2.0,
        )

    # ======================================================
    # SUMMARY + BRIDGE TO VIDEO 11
    # ======================================================
    def summary(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ tư duy thiết diện I", "Dựng đúng trước — tính sau", "7/7")
        left=VGroup(
            VGroup(txt("1",18,GOLD,BOLD),txt("Hai điểm cùng mặt",20,INK),txt("→ nối",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("2",18,GOLD,BOLD),txt("Thiếu điểm",20,INK),txt("→ sang mặt kề",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("3",18,GOLD,BOLD),txt("Mặt đối song song",20,INK),txt("→ giao tuyến song song",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("4",18,GOLD,BOLD),txt("Bế tắc",20,INK),txt("→ kéo dài, tạo điểm phụ",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
            VGroup(txt("5",18,GOLD,BOLD),txt("Kết thúc",20,INK),txt("→ đa giác khép kín trong khối",20,CYAN,BOLD)).arrange(RIGHT,buff=0.12),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30).shift(LEFT*2.75+UP*0.12)
        self.add_fixed_in_frame_mobjects(left)
        self.card("Chốt", "Ba cấu hình đã luyện", [
            ("text","Thiết diện: MNP",19,GOLD,BOLD),
            ("text","Thiết diện: MNQPR",19,GOLD,BOLD),
            ("text","Thiết diện: MNPQRT",19,GOLD,BOLD),
            ("sep",),
            ("text","Tam giác → ngũ giác → lục giác",18,CYAN,BOLD),
            ("text","Số cạnh không đoán trước; nó xuất hiện từ quá trình đi qua các mặt.",16,MUTED,NORMAL),
        ],accent=GOLD)
        self.play(FadeIn(left,shift=RIGHT*0.12),run_time=0.7)
        self.narrate(
            "Ta đã đi từ tam giác trong tứ diện, đến ngũ giác trong hình chóp có điểm phụ ngoài khối, rồi đến lục giác trong hình lập phương nhờ ba cặp mặt song song. Điều quan trọng nhất là không đoán trước thiết diện có mấy cạnh. Cứ đi qua từng mặt, ghi lại giao tuyến thật, đến khi đa giác khép kín thì số cạnh tự xuất hiện. Đó là cách dựng vừa chắc vừa có thể mở rộng sang các bài khó.",
            2.0,
        )
        next_box=VGroup(
            txt("VIDEO 11",17,BLUE,BOLD),
            txt("THIẾT DIỆN II · DIỆN TÍCH & TỶ SỐ",25,GOLD,BOLD),
            txt("Tam giác · hình thang · lục giác · đồng dạng · tỷ số diện tích",18,MUTED),
        ).arrange(DOWN,buff=0.13).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(next_box)
        self.play(FadeIn(next_box),run_time=0.55)
        self.narrate(
            "Ở video mười một, ta giữ nguyên kỹ thuật dựng nhưng bắt đầu tính: diện tích thiết diện, tỷ số diện tích, các thiết diện song song với đáy, hình thang và lục giác trong khối hộp. Khi ấy câu hỏi không chỉ là mặt phẳng cắt tạo ra hình gì, mà còn là làm thế nào biến hình không gian thành một bài hình phẳng đủ đơn giản để tính nhanh.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.principles()
        self.tetra_section()
        self.parallel_section()
        self.pyramid_external_point()
        self.cube_hexagon()
        self.errors_and_algorithm()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_10_thiet_dien_I_dung_giao_tuyen_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + Typst SAFE | HHKG 10")
    print("Angle markers: geometrically exact 3D ray-to-ray arcs")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_10.wav"
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

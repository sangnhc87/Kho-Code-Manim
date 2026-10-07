
from manim import *
from pathlib import Path
import ast
import hashlib
import json
import math
import subprocess
import sys
import time
import numpy as np

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
SMOKE_MEDIA_DIR = ROOT / "media_smoke"

BG = "#08111F"
PANEL = "#0C1A2D"
PANEL_2 = "#10233C"
INK = "#F3F7FF"
MUTED = "#8EA7C2"
GRID = "#284560"
BLUE = "#43C6F9"
CYAN = "#38E0CF"
GOLD = "#FFD84D"
GREEN = "#5CE58A"
RED = "#FF7373"
ORANGE = "#FF9B54"
PURPLE = "#B995FF"
EDGE = "#E7F0FF"
DIM = "#58718C"

def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)

_FORBIDDEN_TYPST_WORDS = {"sect", "intersect", "angle"}

def validate_typst_expr(s):
    words = set(
        s.replace("(", " ").replace(")", " ")
         .replace(",", " ").replace(";", " ").split()
    )
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(f"Forbidden Typst token(s) {bad} in {s!r}")
    if "/" in s:
        raise ValueError(f"Slash fraction forbidden in MathTypst: {s!r}")
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

def _audio_key(text):
    payload = json.dumps(
        {"text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC, "pitch": PITCH},
        ensure_ascii=False, sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]

def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
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
    fc = (
        ";".join(filters) + ";" + "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc,
         "-map", "[m]", "-ar", "48000", "-ac", "2",
         "-t", f"{video_duration:.3f}", str(out_wav)],
        check=True,
    )

def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(audio),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", str(out)],
        check=True,
    )

# ---------- fixed two-column layout ----------
HEADER_Y = 3.52
FOOTER_Y = -3.72
DIVIDER_X = 0.38
LEFT_CENTER = np.array([-3.28, -0.08, 0.0])
RIGHT_CENTER = np.array([3.66, -0.10, 0.0])
CARD_W = 5.55
CARD_H = 5.78
ROW_Y = [1.55, 0.82, 0.09, -0.64, -1.37, -2.10]

def header(video_no, title, progress):
    tag = txt(f"TRẢI PHẲNG · {video_no:02d}", 16, GOLD, BOLD)
    tag.move_to(np.array([-5.80, HEADER_Y, 0]))
    title_m = fit_width(txt(title, 25, INK, BOLD), 8.8)
    title_m.move_to(np.array([-0.55, HEADER_Y, 0]))
    prog = txt(progress, 15, MUTED, BOLD)
    prog.move_to(np.array([6.12, HEADER_Y, 0]))
    rule = Line(
        np.array([-6.75, 3.18, 0]), np.array([6.75, 3.18, 0]),
        color=GRID, stroke_width=1.0,
    )
    return VGroup(tag, title_m, prog, rule)

def footer():
    brand = txt(TEN_THAY, 14, MUTED)
    brand.move_to(np.array([-5.72, FOOTER_Y, 0]))
    series = txt("SERIES TRẢI PHẲNG · ĐƯỜNG ĐI NGẮN NHẤT", 14, MUTED)
    series.move_to(np.array([4.55, FOOTER_Y, 0]))
    return VGroup(brand, series)

def divider():
    return Line(
        np.array([DIVIDER_X, 3.06, 0]),
        np.array([DIVIDER_X, -3.32, 0]),
        color=GRID, stroke_width=1.15, stroke_opacity=0.75,
    )

def lesson_card(title, rows, accent=CYAN):
    bg = RoundedRectangle(
        width=CARD_W, height=CARD_H, corner_radius=0.12,
        fill_color=PANEL, fill_opacity=0.96,
        stroke_color=GRID, stroke_width=1.0, stroke_opacity=0.70,
    ).move_to(RIGHT_CENTER)

    bar = Line(
        bg.get_corner(UL) + RIGHT * 0.20 + DOWN * 0.12,
        bg.get_corner(DL) + RIGHT * 0.20 + UP * 0.12,
        color=accent, stroke_width=4.0,
    )
    tt = fit_width(txt(title, 22, accent, BOLD), 4.55)
    tt.move_to(np.array([RIGHT_CENTER[0] - 0.10, 2.35, 0]))

    content = VGroup()
    for i, row in enumerate(rows[:6]):
        kind, value, size, color = row
        if kind == "text":
            mob = txt(value, size, color)
            max_w, max_h = 4.35, 0.48
        elif kind == "math":
            mob = mty(value, size, color)
            max_w, max_h = 4.20, 0.52
        else:
            raise ValueError(row)

        fit_width(mob, max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        mob.move_to(np.array([RIGHT_CENTER[0], ROW_Y[i], 0]))
        content.add(mob)

    return VGroup(bg, bar, tt, content)

def intro_card(video_no, lines, subtitle):
    bg = RoundedRectangle(
        width=CARD_W, height=5.35, corner_radius=0.15,
        fill_color=PANEL, fill_opacity=0.95,
        stroke_color=GRID, stroke_width=1.0, stroke_opacity=0.70,
    ).move_to(RIGHT_CENTER)
    n = txt(f"TRẢI PHẲNG {video_no:02d}", 24, GOLD, BOLD)
    titles = VGroup(*[fit_width(txt(x, 31, INK, BOLD), 4.55) for x in lines])
    titles.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
    sub = fit_width(txt(subtitle, 18, CYAN), 4.55)
    g = VGroup(n, titles, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    g.move_to(bg.get_center()).align_to(bg, LEFT).shift(RIGHT * 0.45)
    return VGroup(bg, g)

def layout_preflight(sample_cards, verbose=True):
    for card in sample_cards:
        bg = card[0]
        title = card[2]
        body = card[3]
        for mob in [title, *list(body)]:
            if mob.get_left()[0] < bg.get_left()[0] + 0.35:
                raise AssertionError("Card item crosses left safe margin.")
            if mob.get_right()[0] > bg.get_right()[0] - 0.22:
                raise AssertionError("Card item crosses right safe margin.")
            if mob.get_top()[1] > bg.get_top()[1] - 0.18:
                raise AssertionError("Card item crosses top safe margin.")
            if mob.get_bottom()[1] < bg.get_bottom()[1] + 0.18:
                raise AssertionError("Card item crosses bottom safe margin.")
        rows = list(body)
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                overlap = min(rows[i].get_top()[1], rows[j].get_top()[1]) - max(rows[i].get_bottom()[1], rows[j].get_bottom()[1])
                if overlap > 1e-4:
                    raise AssertionError("Two right-card rows overlap.")
    if verbose:
        print("LAYOUT PREFLIGHT OK")
    return True


# ---------- geometry engine: regular tetrahedron ----------
SIDE = 3.0
SQ3 = math.sqrt(3.0)
H_TET = math.sqrt(2.0/3.0) * SIDE

# Regular tetrahedron A.BCD.
# ABC is horizontal, D is above the centroid of ABC.
RAW = {
    "A": np.array([-SIDE/2, -SQ3*SIDE/6, 0.0]),
    "B": np.array([ SIDE/2, -SQ3*SIDE/6, 0.0]),
    "C": np.array([0.0, SQ3*SIDE/3, 0.0]),
    "D": np.array([0.0, 0.0, H_TET]),
}

# The two faces used by the constrained route A -> B touching CD.
FACE1 = ["A", "C", "D"]
FACE2 = ["B", "D", "C"]

WORLD_SCALE = 0.86
WORLD_SHIFT = np.array([-3.20, -0.28, -0.20])


def W(p):
    return WORLD_SCALE * np.array(p, dtype=float) + WORLD_SHIFT


def rotate_point_axis(p, axis_a, axis_b, angle):
    p = np.array(p, dtype=float)
    a = np.array(axis_a, dtype=float)
    b = np.array(axis_b, dtype=float)
    k = b - a
    nk = np.linalg.norm(k)
    if nk < 1e-12:
        raise ValueError("Zero-length rotation axis")
    k = k / nk
    x = p - a
    return a + (
        x * math.cos(angle)
        + np.cross(k, x) * math.sin(angle)
        + k * np.dot(k, x) * (1.0 - math.cos(angle))
    )


def face_normal(vertices):
    q = np.array(vertices, dtype=float)
    n = np.cross(q[1] - q[0], q[2] - q[0])
    return n / np.linalg.norm(n)


def signed_angle_about_axis(v, w, axis):
    v = np.array(v, dtype=float)
    w = np.array(w, dtype=float)
    axis = np.array(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    return math.atan2(np.dot(axis, np.cross(v, w)), np.dot(v, w))


def unfold_angle():
    """Exact rigid rotation taking face BDC into the plane of face ACD.

    We try the two target plane normals +n and -n and choose the placement
    where the two equilateral triangles lie on opposite sides of CD.
    """
    C = RAW["C"]
    D = RAW["D"]
    axis = D - C

    n1 = face_normal([RAW[v] for v in FACE1])
    n2 = face_normal([RAW[v] for v in FACE2])

    base_cent = np.mean([RAW[v] for v in FACE1], axis=0)
    trials = []

    for target in (n1, -n1):
        ang = signed_angle_about_axis(n2, target, axis)
        Bf = rotate_point_axis(RAW["B"], C, D, ang)

        # Coplanarity error.
        plane_error = abs(np.dot(Bf - RAW["A"], n1))

        # The two triangle apices A and Bf should be on opposite sides
        # of hinge CD in the unfolded plane.
        side_A = np.dot(np.cross(axis, RAW["A"] - C), n1)
        side_B = np.dot(np.cross(axis, Bf - C), n1)
        opposite_penalty = 0 if side_A * side_B < 0 else 1

        trials.append((round(plane_error, 12), opposite_penalty, abs(ang), ang, Bf))

    trials.sort(key=lambda z: (z[0] > 1e-9, z[1], z[2]))
    return trials[0][3], trials[0][4]


UNFOLD_ANGLE, B_FLAT = unfold_angle()


def midpoint_cd():
    return (RAW["C"] + RAW["D"]) / 2.0


def geometry_preflight(verbose=True):
    tol = 1e-9

    # All six tetrahedron edges must equal SIDE.
    names = ["A","B","C","D"]
    lengths = []
    for i in range(4):
        for j in range(i+1,4):
            lengths.append(np.linalg.norm(RAW[names[i]] - RAW[names[j]]))
    if not np.allclose(lengths, [SIDE]*6, atol=tol, rtol=0):
        raise AssertionError(("Not a regular tetrahedron", lengths))

    C = RAW["C"]
    D = RAW["D"]
    A = RAW["A"]
    B = RAW["B"]
    M = midpoint_cd()

    # Hinge endpoints remain fixed.
    if np.linalg.norm(rotate_point_axis(C,C,D,UNFOLD_ANGLE)-C) > tol:
        raise AssertionError("C moved under hinge rotation")
    if np.linalg.norm(rotate_point_axis(D,C,D,UNFOLD_ANGLE)-D) > tol:
        raise AssertionError("D moved under hinge rotation")

    # B lands in plane ACD.
    n1 = face_normal([RAW[v] for v in FACE1])
    if abs(np.dot(B_FLAT-A,n1)) > 1e-8:
        raise AssertionError("Unfolded B is not in plane ACD")

    # The two equilateral triangles should be mirror images across CD.
    if abs(np.linalg.norm(A-C) - SIDE) > tol or abs(np.linalg.norm(B_FLAT-C)-SIDE) > tol:
        raise AssertionError("Triangle edge length changed")
    if abs(np.linalg.norm(A-D) - SIDE) > tol or abs(np.linalg.norm(B_FLAT-D)-SIDE) > tol:
        raise AssertionError("Triangle edge length changed")

    # A -> B_flat crosses CD at its midpoint.
    line = B_FLAT - A
    axis = D - C
    # Solve A + t line = C + u axis.
    Mmat = np.column_stack([line, -axis])
    sol, *_ = np.linalg.lstsq(Mmat, C-A, rcond=None)
    t, u = sol
    P = A + t*line
    Q = C + u*axis
    if np.linalg.norm(P-Q) > 1e-8:
        raise AssertionError("Unfolded segment does not intersect CD")
    if abs(t-0.5) > 1e-8 or abs(u-0.5) > 1e-8:
        raise AssertionError(("Intersection not midpoint", t, u))

    # Lengths.
    Lflat = np.linalg.norm(B_FLAT-A)
    Lfold = np.linalg.norm(M-A) + np.linalg.norm(B-M)
    expected = SIDE*math.sqrt(3)
    if abs(Lflat-expected) > 1e-8 or abs(Lfold-expected) > 1e-8:
        raise AssertionError(("Wrong shortest length",Lflat,Lfold,expected))

    # Algebraic check for X on CD:
    # L(x)=2*sqrt((x-a/2)^2+3a^2/4), min at x=a/2.
    xs = np.linspace(0.0,SIDE,4001)
    vals = 2*np.sqrt((xs-SIDE/2)**2 + 3*SIDE**2/4)
    idx = int(np.argmin(vals))
    if abs(xs[idx]-SIDE/2) > SIDE/4000 + 1e-9:
        raise AssertionError("Numerical minimizer not midpoint")
    if abs(vals[idx]-expected) > 1e-8:
        raise AssertionError("Numerical minimum incorrect")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  regular tetrahedron: all 6 edges equal")
        print("  face BCD unfolds rigidly about CD")
        print("  A-B_flat crosses CD at midpoint M")
        print("  AM = MB = sqrt(3)a/2")
        print("  constrained minimum = a*sqrt(3)")
    return True


def solid(a,b,color=EDGE,width=4.0,opacity=0.96):
    return Line(np.array(a,float),np.array(b,float),color=color,stroke_width=width,stroke_opacity=opacity)


def hidden_edge(a,b,color=DIM,width=2.6,opacity=0.67):
    return DashedLine(np.array(a,float),np.array(b,float),color=color,stroke_width=width,
                      stroke_opacity=opacity,dash_length=0.11,dashed_ratio=0.56)


def face_poly(points,color=BLUE,opacity=0.12):
    return Polygon(*[np.array(p,float) for p in points],
                   fill_color=color,fill_opacity=opacity,stroke_width=0)


def tetra_shell():
    p={k:W(v) for k,v in RAW.items()}

    fills=VGroup(
        face_poly([p["A"],p["C"],p["D"]],PURPLE,0.08),
        face_poly([p["B"],p["D"],p["C"]],CYAN,0.08),
        face_poly([p["A"],p["B"],p["D"]],BLUE,0.05),
    )

    # Fixed camera chosen so AB, AC, AD, BD, CD are visible; BC is rear/hidden.
    visible_pairs=[("A","B"),("A","C"),("A","D"),("B","D"),("C","D")]
    hidden_pairs=[("B","C")]

    edges=VGroup(*[solid(p[u],p[v],EDGE,3.8) for u,v in visible_pairs])
    hidden=VGroup(*[hidden_edge(p[u],p[v]) for u,v in hidden_pairs])
    return VGroup(fills,edges,hidden)


def highlighted_faces():
    p={k:W(v) for k,v in RAW.items()}
    return VGroup(
        face_poly([p["A"],p["C"],p["D"]],PURPLE,0.18),
        face_poly([p["B"],p["D"],p["C"]],CYAN,0.18),
    )


def vertex_labels(keys):
    labs=VGroup()
    offsets={
        "A":np.array([-0.12,-0.12,-0.10]),
        "B":np.array([0.12,-0.12,-0.10]),
        "C":np.array([0.00,0.13,-0.05]),
        "D":np.array([0.00,0.00,0.18]),
    }
    for k in keys:
        color=GREEN if k=="A" else (RED if k=="B" else INK)
        lab=mty(k,23,color).move_to(W(RAW[k])+offsets[k])
        labs.add(lab)
    return labs


def unfolding_group(theta):
    """Return face ACD fixed and face BCD rotated by theta about CD."""
    C,D=RAW["C"],RAW["D"]
    B_now=rotate_point_axis(RAW["B"],C,D,theta)

    fixed=VGroup(
        face_poly([W(RAW["A"]),W(C),W(D)],PURPLE,0.18),
        solid(W(RAW["A"]),W(C),PURPLE,3.5),
        solid(W(C),W(D),GOLD,6.5),
        solid(W(D),W(RAW["A"]),PURPLE,3.5),
        Dot3D(W(RAW["A"]),radius=0.075,color=GREEN),
    )

    moving=VGroup(
        face_poly([W(B_now),W(D),W(C)],CYAN,0.18),
        solid(W(B_now),W(D),CYAN,3.5),
        solid(W(D),W(C),GOLD,6.5),
        solid(W(C),W(B_now),CYAN,3.5),
        Dot3D(W(B_now),radius=0.075,color=RED),
    )
    return fixed,moving


def net_2d():
    """Exact 2D net of two equilateral triangles sharing CD."""
    a=SIDE
    C=np.array([-a/2,0.0,0.0])
    D=np.array([ a/2,0.0,0.0])
    A=np.array([0.0, SQ3*a/2, 0.0])
    Bf=np.array([0.0,-SQ3*a/2,0.0])

    pts=np.array([C[:2],D[:2],A[:2],Bf[:2]])
    minx,miny=pts.min(axis=0); maxx,maxy=pts.max(axis=0)
    scale=min(5.6/(maxx-minx),4.8/(maxy-miny))
    mid=np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p[:2])-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    C2,D2,A2,B2=map(T,[C,D,A,Bf])
    M2=(C2+D2)/2

    g=VGroup(
        Polygon(A2,C2,D2,fill_color=PURPLE,fill_opacity=0.16,
                stroke_color=PURPLE,stroke_width=3.0),
        Polygon(B2,D2,C2,fill_color=CYAN,fill_opacity=0.16,
                stroke_color=CYAN,stroke_width=3.0),
        Line(C2,D2,color=GOLD,stroke_width=6.0),
        Line(A2,B2,color=GOLD,stroke_width=6.5),
        Dot(A2,radius=0.075,color=GREEN),
        Dot(B2,radius=0.075,color=RED),
        Dot(M2,radius=0.060,color=GOLD),
    )
    return g, {"A":A2,"Bf":B2,"C":C2,"D":D2,"M":M2}


def folded_path():
    M=midpoint_cd()
    path=VGroup(
        solid(W(RAW["A"]),W(M),GOLD,6.5),
        solid(W(M),W(RAW["B"]),GOLD,6.5),
        Dot3D(W(M),radius=0.065,color=GOLD),
    )
    return path,[RAW["A"],M,RAW["B"]]


def layout_samples():
    return [
        lesson_card("BÀI TOÁN",[
            ("text","Tứ diện đều ABCD cạnh a.",19,INK),
            ("text","Kiến đi từ A đến B.",19,INK),
            ("text","Bắt buộc chạm cạnh đối CD.",19,GOLD),
            ("math","L_(min)=?",34,CYAN),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","C M=M D=frac(a,2)",28,CYAN),
            ("math","A M=M B=frac(a sqrt(3),2)",27,INK),
            ("math","L_(min)=a sqrt(3)",34,GOLD),
        ],CYAN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.96)

    def narrate(self,text,min_visual_time=1.0):
        audio=create_audio(text); dur=probe_duration(audio)
        self.audio_events.append((self.time,audio))
        self.wait(max(dur,min_visual_time))
        return dur

    def narrate_play(self,text,*anims,min_time=1.0,rate_func=smooth):
        audio=create_audio(text); dur=probe_duration(audio)
        self.audio_events.append((self.time,audio))
        self.play(*anims,run_time=max(dur,min_time),rate_func=rate_func)
        return dur

    def add_hud(self,title,progress):
        h=header(7,title,progress); f=footer(); d=divider()
        self.add_fixed_in_frame_mobjects(h,f,d)
        return VGroup(h,f,d)

    def clear_all(self,run_time=0.28):
        mobs=list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs],run_time=run_time)
        self.clear()


def narration_lint(source_path:Path,verbose=True):
    tree=ast.parse(source_path.read_text(encoding="utf-8"))
    spoken=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            fname=node.func.attr if isinstance(node.func,ast.Attribute) else None
            if fname in {"narrate","narrate_play"} and node.args:
                first=node.args[0]
                if isinstance(first,ast.Constant) and isinstance(first.value,str):
                    spoken.append(first.value)
    forbidden=["workflow","render","preflight","engine","code","mã nguồn",
               "camera","animation","cột trái","cột phải","debug"]
    bad=[]
    for line in spoken:
        low=line.lower()
        for word in forbidden:
            if word in low:
                bad.append((word,line))
    if bad:
        raise AssertionError(bad)
    if verbose:
        print(f"NARRATION LINT OK: {len(spoken)} segments")
    return True


class TraiPhang07Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(tetra_shell())
        labs=vertex_labels(["A","B","C","D"])
        for lab in labs:
            self.add_fixed_orientation_mobjects(lab)

        card=intro_card(
            7,
            ["TỨ DIỆN ĐỀU","ĐI QUA CẠNH ĐỐI"],
            "Từ một đỉnh đến một đỉnh, nhưng phải chạm cạnh CD.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Ta chuyển sang một mô hình mới: tứ diện đều. "
            "Bốn mặt đều là tam giác đều cạnh a.",
            1.4,
        )
        self.narrate(
            "Con kiến bắt đầu ở đỉnh A và muốn tới đỉnh B. "
            "Nhưng lần này nó bắt buộc phải chạm cạnh đối C D trước khi tới B.",
            1.6,
        )

    def problem(self):
        self.clear_all()
        self.add_hud("Từ A đến B nhưng phải chạm CD","01 / 11")
        self.add(tetra_shell(),highlighted_faces())
        labs=vertex_labels(["A","B","C","D"])
        for lab in labs:
            self.add_fixed_orientation_mobjects(lab)

        card=lesson_card("BÀI TOÁN",[
            ("text","Tứ diện đều ABCD cạnh a.",19,INK),
            ("text","Kiến đi từ A đến B.",19,INK),
            ("text","Bắt buộc chạm cạnh đối CD.",19,GOLD),
            ("text","Tìm đường ngắn nhất trên mặt tứ diện.",18,CYAN),
            ("math","L_(min)=?",34,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu không có điều kiện, đường ngắn nhất chỉ là cạnh A B và có độ dài a.",
            1.4,
        )
        self.narrate(
            "Điều kiện phải chạm cạnh C D làm bài toán thay đổi hoàn toàn. "
            "Ta phải đi từ A trên mặt A C D tới một điểm của C D, rồi từ đó sang mặt B C D để tới B.",
            1.8,
        )

    def arbitrary_x(self):
        self.clear_all()
        self.add_hud("Gọi X là điểm kiến chạm cạnh CD","02 / 11")
        self.add(tetra_shell(),highlighted_faces())
        C,D=RAW["C"],RAW["D"]
        X=0.28*C+0.72*D
        path=VGroup(
            solid(W(RAW["A"]),W(X),ORANGE,6.0),
            solid(W(X),W(RAW["B"]),ORANGE,6.0),
            Dot3D(W(X),radius=0.065,color=ORANGE),
        )
        self.add(path)
        card=lesson_card("VỚI X BẤT KỲ TRÊN CD",[
            ("math","L(X)=A X+X B",31,ORANGE),
            ("text","AX nằm trên mặt ACD.",19,INK),
            ("text","XB nằm trên mặt BCD.",19,INK),
            ("text","Cần chọn X sao cho tổng nhỏ nhất.",19,CYAN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Gọi X là điểm mà kiến chạm vào cạnh C D. "
            "Khi đó đường đi gồm hai đoạn: A X trên mặt A C D và X B trên mặt B C D.",
            1.6,
        )
        self.narrate(
            "Bài toán bây giờ là chọn vị trí X trên C D sao cho tổng A X cộng X B nhỏ nhất.",
            1.5,
        )

    def isolate_faces(self):
        self.clear_all()
        self.add_hud("Chỉ cần hai mặt ACD và BCD","03 / 11")
        self.add(highlighted_faces())
        C,D=RAW["C"],RAW["D"]
        self.add(solid(W(C),W(D),GOLD,7.0))
        card=lesson_card("CẠNH CHUNG",[
            ("text","Hai mặt cần dùng: ACD và BCD.",19,INK),
            ("text","Cạnh chung của chúng là CD.",19,GOLD),
            ("text","Ta giữ mặt ACD.",19,INK),
            ("text","Mở mặt BCD quanh CD.",19,CYAN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta chỉ cần hai mặt A C D và B C D. Hai mặt này có cạnh chung C D.",
            1.4,
        )
        self.narrate(
            "Giữ mặt A C D, rồi mở mặt B C D quanh cạnh C D. "
            "Khi hai tam giác nằm chung trên một mặt phẳng, đường gấp A X B sẽ trở thành một đường trong mặt phẳng.",
            1.8,
        )

    def unfold(self):
        self.clear_all()
        self.add_hud("Mở mặt BCD quanh cạnh CD","04 / 11")
        theta=ValueTracker(0.0)
        fixed,moving=unfolding_group(0.0)
        self.add(fixed)
        moving_dyn=always_redraw(lambda: unfolding_group(theta.get_value())[1])
        self.add(moving_dyn)

        card=lesson_card("MỞ HAI TAM GIÁC ĐỀU",[
            ("text","C và D đứng yên trên cạnh chung.",19,INK),
            ("text","B đi theo mặt BCD.",19,CYAN),
            ("text","Sau khi mở, hai tam giác nằm phẳng.",19,GOLD),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Các em nhìn cạnh C D: cạnh này đứng yên. "
            "Điểm B đi theo mặt B C D cho đến khi hai tam giác đều nằm trên cùng một mặt phẳng.",
            theta.animate.set_value(UNFOLD_ANGLE),
            min_time=3.3,
            rate_func=smooth,
        )
        self.narrate(
            "Ta gọi ảnh của B sau khi mở là B một. "
            "Lúc này bài toán chỉ còn là tìm đường ngắn nhất từ A tới B một có cắt đoạn C D.",
            1.6,
        )

    def net_solution(self):
        self.clear_all()
        self.add_hud("Đường ngắn nhất trên bản trải","05 / 11")
        net,pts=net_2d()
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("HAI TAM GIÁC ĐỀU",[
            ("text","A và B₁ đối xứng qua CD.",19,INK),
            ("text","Đoạn AB₁ vuông góc CD.",19,CYAN),
            ("text","AB₁ cắt CD tại trung điểm M.",19,GOLD),
            ("math","C M=M D=frac(a,2)",29,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Sau khi trải, hai tam giác đều nằm ở hai phía của cạnh C D. "
            "Hai đỉnh A và B một đối xứng nhau qua C D.",
            1.6,
        )
        self.narrate(
            "Vì thế đoạn thẳng A B một vuông góc với C D và cắt C D tại trung điểm M.",
            1.5,
        )

    def compute_length(self):
        self.clear_all()
        self.add_hud("Tính độ dài","06 / 11")
        net,pts=net_2d()
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("TRONG TAM GIÁC ĐỀU",[
            ("math","A M=frac(a sqrt(3),2)",29,PURPLE),
            ("math","M B_1=frac(a sqrt(3),2)",29,CYAN),
            ("math","A B_1=a sqrt(3)",34,GOLD),
            ("math","L_(min)=a sqrt(3)",34,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trong tam giác đều cạnh a, đường cao bằng a căn ba trên hai. "
            "Do đó A M bằng a căn ba trên hai.",
            1.5,
        )
        self.narrate(
            "Tương tự M B một cũng bằng a căn ba trên hai. "
            "Cộng lại, độ dài đường thẳng A B một bằng a căn ba.",
            1.6,
        )

    def algebra_check(self):
        self.clear_all()
        self.add_hud("Kiểm tra lại bằng một biến","07 / 11")
        net,pts=net_2d()
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("ĐẶT C X=x",[
            ("math","0<=x<=a",26,INK),
            ("math","A X^2=(x-frac(a,2))^2+frac(3a^2,4)",25,PURPLE),
            ("math","X B^2=(x-frac(a,2))^2+frac(3a^2,4)",25,CYAN),
            ("text","Tổng nhỏ nhất khi x=a/2.",19,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta có thể kiểm tra kết quả mà không cần dựa vào hình đối xứng. "
            "Đặt C X bằng x.",
            1.3,
        )
        self.narrate(
            "Trong mỗi tam giác đều, bình phương khoảng cách tới X bằng bình phương x trừ a trên hai, cộng ba a bình phương trên bốn.",
            1.8,
        )
        self.narrate(
            "Hai đoạn A X và X B có cùng độ dài. Tổng của chúng nhỏ nhất khi x bằng a trên hai, tức X chính là trung điểm M.",
            1.7,
        )

    def fold_back(self):
        self.clear_all()
        self.add_hud("Gấp trở lại tứ diện","08 / 11")
        path,pts3=folded_path()
        self.add(tetra_shell(),highlighted_faces(),path)
        card=lesson_card("ĐƯỜNG TRÊN KHỐI",[
            ("text","M là trung điểm của CD.",19,GOLD),
            ("text","AM nằm trên mặt ACD.",19,INK),
            ("text","MB nằm trên mặt BCD.",19,INK),
            ("math","A M+M B=a sqrt(3)",30,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Gấp hai tam giác trở lại. Đoạn thẳng trên bản trải tách thành A M trên mặt A C D và M B trên mặt B C D.",
            1.7,
        )
        self.narrate(
            "Điểm chuyển mặt M chính là trung điểm của cạnh đối C D.",
            1.4,
        )

    def ant_walk(self):
        self.clear_all()
        self.add_hud("Kiến đi theo đường tối ưu","09 / 11")
        path,pts3=folded_path()
        self.add(tetra_shell(),highlighted_faces(),path)
        ant=Dot3D(W(pts3[0]),radius=0.085,color=GREEN)
        self.add(ant)
        card=lesson_card("HÀNH TRÌNH",[
            ("math","A -> M -> B",31,GOLD),
            ("math","C M=M D=frac(a,2)",27,CYAN),
            ("math","L_(min)=a sqrt(3)",34,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Kiến đi từ A tới trung điểm M của C D trên mặt A C D.",
            MoveAlongPath(ant,Line(W(pts3[0]),W(pts3[1]))),
            min_time=2.0,rate_func=linear,
        )
        self.narrate_play(
            "Tại M, nó chuyển sang mặt B C D và đi thẳng tới B.",
            MoveAlongPath(ant,Line(W(pts3[1]),W(pts3[2]))),
            min_time=2.0,rate_func=linear,
        )

    def opposite_edges(self):
        self.clear_all()
        self.add_hud("Ba cặp cạnh đối trong tứ diện đều","10 / 11")
        self.add(tetra_shell())
        card=lesson_card("DO TÍNH ĐỐI XỨNG",[
            ("text","AB và CD là một cặp cạnh đối.",19,GOLD),
            ("text","AC và BD là một cặp cạnh đối.",19,CYAN),
            ("text","AD và BC là một cặp cạnh đối.",19,ORANGE),
            ("text","Bài toán tương tự cho ba cặp cạnh đối.",19,INK),
            ("text","Đường tối ưu luôn đi qua trung điểm cạnh đối.",18,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Tứ diện đều có ba cặp cạnh đối: A B với C D, A C với B D, và A D với B C.",
            1.6,
        )
        self.narrate(
            "Nhờ tính đối xứng, nếu đổi tên các đỉnh thì cách giải hoàn toàn giống nhau: "
            "trải hai mặt có cạnh đối làm cạnh chung, rồi nối thẳng hai ảnh.",
            1.7,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài tứ diện đều","11 / 11")
        self.add(tetra_shell(),highlighted_faces())
        card=lesson_card("BA Ý CẦN NHỚ",[
            ("text","1. Điều kiện phải chạm cạnh đối làm bài toán không còn tầm thường.",18,INK),
            ("text","2. Trải hai tam giác đều qua cạnh chung.",18,INK),
            ("text","3. Đường thẳng đi qua trung điểm cạnh đối.",18,INK),
            ("math","L_(min)=a sqrt(3)",34,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bài tứ diện đều cho một kiểu bản trải mới: không còn các hình chữ nhật, mà là hai tam giác đều ghép theo cạnh chung.",
            1.6,
        )
        self.narrate(
            "Điểm mấu chốt vẫn không đổi. Sau khi trải đúng hai mặt, đường ngắn nhất trở thành một đoạn thẳng. "
            "Trong bài này đoạn ấy đi qua trung điểm cạnh C D và có độ dài a căn ba.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.problem()
        self.arbitrary_x()
        self.isolate_faces()
        self.unfold()
        self.net_solution()
        self.compute_length()
        self.algebra_check()
        self.fold_back()
        self.ant_walk()
        self.opposite_edges()
        self.summary()


class Smoke07(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.96)
        theta=ValueTracker(0.0)
        fixed,_=unfolding_group(0.0)
        moving=always_redraw(lambda: unfolding_group(theta.get_value())[1])
        self.add(fixed,moving)
        self.play(theta.animate.set_value(UNFOLD_ANGLE),run_time=1.4,rate_func=smooth)
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_07_master_smoke"
    config.disable_caching=True
    scene=Smoke07()
    scene.render()
    path=Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():
        raise RuntimeError(path)
    return path


def render_full():
    geometry_preflight(True)
    layout_preflight(layout_samples(),True)
    config.pixel_width=FINAL_WIDTH
    config.pixel_height=FINAL_HEIGHT
    config.frame_rate=FINAL_FPS
    config.media_dir=str(MEDIA_DIR)
    config.output_file="trai_phang_07_tu_dien_deu_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang07Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)
    master_wav=ROOT/"master_narration_trai_phang_07.wav"
    build_master_audio(scene.audio_events,duration,master_wav)

    final_path=video_path.with_name(video_path.stem+"_WITH_AUDIO.mp4")
    mux_audio(video_path,master_wav,final_path)

    print("VIDEO HOAN CHINH:",final_path)
    return final_path


if __name__=="__main__":
    source_path=Path(sys.argv[0]).resolve()
    if "--narration-lint" in sys.argv:
        narration_lint(source_path,True)
        raise SystemExit(0)
    if "--geometry-preflight" in sys.argv:
        geometry_preflight(True)
        raise SystemExit(0)
    if "--layout-preflight" in sys.argv:
        layout_preflight(layout_samples(),True)
        raise SystemExit(0)
    if "--smoke-render" in sys.argv:
        render_smoke()
        raise SystemExit(0)
    render_full()

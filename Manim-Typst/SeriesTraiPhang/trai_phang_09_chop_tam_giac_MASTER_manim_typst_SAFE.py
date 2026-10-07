
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




# ---------- geometry engine: asymmetric triangular pyramid ----------
# One concrete tetrahedral pyramid S.ABC.
#
# In the two faces around the required opposite edge SC:
#   SC = 10
#   AH perp SC, SH = 2, AH = 3
#   BK perp SC, SK = 8, BK = 5
#
# We choose (ASC) perpendicular to (BSC) for the 3D model.
# This gives an exact, clean unfolding:
#   A = (2, 3), B_flat = (8, -5)
#   Lmin = 10
#   SM = 17/4
# ==========================================================

# Construction coordinates before a rigid change of basis.
ORIG = {
    "S": np.array([0.0, 0.0, 0.0]),
    "C": np.array([10.0, 0.0, 0.0]),
    "A": np.array([2.0, 3.0, 0.0]),
    "B": np.array([8.0, 0.0, 5.0]),
}

def _base_horizontal(raw):
    """Rigidly express ABC as z=0 and place S above it for a clean 3D view."""
    A, B, C, S = [raw[k] for k in ("A","B","C","S")]
    O = (A + B + C) / 3.0

    e1 = B - A
    e1 = e1 / np.linalg.norm(e1)

    temp = C - A
    e2 = temp - np.dot(temp, e1) * e1
    e2 = e2 / np.linalg.norm(e2)

    e3 = np.cross(e1, e2)
    e3 = e3 / np.linalg.norm(e3)
    if np.dot(S - O, e3) < 0:
        e3 = -e3

    R = np.stack([e1, e2, e3], axis=0)
    return {k: R @ (p - O) for k, p in raw.items()}

RAW = _base_horizontal(ORIG)

FACES = {
    "base": ["A","B","C"],
    "sab": ["S","A","B"],
    "sbc": ["S","B","C"],
    "sca": ["S","C","A"],
}
FACE_COLORS = {
    "base": BLUE,
    "sab": ORANGE,
    "sbc": CYAN,
    "sca": PURPLE,
}

CORRECT_FACES = ["sca","sbc"]
WRONG_FACES = ["sab","base"]

WORLD_SCALE = 0.62
WORLD_SHIFT = np.array([-3.18, -0.22, -0.15])

CAM_PHI = 67 * DEGREES
CAM_THETA = -48 * DEGREES


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


def face_normal(points):
    q = np.array(points, dtype=float)
    n = np.cross(q[1] - q[0], q[2] - q[0])
    return n / np.linalg.norm(n)


def outward_normal(face_name):
    pts = [RAW[v] for v in FACES[face_name]]
    n = face_normal(pts)
    poly_cent = np.mean(list(RAW.values()), axis=0)
    face_cent = np.mean(pts, axis=0)
    if np.dot(n, face_cent - poly_cent) < 0:
        n = -n
    return n


def camera_direction():
    return np.array([
        math.sin(CAM_PHI) * math.cos(CAM_THETA),
        math.sin(CAM_PHI) * math.sin(CAM_THETA),
        math.cos(CAM_PHI),
    ])


def edge_visibility():
    """Classify tetrahedron edges for the fixed camera."""
    faces_by_edge = {}
    for fname, verts in FACES.items():
        for i in range(3):
            u, v = verts[i], verts[(i+1) % 3]
            key = tuple(sorted((u, v)))
            faces_by_edge.setdefault(key, []).append(fname)

    cam = camera_direction()
    front = {
        f: np.dot(outward_normal(f), cam) > 0
        for f in FACES
    }

    visible, hidden = [], []
    for edge, fs in faces_by_edge.items():
        if any(front[f] for f in fs):
            visible.append(edge)
        else:
            hidden.append(edge)
    return visible, hidden


def signed_angle_about_axis(v, w, axis):
    v = np.array(v, dtype=float)
    w = np.array(w, dtype=float)
    axis = np.array(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    return math.atan2(
        np.dot(axis, np.cross(v, w)),
        np.dot(v, w),
    )


def unfold_b_about_sc():
    """Rotate face SBC into the plane of SCA, placing B opposite A across SC."""
    S = RAW["S"]
    C = RAW["C"]
    axis = C - S

    n_fixed = face_normal([RAW[v] for v in FACES["sca"]])
    n_move = face_normal([RAW[v] for v in FACES["sbc"]])

    fixed_cent = np.mean([RAW[v] for v in FACES["sca"]], axis=0)

    trials = []
    for target in (n_fixed, -n_fixed):
        ang = signed_angle_about_axis(n_move, target, axis)
        Bf = rotate_point_axis(RAW["B"], S, C, ang)

        plane_error = abs(np.dot(Bf - RAW["A"], n_fixed))

        moved_cent = np.mean([
            rotate_point_axis(RAW[v], S, C, ang)
            for v in FACES["sbc"]
        ], axis=0)

        side_A = np.dot(np.cross(axis, fixed_cent - S), n_fixed)
        side_B = np.dot(np.cross(axis, moved_cent - S), n_fixed)
        opposite_penalty = 0 if side_A * side_B < 0 else 1

        trials.append((round(plane_error, 12), opposite_penalty, abs(ang), ang, Bf))

    trials.sort(key=lambda z: (z[0] > 1e-9, z[1], z[2]))
    _, _, _, ang, Bf = trials[0]
    return ang, Bf


UNFOLD_ANGLE, B_FLAT = unfold_b_about_sc()

H_RAW = RAW["S"] + 0.2 * (RAW["C"] - RAW["S"])   # SH=2 on SC=10
K_RAW = RAW["S"] + 0.8 * (RAW["C"] - RAW["S"])   # SK=8
M_RAW = RAW["S"] + (17.0/40.0) * (RAW["C"] - RAW["S"])  # SM=17/4


def geometry_preflight(verbose=True):
    tol = 1e-9

    # Design-side checks.
    S0, C0, A0, B0 = [ORIG[k] for k in ("S","C","A","B")]
    H0 = S0 + 0.2*(C0-S0)
    K0 = S0 + 0.8*(C0-S0)

    if abs(np.linalg.norm(C0-S0)-10.0) > tol:
        raise AssertionError("SC must equal 10")
    if abs(np.linalg.norm(H0-S0)-2.0) > tol:
        raise AssertionError("SH must equal 2")
    if abs(np.linalg.norm(A0-H0)-3.0) > tol:
        raise AssertionError("AH must equal 3")
    if abs(np.dot(A0-H0, C0-S0)) > tol:
        raise AssertionError("AH must be perpendicular to SC")
    if abs(np.linalg.norm(K0-S0)-8.0) > tol:
        raise AssertionError("SK must equal 8")
    if abs(np.linalg.norm(B0-K0)-5.0) > tol:
        raise AssertionError("BK must equal 5")
    if abs(np.dot(B0-K0, C0-S0)) > tol:
        raise AssertionError("BK must be perpendicular to SC")

    # Two relevant faces are perpendicular in the chosen concrete 3D model.
    n1 = face_normal([ORIG[v] for v in FACES["sca"]])
    n2 = face_normal([ORIG[v] for v in FACES["sbc"]])
    if abs(np.dot(n1, n2)) > tol:
        raise AssertionError("Chosen model should have perpendicular relevant faces")

    # Rigid unfolding around SC.
    S, C = RAW["S"], RAW["C"]
    if np.linalg.norm(rotate_point_axis(S,S,C,UNFOLD_ANGLE)-S) > tol:
        raise AssertionError("S moved during hinge rotation")
    if np.linalg.norm(rotate_point_axis(C,S,C,UNFOLD_ANGLE)-C) > tol:
        raise AssertionError("C moved during hinge rotation")

    fixed_n = face_normal([RAW[v] for v in FACES["sca"]])
    if abs(np.dot(B_FLAT - RAW["A"], fixed_n)) > 1e-8:
        raise AssertionError("B_flat not coplanar with face SCA")

    # Use the original exact 2D unfolded coordinates:
    # S=(0,0), C=(10,0), A=(2,3), B1=(8,-5).
    A2 = np.array([2.0,3.0])
    B2 = np.array([8.0,-5.0])
    S2 = np.array([0.0,0.0])
    C2 = np.array([10.0,0.0])

    v = B2 - A2
    t = -A2[1] / v[1]
    M2 = A2 + t*v

    if abs(t - 3.0/8.0) > tol:
        raise AssertionError("Wrong line parameter")
    if np.linalg.norm(M2 - np.array([17.0/4.0,0.0])) > tol:
        raise AssertionError("Wrong crossing point M")
    if not (0.0 < M2[0] < 10.0):
        raise AssertionError("M must lie in the interior of SC")

    AM = np.linalg.norm(M2-A2)
    MB = np.linalg.norm(B2-M2)
    L = np.linalg.norm(B2-A2)

    if abs(AM - 15.0/4.0) > tol:
        raise AssertionError("AM should be 15/4")
    if abs(MB - 25.0/4.0) > tol:
        raise AssertionError("MB should be 25/4")
    if abs(L - 10.0) > tol:
        raise AssertionError("Unfolded length should be 10")
    if abs((AM+MB) - L) > tol:
        raise AssertionError("Folded and unfolded lengths disagree")

    # Direct AB is shorter but violates the required interior-SC condition.
    AB = np.linalg.norm(ORIG["A"] - ORIG["B"])
    if abs(AB - math.sqrt(70.0)) > tol:
        raise AssertionError("AB should be sqrt(70)")
    if not (AB < 10.0):
        raise AssertionError("Direct edge should be shorter than constrained route")

    # General formula check:
    # A=(p,h1), B'=(q,-h2).
    p,q,h1,h2 = 2.0,8.0,3.0,5.0
    xM = (h2*p + h1*q)/(h1+h2)
    Lg = math.sqrt((q-p)**2 + (h1+h2)**2)
    if abs(xM-17.0/4.0)>tol or abs(Lg-10.0)>tol:
        raise AssertionError("General formula mismatch")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  triangular pyramid S.ABC")
        print("  SC=10, SH=2, AH=3, SK=8, BK=5")
        print("  correct strip: ASC + BSC")
        print("  unfolded A=(2,3), B1=(8,-5)")
        print("  M=(17/4,0), AM=15/4, MB=25/4")
        print("  constrained Lmin=10")
        print("  direct AB=sqrt(70) is shorter but invalid for the SC-interior constraint")
    return True


def solid(a,b,color=EDGE,width=4.0,opacity=0.96):
    return Line(
        np.array(a,float), np.array(b,float),
        color=color, stroke_width=width, stroke_opacity=opacity
    )


def hidden_edge(a,b,color=DIM,width=2.6,opacity=0.68):
    return DashedLine(
        np.array(a,float), np.array(b,float),
        color=color, stroke_width=width, stroke_opacity=opacity,
        dash_length=0.11, dashed_ratio=0.56
    )


def face_poly(points,color=BLUE,opacity=0.12):
    return Polygon(
        *[np.array(p,float) for p in points],
        fill_color=color, fill_opacity=opacity, stroke_width=0
    )


def pyramid_shell():
    p = {k:W(v) for k,v in RAW.items()}

    fills = VGroup(
        face_poly([p[v] for v in FACES["sab"]], ORANGE, 0.050),
        face_poly([p[v] for v in FACES["sbc"]], CYAN, 0.080),
        face_poly([p[v] for v in FACES["sca"]], PURPLE, 0.065),
    )

    visible, hidden = edge_visibility()
    edges = VGroup(*[
        solid(p[u],p[v],EDGE,3.8) for u,v in visible
    ])
    hidden_g = VGroup(*[
        hidden_edge(p[u],p[v]) for u,v in hidden
    ])
    return VGroup(fills,edges,hidden_g)


def highlight_faces(face_names, opacity=0.17):
    return VGroup(*[
        face_poly([W(RAW[v]) for v in FACES[f]], FACE_COLORS[f], opacity)
        for f in face_names
    ])


def vertex_labels(keys):
    offsets = {
        "A": np.array([-0.13,-0.13,-0.04]),
        "B": np.array([ 0.14,-0.12,-0.03]),
        "C": np.array([ 0.13, 0.14,-0.03]),
        "S": np.array([-0.04, 0.02, 0.20]),
    }
    labs = VGroup()
    for k in keys:
        color = GREEN if k=="A" else (RED if k=="B" else INK)
        labs.add(mty(k,23,color).move_to(W(RAW[k])+offsets[k]))
    return labs


def feet_group():
    g = VGroup(
        Dot3D(W(H_RAW), radius=0.060, color=GOLD),
        Dot3D(W(K_RAW), radius=0.060, color=CYAN),
        solid(W(RAW["A"]), W(H_RAW), GOLD, 4.5),
        solid(W(RAW["B"]), W(K_RAW), CYAN, 4.5),
        solid(W(RAW["S"]), W(RAW["C"]), EDGE, 4.0),
    )
    return g


def unfolding_group(theta):
    S,C = RAW["S"],RAW["C"]
    B_now = rotate_point_axis(RAW["B"],S,C,theta)

    fixed = VGroup(
        face_poly([W(RAW["S"]),W(RAW["C"]),W(RAW["A"])],PURPLE,0.18),
        solid(W(RAW["S"]),W(RAW["C"]),GOLD,6.5),
        solid(W(RAW["C"]),W(RAW["A"]),PURPLE,3.4),
        solid(W(RAW["A"]),W(RAW["S"]),PURPLE,3.4),
        Dot3D(W(RAW["A"]),radius=0.075,color=GREEN),
    )

    moving = VGroup(
        face_poly([W(RAW["S"]),W(B_now),W(RAW["C"])],CYAN,0.18),
        solid(W(RAW["S"]),W(RAW["C"]),GOLD,6.5),
        solid(W(RAW["S"]),W(B_now),CYAN,3.4),
        solid(W(B_now),W(RAW["C"]),CYAN,3.4),
        Dot3D(W(B_now),radius=0.075,color=RED),
    )
    return fixed,moving


def net_2d(show_line=True, show_feet=True):
    # Exact unfolded plane:
    # S=(0,0), C=(10,0), A=(2,3), B1=(8,-5)
    S=np.array([0.0,0.0,0.0])
    C=np.array([10.0,0.0,0.0])
    A=np.array([2.0,3.0,0.0])
    B1=np.array([8.0,-5.0,0.0])
    H=np.array([2.0,0.0,0.0])
    K=np.array([8.0,0.0,0.0])
    M=np.array([17.0/4.0,0.0,0.0])

    pts=np.array([S[:2],C[:2],A[:2],B1[:2]])
    minx,miny=pts.min(axis=0); maxx,maxy=pts.max(axis=0)
    scale=min(5.8/(maxx-minx),4.9/(maxy-miny))
    mid=np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p[:2])-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    S2,C2,A2,B2,H2,K2,M2 = map(T,[S,C,A,B1,H,K,M])

    g = VGroup(
        Polygon(S2,C2,A2,fill_color=PURPLE,fill_opacity=0.16,
                stroke_color=PURPLE,stroke_width=3.0),
        Polygon(S2,B2,C2,fill_color=CYAN,fill_opacity=0.16,
                stroke_color=CYAN,stroke_width=3.0),
        Line(S2,C2,color=GOLD,stroke_width=6.0),
        Dot(A2,radius=0.075,color=GREEN),
        Dot(B2,radius=0.075,color=RED),
    )

    if show_feet:
        g.add(
            DashedLine(A2,H2,color=GOLD,stroke_width=2.6,dash_length=0.10),
            DashedLine(B2,K2,color=CYAN,stroke_width=2.6,dash_length=0.10),
            Dot(H2,radius=0.050,color=GOLD),
            Dot(K2,radius=0.050,color=CYAN),
        )

    if show_line:
        g.add(
            Line(A2,B2,color=GOLD,stroke_width=6.5),
            Dot(M2,radius=0.060,color=GREEN),
        )

    return g, {
        "S":S2,"C":C2,"A":A2,"B1":B2,
        "H":H2,"K":K2,"M":M2
    }


def folded_path():
    return VGroup(
        solid(W(RAW["A"]),W(M_RAW),GOLD,6.5),
        solid(W(M_RAW),W(RAW["B"]),GOLD,6.5),
        Dot3D(W(M_RAW),radius=0.065,color=GOLD),
    ), [RAW["A"],M_RAW,RAW["B"]]


def wrong_direct_edge():
    return solid(W(RAW["A"]),W(RAW["B"]),RED,6.5)


def layout_samples():
    return [
        lesson_card("BÀI TOÁN",[
            ("math","S C=10",28,CYAN),
            ("math","S H=2, A H=3",27,GOLD),
            ("math","S K=8, B K=5",27,CYAN),
            ("text","A → B, bắt buộc cắt phần trong của SC.",18,INK),
            ("math","L_(min)=?",34,GOLD),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","S M=frac(17,4)",29,CYAN),
            ("math","A M=frac(15,4)",29,INK),
            ("math","M B=frac(25,4)",29,INK),
            ("math","L_(min)=10",35,GOLD),
        ],CYAN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.93)

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
        h=header(9,title,progress); f=footer(); d=divider()
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


class TraiPhang09Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(pyramid_shell())
        labs=vertex_labels(["S","A","B","C"])
        for lab in labs:
            self.add_fixed_orientation_mobjects(lab)

        card=intro_card(
            9,
            ["CHÓP TAM GIÁC KHÔNG ĐỀU","CHỌN ĐÚNG DẢI MẶT"],
            "A → B, nhưng bắt buộc đi qua một điểm nằm trong cạnh đối SC.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Sau các mô hình đối xứng, ta chuyển sang một chóp tam giác không đều. "
            "Con kiến bắt đầu ở đỉnh A và kết thúc ở đỉnh B.",
            1.5,
        )
        self.narrate(
            "Điều kiện quan trọng là đường đi phải cắt phần bên trong của cạnh đối S C. "
            "Video này tập trung vào một kỹ năng mới: trước khi trải, phải chọn đúng hai mặt gắn với cạnh mà đường bắt buộc đi qua.",
            1.9,
        )

    def data_scene(self):
        self.clear_all()
        self.add_hud("Dữ kiện trên hai mặt quanh SC","01 / 12")
        self.add(pyramid_shell(),highlight_faces(CORRECT_FACES,0.12),feet_group())

        card=lesson_card("HAI ĐƯỜNG VUÔNG GÓC",[
            ("math","S C=10",29,CYAN),
            ("math","S H=2, A H=3",27,GOLD),
            ("math","S K=8, B K=5",27,CYAN),
            ("math","A H perp S C",25,INK),
            ("math","B K perp S C",25,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trên mặt A S C, hạ A H vuông góc với S C. Ta có S H bằng hai và A H bằng ba.",
            1.6,
        )
        self.narrate(
            "Trên mặt B S C, hạ B K vuông góc với S C. Ta có S K bằng tám và B K bằng năm. "
            "Cạnh S C dài mười.",
            1.7,
        )

    def direct_is_wrong(self):
        self.clear_all()
        self.add_hud("Đường ngắn nhất tự do không phải đáp án","02 / 12")
        self.add(pyramid_shell(),wrong_direct_edge())

        card=lesson_card("NẾU BỎ ĐIỀU KIỆN",[
            ("math","A B=sqrt(70)",30,RED),
            ("math","sqrt(70)<10",30,GREEN),
            ("text","Nhưng AB không cắt phần trong của SC.",18,INK),
            ("text","Nó giải một bài toán khác.",19,MUTED),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu bỏ điều kiện phải cắt S C, đường ngắn nhất chỉ là cạnh A B, có độ dài căn bảy mươi.",
            1.5,
        )
        self.narrate(
            "Nhưng cạnh A B không đi qua phần trong của S C. "
            "Vì vậy dù ngắn hơn, nó không phải là một đường hợp lệ của bài toán đang xét.",
            1.6,
        )

    def choose_strip(self):
        self.clear_all()
        self.add_hud("Muốn cắt SC thì phải chọn hai mặt nào?","03 / 12")
        self.add(pyramid_shell(),highlight_faces(CORRECT_FACES,0.18))
        self.add(solid(W(RAW["S"]),W(RAW["C"]),GOLD,7.0))

        card=lesson_card("DẢI MẶT ĐÚNG",[
            ("text","Trước khi chạm SC: đường nằm trên mặt ASC.",18,PURPLE),
            ("text","Sau khi qua SC: đường nằm trên mặt BSC.",18,CYAN),
            ("text","Hai mặt có cạnh chung chính là SC.",18,GOLD),
            ("text","Đây mới là dải cần trải.",19,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Muốn đường đi cắt phần trong của S C, đoạn ngay trước điểm cắt phải nằm trên mặt A S C, "
            "còn đoạn ngay sau điểm cắt phải nằm trên mặt B S C.",
            1.9,
        )
        self.narrate(
            "Vì thế dải mặt đúng đã được xác định ngay từ điều kiện của đề: ta phải trải hai mặt A S C và B S C quanh cạnh chung S C.",
            1.7,
        )

    def wrong_strip(self):
        self.clear_all()
        self.add_hud("Một dải nhìn hợp lý nhưng sai yêu cầu","04 / 12")
        self.add(pyramid_shell(),highlight_faces(WRONG_FACES,0.15))
        self.add(wrong_direct_edge())

        card=lesson_card("DẢI SAB + ABC",[
            ("text","Hai mặt này cùng chứa cạnh AB.",18,INK),
            ("text","Nối A với B cho một đường rất ngắn.",18,RED),
            ("text","Nhưng đường không hề cắt SC.",18,INK),
            ("text","Bản trải đúng hình vẫn có thể sai bài.",19,GOLD),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu ta chọn hai mặt S A B và A B C, ta vẫn có thể mở chúng rất đẹp. "
            "Nhưng cả hai cùng chứa cạnh A B nên đường nối A với B không buộc phải đi qua S C.",
            1.8,
        )
        self.narrate(
            "Đây là điều cần nhớ: một bản trải có thể hoàn toàn đúng về hình học nhưng lại không đúng với điều kiện đường đi của bài toán.",
            1.7,
        )

    def arbitrary_x(self):
        self.clear_all()
        self.add_hud("Gọi X là điểm cắt cạnh SC","05 / 12")
        self.add(pyramid_shell(),highlight_faces(CORRECT_FACES,0.17))

        X = RAW["S"] + 0.58*(RAW["C"]-RAW["S"])
        path=VGroup(
            solid(W(RAW["A"]),W(X),ORANGE,6.0),
            solid(W(X),W(RAW["B"]),ORANGE,6.0),
            Dot3D(W(X),radius=0.065,color=ORANGE),
        )
        self.add(path)

        card=lesson_card("VỚI X THUỘC PHẦN TRONG SC",[
            ("math","L(X)=A X+X B",31,ORANGE),
            ("text","AX nằm trên mặt ASC.",19,INK),
            ("text","XB nằm trên mặt BSC.",19,INK),
            ("text","Cần chọn X sao cho tổng nhỏ nhất.",18,CYAN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Gọi X là điểm mà kiến cắt cạnh S C. "
            "Đường đi gồm A X trên mặt A S C và X B trên mặt B S C.",
            1.6,
        )
        self.narrate(
            "Ta cần tìm vị trí X nằm bên trong S C sao cho tổng A X cộng X B nhỏ nhất.",
            1.5,
        )

    def unfold(self):
        self.clear_all()
        self.add_hud("Mở mặt BSC quanh cạnh SC","06 / 12")

        theta=ValueTracker(0.0)
        fixed,_=unfolding_group(0.0)
        moving=always_redraw(lambda: unfolding_group(theta.get_value())[1])

        self.add(fixed,moving)

        card=lesson_card("MỞ HAI MẶT",[
            ("text","Giữ mặt ASC.",19,INK),
            ("text","S và C đứng yên trên cạnh chung.",18,GOLD),
            ("text","Mở mặt BSC quanh SC.",19,CYAN),
            ("text","Ảnh của B sau khi mở là B₁.",18,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Ta giữ mặt A S C và mở mặt B S C quanh cạnh S C. "
            "Hai điểm S và C đứng yên, còn B đi theo mặt B S C.",
            theta.animate.set_value(UNFOLD_ANGLE),
            min_time=3.2,
            rate_func=smooth,
        )
        self.narrate(
            "Sau khi mở, hai tam giác nằm chung trên một mặt phẳng. "
            "Ta gọi ảnh của B là B một.",
            1.4,
        )

    def net_coordinates(self):
        self.clear_all()
        self.add_hud("Đặt hệ trục ngay trên bản trải","07 / 12")
        net,pts=net_2d(show_line=False,show_feet=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("CHỌN SC LÀM TRỤC NGANG",[
            ("math","S=(0,0), C=(10,0)",25,INK),
            ("math","A=(2,3)",29,GOLD),
            ("math","B_1=(8,-5)",29,CYAN),
            ("text","Hai điểm nằm ở hai phía của SC.",18,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trên bản trải, chọn S C làm trục ngang. Đặt S tại không, không và C tại mười, không.",
            1.6,
        )
        self.narrate(
            "Vì S H bằng hai và A H bằng ba nên A có tọa độ hai, ba. "
            "Sau khi mở sang phía đối diện, B một có tọa độ tám, âm năm.",
            1.9,
        )

    def straight_line(self):
        self.clear_all()
        self.add_hud("Nối A với B₁ bằng đoạn thẳng","08 / 12")
        net,pts=net_2d(show_line=True,show_feet=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("PHƯƠNG TRÌNH ĐƯỜNG THẲNG",[
            ("math","A=(2,3), B_1=(8,-5)",25,INK),
            ("math","y-3=-frac(4,3) times (x-2)",25,GOLD),
            ("math","y=0",27,CYAN),
            ("math","x_M=frac(17,4)",31,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Đường ngắn nhất trên mặt phẳng là đoạn thẳng A B một. "
            "Đường này có hệ số góc âm bốn phần ba.",
            1.5,
        )
        self.narrate(
            "Điểm M nơi A B một cắt S C có tung độ bằng không. "
            "Thế vào phương trình đường thẳng, ta được hoành độ của M bằng mười bảy phần bốn.",
            1.9,
        )
        self.narrate(
            "Vì S được đặt tại hoành độ không, suy ra S M bằng mười bảy phần bốn. "
            "M nằm thực sự bên trong đoạn S C.",
            1.6,
        )

    def compute_length(self):
        self.clear_all()
        self.add_hud("Tính hai đoạn sau khi gấp lại","09 / 12")
        net,pts=net_2d(show_line=True,show_feet=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("ĐỘ DÀI",[
            ("math","A M=sqrt((frac(9,4))^2+3^2)",24,PURPLE),
            ("math","A M=frac(15,4)",29,PURPLE),
            ("math","M B_1=frac(25,4)",29,CYAN),
            ("math","L_(min)=10",36,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Từ A đến M, độ lệch ngang là chín phần bốn và độ lệch đứng là ba. "
            "Theo Pythagore, A M bằng mười lăm phần bốn.",
            1.7,
        )
        self.narrate(
            "Tương tự, M B một bằng hai mươi lăm phần bốn. "
            "Cộng lại, đường đi ngắn nhất có độ dài đúng bằng mười.",
            1.7,
        )

    def proof_minimum(self):
        self.clear_all()
        self.add_hud("Vì sao không có điểm X nào tốt hơn?","10 / 12")
        net,pts=net_2d(show_line=True,show_feet=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("BẤT ĐẲNG THỨC TAM GIÁC",[
            ("math","A X+X B_1>=A B_1",28,INK),
            ("text","Dấu bằng khi A, X, B₁ thẳng hàng.",18,CYAN),
            ("math","X=M",31,GREEN),
            ("math","L_(min)=A B_1=10",32,GOLD),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Với một điểm X bất kỳ trên S C, sau khi trải ta có một đường gấp A X B một.",
            1.5,
        )
        self.narrate(
            "Theo bất đẳng thức tam giác, A X cộng X B một luôn lớn hơn hoặc bằng A B một. "
            "Dấu bằng chỉ xảy ra khi A, X và B một thẳng hàng.",
            1.8,
        )
        self.narrate(
            "Vì vậy M vừa tìm không chỉ cho một đường đẹp, mà là điểm duy nhất cho độ dài nhỏ nhất.",
            1.5,
        )

    def fold_back(self):
        self.clear_all()
        self.add_hud("Gấp lại và cho kiến đi thật","11 / 12")
        path,pts3=folded_path()
        self.add(pyramid_shell(),highlight_faces(CORRECT_FACES,0.17),path)

        ant=Dot3D(W(pts3[0]),radius=0.085,color=GREEN)
        self.add(ant)

        card=lesson_card("ĐƯỜNG TRÊN CHÓP TAM GIÁC",[
            ("text","Đường đi: A → M → B.",19,GOLD),
            ("math","S M=frac(17,4)",28,CYAN),
            ("math","A M=frac(15,4)",27,INK),
            ("math","M B=frac(25,4)",27,INK),
            ("math","L_(min)=10",34,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Kiến đi từ A tới M trên mặt A S C. Điểm M nằm trên S C và cách S mười bảy phần bốn.",
            MoveAlongPath(ant,Line(W(pts3[0]),W(pts3[1]))),
            min_time=2.2,
            rate_func=linear,
        )
        self.narrate_play(
            "Tại M, kiến chuyển sang mặt B S C rồi đi thẳng tới B.",
            MoveAlongPath(ant,Line(W(pts3[1]),W(pts3[2]))),
            min_time=2.0,
            rate_func=linear,
        )

    def general_rule(self):
        self.clear_all()
        self.add_hud("Công thức chung cho hai mặt quanh một cạnh","12 / 12")
        net,pts=net_2d(show_line=True,show_feet=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("TRÊN BẢN TRẢI",[
            ("math","A=(p,h_1)",26,PURPLE),
            ("math","B_1=(q,-h_2)",26,CYAN),
            ("math","L=sqrt((q-p)^2+(h_1+h_2)^2)",23,GOLD),
            ("math","x_M=frac(h_2 p+h_1 q,h_1+h_2)",22,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bài này còn cho một công thức rất hữu ích. "
            "Sau khi trải hai mặt quanh một cạnh, giả sử hai điểm có tọa độ p, h một và q, âm h hai.",
            1.8,
        )
        self.narrate(
            "Độ dài ngắn nhất là căn của q trừ p tất cả bình phương cộng h một cộng h hai tất cả bình phương.",
            1.7,
        )
        self.narrate(
            "Hoành độ điểm đổi mặt là h hai nhân p cộng h một nhân q, rồi chia cho h một cộng h hai. "
            "Trong bài này công thức cho đúng S M bằng mười bảy phần bốn.",
            1.9,
        )
        self.narrate(
            "Điều quan trọng nhất vẫn là bước đầu tiên: phải chọn đúng hai mặt kề với cạnh mà đường bắt buộc đi qua. "
            "Chọn sai dải mặt thì dù tính toán đúng, ta vẫn đang giải sai bài toán.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.data_scene()
        self.direct_is_wrong()
        self.choose_strip()
        self.wrong_strip()
        self.arbitrary_x()
        self.unfold()
        self.net_coordinates()
        self.straight_line()
        self.compute_length()
        self.proof_minimum()
        self.fold_back()
        self.general_rule()


class Smoke09(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.93)

        theta=ValueTracker(0.0)
        fixed,_=unfolding_group(0.0)
        moving=always_redraw(lambda: unfolding_group(theta.get_value())[1])
        self.add(fixed,moving)
        self.play(
            theta.animate.set_value(UNFOLD_ANGLE),
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_09_master_smoke"
    config.disable_caching=True

    scene=Smoke09()
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
    config.output_file="trai_phang_09_chop_tam_giac_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang09Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_09.wav"
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

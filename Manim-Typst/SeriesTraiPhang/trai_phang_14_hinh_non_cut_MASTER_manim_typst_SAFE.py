
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








# ---------- geometry engine: conical frustum / annular sector ----------
# Right circular frustum cut from a 3-4-5 cone.
#
# Bottom radius R = 6
# Top radius r = 3
# Vertical height H = 4
# Frustum slant height g = 5
#
# If extended to the apex:
#   outer slant radius L2 = 10
#   inner slant radius L1 = 5
#   development sector angle Phi = 2*pi*R/L2 = 6*pi/5
#
# A and B lie on the OUTER rim (bottom circle).
# Physical points are only 60 degrees apart by the short way.
# In this lesson we first prescribe the LONG winding class:
#   delta_long = 5*pi/3 = 300 degrees.
# On the annular-sector development this becomes:
#   alpha_long = (R/L2)*delta_long = pi.
#
# The straight chord between A and B passes through the inner hole
# (inner radius 5), so it is NOT a valid lateral-surface path.
#
# Shortest valid path in this class:
# tangent A->P + inner arc P->Q + tangent Q->B.
# Since outer/inner developed radii are 10 and 5:
#   beta = arccos(5/10) = pi/3
#   AP = QB = sqrt(10^2-5^2) = 5*sqrt(3)
#   inner arc angle = pi - 2*pi/3 = pi/3
#   arc PQ = 5*pi/3
#   L_long = 10*sqrt(3) + 5*pi/3.
#
# Without the long-way constraint:
#   delta_sh = pi/3 = 60 degrees
#   alpha_sh = pi/5 = 36 degrees
#   L_sh = 20*sin(pi/10), and this chord stays outside the hole.
# ==========================================================

R_BOTTOM = 6.0
R_TOP = 3.0
H_FRUSTUM = 4.0
SLANT_FRUSTUM = 5.0

OUTER_RHO = 10.0
INNER_RHO = 5.0
RATIO = R_BOTTOM / OUTER_RHO  # 3/5
SECTOR_ANGLE = 2.0 * math.pi * RATIO  # 6*pi/5

DELTA_LONG = 5.0 * math.pi / 3.0
DELTA_SHORT = math.pi / 3.0
ALPHA_LONG = RATIO * DELTA_LONG  # pi
ALPHA_SHORT = RATIO * DELTA_SHORT  # pi/5

PSI_A = math.pi / 10.0
PSI_B = PSI_A + ALPHA_LONG  # 11*pi/10

BETA = math.acos(INNER_RHO / OUTER_RHO)  # pi/3
PSI_P = PSI_A + BETA
PSI_Q = PSI_B - BETA
INNER_ARC_ANGLE = PSI_Q - PSI_P  # pi/3

WORLD_SCALE = 0.56
WORLD_SHIFT = np.array([-3.25, 1.35, 3.20])

CAM_PHI = 67 * DEGREES
CAM_THETA = -47 * DEGREES

SECTOR_VIS_ROT = -SECTOR_ANGLE / 2.0
SECTOR_VIS_SCALE = 0.29
SECTOR_CENTER = np.array([LEFT_CENTER[0]-0.95, LEFT_CENTER[1]-0.15, 0.0])


def W(p):
    return WORLD_SCALE * np.array(p, dtype=float) + WORLD_SHIFT


def iso_point(rho, psi, s):
    """Exact isometric family from frustum to annular sector.

    Same cone-development family as Video 13, but restricted to:
        INNER_RHO <= rho <= OUTER_RHO.
    """
    s = float(s)
    s = max(RATIO, min(1.0, s))
    c = math.sqrt(max(0.0, 1.0 - s*s))
    ang = psi / s
    return np.array([
        rho*s*math.cos(ang),
        rho*s*math.sin(ang),
        -rho*c,
    ], dtype=float)


def closed_frustum_point(rho, psi):
    return iso_point(rho, psi, RATIO)


def flat_xy(rho, psi):
    return np.array([
        rho*math.cos(psi),
        rho*math.sin(psi),
    ], dtype=float)


A_FLAT = flat_xy(OUTER_RHO, PSI_A)
B_FLAT = flat_xy(OUTER_RHO, PSI_B)
P_FLAT = flat_xy(INNER_RHO, PSI_P)
Q_FLAT = flat_xy(INNER_RHO, PSI_Q)


def endpoint_raw(which):
    psi = PSI_A if which == "A" else PSI_B
    return closed_frustum_point(OUTER_RHO, psi)


def tangent_path_flat_points(n_arc=48):
    pts = [A_FLAT]
    pts.append(P_FLAT)
    for j in range(1, n_arc):
        u = j / n_arc
        psi = PSI_P + u * (PSI_Q - PSI_P)
        pts.append(flat_xy(INNER_RHO, psi))
    pts.append(Q_FLAT)
    pts.append(B_FLAT)
    return pts


def rho_psi_from_flat_xy(xy):
    x, y = float(xy[0]), float(xy[1])
    rho = math.hypot(x, y)
    psi = math.atan2(y, x)
    if psi < 0:
        psi += 2*math.pi
    return rho, psi


def mapped_shest_raw(t, s=RATIO):
    """Piecewise shortest valid path in the prescribed long class."""
    len_tan = math.sqrt(OUTER_RHO**2 - INNER_RHO**2)
    len_arc = INNER_RHO * INNER_ARC_ANGLE
    total = 2*len_tan + len_arc

    d = t * total

    if d <= len_tan:
        u = d / len_tan
        xy = (1-u)*A_FLAT + u*P_FLAT
    elif d <= len_tan + len_arc:
        u = (d-len_tan)/len_arc
        psi = PSI_P + u*(PSI_Q-PSI_P)
        xy = flat_xy(INNER_RHO, psi)
    else:
        u = (d-len_tan-len_arc)/len_tan
        xy = (1-u)*Q_FLAT + u*B_FLAT

    rho, psi = rho_psi_from_flat_xy(xy)
    return iso_point(rho, psi, s)


def shortest_long_curve(color=GOLD, width=6.0):
    return ParametricFunction(
        lambda t: W(mapped_shest_raw(t, RATIO)),
        t_range=[0,1],
        color=color,
        stroke_width=width,
    )


def invalid_long_chord_3d():
    A = W(endpoint_raw("A"))
    B = W(endpoint_raw("B"))
    return DashedLine(
        A, B,
        color=RED,
        stroke_width=4.8,
        dash_length=0.12,
    )


def frustum_surface():
    return Surface(
        lambda u, v: W(iso_point(
            INNER_RHO + (OUTER_RHO-INNER_RHO)*v,
            SECTOR_ANGLE*u,
            RATIO,
        )),
        u_range=[0,1],
        v_range=[0,1],
        resolution=(30,9),
        fill_color=BLUE,
        fill_opacity=0.060,
        stroke_width=0.0,
    )


def frustum_wireframe():
    g = VGroup(frustum_surface())

    # Top and bottom rims.
    for rho, color in [(INNER_RHO, CYAN), (OUTER_RHO, EDGE)]:
        g.add(ParametricFunction(
            lambda psi, rho=rho: W(closed_frustum_point(rho, psi)),
            t_range=[0, SECTOR_ANGLE],
            color=color,
            stroke_width=3.5,
        ))

    # Generators.
    for j in range(13):
        psi = SECTOR_ANGLE*j/12
        g.add(Line(
            W(closed_frustum_point(INNER_RHO, psi)),
            W(closed_frustum_point(OUTER_RHO, psi)),
            color=GOLD if j == 0 else GRID,
            stroke_width=4.5 if j == 0 else 1.8,
            stroke_opacity=1.0 if j == 0 else 0.64,
        ))

    # Intermediate slant levels.
    for rho in [6.25, 7.5, 8.75]:
        g.add(ParametricFunction(
            lambda psi, rho=rho: W(closed_frustum_point(rho, psi)),
            t_range=[0, SECTOR_ANGLE],
            color=GRID,
            stroke_width=1.45,
            stroke_opacity=0.50,
        ))

    return g


def frustum_endpoints():
    A = W(endpoint_raw("A"))
    B = W(endpoint_raw("B"))
    return A, B


def unfold_wire_group(s):
    g = VGroup()

    for rho, color, width in [
        (INNER_RHO, CYAN, 3.3),
        (6.25, GRID, 1.4),
        (7.5, GRID, 1.4),
        (8.75, GRID, 1.4),
        (OUTER_RHO, EDGE, 3.4),
    ]:
        pts = [
            W(iso_point(rho, SECTOR_ANGLE*k/120, s))
            for k in range(121)
        ]
        curve = VMobject(
            color=color,
            stroke_width=width,
            stroke_opacity=0.78 if rho in {INNER_RHO, OUTER_RHO} else 0.52,
        )
        curve.set_points_as_corners(pts)
        g.add(curve)

    for j in range(13):
        psi = SECTOR_ANGLE*j/12
        g.add(Line(
            W(iso_point(INNER_RHO, psi, s)),
            W(iso_point(OUTER_RHO, psi, s)),
            color=GOLD if j in {0,12} else GRID,
            stroke_width=4.3 if j in {0,12} else 1.65,
            stroke_opacity=0.82,
        ))

    return g


def unfold_path_group(s):
    pts = [
        W(mapped_shest_raw(k/120, s))
        for k in range(121)
    ]
    path = VMobject(color=GOLD, stroke_width=6.1)
    path.set_points_as_corners(pts)

    A = W(iso_point(OUTER_RHO, PSI_A, s))
    B = W(iso_point(OUTER_RHO, PSI_B, s))

    return VGroup(
        path,
        Dot3D(A, radius=0.070, color=GREEN),
        Dot3D(B, radius=0.070, color=RED),
    )


def sector_visual_point(rho, psi):
    ang = psi + SECTOR_VIS_ROT
    return SECTOR_CENTER + SECTOR_VIS_SCALE*np.array([
        rho*math.cos(ang),
        rho*math.sin(ang),
        0.0,
    ])


def annular_sector(show_invalid=False, show_valid=False, show_tangent_points=False):
    outer_pts = [
        sector_visual_point(OUTER_RHO, SECTOR_ANGLE*k/160)
        for k in range(161)
    ]
    inner_pts = [
        sector_visual_point(INNER_RHO, SECTOR_ANGLE*k/160)
        for k in range(161)
    ]

    S = SECTOR_CENTER
    A = sector_visual_point(OUTER_RHO, PSI_A)
    B = sector_visual_point(OUTER_RHO, PSI_B)
    P = sector_visual_point(INNER_RHO, PSI_P)
    Q = sector_visual_point(INNER_RHO, PSI_Q)

    # Fill annular sector by polygons between sampled arcs.
    fill = VGroup()
    for k in range(160):
        fill.add(Polygon(
            inner_pts[k], outer_pts[k], outer_pts[k+1], inner_pts[k+1],
            fill_color=BLUE,
            fill_opacity=0.095,
            stroke_width=0.0,
        ))

    outer_arc = VMobject(color=EDGE, stroke_width=3.3)
    outer_arc.set_points_as_corners(outer_pts)

    inner_arc = VMobject(color=CYAN, stroke_width=3.3)
    inner_arc.set_points_as_corners(inner_pts)

    side1 = Line(inner_pts[0], outer_pts[0], color=GOLD, stroke_width=4.0)
    side2 = Line(inner_pts[-1], outer_pts[-1], color=GOLD, stroke_width=4.0)

    g = VGroup(
        fill, outer_arc, inner_arc, side1, side2,
        Dot(A, radius=0.070, color=GREEN),
        Dot(B, radius=0.070, color=RED),
    )

    if show_invalid:
        g.add(Line(A, B, color=RED, stroke_width=5.4))

    if show_valid:
        tan1 = Line(A, P, color=GOLD, stroke_width=5.8)
        tan2 = Line(Q, B, color=GOLD, stroke_width=5.8)

        arc_pts = [
            sector_visual_point(
                INNER_RHO,
                PSI_P + (PSI_Q-PSI_P)*k/80
            )
            for k in range(81)
        ]
        arc = VMobject(color=GOLD, stroke_width=6.0)
        arc.set_points_as_corners(arc_pts)
        g.add(tan1, arc, tan2)

    if show_tangent_points:
        g.add(
            Dot(P, radius=0.058, color=GOLD),
            Dot(Q, radius=0.058, color=GOLD),
        )

    return g, {
        "A": A, "B": B, "P": P, "Q": Q, "S": S,
    }


def short_class_sector():
    """Separate, simple diagram for the unrestricted short class."""
    center = SECTOR_CENTER
    scale = SECTOR_VIS_SCALE

    # Use A at psi=0.40 and B at +alpha_sh.
    pa = 0.55
    pb = pa + ALPHA_SHORT

    def T(rho, psi):
        ang = psi - 0.85
        return center + scale*np.array([
            rho*math.cos(ang),
            rho*math.sin(ang),
            0.0,
        ])

    A = T(OUTER_RHO, pa)
    B = T(OUTER_RHO, pb)

    # Inner circle reference only.
    inner = Circle(
        radius=scale*INNER_RHO,
        color=CYAN,
        stroke_width=2.8,
    ).move_to(center)

    outer = Circle(
        radius=scale*OUTER_RHO,
        color=EDGE,
        stroke_width=2.8,
    ).move_to(center)

    return VGroup(
        outer, inner,
        Dot(A, radius=0.070, color=GREEN),
        Dot(B, radius=0.070, color=RED),
        Line(A, B, color=GOLD, stroke_width=6.0),
    )


def geometry_preflight(verbose=True):
    tol = 1e-9

    if abs(math.hypot(R_BOTTOM-R_TOP, H_FRUSTUM)-SLANT_FRUSTUM) > tol:
        raise AssertionError("Frustum slant should be 5")

    if abs(RATIO-3.0/5.0) > tol:
        raise AssertionError("Development ratio should be 3/5")

    if abs(SECTOR_ANGLE-6.0*math.pi/5.0) > tol:
        raise AssertionError("Sector angle should be 6pi/5")

    if abs(ALPHA_LONG-math.pi) > tol:
        raise AssertionError("Long developed angle should be pi")

    if abs(ALPHA_SHORT-math.pi/5.0) > tol:
        raise AssertionError("Short developed angle should be pi/5")

    if abs(BETA-math.pi/3.0) > tol:
        raise AssertionError("Tangent beta should be pi/3")

    if abs(INNER_ARC_ANGLE-math.pi/3.0) > tol:
        raise AssertionError("Inner arc angle should be pi/3")

    # Straight long-class chord crosses the hole.
    # With alpha=pi, chord is a diameter through the origin.
    line_mid = 0.5*(A_FLAT+B_FLAT)
    if np.linalg.norm(line_mid) > 1e-8:
        raise AssertionError("Long-class chord should pass through center")
    if np.linalg.norm(line_mid) >= INNER_RHO:
        raise AssertionError("Chord must enter the inner hole")

    # Tangency.
    AP = np.linalg.norm(A_FLAT-P_FLAT)
    QB = np.linalg.norm(Q_FLAT-B_FLAT)
    expected_tan = 5.0*math.sqrt(3.0)

    if abs(AP-expected_tan) > 1e-8 or abs(QB-expected_tan) > 1e-8:
        raise AssertionError("Wrong tangent length")

    if abs(np.dot(P_FLAT, A_FLAT-P_FLAT)) > 1e-8:
        raise AssertionError("AP not tangent to inner circle")
    if abs(np.dot(Q_FLAT, B_FLAT-Q_FLAT)) > 1e-8:
        raise AssertionError("QB not tangent to inner circle")

    arc_len = INNER_RHO*INNER_ARC_ANGLE
    expected_long = 10.0*math.sqrt(3.0) + 5.0*math.pi/3.0
    if abs(AP + arc_len + QB - expected_long) > 1e-8:
        raise AssertionError("Long-class shortest length mismatch")

    # Short class chord validity.
    short_len = 2*OUTER_RHO*math.sin(ALPHA_SHORT/2.0)
    short_min_radius = OUTER_RHO*math.cos(ALPHA_SHORT/2.0)
    if not (short_min_radius > INNER_RHO):
        raise AssertionError("Short-class chord should stay outside the hole")

    expected_sh = 20.0*math.sin(math.pi/10.0)
    if abs(short_len-expected_sh) > tol:
        raise AssertionError("Short-class chord length mismatch")

    if not (expected_sh < expected_long):
        raise AssertionError("Unrestricted short class should be shorter")

    # Metric verification of isometric unrolling family.
    for s in [RATIO,0.72,0.86,1.0]:
        c = math.sqrt(max(0.0,1.0-s*s))
        for rho in [INNER_RHO,7.5,OUTER_RHO]:
            for psi in [0.2,1.4,3.0]:
                ang = psi/s
                E_rho = np.array([
                    s*math.cos(ang),
                    s*math.sin(ang),
                    -c,
                ])
                E_psi = np.array([
                    -rho*math.sin(ang),
                    rho*math.cos(ang),
                    0.0,
                ])
                if abs(np.linalg.norm(E_rho)-1.0)>1e-8:
                    raise AssertionError("rho metric failed")
                if abs(np.linalg.norm(E_psi)-rho)>1e-8:
                    raise AssertionError("psi metric failed")
                if abs(np.dot(E_rho,E_psi))>1e-8:
                    raise AssertionError("metric orthogonality failed")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  frustum R=6, r=3, H=4, slant=5")
        print("  annular sector radii 10 and 5, angle 6pi/5")
        print("  prescribed long class: physical 300 deg -> developed pi")
        print("  straight developed chord crosses the inner hole")
        print("  valid optimum: tangent + inner arc + tangent")
        print("  AP=QB=5sqrt(3), arc=5pi/3")
        print("  L_long=10sqrt(3)+5pi/3")
        print("  unrestricted short class: alpha=pi/5, L=20 sin(pi/10)")
    return True


def layout_samples():
    return [
        lesson_card("BÀI TOÁN",[
            ("math","R=6, r=3, H=4",27,CYAN),
            ("text","A, B nằm trên vành đáy lớn.",18,INK),
            ("text","Xét lớp đường đi theo chiều dài 300°.",17,GOLD),
            ("math","alpha=pi",29,CYAN),
            ("math","L_(min)=?",34,GOLD),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","A P=Q B=5 sqrt(3)",27,CYAN),
            ("math","s_(P Q)=frac(5 pi,3)",27,CYAN),
            ("math","L=10 sqrt(3)+frac(5 pi,3)",29,GOLD),
        ],CYAN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.95)

    def narrate(self,text,min_visual_time=1.0):
        audio=create_audio(text)
        dur=probe_duration(audio)
        self.audio_events.append((self.time,audio))
        self.wait(max(dur,min_visual_time))
        return dur

    def narrate_play(self,text,*anims,min_time=1.0,rate_func=smooth):
        audio=create_audio(text)
        dur=probe_duration(audio)
        self.audio_events.append((self.time,audio))
        self.play(*anims,run_time=max(dur,min_time),rate_func=rate_func)
        return dur

    def add_hud(self,title,progress):
        h=header(14,title,progress)
        f=footer()
        d=divider()
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

    forbidden=[
        "workflow","render","preflight","engine","code","mã nguồn",
        "camera","animation","cột trái","cột phải","debug"
    ]

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


class TraiPhang14Master(BaseLesson):
    def intro(self):
        self.clear_all()
        A,B=frustum_endpoints()

        self.add(
            frustum_wireframe(),
            shortest_long_curve(),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=intro_card(
            14,
            ["HÌNH NÓN CỤT","VÀNH QUẠT CÓ MỘT LỖ Ở GIỮA"],
            "Đoạn thẳng trên bản trải chưa chắc là một đường hợp lệ.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Với hình nón, bản khai triển là một hình quạt kín từ đỉnh tới cung ngoài. "
            "Sang hình nón cụt, phần gần đỉnh đã bị cắt đi.",
            1.8,
        )
        self.narrate(
            "Vì thế bản khai triển trở thành một vành quạt có lỗ ở giữa. "
            "Đây là lúc ta phải kiểm tra xem đoạn thẳng nối hai điểm có thật sự nằm trong miền khai triển hay không.",
            1.9,
        )

    def model(self):
        self.clear_all()
        self.add_hud("Mô hình nón cụt 3 - 4 - 5","01 / 13")

        A,B=frustum_endpoints()
        self.add(
            frustum_wireframe(),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("KÍCH THƯỚC",[
            ("math","R=6",28,CYAN),
            ("math","r=3",28,CYAN),
            ("math","H=4",28,GOLD),
            ("math","g=5",29,GREEN),
            ("text","A, B nằm trên vành đáy lớn.",18,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Đáy lớn có bán kính sáu, đáy nhỏ có bán kính ba, chiều cao bằng bốn.",
            1.5,
        )
        self.narrate(
            "Độ chênh hai bán kính bằng ba, nên đường sinh của nón cụt bằng căn của ba bình phương cộng bốn bình phương, tức bằng năm.",
            1.8,
        )

    def extend_cone(self):
        self.clear_all()
        self.add_hud("Kéo dài các đường sinh tới đỉnh tưởng tượng","02 / 13")

        ann,pts=annular_sector(show_invalid=False,show_valid=False)
        self.add_fixed_in_frame_mobjects(ann)

        card=lesson_card("NẾU KÉO DÀI THÀNH NÓN ĐẦY",[
            ("math","rho_2=10",28,CYAN),
            ("math","rho_1=5",28,CYAN),
            ("text","Phần nón cụt nằm giữa hai bán kính này.",18,INK),
            ("math","Phi=frac(6 pi,5)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Kéo dài các đường sinh của nón cụt tới một đỉnh tưởng tượng. "
            "Do hai bán kính đáy là sáu và ba, hai khoảng cách theo đường sinh tới đỉnh tưởng tượng có tỉ lệ hai trên một.",
            1.9,
        )
        self.narrate(
            "Hiệu hai khoảng cách ấy chính là đường sinh nón cụt bằng năm. "
            "Vì vậy bán kính ngoài của vành quạt là mười, bán kính trong là năm.",
            1.8,
        )
        self.narrate(
            "Góc của toàn vành quạt vẫn bằng sáu pi trên năm, giống nón ba bốn năm ở video trước.",
            1.6,
        )

    def long_class(self):
        self.clear_all()
        self.add_hud("Chọn lớp đường đi theo chiều dài quanh trục","03 / 13")

        self.add(frustum_wireframe())

        card=lesson_card("HAI ĐIỂM A, B",[
            ("text","Theo chiều ngắn: cách nhau 60°.",18,CYAN),
            ("text","Ta xét chiều còn lại: 300°.",18,GOLD),
            ("math","delta_L=frac(5 pi,3)",27,GOLD),
            ("math","alpha_L=frac(3,5) delta_L=pi",25,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hai điểm A và B trên vành đáy lớn thực ra chỉ cách nhau sáu mươi độ theo chiều ngắn.",
            1.5,
        )
        self.narrate(
            "Nhưng trong phần chính của bài, ta xét lớp đường đi theo chiều còn lại quanh trục, tức ba trăm độ.",
            1.7,
        )
        self.narrate(
            "Khi khai triển, góc này được nhân với ba phần năm. "
            "Ba trăm độ trên nón cụt trở thành đúng một trăm tám mươi độ trên vành quạt.",
            1.9,
        )

    def exact_unroll(self):
        self.clear_all()
        self.add_hud("Mở nón cụt thành một vành quạt","04 / 13")

        s=ValueTracker(RATIO)
        mesh=always_redraw(lambda: unfold_wire_group(s.get_value()))
        path=always_redraw(lambda: unfold_path_group(s.get_value()))
        self.add(mesh,path)

        card=lesson_card("KHAI TRIỂN",[
            ("text","Các đường sinh giữ nguyên độ dài.",18,INK),
            ("text","Đáy lớn mở thành cung bán kính 10.",18,CYAN),
            ("text","Đáy nhỏ mở thành cung bán kính 5.",18,CYAN),
            ("text","Miền phẳng có một lỗ ở giữa.",18,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Ta mở mặt xung quanh của nón cụt từ từ. "
            "Đường sinh vẫn giữ nguyên, còn hai đường tròn đáy mở thành hai cung đồng tâm.",
            s.animate.set_value(1.0),
            min_time=5.2,
            rate_func=smooth,
        )
        self.narrate(
            "Khi mở hoàn toàn, ta được một vành quạt: phần giữa bán kính năm và bán kính mười.",
            1.6,
        )

    def invalid_chord(self):
        self.clear_all()
        self.add_hud("Nối thẳng A với B: nhìn ngắn nhưng sai","05 / 13")

        ann,pts=annular_sector(show_invalid=True,show_valid=False)
        self.add_fixed_in_frame_mobjects(ann)

        card=lesson_card("ĐOẠN THẲNG AB",[
            ("math","hat(A S B)=pi",28,RED),
            ("math","A B=20",31,RED),
            ("text","Nhưng đoạn AB đi xuyên qua lỗ bán kính 5.",18,INK),
            ("text","Nó không nằm trọn trong vành quạt.",18,GOLD),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trên bản trải, A và B nằm đối nhau qua tâm của hai đường tròn. "
            "Nếu chỉ nhìn hai đầu mút, đoạn thẳng A B có độ dài hai mươi.",
            1.8,
        )
        self.narrate(
            "Nhưng đoạn thẳng này đi xuyên qua phần lỗ bán kính năm. "
            "Phần lỗ không thuộc mặt nón cụt, nên A B không phải đường hợp lệ.",
            1.8,
        )

    def tangent_idea(self):
        self.clear_all()
        self.add_hud("Đường ngắn nhất phải ôm lấy lỗ","06 / 13")

        ann,pts=annular_sector(
            show_invalid=False,
            show_valid=True,
            show_tangent_points=True
        )
        self.add_fixed_in_frame_mobjects(ann)

        card=lesson_card("CẤU TRÚC ĐƯỜNG TỐI ƯU",[
            ("text","Từ A đi tiếp tuyến tới đường tròn trong.",17,GOLD),
            ("text","Đi theo một cung của đường tròn trong.",17,CYAN),
            ("text","Rồi đi tiếp tuyến tới B.",17,GOLD),
            ("text","Hai điểm tiếp xúc là P và Q.",18,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Khi đoạn thẳng bị chặn bởi một lỗ tròn, đường ngắn nhất không thể gấp khúc tùy ý.",
            1.5,
        )
        self.narrate(
            "Nó phải đi thẳng từ A tới điểm tiếp xúc P, men theo đường tròn trong từ P tới Q, rồi đi thẳng từ Q tới B.",
            1.9,
        )
        self.narrate(
            "Hai đoạn thẳng A P và Q B là các tiếp tuyến của đường tròn bán kính năm.",
            1.6,
        )

    def tangent_length(self):
        self.clear_all()
        self.add_hud("Tính hai đoạn tiếp tuyến","07 / 13")

        ann,pts=annular_sector(
            show_valid=True,
            show_tangent_points=True
        )
        self.add_fixed_in_frame_mobjects(ann)

        card=lesson_card("TRONG TAM GIÁC VUÔNG SAP",[
            ("math","S A=10",28,INK),
            ("math","S P=5",28,INK),
            ("math","A P=sqrt(10^2-5^2)",26,CYAN),
            ("math","A P=5 sqrt(3)",31,GOLD),
            ("math","Q B=5 sqrt(3)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bán kính tới điểm tiếp xúc vuông góc với tiếp tuyến. "
            "Vì S A bằng mười và S P bằng năm, tam giác S A P vuông tại P.",
            1.8,
        )
        self.narrate(
            "Do đó A P bằng căn của một trăm trừ hai mươi lăm, tức năm căn ba. "
            "Phía bên kia hoàn toàn đối xứng nên Q B cũng bằng năm căn ba.",
            1.9,
        )

    def inner_arc(self):
        self.clear_all()
        self.add_hud("Tính cung PQ trên đường tròn trong","08 / 13")

        ann,pts=annular_sector(
            show_valid=True,
            show_tangent_points=True
        )
        self.add_fixed_in_frame_mobjects(ann)

        card=lesson_card("GÓC TIẾP XÚC",[
            ("math","cos beta=frac(5,10)=frac(1,2)",26,INK),
            ("math","beta=frac(pi,3)",30,CYAN),
            ("math","hat(P S Q)=pi-2 beta=frac(pi,3)",23,GOLD),
            ("math","s_(P Q)=5 times frac(pi,3)",25,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Gọi beta là góc A S P. "
            "Trong tam giác vuông S A P, cos beta bằng năm trên mười, tức một phần hai.",
            1.8,
        )
        self.narrate(
            "Vì vậy beta bằng pi trên ba. "
            "Góc từ A tới B là pi, nên góc P S Q còn lại cũng bằng pi trên ba.",
            1.8,
        )
        self.narrate(
            "Bán kính đường tròn trong bằng năm, vì thế độ dài cung P Q bằng năm pi trên ba.",
            1.6,
        )

    def result(self):
        self.clear_all()
        self.add_hud("Độ dài nhỏ nhất trong lớp 300°","09 / 13")

        ann,pts=annular_sector(
            show_valid=True,
            show_tangent_points=True
        )
        self.add_fixed_in_frame_mobjects(ann)

        card=lesson_card("CỘNG BA PHẦN",[
            ("math","L=A P+s_(P Q)+Q B",25,INK),
            ("math","L=5 sqrt(3)+frac(5 pi,3)+5 sqrt(3)",23,CYAN),
            ("math","L=10 sqrt(3)+frac(5 pi,3)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Đường tối ưu gồm đúng ba phần: tiếp tuyến A P, cung P Q và tiếp tuyến Q B.",
            1.6,
        )
        self.narrate(
            "Cộng lại, độ dài nhỏ nhất trong lớp đi theo chiều ba trăm độ là mười căn ba cộng năm pi trên ba.",
            1.8,
        )

    def fold_walk(self):
        self.clear_all()
        self.add_hud("Gấp lại: đường tối ưu chạm vành trên","10 / 13")

        A,B=frustum_endpoints()
        path=shortest_long_curve(GOLD,6.0)
        ant=Dot3D(A,radius=0.085,color=GREEN)

        self.add(
            frustum_wireframe(),
            path,
            ant,
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("TRÊN NÓN CỤT",[
            ("text","Đường đi chạm vành trên tại P.",18,GOLD),
            ("text","Đi dọc một đoạn trên vành trên.",18,CYAN),
            ("text","Rời vành trên tại Q rồi xuống B.",18,GOLD),
            ("math","L=10 sqrt(3)+frac(5 pi,3)",27,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Khi gấp vành quạt trở lại, đoạn A P đi từ đáy lớn lên vành trên, "
            "sau đó đường đi men theo vành trên rồi rời vành tại Q để xuống B.",
            MoveAlongPath(ant,shortest_long_curve(GOLD,1.0)),
            min_time=5.0,
            rate_func=linear,
        )

    def short_class(self):
        self.clear_all()
        self.add_hud("Nếu không ép đi theo chiều dài thì sao?","11 / 13")

        dia=short_class_sector()
        self.add_fixed_in_frame_mobjects(dia)

        card=lesson_card("CHIỀU NGẮN CHỈ 60°",[
            ("math","delta_S=frac(pi,3)",27,CYAN),
            ("math","alpha_S=frac(pi,5)",27,CYAN),
            ("math","L_sh=20 sin frac(pi,10)",27,GOLD),
            ("text","Đoạn thẳng này không chạm lỗ.",18,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu đề bài không bắt buộc đi theo chiều ba trăm độ, ta nên xét chiều còn lại chỉ sáu mươi độ.",
            1.7,
        )
        self.narrate(
            "Sau khi đổi góc, sáu mươi độ trở thành ba mươi sáu độ trên bản trải.",
            1.6,
        )
        self.narrate(
            "Đoạn dây cung tương ứng nằm hoàn toàn bên ngoài lỗ bán kính năm, nên lần này nó hợp lệ và ngắn hơn rất nhiều.",
            1.8,
        )

    def validity_rule(self):
        self.clear_all()
        self.add_hud("Khi nào đoạn thẳng bị lỗ chặn?","12 / 13")

        ann,pts=annular_sector(show_invalid=True,show_valid=False)
        self.add_fixed_in_frame_mobjects(ann)

        card=lesson_card("HAI ĐIỂM CÙNG Ở BÁN KÍNH NGOÀI R",[
            ("math","d=R cos frac(alpha,2)",24,CYAN),
            ("text","Đây là khoảng cách từ tâm tới dây cung.",17,INK),
            ("math","d>=r_1",25,GREEN),
            ("text","thì đoạn thẳng nằm ngoài lỗ.",17,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Có một cách kiểm tra rất nhanh. "
            "Với hai điểm trên cùng đường tròn ngoài bán kính R, cách nhau góc alpha, khoảng cách từ tâm tới dây cung bằng R cos alpha trên hai.",
            2.0,
        )
        self.narrate(
            "Nếu khoảng cách này lớn hơn hoặc bằng bán kính trong, đoạn thẳng không chui vào lỗ và hoàn toàn hợp lệ.",
            1.7,
        )
        self.narrate(
            "Nếu nó nhỏ hơn bán kính trong, ta phải thay đoạn thẳng bằng cấu trúc tiếp tuyến, cung tròn, tiếp tuyến như vừa làm.",
            1.8,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài hình nón cụt","13 / 13")

        A,B=frustum_endpoints()
        self.add(
            frustum_wireframe(),
            shortest_long_curve(GOLD,6.0),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("BỐN Ý CẦN NHỚ",[
            ("text","1. Nón cụt trải thành một vành quạt.",18,INK),
            ("text","2. Vành quạt có lỗ nên phải kiểm tra đường thẳng.",17,INK),
            ("text","3. Nếu bị chặn: tiếp tuyến + cung + tiếp tuyến.",17,CYAN),
            ("math","L=10 sqrt(3)+frac(5 pi,3)",27,GOLD),
            ("text","4. Luôn phân biệt lớp đường đang xét.",17,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hình nón cụt bổ sung một điều mà hình nón đầy chưa có: miền khai triển có một lỗ ở giữa.",
            1.7,
        )
        self.narrate(
            "Vì thế không được máy móc nối thẳng hai điểm. "
            "Trước hết phải kiểm tra xem đoạn thẳng có nằm hoàn toàn trong vành quạt hay không.",
            1.8,
        )
        self.narrate(
            "Trong lớp đường ba trăm độ của bài này, đoạn thẳng đi qua lỗ nên không hợp lệ. "
            "Đường tối ưu phải tiếp xúc vành trong, đi theo một cung, rồi rời vành để tới B.",
            1.9,
        )

    def construct(self):
        self.intro()
        self.model()
        self.extend_cone()
        self.long_class()
        self.exact_unroll()
        self.invalid_chord()
        self.tangent_idea()
        self.tangent_length()
        self.inner_arc()
        self.result()
        self.fold_walk()
        self.short_class()
        self.validity_rule()
        self.summary()


class Smoke14(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.95)

        s=ValueTracker(RATIO)
        mesh=always_redraw(lambda: unfold_wire_group(s.get_value()))
        path=always_redraw(lambda: unfold_path_group(s.get_value()))
        self.add(mesh,path)
        self.play(
            s.animate.set_value(1.0),
            run_time=2.5,
            rate_func=smooth,
        )
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)

    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_14_master_smoke"
    config.disable_caching=True

    scene=Smoke14()
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
    config.output_file="trai_phang_14_hinh_non_cut_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang14Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_14.wav"
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

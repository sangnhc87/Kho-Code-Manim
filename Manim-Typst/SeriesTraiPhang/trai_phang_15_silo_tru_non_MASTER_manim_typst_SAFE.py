
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









# ---------- geometry engine: silo = cylinder + cone ----------
# Educational model:
#
# Cylinder:
#   radius R = 3
#   height Hc = 4
#
# Conical roof:
#   base radius R = 3
#   vertical height Hn = 4
#   slant length l = 5
#
# Surface route:
#   A is on the lower rim of the cylinder at angle 0.
#   M is a FIXED maintenance point on the circular joint at angle 2*pi/3.
#   B is on the conical roof, halfway along a generator from the apex:
#       rho_B = 5/2 from apex along the cone.
#   B has azimuth 3*pi/2.
#
# Hence:
#   cylinder angular change A->M = 2*pi/3
#   developed horizontal cylinder shift = R*(2*pi/3) = 2*pi
#   d_cyl = sqrt((2*pi)^2 + 4^2) = 2*sqrt(pi^2+4)
#
# On the cone:
#   physical azimuth change M->B = 5*pi/6
#   development factor = R/l = 3/5
#   developed angle alpha = pi/2
#   M lies at radius 5 in the sector
#   B lies at radius 5/2 in the sector
#   d_cone = sqrt(5^2 + (5/2)^2) = 5*sqrt(5)/2
#
# Therefore the shortest route constrained to pass through M is:
#   Lmin = 2*sqrt(pi^2+4) + 5*sqrt(5)/2
#
# This video deliberately teaches COMPOSITION:
# shortest-on-cylinder + shortest-on-cone, joined at the fixed seam point M.
# ==========================================================

RADIUS = 3.0
CYL_H = 4.0
CONE_H = 4.0
SLANT = 5.0
APEX_Z = CYL_H + CONE_H

THETA_A = 0.0
THETA_M = 2.0 * math.pi / 3.0
THETA_B = 3.0 * math.pi / 2.0

DELTA_CYL = THETA_M - THETA_A        # 2*pi/3
DELTA_CONE = THETA_B - THETA_M      # 5*pi/6
RATIO = RADIUS / SLANT               # 3/5
ALPHA_CONE = RATIO * DELTA_CONE      # pi/2
RHO_B = SLANT / 2.0                  # 5/2

CYL_ARC = RADIUS * DELTA_CYL         # 2*pi
CYL_LEN = math.hypot(CYL_ARC, CYL_H)

CONE_LEN = math.sqrt(
    SLANT**2 + RHO_B**2
    - 2.0*SLANT*RHO_B*math.cos(ALPHA_CONE)
)

TOTAL_LEN = CYL_LEN + CONE_LEN

WORLD_SCALE = 0.68
WORLD_SHIFT = np.array([-3.25, -0.18, -0.35])

CAM_PHI = 67 * DEGREES
CAM_THETA = -48 * DEGREES

# Visual flat layouts.
RECT_W = 5.65
RECT_H = 3.10
SECTOR_CENTER = np.array([LEFT_CENTER[0]-0.45, LEFT_CENTER[1]-0.10, 0.0])
SECTOR_SCALE = 0.62
SECTOR_ROT = -0.95


def W(p):
    return WORLD_SCALE * np.array(p, dtype=float) + WORLD_SHIFT


def cyl_point(theta, z):
    return np.array([
        RADIUS*math.cos(theta),
        RADIUS*math.sin(theta),
        z,
    ], dtype=float)


def cone_point_from_rho(theta, rho):
    """Point on conical roof, rho measured from apex along a generator."""
    radial = (RADIUS/SLANT)*rho
    z = APEX_Z - (CONE_H/SLANT)*rho
    return np.array([
        radial*math.cos(theta),
        radial*math.sin(theta),
        z,
    ], dtype=float)


A_RAW = cyl_point(THETA_A, 0.0)
M_RAW = cyl_point(THETA_M, CYL_H)
B_RAW = cone_point_from_rho(THETA_B, RHO_B)
S_RAW = np.array([0.0, 0.0, APEX_Z], dtype=float)


def cylinder_surface():
    return Surface(
        lambda u, v: W(cyl_point(u, CYL_H*v)),
        u_range=[0, TAU],
        v_range=[0, 1],
        resolution=(28, 8),
        fill_color=BLUE,
        fill_opacity=0.055,
        stroke_width=0.0,
    )


def cone_surface():
    return Surface(
        lambda u, v: W(cone_point_from_rho(u, SLANT*v)),
        u_range=[0, TAU],
        v_range=[0.02, 1],
        resolution=(28, 8),
        fill_color=PURPLE,
        fill_opacity=0.060,
        stroke_width=0.0,
    )


def silo_wireframe():
    g = VGroup(cylinder_surface(), cone_surface())

    # Cylinder bottom and joint rim.
    for z, color, width in [
        (0.0, EDGE, 3.4),
        (CYL_H, GOLD, 4.0),
    ]:
        g.add(ParametricFunction(
            lambda th, z=z: W(cyl_point(th, z)),
            t_range=[0, TAU],
            color=color,
            stroke_width=width,
        ))

    # Cone apex and generators.
    for j in range(12):
        th = TAU*j/12
        g.add(
            Line(
                W(cyl_point(th, 0.0)),
                W(cyl_point(th, CYL_H)),
                color=GRID,
                stroke_width=1.7,
                stroke_opacity=0.58,
            ),
            Line(
                W(S_RAW),
                W(cyl_point(th, CYL_H)),
                color=GRID,
                stroke_width=1.7,
                stroke_opacity=0.58,
            ),
        )

    # Highlight generator through A as a reference.
    g.add(Line(
        W(cyl_point(THETA_A, 0.0)),
        W(cyl_point(THETA_A, CYL_H)),
        color=CYAN,
        stroke_width=3.2,
        stroke_opacity=0.85,
    ))

    return g


def cylinder_geodesic_raw(t):
    theta = THETA_A + DELTA_CYL*t
    z = CYL_H*t
    return cyl_point(theta, z)


def cone_geodesic_flat_xy(t):
    """Straight segment in the cone sector from M_flat to B_flat."""
    M2 = np.array([SLANT, 0.0], dtype=float)
    B2 = np.array([
        RHO_B*math.cos(ALPHA_CONE),
        RHO_B*math.sin(ALPHA_CONE),
    ], dtype=float)
    return (1.0-t)*M2 + t*B2


def rho_psi_from_flat(xy):
    x, y = float(xy[0]), float(xy[1])
    rho = math.hypot(x, y)
    psi = math.atan2(y, x)
    return rho, psi


def cone_geodesic_raw(t):
    xy = cone_geodesic_flat_xy(t)
    rho, alpha = rho_psi_from_flat(xy)

    # alpha on sector -> physical azimuth offset multiplied by l/R.
    theta = THETA_M + alpha / RATIO
    return cone_point_from_rho(theta, rho)


def cylinder_geodesic(color=GOLD, width=6.0):
    return ParametricFunction(
        lambda t: W(cylinder_geodesic_raw(t)),
        t_range=[0, 1],
        color=color,
        stroke_width=width,
    )


def cone_geodesic(color=CYAN, width=6.0):
    return ParametricFunction(
        lambda t: W(cone_geodesic_raw(t)),
        t_range=[0, 1],
        color=color,
        stroke_width=width,
    )


def total_route_group():
    return VGroup(
        cylinder_geodesic(GOLD, 6.0),
        cone_geodesic(CYAN, 6.0),
        Dot3D(W(A_RAW), radius=0.080, color=GREEN),
        Dot3D(W(M_RAW), radius=0.070, color=GOLD),
        Dot3D(W(B_RAW), radius=0.080, color=RED),
    )


def cylinder_rect():
    """Rectangle development for A -> M."""
    left = LEFT_CENTER[0] - RECT_W/2
    bottom = LEFT_CENTER[1] - RECT_H/2

    # Show one full circumference rectangle: width 6*pi, height 4.
    CIRC = TAU*RADIUS

    def T(s, z):
        return np.array([
            left + RECT_W*(s/CIRC),
            bottom + RECT_H*(z/CYL_H),
            0.0,
        ])

    A = T(0.0, 0.0)
    M = T(CYL_ARC, CYL_H)

    rect = Rectangle(
        width=RECT_W,
        height=RECT_H,
        stroke_color=EDGE,
        stroke_width=3.0,
        fill_color=BLUE,
        fill_opacity=0.08,
    ).move_to(LEFT_CENTER)

    seam0 = Line(T(0,0), T(0,CYL_H), color=GOLD, stroke_width=4.4)
    seam1 = Line(T(CIRC,0), T(CIRC,CYL_H), color=GOLD, stroke_width=4.4)

    g = VGroup(
        rect,
        seam0,
        seam1,
        Dot(A, radius=0.072, color=GREEN),
        Dot(M, radius=0.072, color=GOLD),
        Line(A, M, color=GOLD, stroke_width=6.2),
    )
    return g, {"A":A, "M":M, "T":T}


def sector_point(rho, alpha):
    ang = alpha + SECTOR_ROT
    return SECTOR_CENTER + SECTOR_SCALE*np.array([
        rho*math.cos(ang),
        rho*math.sin(ang),
        0.0,
    ])


def cone_sector():
    """Cone roof sector, with M and B highlighted."""
    phi = TAU*RATIO  # 6*pi/5

    arc_pts = [
        sector_point(SLANT, phi*k/120)
        for k in range(121)
    ]
    center = SECTOR_CENTER

    poly = Polygon(
        center, *arc_pts,
        fill_color=PURPLE,
        fill_opacity=0.10,
        stroke_width=0.0,
    )
    arc = VMobject(color=EDGE, stroke_width=3.2)
    arc.set_points_as_corners(arc_pts)

    side1 = Line(center, arc_pts[0], color=GOLD, stroke_width=3.7)
    side2 = Line(center, arc_pts[-1], color=GOLD, stroke_width=3.7)

    # Place M at alpha=0 and B at alpha=pi/2 after a local rigid rotation.
    M = sector_point(SLANT, 0.0)
    B = sector_point(RHO_B, ALPHA_CONE)

    g = VGroup(
        poly, arc, side1, side2,
        Dot(center, radius=0.050, color=INK),
        Dot(M, radius=0.072, color=GOLD),
        Dot(B, radius=0.072, color=RED),
        Line(M, B, color=CYAN, stroke_width=6.2),
        Line(center, M, color=DIM, stroke_width=2.2),
        Line(center, B, color=DIM, stroke_width=2.2),
    )
    return g, {"S":center, "M":M, "B":B}


def paired_flat_diagram():
    """Show rectangle and sector together, but not physically glued."""
    cyl, cpts = cylinder_rect()
    cone, npts = cone_sector()

    cyl.scale(0.78).shift(UP*1.35)
    cone.scale(0.72).shift(DOWN*1.18)

    return VGroup(cyl, cone)


def geometry_preflight(verbose=True):
    tol = 1e-9

    # Core silo dimensions.
    if abs(math.hypot(RADIUS, CONE_H) - SLANT) > tol:
        raise AssertionError("Cone roof should be 3-4-5")
    if abs(RATIO - 3.0/5.0) > tol:
        raise AssertionError("Cone development ratio should be 3/5")

    # Named point checks.
    if abs(np.linalg.norm(A_RAW[:2]) - RADIUS) > tol:
        raise AssertionError("A must lie on lower rim")
    if abs(np.linalg.norm(M_RAW[:2]) - RADIUS) > tol or abs(M_RAW[2]-CYL_H) > tol:
        raise AssertionError("M must lie on circular joint")

    expected_B_rad = RATIO*RHO_B
    expected_B_z = APEX_Z - (CONE_H/SLANT)*RHO_B
    if abs(np.linalg.norm(B_RAW[:2]) - expected_B_rad) > tol:
        raise AssertionError("Wrong B radial coordinate")
    if abs(B_RAW[2] - expected_B_z) > tol:
        raise AssertionError("Wrong B height")

    # Cylinder development.
    if abs(DELTA_CYL - 2.0*math.pi/3.0) > tol:
        raise AssertionError("Cylinder angular separation mismatch")
    if abs(CYL_ARC - 2.0*math.pi) > tol:
        raise AssertionError("Cylinder developed horizontal shift should be 2pi")

    expected_cyl = 2.0*math.sqrt(math.pi**2 + 4.0)
    if abs(CYL_LEN - expected_cyl) > tol:
        raise AssertionError("Cylinder segment length mismatch")

    # Cone development.
    if abs(DELTA_CONE - 5.0*math.pi/6.0) > tol:
        raise AssertionError("Cone physical angle mismatch")
    if abs(ALPHA_CONE - math.pi/2.0) > tol:
        raise AssertionError("Cone developed angle should be pi/2")

    expected_cone = 5.0*math.sqrt(5.0)/2.0
    if abs(CONE_LEN - expected_cone) > tol:
        raise AssertionError("Cone segment length mismatch")

    # Verify cone geodesic endpoints in 3D.
    if np.linalg.norm(cone_geodesic_raw(0.0) - M_RAW) > 1e-8:
        raise AssertionError("Cone path must start at M")
    if np.linalg.norm(cone_geodesic_raw(1.0) - B_RAW) > 1e-8:
        raise AssertionError("Cone path must end at B")

    # Piecewise total.
    expected_total = expected_cyl + expected_cone
    if abs(TOTAL_LEN - expected_total) > tol:
        raise AssertionError("Total length mismatch")

    # Alternative directions within each piece are longer.
    cyl_alt = math.hypot(RADIUS*(TAU-DELTA_CYL), CYL_H)
    if not (CYL_LEN < cyl_alt):
        raise AssertionError("Chosen cylinder direction should be shorter")

    alpha_alt = RATIO*(TAU-DELTA_CONE)
    cone_alt = math.sqrt(
        SLANT**2 + RHO_B**2
        - 2*SLANT*RHO_B*math.cos(alpha_alt)
    )
    if not (CONE_LEN < cone_alt):
        raise AssertionError("Chosen cone direction should be shorter")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  silo: cylinder r=3,h=4 + cone roof r=3,h=4,l=5")
        print("  fixed joint point M at angle 2pi/3")
        print("  B at rho=5/2 from apex, azimuth 3pi/2")
        print("  cylinder development shift=2pi")
        print("  d_cyl=2*sqrt(pi^2+4)")
        print("  cone developed angle=pi/2")
        print("  d_cone=5*sqrt(5)/2")
        print("  total=2*sqrt(pi^2+4)+5*sqrt(5)/2")
    return True


def layout_samples():
    return [
        lesson_card("MÔ HÌNH SILO",[
            ("math","r=3",28,CYAN),
            ("math","h_tr=4",27,CYAN),
            ("math","h_(non)=4, l=5",26,CYAN),
            ("text","A ở đáy trụ, B trên mái nón.",18,INK),
            ("text","Đường đi bắt buộc qua điểm nối M.",18,GOLD),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","L_tr=2 sqrt(pi^2+4)",27,GOLD),
            ("math","L_(non)=frac(5 sqrt(5),2)",27,CYAN),
            ("math","L_(min)=2 sqrt(pi^2+4)+frac(5 sqrt(5),2)",24,GREEN),
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
        h=header(15,title,progress)
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


class TraiPhang15Master(BaseLesson):
    def intro(self):
        self.clear_all()

        self.add(silo_wireframe(), total_route_group())

        card=intro_card(
            15,
            ["SILO TRỤ + NÓN","GHÉP HAI PHÉP KHAI TRIỂN"],
            "Một đường đi nhưng đi qua hai loại mặt khác nhau.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Video mười lăm ghép hai mô hình đã học: một thân hình trụ và một mái hình nón.",
            1.5,
        )
        self.narrate(
            "Đường đi bắt đầu trên thân trụ, đi qua vòng nối giữa hai phần, rồi tiếp tục trên mái nón. "
            "Ta sẽ phải dùng hai bản khai triển khác nhau trong cùng một bài.",
            1.9,
        )

    def model(self):
        self.clear_all()
        self.add_hud("Một silo có thân trụ và mái nón","01 / 12")

        self.add(
            silo_wireframe(),
            Dot3D(W(A_RAW),radius=0.080,color=GREEN),
            Dot3D(W(M_RAW),radius=0.070,color=GOLD),
            Dot3D(W(B_RAW),radius=0.080,color=RED),
        )

        card=lesson_card("KÍCH THƯỚC",[
            ("math","r=3",29,CYAN),
            ("math","h_tr=4",27,CYAN),
            ("math","h_(non)=4",27,CYAN),
            ("math","l=5",29,GOLD),
            ("text","M là một điểm bảo trì cố định trên vòng nối.",17,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Thân silo là hình trụ bán kính ba, cao bốn. "
            "Mái là hình nón cùng bán kính đáy ba và cao bốn, nên đường sinh của mái bằng năm.",
            1.8,
        )
        self.narrate(
            "Điểm A nằm trên vành dưới của thân trụ. "
            "Điểm B nằm trên mái nón. Đường đi bắt buộc phải qua điểm bảo trì M trên vòng nối.",
            1.8,
        )

    def locate_points(self):
        self.clear_all()
        self.add_hud("Vị trí ba điểm A, M, B","02 / 12")

        self.add(silo_wireframe(), total_route_group())

        card=lesson_card("CÁC GÓC QUANH TRỤC",[
            ("text","A được chọn làm mốc góc 0°.",18,GREEN),
            ("text","M lệch A một góc 120°.",18,GOLD),
            ("text","Từ M tới phương của B là 150°.",18,CYAN),
            ("text","B nằm giữa một đường sinh của mái.",18,RED),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta lấy đường sinh qua A làm mốc. "
            "Điểm M trên vòng nối lệch A một trăm hai mươi độ quanh trục.",
            1.7,
        )
        self.narrate(
            "Từ M tới đường sinh chứa B lệch thêm một trăm năm mươi độ. "
            "Điểm B nằm đúng giữa đường sinh của mái tính từ đỉnh xuống vòng nối.",
            1.9,
        )

    def split_problem(self):
        self.clear_all()
        self.add_hud("Vì M cố định, bài toán tách thành hai phần","03 / 12")

        self.add(silo_wireframe())
        self.add(
            cylinder_geodesic(GOLD,6.0),
            cone_geodesic(CYAN,6.0),
            Dot3D(W(M_RAW),radius=0.075,color=GOLD),
        )

        card=lesson_card("TÁCH BÀI TOÁN",[
            ("text","Phần 1: ngắn nhất từ A tới M trên hình trụ.",17,GOLD),
            ("text","Phần 2: ngắn nhất từ M tới B trên hình nón.",17,CYAN),
            ("text","M là điểm chung cố định.",18,INK),
            ("text","Tối ưu từng phần rồi cộng lại.",18,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Do M đã được cố định, mọi đường hợp lệ từ A tới B đều phải gồm một đoạn trên thân trụ từ A tới M và một đoạn trên mái từ M tới B.",
            1.9,
        )
        self.narrate(
            "Vì vậy ta có thể tìm đường ngắn nhất của từng phần một cách độc lập, rồi cộng hai kết quả.",
            1.6,
        )

    def cylinder_flat(self):
        self.clear_all()
        self.add_hud("Phần 1: trải thân trụ","04 / 12")

        rect,pts=cylinder_rect()
        self.add_fixed_in_frame_mobjects(rect)

        card=lesson_card("A → M TRÊN HÌNH TRỤ",[
            ("math","Delta theta=frac(2 pi,3)",27,CYAN),
            ("math","Delta s=r Delta theta=2 pi",26,CYAN),
            ("math","Delta z=4",29,INK),
            ("text","Trên hình chữ nhật, nối A với M.",18,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trải mặt xung quanh của thân trụ thành hình chữ nhật.",
            1.3,
        )
        self.narrate(
            "Từ A tới M lệch một trăm hai mươi độ. "
            "Độ lệch ngang trên bản khai triển bằng bán kính ba nhân hai pi trên ba, tức hai pi.",
            1.9,
        )
        self.narrate(
            "Độ lệch đứng bằng chiều cao thân trụ là bốn. "
            "Vì thế đường ngắn nhất của phần này là đường chéo tương ứng.",
            1.7,
        )

    def cylinder_length(self):
        self.clear_all()
        self.add_hud("Tính độ dài trên phần hình trụ","05 / 12")

        rect,pts=cylinder_rect()
        self.add_fixed_in_frame_mobjects(rect)

        card=lesson_card("PYTHAGORE",[
            ("math","L_tr^2=(2 pi)^2+4^2",28,INK),
            ("math","L_tr=sqrt(4 pi^2+16)",28,CYAN),
            ("math","L_tr=2 sqrt(pi^2+4)",32,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Theo Pythagore, bình phương độ dài phần trên thân trụ bằng bốn pi bình phương cộng mười sáu.",
            1.7,
        )
        self.narrate(
            "Do đó độ dài ngắn nhất từ A tới M trên thân trụ bằng hai nhân căn của pi bình phương cộng bốn.",
            1.8,
        )

    def cone_flat(self):
        self.clear_all()
        self.add_hud("Phần 2: trải mái nón","06 / 12")

        sector,pts=cone_sector()
        self.add_fixed_in_frame_mobjects(sector)

        card=lesson_card("M → B TRÊN MÁI NÓN",[
            ("math","l=5",28,CYAN),
            ("math","rho_B=frac(5,2)",27,CYAN),
            ("math","delta=frac(5 pi,6)",27,INK),
            ("math","alpha=frac(3,5) delta=frac(pi,2)",25,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bây giờ xét phần mái nón. "
            "Điểm M nằm trên vành đáy của mái nên cách đỉnh theo đường sinh một đoạn năm.",
            1.7,
        )
        self.narrate(
            "Điểm B nằm giữa một đường sinh nên cách đỉnh theo mặt nón một đoạn năm trên hai.",
            1.7,
        )
        self.narrate(
            "Góc quanh trục từ M tới B là năm pi trên sáu. "
            "Khi trải nón, góc này được nhân với ba phần năm và trở thành đúng pi trên hai.",
            1.9,
        )

    def cone_length(self):
        self.clear_all()
        self.add_hud("Tính độ dài trên phần hình nón","07 / 12")

        sector,pts=cone_sector()
        self.add_fixed_in_frame_mobjects(sector)

        card=lesson_card("TAM GIÁC VUÔNG TRÊN HÌNH QUẠT",[
            ("math","S M=5",28,INK),
            ("math","S B=frac(5,2)",28,INK),
            ("math","hat(M S B)=frac(pi,2)",27,CYAN),
            ("math","L_(non)=frac(5 sqrt(5),2)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trên hình quạt, M và B tạo với đỉnh S một góc chín mươi độ.",
            1.5,
        )
        self.narrate(
            "Hai khoảng cách tới S lần lượt là năm và năm trên hai. "
            "Do đó M B bằng căn của hai mươi lăm cộng hai mươi lăm phần bốn.",
            1.8,
        )
        self.narrate(
            "Rút gọn, độ dài ngắn nhất trên phần mái nón bằng năm căn năm trên hai.",
            1.6,
        )

    def combine(self):
        self.clear_all()
        self.add_hud("Ghép hai kết quả tại điểm M","08 / 12")

        pair=paired_flat_diagram()
        self.add_fixed_in_frame_mobjects(pair)

        card=lesson_card("TỔNG ĐỘ DÀI",[
            ("math","L_(min)=L_tr+L_(non)",27,INK),
            ("math","L_tr=2 sqrt(pi^2+4)",26,GOLD),
            ("math","L_(non)=frac(5 sqrt(5),2)",26,CYAN),
            ("math","L_(min)=2 sqrt(pi^2+4)+frac(5 sqrt(5),2)",22,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hai bản khai triển nhìn rất khác nhau, nhưng chúng gặp nhau ở cùng một điểm vật lý là M.",
            1.6,
        )
        self.narrate(
            "Vì M cố định, độ dài nhỏ nhất toàn tuyến chỉ là tổng của hai độ dài nhỏ nhất vừa tìm.",
            1.7,
        )

    def proof(self):
        self.clear_all()
        self.add_hud("Vì sao tối ưu từng phần rồi cộng là đúng?","09 / 12")

        self.add(silo_wireframe(), total_route_group())

        card=lesson_card("VỚI MỌI ĐƯỜNG ĐI QUA M",[
            ("math","L_(A M)>=L_tr",27,GOLD),
            ("math","L_(M B)>=L_(non)",27,CYAN),
            ("math","L>=L_tr+L_(non)",28,INK),
            ("text","Dấu bằng khi cả hai đoạn đều tối ưu.",17,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Lập luận rất ngắn. "
            "Bất kỳ đường nào từ A tới M trên thân trụ cũng không thể ngắn hơn đường chéo của bản khai triển.",
            1.8,
        )
        self.narrate(
            "Tương tự, bất kỳ đường nào từ M tới B trên mái nón cũng không thể ngắn hơn đoạn thẳng trên hình quạt.",
            1.8,
        )
        self.narrate(
            "Cộng hai bất đẳng thức, ta được cận dưới cho toàn tuyến. "
            "Đường đang vẽ đạt đồng thời cả hai cận nên chính là đường ngắn nhất qua M.",
            1.9,
        )

    def ant_walk(self):
        self.clear_all()
        self.add_hud("Cho kiến đi toàn tuyến trên silo","10 / 12")

        cyl_path=cylinder_geodesic(GOLD,6.0)
        cone_path=cone_geodesic(CYAN,6.0)
        ant=Dot3D(W(A_RAW),radius=0.085,color=GREEN)

        self.add(
            silo_wireframe(),
            cyl_path,
            cone_path,
            ant,
            Dot3D(W(M_RAW),radius=0.070,color=GOLD),
            Dot3D(W(B_RAW),radius=0.080,color=RED),
        )

        card=lesson_card("HÀNH TRÌNH",[
            ("text","A → M: đường xoắn trên thân trụ.",18,GOLD),
            ("text","M → B: đường địa trắc trên mái nón.",18,CYAN),
            ("text","M là điểm chuyển loại mặt.",18,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Từ A, kiến đi theo đường xoắn ngắn nhất trên thân trụ và tới đúng điểm bảo trì M.",
            MoveAlongPath(ant,cylinder_geodesic(GOLD,1.0)),
            min_time=4.0,
            rate_func=linear,
        )
        self.narrate_play(
            "Tại M, nó chuyển sang mái nón và tiếp tục theo đường ngắn nhất trên mặt nón cho tới B.",
            MoveAlongPath(ant,cone_geodesic(CYAN,1.0)),
            min_time=3.5,
            rate_func=linear,
        )

    def moving_m_extension(self):
        self.clear_all()
        self.add_hud("Nếu M không cố định thì bài toán khó hơn","11 / 12")

        self.add(silo_wireframe())

        card=lesson_card("M LÚC NÀY LÀ BIẾN",[
            ("text","M có thể chạy trên cả vòng nối.",18,INK),
            ("text","Độ dài phần trụ thay đổi theo M.",18,GOLD),
            ("text","Độ dài phần nón cũng thay đổi theo M.",18,CYAN),
            ("text","Ta phải tối ưu tổng của hai hàm.",18,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu đề bài không cho sẵn điểm M mà cho phép điểm chuyển mặt chạy trên toàn bộ vòng nối, "
            "ta không còn được tối ưu hai phần độc lập.",
            1.9,
        )
        self.narrate(
            "Khi M thay đổi, độ dài trên thân trụ và độ dài trên mái nón cùng thay đổi. "
            "Lúc đó phải tối ưu tổng của hai đại lượng theo vị trí của M.",
            1.8,
        )
        self.narrate(
            "Đó là phiên bản nâng cao của bài silo và là cầu nối rất tự nhiên tới các bài tham số ở cuối series.",
            1.7,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài silo trụ + nón","12 / 12")

        self.add(silo_wireframe(), total_route_group())

        card=lesson_card("BỐN Ý CẦN NHỚ",[
            ("text","1. Mặt trụ → hình chữ nhật.",18,INK),
            ("text","2. Mặt nón → hình quạt.",18,INK),
            ("text","3. M cố định nên tối ưu riêng từng phần.",17,CYAN),
            ("math","L_tr=2 sqrt(pi^2+4)",25,GOLD),
            ("math","L_(non)=frac(5 sqrt(5),2)",25,CYAN),
            ("math","L_(min)=L_tr+L_(non)",26,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bài silo là lần đầu tiên trong series một đường đi phải qua hai loại mặt cong khác nhau.",
            1.6,
        )
        self.narrate(
            "Trên thân trụ, ta dùng hình chữ nhật. "
            "Trên mái nón, ta dùng hình quạt và phải đổi góc theo tỉ số bán kính trên đường sinh.",
            1.8,
        )
        self.narrate(
            "Vì điểm nối M cố định, hai bài toán ghép lại rất sạch: giải ngắn nhất từng phần rồi cộng.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.model()
        self.locate_points()
        self.split_problem()
        self.cylinder_flat()
        self.cylinder_length()
        self.cone_flat()
        self.cone_length()
        self.combine()
        self.proof()
        self.ant_walk()
        self.moving_m_extension()
        self.summary()


class Smoke15(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.95)
        self.add(
            silo_wireframe(),
            cylinder_geodesic(GOLD,5.5),
            cone_geodesic(CYAN,5.5),
        )
        self.wait(0.3)


def render_smoke():
    geometry_preflight(True)

    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_15_master_smoke"
    config.disable_caching=True

    scene=Smoke15()
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
    config.output_file="trai_phang_15_silo_tr_non_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang15Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_15.wav"
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

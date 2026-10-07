
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







# ---------- geometry engine: cone lateral surface ----------
# Right circular cone with:
#   base radius r=3
#   vertical height h=4
#   slant height l=5
#
# Two points A, B lie on the base rim.
# Their azimuthal separation on the cone is:
#   delta = 5*pi/6 = 150 degrees.
#
# Development:
#   lateral sector radius = l = 5
#   sector angle Phi = 2*pi*r/l = 6*pi/5
#   developed separation alpha = (r/l)*delta = pi/2
#
# Therefore the shortest lateral path is the sector chord:
#   L = 2*l*sin(alpha/2) = 5*sqrt(2).
#
# Exact continuous unrolling:
# parameter s = sin(beta) varies from r/l to 1.
# E(rho,psi;s) = (
#   rho*s*cos(psi/s),
#   rho*s*sin(psi/s),
#   -rho*sqrt(1-s^2)
# )
#
# Its metric is exactly d(rho)^2 + rho^2 d(psi)^2 for every s.
# Thus s=r/l is the cone and s=1 is the flat sector.
# ==========================================================

RADIUS = 3.0
HEIGHT = 4.0
SLANT = 5.0
RATIO = RADIUS / SLANT
SECTOR_ANGLE = 2.0 * math.pi * RATIO  # 6*pi/5

DELTA = 5.0 * math.pi / 6.0
ALPHA = RATIO * DELTA                 # pi/2

# Keep A and B away from the cut seam in the flat sector.
PSI_A = math.pi / 5.0
PSI_B = PSI_A + ALPHA

WORLD_SCALE = 0.72
WORLD_SHIFT = np.array([-3.28,0.55,1.15])

CAM_PHI = 67 * DEGREES
CAM_THETA = -47 * DEGREES

SECTOR_VIS_ROT = -SECTOR_ANGLE / 2.0
SECTOR_VIS_SCALE = 0.49
SECTOR_CENTER = np.array([LEFT_CENTER[0]-0.90, LEFT_CENTER[1]-0.05, 0.0])


def W(p):
    return WORLD_SCALE * np.array(p,dtype=float) + WORLD_SHIFT


def iso_point(rho,psi,s):
    """Exact isometric family from cone to sector."""
    s=float(s)
    s=max(RATIO,min(1.0,s))
    c=math.sqrt(max(0.0,1.0-s*s))
    ang=psi/s
    return np.array([
        rho*s*math.cos(ang),
        rho*s*math.sin(ang),
        -rho*c,
    ],dtype=float)


def closed_cone_point(rho,psi):
    return iso_point(rho,psi,RATIO)


def endpoint_raw(which):
    psi=PSI_A if which=="A" else PSI_B
    return closed_cone_point(SLANT,psi)


def flat_xy_from_rho_psi(rho,psi):
    return np.array([
        rho*math.cos(psi),
        rho*math.sin(psi),
    ],dtype=float)


def rho_psi_from_flat_xy(xy):
    x,y=float(xy[0]),float(xy[1])
    rho=math.hypot(x,y)
    psi=math.atan2(y,x)
    if psi < 0:
        psi += 2*math.pi
    return rho,psi


A_FLAT = flat_xy_from_rho_psi(SLANT,PSI_A)
B_FLAT = flat_xy_from_rho_psi(SLANT,PSI_B)


def geodesic_flat_xy(t):
    return (1.0-t)*A_FLAT + t*B_FLAT


def geodesic_raw(t,s=RATIO):
    xy=geodesic_flat_xy(t)
    rho,psi=rho_psi_from_flat_xy(xy)
    return iso_point(rho,psi,s)


def cone_geodesic(color=GOLD,width=6.0):
    return ParametricFunction(
        lambda t: W(geodesic_raw(t,RATIO)),
        t_range=[0,1],
        color=color,
        stroke_width=width,
    )


def generator_via_apex():
    A=endpoint_raw("A")
    B=endpoint_raw("B")
    S=np.array([0.0,0.0,0.0])
    return VGroup(
        Line(W(A),W(S),color=CYAN,stroke_width=4.7),
        Line(W(S),W(B),color=CYAN,stroke_width=4.7),
    )


def cone_surface():
    surf=Surface(
        lambda u,v: W(iso_point(
            SLANT*v,
            SECTOR_ANGLE*u,
            RATIO
        )),
        u_range=[0,1],
        v_range=[0.025,1],
        resolution=(30,10),
        fill_color=BLUE,
        fill_opacity=0.065,
        stroke_width=0.0,
    )
    return surf


def cone_wireframe():
    g=VGroup(cone_surface())

    # Base rim.
    g.add(ParametricFunction(
        lambda psi: W(closed_cone_point(SLANT,psi)),
        t_range=[0,SECTOR_ANGLE],
        color=EDGE,
        stroke_width=3.6,
    ))

    # Generators.
    for j in range(13):
        psi=SECTOR_ANGLE*j/12
        g.add(Line(
            W(closed_cone_point(0.0,psi)),
            W(closed_cone_point(SLANT,psi)),
            color=GOLD if j==0 else GRID,
            stroke_width=4.8 if j==0 else 1.9,
            stroke_opacity=1.0 if j==0 else 0.66,
        ))

    # Slant-level circles.
    for q in [0.25,0.50,0.75]:
        rho=SLANT*q
        g.add(ParametricFunction(
            lambda psi,rho=rho: W(closed_cone_point(rho,psi)),
            t_range=[0,SECTOR_ANGLE],
            color=GRID,
            stroke_width=1.55,
            stroke_opacity=0.55,
        ))

    return g


def cone_endpoints():
    A=W(endpoint_raw("A"))
    B=W(endpoint_raw("B"))
    S=W(np.array([0.0,0.0,0.0]))
    return A,B,S


def direct_chord():
    A,B,S=cone_endpoints()
    return DashedLine(
        A,B,
        color=RED,
        stroke_width=5.0,
        dash_length=0.12,
    )


def unfold_wire_group(s):
    """Wireframe of the exact isometric unrolling state."""
    g=VGroup()

    # Constant slant-distance curves.
    for q in [0.25,0.50,0.75,1.0]:
        rho=SLANT*q
        pts=[
            W(iso_point(rho,SECTOR_ANGLE*k/96,s))
            for k in range(97)
        ]
        curve=VMobject(
            color=EDGE if q==1.0 else GRID,
            stroke_width=3.4 if q==1.0 else 1.6,
            stroke_opacity=0.88 if q==1.0 else 0.62,
        )
        curve.set_points_as_corners(pts)
        g.add(curve)

    # Generators.
    for j in range(13):
        psi=SECTOR_ANGLE*j/12
        p0=W(iso_point(0.0,psi,s))
        p1=W(iso_point(SLANT,psi,s))
        g.add(Line(
            p0,p1,
            color=GOLD if j in {0,12} else GRID,
            stroke_width=4.5 if j in {0,12} else 1.7,
            stroke_opacity=0.85,
        ))

    return g


def unfold_path_group(s):
    pts=[
        W(geodesic_raw(k/96,s))
        for k in range(97)
    ]
    path=VMobject(color=GOLD,stroke_width=6.2)
    path.set_points_as_corners(pts)

    A=W(iso_point(SLANT,PSI_A,s))
    B=W(iso_point(SLANT,PSI_B,s))

    return VGroup(
        path,
        Dot3D(A,radius=0.070,color=GREEN),
        Dot3D(B,radius=0.070,color=RED),
    )


def sector_visual_point(rho,psi):
    ang=psi+SECTOR_VIS_ROT
    return SECTOR_CENTER + SECTOR_VIS_SCALE*np.array([
        rho*math.cos(ang),
        rho*math.sin(ang),
        0.0,
    ])


def sector_net(show_chord=True,show_radii=True):
    arc_pts=[
        sector_visual_point(SLANT,SECTOR_ANGLE*k/120)
        for k in range(121)
    ]
    S=SECTOR_CENTER
    A=sector_visual_point(SLANT,PSI_A)
    B=sector_visual_point(SLANT,PSI_B)

    # Filled sector.
    poly=Polygon(
        S,*arc_pts,
        fill_color=BLUE,
        fill_opacity=0.10,
        stroke_width=0.0,
    )

    arc=VMobject(color=EDGE,stroke_width=3.4)
    arc.set_points_as_corners(arc_pts)

    side1=Line(S,arc_pts[0],color=GOLD,stroke_width=4.0)
    side2=Line(S,arc_pts[-1],color=GOLD,stroke_width=4.0)

    g=VGroup(
        poly,arc,side1,side2,
        Dot(S,radius=0.050,color=INK),
        Dot(A,radius=0.072,color=GREEN),
        Dot(B,radius=0.072,color=RED),
    )

    if show_radii:
        g.add(
            Line(S,A,color=PURPLE,stroke_width=2.6,stroke_opacity=0.75),
            Line(S,B,color=CYAN,stroke_width=2.6,stroke_opacity=0.75),
        )

    if show_chord:
        g.add(Line(A,B,color=GOLD,stroke_width=6.3))

    return g,{"S":S,"A":A,"B":B}


def base_top_view():
    center=LEFT_CENTER + LEFT*0.35
    rad=1.55

    circle=Circle(
        radius=rad,
        color=EDGE,
        stroke_width=3.0
    ).move_to(center)

    # Physical azimuths in the closed cone.
    thetaA=PSI_A/RATIO
    thetaB=PSI_B/RATIO

    A=center+rad*np.array([math.cos(thetaA),math.sin(thetaA),0.0])
    B=center+rad*np.array([math.cos(thetaB),math.sin(thetaB),0.0])

    arc=Arc(
        radius=rad*0.72,
        start_angle=thetaA,
        angle=DELTA,
        color=GOLD,
        stroke_width=5.0,
    ).move_arc_center_to(center)

    return VGroup(
        circle,
        Line(center,A,color=GREEN,stroke_width=3.8),
        Line(center,B,color=RED,stroke_width=3.8),
        arc,
        Dot(A,radius=0.065,color=GREEN),
        Dot(B,radius=0.065,color=RED),
        Dot(center,radius=0.045,color=INK),
    )


def geometry_preflight(verbose=True):
    tol=1e-9

    if abs(math.sqrt(RADIUS**2+HEIGHT**2)-SLANT)>tol:
        raise AssertionError("Slant height should be 5")
    if abs(RATIO-3.0/5.0)>tol:
        raise AssertionError("r/l should be 3/5")
    if abs(SECTOR_ANGLE-6.0*math.pi/5.0)>tol:
        raise AssertionError("Sector angle should be 6pi/5")
    if abs(ALPHA-math.pi/2.0)>tol:
        raise AssertionError("Developed separation should be pi/2")

    # Base arc corresponding to delta equals sector arc corresponding to alpha.
    arc_cone=RADIUS*DELTA
    arc_sector=SLANT*ALPHA
    if abs(arc_cone-arc_sector)>tol:
        raise AssertionError("Arc length not preserved")

    expected=SLANT*math.sqrt(2.0)
    flat_len=np.linalg.norm(B_FLAT-A_FLAT)
    if abs(flat_len-expected)>tol:
        raise AssertionError(("Wrong flat chord length",flat_len,expected))

    # Compare via apex.
    if not (expected < 2*SLANT):
        raise AssertionError("Chord should beat the route via apex")

    # Chord in 3D base plane is shorter but not on lateral surface.
    A3=endpoint_raw("A")
    B3=endpoint_raw("B")
    chord3=np.linalg.norm(B3-A3)
    expected_chord3=2*RADIUS*math.sin(DELTA/2)
    if abs(chord3-expected_chord3)>1e-8:
        raise AssertionError("3D base chord mismatch")
    if not (chord3 < expected):
        raise AssertionError("Interior/base chord should be shorter")

    # Exact metric check of the isometric family.
    # Analytical derivatives:
    # E_rho has norm 1; E_psi has norm rho; dot=0.
    for s in [RATIO,0.72,0.86,1.0]:
        c=math.sqrt(max(0.0,1-s*s))
        for rho in [0.7,2.2,SLANT]:
            for psi in [0.2,1.1,2.5]:
                ang=psi/s
                E_rho=np.array([
                    s*math.cos(ang),
                    s*math.sin(ang),
                    -c,
                ])
                E_psi=np.array([
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

    # Geodesic flattening: endpoint distance stays expected in developed sector.
    # General rim formula for the chosen no-extra-winding class.
    general=2*SLANT*math.sin((RADIUS/SLANT)*DELTA/2)
    if abs(general-expected)>tol:
        raise AssertionError("General rim formula mismatch")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  cone r=3, h=4, slant l=5")
        print("  sector radius 5, sector angle 6pi/5")
        print("  base angular separation delta=5pi/6")
        print("  developed separation alpha=pi/2")
        print("  exact isometric unrolling family verified")
        print("  shortest lateral path L=5sqrt(2)")
        print("  route via apex = 10")
    return True


def layout_samples():
    return [
        lesson_card("BÀI TOÁN",[
            ("math","r=3, h=4, l=5",27,CYAN),
            ("math","delta=frac(5 pi,6)",28,CYAN),
            ("text","A, B nằm trên vành đáy.",19,INK),
            ("text","Chỉ được đi trên mặt xung quanh.",18,GOLD),
            ("math","L_(min)=?",34,GOLD),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","Phi=frac(6 pi,5)",28,CYAN),
            ("math","alpha=frac(r,l) delta=frac(pi,2)",27,CYAN),
            ("math","L=2l sin frac(alpha,2)",27,INK),
            ("math","L=5 sqrt(2)",35,GOLD),
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
        h=header(13,title,progress)
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


class TraiPhang13Master(BaseLesson):
    def intro(self):
        self.clear_all()
        A,B,S=cone_endpoints()
        self.add(
            cone_wireframe(),
            cone_geodesic(),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=intro_card(
            13,
            ["HÌNH NÓN","TRẢI THÀNH HÌNH QUẠT"],
            "Góc quanh trục đổi thành một góc nhỏ hơn trên bản khai triển.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Sau hình trụ, ta sang hình nón. "
            "Mặt xung quanh của hình nón cũng khai triển được mà không làm thay đổi độ dài.",
            1.7,
        )
        self.narrate(
            "Nhưng có một điểm mới rất quan trọng: khi trải ra thành hình quạt, "
            "góc quanh trục của hình nón không được giữ nguyên.",
            1.8,
        )

    def problem(self):
        self.clear_all()
        self.add_hud("Hai điểm A, B trên vành đáy","01 / 13")

        A,B,S=cone_endpoints()
        self.add(
            cone_wireframe(),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("BÀI TOÁN",[
            ("math","r=3",29,CYAN),
            ("math","h=4",29,CYAN),
            ("math","l=5",29,GOLD),
            ("math","delta=frac(5 pi,6)",28,CYAN),
            ("text","Chỉ đi trên mặt xung quanh.",18,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hình nón có bán kính đáy ba, chiều cao bốn, nên đường sinh bằng năm.",
            1.5,
        )
        self.narrate(
            "Hai điểm A và B nằm trên vành đáy. "
            "Nhìn từ trên xuống, góc nhỏ hơn giữa hai bán kính tới A và B bằng năm pi trên sáu, tức một trăm năm mươi độ.",
            1.9,
        )

    def invalid_chord(self):
        self.clear_all()
        self.add_hud("Đoạn thẳng AB không nằm trên mặt nón","02 / 13")

        A,B,S=cone_endpoints()
        self.add(
            cone_wireframe(),
            direct_chord(),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("NỐI THẲNG TRONG KHÔNG GIAN",[
            ("math","A B=2r sin frac(delta,2)",25,RED),
            ("math","A B=6 sin frac(5 pi,12)",24,RED),
            ("text","Đoạn này nằm trong mặt phẳng đáy.",18,INK),
            ("text","Không phải đường trên mặt xung quanh.",18,GOLD),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu nối thẳng A với B, ta được một dây cung của đường tròn đáy. "
            "Đường này nằm trong mặt phẳng đáy chứ không nằm trên mặt xung quanh của nón.",
            1.8,
        )
        self.narrate(
            "Vì thế ta phải tìm một đường khác thực sự nằm trên mặt nón.",
            1.4,
        )

    def derive_sector(self):
        self.clear_all()
        self.add_hud("Mặt nón trải thành một hình quạt","03 / 13")

        net,pts=sector_net(show_chord=False,show_radii=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("BÁN KÍNH HÌNH QUẠT",[
            ("math","l=sqrt(r^2+h^2)",27,INK),
            ("math","l=sqrt(3^2+4^2)=5",27,GOLD),
            ("text","Bán kính hình quạt chính là đường sinh.",18,CYAN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Khi cắt mặt nón theo một đường sinh rồi trải ra, ta được một hình quạt tròn.",
            1.5,
        )
        self.narrate(
            "Bán kính của hình quạt chính là đường sinh của nón. "
            "Ở đây đường sinh bằng năm.",
            1.5,
        )

    def sector_angle(self):
        self.clear_all()
        self.add_hud("Tính góc của hình quạt","04 / 13")

        net,pts=sector_net(show_chord=False,show_radii=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("ĐỘ DÀI CUNG PHẢI GIỮ NGUYÊN",[
            ("math","l Phi=2 pi r",29,INK),
            ("math","5 Phi=6 pi",29,CYAN),
            ("math","Phi=frac(6 pi,5)",35,GOLD),
            ("text","Tức 216°.",19,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Cung ngoài của hình quạt chính là toàn bộ đường tròn đáy trước khi cắt.",
            1.5,
        )
        self.narrate(
            "Vì thế năm nhân góc Phi phải bằng chu vi sáu pi. "
            "Suy ra Phi bằng sáu pi trên năm, tức hai trăm mười sáu độ.",
            1.8,
        )

    def exact_unroll(self):
        self.clear_all()
        self.add_hud("Mở mặt nón liên tục thành hình quạt","05 / 13")

        s=ValueTracker(RATIO)
        mesh=always_redraw(lambda: unfold_wire_group(s.get_value()))
        path=always_redraw(lambda: unfold_path_group(s.get_value()))
        self.add(mesh,path)

        card=lesson_card("KHAI TRIỂN KHÔNG KÉO GIÃN",[
            ("text","Đỉnh nón giữ nguyên.",18,INK),
            ("text","Các đường sinh vẫn giữ đúng độ dài.",18,CYAN),
            ("text","Các cung cùng độ dài mở dần thành cung phẳng.",17,CYAN),
            ("text","Đường vàng dần trở thành đoạn thẳng.",18,GOLD),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Ta mở mặt nón từ từ. Đỉnh nón được giữ cố định, còn mặt nón mở rộng dần cho tới khi nằm phẳng.",
            s.animate.set_value(1.0),
            min_time=5.2,
            rate_func=smooth,
        )
        self.narrate(
            "Trong suốt quá trình này, độ dài trên mặt không thay đổi. "
            "Đường vàng trên nón cuối cùng trở thành đúng một đoạn thẳng trong hình quạt.",
            1.8,
        )

    def base_angle(self):
        self.clear_all()
        self.add_hud("Góc 150° quanh trục sẽ thành bao nhiêu?","06 / 13")

        dia=base_top_view()
        self.add_fixed_in_frame_mobjects(dia)

        card=lesson_card("TRÊN ĐƯỜNG TRÒN ĐÁY",[
            ("math","delta=frac(5 pi,6)",30,GOLD),
            ("math","s=r delta",29,CYAN),
            ("math","s=3 times frac(5 pi,6)",26,INK),
            ("math","s=frac(5 pi,2)",30,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Xét cung nhỏ từ A tới B trên đường tròn đáy. "
            "Góc ở tâm là năm pi trên sáu.",
            1.5,
        )
        self.narrate(
            "Độ dài cung ấy bằng r nhân delta, tức ba nhân năm pi trên sáu, bằng năm pi trên hai.",
            1.8,
        )

    def angle_conversion(self):
        self.clear_all()
        self.add_hud("Đổi góc trên nón thành góc trên hình quạt","07 / 13")

        net,pts=sector_net(show_chord=False,show_radii=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("CÙNG MỘT ĐỘ DÀI CUNG",[
            ("math","r delta=l alpha",29,INK),
            ("math","alpha=frac(r,l) delta",29,CYAN),
            ("math","alpha=frac(3,5) times frac(5 pi,6)",26,INK),
            ("math","alpha=frac(pi,2)",35,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trên hình quạt, cùng cung A B ấy nằm trên đường tròn bán kính năm. "
            "Gọi góc tương ứng là alpha.",
            1.6,
        )
        self.narrate(
            "Vì độ dài cung được giữ nguyên, r nhân delta bằng l nhân alpha.",
            1.5,
        )
        self.narrate(
            "Do đó alpha bằng r trên l nhân delta. "
            "Thay số, alpha bằng pi trên hai, tức chín mươi độ.",
            1.8,
        )

    def shortest_chord(self):
        self.clear_all()
        self.add_hud("Trên hình quạt, nối thẳng A với B","08 / 13")

        net,pts=sector_net(show_chord=True,show_radii=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("TAM GIÁC CÂN SAB",[
            ("math","S A=S B=5",28,CYAN),
            ("math","widehat(A S B)=frac(pi,2)",28,CYAN),
            ("math","A B=sqrt(5^2+5^2)",28,INK),
            ("math","A B=5 sqrt(2)",35,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Sau khi trải, A và B nằm trên hai bán kính của hình quạt và tạo với đỉnh S một góc chín mươi độ.",
            1.7,
        )
        self.narrate(
            "Đường ngắn nhất trên mặt phẳng là đoạn thẳng A B. "
            "Tam giác S A B vuông cân với hai cạnh góc vuông đều bằng năm.",
            1.8,
        )
        self.narrate(
            "Vì vậy độ dài đường ngắn nhất trên mặt nón là năm căn hai.",
            1.5,
        )

    def compare_apex(self):
        self.clear_all()
        self.add_hud("Đi qua đỉnh nón có ngắn hơn không?","09 / 13")

        A,B,S=cone_endpoints()
        self.add(
            cone_wireframe(),
            cone_geodesic(GOLD,6.0),
            generator_via_apex(),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("SO SÁNH",[
            ("math","A S+S B=10",30,CYAN),
            ("math","L_(min)=5 sqrt(2)",32,GOLD),
            ("math","5 sqrt(2)<10",30,GREEN),
            ("text","Đường qua đỉnh không tối ưu.",18,INK),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Một phương án khác là đi từ A lên đỉnh S rồi từ S xuống B. "
            "Đường này dài năm cộng năm, tức mười.",
            1.7,
        )
        self.narrate(
            "Năm căn hai nhỏ hơn mười, nên đường tối ưu không đi qua đỉnh nón.",
            1.5,
        )

    def ant_walk(self):
        self.clear_all()
        self.add_hud("Cho kiến đi trên đường tối ưu","10 / 13")

        A,B,S=cone_endpoints()
        path=cone_geodesic(GOLD,6.0)
        ant=Dot3D(A,radius=0.085,color=GREEN)

        self.add(
            cone_wireframe(),
            path,
            ant,
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("ĐƯỜNG TRÊN MẶT NÓN",[
            ("math","delta=frac(5 pi,6)",27,CYAN),
            ("math","alpha=frac(pi,2)",27,CYAN),
            ("math","L_(min)=5 sqrt(2)",33,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Khi gấp hình quạt trở lại thành nón, đoạn thẳng A B trở thành một đường cong trên mặt nón.",
            MoveAlongPath(ant,cone_geodesic(GOLD,1.0)),
            min_time=4.0,
            rate_func=linear,
        )
        self.narrate(
            "Đường cong này không phải cung tròn. "
            "Nó là ảnh của đoạn thẳng trên bản khai triển và có độ dài đúng năm căn hai.",
            1.8,
        )

    def general_rim_formula(self):
        self.clear_all()
        self.add_hud("Công thức cho hai điểm bất kỳ trên vành đáy","11 / 13")

        net,pts=sector_net(show_chord=True,show_radii=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("HÌNH NÓN BÁN KÍNH r, ĐƯỜNG SINH l",[
            ("math","alpha=frac(r,l) delta",27,CYAN),
            ("math","L=2l sin frac(alpha,2)",27,GOLD),
            ("math","L=2l sin frac(r delta,2l)",25,GREEN),
            ("text","Xét bản khai triển tương ứng với cung đã chọn.",17,INK),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Với hai điểm bất kỳ trên vành đáy, nếu góc quanh trục là delta thì góc trên hình quạt bằng r trên l nhân delta.",
            1.8,
        )
        self.narrate(
            "Hai điểm đều cách đỉnh hình quạt một đoạn l. "
            "Độ dài dây cung vì thế bằng hai l nhân sin của một nửa góc alpha.",
            1.8,
        )
        self.narrate(
            "Suy ra công thức L bằng hai l nhân sin của r delta chia hai l.",
            1.6,
        )

    def general_two_radii(self):
        self.clear_all()
        self.add_hud("Hai điểm không nhất thiết nằm trên vành đáy","12 / 13")

        net,pts=sector_net(show_chord=False,show_radii=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("NẾU CÁCH ĐỈNH S CÁC ĐOẠN ρ₁, ρ₂",[
            ("math","alpha=frac(r,l) delta",26,CYAN),
            ("math","L^2=rho_1^2+rho_2^2",25,INK),
            ("math","-2 rho_1 rho_2 cos alpha",24,INK),
            ("text","Chỉ là định lý cos trên bản khai triển.",17,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu hai điểm không nằm trên vành đáy mà nằm ở hai vị trí bất kỳ trên mặt nón, "
            "ta gọi khoảng cách theo đường sinh từ đỉnh tới chúng là rho một và rho hai.",
            1.9,
        )
        self.narrate(
            "Sau khi trải, ta chỉ có một tam giác phẳng với hai cạnh rho một, rho hai và góc xen giữa alpha. "
            "Định lý cos cho ngay bình phương độ dài.",
            1.8,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài hình nón","13 / 13")

        A,B,S=cone_endpoints()
        self.add(
            cone_wireframe(),
            cone_geodesic(GOLD,6.0),
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("BỐN Ý CẦN NHỚ",[
            ("text","1. Mặt nón trải thành hình quạt.",18,INK),
            ("text","2. Bán kính quạt là đường sinh l.",18,INK),
            ("math","Phi=frac(2 pi r,l)",27,CYAN),
            ("math","alpha=frac(r,l) delta",27,CYAN),
            ("math","L=2l sin frac(alpha,2)",28,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Điểm mới quan trọng nhất của hình nón là sự đổi góc. "
            "Góc quanh trục delta không giữ nguyên khi trải.",
            1.6,
        )
        self.narrate(
            "Nó được nhân với tỉ số r trên l. "
            "Sau bước đổi góc ấy, bài toán lại trở về hình học phẳng rất quen thuộc.",
            1.7,
        )
        self.narrate(
            "Trong ví dụ này, một trăm năm mươi độ trên hình nón trở thành chín mươi độ trên hình quạt, "
            "và đường ngắn nhất có độ dài năm căn hai.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.problem()
        self.invalid_chord()
        self.derive_sector()
        self.sector_angle()
        self.exact_unroll()
        self.base_angle()
        self.angle_conversion()
        self.shortest_chord()
        self.compare_apex()
        self.ant_walk()
        self.general_rim_formula()
        self.general_two_radii()
        self.summary()


class Smoke13(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.95)

        s=ValueTracker(RATIO)
        mesh=always_redraw(lambda: unfold_wire_group(s.get_value()))
        path=always_redraw(lambda: unfold_path_group(s.get_value()))
        self.add(mesh,path)
        self.play(
            s.animate.set_value(1.0),
            run_time=2.4,
            rate_func=smooth,
        )
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)

    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_13_master_smoke"
    config.disable_caching=True

    scene=Smoke13()
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
    config.output_file="trai_phang_13_hinh_non_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang13Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_13.wav"
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

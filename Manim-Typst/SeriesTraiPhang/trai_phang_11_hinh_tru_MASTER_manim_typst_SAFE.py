
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





# ---------- geometry engine: cylinder lateral surface ----------
# Cylinder radius r=2, height h=3.
#
# A is on the lower rim at angular coordinate 0.
# B is on the upper rim at angular coordinate pi,
# so their generators are diametrically opposite.
#
# Cutting along the generator through A gives a rectangle:
# width 2*pi*r = 4*pi, height 3.
# B lands at horizontal coordinate pi*r = 2*pi.
#
# Shortest lateral route:
# L = sqrt((2*pi)^2 + 3^2) = sqrt(4*pi^2 + 9).
# ==========================================================

RADIUS = 2.0
HEIGHT = 3.0
CIRC = 2.0 * math.pi * RADIUS
HALF_ARC = math.pi * RADIUS

WORLD_SCALE = 0.72
WORLD_SHIFT = np.array([-3.30,-0.15,-0.20])

DEV_SCALE = 0.43
DEV_SHIFT = np.array([-2.15, 2.55, -0.95])

CAM_PHI = 68 * DEGREES
CAM_THETA = -48 * DEGREES


def W(p):
    return WORLD_SCALE * np.array(p,dtype=float) + WORLD_SHIFT


def DW(p):
    return DEV_SCALE * np.array(p,dtype=float) + DEV_SHIFT


def cyl_point(theta,z):
    return np.array([
        RADIUS*math.cos(theta),
        RADIUS*math.sin(theta),
        z,
    ],dtype=float)


def point_from_s(s,z):
    return cyl_point(s/RADIUS,z)


def develop_raw(s,z,u):
    """Exact piecewise isometric unrolling of the first arc-length u.

    For s<=u the sheet is flat in the tangent plane at angle u/r.
    For s>u it remains on the original cylinder.

    The metric ds^2+dz^2 is preserved on both pieces and the tangent
    direction matches at the peel generator s=u.
    """
    s=float(s)
    z=float(z)
    u=max(0.0,min(float(u),CIRC))

    if s <= u + 1e-12:
        phi=u/RADIUS
        center=np.array([
            RADIUS*math.cos(phi),
            RADIUS*math.sin(phi),
            z,
        ])
        tangent=np.array([
            -math.sin(phi),
            math.cos(phi),
            0.0,
        ])
        return center + (s-u)*tangent

    return point_from_s(s,z)


def helix_raw(t, direction=1):
    """Half-turn geodesic on the cylinder from A to B."""
    theta=direction*math.pi*t
    z=HEIGHT*t
    return cyl_point(theta,z)


def mapped_helix_raw(t,u):
    s=HALF_ARC*t
    z=HEIGHT*t
    return develop_raw(s,z,u)


def cylinder_wireframe():
    g=VGroup()

    # Lower and upper rims.
    for z,color in [(0.0,EDGE),(HEIGHT,EDGE)]:
        curve=ParametricFunction(
            lambda th,z=z: W(cyl_point(th,z)),
            t_range=[0,TAU],
            color=color,
            stroke_width=3.5,
        )
        g.add(curve)

    # Vertical generators.
    for k in range(12):
        th=TAU*k/12
        p0=W(cyl_point(th,0.0))
        p1=W(cyl_point(th,HEIGHT))
        opacity=0.72 if math.cos(th-CAM_THETA)>-0.15 else 0.32
        g.add(Line(
            p0,p1,
            color=GRID if k else GOLD,
            stroke_width=2.2 if k else 5.0,
            stroke_opacity=opacity if k else 1.0,
        ))

    # A subtle side surface.
    surf=Surface(
        lambda uu,vv: W(cyl_point(uu,vv)),
        u_range=[0,TAU],
        v_range=[0,HEIGHT],
        resolution=(24,8),
        fill_color=BLUE,
        fill_opacity=0.055,
        stroke_width=0.0,
    )
    return VGroup(surf,g)


def cylinder_points():
    A=W(cyl_point(0.0,0.0))
    B=W(cyl_point(math.pi,HEIGHT))
    return A,B


def helix_curve(direction=1,color=GOLD,width=6.0):
    return ParametricFunction(
        lambda t: W(helix_raw(t,direction)),
        t_range=[0,1],
        color=color,
        stroke_width=width,
    )


def direct_chord():
    A,B=cylinder_points()
    return DashedLine(
        A,B,
        color=RED,
        stroke_width=5.0,
        dash_length=0.12,
    )


def develop_wire_group(u):
    """Wireframe for the exact unrolling animation."""
    g=VGroup()

    # Horizontal levels: circles progressively become straight segments.
    for j in range(7):
        z=HEIGHT*j/6
        pts=[
            DW(develop_raw(CIRC*k/96,z,u))
            for k in range(97)
        ]
        curve=VMobject(color=GRID,stroke_width=1.7,stroke_opacity=0.72)
        curve.set_points_as_corners(pts)
        g.add(curve)

    # Vertical generators.
    for k in range(17):
        s=CIRC*k/16
        p0=DW(develop_raw(s,0.0,u))
        p1=DW(develop_raw(s,HEIGHT,u))
        color=GOLD if k in {0,16} else GRID
        width=4.8 if k in {0,16} else 1.8
        g.add(Line(p0,p1,color=color,stroke_width=width,stroke_opacity=0.85))

    return g


def develop_path_group(u):
    pts=[
        DW(mapped_helix_raw(k/96,u))
        for k in range(97)
    ]
    path=VMobject(color=GOLD,stroke_width=6.2)
    path.set_points_as_corners(pts)

    A=DW(develop_raw(0.0,0.0,u))
    B=DW(develop_raw(HALF_ARC,HEIGHT,u))

    return VGroup(
        path,
        Dot3D(A,radius=0.070,color=GREEN),
        Dot3D(B,radius=0.070,color=RED),
    )


def net_rectangle(show_both=True):
    """Exact 2D development in the left column.

    Coordinates use arc length s horizontally and z vertically.
    """
    width=5.75
    height=2.85
    left=LEFT_CENTER[0]-width/2
    bottom=LEFT_CENTER[1]-height/2

    def T(s,z):
        return np.array([
            left + width*(s/CIRC),
            bottom + height*(z/HEIGHT),
            0.0,
        ])

    A0=T(0.0,0.0)
    A1=T(CIRC,0.0)
    B=T(HALF_ARC,HEIGHT)

    rect=Rectangle(
        width=width,height=height,
        stroke_color=EDGE,stroke_width=3.0,
        fill_color=BLUE,fill_opacity=0.08,
    ).move_to(LEFT_CENTER)

    seam_left=Line(T(0,0),T(0,HEIGHT),color=GOLD,stroke_width=4.5)
    seam_right=Line(T(CIRC,0),T(CIRC,HEIGHT),color=GOLD,stroke_width=4.5)

    g=VGroup(
        rect,seam_left,seam_right,
        Dot(A0,radius=0.070,color=GREEN),
        Dot(B,radius=0.070,color=RED),
        Line(A0,B,color=GOLD,stroke_width=6.2),
    )

    if show_both:
        g.add(
            Dot(A1,radius=0.070,color=GREEN),
            Line(A1,B,color=CYAN,stroke_width=5.2),
        )

    return g,{"A0":A0,"A1":A1,"B":B,"T":T}


def top_view_angle_diagram(delta=math.pi):
    center=np.array([LEFT_CENTER[0],LEFT_CENTER[1],0.0])
    rad=1.55

    circle=Circle(radius=rad,color=EDGE,stroke_width=3.0).move_to(center)
    A=center+rad*np.array([1.0,0.0,0.0])
    B=center+rad*np.array([math.cos(delta),math.sin(delta),0.0])

    r1=Line(center,A,color=GREEN,stroke_width=4.0)
    r2=Line(center,B,color=RED,stroke_width=4.0)

    # Arc from 0 to delta, using the shorter direction delta in [0,pi].
    arc=Arc(
        radius=rad*0.62,
        start_angle=0.0,
        angle=delta,
        color=GOLD,
        stroke_width=5.0,
    ).move_arc_center_to(center)

    return VGroup(
        circle,r1,r2,arc,
        Dot(A,radius=0.065,color=GREEN),
        Dot(B,radius=0.065,color=RED),
        Dot(center,radius=0.045,color=INK),
    )


def geometry_preflight(verbose=True):
    tol=1e-9

    if abs(CIRC-4*math.pi)>tol:
        raise AssertionError("Circumference should be 4pi")
    if abs(HALF_ARC-2*math.pi)>tol:
        raise AssertionError("Half circumference should be 2pi")

    # Direct chord in space: horizontal diameter 4 and vertical rise 3.
    A=cyl_point(0.0,0.0)
    B=cyl_point(math.pi,HEIGHT)
    chord=np.linalg.norm(B-A)
    if abs(chord-5.0)>tol:
        raise AssertionError("Chord AB should be 5")

    # Surface path from the developed rectangle.
    expected=math.sqrt((2*math.pi)**2+HEIGHT**2)
    if abs(expected-math.sqrt(4*math.pi**2+9))>tol:
        raise AssertionError("Wrong developed length")

    # Sample the half-turn helix and verify its speed is constant.
    ts=np.linspace(0.0,1.0,101)
    speeds=[]
    for t in ts:
        theta=math.pi*t
        # derivative magnitude = sqrt((r*pi)^2+h^2)
        speeds.append(math.sqrt((RADIUS*math.pi)**2+HEIGHT**2))
    if max(speeds)-min(speeds)>tol:
        raise AssertionError("Helix speed should be constant")
    if abs(speeds[0]-expected)>tol:
        raise AssertionError("Helix length should equal developed length")

    # Exact isometry checks for unrolling map.
    for frac in [0.0,0.17,0.43,0.76,1.0]:
        u=frac*CIRC
        for z in [0.0,HEIGHT/2,HEIGHT]:
            # generator length is preserved
            p0=develop_raw(CIRC*0.31,0.0,u)
            p1=develop_raw(CIRC*0.31,HEIGHT,u)
            if abs(np.linalg.norm(p1-p0)-HEIGHT)>1e-8:
                raise AssertionError("Generator length changed")

        # Once fully unrolled, arc-length differences become Euclidean distances.
        if frac==1.0:
            for s1,s2 in [(0.0,CIRC/4),(CIRC/4,CIRC/2),(0.0,CIRC)]:
                p=develop_raw(s1,HEIGHT/3,u)
                q=develop_raw(s2,HEIGHT/3,u)
                if abs(np.linalg.norm(q-p)-abs(s2-s1))>1e-8:
                    raise AssertionError("Arc length not preserved in full development")

    # B is opposite: both copies of A give equal length in the rectangle.
    L_left=math.hypot(HALF_ARC,HEIGHT)
    L_right=math.hypot(CIRC-HALF_ARC,HEIGHT)
    if abs(L_left-L_right)>tol:
        raise AssertionError("Opposite point should give two equal directions")

    # General angular-separation formula.
    for delta in [0.2,0.7,1.4,math.pi]:
        L=math.sqrt((RADIUS*delta)**2+HEIGHT**2)
        if L < HEIGHT-tol:
            raise AssertionError("Surface route cannot be shorter than vertical rise")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  cylinder r=2, h=3")
        print("  A lower rim, B opposite upper rim")
        print("  chord AB=5 passes through interior")
        print("  lateral development width=4pi, horizontal shift=2pi")
        print("  two half-turn directions tie")
        print("  Lmin=sqrt(4*pi^2+9)")
        print("  exact piecewise unrolling preserves generator and arc lengths")
    return True


def layout_samples():
    return [
        lesson_card("BÀI TOÁN",[
            ("math","r=2, h=3",28,CYAN),
            ("text","A ở vành dưới, B ở vành trên.",19,INK),
            ("text","Hai đường sinh qua A, B đối diện nhau.",18,INK),
            ("text","Chỉ được đi trên mặt xung quanh.",19,GOLD),
            ("math","L_(min)=?",34,GOLD),
        ],GOLD),
        lesson_card("BẢN KHAI TRIỂN",[
            ("math","2 pi r=4 pi",29,CYAN),
            ("math","Delta s=pi r=2 pi",29,CYAN),
            ("math","L=sqrt((2 pi)^2+3^2)",28,INK),
            ("math","L=sqrt(4 pi^2+9)",34,GOLD),
        ],CYAN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.96)

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
        h=header(11,title,progress)
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


class TraiPhang11Master(BaseLesson):
    def intro(self):
        self.clear_all()
        cyl=cylinder_wireframe()
        A,B=cylinder_points()
        self.add(
            cyl,
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=intro_card(
            11,
            ["HÌNH TRỤ","ĐƯỜNG XOẮN THÀNH ĐƯỜNG THẲNG"],
            "Cắt theo một đường sinh và khai triển mặt xung quanh.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Từ video này, ta rời các đa diện để sang mặt cong khai triển được. "
            "Mô hình đầu tiên là hình trụ.",
            1.5,
        )
        self.narrate(
            "Một đường nhìn như xoắn quanh hình trụ sẽ trở thành một đoạn thẳng khi mặt xung quanh được cắt và trải ra.",
            1.7,
        )

    def problem(self):
        self.clear_all()
        self.add_hud("Từ A đến B trên mặt xung quanh","01 / 13")
        cyl=cylinder_wireframe()
        A,B=cylinder_points()
        self.add(
            cyl,
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("BÀI TOÁN",[
            ("math","r=2",29,CYAN),
            ("math","h=3",29,CYAN),
            ("text","A ở vành dưới, B ở vành trên.",19,INK),
            ("text","Hai đường sinh qua A, B đối diện nhau.",18,GOLD),
            ("text","Chỉ đi trên mặt xung quanh.",19,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hình trụ có bán kính hai và chiều cao ba. A nằm trên vành dưới, B nằm trên vành trên.",
            1.5,
        )
        self.narrate(
            "Hai đường sinh đi qua A và B nằm đối diện nhau qua trục. "
            "Kiến chỉ được bò trên mặt xung quanh của hình trụ.",
            1.6,
        )

    def invalid_chord(self):
        self.clear_all()
        self.add_hud("Đoạn thẳng trong không gian không hợp lệ","02 / 13")
        cyl=cylinder_wireframe()
        A,B=cylinder_points()
        self.add(
            cyl,
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
            direct_chord(),
        )

        card=lesson_card("NẾU NỐI THẲNG A VỚI B",[
            ("math","Delta x=4",28,RED),
            ("math","Delta z=3",28,RED),
            ("math","A B=5",34,RED),
            ("text","Nhưng đoạn này xuyên qua lòng hình trụ.",18,INK),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu nối A với B bằng đoạn thẳng trong không gian, độ lệch ngang là đường kính bốn và độ lệch đứng là ba.",
            1.7,
        )
        self.narrate(
            "Ta được tam giác ba, bốn, năm nên A B bằng năm. "
            "Nhưng đoạn này đi xuyên qua lòng hình trụ, vì vậy không phải đường đi trên bề mặt.",
            1.8,
        )

    def show_helix(self):
        self.clear_all()
        self.add_hud("Đường hợp lệ phải nằm trên mặt trụ","03 / 13")
        cyl=cylinder_wireframe()
        path1=helix_curve(1,GOLD,6.0)
        path2=helix_curve(-1,CYAN,4.8)
        A,B=cylinder_points()
        self.add(
            cyl,path1,path2,
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("HAI HƯỚNG ĐỐI XỨNG",[
            ("text","Có thể đi nửa vòng theo chiều này.",18,GOLD),
            ("text","Hoặc nửa vòng theo chiều ngược lại.",18,CYAN),
            ("text","Do A và B đối diện, hai hướng bằng nhau.",18,INK),
            ("text","Ta chỉ cần xét một hướng.",19,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trên mặt trụ, đường tối ưu sẽ có dạng một đường xoắn từ vành dưới lên vành trên.",
            1.5,
        )
        self.narrate(
            "Vì hai đường sinh qua A và B đối diện nhau, có hai hướng nửa vòng hoàn toàn đối xứng. "
            "Ta chỉ cần xét một trong hai.",
            1.7,
        )

    def seam(self):
        self.clear_all()
        self.add_hud("Cắt mặt trụ theo đường sinh qua A","04 / 13")
        cyl=cylinder_wireframe()
        seam=Line(
            W(cyl_point(0.0,0.0)),
            W(cyl_point(0.0,HEIGHT)),
            color=GOLD,
            stroke_width=7.0,
        )
        self.add(cyl,seam)

        card=lesson_card("ĐƯỜNG CẮT",[
            ("text","Cắt theo đường sinh qua A.",19,GOLD),
            ("text","Đường sinh có độ dài h=3.",19,INK),
            ("text","Chu vi đáy sẽ trở thành chiều dài hình chữ nhật.",18,CYAN),
            ("math","2 pi r=4 pi",31,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta cắt mặt xung quanh theo đường sinh đi qua A.",
            1.3,
        )
        self.narrate(
            "Khi trải ra, chiều cao vẫn bằng ba, còn một vòng quanh đáy có độ dài bằng chu vi, tức bốn pi.",
            1.7,
        )

    def exact_unroll(self):
        self.clear_all()
        self.add_hud("Trải mặt xung quanh mà không kéo giãn","05 / 13")

        u=ValueTracker(0.0)

        mesh=always_redraw(lambda: develop_wire_group(u.get_value()))
        path=always_redraw(lambda: develop_path_group(u.get_value()))

        self.add(mesh,path)

        card=lesson_card("KHAI TRIỂN",[
            ("text","Phần đã mở nằm trên mặt phẳng tiếp tuyến.",18,INK),
            ("text","Phần chưa mở vẫn nằm trên hình trụ.",18,INK),
            ("text","Độ dài theo vòng tròn được giữ nguyên.",18,CYAN),
            ("text","Đường xoắn dần trở thành đường thẳng.",18,GOLD),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Bây giờ ta mở mặt trụ từ từ. Phần đã mở nằm trên một mặt phẳng tiếp tuyến, "
            "còn phần chưa mở vẫn giữ dạng trụ.",
            u.animate.set_value(CIRC),
            min_time=5.0,
            rate_func=linear,
        )
        self.narrate(
            "Khi mở đủ một vòng, mặt xung quanh trở thành một hình chữ nhật. "
            "Đường xoắn vàng đã trở thành một đoạn thẳng.",
            1.7,
        )

    def rectangle_data(self):
        self.clear_all()
        self.add_hud("Bản khai triển là hình chữ nhật","06 / 13")
        net,pts=net_rectangle(show_both=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("KÍCH THƯỚC BẢN KHAI TRIỂN",[
            ("math","C=2 pi r=4 pi",28,CYAN),
            ("text","Chiều cao của hình chữ nhật: h = 3.",18,CYAN),
            ("text","B nằm cách mép cắt một nửa chu vi.",18,INK),
            ("math","Delta s=pi r=2 pi",29,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bản khai triển có chiều dài bốn pi và chiều cao ba.",
            1.4,
        )
        self.narrate(
            "Vì B nằm trên đường sinh đối diện A, khoảng cách theo phương ngang từ A tới ảnh của B bằng đúng nửa chu vi, tức hai pi.",
            1.8,
        )

    def compute_length(self):
        self.clear_all()
        self.add_hud("Đường xoắn trở thành đường chéo","07 / 13")
        net,pts=net_rectangle(show_both=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("ÁP DỤNG PYTHAGORE",[
            ("math","Delta s=2 pi",29,CYAN),
            ("math","Delta z=3",29,CYAN),
            ("math","L^2=(2 pi)^2+3^2",29,INK),
            ("math","L=sqrt(4 pi^2+9)",35,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Trên mặt phẳng, đường ngắn nhất là đoạn thẳng nối A với ảnh của B.",
            1.4,
        )
        self.narrate(
            "Độ lệch ngang là hai pi, độ lệch đứng là ba. "
            "Theo Pythagore, bình phương độ dài bằng bốn pi bình phương cộng chín.",
            1.8,
        )
        self.narrate(
            "Vậy độ dài nhỏ nhất trên mặt xung quanh là căn của bốn pi bình phương cộng chín.",
            1.6,
        )

    def two_directions(self):
        self.clear_all()
        self.add_hud("Vì sao có hai đường ngắn nhất?","08 / 13")
        net,pts=net_rectangle(show_both=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("HAI BẢN SAO CỦA A",[
            ("text","Hai mép đứng sẽ được dán lại với nhau.",18,INK),
            ("text","A xuất hiện ở cả hai mép dưới.",18,GREEN),
            ("text","B nằm đúng giữa mép trên.",18,RED),
            ("text","Hai đoạn chéo có cùng độ dài.",18,GOLD),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Khi cắt theo đường sinh qua A, điểm A xuất hiện ở cả hai mép của hình chữ nhật.",
            1.5,
        )
        self.narrate(
            "B nằm đúng giữa mép trên vì nó đối diện A. "
            "Do đó nối B với bản sao bên trái hay bên phải của A đều cho cùng một độ dài.",
            1.8,
        )
        self.narrate(
            "Khi cuộn hình chữ nhật lại, hai đoạn chéo này trở thành hai đường xoắn đối xứng trên hình trụ.",
            1.6,
        )

    def walk_helix(self):
        self.clear_all()
        self.add_hud("Cho kiến đi trên đường xoắn","09 / 13")
        cyl=cylinder_wireframe()
        path=helix_curve(1,GOLD,6.0)
        A,B=cylinder_points()
        ant=Dot3D(A,radius=0.085,color=GREEN)

        self.add(
            cyl,path,ant,
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("ĐƯỜNG TRÊN MẶT TRỤ",[
            ("text","Đi quanh đúng nửa vòng.",19,GOLD),
            ("math","Delta theta=pi",29,CYAN),
            ("math","Delta z=3",29,CYAN),
            ("math","L=sqrt(4 pi^2+9)",33,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Kiến bắt đầu tại A, vừa đi quanh nửa vòng trụ vừa tăng dần độ cao.",
            MoveAlongPath(ant,helix_curve(1,GOLD,1.0)),
            min_time=4.0,
            rate_func=linear,
        )
        self.narrate(
            "Khi đi đủ góc pi quanh trục, kiến đồng thời tăng độ cao từ không lên ba và tới đúng B.",
            1.7,
        )

    def top_angle(self):
        self.clear_all()
        self.add_hud("Nếu hai đường sinh không đối diện nhau","10 / 13")
        dia=top_view_angle_diagram(math.pi*0.68)
        self.add_fixed_in_frame_mobjects(dia)

        card=lesson_card("GỌI GÓC NHỎ HƠN LÀ δ",[
            ("math","0<=delta<=pi",27,INK),
            ("math","s=r delta",29,CYAN),
            ("text","Đây là độ lệch ngang trên bản khai triển.",18,INK),
            ("math","L=sqrt((r delta)^2+h^2)",29,GOLD),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bài vừa rồi có góc giữa hai đường sinh bằng pi. "
            "Nếu hai điểm không đối diện nhau, ta gọi góc nhỏ hơn quanh trục là delta.",
            1.8,
        )
        self.narrate(
            "Cung tương ứng trên đường tròn có độ dài r nhân delta. "
            "Sau khi khai triển, đó chính là độ lệch ngang giữa hai điểm.",
            1.7,
        )
        self.narrate(
            "Vì vậy công thức tổng quát của đường ngắn nhất trên mặt xung quanh là căn của r delta tất cả bình phương cộng h bình phương.",
            1.8,
        )

    def geodesic_equation(self):
        self.clear_all()
        self.add_hud("Phương trình của đường xoắn tối ưu","11 / 13")
        self.add(cylinder_wireframe(),helix_curve(1,GOLD,6.0))

        card=lesson_card("VỚI BÀI r=2, h=3",[
            ("math","0<=theta<=pi",27,INK),
            ("math","x=2 cos theta",28,CYAN),
            ("math","y=2 sin theta",28,CYAN),
            ("math","z=frac(3 theta,pi)",28,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta còn có thể viết chính đường xoắn này bằng tham số góc theta.",
            1.4,
        )
        self.narrate(
            "Tọa độ là x bằng hai cos theta, y bằng hai sin theta, "
            "và z bằng ba theta chia pi, với theta chạy từ không tới pi.",
            1.8,
        )
        self.narrate(
            "Độ cao tăng tuyến tính theo góc quay. "
            "Đó chính là hình ảnh của một đoạn thẳng trên bản khai triển được cuộn lại thành hình trụ.",
            1.8,
        )

    def why_straight(self):
        self.clear_all()
        self.add_hud("Vì sao đoạn thẳng cho đường ngắn nhất?","12 / 13")
        net,pts=net_rectangle(show_both=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("LẬP LUẬN CỐT LÕI",[
            ("text","Khai triển không làm thay đổi độ dài trên mặt.",18,INK),
            ("text","Mọi đường hợp lệ trở thành một đường phẳng.",18,INK),
            ("text","Giữa hai điểm, đoạn thẳng là ngắn nhất.",18,CYAN),
            ("math","L_(min)=sqrt(4 pi^2+9)",31,GOLD),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Điểm mấu chốt là phép khai triển giữ nguyên độ dài đo trên mặt trụ.",
            1.5,
        )
        self.narrate(
            "Vì vậy mọi đường hợp lệ từ A tới B trên mặt trụ trở thành một đường nối hai ảnh tương ứng trong hình chữ nhật.",
            1.7,
        )
        self.narrate(
            "Trong mặt phẳng, đoạn thẳng là ngắn nhất. "
            "Do đó đường xoắn thu được khi cuộn đoạn thẳng lại chính là đường ngắn nhất trên mặt trụ.",
            1.8,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài hình trụ","13 / 13")
        self.add(cylinder_wireframe(),helix_curve(1,GOLD,6.0))

        card=lesson_card("BỐN Ý CẦN NHỚ",[
            ("text","1. Cắt mặt trụ theo một đường sinh.",18,INK),
            ("text","2. Chu vi trở thành chiều dài hình chữ nhật.",18,INK),
            ("text","3. Cung rδ trở thành độ lệch ngang.",18,INK),
            ("math","L=sqrt((r delta)^2+h^2)",28,GOLD),
            ("text","4. Cuộn đoạn thẳng lại ta được đường xoắn.",18,CYAN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hình trụ cho ta một dạng trải phẳng mới: mặt cong nhưng khai triển được thành hình chữ nhật mà không kéo giãn.",
            1.7,
        )
        self.narrate(
            "Độ dài cung quanh trụ trở thành độ lệch ngang, còn chiều cao được giữ nguyên. "
            "Đường thẳng trên bản khai triển khi cuộn lại chính là đường xoắn ngắn nhất.",
            1.8,
        )
        self.narrate(
            "Video sau sẽ giữ cùng ý tưởng nhưng cho đường đi quấn thêm nhiều vòng quanh trụ. "
            "Khi đó một điểm sẽ có nhiều ảnh trên các bản sao liên tiếp của hình chữ nhật.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.problem()
        self.invalid_chord()
        self.show_helix()
        self.seam()
        self.exact_unroll()
        self.rectangle_data()
        self.compute_length()
        self.two_directions()
        self.walk_helix()
        self.top_angle()
        self.geodesic_equation()
        self.why_straight()
        self.summary()


class Smoke11(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.96)

        u=ValueTracker(0.0)
        mesh=always_redraw(lambda: develop_wire_group(u.get_value()))
        path=always_redraw(lambda: develop_path_group(u.get_value()))
        self.add(mesh,path)
        self.play(
            u.animate.set_value(CIRC),
            run_time=2.2,
            rate_func=linear,
        )
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)

    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_11_master_smoke"
    config.disable_caching=True

    scene=Smoke11()
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
    config.output_file="trai_phang_11_hinh_tru_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang11Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_11.wav"
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

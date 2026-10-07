
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






# ---------- geometry engine: cylinder with winding number ----------
# Cylinder radius r=2, height h=3.
#
# A is on the lower rim and B is directly above A on the upper rim
# (same generator). A path is required to wind exactly k full turns
# before reaching B.
#
# Universal-cover development:
#   circumference C = 2*pi*r = 4*pi
#   B_k is the kth copy of B at horizontal coordinate k*C
#   L_k = sqrt((k*C)^2 + h^2)
#
# For signed k:
#   k>0 and k<0 are opposite winding directions.
#   L_k depends only on |k| when A and B lie on the same generator.
# ==========================================================

RADIUS = 2.0
HEIGHT = 3.0
CIRC = 2.0 * math.pi * RADIUS

WORLD_SCALE = 0.72
WORLD_SHIFT = np.array([-3.30,-0.15,-0.20])

CAM_PHI = 68 * DEGREES
CAM_THETA = -48 * DEGREES


def W(p):
    return WORLD_SCALE * np.array(p,dtype=float) + WORLD_SHIFT


def cyl_point(theta,z):
    return np.array([
        RADIUS*math.cos(theta),
        RADIUS*math.sin(theta),
        z,
    ],dtype=float)


def helix_raw(t,k,delta=0.0):
    theta=(delta + TAU*k)*t
    z=HEIGHT*t
    return cyl_point(theta,z)


def helix_curve(k,delta=0.0,color=GOLD,width=6.0):
    return ParametricFunction(
        lambda t: W(helix_raw(t,k,delta)),
        t_range=[0,1],
        color=color,
        stroke_width=width,
    )


def cylinder_wireframe():
    g=VGroup()

    for z in [0.0,HEIGHT]:
        g.add(ParametricFunction(
            lambda th,z=z: W(cyl_point(th,z)),
            t_range=[0,TAU],
            color=EDGE,
            stroke_width=3.5,
        ))

    for j in range(16):
        th=TAU*j/16
        p0=W(cyl_point(th,0.0))
        p1=W(cyl_point(th,HEIGHT))
        color=GOLD if j==0 else GRID
        width=4.8 if j==0 else 1.9
        opacity=1.0 if j==0 else 0.66
        g.add(Line(
            p0,p1,
            color=color,
            stroke_width=width,
            stroke_opacity=opacity,
        ))

    surf=Surface(
        lambda u,v: W(cyl_point(u,v)),
        u_range=[0,TAU],
        v_range=[0,HEIGHT],
        resolution=(24,8),
        fill_color=BLUE,
        fill_opacity=0.055,
        stroke_width=0.0,
    )
    return VGroup(surf,g)


def cylinder_endpoints():
    A=W(cyl_point(0.0,0.0))
    B=W(cyl_point(0.0,HEIGHT))
    return A,B


def strip_mapper(x,z,xmin,xmax,width=5.85,height=3.15):
    left=LEFT_CENTER[0]-width/2
    bottom=LEFT_CENTER[1]-height/2
    return np.array([
        left + width*(x-xmin)/(xmax-xmin),
        bottom + height*z/HEIGHT,
        0.0,
    ])


def universal_strip(kmin=-2,kmax=2,highlight_k=None,delta=0.0,show_lines=False):
    """Several adjacent rectangle copies of the cylinder development."""
    xmin=kmin*CIRC
    xmax=kmax*CIRC

    g=VGroup()

    # Four/five rectangle copies.
    for m in range(kmin,kmax):
        x0=m*CIRC
        x1=(m+1)*CIRC

        p00=strip_mapper(x0,0,xmin,xmax)
        p10=strip_mapper(x1,0,xmin,xmax)
        p11=strip_mapper(x1,HEIGHT,xmin,xmax)
        p01=strip_mapper(x0,HEIGHT,xmin,xmax)

        fill=BLUE if m%2==0 else PANEL_2
        g.add(Polygon(
            p00,p10,p11,p01,
            fill_color=fill,
            fill_opacity=0.10,
            stroke_color=GRID,
            stroke_width=2.0,
        ))

    # Seams at multiples of circumference.
    for m in range(kmin,kmax+1):
        x=m*CIRC
        g.add(Line(
            strip_mapper(x,0,xmin,xmax),
            strip_mapper(x,HEIGHT,xmin,xmax),
            color=GRID if m!=0 else GOLD,
            stroke_width=2.0 if m!=0 else 4.6,
        ))

    A=strip_mapper(0.0,0.0,xmin,xmax)
    g.add(Dot(A,radius=0.072,color=GREEN))

    # Copies of B. Physical B is on same generator, so B_m at x=m*CIRC.
    for m in range(kmin,kmax+1):
        x=m*CIRC
        Bm=strip_mapper(x,HEIGHT,xmin,xmax)
        color=RED if m==highlight_k else MUTED
        radius=0.072 if m==highlight_k else 0.050
        g.add(Dot(Bm,radius=radius,color=color))

        if show_lines:
            line_color=GOLD if m==highlight_k else DIM
            line_width=6.0 if m==highlight_k else 2.1
            line_opacity=1.0 if m==highlight_k else 0.45
            g.add(Line(
                A,Bm,
                color=line_color,
                stroke_width=line_width,
                stroke_opacity=line_opacity,
            ))

    return g, {
        "A":A,
        "xmin":xmin,
        "xmax":xmax,
        "T":lambda x,z: strip_mapper(x,z,xmin,xmax),
    }


def single_k_strip(k,delta=0.0):
    """A focused flat strip for one winding class."""
    target=RADIUS*(delta+TAU*k)

    if abs(target)<1e-12:
        xmin=-0.45*CIRC
        xmax=0.45*CIRC
    elif target>0:
        xmin=0.0
        xmax=max(target,CIRC)
    else:
        xmin=min(target,-CIRC)
        xmax=0.0

    # small padding
    pad=max(0.12*CIRC,0.08*(xmax-xmin))
    xmin-=pad
    xmax+=pad

    width=5.8
    height=3.05

    def T(x,z):
        return strip_mapper(x,z,xmin,xmax,width,height)

    g=VGroup()

    m0=math.floor(xmin/CIRC)
    m1=math.ceil(xmax/CIRC)

    for m in range(m0,m1):
        x0=max(xmin,m*CIRC)
        x1=min(xmax,(m+1)*CIRC)
        if x1<=x0:
            continue
        g.add(Polygon(
            T(x0,0),T(x1,0),T(x1,HEIGHT),T(x0,HEIGHT),
            fill_color=BLUE if m%2==0 else PANEL_2,
            fill_opacity=0.10,
            stroke_color=GRID,
            stroke_width=1.8,
        ))

    for m in range(m0,m1+1):
        x=m*CIRC
        if xmin<=x<=xmax:
            g.add(Line(
                T(x,0),T(x,HEIGHT),
                color=GRID if m!=0 else GOLD,
                stroke_width=2.0 if m!=0 else 4.5,
            ))

    A=T(0.0,0.0)
    B=T(target,HEIGHT)

    g.add(
        Dot(A,radius=0.073,color=GREEN),
        Dot(B,radius=0.073,color=RED),
        Line(A,B,color=GOLD,stroke_width=6.3),
    )

    return g,{"A":A,"B":B,"target":target,"T":T}


def copies_axis_diagram(delta):
    """Show B copies for a general angular separation delta."""
    kmin,kmax=-2,2
    xmin=RADIUS*(delta+TAU*kmin)-0.15*CIRC
    xmax=RADIUS*(delta+TAU*kmax)+0.15*CIRC

    width=5.85
    height=2.9

    def T(x,z):
        return strip_mapper(x,z,xmin,xmax,width,height)

    g=VGroup()

    A=T(0.0,0.0)
    g.add(Dot(A,radius=0.072,color=GREEN))

    for k in range(kmin,kmax+1):
        x=RADIUS*(delta+TAU*k)
        Bk=T(x,HEIGHT)
        g.add(
            Dot(Bk,radius=0.056,color=RED if k==0 else MUTED),
            Line(
                A,Bk,
                color=GOLD if k==0 else DIM,
                stroke_width=5.2 if k==0 else 2.0,
                stroke_opacity=1.0 if k==0 else 0.45,
            )
        )

    # baseline and top line
    g.add(
        Line(T(xmin,0),T(xmax,0),color=GRID,stroke_width=1.8),
        Line(T(xmin,HEIGHT),T(xmax,HEIGHT),color=GRID,stroke_width=1.8),
    )
    return g


def geometry_preflight(verbose=True):
    tol=1e-9

    if abs(CIRC-4*math.pi)>tol:
        raise AssertionError("Circumference should be 4pi")

    A=cyl_point(0.0,0.0)
    B=cyl_point(0.0,HEIGHT)
    if abs(np.linalg.norm(B-A)-HEIGHT)>tol:
        raise AssertionError("A and B must be on same generator")

    # k=0,1,2,3 formulas.
    for k in range(4):
        expected=math.sqrt((k*CIRC)**2+HEIGHT**2)

        # Speed of helix theta=2pi*k*t, z=h*t.
        speed=math.sqrt((RADIUS*TAU*k)**2+HEIGHT**2)
        if abs(speed-expected)>tol:
            raise AssertionError(("Helix length mismatch",k,speed,expected))

        # Universal-cover line length.
        flat=math.hypot(k*CIRC,HEIGHT)
        if abs(flat-expected)>tol:
            raise AssertionError(("Flat length mismatch",k,flat,expected))

    # Signed winding symmetry when endpoints use same generator.
    for k in [1,2,3]:
        lp=math.hypot(k*CIRC,HEIGHT)
        lm=math.hypot(-k*CIRC,HEIGHT)
        if abs(lp-lm)>tol:
            raise AssertionError("Opposite winding directions should tie")

    # Length strictly increases with |k|.
    vals=[math.hypot(k*CIRC,HEIGHT) for k in range(4)]
    if not all(vals[i]<vals[i+1] for i in range(len(vals)-1)):
        raise AssertionError("Lengths should increase with k")

    # General angular-separation formula.
    delta=math.pi/3
    for k in range(-2,3):
        x=RADIUS*(delta+TAU*k)
        L=math.sqrt(x*x+HEIGHT*HEIGHT)
        if L<HEIGHT-tol:
            raise AssertionError("Invalid general length")

    # For delta in (-pi,pi), k=0 is globally shortest.
    delta=0.8
    vals={k:math.hypot(RADIUS*(delta+TAU*k),HEIGHT) for k in range(-3,4)}
    kbest=min(vals,key=vals.get)
    if kbest!=0:
        raise AssertionError(("Expected k=0 for small delta",kbest))

    # At delta=pi, k=0 and k=-1 tie.
    delta=math.pi
    l0=math.hypot(RADIUS*delta,HEIGHT)
    lm1=math.hypot(RADIUS*(delta-TAU),HEIGHT)
    if abs(l0-lm1)>tol:
        raise AssertionError("Antipodal tie should occur")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  cylinder r=2, h=3")
        print("  A and B on same generator")
        print("  exact k-turn class: L_k=sqrt((4*pi*k)^2+9)")
        print("  k and -k have equal length")
        print("  L_0<L_1<L_2<L_3")
        print("  general copy formula: L_k=sqrt((r(delta+2*pi*k))^2+h^2)")
    return True


def layout_samples():
    return [
        lesson_card("BÀI TOÁN",[
            ("math","r=2, h=3",28,CYAN),
            ("text","A và B nằm trên cùng một đường sinh.",18,INK),
            ("text","Đường đi phải quấn đúng k vòng.",18,GOLD),
            ("text","k = 0, 1, 2, ...",18,CYAN),
            ("math","L_k=?",34,GOLD),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","C=2 pi r=4 pi",28,CYAN),
            ("math","Delta s_k=4 pi k",28,CYAN),
            ("math","L_k=sqrt((4 pi k)^2+9)",29,GOLD),
            ("text","Đây là cực tiểu trong lớp quấn k vòng.",18,GREEN),
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
        h=header(12,title,progress)
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


class TraiPhang12Master(BaseLesson):
    def intro(self):
        self.clear_all()
        cyl=cylinder_wireframe()
        A,B=cylinder_endpoints()

        self.add(
            cyl,
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
            helix_curve(1,0.0,GOLD,5.8),
            helix_curve(2,0.0,CYAN,4.2),
        )

        card=intro_card(
            12,
            ["HÌNH TRỤ","ĐƯỜNG ĐI QUẤN k VÒNG"],
            "Một điểm đích, nhưng có vô số ảnh trên bản khai triển.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Ở video trước, ta chọn đường đi ngắn nhất giữa hai điểm trên mặt trụ. "
            "Bây giờ ta thêm một điều kiện mới: đường đi phải quấn quanh trụ đúng một số vòng cho trước.",
            1.8,
        )
        self.narrate(
            "Khi số vòng thay đổi, điểm đầu và điểm cuối trên hình trụ vẫn giữ nguyên, "
            "nhưng trên bản khai triển ta phải nối tới những bản sao khác nhau của điểm cuối.",
            1.8,
        )

    def problem(self):
        self.clear_all()
        self.add_hud("A và B nằm trên cùng một đường sinh","01 / 13")

        cyl=cylinder_wireframe()
        A,B=cylinder_endpoints()
        self.add(
            cyl,
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("BÀI TOÁN",[
            ("math","r=2",29,CYAN),
            ("math","h=3",29,CYAN),
            ("text","A ở vành dưới, B ở vành trên.",19,INK),
            ("text","A và B cùng một đường sinh.",18,INK),
            ("text","Đường đi quấn đúng k vòng.",19,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hình trụ vẫn có bán kính hai và chiều cao ba. "
            "Lần này A và B nằm trên cùng một đường sinh, A ở dưới và B ở trên.",
            1.7,
        )
        self.narrate(
            "Nếu không bắt buộc quấn vòng, đường ngắn nhất chỉ là đường sinh A B. "
            "Nhưng ta sẽ lần lượt yêu cầu đường đi quấn một vòng, hai vòng, rồi k vòng.",
            1.8,
        )

    def k_zero(self):
        self.clear_all()
        self.add_hud("Trường hợp k = 0","02 / 13")

        cyl=cylinder_wireframe()
        A,B=cylinder_endpoints()
        vertical=Line(A,B,color=GOLD,stroke_width=6.0)

        self.add(
            cyl,vertical,
            Dot3D(A,radius=0.080,color=GREEN),
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("KHÔNG QUẤN VÒNG",[
            ("math","k=0",31,CYAN),
            ("math","Delta s_0=0",29,INK),
            ("math","L_0=h=3",35,GOLD),
            ("text","Đây là đường ngắn nhất tự do.",18,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Với k bằng không, kiến không đi vòng quanh trụ. "
            "Nó chỉ đi thẳng theo đường sinh từ A lên B.",
            1.5,
        )
        self.narrate(
            "Độ dài khi đó đúng bằng chiều cao, tức là ba.",
            1.3,
        )

    def copies_idea(self):
        self.clear_all()
        self.add_hud("Tại sao B có nhiều ảnh?","03 / 13")

        strip,meta=universal_strip(-2,2,highlight_k=1,show_lines=False)
        self.add_fixed_in_frame_mobjects(strip)

        card=lesson_card("MỖI HÌNH CHỮ NHẬT RỘNG 4π",[
            ("math","C=2 pi r=4 pi",29,CYAN),
            ("text","Dán mép phải vào mép trái ta được hình trụ.",18,INK),
            ("text","Tiếp tục sang bản sao kế bên tương ứng thêm 1 vòng.",17,GOLD),
            ("text","B có vô số bản sao Bₖ.",19,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta tưởng tượng bản khai triển không chỉ có một hình chữ nhật, mà được lặp lại vô hạn sang hai phía.",
            1.7,
        )
        self.narrate(
            "Mỗi hình chữ nhật rộng đúng một chu vi, tức bốn pi. "
            "Đi qua thêm một bản sao theo phương ngang tương ứng với quấn thêm đúng một vòng quanh trụ.",
            1.9,
        )
        self.narrate(
            "Vì thế cùng một điểm B trên hình trụ có vô số ảnh trên dải phẳng kéo dài.",
            1.6,
        )

    def one_turn_flat(self):
        self.clear_all()
        self.add_hud("Quấn đúng 1 vòng","04 / 13")

        strip,meta=single_k_strip(1)
        self.add_fixed_in_frame_mobjects(strip)

        card=lesson_card("k = 1",[
            ("math","Delta s_1=4 pi",30,CYAN),
            ("math","Delta z=3",29,CYAN),
            ("math","L_1=sqrt((4 pi)^2+3^2)",27,INK),
            ("math","L_1=sqrt(16 pi^2+9)",32,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Muốn quấn đúng một vòng, ta không nối A với bản sao B ngay phía trên. "
            "Ta nối A với bản sao kế tiếp của B, cách ngang đúng một chu vi.",
            1.8,
        )
        self.narrate(
            "Độ lệch ngang là bốn pi, độ lệch đứng là ba. "
            "Vậy độ dài nhỏ nhất trong lớp đường quấn một vòng là căn của mười sáu pi bình phương cộng chín.",
            1.9,
        )

    def one_turn_cylinder(self):
        self.clear_all()
        self.add_hud("Cuộn đoạn thẳng lại: đường xoắn 1 vòng","05 / 13")

        cyl=cylinder_wireframe()
        path=helix_curve(1,0.0,GOLD,6.0)
        A,B=cylinder_endpoints()
        ant=Dot3D(A,radius=0.085,color=GREEN)

        self.add(
            cyl,path,ant,
            Dot3D(B,radius=0.080,color=RED),
        )

        card=lesson_card("ĐƯỜNG XOẮN 1 VÒNG",[
            ("text","Góc quay: từ 0 đến 2π.",18,CYAN),
            ("text","Độ cao: từ 0 đến 3.",18,CYAN),
            ("math","L_1=sqrt(16 pi^2+9)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Khi cuộn bản khai triển lại, đoạn thẳng vừa rồi trở thành một đường xoắn đi đúng một vòng quanh trụ.",
            MoveAlongPath(ant,helix_curve(1,0.0,GOLD,1.0)),
            min_time=4.3,
            rate_func=linear,
        )

    def two_turns_flat(self):
        self.clear_all()
        self.add_hud("Quấn đúng 2 vòng","06 / 13")

        strip,meta=single_k_strip(2)
        self.add_fixed_in_frame_mobjects(strip)

        card=lesson_card("k = 2",[
            ("math","Delta s_2=8 pi",30,CYAN),
            ("math","Delta z=3",29,CYAN),
            ("math","L_2=sqrt((8 pi)^2+3^2)",27,INK),
            ("math","L_2=sqrt(64 pi^2+9)",32,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu bắt buộc quấn hai vòng, điểm đích phải là bản sao của B cách A hai chu vi theo phương ngang.",
            1.7,
        )
        self.narrate(
            "Độ lệch ngang lúc này là tám pi. "
            "Đường ngắn nhất trong lớp hai vòng có độ dài căn của sáu mươi bốn pi bình phương cộng chín.",
            1.9,
        )

    def compare_classes(self):
        self.clear_all()
        self.add_hud("Mỗi số vòng là một lớp đường khác nhau","07 / 13")

        strip,meta=universal_strip(-2,2,highlight_k=1,show_lines=True)
        self.add_fixed_in_frame_mobjects(strip)

        card=lesson_card("SO SÁNH",[
            ("math","L_0=3",27,GREEN),
            ("math","L_1=sqrt(16 pi^2+9)",27,GOLD),
            ("math","L_2=sqrt(64 pi^2+9)",27,CYAN),
            ("math","L_0<L_1<L_2",31,INK),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Các đường k bằng không, một và hai không cạnh tranh trong cùng một điều kiện. "
            "Mỗi giá trị k là một lớp đường với số vòng khác nhau.",
            1.8,
        )
        self.narrate(
            "Trong từng lớp, đoạn thẳng tới đúng bản sao B tương ứng là ngắn nhất. "
            "Còn nếu không ràng buộc số vòng, k bằng không tất nhiên thắng.",
            1.8,
        )

    def formula_k(self):
        self.clear_all()
        self.add_hud("Công thức cho k vòng","08 / 13")

        strip,meta=universal_strip(-2,2,highlight_k=2,show_lines=True)
        self.add_fixed_in_frame_mobjects(strip)

        card=lesson_card("VỚI r=2, h=3",[
            ("math","C=4 pi",29,CYAN),
            ("math","Delta s_k=4 pi k",29,CYAN),
            ("math","L_k=sqrt((4 pi k)^2+9)",30,GOLD),
            ("text","k = 0, 1, 2, ...",18,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Với bán kính hai, mỗi vòng bổ sung thêm bốn pi vào độ lệch ngang trên dải phẳng.",
            1.6,
        )
        self.narrate(
            "Do đó với k vòng, độ lệch ngang là bốn pi k, còn độ lệch đứng vẫn bằng ba.",
            1.7,
        )
        self.narrate(
            "Công thức là L k bằng căn của bốn pi k tất cả bình phương cộng chín.",
            1.6,
        )

    def signed_k(self):
        self.clear_all()
        self.add_hud("k dương và k âm là hai chiều quấn","09 / 13")

        strip,meta=universal_strip(-2,2,highlight_k=-1,show_lines=True)
        self.add_fixed_in_frame_mobjects(strip)

        card=lesson_card("SỐ VÒNG CÓ HƯỚNG",[
            ("text","k > 0: quấn theo một chiều.",18,GOLD),
            ("text","k < 0: quấn theo chiều ngược lại.",18,CYAN),
            ("math","L_(-k)=L_k",30,GREEN),
            ("text","Do A và B cùng một đường sinh.",18,INK),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu muốn phân biệt chiều quấn, ta cho k mang dấu. "
            "K dương là một chiều, k âm là chiều ngược lại.",
            1.6,
        )
        self.narrate(
            "Trong bài này A và B cùng một đường sinh nên hai hướng đối xứng. "
            "Vì thế k và âm k cho cùng một độ dài.",
            1.7,
        )

    def general_delta(self):
        self.clear_all()
        self.add_hud("Nếu A và B không cùng một đường sinh","10 / 13")

        delta=math.pi/3
        dia=copies_axis_diagram(delta)
        self.add_fixed_in_frame_mobjects(dia)

        card=lesson_card("GÓC LỆCH BAN ĐẦU δ",[
            ("math","Delta theta_k=delta+2 pi k",26,CYAN),
            ("math","Delta s_k=r(delta+2 pi k)",25,CYAN),
            ("math","L_k=sqrt((r(delta+2 pi k))^2+h^2)",22,GOLD),
            ("text","k có thể âm, dương hoặc bằng 0.",17,INK),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu A và B không nằm trên cùng một đường sinh, ta gọi delta là góc lệch ban đầu từ A tới B.",
            1.7,
        )
        self.narrate(
            "Khi thêm k vòng, tổng góc quay trở thành delta cộng hai pi k. "
            "Độ lệch ngang trên bản khai triển là r nhân chính góc đó.",
            1.9,
        )
        self.narrate(
            "Vì vậy mỗi số nguyên k tạo ra một đường xoắn khác nhau với độ dài căn của r nhân delta cộng hai pi k tất cả bình phương cộng h bình phương.",
            1.9,
        )

    def global_shortest(self):
        self.clear_all()
        self.add_hud("Muốn ngắn nhất tự do thì chọn bản sao gần nhất","11 / 13")

        delta=0.8
        dia=copies_axis_diagram(delta)
        self.add_fixed_in_frame_mobjects(dia)

        card=lesson_card("KHÔNG RÀNG BUỘC SỐ VÒNG",[
            ("text","Xét tất cả các bản sao Bₖ.",18,INK),
            ("text","Chọn ảnh có |δ+2πk| nhỏ nhất.",18,CYAN),
            ("text","Chọn k để Lₖ nhỏ nhất.",18,GOLD),
            ("text","Đó là đường ngắn nhất toàn cục.",18,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu đề bài không ấn định số vòng, ta phải xét tất cả các bản sao của B.",
            1.5,
        )
        self.narrate(
            "Bản sao cho độ lệch ngang có giá trị tuyệt đối nhỏ nhất sẽ cho đường ngắn nhất toàn cục.",
            1.6,
        )
        self.narrate(
            "Đây là cách nhìn rất mạnh: thay vì so sánh vô số đường xoắn trên hình trụ, ta chỉ việc tìm bản sao gần nhất trên dải phẳng.",
            1.8,
        )

    def antipodal_tie(self):
        self.clear_all()
        self.add_hud("Trường hợp đối diện: hai bản sao cùng gần","12 / 13")

        delta=math.pi
        dia=copies_axis_diagram(delta)
        self.add_fixed_in_frame_mobjects(dia)

        card=lesson_card("KHI δ = π",[
            ("math","k=0",28,GOLD),
            ("math","k=-1",28,CYAN),
            ("math","L_0=L_(-1)",31,GREEN),
            ("text","Hai đường xoắn đối xứng cùng ngắn nhất.",18,INK),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu hai đường sinh đối diện nhau, delta bằng pi. "
            "Khi đó có hai bản sao của B nằm gần A như nhau.",
            1.6,
        )
        self.narrate(
            "Một bản ứng với k bằng không, bản kia ứng với k bằng âm một. "
            "Hai đường xoắn đối xứng có cùng độ dài nhỏ nhất.",
            1.7,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài quấn k vòng","13 / 13")

        cyl=cylinder_wireframe()
        self.add(
            cyl,
            helix_curve(1,0.0,GOLD,5.8),
            helix_curve(2,0.0,CYAN,4.2),
        )

        card=lesson_card("BỐN Ý CẦN NHỚ",[
            ("text","1. Mỗi vòng thêm một chu vi trên bản trải.",17,INK),
            ("text","2. Mỗi k chọn một bản sao khác của B.",17,INK),
            ("text","3. Trong lớp k, nối thẳng là ngắn nhất.",17,CYAN),
            ("math","L_k=sqrt((2 pi r k)^2+h^2)",27,GOLD),
            ("text","4. Không ràng buộc: chọn bản sao gần nhất.",17,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ý tưởng của video mười hai có thể gói trong một câu: mỗi vòng quấn thêm đúng một chu vi vào bản khai triển.",
            1.7,
        )
        self.narrate(
            "Với hai điểm cùng một đường sinh, lớp quấn k vòng có độ dài căn của hai pi r k tất cả bình phương cộng h bình phương.",
            1.8,
        )
        self.narrate(
            "Khi điểm cuối lệch một góc delta, ta chỉ thay hai pi k bằng delta cộng hai pi k. "
            "Từ đây bài toán nhiều đường xoắn trở thành bài toán chọn đúng bản sao trên mặt phẳng.",
            1.9,
        )

    def construct(self):
        self.intro()
        self.problem()
        self.k_zero()
        self.copies_idea()
        self.one_turn_flat()
        self.one_turn_cylinder()
        self.two_turns_flat()
        self.compare_classes()
        self.formula_k()
        self.signed_k()
        self.general_delta()
        self.global_shortest()
        self.antipodal_tie()
        self.summary()


class Smoke12(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.96)

        cyl=cylinder_wireframe()
        self.add(cyl,helix_curve(2,0.0,GOLD,5.8))
        self.wait(0.25)

        self.clear()
        strip,meta=single_k_strip(2)
        self.add_fixed_in_frame_mobjects(strip)
        self.wait(0.25)


def render_smoke():
    geometry_preflight(True)

    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_12_master_smoke"
    config.disable_caching=True

    scene=Smoke12()
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
    config.output_file="trai_phang_12_hinh_tru_k_vong_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang12Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_12.wav"
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


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










# ---------- geometry engine: moving target on a cube edge ----------
# Cube side a = 4.
#
# Bottom: A-B-C-D, top: A'-B'-C'-D'.
# Start A is fixed.
# Target P moves on the vertical edge C-C'.
# Let t = CP, 0 <= t <= 4.
#
# The route is constrained to the two-face strip:
#   bottom ABCD -> right face BCC'B'.
#
# Unfold the right face around hinge BC by +90 degrees.
# In the plane:
#   A  = (-2,-2)
#   P1 = (2+t, 2)
# so
#   L(t) = sqrt((4+t)^2 + 4^2).
#
# The straight line A-P1 crosses hinge BC at X.
# With BX measured from B toward C:
#   BX = 16/(4+t).
# Thus X slides continuously from C toward the midpoint of BC as P rises.
# At t=4 we recover the 2-face endpoint C' case:
#   BX=2, L=4*sqrt(5).
# ==========================================================

A_SIDE = 4.0
HALF = A_SIDE/2.0

RAW = {
    'A':  np.array([-HALF,-HALF,0.0]),
    'B':  np.array([ HALF,-HALF,0.0]),
    'C':  np.array([ HALF, HALF,0.0]),
    'D':  np.array([-HALF, HALF,0.0]),
    'A1': np.array([-HALF,-HALF,A_SIDE]),
    'B1': np.array([ HALF,-HALF,A_SIDE]),
    'C1': np.array([ HALF, HALF,A_SIDE]),
    'D1': np.array([-HALF, HALF,A_SIDE]),
}

BOTTOM_FACE = ['A','B','C','D']
RIGHT_FACE = ['B','C','C1','B1']
UNFOLD_ANGLE = PI/2

WORLD_SCALE = 0.78
WORLD_SHIFT = np.array([-3.15,-0.25,-0.35])
CAM_PHI = 68*DEGREES
CAM_THETA = -49*DEGREES


def W(p):
    return WORLD_SCALE*np.array(p,dtype=float)+WORLD_SHIFT


def p_raw(t):
    t=float(t)
    return RAW['C'] + (t/A_SIDE)*(RAW['C1']-RAW['C'])


def x_raw(t):
    t=float(t)
    bx=A_SIDE*A_SIDE/(A_SIDE+t)
    return RAW['B'] + (bx/A_SIDE)*(RAW['C']-RAW['B'])


def p_flat_raw(t):
    # Exact image after rotating right face +90 degrees around BC.
    return np.array([HALF+t, HALF, 0.0])


def length_t(t):
    return math.sqrt((A_SIDE+t)**2 + A_SIDE**2)


def bx_t(t):
    return A_SIDE*A_SIDE/(A_SIDE+t)


def rotate_point_axis(p, axis_a, axis_b, angle):
    p=np.array(p,dtype=float)
    a=np.array(axis_a,dtype=float)
    b=np.array(axis_b,dtype=float)
    k=b-a
    nk=np.linalg.norm(k)
    if nk<1e-12:
        raise ValueError('Zero-length axis')
    k=k/nk
    x=p-a
    return a + (
        x*math.cos(angle)
        + np.cross(k,x)*math.sin(angle)
        + k*np.dot(k,x)*(1.0-math.cos(angle))
    )


def geometry_preflight(verbose=True):
    tol=1e-9

    # Cube edges.
    edge_pairs=[
        ('A','B'),('B','C'),('C','D'),('D','A'),
        ('A1','B1'),('B1','C1'),('C1','D1'),('D1','A1'),
        ('A','A1'),('B','B1'),('C','C1'),('D','D1'),
    ]
    for u,v in edge_pairs:
        if abs(np.linalg.norm(RAW[u]-RAW[v])-A_SIDE)>tol:
            raise AssertionError(f'Wrong cube edge {u}{v}')

    # Rigid unfolding around BC.
    B,C=RAW['B'],RAW['C']
    for t in [0.0,0.7,2.0,3.3,4.0]:
        P=p_raw(t)
        Pf=rotate_point_axis(P,B,C,UNFOLD_ANGLE)
        target=p_flat_raw(t)
        if np.linalg.norm(Pf-target)>1e-8:
            raise AssertionError(('Wrong unfolded P',t,Pf,target))
        if abs(np.linalg.norm(P-C)-np.linalg.norm(Pf-C))>tol:
            raise AssertionError('Rigid distance changed')

        X=x_raw(t)
        if not (-tol <= bx_t(t) <= A_SIDE+tol):
            raise AssertionError('X left hinge segment')

        folded=np.linalg.norm(RAW['A']-X)+np.linalg.norm(P-X)
        flat=np.linalg.norm(p_flat_raw(t)-RAW['A'])
        if abs(folded-flat)>1e-8:
            raise AssertionError(('Folded/flat mismatch',t,folded,flat))
        if abs(flat-length_t(t))>tol:
            raise AssertionError('Length formula mismatch')

    # Special values.
    if abs(length_t(0.0)-4*math.sqrt(2))>tol:
        raise AssertionError('t=0 length wrong')
    if abs(length_t(2.0)-2*math.sqrt(13))>tol:
        raise AssertionError('t=2 length wrong')
    if abs(length_t(4.0)-4*math.sqrt(5))>tol:
        raise AssertionError('t=4 length wrong')

    if abs(bx_t(0.0)-4.0)>tol:
        raise AssertionError('X should be C at t=0')
    if abs(bx_t(2.0)-8.0/3.0)>tol:
        raise AssertionError('t=2 crossing wrong')
    if abs(bx_t(4.0)-2.0)>tol:
        raise AssertionError('X should be midpoint at t=4')

    # Monotonicity on [0,4]: L'(t)=(4+t)/L(t)>0 and BX decreases.
    for t in np.linspace(0,4,9):
        deriv=(A_SIDE+t)/length_t(t)
        dbx=-(A_SIDE*A_SIDE)/(A_SIDE+t)**2
        if not (deriv>0 and dbx<0):
            raise AssertionError('Monotonicity failed')

    # General side a formula check.
    for a in [1.0,2.5,7.0]:
        for t in [0.0,0.4*a,a]:
            L=math.sqrt((a+t)**2+a*a)
            BX=a*a/(a+t)
            if not (0.5*a-1e-9 <= BX <= a+1e-9):
                raise AssertionError('General hinge ratio out of range')
            if L<=0:
                raise AssertionError('General length invalid')

    if verbose:
        print('GEOMETRY PREFLIGHT OK')
        print('  cube side a=4')
        print('  target P moves on CC\' with t=CP in [0,4]')
        print('  prescribed strip: bottom ABCD -> right BCC\'B\'')
        print('  unfold right face +90 degrees around BC')
        print('  L(t)=sqrt((4+t)^2+16)')
        print('  BX(t)=16/(4+t)')
        print('  t=0: X=C, L=4sqrt(2)')
        print('  t=4: X=midpoint(BC), L=4sqrt(5)')
    return True


def solid(a,b,color=EDGE,width=4.0,opacity=0.96):
    return Line(np.array(a,float),np.array(b,float),color=color,stroke_width=width,stroke_opacity=opacity)


def hidden_edge(a,b,color=DIM,width=2.5,opacity=0.60):
    return DashedLine(np.array(a,float),np.array(b,float),color=color,stroke_width=width,stroke_opacity=opacity,dash_length=0.11,dashed_ratio=0.56)


def face_poly(points,color=BLUE,opacity=0.12):
    return Polygon(*[np.array(p,float) for p in points],fill_color=color,fill_opacity=opacity,stroke_width=0)


def cube_shell():
    p={k:W(v) for k,v in RAW.items()}
    fills=VGroup(
        face_poly([p[v] for v in BOTTOM_FACE],PURPLE,0.075),
        face_poly([p[v] for v in RIGHT_FACE],CYAN,0.085),
    )
    edges=VGroup(
        solid(p['A'],p['B'],EDGE,3.5),
        solid(p['B'],p['C'],GOLD,4.6),
        solid(p['C'],p['D'],EDGE,3.5),
        hidden_edge(p['D'],p['A']),
        solid(p['A1'],p['B1'],EDGE,3.5),
        solid(p['B1'],p['C1'],EDGE,3.5),
        solid(p['C1'],p['D1'],EDGE,3.5),
        hidden_edge(p['D1'],p['A1']),
        solid(p['A'],p['A1'],EDGE,3.2),
        solid(p['B'],p['B1'],EDGE,3.2),
        solid(p['C'],p['C1'],CYAN,4.5),
        hidden_edge(p['D'],p['D1']),
    )
    return VGroup(fills,edges)


def cube_labels():
    offsets={
        'A':np.array([-0.16,-0.12,-0.05]),
        'B':np.array([ 0.15,-0.12,-0.05]),
        'C':np.array([ 0.15, 0.12,-0.05]),
        'D':np.array([-0.16, 0.12,-0.05]),
        'C1':np.array([0.14,0.12,0.15]),
    }
    labs=VGroup()
    for k in ['A','B','C','D','C1']:
        color=GREEN if k=='A' else INK
        label=k.replace('1',"'")
        labs.add(mty(label,22,color).move_to(W(RAW[k])+offsets[k]))
    return labs


def moving_folded_group(t):
    P=p_raw(t)
    X=x_raw(t)
    return VGroup(
        Dot3D(W(P),radius=0.082,color=RED),
        Dot3D(W(X),radius=0.062,color=GOLD),
        solid(W(RAW['A']),W(X),GOLD,6.0),
        solid(W(X),W(P),GOLD,6.0),
    )


def right_face_group(t=2.0):
    pts=[W(RAW[v]) for v in RIGHT_FACE]
    poly=face_poly(pts,CYAN,0.18)
    border=VGroup(*[
        solid(pts[i],pts[(i+1)%4],CYAN,3.1)
        for i in range(4)
    ])
    P=p_raw(t)
    g=VGroup(poly,border,Dot3D(W(P),radius=0.080,color=RED))
    return g


def bottom_face_group():
    pts=[W(RAW[v]) for v in BOTTOM_FACE]
    poly=face_poly(pts,PURPLE,0.18)
    border=VGroup(*[
        solid(pts[i],pts[(i+1)%4],PURPLE,3.1)
        for i in range(4)
    ])
    return VGroup(poly,border,Dot3D(W(RAW['A']),radius=0.080,color=GREEN))


def net_mapper():
    width=5.75
    height=4.95
    # Net bounding rectangle for t up to 4: x raw from -2 to 6, y -2 to 2.
    xmin,xmax=-2.0,6.0
    ymin,ymax=-2.0,2.0
    left=LEFT_CENTER[0]-width/2
    bottom=LEFT_CENTER[1]-height/2
    def T(x,y):
        return np.array([
            left + width*(x-xmin)/(xmax-xmin),
            bottom + height*(y-ymin)/(ymax-ymin),
            0.0,
        ])
    return T


def net_static(t=2.0,show_path=True):
    T=net_mapper()
    bottom=Polygon(
        T(-2,-2),T(2,-2),T(2,2),T(-2,2),
        fill_color=PURPLE,fill_opacity=0.14,
        stroke_color=PURPLE,stroke_width=3.0,
    )
    right=Polygon(
        T(2,-2),T(6,-2),T(6,2),T(2,2),
        fill_color=CYAN,fill_opacity=0.12,
        stroke_color=CYAN,stroke_width=3.0,
    )
    hinge=Line(T(2,-2),T(2,2),color=GOLD,stroke_width=5.0)

    P1=p_flat_raw(t)
    bx=bx_t(t)
    X=np.array([2.0,-2.0+bx])
    A2=T(-2,-2)
    P2=T(P1[0],P1[1])
    X2=T(X[0],X[1])

    g=VGroup(
        bottom,right,hinge,
        Dot(A2,radius=0.072,color=GREEN),
        Dot(P2,radius=0.072,color=RED),
    )
    if show_path:
        g.add(Line(A2,P2,color=GOLD,stroke_width=6.2),Dot(X2,radius=0.058,color=GOLD))
    return g,{'A':A2,'P1':P2,'X':X2,'T':T}


def dynamic_net_group(tracker):
    def build():
        t=tracker.get_value()
        g,_=net_static(t,show_path=True)
        return g
    return always_redraw(build)


def layout_samples():
    return [
        lesson_card('ĐIỂM ĐÍCH DI ĐỘNG',[
            ('math','a=4',28,CYAN),
            ('math','P in C C\'',28,CYAN),
            ('math','t=C P',29,GOLD),
            ('math','0<=t<=4',27,INK),
            ('text','Đường đi dùng đáy và mặt bên phải.',18,GREEN),
        ],GOLD),
        lesson_card('KẾT QUẢ THEO t',[
            ('math','L(t)=sqrt((4+t)^2+16)',27,GOLD),
            ('math','B X=frac(16,4+t)',28,CYAN),
            ('math','L\'(t)=frac(4+t,L(t))>0',25,GREEN),
            ('text','P đi lên thì X trượt từ C về trung điểm BC.',17,INK),
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
        h=header(17,title,progress)
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
    tree=ast.parse(source_path.read_text(encoding='utf-8'))
    spoken=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call):
            fname=node.func.attr if isinstance(node.func,ast.Attribute) else None
            if fname in {'narrate','narrate_play'} and node.args:
                first=node.args[0]
                if isinstance(first,ast.Constant) and isinstance(first.value,str):
                    spoken.append(first.value)

    forbidden=['workflow','render','preflight','engine','code','mã nguồn','camera','animation','cột trái','cột phải','debug']
    bad=[]
    for line in spoken:
        low=line.lower()
        for word in forbidden:
            if word in low:
                bad.append((word,line))
    if bad:
        raise AssertionError(bad)
    if verbose:
        print(f'NARRATION LINT OK: {len(spoken)} segments')
    return True


class TraiPhang17Master(BaseLesson):
    def intro(self):
        self.clear_all()
        tracker=ValueTracker(0.0)
        moving=always_redraw(lambda: moving_folded_group(tracker.get_value()))
        self.add(cube_shell(),moving)

        card=intro_card(
            17,
            ['ĐIỂM ĐÍCH CHẠY TRÊN CẠNH','ĐƯỜNG NGẮN NHẤT THAY ĐỔI THEO t'],
            'P di chuyển trên CC\'; điểm đổi mặt X cũng phải di chuyển.',
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            'Ở các video trước, điểm đầu và điểm cuối thường được giữ cố định. '
            'Bây giờ ta cho điểm đích P chạy dọc theo một cạnh của khối lập phương.',
            1.7,
        )
        self.narrate_play(
            'Khi P đi từ C lên C phẩy, đường ngắn nhất trên hai mặt cũng thay đổi liên tục, '
            'và điểm chuyển mặt trên cạnh B C cũng trượt theo.',
            tracker.animate.set_value(4.0),
            min_time=4.0,
            rate_func=linear,
        )

    def problem(self):
        self.clear_all()
        self.add_hud('Khối lập phương cạnh 4','01 / 13')
        self.add(cube_shell())
        labs=cube_labels()
        for lab in labs:
            self.add_fixed_orientation_mobjects(lab)

        P=p_raw(2.0)
        self.add(Dot3D(W(P),radius=0.082,color=RED))

        card=lesson_card('BÀI TOÁN',[
            ('math','A B=4',28,CYAN),
            ('math','P in C C\'',27,CYAN),
            ('text','A cố định, P là điểm đích di động.',18,INK),
            ('text','Chỉ dùng đáy ABCD và mặt BCC\'B\'.',17,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Khối lập phương có cạnh bằng bốn. A là điểm xuất phát cố định, còn P chạy trên cạnh thẳng đứng C C phẩy.',
            1.7,
        )
        self.narrate(
            'Ta xét các đường đi chỉ nằm trên hai mặt: đáy A B C D và mặt bên B C C phẩy B phẩy.',
            1.7,
        )

    def parameter(self):
        self.clear_all()
        self.add_hud('Đặt t = CP','02 / 13')
        tracker=ValueTracker(0.0)
        moving=always_redraw(lambda: VGroup(
            cube_shell(),
            Dot3D(W(p_raw(tracker.get_value())),radius=0.085,color=RED),
        ))
        self.add(moving)

        card=lesson_card('THAM SỐ',[
            ('math','t=C P',31,GOLD),
            ('math','0<=t<=4',29,CYAN),
            ('math','t=0 => P=C',25,INK),
            ('math','t=4 => P=C\'',25,INK),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Đặt t bằng C P. Vì cạnh C C phẩy dài bốn nên t chạy từ không tới bốn.',
            1.6,
        )
        self.narrate_play(
            'Khi t bằng không, P trùng C. Khi t bằng bốn, P lên tới C phẩy.',
            tracker.animate.set_value(4.0),
            min_time=3.5,
            rate_func=linear,
        )

    def arbitrary_x(self):
        self.clear_all()
        self.add_hud('Với một vị trí P, gọi X là điểm đổi mặt','03 / 13')
        t0=2.0
        self.add(cube_shell(),moving_folded_group(t0))

        card=lesson_card('VỚI X THUỘC BC',[
            ('math','L=A X+X P',31,ORANGE),
            ('text','AX nằm trên đáy.',19,PURPLE),
            ('text','XP nằm trên mặt bên phải.',19,CYAN),
            ('text','Cần chọn X sao cho tổng nhỏ nhất.',18,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Giữ P ở một vị trí bất kỳ. Gọi X là điểm đường đi chuyển từ đáy sang mặt bên trên cạnh B C.',
            1.7,
        )
        self.narrate(
            'Độ dài là A X cộng X P. Ta cần tìm vị trí X tốt nhất cho từng giá trị của t.',
            1.6,
        )

    def unfold(self):
        self.clear_all()
        self.add_hud('Mở mặt bên phải quanh BC','04 / 13')
        t0=2.0
        bottom=bottom_face_group()
        right=right_face_group(t0)
        self.add(bottom,right)

        card=lesson_card('TRẢI HAI MẶT',[
            ('text','Giữ đáy ABCD.',19,PURPLE),
            ('text','Cạnh BC đứng yên.',19,GOLD),
            ('text','Mở mặt BCC\'B\' quanh BC.',18,CYAN),
            ('text','P đi theo chính mặt bên.',18,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Ta giữ đáy và mở mặt bên phải quanh cạnh chung B C. Cạnh B C đứng yên trong suốt quá trình.',
            1.7,
        )
        self.narrate_play(
            'Điểm P nằm trên mặt bên nên nó phải đi theo đúng phép quay của mặt ấy.',
            Rotate(
                right,
                angle=UNFOLD_ANGLE,
                axis=W(RAW['C'])-W(RAW['B']),
                about_point=W(RAW['B']),
            ),
            min_time=3.2,
            rate_func=smooth,
        )

    def net_coords(self):
        self.clear_all()
        self.add_hud('Tọa độ trên bản trải','05 / 13')
        net,pts=net_static(2.0,show_path=False)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card('CHỌN HỆ TRỤC',[
            ('math','A=(-2,-2)',27,INK),
            ('math','B=(2,-2), C=(2,2)',24,INK),
            ('math','P_1=(2+t,2)',29,CYAN),
            ('text','P₁ là ảnh của P sau khi mở.',18,GOLD),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Trên bản trải, đặt A tại âm hai, âm hai; B tại hai, âm hai; và C tại hai, hai.',
            1.7,
        )
        self.narrate(
            'Khi P cách C một đoạn t theo phương thẳng đứng, sau khi mở nó trở thành P một có tọa độ hai cộng t, hai.',
            1.9,
        )

    def length_formula(self):
        self.clear_all()
        self.add_hud('Độ dài ngắn nhất là một hàm của t','06 / 13')
        net,pts=net_static(2.0,show_path=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card('PYTHAGORE TRÊN BẢN TRẢI',[
            ('math','Delta x=4+t',28,CYAN),
            ('math','Delta y=4',28,CYAN),
            ('math','L(t)^2=(4+t)^2+4^2',26,INK),
            ('math','L(t)=sqrt((4+t)^2+16)',31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Trong mặt phẳng, đường ngắn nhất là đoạn thẳng A P một.',
            1.4,
        )
        self.narrate(
            'Độ lệch ngang là bốn cộng t, còn độ lệch đứng luôn bằng bốn. '
            'Vì vậy L của t bằng căn của bốn cộng t tất cả bình phương cộng mười sáu.',
            2.0,
        )

    def crossing_formula(self):
        self.clear_all()
        self.add_hud('Điểm đổi mặt X cũng phụ thuộc t','07 / 13')
        net,pts=net_static(2.0,show_path=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card('TAM GIÁC ĐỒNG DẠNG',[
            ('math','frac(B X,4)=frac(4,4+t)',26,INK),
            ('math','B X=frac(16,4+t)',31,GOLD),
            ('text','t tăng thì BX giảm.',18,CYAN),
            ('text','X trượt từ C về phía B.',18,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Đoạn thẳng A P một cắt cạnh B C tại X. Từ hai tam giác đồng dạng, ta có B X trên bốn bằng bốn trên bốn cộng t.',
            1.9,
        )
        self.narrate(
            'Suy ra B X bằng mười sáu chia bốn cộng t. '
            'Đây là công thức mô tả chính xác cách điểm đổi mặt trượt trên cạnh B C.',
            1.9,
        )

    def dynamic_net(self):
        self.clear_all()
        self.add_hud('Cho t chạy liên tục từ 0 đến 4','08 / 13')
        tracker=ValueTracker(0.0)
        dyn=dynamic_net_group(tracker)
        self.add_fixed_in_frame_mobjects(dyn)

        card=lesson_card('CHUYỂN ĐỘNG TRÊN BẢN TRẢI',[
            ('text','P₁ đi sang phải khi t tăng.',18,RED),
            ('text','Đường thẳng tối ưu quay dần.',18,GOLD),
            ('text','X trượt xuống dọc cạnh BC.',18,CYAN),
            ('math','B X=frac(16,4+t)',28,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            'Khi t tăng từ không tới bốn, P một đi dần sang phải. '
            'Đoạn thẳng tối ưu thay đổi liên tục và giao điểm X trượt từ C về trung điểm của B C.',
            tracker.animate.set_value(4.0),
            min_time=5.0,
            rate_func=linear,
        )

    def dynamic_folded(self):
        self.clear_all()
        self.add_hud('Cùng chuyển động ấy trên khối lập phương','09 / 13')
        tracker=ValueTracker(0.0)
        dyn=always_redraw(lambda: moving_folded_group(tracker.get_value()))
        self.add(cube_shell(),dyn)

        card=lesson_card('TRÊN HÌNH GẤP',[
            ('text','P đi lên trên CC\'.',18,RED),
            ('text','X trượt trên BC.',18,GOLD),
            ('text','Hai đoạn AX và XP luôn khớp với một đoạn thẳng khi trải.',17,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            'Trên hình gấp, ta thấy cùng một hiện tượng: P đi lên, X trượt dọc B C, '
            'và đường gấp A X P luôn là ảnh của một đoạn thẳng trên bản trải.',
            tracker.animate.set_value(4.0),
            min_time=5.0,
            rate_func=linear,
        )

    def special_values(self):
        self.clear_all()
        self.add_hud('Ba vị trí đặc biệt của P','10 / 13')
        net,pts=net_static(2.0,show_path=True)
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card('THAY t',[
            ('math','t=0: L=4 sqrt(2), B X=4',24,INK),
            ('math','t=2: L=2 sqrt(13), B X=frac(8,3)',23,CYAN),
            ('math','t=4: L=4 sqrt(5), B X=2',24,GOLD),
            ('text','Điểm đổi mặt tiến dần từ C về trung điểm.',17,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Khi t bằng không, P chính là C và X cũng chính là C. Đường đi chỉ còn đường chéo A C của đáy.',
            1.8,
        )
        self.narrate(
            'Khi t bằng hai, độ dài là hai căn mười ba và B X bằng tám phần ba.',
            1.6,
        )
        self.narrate(
            'Khi t bằng bốn, P tới C phẩy, X trở thành trung điểm của B C và độ dài bằng bốn căn năm.',
            1.8,
        )

    def monotonic(self):
        self.clear_all()
        self.add_hud('P càng lên cao, đường ngắn nhất càng dài','11 / 13')
        self.add(cube_shell())

        card=lesson_card('XÉT HÀM L(t)',[
            ('math','L(t)=sqrt((4+t)^2+16)',26,INK),
            ('math','L\'(t)=frac(4+t,L(t))',26,CYAN),
            ('math','L\'(t)>0',31,GREEN),
            ('text','Nên L(t) tăng trên [0,4].',18,GOLD),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Ta còn đọc được xu hướng từ công thức. Đạo hàm của L theo t bằng bốn cộng t chia L của t.',
            1.7,
        )
        self.narrate(
            'Trên đoạn từ không tới bốn, biểu thức này luôn dương. '
            'Vì vậy P càng đi lên cao thì đường ngắn nhất trong dải hai mặt càng dài.',
            1.9,
        )

    def recover_video01(self):
        self.clear_all()
        self.add_hud('Khi t = 4, ta gặp lại bài hai mặt quen thuộc','12 / 13')
        self.add(cube_shell(),moving_folded_group(4.0))

        card=lesson_card('P = C\'',[
            ('math','t=4',29,CYAN),
            ('math','B X=frac(16,8)=2',28,INK),
            ('text','X là trung điểm BC.',18,GOLD),
            ('math','L=4 sqrt(5)',33,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Trường hợp cuối t bằng bốn chính là bài A tới C phẩy trên hai mặt mà ta đã gặp ở đầu series.',
            1.7,
        )
        self.narrate(
            'Công thức động tự động trả lại kết quả cũ: điểm đổi mặt là trung điểm B C và độ dài bằng bốn căn năm.',
            1.8,
        )

    def general_formula(self):
        self.clear_all()
        self.add_hud('Công thức tổng quát với cạnh khối lập phương a','13 / 13')
        self.add(cube_shell())

        card=lesson_card('VỚI 0 ≤ t ≤ a',[
            ('math','L(t)=sqrt((a+t)^2+a^2)',27,GOLD),
            ('math','B X=frac(a^2,a+t)',28,CYAN),
            ('math','L\'(t)=frac(a+t,L(t))>0',25,GREEN),
            ('text','Một tham số điều khiển cả độ dài lẫn điểm đổi mặt.',17,INK),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            'Nếu cạnh khối lập phương là a thay vì bốn, công thức hoàn toàn tương tự.',
            1.5,
        )
        self.narrate(
            'Độ dài nhỏ nhất bằng căn của a cộng t tất cả bình phương cộng a bình phương. '
            'Vị trí đổi mặt thỏa B X bằng a bình phương chia a cộng t.',
            2.0,
        )
        self.narrate(
            'Video này cho thấy khi điểm đích chuyển động, không chỉ đáp số thay đổi mà chính đường đi tối ưu cũng chuyển động theo một quy luật hình học rất rõ.',
            1.9,
        )

    def construct(self):
        self.intro()
        self.problem()
        self.parameter()
        self.arbitrary_x()
        self.unfold()
        self.net_coords()
        self.length_formula()
        self.crossing_formula()
        self.dynamic_net()
        self.dynamic_folded()
        self.special_values()
        self.monotonic()
        self.recover_video01()
        self.general_formula()


class Smoke17(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.96)

        tracker=ValueTracker(0.0)
        dyn=always_redraw(lambda: moving_folded_group(tracker.get_value()))
        self.add(cube_shell(),dyn)
        self.play(tracker.animate.set_value(4.0),run_time=1.3,rate_func=linear)
        self.wait(0.1)

        self.clear()
        bottom=bottom_face_group()
        right=right_face_group(2.0)
        self.add(bottom,right)
        self.play(
            Rotate(
                right,
                angle=UNFOLD_ANGLE,
                axis=W(RAW['C'])-W(RAW['B']),
                about_point=W(RAW['B']),
            ),
            run_time=1.1,
            rate_func=smooth,
        )
        self.wait(0.1)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file='trai_phang_17_master_smoke'
    config.disable_caching=True
    scene=Smoke17()
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
    config.output_file='trai_phang_17_diem_dich_chay_tren_canh_MASTER_1080p'
    config.disable_caching=False

    scene=TraiPhang17Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/'master_narration_trai_phang_17.wav'
    build_master_audio(scene.audio_events,duration,master_wav)

    final_path=video_path.with_name(video_path.stem+'_WITH_AUDIO.mp4')
    mux_audio(video_path,master_wav,final_path)

    print('VIDEO HOAN CHINH:',final_path)
    return final_path


if __name__=='__main__':
    source_path=Path(sys.argv[0]).resolve()

    if '--narration-lint' in sys.argv:
        narration_lint(source_path,True)
        raise SystemExit(0)
    if '--geometry-preflight' in sys.argv:
        geometry_preflight(True)
        raise SystemExit(0)
    if '--layout-preflight' in sys.argv:
        layout_preflight(layout_samples(),True)
        raise SystemExit(0)
    if '--smoke-render' in sys.argv:
        render_smoke()
        raise SystemExit(0)

    render_full()

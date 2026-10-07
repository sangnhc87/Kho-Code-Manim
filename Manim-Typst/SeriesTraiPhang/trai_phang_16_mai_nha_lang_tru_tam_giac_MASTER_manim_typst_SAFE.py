
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
    titles.arrange(DOWN, aligned_ed=LEFT, buff=0.10)
    sub = fit_width(txt(subtitle, 18, CYAN), 4.55)
    g = VGroup(n, titles, sub).arrange(DOWN, aligned_ed=LEFT, buff=0.25)
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









# ---------- geometry engine: triangular-prism roof ----------
# Practical roof model: cross-section 3-4-5, house length 8.
# Two roof rectangles 5x8 unfold to one 10x8 rectangle.
# Start A, end B1. Shortest roof path crosses ridge SS1 at its midpoint M.
# Lmin = sqrt(10^2+8^2) = 2*sqrt(41).

HALF_WIDTH = 3.0
RISE = 4.0
ROOF_SLANT = 5.0
HOUSE_LEN = 8.0

RAW = {
    "A":  np.array([-HALF_WIDTH, -HOUSE_LEN/2, 0.0]),
    "B":  np.array([ HALF_WIDTH, -HOUSE_LEN/2, 0.0]),
    "S":  np.array([0.0, -HOUSE_LEN/2, RISE]),
    "A1": np.array([-HALF_WIDTH,  HOUSE_LEN/2, 0.0]),
    "B1": np.array([ HALF_WIDTH,  HOUSE_LEN/2, 0.0]),
    "S1": np.array([0.0,  HOUSE_LEN/2, RISE]),
}

FACES = {
    "left_roof":  ["A","S","S1","A1"],
    "right_roof": ["S","B","B1","S1"],
}

WORLD_SCALE = 0.68
WORLD_SHIFT = np.array([-3.18,-0.20,-0.20])
CAM_PHI = 66 * DEGREES
CAM_THETA = -48 * DEGREES


def W(p):
    return WORLD_SCALE*np.array(p,dtype=float)+WORLD_SHIFT


def rotate_point_axis(p, axis_a, axis_b, angle):
    p=np.array(p,dtype=float)
    a=np.array(axis_a,dtype=float)
    b=np.array(axis_b,dtype=float)
    k=b-a
    nk=np.linalg.norm(k)
    if nk<1e-12:
        raise ValueError("Zero-length axis")
    k=k/nk
    x=p-a
    return a + (
        x*math.cos(angle)
        + np.cross(k,x)*math.sin(angle)
        + k*np.dot(k,x)*(1.0-math.cos(angle))
    )


def face_normal(points):
    q=np.array(points,dtype=float)
    n=np.cross(q[1]-q[0],q[2]-q[0])
    return n/np.linalg.norm(n)


def signed_angle_about_axis(v,w,axis):
    v=np.array(v,dtype=float)
    w=np.array(w,dtype=float)
    axis=np.array(axis,dtype=float)
    axis=axis/np.linalg.norm(axis)
    return math.atan2(np.dot(axis,np.cross(v,w)),np.dot(v,w))


def pairwise_distances(points):
    vals=[]
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            vals.append(np.linalg.norm(np.array(points[i])-np.array(points[j])))
    return np.array(vals)


def unfold_right_numeric():
    fixed={v:RAW[v].copy() for v in FACES["left_roof"]}
    moving={v:RAW[v].copy() for v in FACES["right_roof"]}
    n0=face_normal([fixed[v] for v in FACES["left_roof"]])
    plane_p=fixed["A"].copy()
    a=RAW["S"].copy()
    b=RAW["S1"].copy()
    axis=b-a
    n_move=face_normal([moving[v] for v in FACES["right_roof"]])
    fixed_cent=np.mean(list(fixed.values()),axis=0)
    trials=[]
    for target in (n0,-n0):
        ang=signed_angle_about_axis(n_move,target,axis)
        test={v:rotate_point_axis(moving[v],a,b,ang) for v in moving}
        err=max(abs(np.dot(q-plane_p,n0)) for q in test.values())
        side_fixed=np.dot(np.cross(axis,fixed_cent-a),n0)
        move_cent=np.mean(list(test.values()),axis=0)
        side_move=np.dot(np.cross(axis,move_cent-a),n0)
        opposite_penalty=0 if side_fixed*side_move<0 else 1
        trials.append((round(err,12),opposite_penalty,abs(ang),ang,test))
    trials.sort(key=lambda z:(z[0]>1e-8,z[1],z[2]))
    _,_,_,ang,test=trials[0]
    return ang,test,n0,plane_p


UNFOLD_ANGLE, RIGHT_FLAT, LEFT_NORMAL, LEFT_PLANE_P = unfold_right_numeric()
M_RAW = 0.5*(RAW["S"]+RAW["S1"])


def geometry_preflight(verbose=True):
    tol=1e-9
    if abs(np.linalg.norm(RAW["A"]-RAW["S"])-ROOF_SLANT)>tol:
        raise AssertionError("Left slant should be 5")
    if abs(np.linalg.norm(RAW["B"]-RAW["S"])-ROOF_SLANT)>tol:
        raise AssertionError("Right slant should be 5")
    if abs(np.linalg.norm(RAW["A"]-RAW["B"])-6.0)>tol:
        raise AssertionError("House width should be 6")
    for u,v in [("A","A1"),("B","B1"),("S","S1")]:
        if abs(np.linalg.norm(RAW[u]-RAW[v])-HOUSE_LEN)>tol:
            raise AssertionError("Prism length should be 8")

    before=[RAW[v] for v in FACES["right_roof"]]
    after=[RIGHT_FLAT[v] for v in FACES["right_roof"]]
    if not np.allclose(pairwise_distances(before),pairwise_distances(after),atol=1e-9,rtol=0):
        raise AssertionError("Right roof face distorted")
    if max(abs(np.dot(q-LEFT_PLANE_P,LEFT_NORMAL)) for q in after)>1e-8:
        raise AssertionError("Right roof not coplanar after unfolding")

    expected=2.0*math.sqrt(41.0)
    if abs(np.linalg.norm(M_RAW-RAW["S"])-4.0)>tol:
        raise AssertionError("SM should be 4")
    folded=np.linalg.norm(RAW["A"]-M_RAW)+np.linalg.norm(RAW["B1"]-M_RAW)
    if abs(folded-expected)>1e-8:
        raise AssertionError("Folded path mismatch")
    if abs(np.linalg.norm(RAW["A"]-M_RAW)-math.sqrt(41.0))>tol:
        raise AssertionError("AM should be sqrt41")
    if abs(np.linalg.norm(RAW["B1"]-M_RAW)-math.sqrt(41.0))>tol:
        raise AssertionError("MB1 should be sqrt41")

    direct=np.linalg.norm(RAW["B1"]-RAW["A"])
    if abs(direct-10.0)>tol:
        raise AssertionError("Direct chord should be 10")
    if not direct<expected:
        raise AssertionError("Direct chord should be shorter but invalid")
    if not expected < 18.0:
        raise AssertionError("Optimal route should beat edge route")

    general=math.sqrt(4*(HALF_WIDTH**2+RISE**2)+HOUSE_LEN**2)
    if abs(general-expected)>tol:
        raise AssertionError("General formula mismatch")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  triangular-prism roof: half-width 3, rise 4, slant 5, length 8")
        print("  two roof rectangles 5x8 unfold rigidly around ridge")
        print("  flat net = 10x8 rectangle")
        print("  ridge crossing M is midpoint: SM=4")
        print("  AM=MB1=sqrt(41)")
        print("  Lmin=2*sqrt(41)")
        print("  direct spatial chord=10 is invalid")
    return True


def solid(a,b,color=EDGE,width=4.0,opacity=0.96):
    return Line(np.array(a,float),np.array(b,float),color=color,stroke_width=width,stroke_opacity=opacity)


def hidden_ed(a,b,color=DIM,width=2.5,opacity=0.62):
    return DashedLine(np.array(a,float),np.array(b,float),color=color,stroke_width=width,stroke_opacity=opacity,dash_length=0.11,dashed_ratio=0.56)


def face_poly(points,color=BLUE,opacity=0.12):
    return Polygon(*[np.array(p,float) for p in points],fill_color=color,fill_opacity=opacity,stroke_width=0)


def roof_shell():
    p={k:W(v) for k,v in RAW.items()}
    fills=VGroup(
        face_poly([p[v] for v in FACES["left_roof"]],PURPLE,0.10),
        face_poly([p[v] for v in FACES["right_roof"]],CYAN,0.10),
    )
    edges=VGroup(
        solid(p["A"],p["S"],EDGE,3.7), solid(p["S"],p["B"],EDGE,3.7),
        solid(p["A1"],p["S1"],EDGE,3.7), solid(p["S1"],p["B1"],EDGE,3.7),
        solid(p["A"],p["A1"],EDGE,3.5), solid(p["B"],p["B1"],EDGE,3.5),
        solid(p["S"],p["S1"],GOLD,5.0),
        hidden_ed(p["A"],p["B"],DIM,2.4), hidden_ed(p["A1"],p["B1"],DIM,2.4),
    )
    return VGroup(fills,edges)


def roof_labels():
    offsets={
        "A":np.array([-0.14,-0.12,-0.06]), "B":np.array([0.14,-0.12,-0.06]),
        "S":np.array([0.0,-0.10,0.18]), "A1":np.array([-0.14,0.14,-0.05]),
        "B1":np.array([0.14,0.14,-0.05]), "S1":np.array([0.0,0.14,0.18]),
    }
    labs=VGroup()
    for k in ["A","B","S","A1","B1","S1"]:
        color=GREEN if k=="A" else (RED if k=="B1" else INK)
        labs.add(mty(k.replace("1","'"),22,color).move_to(W(RAW[k])+offsets[k]))
    return labs


def folded_route():
    return VGroup(
        solid(W(RAW["A"]),W(M_RAW),GOLD,6.4),
        solid(W(M_RAW),W(RAW["B1"]),GOLD,6.4),
        Dot3D(W(M_RAW),radius=0.065,color=GOLD),
    ), [RAW["A"],M_RAW,RAW["B1"]]


def direct_chord():
    return DashedLine(W(RAW["A"]),W(RAW["B1"]),color=RED,stroke_width=5.0,dash_length=0.12)


def face_mob(face_name,color,start_vertex=None,end_vertex=None):
    pts=[W(RAW[v]) for v in FACES[face_name]]
    poly=face_poly(pts,color,0.18)
    border=VGroup(*[solid(pts[i],pts[(i+1)%4],color,3.1) for i in range(4)])
    g=VGroup(poly,border)
    if start_vertex:
        g.add(Dot3D(W(RAW[start_vertex]),radius=0.075,color=GREEN))
    if end_vertex:
        g.add(Dot3D(W(RAW[end_vertex]),radius=0.075,color=RED))
    return g


def unfold_mobs():
    return face_mob("left_roof",PURPLE,"A",None), face_mob("right_roof",CYAN,None,"B1")


def net_rectangle(show_path=True):
    width=5.8
    height=4.64
    left=LEFT_CENTER[0]-width/2
    bottom=LEFT_CENTER[1]-height/2
    def T(x,y):
        return np.array([left+width*(x/10.0),bottom+height*(y/8.0),0.0])
    A,S,S1,B1,M=T(0,0),T(5,0),T(5,8),T(10,8),T(5,4)
    left_face=Polygon(T(0,0),T(5,0),T(5,8),T(0,8),fill_color=PURPLE,fill_opacity=0.14,stroke_color=PURPLE,stroke_width=3.0)
    right_face=Polygon(T(5,0),T(10,0),T(10,8),T(5,8),fill_color=CYAN,fill_opacity=0.14,stroke_color=CYAN,stroke_width=3.0)
    ridge=Line(S,S1,color=GOLD,stroke_width=5.0)
    g=VGroup(left_face,right_face,ridge,Dot(A,radius=0.073,color=GREEN),Dot(B1,radius=0.073,color=RED))
    if show_path:
        g.add(Line(A,B1,color=GOLD,stroke_width=6.3),Dot(M,radius=0.060,color=GOLD))
    return g,{"A":A,"S":S,"S1":S1,"B1":B1,"M":M,"T":T}


def cross_section_diagram():
    center=LEFT_CENTER+DOWN*0.15
    A=center+np.array([-2.25,-1.5,0.0])
    B=center+np.array([2.25,-1.5,0.0])
    S=center+np.array([0.0,1.5,0.0])
    N=(A+B)/2
    return VGroup(
        Polygon(A,S,B,fill_color=BLUE,fill_opacity=0.10,stroke_color=EDGE,stroke_width=3.0),
        DashedLine(S,N,color=CYAN,stroke_width=2.6,dash_length=0.10),
        Dot(N,radius=0.050,color=CYAN),
    )


def layout_samples():
    return [
        lesson_card("MÁI NHÀ",[
            ("math","A B=6",28,CYAN),
            ("math","S N=4",28,CYAN),
            ("math","A S=S B=5",28,GOLD),
            ("math","S S'=8",28,CYAN),
            ("text","Cáp đi từ A tới B' trên hai mái dốc.",18,INK),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","S M=4",29,CYAN),
            ("math","A M=M B'=sqrt(41)",27,INK),
            ("math","L_(min)=2 sqrt(41)",34,GOLD),
        ],CYAN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.96)

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
        h=header(16,title,progress); f=footer(); d=divider()
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
    forbidden=["workflow","render","preflight","engine","code","mã nguồn","camera","animation","cột trái","cột phải","debug"]
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


class TraiPhang16Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(roof_shell())
        for lab in roof_labels():
            self.add_fixed_orientation_mobjects(lab)
        card=intro_card(16,["MÁI NHÀ LĂNG TRỤ TAM GIÁC","DÂY CÁP QUA HAI MÁI DỐC"],"Mở hai mái quanh đường nóc để biến đường gấp thành đường thẳng.")
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)
        self.narrate("Ta quay lại một mô hình rất thực tế: mái nhà có tiết diện tam giác cân và kéo dài theo dạng lăng trụ.",1.7)
        self.narrate("Một sợi cáp cần đi từ mép mái bên trái ở đầu nhà tới mép mái bên phải ở cuối nhà, và toàn bộ sợi cáp phải nằm trên hai mặt mái.",1.9)

    def dimensions(self):
        self.clear_all(); self.add_hud("Tiết diện mái là tam giác 3 - 4 - 5","01 / 12")
        self.add_fixed_in_frame_mobjects(cross_section_diagram())
        card=lesson_card("TIẾT DIỆN TRƯỚC",[("math","A B=6",28,CYAN),("math","A N=N B=3",27,INK),("math","S N=4",28,CYAN),("math","A S=S B=5",31,GOLD)],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Chiều rộng ngôi nhà là sáu. Đường nóc nằm chính giữa nên mỗi nửa chiều rộng bằng ba.",1.6)
        self.narrate("Nóc cao hơn mép mái bốn đơn vị. Vì thế mỗi mái dốc có độ dài căn của ba bình phương cộng bốn bình phương, tức bằng năm.",1.8)

    def full_model(self):
        self.clear_all(); self.add_hud("Chiều dài ngôi nhà bằng 8","02 / 12"); self.add(roof_shell())
        card=lesson_card("MÔ HÌNH LĂNG TRỤ",[("math","A S=S B=5",28,GOLD),("math","S S'=8",29,CYAN),("text","Mỗi mái là một hình chữ nhật 5 × 8.",18,INK),("text","Điểm đầu A, điểm cuối B'.",18,GREEN)],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Ngôi nhà dài tám đơn vị. Vì vậy mỗi mặt mái là một hình chữ nhật có kích thước năm nhân tám.",1.6)
        self.narrate("Ta cần nối A ở mép mái trước bên trái với B phẩy ở mép mái sau bên phải.",1.5)

    def invalid_direct(self):
        self.clear_all(); self.add_hud("Nối thẳng trong không gian là không hợp lệ","03 / 12")
        self.add(roof_shell(),direct_chord(),Dot3D(W(RAW["A"]),radius=0.080,color=GREEN),Dot3D(W(RAW["B1"]),radius=0.080,color=RED))
        card=lesson_card("ĐOẠN THẲNG A B'",[("math","Delta x=6",28,RED),("math","Delta y=8",28,RED),("math","A B'=10",33,RED),("text","Nhưng đoạn này đi xuyên qua khoảng không dưới mái.",17,INK)],RED)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Nếu nối thẳng A với B phẩy trong không gian, ta có độ lệch ngang sáu và độ lệch dọc tám.",1.7)
        self.narrate("Độ dài chỉ bằng mười, nhưng đoạn này đi xuyên qua khoảng không dưới mái. Nó không nằm trên bề mặt mái nên không được phép.",1.8)

    def arbitrary_x(self):
        self.clear_all(); self.add_hud("Gọi X là điểm cáp vượt qua đường nóc","04 / 12"); self.add(roof_shell())
        X=RAW["S"]+0.63*(RAW["S1"]-RAW["S"])
        self.add(VGroup(solid(W(RAW["A"]),W(X),ORANGE,6.0),solid(W(X),W(RAW["B1"]),ORANGE,6.0),Dot3D(W(X),radius=0.065,color=ORANGE)))
        card=lesson_card("VỚI X THUỘC S S'",[("math","L(X)=A X+X B'",30,ORANGE),("text","AX nằm trên mái trái.",19,INK),("text","XB' nằm trên mái phải.",19,INK),("text","Ta cần chọn X tốt nhất.",19,CYAN)],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Gọi X là điểm mà sợi cáp vượt qua đường nóc S S phẩy.",1.4)
        self.narrate("Độ dài cáp bằng A X cộng X B phẩy. Muốn chọn X tốt nhất, ta mở hai mái ra quanh chính đường nóc.",1.7)

    def unfold(self):
        self.clear_all(); self.add_hud("Mở mái phải quanh đường nóc","05 / 12")
        left,right=unfold_mobs(); self.add(left,right)
        card=lesson_card("TRẢI HAI MÁI",[("text","Giữ mái trái.",19,INK),("text","Mở mái phải quanh S S'.",19,CYAN),("text","Đường nóc đứng yên.",19,GOLD),("text","Hai hình chữ nhật cùng nằm phẳng.",18,GREEN)],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Ta giữ mái trái và mở mái phải quanh đường nóc S S phẩy như mở một cánh cửa rất dài.",1.7)
        self.narrate_play("Khi mở xong, hai hình chữ nhật năm nhân tám nằm chung trên một mặt phẳng.",Rotate(right,angle=UNFOLD_ANGLE,axis=W(RAW["S1"])-W(RAW["S"]),about_point=W(RAW["S"])),min_time=3.0,rate_func=smooth)

    def net(self):
        self.clear_all(); self.add_hud("Hai mái ghép thành hình chữ nhật 10 × 8","06 / 12")
        net,_=net_rectangle(show_path=False); self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("BẢN TRẢI",[("text","Mái trái rộng 5.",19,PURPLE),("text","Mái phải rộng 5.",19,CYAN),("math","w=10",29,GOLD),("math","d=8",29,GOLD)],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Trên bản trải, hai mái ghép thành một hình chữ nhật có chiều ngang mười và chiều dọc tám.",1.6)
        self.narrate("Đường nóc chính là đường thẳng ở giữa, cách mỗi mép bên đúng năm đơn vị.",1.6)

    def straight_line(self):
        self.clear_all(); self.add_hud("Nối A với B' bằng đoạn thẳng","07 / 12")
        net,_=net_rectangle(show_path=True); self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("ĐƯỜNG NGẮN NHẤT TRÊN BẢN TRẢI",[("math","Delta x=10",29,CYAN),("math","Delta y=8",29,CYAN),("math","L^2=10^2+8^2",28,INK),("math","L=2 sqrt(41)",35,GOLD)],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Bây giờ bài toán trở thành rất quen thuộc. Giữa A và B phẩy trên mặt phẳng, đường ngắn nhất là đoạn thẳng.",1.7)
        self.narrate("Độ lệch ngang bằng mười, độ lệch dọc bằng tám. Theo Pythagore, độ dài cáp nhỏ nhất bằng hai căn bốn mươi mốt.",1.8)

    def ridge_crossing(self):
        self.clear_all(); self.add_hud("Sợi cáp cắt đường nóc ở đâu?","08 / 12")
        net,_=net_rectangle(show_path=True); self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("GIAO VỚI ĐƯỜNG NÓC",[("text","Đường nóc nằm tại x = 5.",18,INK),("text","AB' đi từ x = 0 đến x = 10.",18,INK),("text","Nên nó gặp nóc đúng ở nửa đường.",18,CYAN),("math","S M=M S'=4",31,GOLD)],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Đường nóc nằm đúng giữa bản trải, tại vị trí ngang bằng năm.",1.4)
        self.narrate("Đoạn A B phẩy đi từ mép ngang không tới mép ngang mười, nên nó cắt đường nóc đúng tại trung điểm M của S S phẩy.",1.8)
        self.narrate("Vì S S phẩy dài tám, ta có S M bằng M S phẩy bằng bốn.",1.5)

    def segment_lengths(self):
        self.clear_all(); self.add_hud("Hai đoạn trên hai mái có cùng độ dài","09 / 12")
        net,_=net_rectangle(show_path=True); self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("MỖI NỬA ĐƯỜNG CÁP",[("math","A M=sqrt(5^2+4^2)",27,PURPLE),("math","A M=sqrt(41)",31,GOLD),("math","M B'=sqrt(41)",31,CYAN),("math","L=2 sqrt(41)",34,GREEN)],GREEN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Từ A tới M, sợi cáp đi ngang trên bản trải năm đơn vị và đi dọc bốn đơn vị.",1.6)
        self.narrate("Vì vậy A M bằng căn bốn mươi mốt. Phần từ M tới B phẩy đối xứng nên cũng bằng căn bốn mươi mốt.",1.7)

    def fold_walk(self):
        self.clear_all(); self.add_hud("Gấp lại và đặt sợi cáp thật lên mái","10 / 12")
        route,pts=folded_route(); ant=Dot3D(W(pts[0]),radius=0.085,color=GREEN)
        self.add(roof_shell(),route,ant,Dot3D(W(pts[2]),radius=0.080,color=RED))
        card=lesson_card("ĐƯỜNG TRÊN MÁI NHÀ",[("text","A → M trên mái trái.",18,PURPLE),("text","M → B' trên mái phải.",18,CYAN),("math","S M=4",29,GOLD),("math","L_(min)=2 sqrt(41)",32,GREEN)],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate_play("Khi gấp mái lại, đoạn thẳng trên bản trải trở thành một đường gấp tại M trên đường nóc.",MoveAlongPath(ant,Line(W(pts[0]),W(pts[1]))),min_time=2.6,rate_func=linear)
        self.narrate_play("Từ M, sợi cáp tiếp tục trên mái phải tới B phẩy. Tổng chiều dài vẫn là hai căn bốn mươi mốt.",MoveAlongPath(ant,Line(W(pts[1]),W(pts[2]))),min_time=2.6,rate_func=linear)

    def compare_eds(self):
        self.clear_all(); self.add_hud("Đi men theo các cạnh có dài hơn không?","11 / 12"); self.add(roof_shell())
        edge_path=VGroup(solid(W(RAW["A"]),W(RAW["S"]),RED,4.8),solid(W(RAW["S"]),W(RAW["S1"]),RED,4.8),solid(W(RAW["S1"]),W(RAW["B1"]),RED,4.8))
        route,_=folded_route(); self.add(edge_path,route)
        card=lesson_card("SO SÁNH",[("math","L_e=5+8+5=18",27,RED),("math","L_(min)=2 sqrt(41)",31,GOLD),("math","2 sqrt(41)<18",29,GREEN),("text","Không cần bám theo các cạnh mái.",18,INK)],GREEN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Nếu đi men theo cạnh mái lên nóc, chạy dọc hết đường nóc rồi xuống phía bên kia, độ dài là mười tám.",1.8)
        self.narrate("Hai căn bốn mươi mốt nhỏ hơn mười tám. Đường ngắn nhất thực sự đi chéo qua cả hai mặt mái.",1.7)

    def general_formula(self):
        self.clear_all(); self.add_hud("Công thức tổng quát cho mái đối xứng","12 / 12"); self.add(roof_shell())
        card=lesson_card("GỌI NỬA RỘNG a, ĐỘ CAO h, CHIỀU DÀI d",[("math","s=sqrt(a^2+h^2)",25,CYAN),("math","L_(min)=sqrt((2s)^2+d^2)",25,GOLD),("math","L_(min)=sqrt(4(a^2+h^2)+d^2)",23,GREEN),("text","Điểm cắt nóc là trung điểm khi hai đầu đối xứng.",17,INK)],GREEN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate("Với mái đối xứng tổng quát, gọi nửa chiều rộng nhà là a, độ cao mái là h và chiều dài nhà là d.",1.8)
        self.narrate("Độ dài một mái dốc là căn của a bình phương cộng h bình phương. Sau khi trải, chiều ngang của hai mái là hai lần độ dài ấy.",1.9)
        self.narrate("Do đó chiều dài cáp nhỏ nhất bằng căn của bốn lần tổng a bình phương và h bình phương, cộng d bình phương. Trong cấu hình hai đầu đối xứng, cáp luôn cắt đường nóc tại trung điểm.",2.0)

    def construct(self):
        self.intro(); self.dimensions(); self.full_model(); self.invalid_direct(); self.arbitrary_x(); self.unfold(); self.net(); self.straight_line(); self.ridge_crossing(); self.segment_lengths(); self.fold_walk(); self.compare_eds(); self.general_formula()


class Smoke16(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.96)
        left,right=unfold_mobs(); self.add(left,right)
        self.play(Rotate(right,angle=UNFOLD_ANGLE,axis=W(RAW["S1"])-W(RAW["S"]),about_point=W(RAW["S"])),run_time=1.6,rate_func=smooth)
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854; config.pixel_height=480; config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR); config.output_file="trai_phang_16_master_smoke"; config.disable_caching=True
    scene=Smoke16(); scene.render()
    path=Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():
        raise RuntimeError(path)
    return path


def render_full():
    geometry_preflight(True); layout_preflight(layout_samples(),True)
    config.pixel_width=FINAL_WIDTH; config.pixel_height=FINAL_HEIGHT; config.frame_rate=FINAL_FPS
    config.media_dir=str(MEDIA_DIR); config.output_file="trai_phang_16_mai_nha_lang_tru_tam_giac_MASTER_1080p"; config.disable_caching=False
    scene=TraiPhang16Master(); scene.render()
    video_path=Path(scene.renderer.file_writer.movie_file_path); duration=probe_duration(video_path)
    master_wav=ROOT/"master_narration_trai_phang_16.wav"; build_master_audio(scene.audio_events,duration,master_wav)
    final_path=video_path.with_name(video_path.stem+"_WITH_AUDIO.mp4"); mux_audio(video_path,master_wav,final_path)
    print("VIDEO HOAN CHINH:",final_path)
    return final_path


if __name__=="__main__":
    source_path=Path(sys.argv[0]).resolve()
    if "--narration-lint" in sys.argv:
        narration_lint(source_path,True); raise SystemExit(0)
    if "--geometry-preflight" in sys.argv:
        geometry_preflight(True); raise SystemExit(0)
    if "--layout-preflight" in sys.argv:
        layout_preflight(layout_samples(),True); raise SystemExit(0)
    if "--smoke-render" in sys.argv:
        render_smoke(); raise SystemExit(0)
    render_full()

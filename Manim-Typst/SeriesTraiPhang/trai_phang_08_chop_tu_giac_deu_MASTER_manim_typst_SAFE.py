
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



# ---------- geometry engine: regular square pyramid ----------
# Regular square pyramid S.ABCD
# Base edge = 6, lateral edges = 5.
BASE = 6.0
LATERAL = 5.0
PYR_H = math.sqrt(7.0)

RAW = {
    "A": np.array([-3.0,-3.0,0.0]),
    "B": np.array([ 3.0,-3.0,0.0]),
    "C": np.array([ 3.0, 3.0,0.0]),
    "D": np.array([-3.0, 3.0,0.0]),
    "S": np.array([ 0.0, 0.0,PYR_H]),
}

FACES = {
    "f1": ["S","A","B"],   # SAB
    "f2": ["S","B","C"],   # SBC
    "f3": ["S","C","D"],   # SCD
    "f4": ["S","D","A"],   # SDA
}
FACE_COLORS = [PURPLE, CYAN, BLUE, ORANGE]

ROUTE_B = ["f1","f2"]
ROUTE_D = ["f4","f3"]
FAN_CHAIN = ["f1","f2","f3","f4"]

WORLD_SCALE = 0.76
WORLD_SHIFT = np.array([-3.23,-0.28,-0.10])


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


def shared_edge(f1,f2):
    common=[v for v in FACES[f1] if v in FACES[f2]]
    if len(common)!=2:
        raise ValueError(f"{f1}, {f2} are not adjacent")
    return common


def unfold_chain_numeric(chain):
    """Unfold a chain of triangular side faces into the plane of chain[0]."""
    fc={f:{v:RAW[v].copy() for v in FACES[f]} for f in chain}
    base=chain[0]
    base_pts=[fc[base][v] for v in FACES[base]]
    n0=face_normal(base_pts)
    plane_p=base_pts[0].copy()
    steps=[]

    for i in range(1,len(chain)):
        prev,cur=chain[i-1],chain[i]
        edge=shared_edge(prev,cur)
        a=fc[cur][edge[0]].copy()
        b=fc[cur][edge[1]].copy()
        axis=b-a

        n_cur=face_normal([fc[cur][v] for v in FACES[cur]])
        prev_cent=np.mean([fc[prev][v] for v in FACES[prev]],axis=0)

        trials=[]
        for target in (n0,-n0):
            ang=signed_angle_about_axis(n_cur,target,axis)
            test={v:rotate_point_axis(fc[cur][v],a,b,ang) for v in FACES[cur]}
            err=max(abs(np.dot(q-plane_p,n0)) for q in test.values())

            hv=b-a
            prev_side=np.dot(np.cross(hv,prev_cent-a),n0)
            cur_cent=np.mean(list(test.values()),axis=0)
            cur_side=np.dot(np.cross(hv,cur_cent-a),n0)
            opposite_penalty=0 if prev_side*cur_side<0 else 1

            trials.append((round(err,12),opposite_penalty,abs(ang),ang))

        trials.sort(key=lambda z:(z[0]>1e-8,z[1],z[2]))
        ang=trials[0][3]

        for j in range(i,len(chain)):
            f=chain[j]
            for v in FACES[f]:
                fc[f][v]=rotate_point_axis(fc[f][v],a,b,ang)

        steps.append({"index":i,"edge":edge,"a":a,"b":b,"angle":ang})

    return fc,steps,n0,plane_p


def plane_basis(chain,fc,n0):
    f=chain[0]
    p0=fc[f][FACES[f][0]].copy()
    e1=fc[f][FACES[f][1]]-p0
    e1=e1/np.linalg.norm(e1)
    e2=np.cross(n0,e1)
    e2=e2/np.linalg.norm(e2)
    return p0,e1,e2


def proj2(x,basis):
    p0,e1,e2=basis
    d=np.array(x)-p0
    return np.array([np.dot(d,e1),np.dot(d,e2)])


def seg_inter(P,Q,A,B,tol=1e-9):
    P,Q,A,B=map(lambda z:np.array(z,dtype=float),[P,Q,A,B])
    v=Q-P
    w=B-A
    M=np.array([[v[0],-w[0]],[v[1],-w[1]]],dtype=float)
    if abs(np.linalg.det(M))<1e-10:
        return None
    t,u=np.linalg.solve(M,A-P)
    if -tol<=t<=1+tol and -tol<=u<=1+tol:
        return float(t),float(u),P+t*v
    return None


def path_data(chain,start_vertex,end_vertex):
    fc,steps,n0,plane_p=unfold_chain_numeric(chain)
    basis=plane_basis(chain,fc,n0)

    P3=fc[chain[0]][start_vertex]
    Q3=fc[chain[-1]][end_vertex]
    P=proj2(P3,basis)
    Q=proj2(Q3,basis)

    hits=[]
    for i in range(len(chain)-1):
        edge=shared_edge(chain[i],chain[i+1])
        A2=proj2(fc[chain[i]][edge[0]],basis)
        B2=proj2(fc[chain[i]][edge[1]],basis)
        hit=seg_inter(P,Q,A2,B2)
        if hit is None:
            raise AssertionError(f"Path misses hinge {edge}")
        t,u,X2=hit
        if not (1e-8<t<1-1e-8 and 1e-8<u<1-1e-8):
            raise AssertionError(f"Hinge crossing not interior: {edge}, {t}, {u}")
        raw_a=RAW[edge[0]]
        raw_b=RAW[edge[1]]
        raw_x=raw_a+u*(raw_b-raw_a)
        hits.append({"edge":edge,"t":t,"u":u,"p2":X2,"raw":raw_x})

    return {
        "fc":fc,"steps":steps,"basis":basis,
        "P2":P,"Q2":Q,"Praw":RAW[start_vertex].copy(),"Qraw":RAW[end_vertex].copy(),
        "hits":hits,"length":float(np.linalg.norm(Q-P)),
    }


def rigid_preflight_chain(chain):
    before={f:[RAW[v].copy() for v in FACES[f]] for f in chain}
    fc,steps,n0,plane_p=unfold_chain_numeric(chain)
    for f in chain:
        after=[fc[f][v] for v in FACES[f]]
        if not np.allclose(pairwise_distances(before[f]),pairwise_distances(after),atol=1e-9,rtol=0):
            raise AssertionError(f"Face {f} distorted")
        if max(abs(np.dot(q-plane_p,n0)) for q in after)>1e-8:
            raise AssertionError(f"Face {f} not coplanar after unfolding")
    return True


def lateral_apex_angle():
    # In a 5-5-6 triangle: cos(phi)=(25+25-36)/(2*25)=7/25.
    return math.acos(7.0/25.0)


def midpoint_ab():
    return (RAW["A"]+RAW["B"])/2.0


def geometry_preflight(verbose=True):
    tol=1e-9

    # Base square and four equal lateral edges.
    for u,v in [("A","B"),("B","C"),("C","D"),("D","A")]:
        if abs(np.linalg.norm(RAW[u]-RAW[v])-BASE)>tol:
            raise AssertionError("Wrong base edge")
    for v in ["A","B","C","D"]:
        if abs(np.linalg.norm(RAW["S"]-RAW[v])-LATERAL)>tol:
            raise AssertionError("Wrong lateral edge")

    # Pyramid height check.
    if abs(PYR_H-math.sqrt(7.0))>tol:
        raise AssertionError("Wrong pyramid height")

    rigid_preflight_chain(ROUTE_B)
    rigid_preflight_chain(ROUTE_D)
    rigid_preflight_chain(FAN_CHAIN)

    db=path_data(ROUTE_B,"A","C")
    dd=path_data(ROUTE_D,"A","C")

    expected=48.0/5.0
    if abs(db["length"]-expected)>1e-8 or abs(dd["length"]-expected)>1e-8:
        raise AssertionError(("Wrong lateral path length",db["length"],dd["length"]))

    # Hinge parameter from S to B or D must be 7/25.
    if abs(db["hits"][0]["u"]-7.0/25.0)>1e-8:
        raise AssertionError(("Wrong point on SB",db["hits"][0]["u"]))
    if abs(dd["hits"][0]["u"]-7.0/25.0)>1e-8:
        raise AssertionError(("Wrong point on SD",dd["hits"][0]["u"]))

    # Folded length on actual faces.
    M=RAW["S"]+(7.0/25.0)*(RAW["B"]-RAW["S"])
    folded=np.linalg.norm(RAW["A"]-M)+np.linalg.norm(RAW["C"]-M)
    if abs(folded-expected)>1e-8:
        raise AssertionError("Folded route B length mismatch")

    # Face 5-5-6: slant altitude to AB is 4; area is 12.
    N=midpoint_ab()
    if abs(np.linalg.norm(RAW["S"]-N)-4.0)>1e-8:
        raise AssertionError("5-5-6 face altitude should be 4")
    area=0.5*BASE*4.0
    if abs(area-12.0)>tol:
        raise AssertionError("Face area should be 12")

    # Distance A to SB = 24/5, SM=7/5.
    AM=expected/2.0
    SM=np.linalg.norm(M-RAW["S"])
    if abs(AM-24.0/5.0)>tol or abs(SM-7.0/5.0)>tol:
        raise AssertionError("Wrong transition geometry")

    # Fan gap must be positive.
    phi=lateral_apex_angle()
    if not (4*phi < 2*math.pi):
        raise AssertionError("Fan should have a positive gap")

    # General formula check at a=6, l=5.
    general=(BASE/LATERAL)*math.sqrt(4*LATERAL**2-BASE**2)
    if abs(general-expected)>tol:
        raise AssertionError("General formula mismatch")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  square base edge 6, lateral edge 5, height sqrt(7)")
        print("  each side face is 5-5-6, altitude 4")
        print("  two symmetric lateral routes A->C")
        print("  transition point on SB/SD: S-distance 7/5")
        print("  Lmin on lateral surface = 48/5")
        print("  full four-face fan is coplanar with positive angular gap")
    return True


def solid(a,b,color=EDGE,width=4.0,opacity=0.96):
    return Line(np.array(a,float),np.array(b,float),
                color=color,stroke_width=width,stroke_opacity=opacity)


def hidden_edge(a,b,color=DIM,width=2.6,opacity=0.68):
    return DashedLine(np.array(a,float),np.array(b,float),
                      color=color,stroke_width=width,stroke_opacity=opacity,
                      dash_length=0.11,dashed_ratio=0.56)


def face_poly(points,color=BLUE,opacity=0.12):
    return Polygon(*[np.array(p,float) for p in points],
                   fill_color=color,fill_opacity=opacity,stroke_width=0)


def pyramid_shell():
    p={k:W(v) for k,v in RAW.items()}

    fills=VGroup(
        face_poly([p["S"],p["A"],p["B"]],PURPLE,0.075),
        face_poly([p["S"],p["B"],p["C"]],CYAN,0.090),
        face_poly([p["S"],p["C"],p["D"]],BLUE,0.045),
    )

    visible=[
        ("A","B"),("B","C"),
        ("S","A"),("S","B"),("S","C"),
    ]
    hidden=[
        ("C","D"),("D","A"),("S","D"),
    ]

    edges=VGroup(*[solid(p[u],p[v],EDGE,3.8) for u,v in visible])
    hidden_g=VGroup(*[hidden_edge(p[u],p[v]) for u,v in hidden])
    return VGroup(fills,edges,hidden_g)


def highlight_faces(face_names,opacity=0.17):
    g=VGroup()
    for i,f in enumerate(face_names):
        g.add(face_poly([W(RAW[v]) for v in FACES[f]],FACE_COLORS[i%len(FACE_COLORS)],opacity))
    return g


def vertex_labels(keys):
    offsets={
        "A":np.array([-0.15,-0.15,-0.06]),
        "B":np.array([0.15,-0.15,-0.06]),
        "C":np.array([0.15,0.14,-0.04]),
        "D":np.array([-0.15,0.14,-0.04]),
        "S":np.array([0.0,0.0,0.20]),
    }
    labs=VGroup()
    for k in keys:
        color=GREEN if k=="A" else (RED if k=="C" else INK)
        labs.add(mty(k,23,color).move_to(W(RAW[k])+offsets[k]))
    return labs


def face_mob(face_name,color,start_vertex=None,end_vertex=None):
    pts=[W(RAW[v]) for v in FACES[face_name]]
    poly=face_poly(pts,color,0.17)
    border=VGroup(*[
        solid(pts[i],pts[(i+1)%3],color,3.3) for i in range(3)
    ])
    g=VGroup(poly,border)
    if start_vertex is not None:
        g.add(Dot3D(W(RAW[start_vertex]),radius=0.075,color=GREEN))
    if end_vertex is not None:
        g.add(Dot3D(W(RAW[end_vertex]),radius=0.075,color=RED))
    return g


def make_chain_mobs(chain,start_vertex=None,end_vertex=None):
    mobs=[]
    for i,f in enumerate(chain):
        mobs.append(face_mob(
            f,FACE_COLORS[i%len(FACE_COLORS)],
            start_vertex if i==0 else None,
            end_vertex if i==len(chain)-1 else None
        ))
    return mobs


def unfold_animations(scene,chain,mobs,run_each=1.35):
    _,steps,_,_=unfold_chain_numeric(chain)
    for step in steps:
        i=step["index"]
        downstream=VGroup(*mobs[i:])
        a=W(step["a"]); b=W(step["b"])
        scene.play(
            Rotate(downstream,angle=step["angle"],axis=b-a,about_point=a),
            run_time=run_each,rate_func=smooth,
        )


def net_group(chain,start_vertex,end_vertex,width=5.8,height=4.9):
    d=path_data(chain,start_vertex,end_vertex)
    fc,basis=d["fc"],d["basis"]

    face2={}
    all2=[]
    for f in chain:
        arr=[proj2(fc[f][v],basis) for v in FACES[f]]
        face2[f]=arr
        all2+=arr

    all2=np.array(all2)
    minx,miny=all2.min(axis=0)
    maxx,maxy=all2.max(axis=0)
    scale=min(width/max(maxx-minx,1e-9),height/max(maxy-miny,1e-9))
    mid=np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p)-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    g=VGroup()
    for i,f in enumerate(chain):
        pts=[T(q) for q in face2[f]]
        g.add(Polygon(
            *pts,fill_color=FACE_COLORS[i%len(FACE_COLORS)],fill_opacity=0.16,
            stroke_color=FACE_COLORS[i%len(FACE_COLORS)],stroke_width=3.0
        ))

    P=T(d["P2"]); Q=T(d["Q2"])
    g.add(Dot(P,radius=0.075,color=GREEN))
    g.add(Dot(Q,radius=0.075,color=RED))
    g.add(Line(P,Q,color=GOLD,stroke_width=6.5))

    for h in d["hits"]:
        g.add(Dot(T(h["p2"]),radius=0.060,color=GOLD))

    return g,d,T


def folded_route_B():
    d=path_data(ROUTE_B,"A","C")
    M=d["hits"][0]["raw"]
    path=VGroup(
        solid(W(RAW["A"]),W(M),GOLD,6.5),
        solid(W(M),W(RAW["C"]),GOLD,6.5),
        Dot3D(W(M),radius=0.065,color=GOLD),
    )
    return path,[RAW["A"],M,RAW["C"]]


def folded_route_D():
    d=path_data(ROUTE_D,"A","C")
    M=d["hits"][0]["raw"]
    path=VGroup(
        solid(W(RAW["A"]),W(M),CYAN,5.5),
        solid(W(M),W(RAW["C"]),CYAN,5.5),
        Dot3D(W(M),radius=0.060,color=CYAN),
    )
    return path,[RAW["A"],M,RAW["C"]]


def full_fan_net():
    """Analytical fan of four congruent 5-5-6 side triangles."""
    phi=lateral_apex_angle()
    r=LATERAL
    pts=[]
    for k in range(5):
        ang=k*phi
        pts.append(np.array([r*math.cos(ang),r*math.sin(ang),0.0]))

    S2=np.array([0.0,0.0,0.0])

    allp=np.array([p[:2] for p in pts]+[[0.0,0.0]])
    minx,miny=allp.min(axis=0); maxx,maxy=allp.max(axis=0)
    scale=min(5.7/max(maxx-minx,1e-9),4.9/max(maxy-miny,1e-9))
    mid=np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p[:2])-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    S=T(S2)
    q=[T(p) for p in pts]

    g=VGroup()
    for i in range(4):
        g.add(Polygon(
            S,q[i],q[i+1],
            fill_color=FACE_COLORS[i],fill_opacity=0.14,
            stroke_color=FACE_COLORS[i],stroke_width=2.8
        ))

    # Route A->C via B: q0 to q2. Route via D: q4 to q2.
    g.add(Line(q[0],q[2],color=GOLD,stroke_width=5.8))
    g.add(Line(q[4],q[2],color=CYAN,stroke_width=5.0))
    g.add(Dot(S,radius=0.060,color=INK))
    g.add(Dot(q[0],radius=0.068,color=GREEN))
    g.add(Dot(q[2],radius=0.068,color=RED))
    g.add(Dot(q[4],radius=0.055,color=GREEN))

    # Small dashed indication of the fan gap between the two copies of A.
    g.add(DashedLine(q[0],q[4],color=DIM,stroke_width=2.0,dash_length=0.10))
    return g,{"S":S,"A0":q[0],"B":q[1],"C":q[2],"D":q[3],"A4":q[4],"phi":phi}


def face_triangle_2d():
    """Standalone 5-5-6 triangle SAB for area/altitude calculations."""
    a=BASE
    S=np.array([0.0,2.4,0.0])
    A=np.array([-2.8,-1.6,0.0])
    B=np.array([2.8,-1.6,0.0])
    N=(A+B)/2

    # This drawing is shape-correct up to uniform scaling:
    # horizontal half-base 3 and altitude 4.
    rawA=np.array([-3.0,0.0,0.0])
    rawB=np.array([3.0,0.0,0.0])
    rawS=np.array([0.0,4.0,0.0])
    pts=np.array([rawA[:2],rawB[:2],rawS[:2]])
    minx,miny=pts.min(axis=0); maxx,maxy=pts.max(axis=0)
    scale=min(5.5/(maxx-minx),4.5/(maxy-miny))
    mid=np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p[:2])-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    A2,B2,S2=map(T,[rawA,rawB,rawS])
    N2=(A2+B2)/2

    g=VGroup(
        Polygon(S2,A2,B2,fill_color=PURPLE,fill_opacity=0.15,
                stroke_color=PURPLE,stroke_width=3.0),
        Line(S2,N2,color=CYAN,stroke_width=4.0),
        Dot(N2,radius=0.055,color=CYAN),
    )
    return g,{"S":S2,"A":A2,"B":B2,"N":N2}


def layout_samples():
    return [
        lesson_card("BÀI TOÁN",[
            ("math","A B=6",28,CYAN),
            ("math","S A=S B=S C=S D=5",25,CYAN),
            ("text","Kiến đi từ A đến C trên các mặt bên.",19,INK),
            ("math","L_(min)=?",34,GOLD),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","S M=frac(7,5)",28,CYAN),
            ("math","A M=frac(24,5)",28,INK),
            ("math","L_(min)=frac(48,5)",34,GOLD),
        ],CYAN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.95)

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
        h=header(8,title,progress); f=footer(); d=divider()
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


class TraiPhang08Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(pyramid_shell())
        labs=vertex_labels(["S","A","B","C","D"])
        for lab in labs:
            self.add_fixed_orientation_mobjects(lab)

        card=intro_card(
            8,
            ["CHÓP TỨ GIÁC ĐỀU","MỞ MẶT BÊN KIỂU CÁNH QUẠT"],
            "Từ đỉnh A đến đỉnh C, chỉ được đi trên các mặt bên.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Ta chuyển sang hình chóp tứ giác đều. "
            "Đáy A B C D là hình vuông cạnh sáu, còn bốn cạnh bên S A, S B, S C, S D đều bằng năm.",
            1.8,
        )
        self.narrate(
            "Con kiến bắt đầu tại đỉnh A và muốn tới đỉnh đối diện C, nhưng chỉ được đi trên các mặt bên của hình chóp.",
            1.6,
        )

    def model_check(self):
        self.clear_all()
        self.add_hud("Mô hình 5 - 5 - 6","01 / 13")
        self.add(pyramid_shell(),highlight_faces(["f1","f2"],0.12))
        card=lesson_card("DỮ KIỆN HÌNH CHÓP",[
            ("math","A B=6",28,CYAN),
            ("math","S A=S B=S C=S D=5",25,CYAN),
            ("text","Mỗi mặt bên là tam giác cân 5 - 5 - 6.",18,INK),
            ("math","S O=sqrt(7)",27,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Vì tâm O của hình vuông cách mỗi đỉnh đáy một đoạn ba căn hai, nên từ tam giác vuông S O A ta có S O bằng căn bảy.",
            1.7,
        )
        self.narrate(
            "Mỗi mặt bên là một tam giác cân có hai cạnh bằng năm và đáy bằng sáu. "
            "Đây là cấu hình năm, năm, sáu rất thuận lợi để tính toán.",
            1.6,
        )

    def problem(self):
        self.clear_all()
        self.add_hud("Từ A đến C trên mặt bên","02 / 13")
        self.add(pyramid_shell())
        pathB,_=folded_route_B()
        pathD,_=folded_route_D()
        self.add(pathB,pathD)

        card=lesson_card("HAI HƯỚNG ĐỐI XỨNG",[
            ("text","Hướng qua B: mặt SAB rồi SBC.",19,GOLD),
            ("text","Hướng qua D: mặt SAD rồi SCD.",19,CYAN),
            ("text","Hai hướng đối xứng qua mặt phẳng SOC.",18,INK),
            ("text","Chỉ cần giải một hướng.",19,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Từ A tới C trên mặt bên có hai hướng tự nhiên. "
            "Một hướng đi qua hai mặt S A B và S B C; hướng kia đi qua S A D và S D C.",
            1.8,
        )
        self.narrate(
            "Do hình chóp đều, hai hướng đối xứng và có cùng độ dài. "
            "Ta chỉ cần giải hướng đi qua cạnh chung S B.",
            1.6,
        )

    def arbitrary_x(self):
        self.clear_all()
        self.add_hud("Gọi X là điểm đổi mặt trên SB","03 / 13")
        self.add(pyramid_shell(),highlight_faces(["f1","f2"],0.17))

        X=RAW["S"]+0.55*(RAW["B"]-RAW["S"])
        path=VGroup(
            solid(W(RAW["A"]),W(X),ORANGE,6.0),
            solid(W(X),W(RAW["C"]),ORANGE,6.0),
            Dot3D(W(X),radius=0.065,color=ORANGE),
        )
        self.add(path)

        card=lesson_card("VỚI X THUỘC SB",[
            ("math","L(X)=A X+X C",31,ORANGE),
            ("text","AX nằm trên mặt SAB.",19,INK),
            ("text","XC nằm trên mặt SBC.",19,INK),
            ("text","Ta cần chọn X tốt nhất.",19,CYAN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Gọi X là điểm mà kiến chuyển từ mặt S A B sang mặt S B C. "
            "Khi đó độ dài đường đi là A X cộng X C.",
            1.6,
        )
        self.narrate(
            "Thay vì tìm X trực tiếp trên hình không gian, ta mở hai tam giác qua cạnh chung S B.",
            1.5,
        )

    def unfold_two_faces(self):
        self.clear_all()
        self.add_hud("Mở hai mặt quanh cạnh SB","04 / 13")
        mobs=make_chain_mobs(ROUTE_B,"A","C")
        self.add(*mobs)

        card=lesson_card("MỞ HAI MẶT",[
            ("text","Giữ mặt SAB.",19,INK),
            ("text","Mở mặt SBC quanh cạnh SB.",19,CYAN),
            ("text","Điểm C đi theo chính mặt SBC.",19,INK),
            ("text","Hai tam giác 5 - 5 - 6 nằm phẳng.",18,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta giữ mặt S A B và mở mặt S B C quanh cạnh S B. "
            "Điểm C đi theo mặt S B C cho đến khi hai tam giác nằm trên cùng một mặt phẳng.",
            1.8,
        )
        unfold_animations(self,ROUTE_B,mobs,run_each=2.1)
        self.narrate(
            "Ta gọi ảnh của C sau khi mở là C một. "
            "Bài toán lúc này là tìm đường ngắn nhất từ A tới C một.",
            1.5,
        )

    def net_symmetry(self):
        self.clear_all()
        self.add_hud("Hai tam giác đối xứng qua SB","05 / 13")
        net,d,T=net_group(ROUTE_B,"A","C")
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("TRÊN BẢN TRẢI",[
            ("text","A và C₁ đối xứng qua SB.",19,INK),
            ("text","AC₁ vuông góc SB.",19,CYAN),
            ("text","Gọi M = AC₁ cắt SB.",19,GOLD),
            ("text","M không phải trung điểm SB.",19,RED),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hai tam giác S A B và S B C một bằng nhau và nằm ở hai phía của S B. "
            "Vì vậy A và C một đối xứng nhau qua S B.",
            1.7,
        )
        self.narrate(
            "Đoạn thẳng A C một vuông góc S B tại M. "
            "Khác bài tứ diện đều trước đó, M không phải là trung điểm của S B.",
            1.6,
        )

    def face_556(self):
        self.clear_all()
        self.add_hud("Khai thác tam giác 5 - 5 - 6","06 / 13")
        tri,pts=face_triangle_2d()
        self.add_fixed_in_frame_mobjects(tri)

        card=lesson_card("TRONG TAM GIÁC SAB",[
            ("math","S A=S B=5",27,CYAN),
            ("math","A B=6",28,CYAN),
            ("math","A N=N B=3",27,INK),
            ("math","S N=4",30,GOLD),
            ("math","K=frac(1,2) times 6 times 4=12",25,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Gọi N là trung điểm của A B. Vì tam giác S A B cân, S N vuông góc A B.",
            1.5,
        )
        self.narrate(
            "Ta có A N bằng ba, S A bằng năm, nên tam giác vuông S N A là bộ ba, bốn, năm. "
            "Suy ra S N bằng bốn.",
            1.7,
        )
        self.narrate(
            "Diện tích tam giác S A B vì thế bằng một nửa nhân sáu nhân bốn, tức bằng mười hai.",
            1.5,
        )

    def transition_point(self):
        self.clear_all()
        self.add_hud("Tìm chính xác điểm M trên SB","07 / 13")
        net,d,T=net_group(ROUTE_B,"A","C")
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("DÙNG DIỆN TÍCH",[
            ("math","K=frac(1,2) times S B times A M",25,INK),
            ("math","12=frac(1,2) times 5 times A M",25,INK),
            ("math","A M=frac(24,5)",31,GOLD),
            ("math","S M=frac(7,5)",31,CYAN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "M chính là chân đường vuông góc từ A xuống S B. "
            "Ta tính A M bằng cách dùng lại diện tích của tam giác S A B.",
            1.6,
        )
        self.narrate(
            "Mười hai bằng một nửa nhân S B, tức năm, nhân A M. "
            "Vì vậy A M bằng hai mươi bốn phần năm.",
            1.6,
        )
        self.narrate(
            "Trong tam giác vuông A M S, S A bằng năm. "
            "Từ định lý Pythagore suy ra S M bằng bảy phần năm.",
            1.6,
        )

    def length_result(self):
        self.clear_all()
        self.add_hud("Độ dài ngắn nhất qua hai mặt","08 / 13")
        net,d,T=net_group(ROUTE_B,"A","C")
        self.add_fixed_in_frame_mobjects(net)

        card=lesson_card("KẾT QUẢ HƯỚNG QUA B",[
            ("math","A M=M C_1=frac(24,5)",28,INK),
            ("math","A C_1=frac(48,5)",34,GOLD),
            ("math","L_(min)=frac(48,5)",35,GREEN),
            ("text","Điểm đổi mặt: SM = 7/5.",19,CYAN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Do A và C một đối xứng qua S B, ta có M C một bằng A M, cũng bằng hai mươi bốn phần năm.",
            1.5,
        )
        self.narrate(
            "Vì thế A C một bằng bốn mươi tám phần năm. "
            "Đây là độ dài nhỏ nhất theo hướng đi qua hai mặt S A B và S B C.",
            1.7,
        )

    def compare_base(self):
        self.clear_all()
        self.add_hud("Nếu được đi trên đáy thì sao?","09 / 13")
        self.add(pyramid_shell())
        p={k:W(v) for k,v in RAW.items()}
        self.add(solid(p["A"],p["C"],RED,6.5))
        path,_=folded_route_B()
        self.add(path)

        card=lesson_card("RÀNG BUỘC RẤT QUAN TRỌNG",[
            ("math","A C=6 sqrt(2)",29,RED),
            ("math","L_(side)=frac(48,5)",29,GOLD),
            ("math","6 sqrt(2)<frac(48,5)",27,GREEN),
            ("text","Vì bài yêu cầu chỉ đi trên các mặt bên.",18,INK),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu kiến được phép đi trên mặt đáy, nó chỉ cần đi theo đường chéo A C của hình vuông, dài sáu căn hai.",
            1.6,
        )
        self.narrate(
            "Sáu căn hai nhỏ hơn bốn mươi tám phần năm. "
            "Vì thế điều kiện chỉ được đi trên các mặt bên là điều kiện quyết định của bài toán.",
            1.7,
        )

    def full_fan(self):
        self.clear_all()
        self.add_hud("Mở cả bốn mặt bên thành một cánh quạt","10 / 13")
        fan,pts=full_fan_net()
        self.add_fixed_in_frame_mobjects(fan)

        card=lesson_card("BẢN TRẢI CÁNH QUẠT",[
            ("math","cos phi=frac(7,25)",28,CYAN),
            ("text","Mỗi tam giác có góc đỉnh φ tại S.",18,INK),
            ("math","4 phi<2 pi",29,GOLD),
            ("text","Vì vậy bản trải còn một khe hở.",18,INK),
            ("text","Hai đường A→C đối xứng hiện cùng lúc.",18,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu cắt một cạnh bên rồi mở cả bốn mặt, ta thu được một hình cánh quạt gồm bốn tam giác năm, năm, sáu cùng gặp tại S.",
            1.8,
        )
        self.narrate(
            "Góc ở đỉnh S của mỗi tam giác có cos bằng bảy phần hai mươi lăm. "
            "Tổng bốn góc vẫn nhỏ hơn một vòng tròn, nên bản trải còn một khe hở.",
            1.8,
        )
        self.narrate(
            "Trên cánh quạt này, hai hướng từ A tới C qua B hoặc qua D xuất hiện đối xứng và có cùng độ dài.",
            1.6,
        )

    def fold_and_walk(self):
        self.clear_all()
        self.add_hud("Gấp lại và cho kiến đi thật","11 / 13")
        path,pts=folded_route_B()
        self.add(pyramid_shell(),highlight_faces(["f1","f2"],0.17),path)

        ant=Dot3D(W(pts[0]),radius=0.085,color=GREEN)
        self.add(ant)

        card=lesson_card("ĐƯỜNG TRÊN HÌNH CHÓP",[
            ("text","Đường đi: A → M → C.",19,GOLD),
            ("math","S M=frac(7,5)",28,CYAN),
            ("math","A M=M C=frac(24,5)",27,INK),
            ("math","L_(min)=frac(48,5)",33,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Kiến đi từ A tới M trên mặt S A B. M nằm trên cạnh S B và cách S một đoạn bảy phần năm.",
            MoveAlongPath(ant,Line(W(pts[0]),W(pts[1]))),
            min_time=2.2,rate_func=linear,
        )
        self.narrate_play(
            "Tại M, kiến chuyển sang mặt S B C rồi đi thẳng tới C.",
            MoveAlongPath(ant,Line(W(pts[1]),W(pts[2]))),
            min_time=2.0,rate_func=linear,
        )

    def general_formula(self):
        self.clear_all()
        self.add_hud("Công thức tổng quát cho chóp đều","12 / 13")
        self.add(pyramid_shell())

        card=lesson_card("GỌI CẠNH ĐÁY a, CẠNH BÊN l",[
            ("math","K=frac(a,4) sqrt(4l^2-a^2)",25,INK),
            ("math","d(A,S B)=frac(a sqrt(4l^2-a^2),2l)",24,CYAN),
            ("math","L=frac(a sqrt(4l^2-a^2),l)",27,GOLD),
            ("math","S M=l-frac(a^2,2l)",27,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Kết quả vừa làm không chỉ đúng với số sáu và năm. "
            "Với chóp tứ giác đều có cạnh đáy a và cạnh bên l, hai mặt kề vẫn là hai tam giác cân bằng nhau.",
            1.8,
        )
        self.narrate(
            "Trải hai mặt qua cạnh chung, hai đỉnh đối diện nhau qua cạnh ấy. "
            "Từ diện tích tam giác cân, ta thu được độ dài đường đi bằng a nhân căn bốn l bình phương trừ a bình phương, rồi chia cho l.",
            2.0,
        )
        self.narrate(
            "Điểm đổi mặt cách S một đoạn l trừ a bình phương chia hai l. "
            "Thay a bằng sáu và l bằng năm, ta trở lại S M bằng bảy phần năm và độ dài bốn mươi tám phần năm.",
            1.8,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài chóp tứ giác đều","13 / 13")
        self.add(pyramid_shell(),highlight_faces(["f1","f2"],0.13))

        card=lesson_card("BỐN Ý CẦN NHỚ",[
            ("text","1. A→C trên mặt bên có hai hướng đối xứng.",18,INK),
            ("text","2. Mở hai tam giác qua cạnh chung.",18,INK),
            ("text","3. Điểm đổi mặt không nhất thiết là trung điểm.",18,INK),
            ("math","S M=frac(7,5)",27,CYAN),
            ("math","L_(min)=frac(48,5)",33,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Bài chóp tứ giác đều cho ta một bước tiến mới: bản trải là các tam giác cân ghép thành cánh quạt, không còn là dải chữ nhật.",
            1.7,
        )
        self.narrate(
            "Và quan trọng hơn, điểm đổi mặt không nhất thiết là trung điểm. "
            "Trong mô hình năm, năm, sáu này, điểm tối ưu trên S B cách S đúng bảy phần năm.",
            1.7,
        )
        self.narrate(
            "Đường ngắn nhất từ A tới C khi chỉ đi trên các mặt bên có độ dài bốn mươi tám phần năm.",
            1.4,
        )

    def construct(self):
        self.intro()
        self.model_check()
        self.problem()
        self.arbitrary_x()
        self.unfold_two_faces()
        self.net_symmetry()
        self.face_556()
        self.transition_point()
        self.length_result()
        self.compare_base()
        self.full_fan()
        self.fold_and_walk()
        self.general_formula()
        self.summary()


class Smoke08(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.95)

        # Smoke 1: two-face unfolding.
        mobs=make_chain_mobs(ROUTE_B,"A","C")
        self.add(*mobs)
        unfold_animations(self,ROUTE_B,mobs,run_each=0.65)
        self.wait(0.1)

        # Smoke 2: full four-face fan unfolding.
        self.clear()
        mobs=make_chain_mobs(FAN_CHAIN,"A",None)
        self.add(*mobs)
        unfold_animations(self,FAN_CHAIN,mobs,run_each=0.38)
        self.wait(0.1)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_08_master_smoke"
    config.disable_caching=True

    scene=Smoke08()
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
    config.output_file="trai_phang_08_chop_tu_giac_deu_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang08Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_08.wav"
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

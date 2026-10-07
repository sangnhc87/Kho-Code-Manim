
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










# ---------- geometry engine: one forbidden face ----------
# Rectangular box 8 x 5 x 4.
# P=(2,0,3) on the front face; Q=(6,5,3) on the back face.
# The top face z=4 is forbidden (its interior and all paths through it).
# Legal routes can use the other five faces, including their edges.
#
# Without the restriction: front -> top -> back:
#   developed displacement (dx,dy) = (4, 1+5+1) = (4,7)
#   L_top = sqrt(65), but this route crosses the FORBIDDEN top.
#
# Valid replacement: front -> bottom -> back:
#   developed displacement (dx,dy) = (4, 3+5+3) = (4,11)
#   L_bottom = sqrt(137)
#   crosses front-bottom at x=34/11,
#   crosses bottom-back at x=54/11.
#
# Alternative three-face routes front -> left/right -> back:
#   L_left = L_right = 13.
# Exhaustive preflight checks all simple adjacent face strips that avoid top,
# including four-face chains; the best is sqrt(137).

BOX_X=8.0
BOX_Y=5.0
BOX_Z=4.0
P_RAW=np.array([2.0,0.0,3.0])
Q_RAW=np.array([6.0,BOX_Y,3.0])
V={
    'A': np.array([0.0,0.0,0.0]),
    'B': np.array([BOX_X,0.0,0.0]),
    'C': np.array([BOX_X,BOX_Y,0.0]),
    'D': np.array([0.0,BOX_Y,0.0]),
    'E': np.array([0.0,0.0,BOX_Z]),
    'F': np.array([BOX_X,0.0,BOX_Z]),
    'G': np.array([BOX_X,BOX_Y,BOX_Z]),
    'H': np.array([0.0,BOX_Y,BOX_Z]),
}
FACES={
    'front':['A','B','F','E'],
    'right':['B','C','G','F'],
    'back':['D','H','G','C'],
    'left':['A','E','H','D'],
    'bottom':['A','D','C','B'],
    'top':['E','F','G','H'],
}
ALLOWED={'front','back','left','right','bottom'}
FACE_COLORS={
    'front':PURPLE,'back':CYAN,'bottom':BLUE,
    'left':ORANGE,'right':GREEN,'top':RED,
}
TOP_CHAIN=['front','top','back']
BOTTOM_CHAIN=['front','bottom','back']
LEFT_CHAIN=['front','left','back']
RIGHT_CHAIN=['front','right','back']
WORLD_SCALE=0.59
WORLD_SHIFT=np.array([-3.25,-0.25,-0.30])
CAM_PHI=67*DEGREES
CAM_THETA=-44*DEGREES


def W(p):
    return WORLD_SCALE*np.array(p,dtype=float)+WORLD_SHIFT


def rotate_point_axis(p,a,b,t):
    p=np.array(p,dtype=float); a=np.array(a,dtype=float); b=np.array(b,dtype=float)
    k=b-a; k=k/np.linalg.norm(k); x=p-a
    return a+x*math.cos(t)+np.cross(k,x)*math.sin(t)+k*np.dot(k,x)*(1-math.cos(t))


def face_normal(points):
    a,b,c=map(lambda p:np.array(p,dtype=float),points[:3])
    n=np.cross(b-a,c-a)
    return n/np.linalg.norm(n)


def shared_edge(f,g):
    e=[p for p in FACES[f] if p in FACES[g]]
    if len(e)!=2:
        raise ValueError(f'Faces not adjacent: {f}, {g}')
    return e


def pairwise_distances(points):
    return sorted(float(np.linalg.norm(points[i]-points[j]))
                  for i in range(len(points)) for j in range(i+1,len(points)))


def planar_hinge_intersection(P,Q,U,Vv):
    d=Q-P; w=Vv-U
    m=np.array([[d[0],-w[0]],[d[1],-w[1]]],dtype=float)
    if abs(np.linalg.det(m))<1e-10:
        return None
    t,u=np.linalg.solve(m,U-P)
    if 1e-8<t<1-1e-8 and 1e-8<u<1-1e-8:
        return float(t),float(u)
    return None


def unfold_chain(chain):
    """Exact rigid downstream rotations and planar straight-line crossings."""
    fc={f:{v:V[v].copy() for v in FACES[f]} for f in chain}
    fc[chain[0]]['START']=P_RAW.copy()
    fc[chain[-1]]['END']=Q_RAW.copy()

    root=chain[0]
    root0=fc[root][FACES[root][0]].copy()
    n0=face_normal([fc[root][v] for v in FACES[root]])
    steps=[]
    for i in range(1,len(chain)):
        prev,cur=chain[i-1:i+1]
        edge=shared_edge(prev,cur)
        a,b=fc[cur][edge[0]].copy(),fc[cur][edge[1]].copy()
        axis=(b-a)/np.linalg.norm(b-a)
        mn=face_normal([fc[cur][v] for v in FACES[cur]])
        pc=np.mean([fc[prev][v] for v in FACES[prev]],axis=0)
        side1=np.dot(np.cross(b-a,pc-a),n0)
        opts=[]
        for target in (n0,-n0):
            angle=math.atan2(np.dot(axis,np.cross(mn,target)),np.dot(mn,target))
            transformed={v:rotate_point_axis(p,a,b,angle) for v,p in fc[cur].items()}
            err=max(abs(np.dot(p-root0,n0)) for p in transformed.values())
            cc=np.mean([transformed[v] for v in FACES[cur]],axis=0)
            side2=np.dot(np.cross(b-a,cc-a),n0)
            opts.append(((err>1e-7,side1*side2>=-1e-9,abs(angle)),angle))
        angle=min(opts,key=lambda z:z[0])[1]
        for downstream in chain[i:]:
            fc[downstream]={v:rotate_point_axis(p,a,b,angle)
                            for v,p in fc[downstream].items()}
        steps.append({'i':i,'a':a,'b':b,'angle':angle,'edge':edge})

    ex=fc[root][FACES[root][1]]-root0
    ex=ex/np.linalg.norm(ex)
    ey=np.cross(n0,ex)
    def project(p):
        v=p-root0
        return np.array([np.dot(v,ex),np.dot(v,ey)])
    P=project(fc[root]['START'])
    Q=project(fc[chain[-1]]['END'])
    hits=[]
    for i in range(len(chain)-1):
        e=shared_edge(chain[i],chain[i+1])
        U=project(fc[chain[i]][e[0]])
        Vv=project(fc[chain[i]][e[1]])
        h=planar_hinge_intersection(P,Q,U,Vv)
        if h is None:return None
        t,u=h
        point_raw=V[e[0]]+u*(V[e[1]]-V[e[0]])
        hits.append({'edge':e,'t':t,'u':u,'raw':point_raw,'flat':P+t*(Q-P)})
    if any(hits[i]['t']>=hits[i+1]['t'] for i in range(len(hits)-1)):
        return None
    return {'fc':fc,'steps':steps,'P2':P,'Q2':Q,'hits':hits,
            'length':float(np.linalg.norm(Q-P)),'n':n0,'origin':root0}


def enumerate_routes(allowed=ALLOWED):
    adjacent={f:[g for g in allowed if g!=f and len(set(FACES[f])&set(FACES[g]))==2]
              for f in allowed}
    paths=[]
    def dfs(current,chain):
        if current=='back':
            data=unfold_chain(chain)
            if data is not None:
                paths.append((data['length'],list(chain),data))
            return
        for nxt in adjacent[current]:
            if nxt not in chain:
                dfs(nxt,chain+[nxt])
    dfs('front',['front'])
    return sorted(paths,key=lambda p:p[0])


def geometry_preflight(verbose=True):
    tol=1e-8
    # Dimensions and all 12 box edges.
    for f,vs in FACES.items():
        n=face_normal([V[v] for v in vs])
        if abs(np.linalg.norm(n)-1.0)>tol:raise AssertionError(f)
    free=enumerate_routes(set(FACES))
    legal=enumerate_routes(ALLOWED)
    if not free or not legal:raise AssertionError('Missing valid face-strip paths')
    if abs(free[0][0]-math.sqrt(65))>tol:raise AssertionError('Free optimum mismatch')
    if free[0][1]!=TOP_CHAIN:raise AssertionError(('Free route wrong',free[0][1]))
    if abs(legal[0][0]-math.sqrt(137))>tol:raise AssertionError('Constrained optimum mismatch')
    if legal[0][1]!=BOTTOM_CHAIN:raise AssertionError(('Allowed route wrong',legal[0][1]))
    if abs(unfold_chain(LEFT_CHAIN)['length']-13)>tol:raise AssertionError('Left wrong')
    if abs(unfold_chain(RIGHT_CHAIN)['length']-13)>tol:raise AssertionError('Right wrong')

    for seq in [TOP_CHAIN,BOTTOM_CHAIN,LEFT_CHAIN,RIGHT_CHAIN]:
        data=unfold_chain(seq)
        for f in seq:
            before=[V[v] for v in FACES[f]]
            after=[data['fc'][f][v] for v in FACES[f]]
            if not np.allclose(pairwise_distances(before),pairwise_distances(after),atol=tol,rtol=0):
                raise AssertionError('Unfolding distorted '+f)
            if any(abs(np.dot(p-data['origin'],data['n']))>tol for p in after):
                raise AssertionError('Not coplanar '+f)
        coords=[P_RAW]+[h['raw'] for h in data['hits']]+[Q_RAW]
        folded=sum(np.linalg.norm(b-a) for a,b in zip(coords,coords[1:]))
        if abs(folded-data['length'])>tol:
            raise AssertionError('Fold/unfold length mismatch')

    bottom=unfold_chain(BOTTOM_CHAIN)
    top=unfold_chain(TOP_CHAIN)
    b1,b2=(h['raw'] for h in bottom['hits'])
    if abs(b1[0]-34.0/11.0)>tol or abs(b2[0]-54.0/11.0)>tol:
        raise AssertionError('Wrong bottom crossing positions')
    if abs(bottom['hits'][0]['t']-3/11)>tol or abs(bottom['hits'][1]['t']-8/11)>tol:
        raise AssertionError('Wrong path crossing fractions')
    if not all(len(set(seq)&{'top'})==0 for _,seq,_ in legal):
        raise AssertionError('Forbidden face leaked')
    if verbose:
        print('GEOMETRY PREFLIGHT OK')
        print('  box 8x5x4, start front P=(2,0,3), end back Q=(6,5,3)')
        print('  forbidden face: TOP (z=4)')
        print('  free optimum: front-top-back, sqrt(65)')
        print('  allowed optimum: front-bottom-back, sqrt(137)')
        print('  left and right alternatives: 13')
        print('  bottom crossing x positions: 34/11, 54/11')
        print(f'  enumerated simple valid routes: {len(free)} before ban, {len(legal)} after ban')
        print('  rigid face distances, coplanarity and folded paths verified')
    return True


def solid(a,b,color=EDGE,width=3.5,opacity=1):
    return Line(np.array(a,float),np.array(b,float),color=color,
                stroke_width=width,stroke_opacity=opacity)


def dashed(a,b,color=DIM,width=2.5):
    return DashedLine(np.array(a,float),np.array(b,float),color=color,
                      stroke_width=width,dash_length=0.11,dashed_ratio=0.55)


def plane_face(f,opacity=0.1):
    color=FACE_COLORS[f]
    return Polygon(*[W(V[v]) for v in FACES[f]],
                   fill_color=color,fill_opacity=opacity,
                   stroke_color=color,stroke_width=1.4,stroke_opacity=0.55)


def box_shell(mark_forbidden=True):
    faces=VGroup(plane_face('front',0.07),plane_face('right',0.07),
                 plane_face('back',0.035),plane_face('left',0.035),
                 plane_face('bottom',0.055),plane_face('top',0.15 if mark_forbidden else 0.035))
    edges=VGroup()
    for names in [('A','B'),('B','C'),('C','D'),('D','A'),
                  ('E','F'),('F','G'),('G','H'),('H','E'),
                  ('A','E'),('B','F'),('C','G'),('D','H')]:
        u,v=names
        color=RED if mark_forbidden and u in 'EFGH' and v in 'EFGH' else EDGE
        edges.add(solid(W(V[u]),W(V[v]),color,2.7))
    return VGroup(faces,edges)


def endpoint_dots():
    return VGroup(Dot3D(W(P_RAW),radius=0.083,color=GREEN),
                  Dot3D(W(Q_RAW),radius=0.083,color=RED))


def folded_route(chain,color=GOLD):
    d=unfold_chain(chain)
    if d is None:raise ValueError(chain)
    p=[P_RAW]+[h['raw'] for h in d['hits']]+[Q_RAW]
    group=VGroup(*[solid(W(a),W(b),color,5.2)
                   for a,b in zip(p,p[1:])])
    for point in p[1:-1]:
        group.add(Dot3D(W(point),radius=0.065,color=color))
    return group,p


def route_face_objects(chain,color=GOLD):
    d=unfold_chain(chain)
    xyz=[P_RAW]+[h['raw'] for h in d['hits']]+[Q_RAW]
    objects=[]
    for i,f in enumerate(chain):
        verts=[W(V[v]) for v in FACES[f]]
        border=VGroup(*[solid(verts[j],verts[(j+1)%4],FACE_COLORS[f],2.5)
                         for j in range(4)])
        face=Polygon(*verts,fill_color=FACE_COLORS[f],fill_opacity=0.13,
                     stroke_width=0)
        line=solid(W(xyz[i]),W(xyz[i+1]),color,5.0)
        objects.append(VGroup(face,border,line))
    return objects,d


def net_diagram(kind='bottom',show_path=True,show_numbers=False):
    # Whole faces, not clipped to the useful path.
    # Both nets span 8 by 13 in exact length units.
    # Top: front y=0..4, top 4..9, back 9..13, P=(2,3), Q=(6,10).
    # Bottom: back y=-9..-5, bottom -5..0, front 0..4,
    #         P=(2,3), Q=(6,-8).
    if kind=='top':
        rects=[('front',0,4),('top',4,9),('back',9,13)]
        y0,y1=0,13
        P2=np.array([2.,3.]);Q2=np.array([6.,10.]);hinges=[4,9]
        path_color=RED
    else:
        rects=[('back',-9,-5),('bottom',-5,0),('front',0,4)]
        y0,y1=-9,4
        P2=np.array([2.,3.]);Q2=np.array([6.,-8.]);hinges=[0,-5]
        path_color=GOLD
    sc=min(5.6/BOX_X,5.02/(y1-y0))
    center_y=(y0+y1)/2
    def T(x,y):
        return np.array([LEFT_CENTER[0]+sc*(x-4),
                         LEFT_CENTER[1]+sc*(y-center_y),0.])
    g=VGroup()
    for name,lo,hi in rects:
        g.add(Polygon(T(0,lo),T(8,lo),T(8,hi),T(0,hi),
                      fill_color=FACE_COLORS[name],
                      fill_opacity=0.26 if name=='top' else 0.105,
                      stroke_color=RED if name=='top' else FACE_COLORS[name],
                      stroke_width=3.2 if name=='top' else 2.3))
    for h in hinges:
        g.add(Line(T(0,h),T(8,h),color=GOLD,stroke_width=3.1))
    P=T(*P2);Q=T(*Q2)
    g.add(Dot(P,radius=0.071,color=GREEN),Dot(Q,radius=0.071,color=RED))
    if show_path:
        g.add(Line(P,Q,color=path_color,stroke_width=6.1))
        dx=Q2[0]-P2[0];dy=Q2[1]-P2[1]
        for h in hinges:
            frac=(h-P2[1])/dy
            g.add(Dot(T(P2[0]+frac*dx,h),radius=0.055,color=GOLD))
    return g,{'P':P,'Q':Q,'T':T,'hinges':hinges,'P2':P2,'Q2':Q2}


def comparison_bars():
    vals=[('Nắp trên (cấm)',math.sqrt(65),RED),
          ('Qua đáy',math.sqrt(137),GOLD),
          ('Qua mặt trái',13,ORANGE),
          ('Qua mặt phải',13,CYAN)]
    left=LEFT_CENTER[0]-2.65
    g=VGroup()
    for i,(lab,value,color) in enumerate(vals):
        y=1.78-1.15*i
        title=txt(lab,20,INK)
        title.move_to(np.array([left+1.2,y+0.31,0]))
        bg=Rectangle(width=4.7,height=0.16,
                     stroke_width=0,fill_color=GRID,fill_opacity=0.6)
        bg.move_to([left+2.35,y-0.07,0])
        fill=Rectangle(width=4.7*value/14.2,height=0.16,
                       stroke_width=0,fill_color=color,fill_opacity=0.9)
        fill.move_to([left+2.35-4.7/2+fill.width/2,y-0.07,0])
        g.add(title,bg,fill)
    return g


def layout_samples():
    return [
        lesson_card('MỘT MẶT BỊ CẤM',[
            ('math','8 times 5 times 4',28,CYAN),
            ('text','P trên mặt trước, Q trên mặt sau.',18,INK),
            ('text','Không được đi trên nắp trên.',19,RED),
            ('math','L_(min)=?',35,GOLD),
        ],RED),
        lesson_card('KẾT QUẢ',[
            ('math','L_1=sqrt(65)',29,RED),
            ('math','L_2=sqrt(137)',29,GOLD),
            ('math','L_3=L_4=13',25,CYAN),
            ('math','sqrt(137)<13',28,GREEN),
        ],GOLD),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.94)

    def narrate(self,text,min_visual_time=1.0):
        sound=create_audio(text);duration=probe_duration(sound)
        self.audio_events.append((self.time,sound))
        self.wait(max(duration,min_visual_time))
        return duration

    def narrate_play(self,text,*animations,min_time=1.0,rate_func=smooth):
        sound=create_audio(text);duration=probe_duration(sound)
        self.audio_events.append((self.time,sound))
        self.play(*animations,run_time=max(duration,min_time),rate_func=rate_func)
        return duration

    def add_hud(self,title,progress):
        h=header(18,title,progress); f=footer(); d=divider()
        self.add_fixed_in_frame_mobjects(h,f,d)
        return VGroup(h,f,d)

    def clear_all(self,run_time=0.28):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=run_time)
        self.clear()


def narration_lint(source_path:Path,verbose=True):
    tree=ast.parse(source_path.read_text(encoding='utf-8'))
    spoken=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
            if node.func.attr in {'narrate','narrate_play'} and node.args:
                s=node.args[0]
                if isinstance(s,ast.Constant) and isinstance(s.value,str):spoken.append(s.value)
    forbidden=['workflow','render','preflight','engine','code','mã nguồn','camera',
               'animation','cột trái','cột phải','debug']
    bad=[(w,line) for line in spoken for w in forbidden if w in line.lower()]
    if bad:raise AssertionError(bad)
    if verbose:print('NARRATION LINT OK:',len(spoken),'segments')
    return True


class TraiPhang18Master(BaseLesson):
    def intro(self):
        self.clear_all()
        bad,_=folded_route(TOP_CHAIN,RED)
        self.add(box_shell(True),bad,endpoint_dots())
        card=intro_card(18,['MỘT MẶT BỊ CẤM','ĐƯỜNG NGẮN NHẤT PHẢI ĐỔI HƯỚNG'],
                        'Mặt trên bị cấm; phải tìm dải mặt khác hợp lệ.')
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.65)
        self.narrate('Một con kiến muốn đi từ mặt trước tới mặt sau của một hộp chữ nhật. '
                     'Nếu mọi mặt đều được đi qua, ta đã biết cách trải để tìm đường ngắn nhất.')
        self.narrate('Nhưng lần này, toàn bộ nắp trên là vùng cấm. '
                     'Đường đi ngắn nhất trước đó có thể không còn sử dụng được.')

    def problem(self):
        self.clear_all();self.add_hud('Xác định hai điểm và mặt bị cấm','01 / 12')
        self.add(box_shell(True),endpoint_dots())
        c=lesson_card('HỘP CHỮ NHẬT',[
            ('math','a=8, b=5, h=4',27,CYAN),
            ('text','P nằm trên mặt trước, cao 3.',18,INK),
            ('text','Q nằm trên mặt sau, cao 3.',18,INK),
            ('text','Mặt trên không được đi qua.',19,RED),
        ],RED)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Chiều dài hộp là tám, chiều rộng là năm và chiều cao bằng bốn. '
                     'Điểm P nằm trên mặt trước, điểm Q nằm trên mặt sau. Cả hai đều cao ba so với đáy.')
        self.narrate('Nhìn theo cạnh dài tám, P cách đầu bên trái hai đơn vị, '
                     'còn Q cách đầu bên trái sáu đơn vị. Mọi phần khác của vỏ hộp được đi, trừ nắp trên.')

    def apparent_short(self):
        self.clear_all();self.add_hud('Nếu được đi qua nắp trên','02 / 12')
        self.add(box_shell(False),folded_route(TOP_CHAIN,RED)[0],endpoint_dots())
        c=lesson_card('DẢI MẶT NGẮN NHẤT BAN ĐẦU',[
            ('text','Mặt trước → nắp trên → mặt sau.',18,RED),
            ('math','Delta x=4',28,CYAN),
            ('math','Delta y=1+5+1=7',26,CYAN),
            ('math','L_1=sqrt(4^2+7^2)',26,INK),
            ('math','L_1=sqrt(65)',31,RED),
        ],RED)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Nếu không cấm nắp trên, ta trải mặt trước, mặt trên và mặt sau thành một dải phẳng.')
        self.narrate('Đường thẳng nối hai ảnh của P và Q lệch ngang bốn đơn vị. '
                     'Theo chiều dải mặt, nó đi một đơn vị lên nắp, năm đơn vị qua nắp, rồi một đơn vị xuống.')
        self.narrate('Độ dài khi ấy là căn sáu mươi lăm. '
                     'Đây là phương án ngắn nhất khi chưa áp dụng lệnh cấm.')

    def reject_top(self):
        self.clear_all();self.add_hud('Vì sao đường căn 65 bị loại?','03 / 12')
        net,_=net_diagram('top',True)
        self.add_fixed_in_frame_mobjects(net)
        c=lesson_card('DẢI MẶT TRÊN BỊ GẠCH BỎ',[
            ('math','L_1=sqrt(65)',29,RED),
            ('text','Đường đi đi xuyên qua miền đỏ.',18,RED),
            ('text','Miền đỏ là nắp trên bị cấm.',18,INK),
            ('text','Ngắn hơn nhưng không hợp lệ.',19,GOLD),
        ],RED)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Trên bản trải, đoạn thẳng đi xuyên qua phần nắp trên đang được đánh dấu đỏ.')
        self.narrate('Vì phần này bị cấm nên dù độ dài chỉ là căn sáu mươi lăm, '
                     'ta phải loại đường ấy khỏi các phương án.')

    def propose_alternatives(self):
        self.clear_all();self.add_hud('Còn những đường nào được phép?','04 / 12')
        self.add(box_shell(True),folded_route(BOTTOM_CHAIN,GOLD)[0],endpoint_dots())
        c=lesson_card('THỬ CÁC HƯỚNG KHÁC',[
            ('text','Qua đáy: mặt trước → đáy → mặt sau.',17,GOLD),
            ('text','Qua mặt trái rồi ra mặt sau.',18,ORANGE),
            ('text','Qua mặt phải rồi ra mặt sau.',18,CYAN),
            ('text','Cần so sánh độ dài, không đoán bằng mắt.',17,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Bây giờ ta có ba hướng dễ nhìn thấy. '
                     'Một hướng đi qua đáy, một hướng vòng sang mặt trái, và một hướng vòng sang mặt phải.')
        self.narrate('Cả ba đều tránh nắp trên. Nhưng hướng nào thật sự ngắn nhất? '
                     'Ta sẽ lần lượt đưa chúng về mặt phẳng để so sánh.')

    def unfold_bottom(self):
        self.clear_all();self.add_hud('Mở ba mặt: trước, đáy, sau','05 / 12')
        mobs,d=route_face_objects(BOTTOM_CHAIN,GOLD)
        self.add(*mobs)
        c=lesson_card('MỞ MẶT MÀ KHÔNG KÉO GIÃN',[
            ('text','Giữ mặt trước.',19,PURPLE),
            ('text','Mở đáy và mặt sau qua cạnh chung.',17,CYAN),
            ('text','Sau đó mở tiếp mặt sau.',18,INK),
            ('text','Đường màu vàng đi cùng chính các mặt.',17,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(c)
        a=d['steps'][0]
        self.narrate_play('Ta giữ mặt trước và mở cả phần đáy cùng mặt sau quanh cạnh chung với mặt trước.',
                         Rotate(VGroup(*mobs[1:]),angle=a['angle'],axis=W(a['b'])-W(a['a']),about_point=W(a['a'])),
                         min_time=3.0)
        b=d['steps'][1]
        self.narrate_play('Tiếp đó, ta mở riêng mặt sau quanh cạnh chung với đáy.',
                         Rotate(mobs[2],angle=b['angle'],axis=W(b['b'])-W(b['a']),about_point=W(b['a'])),
                         min_time=2.5)
        self.narrate('Ba mặt đã nằm chung trên mặt phẳng. '
                     'Những đoạn đường màu vàng cũng nằm thẳng hàng vì chúng được mở cùng các mặt.')

    def bottom_net(self):
        self.clear_all();self.add_hud('Tính đường đi qua đáy','06 / 12')
        net,_=net_diagram('bottom',True)
        self.add_fixed_in_frame_mobjects(net)
        c=lesson_card('TRÊN BẢN TRẢI QUA ĐÁY',[
            ('math','Delta x=6-2=4',27,CYAN),
            ('math','Delta y=3+5+3=11',25,CYAN),
            ('math','L_2^2=4^2+11^2',27,INK),
            ('math','L_2=sqrt(137)',34,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Ở dải mặt qua đáy, độ lệch ngang vẫn bằng bốn. '
                     'Nhưng theo chiều dải mặt, ta xuống ba đơn vị, đi ngang qua đáy năm đơn vị, rồi lên ba đơn vị.')
        self.narrate('Tổng độ lệch ấy bằng mười một. '
                     'Theo định lý Pythagore, độ dài phương án qua đáy là căn một trăm ba mươi bảy.')

    def bottom_crossings(self):
        self.clear_all();self.add_hud('Xác định hai điểm chuyển mặt','07 / 12')
        net,_=net_diagram('bottom',True)
        self.add_fixed_in_frame_mobjects(net)
        c=lesson_card('HAI ĐIỂM TRÊN CẠNH GẤP',[
            ('text','Đoạn thẳng chia dải theo tỉ lệ 3 : 5 : 3.',17,INK),
            ('math','x_X=2+frac(3,11) times 4',25,CYAN),
            ('math','x_X=frac(34,11)',28,GOLD),
            ('math','x_Y=2+frac(8,11) times 4',25,CYAN),
            ('math','x_Y=frac(54,11)',28,GOLD),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Đường vàng đi qua hai cạnh gấp. '
                     'Ta gọi X là điểm chuyển từ mặt trước xuống đáy, Y là điểm từ đáy lên mặt sau.')
        self.narrate('Theo sự tăng đều của hoành độ dọc theo đoạn thẳng, '
                     'hoành độ X bằng ba mươi bốn phần mười một, '
                     'còn hoành độ Y bằng năm mươi bốn phần mười một.')
        self.narrate('Cả hai đều nằm bên trong các cạnh dài tám, '
                     'nên đường đi qua đúng ba mặt đã chọn là hoàn toàn hợp lệ.')

    def side_routes(self):
        self.clear_all();self.add_hud('So sánh với hướng vòng hai bên','08 / 12')
        self.add(box_shell(True),folded_route(LEFT_CHAIN,ORANGE)[0],folded_route(RIGHT_CHAIN,CYAN)[0])
        c=lesson_card('DẢI QUA MẶT TRÁI HOẶC PHẢI',[
            ('math','L_3=2+5+6=13',26,ORANGE),
            ('math','L_4=6+5+2=13',26,CYAN),
            ('math','L_2=sqrt(137)',29,GOLD),
            ('math','sqrt(137)<13',30,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Nếu vòng qua mặt trái, khi trải ba mặt ta được độ lệch ngang bằng hai cộng năm cộng sáu, tức mười ba.')
        self.narrate('Vòng qua mặt phải, con số tương ứng là sáu cộng năm cộng hai, cũng bằng mười ba.')
        self.narrate('Cả hai đường bên dài mười ba, lớn hơn căn một trăm ba mươi bảy. '
                     'Vì vậy dải qua đáy tốt hơn các đường vòng qua hai bên.')

    def check_all_routes(self):
        self.clear_all();self.add_hud('Kiểm tra cả các dải đi qua nhiều mặt','09 / 12')
        chart=comparison_bars()
        self.add_fixed_in_frame_mobjects(chart)
        c=lesson_card('SO SÁNH CÁC PHƯƠNG ÁN',[
            ('math','sqrt(65)',28,RED),
            ('text','Ngắn nhất ban đầu, nhưng qua mặt cấm.',17,INK),
            ('math','sqrt(137)',30,GOLD),
            ('text','Ngắn nhất trong các đường được phép.',17,GREEN),
            ('math','13>sqrt(137)',27,CYAN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Ta còn cần cẩn thận: liệu đường đi qua bốn mặt có ngắn hơn đường qua đáy hay không?')
        self.narrate('Khi kiểm tra các chuỗi mặt liên tiếp hợp lệ, '
                     'các phương án đi qua bốn mặt cũng đều dài hơn căn một trăm ba mươi bảy.')
        self.narrate('Do đó kết luận lần này không chỉ đúng với ba hướng vừa nhìn thấy, '
                     'mà đúng với toàn bộ những đường đi được phép trên vỏ hộp.')

    def walk(self):
        self.clear_all();self.add_hud('Đặt lại đường đi lên hình hộp','10 / 12')
        path,coords=folded_route(BOTTOM_CHAIN,GOLD)
        ant=Dot3D(W(P_RAW),radius=0.087,color=GREEN)
        self.add(box_shell(True),path,endpoint_dots(),ant)
        c=lesson_card('ĐƯỜNG NGẮN NHẤT HỢP LỆ',[
            ('text','P → X trên mặt trước.',18,PURPLE),
            ('text','X → Y trên mặt đáy.',18,BLUE),
            ('text','Y → Q trên mặt sau.',18,CYAN),
            ('math','L_(min)=sqrt(137)',33,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(c)
        for i,line in enumerate([
            'Từ P, kiến đi xuống theo đoạn thẳng trên mặt trước tới X.',
            'Qua X, kiến chuyển xuống đáy rồi tiếp tục theo đoạn thẳng tới Y.',
            'Tại Y, kiến lên mặt sau và đi thẳng tới Q. Đường này không chạm nắp trên.',
        ]):
            self.narrate_play(line,MoveAlongPath(ant,Line(W(coords[i]),W(coords[i+1]))),
                             min_time=2.1,rate_func=linear)

    def proof(self):
        self.clear_all();self.add_hud('Lý do cách trải cho đáp án tối ưu','11 / 12')
        net,_=net_diagram('bottom',True)
        self.add_fixed_in_frame_mobjects(net)
        c=lesson_card('LẬP LUẬN',[
            ('text','Mỗi chuỗi mặt được trải đúng theo cạnh chung.',17,INK),
            ('text','Đường phẳng ngắn nhất là đoạn thẳng.',17,CYAN),
            ('text','Chỉ giữ đường cắt các cạnh theo đúng thứ tự.',17,INK),
            ('text','Loại mọi chuỗi chứa nắp trên.',18,RED),
            ('math','L_(min)=sqrt(137)',31,GOLD),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Muốn so sánh chặt chẽ, với mỗi dải mặt ta mở các mặt bằng phép quay quanh đúng cạnh chung.')
        self.narrate('Sau khi trải, ta lấy đoạn thẳng nối hai điểm và kiểm tra nó có đi qua các cạnh gấp '
                     'đúng thứ tự, đúng phần bên trong hay không.')
        self.narrate('Bỏ tất cả dải mặt chứa nắp trên, rồi so các đường còn hợp lệ. '
                     'Kết quả nhỏ nhất là căn một trăm ba mươi bảy.')

    def summary(self):
        self.clear_all();self.add_hud('Chốt bài: một mặt bị cấm','12 / 12')
        self.add(box_shell(True),folded_route(BOTTOM_CHAIN,GOLD)[0],endpoint_dots())
        c=lesson_card('ĐIỀU CẦN NHỚ',[
            ('text','1. Vùng cấm làm thay đổi bài toán.',17,RED),
            ('text','2. Liệt kê các dải mặt còn hợp lệ.',17,INK),
            ('text','3. Mở mặt, nối thẳng và kiểm tra giao cạnh.',17,CYAN),
            ('math','L_1=sqrt(65)',25,RED),
            ('math','L_2=sqrt(137)',28,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(c)
        self.narrate('Bài này cho thấy đường ngắn nhất không chỉ phụ thuộc vào kích thước hình hộp, '
                     'mà còn phụ thuộc vào những vùng bề mặt được phép sử dụng.')
        self.narrate('Không có vùng cấm, đường đi qua nắp trên là ngắn nhất với độ dài căn sáu mươi lăm. '
                     'Khi cấm nắp trên, đường tối ưu chuyển qua đáy và dài căn một trăm ba mươi bảy.')
        self.narrate('Trong những bài phức tạp hơn, điều quan trọng là chọn và kiểm tra các dải mặt hợp lệ '
                     'trước khi kết luận đáp án.')

    def construct(self):
        self.intro()
        self.problem()
        self.apparent_short()
        self.reject_top()
        self.propose_alternatives()
        self.unfold_bottom()
        self.bottom_net()
        self.bottom_crossings()
        self.side_routes()
        self.check_all_routes()
        self.walk()
        self.proof()
        self.summary()


class Smoke18(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.94)
        mobs,d=route_face_objects(BOTTOM_CHAIN,GOLD)
        self.add(*mobs)
        a,b=d['steps']
        self.play(Rotate(VGroup(*mobs[1:]),angle=a['angle'],
                         axis=W(a['b'])-W(a['a']),about_point=W(a['a'])),
                  run_time=1.25)
        self.play(Rotate(mobs[2],angle=b['angle'],
                         axis=W(b['b'])-W(b['a']),about_point=W(b['a'])),
                  run_time=1.0)
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854;config.pixel_height=480;config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file='trai_phang_18_master_smoke'
    config.disable_caching=True
    scene=Smoke18();scene.render()
    path=Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():raise RuntimeError(path)
    return path


def render_full():
    geometry_preflight(True)
    layout_preflight(layout_samples(),True)
    config.pixel_width=FINAL_WIDTH;config.pixel_height=FINAL_HEIGHT
    config.frame_rate=FINAL_FPS;config.media_dir=str(MEDIA_DIR)
    config.output_file='trai_phang_18_mot_mat_bi_cam_MASTER_1080p'
    config.disable_caching=False
    scene=TraiPhang18Master();scene.render()
    raw=Path(scene.renderer.file_writer.movie_file_path)
    master=ROOT/'master_narration_trai_phang_18.wav'
    build_master_audio(scene.audio_events,probe_duration(raw),master)
    out=raw.with_name(raw.stem+'_WITH_AUDIO.mp4')
    mux_audio(raw,master,out)
    print('VIDEO HOAN CHINH:',out)
    return out


if __name__=='__main__':
    source_path=Path(sys.argv[0]).resolve()
    if '--narration-lint' in sys.argv:
        narration_lint(source_path,True);raise SystemExit(0)
    if '--geometry-preflight' in sys.argv:
        geometry_preflight(True);raise SystemExit(0)
    if '--layout-preflight' in sys.argv:
        layout_preflight(layout_samples(),True);raise SystemExit(0)
    if '--smoke-render' in sys.argv:
        render_smoke();raise SystemExit(0)
    render_full()

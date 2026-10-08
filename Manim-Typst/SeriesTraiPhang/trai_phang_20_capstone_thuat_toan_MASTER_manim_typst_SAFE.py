
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


# ---------- VIDEO 20: CAPSTONE — ALGORITHM FOR SHORTEST SURFACE ROUTES ----------
# Capstone numerical example repeats the 8 x 5 x 4 box from Video 18,
# but now demonstrates a general-purpose finite search over valid face strips.
# Two states: free surface and with the top forbidden.
# Geometry engine independently unfolds EVERY simple adjacent-face chain
# and rejects any candidate whose straight line does not cross the common
# hinge edges in the correct order, strictly in their interiors.

VIDEO_NO=20
ALL_FACES=set(FACES)


def algorithm_results(forbidden=()):
    allowed=ALL_FACES-set(forbidden)
    choices=enumerate_routes(allowed)
    return choices


def audit_algorithm(verbose=True):
    geometry_preflight(False)
    free=algorithm_results()
    limited=algorithm_results(('top',))
    if not free or not limited:
        raise AssertionError('No routes')
    if free[0][1]!=TOP_CHAIN or abs(free[0][0]-math.sqrt(65))>1e-8:
        raise AssertionError(('Unexpected unrestricted optimum',free[0][:2]))
    if limited[0][1]!=BOTTOM_CHAIN or abs(limited[0][0]-math.sqrt(137))>1e-8:
        raise AssertionError(('Unexpected constrained optimum',limited[0][:2]))
    if len(limited)>=len(free):
        raise AssertionError('Forbidden face not removed correctly')
    if any('top' in chain for _,chain,_ in limited):
        raise AssertionError('Forbidden face appeared in legal list')
    if len(free)<4 or len(limited)<3:
        raise AssertionError('Expected multiple independent candidates')
    if verbose:
        print('ALGORITHM AUDIT OK')
        print('  unrestricted routes:',len(free))
        print('  allowed routes after banning top:',len(limited))
        print('  free winner:', free[0][1],f'{free[0][0]:.9f}')
        print('  restricted winner:', limited[0][1],f'{limited[0][0]:.9f}')
        print('  all valid paths cross hinges in the correct order')
        print('  folded lengths, rigid hinges, and face shape are preflight checked')
    return True


def algorithm_overview(active=0):
    stages=[
        '1. Xác định A, B và các mặt được đi',
        '2. Liệt kê các dải mặt nối A tới B',
        '3. Mở từng dải qua đúng cạnh chung',
        '4. Nối thẳng, kiểm tra giao cạnh',
        '5. Loại đường sai, chọn độ dài nhỏ nhất',
    ]
    group=VGroup()
    for i,label in enumerate(stages):
        y=2.00-0.98*i
        width=5.72
        rect=RoundedRectangle(
            width=width,height=0.75,corner_radius=0.09,
            stroke_color=GOLD if i==active else GRID,
            stroke_width=2.5 if i==active else 1.3,
            fill_color=PANEL_2 if i==active else PANEL,
            fill_opacity=0.96,
        ).move_to([LEFT_CENTER[0],y,0])
        line=fit_width(txt(label,19,GOLD if i==active else INK),5.30)
        line.move_to(rect)
        group.add(rect,line)
        if i<4:
            arrow=Arrow(
                [LEFT_CENTER[0],y-0.39,0],
                [LEFT_CENTER[0],y-0.59,0],
                buff=0,stroke_width=2.1,color=CYAN,
                max_tip_length_to_length_ratio=0.45,
            )
            group.add(arrow)
    return group


def compact_candidate_board(block_top=False):
    rows=[
        ('Trước → nắp → sau',math.sqrt(65),RED if block_top else GOLD),
        ('Trước → đáy → sau',math.sqrt(137),GOLD if block_top else CYAN),
        ('Trước → trái → sau',13.0,ORANGE),
        ('Trước → phải → sau',13.0,BLUE),
    ]
    group=VGroup()
    left=LEFT_CENTER[0]-2.66
    top=1.94
    for i,(name,value,color) in enumerate(rows):
        y=top-1.18*i
        label=fit_width(txt(name,19,INK),5.1)
        label.move_to([LEFT_CENTER[0],y+0.23,0])
        bg=Rectangle(width=4.92,height=0.18,stroke_width=0,
                     fill_color=GRID,fill_opacity=0.65).move_to([LEFT_CENTER[0],y-0.15,0])
        bar=Rectangle(width=4.92*value/14.0,height=0.18,stroke_width=0,
                      fill_color=color,fill_opacity=0.95)
        bar.move_to([left+bar.width/2+0.20,y-0.15,0])
        group.add(label,bg,bar)
    return group


def layout_samples():
    return [
        lesson_card('BÀI TOÁN TỔNG HỢP',[
            ('math','8 times 5 times 4',29,CYAN),
            ('text','P trên mặt trước; Q trên mặt sau.',18,INK),
            ('text','Thử khi được đi qua tất cả các mặt.',18,INK),
            ('text','Sau đó cấm nắp trên và tìm lại.',18,RED),
        ],GOLD),
        lesson_card('KẾT QUẢ THUẬT TOÁN',[
            ('math','L_(free)=sqrt(65)',28,CYAN),
            ('math','L_(valid)=sqrt(137)',29,GOLD),
            ('math','sqrt(137)<13',27,GREEN),
            ('text','Chỉ so sánh những dải mặt hợp lệ.',17,INK),
        ],GREEN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.94)

    def narrate(self,text,min_visual_time=1.0):
        sound=create_audio(text)
        duration=probe_duration(sound)
        self.audio_events.append((self.time,sound))
        self.wait(max(duration,min_visual_time))
        return duration

    def narrate_play(self,text,*animations,min_time=1.0,rate_func=smooth):
        sound=create_audio(text)
        duration=probe_duration(sound)
        self.audio_events.append((self.time,sound))
        self.play(*animations,run_time=max(duration,min_time),rate_func=rate_func)
        return duration

    def add_hud(self,title,progress):
        h=header(VIDEO_NO,title,progress)
        f=footer()
        d=divider()
        self.add_fixed_in_frame_mobjects(h,f,d)
        return VGroup(h,f,d)

    def show_card(self,title,rows,accent=CYAN):
        card=lesson_card(title,rows,accent)
        self.add_fixed_in_frame_mobjects(card)
        return card

    def show_flat(self,mob):
        self.add_fixed_in_frame_mobjects(mob)
        return mob

    def clear_all(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.22)
        self.clear()


def narration_lint(path:Path,verbose=True):
    tree=ast.parse(path.read_text(encoding='utf-8'))
    spoken=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) \
           and node.func.attr in ('narrate','narrate_play') and node.args:
            arg=node.args[0]
            if isinstance(arg,ast.Constant) and isinstance(arg.value,str):
                spoken.append(arg.value)
    bad_tokens=['workflow','render','preflight','engine','code','mã nguồn',
                'camera','animation','cột trái','cột phải','debug']
    errors=[(w,spoken_line) for spoken_line in spoken
            for w in bad_tokens if w in spoken_line.lower()]
    if errors:raise AssertionError(errors)
    if verbose:
        print('NARRATION LINT OK:',len(spoken),'segments;',
              sum(len(s.split()) for s in spoken),'words')
    return True


class TraiPhang20Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(box_shell(False),folded_route(TOP_CHAIN,GOLD)[0],endpoint_dots())
        card=intro_card(20,
            ['TỔNG KẾT SERIES TRẢI PHẲNG',
             'TÌM ĐƯỜNG NGẮN NHẤT BẰNG MỘT QUY TRÌNH'],
            'Liệt kê – khai triển – kiểm tra – so sánh.')
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)
        self.narrate('Đến video cuối, ta thử ghép tất cả tư duy đã học thành một cách giải có thứ tự, thay vì chọn đường theo cảm giác.')
        self.narrate('Mỗi đường đi trên nhiều mặt sẽ được kiểm tra qua một bản khai triển. Chỉ những đường hợp lệ mới được đem ra so sánh.')

    def problem(self):
        self.clear_all();self.add_hud('Một hình hộp, hai điểm trên hai mặt đối diện','01 / 15')
        self.add(box_shell(False),endpoint_dots())
        self.show_card('ĐỀ BÀI',[
            ('math','a=8, b=5, h=4',28,CYAN),
            ('text','P nằm trên mặt trước, cao 3.',18,INK),
            ('text','Q nằm trên mặt sau, cao 3.',18,INK),
            ('math','x_P=2, x_Q=6',27,GOLD),
            ('text','Tìm đường ngắn nhất trên vỏ hộp.',17,GREEN),
        ],GOLD)
        self.narrate('Ta dùng một hình hộp dài tám, rộng năm, cao bốn. Điểm P nằm trên mặt trước, điểm Q nằm trên mặt sau.')
        self.narrate('Cả hai điểm đều cao ba so với đáy. Theo chiều dài hộp, P ở vị trí hai còn Q ở vị trí sáu.')

    def steps(self):
        self.clear_all();self.add_hud('Năm bước giải bài toán đường ngắn nhất','02 / 15')
        self.show_flat(algorithm_overview(0))
        self.show_card('KHÔNG ĐOÁN BẰNG MẮT',[
            ('text','Bước 1: xác định điều kiện đi.',18,CYAN),
            ('text','Bước 2: xét các dải mặt có thể đi.',17,INK),
            ('text','Bước 3: trải đúng theo cạnh chung.',17,INK),
            ('text','Bước 4: kiểm tra đoạn thẳng có hợp lệ.',17,INK),
            ('text','Bước 5: chọn đường ngắn nhất.',18,GOLD),
        ],GOLD)
        self.narrate('Quy trình gồm năm bước: biết điểm đầu và cuối, liệt kê các dải mặt, trải từng dải, kiểm tra đường nối thẳng, rồi mới chọn độ dài nhỏ nhất.')
        self.narrate('Bước kiểm tra ở giữa đặc biệt quan trọng: một đoạn thẳng có thể đi ra ngoài dải mặt, cắt sai thứ tự cạnh hoặc đi vào vùng cấm.')

    def face_graph(self):
        self.clear_all();self.add_hud('Liệt kê các mặt kề nhau','03 / 15')
        self.add(box_shell(False),endpoint_dots())
        self.show_card('CÁC MẶT CÓ THỂ ĐI',[
            ('text','P thuộc mặt trước.',18,PURPLE),
            ('text','Q thuộc mặt sau.',18,CYAN),
            ('text','Có thể nối qua trên, dưới, trái, phải.',17,INK),
            ('text','Chỉ chuyển giữa hai mặt chung cạnh.',18,GOLD),
        ],CYAN)
        self.narrate('Muốn liệt kê, ta xem các mặt như những ô nối nhau bằng cạnh chung. Không thể nhảy từ một mặt sang mặt không kề nó.')
        self.narrate('Từ mặt trước tới mặt sau, ta thấy ngay bốn hướng cơ bản: qua nắp trên, qua đáy, vòng sang trái hoặc vòng sang phải.')

    def enumerate(self):
        self.clear_all();self.add_hud('Không quên các dải đi qua nhiều mặt','04 / 15')
        board=compact_candidate_board(False)
        self.show_flat(board)
        self.show_card('KIỂM TRA CÓ HỆ THỐNG',[
            ('text','Liệt kê các chuỗi mặt liền nhau.',18,INK),
            ('text','Không lặp mặt trong một dải đơn giản.',17,INK),
            ('text','Mở mỗi chuỗi rồi kiểm tra đoạn thẳng.',17,CYAN),
            ('text','Không chỉ thử 4 hướng nhìn thấy.',17,GOLD),
        ],GOLD)
        self.narrate('Bốn hướng cơ bản giúp ta dự đoán. Nhưng một lời giải chắc chắn còn phải kiểm tra những dải đi qua nhiều mặt.')
        self.narrate('Ta lần lượt xét các chuỗi mặt liền nhau, không lặp lại mặt trong cùng một dải đơn giản, rồi loại các dải có đường nối sai vị trí hoặc thứ tự.')

    def open_top(self):
        self.clear_all();self.add_hud('Thử mở dải trước – nắp – sau','05 / 15')
        mobs,d=route_face_objects(TOP_CHAIN,GOLD)
        self.add(*mobs)
        self.show_card('MỞ ĐÚNG CẠNH CHUNG',[
            ('text','Giữ mặt trước làm mốc.',18,PURPLE),
            ('text','Quay đồng thời hai mặt còn lại.',17,CYAN),
            ('text','Sau đó quay riêng mặt cuối.',17,GOLD),
            ('text','Độ dài các cạnh không đổi.',18,GREEN),
        ],GOLD)
        step=d['steps'][0]
        self.narrate_play('Đầu tiên giữ mặt trước và mở cả hai mặt phía sau quanh cạnh chung thứ nhất.',
            Rotate(VGroup(*mobs[1:]),angle=step['angle'],
                   axis=W(step['b'])-W(step['a']),about_point=W(step['a'])),min_time=2.7)
        step=d['steps'][1]
        self.narrate_play('Tiếp theo mở riêng mặt sau quanh cạnh chung thứ hai. Ba mặt nằm trên cùng một mặt phẳng.',
            Rotate(mobs[2],angle=step['angle'],
                   axis=W(step['b'])-W(step['a']),about_point=W(step['a'])),min_time=2.5)

    def top_candidate(self):
        self.clear_all();self.add_hud('Trên bản trải, đo đường qua nắp','06 / 15')
        net,_=net_diagram('top',True)
        self.show_flat(net)
        self.show_card('BẢN TRẢI NẮP TRÊN',[
            ('math','Delta x=6-2=4',26,CYAN),
            ('math','Delta y=1+5+1=7',27,CYAN),
            ('math','L_(top)^2=4^2+7^2',27,INK),
            ('math','L_(top)=sqrt(65)',31,GOLD),
        ],GOLD)
        self.narrate('Hai ảnh của P và Q cách nhau bốn đơn vị theo chiều dài và bảy đơn vị dọc theo dải mặt.')
        self.narrate('Định lý Pythagore cho căn sáu mươi lăm. Đây là đường tốt nhất nếu nắp trên vẫn được phép sử dụng.')

    def restriction(self):
        self.clear_all();self.add_hud('Thay một điều kiện: cấm mặt trên','07 / 15')
        self.add(box_shell(True),endpoint_dots(),folded_route(TOP_CHAIN,RED)[0])
        self.show_card('ĐIỀU KIỆN MỚI',[
            ('text','Không được đi qua nắp trên.',18,RED),
            ('math','L_(top)=sqrt(65)',29,RED),
            ('text','Ngắn hơn nhưng KHÔNG hợp lệ.',18,INK),
            ('text','Loại mọi dải mặt chứa nắp.',18,GOLD),
        ],RED)
        self.narrate('Bây giờ yêu cầu thay đổi: không được đi qua nắp trên. Đường căn sáu mươi lăm vừa tìm tuy ngắn nhưng phải loại.')
        self.narrate('Cách làm đúng không phải sửa số liệu, mà là bỏ tất cả dải mặt dùng nắp trên và kiểm tra lại những phương án còn lại.')

    def reopen_bottom(self):
        self.clear_all();self.add_hud('Mở dải hợp lệ: trước – đáy – sau','08 / 15')
        mobs,d=route_face_objects(BOTTOM_CHAIN,GOLD)
        self.add(*mobs)
        self.show_card('QUAY THẬT QUANH CẠNH GẤP',[
            ('text','Mặt trước giữ cố định.',18,PURPLE),
            ('text','Mặt đáy và mặt sau được mở dần.',18,CYAN),
            ('text','Nối thẳng trên bản trải mới.',18,INK),
            ('text','Không có mặt cấm trong dải này.',17,GREEN),
        ],GREEN)
        step=d['steps'][0]
        self.narrate_play('Giữ mặt trước rồi trải phần đáy cùng mặt sau xuống qua cạnh chung thứ nhất.',
            Rotate(VGroup(*mobs[1:]),angle=step['angle'],
                   axis=W(step['b'])-W(step['a']),about_point=W(step['a'])),min_time=2.7)
        step=d['steps'][1]
        self.narrate_play('Tiếp tục mở riêng mặt sau quanh cạnh chung với đáy. Đường vàng đi cùng ba mặt khi ta trải.',
            Rotate(mobs[2],angle=step['angle'],
                   axis=W(step['b'])-W(step['a']),about_point=W(step['a'])),min_time=2.5)

    def bottom_candidate(self):
        self.clear_all();self.add_hud('Đo chiều dài đường qua đáy','09 / 15')
        net,_=net_diagram('bottom',True)
        self.show_flat(net)
        self.show_card('PYTHAGORE TRÊN BẢN TRẢI',[
            ('math','Delta x=4',29,CYAN),
            ('math','Delta y=3+5+3=11',26,CYAN),
            ('math','L_(bottom)^2=4^2+11^2',25,INK),
            ('math','L_(bottom)=sqrt(137)',31,GOLD),
        ],GOLD)
        self.narrate('Trên dải qua đáy, chênh lệch theo chiều dài vẫn là bốn, nhưng độ lệch qua ba mặt là ba cộng năm cộng ba, bằng mười một.')
        self.narrate('Do đó đường thẳng trên dải này có độ dài căn một trăm ba mươi bảy.')

    def edge_validation(self):
        self.clear_all();self.add_hud('Kiểm tra hai điểm cắt cạnh gấp','10 / 15')
        net,_=net_diagram('bottom',True)
        self.show_flat(net)
        self.show_card('ĐOẠN THẲNG THẬT SỰ HỢP LỆ',[
            ('math','x_X=2+frac(3,11) times 4',24,INK),
            ('math','x_X=frac(34,11)',29,GOLD),
            ('math','x_Y=2+frac(8,11) times 4',24,INK),
            ('math','x_Y=frac(54,11)',29,GOLD),
        ],GREEN)
        self.narrate('Chưa được kết luận ngay. Ta cần kiểm tra đoạn thẳng có cắt đúng hai cạnh gấp, theo thứ tự từ mặt trước sang đáy rồi lên mặt sau.')
        self.narrate('Hai hoành độ lần lượt là ba mươi bốn phần mười một và năm mươi bốn phần mười một. Cả hai đều nằm trong cạnh dài tám.')
        self.narrate('Như vậy đường này không đi sai mặt, không cắt ra ngoài cạnh và thật sự hợp lệ.')

    def others(self):
        self.clear_all();self.add_hud('So sánh cả hai đường vòng bên','11 / 15')
        self.add(box_shell(True),folded_route(LEFT_CHAIN,ORANGE)[0],
                 folded_route(RIGHT_CHAIN,CYAN)[0],endpoint_dots())
        self.show_card('HAI DẢI QUA MẶT BÊN',[
            ('math','L_(left)=13',28,ORANGE),
            ('math','L_(right)=13',28,CYAN),
            ('math','L_(bottom)=sqrt(137)',27,GOLD),
            ('math','sqrt(137)<13',30,GREEN),
        ],GREEN)
        self.narrate('Nếu vòng qua mặt trái hay mặt phải, bản trải cho độ dài mười ba trong cả hai trường hợp.')
        self.narrate('Vì căn một trăm ba mươi bảy nhỏ hơn mười ba, đường qua đáy thắng cả hai phương án này.')

    def choose(self):
        self.clear_all();self.add_hud('Loại đường sai rồi chọn giá trị nhỏ nhất','12 / 15')
        self.show_flat(compact_candidate_board(True))
        self.show_card('SO SÁNH CÓ ĐIỀU KIỆN',[
            ('math','sqrt(65)',27,RED),
            ('text','Bỏ vì dùng mặt cấm.',17,RED),
            ('math','sqrt(137)',30,GOLD),
            ('text','Ngắn nhất trong các dải được phép.',17,GREEN),
            ('math','13>sqrt(137)',27,CYAN),
        ],GOLD)
        self.narrate('Khi so các dải đã qua kiểm tra, ta thấy đường căn một trăm ba mươi bảy nhỏ hơn các đường dài mười ba.')
        self.narrate('Ta cũng đã xét các dải nhiều mặt mà vẫn đi đúng cạnh gấp. Không dải hợp lệ nào cho độ dài nhỏ hơn kết quả qua đáy.')

    def walk(self):
        self.clear_all();self.add_hud('Đưa lời giải phẳng về lại hình hộp','13 / 15')
        path,vertices3=folded_route(BOTTOM_CHAIN,GOLD)
        ant=Dot3D(W(P_RAW),radius=0.088,color=GREEN)
        self.add(box_shell(True),path,endpoint_dots(),ant)
        self.show_card('ĐƯỜNG NGẮN NHẤT HỢP LỆ',[
            ('text','P → X trên mặt trước.',18,PURPLE),
            ('text','X → Y trên mặt đáy.',18,BLUE),
            ('text','Y → Q trên mặt sau.',18,CYAN),
            ('math','L_(min)=sqrt(137)',31,GOLD),
        ],GOLD)
        lines=[
            'Kiến bắt đầu từ P, đi trên mặt trước tới X, đúng cạnh chuyển xuống đáy.',
            'Qua X, kiến tiếp tục theo đoạn thẳng trên đáy đến Y ở cạnh chuyển lên mặt sau.',
            'Từ Y, kiến leo lên mặt sau và tới Q. Toàn bộ đường vàng đều nằm trên các mặt được phép.',
        ]
        for i,text in enumerate(lines):
            self.narrate_play(text,
                MoveAlongPath(ant,Line(W(vertices3[i]),W(vertices3[i+1]))),
                min_time=2.1,rate_func=linear)

    def proof(self):
        self.clear_all();self.add_hud('Lập luận tổng quát cho thuật toán','14 / 15')
        self.show_flat(algorithm_overview(4))
        self.show_card('TẠI SAO QUY TRÌNH ĐÚNG?',[
            ('text','Mỗi đường tối ưu thuộc một dải mặt hợp lệ.',17,INK),
            ('text','Phép mở mặt giữ nguyên độ dài.',17,INK),
            ('text','Trên dải phẳng, đoạn thẳng ngắn nhất.',17,CYAN),
            ('text','So sánh sau khi lọc đúng miền đi.',17,GOLD),
        ],GREEN)
        self.narrate('Trên hình hộp lồi, ta có thể tìm đường ngắn nhất bằng cách xét những dải mặt liên tiếp mà đường đi qua.')
        self.narrate('Mỗi dải được mở bằng những phép quay không làm biến dạng mặt. Đoạn thẳng chỉ được giữ lại nếu đi qua các cạnh chung đúng thứ tự và đúng vị trí.')
        self.narrate('Vì các dải hợp lệ đều đã được xét, lấy đường ngắn nhất trong những đường còn lại cho ta kết quả toàn cục của bài toán.')

    def conclusion(self):
        self.clear_all();self.add_hud('Video 20: tổng kết toàn bộ series','15 / 15')
        self.add(box_shell(True),folded_route(BOTTOM_CHAIN,GOLD)[0],endpoint_dots())
        self.show_card('CỐT LÕI 20 VIDEO',[
            ('text','Xác định mặt được đi và điều kiện.',17,INK),
            ('text','Chọn dải mặt, mở đúng cạnh bản lề.',17,INK),
            ('text','Nối thẳng, kiểm tra giao cạnh.',17,CYAN),
            ('text','Loại đường sai, so sánh đường đúng.',17,GOLD),
            ('math','L_(min)=sqrt(137)',29,GREEN),
        ],GOLD)
        self.narrate('Hai mươi bài toán đã cho ta một phương pháp chung: muốn tìm đường ngắn nhất trên bề mặt, trước tiên phải hiểu thật rõ mình được đi ở đâu.')
        self.narrate('Với mặt phẳng hoặc mặt khai triển được, ta biến đường đi thành đoạn thẳng. Với nhiều mặt ghép, ta liệt kê dải mặt, kiểm tra tính hợp lệ, rồi chọn độ dài nhỏ nhất.')
        self.narrate('Và đây là điều quan trọng nhất: một lời giải đẹp không chỉ có con số đúng, mà còn chỉ ra được đường đi thật trên hình ban đầu.')

    def construct(self):
        self.intro();self.problem();self.steps();self.face_graph();self.enumerate()
        self.open_top();self.top_candidate();self.restriction();self.reopen_bottom()
        self.bottom_candidate();self.edge_validation();self.others();self.choose()
        self.walk();self.proof();self.conclusion()


class Smoke20(ThreeDScene):
    def construct(self):
        audit_algorithm(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.94)
        mobs,data=route_face_objects(BOTTOM_CHAIN,GOLD)
        self.add(*mobs)
        a=data['steps'][0]
        self.play(Rotate(VGroup(*mobs[1:]),angle=a['angle'],
                         axis=W(a['b'])-W(a['a']),about_point=W(a['a'])),run_time=1.3)
        b=data['steps'][1]
        self.play(Rotate(mobs[2],angle=b['angle'],
                         axis=W(b['b'])-W(b['a']),about_point=W(b['a'])),run_time=1.3)
        self.wait(0.2)


def render_smoke():
    audit_algorithm(True)
    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file='trai_phang_20_master_smoke'
    config.disable_caching=True
    scene=Smoke20();scene.render()
    path=Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():raise RuntimeError(path)
    return path


def render_full():
    audit_algorithm(True)
    layout_preflight(layout_samples(),True)
    config.pixel_width=FINAL_WIDTH
    config.pixel_height=FINAL_HEIGHT
    config.frame_rate=FINAL_FPS
    config.media_dir=str(MEDIA_DIR)
    config.output_file='trai_phang_20_capstone_thuat_toan_MASTER_1080p'
    config.disable_caching=False
    scene=TraiPhang20Master();scene.render()
    video=Path(scene.renderer.file_writer.movie_file_path)
    audio=ROOT/'master_narration_trai_phang_20.wav'
    build_master_audio(scene.audio_events,probe_duration(video),audio)
    output=video.with_name(video.stem+'_WITH_AUDIO.mp4')
    mux_audio(video,audio,output)
    print('VIDEO HOAN CHINH:',output)
    return output


if __name__=='__main__':
    source_path=Path(sys.argv[0]).resolve()
    if '--narration-lint' in sys.argv:
        narration_lint(source_path,True);raise SystemExit(0)
    if '--geometry-preflight' in sys.argv:
        audit_algorithm(True);raise SystemExit(0)
    if '--layout-preflight' in sys.argv:
        layout_preflight(layout_samples(),True);raise SystemExit(0)
    if '--smoke-render' in sys.argv:
        render_smoke();raise SystemExit(0)
    render_full()

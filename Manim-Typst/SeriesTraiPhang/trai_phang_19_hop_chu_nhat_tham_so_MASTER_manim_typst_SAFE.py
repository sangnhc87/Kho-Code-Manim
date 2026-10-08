
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










# ---------- Video 19: switching shortest net for an adjustable box ----------
# Box: a=4 (x), b=6 (y), h=t (z), 2<=t<=10.
# Ant starts at A=(0,0,0); destination G=(4,6,t), opposite vertex.
# Route I: left -> top: L_I=sqrt((t+4)^2+36).
# Route II: front -> right: L_II=sqrt(100+t^2).
# Route III: bottom -> back: L_III=sqrt((t+6)^2+16).
# L_I^2 - L_II^2 = 8(t-6).
# L_III^2 - L_I^2 = 4t>0.
# Therefore the global shortest on all six faces switches at t=6.
# At t=6 there are four two-face routes, two representatives of each net.

A_LEN=4.0
B_LEN=6.0
T_MIN=2.0
T_MAX=10.0
CAM_PHI=68*DEGREES
CAM_THETA=-42*DEGREES
WORLD_SCALE=0.54
WORLD_SHIFT=np.array([-3.30,-0.18,-0.38])
FACES={
    'front': ['A','B','F','E'],
    'right': ['B','C','G','F'],
    'back': ['D','H','G','C'],
    'left': ['A','E','H','D'],
    'bottom': ['A','D','C','B'],
    'top': ['E','F','G','H'],
}
FACE_COLORS={'front':PURPLE,'right':CYAN,'back':ORANGE,'left':BLUE,'bottom':GREEN,'top':GOLD}
ROUTES={
    'I':['left','top'],
    'II':['front','right'],
    'III':['bottom','back'],
}

def vertices(t):
    a,b=A_LEN,B_LEN
    return {
        'A':np.array([0.,0.,0.]),'B':np.array([a,0.,0.]),
        'C':np.array([a,b,0.]),'D':np.array([0.,b,0.]),
        'E':np.array([0.,0.,t]),'F':np.array([a,0.,t]),
        'G':np.array([a,b,t]),'H':np.array([0.,b,t]),
    }

def lengths(t):
    return {
        'I':math.hypot(t+A_LEN,B_LEN),
        'II':math.hypot(A_LEN+B_LEN,t),
        'III':math.hypot(t+B_LEN,A_LEN),
    }

def winner(t):
    if abs(t-B_LEN)<1e-9: return ('I','II')
    return ('I',) if t<B_LEN else ('II',)

def W(p):
    return np.array(p,dtype=float)*WORLD_SCALE+WORLD_SHIFT

def face_normal(pts):
    q=np.array(pts,dtype=float)
    n=np.cross(q[1]-q[0],q[2]-q[0])
    return n/np.linalg.norm(n)

def rotate_point_axis(p,a,b,theta):
    p=np.array(p,dtype=float);a=np.array(a,dtype=float);b=np.array(b,dtype=float)
    axis=b-a;axis=axis/np.linalg.norm(axis)
    v=p-a
    return a+v*math.cos(theta)+np.cross(axis,v)*math.sin(theta)+axis*np.dot(axis,v)*(1-math.cos(theta))

def shared_edge(f,g):
    edge=[v for v in FACES[f] if v in FACES[g]]
    if len(edge)!=2:raise ValueError((f,g))
    return edge

def hinge_intersection(P,Q,U,V):
    direction=Q-P; edge=V-U
    matrix=np.array([[direction[0],-edge[0]],[direction[1],-edge[1]]],dtype=float)
    if abs(np.linalg.det(matrix))<1e-10:return None
    time,u=np.linalg.solve(matrix,U-P)
    if not (1e-8<time<1-1e-8 and 1e-8<u<1-1e-8):return None
    return float(time),float(u)

def unfold_chain(chain,t):
    '''Rotate the entire downstream strip rigidly around each exact hinge.'''
    v=vertices(t)
    fc={f:{k:v[k].copy() for k in FACES[f]} for f in chain}
    fc[chain[0]]['START']=v['A'].copy()
    fc[chain[-1]]['END']=v['G'].copy()
    root=chain[0]
    root_p=fc[root][FACES[root][0]].copy()
    n0=face_normal([fc[root][key] for key in FACES[root]])
    steps=[]
    for j in range(1,len(chain)):
        prev,cur=chain[j-1],chain[j]
        edge=shared_edge(prev,cur)
        a,b=fc[cur][edge[0]].copy(),fc[cur][edge[1]].copy()
        axis=(b-a)/np.linalg.norm(b-a)
        n_move=face_normal([fc[cur][key] for key in FACES[cur]])
        cent_prev=np.mean([fc[prev][key] for key in FACES[prev]],axis=0)
        sign_prev=np.dot(np.cross(b-a,cent_prev-a),n0)
        trials=[]
        for target in (n0,-n0):
            theta=math.atan2(np.dot(axis,np.cross(n_move,target)),np.dot(n_move,target))
            test={key:rotate_point_axis(point,a,b,theta) for key,point in fc[cur].items()}
            err=max(abs(np.dot(point-root_p,n0)) for point in test.values())
            cent_cur=np.mean([test[key] for key in FACES[cur]],axis=0)
            sign_cur=np.dot(np.cross(b-a,cent_cur-a),n0)
            trials.append(((err>1e-7,sign_prev*sign_cur>=-1e-9,abs(theta)),theta))
        theta=min(trials,key=lambda z:z[0])[1]
        for downstream in chain[j:]:
            fc[downstream]={key:rotate_point_axis(point,a,b,theta)
                            for key,point in fc[downstream].items()}
        steps.append({'j':j,'a':a,'b':b,'angle':theta,'edge':edge})
    ex=fc[root][FACES[root][1]]-root_p
    ex=ex/np.linalg.norm(ex)
    ey=np.cross(n0,ex)
    def project(point):
        d=point-root_p
        return np.array([np.dot(d,ex),np.dot(d,ey)])
    p=project(fc[root]['START'])
    q=project(fc[chain[-1]]['END'])
    hits=[]
    for j in range(len(chain)-1):
        edge=shared_edge(chain[j],chain[j+1])
        u2=project(fc[chain[j]][edge[0]])
        v2=project(fc[chain[j]][edge[1]])
        result=hinge_intersection(p,q,u2,v2)
        if result is None:return None
        s,h=result
        raw=v[edge[0]]+h*(v[edge[1]]-v[edge[0]])
        hits.append({'s':s,'u':h,'raw':raw,'edge':edge})
    if any(hits[i]['s']>=hits[i+1]['s'] for i in range(len(hits)-1)):return None
    return {'length':float(np.linalg.norm(p-q)),'steps':steps,
            'hits':hits,'fc':fc,'P2':p,'Q2':q,'normal':n0,'origin':root_p}

def enumerate_valid(t):
    '''Enumerate every simple adjacent-face strip from corner A to corner G.'''
    sources={'front','left','bottom'}
    targets={'right','back','top'}
    adjacency={f:[g for g in FACES if g!=f and len(set(FACES[f])&set(FACES[g]))==2]
               for f in FACES}
    found=[]
    def dfs(chain):
        last=chain[-1]
        if last in targets:
            data=unfold_chain(chain,t)
            if data is not None:
                found.append((tuple(chain),data['length']))
            # A strip can still leave and re-enter G's face but then cannot be shortest;
            # enumerate those too for a stronger consistency check.
        for next_face in adjacency[last]:
            if next_face not in chain:
                dfs(chain+[next_face])
    for start in sources:
        dfs([start])
    return sorted(found,key=lambda x:x[1])

def geometry_preflight(verbose=True):
    tol=2e-7
    grid=[2.,3.,4.,5.,5.9,6.,6.1,7.,8.,9.,10.]
    routes_checked=0
    for t in grid:
        v=vertices(t)
        assert abs(np.linalg.norm(v['A']-v['B'])-4)<tol
        assert abs(np.linalg.norm(v['B']-v['C'])-6)<tol
        assert abs(np.linalg.norm(v['C']-v['G'])-t)<tol
        ls=lengths(t)
        assert abs(ls['I']**2-ls['II']**2-8*(t-6))<tol
        assert abs(ls['III']**2-ls['I']**2-4*t)<tol
        for name,chain in ROUTES.items():
            d=unfold_chain(chain,t)
            if d is None:raise AssertionError(('missing hinge crossing',t,chain))
            if abs(d['length']-ls[name])>tol:raise AssertionError((t,name,'net',d['length'],ls[name]))
            if len(d['hits'])!=1:raise AssertionError('Should cross one hinge')
            X=d['hits'][0]['raw']
            folded=np.linalg.norm(v['A']-X)+np.linalg.norm(X-v['G'])
            if abs(folded-ls[name])>tol:raise AssertionError((t,name,'folded',folded,ls[name]))
            if any(abs(np.dot(p-d['origin'],d['normal']))>tol
                   for f in chain for p in (d['fc'][f][key] for key in FACES[f])):
                raise AssertionError('noncoplanar face')
            # Every opened face must be rigid: all six pairwise distances agree.
            for f in chain:
                before=[v[key] for key in FACES[f]]
                after=[d['fc'][f][key] for key in FACES[f]]
                for i in range(4):
                    for j in range(i+1,4):
                        db=np.linalg.norm(before[i]-before[j])
                        da=np.linalg.norm(after[i]-after[j])
                        if abs(db-da)>tol:
                            raise AssertionError(('face distorted',t,name,f,i,j,db,da))
            a,b=d['steps'][0]['a'],d['steps'][0]['b']
            if max(np.linalg.norm(rotate_point_axis(q,a,b,d['steps'][0]['angle'])-q)
                   for q in (a,b))>tol:raise AssertionError('hinge moved')
        all_routes=enumerate_valid(t)
        routes_checked+=len(all_routes)
        if not all_routes:raise AssertionError(('no candidate',t))
        best=all_routes[0][1]
        expected=min(ls.values())
        if abs(best-expected)>tol:raise AssertionError(('enumerated shortest mismatch',t,best,expected,all_routes[:5]))
        if verbose:
            print(f'  t={t:4.1f}: candidates={len(all_routes):2d}, best={best:.8f}, choice={winner(t)}')
    # Physical hinge positions for representative routes.
    for t in [2.,6.,9.]:
        v=vertices(t)
        XI=unfold_chain(ROUTES['I'],t)['hits'][0]['raw']
        XII=unfold_chain(ROUTES['II'],t)['hits'][0]['raw']
        XIII=unfold_chain(ROUTES['III'],t)['hits'][0]['raw']
        assert np.linalg.norm(XI-np.array([0,6*t/(t+4),t]))<tol
        assert np.linalg.norm(XII-np.array([4,0,2*t/5]))<tol
        assert np.linalg.norm(XIII-np.array([24/(6+t),6,0]))<tol
    if verbose:
        print(f'GEOMETRY PREFLIGHT OK: {len(grid)} t samples, {routes_checked} valid candidate strips')
        print('  I: left -> top, L_I=sqrt((t+4)^2+36)')
        print('  II: front -> right, L_II=sqrt(t^2+100)')
        print('  III: bottom -> back, L_III=sqrt((t+6)^2+16)')
        print('  Switch at t=6: L_min=2sqrt(34), tie')
    return True

# ---------- visual geometry ----------

def solid(a,b,color=EDGE,width=3.5):
    return Line(np.array(a,float),np.array(b,float),color=color,stroke_width=width)

def dashed(a,b,color=DIM,width=2.4):
    return DashedLine(np.array(a,float),np.array(b,float),color=color,
                      stroke_width=width,dash_length=0.10,dashed_ratio=0.53)

def plane_face(t,face,color=None,opacity=0.11):
    v=vertices(t)
    return Polygon(*[W(v[key]) for key in FACES[face]],
                   fill_color=color or FACE_COLORS[face],fill_opacity=opacity,
                   stroke_width=0)

def face_edge_visibility(t):
    # Front-facing classification from the fixed orientation.
    v=vertices(t)
    theta=CAM_THETA;phi=CAM_PHI
    cam=np.array([math.sin(phi)*math.cos(theta),math.sin(phi)*math.sin(theta),math.cos(phi)])
    cent=np.mean(list(v.values()),axis=0)
    front={}
    for f,keys in FACES.items():
        pts=[v[k] for k in keys]
        n=face_normal(pts)
        if np.dot(n,np.mean(pts,axis=0)-cent)<0:n=-n
        front[f]=np.dot(n,cam)>0
    edges={}
    for f,ks in FACES.items():
        for i in range(4):
            u,w=ks[i],ks[(i+1)%4]
            edges.setdefault(tuple(sorted([u,w])),set()).add(f)
    return [(u,w,any(front[f] for f in fs)) for (u,w),fs in edges.items()]

def box_shell(t,highlight=()):
    v=vertices(t)
    fills=VGroup(*[plane_face(t,f,opacity=0.16 if f in highlight else 0.025)
                   for f in FACES])
    edges=VGroup()
    for u,w,visible in face_edge_visibility(t):
        edges.add(solid(W(v[u]),W(v[w]),EDGE,3.2) if visible else dashed(W(v[u]),W(v[w])))
    return VGroup(fills,edges)

def route_folded(t,name,color=GOLD,width=5.8):
    v=vertices(t)
    d=unfold_chain(ROUTES[name],t)
    X=d['hits'][0]['raw']
    return VGroup(solid(W(v['A']),W(X),color,width),
                  solid(W(X),W(v['G']),color,width),
                  Dot3D(W(X),radius=0.061,color=color))

def model_with_routes(t,primary=('I','II')):
    m=VGroup(box_shell(t,highlight=set(sum([ROUTES[n] for n in primary],[]))))
    colors={'I':GOLD,'II':CYAN,'III':ORANGE}
    for name in primary:
        m.add(route_folded(t,name,colors[name],5.7 if name==primary[0] else 4.0))
    v=vertices(t)
    m.add(Dot3D(W(v['A']),radius=0.085,color=GREEN),
          Dot3D(W(v['G']),radius=0.085,color=RED))
    return m

def unfolding_face_mob(face,t,start=False,end=False):
    v=vertices(t);coords=[W(v[k]) for k in FACES[face]]
    m=VGroup(Polygon(*coords,fill_color=FACE_COLORS[face],fill_opacity=0.20,
                     stroke_color=FACE_COLORS[face],stroke_width=3.0))
    if start:m.add(Dot3D(W(v['A']),radius=0.076,color=GREEN))
    if end:m.add(Dot3D(W(v['G']),radius=0.076,color=RED))
    return m

def net_diagram(name,t,show_path=True):
    '''Exact rectangle of two adjacent unfolded faces, with real hinge position.'''
    if name=='I':
        first=t;second=A_LEN;height=B_LEN
    elif name=='II':
        first=A_LEN;second=B_LEN;height=t
    elif name=='III':
        first=B_LEN;second=t;height=A_LEN
    else:raise ValueError(name)
    total=first+second
    scale=min(5.70/total,4.75/height)
    origin=LEFT_CENTER + np.array([-total*scale/2,-height*scale/2,0.])
    def T(x,y):return origin+np.array([x*scale,y*scale,0.])
    color_first={'I':BLUE,'II':PURPLE,'III':GREEN}[name]
    color_second={'I':GOLD,'II':CYAN,'III':ORANGE}[name]
    g=VGroup(
        Polygon(T(0,0),T(first,0),T(first,height),T(0,height),
                fill_color=color_first,fill_opacity=0.14,
                stroke_color=color_first,stroke_width=3),
        Polygon(T(first,0),T(total,0),T(total,height),T(first,height),
                fill_color=color_second,fill_opacity=0.14,
                stroke_color=color_second,stroke_width=3),
        Line(T(first,0),T(first,height),color=GOLD,stroke_width=4.8),
        Dot(T(0,0),radius=0.076,color=GREEN),
        Dot(T(total,height),radius=0.076,color=RED))
    cross_y=height*first/total
    if show_path:
        g.add(Line(T(0,0),T(total,height),color=GOLD,stroke_width=5.9),
              Dot(T(first,cross_y),radius=0.061,color=GOLD))
    return g, {'A':T(0,0),'G':T(total,height),'X':T(first,cross_y),
               'width':total,'height':height,'hinge':first}

def length_chart(t):
    vals=lengths(t)
    # Bars share the same fixed scale; values are actual mathematical distances.
    x0=LEFT_CENTER[0]-2.30
    y0=-1.95
    g=VGroup()
    for i,name in enumerate(['I','II','III']):
        c={'I':GOLD,'II':CYAN,'III':ORANGE}[name]
        y=y0+2.0-0.85*i
        start=np.array([x0,y,0.]);end=start+RIGHT*(vals[name]*0.25)
        g.add(Line(start,end,color=c,stroke_width=17,stroke_opacity=0.89))
        lab=txt('I / trái-nắp' if name=='I' else ('II / trước-phải' if name=='II' else 'III / đáy-sau'),18,c)
        lab.move_to(start+RIGHT*1.06+UP*0.27)
        g.add(lab)
    return g

def layout_samples():
    return [
        lesson_card('BÀI TOÁN',[
            ('math','a=4, b=6',29,CYAN),
            ('math','h=t, 2<=t<=10',28,CYAN),
            ('text','A và G là hai đỉnh đối diện.',19,INK),
            ('text','Tìm đường ngắn nhất trên vỏ hộp.',18,GOLD),
        ],GOLD),
        lesson_card('ĐỔI PHƯƠNG ÁN',[
            ('math','L_I^2=(t+4)^2+36',27,BLUE),
            ('math','L_(I I)^2=t^2+100',27,CYAN),
            ('math','L_I^2-L_(I I)^2=8(t-6)',26,GOLD),
            ('math','t=6',34,GREEN),
        ],CYAN),
    ]

class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.94)
    def narrate(self,text, min_visual_time=1.0):
        path=create_audio(text);duration=probe_duration(path)
        self.audio_events.append((self.time,path))
        self.wait(max(duration,min_visual_time))
        return duration
    def narrate_play(self,text,*animations,min_time=1.,rate_func=smooth):
        path=create_audio(text);duration=probe_duration(path)
        self.audio_events.append((self.time,path))
        self.play(*animations,run_time=max(min_time,duration),rate_func=rate_func)
        return duration
    def add_hud(self,heading,progress):
        h=header(19,heading,progress);f=footer();d=divider()
        self.add_fixed_in_frame_mobjects(h,f,d)
    def clear_all(self):
        if self.mobjects:self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=0.28)
        self.clear()
    def show_card(self,heading,rows,accent=CYAN):
        card=lesson_card(heading,rows,accent)
        self.add_fixed_in_frame_mobjects(card)
        return card
    def show_net(self,name,t,show_path=True):
        g,points=net_diagram(name,t,show_path)
        self.add_fixed_in_frame_mobjects(g)
        return g,points

class TraiPhang19Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(model_with_routes(5.,('I','II')))
        card=intro_card(19,['HỘP CHỮ NHẬT CÓ THAM SỐ','ĐỔI KIỂU ĐƯỜNG NGẮN NHẤT'],
                        'Chiều cao thay đổi: phương án tối ưu có đổi không?')
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.narrate('Ở những bài trước, kích thước hình được cho cố định. '
                     'Hôm nay ta giữ hai cạnh của hình hộp nhưng thay đổi chiều cao.')
        self.narrate('Điều bất ngờ là khi hình hộp cao dần, con đường ngắn nhất giữa hai đỉnh đối diện '
                     'không còn đi qua cùng một cặp mặt như ban đầu.')

    def problem(self):
        self.clear_all();self.add_hud('Cố định hai cạnh, cho chiều cao thay đổi','01 / 14')
        self.add(model_with_routes(4.,('I',)))
        self.show_card('BÀI TOÁN',[
            ('math','A B=4',29,CYAN),('math','B C=6',29,CYAN),
            ('math','A E=t, 2<=t<=10',27,GOLD),
            ('text','A và G là hai đỉnh đối diện.',18,INK),
            ('text','Kiến chỉ đi trên vỏ hình hộp.',18,GREEN),
        ],GOLD)
        self.narrate('Cho hình hộp chữ nhật có hai cạnh đáy dài bốn và sáu. '
                     'Chiều cao ký hiệu là t, thay đổi từ hai đến mười.')
        self.narrate('Kiến xuất phát ở đỉnh A, muốn đến đỉnh đối diện G, '
                     'và bắt buộc đi trên mặt ngoài hình hộp. Tìm đường ngắn nhất theo t.')

    def candidate_paths(self):
        self.clear_all();self.add_hud('Ba cách ghép hai mặt kề','02 / 14')
        self.add(model_with_routes(5.,('I','II')))
        self.show_card('BA KIỂU BẢN TRẢI',[
            ('text','I. Mặt trái rồi mặt trên.',18,BLUE),
            ('text','II. Mặt trước rồi mặt phải.',18,CYAN),
            ('text','III. Mặt đáy rồi mặt sau.',18,ORANGE),
            ('text','Mỗi kiểu cho một đường chéo khác nhau.',17,GOLD),
        ],CYAN)
        self.narrate('Giữa hai đỉnh đối diện, ta xét ba kiểu bản trải hình chữ nhật. '
                     'Kiểu một qua mặt trái và nắp trên. Kiểu hai qua mặt trước và mặt phải.')
        self.narrate('Kiểu ba đi qua đáy và mặt sau. '
                     'Trước khi kết luận, ta phải tính cả ba, vì mỗi kiểu cho một đường chéo khác nhau.')

    def unfold_one(self):
        self.clear_all();self.add_hud('Mở mặt trên quanh cạnh EH','03 / 14')
        t=4.; chain=ROUTES['I']; d=unfold_chain(chain,t)
        left=unfolding_face_mob('left',t,start=True)
        top=unfolding_face_mob('top',t,end=True)
        self.add(left,top)
        self.show_card('PHƯƠNG ÁN I',[
            ('text','Giữ mặt trái, mở nắp quanh EH.',18,BLUE),
            ('text','Mặt trái: kích thước t × 6.',18,INK),
            ('text','Nắp trên: kích thước 4 × 6.',18,INK),
            ('math','L_I^2=(t+4)^2+6^2',27,GOLD),
        ],GOLD)
        step=d['steps'][0]
        self.narrate_play('Ta giữ mặt trái, rồi mở nắp trên quanh cạnh E H. '
                          'Cạnh chung đứng yên và cả nắp quay cứng như một cánh cửa.',
                          Rotate(top,angle=step['angle'],axis=W(step['b'])-W(step['a']),
                                 about_point=W(step['a'])),min_time=3.8)
        self.narrate('Sau khi trải, hai mặt trở thành hình chữ nhật có một chiều t cộng bốn, '
                     'chiều kia bằng sáu.')

    def net_one(self):
        self.clear_all();self.add_hud('Độ dài phương án I','04 / 14')
        self.show_net('I',4.)
        self.show_card('QUA MẶT TRÁI VÀ NẮP',[
            ('math','u=t+4',27,BLUE),('math','v=6',27,CYAN),
            ('math','L_I^2=(t+4)^2+36',30,GOLD),
            ('text','Tại t = 4, chiều ngang bằng 8.',18,INK),
        ],GOLD)
        self.narrate('Trên bản trải thứ nhất, đường đi tốt nhất là đường chéo. '
                     'Bình phương độ dài bằng t cộng bốn tất cả bình phương, cộng ba mươi sáu.')

    def unfold_two(self):
        self.clear_all();self.add_hud('Mở mặt phải quanh cạnh BF','05 / 14')
        t=8.;d=unfold_chain(ROUTES['II'],t)
        front=unfolding_face_mob('front',t,start=True)
        right=unfolding_face_mob('right',t,end=True)
        self.add(front,right)
        self.show_card('PHƯƠNG ÁN II',[
            ('text','Giữ mặt trước, mở mặt phải quanh BF.',17,CYAN),
            ('text','Mặt trước rộng 4, mặt phải rộng 6.',18,INK),
            ('text','Cả hai đều cao t.',18,INK),
            ('math','L_(I I)^2=10^2+t^2',29,GOLD),
        ],CYAN)
        step=d['steps'][0]
        self.narrate_play('Với kiểu thứ hai, ta giữ mặt trước rồi mở mặt phải quanh cạnh B F. '
                          'Cạnh B F là bản lề và không di chuyển.',
                          Rotate(right,angle=step['angle'],axis=W(step['b'])-W(step['a']),
                                 about_point=W(step['a'])),min_time=3.8)
        self.narrate('Hai mặt ghép thành hình chữ nhật rộng mười, cao t. '
                     'Đường ngắn nhất trong dải này lại là đường chéo.')

    def net_two(self):
        self.clear_all();self.add_hud('Độ dài phương án II','06 / 14')
        self.show_net('II',8.)
        self.show_card('QUA MẶT TRƯỚC VÀ MẶT PHẢI',[
            ('math','u=4+6=10',28,CYAN),
            ('math','v=t',28,INK),
            ('math','L_(I I)^2=100+t^2',32,GOLD),
            ('text','Phương án II lợi hơn khi hộp đủ cao.',18,GREEN),
        ],CYAN)
        self.narrate('Trong kiểu thứ hai, bình phương đường chéo bằng một trăm cộng t bình phương. '
                     'Ta sẽ so kết quả này với kiểu thứ nhất mà chưa cần lấy căn.')

    def third_candidate(self):
        self.clear_all();self.add_hud('Đừng quên phương án thứ ba','07 / 14')
        self.show_net('III',5.)
        self.show_card('QUA ĐÁY VÀ MẶT SAU',[
            ('math','u=t+6',28,ORANGE),
            ('math','v=4',28,CYAN),
            ('math','L_(I I I)^2=(t+6)^2+16',27,GOLD),
            ('text','Vẫn phải xét trước khi loại.',18,INK),
        ],ORANGE)
        self.narrate('Còn một kiểu nữa: mở mặt đáy với mặt sau. '
                     'Bản trải có hai chiều là t cộng sáu và bốn.')
        self.narrate('Độ dài đường chéo của kiểu ba bằng căn của t cộng sáu tất cả bình phương, '
                     'cộng mười sáu. Đừng bỏ một phương án chỉ vì nhìn hình có vẻ dài hơn.')

    def eliminate_third(self):
        self.clear_all();self.add_hud('Chứng minh phương án III không thắng','08 / 14')
        self.show_net('III',5.)
        self.show_card('SO SÁNH BÌNH PHƯƠNG',[
            ('math','L_(I I I)^2=(t+6)^2+16',27,ORANGE),
            ('math','L_I^2=(t+4)^2+36',27,BLUE),
            ('math','L_(I I I)^2-L_I^2=4t',29,GOLD),
            ('math','4t>0',30,GREEN),
        ],GREEN)
        self.narrate('Trừ hai bình phương của kiểu ba và kiểu một, '
                     'ta được đúng bốn t.')
        self.narrate('Vì t luôn dương, phương án ba dài hơn phương án một. '
                     'Do đó phương án ba không thể ngắn nhất và được loại bằng lập luận, chứ không phải bằng cảm giác.')

    def compare_two(self):
        self.clear_all();self.add_hud('Tìm mốc chuyển phương án','09 / 14')
        chart=length_chart(5.)
        self.add_fixed_in_frame_mobjects(chart)
        self.show_card('SO SÁNH I VÀ II',[
            ('math','L_I^2=(t+4)^2+36',27,BLUE),
            ('math','L_(I I)^2=100+t^2',27,CYAN),
            ('math','L_I^2-L_(I I)^2=8(t-6)',27,GOLD),
            ('math','t=6',35,GREEN),
        ],GOLD)
        self.narrate('Giờ chỉ còn hai phương án một và hai. '
                     'Lấy bình phương độ dài của kiểu một trừ kiểu hai, ta được tám nhân t trừ sáu.')
        self.narrate('Dấu của hiệu đổi khi t bằng sáu. '
                     'Đây chính là chiều cao mà hai đường ngắn nhất bằng nhau.')

    def low_height(self):
        self.clear_all();self.add_hud('Khi t nhỏ hơn 6: đi qua mặt trái và nắp','10 / 14')
        self.add(model_with_routes(3.,('I','II')))
        self.show_card('TỪ 2 ĐẾN TRƯỚC 6',[
            ('math','t<6',30,CYAN),
            ('math','L_I^2-L_(I I)^2<0',28,INK),
            ('math','L_I<L_(I I)',32,GREEN),
            ('text','Chọn dải trái → nắp trên.',18,GOLD),
        ],GREEN)
        self.narrate('Khi t nhỏ hơn sáu, hiệu hai bình phương âm. '
                     'Vì vậy đường qua mặt trái rồi nắp trên là ngắn nhất.')
        self.narrate('Chẳng hạn t bằng ba, đường vàng trên hình là phương án tốt hơn.')

    def tie(self):
        self.clear_all();self.add_hud('Tại t=6: hai kiểu cùng ngắn nhất','11 / 14')
        self.add(model_with_routes(6.,('I','II')))
        self.show_card('ĐIỂM CHUYỂN PHƯƠNG ÁN',[
            ('math','t=6',29,CYAN),
            ('math','L_I=L_(I I)',30,INK),
            ('math','L_(m i n)=sqrt(136)=2 sqrt(34)',29,GOLD),
            ('text','Hai dải khác nhau, độ dài bằng nhau.',18,GREEN),
        ],GOLD)
        self.narrate('Đúng tại t bằng sáu, hai bản trải cho hai đường dài bằng nhau. '
                     'Độ dài chung bằng hai căn ba mươi bốn.')
        self.narrate('Đó là ngưỡng đổi phương án. '
                     'Trên hình hộp thật, hai đường đi qua những cặp mặt khác nhau nhưng vẫn cùng tối ưu.')

    def high_height(self):
        self.clear_all();self.add_hud('Khi t lớn hơn 6: đi qua mặt trước và mặt phải','12 / 14')
        self.add(model_with_routes(9.,('II','I')))
        self.show_card('TRÊN 6 ĐẾN 10',[
            ('math','t>6',30,CYAN),
            ('math','L_I^2-L_(I I)^2>0',28,INK),
            ('math','L_(I I)<L_I',32,GREEN),
            ('text','Chọn dải trước → phải.',18,GOLD),
        ],GREEN)
        self.narrate('Khi t lớn hơn sáu, hiệu hai bình phương dương. '
                     'Lúc này phương án qua mặt trước và mặt phải ngắn hơn.')
        self.narrate('Như vậy chỉ thay đổi chiều cao, nhưng con đường tối ưu đã chuyển sang một cặp mặt khác.')

    def dynamic_switch(self):
        self.clear_all();self.add_hud('Quan sát hai đường cùng thay đổi theo t','13 / 14')
        t=ValueTracker(2.0)
        model=always_redraw(lambda:model_with_routes(
            t.get_value(), ('I','II') if t.get_value()<=6 else ('II','I')))
        self.add(model)
        self.show_card('QUY TẮC CHỌN THEO t',[
            ('text','2 ≤ t < 6: chọn mặt trái và nắp.',18,BLUE),
            ('text','t = 6: hai kiểu bằng nhau.',19,GOLD),
            ('text','6 < t ≤ 10: chọn trước và phải.',18,CYAN),
            ('text','Đường tối ưu đổi kiểu tại t = 6.',18,GREEN),
        ],GOLD)
        self.narrate_play('Bây giờ nhìn hình hộp cao dần từ hai tới mười. '
                          'Hai đường đều thay đổi liên tục, nhưng đường ngắn nhất đổi từ kiểu một sang kiểu hai khi vượt t bằng sáu.',
                          t.animate.set_value(10.0),min_time=7.0,rate_func=linear)
        self.narrate('Vị trí chuyển mặt trên mỗi cạnh gấp cũng dịch chuyển đúng theo chiều cao, '
                     'không phải một điểm cố định cho mọi t.')

    def conclusion(self):
        self.clear_all();self.add_hud('Chốt bài toán tham số','14 / 14')
        self.add(model_with_routes(6.,('I','II')))
        self.show_card('HÀM GIÁ TRỊ NHỎ NHẤT',[
            ('text','2 ≤ t ≤ 6:',18,BLUE),
            ('math','L_(m i n)=sqrt((t+4)^2+36)',26,BLUE),
            ('text','6 ≤ t ≤ 10:',18,CYAN),
            ('math','L_(m i n)=sqrt(t^2+100)',28,CYAN),
            ('math','t_0=6',30,GOLD),
        ],GREEN)
        self.narrate('Kết luận cuối cùng là một hàm cho theo từng khoảng. '
                     'Từ hai tới sáu, lấy căn của t cộng bốn bình phương cộng ba mươi sáu.')
        self.narrate('Từ sáu tới mười, lấy căn của t bình phương cộng một trăm. '
                     'Hai công thức nối nhau tại t bằng sáu.')
        self.narrate('Đây là một ứng dụng rất đẹp của tư duy hàm số: '
                     'đường đi ngắn nhất trên một vật thể có thể đổi hẳn phương án khi tham số vượt một ngưỡng.')

    def construct(self):
        self.intro();self.problem();self.candidate_paths();self.unfold_one();self.net_one()
        self.unfold_two();self.net_two();self.third_candidate();self.eliminate_third()
        self.compare_two();self.low_height();self.tie();self.high_height()
        self.dynamic_switch();self.conclusion()

class Smoke19(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.94)
        for name,t in [('I',4.),('II',8.)]:
            chain=ROUTES[name];data=unfold_chain(chain,t)
            a=unfolding_face_mob(chain[0],t,start=True)
            b=unfolding_face_mob(chain[1],t,end=True)
            self.add(a,b)
            step=data['steps'][0]
            self.play(Rotate(b,angle=step['angle'],axis=W(step['b'])-W(step['a']),
                             about_point=W(step['a'])),run_time=1.1)
            self.wait(0.1);self.clear()

def narration_lint(source_path:Path,verbose=True):
    tree=ast.parse(source_path.read_text(encoding='utf-8'))
    spoken=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) \
           and node.func.attr in ('narrate','narrate_play') and node.args:
            if isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):
                spoken.append(node.args[0].value)
    forbidden=['workflow','render','preflight','engine','code','mã nguồn','camera',
               'animation','cột trái','cột phải','debug']
    bad=[(x,s) for s in spoken for x in forbidden if x in s.lower()]
    if bad:raise AssertionError(bad)
    if verbose:print('NARRATION LINT OK:',len(spoken),'segments')
    return True

def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854;config.pixel_height=480;config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file='trai_phang_19_master_smoke'
    config.disable_caching=True
    scene=Smoke19();scene.render()
    path=Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():raise RuntimeError(path)
    return path

def render_full():
    geometry_preflight(True);layout_preflight(layout_samples(),True)
    config.pixel_width=FINAL_WIDTH;config.pixel_height=FINAL_HEIGHT
    config.frame_rate=FINAL_FPS;config.media_dir=str(MEDIA_DIR)
    config.output_file='trai_phang_19_hop_chu_nhat_tham_so_MASTER_1080p'
    config.disable_caching=False
    scene=TraiPhang19Master();scene.render()
    raw=Path(scene.renderer.file_writer.movie_file_path)
    master=ROOT/'master_narration_trai_phang_19.wav'
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

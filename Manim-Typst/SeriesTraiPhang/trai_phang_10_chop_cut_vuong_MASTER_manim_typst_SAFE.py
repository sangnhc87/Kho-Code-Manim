
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





# ---------- geometry engine: regular square frustum ----------
# Square frustum ABCD.A'B'C'D'
#
# Bottom square side = 6
# Top square side    = 4
# Vertical height   = 2*sqrt(2)
#
# Each lateral face is an isosceles trapezoid:
#   bases 6 and 4
#   trapezoid height 3
#   lateral legs sqrt(10)
#
# Primary problem:
#   A -> C, only on lateral surface.
# There are two symmetric 2-face routes:
#   via B : f1 -> f2
#   via D : f4 -> f3
# ==========================================================

BOTTOM = 6.0
TOP = 4.0
HEIGHT = 2.0 * math.sqrt(2.0)
D = (BOTTOM - TOP) / 2.0  # inward offset = 1
FACE_HEIGHT = math.sqrt(HEIGHT**2 + D**2)  # = 3
LEG = math.sqrt(HEIGHT**2 + 2*D**2)        # = sqrt(10)

RAW = {
    "A":  np.array([-3.0,-3.0,0.0]),
    "B":  np.array([ 3.0,-3.0,0.0]),
    "C":  np.array([ 3.0, 3.0,0.0]),
    "D":  np.array([-3.0, 3.0,0.0]),
    "A1": np.array([-2.0,-2.0,HEIGHT]),
    "B1": np.array([ 2.0,-2.0,HEIGHT]),
    "C1": np.array([ 2.0, 2.0,HEIGHT]),
    "D1": np.array([-2.0, 2.0,HEIGHT]),
}

FACES = {
    "bottom": ["A","D","C","B"],
    "top":    ["A1","B1","C1","D1"],
    "f1":     ["A","B","B1","A1"],
    "f2":     ["B","C","C1","B1"],
    "f3":     ["C","D","D1","C1"],
    "f4":     ["D","A","A1","D1"],
}
FACE_COLORS = {
    "f1": PURPLE,
    "f2": CYAN,
    "f3": BLUE,
    "f4": ORANGE,
}

ROUTE_B = ["f1","f2"]
ROUTE_D = ["f4","f3"]
BAND = ["f1","f2","f3","f4"]

WORLD_SCALE = 0.70
WORLD_SHIFT = np.array([-3.18,-0.25,-0.10])

CAM_PHI = 67 * DEGREES
CAM_THETA = -48 * DEGREES


def W(p):
    return WORLD_SCALE * np.array(p, dtype=float) + WORLD_SHIFT


def rotate_point_axis(p, axis_a, axis_b, angle):
    p = np.array(p, dtype=float)
    a = np.array(axis_a, dtype=float)
    b = np.array(axis_b, dtype=float)
    k = b - a
    nk = np.linalg.norm(k)
    if nk < 1e-12:
        raise ValueError("Zero-length rotation axis")
    k = k / nk
    x = p - a
    return a + (
        x * math.cos(angle)
        + np.cross(k, x) * math.sin(angle)
        + k * np.dot(k, x) * (1.0 - math.cos(angle))
    )


def pairwise_distances(points):
    vals = []
    for i in range(len(points)):
        for j in range(i+1,len(points)):
            vals.append(np.linalg.norm(np.array(points[i])-np.array(points[j])))
    return np.array(vals)


def face_normal(points):
    q = np.array(points, dtype=float)
    n = np.cross(q[1]-q[0], q[2]-q[0])
    return n / np.linalg.norm(n)


def outward_normal(face_name):
    pts = [RAW[v] for v in FACES[face_name]]
    n = face_normal(pts)
    poly_cent = np.mean(list(RAW.values()), axis=0)
    face_cent = np.mean(pts, axis=0)
    if np.dot(n, face_cent-poly_cent) < 0:
        n = -n
    return n


def camera_direction():
    return np.array([
        math.sin(CAM_PHI)*math.cos(CAM_THETA),
        math.sin(CAM_PHI)*math.sin(CAM_THETA),
        math.cos(CAM_PHI),
    ])


def edge_visibility():
    faces_by_edge = {}
    for fname, verts in FACES.items():
        for i in range(len(verts)):
            u, v = verts[i], verts[(i+1)%len(verts)]
            key = tuple(sorted((u,v)))
            faces_by_edge.setdefault(key, []).append(fname)

    cam = camera_direction()
    front = {f: np.dot(outward_normal(f), cam) > 0 for f in FACES}

    visible, hidden = [], []
    for edge, fs in faces_by_edge.items():
        if any(front[f] for f in fs):
            visible.append(edge)
        else:
            hidden.append(edge)
    return visible, hidden


def shared_edge(f1,f2):
    common = [v for v in FACES[f1] if v in FACES[f2]]
    if len(common) != 2:
        raise ValueError(f"{f1}, {f2} are not adjacent")
    return common


def signed_angle_about_axis(v,w,axis):
    v = np.array(v,dtype=float)
    w = np.array(w,dtype=float)
    axis = np.array(axis,dtype=float)
    axis = axis/np.linalg.norm(axis)
    return math.atan2(
        np.dot(axis,np.cross(v,w)),
        np.dot(v,w),
    )


def unfold_chain_numeric(chain):
    fc = {f:{v:RAW[v].copy() for v in FACES[f]} for f in chain}
    base = chain[0]
    base_pts = [fc[base][v] for v in FACES[base]]
    n0 = face_normal(base_pts)
    plane_p = base_pts[0].copy()
    steps = []

    for i in range(1,len(chain)):
        prev,cur = chain[i-1],chain[i]
        edge = shared_edge(prev,cur)
        a = fc[cur][edge[0]].copy()
        b = fc[cur][edge[1]].copy()
        axis = b-a

        n_cur = face_normal([fc[cur][v] for v in FACES[cur]])
        prev_cent = np.mean([fc[prev][v] for v in FACES[prev]],axis=0)

        trials = []
        for target in (n0,-n0):
            ang = signed_angle_about_axis(n_cur,target,axis)
            test = {v:rotate_point_axis(fc[cur][v],a,b,ang) for v in FACES[cur]}
            err = max(abs(np.dot(q-plane_p,n0)) for q in test.values())

            hv = b-a
            prev_side = np.dot(np.cross(hv,prev_cent-a),n0)
            cur_cent = np.mean(list(test.values()),axis=0)
            cur_side = np.dot(np.cross(hv,cur_cent-a),n0)
            opposite_penalty = 0 if prev_side*cur_side < 0 else 1

            trials.append((round(err,12),opposite_penalty,abs(ang),ang))

        trials.sort(key=lambda z:(z[0]>1e-8,z[1],z[2]))
        ang = trials[0][3]

        for j in range(i,len(chain)):
            f = chain[j]
            for v in FACES[f]:
                fc[f][v] = rotate_point_axis(fc[f][v],a,b,ang)

        steps.append({"index":i,"edge":edge,"a":a,"b":b,"angle":ang})

    return fc,steps,n0,plane_p


def plane_basis(chain,fc,n0):
    f = chain[0]
    p0 = fc[f][FACES[f][0]].copy()
    e1 = fc[f][FACES[f][1]] - p0
    e1 = e1/np.linalg.norm(e1)
    e2 = np.cross(n0,e1)
    e2 = e2/np.linalg.norm(e2)
    return p0,e1,e2


def proj2(x,basis):
    p0,e1,e2 = basis
    d = np.array(x)-p0
    return np.array([np.dot(d,e1),np.dot(d,e2)])


def seg_inter(P,Q,A,B,tol=1e-9):
    P,Q,A,B = map(lambda z:np.array(z,dtype=float),[P,Q,A,B])
    v = Q-P
    w = B-A
    M = np.array([[v[0],-w[0]],[v[1],-w[1]]],dtype=float)
    if abs(np.linalg.det(M)) < 1e-10:
        return None
    t,u = np.linalg.solve(M,A-P)
    if -tol <= t <= 1+tol and -tol <= u <= 1+tol:
        return float(t),float(u),P+t*v
    return None


def path_data(chain,start_vertex,end_vertex):
    fc,steps,n0,plane_p = unfold_chain_numeric(chain)
    basis = plane_basis(chain,fc,n0)

    P3 = fc[chain[0]][start_vertex]
    Q3 = fc[chain[-1]][end_vertex]
    P = proj2(P3,basis)
    Q = proj2(Q3,basis)

    hits = []
    for i in range(len(chain)-1):
        edge = shared_edge(chain[i],chain[i+1])
        A2 = proj2(fc[chain[i]][edge[0]],basis)
        B2 = proj2(fc[chain[i]][edge[1]],basis)
        hit = seg_inter(P,Q,A2,B2)
        if hit is None:
            raise AssertionError(f"Path misses hinge {edge}")
        t,u,X2 = hit
        if not (1e-8<t<1-1e-8 and 1e-8<u<1-1e-8):
            raise AssertionError(f"Hinge crossing not interior: {edge}, t={t}, u={u}")

        raw_a = RAW[edge[0]]
        raw_b = RAW[edge[1]]
        raw_x = raw_a + u*(raw_b-raw_a)
        hits.append({"edge":edge,"t":t,"u":u,"p2":X2,"raw":raw_x})

    return {
        "fc":fc,"steps":steps,"basis":basis,
        "P2":P,"Q2":Q,
        "Praw":RAW[start_vertex].copy(),
        "Qraw":RAW[end_vertex].copy(),
        "hits":hits,
        "length":float(np.linalg.norm(Q-P)),
    }


def rigid_preflight_chain(chain):
    before = {f:[RAW[v].copy() for v in FACES[f]] for f in chain}
    fc,steps,n0,plane_p = unfold_chain_numeric(chain)

    for f in chain:
        after = [fc[f][v] for v in FACES[f]]
        if not np.allclose(
            pairwise_distances(before[f]),
            pairwise_distances(after),
            atol=1e-9,rtol=0
        ):
            raise AssertionError(f"Face {f} distorted")

        if max(abs(np.dot(q-plane_p,n0)) for q in after) > 1e-8:
            raise AssertionError(f"Face {f} not coplanar after unfolding")
    return True


def geometry_preflight(verbose=True):
    tol = 1e-9

    # Basic frustum geometry.
    for u,v in [("A","B"),("B","C"),("C","D"),("D","A")]:
        if abs(np.linalg.norm(RAW[u]-RAW[v]) - BOTTOM) > tol:
            raise AssertionError("Wrong bottom edge")
    for u,v in [("A1","B1"),("B1","C1"),("C1","D1"),("D1","A1")]:
        if abs(np.linalg.norm(RAW[u]-RAW[v]) - TOP) > tol:
            raise AssertionError("Wrong top edge")
    for u,v in [("A","A1"),("B","B1"),("C","C1"),("D","D1")]:
        if abs(np.linalg.norm(RAW[u]-RAW[v]) - LEG) > tol:
            raise AssertionError("Wrong lateral edge")

    if abs(FACE_HEIGHT-3.0) > tol:
        raise AssertionError("Face trapezoid height should be 3")
    if abs(LEG-math.sqrt(10.0)) > tol:
        raise AssertionError("Lateral leg should be sqrt(10)")

    rigid_preflight_chain(ROUTE_B)
    rigid_preflight_chain(ROUTE_D)
    rigid_preflight_chain(BAND)

    db = path_data(ROUTE_B,"A","C")
    dd = path_data(ROUTE_D,"A","C")

    expected = 18.0*math.sqrt(10.0)/5.0
    if abs(db["length"]-expected) > 1e-8:
        raise AssertionError(("Wrong route B length",db["length"],expected))
    if abs(dd["length"]-expected) > 1e-8:
        raise AssertionError(("Wrong route D length",dd["length"],expected))

    # For route via B, the crossing point is 3/5 of the way from B to B'.
    uB = db["hits"][0]["u"]
    if abs(uB-3.0/5.0) > 1e-8:
        raise AssertionError(("Wrong hinge parameter",uB))

    # Exact face-plane calculation:
    # A=(0,0), B=(6,0), A'=(1,3), B'=(5,3)
    # leg BB'=sqrt(10), area triangle ABB'=9
    # distance A to BB' = 18/sqrt(10) = 9sqrt(10)/5
    AM = 9.0*math.sqrt(10.0)/5.0
    BM = 3.0*math.sqrt(10.0)/5.0
    if abs(2*AM-expected) > tol:
        raise AssertionError("Reflection length mismatch")
    if abs(BM/LEG-3.0/5.0) > tol:
        raise AssertionError("BM parameter mismatch")

    # Folded length equals planar length.
    M = db["hits"][0]["raw"]
    folded = np.linalg.norm(RAW["A"]-M) + np.linalg.norm(RAW["C"]-M)
    if abs(folded-expected) > 1e-8:
        raise AssertionError("Folded length mismatch")

    # If bottom is allowed, diagonal AC is shorter.
    base_diag = BOTTOM*math.sqrt(2.0)
    if not (base_diag < expected):
        raise AssertionError("Base diagonal should be shorter")

    # General formula for a square frustum.
    a,b,H = BOTTOM,TOP,HEIGHT
    d = (a-b)/2
    s = math.sqrt(H*H+d*d)
    ell = math.sqrt(H*H+2*d*d)
    general_L = 2*a*s/ell
    general_BM = a*d/ell

    if abs(general_L-expected) > tol:
        raise AssertionError("General L formula mismatch")
    if abs(general_BM-BM) > tol:
        raise AssertionError("General BM formula mismatch")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  square frustum: bottom 6, top 4, height 2sqrt(2)")
        print("  each lateral face: trapezoid bases 6,4; height 3; legs sqrt(10)")
        print("  two symmetric 2-face routes A->C")
        print("  transition point on BB': BM = 3sqrt(10)/5")
        print("  AM = 9sqrt(10)/5")
        print("  Lmin on lateral surface = 18sqrt(10)/5")
        print("  full four-trapezoid band unfolds rigidly")
    return True


def solid(a,b,color=EDGE,width=4.0,opacity=0.96):
    return Line(
        np.array(a,float),np.array(b,float),
        color=color,stroke_width=width,stroke_opacity=opacity
    )


def hidden_edge(a,b,color=DIM,width=2.6,opacity=0.68):
    return DashedLine(
        np.array(a,float),np.array(b,float),
        color=color,stroke_width=width,stroke_opacity=opacity,
        dash_length=0.11,dashed_ratio=0.56
    )


def face_poly(points,color=BLUE,opacity=0.12):
    return Polygon(
        *[np.array(p,float) for p in points],
        fill_color=color,fill_opacity=opacity,stroke_width=0
    )


def frustum_shell():
    p = {k:W(v) for k,v in RAW.items()}

    fills = VGroup(
        face_poly([p[v] for v in FACES["f1"]],PURPLE,0.070),
        face_poly([p[v] for v in FACES["f2"]],CYAN,0.085),
        face_poly([p[v] for v in FACES["top"]],BLUE,0.055),
    )

    visible, hidden = edge_visibility()
    edges = VGroup(*[
        solid(p[u],p[v],EDGE,3.7) for u,v in visible
    ])
    hidden_g = VGroup(*[
        hidden_edge(p[u],p[v]) for u,v in hidden
    ])
    return VGroup(fills,edges,hidden_g)


def highlight_faces(face_names,opacity=0.17):
    return VGroup(*[
        face_poly([W(RAW[v]) for v in FACES[f]],FACE_COLORS[f],opacity)
        for f in face_names
    ])


def vertex_labels(keys):
    offsets = {
        "A":np.array([-0.15,-0.15,-0.05]),
        "B":np.array([ 0.15,-0.15,-0.05]),
        "C":np.array([ 0.15, 0.14,-0.04]),
        "D":np.array([-0.15, 0.14,-0.04]),
        "A1":np.array([-0.12,-0.11,0.13]),
        "B1":np.array([ 0.12,-0.11,0.13]),
        "C1":np.array([ 0.12, 0.11,0.13]),
        "D1":np.array([-0.12, 0.11,0.13]),
    }
    labs = VGroup()
    for k in keys:
        color = GREEN if k=="A" else (RED if k=="C" else INK)
        label = k.replace("1","'")
        labs.add(mty(label,22,color).move_to(W(RAW[k])+offsets[k]))
    return labs


def face_mob(face_name,color,start_vertex=None,end_vertex=None):
    pts = [W(RAW[v]) for v in FACES[face_name]]
    poly = face_poly(pts,color,0.17)
    border = VGroup(*[
        solid(pts[i],pts[(i+1)%4],color,3.2)
        for i in range(4)
    ])
    g = VGroup(poly,border)

    if start_vertex is not None:
        g.add(Dot3D(W(RAW[start_vertex]),radius=0.075,color=GREEN))
    if end_vertex is not None:
        g.add(Dot3D(W(RAW[end_vertex]),radius=0.075,color=RED))
    return g


def make_chain_mobs(chain,start_vertex=None,end_vertex=None):
    mobs = []
    for i,f in enumerate(chain):
        mobs.append(face_mob(
            f,
            FACE_COLORS[f],
            start_vertex if i==0 else None,
            end_vertex if i==len(chain)-1 else None,
        ))
    return mobs


def unfold_animations(scene,chain,mobs,run_each=1.35):
    _,steps,_,_ = unfold_chain_numeric(chain)
    for step in steps:
        i = step["index"]
        downstream = VGroup(*mobs[i:])
        a = W(step["a"])
        b = W(step["b"])

        scene.play(
            Rotate(
                downstream,
                angle=step["angle"],
                axis=b-a,
                about_point=a,
            ),
            run_time=run_each,
            rate_func=smooth,
        )


def net_group(chain,start_vertex,end_vertex,width=5.9,height=4.9):
    d = path_data(chain,start_vertex,end_vertex)
    fc,basis = d["fc"],d["basis"]

    face2 = {}
    all2 = []
    for f in chain:
        arr = [proj2(fc[f][v],basis) for v in FACES[f]]
        face2[f] = arr
        all2 += arr

    all2 = np.array(all2)
    minx,miny = all2.min(axis=0)
    maxx,maxy = all2.max(axis=0)
    scale = min(
        width/max(maxx-minx,1e-9),
        height/max(maxy-miny,1e-9)
    )
    mid = np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q = (np.array(p)-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    g = VGroup()
    for f in chain:
        pts = [T(q) for q in face2[f]]
        g.add(Polygon(
            *pts,
            fill_color=FACE_COLORS[f],
            fill_opacity=0.16,
            stroke_color=FACE_COLORS[f],
            stroke_width=3.0
        ))

    P = T(d["P2"])
    Q = T(d["Q2"])
    g.add(
        Dot(P,radius=0.075,color=GREEN),
        Dot(Q,radius=0.075,color=RED),
        Line(P,Q,color=GOLD,stroke_width=6.5),
    )

    for h in d["hits"]:
        g.add(Dot(T(h["p2"]),radius=0.060,color=GOLD))

    return g,d,T


def folded_route_B():
    d = path_data(ROUTE_B,"A","C")
    M = d["hits"][0]["raw"]
    path = VGroup(
        solid(W(RAW["A"]),W(M),GOLD,6.5),
        solid(W(M),W(RAW["C"]),GOLD,6.5),
        Dot3D(W(M),radius=0.065,color=GOLD),
    )
    return path,[RAW["A"],M,RAW["C"]]


def folded_route_D():
    d = path_data(ROUTE_D,"A","C")
    M = d["hits"][0]["raw"]
    path = VGroup(
        solid(W(RAW["A"]),W(M),CYAN,5.4),
        solid(W(M),W(RAW["C"]),CYAN,5.4),
        Dot3D(W(M),radius=0.060,color=CYAN),
    )
    return path,[RAW["A"],M,RAW["C"]]


def single_face_diagram():
    """Exact 2D trapezoid with bases 6,4 and height 3."""
    A = np.array([0.0,0.0,0.0])
    B = np.array([6.0,0.0,0.0])
    A1 = np.array([1.0,3.0,0.0])
    B1 = np.array([5.0,3.0,0.0])

    pts = np.array([A[:2],B[:2],A1[:2],B1[:2]])
    minx,miny = pts.min(axis=0)
    maxx,maxy = pts.max(axis=0)
    scale = min(5.5/(maxx-minx),4.2/(maxy-miny))
    mid = np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q = (np.array(p[:2])-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    A2,B2,A12,B12 = map(T,[A,B,A1,B1])
    N = T(np.array([5.0,0.0,0.0]))

    g = VGroup(
        Polygon(
            A2,B2,B12,A12,
            fill_color=PURPLE,fill_opacity=0.15,
            stroke_color=PURPLE,stroke_width=3.0
        ),
        DashedLine(B12,N,color=CYAN,stroke_width=2.8,dash_length=0.10),
        Dot(N,radius=0.055,color=CYAN),
    )
    return g,{"A":A2,"B":B2,"A1":A12,"B1":B12,"N":N}


def band_net_2d():
    """Flatten all four lateral trapezoids using the exact rigid engine."""
    chain = BAND
    fc,steps,n0,plane_p = unfold_chain_numeric(chain)
    basis = plane_basis(chain,fc,n0)

    all2 = []
    face2 = {}
    for f in chain:
        arr = [proj2(fc[f][v],basis) for v in FACES[f]]
        face2[f] = arr
        all2 += arr

    all2 = np.array(all2)
    minx,miny = all2.min(axis=0)
    maxx,maxy = all2.max(axis=0)
    scale = min(
        5.9/max(maxx-minx,1e-9),
        4.9/max(maxy-miny,1e-9)
    )
    mid = np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p)-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    g = VGroup()
    for f in chain:
        pts = [T(q) for q in face2[f]]
        g.add(Polygon(
            *pts,
            fill_color=FACE_COLORS[f],
            fill_opacity=0.14,
            stroke_color=FACE_COLORS[f],
            stroke_width=2.8
        ))
    return g


def layout_samples():
    return [
        lesson_card("MÔ HÌNH",[
            ("math","A B=6",28,CYAN),
            ("math","A' B'=4",28,CYAN),
            ("math","H=2 sqrt(2)",28,CYAN),
            ("text","Mỗi mặt bên là hình thang cân.",19,INK),
            ("math","L_(min)=?",34,GOLD),
        ],GOLD),
        lesson_card("KẾT QUẢ",[
            ("math","B M=frac(3 sqrt(10),5)",27,CYAN),
            ("math","A M=frac(9 sqrt(10),5)",27,INK),
            ("math","L_(min)=frac(18 sqrt(10),5)",32,GOLD),
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
        h=header(10,title,progress)
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


class TraiPhang10Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(frustum_shell())
        labs = vertex_labels(["A","B","C","D","A1","B1","C1","D1"])
        for lab in labs:
            self.add_fixed_orientation_mobjects(lab)

        card = intro_card(
            10,
            ["CHÓP CỤT VUÔNG","DẢI HÌNH THANG"],
            "Từ A đến C, chỉ được đi trên các mặt bên.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)

        self.narrate(
            "Video mười chuyển sang chóp cụt vuông. "
            "Các mặt bên không còn là tam giác mà là những hình thang cân.",
            1.5,
        )
        self.narrate(
            "Con kiến bắt đầu tại đỉnh A của đáy lớn và kết thúc tại đỉnh đối diện C, "
            "nhưng chỉ được đi trên các mặt bên.",
            1.6,
        )

    def model(self):
        self.clear_all()
        self.add_hud("Một chóp cụt có số liệu rất gọn","01 / 13")
        self.add(frustum_shell(),highlight_faces(["f1","f2"],0.11))

        card = lesson_card("KÍCH THƯỚC",[
            ("math","A B=6",28,CYAN),
            ("math","A' B'=4",28,CYAN),
            ("math","H=2 sqrt(2)",28,GOLD),
            ("text","Hai đáy là hai hình vuông đồng tâm.",18,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Đáy lớn có cạnh sáu, đáy nhỏ có cạnh bốn, và chiều cao của chóp cụt bằng hai căn hai.",
            1.5,
        )
        self.narrate(
            "Hai đáy đồng tâm và song song. "
            "Mỗi đỉnh của đáy nhỏ lùi vào một đơn vị theo hai phương so với đỉnh tương ứng của đáy lớn.",
            1.8,
        )

    def side_face(self):
        self.clear_all()
        self.add_hud("Mỗi mặt bên là hình thang 6 - 4","02 / 13")
        diag,pts = single_face_diagram()
        self.add_fixed_in_frame_mobjects(diag)

        card = lesson_card("MẶT ABB'A'",[
            ("math","A B=6",27,INK),
            ("math","A' B'=4",27,INK),
            ("text","Mỗi bên lệch vào 1.",18,CYAN),
            ("math","h_(trap)=3",29,GOLD),
            ("math","B B'=sqrt(10)",29,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Xét riêng mặt A B B phẩy A phẩy. "
            "Hai đáy song song dài sáu và bốn, nên mỗi đầu của đáy nhỏ lệch vào một đơn vị.",
            1.7,
        )
        self.narrate(
            "Chiều cao của hình thang trên chính mặt bên bằng căn của tám cộng một, tức bằng ba.",
            1.6,
        )
        self.narrate(
            "Cạnh bên B B phẩy có một đơn vị lệch ngang trên mặt và ba đơn vị theo chiều cao của hình thang, "
            "nên B B phẩy bằng căn mười.",
            1.8,
        )

    def two_routes(self):
        self.clear_all()
        self.add_hud("Từ A đến C có hai hướng đối xứng","03 / 13")
        self.add(frustum_shell())

        pB,_ = folded_route_B()
        pD,_ = folded_route_D()
        self.add(pB,pD)

        card = lesson_card("HAI HƯỚNG",[
            ("text","Qua B: mặt ABB'A' → BCC'B'.",18,GOLD),
            ("text","Qua D: mặt DAA'D' → CDD'C'.",18,CYAN),
            ("text","Hai hướng đối xứng.",19,INK),
            ("text","Chỉ cần giải hướng qua B.",19,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Từ A tới C trên các mặt bên có hai hướng hoàn toàn đối xứng. "
            "Một hướng qua hai mặt kề tại B, hướng kia qua hai mặt kề tại D.",
            1.7,
        )
        self.narrate(
            "Hai hướng có cùng độ dài, nên ta chỉ giải dải gồm mặt A B B phẩy A phẩy và mặt B C C phẩy B phẩy.",
            1.7,
        )

    def arbitrary_x(self):
        self.clear_all()
        self.add_hud("Gọi X là điểm đổi mặt trên BB'","04 / 13")
        self.add(frustum_shell(),highlight_faces(ROUTE_B,0.17))

        X = RAW["B"] + 0.46*(RAW["B1"]-RAW["B"])
        path = VGroup(
            solid(W(RAW["A"]),W(X),ORANGE,6.0),
            solid(W(X),W(RAW["C"]),ORANGE,6.0),
            Dot3D(W(X),radius=0.065,color=ORANGE),
        )
        self.add(path)

        card = lesson_card("VỚI X THUỘC BB'",[
            ("math","L(X)=A X+X C",31,ORANGE),
            ("text","AX nằm trên mặt thứ nhất.",19,INK),
            ("text","XC nằm trên mặt thứ hai.",19,INK),
            ("text","Ta cần chọn X tốt nhất.",19,CYAN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Gọi X là điểm con kiến đổi từ mặt thứ nhất sang mặt thứ hai trên cạnh B B phẩy.",
            1.4,
        )
        self.narrate(
            "Đường đi có độ dài A X cộng X C. "
            "Ta sẽ mở hai hình thang quanh cạnh chung B B phẩy để tìm vị trí X tối ưu.",
            1.7,
        )

    def unfold_two(self):
        self.clear_all()
        self.add_hud("Mở hai hình thang quanh BB'","05 / 13")
        mobs = make_chain_mobs(ROUTE_B,"A","C")
        self.add(*mobs)

        card = lesson_card("TRẢI HAI MẶT",[
            ("text","Giữ mặt ABB'A'.",19,INK),
            ("text","Mở mặt BCC'B' quanh BB'.",19,CYAN),
            ("text","C đi theo chính mặt thứ hai.",19,INK),
            ("text","Hai hình thang nằm chung một mặt phẳng.",18,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta giữ mặt A B B phẩy A phẩy và mở mặt B C C phẩy B phẩy quanh cạnh B B phẩy.",
            1.6,
        )
        unfold_animations(self,ROUTE_B,mobs,run_each=2.2)
        self.narrate(
            "Sau khi mở, hai hình thang cân bằng nhau nằm ở hai phía của cạnh chung B B phẩy.",
            1.5,
        )

    def reflection(self):
        self.clear_all()
        self.add_hud("Ảnh của C là ảnh đối xứng của A","06 / 13")
        net,d,T = net_group(ROUTE_B,"A","C")
        self.add_fixed_in_frame_mobjects(net)

        card = lesson_card("TRÊN BẢN TRẢI",[
            ("text","Gọi C₁ là ảnh của C sau khi mở.",18,INK),
            ("text","A và C₁ đối xứng qua BB'.",18,CYAN),
            ("text","AC₁ vuông góc BB'.",19,GOLD),
            ("text","M là chân đường vuông góc.",19,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Vì hai mặt bên là hai hình thang cân bằng nhau, khi mở quanh B B phẩy, "
            "điểm C chuyển thành điểm C một đối xứng với A qua B B phẩy.",
            1.9,
        )
        self.narrate(
            "Vì vậy đường ngắn nhất A C một vuông góc với B B phẩy. "
            "Gọi M là giao điểm của A C một với B B phẩy.",
            1.6,
        )

    def area_distance(self):
        self.clear_all()
        self.add_hud("Tính khoảng cách từ A đến BB'","07 / 13")
        diag,pts = single_face_diagram()
        self.add_fixed_in_frame_mobjects(diag)

        card = lesson_card("TAM GIÁC ABB'",[
            ("math","K=frac(1,2) times 6 times 3=9",24,INK),
            ("math","K=frac(1,2) times sqrt(10) times A M",23,INK),
            ("math","A M=frac(18,sqrt(10))",27,GOLD),
            ("math","A M=frac(9 sqrt(10),5)",29,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Xét tam giác A B B phẩy nằm trong hình thang thứ nhất. "
            "Lấy A B làm đáy, chiều cao tới A B là ba, nên diện tích tam giác bằng chín.",
            1.8,
        )
        self.narrate(
            "Nếu lấy B B phẩy bằng căn mười làm đáy, chiều cao tương ứng chính là A M. "
            "Do đó chín bằng một nửa nhân căn mười nhân A M.",
            1.8,
        )
        self.narrate(
            "Suy ra A M bằng chín căn mười trên năm.",
            1.3,
        )

    def transition_point(self):
        self.clear_all()
        self.add_hud("M nằm ở đâu trên cạnh BB'?","08 / 13")
        net,d,T = net_group(ROUTE_B,"A","C")
        self.add_fixed_in_frame_mobjects(net)

        card = lesson_card("VỊ TRÍ ĐỔI MẶT",[
            ("text","Đặt β = góc ABB'.",18,CYAN),
            ("math","cos beta=frac(1,sqrt(10))",26,INK),
            ("math","B M=6 cos beta=frac(6,sqrt(10))",25,INK),
            ("math","B M=frac(3 sqrt(10),5)",29,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta còn cần biết chính xác M nằm ở đâu trên B B phẩy.",
            1.3,
        )
        self.narrate(
            "Trong hình thang, từ B tới B phẩy lệch vào một đơn vị và đi lên ba đơn vị. "
            "Vì vậy cos của góc A B B phẩy bằng một trên căn mười.",
            1.8,
        )
        self.narrate(
            "Chiếu A B lên B B phẩy, ta được B M bằng sáu trên căn mười, "
            "hay ba căn mười trên năm.",
            1.6,
        )

    def result(self):
        self.clear_all()
        self.add_hud("Độ dài ngắn nhất","09 / 13")
        net,d,T = net_group(ROUTE_B,"A","C")
        self.add_fixed_in_frame_mobjects(net)

        card = lesson_card("DO ĐỐI XỨNG",[
            ("math","M C_1=A M",29,CYAN),
            ("math","A C_1=2 A M",29,INK),
            ("math","L_(min)=frac(18 sqrt(10),5)",32,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Do A và C một đối xứng qua B B phẩy, M là trung điểm của đoạn A C một.",
            1.5,
        )
        self.narrate(
            "Vì thế đường ngắn nhất bằng hai lần A M. "
            "Kết quả là mười tám căn mười trên năm.",
            1.6,
        )

    def compare_base(self):
        self.clear_all()
        self.add_hud("Nếu được đi trên đáy thì sao?","10 / 13")
        self.add(frustum_shell())

        p={k:W(v) for k,v in RAW.items()}
        self.add(solid(p["A"],p["C"],RED,6.5))
        route,_ = folded_route_B()
        self.add(route)

        card = lesson_card("ĐIỀU KIỆN CHỈ ĐI MẶT BÊN",[
            ("math","A C=6 sqrt(2)",29,RED),
            ("math","L_(side)=frac(18 sqrt(10),5)",26,GOLD),
            ("math","6 sqrt(2)<frac(18 sqrt(10),5)",24,GREEN),
            ("text","Đường chéo đáy ngắn hơn nhưng không hợp lệ.",17,INK),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu được đi trên đáy lớn, con kiến chỉ cần đi theo đường chéo A C dài sáu căn hai.",
            1.5,
        )
        self.narrate(
            "Đường này ngắn hơn đường trên các mặt bên. "
            "Vì vậy điều kiện chỉ đi trên mặt bên vẫn là phần quyết định của bài toán.",
            1.6,
        )

    def full_band(self):
        self.clear_all()
        self.add_hud("Mở cả bốn mặt bên thành một dải","11 / 13")
        band = band_net_2d()
        self.add_fixed_in_frame_mobjects(band)

        card = lesson_card("DẢI BỐN HÌNH THANG",[
            ("text","Mỗi mặt: hình thang cân 6 - 4.",19,INK),
            ("text","Các mặt ghép qua cạnh bên.",19,CYAN),
            ("text","Bản trải không còn là dải chữ nhật.",18,GOLD),
            ("text","Đường tối ưu phụ thuộc dải mặt đã chọn.",18,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Nếu cắt một cạnh bên rồi mở cả bốn mặt, ta được một dải gồm bốn hình thang cân nối tiếp nhau.",
            1.6,
        )
        self.narrate(
            "Khác lăng trụ, dải này không phải một hình chữ nhật dài. "
            "Các cạnh bên nghiêng làm toàn bộ bản trải đổi hướng sau mỗi hình thang.",
            1.8,
        )

    def fold_and_walk(self):
        self.clear_all()
        self.add_hud("Gấp lại và cho kiến đi thật","12 / 13")
        route,pts = folded_route_B()
        self.add(frustum_shell(),highlight_faces(ROUTE_B,0.17),route)

        ant = Dot3D(W(pts[0]),radius=0.085,color=GREEN)
        self.add(ant)

        card = lesson_card("ĐƯỜNG TRÊN CHÓP CỤT",[
            ("text","Đường đi: A → M → C.",19,GOLD),
            ("math","B M=frac(3 sqrt(10),5)",27,CYAN),
            ("math","A M=frac(9 sqrt(10),5)",27,INK),
            ("math","L_(min)=frac(18 sqrt(10),5)",30,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Kiến đi từ A tới M trên mặt A B B phẩy A phẩy.",
            MoveAlongPath(ant,Line(W(pts[0]),W(pts[1]))),
            min_time=2.0,
            rate_func=linear,
        )
        self.narrate_play(
            "Tại M, kiến chuyển sang mặt B C C phẩy B phẩy rồi đi thẳng tới C.",
            MoveAlongPath(ant,Line(W(pts[1]),W(pts[2]))),
            min_time=2.0,
            rate_func=linear,
        )

    def general_formula(self):
        self.clear_all()
        self.add_hud("Công thức tổng quát cho hai mặt kề","13 / 13")
        self.add(frustum_shell())

        card = lesson_card("GỌI ĐÁY LỚN a, ĐÁY NHỎ b",[
            ("math","d=frac(a-b,2)",25,INK),
            ("math","s=sqrt(H^2+d^2)",25,CYAN),
            ("math","l=sqrt(H^2+2d^2)",25,CYAN),
            ("math","L=frac(2a s,l)",28,GOLD),
            ("math","B M=frac(a d,l)",28,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Ta có thể viết công thức chung cho chóp cụt vuông. "
            "Gọi cạnh đáy lớn là a, cạnh đáy nhỏ là b, chiều cao là H, và d bằng a trừ b chia hai.",
            1.8,
        )
        self.narrate(
            "Chiều cao của hình thang bên là căn H bình phương cộng d bình phương. "
            "Cạnh bên của chóp cụt là căn H bình phương cộng hai d bình phương.",
            1.9,
        )
        self.narrate(
            "Với đường từ hai đỉnh đối diện qua hai mặt kề, độ dài ngắn nhất bằng hai a nhân chiều cao hình thang, rồi chia cho cạnh bên.",
            1.8,
        )
        self.narrate(
            "Trong bài này, a bằng sáu, b bằng bốn, H bằng hai căn hai. "
            "Ta thu lại đúng B M bằng ba căn mười trên năm và độ dài mười tám căn mười trên năm.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.model()
        self.side_face()
        self.two_routes()
        self.arbitrary_x()
        self.unfold_two()
        self.reflection()
        self.area_distance()
        self.transition_point()
        self.result()
        self.compare_base()
        self.full_band()
        self.fold_and_walk()
        self.general_formula()


class Smoke10(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=CAM_PHI,theta=CAM_THETA,zoom=0.95)

        # Smoke the two-face unfolding.
        mobs = make_chain_mobs(ROUTE_B,"A","C")
        self.add(*mobs)
        unfold_animations(self,ROUTE_B,mobs,run_each=0.65)
        self.wait(0.1)

        # Smoke the four-face lateral band.
        self.clear()
        mobs = make_chain_mobs(BAND,"A",None)
        self.add(*mobs)
        unfold_animations(self,BAND,mobs,run_each=0.35)
        self.wait(0.1)


def render_smoke():
    geometry_preflight(True)

    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_10_master_smoke"
    config.disable_caching=True

    scene=Smoke10()
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
    config.output_file="trai_phang_10_chop_cut_vuong_MASTER_1080p"
    config.disable_caching=False

    scene=TraiPhang10Master()
    scene.render()

    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)

    master_wav=ROOT/"master_narration_trai_phang_10.wav"
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

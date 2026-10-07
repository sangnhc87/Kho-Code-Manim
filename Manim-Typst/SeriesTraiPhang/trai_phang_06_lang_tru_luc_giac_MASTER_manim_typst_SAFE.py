
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


# ---------- geometry engine: regular hexagonal prism ----------
SIDE = 3.0
HEIGHT = 4.5
RADIUS = SIDE
TURN = 60 * DEGREES

# Bottom regular hexagon A B C D E F, counterclockwise.
angles = [240, 300, 0, 60, 120, 180]
bottom = {
    name: np.array([
        RADIUS * math.cos(math.radians(ang)),
        RADIUS * math.sin(math.radians(ang)),
        0.0
    ])
    for name, ang in zip(["A","B","C","D","E","F"], angles)
}
RAW = {}
for name, p in bottom.items():
    RAW[name] = p
    RAW[name+"1"] = p + np.array([0.0, 0.0, HEIGHT])

FACES = {
    "s1": ["A","B","B1","A1"],
    "s2": ["B","C","C1","B1"],
    "s3": ["C","D","D1","C1"],
    "s4": ["D","E","E1","D1"],
    "s5": ["E","F","F1","E1"],
    "s6": ["F","A","A1","F1"],
}
FACE_COLORS = [PURPLE, CYAN, BLUE, ORANGE, GREEN, GOLD]

CHAIN_SHORT = ["s1","s2"]
CHAIN_LONG = ["s6","s5","s4","s3"]
START = "A"
END = "C1"

CHAIN_SYM_1 = ["s1","s2","s3"]
CHAIN_SYM_2 = ["s6","s5","s4"]
SYM_END = "D1"

WORLD_SCALE = 0.68
WORLD_SHIFT = np.array([-3.20, -0.18, -0.20])


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
        for j in range(i + 1, len(points)):
            vals.append(np.linalg.norm(np.array(points[i]) - np.array(points[j])))
    return np.array(vals)


def shared_edge(f1, f2):
    common = [v for v in FACES[f1] if v in FACES[f2]]
    if len(common) != 2:
        raise ValueError(f"Faces {f1} and {f2} are not adjacent")
    return common


def face_normal(coords):
    q = np.array(coords)
    n = np.cross(q[1] - q[0], q[2] - q[1])
    n = n / np.linalg.norm(n)
    return n


def unfold_chain_numeric(chain):
    fc = {f: {v: RAW[v].copy() for v in FACES[f]} for f in chain}
    base = chain[0]
    base_coords = [fc[base][v] for v in FACES[base]]
    n0 = face_normal(base_coords)
    plane_p = base_coords[0].copy()
    steps = []

    for i in range(1, len(chain)):
        prev, cur = chain[i-1], chain[i]
        edge = shared_edge(prev, cur)
        a = fc[cur][edge[0]].copy()
        b = fc[cur][edge[1]].copy()
        prev_cent = np.mean([fc[prev][v] for v in FACES[prev]], axis=0)

        trials = []
        for sign in (1, -1):
            ang = sign * TURN
            test = {v: rotate_point_axis(fc[cur][v], a, b, ang) for v in FACES[cur]}
            dist = max(abs(np.dot(q - plane_p, n0)) for q in test.values())
            hv = b - a
            prev_side = np.dot(np.cross(hv, prev_cent - a), n0)
            cur_cent = np.mean(list(test.values()), axis=0)
            cur_side = np.dot(np.cross(hv, cur_cent - a), n0)
            overlap_penalty = 1 if prev_side * cur_side >= 0 else 0
            trials.append((round(dist, 12), overlap_penalty, sign))

        trials.sort(key=lambda z: (z[0] > 1e-8, z[1], z[0]))
        ang = trials[0][2] * TURN

        for j in range(i, len(chain)):
            f = chain[j]
            for v in FACES[f]:
                fc[f][v] = rotate_point_axis(fc[f][v], a, b, ang)

        steps.append({"index": i, "edge": edge, "a": a, "b": b, "angle": ang})

    return fc, steps, n0, plane_p


def plane_basis(chain, fc, n0):
    f = chain[0]
    p0 = fc[f][FACES[f][0]].copy()
    e1 = fc[f][FACES[f][1]] - p0
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(n0, e1)
    e2 = e2 / np.linalg.norm(e2)
    return p0, e1, e2


def proj2(x, basis):
    p0, e1, e2 = basis
    d = np.array(x) - p0
    return np.array([np.dot(d, e1), np.dot(d, e2)])


def seg_inter(P, Q, A, B, tol=1e-9):
    P, Q, A, B = map(lambda z: np.array(z, dtype=float), [P, Q, A, B])
    v = Q - P
    w = B - A
    M = np.array([[v[0], -w[0]], [v[1], -w[1]]], dtype=float)
    if abs(np.linalg.det(M)) < 1e-10:
        return None
    t, u = np.linalg.solve(M, A - P)
    if -tol <= t <= 1+tol and -tol <= u <= 1+tol:
        return float(t), float(u), P + t*v
    return None


def path_data(chain, start_vertex, end_vertex):
    fc, steps, n0, plane_p = unfold_chain_numeric(chain)
    basis = plane_basis(chain, fc, n0)
    P3 = fc[chain[0]][start_vertex]
    Q3 = fc[chain[-1]][end_vertex]
    P = proj2(P3, basis)
    Q = proj2(Q3, basis)
    hits = []

    for i in range(len(chain)-1):
        edge = shared_edge(chain[i], chain[i+1])
        A2 = proj2(fc[chain[i]][edge[0]], basis)
        B2 = proj2(fc[chain[i]][edge[1]], basis)
        hit = seg_inter(P, Q, A2, B2)
        if hit is None:
            raise AssertionError(f"Straight line misses hinge {edge}")
        t, u, X2 = hit
        if not (1e-8 < t < 1-1e-8 and 1e-8 < u < 1-1e-8):
            raise AssertionError(f"Hinge crossing not interior: {edge}, t={t}, u={u}")
        raw_a = RAW[edge[0]]
        raw_b = RAW[edge[1]]
        raw_x = raw_a + u*(raw_b-raw_a)
        hits.append({"edge":edge, "t":t, "u":u, "p2":X2, "raw":raw_x})

    if any(hits[i]["t"] >= hits[i+1]["t"]-1e-9 for i in range(len(hits)-1)):
        raise AssertionError("Hinge order is wrong")

    return {
        "fc":fc, "steps":steps, "basis":basis,
        "P2":P, "Q2":Q, "Praw":RAW[start_vertex].copy(), "Qraw":RAW[end_vertex].copy(),
        "hits":hits, "length":float(np.linalg.norm(Q-P)),
    }


def rigid_preflight_chain(chain):
    before = {f:[RAW[v].copy() for v in FACES[f]] for f in chain}
    fc, steps, n0, plane_p = unfold_chain_numeric(chain)
    for f in chain:
        after = [fc[f][v] for v in FACES[f]]
        if not np.allclose(pairwise_distances(before[f]), pairwise_distances(after), atol=1e-9, rtol=0):
            raise AssertionError(f"Face {f} distorted")
        if max(abs(np.dot(q-plane_p, n0)) for q in after) > 1e-8:
            raise AssertionError(f"Face {f} not coplanar")
    return True


def geometry_preflight(verbose=True):
    for ch in [CHAIN_SHORT, CHAIN_LONG, CHAIN_SYM_1, CHAIN_SYM_2]:
        rigid_preflight_chain(ch)

    ds = path_data(CHAIN_SHORT, START, END)
    dl = path_data(CHAIN_LONG, START, END)
    d31 = path_data(CHAIN_SYM_1, START, SYM_END)
    d32 = path_data(CHAIN_SYM_2, START, SYM_END)

    short_expected = math.sqrt((2*SIDE)**2 + HEIGHT**2)
    long_expected = math.sqrt((4*SIDE)**2 + HEIGHT**2)
    sym_expected = math.sqrt((3*SIDE)**2 + HEIGHT**2)

    if abs(ds["length"] - short_expected) > 1e-8:
        raise AssertionError(("short", ds["length"], short_expected))
    if abs(dl["length"] - long_expected) > 1e-8:
        raise AssertionError(("long", dl["length"], long_expected))
    if abs(d31["length"] - sym_expected) > 1e-8 or abs(d32["length"] - sym_expected) > 1e-8:
        raise AssertionError("Symmetric 3-face routes disagree")

    if abs(ds["hits"][0]["u"] - 0.5) > 1e-8:
        raise AssertionError("Short-route hinge should be midpoint")

    long_u = [h["u"] for h in dl["hits"]]
    if not np.allclose(long_u, [0.25,0.50,0.75], atol=1e-8, rtol=0):
        raise AssertionError(("Long-route hinge ratios", long_u))

    if not (ds["length"] < dl["length"]):
        raise AssertionError("Short route must beat long route")

    # General comparison for m=1,2,3 on a hexagonal prism.
    for m in (1,2,3):
        l1 = math.sqrt((m*SIDE)**2 + HEIGHT**2)
        l2 = math.sqrt(((6-m)*SIDE)**2 + HEIGHT**2)
        if m < 3 and not l1 < l2:
            raise AssertionError("Expected shorter circumferential direction")
        if m == 3 and abs(l1-l2) > 1e-9:
            raise AssertionError("Opposite vertex must tie")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  A -> C' short route: 2 faces, L=sqrt((2a)^2+h^2)")
        print("  A -> C' long route: 4 faces, L=sqrt((4a)^2+h^2)")
        print("  short hinge: h/2")
        print("  long hinges: h/4, h/2, 3h/4")
        print("  A -> D' two 3-face routes tie")
    return True


def solid(a,b,color=EDGE,width=4.0,opacity=0.96):
    return Line(np.array(a,float),np.array(b,float),color=color,stroke_width=width,stroke_opacity=opacity)


def hidden_edge(a,b,color=DIM,width=2.5,opacity=0.64):
    return DashedLine(np.array(a,float),np.array(b,float),color=color,stroke_width=width,
                      stroke_opacity=opacity,dash_length=0.10,dashed_ratio=0.56)


def face_poly(points,color=BLUE,opacity=0.12):
    return Polygon(*[np.array(p,float) for p in points],fill_color=color,fill_opacity=opacity,stroke_width=0)


def prism_shell():
    p = {k:W(v) for k,v in RAW.items()}
    # Subtle lateral fills.
    fills = VGroup(*[
        face_poly([p[v] for v in FACES[f]], FACE_COLORS[i], 0.055)
        for i,f in enumerate(["s1","s2","s3","s4","s5","s6"])
    ])
    edges = VGroup()
    names = ["A","B","C","D","E","F"]
    for i,name in enumerate(names):
        nxt = names[(i+1)%6]
        edges.add(solid(p[name],p[nxt],EDGE,3.3))
        edges.add(solid(p[name+"1"],p[nxt+"1"],EDGE,3.3))
        edges.add(solid(p[name],p[name+"1"],EDGE,3.1))
    return VGroup(fills,edges)


def highlight_chain(chain, opacity=0.15):
    g=VGroup()
    for i,f in enumerate(chain):
        g.add(face_poly([W(RAW[v]) for v in FACES[f]], FACE_COLORS[i%len(FACE_COLORS)], opacity))
    return g


def strip_face_mob(face_name,color,start_vertex=None,end_vertex=None):
    pts=[W(RAW[v]) for v in FACES[face_name]]
    poly=face_poly(pts,color,0.16)
    border=VGroup(*[
        solid(pts[i],pts[(i+1)%4],color,3.2) for i in range(4)
    ])
    g=VGroup(poly,border)
    if start_vertex is not None:
        g.add(Dot3D(W(RAW[start_vertex]),radius=0.074,color=GREEN))
    if end_vertex is not None:
        g.add(Dot3D(W(RAW[end_vertex]),radius=0.074,color=RED))
    return g


def make_strip_mobs(chain,start_vertex,end_vertex):
    mobs=[]
    for i,f in enumerate(chain):
        mobs.append(strip_face_mob(
            f, FACE_COLORS[i%len(FACE_COLORS)],
            start_vertex if i==0 else None,
            end_vertex if i==len(chain)-1 else None
        ))
    return mobs


def unfold_animations(scene,chain,face_mobs,run_each=1.35):
    _,steps,_,_=unfold_chain_numeric(chain)
    for step in steps:
        i=step["index"]
        downstream=VGroup(*face_mobs[i:])
        a=W(step["a"]); b=W(step["b"])
        scene.play(Rotate(downstream,angle=step["angle"],axis=b-a,about_point=a),
                   run_time=run_each,rate_func=smooth)


def folded_path_group(chain,start_vertex,end_vertex,width=6.4):
    d=path_data(chain,start_vertex,end_vertex)
    pts=[d["Praw"]]+[h["raw"] for h in d["hits"]]+[d["Qraw"]]
    lines=VGroup(*[
        solid(W(pts[i]),W(pts[i+1]),GOLD,width) for i in range(len(pts)-1)
    ])
    dots=VGroup(*[Dot3D(W(p),radius=0.055,color=GOLD) for p in pts[1:-1]])
    return VGroup(lines,dots),pts,d


def net_group(chain,start_vertex,end_vertex,width=6.0,height=5.0):
    d=path_data(chain,start_vertex,end_vertex)
    fc,basis=d["fc"],d["basis"]
    face2={}
    all2=[]
    for f in chain:
        arr=[proj2(fc[f][v],basis) for v in FACES[f]]
        face2[f]=arr
        all2+=arr
    all2=np.array(all2)
    minx,miny=all2.min(axis=0); maxx,maxy=all2.max(axis=0)
    scale=min(width/max(maxx-minx,1e-9),height/max(maxy-miny,1e-9))
    mid=np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p)-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    g=VGroup()
    for i,f in enumerate(chain):
        pts=[T(q) for q in face2[f]]
        g.add(Polygon(*pts,fill_color=FACE_COLORS[i%len(FACE_COLORS)],fill_opacity=0.15,
                      stroke_color=FACE_COLORS[i%len(FACE_COLORS)],stroke_width=2.8))
    P=T(d["P2"]); Q=T(d["Q2"])
    g.add(Dot(P,radius=0.075,color=GREEN))
    g.add(Dot(Q,radius=0.075,color=RED))
    g.add(Line(P,Q,color=GOLD,stroke_width=6.4))
    for h in d["hits"]:
        g.add(Dot(T(h["p2"]),radius=0.055,color=GOLD))
    return g,d,T


def vertex_labels(keys):
    labs=VGroup()
    for k in keys:
        color=GREEN if k==START else (RED if k in {END,SYM_END} else INK)
        off=np.array([0.0,0.0,0.20])
        lab=mty(k.replace("1","'"),22,color).move_to(W(RAW[k])+off)
        labs.add(lab)
    return labs


def layout_samples():
    return [
        lesson_card("HAI HƯỚNG QUANH KHỐI",[
            ("text","A → C' có hai cách đi quanh mặt bên.",19,INK),
            ("math","L_2 = sqrt((2a)^2+h^2)",28,GOLD),
            ("math","L_4 = sqrt((4a)^2+h^2)",28,CYAN),
            ("math","L_2 < L_4",32,GREEN),
        ],GOLD),
        lesson_card("TRƯỜNG HỢP ĐỐI XỨNG",[
            ("text","A → D' có 3 mặt theo mỗi chiều.",19,INK),
            ("math","L = sqrt((3a)^2+h^2)",29,GOLD),
            ("text","Hai hướng cho cùng kết quả.",19,CYAN),
        ],CYAN),
    ]


class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events=[]
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.90)

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
        h=header(6,title,progress); f=footer(); d=divider()
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


class TraiPhang06Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.add(prism_shell())
        card=intro_card(
            6,
            ["LĂNG TRỤ LỤC GIÁC ĐỀU","HAI HƯỚNG QUANH KHỐI"],
            "Cùng hai đỉnh, nhưng đi theo chiều nào ngắn hơn?",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)
        self.narrate(
            "Với lăng trụ tam giác ở bài trước, hai chiều đi quanh khối là hoàn toàn đối xứng. "
            "Sang lăng trụ lục giác đều, điều thú vị mới xuất hiện: cùng hai đỉnh nhưng một chiều có thể đi qua ít mặt hơn chiều kia.",
            1.8,
        )
        self.narrate(
            "Ta sẽ bắt đầu tại đỉnh A ở đáy dưới và kết thúc tại C phẩy ở đáy trên. "
            "Cả hai đường đều chỉ đi trên các mặt bên của lăng trụ.",
            1.6,
        )

    def problem(self):
        self.clear_all()
        self.add_hud("Từ A đến C' trên các mặt bên","01 / 12")
        self.add(prism_shell(),highlight_chain(CHAIN_SHORT,0.12),highlight_chain(CHAIN_LONG,0.07))
        self.add_fixed_orientation_mobjects(*list(vertex_labels(["A","B","C","C1"])))
        card=lesson_card("BÀI TOÁN",[
            ("math","A B=B C=C D=D E=E F=F A=a",23,CYAN),
            ("math","A A'=h",27,CYAN),
            ("text","Điểm đầu A, điểm cuối C'.",19,INK),
            ("text","Chỉ được đi trên các mặt bên.",19,INK),
            ("text","Có hai hướng đi quanh lăng trụ.",19,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Đáy là lục giác đều cạnh a, còn chiều cao lăng trụ là h. "
            "Từ A tới C phẩy, nếu nhìn quanh chu vi đáy, ta có thể đi theo chiều qua B, hoặc đi theo chiều ngược lại qua F, E và D.",
            1.8,
        )
        self.narrate(
            "Hai hướng đều hợp lệ. Nhưng số mặt phải đi qua khác nhau, nên chưa thể kết luận bằng mắt hướng nào ngắn hơn.",
            1.5,
        )

    def two_routes_3d(self):
        self.clear_all()
        self.add_hud("Hai dải mặt cạnh tranh","02 / 12")
        self.add(prism_shell())
        short=highlight_chain(CHAIN_SHORT,0.18)
        long=highlight_chain(CHAIN_LONG,0.12)
        self.add(short,long)
        card=lesson_card("HAI PHƯƠNG ÁN",[
            ("text","Hướng ngắn quanh chu vi:",19,GOLD),
            ("text","AB B'A' → BC C'B'  (2 mặt)",19,INK),
            ("text","Hướng còn lại:",19,CYAN),
            ("text","FA A'F' → EF F'E' → DE E'D' → CD D'C'  (4 mặt)",17,INK),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Hướng thứ nhất đi qua đúng hai mặt bên: mặt A B B phẩy A phẩy và mặt B C C phẩy B phẩy.",
            1.4,
        )
        self.narrate(
            "Hướng thứ hai đi vòng phía còn lại của lăng trụ nên phải qua bốn mặt bên liên tiếp. "
            "Ta sẽ trải cả hai dải rồi so sánh.",
            1.6,
        )

    def unfold_short(self):
        self.clear_all()
        self.add_hud("Hướng 1 · Đi qua 2 mặt","03 / 12")
        mobs=make_strip_mobs(CHAIN_SHORT,START,END)
        self.add(*mobs)
        card=lesson_card("MỞ HAI MẶT",[
            ("text","Giữ mặt ABB'A'.",19,INK),
            ("text","Mở mặt BCC'B' quanh BB'.",19,CYAN),
            ("text","Sau khi mở: hình chữ nhật 2a × h.",19,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Ta giữ mặt A B B phẩy A phẩy và mở mặt B C C phẩy B phẩy quanh cạnh B B phẩy.",
            1.5,
        )
        unfold_animations(self,CHAIN_SHORT,mobs,run_each=1.8)
        self.narrate(
            "Hai mặt nằm phẳng thành một hình chữ nhật có chiều dài hai a và chiều cao h.",
            1.4,
        )

    def short_net(self):
        self.clear_all()
        self.add_hud("Đường ngắn nhất theo hướng 2 mặt","04 / 12")
        net,d,T=net_group(CHAIN_SHORT,START,END)
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("HƯỚNG 1",[
            ("math","L_2=sqrt((2a)^2+h^2)",30,GOLD),
            ("math","L_2=sqrt(4a^2+h^2)",30,GOLD),
            ("text","Đường thẳng cắt BB' tại trung điểm.",19,INK),
            ("math","B X=frac(h,2)",29,CYAN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Trong bản trải này, đường ngắn nhất từ A tới ảnh của C phẩy là đường chéo của hình chữ nhật hai a nhân h.",
            1.5,
        )
        self.narrate(
            "Vì vậy độ dài phương án thứ nhất là căn của bốn a bình phương cộng h bình phương. "
            "Đường chéo cắt cạnh B B phẩy đúng tại trung điểm.",
            1.7,
        )

    def unfold_long(self):
        self.clear_all()
        self.add_hud("Hướng 2 · Đi vòng qua 4 mặt","05 / 12")
        mobs=make_strip_mobs(CHAIN_LONG,START,END)
        self.add(*mobs)
        card=lesson_card("MỞ BỐN MẶT",[
            ("text","Giữ mặt FAA'F'.",19,INK),
            ("text","Mở lần lượt qua FF', EE', DD'.",19,CYAN),
            ("text","Bốn mặt tạo hình chữ nhật 4a × h.",19,GOLD),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Bây giờ đi theo chiều ngược lại. Ta giữ mặt F A A phẩy F phẩy rồi mở lần lượt ba mặt tiếp theo quanh F F phẩy, E E phẩy và D D phẩy.",
            1.8,
        )
        unfold_animations(self,CHAIN_LONG,mobs,run_each=1.15)
        self.narrate(
            "Khi bốn mặt đã nằm phẳng, ta nhận được một hình chữ nhật có chiều dài bốn a và chiều cao h.",
            1.5,
        )

    def long_net(self):
        self.clear_all()
        self.add_hud("Đường ngắn nhất theo hướng 4 mặt","06 / 12")
        net,d,T=net_group(CHAIN_LONG,START,END,width=6.0,height=4.8)
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("HƯỚNG 2",[
            ("math","L_4=sqrt((4a)^2+h^2)",30,CYAN),
            ("math","L_4=sqrt(16a^2+h^2)",30,CYAN),
            ("math","F X_1=frac(h,4)",27,INK),
            ("math","E X_2=frac(h,2)",27,INK),
            ("math","D X_3=frac(3h,4)",27,INK),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Đường ngắn nhất của dải bốn mặt là đường chéo của hình chữ nhật bốn a nhân h. "
            "Do đó độ dài là căn của mười sáu a bình phương cộng h bình phương.",
            1.7,
        )
        self.narrate(
            "Ba lần đổi mặt xảy ra lần lượt ở độ cao một phần tư h, một phần hai h và ba phần tư h.",
            1.5,
        )

    def compare(self):
        self.clear_all()
        self.add_hud("So sánh hai hướng","07 / 12")
        self.add(prism_shell(),highlight_chain(CHAIN_SHORT,0.14),highlight_chain(CHAIN_LONG,0.07))
        card=lesson_card("SO SÁNH BÌNH PHƯƠNG",[
            ("math","L_2^2=4a^2+h^2",29,GOLD),
            ("math","L_4^2=16a^2+h^2",29,CYAN),
            ("math","L_4^2-L_2^2=12a^2",29,INK),
            ("math","L_2<L_4",34,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Ta không cần bấm máy. Hai phương án có cùng phần h bình phương, nên chỉ cần so sánh bốn a bình phương với mười sáu a bình phương.",
            1.6,
        )
        self.narrate(
            "Hiệu hai bình phương bằng mười hai a bình phương, luôn dương. "
            "Vì vậy hướng đi qua hai mặt luôn ngắn hơn hướng vòng qua bốn mặt.",
            1.7,
        )

    def fold_short_and_walk(self):
        self.clear_all()
        self.add_hud("Gấp lại hướng tối ưu","08 / 12")
        path,pts,d=folded_path_group(CHAIN_SHORT,START,END)
        self.add(prism_shell(),highlight_chain(CHAIN_SHORT,0.16),path)
        ant=Dot3D(W(pts[0]),radius=0.082,color=GREEN)
        self.add(ant)
        card=lesson_card("ĐƯỜNG TỐI ƯU",[
            ("text","A → X → C'",19,GOLD),
            ("math","B X=frac(h,2)",29,CYAN),
            ("math","L_(min)=sqrt(4a^2+h^2)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate_play(
            "Kiến đi trên mặt A B B phẩy A phẩy từ A tới trung điểm X của B B phẩy.",
            MoveAlongPath(ant,Line(W(pts[0]),W(pts[1]))),
            min_time=2.0,rate_func=linear,
        )
        self.narrate_play(
            "Từ X, nó sang mặt B C C phẩy B phẩy và đi thẳng tới C phẩy.",
            MoveAlongPath(ant,Line(W(pts[1]),W(pts[2]))),
            min_time=2.0,rate_func=linear,
        )

    def symmetric_case(self):
        self.clear_all()
        self.add_hud("Khi hai hướng dài bằng nhau","09 / 12")
        self.add(prism_shell())
        self.add(highlight_chain(CHAIN_SYM_1,0.13),highlight_chain(CHAIN_SYM_2,0.08))
        card=lesson_card("ĐỔI ĐIỂM CUỐI THÀNH D'",[
            ("text","A và D là hai đỉnh đối diện của lục giác.",19,INK),
            ("text","Mỗi chiều quanh khối đều qua 3 mặt.",19,CYAN),
            ("math","L=sqrt((3a)^2+h^2)",30,GOLD),
            ("text","Hai hướng cho cùng một độ dài.",19,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Bây giờ chỉ thay điểm cuối C phẩy bằng D phẩy. A và D là hai đỉnh đối diện của lục giác đều.",
            1.5,
        )
        self.narrate(
            "Đi theo chiều nào cũng phải qua đúng ba mặt bên. Vì thế hai bản trải đều có chiều dài ba a và chiều cao h, nên hai hướng cho cùng kết quả.",
            1.8,
        )

    def general_rule(self):
        self.clear_all()
        self.add_hud("Quy tắc tổng quát cho lục giác đều","10 / 12")
        self.add(prism_shell())
        card=lesson_card("GỌI m LÀ SỐ CẠNH THEO MỘT CHIỀU",[
            ("math","L_m=sqrt((ma)^2+h^2)",28,GOLD),
            ("math","L_(6-m)=sqrt(((6-m)a)^2+h^2)",27,CYAN),
            ("text","Xét m = 1, 2 hoặc 3.",19,INK),
            ("text","Chọn chiều có số cạnh nhỏ hơn.",19,GREEN),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Ta có thể gom cả bài toán vào một quy tắc. Nếu theo một chiều quanh đáy cần đi qua m cạnh, chiều còn lại cần sáu trừ m cạnh.",
            1.7,
        )
        self.narrate(
            "Hai độ dài tương ứng là căn của m a tất cả bình phương cộng h bình phương, và căn của sáu trừ m nhân a tất cả bình phương cộng h bình phương.",
            1.9,
        )
        self.narrate(
            "Vì h giống nhau ở cả hai phương án, ta chỉ cần chọn chiều có số cạnh quanh đáy nhỏ hơn. Nếu m bằng ba thì hai chiều hòa nhau.",
            1.7,
        )

    def concrete_example(self):
        self.clear_all()
        self.add_hud("Ví dụ nhanh với h=3a","11 / 12")
        self.add(prism_shell(),highlight_chain(CHAIN_SHORT,0.14),highlight_chain(CHAIN_LONG,0.07))
        card=lesson_card("A → C'",[
            ("math","h=3a",28,CYAN),
            ("math","L_2=sqrt(4a^2+9a^2)=a sqrt(13)",27,GOLD),
            ("math","L_4=sqrt(16a^2+9a^2)=5a",27,CYAN),
            ("math","a sqrt(13)<5a",30,GREEN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Chẳng hạn nếu chiều cao bằng ba a, hướng qua hai mặt có độ dài a căn mười ba, còn hướng vòng qua bốn mặt dài đúng năm a.",
            1.7,
        )
        self.narrate(
            "Ví dụ số này chỉ để kiểm tra trực giác. Kết luận hướng hai mặt ngắn hơn đã được chứng minh đúng với mọi h dương.",
            1.5,
        )

    def summary(self):
        self.clear_all()
        self.add_hud("Chốt bài lăng trụ lục giác","12 / 12")
        self.add(prism_shell())
        card=lesson_card("BA Ý CẦN NHỚ",[
            ("text","1. Cùng hai đỉnh có thể có hai hướng quanh khối.",18,INK),
            ("text","2. Trải từng hướng thành một hình chữ nhật.",18,INK),
            ("text","3. So sánh chiều dài quanh đáy trước.",18,INK),
            ("math","A -> C': L_(min)=sqrt(4a^2+h^2)",27,GOLD),
            ("math","A -> D': L=sqrt(9a^2+h^2)",27,CYAN),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Lăng trụ lục giác cho ta bài học mới: trước khi tính toán, hãy nhìn xem từ điểm đầu tới điểm cuối có bao nhiêu hướng quanh chu vi đáy.",
            1.7,
        )
        self.narrate(
            "Mỗi hướng tạo ra một bản trải khác nhau. Với A tới C phẩy, hướng qua hai mặt thắng hướng qua bốn mặt. "
            "Với A tới D phẩy, hai hướng ba mặt hoàn toàn đối xứng và có cùng độ dài.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.problem()
        self.two_routes_3d()
        self.unfold_short()
        self.short_net()
        self.unfold_long()
        self.long_net()
        self.compare()
        self.fold_short_and_walk()
        self.symmetric_case()
        self.general_rule()
        self.concrete_example()
        self.summary()


class Smoke06(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.9)
        for chain,s,e in [(CHAIN_SHORT,START,END),(CHAIN_LONG,START,END)]:
            self.clear()
            mobs=make_strip_mobs(chain,s,e)
            self.add(*mobs)
            unfold_animations(self,chain,mobs,run_each=0.35)
            self.wait(0.1)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_06_master_smoke"
    config.disable_caching=True
    scene=Smoke06()
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
    config.output_file="trai_phang_06_lang_tru_luc_giac_MASTER_1080p"
    config.disable_caching=False
    scene=TraiPhang06Master()
    scene.render()
    video_path=Path(scene.renderer.file_writer.movie_file_path)
    duration=probe_duration(video_path)
    master_wav=ROOT/"master_narration_trai_phang_06.wav"
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

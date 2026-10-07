
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

# ---------- geometry engine: regular triangular prism ----------
SIDE = 3.0
HEIGHT = 4.0
SQ3 = math.sqrt(3.0)

A0 = np.array([-SIDE/2, -SQ3*SIDE/6, 0.0])
B0 = np.array([ SIDE/2, -SQ3*SIDE/6, 0.0])
C0 = np.array([0.0, SQ3*SIDE/3, 0.0])
UPV = np.array([0.0, 0.0, HEIGHT])

RAW = {
    "A": A0, "B": B0, "C": C0,
    "A1": A0 + UPV, "B1": B0 + UPV, "C1": C0 + UPV,
}

FACES = {
    "side1": ["A", "B", "B1", "A1"],
    "side2": ["B", "C", "C1", "B1"],
    "side3": ["C", "A", "A1", "C1"],
}
FACE_COLORS = [PURPLE, CYAN, ORANGE]
CHAIN = ["side1", "side2", "side3"]
START = "A"
END = "A1"
WORLD_SCALE = 0.83
WORLD_SHIFT = np.array([-3.15, -0.20, -0.15])


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


def unfold_chain_numeric(chain=CHAIN):
    fc = {f: {v: RAW[v].copy() for v in FACES[f]} for f in chain}
    steps = []

    # For an equilateral triangular prism, flattening each next lateral face
    # into the plane of side1 requires a -120 degree rigid rotation.
    for i in range(1, len(chain)):
        prev, cur = chain[i - 1], chain[i]
        edge = shared_edge(prev, cur)
        a = fc[cur][edge[0]].copy()
        b = fc[cur][edge[1]].copy()
        angle = -120 * DEGREES

        for j in range(i, len(chain)):
            f = chain[j]
            for v in FACES[f]:
                fc[f][v] = rotate_point_axis(fc[f][v], a, b, angle)

        steps.append({"index": i, "edge": edge, "a": a, "b": b, "angle": angle})

    return fc, steps


def plane_basis(fc):
    p0 = fc["side1"]["A"].copy()
    e1 = fc["side1"]["B"] - p0
    e1 = e1 / np.linalg.norm(e1)
    e2 = fc["side1"]["A1"] - p0
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
    if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
        return float(t), float(u), P + t * v
    return None


def path_data(chain=CHAIN, start_vertex=START, end_vertex=END):
    fc, steps = unfold_chain_numeric(chain)
    basis = plane_basis(fc)
    P3 = fc[chain[0]][start_vertex]
    Q3 = fc[chain[-1]][end_vertex]
    P = proj2(P3, basis)
    Q = proj2(Q3, basis)
    hits = []

    for i in range(len(chain) - 1):
        edge = shared_edge(chain[i], chain[i + 1])
        A2 = proj2(fc[chain[i]][edge[0]], basis)
        B2 = proj2(fc[chain[i]][edge[1]], basis)
        hit = seg_inter(P, Q, A2, B2)
        if hit is None:
            raise AssertionError(f"Straight line misses hinge {edge}")
        t, u, X2 = hit
        if not (1e-8 < t < 1 - 1e-8 and 1e-8 < u < 1 - 1e-8):
            raise AssertionError(f"Hinge crossing not strictly inside {edge}: t={t}, u={u}")
        raw_a = RAW[edge[0]]
        raw_b = RAW[edge[1]]
        raw_x = raw_a + u * (raw_b - raw_a)
        hits.append({"edge": edge, "t": t, "u": u, "p2": X2, "raw": raw_x})

    if any(hits[i]["t"] >= hits[i+1]["t"] - 1e-9 for i in range(len(hits)-1)):
        raise AssertionError("Hinge crossings are not in order")

    return {
        "fc": fc,
        "steps": steps,
        "basis": basis,
        "P2": P,
        "Q2": Q,
        "Praw": RAW[start_vertex].copy(),
        "Qraw": RAW[end_vertex].copy(),
        "hits": hits,
        "length": float(np.linalg.norm(Q - P)),
    }


def geometry_preflight(verbose=True):
    fc0 = {f: {v: RAW[v].copy() for v in FACES[f]} for f in CHAIN}
    fc, steps = unfold_chain_numeric(CHAIN)

    # 1) Each rectangular side face remains rigid.
    for f in CHAIN:
        before = [fc0[f][v] for v in FACES[f]]
        after = [fc[f][v] for v in FACES[f]]
        if not np.allclose(pairwise_distances(before), pairwise_distances(after), atol=1e-9, rtol=0):
            raise AssertionError(f"Face {f} distorted")

    # 2) All three unfolded side faces are coplanar with side1.
    y0 = RAW["A"][1]
    for f in CHAIN:
        for v in FACES[f]:
            if abs(fc[f][v][1] - y0) > 1e-8:
                raise AssertionError(f"Face {f} not coplanar after unfold")

    # 3) End image is exactly three side lengths away horizontally and h vertically.
    d = path_data()
    dx = abs(d["Q2"][0] - d["P2"][0])
    dy = abs(d["Q2"][1] - d["P2"][1])
    if abs(dx - 3*SIDE) > 1e-8 or abs(dy - HEIGHT) > 1e-8:
        raise AssertionError((dx, dy))

    expected = math.sqrt((3*SIDE)**2 + HEIGHT**2)
    if abs(d["length"] - expected) > 1e-8:
        raise AssertionError((d["length"], expected))

    # 4) Crossings occur at 1/3 and 2/3 of the whole straight segment,
    # and at heights h/3 and 2h/3 on BB' and CC'.
    expected_t = [1/3, 2/3]
    expected_u = [1/3, 2/3]
    for hrec, t0, u0 in zip(d["hits"], expected_t, expected_u):
        if abs(hrec["t"] - t0) > 1e-8 or abs(hrec["u"] - u0) > 1e-8:
            raise AssertionError((hrec, t0, u0))

    # 5) Folded three-segment route has exactly the same length.
    pts = [d["Praw"]] + [hrec["raw"] for hrec in d["hits"]] + [d["Qraw"]]
    folded = sum(np.linalg.norm(pts[i+1]-pts[i]) for i in range(len(pts)-1))
    if abs(folded - expected) > 1e-8:
        raise AssertionError((folded, expected))

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  regular triangular prism lateral strip")
        print("  rigid unfold angles: -120 deg, -120 deg")
        print("  net size: 3a x h")
        print("  BX = h/3, CY = 2h/3")
        print("  L = sqrt(9a^2+h^2)")
    return True


# ---------- drawing ----------
def solid(a, b, color=EDGE, width=4.0, opacity=0.96):
    return Line(np.array(a,float), np.array(b,float), color=color, stroke_width=width, stroke_opacity=opacity)


def hidden_edge(a, b, color=DIM, width=2.6, opacity=0.68):
    return DashedLine(np.array(a,float), np.array(b,float), color=color, stroke_width=width,
                      stroke_opacity=opacity, dash_length=0.11, dashed_ratio=0.56)


def face_poly(points, color=BLUE, opacity=0.12):
    return Polygon(*[np.array(p,float) for p in points], fill_color=color,
                   fill_opacity=opacity, stroke_width=0)


def prism_shell():
    p = {k: W(v) for k,v in RAW.items()}
    side1 = face_poly([p[v] for v in FACES["side1"]], PURPLE, 0.07)
    side2 = face_poly([p[v] for v in FACES["side2"]], CYAN, 0.09)
    top = face_poly([p["A1"],p["B1"],p["C1"]], BLUE, 0.07)

    visible_pairs = [
        ("A","B"),("B","C"),
        ("A","A1"),("B","B1"),("C","C1"),
        ("A1","B1"),("B1","C1"),("C1","A1"),
    ]
    hidden_pairs = [("C","A")]

    edges = VGroup(*[solid(p[u],p[v],EDGE,3.8) for u,v in visible_pairs])
    hidden = VGroup(*[hidden_edge(p[u],p[v]) for u,v in hidden_pairs])
    return VGroup(side1, side2, top, edges, hidden)


def highlight_chain():
    g = VGroup()
    for i,f in enumerate(CHAIN):
        pts = [W(RAW[v]) for v in FACES[f]]
        g.add(face_poly(pts, FACE_COLORS[i], 0.13))
    return g


def label_vertices(scene, keys=("A","B","C","A1","B1","C1")):
    pretty = {"A":"A","B":"B","C":"C","A1":"A'","B1":"B'","C1":"C'"}
    offsets = {
        "A": np.array([-0.14,-0.12,-0.05]),
        "B": np.array([0.14,-0.12,-0.05]),
        "C": np.array([0.05,0.16,-0.03]),
        "A1":np.array([-0.15,-0.08,0.14]),
        "B1":np.array([0.14,-0.08,0.14]),
        "C1":np.array([0.05,0.14,0.14]),
    }
    for k in keys:
        color = GREEN if k=="A" else (RED if k=="A1" else INK)
        lab = mty(pretty[k], 23, color).move_to(W(RAW[k]) + offsets[k])
        scene.add_fixed_orientation_mobjects(lab)


def strip_face_mob(face_name, color, start_vertex=None, end_vertex=None):
    pts = [W(RAW[v]) for v in FACES[face_name]]
    poly = face_poly(pts, color, 0.17)
    border = VGroup(*[solid(pts[i], pts[(i+1)%4], color, 3.2) for i in range(4)])
    g = VGroup(poly, border)
    if start_vertex is not None:
        g.add(Dot3D(W(RAW[start_vertex]), radius=0.075, color=GREEN))
    if end_vertex is not None:
        g.add(Dot3D(W(RAW[end_vertex]), radius=0.075, color=RED))
    return g


def make_strip_mobs():
    mobs=[]
    for i,f in enumerate(CHAIN):
        mobs.append(strip_face_mob(
            f, FACE_COLORS[i],
            START if i==0 else None,
            END if i==len(CHAIN)-1 else None,
        ))
    return mobs


def unfold_animations(scene, face_mobs, run_each=1.5):
    _, steps = unfold_chain_numeric(CHAIN)
    for step in steps:
        i = step["index"]
        downstream = VGroup(*face_mobs[i:])
        a = W(step["a"])
        b = W(step["b"])
        scene.play(
            Rotate(downstream, angle=step["angle"], axis=b-a, about_point=a),
            run_time=run_each, rate_func=smooth,
        )


def folded_path_group(width=6.5):
    d = path_data()
    pts = [d["Praw"]] + [hrec["raw"] for hrec in d["hits"]] + [d["Qraw"]]
    lines = VGroup(*[solid(W(pts[i]),W(pts[i+1]),GOLD,width) for i in range(len(pts)-1)])
    dots = VGroup(*[Dot3D(W(p),radius=0.058,color=GOLD) for p in pts[1:-1]])
    return VGroup(lines,dots), pts, d


def net_group(width=6.0, height=5.0):
    d = path_data()
    fc, basis = d["fc"], d["basis"]
    face2={}
    all2=[]
    for f in CHAIN:
        arr=[proj2(fc[f][v],basis) for v in FACES[f]]
        face2[f]=arr
        all2 += arr
    all2=np.array(all2)
    minx,miny=all2.min(axis=0)
    maxx,maxy=all2.max(axis=0)
    scale=min(width/max(maxx-minx,1e-9), height/max(maxy-miny,1e-9))
    mid=np.array([(minx+maxx)/2,(miny+maxy)/2])

    def T(p):
        q=(np.array(p)-mid)*scale
        return np.array([q[0]+LEFT_CENTER[0],q[1]+LEFT_CENTER[1],0.0])

    g=VGroup()
    for i,f in enumerate(CHAIN):
        pts=[T(q) for q in face2[f]]
        g.add(Polygon(*pts,fill_color=FACE_COLORS[i],fill_opacity=0.15,
                      stroke_color=FACE_COLORS[i],stroke_width=2.8))
    P=T(d["P2"]); Q=T(d["Q2"])
    g.add(Dot(P,radius=0.075,color=GREEN),Dot(Q,radius=0.075,color=RED))
    g.add(Line(P,Q,color=GOLD,stroke_width=6.5))
    for hrec in d["hits"]:
        g.add(Dot(T(hrec["p2"]),radius=0.055,color=GOLD))
    return g,d,T
class BaseLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(phi=67*DEGREES, theta=-48*DEGREES, zoom=0.98)

    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def narrate_play(self, text, *anims, min_time=1.0, rate_func=smooth):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.play(*anims, run_time=max(dur, min_time), rate_func=rate_func)
        return dur

    def add_hud(self, video_no, title, progress):
        h = header(video_no, title, progress)
        f = footer()
        d = divider()
        self.add_fixed_in_frame_mobjects(h, f, d)
        return VGroup(h, f, d)

    def clear_all(self, run_time=0.30):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
        self.clear()

def narration_lint(source_path: Path, verbose=True):
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    spoken = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fname = node.func.attr if isinstance(node.func, ast.Attribute) else None
            if fname in {"narrate", "narrate_play"} and node.args:
                first = node.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    spoken.append(first.value)

    forbidden = [
        "workflow", "render", "preflight", "engine", "code", "mã nguồn",
        "camera", "animation", "cột trái", "cột phải", "debug",
    ]
    bad = []
    for text_value in spoken:
        low = text_value.lower()
        for word in forbidden:
            if word in low:
                bad.append((word, text_value))
    if bad:
        raise AssertionError(f"Production jargon leaked into narration: {bad}")
    if verbose:
        print(f"NARRATION LINT OK: {len(spoken)} spoken segments")
    return True


# ==========================================================
# VIDEO 05 MASTER — LĂNG TRỤ ĐỨNG TAM GIÁC ĐỀU, 3 MẶT BÊN
# ==========================================================

def layout_samples():
    return [
        lesson_card("BÀI TOÁN", [
            ("text","Lăng trụ đứng tam giác đều.",20,INK),
            ("math","A B=B C=C A=a",27,CYAN),
            ("math","A A'=h",27,CYAN),
            ("text","Kiến đi từ A tới A'.",20,INK),
            ("text","Phải đi qua đủ ba mặt bên.",19,GOLD),
        ], GOLD),
        lesson_card("BẢN TRẢI", [
            ("math","Delta x=3a",29,CYAN),
            ("math","Delta y=h",29,CYAN),
            ("math","L=sqrt(9a^2+h^2)",31,GOLD),
        ], CYAN),
    ]


class TraiPhang05Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES,theta=-48*DEGREES,zoom=0.92)
        self.add(prism_shell(), highlight_chain())
        label_vertices(self, ("A","A1"))
        card=intro_card(
            5,
            ["LĂNG TRỤ TAM GIÁC ĐỀU", "KIẾN ĐI QUA 3 MẶT BÊN"],
            "Một vòng quanh mặt bên, từ đỉnh A đến đỉnh A'.",
        )
        self.add_fixed_in_frame_mobjects(card,divider(),footer())
        self.play(FadeIn(card),run_time=0.7)
        self.narrate(
            "Ta chuyển sang một khối mới: lăng trụ đứng có đáy là tam giác đều. "
            "Con kiến bắt đầu ở đỉnh A và kết thúc ở đỉnh A phẩy.",
            1.6,
        )
        self.narrate(
            "Nếu được đi tự do, kiến chỉ cần đi theo cạnh A A phẩy. "
            "Nhưng trong bài này, nó phải đi vòng qua đủ ba mặt bên trước khi tới A phẩy.",
            1.7,
        )

    def setup_problem(self):
        self.clear_all()
        self.add_hud(5,"Từ A đến A' qua đủ ba mặt bên","01 / 12")
        self.add(prism_shell(), highlight_chain())
        label_vertices(self)
        p={k:W(v) for k,v in RAW.items()}
        self.add(Dot3D(p["A"],radius=0.08,color=GREEN),Dot3D(p["A1"],radius=0.08,color=RED))

        card=lesson_card("DỮ KIỆN",[
            ("math","A B=B C=C A=a",27,CYAN),
            ("math","A A'=B B'=C C'=h",25,CYAN),
            ("text","Điểm đầu A, điểm cuối A'.",19,INK),
            ("text","Phải đi qua đủ 3 mặt bên.",19,GOLD),
            ("math","L_(min)=?",34,RED),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Đáy A B C là tam giác đều cạnh a. Ba cạnh bên A A phẩy, B B phẩy và C C phẩy đều dài h và vuông góc với đáy.",
            1.7,
        )
        self.narrate(
            "Ta yêu cầu kiến đi lần lượt qua mặt A B B phẩy A phẩy, rồi B C C phẩy B phẩy, rồi C A A phẩy C phẩy. "
            "Như vậy kiến sẽ đổi mặt hai lần.",
            1.8,
        )

    def compare_free_path(self):
        self.clear_all()
        self.add_hud(5,"Đừng quên điều kiện của bài toán","02 / 12")
        self.add(prism_shell())
        label_vertices(self,("A","A1"))
        p={k:W(v) for k,v in RAW.items()}
        direct=solid(p["A"],p["A1"],RED,7.0)
        self.play(Create(direct),run_time=0.7)

        card=lesson_card("NẾU ĐI TỰ DO",[
            ("math","A A'=h",35,RED),
            ("text","Đây là đường ngắn nhất nếu không có ràng buộc.",18,INK),
            ("text","Nhưng nó không đi qua ba mặt bên.",19,MUTED),
            ("text","Bài đang hỏi một đường đi khác.",19,CYAN),
        ],RED)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Trước khi trải phẳng, ta phải đọc đúng đề. Nếu bỏ điều kiện đi qua ba mặt bên, đáp án chỉ là cạnh A A phẩy, dài h.",
            1.6,
        )
        self.narrate(
            "Vì vậy kết quả sắp tìm là đường ngắn nhất trong dải ba mặt bên đã cho, không phải đường ngắn nhất tự do trên toàn bộ khối.",
            1.7,
        )

    def show_hinges(self):
        self.clear_all()
        self.add_hud(5,"Hai lần đổi mặt","03 / 12")
        self.add(prism_shell(),highlight_chain())
        label_vertices(self)
        p={k:W(v) for k,v in RAW.items()}
        hinges=VGroup(
            solid(p["B"],p["B1"],GOLD,7.0),
            solid(p["C"],p["C1"],ORANGE,7.0),
        )
        self.play(Create(hinges),run_time=0.8)

        card=lesson_card("HAI CẠNH CHUNG",[
            ("math","X in B B'",27,GOLD),
            ("math","Y in C C'",27,ORANGE),
            ("text","A → X nằm trên mặt thứ nhất.",18,INK),
            ("text","X → Y nằm trên mặt thứ hai.",18,INK),
            ("text","Y → A' nằm trên mặt thứ ba.",18,INK),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Gọi X là điểm kiến chuyển từ mặt thứ nhất sang mặt thứ hai trên cạnh B B phẩy. "
            "Gọi Y là điểm chuyển tiếp theo trên cạnh C C phẩy.",
            1.6,
        )
        self.narrate(
            "Nếu làm trực tiếp trên hình không gian, cả X lẫn Y đều chưa biết. "
            "Ta sẽ mở ba mặt bên ra để hai điểm này tự xuất hiện trên một đường thẳng.",
            1.7,
        )

    def unfold_first(self):
        self.clear_all()
        self.add_hud(5,"Mở mặt bên thứ hai","04 / 12")
        mobs=make_strip_mobs()
        self.add(*mobs)
        card=lesson_card("BƯỚC 1",[
            ("text","Giữ mặt ABB'A' làm mặt đầu tiên.",19,INK),
            ("text","Mở mặt BCC'B' quanh BB'.",19,CYAN),
            ("text","Góc mở: 120°.",19,GOLD),
            ("text","Mặt thứ ba đi theo cùng dải.",19,MUTED),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Ta giữ mặt A B B phẩy A phẩy. Mặt B C C phẩy B phẩy được mở quanh cạnh B B phẩy.",
            1.5,
        )
        self.narrate(
            "Vì đáy là tam giác đều, để hai mặt bên nằm phẳng với nhau ta phải mở một góc một trăm hai mươi độ.",
            1.6,
        )
        _,steps=unfold_chain_numeric(CHAIN)
        step=steps[0]
        downstream=VGroup(*mobs[1:])
        a=W(step["a"]); b=W(step["b"])
        self.play(Rotate(downstream,angle=step["angle"],axis=b-a,about_point=a),run_time=2.2,rate_func=smooth)
        self.narrate(
            "Sau bước này, hai mặt đầu đã nằm trên cùng một mặt phẳng. Mặt thứ ba vẫn nối liền với mặt thứ hai để chuẩn bị mở tiếp.",
            1.6,
        )

    def unfold_second(self):
        self.clear_all()
        self.add_hud(5,"Mở mặt bên thứ ba","05 / 12")
        mobs=make_strip_mobs()
        self.add(*mobs)
        _,steps=unfold_chain_numeric(CHAIN)
        step0=steps[0]
        self.play(Rotate(VGroup(*mobs[1:]),angle=step0["angle"],axis=W(step0["b"])-W(step0["a"]),about_point=W(step0["a"])),run_time=0.35,rate_func=linear)

        card=lesson_card("BƯỚC 2",[
            ("text","Mở mặt CAA'C' quanh CC'.",19,CYAN),
            ("text","Góc mở: 120°.",19,GOLD),
            ("text","Ba mặt bên trở thành một dải chữ nhật.",19,INK),
            ("text","Kích thước bản trải: 3a × h.",19,ORANGE),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Bây giờ ta mở mặt thứ ba quanh cạnh C C phẩy, cũng một góc một trăm hai mươi độ.",
            1.5,
        )
        step1=steps[1]
        self.play(Rotate(mobs[2],angle=step1["angle"],axis=W(step1["b"])-W(step1["a"]),about_point=W(step1["a"])),run_time=2.2,rate_func=smooth)
        self.narrate(
            "Ba hình chữ nhật ghép lại thành một dải duy nhất. Chiều dài của dải là ba a, còn chiều cao là h.",
            1.6,
        )

    def net_and_length(self):
        self.clear_all()
        self.add_hud(5,"Đường gấp trở thành đường chéo","06 / 12")
        net,d,T=net_group()
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("BẢN TRẢI",[
            ("math","Delta x=3a",29,CYAN),
            ("math","Delta y=h",29,CYAN),
            ("math","L=sqrt((3a)^2+h^2)",29,INK),
            ("math","L=sqrt(9a^2+h^2)",34,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Trên bản trải, A và ảnh của A phẩy nằm ở hai góc đối diện của hình chữ nhật có kích thước ba a và h.",
            1.6,
        )
        self.narrate(
            "Vì vậy độ dài đường thẳng bằng căn của chín a bình phương cộng h bình phương.",
            1.5,
        )

    def proof_minimum(self):
        self.clear_all()
        self.add_hud(5,"Vì sao đây là đường ngắn nhất?","07 / 12")
        net,d,T=net_group()
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("LẬP LUẬN",[
            ("text","Mọi đường hợp lệ đều nối cùng hai điểm.",19,INK),
            ("text","Mở mặt không làm thay đổi độ dài.",19,INK),
            ("text","Trong mặt phẳng, đoạn thẳng là ngắn nhất.",19,CYAN),
            ("math","L_(min)=sqrt(9a^2+h^2)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Ta chưa xong chỉ vì đã tính được một độ dài. Cần chứng minh không có đường nào khác trong ba mặt bên ngắn hơn.",
            1.5,
        )
        self.narrate(
            "Sau khi mở ba mặt, mọi đường hợp lệ đều trở thành một đường nối cùng hai điểm trên mặt phẳng. "
            "Đoạn thẳng là ngắn nhất, nên căn của chín a bình phương cộng h bình phương chính là giá trị nhỏ nhất.",
            1.9,
        )

    def locate_crossings(self):
        self.clear_all()
        self.add_hud(5,"Hai điểm đổi mặt nằm ở đâu?","08 / 12")
        net,d,T=net_group()
        self.add_fixed_in_frame_mobjects(net)
        card=lesson_card("ĐỌC TỪ ĐƯỜNG THẲNG",[
            ("math","B X=frac(h,3)",31,GOLD),
            ("math","C Y=frac(2h,3)",31,ORANGE),
            ("text","X và Y đều nằm bên trong cạnh bên.",19,INK),
            ("text","Đường đi thật sự qua đủ ba mặt.",19,GREEN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Đường thẳng cắt cạnh B B phẩy sau một phần ba chiều ngang của dải, nên độ cao của X bằng h trên ba.",
            1.6,
        )
        self.narrate(
            "Nó cắt cạnh C C phẩy sau hai phần ba chiều ngang, nên C Y bằng hai h trên ba. "
            "Cả hai điểm đều nằm trong lòng cạnh, vì thế đường không chạm một đỉnh trung gian.",
            1.8,
        )

    def fold_back(self):
        self.clear_all()
        self.add_hud(5,"Gấp lại lăng trụ","09 / 12")
        path,pts,d=folded_path_group()
        self.add(prism_shell(),highlight_chain(),path)
        label_vertices(self,("A","A1"))
        card=lesson_card("ĐƯỜNG TRÊN KHỐI",[
            ("math","A -> X -> Y -> A'",29,GOLD),
            ("text","AX nằm trên mặt ABB'A'.",18,INK),
            ("text","XY nằm trên mặt BCC'B'.",18,INK),
            ("text","YA' nằm trên mặt CAA'C'.",18,INK),
        ],GREEN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Khi gấp hình trở lại, đoạn thẳng trên bản trải tách thành ba đoạn A X, X Y và Y A phẩy.",
            1.5,
        )
        self.narrate(
            "Ba đoạn ấy lần lượt nằm trên đúng ba mặt bên. Như vậy đường vừa tìm thực sự thỏa điều kiện của bài toán.",
            1.6,
        )

    def ant_walk(self):
        self.clear_all()
        self.add_hud(5,"Cho kiến đi theo đường tối ưu","10 / 12")
        path,pts,d=folded_path_group()
        self.add(prism_shell(),highlight_chain(),path)
        ant=Dot3D(W(pts[0]),radius=0.085,color=GREEN)
        self.add(ant)
        card=lesson_card("HÀNH TRÌNH",[
            ("math","A -> X",25,INK),
            ("math","X -> Y",25,INK),
            ("math","Y -> A'",25,INK),
            ("math","L=sqrt(9a^2+h^2)",31,GOLD),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        phrases=[
            "Kiến rời A và đi trên mặt thứ nhất tới X.",
            "Từ X, kiến sang mặt thứ hai và đi tới Y.",
            "Từ Y, kiến sang mặt thứ ba và đi tới A phẩy.",
        ]
        for i,phrase in enumerate(phrases):
            self.narrate_play(phrase,MoveAlongPath(ant,Line(W(pts[i]),W(pts[i+1]))),min_time=1.8,rate_func=linear)

    def other_direction(self):
        self.clear_all()
        self.add_hud(5,"Nếu đi vòng theo chiều ngược lại?","11 / 12")
        self.add(prism_shell(),highlight_chain())
        label_vertices(self,("A","A1"))
        card=lesson_card("TÍNH ĐỐI XỨNG",[
            ("text","Ba mặt bên có cùng kích thước a × h.",19,INK),
            ("text","Đi theo chiều ngược lại tạo dải giống hệt.",19,INK),
            ("math","L=sqrt(9a^2+h^2)",32,GOLD),
            ("text","Hai hướng quanh lăng trụ cho cùng độ dài.",19,CYAN),
        ],CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Lăng trụ này có ba mặt bên bằng nhau. Nếu kiến đi vòng theo chiều ngược lại qua đủ ba mặt, ta nhận được một dải chữ nhật hoàn toàn giống như trước.",
            1.8,
        )
        self.narrate(
            "Vì vậy hai hướng quanh lăng trụ cho cùng một độ dài. Sang lăng trụ nhiều cạnh hơn, hai hướng có thể tạo ra những quãng đường khác nhau và ta sẽ phải so sánh.",
            1.8,
        )

    def summary(self):
        self.clear_all()
        self.add_hud(5,"Chốt bài lăng trụ tam giác","12 / 12")
        self.add(prism_shell(),highlight_chain())
        label_vertices(self,("A","A1"))
        card=lesson_card("KẾT QUẢ",[
            ("math","B X=frac(h,3)",26,GOLD),
            ("math","C Y=frac(2h,3)",26,ORANGE),
            ("math","L_(min)=sqrt(9a^2+h^2)",31,CYAN),
            ("text","Ba mặt bên → một hình chữ nhật 3a × h.",18,INK),
        ],GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Với lăng trụ đứng tam giác đều, khi kiến phải đi vòng qua đủ ba mặt bên từ A tới A phẩy, bản trải là hình chữ nhật ba a nhân h.",
            1.7,
        )
        self.narrate(
            "Đường ngắn nhất có độ dài căn của chín a bình phương cộng h bình phương. "
            "Điểm đổi mặt nằm ở các độ cao h trên ba và hai h trên ba.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.setup_problem()
        self.compare_free_path()
        self.show_hinges()
        self.unfold_first()
        self.unfold_second()
        self.net_and_length()
        self.proof_minimum()
        self.locate_crossings()
        self.fold_back()
        self.ant_walk()
        self.other_direction()
        self.summary()


class Smoke05(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=67*DEGREES,theta=-48*DEGREES,zoom=0.92)
        mobs=make_strip_mobs()
        self.add(*mobs)
        unfold_animations(self,mobs,run_each=0.45)
        self.wait(0.15)


def render_smoke():
    geometry_preflight(True)
    config.pixel_width=854
    config.pixel_height=480
    config.frame_rate=15
    config.media_dir=str(SMOKE_MEDIA_DIR)
    config.output_file="trai_phang_05_master_smoke"
    config.disable_caching=True
    scene=Smoke05()
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
    config.output_file="trai_phang_05_lang_tru_tam_giac_MASTER_1080p"
    config.disable_caching=False
    scene=TraiPhang05Master()
    scene.render()
    video_path=Path(scene.renderer.file_writer.movie_file_path)
    video_duration=probe_duration(video_path)
    master_wav=ROOT/"master_narration_trai_phang_05.wav"
    build_master_audio(scene.audio_events,video_duration,master_wav)
    final_path=video_path.with_name(video_path.stem+"_WITH_AUDIO.mp4")
    mux_audio(video_path,master_wav,final_path)
    print("VIDEO HOAN CHINH:",final_path)
    return final_path


if __name__ == "__main__":
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

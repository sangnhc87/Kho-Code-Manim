
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

# ---------- geometry engine ----------
FACES = {
    "front": ["A", "B", "B1", "A1"],
    "right": ["B", "C", "C1", "B1"],
    "back": ["D", "D1", "C1", "C"],
    "left": ["A", "A1", "D1", "D"],
    "bottom": ["A", "D", "C", "B"],
    "top": ["A1", "B1", "C1", "D1"],
}
FACE_COLORS = [PURPLE, CYAN, BLUE, ORANGE, GREEN, GOLD]

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

def pairwise_distances(points):
    vals = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            vals.append(np.linalg.norm(np.array(points[i]) - np.array(points[j])))
    return np.array(vals)

def unfold_chain_numeric(chain):
    fc = {f: {v: RAW[v].copy() for v in FACES[f]} for f in chain}
    base = chain[0]
    base_coords = [fc[base][v] for v in FACES[base]]
    n0 = face_normal(base_coords)
    plane_p = base_coords[0].copy()
    steps = []

    for i in range(1, len(chain)):
        prev, cur = chain[i - 1], chain[i]
        edge = shared_edge(prev, cur)
        a = fc[cur][edge[0]].copy()
        b = fc[cur][edge[1]].copy()
        prev_cent = np.mean([fc[prev][v] for v in FACES[prev]], axis=0)

        trials = []
        for sign in (1, -1):
            ang = sign * PI / 2
            test = {v: rotate_point_axis(fc[cur][v], a, b, ang) for v in FACES[cur]}
            dist = max(abs(np.dot(q - plane_p, n0)) for q in test.values())
            hv = b - a
            prev_side = np.dot(np.cross(hv, prev_cent - a), n0)
            cur_cent = np.mean(list(test.values()), axis=0)
            cur_side = np.dot(np.cross(hv, cur_cent - a), n0)
            overlap_penalty = 1 if prev_side * cur_side >= 0 else 0
            trials.append((round(dist, 12), overlap_penalty, sign))

        trials.sort(key=lambda z: (z[0] > 1e-8, z[1], z[0]))
        ang = trials[0][2] * PI / 2

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
    if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
        return float(t), float(u), P + t * v
    return None

def path_data(chain, start_vertex, end_vertex):
    fc, steps, n0, plane_p = unfold_chain_numeric(chain)
    basis = plane_basis(chain, fc, n0)
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
            raise AssertionError(f"Hinge crossing is not strictly inside edge {edge}: t={t}, u={u}")
        raw_a = RAW[edge[0]]
        raw_b = RAW[edge[1]]
        raw_x = raw_a + u * (raw_b - raw_a)
        hits.append({"edge": edge, "t": t, "u": u, "p2": X2, "raw": raw_x})

    if any(hits[i]["t"] >= hits[i + 1]["t"] - 1e-9 for i in range(len(hits) - 1)):
        raise AssertionError("Hinge crossings are not in the required order.")

    return {
        "fc": fc, "steps": steps, "basis": basis,
        "P2": P, "Q2": Q,
        "Praw": RAW[start_vertex].copy(),
        "Qraw": RAW[end_vertex].copy(),
        "hits": hits,
        "length": float(np.linalg.norm(Q - P)),
    }

def rigid_preflight_chain(chain):
    fc0 = {f: {v: RAW[v].copy() for v in FACES[f]} for f in chain}
    fc, steps, n0, plane_p = unfold_chain_numeric(chain)
    for f in chain:
        before = [fc0[f][v] for v in FACES[f]]
        after = [fc[f][v] for v in FACES[f]]
        if not np.allclose(
            pairwise_distances(before), pairwise_distances(after),
            atol=1e-9, rtol=0
        ):
            raise AssertionError(f"Face {f} was distorted.")
        if max(abs(np.dot(q - plane_p, n0)) for q in after) > 1e-8:
            raise AssertionError(f"Face {f} did not land on base plane.")
    return True

# ---------- drawing ----------
WORLD_SHIFT = np.array([-3.23, -0.12, 0.0])

def W(p):
    return WORLD_SCALE * np.array(p, dtype=float) + WORLD_SHIFT

def solid(a, b, color=EDGE, width=4.0, opacity=0.96):
    return Line(
        np.array(a, dtype=float), np.array(b, dtype=float),
        color=color, stroke_width=width, stroke_opacity=opacity,
    )

def hidden_edge(a, b, color=DIM, width=2.6, opacity=0.68):
    return DashedLine(
        np.array(a, dtype=float), np.array(b, dtype=float),
        color=color, stroke_width=width, stroke_opacity=opacity,
        dash_length=0.11, dashed_ratio=0.56,
    )

def face_poly(points, color=BLUE, opacity=0.12):
    return Polygon(
        *[np.array(p, dtype=float) for p in points],
        fill_color=color, fill_opacity=opacity, stroke_width=0,
    )

def box_shell():
    p = {k: W(v) for k, v in RAW.items()}
    faces = VGroup(
        face_poly([p[x] for x in FACES["front"]], PURPLE, 0.055),
        face_poly([p[x] for x in FACES["right"]], CYAN, 0.085),
        face_poly([p[x] for x in FACES["top"]], BLUE, 0.060),
    )
    visible = [
        ("A","B"),("B","C"),("A","A1"),("B","B1"),("C","C1"),
        ("A1","B1"),("B1","C1"),("C1","D1"),("D1","A1")
    ]
    hidden = [("C","D"),("D","A"),("D","D1")]
    edges = VGroup(*[solid(p[a], p[b], EDGE, 3.8) for a,b in visible])
    hid = VGroup(*[hidden_edge(p[a], p[b]) for a,b in hidden])
    return VGroup(faces, edges, hid)

def highlight_chain(chain):
    g = VGroup()
    for i, f in enumerate(chain):
        pts = [W(RAW[v]) for v in FACES[f]]
        g.add(face_poly(pts, FACE_COLORS[i % len(FACE_COLORS)], 0.13))
    return g

def strip_face_mob(face_name, color, start_vertex=None, end_vertex=None):
    pts = [W(RAW[v]) for v in FACES[face_name]]
    poly = face_poly(pts, color, 0.16)
    border = VGroup(*[
        solid(pts[i], pts[(i + 1) % 4], color, 3.3)
        for i in range(4)
    ])
    g = VGroup(poly, border)
    if start_vertex is not None:
        g.add(Dot3D(W(RAW[start_vertex]), radius=0.075, color=GREEN))
    if end_vertex is not None:
        g.add(Dot3D(W(RAW[end_vertex]), radius=0.075, color=RED))
    return g

def make_strip_mobs(chain, start_vertex, end_vertex):
    mobs = []
    for i, f in enumerate(chain):
        s = start_vertex if i == 0 else None
        e = end_vertex if i == len(chain) - 1 else None
        mobs.append(strip_face_mob(f, FACE_COLORS[i % len(FACE_COLORS)], s, e))
    return mobs

def unfold_animations(scene, chain, face_mobs, run_each=1.5):
    _, steps, _, _ = unfold_chain_numeric(chain)
    for step in steps:
        i = step["index"]
        downstream = VGroup(*face_mobs[i:])
        a = W(step["a"])
        b = W(step["b"])
        scene.play(
            Rotate(downstream, angle=step["angle"], axis=b - a, about_point=a),
            run_time=run_each, rate_func=smooth,
        )

def folded_path_group(chain, start_vertex, end_vertex, width=6.5):
    d = path_data(chain, start_vertex, end_vertex)
    pts = [d["Praw"]] + [h["raw"] for h in d["hits"]] + [d["Qraw"]]
    lines = VGroup(*[
        solid(W(pts[i]), W(pts[i + 1]), GOLD, width)
        for i in range(len(pts) - 1)
    ])
    dots = VGroup(*[
        Dot3D(W(p), radius=0.058, color=GOLD) for p in pts[1:-1]
    ])
    return VGroup(lines, dots), pts, d

def net_group(chain, start_vertex, end_vertex, width=6.1, height=5.0):
    d = path_data(chain, start_vertex, end_vertex)
    fc, basis = d["fc"], d["basis"]
    face2 = {}
    all2 = []
    for f in chain:
        arr = [proj2(fc[f][v], basis) for v in FACES[f]]
        face2[f] = arr
        all2 += arr

    all2 = np.array(all2)
    minx, miny = all2.min(axis=0)
    maxx, maxy = all2.max(axis=0)
    scale = min(width / max(maxx-minx, 1e-9), height / max(maxy-miny, 1e-9))
    mid = np.array([(minx+maxx)/2, (miny+maxy)/2])

    def T(p):
        q = (np.array(p) - mid) * scale
        return np.array([q[0] + LEFT_CENTER[0], q[1] + LEFT_CENTER[1], 0.0])

    g = VGroup()
    for i, f in enumerate(chain):
        pts = [T(q) for q in face2[f]]
        g.add(Polygon(
            *pts,
            fill_color=FACE_COLORS[i % len(FACE_COLORS)],
            fill_opacity=0.15,
            stroke_color=FACE_COLORS[i % len(FACE_COLORS)],
            stroke_width=2.8,
        ))

    P = T(d["P2"])
    Q = T(d["Q2"])
    g.add(Dot(P, radius=0.075, color=GREEN))
    g.add(Dot(Q, radius=0.075, color=RED))
    g.add(Line(P, Q, color=GOLD, stroke_width=6.5))
    for h in d["hits"]:
        g.add(Dot(T(h["p2"]), radius=0.055, color=GOLD))
    return g, d, T

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
# VIDEO 02 MASTER — LẬP PHƯƠNG, DẢI 4 MẶT
# ==========================================================
SIDE = 3.0
H = SIDE / 2.0
RAW = {
    "A": np.array([-H,-H,-H]), "B": np.array([ H,-H,-H]),
    "C": np.array([ H, H,-H]), "D": np.array([-H, H,-H]),
    "A1": np.array([-H,-H, H]), "B1": np.array([ H,-H, H]),
    "C1": np.array([ H, H, H]), "D1": np.array([-H, H, H]),
}
WORLD_SCALE = 0.78

CHAIN = ["front", "right", "bottom", "back"]
START = "A1"
END = "D1"

def geometry_preflight(verbose=True):
    rigid_preflight_chain(CHAIN)
    d = path_data(CHAIN, START, END)
    expected = SIDE * math.sqrt(13)
    if abs(d["length"] - expected) > 1e-8:
        raise AssertionError((d["length"], expected))
    expected_t = [1/3, 1/2, 2/3]
    expected_u = [1/3, 1/2, 2/3]
    for h, t0, u0 in zip(d["hits"], expected_t, expected_u):
        if abs(h["t"] - t0) > 1e-8 or abs(h["u"] - u0) > 1e-8:
            raise AssertionError(("unexpected hinge point", h))
    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  A' -> D' through front -> right -> bottom -> back")
        print("  three hinge crossings are strictly interior")
        print("  t = 1/3, 1/2, 2/3")
        print("  L = a*sqrt(13)")
    return True

def layout_samples():
    return [
        lesson_card("BÀI TOÁN", [
            ("text","Kiến đi từ A' đến D'.",20,INK),
            ("text","Phải đi qua đúng bốn mặt đã tô.",20,INK),
            ("text","Mặt trước → mặt phải → mặt đáy → mặt sau.",18,CYAN),
            ("text","Tìm đường ngắn nhất trong dải này.",19,MUTED),
        ], GOLD),
        lesson_card("BẢN TRẢI", [
            ("math","Delta x = 3a",28,CYAN),
            ("math","Delta y = 2a",28,CYAN),
            ("math","L = sqrt((3a)^2+(2a)^2)",28,INK),
            ("math","L = a sqrt(13)",34,GOLD),
        ], CYAN),
    ]

class TraiPhang02Master(BaseLesson):
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES, theta=-48*DEGREES, zoom=0.92)
        self.add(box_shell(), highlight_chain(CHAIN))
        card = intro_card(
            2,
            ["LẬP PHƯƠNG", "ĐƯỜNG ĐI QUA 4 MẶT"],
            "Bắt đầu ở một đỉnh, kết thúc ở một đỉnh.",
        )
        self.add_fixed_in_frame_mobjects(card, divider(), footer())
        self.play(FadeIn(card), run_time=0.7)
        self.narrate(
            "Hôm nay con kiến vẫn bắt đầu ở một đỉnh và kết thúc ở một đỉnh. "
            "Nhưng lần này nó phải đi trong một dải gồm bốn mặt của lập phương. "
            "Điểm đầu là A phẩy, điểm cuối là D phẩy.",
            1.7,
        )
        self.narrate(
            "Bốn mặt được đi qua theo thứ tự: mặt trước, mặt phải, mặt đáy rồi mặt sau. "
            "Đây là một bài toán có ràng buộc đường đi. Ta chỉ tìm đường ngắn nhất trong đúng dải bốn mặt ấy.",
            1.7,
        )

    def setup_problem(self):
        self.clear_all()
        self.add_hud(2, "Từ A' đến D' qua đúng bốn mặt", "01 / 10")
        self.add(box_shell(), highlight_chain(CHAIN))
        p = {k: W(v) for k,v in RAW.items()}
        self.add(Dot3D(p["A1"], radius=0.08, color=GREEN),
                 Dot3D(p["D1"], radius=0.08, color=RED))
        card = lesson_card("BÀI TOÁN", [
            ("text","Điểm đầu: A'.",20,GREEN),
            ("text","Điểm cuối: D'.",20,RED),
            ("text","Dải mặt: trước → phải → đáy → sau.",19,CYAN),
            ("text","Đường đi phải nằm hoàn toàn trong dải.",19,INK),
            ("math","L_(min) = ?",34,GOLD),
        ], GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Các em nhìn bốn mặt đang được tô màu. "
            "Đường đi phải bắt đầu trên mặt trước, lần lượt sang mặt phải, xuống mặt đáy, rồi sang mặt sau để tới D phẩy.",
            1.6,
        )
        self.narrate(
            "Như vậy con kiến sẽ đổi mặt ba lần. "
            "Ba cạnh chung mà nó phải đi qua là B B phẩy, B C và C D.",
            1.5,
        )

    def show_hinges(self):
        self.clear_all()
        self.add_hud(2, "Ba cạnh chung cần đi qua", "02 / 10")
        self.add(box_shell(), highlight_chain(CHAIN))
        p = {k: W(v) for k,v in RAW.items()}
        hinges = VGroup(
            solid(p["B"], p["B1"], GOLD, 7.0),
            solid(p["B"], p["C"], ORANGE, 7.0),
            solid(p["C"], p["D"], GREEN, 7.0),
        )
        self.play(Create(hinges), run_time=0.8)
        card = lesson_card("BA LẦN ĐỔI MẶT", [
            ("math","X in B B'",27,GOLD),
            ("math","Y in B C",27,ORANGE),
            ("math","Z in C D",27,GREEN),
            ("text","Ta chưa biết X, Y, Z nằm ở đâu.",19,INK),
            ("text","Bản trải sẽ xác định cả ba điểm.",19,MUTED),
        ], CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Gọi X là điểm kiến đi qua cạnh B B phẩy, Y thuộc B C và Z thuộc C D. "
            "Nếu giải trực tiếp trên khối, ba điểm này đều chưa biết nên bài toán khá rối.",
            1.6,
        )
        self.narrate(
            "Ta sẽ không tìm từng điểm một trên hình không gian. "
            "Thay vào đó, mở cả dải bốn mặt ra. Khi bốn mặt nằm phẳng, ba điểm X, Y, Z sẽ xuất hiện tự nhiên trên một đoạn thẳng.",
            1.7,
        )

    def unfold_strip(self):
        self.clear_all()
        self.add_hud(2, "Mở dải bốn mặt", "03 / 10")
        mobs = make_strip_mobs(CHAIN, START, END)
        self.add(*mobs)
        card = lesson_card("MỞ LẦN LƯỢT", [
            ("text","Giữ mặt trước làm mặt đầu tiên.",19,INK),
            ("text","Mở mặt phải quanh BB'.",19,CYAN),
            ("text","Tiếp tục mở mặt đáy quanh BC.",19,CYAN),
            ("text","Cuối cùng mở mặt sau quanh CD.",19,CYAN),
        ], CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Ta giữ mặt trước ở vị trí ban đầu. Trước hết mở mặt phải quanh B B phẩy. "
            "Sau đó mở tiếp mặt đáy quanh B C, và cuối cùng mở mặt sau quanh C D.",
            1.8,
        )
        unfold_animations(self, CHAIN, mobs, run_each=1.35)
        self.narrate(
            "Sau ba lần mở, cả bốn mặt đã nằm trên cùng một mặt phẳng. "
            "Đường đi ngắn nhất trong dải bây giờ chỉ còn là đường ngắn nhất giữa hai điểm A phẩy và ảnh của D phẩy.",
            1.7,
        )

    def net_and_length(self):
        self.clear_all()
        self.add_hud(2, "Đường gấp trở thành một đoạn thẳng", "04 / 10")
        net, d, T = net_group(CHAIN, START, END)
        self.add_fixed_in_frame_mobjects(net)
        card = lesson_card("BẢN TRẢI", [
            ("math","Delta x = 3a",29,CYAN),
            ("math","Delta y = 2a",29,CYAN),
            ("math","L = sqrt((3a)^2+(2a)^2)",27,INK),
            ("math","L = a sqrt(13)",36,GOLD),
        ], GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Trên bản trải, từ A phẩy đến ảnh của D phẩy ta dịch theo một phương ba cạnh a, "
            "và theo phương vuông góc hai cạnh a.",
            1.5,
        )
        self.narrate(
            "Vì thế độ dài đường thẳng là căn của chín a bình phương cộng bốn a bình phương. "
            "Kết quả là a căn mười ba.",
            1.5,
        )

    def locate_crossings(self):
        self.clear_all()
        self.add_hud(2, "Ba điểm đổi mặt nằm ở đâu?", "05 / 10")
        net, d, T = net_group(CHAIN, START, END)
        self.add_fixed_in_frame_mobjects(net)
        card = lesson_card("VỊ TRÍ BA ĐIỂM", [
            ("math","B X = frac(a,3)",28,GOLD),
            ("math","B Y = frac(a,2)",28,ORANGE),
            ("math","D Z = frac(2a,3)",28,GREEN),
            ("text","Ba điểm cùng nằm trên một đường thẳng.",19,INK),
        ], CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Đoạn thẳng này cắt ba cạnh chung tại X, Y và Z. "
            "Vì toàn bộ độ dịch ngang là ba a, các vị trí tương ứng xuất hiện ở một phần ba, một phần hai và hai phần ba của hành trình.",
            1.7,
        )
        self.narrate(
            "Từ đó ta đọc được B X bằng a trên ba; Y là trung điểm của B C; "
            "còn D Z bằng hai a trên ba. Đây chính là ba điểm mà con kiến phải đổi mặt khi gấp hình trở lại.",
            1.7,
        )

    def proof_minimum(self):
        self.clear_all()
        self.add_hud(2, "Vì sao đây là đường ngắn nhất?", "06 / 10")
        net, d, T = net_group(CHAIN, START, END)
        self.add_fixed_in_frame_mobjects(net)
        card = lesson_card("LẬP LUẬN", [
            ("text","Mọi đường hợp lệ trong dải đều nối cùng hai điểm.",19,INK),
            ("text","Sau khi mở, độ dài từng đoạn không thay đổi.",19,INK),
            ("text","Trong mặt phẳng, đoạn thẳng là ngắn nhất.",19,CYAN),
            ("math","L_(min) = a sqrt(13)",34,GOLD),
        ], GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Điểm quan trọng không phải chỉ là tính được a căn mười ba. "
            "Ta còn phải biết vì sao không có một đường ngoằn ngoèo khác trong bốn mặt ngắn hơn.",
            1.5,
        )
        self.narrate(
            "Khi bốn mặt được mở ra, mọi đường hợp lệ trong dải đều trở thành một đường nối cùng hai điểm trên mặt phẳng. "
            "Trong tất cả những đường đó, đoạn thẳng là ngắn nhất. Vì vậy a căn mười ba là giá trị nhỏ nhất thật sự trong dải đã cho.",
            1.9,
        )

    def fold_back(self):
        self.clear_all()
        self.add_hud(2, "Gấp trở lại khối lập phương", "07 / 10")
        path, pts, d = folded_path_group(CHAIN, START, END)
        self.add(box_shell(), highlight_chain(CHAIN), path)
        card = lesson_card("ĐƯỜNG TRÊN KHỐI", [
            ("math","A' -> X -> Y -> Z -> D'",26,GOLD),
            ("text","A'X nằm trên mặt trước.",18,INK),
            ("text","XY nằm trên mặt phải.",18,INK),
            ("text","YZ nằm trên mặt đáy.",18,INK),
            ("text","ZD' nằm trên mặt sau.",18,INK),
        ], GREEN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Bây giờ gấp bản trải trở lại trong suy nghĩ. "
            "Đoạn thẳng vừa tìm tách thành bốn đoạn A phẩy X, X Y, Y Z và Z D phẩy.",
            1.5,
        )
        self.narrate(
            "Mỗi đoạn nằm trên đúng một mặt của dải. "
            "Không đoạn nào xuyên qua lòng khối, và ba điểm đổi mặt đều nằm bên trong các cạnh chung.",
            1.6,
        )

    def ant_walk(self):
        self.clear_all()
        self.add_hud(2, "Cho kiến đi theo đường vừa tìm", "08 / 10")
        path, pts, d = folded_path_group(CHAIN, START, END)
        self.add(box_shell(), highlight_chain(CHAIN), path)
        ant = Dot3D(W(pts[0]), radius=0.085, color=GREEN)
        self.add(ant)
        card = lesson_card("HÀNH TRÌNH", [
            ("math","A' -> X",25,INK),
            ("math","X -> Y",25,INK),
            ("math","Y -> Z",25,INK),
            ("math","Z -> D'",25,INK),
            ("math","L = a sqrt(13)",34,GOLD),
        ], GOLD)
        self.add_fixed_in_frame_mobjects(card)
        phrases = [
            "Đầu tiên, kiến đi trên mặt trước từ A phẩy tới X.",
            "Tiếp theo, nó sang mặt phải và đi từ X tới Y.",
            "Sau đó, nó đi trên mặt đáy từ Y tới Z.",
            "Cuối cùng, kiến sang mặt sau và tới D phẩy.",
        ]
        for i, phrase in enumerate(phrases):
            self.narrate_play(
                phrase,
                MoveAlongPath(ant, Line(W(pts[i]), W(pts[i+1]))),
                min_time=1.8, rate_func=linear,
            )

    def reflection_note(self):
        self.clear_all()
        self.add_hud(2, "Một dấu hiệu để tự kiểm tra", "09 / 10")
        net, d, T = net_group(CHAIN, START, END)
        self.add_fixed_in_frame_mobjects(net)
        card = lesson_card("KHI ĐÃ TRẢI PHẲNG", [
            ("text","Bốn đoạn phải nối thành một đường thẳng.",19,INK),
            ("text","Nếu còn gấp khúc tại một cạnh chung,",19,INK),
            ("text","ta vẫn còn rút ngắn được đường đi.",19,CYAN),
            ("math","A', X, Y, Z, D'_f",27,GOLD),
            ("text","cùng nằm trên một đường thẳng.",19,GREEN),
        ], CYAN)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Có một cách rất nhanh để tự kiểm tra kết quả. "
            "Sau khi trải đúng bốn mặt, bốn đoạn của đường kiến phải ghép thành một đường thẳng duy nhất.",
            1.5,
        )
        self.narrate(
            "Nếu tại một cạnh chung đường vẫn còn gãy, ta có thể nối thẳng hai đầu để làm nó ngắn hơn. "
            "Vì vậy tính thẳng hàng trên bản trải là dấu hiệu đặc trưng của đường ngắn nhất.",
            1.6,
        )

    def summary(self):
        self.clear_all()
        self.add_hud(2, "Chốt bài 4 mặt", "10 / 10")
        self.add(box_shell(), highlight_chain(CHAIN))
        card = lesson_card("KẾT QUẢ", [
            ("math","A' -> X -> Y -> Z -> D'",25,INK),
            ("math","B X = frac(a,3)",25,GOLD),
            ("math","B Y = frac(a,2)",25,ORANGE),
            ("math","D Z = frac(2a,3)",25,GREEN),
            ("math","L_(min)=a sqrt(13)",34,CYAN),
        ], GOLD)
        self.add_fixed_in_frame_mobjects(card)
        self.narrate(
            "Bài bốn mặt có ba lần đổi mặt, nhưng sau khi trải đúng dải thì toàn bộ bài toán chỉ còn là một đoạn thẳng. "
            "Độ dài ngắn nhất là a căn mười ba.",
            1.5,
        )
        self.narrate(
            "Điều đáng nhớ hơn công thức là cách làm: xác định đúng dải mặt, mở lần lượt theo các cạnh chung, "
            "nối hai điểm bằng đoạn thẳng, rồi gấp lại để đọc vị trí các điểm đổi mặt.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.setup_problem()
        self.show_hinges()
        self.unfold_strip()
        self.net_and_length()
        self.locate_crossings()
        self.proof_minimum()
        self.fold_back()
        self.ant_walk()
        self.reflection_note()
        self.summary()

class Smoke02(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        self.set_camera_orientation(phi=67*DEGREES, theta=-48*DEGREES, zoom=1.0)
        mobs = make_strip_mobs(CHAIN, START, END)
        self.add(*mobs)
        unfold_animations(self, CHAIN, mobs, run_each=0.45)
        self.wait(0.15)

def render_smoke():
    geometry_preflight(True)
    config.pixel_width = 854
    config.pixel_height = 480
    config.frame_rate = 15
    config.media_dir = str(SMOKE_MEDIA_DIR)
    config.output_file = "trai_phang_02_master_smoke"
    config.disable_caching = True
    scene = Smoke02()
    scene.render()
    path = Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():
        raise RuntimeError(path)
    return path

def render_full():
    geometry_preflight(True)
    layout_preflight(layout_samples(), True)
    config.pixel_width = FINAL_WIDTH
    config.pixel_height = FINAL_HEIGHT
    config.frame_rate = FINAL_FPS
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "trai_phang_02_lap_phuong_bon_mat_MASTER_1080p"
    config.disable_caching = False
    scene = TraiPhang02Master()
    scene.render()
    video_path = Path(scene.renderer.file_writer.movie_file_path)
    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_trai_phang_02.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)
    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    print("VIDEO HOAN CHINH:", final_path)
    return final_path

if __name__ == "__main__":
    source_path = Path(sys.argv[0]).resolve()
    if "--narration-lint" in sys.argv:
        narration_lint(source_path, True)
        raise SystemExit(0)
    if "--geometry-preflight" in sys.argv:
        geometry_preflight(True)
        raise SystemExit(0)
    if "--layout-preflight" in sys.argv:
        layout_preflight(layout_samples(), True)
        raise SystemExit(0)
    if "--smoke-render" in sys.argv:
        render_smoke()
        raise SystemExit(0)
    render_full()

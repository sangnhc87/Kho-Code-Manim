from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time
import numpy as np

# ==========================================================
# SERIES TRAI PHANG 01
# KIEN TREN LAP PHUONG - DUONG DI NGAN NHAT TREN BE MAT
# Manim Community + MathTypst SAFE | Standalone 100%
#
# Muc tieu:
# - Mot mo hinh duy nhat: lap phuong.
# - Trai mat bang phep quay cung quanh DUNG canh ban le.
# - Bao toan do dai / goc / diem tren mat.
# - Geometry preflight truoc khi render.
# - 480p smoke render truoc 1080p final.
# - TTS master-track, mux mot lan.
# ==========================================================

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

# ==========================================================
# PALETTE
# ==========================================================
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

# ==========================================================
# TYPOGRAPHY + TYPST SAFETY
# ==========================================================
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
        raise ValueError(
            f"Forbidden Typst token(s) {bad} in {s!r}. "
            "Use inter for intersection and hat(...) for plane angles."
        )
    if "/" in s:
        raise ValueError(
            f"Slash fraction forbidden in MathTypst: {s!r}. "
            "Use frac(..., ...)."
        )
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


# ==========================================================
# AUDIO + MASTER TRACK
# ==========================================================
def _audio_key(text):
    payload = json.dumps(
        {
            "text": text,
            "voice": GIONG_DOC,
            "rate": TOC_DO_DOC,
            "pitch": PITCH,
            "engine": "edge-tts",
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
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
        ";".join(filters)
        + ";"
        + "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", *inputs,
            "-filter_complex", fc,
            "-map", "[m]",
            "-ar", "48000",
            "-ac", "2",
            "-t", f"{video_duration:.3f}",
            str(out_wav),
        ],
        check=True,
    )


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(video),
            "-i", str(audio),
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(out),
        ],
        check=True,
    )


# ==========================================================
# RIGID GEOMETRY ENGINE
# ==========================================================
SIDE_RAW = 3.0
HALF = SIDE_RAW / 2.0

# Cube coordinates, before visual scale/shift.
A0  = np.array([-HALF, -HALF, 0.0])
B0  = np.array([ HALF, -HALF, 0.0])
C0  = np.array([ HALF,  HALF, 0.0])
D0  = np.array([-HALF,  HALF, 0.0])
A10 = np.array([-HALF, -HALF, SIDE_RAW])
B10 = np.array([ HALF, -HALF, SIDE_RAW])
C10 = np.array([ HALF,  HALF, SIDE_RAW])
D10 = np.array([-HALF,  HALF, SIDE_RAW])

# Visual map. Uniform scale + translation preserves the geometry.
GEO_SCALE = 0.78
GEO_SHIFT = np.array([-2.15, -0.10, -0.15])


def V(p):
    return GEO_SCALE * np.array(p, dtype=float) + GEO_SHIFT


def rotate_point_axis(p, axis_a, axis_b, angle):
    """Rodrigues rotation around the oriented line axis_a -> axis_b."""
    p = np.array(p, dtype=float)
    a = np.array(axis_a, dtype=float)
    b = np.array(axis_b, dtype=float)
    k = b - a
    nk = np.linalg.norm(k)
    if nk < 1e-12:
        raise ValueError("Rotation axis has zero length.")
    k = k / nk
    x = p - a
    xr = (
        x * math.cos(angle)
        + np.cross(k, x) * math.sin(angle)
        + k * np.dot(k, x) * (1.0 - math.cos(angle))
    )
    return a + xr


def rotate_points_axis(points, axis_a, axis_b, angle):
    return [rotate_point_axis(p, axis_a, axis_b, angle) for p in points]


def pairwise_distances(points):
    out = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            out.append(np.linalg.norm(np.array(points[i]) - np.array(points[j])))
    return np.array(out)


def point_to_line_parameter(p, a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    p = np.array(p, dtype=float)
    d = b - a
    return float(np.dot(p - a, d) / np.dot(d, d))


def geometry_preflight(verbose=True):
    """Hard checks for the exact unfolding used in Video 01."""
    tol = 1e-9
    right0 = [B0, C0, C10, B10]
    right_flat = rotate_points_axis(right0, B0, C0, PI / 2)

    # 1. Rigid motion preserves all pairwise distances.
    if not np.allclose(
        pairwise_distances(right0),
        pairwise_distances(right_flat),
        atol=tol,
        rtol=0,
    ):
        raise AssertionError("Rigid unfold does not preserve pairwise distances.")

    # 2. Hinge endpoints must stay fixed.
    if np.linalg.norm(right_flat[0] - B0) > tol:
        raise AssertionError("B moved although B lies on the hinge.")
    if np.linalg.norm(right_flat[1] - C0) > tol:
        raise AssertionError("C moved although C lies on the hinge.")

    # 3. The unfolded moving face must be coplanar with the bottom face z=0.
    z_values = [p[2] for p in right_flat]
    if max(abs(z) for z in z_values) > tol:
        raise AssertionError("Moving face is not coplanar after unfolding.")

    # 4. Check exact image of C'.
    C1_flat = right_flat[2]
    expected_C1 = np.array([3.0 * HALF, HALF, 0.0])
    if np.linalg.norm(C1_flat - expected_C1) > tol:
        raise AssertionError(
            f"Unexpected image of C': {C1_flat}; expected {expected_C1}."
        )

    # 5. The straight segment A-C1 crosses the hinge BC exactly at its midpoint M.
    M = (B0 + C0) / 2.0
    lam = point_to_line_parameter(M, A0, C1_flat)
    reconstructed = A0 + lam * (C1_flat - A0)
    if not (0.0 < lam < 1.0):
        raise AssertionError("Hinge crossing lies outside unfolded straight segment.")
    if np.linalg.norm(reconstructed - M) > tol:
        raise AssertionError("Unfolded shortest segment does not pass through hinge midpoint.")

    # 6. Length in the net equals the folded two-segment path.
    unfolded_len = np.linalg.norm(C1_flat - A0)
    folded_len = np.linalg.norm(M - A0) + np.linalg.norm(C10 - M)
    expected = SIDE_RAW * math.sqrt(5.0)
    if abs(unfolded_len - folded_len) > tol:
        raise AssertionError("Folded and unfolded path lengths disagree.")
    if abs(unfolded_len - expected) > tol:
        raise AssertionError("Shortest length is not a*sqrt(5) in raw units.")

    # 7. The path pieces are on the intended faces.
    if abs(A0[2]) > tol or abs(M[2]) > tol:
        raise AssertionError("A-M is not on bottom face z=0.")
    if abs(M[0] - HALF) > tol or abs(C10[0] - HALF) > tol:
        raise AssertionError("M-C' is not on right face x=a/2.")

    # 8. Sample the one-parameter broken path and verify minimum at t=1/2.
    ts = np.linspace(0.0, 1.0, 2001)
    vals = (
        SIDE_RAW * np.sqrt(1.0 + ts * ts)
        + SIDE_RAW * np.sqrt(1.0 + (1.0 - ts) ** 2)
    )
    idx = int(np.argmin(vals))
    if abs(ts[idx] - 0.5) > 1e-3:
        raise AssertionError("Numerical hinge-point minimum is not at t=1/2.")
    if abs(vals[idx] - expected) > 1e-6:
        raise AssertionError("Numerical minimum does not equal a*sqrt(5).")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print(f"  rigid face pairwise distances: preserved")
        print(f"  hinge endpoints B,C: fixed")
        print(f"  unfolded face: coplanar with bottom face")
        print(f"  hinge crossing M: midpoint of BC")
        print(f"  straight length: {unfolded_len:.12f} = a*sqrt(5)")
        print(f"  folded path length: {folded_len:.12f}")
        print(f"  sampled minimum: t={ts[idx]:.4f}")
    return True


# ==========================================================
# 3D DRAWING HELPERS
# ==========================================================
def solid(a, b, color=EDGE, width=4.0, opacity=0.96):
    return Line(
        np.array(a, dtype=float),
        np.array(b, dtype=float),
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
    )


def hidden_edge(a, b, color=DIM, width=2.7, opacity=0.72, dash=0.11):
    return DashedLine(
        np.array(a, dtype=float),
        np.array(b, dtype=float),
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def aux(a, b, color=CYAN, width=3.5, opacity=0.92, dash=0.11):
    return DashedLine(
        np.array(a, dtype=float),
        np.array(b, dtype=float),
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def face(*points, color=BLUE, opacity=0.10):
    return Polygon(
        *[np.array(p, dtype=float) for p in points],
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=0,
    )


def corner_mark_2d(vertex, u, v, size=0.23, color=GOLD, width=4.2):
    u = np.array(u, dtype=float)
    v = np.array(v, dtype=float)
    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)
    p1 = vertex + size * u
    p2 = vertex + size * (u + v)
    p3 = vertex + size * v
    return VGroup(
        solid(p1, p2, color, width),
        solid(p2, p3, color, width),
    )


def cube_points_visual():
    raw = {
        "A": A0, "B": B0, "C": C0, "D": D0,
        "A1": A10, "B1": B10, "C1": C10, "D1": D10,
    }
    return {k: V(p) for k, p in raw.items()}


def cube_model():
    p = cube_points_visual()

    # Three visible faces from the chosen front-right-above camera.
    faces = VGroup(
        face(p["A"], p["B"], p["B1"], p["A1"], color=PURPLE, opacity=0.055),
        face(p["B"], p["C"], p["C1"], p["B1"], color=CYAN, opacity=0.095),
        face(p["A1"], p["B1"], p["C1"], p["D1"], color=BLUE, opacity=0.075),
    )

    # Visible vs hidden edges for the fixed teaching camera.
    visible_pairs = [
        ("A", "B"), ("B", "C"),
        ("A", "A1"), ("B", "B1"), ("C", "C1"),
        ("A1", "B1"), ("B1", "C1"), ("C1", "D1"), ("D1", "A1"),
    ]
    hidden_pairs = [
        ("C", "D"), ("D", "A"), ("D", "D1"),
    ]

    edges = VGroup(*[
        solid(p[u], p[v], EDGE, 4.0, 0.96) for u, v in visible_pairs
    ])
    hidden = VGroup(*[
        hidden_edge(p[u], p[v], DIM, 2.7, 0.70) for u, v in hidden_pairs
    ])

    dots = VGroup(*[
        Dot3D(p[k], radius=0.055, color=GOLD if k not in {"A", "C1"} else (GREEN if k == "A" else RED))
        for k in p
    ])
    return {"p": p, "faces": faces, "edges": edges, "hidden": hidden, "dots": dots}


def right_face_visual(theta):
    pts_raw = rotate_points_axis([B0, C0, C10, B10], B0, C0, theta)
    B, C, C1, B1 = [V(p) for p in pts_raw]
    poly = face(B, C, C1, B1, color=CYAN, opacity=0.16)
    edges = VGroup(
        solid(B, C, GOLD, 6.0, 1.0),
        solid(C, C1, CYAN, 4.4, 0.96),
        solid(C1, B1, CYAN, 4.4, 0.96),
        solid(B1, B, CYAN, 4.4, 0.96),
    )
    c_dot = Dot3D(C1, radius=0.07, color=RED)
    return VGroup(poly, edges, c_dot)


def bottom_face_visual():
    A, B, C, D = [V(p) for p in [A0, B0, C0, D0]]
    return VGroup(
        face(A, B, C, D, color=BLUE, opacity=0.13),
        solid(A, B, BLUE, 4.2),
        solid(B, C, GOLD, 6.0),
        solid(C, D, BLUE, 4.2),
        solid(D, A, BLUE, 4.2),
        Dot3D(A, radius=0.07, color=GREEN),
    )


def net_points_visual():
    c1_flat_raw = rotate_point_axis(C10, B0, C0, PI / 2)
    b1_flat_raw = rotate_point_axis(B10, B0, C0, PI / 2)
    return {
        "A": V(A0), "B": V(B0), "C": V(C0), "D": V(D0),
        "C1f": V(c1_flat_raw), "B1f": V(b1_flat_raw),
        "M": V((B0 + C0) / 2.0),
    }


# ==========================================================
# LAYOUT
# ==========================================================
def header_group(chapter, title, subtitle=None, progress=""):
    left = txt(chapter, 17, GOLD, BOLD)
    main = fit_width(txt(title, 31, INK, BOLD), 10.0)
    left.to_corner(UL, buff=0.28)
    main.next_to(left, DOWN, aligned_edge=LEFT, buff=0.08)

    items = [left, main]
    if subtitle:
        sub = fit_width(txt(subtitle, 18, MUTED), 10.5)
        sub.next_to(main, DOWN, aligned_edge=LEFT, buff=0.07)
        items.append(sub)

    if progress:
        pg = txt(progress, 17, MUTED, BOLD).to_corner(UR, buff=0.30)
        items.append(pg)

    rule = Line(LEFT * 6.65, RIGHT * 6.65, color=GRID, stroke_width=1.1)
    rule.to_edge(UP, buff=1.12 if subtitle else 0.96)
    items.append(rule)
    return VGroup(*items)


def footer_group():
    brand = txt(TEN_THAY, 16, MUTED)
    series = txt("TRẢI PHẲNG · ĐƯỜNG ĐI NGẮN NHẤT", 16, MUTED)
    brand.to_corner(DL, buff=0.24)
    series.to_corner(DR, buff=0.24)
    return VGroup(brand, series)


def info_card(title, items, accent=GOLD, width=5.0, height=5.05):
    bg = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        fill_color=PANEL,
        fill_opacity=0.94,
        stroke_color=GRID,
        stroke_opacity=0.55,
        stroke_width=1.1,
    )
    bg.move_to(RIGHT * 4.15 + DOWN * 0.20)

    accent_line = Line(
        bg.get_corner(UL) + RIGHT * 0.22 + DOWN * 0.10,
        bg.get_corner(DL) + RIGHT * 0.22 + UP * 0.10,
        color=accent,
        stroke_width=4.0,
    )

    title_m = fit_width(txt(title, 24, accent, BOLD), width - 0.70)
    title_m.move_to(bg.get_top() + DOWN * 0.38)
    title_m.align_to(bg, LEFT).shift(RIGHT * 0.48)

    body = VGroup()
    for item in items:
        kind = item[0]
        if kind == "text":
            _, s, size, color = item
            mob = txt(s, size, color)
        elif kind == "math":
            _, s, size, color = item
            mob = mty(s, size, color)
        elif kind == "gap":
            mob = Rectangle(width=0.01, height=0.08, stroke_opacity=0, fill_opacity=0)
        else:
            raise ValueError(f"Unknown card item: {kind}")
        body.add(mob)

    body.arrange(DOWN, aligned_edge=LEFT, buff=0.20)
    fit_width(body, width - 0.78)
    body.next_to(title_m, DOWN, aligned_edge=LEFT, buff=0.28)
    if body.get_bottom()[1] < bg.get_bottom()[1] + 0.22:
        body.scale_to_fit_height(height - 1.22)
        body.next_to(title_m, DOWN, aligned_edge=LEFT, buff=0.24)

    return VGroup(bg, accent_line, title_m, body)


# ==========================================================
# MAIN LESSON
# ==========================================================
class TraiPhang01(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(
            phi=67 * DEGREES,
            theta=-48 * DEGREES,
            zoom=0.98,
        )

    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def narrate_play(self, text, *animations, min_time=1.0, rate_func=smooth):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.play(*animations, run_time=max(dur, min_time), rate_func=rate_func)
        return dur

    def narrate_camera(self, text, phi=None, theta=None, zoom=None):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        kwargs = {"run_time": max(dur, 1.5)}
        if phi is not None:
            kwargs["phi"] = phi
        if theta is not None:
            kwargs["theta"] = theta
        if zoom is not None:
            kwargs["zoom"] = zoom
        self.move_camera(**kwargs)
        return dur

    def add_hud(self, chapter, title, subtitle, progress):
        h = header_group(chapter, title, subtitle, progress)
        f = footer_group()
        self.add_fixed_in_frame_mobjects(h, f)
        return VGroup(h, f)

    def clear_all(self, run_time=0.35):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
        self.clear()

    def vertex_labels(self, p, keys=None):
        if keys is None:
            keys = ["A", "B", "C", "D", "A1", "B1", "C1", "D1"]
        pretty = {
            "A": "A", "B": "B", "C": "C", "D": "D",
            "A1": "A'", "B1": "B'", "C1": "C'", "D1": "D'",
        }
        offsets = {
            "A": [-0.16, -0.14, -0.04],
            "B": [ 0.14, -0.14, -0.04],
            "C": [ 0.14,  0.12, -0.02],
            "D": [-0.16,  0.12, -0.02],
            "A1": [-0.15, -0.12,  0.13],
            "B1": [ 0.13, -0.12,  0.13],
            "C1": [ 0.14,  0.12,  0.13],
            "D1": [-0.16,  0.12,  0.13],
        }
        labs = VGroup()
        for k in keys:
            color = GREEN if k == "A" else (RED if k == "C1" else INK)
            lab = mty(pretty[k], 24, color).move_to(p[k] + np.array(offsets[k]))
            self.add_fixed_orientation_mobjects(lab)
            labs.add(lab)
        return labs

    # ------------------------------------------------------
    # 0. INTRO
    # ------------------------------------------------------
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=62 * DEGREES, theta=-48 * DEGREES, zoom=0.92)
        G = cube_model()
        self.add(G["faces"], G["edges"], G["hidden"], G["dots"])
        self.vertex_labels(G["p"], ["A", "C1"])

        title = txt("TRẢI PHẲNG 01", 42, GOLD, BOLD)
        sub = txt("KIẾN TRÊN LẬP PHƯƠNG", 35, INK, BOLD)
        line = txt("Một đường gấp khúc 3D có thể trở thành một đoạn thẳng 2D", 22, CYAN)
        g = VGroup(title, sub, line).arrange(DOWN, buff=0.18)
        g.to_edge(RIGHT, buff=0.52).shift(UP * 0.35)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g, shift=UP * 0.08), run_time=0.8)

        self.narrate(
            "Series mới bắt đầu bằng bài toán kinh điển nhưng rất giàu ý tưởng. "
            "Một con kiến đứng tại đỉnh A của lập phương cạnh a và muốn đi trên bề mặt tới đỉnh đối diện C phẩy. "
            "Nó không được bay xuyên qua khối. Mục tiêu của chúng ta không chỉ là ra đáp số, mà phải nhìn thấy chính xác mặt nào được mở, quay quanh cạnh nào, đường đi biến đổi ra sao và vì sao độ dài được bảo toàn.",
            2.0,
        )
        self.move_camera(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.98, run_time=1.2)

    # ------------------------------------------------------
    # 1. PROBLEM
    # ------------------------------------------------------
    def problem(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.98)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Kiến trên lập phương",
            "Từ A đến C' nhưng chỉ được đi trên bề mặt",
            "01 / 08",
        )
        G = cube_model()
        self.add(G["faces"], G["edges"], G["hidden"], G["dots"])
        self.vertex_labels(G["p"], ["A", "B", "C", "B1", "C1"])

        card = info_card(
            "ĐỀ BÀI",
            [
                ("text", "Lập phương cạnh a.", 22, INK),
                ("text", "Kiến đi từ A đến C'.", 22, INK),
                ("text", "Chỉ được bò trên các mặt.", 22, MUTED),
                ("gap",),
                ("math", "L_0 = ?", 37, GOLD),
            ],
            accent=GOLD,
        )
        self.add_fixed_in_frame_mobjects(card)
        self.play(FadeIn(card), run_time=0.6)

        # Show a naive edge route A -> B -> B' -> C'
        p = G["p"]
        edge_route = VGroup(
            solid(p["A"], p["B"], ORANGE, 7.0),
            solid(p["B"], p["B1"], ORANGE, 7.0),
            solid(p["B1"], p["C1"], ORANGE, 7.0),
        )
        ant = Dot3D(p["A"], radius=0.085, color=GREEN)
        self.add(ant)
        self.narrate_play(
            "Nếu chỉ đi theo các cạnh, một lộ trình rất tự nhiên là A đến B, lên B phẩy rồi sang C phẩy. "
            "Ba đoạn đều dài a nên tổng bằng ba a. Nhưng đây chỉ là một đường đi hợp lệ, chưa có lý do gì để tin nó ngắn nhất.",
            Create(edge_route),
            min_time=2.0,
        )
        formula = mty("L_1 = 3 a", 32, ORANGE)
        formula.move_to(RIGHT * 4.15 + DOWN * 1.80)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(FadeIn(formula), run_time=0.4)
        self.narrate(
            "Bài toán đường đi ngắn nhất trên bề mặt khác bài khoảng cách trong không gian. "
            "Đoạn thẳng A C phẩy xuyên qua bên trong lập phương nên không được phép. "
            "Ta phải biến bề mặt cong gấp khúc thành một miền phẳng mà vẫn giữ nguyên độ dài.",
            1.6,
        )

    # ------------------------------------------------------
    # 2. ISOLATE TWO FACES
    # ------------------------------------------------------
    def isolate_faces(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.02)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Chọn đúng hai mặt",
            "Đáy ABCD và mặt bên BCC'B' chung cạnh BC",
            "02 / 08",
        )

        bottom = bottom_face_visual()
        right = right_face_visual(0.0)
        self.add(bottom, right)

        p = cube_points_visual()
        labels = VGroup()
        for key, pos, color in [
            ("A", p["A"], GREEN),
            ("B", p["B"], INK),
            ("C", p["C"], INK),
            ("C'", p["C1"], RED),
        ]:
            lab = mty(key, 25, color).move_to(pos + np.array([0.0, 0.0, 0.16]))
            self.add_fixed_orientation_mobjects(lab)
            labels.add(lab)

        card = info_card(
            "Ý TƯỞNG",
            [
                ("text", "Hai mặt chung cạnh BC.", 21, INK),
                ("text", "BC là bản lề.", 21, GOLD),
                ("text", "Giữ BC cố định.", 21, MUTED),
                ("text", "Quay cứng mặt BCC'B'.", 21, MUTED),
                ("gap",),
                            ],
            accent=CYAN,
        )
        self.add_fixed_in_frame_mobjects(card)
        self.play(FadeIn(card), run_time=0.5)

        self.narrate(
            "Một lựa chọn tốt là giữ nguyên mặt đáy A B C D và mở mặt bên B C C phẩy B phẩy. "
            "Hai mặt có cạnh chung B C. Cạnh này sẽ đóng vai trò bản lề: mọi điểm trên B C phải đứng yên, còn toàn bộ mặt bên quay như một tấm cứng. "
            "Đây là điều kiện kỹ thuật rất quan trọng: ta không được kéo giãn, bóp méo hay dịch từng điểm riêng rẽ.",
            2.0,
        )

        hinge = solid(V(B0), V(C0), GOLD, 8.0)
        self.play(Indicate(hinge, color=GOLD, scale_factor=1.05), run_time=0.8)
        self.narrate(
            "Vì phép quay là một đẳng cự, mọi khoảng cách nằm trên mặt B C C phẩy B phẩy được bảo toàn. "
            "Đặc biệt, đường kiến sau khi gấp trở lại sẽ có đúng độ dài như đường thẳng tương ứng trên bản trải.",
            1.4,
        )

    # ------------------------------------------------------
    # 3. RIGID UNFOLD
    # ------------------------------------------------------
    def unfold(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.02)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Mở mặt quanh cạnh BC",
            "Phép quay cứng: cạnh bản lề đứng yên, mọi độ dài được giữ nguyên",
            "03 / 08",
        )

        bottom = bottom_face_visual()
        self.add(bottom)

        theta = ValueTracker(0.0)
        moving = always_redraw(lambda: right_face_visual(theta.get_value()))
        self.add(moving)

        card = info_card(
            "GEOMETRY",
            [
                ("text", "Trục quay: BC", 21, GOLD),
                ("text", "Góc quay: 90°", 21, INK),
                ("text", "B, C bất động.", 21, MUTED),
                ("text", "C' chuyển thành C₁.", 21, MUTED),
                ("gap",),
                ("math", "B C = B C", 29, CYAN),
                ("math", "B C' = B C_1", 29, CYAN),
            ],
            accent=GOLD,
        )
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Bây giờ mặt bên quay đúng chín mươi độ quanh đường thẳng B C. "
            "Hãy chú ý hai đầu B và C của bản lề không hề chuyển động. "
            "Điểm C phẩy chuyển động theo một cung tròn và cuối cùng rơi xuống cùng mặt phẳng với đáy. "
            "Ta gọi ảnh của C phẩy sau khi trải là C một.",
            theta.animate.set_value(PI / 2),
            min_time=4.0,
            rate_func=smooth,
        )

        self.narrate_camera(
            "Sau khi hai mặt đã đồng phẳng, ta chuyển camera về nhìn vuông góc bản trải. "
            "Lúc này bài toán ba chiều biến thành một bài hình học phẳng hoàn toàn chính xác.",
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1.02,
        )

    # ------------------------------------------------------
    # 4. THE NET
    # ------------------------------------------------------
    def net_and_straight_line(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.02)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Bản trải là hình chữ nhật 2a × a",
            "Đường ngắn nhất trong mặt phẳng là đoạn thẳng",
            "04 / 08",
        )

        n = net_points_visual()
        A, B, C, D = n["A"], n["B"], n["C"], n["D"]
        C1, B1 = n["C1f"], n["B1f"]
        M = n["M"]

        net = VGroup(
            face(A, B, C, D, color=BLUE, opacity=0.12),
            face(B, C, C1, B1, color=CYAN, opacity=0.12),
            solid(A, B, BLUE, 4.0),
            solid(B, C, GOLD, 5.5),
            solid(C, D, BLUE, 4.0),
            solid(D, A, BLUE, 4.0),
            solid(C, C1, CYAN, 4.0),
            solid(C1, B1, CYAN, 4.0),
            solid(B1, B, CYAN, 4.0),
        )
        self.add(net)

        # Labels are now fixed in the 2D plane.
        for s, pt, color, off in [
            ("A", A, GREEN, [-0.18, -0.14, 0]),
            ("B", B, INK, [0.0, -0.17, 0]),
            ("C", C, INK, [0.0, 0.17, 0]),
            ("C_1", C1, RED, [0.18, 0.15, 0]),
        ]:
            lab = mty(s, 24, color).move_to(pt + np.array(off))
            self.add(lab)

        straight = solid(A, C1, GOLD, 7.0)
        self.play(Create(straight), run_time=0.9)

        card = info_card(
            "BẢN TRẢI",
            [
                ("math", "A C_1 = sqrt((2 a)^2 + a^2)", 29, INK),
                ("math", "A C_1 = a sqrt(5)", 37, GOLD),
                ("gap",),
                ("text", "Đường thẳng cắt BC tại M.", 20, MUTED),
                ("math", "B M = M C = frac(a,2)", 29, CYAN),
            ],
            accent=GOLD,
        )
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Hai hình vuông ghép thành hình chữ nhật có chiều dài hai a và chiều rộng a. "
            "Trong mặt phẳng, đường ngắn nhất từ A tới ảnh C một là đoạn thẳng A C một. "
            "Bởi định lý Pythagore, độ dài của nó bằng căn của bốn a bình phương cộng a bình phương, tức a căn năm.",
            2.0,
        )

        m_dot = Dot(M, radius=0.07, color=GOLD)
        self.play(FadeIn(m_dot), run_time=0.35)
        m_lab = mty("M", 24, GOLD).move_to(M + DOWN * 0.18)
        self.add(m_lab)
        self.play(FadeIn(m_lab), run_time=0.3)

        self.narrate(
            "Đoạn A C một đi qua cạnh bản lề B C đúng tại trung điểm M. "
            "Đây không phải điều ta đoán bằng mắt. Tọa độ trên hình chữ nhật cho thấy đường từ góc trái dưới tới góc phải trên đi qua đường x bằng a tại đúng nửa chiều cao.",
            1.6,
        )

    # ------------------------------------------------------
    # 5. MOVE CROSSING POINT
    # ------------------------------------------------------
    def moving_crossing(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.02)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Nếu kiến qua BC tại một điểm X bất kỳ?",
            "Biến bài toán thành một họ đường gấp khúc trong bản trải",
            "05 / 08",
        )

        n = net_points_visual()
        A, B, C, D = n["A"], n["B"], n["C"], n["D"]
        C1, B1 = n["C1f"], n["B1f"]

        net = VGroup(
            face(A, B, C, D, color=BLUE, opacity=0.09),
            face(B, C, C1, B1, color=CYAN, opacity=0.09),
            solid(A, B, BLUE, 3.5),
            solid(B, C, GOLD, 5.0),
            solid(C, D, BLUE, 3.5),
            solid(D, A, BLUE, 3.5),
            solid(C, C1, CYAN, 3.5),
            solid(C1, B1, CYAN, 3.5),
            solid(B1, B, CYAN, 3.5),
        )
        self.add(net)

        t = ValueTracker(0.12)
        def x_point():
            return B + t.get_value() * (C - B)

        xdot = always_redraw(lambda: Dot(x_point(), radius=0.065, color=ORANGE))
        path = always_redraw(lambda: VGroup(
            solid(A, x_point(), ORANGE, 5.0),
            solid(x_point(), C1, ORANGE, 5.0),
        ))
        self.add(path, xdot)

        card = info_card(
            "ĐỘ DÀI QUA X",
            [
                ("math", "B X = t a", 30, ORANGE),
                ("math", "A X = a sqrt(1+t^2)", 28, INK),
                ("math", "X C_1 = a sqrt(1+(1-t)^2)", 27, INK),
                ("gap",),
                ("math", "L(t) = A X + X C_1", 31, GOLD),
            ],
            accent=ORANGE,
        )
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Giả sử kiến cắt cạnh B C tại một điểm X bất kỳ. "
            "Đặt B X bằng t a, với t chạy từ không đến một. "
            "Trên bản trải, đường đi có hai đoạn A X và X C một. "
            "Ta có thể viết tổng độ dài thành một hàm của t, nhưng điều quan trọng hơn là nhìn ra hai đoạn này chỉ là một đường gấp khúc nối A với C một.",
            t.animate.set_value(0.86),
            min_time=4.0,
            rate_func=linear,
        )

        self.narrate_play(
            "Khi X chạy dọc B C, tổng độ dài thay đổi. "
            "Nó chỉ nhỏ nhất khi hai đoạn thẳng hàng, bởi bất đẳng thức tam giác. "
            "Điều kiện thẳng hàng xảy ra đúng tại trung điểm M, tương ứng t bằng một phần hai.",
            t.animate.set_value(0.50),
            min_time=3.0,
            rate_func=smooth,
        )

        result = mty("t = frac(1,2)", 34, GREEN)
        result.move_to(RIGHT * 4.15 + DOWN * 2.15)
        self.add_fixed_in_frame_mobjects(result)
        self.play(FadeIn(result), run_time=0.4)

    # ------------------------------------------------------
    # 6. COMPUTE AND FOLD BACK
    # ------------------------------------------------------
    def fold_back(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.02)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Gấp trở lại lập phương",
            "Đoạn thẳng 2D trở thành hai đoạn geodesic trên hai mặt",
            "06 / 08",
        )

        n = net_points_visual()
        A, B, C, D = n["A"], n["B"], n["C"], n["D"]
        C1, B1, M = n["C1f"], n["B1f"], n["M"]

        bottom = VGroup(
            face(A, B, C, D, color=BLUE, opacity=0.12),
            solid(A, B, BLUE, 3.8),
            solid(B, C, GOLD, 5.5),
            solid(C, D, BLUE, 3.8),
            solid(D, A, BLUE, 3.8),
        )
        right_flat = VGroup(
            face(B, C, C1, B1, color=CYAN, opacity=0.13),
            solid(B, C, GOLD, 5.5),
            solid(C, C1, CYAN, 3.8),
            solid(C1, B1, CYAN, 3.8),
            solid(B1, B, CYAN, 3.8),
        )
        path1 = solid(A, M, GOLD, 7.0)
        path2 = solid(M, C1, GOLD, 7.0)
        self.add(bottom, right_flat, path1, path2)

        card = info_card(
            "ĐỘ DÀI TỐI ƯU",
            [
                ("math", "A M = frac(a sqrt(5),2)", 29, INK),
                ("math", "M C' = frac(a sqrt(5),2)", 29, INK),
                ("gap",),
                ("math", "L_0 = a sqrt(5)", 40, GOLD),
                ("text", "M là trung điểm BC.", 20, MUTED),
            ],
            accent=GREEN,
        )
        self.add_fixed_in_frame_mobjects(card)

        self.narrate(
            "Tại M, mỗi nửa của đường đi có độ dài a căn năm trên hai. "
            "Tổng bằng a căn năm. Bây giờ ta gấp mặt bên trở lại. "
            "Nếu mô hình được dựng đúng, đoạn M C một phải quay cùng mặt và trở thành chính đoạn M C phẩy trên mặt bên của lập phương.",
            1.8,
        )

        # Rebuild as a tracker-driven folded system so the path segment moves
        # by the same rigid rotation as the face.
        self.remove(right_flat, path2)
        theta = ValueTracker(PI / 2)

        moving_face = always_redraw(lambda: right_face_visual(theta.get_value()))

        def moving_path_segment():
            C_now_raw = rotate_point_axis(C10, B0, C0, theta.get_value())
            return solid(V((B0 + C0) / 2.0), V(C_now_raw), GOLD, 7.0)

        moving_path = always_redraw(moving_path_segment)
        self.add(moving_face, moving_path)

        self.narrate_camera(
            "Ta rời góc nhìn bản trải và trở lại phối cảnh ba chiều trước khi gấp.",
            phi=67 * DEGREES,
            theta=-48 * DEGREES,
            zoom=1.02,
        )

        self.narrate_play(
            "Mặt bên gấp ngược đúng chín mươi độ quanh B C. "
            "Đường vàng không trượt trên mặt; nó quay cùng mặt. "
            "Vì vậy độ dài sau khi gấp hoàn toàn không thay đổi.",
            theta.animate.set_value(0.0),
            min_time=4.0,
            rate_func=smooth,
        )

        self.narrate(
            "Kết quả trên khối ba chiều là đường gấp A M rồi M C phẩy. "
            "Tại cạnh B C, khi hai mặt được trải phẳng, hai đoạn trở thành một đường thẳng. "
            "Đó chính là điều kiện phản xạ đặc trưng của đường ngắn nhất trên một đa diện.",
            1.8,
        )

    # ------------------------------------------------------
    # 7. ANT WALKS THE OPTIMAL PATH
    # ------------------------------------------------------
    def ant_walk(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.98)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Kiểm chứng trên khối 3D",
            "Kiến đi A → M → C' trên đúng hai mặt",
            "07 / 08",
        )

        G = cube_model()
        self.add(G["faces"], G["edges"], G["hidden"], G["dots"])
        self.vertex_labels(G["p"], ["A", "B", "C", "C1"])

        Mraw = (B0 + C0) / 2.0
        A = V(A0)
        M = V(Mraw)
        C1 = V(C10)

        optimal = VGroup(
            solid(A, M, GOLD, 7.0),
            solid(M, C1, GOLD, 7.0),
        )
        self.play(Create(optimal), run_time=0.8)

        ant = Dot3D(A, radius=0.09, color=GREEN)
        self.add(ant)

        card = info_card(
            "SO SÁNH",
            [
                ("math", "L_1 = 3 a", 29, ORANGE),
                ("math", "L_2 = a (1+sqrt(2))", 29, MUTED),
                ("math", "L_0=a sqrt(5)", 36, GOLD),
                ("gap",),
                ("math", "sqrt(5) < 1+sqrt(2) < 3", 28, GREEN),
            ],
            accent=GOLD,
        )
        self.add_fixed_in_frame_mobjects(card)

        self.narrate_play(
            "Bây giờ con kiến đi theo đúng đường vừa chứng minh. "
            "Nửa đầu nằm trên mặt đáy và kết thúc tại trung điểm M của B C.",
            MoveAlongPath(ant, Line(A, M)),
            min_time=2.3,
            rate_func=linear,
        )
        self.narrate_play(
            "Từ M, kiến chuyển sang mặt bên B C C phẩy B phẩy và đi thẳng tới C phẩy. "
            "Không có đoạn nào xuyên qua bên trong khối.",
            MoveAlongPath(ant, Line(M, C1)),
            min_time=2.3,
            rate_func=linear,
        )

        self.narrate(
            "Ta cũng có thể so sánh với một đường hợp lệ khác: A tới B rồi đi theo đường chéo mặt B C phẩy, dài a cộng a căn hai. "
            "Giá trị đó vẫn lớn hơn a căn năm. "
            "Các cách chọn hai mặt tương đương khác của lập phương cho cùng kết quả do tính đối xứng.",
            1.8,
        )

    # ------------------------------------------------------
    # 8. SUMMARY
    # ------------------------------------------------------
    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_hud(
            "TRẢI PHẲNG · 01",
            "Bản đồ phương pháp",
            "Từ một đường đi trên đa diện tới một đoạn thẳng trong bản trải",
            "08 / 08",
        )

        left = VGroup(
            txt("1", 24, GOLD, BOLD),
            txt("Chọn chuỗi mặt mà đường có thể đi qua.", 22, INK),
            txt("2", 24, GOLD, BOLD),
            txt("Mở từng mặt bằng phép quay cứng quanh cạnh chung.", 22, INK),
            txt("3", 24, GOLD, BOLD),
            txt("Biến đổi điểm cùng đúng phép quay của mặt.", 22, INK),
            txt("4", 24, GOLD, BOLD),
            txt("Nối hai ảnh bằng đoạn thẳng.", 22, INK),
            txt("5", 24, GOLD, BOLD),
            txt("Gấp lại và kiểm tra đường nằm trên đúng các mặt.", 22, INK),
        )
        # Arrange as five two-item rows.
        rows = VGroup(*[
            VGroup(left[2*i], left[2*i+1]).arrange(RIGHT, buff=0.22)
            for i in range(5)
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        rows.move_to(LEFT * 2.7 + DOWN * 0.10)
        self.add_fixed_in_frame_mobjects(rows)

        right = info_card(
            "KẾT QUẢ VIDEO 01",
            [
                ("math", "B M = M C = frac(a,2)", 28, CYAN),
                ("math", "A M = M C' = frac(a sqrt(5),2)", 26, INK),
                ("gap",),
                ("math", "L_0 = a sqrt(5)", 42, GOLD),
                ("gap",),
                ("text", "Không kéo giãn mặt.", 19, MUTED),
                ("text", "Không dịch điểm bằng tay.", 19, MUTED),
                ("text", "Không đoán đường trên hình phối cảnh.", 19, MUTED),
            ],
            accent=GREEN,
            width=5.05,
            height=5.10,
        )
        self.add_fixed_in_frame_mobjects(right)

        self.narrate(
            "Video một kết thúc bằng năm bước sẽ dùng xuyên suốt cả series. "
            "Một: chọn đúng chuỗi mặt. Hai: mở mặt bằng phép quay cứng quanh cạnh chung. "
            "Ba: mọi điểm và mọi đoạn trên mặt phải đi theo cùng phép biến đổi. "
            "Bốn: giải bài toán đường thẳng trong bản trải. "
            "Năm: gấp trở lại để kiểm tra đường vừa tìm thực sự nằm trên các mặt đã chọn.",
            2.0,
        )
        self.narrate(
            "Kết quả của mô hình đầu tiên là L sao bằng a căn năm, với điểm chuyển mặt M là trung điểm B C. "
            "Nhưng điều đáng giữ lại không phải riêng con số căn năm, mà là nguyên lý: đường gấp khúc ngắn nhất trên các mặt trở thành một đoạn thẳng sau khi các mặt liên quan được trải đúng hình học.",
            1.8,
        )

        badge = txt("VIDEO 02 · HỘP CHỮ NHẬT — PHẢI SO SÁNH NHIỀU BẢN TRẢI", 19, CYAN, BOLD)
        badge.to_edge(DOWN, buff=0.62)
        self.add_fixed_in_frame_mobjects(badge)
        self.play(FadeIn(badge), run_time=0.5)
        self.narrate(
            "Sang video hai, khối hộp chữ nhật sẽ phá vỡ sự đối xứng đẹp của lập phương. "
            "Một bản trải đúng chưa chắc cho đường ngắn nhất toàn cục; ta phải tạo nhiều ứng viên, kiểm tra tính hợp lệ và so sánh chúng.",
            1.4,
        )

    def construct(self):
        self.intro()
        self.problem()
        self.isolate_faces()
        self.unfold()
        self.net_and_straight_line()
        self.moving_crossing()
        self.fold_back()
        self.ant_walk()
        self.summary()


# ==========================================================
# 480P SMOKE SCENE - NO TTS
# ==========================================================
class UnfoldSmoke(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)
        self.add(bottom_face_visual())
        theta = ValueTracker(0.0)
        moving = always_redraw(lambda: right_face_visual(theta.get_value()))
        self.add(moving)
        eq = mty("L_0 = a sqrt(5)", 30, GOLD).to_corner(UR, buff=0.25)
        self.add_fixed_in_frame_mobjects(eq)
        self.play(theta.animate.set_value(PI / 2), run_time=1.4)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.8)
        self.wait(0.2)


# ==========================================================
# RENDERERS
# ==========================================================
def render_smoke():
    geometry_preflight(verbose=True)
    config.pixel_width = 854
    config.pixel_height = 480
    config.frame_rate = 15
    config.media_dir = str(SMOKE_MEDIA_DIR)
    config.output_file = "trai_phang_01_unfold_smoke"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = True
    scene = UnfoldSmoke()
    scene.render()
    path = Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():
        raise RuntimeError(f"Khong tim thay smoke video: {path}")
    print(f"SMOKE VIDEO: {path}")
    return path


def render_full():
    geometry_preflight(verbose=True)

    config.pixel_width = FINAL_WIDTH
    config.pixel_height = FINAL_HEIGHT
    config.frame_rate = FINAL_FPS
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "trai_phang_01_kien_lap_phuong_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst)")
    print("Geometry engine: rigid hinge rotation + hard preflight")

    scene = TraiPhang01()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_trai_phang_01.wav"
    build_master_audio(scene.audio_events, video_duration, master_wav)

    final_path = video_path.with_name(video_path.stem + "_WITH_AUDIO.mp4")
    mux_audio(video_path, master_wav, final_path)
    validate_audio(master_wav)

    print("\n============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


if __name__ == "__main__":
    if "--geometry-preflight" in sys.argv:
        geometry_preflight(verbose=True)
        raise SystemExit(0)
    if "--smoke-render" in sys.argv:
        render_smoke()
        raise SystemExit(0)
    render_full()

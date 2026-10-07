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

# ==========================================================
# SERIES TRAI PHANG - VIDEO 01 MASTER
# LAP PHUONG: KIEN DI QUA HAI MAT KE NHAU
# Manim Community + native MathTypst + Edge TTS
# ==========================================================
# Muc tieu day hoc:
# 1. Hoc sinh hieu vi sao phai trai phang.
# 2. Hoc sinh tu nhan ra canh chung BC la noi doi mat.
# 3. Hoc sinh thay duong gap A-X-C' bien thanh duong gap A-X-C1.
# 4. Dung bat dang thuc tam giac de chung minh nghiem ngan nhat.
# 5. Gap lai de kiem chung duong tim duoc nam tren dung hai mat.
#
# Luu y san xuat:
# - Tat ca noi dung ky thuat nam trong code/workflow, KHONG doc trong TTS.
# - Bo cuc hai cot co dinh: hinh trai, bai giai phai.
# - Khong co title/cong thuc lon de len hinh 3D.
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


# ==========================================================
# AUDIO - MASTER TRACK ARCHITECTURE
# ==========================================================
def _audio_key(text):
    payload = json.dumps(
        {
            "text": text,
            "voice": GIONG_DOC,
            "rate": TOC_DO_DOC,
            "pitch": PITCH,
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
# LAYOUT - FIXED TWO COLUMNS
# ==========================================================
HEADER_Y = 3.52
FOOTER_Y = -3.72
DIVIDER_X = 0.38
LEFT_CENTER = np.array([-3.28, -0.08, 0.0])
RIGHT_CENTER = np.array([3.66, -0.10, 0.0])
CARD_W = 5.55
CARD_H = 5.78
ROW_Y = [1.55, 0.82, 0.09, -0.64, -1.37, -2.10]


def header(title, progress):
    tag = txt("TRẢI PHẲNG · 01", 16, GOLD, BOLD)
    tag.move_to(np.array([-5.80, HEADER_Y, 0]))
    title_m = fit_width(txt(title, 25, INK, BOLD), 8.8)
    title_m.move_to(np.array([-0.55, HEADER_Y, 0]))
    prog = txt(progress, 15, MUTED, BOLD)
    prog.move_to(np.array([6.12, HEADER_Y, 0]))
    rule = Line(
        np.array([-6.75, 3.18, 0]),
        np.array([6.75, 3.18, 0]),
        color=GRID,
        stroke_width=1.0,
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
        color=GRID,
        stroke_width=1.15,
        stroke_opacity=0.75,
    )


def lesson_card(title, rows, accent=CYAN):
    """Right-column card with six fixed non-overlapping row slots."""
    bg = RoundedRectangle(
        width=CARD_W,
        height=CARD_H,
        corner_radius=0.12,
        fill_color=PANEL,
        fill_opacity=0.96,
        stroke_color=GRID,
        stroke_width=1.0,
        stroke_opacity=0.70,
    ).move_to(RIGHT_CENTER)

    bar = Line(
        bg.get_corner(UL) + RIGHT * 0.20 + DOWN * 0.12,
        bg.get_corner(DL) + RIGHT * 0.20 + UP * 0.12,
        color=accent,
        stroke_width=4.0,
    )

    tt = fit_width(txt(title, 22, accent, BOLD), 4.55)
    tt.move_to(np.array([RIGHT_CENTER[0] - 0.10, 2.35, 0]))

    content = VGroup()
    for i, row in enumerate(rows[:6]):
        kind, value, size, color = row
        if kind == "text":
            mob = txt(value, size, color)
            max_w = 4.35
            max_h = 0.48
        elif kind == "math":
            mob = mty(value, size, color)
            max_w = 4.20
            max_h = 0.52
        else:
            raise ValueError(f"Unknown row type: {kind}")

        fit_width(mob, max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        mob.move_to(np.array([RIGHT_CENTER[0], ROW_Y[i], 0]))
        content.add(mob)

    return VGroup(bg, bar, tt, content)


def layout_preflight(verbose=True):
    samples = [
        lesson_card(
            "MỞ HAI MẶT RA",
            [
                ("text", "Giữ nguyên mặt đáy ABCD.", 20, INK),
                ("text", "Mở mặt BCC'B' quanh cạnh BC.", 20, INK),
                ("text", "Sau 90°, hai mặt nằm cùng một mặt phẳng.", 19, MUTED),
                ("math", "A C_1 = a sqrt(5)", 31, GOLD),
                ("math", "B M = M C = frac(a,2)", 28, CYAN),
            ],
            CYAN,
        ),
        lesson_card(
            "CHỨNG MINH NGẮN NHẤT",
            [
                ("math", "A X + X C_1 >= A C_1", 27, GOLD),
                ("text", "Dấu bằng khi A, X, C₁ thẳng hàng.", 19, INK),
                ("math", "B M = M C = frac(a,2)", 28, CYAN),
                ("math", "L_(min)=a sqrt(5)", 34, GREEN),
            ],
            GOLD,
        ),
    ]

    for card in samples:
        bg = card[0]
        title = card[2]
        body = card[3]
        # All items stay inside card margins.
        for mob in [title, *list(body)]:
            if mob.get_left()[0] < bg.get_left()[0] + 0.36:
                raise AssertionError("Right-card item crosses left safe margin.")
            if mob.get_right()[0] > bg.get_right()[0] - 0.22:
                raise AssertionError("Right-card item crosses right safe margin.")
            if mob.get_top()[1] > bg.get_top()[1] - 0.18:
                raise AssertionError("Right-card item crosses top safe margin.")
            if mob.get_bottom()[1] < bg.get_bottom()[1] + 0.18:
                raise AssertionError("Right-card item crosses bottom safe margin.")

        # Body rows must not overlap vertically.
        rows = list(body)
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                vertical_gap = max(
                    rows[i].get_bottom()[1] - rows[j].get_top()[1],
                    rows[j].get_bottom()[1] - rows[i].get_top()[1],
                )
                if vertical_gap < -1e-4:
                    raise AssertionError("Two right-card rows overlap.")

    if verbose:
        print("LAYOUT PREFLIGHT OK")
        print("  fixed two-column composition")
        print("  card rows inside safe margins")
        print("  no row overlap")
    return True


# ==========================================================
# EXACT CUBE GEOMETRY
# ==========================================================
SIDE_RAW = 3.0
H = SIDE_RAW / 2.0

A0 = np.array([-H, -H, -H])
B0 = np.array([ H, -H, -H])
C0 = np.array([ H,  H, -H])
D0 = np.array([-H,  H, -H])
A10 = np.array([-H, -H,  H])
B10 = np.array([ H, -H,  H])
C10 = np.array([ H,  H,  H])
D10 = np.array([-H,  H,  H])
M0 = (B0 + C0) / 2.0

WORLD_SCALE = 0.80
WORLD_SHIFT = np.array([-3.23, -0.12, 0.0])


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


def unfolded_right_points(angle=PI / 2):
    raw = [B0, C0, C10, B10]
    return [rotate_point_axis(p, B0, C0, angle) for p in raw]


def geometry_preflight(verbose=True):
    tol = 1e-9
    before = [B0, C0, C10, B10]
    after = unfolded_right_points(PI / 2)

    # Rigid face.
    if not np.allclose(
        pairwise_distances(before), pairwise_distances(after), atol=tol, rtol=0
    ):
        raise AssertionError("Unfolding does not preserve face distances.")

    # Hinge fixed.
    if np.linalg.norm(after[0] - B0) > tol or np.linalg.norm(after[1] - C0) > tol:
        raise AssertionError("Hinge BC moved during unfolding.")

    # Coplanar with bottom z=-H.
    if max(abs(p[2] + H) for p in after) > tol:
        raise AssertionError("Unfolded right face is not coplanar with bottom face.")

    C1_flat = after[2]
    expected_C1_flat = np.array([3 * H, H, -H])
    if np.linalg.norm(C1_flat - expected_C1_flat) > tol:
        raise AssertionError("Image of C' after unfolding is incorrect.")

    # Straight A-C1_flat crosses x=H at midpoint of BC.
    t = (H - A0[0]) / (C1_flat[0] - A0[0])
    X = A0 + t * (C1_flat - A0)
    if abs(t - 0.5) > tol:
        raise AssertionError("Straight path does not meet hinge at half parameter.")
    if np.linalg.norm(X - M0) > tol:
        raise AssertionError("Straight path does not meet BC at its midpoint.")

    # Length equality folded/unfolded.
    flat_len = np.linalg.norm(C1_flat - A0)
    folded_len = np.linalg.norm(M0 - A0) + np.linalg.norm(C10 - M0)
    expected = SIDE_RAW * math.sqrt(5)
    if abs(flat_len - expected) > tol or abs(folded_len - expected) > tol:
        raise AssertionError("Shortest length must equal a*sqrt(5).")
    if abs(flat_len - folded_len) > tol:
        raise AssertionError("Folded and unfolded path lengths differ.")

    # Naive legal paths are longer.
    edge_route = 3 * SIDE_RAW
    corner_route = SIDE_RAW * (1 + math.sqrt(2))
    if not (expected < corner_route < edge_route):
        raise AssertionError("Comparison with simple legal routes failed.")

    # Sample L(x), x in [0,a]. Minimum at a/2.
    xs = np.linspace(0.0, SIDE_RAW, 4001)
    vals = np.sqrt(SIDE_RAW**2 + xs**2) + np.sqrt(
        SIDE_RAW**2 + (SIDE_RAW - xs) ** 2
    )
    idx = int(np.argmin(vals))
    if abs(xs[idx] - SIDE_RAW / 2) > 1e-3:
        raise AssertionError("Numerical check: minimizing hinge point is not midpoint.")
    if abs(vals[idx] - expected) > 1e-6:
        raise AssertionError("Numerical check: minimum is not a*sqrt(5).")

    if verbose:
        print("GEOMETRY PREFLIGHT OK")
        print("  rigid unfolding of face BCC'B'")
        print("  hinge BC fixed")
        print("  unfolded face coplanar with ABCD")
        print("  straight line crosses BC at midpoint M")
        print("  folded length = unfolded length = a*sqrt(5)")
        print("  numerical L(x) minimum at x=a/2")
    return True


# ==========================================================
# DRAWING HELPERS
# ==========================================================
def solid(a, b, color=EDGE, width=4.0, opacity=0.96):
    return Line(
        np.array(a, dtype=float),
        np.array(b, dtype=float),
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
    )


def hidden_edge(a, b, color=DIM, width=2.7, opacity=0.70):
    return DashedLine(
        np.array(a, dtype=float),
        np.array(b, dtype=float),
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=0.11,
        dashed_ratio=0.56,
    )


def face_poly(*points, color=BLUE, opacity=0.10):
    return Polygon(
        *[np.array(p, dtype=float) for p in points],
        fill_color=color,
        fill_opacity=opacity,
        stroke_width=0,
    )


def cube_points():
    raw = {
        "A": A0, "B": B0, "C": C0, "D": D0,
        "A1": A10, "B1": B10, "C1": C10, "D1": D10,
    }
    return {k: W(v) for k, v in raw.items()}


def cube_visual(show_faces=True):
    p = cube_points()

    faces = VGroup()
    if show_faces:
        faces.add(
            face_poly(p["A"], p["B"], p["C"], p["D"], color=BLUE, opacity=0.055),
            face_poly(p["B"], p["C"], p["C1"], p["B1"], color=CYAN, opacity=0.10),
            face_poly(p["A1"], p["B1"], p["C1"], p["D1"], color=PURPLE, opacity=0.05),
        )

    visible_pairs = [
        ("A", "B"), ("B", "C"),
        ("A", "A1"), ("B", "B1"), ("C", "C1"),
        ("A1", "B1"), ("B1", "C1"), ("C1", "D1"), ("D1", "A1"),
    ]
    hidden_pairs = [("C", "D"), ("D", "A"), ("D", "D1")]

    edges = VGroup(*[
        solid(p[u], p[v], EDGE, 4.0) for u, v in visible_pairs
    ])
    hidden = VGroup(*[
        hidden_edge(p[u], p[v]) for u, v in hidden_pairs
    ])

    dots = VGroup(*[
        Dot3D(
            p[k],
            radius=0.055,
            color=GREEN if k == "A" else (RED if k == "C1" else GOLD),
        )
        for k in p
    ])
    return VGroup(faces, edges, hidden, dots)


def bottom_face_visual():
    A, B, C, D = map(W, [A0, B0, C0, D0])
    return VGroup(
        face_poly(A, B, C, D, color=BLUE, opacity=0.13),
        solid(A, B, BLUE, 4.0),
        solid(B, C, GOLD, 6.0),
        solid(C, D, BLUE, 4.0),
        solid(D, A, BLUE, 4.0),
        Dot3D(A, radius=0.07, color=GREEN),
    )


def right_face_visual(angle):
    B, C, C1, B1 = [W(p) for p in unfolded_right_points(angle)]
    return VGroup(
        face_poly(B, C, C1, B1, color=CYAN, opacity=0.16),
        solid(B, C, GOLD, 6.0),
        solid(C, C1, CYAN, 4.0),
        solid(C1, B1, CYAN, 4.0),
        solid(B1, B, CYAN, 4.0),
        Dot3D(C1, radius=0.07, color=RED),
    )


def flat_points():
    pts = unfolded_right_points(PI / 2)
    return {
        "A": W(A0),
        "B": W(B0),
        "C": W(C0),
        "D": W(D0),
        "B1f": W(pts[3]),
        "C1f": W(pts[2]),
        "M": W(M0),
    }


def flat_net_visual():
    p = flat_points()
    return VGroup(
        face_poly(p["A"], p["B"], p["C"], p["D"], color=BLUE, opacity=0.12),
        face_poly(p["B"], p["B1f"], p["C1f"], p["C"], color=CYAN, opacity=0.12),
        solid(p["A"], p["B"], BLUE, 4.0),
        solid(p["B"], p["C"], GOLD, 5.5),
        solid(p["C"], p["D"], BLUE, 4.0),
        solid(p["D"], p["A"], BLUE, 4.0),
        solid(p["B"], p["B1f"], CYAN, 4.0),
        solid(p["B1f"], p["C1f"], CYAN, 4.0),
        solid(p["C1f"], p["C"], CYAN, 4.0),
    )


def add_vertex_label(scene, text_value, point, color=INK, offset=(0, 0, 0.15), size=23):
    mob = mty(text_value, size, color).move_to(point + np.array(offset, dtype=float))
    scene.add_fixed_orientation_mobjects(mob)
    return mob


# ==========================================================
# MAIN LESSON
# ==========================================================
class TraiPhang01Master(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)

    def narrate(self, text, hold=0.45):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(dur + hold)
        return dur

    def narrate_play(self, text, *animations, min_time=1.0, hold=0.35, rate_func=smooth):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.play(*animations, run_time=max(dur, min_time), rate_func=rate_func)
        if hold > 0:
            self.wait(hold)
        return dur

    def narrate_camera(self, text, phi=None, theta=None, zoom=None, hold=0.35):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        kwargs = {"run_time": max(dur, 1.4)}
        if phi is not None:
            kwargs["phi"] = phi
        if theta is not None:
            kwargs["theta"] = theta
        if zoom is not None:
            kwargs["zoom"] = zoom
        self.move_camera(**kwargs)
        if hold > 0:
            self.wait(hold)
        return dur

    def add_frame(self, title, progress):
        h = header(title, progress)
        f = footer()
        d = divider()
        self.add_fixed_in_frame_mobjects(h, f, d)
        return VGroup(h, f, d)

    def add_card(self, title, rows, accent=CYAN):
        card = lesson_card(title, rows, accent)
        self.add_fixed_in_frame_mobjects(card)
        return card

    def clear_all(self, run_time=0.30):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
        self.clear()

    # ------------------------------------------------------
    # 01 - MO BAI
    # ------------------------------------------------------
    def scene_01_problem(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)
        self.add_frame("Kiến đi ngắn nhất qua hai mặt của lập phương", "01 / 10")

        cube = cube_visual()
        self.add(cube)
        p = cube_points()
        add_vertex_label(self, "A", p["A"], GREEN, (-0.18, -0.12, -0.08))
        add_vertex_label(self, "C'", p["C1"], RED, (0.12, 0.10, 0.16))

        self.add_card(
            "BÀI TOÁN",
            [
                ("text", "Lập phương ABCD.A'B'C'D' cạnh a.", 19, INK),
                ("text", "Kiến đi từ A đến C'.", 20, INK),
                ("text", "Chỉ được bò trên mặt đáy và mặt BCC'B'.", 18, MUTED),
                ("text", "Hỏi: đường đi ngắn nhất dài bao nhiêu?", 19, GOLD),
            ],
            GOLD,
        )

        self.narrate(
            "Các em nhìn vào khối lập phương. Con kiến bắt đầu ở đỉnh A và muốn tới đỉnh C phẩy. "
            "Trong bài này, nó chỉ được bò trên hai mặt: mặt đáy A B C D và mặt bên B C C phẩy B phẩy. "
            "Câu hỏi là: nó nên đổi từ mặt đáy sang mặt bên tại đâu để tổng quãng đường ngắn nhất?",
            hold=0.9,
        )
        self.narrate(
            "Nếu cho kiến đi xuyên qua lòng khối thì bài toán quá dễ, nhưng đó không phải đường đi trên bề mặt. "
            "Vì vậy ta phải tôn trọng hai mặt đã cho và tìm đường ngắn nhất ngay trên chúng.",
            hold=0.8,
        )

    # ------------------------------------------------------
    # 02 - HAI DUONG DE THAY NHUNG CHUA TOI UU
    # ------------------------------------------------------
    def scene_02_first_guesses(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)
        self.add_frame("Thử vài đường đi hợp lệ trước khi tối ưu", "02 / 10")

        cube = cube_visual()
        self.add(cube)
        p = cube_points()
        add_vertex_label(self, "A", p["A"], GREEN, (-0.18, -0.12, -0.08))
        add_vertex_label(self, "B", p["B"], INK, (0.12, -0.12, -0.08))
        add_vertex_label(self, "B'", p["B1"], INK, (0.13, -0.08, 0.15))
        add_vertex_label(self, "C'", p["C1"], RED, (0.12, 0.10, 0.16))

        edge_route = VGroup(
            solid(p["A"], p["B"], ORANGE, 7.0),
            solid(p["B"], p["B1"], ORANGE, 7.0),
            solid(p["B1"], p["C1"], ORANGE, 7.0),
        )
        self.add_card(
            "THỬ ĐƯỜNG ĐI",
            [
                ("text", "Đi theo ba cạnh: A → B → B' → C'.", 18, INK),
                ("math", "L_1 = 3a", 31, ORANGE),
                ("text", "Một cách khác: A → B rồi đi chéo tới C'.", 18, INK),
                ("math", "L_2 = a+a sqrt(2)", 29, CYAN),
            ],
            ORANGE,
        )

        self.narrate_play(
            "Cách đầu tiên rất tự nhiên: đi theo ba cạnh của lập phương. Khi đó quãng đường bằng ba a. "
            "Đường này chắc chắn hợp lệ, nhưng khá dài.",
            Create(edge_route),
            min_time=2.4,
        )

        diag_route = VGroup(
            solid(p["A"], p["B"], CYAN, 7.0),
            solid(p["B"], p["C1"], CYAN, 7.0),
        )
        self.play(FadeOut(edge_route), Create(diag_route), run_time=0.9)
        self.narrate(
            "Ta có thể làm tốt hơn: từ A đi tới B, rồi đi theo đường chéo của mặt bên tới C phẩy. "
            "Độ dài lúc này là a cộng a căn hai. Nhưng câu hỏi vẫn còn: có thể ngắn hơn nữa không?",
            hold=0.9,
        )

    # ------------------------------------------------------
    # 03 - DIEM DOI MAT X
    # ------------------------------------------------------
    def scene_03_where_to_cross(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)
        self.add_frame("Điểm đổi mặt nên nằm ở đâu trên BC?", "03 / 10")

        cube = cube_visual()
        self.add(cube)
        p = cube_points()
        A, B, C, C1 = p["A"], p["B"], p["C"], p["C1"]
        add_vertex_label(self, "A", A, GREEN, (-0.18, -0.12, -0.08))
        add_vertex_label(self, "B", B, INK, (0.12, -0.12, -0.08))
        add_vertex_label(self, "C", C, INK, (0.12, 0.10, -0.06))
        add_vertex_label(self, "C'", C1, RED, (0.12, 0.10, 0.16))

        t = ValueTracker(0.16)
        X = always_redraw(lambda: B + t.get_value() * (C - B))
        xdot = always_redraw(lambda: Dot3D(X(), radius=0.075, color=GOLD))
        path = always_redraw(
            lambda: VGroup(
                solid(A, X(), GOLD, 6.5),
                solid(X(), C1, GOLD, 6.5),
            )
        )
        self.add(path, xdot)

        self.add_card(
            "GỌI X LÀ ĐIỂM ĐỔI MẶT",
            [
                ("text", "X chạy trên cạnh chung BC.", 20, INK),
                ("text", "Đường đi có dạng A → X → C'.", 20, INK),
                ("math", "L = A X + X C'", 31, GOLD),
                ("text", "Ta cần chọn X sao cho tổng này nhỏ nhất.", 19, MUTED),
            ],
            GOLD,
        )

        self.narrate_play(
            "Mọi đường đi từ mặt đáy sang mặt bên đều phải đi qua cạnh chung B C. "
            "Gọi X là điểm mà con kiến đổi mặt. Khi X thay đổi, hai đoạn A X và X C phẩy cũng thay đổi. "
            "Ta cần tìm vị trí của X để tổng hai đoạn nhỏ nhất.",
            t.animate.set_value(0.84),
            min_time=4.4,
            rate_func=linear,
        )
        self.narrate_play(
            "Nhìn trực tiếp trên hình ba chiều thì rất khó đoán X nên nằm ở đâu. "
            "Đây chính là lúc trải phẳng phát huy tác dụng.",
            t.animate.set_value(0.50),
            min_time=2.4,
        )

    # ------------------------------------------------------
    # 04 - TRAI MAT
    # ------------------------------------------------------
    def scene_04_unfold(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)
        self.add_frame("Mở mặt bên xuống cùng mặt phẳng với đáy", "04 / 10")

        bottom = bottom_face_visual()
        self.add(bottom)
        angle = ValueTracker(0.0)
        moving = always_redraw(lambda: right_face_visual(angle.get_value()))
        self.add(moving)

        self.add_card(
            "MỞ HAI MẶT RA",
            [
                ("text", "Giữ nguyên mặt đáy ABCD.", 20, INK),
                ("text", "Mở mặt BCC'B' quanh cạnh BC.", 20, INK),
                ("text", "Sau 90°, hai mặt nằm cùng một mặt phẳng.", 18, MUTED),
                ("text", "Ảnh của C' sau khi mở gọi là C₁.", 19, CYAN),
            ],
            CYAN,
        )

        self.narrate_play(
            "Ta giữ nguyên mặt đáy. Bây giờ mở mặt bên B C C phẩy B phẩy xuống quanh cạnh B C, giống như mở một cánh cửa. "
            "Các em để ý: B và C không di chuyển, còn C phẩy đi theo mặt bên.",
            angle.animate.set_value(PI / 2),
            min_time=5.0,
            rate_func=smooth,
        )
        self.narrate_camera(
            "Khi mở đủ chín mươi độ, hai mặt nằm trên cùng một mặt phẳng. Ta đổi sang góc nhìn thẳng từ trên xuống để thấy bản trải thật rõ.",
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            zoom=1.0,
            hold=0.8,
        )

    # ------------------------------------------------------
    # 05 - DUONG THANG TREN BAN TRAI
    # ------------------------------------------------------
    def scene_05_straight_line(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_frame("Trên bản trải, đường ngắn nhất phải là đoạn thẳng", "05 / 10")

        net = flat_net_visual()
        self.add(net)
        p = flat_points()
        A, B, C, C1f, M = p["A"], p["B"], p["C"], p["C1f"], p["M"]

        for lab, pt, col, off in [
            ("A", A, GREEN, (-0.18, -0.14, 0)),
            ("B", B, INK, (0.00, -0.17, 0)),
            ("C", C, INK, (0.00, 0.17, 0)),
            ("C_1", C1f, RED, (0.18, 0.15, 0)),
        ]:
            self.add(mty(lab, 23, col).move_to(pt + np.array(off)))

        self.add_card(
            "Ý TƯỞNG QUYẾT ĐỊNH",
            [
                ("text", "X vẫn nằm trên đoạn BC.", 20, INK),
                ("text", "Đường đi trở thành A → X → C₁.", 19, INK),
                ("math", "A X + X C_1 >= A C_1", 28, GOLD),
                ("text", "Dấu bằng khi A, X, C₁ thẳng hàng.", 18, GREEN),
            ],
            GOLD,
        )

        t = ValueTracker(0.18)
        X = always_redraw(lambda: B + t.get_value() * (C - B))
        xdot = always_redraw(lambda: Dot(X(), radius=0.07, color=ORANGE))
        broken = always_redraw(
            lambda: VGroup(
                solid(A, X(), ORANGE, 5.5),
                solid(X(), C1f, ORANGE, 5.5),
            )
        )
        self.add(broken, xdot)

        self.narrate_play(
            "Sau khi trải phẳng, điểm X vẫn nằm trên cạnh B C. Đường A X rồi X C một là một đường gấp khúc trong mặt phẳng. "
            "Theo bất đẳng thức tam giác, tổng A X cộng X C một luôn lớn hơn hoặc bằng đoạn thẳng A C một.",
            t.animate.set_value(0.80),
            min_time=4.5,
            rate_func=linear,
        )

        self.narrate_play(
            "Dấu bằng chỉ xảy ra khi A, X và C một nằm trên cùng một đường thẳng. "
            "Vì vậy ta không cần đoán nữa: chỉ việc nối thẳng A với C một; giao điểm của đường thẳng này với B C chính là vị trí đổi mặt tối ưu.",
            t.animate.set_value(0.50),
            min_time=4.0,
            rate_func=smooth,
        )

        self.remove(broken)
        direct = solid(A, C1f, GOLD, 7.0)
        self.play(Create(direct), run_time=0.9)
        self.wait(0.6)

    # ------------------------------------------------------
    # 06 - TIM M VA DO DAI
    # ------------------------------------------------------
    def scene_06_compute(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_frame("Tính chính xác vị trí đổi mặt và độ dài ngắn nhất", "06 / 10")

        net = flat_net_visual()
        self.add(net)
        p = flat_points()
        A, B, C, C1f, M = p["A"], p["B"], p["C"], p["C1f"], p["M"]
        direct = solid(A, C1f, GOLD, 7.0)
        self.add(direct)
        self.add(Dot(M, radius=0.075, color=GOLD))
        self.add(mty("M", 23, GOLD).move_to(M + DOWN * 0.20))

        self.add_card(
            "TÍNH TOÁN",
            [
                ("text", "Bản trải là hình chữ nhật 2a × a.", 19, INK),
                ("math", "A C_1 = sqrt((2a)^2+a^2)", 28, INK),
                ("math", "A C_1 = a sqrt(5)", 33, GOLD),
                ("math", "B M = M C = frac(a,2)", 27, CYAN),
                ("math", "L_(min)=a sqrt(5)", 33, GREEN),
            ],
            GREEN,
        )

        self.narrate(
            "Hai hình vuông ghép lại thành một hình chữ nhật có chiều dài hai a và chiều rộng a. "
            "Vì thế đoạn A C một là đường chéo của hình chữ nhật này.",
            hold=0.8,
        )
        self.narrate(
            "Áp dụng định lý Pythagore, A C một bằng căn của hai a bình phương cộng a bình phương, tức là a căn năm. "
            "Đây chính là độ dài nhỏ nhất mà con kiến có thể đi trên hai mặt đã cho.",
            hold=0.8,
        )
        self.narrate(
            "Đường A C một đi qua B C tại trung điểm M. Do đó B M bằng M C bằng a trên hai. "
            "Vậy trên khối ban đầu, con kiến phải đổi mặt đúng tại trung điểm của cạnh B C.",
            hold=0.9,
        )

    # ------------------------------------------------------
    # 07 - SO SANH
    # ------------------------------------------------------
    def scene_07_compare(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_frame("So sánh với những đường đi ban đầu", "07 / 10")

        p = flat_points()
        A, C1f = p["A"], p["C1f"]
        self.add(flat_net_visual(), solid(A, C1f, GOLD, 7.0))

        self.add_card(
            "SO SÁNH",
            [
                ("math", "L_(min)=a sqrt(5)", 33, GREEN),
                ("math", "L_2=a(1+sqrt(2))", 28, CYAN),
                ("math", "L_1=3a", 29, ORANGE),
                ("math", "sqrt(5) < 1+sqrt(2) < 3", 26, GOLD),
            ],
            GREEN,
        )

        self.narrate(
            "Bây giờ ta quay lại hai đường đã thử lúc đầu. Đường đi theo ba cạnh dài ba a. "
            "Đường đi qua B rồi chéo tới C phẩy dài a nhân một cộng căn hai. "
            "Còn đường vừa tìm được chỉ dài a căn năm.",
            hold=0.7,
        )
        self.narrate(
            "Vì căn năm nhỏ hơn một cộng căn hai, và một cộng căn hai nhỏ hơn ba, đường qua trung điểm M thật sự ngắn hơn cả hai cách ban đầu. "
            "Quan trọng hơn, ta đã chứng minh được nó ngắn nhất trong tất cả các vị trí X trên B C, chứ không chỉ ngắn hơn vài đường thử.",
            hold=0.9,
        )

    # ------------------------------------------------------
    # 08 - GAP LAI
    # ------------------------------------------------------
    def scene_08_fold_back(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_frame("Gấp lại để kiểm tra đường vừa tìm", "08 / 10")

        bottom = bottom_face_visual()
        self.add(bottom)
        angle = ValueTracker(PI / 2)
        moving = always_redraw(lambda: right_face_visual(angle.get_value()))
        self.add(moving)

        A = W(A0)
        M = W(M0)
        self.add(solid(A, M, GOLD, 7.0))

        def second_piece():
            c_now = rotate_point_axis(C10, B0, C0, angle.get_value())
            return solid(M, W(c_now), GOLD, 7.0)

        moving_path = always_redraw(second_piece)
        self.add(moving_path)

        self.add_card(
            "GẤP TRỞ LẠI",
            [
                ("text", "Đoạn AM nằm trên mặt đáy.", 20, INK),
                ("text", "Đoạn MC₁ đi cùng mặt bên khi gấp.", 19, INK),
                ("text", "Sau khi gấp: MC₁ trở thành MC'.", 19, MUTED),
                ("math", "A M + M C' = a sqrt(5)", 29, GOLD),
            ],
            GOLD,
        )

        self.narrate_camera(
            "Ta đã giải xong trên bản trải. Bây giờ gấp mặt bên trở lại để xem đường thẳng vừa tìm biến thành đường nào trên lập phương.",
            phi=67 * DEGREES,
            theta=-48 * DEGREES,
            zoom=1.0,
            hold=0.5,
        )
        self.narrate_play(
            "Đoạn A M nằm nguyên trên mặt đáy. Đoạn M C một đi cùng mặt bên khi mặt này được gấp lên. "
            "Khi khối trở lại hình dạng ban đầu, M C một trở thành đúng đoạn M C phẩy.",
            angle.animate.set_value(0.0),
            min_time=4.7,
            rate_func=smooth,
        )
        self.narrate(
            "Như vậy đường ngắn nhất trên khối là A đến M, rồi M đến C phẩy, với M là trung điểm B C. "
            "Không có đoạn nào xuyên qua bên trong lập phương.",
            hold=0.8,
        )

    # ------------------------------------------------------
    # 09 - KIEN CHAY THAT
    # ------------------------------------------------------
    def scene_09_ant_walk(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)
        self.add_frame("Con kiến đi theo đường tối ưu", "09 / 10")

        cube = cube_visual()
        self.add(cube)
        p = cube_points()
        A, M, C1 = W(A0), W(M0), W(C10)
        add_vertex_label(self, "A", A, GREEN, (-0.18, -0.12, -0.08))
        add_vertex_label(self, "M", M, GOLD, (0.12, 0.00, -0.08))
        add_vertex_label(self, "C'", C1, RED, (0.12, 0.10, 0.16))

        route = VGroup(
            solid(A, M, GOLD, 7.0),
            solid(M, C1, GOLD, 7.0),
        )
        self.play(Create(route), run_time=0.9)
        ant = Dot3D(A, radius=0.09, color=GREEN)
        self.add(ant)

        self.add_card(
            "KẾT QUẢ",
            [
                ("math", "M in B C", 27, INK),
                ("math", "B M = M C = frac(a,2)", 28, CYAN),
                ("math", "L_(min)=a sqrt(5)", 35, GOLD),
                ("text", "Đường đi: A → M → C'.", 20, GREEN),
            ],
            GOLD,
        )

        self.narrate_play(
            "Con kiến đi từ A tới trung điểm M của B C trên mặt đáy.",
            MoveAlongPath(ant, Line(A, M)),
            min_time=2.5,
            rate_func=linear,
        )
        self.narrate_play(
            "Tại M, nó chuyển sang mặt bên và tiếp tục đi thẳng tới C phẩy. "
            "Hai đoạn này chính là hai phần của một đoạn thẳng duy nhất khi ta mở hai mặt ra.",
            MoveAlongPath(ant, Line(M, C1)),
            min_time=3.0,
            rate_func=linear,
        )

    # ------------------------------------------------------
    # 10 - TONG KET
    # ------------------------------------------------------
    def scene_10_summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_frame("Phương pháp cho bài đường đi qua hai mặt kề nhau", "10 / 10")

        left_box = RoundedRectangle(
            width=6.1,
            height=5.6,
            corner_radius=0.12,
            fill_color=PANEL_2,
            fill_opacity=0.52,
            stroke_color=GRID,
            stroke_width=1.0,
        ).move_to(LEFT_CENTER)
        self.add(left_box)

        steps = VGroup(
            VGroup(txt("1", 22, GOLD, BOLD), txt("Xác định hai mặt mà đường đi sử dụng.", 20, INK)).arrange(RIGHT, buff=0.24),
            VGroup(txt("2", 22, GOLD, BOLD), txt("Mở một mặt quanh cạnh chung.", 20, INK)).arrange(RIGHT, buff=0.24),
            VGroup(txt("3", 22, GOLD, BOLD), txt("Nối thẳng hai điểm trên bản trải.", 20, INK)).arrange(RIGHT, buff=0.24),
            VGroup(txt("4", 22, GOLD, BOLD), txt("Tìm giao điểm với cạnh chung.", 20, INK)).arrange(RIGHT, buff=0.24),
            VGroup(txt("5", 22, GOLD, BOLD), txt("Gấp lại và đọc đường đi trên khối.", 20, INK)).arrange(RIGHT, buff=0.24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        steps.move_to(LEFT_CENTER)
        self.add_fixed_in_frame_mobjects(steps)

        self.add_card(
            "BÀI HỌC CỐT LÕI",
            [
                ("text", "Đừng tối ưu trực tiếp trên hình phối cảnh.", 18, INK),
                ("text", "Hãy đưa các mặt liên quan về cùng một mặt phẳng.", 18, INK),
                ("math", "A X + X C_1 >= A C_1", 27, GOLD),
                ("math", "L_(min)=a sqrt(5)", 34, GREEN),
                ("text", "M là trung điểm của BC.", 20, CYAN),
            ],
            GREEN,
        )

        self.narrate(
            "Ta chốt lại cách làm. Trước hết xác định những mặt mà con kiến được phép đi qua. "
            "Sau đó mở các mặt ấy ra quanh cạnh chung. Khi đã nằm trên cùng một mặt phẳng, nối hai điểm bằng đoạn thẳng. "
            "Giao điểm của đoạn thẳng với cạnh chung cho ta điểm đổi mặt trên khối.",
            hold=0.8,
        )
        self.narrate(
            "Trong bài này, điểm đổi mặt là trung điểm M của B C và quãng đường ngắn nhất bằng a căn năm. "
            "Điều cần nhớ nhất không phải con số a căn năm, mà là ý tưởng: một đường gấp trên hai mặt có thể trở thành một đoạn thẳng sau khi trải đúng hai mặt đó.",
            hold=1.0,
        )
        badge = txt("VIDEO 02 · KIẾN ĐI QUA BA MẶT", 18, CYAN, BOLD)
        badge.move_to(np.array([3.65, -2.78, 0]))
        self.add_fixed_in_frame_mobjects(badge)
        self.play(FadeIn(badge), run_time=0.5)
        self.narrate(
            "Ở video tiếp theo, hai điểm sẽ nằm trên hai mặt không kề nhau. Khi đó con kiến bắt buộc phải đi qua một mặt trung gian, và bản trải sẽ gồm ba mặt nối tiếp.",
            hold=0.8,
        )

    def construct(self):
        self.scene_01_problem()
        self.scene_02_first_guesses()
        self.scene_03_where_to_cross()
        self.scene_04_unfold()
        self.scene_05_straight_line()
        self.scene_06_compute()
        self.scene_07_compare()
        self.scene_08_fold_back()
        self.scene_09_ant_walk()
        self.scene_10_summary()


# ==========================================================
# SMOKE SCENE - NO TTS
# ==========================================================
class Smoke01Master(ThreeDScene):
    def construct(self):
        geometry_preflight(False)
        layout_preflight(False)
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=1.0)
        self.add(bottom_face_visual())
        angle = ValueTracker(0.0)
        moving = always_redraw(lambda: right_face_visual(angle.get_value()))
        self.add(moving)
        card = lesson_card(
            "MỞ HAI MẶT RA",
            [
                ("text", "Giữ nguyên mặt đáy ABCD.", 20, INK),
                ("text", "Mở mặt BCC'B' quanh cạnh BC.", 20, INK),
                ("math", "L_(min)=a sqrt(5)", 32, GOLD),
            ],
            CYAN,
        )
        self.add_fixed_in_frame_mobjects(card, divider())
        self.play(angle.animate.set_value(PI / 2), run_time=1.5)
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=0.8)
        self.wait(0.2)


# ==========================================================
# SOURCE LINT FOR STUDENT-FACING NARRATION
# ==========================================================
STUDENT_AUDIO_FORBIDDEN = [
    "workflow",
    "render",
    "preflight",
    "engine",
    "cột trái",
    "cột phải",
    "animation",
    "camera",
    "mã nguồn",
    "code",
]


def narration_lint(verbose=True):
    source = Path(sys.argv[0]).resolve().read_text(encoding="utf-8")
    tree = ast.parse(source)
    narrations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"narrate", "narrate_play", "narrate_camera"} and node.args:
                value = node.args[0]
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    narrations.append(value.value)
    bad = []
    for text_value in narrations:
        low = text_value.lower()
        for term in STUDENT_AUDIO_FORBIDDEN:
            if term in low:
                bad.append((term, text_value))
    if bad:
        for term, text_value in bad:
            print("BAD NARRATION TERM:", term, "::", text_value)
        raise AssertionError("Production jargon found in student-facing narration.")
    if verbose:
        words = sum(len(x.split()) for x in narrations)
        print(f"NARRATION LINT OK: {len(narrations)} segments, about {words} words")
    return True


# ==========================================================
# RENDERERS
# ==========================================================
def render_smoke():
    geometry_preflight(True)
    layout_preflight(True)
    narration_lint(True)

    config.pixel_width = 854
    config.pixel_height = 480
    config.frame_rate = 15
    config.media_dir = str(SMOKE_MEDIA_DIR)
    config.output_file = "trai_phang_01_master_smoke"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = True

    scene = Smoke01Master()
    scene.render()
    path = Path(scene.renderer.file_writer.movie_file_path)
    if not path.exists():
        raise RuntimeError(f"Khong tim thay smoke video: {path}")
    print(f"SMOKE VIDEO: {path}")
    return path


def render_full():
    geometry_preflight(True)
    layout_preflight(True)
    narration_lint(True)

    config.pixel_width = FINAL_WIDTH
    config.pixel_height = FINAL_HEIGHT
    config.frame_rate = FINAL_FPS
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "trai_phang_01_lap_phuong_hai_mat_MASTER_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    scene = TraiPhang01Master()
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

    print("============================================================")
    print(f"VIDEO HOAN CHINH: {final_path}")
    print(f"Narration segments: {len(scene.audio_events)}")
    print(f"Duration: {probe_duration(final_path):.2f}s")
    print("============================================================")
    return final_path


if __name__ == "__main__":
    if "--geometry-preflight" in sys.argv:
        geometry_preflight(True)
        raise SystemExit(0)
    if "--layout-preflight" in sys.argv:
        layout_preflight(True)
        raise SystemExit(0)
    if "--narration-lint" in sys.argv:
        narration_lint(True)
        raise SystemExit(0)
    if "--smoke-render" in sys.argv:
        render_smoke()
        raise SystemExit(0)
    render_full()

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
# HHKG CHUYEN SAU 05 - MANIM + TYPST - MASTER TEMPLATE
# Standalone 100% for GitHub Actions
#
# Visual grammar for the whole HHKG series:
#   - visible polyhedron edges: solid
#   - hidden polyhedron edges: dashed neutral
#   - auxiliary / projection lines: dashed accent
#   - fixed teaching camera inside each geometry scene
#   - mathematics only in MathTypst; prose in Text
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

# ==========================================================
# PREMIUM PALETTE
# ==========================================================
BG = "#08111F"
PANEL = "#0D1B2E"
PANEL_2 = "#10233C"
INK = "#F3F7FF"
MUTED = "#8EA7C2"
GRID = "#25415E"
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
# TYPOGRAPHY
# ==========================================================
def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


_FORBIDDEN_TYPST_WORDS = {"sect", "intersect", "angle"}


def validate_typst_expr(s):
    """Fail early on known-invalid Typst math tokens used in this series."""
    words = set(s.replace("(", " " ).replace(")", " " ).replace(",", " " ).split())
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(
            f"Forbidden Typst math token(s) {bad} in {s!r}. "
            "Use 'inter' for intersection and 'hat(...)' for plane angles."
        )
    if "/" in s:
        raise ValueError(
            f"Slash fraction is forbidden in HHKG MathTypst: {s!r}. Use frac(..., ...)."
        )
    return s


def mty(s, size=38, color=INK):
    """Math only. Text prose must use txt()."""
    s = validate_typst_expr(s)
    try:
        return MathTypst(s, font_size=size, color=color)
    except Exception as exc:
        raise RuntimeError(f"MathTypst failed for expression: {s!r}") from exc


def fit_width(mob, width):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def fit_height(mob, height):
    if mob.height > height:
        mob.scale_to_fit_height(height)
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

    filter_complex = (
        ";".join(filters)
        + ";"
        + "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    )

    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", *inputs,
            "-filter_complex", filter_complex,
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
# 3D GEOMETRY
# ==========================================================
GEO_SCALE = 0.80
GEO_SHIFT = np.array([-1.78, -0.02, -0.08])
VIEW_PHI = 68 * DEGREES
VIEW_THETA = -54 * DEGREES
VIEW_ZOOM = 0.97


def L(x, y, z):
    """Logical geometry -> scene geometry."""
    return GEO_SCALE * np.array([float(x), float(y), float(z)]) + GEO_SHIFT


def solid(a, b, color=EDGE, width=4.0, opacity=0.94):
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def hidden_edge(a, b, color=DIM, width=2.7, opacity=0.70, dash=0.11):
    return DashedLine(
        a, b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def aux(a, b, color=CYAN, width=3.7, opacity=0.90, dash=0.11):
    return DashedLine(
        a, b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.56,
    )


def face(*points, color=BLUE, opacity=0.10, stroke=BLUE, stroke_width=0.0):
    return Polygon(
        *points,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=stroke_width,
        stroke_opacity=0.0 if stroke_width == 0 else 0.55,
    )


def right_angle_3d(vertex, u, v, size=0.30, color=GOLD, width=4.5):
    u = np.array(u, dtype=float)
    v = np.array(v, dtype=float)
    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)
    p1 = vertex + size * u
    p2 = vertex + size * (u + v)
    p3 = vertex + size * v
    return VGroup(
        solid(p1, p2, color=color, width=width),
        solid(p2, p3, color=color, width=width),
    )


def arc_basis(center, e1, e2, angle, radius=0.52, color=GOLD, width=6):
    e1 = np.array(e1, dtype=float)
    e2 = np.array(e2, dtype=float)
    e1 /= np.linalg.norm(e1)
    e2 /= np.linalg.norm(e2)
    return ParametricFunction(
        lambda t: center + radius * (math.cos(t) * e1 + math.sin(t) * e2),
        t_range=[0, angle],
        color=color,
        stroke_width=width,
    )


# ==========================================================
# SCENE
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(
            phi=VIEW_PHI,
            theta=VIEW_THETA,
            zoom=VIEW_ZOOM,
        )

    # ------------------------------------------------------
    # AUDIO
    # ------------------------------------------------------
    def narrate(self, text, min_visual_time=1.0):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.wait(max(dur, min_visual_time))
        return dur

    def narrate_play(self, text, *animations, min_time=1.0, rate_func=linear):
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        self.play(*animations, run_time=max(dur, min_time), rate_func=rate_func)
        return dur

    def narrate_camera(self, text, **kwargs):
        # The didactic view is intentionally fixed so hidden-edge styling stays correct.
        return self.narrate(text, min_visual_time=1.8)

    # ------------------------------------------------------
    # FIXED 2-COLUMN UI
    # ------------------------------------------------------
    def clear_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.32)
        self.clear()

    def add_header(self, title, subtitle, progress):
        series = txt("HHKG CHUYÊN SÂU · 05", 15, BLUE, BOLD)
        series.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.30)

        title_m = fit_width(txt(title, 29, INK, BOLD), 8.9)
        title_m.next_to(series, DOWN, buff=0.045, aligned_edge=LEFT)

        sub_m = fit_width(txt(subtitle, 17, MUTED), 8.9)
        sub_m.next_to(title_m, DOWN, buff=0.045, aligned_edge=LEFT)

        accent = Line(
            series.get_left() + DOWN * 0.13,
            series.get_left() + RIGHT * 0.62 + DOWN * 0.13,
            color=GOLD, stroke_width=3.2,
        )

        prog = txt(progress, 15, MUTED, BOLD)
        prog.to_edge(UP, buff=0.20).to_edge(RIGHT, buff=0.32)

        rule = Line(
            LEFT * 6.82, RIGHT * 6.82,
            color=GRID, stroke_width=0.9, stroke_opacity=0.42,
        ).shift(UP * 2.78)

        divider = Line(
            np.array([1.50, -2.83, 0]),
            np.array([1.50, 2.64, 0]),
            color=GRID, stroke_width=1.0, stroke_opacity=0.42,
        )

        teacher = txt(TEN_THAY, 15, MUTED)
        teacher.to_edge(DOWN, buff=0.10).to_edge(LEFT, buff=0.30)

        hud = VGroup(series, title_m, sub_m, accent, prog, rule, divider, teacher)
        self.add_fixed_in_frame_mobjects(hud)
        return hud

    def card(self, kicker, title, items, accent=GOLD, height=5.25, auto_add=True):
        bg = Rectangle(
            width=5.12,
            height=height,
            fill_color=PANEL,
            fill_opacity=0.90,
            stroke_color=GRID,
            stroke_width=0.9,
            stroke_opacity=0.36,
        ).move_to(RIGHT * 4.28 + DOWN * 0.03)

        spine = Line(
            bg.get_corner(UL) + RIGHT * 0.12 + DOWN * 0.18,
            bg.get_corner(DL) + RIGHT * 0.12 + UP * 0.18,
            color=accent, stroke_width=3.8, stroke_opacity=0.95,
        )

        k = txt(kicker.upper(), 14, accent, BOLD)
        k.move_to(bg.get_corner(UL) + RIGHT * 0.36 + DOWN * 0.30, aligned_edge=LEFT)

        t = fit_width(txt(title, 23, INK, BOLD), 4.30)
        t.next_to(k, DOWN, buff=0.10, aligned_edge=LEFT)

        body = VGroup()
        for item in items:
            kind = item[0]
            if kind == "text":
                _, text_s, size, color, weight = item
                mob = txt(text_s, size, color, weight)
            elif kind == "math":
                _, expr, size, color = item
                mob = mty(expr, size, color)
            elif kind == "sep":
                mob = Line(LEFT * 2.00, RIGHT * 2.00, color=GRID, stroke_width=0.9, stroke_opacity=0.55)
            elif kind == "obj":
                mob = item[1]
            else:
                raise ValueError(f"Unknown card item: {kind}")
            body.add(fit_width(mob, 4.28))

        body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        body.next_to(t, DOWN, buff=0.22, aligned_edge=LEFT)
        fit_height(body, height - 1.45)

        group = VGroup(bg, spine, k, t, body)
        if auto_add:
            self.add_fixed_in_frame_mobjects(group)
        return group

    def swap_card(self, old, new, run_time=0.45):
        new.set_opacity(0)
        self.add_fixed_in_frame_mobjects(new)
        self.play(
            FadeOut(old, shift=UP * 0.05),
            new.animate.set_opacity(1),
            run_time=run_time,
        )
        self.remove_fixed_in_frame_mobjects(old)

    def takeaway(self, text_s):
        label = fit_width(txt(text_s, 16, CYAN, BOLD), 7.15)
        label.move_to(LEFT * 2.55 + DOWN * 2.52)
        self.add_fixed_in_frame_mobjects(label)
        return label

    def legend(self):
        return VGroup()

    # ------------------------------------------------------
    # MODEL
    # ------------------------------------------------------
    def pts(self):
        return {
            "A": L(-2, -2, 0),
            "B": L( 2, -2, 0),
            "C": L( 2,  2, 0),
            "D": L(-2,  2, 0),
            "S": L(-2, -2, 3),
        }

    def pyramid(self, dim=False, base_fill=0.08):
        p = self.pts()

        vis_color = DIM if dim else EDGE
        vis_opacity = 0.42 if dim else 0.94
        vis_width = 2.5 if dim else 3.8

        hid_color = "#405A73" if dim else DIM
        hid_opacity = 0.42 if dim else 0.70
        hid_width = 2.1 if dim else 2.7

        # Fixed teaching view:
        # visible: AB, BC, SA, SB, SC
        # hidden:  CD, DA, SD
        visible_edges = VGroup(
            solid(p["A"], p["B"], vis_color, vis_width, vis_opacity),
            solid(p["B"], p["C"], vis_color, vis_width, vis_opacity),
            solid(p["S"], p["A"], vis_color, vis_width, vis_opacity),
            solid(p["S"], p["B"], vis_color, vis_width, vis_opacity),
            solid(p["S"], p["C"], vis_color, vis_width, vis_opacity),
        )
        hidden_edges = VGroup(
            hidden_edge(p["C"], p["D"], hid_color, hid_width, hid_opacity),
            hidden_edge(p["D"], p["A"], hid_color, hid_width, hid_opacity),
            hidden_edge(p["S"], p["D"], hid_color, hid_width, hid_opacity),
        )

        base = face(
            p["A"], p["B"], p["C"], p["D"],
            color=BLUE, opacity=base_fill, stroke_width=0,
        )

        dots = VGroup(
            Dot3D(p["A"], radius=0.055, color=GOLD),
            Dot3D(p["B"], radius=0.055, color=GOLD),
            Dot3D(p["C"], radius=0.055, color=GOLD),
            Dot3D(p["D"], radius=0.055, color=GOLD),
            Dot3D(p["S"], radius=0.062, color=RED),
        )

        return {
            "p": p,
            "base": base,
            "visible_edges": visible_edges,
            "hidden_edges": hidden_edges,
            "edges": VGroup(visible_edges, hidden_edges),
            "dots": dots,
        }

    def labels(self, model, names=("A", "B", "C", "D", "S")):
        p = model["p"]
        offsets = {
            "A": np.array([-0.20, -0.18, -0.03]),
            "B": np.array([ 0.18, -0.16, -0.03]),
            "C": np.array([ 0.18,  0.13,  0.04]),
            "D": np.array([-0.20,  0.13,  0.04]),
            "S": np.array([-0.18, -0.13,  0.16]),
        }
        labs = VGroup()
        for name in names:
            lab = mty(name, 25, RED if name == "S" else GOLD)
            lab.move_to(p[name] + offsets[name])
            self.add_fixed_orientation_mobjects(lab)
            labs.add(lab)
        return labs

    def show_base_model(self, dim=False, base_fill=0.08):
        G = self.pyramid(dim=dim, base_fill=base_fill)
        self.add(G["base"], G["edges"], G["dots"])
        self.labels(G)
        return G


    # ======================================================
    # CUBE HELPERS FOR VIDEO 04
    # ======================================================
    def cube_pts(self):
        return {
            "A": L(-2, -2, 0),
            "B": L( 2, -2, 0),
            "C": L( 2,  2, 0),
            "D": L(-2,  2, 0),
            "A1":L(-2, -2, 4),
            "B1":L( 2, -2, 4),
            "C1":L( 2,  2, 4),
            "D1":L(-2,  2, 4),
        }

    def cube(self, dim=False, base_fill=0.05, top_fill=0.025):
        p = self.cube_pts()
        vis_color = DIM if dim else EDGE
        vis_opacity = 0.42 if dim else 0.94
        vis_width = 2.4 if dim else 3.7
        hid_color = "#405A73" if dim else DIM
        hid_opacity = 0.42 if dim else 0.68
        hid_width = 2.0 if dim else 2.6

        visible = VGroup(
            solid(p["A"],p["B"],vis_color,vis_width,vis_opacity),
            solid(p["B"],p["C"],vis_color,vis_width,vis_opacity),
            solid(p["A"],p["A1"],vis_color,vis_width,vis_opacity),
            solid(p["B"],p["B1"],vis_color,vis_width,vis_opacity),
            solid(p["C"],p["C1"],vis_color,vis_width,vis_opacity),
            solid(p["A1"],p["B1"],vis_color,vis_width,vis_opacity),
            solid(p["B1"],p["C1"],vis_color,vis_width,vis_opacity),
        )
        hidden = VGroup(
            hidden_edge(p["C"],p["D"],hid_color,hid_width,hid_opacity),
            hidden_edge(p["D"],p["A"],hid_color,hid_width,hid_opacity),
            hidden_edge(p["D"],p["D1"],hid_color,hid_width,hid_opacity),
            hidden_edge(p["C1"],p["D1"],hid_color,hid_width,hid_opacity),
            hidden_edge(p["D1"],p["A1"],hid_color,hid_width,hid_opacity),
        )
        base = face(p["A"],p["B"],p["C"],p["D"],color=BLUE,opacity=base_fill,stroke_width=0)
        top = face(p["A1"],p["B1"],p["C1"],p["D1"],color=PURPLE,opacity=top_fill,stroke_width=0)
        dots = VGroup(*[Dot3D(p[k],radius=0.047,color=GOLD) for k in p])
        return {"p":p,"visible_edges":visible,"hidden_edges":hidden,"edges":VGroup(visible,hidden),"base":base,"top":top,"dots":dots}

    def cube_labels(self, G, names=None):
        p=G["p"]
        if names is None:
            names=["A","B","C","D","A1","B1","C1","D1"]
        offsets={
            "A":np.array([-0.18,-0.16,-0.05]), "B":np.array([0.17,-0.15,-0.04]),
            "C":np.array([0.16,0.13,0.03]), "D":np.array([-0.18,0.13,0.03]),
            "A1":np.array([-0.20,-0.14,0.14]), "B1":np.array([0.16,-0.13,0.12]),
            "C1":np.array([0.16,0.12,0.12]), "D1":np.array([-0.20,0.12,0.12]),
        }
        labs=VGroup()
        for name in names:
            show=name.replace("1", "'")
            lab=mty(show,23,GOLD)
            lab.move_to(p[name]+offsets[name])
            self.add_fixed_orientation_mobjects(lab)
            labs.add(lab)
        return labs

    def show_cube(self, dim=False, base_fill=0.05, top_fill=0.025):
        G=self.cube(dim=dim,base_fill=base_fill,top_fill=top_fill)
        self.add(G["base"],G["top"],G["edges"],G["dots"])
        self.cube_labels(G)
        return G
    # ======================================================
    # REGULAR TETRAHEDRON HELPERS
    # ======================================================
    def regular_tetra_pts(self):
        a = 4.0
        return {
            "A": L(-a / 2, -a / (2 * math.sqrt(3)), 0),
            "B": L( a / 2, -a / (2 * math.sqrt(3)), 0),
            "C": L(0, a / math.sqrt(3), 0),
            "D": L(0, 0, a * math.sqrt(2 / 3)),
        }

    def regular_tetra(self, dim=False):
        p = self.regular_tetra_pts()
        vis_color = DIM if dim else EDGE
        vis_opacity = 0.40 if dim else 0.94
        vis_width = 2.4 if dim else 3.7
        hid_color = "#405A73" if dim else DIM
        hid_opacity = 0.40 if dim else 0.70
        hid_width = 2.0 if dim else 2.6

        visible = VGroup(
            solid(p["A"], p["B"], vis_color, vis_width, vis_opacity),
            solid(p["A"], p["C"], vis_color, vis_width, vis_opacity),
            solid(p["B"], p["C"], vis_color, vis_width, vis_opacity),
            solid(p["A"], p["D"], vis_color, vis_width, vis_opacity),
            solid(p["B"], p["D"], vis_color, vis_width, vis_opacity),
        )
        hidden = VGroup(
            hidden_edge(p["C"], p["D"], hid_color, hid_width, hid_opacity),
        )
        base = face(p["A"], p["B"], p["C"], color=BLUE, opacity=0.055, stroke_width=0)
        side = face(p["A"], p["B"], p["D"], color=PURPLE, opacity=0.025, stroke_width=0)
        dots = VGroup(*[Dot3D(p[k], radius=0.052, color=GOLD if k != "D" else RED) for k in p])
        return {"p": p, "visible": visible, "hidden": hidden, "edges": VGroup(visible, hidden), "base": base, "side": side, "dots": dots}

    def regular_tetra_labels(self, G):
        p = G["p"]
        offsets = {
            "A": np.array([-0.18, -0.16, -0.04]),
            "B": np.array([ 0.17, -0.15, -0.03]),
            "C": np.array([ 0.16,  0.13,  0.04]),
            "D": np.array([-0.13,  0.00,  0.16]),
        }
        labs = VGroup()
        for name in ["A", "B", "C", "D"]:
            lab = mty(name, 24, RED if name == "D" else GOLD)
            lab.move_to(p[name] + offsets[name])
            self.add_fixed_orientation_mobjects(lab)
            labs.add(lab)
        return labs

    def show_regular_tetra(self, dim=False):
        G = self.regular_tetra(dim=dim)
        self.add(G["base"], G["side"], G["edges"], G["dots"])
        self.regular_tetra_labels(G)
        return G

    # ======================================================
    # RIGHT TETRAHEDRON HELPERS
    # ======================================================
    def right_tetra_pts(self, bx=4.6, by=3.3, dz=4.1):
        return {
            "A": L(-1.7, -1.25, 0),
            "B": L(-1.7 + bx, -1.25, 0),
            "C": L(-1.7, -1.25 + by, 0),
            "D": L(-1.7, -1.25, dz),
        }

    def right_tetra(self, dim=False, bx=4.6, by=3.3, dz=4.1):
        p = self.right_tetra_pts(bx=bx, by=by, dz=dz)
        vis_color = DIM if dim else EDGE
        vis_opacity = 0.42 if dim else 0.94
        vis_width = 2.4 if dim else 3.7
        hid_color = "#405A73" if dim else DIM
        hid_opacity = 0.40 if dim else 0.68
        hid_width = 2.0 if dim else 2.6

        visible = VGroup(
            solid(p["A"], p["B"], vis_color, vis_width, vis_opacity),
            solid(p["A"], p["C"], vis_color, vis_width, vis_opacity),
            solid(p["A"], p["D"], vis_color, vis_width, vis_opacity),
            solid(p["B"], p["C"], vis_color, vis_width, vis_opacity),
            solid(p["B"], p["D"], vis_color, vis_width, vis_opacity),
        )
        hidden = VGroup(hidden_edge(p["C"], p["D"], hid_color, hid_width, hid_opacity))
        plane = face(p["A"], p["C"], p["D"], color=BLUE, opacity=0.08, stroke_width=0)
        dots = VGroup(*[Dot3D(p[k], radius=0.052, color=GOLD if k != "B" else ORANGE) for k in p])
        return {"p": p, "visible": visible, "hidden": hidden, "edges": VGroup(visible, hidden), "plane": plane, "dots": dots}

    def right_tetra_labels(self, G):
        p = G["p"]
        offsets = {
            "A": np.array([-0.18, -0.17, -0.04]),
            "B": np.array([ 0.18, -0.13, -0.03]),
            "C": np.array([ 0.17,  0.12,  0.04]),
            "D": np.array([-0.13, -0.05,  0.16]),
        }
        labs = VGroup()
        for name in ["A", "B", "C", "D"]:
            lab = mty(name, 24, ORANGE if name == "B" else GOLD)
            lab.move_to(p[name] + offsets[name])
            self.add_fixed_orientation_mobjects(lab)
            labs.add(lab)
        return labs

    def show_right_tetra(self, dim=False, bx=4.6, by=3.3, dz=4.1):
        G = self.right_tetra(dim=dim, bx=bx, by=by, dz=dz)
        self.add(G["plane"], G["edges"], G["dots"])
        self.right_tetra_labels(G)
        return G


    # ======================================================
    # VIDEO 05 MODELS
    # ======================================================
    def wedge_model(self, theta=58 * DEGREES, dim=False):
        """Abstract dihedral wedge with common edge parallel to Ox."""
        x0, x1 = -2.8, 2.8
        depth = 2.25
        c, ss = math.cos(theta), math.sin(theta)
        A = L(x0, 0, 0)
        B = L(x1, 0, 0)
        G1 = L(x0, -depth, 0)
        G2 = L(x1, -depth, 0)
        U1 = L(x0, -depth * c, depth * ss)
        U2 = L(x1, -depth * c, depth * ss)
        O = L(0, 0, 0)
        G = L(0, -1.65, 0)
        U = L(0, -1.65 * c, 1.65 * ss)

        lower = face(A, B, G2, G1, color=BLUE, opacity=0.14, stroke_width=0)
        upper = face(A, B, U2, U1, color=PURPLE, opacity=0.18, stroke_width=0)
        common = solid(A, B, GOLD, 6.5, 1.0)
        r1 = solid(O, G, CYAN, 5.4, 1.0)
        r2 = solid(O, U, GREEN, 5.4, 1.0)
        arc = arc_basis(O, G - O, U - O, theta, radius=0.58, color=GOLD, width=6)
        return {
            "lower": lower, "upper": upper, "common": common,
            "r1": r1, "r2": r2, "arc": arc,
            "A": A, "B": B, "O": O, "G": G, "U": U,
        }

    def regular_square_pyramid(self, h=3.0, dim=False, base_fill=0.075):
        p = {
            "A": L(-2, -2, 0), "B": L(2, -2, 0),
            "C": L(2, 2, 0), "D": L(-2, 2, 0),
            "O": L(0, 0, 0), "S": L(0, 0, h),
            "M": L(0, -2, 0),
        }
        vis_color = DIM if dim else EDGE
        vis_opacity = 0.42 if dim else 0.94
        vis_width = 2.5 if dim else 3.8
        hid_color = "#405A73" if dim else DIM
        hid_opacity = 0.42 if dim else 0.68
        hid_width = 2.0 if dim else 2.6
        visible = VGroup(
            solid(p["A"], p["B"], vis_color, vis_width, vis_opacity),
            solid(p["B"], p["C"], vis_color, vis_width, vis_opacity),
            solid(p["S"], p["A"], vis_color, vis_width, vis_opacity),
            solid(p["S"], p["B"], vis_color, vis_width, vis_opacity),
            solid(p["S"], p["C"], vis_color, vis_width, vis_opacity),
        )
        hidden = VGroup(
            hidden_edge(p["C"], p["D"], hid_color, hid_width, hid_opacity),
            hidden_edge(p["D"], p["A"], hid_color, hid_width, hid_opacity),
            hidden_edge(p["S"], p["D"], hid_color, hid_width, hid_opacity),
        )
        base = face(p["A"], p["B"], p["C"], p["D"], color=BLUE, opacity=base_fill, stroke_width=0)
        dots = VGroup(*[
            Dot3D(p[k], radius=0.052, color=(RED if k == "S" else GOLD))
            for k in ["A", "B", "C", "D", "S"]
        ])
        return {"p": p, "base": base, "visible": visible, "hidden": hidden, "edges": VGroup(visible, hidden), "dots": dots}

    def regular_square_labels(self, G, extra=("O", "M")):
        p = G["p"]
        offsets = {
            "A": np.array([-0.18,-0.16,-0.04]), "B": np.array([0.17,-0.15,-0.03]),
            "C": np.array([0.17,0.13,0.03]), "D": np.array([-0.18,0.13,0.03]),
            "S": np.array([-0.12,0.00,0.16]), "O": np.array([0.10,0.10,0.02]),
            "M": np.array([0.10,-0.14,0.02]),
        }
        labs=VGroup()
        for name in ["A","B","C","D","S"] + list(extra):
            if name not in p:
                continue
            lab=mty(name,23,RED if name=="S" else GOLD)
            lab.move_to(p[name]+offsets[name])
            self.add_fixed_orientation_mobjects(lab)
            labs.add(lab)
        return labs

    def show_regular_square_pyramid(self, h=3.0, dim=False, base_fill=0.075, extra=("O","M")):
        G=self.regular_square_pyramid(h=h,dim=dim,base_fill=base_fill)
        self.add(G["base"],G["edges"],G["dots"])
        self.regular_square_labels(G,extra=extra)
        return G

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        series = txt("HHKG CHUYÊN SÂU · 05", 18, BLUE, BOLD)
        title = txt("GÓC NHỊ DIỆN CHUYÊN SÂU", 44, INK, BOLD)
        sub = txt("Mặt cắt vuông góc · chóp đều · tứ diện đều · điểm động · bài ngược", 25, CYAN, BOLD)
        line = Line(LEFT*2.25, RIGHT*2.25, color=GOLD, stroke_width=3.2)
        note = txt("Không đo góc bằng mắt — luôn dựng đúng mặt phẳng vuông góc cạnh chung", 22, MUTED)
        brand = txt(TEN_THAY, 18, MUTED)
        g = VGroup(series, line, title, sub, note, brand).arrange(DOWN, buff=0.22)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g, shift=UP*0.08), run_time=0.9)
        self.narrate(
            "Chào các em. Video năm đi sâu vào một trong những phần dễ sai nhất của hình học không gian: góc nhị diện. Khó khăn không nằm ở công thức lượng giác, mà nằm ở việc chọn đúng hai tia để đo góc. Hai mặt phẳng có thể nhìn rất rõ trên hình, nhưng nếu ta chọn hai đường tùy ý nằm trên hai mặt thì góc thu được hầu như không có ý nghĩa. Trong video này, thầy sẽ bắt đầu từ định nghĩa hình học, biến góc nhị diện thành một góc phẳng bằng mặt cắt vuông góc cạnh chung, rồi áp dụng vào hình chóp vuông, chóp đều, tứ diện đều, hình lập phương, một bài có tham số động và một mô hình thực tế. Mục tiêu cuối cùng là các em nhìn cấu hình và biết ngay phải cắt ở đâu.",
            2.0,
        )

    # ======================================================
    # 1. DEFINITION BY PERPENDICULAR CROSS-SECTION
    # ======================================================
    def definition_scene(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.98)
        self.add_header("Bản chất của góc nhị diện", "Một cạnh chung – một mặt cắt vuông góc – một góc phẳng", "1/9")
        W = self.wedge_model(theta=58*DEGREES)
        self.add(W["lower"], W["upper"], W["common"])
        self.play(Create(W["r1"]), Create(W["r2"]), Create(W["arc"]), run_time=0.9)

        problem = self.card(
            "NGUYÊN LÝ",
            "Cắt vuông góc cạnh chung",
            [
                ("text", "Hai mặt phẳng gặp nhau theo cạnh l.", 18, INK, NORMAL),
                ("math", "l perp m", 30, CYAN),
                ("math", "l perp n", 30, GREEN),
                ("math", "phi = hat(m n, size: #145%)", 31, GOLD),
                ("sep",),
                ("text", "m và n phải nằm trong hai mặt tương ứng, tại cùng một điểm của l.", 16, MUTED, NORMAL),
            ],
            accent=GOLD,
        )
        self.narrate(
            "Ta bắt đầu từ một mô hình trừu tượng. Hai nửa mặt phẳng cùng có cạnh chung l. Chọn một điểm trên l, rồi trong mỗi mặt dựng một tia cùng vuông góc với l. Góc giữa hai tia đó chính là góc phẳng của góc nhị diện. Một cách tương đương và thường dễ dùng hơn là dựng một mặt phẳng vuông góc với l. Mặt phẳng này cắt hai mặt ban đầu theo hai đường m và n; góc giữa m và n chính là góc nhị diện. Đây là nguyên lý xuyên suốt toàn bộ video.",
            2.1,
        )
        self.narrate(
            "Điều cần tránh là chọn một đường trên mặt thứ nhất và một đường trên mặt thứ hai chỉ vì chúng trông có vẻ thuận mắt. Nếu hai đường đó không cùng vuông góc cạnh chung thì góc của chúng không phải góc nhị diện. Vì vậy thứ tự tư duy nên là: tìm cạnh chung, chọn điểm trên cạnh, dựng mặt cắt vuông góc cạnh chung, rồi mới tính góc phẳng trong mặt cắt.",
            1.8,
        )
        self.takeaway("Cạnh chung → mặt cắt vuông góc → góc phẳng")

    # ======================================================
    # 2. RIGHT SQUARE PYRAMID
    # ======================================================
    def right_pyramid_example(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.97)
        self.add_header("Bài 1 · Hình chóp vuông", "Góc nhị diện giữa (SBC) và đáy theo cạnh BC", "2/9")
        G = self.show_base_model(dim=False, base_fill=0.08)
        p=G["p"]
        face_sbc = face(p["S"],p["B"],p["C"],color=PURPLE,opacity=0.20,stroke_width=0)
        bc=solid(p["B"],p["C"],GOLD,6.4,1.0)
        ba=solid(p["B"],p["A"],CYAN,5.3,1.0)
        bs=solid(p["B"],p["S"],GREEN,5.3,1.0)
        beta=math.atan2(3,4)
        arc=arc_basis(p["B"],p["A"]-p["B"],p["S"]-p["B"],beta,radius=0.48)
        self.play(FadeIn(face_sbc),Create(bc),Create(ba),Create(bs),Create(arc),run_time=1.0)

        card=self.card(
            "LỜI GIẢI",
            "Dùng ngay tam giác 3–4–5",
            [
                ("math", "B A perp B C", 29, CYAN),
                ("math", "B S perp B C", 29, GREEN),
                ("math", "beta = hat(A B S, size: #145%)", 30, GOLD),
                ("math", "S B = 5", 29, INK),
                ("math", "sin beta = frac(3, 5)", 31, GOLD),
                ("math", "tan beta = frac(3, 4)", 31, GOLD),
            ],
            accent=GOLD,
        )
        self.narrate(
            "Xét lại hình chóp S.ABCD có đáy là hình vuông cạnh bốn, SA bằng ba và vuông góc đáy. Ta cần góc nhị diện giữa mặt SBC và mặt đáy theo cạnh BC. Trong đáy, BA vuông góc BC. Mặt khác, BC song song AD; mà AD vuông góc cả AB lẫn SA nên AD vuông góc mặt SAB. Suy ra BC cũng vuông góc mặt SAB, đặc biệt BC vuông góc BS. Vì vậy hai tia BA và BS chính là hai tia của mặt cắt vuông góc cạnh chung BC.",
            2.1,
        )
        self.narrate(
            "Góc nhị diện cần tìm là góc ABS. Tam giác SAB vuông tại A, có SA bằng ba, AB bằng bốn nên SB bằng năm. Ta đọc ngay sin beta bằng ba phần năm và tang beta bằng ba phần bốn. Điểm đáng nhớ không phải bộ số ba bốn năm, mà là cách dựng: cạnh chung là BC, và ta chủ động tìm hai đường BA, BS cùng vuông góc BC.",
            1.8,
        )
        self.takeaway("Nhìn cạnh chung trước, lượng giác sau")

    # ======================================================
    # 3. REGULAR SQUARE PYRAMID
    # ======================================================
    def regular_pyramid_example(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.97)
        self.add_header("Bài 2 · Hình chóp đều", "Một mặt cắt chuẩn dùng được cho mọi mặt bên", "3/9")
        h=2*math.sqrt(2)
        G=self.show_regular_square_pyramid(h=h,base_fill=0.08)
        p=G["p"]
        side=face(p["S"],p["A"],p["B"],color=PURPLE,opacity=0.20,stroke_width=0)
        ab=solid(p["A"],p["B"],GOLD,6.2,1.0)
        om=solid(p["O"],p["M"],CYAN,5.0,1.0)
        sm=solid(p["S"],p["M"],GREEN,5.0,1.0)
        so=aux(p["S"],p["O"],ORANGE,3.8,0.9)
        theta=math.atan2(h,2)
        arc=arc_basis(p["M"],p["O"]-p["M"],p["S"]-p["M"],theta,radius=0.47)
        self.play(FadeIn(side),Create(ab),Create(om),Create(sm),Create(so),Create(arc),run_time=1.0)

        card=self.card(
            "LỜI GIẢI",
            "Trung điểm cạnh đáy là chìa khóa",
            [
                ("math", "O M perp A B", 28, CYAN),
                ("math", "S M perp A B", 28, GREEN),
                ("math", "phi = hat(O M S, size: #145%)", 30, GOLD),
                ("math", "O M = frac(a, 2)", 29, INK),
                ("math", "tan phi = frac(S O, O M) = frac(2 h, a)", 29, GOLD),
                ("math", "a = 4, h = 2 sqrt(2)", 26, INK),
                ("math", "tan phi = sqrt(2)", 30, GOLD),
            ],
            accent=PURPLE,
        )
        self.narrate(
            "Bây giờ xét hình chóp đều S.ABCD, đáy là hình vuông cạnh a, tâm O và SO bằng h. Ta tìm góc nhị diện giữa mặt SAB và đáy theo cạnh AB. Với chóp đều, hãy nghĩ ngay tới trung điểm M của cạnh AB. Trong hình vuông, đoạn OM vuông góc AB. Trong tam giác cân SAB, đường trung tuyến SM cũng vuông góc AB. Vì vậy mặt phẳng SOM chính là mặt cắt vuông góc cạnh chung AB.",
            2.0,
        )
        self.narrate(
            "Góc nhị diện trở thành góc OMS. Tam giác SOM vuông tại O, trong đó OM bằng a trên hai và SO bằng h. Vì thế tang phi bằng SO chia OM, tức bằng hai h trên a. Công thức này rất mạnh: với mọi chóp tứ giác đều, chỉ cần biết chiều cao và cạnh đáy là ta có ngay góc nhị diện giữa một mặt bên và đáy. Trong ví dụ a bằng bốn và h bằng hai căn hai, tang phi bằng căn hai.",
            2.0,
        )
        self.takeaway("Chóp đều: tâm đáy + trung điểm cạnh → mặt cắt chuẩn")

    # ======================================================
    # 4. REGULAR TETRAHEDRON DIHEDRAL ANGLE
    # ======================================================
    def tetrahedron_example(self):
        self.clear_all()
        self.set_camera_orientation(phi=69*DEGREES,theta=-52*DEGREES,zoom=0.98)
        self.add_header("Bài 3 · Tứ diện đều", "Một hằng số đẹp của hình học không gian", "4/9")
        G=self.show_regular_tetra(dim=False)
        p=G["p"]
        M=(p["A"]+p["B"])/2
        md=solid(M,p["D"],GREEN,5.1,1.0)
        mc=solid(M,p["C"],CYAN,5.1,1.0)
        ab=solid(p["A"],p["B"],GOLD,6.1,1.0)
        dot=Dot3D(M,radius=0.052,color=GOLD)
        mlab=mty("M",22,GOLD).move_to(M+np.array([0.10,-0.12,0.03]))
        self.add_fixed_orientation_mobjects(mlab)
        # actual angle at M between MC and MD
        u=(p["C"]-M)/np.linalg.norm(p["C"]-M)
        v=(p["D"]-M)/np.linalg.norm(p["D"]-M)
        ang=math.acos(float(np.clip(np.dot(u,v),-1,1)))
        arc=arc_basis(M,u,v,ang,radius=0.44)
        self.play(Create(ab),FadeIn(dot),Create(mc),Create(md),Create(arc),run_time=1.0)

        card=self.card(
            "LỜI GIẢI",
            "Góc nhị diện của tứ diện đều",
            [
                ("math", "M C perp A B", 28, CYAN),
                ("math", "M D perp A B", 28, GREEN),
                ("math", "theta = hat(C M D, size: #145%)", 30, GOLD),
                ("math", "M C = M D = frac(a sqrt(3), 2)", 28, INK),
                ("math", "C D = a", 28, INK),
                ("math", "cos theta = frac(1, 3)", 33, GOLD),
            ],
            accent=GOLD,
        )
        self.narrate(
            "Một cấu hình rất đẹp là tứ diện đều ABCD cạnh a. Ta xét góc nhị diện giữa hai mặt ABC và ABD theo cạnh AB. Gọi M là trung điểm AB. Vì ABC và ABD đều là tam giác đều, hai đường trung tuyến MC và MD đồng thời vuông góc AB. Do đó góc nhị diện cần tìm chính là góc CMD. Bài toán không gian đã được đưa hoàn toàn về tam giác CMD.",
            2.0,
        )
        self.narrate(
            "Trong tam giác đều cạnh a, trung tuyến có độ dài a căn ba trên hai, nên MC bằng MD bằng a căn ba trên hai; còn CD bằng a. Áp dụng định lý cosin cho tam giác CMD, ta được cos theta bằng một phần ba. Đây là một hằng số đặc trưng của tứ diện đều: góc nhị diện trong của hai mặt kề có cos bằng một phần ba. Kết quả này rất đáng nhớ, nhưng quan trọng hơn là cách dựng trung điểm cạnh chung để tạo mặt cắt vuông góc.",
            2.0,
        )
        self.takeaway("Tứ diện đều: trung điểm cạnh chung biến nhị diện thành tam giác cân")

    # ======================================================
    # 5. CUBE OBLIQUE PLANE VS BASE
    # ======================================================
    def cube_example(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.97)
        self.add_header("Bài 4 · Hình lập phương", "Mặt phẳng chéo và mặt đáy", "5/9")
        G=self.show_cube(dim=False,base_fill=0.05,top_fill=0.015)
        p=G["p"]
        O=(p["B"]+p["D"])/2
        plane=face(p["A1"],p["B"],p["D"],color=PURPLE,opacity=0.20,stroke_width=0)
        bd=aux(p["B"],p["D"],GOLD,4.2,0.95)
        oa=solid(O,p["A"],CYAN,5.0,1.0)
        oa1=solid(O,p["A1"],GREEN,5.0,1.0)
        aa1=solid(p["A"],p["A1"],ORANGE,4.2,0.95)
        dot=Dot3D(O,radius=0.05,color=GOLD)
        olab=mty("O",22,GOLD).move_to(O+np.array([0.10,0.08,0.03]))
        self.add_fixed_orientation_mobjects(olab)
        # angle A O A'
        u=(p["A"]-O)/np.linalg.norm(p["A"]-O)
        v=(p["A1"]-O)/np.linalg.norm(p["A1"]-O)
        ang=math.acos(float(np.clip(np.dot(u,v),-1,1)))
        arc=arc_basis(O,u,v,ang,radius=0.45)
        self.play(FadeIn(plane),Create(bd),FadeIn(dot),Create(oa),Create(oa1),Create(aa1),Create(arc),run_time=1.0)

        card=self.card(
            "LỜI GIẢI",
            "Giao tuyến BD quyết định mặt cắt",
            [
                ("math", "(A' B D) inter (A B C D) = B D", 26, GOLD),
                ("math", "O A perp B D", 28, CYAN),
                ("math", "O A' perp B D", 28, GREEN),
                ("math", "beta = hat(A O A', size: #145%)", 29, GOLD),
                ("math", "O A = frac(a, sqrt(2))", 28, INK),
                ("math", "tan beta = frac(A A', O A) = sqrt(2)", 29, GOLD),
            ],
            accent=PURPLE,
        )
        self.narrate(
            "Trong hình lập phương, xét mặt phẳng A phẩy B D và mặt đáy ABCD. Hai mặt cắt nhau theo đường chéo BD. Gọi O là tâm hình vuông đáy. Đường OA nằm trong đáy và vuông góc BD. Ta cũng có OA phẩy vuông góc BD: thành phần ngang của OA phẩy chính là OA, còn cạnh AA phẩy vuông góc mặt đáy nên vuông góc BD. Vì vậy góc giữa OA và OA phẩy chính là góc nhị diện của hai mặt.",
            2.0,
        )
        self.narrate(
            "Tam giác AOA phẩy vuông tại A. Nửa đường chéo OA bằng a trên căn hai, còn AA phẩy bằng a. Do đó tang beta bằng AA phẩy chia OA, bằng căn hai. Cấu hình này cho thấy khi cạnh chung là một đường chéo, điểm tâm của hình vuông thường là vị trí rất tốt để dựng mặt cắt vuông góc.",
            1.8,
        )
        self.takeaway("Cạnh chung là đường chéo → nghĩ tới tâm và đường chéo còn lại")

    # ======================================================
    # 6. DYNAMIC PARAMETER IN REGULAR SQUARE PYRAMID
    # ======================================================
    def dynamic_parameter(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES,theta=-54*DEGREES,zoom=0.97)
        self.add_header("Bài 5 · Điểm động theo chiều cao", "Góc nhị diện tăng thế nào khi đỉnh nâng lên?", "6/9")
        h=ValueTracker(1.2)
        # fixed base
        p0=self.regular_square_pyramid(h=1.2)["p"]
        base=face(p0["A"],p0["B"],p0["C"],p0["D"],color=BLUE,opacity=0.075,stroke_width=0)
        base_edges=VGroup(
            solid(p0["A"],p0["B"],EDGE,3.8,0.94), solid(p0["B"],p0["C"],EDGE,3.8,0.94),
            hidden_edge(p0["C"],p0["D"],DIM,2.6,0.68), hidden_edge(p0["D"],p0["A"],DIM,2.6,0.68),
        )
        self.add(base,base_edges)
        for name,pt in [("A",p0["A"]),("B",p0["B"]),("C",p0["C"]),("D",p0["D"]),("O",p0["O"]),("M",p0["M"])]:
            lab=mty(name,22,GOLD).move_to(pt+np.array([0.10,-0.10,0.03]))
            self.add_fixed_orientation_mobjects(lab)
        def Spt(): return L(0,0,h.get_value())
        side_edges=always_redraw(lambda: VGroup(
            solid(Spt(),p0["A"],EDGE,3.2,0.90),solid(Spt(),p0["B"],EDGE,3.2,0.90),
            solid(Spt(),p0["C"],EDGE,3.2,0.90),hidden_edge(Spt(),p0["D"],DIM,2.5,0.65),
        ))
        so=always_redraw(lambda: aux(Spt(),p0["O"],ORANGE,3.5,0.90))
        sm=always_redraw(lambda: solid(Spt(),p0["M"],GREEN,5.0,1.0))
        om=solid(p0["O"],p0["M"],CYAN,5.0,1.0)
        sdot=always_redraw(lambda: Dot3D(Spt(),radius=0.06,color=RED))
        slab=always_redraw(lambda: mty("S",22,RED).move_to(Spt()+np.array([-0.12,0,0.15])))
        self.add(side_edges,so,sm,om,sdot)
        self.add_fixed_orientation_mobjects(slab)

        # dynamic fixed-frame math readout using Text to avoid per-frame Typst compilation
        readout=always_redraw(lambda: VGroup(
            txt(f"h = {h.get_value():.2f}",17,ORANGE,BOLD),
            txt(f"tan φ = {h.get_value()/2:.2f}",17,GOLD,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.08).move_to(RIGHT*4.25+DOWN*1.95))
        self.add_fixed_in_frame_mobjects(readout)

        card=self.card(
            "THAM SỐ",
            "Giữ cạnh đáy a = 4",
            [
                ("math", "O M = 2", 29, CYAN),
                ("math", "tan phi = frac(h, 2)", 31, GOLD),
                ("text", "h tăng  ⇒  tan φ tăng  ⇒  φ tăng.", 17, INK, NORMAL),
                ("sep",),
                ("text", "Nếu tan φ = √3 thì:", 17, MUTED, NORMAL),
                ("math", "frac(h, 2) = sqrt(3)", 29, INK),
                ("math", "h = 2 sqrt(3)", 32, GOLD),
            ],
            accent=GREEN,
        )
        self.narrate_play(
            "Giữ hình vuông đáy cạnh bốn và nâng đỉnh S lên cao dần. Trung điểm M của AB và tâm O không đổi, nên OM luôn bằng hai. Mặt cắt SOM vẫn là mặt cắt chuẩn cho góc nhị diện. Ta có tang phi bằng h chia hai. Vì vậy khi chiều cao h tăng, tang phi tăng và chính góc nhị diện cũng tăng. Trên hình, cạnh bên dựng đứng dần lên và mặt bên dốc hơn rõ rệt.",
            h.animate.set_value(4.8),
            min_time=5.2,
        )
        self.narrate_play(
            "Bài ngược cũng rất gọn. Nếu đề cho góc nhị diện có tang bằng căn ba, ta không cần dựng lại từ đầu: h trên hai bằng căn ba, nên h bằng hai căn ba. Đây là một ví dụ quan trọng về việc biến hình học không gian thành một quan hệ tham số đơn giản sau khi đã tìm đúng mặt cắt.",
            h.animate.set_value(2*math.sqrt(3)),
            min_time=4.3,
        )
        self.takeaway("Sau khi có mặt cắt chuẩn, bài tham số chỉ còn là lượng giác phẳng")

    # ======================================================
    # 7. REAL-WORLD RAMP
    # ======================================================
    def practical_ramp(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES,theta=-52*DEGREES,zoom=0.98)
        self.add_header("Bài 6 · Mô hình thực tế", "Mặt dốc và mặt đất tạo một góc nhị diện", "7/9")
        # Ground and ramp share front edge AB along x.
        A=L(-2.7,-1.7,0); B=L(2.7,-1.7,0)
        C=L(2.7,2.3,0); D=L(-2.7,2.3,0)
        C1=L(2.7,2.3,1.5); D1=L(-2.7,2.3,1.5)
        ground=face(A,B,C,D,color=BLUE,opacity=0.11,stroke_width=0)
        ramp=face(A,B,C1,D1,color=PURPLE,opacity=0.22,stroke_width=0)
        edge=solid(A,B,GOLD,6.3,1.0)
        M=(A+B)/2; N=(C+D)/2; N1=(C1+D1)/2
        mn=solid(M,N,CYAN,5.0,1.0)
        mn1=solid(M,N1,GREEN,5.0,1.0)
        rise=solid(N,N1,ORANGE,4.2,0.95)
        ang=math.atan2(1.5,4.0)
        arc=arc_basis(M,N-M,N1-M,ang,radius=0.47)
        self.add(ground,ramp)
        self.play(Create(edge),Create(mn),Create(mn1),Create(rise),Create(arc),run_time=1.0)

        card=self.card(
            "MÔ HÌNH",
            "Đường dốc dài theo phương ngang 4 m",
            [
                ("text", "Độ cao cuối dốc: 1,5 m", 17, INK, NORMAL),
                ("math", "M N = 4", 28, CYAN),
                ("math", "N N_1 = 1.5", 28, ORANGE),
                ("math", "alpha = hat(N M N_1, size: #145%)", 29, GOLD),
                ("math", "tan alpha = frac(1.5, 4) = frac(3, 8)", 29, GOLD),
                ("text", "Chiều dài theo cạnh chung không ảnh hưởng góc dốc.", 16, MUTED, NORMAL),
            ],
            accent=CYAN,
        )
        self.narrate(
            "Một mô hình thực tế rất tự nhiên là mặt dốc của một ram dốc gặp mặt đất theo một cạnh thẳng. Muốn đo độ dốc, ta không cần quan tâm mặt dốc dài bao nhiêu theo cạnh chung. Ta cắt công trình bởi một mặt phẳng vuông góc cạnh chung. Trong mặt cắt đó, phương ngang dài bốn mét và độ nâng cao là một phẩy năm mét. Góc nhị diện trở thành góc của một tam giác vuông đơn giản.",
            2.0,
        )
        self.narrate(
            "Vì vậy tang alpha bằng một phẩy năm chia bốn, bằng ba phần tám. Kết quả cho thấy một đặc điểm quan trọng của góc nhị diện trong các mô hình mái, ram dốc hay tấm nghiêng: kích thước dọc theo cạnh chung không ảnh hưởng góc; chỉ mặt cắt vuông góc cạnh đó mới quyết định độ dốc. Đây chính là lý do kỹ thuật dùng mặt cắt vuông góc hiệu quả cả trong toán học lẫn thiết kế thực tế.",
            1.9,
        )
        self.takeaway("Mô hình 3D → cắt vuông góc cạnh bản lề → tam giác 2D")

    # ======================================================
    # COMMON MISTAKES
    # ======================================================
    def mistakes(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Những lỗi rất dễ mất điểm", "Góc nhị diện sai thường vì dựng sai, không phải vì tính sai", "8/9")
        items=VGroup(
            VGroup(txt("01",18,RED,BOLD),txt("Chọn hai đường bất kỳ trên hai mặt.",22,INK,BOLD),txt("→ phải cùng vuông góc cạnh chung.",18,CYAN)).arrange(DOWN,aligned_edge=LEFT,buff=0.06),
            VGroup(txt("02",18,RED,BOLD),txt("Hai đường vuông góc cạnh chung nhưng tại hai điểm khác nhau.",22,INK,BOLD),txt("→ cần cùng xuất phát từ một điểm trên cạnh chung.",18,CYAN)).arrange(DOWN,aligned_edge=LEFT,buff=0.06),
            VGroup(txt("03",18,RED,BOLD),txt("Nhầm góc giữa hai mặt với góc giữa hai đường pháp tuyến.",22,INK,BOLD),txt("→ phải kiểm tra quy ước góc cần lấy và cấu hình cụ thể.",18,CYAN)).arrange(DOWN,aligned_edge=LEFT,buff=0.06),
            VGroup(txt("04",18,RED,BOLD),txt("Bấm máy tìm số đo góc quá sớm.",22,INK,BOLD),txt("→ giữ sin, cos, tan chính xác nếu đề không yêu cầu độ.",18,CYAN)).arrange(DOWN,aligned_edge=LEFT,buff=0.06),
            VGroup(txt("05",18,RED,BOLD),txt("Thấy chóp đều nhưng quên trung điểm cạnh đáy.",22,INK,BOLD),txt("→ tâm đáy + trung điểm cạnh thường tạo mặt cắt chuẩn.",18,CYAN)).arrange(DOWN,aligned_edge=LEFT,buff=0.06),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.26).move_to(ORIGIN+DOWN*0.05)
        fit_width(items,11.9)
        self.add_fixed_in_frame_mobjects(items)
        self.play(LaggedStart(*[FadeIn(x,shift=RIGHT*0.08) for x in items],lag_ratio=0.12),run_time=1.3)
        self.narrate(
            "Trước khi kết thúc, thầy chốt năm lỗi thường gặp. Một, chọn hai đường bất kỳ trên hai mặt. Hai, hai đường có vuông góc cạnh chung nhưng lại xuất phát tại hai điểm khác nhau. Ba, dùng công thức liên quan tới pháp tuyến nhưng không kiểm tra đúng góc nhị diện mà đề yêu cầu. Bốn, đổi sang số đo độ quá sớm làm lời giải dài và dễ sai. Năm, với chóp đều, quên mất bộ ba tâm đáy, trung điểm cạnh đáy và đỉnh thường tạo ngay mặt cắt vuông góc cạnh chung. Nếu tránh được năm lỗi này, phần góc nhị diện sẽ nhẹ đi rất nhiều.",
            2.2,
        )

    # ======================================================
    # SUMMARY + DEEP ROADMAP
    # ======================================================
    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Tổng kết chuyên đề", "Một quy trình đủ mạnh cho phần lớn bài góc nhị diện THPT", "9/9")
        left=VGroup(
            txt("QUY TRÌNH 5 BƯỚC",20,GOLD,BOLD),
            txt("1. Xác định cạnh chung của hai mặt.",20,INK),
            txt("2. Chọn một điểm thuận lợi trên cạnh chung.",20,INK),
            txt("3. Dựng hai đường cùng vuông góc cạnh chung.",20,INK),
            txt("4. Đưa về tam giác phẳng chứa hai đường đó.",20,INK),
            txt("5. Tính sin, cos hoặc tan trước khi tìm số đo góc.",20,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.22).move_to(LEFT*2.9+UP*0.15)
        right=VGroup(
            txt("CÁC KẾT QUẢ ĐẸP",20,CYAN,BOLD),
            mty("tan phi = frac(2 h, a)",28,GOLD),
            mty("cos theta = frac(1, 3)",29,GOLD),
            mty("tan beta = sqrt(2)",29,GOLD),
            mty("tan alpha = frac(3, 8)",29,GOLD),
            txt("Chóp đều · tứ diện đều · lập phương · mô hình dốc",17,MUTED),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.24).move_to(RIGHT*3.0+UP*0.15)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left),FadeIn(right),run_time=0.9)
        self.narrate(
            "Toàn bộ chuyên đề có thể nén thành năm bước. Xác định cạnh chung. Chọn điểm thuận lợi trên cạnh. Dựng trong mỗi mặt một đường vuông góc cạnh chung. Đưa hai đường đó vào cùng một tam giác hoặc một mặt cắt phẳng. Cuối cùng mới dùng lượng giác. Qua sáu bài, ta đã gặp từ chóp vuông, chóp đều, tứ diện đều, hình lập phương tới mô hình mặt dốc và bài tham số. Nếu các em có thể tự chỉ ra mặt cắt vuông góc trong từng hình mà chưa cần nhìn lời giải, thì phần quan trọng nhất của góc nhị diện đã được nắm chắc.",
            2.1,
        )
        roadmap=VGroup(
            txt("CHẶNG TIẾP THEO CỦA SERIES",19,GOLD,BOLD),
            txt("06 · Thể tích & tỷ số thể tích I",18,MUTED),
            txt("07 · Tỷ số thể tích nâng cao & biến đổi tứ diện",18,MUTED),
            txt("08 · Thiết diện I – dựng đúng giao tuyến",18,MUTED),
            txt("09 · Thiết diện II – diện tích, tỷ số, cực trị",18,MUTED),
            txt("10 · Nón · trụ · cầu · chóp cụt · mô hình lạ",18,MUTED),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.12).to_edge(DOWN,buff=0.32)
        self.add_fixed_in_frame_mobjects(roadmap)
        self.play(FadeIn(roadmap),run_time=0.6)
        self.narrate(
            "Từ video sáu, series chuyển sang thể tích và tỷ số thể tích, rồi thiết diện, các khối tròn xoay, điểm động, cực trị hình học không gian, mô hình thực tế và cuối cùng là các đề tổng hợp phân hóa cao. Các phần sau vẫn giữ nguyên nguyên tắc: dựng hình chuẩn, giải thích vì sao chọn đường phụ, và ưu tiên một lời giải có cấu trúc thay vì nhiều mẹo rời rạc.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.definition_scene()
        self.right_pyramid_example()
        self.regular_pyramid_example()
        self.tetrahedron_example()
        self.cube_example()
        self.dynamic_parameter()
        self.practical_ramp()
        self.mistakes()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_05_goc_nhi_dien_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst)")
    print("Series: HHKG Chuyen Sau 05 - Goc nhi dien chuyen sau")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_05.wav"
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
    render_full()

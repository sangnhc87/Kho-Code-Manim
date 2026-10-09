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
# HHKG CHUYEN SAU 04 - MANIM + TYPST - MASTER TEMPLATE
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


_FORBIDDEN_TYPST_WORDS = {"sect", "intersect"}


def validate_typst_expr(s):
    """Fail early on known-invalid Typst math tokens used in this series."""
    words = set(s.replace("(", " " ).replace(")", " " ).replace(",", " " ).split())
    bad = sorted(words & _FORBIDDEN_TYPST_WORDS)
    if bad:
        raise ValueError(
            f"Forbidden Typst math token(s) {bad} in {s!r}. "
            "Use 'inter' for intersection."
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
        series = txt("HHKG CHUYÊN SÂU · 04", 15, BLUE, BOLD)
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
    # INTRO
    # ======================================================

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        series = txt("HHKG CHUYÊN SÂU · 04", 18, BLUE, BOLD)
        title = txt("GÓC TRONG KHÔNG GIAN", 44, INK, BOLD)
        sub = txt("Hai đường · đường–mặt · hai mặt · điểm động", 27, CYAN, BOLD)
        line = Line(LEFT*2.2, RIGHT*2.2, color=GOLD, stroke_width=3.2)
        note = txt("Một chuyên đề nền tảng trước khi đi sâu vào góc nhị diện", 23, MUTED)
        brand = txt(TEN_THAY, 18, MUTED)
        g = VGroup(series, line, title, sub, note, brand).arrange(DOWN, buff=0.22)
        self.add_fixed_in_frame_mobjects(g)
        self.play(FadeIn(g, shift=UP*0.08), run_time=0.9)
        self.narrate(
            "Chào các em. Video bốn của series hình học không gian chuyên sâu tập trung vào một chủ đề tưởng quen nhưng rất dễ nhầm: góc trong không gian. Ta sẽ không học ba công thức rời rạc. Thầy muốn các em thấy một nguyên tắc thống nhất: muốn đo góc trong không gian, ta phải đưa hai hướng cần so sánh về cùng một mặt phẳng thích hợp. Với hai đường chéo nhau, ta tìm hướng song song hoặc chứng minh vuông góc qua một mặt phẳng. Với đường và mặt, ta tìm hình chiếu của đường lên mặt. Với hai mặt, ta tìm giao tuyến rồi chọn hai đường cùng vuông góc giao tuyến. Cuối video, ta còn xét một điểm động để thấy góc thay đổi thế nào mà không cần tính số đo bằng máy.",
            2.0,
        )

    # ======================================================
    # METHOD MAP
    # ======================================================
    def method_map(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_header("Bản đồ phương pháp", "Ba loại góc – một tư duy chung", "1/8")
        boxes = VGroup()
        data = [
            ("HAI ĐƯỜNG", "Đưa về hai hướng cắt nhau", GOLD),
            ("ĐƯỜNG – MẶT", "Tìm hình chiếu của đường lên mặt", CYAN),
            ("HAI MẶT", "Vuông góc với giao tuyến", PURPLE),
            ("ĐIỂM ĐỘNG", "Biểu diễn tan, sin hoặc cos theo tham số", GREEN),
        ]
        for head, body, col in data:
            r = Rectangle(width=5.6, height=1.15, fill_color=PANEL, fill_opacity=0.92,
                          stroke_color=GRID, stroke_width=1.0, stroke_opacity=0.45)
            h = txt(head, 18, col, BOLD)
            b = txt(body, 18, INK)
            vg = VGroup(r,h,b)
            h.move_to(r.get_left()+RIGHT*0.32+UP*0.18, aligned_edge=LEFT)
            b.move_to(r.get_left()+RIGHT*0.32+DOWN*0.18, aligned_edge=LEFT)
            boxes.add(vg)
        boxes.arrange(DOWN, buff=0.18).shift(DOWN*0.10)
        self.add_fixed_in_frame_mobjects(boxes)
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT*0.12) for x in boxes], lag_ratio=0.12), run_time=1.4)
        self.narrate(
            "Trước khi làm bài, ta khóa bốn phản xạ. Một, với hai đường, góc chỉ phụ thuộc phương của chúng, nên có thể tịnh tiến một hướng bằng đường song song để đưa về cùng một điểm. Hai, với đường và mặt, góc cần tìm là góc giữa đường đó và hình chiếu vuông góc của nó trên mặt. Ba, với hai mặt, điều quyết định là giao tuyến: trong mỗi mặt ta chọn một đường vuông góc với giao tuyến tại cùng một điểm. Bốn, khi có điểm động, đừng vội lấy arctang hay arccos. Hãy tìm một tỷ số lượng giác đơn giản theo tham số; tính đơn điệu của tỷ số thường cho ngay tính đơn điệu của góc.",
            2.0,
        )

    # ======================================================
    # EX1: CUBE - SKEW LINES HIDDEN ORTHOGONALITY
    # ======================================================
    def ex1_cube_skew_perpendicular(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Hai đường chéo nhau", "Trong hình lập phương: tìm góc giữa AC' và BD", "2/8")
        G = self.show_cube(dim=True, base_fill=0.035, top_fill=0.015)
        p = G["p"]
        O = (p["A"] + p["C"]) / 2
        O1 = (p["A1"] + p["C1"]) / 2
        plane = face(p["A"], p["C"], p["C1"], p["A1"], color=PURPLE, opacity=0.12, stroke_width=0)
        bd = solid(p["B"], p["D"], CYAN, 5.6, 0.98)
        ac1 = solid(p["A"], p["C1"], GOLD, 6.2, 1.0)
        ac = aux(p["A"], p["C"], MUTED, 3.2, 0.72)
        oo1 = aux(O, O1, GREEN, 3.6, 0.92)
        odot = Dot3D(O, radius=0.055, color=GOLD)
        o1dot = Dot3D(O1, radius=0.055, color=GREEN)
        self.play(FadeIn(plane), Create(bd), Create(ac1), Create(ac), Create(oo1), FadeIn(odot), FadeIn(o1dot), run_time=1.1)
        card1 = self.card("Đề bài", "Một cặp chéo nhau rất đặc biệt", [
            ("math", "A B C D . A' B' C' D'", 27, INK),
            ("text", "Tìm góc giữa hai đường", 18, MUTED, NORMAL),
            ("math", "A C'", 34, GOLD),
            ("math", "B D", 34, CYAN),
        ], accent=GOLD, height=4.6)
        self.narrate(
            "Trong hình lập phương, hai đường AC phẩy và BD chéo nhau nên không có một góc phẳng hiện sẵn để đo. Cách tốt hơn là nhìn một mặt phẳng chứa AC phẩy. Mặt ACC phẩy A phẩy là mặt phẳng chéo đi qua AC phẩy. Gọi O là tâm đáy và O phẩy là tâm mặt trên. Đường OO phẩy nằm trong mặt phẳng này.",
            1.8,
        )
        card2 = self.card("Lời giải", "Chứng minh BD vuông góc một mặt phẳng", [
            ("math", "B D perp A C", 28, CYAN),
            ("math", "B D perp O O'", 28, GREEN),
            ("math", "A C inter O O' = O", 27, INK),
            ("math", "B D perp (A C C' A')", 28, GOLD),
            ("text", "AC' nằm trong mặt phẳng ACC'A'.", 17, MUTED, NORMAL),
            ("math", "B D perp A C'", 33, GOLD),
            ("sep",),
            ("text", "Góc giữa hai đường bằng 90°.", 18, GREEN, BOLD),
        ], accent=CYAN, height=5.1, auto_add=False)
        self.swap_card(card1, card2)
        self.narrate(
            "Trong hình vuông ABCD, hai đường chéo AC và BD vuông góc. Mặt khác OO phẩy song song các cạnh đứng của hình lập phương nên vuông góc với mặt đáy; vì BD nằm trong đáy, BD cũng vuông góc OO phẩy. Hai đường AC và OO phẩy cắt nhau tại O và cùng nằm trong mặt ACC phẩy A phẩy. Vì BD vuông góc với hai đường cắt nhau ấy, BD vuông góc cả mặt phẳng. Do AC phẩy nằm trong mặt phẳng đó, suy ra BD vuông góc AC phẩy. Góc giữa hai đường chéo nhau bằng chín mươi độ mà không cần tính một tích vô hướng nào.",
            2.2,
        )
        self.takeaway("Bài hai đường chéo nhau: thử tìm một mặt phẳng chứa một đường và vuông góc đường kia.")

    # ======================================================
    # EX2: LINE - PLANE IN CUBE
    # ======================================================
    def ex2_cube_line_plane(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 2 · Góc đường – mặt", "Tìm góc giữa AC' và mặt đáy của hình lập phương", "3/8")
        G = self.show_cube(dim=True, base_fill=0.07, top_fill=0.015)
        p = G["p"]
        ac1 = solid(p["A"], p["C1"], GOLD, 6.2, 1.0)
        ac = aux(p["A"], p["C"], CYAN, 4.3, 0.95)
        cc1 = solid(p["C"], p["C1"], GREEN, 5.0, 0.96)
        e1 = (p["C"]-p["A"])/np.linalg.norm(p["C"]-p["A"])
        e2 = np.array([0.0,0.0,1.0])
        alpha = math.atan(1/math.sqrt(2))
        arc = arc_basis(p["A"], e1, e2, alpha, radius=0.42)
        self.play(Create(ac1), Create(ac), Create(cc1), Create(arc), run_time=1.0)
        card = self.card("Lời giải", "Hình chiếu quyết định góc", [
            ("math", "A C' -> A C", 29, CYAN),
            ("math", "alpha = hat(C' A C, size: #145%)", 30, GOLD),
            ("math", "A C = a sqrt(2)", 29, INK),
            ("math", "C C' = a", 29, INK),
            ("math", "A C' = a sqrt(3)", 29, INK),
            ("math", "tan alpha = frac(1, sqrt(2))", 31, GOLD),
            ("math", "sin alpha = frac(1, sqrt(3))", 31, GREEN),
        ], accent=CYAN, height=5.15)
        self.narrate(
            "Bây giờ vẫn là đường AC phẩy, nhưng ta hỏi góc giữa đường này và mặt đáy. C phẩy chiếu vuông góc xuống C, còn A vốn nằm trên đáy, nên hình chiếu của AC phẩy lên đáy là AC. Do đó góc cần tìm là góc C phẩy A C. Đây là bước quan trọng nhất; sau khi tìm đúng hình chiếu, bài toán trở thành tam giác vuông ACC phẩy.",
            1.8,
        )
        self.narrate(
            "Trong hình lập phương cạnh a, AC bằng a căn hai, CC phẩy bằng a và AC phẩy bằng a căn ba. Vì vậy tang alpha bằng một trên căn hai; tương đương sin alpha bằng một trên căn ba. Ta không cần tính góc ra độ. Trong bài thi, một giá trị lượng giác chính xác thường đẹp hơn và ít sai hơn một số thập phân.",
            1.8,
        )
        self.takeaway("Đường – mặt: chiếu đường xuống mặt trước, rồi mới tính góc trong tam giác phẳng.")

    # ======================================================
    # EX3: LINE - PLANE WITH NON-BASE PLANE
    # ======================================================
    def ex3_pyramid_line_plane(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 3 · Hình chiếu không nằm ở đáy", "Tìm góc giữa SC và mặt (SAB)", "4/8")
        G = self.show_base_model(dim=True, base_fill=0.045)
        p = G["p"]
        plane_sab = face(p["S"], p["A"], p["B"], color=PURPLE, opacity=0.15, stroke_width=0)
        sc = solid(p["S"], p["C"], GOLD, 6.0, 1.0)
        sb = aux(p["S"], p["B"], CYAN, 4.4, 0.96)
        cb = solid(p["C"], p["B"], GREEN, 4.8, 0.96)
        self.play(FadeIn(plane_sab), Create(sc), Create(sb), Create(cb), run_time=1.0)
        # Arc at S between SB and SC
        u = (p["B"]-p["S"]); u=u/np.linalg.norm(u)
        # plane basis direction orthogonal to u toward C component
        vc = p["C"]-p["S"]
        comp = vc - np.dot(vc,u)*u
        comp = comp/np.linalg.norm(comp)
        gamma = math.atan2(4,5)
        arc = arc_basis(p["S"], u, comp, gamma, radius=0.40)
        self.play(Create(arc), run_time=0.45)
        card = self.card("Lời giải", "Tìm chân chiếu của C lên (SAB)", [
            ("math", "C B perp A B", 28, CYAN),
            ("math", "C B perp S A", 28, GREEN),
            ("math", "C B perp (S A B)", 29, GOLD),
            ("math", "S C -> S B", 29, CYAN),
            ("math", "gamma = hat(C S B, size: #145%)", 30, GOLD),
            ("math", "S B = 5", 28, INK),
            ("math", "tan gamma = frac(4, 5)", 32, GREEN),
        ], accent=PURPLE, height=5.2)
        self.narrate(
            "Bài này quan trọng vì mặt phẳng cần chiếu không phải là mặt đáy. Ta cần tìm hình chiếu của C lên mặt SAB. Cạnh CB vuông góc AB vì đáy là hình vuông. Đồng thời SA vuông góc mặt đáy nên CB cũng vuông góc SA. Hai đường AB và SA cắt nhau trong mặt SAB, vì thế CB vuông góc mặt SAB. Vậy B chính là hình chiếu vuông góc của C lên mặt này.",
            2.0,
        )
        self.narrate(
            "S nằm sẵn trong mặt SAB, nên hình chiếu của đoạn SC chính là SB. Góc giữa SC và mặt SAB là góc CSB. Tam giác SBC vuông tại B. Ta có SB bằng năm do tam giác SAB là tam giác ba bốn năm, còn BC bằng bốn. Vì thế tang gamma bằng bốn phần năm. Điều cần học ở đây không phải con số bốn phần năm, mà là cách tìm chân chiếu bằng tiêu chuẩn một đường vuông góc với hai đường cắt nhau của mặt phẳng.",
            2.0,
        )

    # ======================================================
    # EX4: PLANE - PLANE IN CUBE
    # ======================================================
    def ex4_cube_plane_plane(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 4 · Góc giữa hai mặt phẳng", "Giữa (ACD') và mặt đáy của hình lập phương", "5/8")
        G = self.show_cube(dim=True, base_fill=0.08, top_fill=0.012)
        p = G["p"]
        O = (p["A"]+p["C"])/2
        plane = face(p["A"],p["C"],p["D1"],color=PURPLE,opacity=0.16,stroke_width=0)
        ac = solid(p["A"],p["C"],GOLD,5.5,1.0)
        od = solid(O,p["D"],CYAN,4.8,0.96)
        od1 = solid(O,p["D1"],GREEN,5.2,0.98)
        dd1 = solid(p["D"],p["D1"],MUTED,3.5,0.75)
        odot=Dot3D(O,radius=0.055,color=GOLD)
        self.play(FadeIn(plane),Create(ac),Create(od),Create(od1),Create(dd1),FadeIn(odot),run_time=1.0)
        # arc in vertical plane D O D'
        e1=(p["D"]-O); e1=e1/np.linalg.norm(e1)
        e2=np.array([0.0,0.0,1.0])
        beta=math.atan(math.sqrt(2))
        arc=arc_basis(O,e1,e2,beta,radius=0.40,color=GOLD)
        self.play(Create(arc),run_time=0.45)
        card = self.card("Lời giải", "Cùng vuông góc giao tuyến AC", [
            ("math", "(A C D') inter (A B C D) = A C", 26, GOLD),
            ("text", "O là trung điểm của AC.", 17, MUTED, NORMAL),
            ("math", "O D perp A C", 28, CYAN),
            ("math", "O D' perp A C", 28, GREEN),
            ("math", "beta = hat(D O D', size: #145%)", 29, GOLD),
            ("math", "O D = frac(a, sqrt(2))", 28, INK),
            ("math", "D D' = a", 28, INK),
            ("math", "tan beta = sqrt(2)", 32, GREEN),
        ], accent=PURPLE, height=5.25)
        self.narrate(
            "Ta chuyển sang góc giữa hai mặt phẳng. Mặt ACD phẩy và mặt đáy giao nhau theo AC. Gọi O là trung điểm AC, cũng là tâm hình vuông đáy. Trong tam giác ADC cân tại D, O là trung điểm AC nên OD vuông góc AC. Mặt khác tam giác AD phẩy C cũng cân tại D phẩy vì D phẩy A và D phẩy C đều bằng a căn hai; do đó D phẩy O cũng vuông góc AC.",
            2.0,
        )
        self.narrate(
            "Hai đường OD và OD phẩy nằm lần lượt trong hai mặt, cùng vuông góc với giao tuyến AC tại O. Vì vậy góc giữa hai mặt chính là góc D O D phẩy. Tam giác O D D phẩy vuông tại D, với OD bằng nửa đường chéo đáy, tức a trên căn hai, còn DD phẩy bằng a. Suy ra tang beta bằng căn hai. Đây là đúng cấu trúc mà video sau về góc nhị diện sẽ khai thác sâu hơn: giao tuyến trước, hai đường vuông góc sau.",
            2.1,
        )
        self.takeaway("Hai mặt: giao tuyến là trục; chọn trong mỗi mặt một đường vuông góc giao tuyến.")

    # ======================================================
    # EX5: REGULAR TETRA - OPPOSITE EDGES
    # ======================================================
    def ex5_regular_tetra_hidden_right_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 5 · Một tính chất lạ của tứ diện đều", "Hai cạnh đối thực ra vuông góc nhau", "6/8")
        G = self.show_regular_tetra(dim=True)
        p = G["p"]
        M=(p["A"]+p["B"])/2
        tri=face(M,p["C"],p["D"],color=PURPLE,opacity=0.15,stroke_width=0)
        ab=solid(p["A"],p["B"],GOLD,6.0,1.0)
        cd=hidden_edge(p["C"],p["D"],CYAN,4.5,0.95,dash=0.09)
        mc=aux(M,p["C"],GREEN,3.8,0.90)
        md=aux(M,p["D"],GREEN,3.8,0.90)
        mdot=Dot3D(M,radius=0.055,color=GOLD)
        self.play(FadeIn(tri),Create(ab),Create(cd),Create(mc),Create(md),FadeIn(mdot),run_time=1.0)
        card=self.card("Lời giải","Dùng mặt phẳng trung trực của AB",[
            ("text","M là trung điểm của AB.",17,MUTED,NORMAL),
            ("math","M C perp A B",28,GREEN),
            ("math","M D perp A B",28,GREEN),
            ("math","M C inter M D = M",27,INK),
            ("math","A B perp (M C D)",29,GOLD),
            ("text","CD nằm trong mặt phẳng (MCD).",17,CYAN,NORMAL),
            ("math","A B perp C D",33,GOLD),
            ("text","Góc giữa AB và CD bằng 90°.",18,GREEN,BOLD),
        ],accent=GOLD,height=5.15)
        self.narrate(
            "Trong tứ diện đều, hai cạnh đối AB và CD nhìn hoàn toàn không có vẻ vuông góc. Gọi M là trung điểm AB. Vì tam giác ABC đều, trung tuyến CM đồng thời là đường cao nên CM vuông góc AB. Tương tự, tam giác ABD đều nên DM vuông góc AB. Hai đường MC và MD cắt nhau tại M và nằm trong mặt MCD, vì thế AB vuông góc mặt phẳng MCD.",
            2.0,
        )
        self.narrate(
            "Cạnh CD nằm trong mặt phẳng MCD, nên AB vuông góc CD. Đây là một tính chất rất đẹp: trong tứ diện đều, mỗi cặp cạnh đối đều vuông góc nhau. Bài này cũng cho thấy một chiến lược quan trọng của góc giữa hai đường chéo nhau: thay vì cố tạo góc bằng cách tịnh tiến, đôi khi chỉ cần chứng minh một đường vuông góc với một mặt phẳng chứa đường kia.",
            1.9,
        )

    # ======================================================
    # EX6: MOVING POINT - ANGLE MONOTONICITY
    # ======================================================
    def ex6_dynamic_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 6 · Điểm động", "M chạy trên CC' – góc giữa AM và đáy thay đổi thế nào?", "7/8")
        G=self.show_cube(dim=True,base_fill=0.06,top_fill=0.012)
        p=G["p"]
        ac=aux(p["A"],p["C"],CYAN,4.0,0.92)
        self.add(ac)
        u=ValueTracker(0.12)
        Mdot=always_redraw(lambda: Dot3D(p["C"]+u.get_value()*(p["C1"]-p["C"]),radius=0.065,color=GOLD))
        AM=always_redraw(lambda: solid(p["A"],p["C"]+u.get_value()*(p["C1"]-p["C"]),GOLD,5.7,1.0))
        CM=always_redraw(lambda: solid(p["C"],p["C"]+u.get_value()*(p["C1"]-p["C"]),GREEN,4.0,0.92))
        def arc_dyn():
            e1=(p["C"]-p["A"]); e1=e1/np.linalg.norm(e1)
            ang=math.atan(u.get_value()/math.sqrt(2))
            return arc_basis(p["A"],e1,np.array([0.0,0.0,1.0]),ang,radius=0.40,color=GOLD)
        arc=always_redraw(arc_dyn)
        self.add(Mdot,AM,CM,arc)
        card=self.card("Mô hình","Không cần tính arctan",[
            ("math","C M = u a",28,GREEN),
            ("math","0 <= u <= 1",27,MUTED),
            ("math","A M -> A C",28,CYAN),
            ("math","tan theta = frac(C M, A C)",29,INK),
            ("math","tan theta = frac(u, sqrt(2))",32,GOLD),
            ("sep",),
            ("text","Khi góc bằng 30 độ:",17,MUTED,NORMAL),
            ("math","frac(u, sqrt(2)) = frac(1, sqrt(3))",28,INK),
            ("math","u = sqrt(frac(2, 3))",32,GREEN),
        ],accent=GREEN,height=5.2)
        self.narrate_play(
            "Cho M chạy từ C lên C phẩy. Hình chiếu của M xuống đáy luôn là C, nên hình chiếu của AM luôn là AC. Đặt CM bằng u nhân a, với u chạy từ không đến một. Trong tam giác vuông ACM, tang theta, là góc giữa AM và đáy, bằng CM trên AC, tức bằng u trên căn hai. Khi u tăng, tang theta tăng, nên chính theta cũng tăng. Ta không cần dùng hàm arctang để kết luận.",
            u.animate.set_value(0.96), min_time=5.0,
        )
        self.narrate_play(
            "Nếu đề hỏi khi nào góc bằng ba mươi độ, ta chỉ cần dùng tang ba mươi độ bằng một trên căn ba. Phương trình u trên căn hai bằng một trên căn ba cho u bằng căn hai phần ba. Đây là mẫu rất đáng nhớ cho các bài điểm động: trước hết biểu diễn một tỷ số lượng giác theo tham số, sau đó dùng tính đơn điệu hoặc giải một phương trình đơn giản.",
            u.animate.set_value(math.sqrt(2/3)), min_time=4.6,
        )

    # ======================================================
    # ERRORS + SUMMARY
    # ======================================================
    def common_errors(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bốn lỗi làm mất điểm", "Góc trong không gian không khó nếu chọn đúng mặt phẳng", "8/8")
        rows=VGroup(
            VGroup(txt("01",20,RED,BOLD),txt("Lấy một góc nhìn giống trên hình vẽ nhưng hai tia không cùng mặt phẳng.",20,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("02",20,RED,BOLD),txt("Góc đường–mặt nhưng quên tìm hình chiếu của đường lên mặt.",20,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("03",20,RED,BOLD),txt("Góc hai mặt nhưng chọn hai đường không cùng vuông góc giao tuyến.",20,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("04",20,RED,BOLD),txt("Có điểm động là lập tức bấm arccos/arctan thay vì xét tỷ số lượng giác.",20,INK)).arrange(RIGHT,buff=0.25),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.42).shift(DOWN*0.05)
        self.add_fixed_in_frame_mobjects(rows)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.10) for r in rows],lag_ratio=0.10),run_time=1.2)
        self.narrate(
            "Có bốn lỗi cần tránh. Thứ nhất, nhìn hình phối cảnh rồi lấy một góc có vẻ đúng dù hai hướng thực tế không nằm trong cùng một mặt phẳng. Thứ hai, bài đường với mặt nhưng bỏ qua bước hình chiếu. Thứ ba, bài hai mặt nhưng chọn hai đường tùy ý thay vì cùng vuông góc với giao tuyến. Thứ tư, gặp điểm động là lập tức bấm arccos hoặc arctang; cách đó vừa dài vừa che mất cấu trúc. Nếu nhớ được ba từ khóa hướng, hình chiếu và giao tuyến, phần lớn bài góc phổ thông sẽ trở nên có hệ thống.",
            2.0,
        )

    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Chốt chuyên đề", "Một bản đồ dùng được cho hầu hết bài góc HHKG", "Tổng kết")
        left=VGroup(
            txt("HAI ĐƯỜNG",18,GOLD,BOLD),
            txt("song song · mặt phẳng vuông góc",18,INK),
            txt("ĐƯỜNG – MẶT",18,CYAN,BOLD),
            txt("hình chiếu của đường",18,INK),
            txt("HAI MẶT",18,PURPLE,BOLD),
            txt("giao tuyến + hai đường vuông góc",18,INK),
            txt("ĐIỂM ĐỘNG",18,GREEN,BOLD),
            txt("tỷ số lượng giác theo tham số",18,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.17).move_to(LEFT*2.9+DOWN*0.05)
        right=VGroup(
            mty("B D perp A C'",28,GOLD),
            mty("tan alpha = frac(1, sqrt(2))",27,CYAN),
            mty("tan gamma = frac(4, 5)",27,GREEN),
            mty("tan beta = sqrt(2)",27,PURPLE),
            mty("A B perp C D",28,GOLD),
            mty("tan theta = frac(u, sqrt(2))",27,GREEN),
        ).arrange(DOWN,buff=0.24).move_to(RIGHT*3.2+DOWN*0.05)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left),FadeIn(right),run_time=0.9)
        self.narrate(
            "Video này đã bao phủ bốn lớp tư duy. Với hai đường, ta có thể đưa về hướng cắt nhau hoặc chứng minh một đường vuông góc một mặt phẳng chứa đường kia. Với đường và mặt, hình chiếu là nhân vật trung tâm. Với hai mặt, giao tuyến là trục để dựng góc. Với điểm động, một tỷ số lượng giác đơn giản thường tốt hơn rất nhiều so với việc tính trực tiếp số đo góc. Video năm sẽ đi sâu riêng vào góc nhị diện: các mặt cắt vuông góc cạnh chung, góc nhị diện trong lăng trụ, chóp đều, hình hộp và các bài góc nhị diện khó mà hình vẽ rất dễ đánh lừa.",
            2.1,
        )

    def construct(self):
        self.intro()
        self.method_map()
        self.ex1_cube_skew_perpendicular()
        self.ex2_cube_line_plane()
        self.ex3_pyramid_line_plane()
        self.ex4_cube_plane_plane()
        self.ex5_regular_tetra_hidden_right_angle()
        self.ex6_dynamic_angle()
        self.common_errors()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_04_goc_trong_khong_gian_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst) - SAFE")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_04.wav"
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

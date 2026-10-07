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
# HHKG CHUYEN SAU 03 - MANIM + TYPST - MASTER TEMPLATE
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
        series = txt("HHKG CHUYÊN SÂU · 03", 15, BLUE, BOLD)
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
    # CUBE HELPERS FOR VIDEO 03
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
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        series = txt("HHKG CHUYÊN SÂU · 03", 18, BLUE, BOLD)
        title = txt("KHOẢNG CÁCH GIỮA HAI ĐƯỜNG THẲNG CHÉO NHAU", 38, INK, BOLD)
        sub = txt("Đường vuông góc chung · mặt phẳng song song · tứ diện đều", 23, CYAN, BOLD)
        rule = Line(LEFT * 1.55, RIGHT * 1.55, color=GOLD, stroke_width=4.0)
        note = txt("Đừng đo khoảng cách giữa hai đường bằng một đoạn nối bất kỳ.", 22, MUTED)
        brand = txt(TEN_THAY, 18, MUTED)
        g = VGroup(series, rule, title, sub, note, brand).arrange(DOWN, buff=0.24)
        self.play(FadeIn(series), Create(rule), run_time=0.5)
        self.play(FadeIn(title, shift=UP * 0.10), FadeIn(sub), run_time=0.8)
        self.play(FadeIn(note), FadeIn(brand), run_time=0.45)
        self.narrate(
            "Chào các em. Video ba đi vào một trong những phần khó nhìn nhất của hình học không gian: khoảng cách giữa hai đường thẳng chéo nhau. Hai đường không cắt nhau, cũng không song song, nên ta không thể lấy một điểm tùy ý trên đường thứ nhất rồi nối sang đường thứ hai. Khoảng cách phải là độ dài đoạn vuông góc với cả hai đường. Trong bài phổ thông, ta có ba hướng tư duy mạnh: dựng trực tiếp đường vuông góc chung khi cấu hình đủ đẹp; đặt một đường vào mặt phẳng song song với đường còn lại để quy về điểm–mặt; hoặc khai thác một mặt phẳng vuông góc để hạ bài toán ba chiều xuống tam giác phẳng. Video này sẽ đi từ cấu hình nhìn thấy ngay đến tứ diện đều và một bài tổng quát có kết quả rất đẹp.",
            2.2,
        )

    # ======================================================
    # METHOD MAP / ABSTRACT CONSTRUCTION
    # ======================================================
    def method_map(self):
        self.clear_all()
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.97)
        self.add_header("Bản chất khoảng cách", "Hai đường chéo nhau – tìm đoạn vuông góc với cả hai", "01 / 08")

        p1, p2, p3, p4 = L(-3.1, -2.0, 0), L(1.6, -2.0, 0), L(1.6, 2.0, 0), L(-3.1, 2.0, 0)
        plane_p = face(p1, p2, p3, p4, color=BLUE, opacity=0.12, stroke_width=0)
        a1, a2 = L(-2.8, -0.6, 0), L(1.4, -0.6, 0)
        b1, b2 = L(-1.4, 1.4, 1.7), L(1.6, -1.2, 1.7)
        bp1, bp2 = L(-1.4, 1.4, 0), L(1.6, -1.2, 0)
        hxy = (0.9076923077, -0.6)
        H = L(hxy[0], hxy[1], 0)
        K = L(hxy[0], hxy[1], 1.7)

        line_a = solid(a1, a2, GOLD, 6.2, 1.0)
        line_b = solid(b1, b2, CYAN, 6.2, 1.0)
        proj_b = aux(bp1, bp2, CYAN, 3.0, 0.72, dash=0.10)
        HK = solid(H, K, GREEN, 6.0, 1.0)
        hdot = Dot3D(H, radius=0.060, color=GREEN)
        kdot = Dot3D(K, radius=0.060, color=GREEN)

        self.play(FadeIn(plane_p), Create(line_a), Create(line_b), run_time=1.0)
        self.play(Create(proj_b), FadeIn(hdot), FadeIn(kdot), Create(HK), run_time=0.8)

        la = mty("a", 24, GOLD).move_to(a1 + np.array([-0.10, -0.08, 0.08]))
        lb = mty("b", 24, CYAN).move_to(b1 + np.array([-0.08, 0.10, 0.08]))
        lH = mty("H", 22, GREEN).move_to(H + np.array([-0.12, -0.10, 0.08]))
        lK = mty("K", 22, GREEN).move_to(K + np.array([0.12, 0.08, 0.08]))
        self.add_fixed_orientation_mobjects(la, lb, lH, lK)

        card = self.card(
            "Mẫu chuẩn",
            "Đưa một đường vào mặt phẳng song song đường kia",
            [
                ("math", "a in (P)", 28, GOLD),
                ("math", "b parallel (P)", 28, CYAN),
                ("math", "H in a, quad K in b", 27, INK),
                ("math", "H K perp a, quad H K perp b", 27, GREEN),
                ("sep",),
                ("math", "d(a,b) = H K", 34, GOLD),
            ],
            accent=GOLD,
        )
        self.narrate(
            "Trước hết hãy nhìn mô hình tổng quát. Đường a nằm trong mặt phẳng P. Đường b không nằm trong P nhưng song song với P. Chiếu vuông góc b xuống P, ta được một đường có cùng phương với b. Vì hai đường trong cùng mặt phẳng P và không song song nhau, hình chiếu ấy sẽ cắt a tại H. Điểm K tương ứng trên b cho đoạn H K vuông góc mặt phẳng P. Khi đó H K đồng thời vuông góc với a và b, nên chính là đường vuông góc chung. Tư duy quan trọng không phải nhớ hình này, mà là nhớ thao tác: tạo một mặt phẳng chứa một đường và song song với đường còn lại.",
            2.1,
        )
        self.takeaway("Hai đường chéo nhau  →  tìm đường vuông góc chung hoặc tạo mặt phẳng song song")

    # ======================================================
    # EXAMPLE 1 - CUBE, OBVIOUS COMMON PERPENDICULAR
    # ======================================================
    def ex1_cube_common_perp(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Nhìn thấy đường vuông góc chung", "Lập phương cạnh a: tính d(A'B, CD)", "02 / 08")
        G = self.show_cube(dim=True, base_fill=0.045, top_fill=0.018)
        p = G["p"]

        l1 = solid(p["A1"], p["B"], GOLD, 6.3, 1.0)
        l2 = hidden_edge(p["C"], p["D"], CYAN, 5.2, 1.0, dash=0.10)
        bc = solid(p["B"], p["C"], GREEN, 6.0, 1.0)
        face_front = face(p["A"], p["B"], p["B1"], p["A1"], color=PURPLE, opacity=0.10, stroke_width=0)
        self.play(FadeIn(face_front), Create(l1), Create(l2), run_time=0.8)
        self.play(Create(bc), run_time=0.55)

        mark1 = right_angle_3d(p["B"], p["A1"] - p["B"], p["C"] - p["B"], size=0.24, color=GREEN)
        mark2 = right_angle_3d(p["C"], p["D"] - p["C"], p["B"] - p["C"], size=0.24, color=GREEN)
        self.play(FadeIn(mark1), FadeIn(mark2), run_time=0.45)

        card = self.card(
            "Lời giải",
            "BC vuông góc với cả hai đường",
            [
                ("math", "B C perp A B", 27, INK),
                ("math", "B C perp B B'", 27, INK),
                ("math", "B C perp (A B B' A')", 27, GREEN),
                ("math", "A' B in (A B B' A')", 26, GOLD),
                ("math", "B C perp A' B", 29, GREEN),
                ("math", "B C perp C D", 29, GREEN),
                ("sep",),
                ("math", "d(A' B, C D) = B C = a", 33, GOLD),
            ],
            accent=GREEN,
        )
        self.narrate(
            "Bài đầu tiên dùng hình lập phương cạnh a. Ta cần khoảng cách giữa đường chéo A phẩy B của mặt trước và cạnh C D của đáy. Hãy tìm một đoạn có hai đầu nằm đúng trên hai đường và vuông góc với cả hai. Đoạn B C là ứng viên rất tự nhiên. B C vuông góc A B và cũng vuông góc B B phẩy, nên B C vuông góc với cả mặt phẳng A B B phẩy A phẩy. Vì A phẩy B nằm trong mặt phẳng ấy, B C vuông góc A phẩy B. Mặt khác trong hình vuông đáy, B C vuông góc C D. Vậy B C là đường vuông góc chung của hai đường chéo nhau.",
            2.0,
        )
        self.narrate(
            "Do đó khoảng cách cần tìm chính là độ dài B C, bằng a. Câu này quan trọng không phải vì kết quả khó, mà vì nó cho ta một thói quen: trước khi dựng mặt phẳng phụ hay tính toán, hãy kiểm tra các cạnh sẵn có trong khối. Có những cấu hình mà đường vuông góc chung đã nằm ngay trên hình, chỉ bị che bởi quá nhiều đường khác.",
            1.6,
        )
        self.takeaway("Ưu tiên 1: kiểm tra xem đường vuông góc chung đã có sẵn trên hình hay chưa")

    # ======================================================
    # EXAMPLE 2 - REGULAR TETRAHEDRON
    # ======================================================
    def ex2_regular_tetra(self):
        self.clear_all()
        self.set_camera_orientation(phi=70 * DEGREES, theta=-43 * DEGREES, zoom=0.96)
        self.add_header("Bài 2 · Tứ diện đều", "Tứ diện ABCD cạnh a: tính d(AB, CD)", "03 / 08")
        G = self.show_regular_tetra(dim=True)
        p = G["p"]

        ab = solid(p["A"], p["B"], GOLD, 6.0, 1.0)
        cd = hidden_edge(p["C"], p["D"], CYAN, 5.2, 1.0, dash=0.10)
        M = (p["A"] + p["B"]) / 2
        N = (p["C"] + p["D"]) / 2
        mdot = Dot3D(M, radius=0.060, color=GREEN)
        ndot = Dot3D(N, radius=0.060, color=GREEN)
        mn = aux(M, N, GOLD, 5.3, 1.0, dash=0.10)
        self.play(Create(ab), Create(cd), FadeIn(mdot), FadeIn(ndot), Create(mn), run_time=1.0)

        lm = mty("M", 23, GREEN).move_to(M + np.array([-0.12, -0.10, 0.08]))
        ln = mty("N", 23, GREEN).move_to(N + np.array([0.12, 0.08, 0.08]))
        self.add_fixed_orientation_mobjects(lm, ln)

        mark_m = right_angle_3d(M, p["B"] - p["A"], N - M, size=0.22, color=GOLD)
        mark_n = right_angle_3d(N, p["D"] - p["C"], M - N, size=0.22, color=GOLD)
        self.play(FadeIn(mark_m), FadeIn(mark_n), run_time=0.45)

        card = self.card(
            "Lời giải",
            "Hai trung điểm tạo đường vuông góc chung",
            [
                ("math", "M A = M B = frac(a, 2)", 27, INK),
                ("math", "N C = N D = frac(a, 2)", 27, INK),
                ("math", "M N perp A B", 29, GREEN),
                ("math", "M N perp C D", 29, GREEN),
                ("sep",),
                ("math", "M C = frac(a sqrt(3), 2)", 28, CYAN),
                ("math", "C N = frac(a, 2)", 28, CYAN),
                ("math", "M N = frac(a, sqrt(2))", 34, GOLD),
            ],
            accent=GOLD,
        )
        self.narrate(
            "Bây giờ đến cấu hình kinh điển: tứ diện đều A B C D cạnh a, cần khoảng cách giữa hai cạnh đối A B và C D. Gọi M, N lần lượt là trung điểm của A B và C D. Trong tam giác đều A B C, trung tuyến C M vuông góc A B. Trong tam giác đều A B D, D M cũng vuông góc A B. Vì C M và D M là hai đường cắt nhau trong mặt phẳng M C D, suy ra A B vuông góc mặt phẳng M C D, nên A B vuông góc M N. Tương tự, từ hai tam giác đều A C D và B C D, ta có C D vuông góc M N. Như vậy M N chính là đường vuông góc chung.",
            2.3,
        )
        self.narrate(
            "Phần độ dài lại rất gọn. Trong tam giác đều A B C, đường trung tuyến C M bằng a căn ba trên hai. Trong tam giác M C D, ta có M C bằng M D và N là trung điểm C D, nên M N là đường cao. Bởi vậy M N bình phương bằng M C bình phương trừ C N bình phương, tức ba a bình phương trên bốn trừ a bình phương trên bốn, bằng a bình phương trên hai. Suy ra khoảng cách giữa hai cạnh đối của tứ diện đều bằng a trên căn hai.",
            2.1,
        )
        self.takeaway("Tứ diện đều: trung điểm hai cạnh đối thường là nơi xuất hiện đường vuông góc chung")

    # ======================================================
    # DYNAMIC VIEW OF THE REGULAR TETRAHEDRON
    # ======================================================
    def dynamic_regular_tetra(self):
        self.clear_all()
        self.set_camera_orientation(phi=70 * DEGREES, theta=-43 * DEGREES, zoom=0.96)
        self.add_header("Quan sát động", "Không phải đoạn nối nào giữa hai đường cũng là khoảng cách", "04 / 08")
        G = self.show_regular_tetra(dim=True)
        p = G["p"]
        self.add(solid(p["A"], p["B"], GOLD, 5.4, 0.95), hidden_edge(p["C"], p["D"], CYAN, 4.8, 0.95, dash=0.10))

        t = ValueTracker(0.08)
        X = always_redraw(lambda: Dot3D(p["A"] + t.get_value() * (p["B"] - p["A"]), radius=0.058, color=ORANGE))
        Y = always_redraw(lambda: Dot3D(p["C"] + t.get_value() * (p["D"] - p["C"]), radius=0.058, color=PURPLE))
        XY = always_redraw(lambda: solid(X.get_center(), Y.get_center(), color=GREEN, width=4.5, opacity=0.92))
        lx = always_redraw(lambda: mty("X", 22, ORANGE).move_to(X.get_center() + np.array([-0.10, -0.08, 0.08])))
        ly = always_redraw(lambda: mty("Y", 22, PURPLE).move_to(Y.get_center() + np.array([0.10, 0.08, 0.08])))
        self.add(X, Y, XY)
        self.add_fixed_orientation_mobjects(lx, ly)

        card = self.card(
            "Một họ đối xứng",
            "X và Y chia hai cạnh cùng tỷ số t",
            [
                ("math", "A X = t A B", 27, ORANGE),
                ("math", "C Y = t C D", 27, PURPLE),
                ("math", "X Y^2 = a^2 (2 t^2 - 2 t + 1)", 26, INK),
                ("math", "= 2 a^2 (t - frac(1, 2))^2 + frac(a^2, 2)", 25, CYAN),
                ("sep",),
                ("math", "t = frac(1, 2) quad -> quad X=M, Y=N", 26, GREEN),
            ],
            accent=CYAN,
        )
        self.narrate_play(
            "Ta cho hai điểm X và Y chuyển động đồng thời trên hai cạnh đối, cùng chia hai cạnh theo tỷ số t. Đoạn X Y thay đổi liên tục. Khi hai điểm tiến về trung điểm, đoạn nối ngắn dần; đi qua trung điểm rồi lại dài ra. Trong họ đối xứng này, bình phương X Y có dạng hai a bình phương nhân t trừ một phần hai tất cả bình phương, cộng a bình phương trên hai. Giá trị nhỏ nhất xuất hiện đúng tại t bằng một phần hai, tức X và Y trở thành M và N.",
            t.animate.set_value(0.92),
            min_time=5.2,
        )
        self.narrate_play(
            "Ta đưa hai điểm trở về vị trí trung điểm. Điều cần nhớ là hình động chỉ giúp ta nhìn thấy quy luật; chứng minh quyết định vẫn là M N vuông góc với cả A B và C D. Khoảng cách giữa hai đường chéo nhau không phải đoạn nối ngắn vì mắt thấy nó ngắn, mà vì đoạn ấy thỏa đúng điều kiện vuông góc chung.",
            t.animate.set_value(0.50),
            min_time=4.2,
        )

    # ======================================================
    # EXAMPLE 3 - RIGHT TETRAHEDRON / SURPRISING INVARIANCE
    # ======================================================
    def ex3_right_tetra(self):
        self.clear_all()
        self.set_camera_orientation(phi=68 * DEGREES, theta=-48 * DEGREES, zoom=0.96)
        self.add_header("Bài 3 · Một kết quả tổng quát đẹp", "AB ⟂ (ACD), AC=b, AD=c và AC ⟂ AD", "05 / 08")
        G = self.show_right_tetra(dim=True, bx=4.6, by=3.3, dz=4.1)
        p = G["p"]

        ab = solid(p["A"], p["B"], ORANGE, 6.0, 1.0)
        cd = hidden_edge(p["C"], p["D"], CYAN, 5.2, 1.0, dash=0.10)

        # Foot H from A to CD in the logical right triangle ACD.
        b = 3.3
        c = 4.1
        yH = b * c * c / (b * b + c * c)
        zH = b * b * c / (b * b + c * c)
        H = L(-1.7, -1.25 + yH, zH)
        ah = aux(p["A"], H, GOLD, 5.0, 1.0, dash=0.10)
        hdot = Dot3D(H, radius=0.060, color=GOLD)
        self.play(Create(ab), Create(cd), FadeIn(hdot), Create(ah), run_time=0.9)
        lh = mty("H", 22, GOLD).move_to(H + np.array([0.10, 0.08, 0.08]))
        self.add_fixed_orientation_mobjects(lh)

        mark_a = right_angle_3d(p["A"], p["B"] - p["A"], H - p["A"], size=0.22, color=GREEN)
        mark_h = right_angle_3d(H, p["D"] - p["C"], p["A"] - H, size=0.22, color=GREEN)
        self.play(FadeIn(mark_a), FadeIn(mark_h), run_time=0.45)

        card = self.card(
            "Lời giải",
            "Quy về đường cao của tam giác ACD",
            [
                ("math", "A B perp (A C D)", 28, GREEN),
                ("math", "A H perp C D", 28, GREEN),
                ("math", "A H perp A B", 28, GREEN),
                ("math", "d(A B, C D) = A H", 30, GOLD),
                ("sep",),
                ("math", "C D = sqrt(b^2 + c^2)", 27, CYAN),
                ("math", "frac(1, 2) b c = frac(1, 2) times C D times A H", 25, INK),
                ("math", "A H = frac(b c, sqrt(b^2 + c^2))", 31, GOLD),
            ],
            accent=GOLD,
        )
        self.narrate(
            "Xét một tứ diện vuông tại A theo nghĩa A B vuông góc với mặt phẳng A C D, đồng thời A C vuông góc A D. Ta cần khoảng cách giữa A B và C D. Hạ A H vuông góc C D trong tam giác A C D. Vì A H nằm trong mặt A C D còn A B vuông góc cả mặt này, A B cũng vuông góc A H. Do đó A H có đầu A nằm trên A B, đầu H nằm trên C D và vuông góc cả hai đường. A H chính là đường vuông góc chung.",
            2.0,
        )
        self.narrate(
            "Tam giác A C D vuông tại A, có hai cạnh góc vuông b và c, nên C D bằng căn b bình phương cộng c bình phương. Tính diện tích tam giác theo hai cách: một nửa b c bằng một nửa C D nhân A H. Suy ra khoảng cách giữa A B và C D bằng b c chia căn b bình phương cộng c bình phương. Điều rất đẹp là độ dài A B không xuất hiện trong kết quả. Chỉ cần A B tiếp tục vuông góc mặt A C D, kéo B ra xa hay đưa B lại gần cũng không làm khoảng cách giữa hai đường thay đổi.",
            2.1,
        )
        self.takeaway("Nếu một đường vuông góc mặt chứa đường kia, hãy tìm đường cao từ giao điểm tới đường còn lại")

    # ======================================================
    # DYNAMIC INVARIANCE IN THE RIGHT TETRAHEDRON
    # ======================================================
    def dynamic_right_tetra(self):
        self.clear_all()
        self.set_camera_orientation(phi=68 * DEGREES, theta=-48 * DEGREES, zoom=0.96)
        self.add_header("Một bất biến đáng nhớ", "Kéo B trên tia AB nhưng khoảng cách vẫn không đổi", "06 / 08")

        A = L(-1.7, -1.25, 0)
        C = L(-1.7, -1.25 + 3.3, 0)
        D = L(-1.7, -1.25, 4.1)
        b = 3.3
        c = 4.1
        yH = b * c * c / (b * b + c * c)
        zH = b * b * c / (b * b + c * c)
        H = L(-1.7, -1.25 + yH, zH)

        plane = face(A, C, D, color=BLUE, opacity=0.10, stroke_width=0)
        cd = hidden_edge(C, D, CYAN, 5.0, 0.95, dash=0.10)
        ah = aux(A, H, GOLD, 5.0, 1.0, dash=0.10)
        self.add(plane, cd, ah, Dot3D(A, radius=0.052, color=GOLD), Dot3D(C, radius=0.052, color=GOLD), Dot3D(D, radius=0.052, color=GOLD), Dot3D(H, radius=0.058, color=GOLD))

        s = ValueTracker(2.4)
        Bdot = always_redraw(lambda: Dot3D(L(-1.7 + s.get_value(), -1.25, 0), radius=0.058, color=ORANGE))
        ABline = always_redraw(lambda: solid(A, Bdot.get_center(), ORANGE, 5.6, 1.0))
        blab = always_redraw(lambda: mty("B", 22, ORANGE).move_to(Bdot.get_center() + np.array([0.12, -0.08, 0.08])))
        self.add(Bdot, ABline)
        self.add_fixed_orientation_mobjects(blab)

        card = self.card(
            "Quan sát",
            "AB thay đổi, AH không đổi",
            [
                ("math", "A B perp (A C D)", 28, GREEN),
                ("math", "d(A B, C D) = A H", 29, GOLD),
                ("math", "A H = frac(b c, sqrt(b^2 + c^2))", 30, CYAN),
                ("sep",),
                ("text", "Độ dài AB không tham gia công thức cuối.", 18, MUTED, NORMAL),
            ],
            accent=ORANGE,
        )
        self.narrate_play(
            "Bây giờ giữ nguyên tam giác A C D và cho B chạy trên tia vuông góc với mặt phẳng A C D. Độ dài A B thay đổi rất nhiều, hình tứ diện trông khác hẳn, nhưng đoạn A H vẫn đứng yên. Vì A H luôn vuông góc C D và cũng luôn vuông góc A B, nên nó vẫn là đường vuông góc chung. Khoảng cách giữa hai đường chỉ phụ thuộc tam giác vuông A C D, không phụ thuộc việc B ở xa A bao nhiêu.",
            s.animate.set_value(5.4),
            min_time=5.2,
        )
        self.narrate_play(
            "Đưa B trở lại gần A, khoảng cách vẫn giữ nguyên. Đây là một ví dụ điển hình của tư duy bất biến trong hình học không gian. Một điểm hoặc một đỉnh chuyển động không có nghĩa mọi đại lượng đều thay đổi. Nếu cấu trúc vuông góc cốt lõi không đổi, khoảng cách có thể hoàn toàn bất biến.",
            s.animate.set_value(3.2),
            min_time=4.0,
        )

    # ======================================================
    # COMMON ERRORS
    # ======================================================
    def common_errors(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_header("Lỗi sai thường gặp", "Hai đường chéo nhau – sai ngay từ định nghĩa là mất toàn bộ bài", "07 / 08")
        rows = VGroup(
            VGroup(txt("Sai 1", 18, RED, BOLD), txt("Lấy đoạn nối hai đường nhưng chỉ vuông góc một đường.", 20, INK)).arrange(RIGHT, buff=0.25),
            VGroup(txt("Sai 2", 18, RED, BOLD), txt("Thấy một đoạn ngắn trên hình rồi kết luận đó là khoảng cách.", 20, INK)).arrange(RIGHT, buff=0.25),
            VGroup(txt("Sai 3", 18, RED, BOLD), txt("Dựng mặt phẳng phụ nhưng quên chứng minh đường kia song song mặt ấy.", 20, INK)).arrange(RIGHT, buff=0.25),
            VGroup(txt("Sai 4", 18, RED, BOLD), txt("Trong tứ diện đều, nối sai hai trung điểm hoặc bỏ bước chứng minh vuông góc.", 20, INK)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).shift(UP * 0.35)
        rule = VGroup(
            txt("Checklist", 22, GOLD, BOLD),
            txt("hai đầu thuộc hai đường?  →  vuông góc đường 1?  →  vuông góc đường 2?", 21, CYAN, BOLD),
        ).arrange(DOWN, buff=0.18).shift(DOWN * 1.65)
        self.add_fixed_in_frame_mobjects(rows, rule)
        self.play(FadeIn(rows, shift=RIGHT * 0.12), FadeIn(rule), run_time=0.85)
        self.narrate(
            "Với hai đường chéo nhau, lỗi nguy hiểm nhất là quên đúng định nghĩa. Đoạn biểu diễn khoảng cách phải có một đầu trên đường thứ nhất, một đầu trên đường thứ hai, và phải vuông góc với cả hai. Nếu dùng mặt phẳng phụ, phải chứng minh mặt phẳng chứa một đường và song song với đường còn lại; nếu thiếu bước song song thì phép quy đổi khoảng cách không hợp lệ. Trong tứ diện đều, việc hai trung điểm trông rất đối xứng chưa đủ: ta vẫn phải chứng minh đoạn nối chúng vuông góc cả hai cạnh đối. Ba câu kiểm tra cuối màn hình nên trở thành phản xạ trước khi các em viết kết luận.",
            2.0,
        )

    # ======================================================
    # SUMMARY + PRACTICE
    # ======================================================
    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_header("Tổng kết", "Khoảng cách giữa hai đường chéo nhau – bốn mẫu nhận dạng", "08 / 08")
        left = VGroup(
            txt("1. Có sẵn đường vuông góc chung", 21, GOLD, BOLD),
            txt("Kiểm tra các cạnh của khối trước khi dựng thêm.", 18, INK),
            txt("2. Tứ diện đều", 21, GOLD, BOLD),
            txt("Thử trung điểm của hai cạnh đối.", 18, INK),
            txt("3. Một đường ⟂ mặt chứa đường kia", 21, GOLD, BOLD),
            txt("Quy về khoảng cách từ giao điểm tới đường còn lại.", 18, INK),
            txt("4. Cấu hình khó nhìn", 21, GOLD, BOLD),
            txt("Tạo mặt phẳng chứa một đường và song song đường kia.", 18, INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(LEFT * 2.65 + UP * 0.25)

        right = VGroup(
            txt("Bài tự luyện", 22, CYAN, BOLD),
            txt("AB ⟂ (ACD), AC=6, AD=8, AC ⟂ AD.", 18, INK),
            txt("Tính d(AB,CD).", 18, INK),
            mty("C D = 10", 28, CYAN),
            mty("frac(1, 2) times 6 times 8 = frac(1, 2) times 10 times h", 25, INK),
            mty("h = frac(24, 5)", 32, GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(RIGHT * 3.15 + UP * 0.25)
        self.add_fixed_in_frame_mobjects(left, right)
        self.play(FadeIn(left, shift=RIGHT * 0.1), FadeIn(right, shift=LEFT * 0.1), run_time=0.9)
        self.narrate(
            "Chốt lại video ba. Khoảng cách giữa hai đường chéo nhau là độ dài đường vuông góc chung. Nếu đường đó đã có sẵn trên hình, dùng ngay. Trong tứ diện đều, hai trung điểm của hai cạnh đối là một cấu hình đặc biệt đẹp. Nếu một đường vuông góc với mặt phẳng chứa đường kia, bài toán hạ xuống khoảng cách từ một điểm tới một đường trong mặt phẳng. Còn khi hình quá khó nhìn, hãy tạo một mặt phẳng chứa một đường và song song với đường còn lại. Bài tự luyện bên phải là phiên bản số của bài tứ diện vuông: tam giác A C D có hai cạnh góc vuông sáu và tám nên C D bằng mười; đường cao từ A xuống C D bằng hai mươi bốn phần năm, cũng chính là khoảng cách giữa A B và C D.",
            2.1,
        )
        outro = txt("Video 04: Góc đường–đường, đường–mặt và mặt–mặt", 22, MUTED, BOLD).to_edge(DOWN, buff=0.42)
        self.add_fixed_in_frame_mobjects(outro)
        self.play(FadeIn(outro), run_time=0.45)
        self.narrate(
            "Video bốn sẽ chuyển sang hệ thống các loại góc trong không gian. Ta sẽ phân biệt góc giữa hai đường, góc giữa đường và mặt, góc giữa hai mặt, và đặc biệt học cách chọn hình chiếu hoặc mặt cắt sao cho góc không gian biến thành một góc phẳng đúng nghĩa.",
            1.4,
        )

    def construct(self):
        self.intro()
        self.method_map()
        self.ex1_cube_common_perp()
        self.ex2_regular_tetra()
        self.dynamic_regular_tetra()
        self.ex3_right_tetra()
        self.dynamic_right_tetra()
        self.common_errors()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_03_hai_duong_cheo_nhau_typst_SAFE_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst)")
    print("Series: HHKG Chuyen Sau 03 SAFE - Khoang cach hai duong thang cheo nhau")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_03.wav"
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

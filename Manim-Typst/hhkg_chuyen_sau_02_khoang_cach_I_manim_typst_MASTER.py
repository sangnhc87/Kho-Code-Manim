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
# HHKG CHUYEN SAU 01 - MANIM + TYPST - MASTER TEMPLATE
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


def mty(s, size=38, color=INK):
    """Math only. Text prose must use txt()."""
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
        series = txt("HHKG CHUYÊN SÂU · 02", 15, BLUE, BOLD)
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
    # CUBE HELPERS FOR VIDEO 02
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
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        series=txt("HHKG CHUYÊN SÂU · 02",18,BLUE,BOLD)
        title=txt("KHOẢNG CÁCH TRONG KHÔNG GIAN I",41,INK,BOLD)
        sub=txt("Điểm–mặt · đường–mặt song song · mặt phẳng phụ · thể tích",23,CYAN,BOLD)
        rule=Line(LEFT*1.45,RIGHT*1.45,color=GOLD,stroke_width=4.0)
        note=txt("Không săn chân vuông góc bằng mắt. Hãy chọn cấu trúc trước.",22,MUTED)
        brand=txt(TEN_THAY,18,MUTED)
        g=VGroup(series,rule,title,sub,note,brand).arrange(DOWN,buff=0.24)
        self.play(FadeIn(series),Create(rule),run_time=0.5)
        self.play(FadeIn(title,shift=UP*0.10),FadeIn(sub),run_time=0.75)
        self.play(FadeIn(note),FadeIn(brand),run_time=0.4)
        self.narrate(
            "Chào các em. Video hai của series tập trung vào khoảng cách trong không gian. Đây là dạng bài rất dễ rối nếu ta chỉ cố nhìn xem chân đường vuông góc nằm ở đâu. Thực ra phần lớn bài phổ thông xoay quanh một hạt nhân duy nhất: khoảng cách từ một điểm đến một mặt phẳng. Từ đó, khoảng cách từ đường thẳng song song đến mặt phẳng chỉ là một trường hợp quy về điểm–mặt. Khi chân vuông góc khó dựng, ta có hai chiến lược rất mạnh: chọn một mặt phẳng phụ vuông góc với mặt phẳng cần xét, hoặc đổi khoảng cách thành chiều cao trong công thức thể tích.",2.2)

    # ======================================================
    # MAP OF METHODS
    # ======================================================
    def method_map(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Bản đồ phương pháp","Một hạt nhân – bốn cách xử lý","01 / 08")
        left=VGroup(
            txt("Khoảng cách cơ bản",23,GOLD,BOLD),
            mty("d(M,(P)) = M H",32,CYAN),
            txt("với MH vuông góc mặt phẳng (P)",19,MUTED),
            Line(LEFT*2.5,RIGHT*2.5,color=GRID,stroke_width=1),
            txt("Ba đường đi thường gặp",22,INK,BOLD),
            txt("1. Dựng trực tiếp H nếu hình cho phép.",19,INK),
            txt("2. Dùng mặt phẳng phụ vuông góc (P).",19,INK),
            txt("3. Dùng thể tích để tránh tìm H.",19,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).move_to(LEFT*2.55+DOWN*0.05)
        right=VGroup(
            txt("Quy về điểm–mặt",23,GOLD,BOLD),
            mty("a parallel (P)",31,CYAN),
            mty("d(a,(P)) = d(A,(P))",30,INK),
            txt("với A là một điểm bất kỳ trên a",18,MUTED),
            Line(LEFT*2.25,RIGHT*2.25,color=GRID,stroke_width=1),
            txt("Tư duy quan trọng",22,INK,BOLD),
            txt("Khoảng cách là độ dài ngắn nhất.",19,INK),
            txt("Muốn tính nhanh, hãy làm nó trở thành",19,INK),
            txt("một đường cao trong tam giác hoặc tứ diện.",19,CYAN,BOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.23).move_to(RIGHT*3.05+DOWN*0.05)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left,shift=RIGHT*0.1),FadeIn(right,shift=LEFT*0.1),run_time=0.9)
        self.narrate(
            "Trước khi vào ví dụ, ta thống nhất một bản đồ. Khoảng cách từ M đến mặt phẳng P là độ dài MH, trong đó H thuộc P và MH vuông góc P. Nếu đường thẳng a song song với P, khoảng cách từ a đến P bằng khoảng cách từ bất kỳ điểm nào trên a đến P. Điều khó không nằm ở định nghĩa mà ở cách tìm MH. Khi hình đẹp, ta dựng trực tiếp. Khi mặt phẳng P có một mặt phẳng khác vuông góc với nó, ta cắt bài toán về một tam giác phẳng. Khi cả hai cách dựng đều xấu, thể tích thường là con đường ngắn nhất.",2.0)

    # ======================================================
    # EXAMPLE 1 - POINT TO PLANE VIA AUXILIARY PLANE
    # ======================================================
    def ex1_aux_plane(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 1 · Điểm đến mặt phẳng","Dùng mặt phẳng phụ để nhìn thấy chân vuông góc","02 / 08")
        G=self.show_base_model(dim=True,base_fill=0.07); p=G["p"]
        sbc=face(p["S"],p["B"],p["C"],color=PURPLE,opacity=0.24,stroke_width=0)
        sab=face(p["S"],p["A"],p["B"],color=GOLD,opacity=0.12,stroke_width=0)
        bc=solid(p["B"],p["C"],GOLD,5.5,1)
        sb=solid(p["S"],p["B"],GREEN,5.2,1)
        ab=solid(p["A"],p["B"],CYAN,5.0,1)
        self.play(FadeIn(sbc),FadeIn(sab),Create(bc),Create(sb),Create(ab),run_time=0.8)
        problem=self.card("Đề bài","Tính d(A,(SBC))",[
            ("math","A B = 4",29,CYAN),("math","S A = 3",29,CYAN),
            ("math","S A perp (A B C D)",28,GREEN),("sep",),
            ("text","Không cần tìm H trong không gian ngay.",18,MUTED,NORMAL),
        ],accent=PURPLE)
        self.narrate(
            "Ta trở lại hình chóp quen thuộc với đáy là hình vuông cạnh bốn và S A bằng ba, vuông góc đáy. Cần tính khoảng cách từ A đến mặt phẳng S B C. Nếu lao ngay vào việc dựng H trong mặt S B C, hình sẽ khó đọc. Thay vào đó, hãy nhìn mặt phẳng S A B. Vì B C vuông góc A B và cũng vuông góc S A, nên B C vuông góc với mặt phẳng S A B. Mà B C nằm trong mặt phẳng S B C, suy ra hai mặt phẳng S A B và S B C vuông góc với nhau.",2.1)
        H_log=np.array([0.0,0.0,0.0])
        # In logical triangle A(-2,-2,0), S(-2,-2,3), B(2,-2,0), foot from A to SB
        A=np.array([-2.,-2.,0.]); S=np.array([-2.,-2.,3.]); B=np.array([2.,-2.,0.])
        v=S-B; t=np.dot(A-B,v)/np.dot(v,v); H_log=B+t*v; H=L(*H_log)
        ah=solid(p["A"],H,GOLD,6.0,1); hdot=Dot3D(H,radius=0.052,color=GOLD)
        mark=right_angle_3d(H,p["A"]-H,p["S"]-p["B"],size=0.19,color=GOLD)
        self.play(Create(ah),FadeIn(hdot),FadeIn(mark),run_time=0.65)
        sol=self.card("Lời giải","Cắt bài toán bằng mặt phẳng (SAB)",[
            ("math","(S A B) perp (S B C)",28,GREEN),
            ("math","H in S B",28,INK),
            ("math","A H perp S B",28,CYAN),
            ("math","d(A,(S B C)) = A H",29,GOLD),
            ("math","S B = 5",28,INK),
            ("math","A H = frac(S A times A B, S B)",27,INK),
            ("math","A H = frac(12, 5)",36,GOLD),
        ],accent=GOLD,auto_add=False)
        self.swap_card(problem,sol)
        self.narrate(
            "Hai mặt phẳng vuông góc nhau và giao nhau theo S B. Vì vậy, trong mặt phẳng S A B, chỉ cần hạ A H vuông góc S B thì A H cũng vuông góc với toàn bộ mặt phẳng S B C. Khoảng cách cần tìm chính là A H. Tam giác S A B vuông tại A, có S A bằng ba, A B bằng bốn nên S B bằng năm. Dùng diện tích tam giác theo hai cách, một nửa S A nhân A B bằng một nửa S B nhân A H. Suy ra A H bằng mười hai phần năm. Đây là mẫu rất mạnh: muốn tính điểm–mặt, hãy tìm một mặt phẳng phụ vuông góc với mặt cần xét rồi biến bài toán thành khoảng cách điểm–đường trong mặt phẳng đó.",2.2)
        self.takeaway("Điểm–mặt khó nhìn  →  tìm mặt phẳng phụ vuông góc  →  đưa về tam giác phẳng")

    # ======================================================
    # EXAMPLE 2 - LINE PARALLEL PLANE
    # ======================================================
    def ex2_line_plane(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=VIEW_THETA,zoom=VIEW_ZOOM)
        self.add_header("Bài 2 · Đường thẳng song song mặt phẳng","Quy ngay về khoảng cách điểm–mặt","03 / 08")
        G=self.show_base_model(dim=True,base_fill=0.07); p=G["p"]
        sbc=face(p["S"],p["B"],p["C"],color=PURPLE,opacity=0.22,stroke_width=0)
        ad=solid(p["A"],p["D"],ORANGE,6.0,1.0)
        bc=solid(p["B"],p["C"],GOLD,5.0,1.0)
        self.play(FadeIn(sbc),Create(ad),Create(bc),run_time=0.7)
        problem=self.card("Đề bài","Tính d(AD,(SBC))",[
            ("math","A D parallel B C",30,CYAN),
            ("math","B C subset (S B C)",28,INK),
            ("text","AD không cắt mặt phẳng (SBC).",18,MUTED,NORMAL),
        ],accent=ORANGE)
        self.narrate(
            "Vẫn trên cấu hình cũ, ta đổi câu hỏi sang khoảng cách từ đường thẳng A D đến mặt phẳng S B C. Đây là lúc cần nhận ra một phép rút gọn rất nhanh. Vì đáy là hình vuông nên A D song song B C, mà B C nằm trong mặt phẳng S B C. Đồng thời A D không nằm trong mặt này, nên A D song song với mặt phẳng S B C. Khi một đường thẳng song song với một mặt phẳng, mọi điểm trên đường đều có cùng khoảng cách tới mặt phẳng.",1.8)
        sol=self.card("Lời giải","Chọn điểm thuận lợi nhất trên AD",[
            ("math","A D parallel (S B C)",30,GREEN),
            ("math","d(A D,(S B C)) = d(A,(S B C))",27,INK),
            ("math","d(A,(S B C)) = frac(12, 5)",31,GOLD),
            ("math","d(A D,(S B C)) = frac(12, 5)",34,GOLD),
        ],accent=GOLD,auto_add=False)
        self.swap_card(problem,sol)
        self.narrate(
            "Ta được phép chọn bất kỳ điểm nào trên A D. Điểm A là lựa chọn tốt nhất vì khoảng cách từ A đến mặt S B C vừa được tính ở bài trước. Do đó khoảng cách từ A D đến mặt S B C bằng mười hai phần năm. Bài này rất ngắn, nhưng tư duy quan trọng: đừng dựng thêm đường vuông góc từ cả một đường thẳng. Hãy kiểm tra quan hệ song song trước; nếu đường song song mặt, toàn bộ bài toán lập tức trở về dạng điểm–mặt quen thuộc.",1.7)
        self.takeaway("Đường song song mặt phẳng  →  lấy một điểm thuận lợi trên đường")

    # ======================================================
    # CUBE CONFIG + AUXILIARY FACE
    # ======================================================
    def ex3_cube_aux(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=-50*DEGREES,zoom=0.90)
        self.add_header("Bài 3 · Mặt phẳng phụ trong hình lập phương","Tính d(A,(BCD'))","04 / 08")
        G=self.show_cube(dim=True,base_fill=0.055,top_fill=0.025); p=G["p"]
        target=face(p["B"],p["C"],p["D1"],color=PURPLE,opacity=0.24,stroke_width=0)
        auxface=face(p["A"],p["B"],p["B1"],p["A1"],color=GOLD,opacity=0.11,stroke_width=0)
        ba1=solid(p["B"],p["A1"],CYAN,5.4,1)
        self.play(FadeIn(target),FadeIn(auxface),Create(ba1),run_time=0.8)
        problem=self.card("Đề bài","Lập phương cạnh a",[
            ("math","A B = A A' = a",29,CYAN),
            ("math","d(A,(B C D'))",30,GOLD),
            ("sep",),
            ("text","Hãy tìm một mặt phẳng phụ vuông góc (BCD').",18,MUTED,NORMAL),
        ],accent=PURPLE)
        self.narrate(
            "Ta chuyển sang hình lập phương cạnh a. Cần tính khoảng cách từ A đến mặt phẳng B C D phẩy. Hình này nếu dựng chân trực tiếp trong mặt chéo sẽ khá khó nhìn. Ta tìm một mặt phẳng phụ có sẵn: mặt A B B phẩy A phẩy. Trong lập phương, B C vuông góc A B và cũng vuông góc B B phẩy, nên B C vuông góc với mặt A B B phẩy A phẩy. Vì B C lại nằm trong mặt B C D phẩy, hai mặt phẳng này vuông góc nhau.",2.0)
        H=(p["B"]+p["A1"])/2
        ah=solid(p["A"],H,GOLD,6.0,1); hdot=Dot3D(H,radius=0.05,color=GOLD)
        mark=right_angle_3d(H,p["A"]-H,p["A1"]-p["B"],size=0.18,color=GOLD)
        self.play(Create(ah),FadeIn(hdot),FadeIn(mark),run_time=0.6)
        sol=self.card("Lời giải","Mặt phụ biến điểm–mặt thành điểm–đường",[
            ("math","(A B B' A') perp (B C D')",27,GREEN),
            ("math","(A B B' A') intersect (B C D') = B A'",26,INK),
            ("math","A H perp B A'",29,CYAN),
            ("math","d(A,(B C D')) = A H",28,GOLD),
            ("math","B A' = a sqrt(2)",28,INK),
            ("math","A H = frac(a, sqrt(2))",34,GOLD),
        ],accent=GOLD,auto_add=False)
        self.swap_card(problem,sol)
        self.narrate(
            "Hai mặt phẳng vuông góc và giao nhau theo đường B A phẩy. Vì thế khoảng cách từ A đến mặt B C D phẩy chính là khoảng cách từ A đến đường B A phẩy trong hình vuông A B B phẩy A phẩy. Tam giác A B A phẩy vuông cân tại A, có hai cạnh góc vuông đều bằng a và cạnh huyền B A phẩy bằng a căn hai. Đường cao từ A xuống cạnh huyền bằng a trên căn hai. Vậy khoảng cách cần tìm là a trên căn hai. Một bài ba chiều đã trở thành bài đường cao trong tam giác vuông cân.",2.0)
        self.takeaway("Mặt phẳng phụ tốt thường là một mặt có sẵn của khối")

    # ======================================================
    # EXAMPLE 4 - SAME DISTANCE VIA VOLUME
    # ======================================================
    def ex4_volume(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=-50*DEGREES,zoom=0.90)
        self.add_header("Bài 4 · Cùng một khoảng cách, cách giải thứ hai","Đổi sang thể tích tứ diện","05 / 08")
        G=self.show_cube(dim=True,base_fill=0.04,top_fill=0.02); p=G["p"]
        target=face(p["B"],p["C"],p["D1"],color=PURPLE,opacity=0.25,stroke_width=0)
        triabc=face(p["A"],p["B"],p["C"],color=BLUE,opacity=0.16,stroke_width=0)
        cd1=solid(p["C"],p["D1"],GREEN,5.0,1)
        bc=solid(p["B"],p["C"],CYAN,5.0,1)
        self.play(FadeIn(target),FadeIn(triabc),Create(cd1),Create(bc),run_time=0.7)
        problem=self.card("Mục tiêu","Tính lại d(A,(BCD'))",[
            ("text","Lần này không dùng mặt phẳng phụ.",18,INK,NORMAL),
            ("text","Xem tứ diện ABCD' theo hai cách.",18,MUTED,NORMAL),
        ],accent=GREEN)
        self.narrate(
            "Cùng một khoảng cách nhưng ta giải lại bằng thể tích để thấy khi nào phương pháp này mạnh hơn. Xét tứ diện A B C D phẩy. Nếu chọn tam giác A B C làm đáy, diện tích đáy bằng một nửa a bình phương và chiều cao từ D phẩy xuống mặt đáy của lập phương bằng a. Vì vậy thể tích tứ diện tính được ngay, không cần dựng bất kỳ chân vuông góc mới nào.",1.6)
        sol=self.card("Lời giải","Một tứ diện – hai cách chọn đáy",[
            ("math","V_(A B C D') = frac(1, 3) times frac(a^2, 2) times a",25,CYAN),
            ("math","V_(A B C D') = frac(a^3, 6)",29,CYAN),
            ("math","B C perp C D'",27,INK),
            ("math","C D' = a sqrt(2)",27,INK),
            ("math","S_(B C D') = frac(a^2 sqrt(2), 2)",26,GREEN),
            ("math","frac(a^3, 6) = frac(1, 3) S_(B C D') d",25,INK),
            ("math","d = frac(a, sqrt(2))",34,GOLD),
        ],accent=GOLD,auto_add=False)
        self.swap_card(problem,sol)
        self.narrate(
            "Thể tích bằng một phần sáu a lập phương. Bây giờ chọn tam giác B C D phẩy làm đáy. Ta có B C vuông góc C D phẩy, B C bằng a và C D phẩy là đường chéo của một mặt vuông nên bằng a căn hai. Diện tích tam giác B C D phẩy bằng a bình phương căn hai chia hai. Chiều cao từ A đến đáy B C D phẩy chính là khoảng cách cần tìm. Thế vào công thức thể tích, ta lại được d bằng a trên căn hai. Cách thể tích đặc biệt hữu ích khi diện tích một mặt và thể tích khối đã dễ tính hơn vị trí chân đường vuông góc.",2.1)
        self.takeaway("Nếu chân vuông góc xấu nhưng thể tích đẹp  →  đổi khoảng cách thành chiều cao")

    # ======================================================
    # DYNAMIC EXTENSION - CONSTANT DISTANCE
    # ======================================================
    def dynamic_extension(self):
        self.clear_all(); self.set_camera_orientation(phi=VIEW_PHI,theta=-50*DEGREES,zoom=0.90)
        self.add_header("Mở rộng · Khoảng cách bất biến","M chạy trên AD của hình lập phương","06 / 08")
        G=self.show_cube(dim=True,base_fill=0.04,top_fill=0.02); p=G["p"]
        target=face(p["B"],p["C"],p["D1"],color=PURPLE,opacity=0.22,stroke_width=0)
        ad=solid(p["A"],p["D"],ORANGE,5.8,1)
        self.add(target,ad)
        t=ValueTracker(0.05)
        def logical_M():
            u=t.get_value(); return np.array([-2.,-2.+4*u,0.])
        def logical_H():
            m=logical_M(); return np.array([0.,m[1],2.])
        Mdot=always_redraw(lambda: Dot3D(L(*logical_M()),radius=0.06,color=GOLD))
        Hdot=always_redraw(lambda: Dot3D(L(*logical_H()),radius=0.045,color=CYAN))
        MH=always_redraw(lambda: aux(L(*logical_M()),L(*logical_H()),color=GOLD,width=4.2,opacity=0.95,dash=0.10))
        mlab=always_redraw(lambda: mty("M",23,GOLD).move_to(L(*logical_M())+np.array([-0.12,-0.10,0.08])))
        self.add(Mdot,Hdot,MH); self.add_fixed_orientation_mobjects(mlab)
        card=self.card("Quan sát","M chạy trên AD",[
            ("math","A D parallel (B C D')",28,GREEN),
            ("math","d(M,(B C D')) = d(A,(B C D'))",25,INK),
            ("math","d(M,(B C D')) = frac(a, sqrt(2))",31,GOLD),
            ("sep",),
            ("text","Khoảng cách không đổi dù M chuyển động.",18,MUTED,NORMAL),
        ],accent=ORANGE)
        self.narrate_play(
            "Cho điểm M chạy từ A đến D. Đoạn vàng đứt biểu diễn đường vuông góc từ M tới mặt B C D phẩy. Ta thấy chân vuông góc chuyển động, nhưng độ dài khoảng cách không đổi. Lý do không nằm ở tính toán mới: A D song song với B C, mà B C nằm trong mặt B C D phẩy, nên A D song song mặt phẳng B C D phẩy. Mọi điểm trên một đường thẳng song song với mặt phẳng đều cách mặt phẳng một khoảng bằng nhau.",
            t.animate.set_value(0.95),min_time=5.0)
        self.narrate(
            "Vì khoảng cách tại A đã bằng a trên căn hai, nên với mọi vị trí M trên A D, khoảng cách từ M tới mặt B C D phẩy vẫn bằng a trên căn hai. Đây là một tính chất rất hữu ích trong các bài điểm động: trước khi lập hàm theo tham số, hãy kiểm tra xem đại lượng có thực sự thay đổi hay không. Đôi khi một bài cực trị biến mất hoàn toàn chỉ nhờ phát hiện quan hệ song song.",1.7)
        self.takeaway("Điểm động chưa chắc tạo đại lượng động  →  kiểm tra song song trước khi lập hàm")

    # ======================================================
    # COMMON ERRORS
    # ======================================================
    def common_errors(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Lỗi sai thường gặp","Khoảng cách là độ dài ngắn nhất, không phải đoạn nhìn thuận mắt","07 / 08")
        rows=VGroup(
            VGroup(txt("Sai 1",18,RED,BOLD),txt("Chọn một đoạn nối điểm với mặt nhưng không vuông góc.",20,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("Sai 2",18,RED,BOLD),txt("Thấy đường song song mặt nhưng vẫn dựng khoảng cách từ đầu.",20,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("Sai 3",18,RED,BOLD),txt("Dựng chân H quá sớm, trước khi tìm mặt phẳng phụ.",20,INK)).arrange(RIGHT,buff=0.25),
            VGroup(txt("Sai 4",18,RED,BOLD),txt("Dùng thể tích nhưng chọn nhầm mặt đáy hoặc chiều cao tương ứng.",20,INK)).arrange(RIGHT,buff=0.25),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.38).shift(UP*0.35)
        rule=VGroup(
            txt("Thứ tự nên nghĩ",22,GOLD,BOLD),
            txt("song song?  →  mặt phẳng phụ?  →  tam giác phẳng?  →  thể tích?",22,CYAN,BOLD),
        ).arrange(DOWN,buff=0.18).shift(DOWN*1.65)
        self.add_fixed_in_frame_mobjects(rows,rule)
        self.play(FadeIn(rows,shift=RIGHT*0.12),FadeIn(rule),run_time=0.85)
        self.narrate(
            "Bốn lỗi phổ biến nhất đều bắt nguồn từ việc dựng hình quá sớm. Một đoạn nối từ điểm đến mặt phẳng chỉ là khoảng cách khi nó vuông góc với mặt phẳng. Nếu đường đã song song với mặt, hãy quy về một điểm trước. Nếu chân vuông góc khó nhìn, đừng ép dựng ngay; hãy tìm mặt phẳng phụ vuông góc với mặt cần xét. Và khi dùng thể tích, phải nói rõ tứ diện nào đang xét, mặt nào được chọn làm đáy và chiều cao tương ứng là khoảng cách nào. Một lời giải khoảng cách tốt thường ngắn vì cấu trúc được chọn đúng từ đầu.",2.0)

    # ======================================================
    # SUMMARY + PRACTICE
    # ======================================================
    def summary(self):
        self.clear_all(); self.set_camera_orientation(phi=0*DEGREES,theta=-90*DEGREES,zoom=1.0)
        self.add_header("Tổng kết","Khoảng cách I – bốn mẫu nhận dạng","08 / 08")
        left=VGroup(
            txt("1. Điểm – mặt",21,GOLD,BOLD),
            txt("Tìm mặt phẳng phụ vuông góc để đưa về điểm–đường.",18,INK),
            txt("2. Đường ∥ mặt",21,GOLD,BOLD),
            txt("Chọn một điểm thuận lợi trên đường.",18,INK),
            txt("3. Chân vuông góc khó dựng",21,GOLD,BOLD),
            txt("Đổi khoảng cách thành chiều cao trong công thức thể tích.",18,INK),
            txt("4. Điểm động",21,GOLD,BOLD),
            txt("Kiểm tra bất biến trước khi lập hàm.",18,INK),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.24).move_to(LEFT*2.65+UP*0.25)
        right=VGroup(
            txt("Bài tự luyện",22,CYAN,BOLD),
            txt("Trong lập phương cạnh a, M là trung điểm AD.",18,INK),
            txt("Tính khoảng cách từ M đến (BCD').",18,INK),
            mty("M in A D",28,CYAN),
            mty("A D parallel (B C D')",28,GREEN),
            mty("d(M,(B C D')) = frac(a, sqrt(2))",30,GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.24).move_to(RIGHT*3.15+UP*0.25)
        self.add_fixed_in_frame_mobjects(left,right)
        self.play(FadeIn(left,shift=RIGHT*0.1),FadeIn(right,shift=LEFT*0.1),run_time=0.9)
        self.narrate(
            "Chốt lại video hai. Dạng điểm–mặt là hạt nhân. Khi có một mặt phẳng phụ vuông góc với mặt cần xét, bài toán ba chiều có thể hạ xuống một tam giác phẳng. Khi một đường thẳng song song với mặt phẳng, khoảng cách đường–mặt được quy về khoảng cách từ một điểm bất kỳ trên đường. Khi chân vuông góc khó dựng nhưng thể tích và diện tích mặt lại đẹp, hãy xem khoảng cách như một chiều cao của tứ diện. Và với điểm động, đừng vội lập hàm: quan hệ song song có thể làm khoảng cách bất biến. Bài tự luyện bên phải chính là một ví dụ như vậy.",2.0)
        outro=txt("Video 03: Khoảng cách giữa hai đường chéo nhau",22,MUTED,BOLD).to_edge(DOWN,buff=0.42)
        self.add_fixed_in_frame_mobjects(outro); self.play(FadeIn(outro),run_time=0.45)
        self.narrate(
            "Ở video ba, ta đi vào phần khó hơn: khoảng cách giữa hai đường chéo nhau. Ta sẽ học đường vuông góc chung, mặt phẳng song song chứa một đường, cách đổi về điểm–mặt, và những cấu hình hình hộp hoặc tứ diện mà nhìn bằng mắt gần như không thấy đường cần dựng.",1.4)

    def construct(self):
        self.intro()
        self.method_map()
        self.ex1_aux_plane()
        self.ex2_line_plane()
        self.ex3_cube_aux()
        self.ex4_volume()
        self.dynamic_extension()
        self.common_errors()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_02_khoang_cach_I_typst_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst)")
    print("Series: HHKG Chuyen Sau 02 - Khoang cach trong khong gian I")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_02.wav"
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

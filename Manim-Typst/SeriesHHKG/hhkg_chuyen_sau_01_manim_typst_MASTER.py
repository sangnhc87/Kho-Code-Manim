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
        series = txt("HHKG CHUYÊN SÂU · 01", 15, BLUE, BOLD)
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
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

        series = txt("HHKG CHUYÊN SÂU · 01", 18, BLUE, BOLD)
        title = txt("MỘT CẤU HÌNH – NHIỀU ĐẠI LƯỢNG", 42, INK, BOLD)
        sub = txt("Góc · góc nhị diện · khoảng cách · thể tích · tỷ số", 24, CYAN, BOLD)
        rule = Line(LEFT * 1.45, RIGHT * 1.45, color=GOLD, stroke_width=4.0)
        note = txt("Nhìn đúng cấu hình, lời giải sẽ ngắn lại.", 23, MUTED)
        brand = txt(TEN_THAY, 18, MUTED)

        g = VGroup(series, rule, title, sub, note, brand).arrange(DOWN, buff=0.24)
        self.play(FadeIn(series), Create(rule), run_time=0.55)
        self.play(FadeIn(title, shift=UP * 0.10), FadeIn(sub), run_time=0.80)
        self.play(FadeIn(note), FadeIn(brand), run_time=0.45)
        self.narrate(
            "Chào các em. Trong hình học không gian, một cấu hình tốt thường chứa nhiều bài toán hơn ta tưởng. Với cùng một hình chóp, ta có thể lần lượt đọc được góc giữa đường thẳng và mặt phẳng, góc nhị diện, thể tích, khoảng cách và tỷ số thể tích. Điều quan trọng không phải là nhớ thật nhiều công thức, mà là biết nên nhìn vào tam giác nào, mặt phẳng nào và quan hệ vuông góc nào. Video này sẽ đi chậm qua từng bước để các em thấy rõ cách một bài toán không gian được đưa về những bài toán phẳng rất quen thuộc.",
            2.0,
        )

    # ======================================================
    # CONFIGURATION
    # ======================================================
    def configuration(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header(
            "Cấu hình gốc",
            "Một hình chóp – năm hướng khai thác",
            "01 / 07",
        )

        G = self.pyramid(base_fill=0.10)
        self.play(FadeIn(G["base"]), Create(G["edges"]), FadeIn(G["dots"]), run_time=1.1)
        self.labels(G)
        self.legend()

        p = G["p"]
        mark1 = right_angle_3d(
            p["A"],
            p["B"] - p["A"],
            p["S"] - p["A"],
            size=0.25,
        )
        self.play(FadeIn(mark1), run_time=0.35)

        card = self.card(
            "Giả thiết",
            "Hình chóp S.ABCD",
            [
                ("text", "Đáy ABCD là hình vuông", 20, MUTED, NORMAL),
                ("math", "A B = B C = 4", 32, CYAN),
                ("math", "S A = 3", 32, CYAN),
                ("math", "S A perp (A B C D)", 31, GREEN),
                ("sep",),
                ("text", "A là hình chiếu vuông góc của S lên đáy.", 18, INK, NORMAL),
            ],
            accent=GOLD,
        )

        self.narrate(
            "Ta xét hình chóp S.ABCD có đáy ABCD là hình vuông cạnh bốn, SA bằng ba và SA vuông góc với mặt phẳng đáy. Vì vậy A là hình chiếu vuông góc của S xuống đáy. Ngay từ giả thiết, ta có hai tam giác vuông rất quan trọng là SAB và SAD. Đặc biệt, tam giác SAB có hai cạnh góc vuông bằng ba và bốn nên SB bằng năm. Các em nên tập thói quen ghi nhận những dữ kiện như vậy ngay khi đọc hình, vì chúng thường được dùng lại ở nhiều câu phía sau.",
            1.8,
        )

        self.narrate_camera(
            "Trước khi làm câu đầu tiên, hãy thử đọc cấu hình bằng ngôn ngữ vuông góc. Từ SA vuông góc với đáy, ta suy ra SA vuông góc với mọi đường thẳng trong đáy đi qua A, chẳng hạn AB, AD và AC. Từ hình vuông, ta còn có AB vuông góc BC, AD vuông góc CD và các cặp cạnh đối song song. Chính những quan hệ đơn giản này sẽ giúp ta dựng được hình chiếu, mặt cắt vuông góc và các tam giác vuông cần thiết.",
            phi=71 * DEGREES,
            theta=-46 * DEGREES,
            zoom=0.97,
        )

    # ======================================================
    # 1. LINE - PLANE ANGLE
    # ======================================================
    def line_plane_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header(
            "Bài 1 · Góc giữa đường thẳng và mặt phẳng",
            "Tìm góc giữa SC và mặt phẳng đáy",
            "02 / 07",
        )

        G = self.show_base_model(dim=True, base_fill=0.09)
        p = G["p"]

        sc = solid(p["S"], p["C"], GOLD, 6.2, 1.0)
        sa = solid(p["S"], p["A"], GREEN, 5.2, 1.0)
        ac = aux(p["A"], p["C"], CYAN, 4.4, 1.0)
        mark = right_angle_3d(
            p["A"],
            p["C"] - p["A"],
            p["S"] - p["A"],
            size=0.24,
            color=GREEN,
        )

        self.play(Create(sc), Create(sa), Create(ac), FadeIn(mark), run_time=0.8)

        problem = self.card(
            "Đề bài",
            "Góc giữa SC và đáy",
            [
                ("text", "Xác định góc giữa đường thẳng SC và mặt phẳng (ABCD).", 20, INK, NORMAL),
                ("sep",),
                ("text", "Quan sát trước khi tính:", 18, GOLD, BOLD),
                ("text", "Hình chiếu của S xuống đáy là điểm nào?", 18, MUTED, NORMAL),
                ("text", "Hình chiếu của SC lên đáy là đoạn nào?", 18, MUTED, NORMAL),
            ],
            accent=BLUE,
        )

        self.narrate(
            "Muốn tìm góc giữa SC và mặt phẳng đáy, ta không đo trực tiếp trong không gian. Theo định nghĩa, góc giữa một đường thẳng và một mặt phẳng là góc giữa đường thẳng đó với hình chiếu vuông góc của nó lên mặt phẳng. S chiếu xuống A, còn C đã nằm trên đáy, vì vậy hình chiếu của SC là AC. Do đó góc cần tìm chính là góc SCA. Đây là bước quyết định; nếu chọn sai hình chiếu thì mọi phép tính phía sau dù đúng cũng không còn giải đúng bài.",
            2.0,
        )

        ca = (p["A"] - p["C"]) / np.linalg.norm(p["A"] - p["C"])
        vertical = np.array([0.0, 0.0, 1.0])
        alpha = math.atan2(3, 4 * math.sqrt(2))
        arc = arc_basis(p["C"], ca, vertical, alpha, radius=0.42)
        self.play(Create(arc), run_time=0.45)

        solution = self.card(
            "Lời giải",
            "Đưa góc không gian về tam giác SAC",
            [
                ("math", "S C -> A C", 29, CYAN),
                ("math", "alpha = hat(S C A, size: #145%)", 31, GOLD),
                ("math", "A C = 4 sqrt(2)", 30, INK),
                ("math", "tan alpha = frac(S A, A C)", 30, INK),
                ("math", "tan alpha = frac(3, 4 sqrt(2))", 34, GOLD),
                ("sep",),
                ("text", "Chỉ cần một giá trị lượng giác thì nên dừng ở đây.", 17, MUTED, NORMAL),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Tam giác SAC vuông tại A. Ta có AC là đường chéo hình vuông cạnh bốn nên AC bằng bốn căn hai. Với alpha là góc SCA, tang alpha bằng cạnh đối SA chia cạnh kề AC, tức bằng ba trên bốn căn hai. Nếu đề chỉ yêu cầu một giá trị lượng giác thì dừng ở đây là đẹp nhất. Một lỗi thường gặp là tiếp tục bấm máy ra số đo góc rồi làm tròn, trong khi kết quả chính xác bằng căn thường có giá trị hơn và phù hợp hơn với câu hỏi trắc nghiệm.",
            2.0,
        )

        self.takeaway("Đường – mặt  →  tìm hình chiếu của đường lên mặt")
        self.wait(0.5)

    # ======================================================
    # 2. DIHEDRAL
    # ======================================================
    def dihedral(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header(
            "Bài 2 · Góc nhị diện",
            "Giữa (SBC) và (ABCD) theo cạnh BC",
            "03 / 07",
        )

        G = self.show_base_model(dim=True, base_fill=0.08)
        p = G["p"]

        face_sbc = face(
            p["S"], p["B"], p["C"],
            color=PURPLE, opacity=0.22,
            stroke=PURPLE, stroke_width=0,
        )
        section_sab = face(
            p["S"], p["A"], p["B"],
            color=GOLD, opacity=0.09,
            stroke=GOLD, stroke_width=0,
        )
        bc = solid(p["B"], p["C"], GOLD, 6.8, 1.0)
        ba = solid(p["B"], p["A"], CYAN, 5.7, 1.0)
        bs = solid(p["B"], p["S"], GREEN, 5.7, 1.0)

        self.play(FadeIn(face_sbc), FadeIn(section_sab), Create(bc), run_time=0.7)

        problem = self.card(
            "Đề bài",
            "Góc nhị diện theo cạnh BC",
            [
                ("text", "Tìm góc giữa hai mặt phẳng (SBC) và (ABCD).", 19, INK, NORMAL),
                ("math", "B C", 31, GOLD),
                ("sep",),
                ("text", "Nguyên tắc:", 18, GOLD, BOLD),
                ("text", "Trong mỗi mặt, chọn một đường cùng vuông góc với cạnh chung BC.", 18, MUTED, NORMAL),
            ],
            accent=PURPLE,
        )

        self.narrate(
            "Với góc nhị diện giữa hai mặt SBC và ABCD, trước hết phải xác định cạnh chung là BC. Muốn biến góc nhị diện thành một góc phẳng, ta chọn trong mỗi mặt một đường cùng vuông góc với BC tại B. Trong đáy, BA vuông góc BC. Mặt khác, AD vuông góc AB và AD cũng vuông góc SA, nên AD vuông góc với mặt phẳng SAB. Vì BC song song AD, suy ra BC vuông góc với mặt phẳng SAB, đặc biệt BC vuông góc BS. Như vậy hai đường cần chọn là BA và BS.",
            2.2,
        )

        self.play(Create(ba), Create(bs), run_time=0.55)

        mark_ba = right_angle_3d(
            p["B"],
            p["C"] - p["B"],
            p["A"] - p["B"],
            size=0.21,
            color=CYAN,
        )
        mark_bs = right_angle_3d(
            p["B"],
            p["C"] - p["B"],
            p["S"] - p["B"],
            size=0.27,
            color=GREEN,
        )
        self.play(FadeIn(mark_ba), FadeIn(mark_bs), run_time=0.45)

        ba_dir = (p["A"] - p["B"]) / np.linalg.norm(p["A"] - p["B"])
        vertical = np.array([0.0, 0.0, 1.0])
        beta = math.atan2(3, 4)
        arc = arc_basis(p["B"], ba_dir, vertical, beta, radius=0.40)
        self.play(Create(arc), run_time=0.45)

        solution = self.card(
            "Lời giải",
            "Đưa góc nhị diện về một góc phẳng",
            [
                ("math", "B A perp B C", 29, CYAN),
                ("math", "B S perp B C", 29, GREEN),
                ("math", "beta = hat(A B S, size: #145%)", 31, GOLD),
                ("math", "S B = 5", 29, INK),
                ("math", "sin beta = frac(3, 5)", 33, GOLD),
                ("math", "tan beta = frac(3, 4)", 33, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Vậy góc nhị diện chính là góc A B S trong mặt phẳng S A B. Tam giác S A B vuông tại A và có ba cạnh ba, bốn, năm. Suy ra sin beta bằng ba phần năm, còn tang beta bằng ba phần bốn. Các em nên phân biệt rất rõ: góc nhị diện không phải là góc giữa hai cạnh bất kỳ nằm trên hai mặt phẳng. Ta chỉ được đọc góc sau khi đã chọn đúng hai đường cùng vuông góc với cạnh chung. Nếu bước dựng này đúng, phần lượng giác phía sau thường rất ngắn.",
            1.9,
        )

        self.takeaway("Góc nhị diện  →  cạnh chung  →  mặt cắt vuông góc cạnh chung")
        self.wait(0.5)

    # ======================================================
    # 3. VOLUME
    # ======================================================
    def volume(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header(
            "Bài 3 · Thể tích hình chóp",
            "Giữ câu dễ thật ngắn",
            "04 / 07",
        )

        G = self.show_base_model(dim=False, base_fill=0.20)
        p = G["p"]

        sa = solid(p["S"], p["A"], GOLD, 6.0, 1.0)
        mark = right_angle_3d(
            p["A"],
            p["B"] - p["A"],
            p["S"] - p["A"],
            size=0.24,
        )
        self.play(Create(sa), FadeIn(mark), run_time=0.55)

        problem = self.card(
            "Đề bài",
            "Tính thể tích S.ABCD",
            [
                ("math", "A B = B C = 4", 30, CYAN),
                ("math", "S A = 3", 30, CYAN),
                ("math", "S A perp (A B C D)", 29, GREEN),
                ("sep",),
                ("text", "Không cần dựng thêm đường phụ.", 18, MUTED, NORMAL),
            ],
            accent=BLUE,
        )
        self.narrate(
            "Ở câu thể tích, dữ kiện đã được đưa về đúng dạng chuẩn: mặt đáy ABCD là hình vuông và S A là đường cao. Vì vậy không cần dựng thêm bất kỳ đường phụ nào. Diện tích đáy bằng bốn nhân bốn, còn chiều cao bằng ba. Đây cũng là một kỹ năng quan trọng trong bài nhiều ý: nhận ra khi nào nên dừng việc dựng hình. Dựng thêm một đường không cần thiết có thể làm che mất quan hệ chính và khiến lời giải dài hơn mà không tạo thêm thông tin.",
            1.5,
        )

        solution = self.card(
            "Lời giải",
            "Dùng trực tiếp đáy × chiều cao",
            [
                ("math", "S_(A B C D) = 4^2 = 16", 30, CYAN),
                ("math", "h = S A = 3", 30, GREEN),
                ("math", "V = frac(1, 3) S_(A B C D) h", 30, INK),
                ("math", "V = frac(1, 3) times 16 times 3", 30, INK),
                ("math", "V = 16", 38, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Diện tích đáy bằng mười sáu và chiều cao bằng ba. Do đó thể tích hình chóp bằng một phần ba nhân mười sáu nhân ba, tức bằng mười sáu. Kết quả này rất đơn giản nhưng không hề thừa: ở bài kế tiếp, ta sẽ dùng chính thể tích để tính một khoảng cách mà nếu dựng trực tiếp thì khá khó. Các em nên tạo thói quen giữ lại những kết quả trung gian như diện tích mặt, độ dài cạnh đặc biệt và thể tích, vì một bài hình học không gian nhiều câu thường được thiết kế để các dữ kiện liên kết với nhau.",
            1.5,
        )

        self.takeaway("Dữ kiện đã cho đúng đáy và chiều cao  →  tính thẳng, không dựng thêm")
        self.wait(0.4)

    # ======================================================
    # 4. DISTANCE TO PLANE
    # ======================================================
    def distance(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header(
            "Bài 4 · Khoảng cách từ điểm đến mặt phẳng",
            "Từ D đến mặt phẳng (SBC)",
            "05 / 07",
        )

        G = self.show_base_model(dim=True, base_fill=0.06)
        p = G["p"]

        sbc = face(
            p["S"], p["B"], p["C"],
            color=PURPLE, opacity=0.25,
            stroke=PURPLE, stroke_width=2.1,
        )

        # Logical foot H = (-14/25, 2, 48/25)
        H = L(-14/25, 2, 48/25)
        dh = solid(p["D"], H, GOLD, 6.0, 1.0)
        hdot = Dot3D(H, radius=0.052, color=GOLD)

        bc_dir = (p["C"] - p["B"]) / np.linalg.norm(p["C"] - p["B"])
        helper_in_plane = aux(
            H - 0.44 * bc_dir,
            H + 0.44 * bc_dir,
            color=CYAN,
            width=3.2,
            opacity=0.78,
        )
        marker = right_angle_3d(
            H,
            p["D"] - H,
            bc_dir,
            size=0.18,
            color=GOLD,
        )

        self.play(FadeIn(sbc), Create(dh), FadeIn(hdot), Create(helper_in_plane), FadeIn(marker), run_time=0.8)

        problem = self.card(
            "Đề bài",
            "Tính d(D,(SBC))",
            [
                ("text", "Có thể dựng chân H, nhưng xác định H trực tiếp không đẹp.", 18, INK, NORMAL),
                ("sep",),
                ("text", "Gợi ý chiến lược:", 18, GOLD, BOLD),
                ("text", "Đổi khoảng cách thành chiều cao của tứ diện SBCD.", 18, MUTED, NORMAL),
            ],
            accent=PURPLE,
        )

        self.narrate(
            "Khoảng cách từ D đến mặt phẳng SBC là độ dài đoạn vuông góc DH. Ta có thể cố dựng chính xác H rồi tính DH, nhưng trong cấu hình này cách đó dài và dễ mắc sai sót. Một hướng đẹp hơn là xem tứ diện SBCD theo hai cách. Nếu chọn tam giác SBC làm đáy thì chiều cao tương ứng chính là khoảng cách cần tìm. Vì vậy ta chỉ cần biết thể tích tứ diện SBCD và diện tích tam giác SBC, không cần xác định tọa độ hay vị trí cụ thể của H.",
            1.9,
        )

        solution = self.card(
            "Lời giải",
            "Đổi khoảng cách thành thể tích",
            [
                ("math", "V_(S B C D) = frac(1, 2) V_(S A B C D) = 8", 27, CYAN),
                ("math", "S B = 5", 28, INK),
                ("math", "S_(S B C) = frac(1, 2) times 5 times 4 = 10", 27, GREEN),
                ("math", "8 = frac(1, 3) times 10 times d", 29, INK),
                ("math", "d = frac(12, 5)", 38, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Tam giác BCD có diện tích bằng một nửa diện tích hình vuông ABCD. Tứ diện SBCD và hình chóp SABCD có cùng chiều cao từ S xuống mặt đáy, nên thể tích tứ diện bằng một nửa, tức bằng tám. Tam giác SBC vuông tại B vì SB vuông góc BC; với SB bằng năm và BC bằng bốn, diện tích tam giác SBC bằng mười. Chọn SBC làm đáy, ta có tám bằng một phần ba nhân mười nhân d. Từ đó khoảng cách bằng mười hai phần năm.",
            2.1,
        )

        self.takeaway("Khoảng cách khó dựng  →  xem nó có thể trở thành chiều cao của một tứ diện hay không")
        self.wait(0.5)

    # ======================================================
    # 5. PARALLEL SECTION + RATIOS
    # ======================================================
    def section_ratio(self):
        self.clear_all()
        self.set_camera_orientation(phi=VIEW_PHI, theta=VIEW_THETA, zoom=VIEW_ZOOM)
        self.add_header(
            "Bài 5 · Thiết diện và tỷ số thể tích",
            "M, N, P, Q là trung điểm bốn cạnh bên",
            "06 / 07",
        )

        G = self.show_base_model(dim=True, base_fill=0.09)
        p = G["p"]

        M = (p["S"] + p["A"]) / 2
        N = (p["S"] + p["B"]) / 2
        Pp = (p["S"] + p["C"]) / 2
        Q = (p["S"] + p["D"]) / 2

        sec = face(
            M, N, Pp, Q,
            color=GOLD, opacity=0.31,
            stroke=GOLD, stroke_width=0,
        )
        sec_edges = VGroup(
            solid(M, N, GOLD, 4.2, 1.0),
            solid(N, Pp, GOLD, 4.2, 1.0),
            solid(Pp, Q, GOLD, 4.2, 1.0),
            solid(Q, M, GOLD, 4.2, 1.0),
        )
        dots = VGroup(*[Dot3D(X, radius=0.048, color=GOLD) for X in [M, N, Pp, Q]])
        self.play(FadeIn(sec), Create(sec_edges), FadeIn(dots), run_time=0.75)

        for name, X, off in [
            ("M", M, np.array([-0.15, -0.14, 0.10])),
            ("N", N, np.array([ 0.13, -0.12, 0.08])),
            ("P", Pp,np.array([ 0.13,  0.12, 0.07])),
            ("Q", Q, np.array([-0.15,  0.12, 0.07])),
        ]:
            lab = mty(name, 22, GOLD)
            lab.move_to(X + off)
            self.add_fixed_orientation_mobjects(lab)

        problem = self.card(
            "Đề bài",
            "Thiết diện qua bốn trung điểm",
            [
                ("text", "M, N, P, Q lần lượt là trung điểm của SA, SB, SC, SD.", 18, INK, NORMAL),
                ("sep",),
                ("text", "Tìm:", 18, GOLD, BOLD),
                ("text", "• quan hệ giữa (MNPQ) và đáy", 18, MUTED, NORMAL),
                ("text", "• tỷ số diện tích hai thiết diện", 18, MUTED, NORMAL),
                ("text", "• tỷ số thể tích hai hình chóp", 18, MUTED, NORMAL),
            ],
            accent=GOLD,
        )

        self.narrate(
            "Bốn điểm M, N, P, Q là trung điểm của bốn cạnh bên nên chúng cùng chia các đoạn SA, SB, SC, SD theo tỷ số một phần hai tính từ S. Theo định lý về mặt phẳng song song với đáy trong hình chóp, MNPQ song song với ABCD. Vì vậy hình chóp nhỏ S.MNPQ đồng dạng với hình chóp lớn S.ABCD với tỷ số đồng dạng bằng một phần hai. Đây là một cấu hình rất quan trọng vì từ một tỷ số độ dài ta suy ra ngay được tỷ số diện tích và tỷ số thể tích.",
            1.7,
        )

        solution = self.card(
            "Lời giải",
            "Từ đồng dạng suy ra bình phương và lập phương",
            [
                ("math", "frac(S M, S A) = frac(S N, S B) = frac(1, 2)", 28, CYAN),
                ("math", "(M N P Q) parallel (A B C D)", 28, GREEN),
                ("math", "frac(S_(M N P Q), S_(A B C D)) = frac(1, 2)^2 = frac(1, 4)", 26, INK),
                ("math", "frac(V_(S M N P Q), V_(S A B C D)) = frac(1, 2)^3", 26, INK),
                ("math", "= frac(1, 8)", 38, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Vì tỷ số đồng dạng bằng một phần hai, tỷ số diện tích của hai đáy tương ứng bằng bình phương, tức một phần tư. Tỷ số thể tích của hai hình chóp đồng dạng bằng lập phương, tức một phần tám. Nếu các điểm không phải trung điểm mà cùng thỏa SM trên SA bằng SN trên SB bằng SP trên SC bằng SQ trên SD bằng k, thì công thức tổng quát là tỷ số diện tích bằng k bình phương và tỷ số thể tích bằng k lập phương.",
            1.8,
        )

        self.narrate_camera(
            "Hãy chú ý hai mặt MNPQ và ABCD có các cạnh tương ứng song song. Điều đó giúp ta nhận ra ngay quan hệ đồng dạng giữa hai hình chóp có chung đỉnh S. Trong bài thi, nếu đã phát hiện mặt cắt song song với đáy thì thường không cần tính từng cạnh của thiết diện. Chỉ cần tìm tỷ số trên một cạnh bên rồi nâng lên lũy thừa hai hoặc ba tùy đại lượng cần hỏi.",
            phi=72 * DEGREES,
            theta=-42 * DEGREES,
            zoom=0.97,
        )

        self.takeaway("Thiết diện song song đáy  →  đồng dạng  →  diện tích theo k², thể tích theo k³")
        self.wait(0.5)

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)
        self.add_header(
            "Bản đồ tư duy",
            "Một cấu hình – năm cách nhìn",
            "07 / 07",
        )

        left_panel = RoundedRectangle(
            width=7.5, height=5.15, corner_radius=0.18,
            fill_color=PANEL, fill_opacity=0.95,
            stroke_color=GRID, stroke_width=1.2,
        ).move_to(LEFT * 2.55 + DOWN * 0.06)

        rows = VGroup(
            VGroup(txt("01", 20, GOLD, BOLD), txt("Góc đường – mặt", 22, INK, BOLD), txt("→ hình chiếu", 22, CYAN, BOLD)).arrange(RIGHT, buff=0.18),
            VGroup(txt("02", 20, GOLD, BOLD), txt("Góc nhị diện", 22, INK, BOLD), txt("→ mặt cắt ⟂ cạnh chung", 22, CYAN, BOLD)).arrange(RIGHT, buff=0.18),
            VGroup(txt("03", 20, GOLD, BOLD), txt("Thể tích", 22, INK, BOLD), txt("→ đáy × chiều cao", 22, CYAN, BOLD)).arrange(RIGHT, buff=0.18),
            VGroup(txt("04", 20, GOLD, BOLD), txt("Khoảng cách khó", 22, INK, BOLD), txt("→ đổi sang thể tích", 22, CYAN, BOLD)).arrange(RIGHT, buff=0.18),
            VGroup(txt("05", 20, GOLD, BOLD), txt("Thiết diện song song", 22, INK, BOLD), txt("→ đồng dạng & tỷ số", 22, CYAN, BOLD)).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.43)
        rows.move_to(left_panel)

        self.add_fixed_in_frame_mobjects(left_panel, rows)
        self.play(FadeIn(left_panel), FadeIn(rows, shift=RIGHT * 0.10), run_time=0.7)

        card = self.card(
            "Kết quả",
            "Năm đáp số của cấu hình",
            [
                ("math", "tan alpha = frac(3, 4 sqrt(2))", 28, INK),
                ("math", "sin beta = frac(3, 5)", 28, INK),
                ("math", "V = 16", 30, INK),
                ("math", "d(D, (S B C)) = frac(12, 5)", 28, INK),
                ("math", "frac(V_(S M N P Q), V_(S A B C D)) = frac(1, 8)", 25, GOLD),
            ],
            accent=GOLD,
        )

        self.narrate(
            "Từ cùng một hình chóp, ta đã dùng năm cách nhìn khác nhau. Góc giữa đường và mặt được đưa về hình chiếu. Góc nhị diện được đưa về một mặt cắt vuông góc cạnh chung. Thể tích dùng trực tiếp đáy và chiều cao. Khoảng cách điểm đến mặt phẳng được biến thành chiều cao của một tứ diện. Thiết diện song song được xử lý bằng đồng dạng. Khi làm hình học không gian, các em nên tự hỏi bài toán đang muốn mình tìm một hình chiếu, một mặt cắt, một chiều cao hay một tỷ số đồng dạng; câu hỏi đó thường chỉ ra lời giải ngắn nhất.",
            2.0,
        )

        self.clear_all()
        end = VGroup(
            txt("HHKG CHUYÊN SÂU", 42, GOLD, BOLD),
            txt("Hình chuẩn trước · công thức sau", 28, CYAN, BOLD),
            txt("Video 02: Khoảng cách trong không gian", 23, INK),
            txt("Điểm – mặt · hai đường chéo nhau · đường vuông góc chung", 20, MUTED),
            txt(TEN_THAY, 18, MUTED),
        ).arrange(DOWN, buff=0.28)
        self.add_fixed_in_frame_mobjects(end)
        self.play(FadeIn(end), run_time=0.8)
        self.narrate(
            "Video tiếp theo sẽ đi sâu vào khoảng cách trong không gian: khoảng cách từ điểm đến mặt phẳng, từ đường thẳng đến mặt phẳng song song, khoảng cách giữa hai đường chéo nhau và cách dựng đường vuông góc chung. Ta sẽ gặp cả những cấu hình mà chân vuông góc rất khó nhìn, nhưng có thể giải gọn bằng thể tích, mặt phẳng phụ hoặc tọa độ hóa có kiểm soát.",
            1.6,
        )

    def construct(self):
        self.intro()
        self.configuration()
        self.line_plane_angle()
        self.dihedral()
        self.volume()
        self.distance()
        self.section_ratio()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_01_manim_typst_MASTER_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst)")
    print("Visual system: HHKG MASTER - fixed camera, correct hidden edges, MathTypst")

    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_01_master.wav"
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

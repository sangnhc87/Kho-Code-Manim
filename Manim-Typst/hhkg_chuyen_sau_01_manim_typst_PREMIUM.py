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
# HHKG CHUYEN SAU 01 - MANIM + TYPST - PREMIUM LAYOUT
# Standalone 100% for GitHub Actions
#
# Visual grammar:
#   - Actual polyhedron edges: solid
#   - Auxiliary / projection lines: dashed
#   - Irrelevant geometry: dimmed, never confused with hidden edges
#   - 2-column layout: 3D figure left, problem/solution card right
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
GEO_SHIFT = np.array([-1.75, 0.0, -0.10])


def L(x, y, z):
    """Logical geometry -> scene geometry."""
    return GEO_SCALE * np.array([float(x), float(y), float(z)]) + GEO_SHIFT


def solid(a, b, color=EDGE, width=4.0, opacity=0.94):
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def aux(a, b, color=CYAN, width=3.7, opacity=0.90, dash=0.13):
    return DashedLine(
        a, b,
        color=color,
        stroke_width=width,
        stroke_opacity=opacity,
        dash_length=dash,
        dashed_ratio=0.58,
    )


def face(*points, color=BLUE, opacity=0.10, stroke=BLUE, stroke_width=1.6):
    return Polygon(
        *points,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=stroke_width,
        stroke_opacity=0.55,
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
            phi=68 * DEGREES,
            theta=-52 * DEGREES,
            zoom=0.92,
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
        audio = create_audio(text)
        dur = probe_duration(audio)
        self.audio_events.append((self.time, audio))
        kwargs["run_time"] = max(dur, 1.8)
        self.move_camera(**kwargs)
        return dur

    # ------------------------------------------------------
    # FIXED 2-COLUMN UI
    # ------------------------------------------------------
    def clear_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.32)
        self.clear()

    def add_header(self, title, subtitle, progress):
        tag = VGroup(
            RoundedRectangle(
                width=1.38, height=0.42, corner_radius=0.08,
                fill_color=PANEL_2, fill_opacity=1,
                stroke_color=BLUE, stroke_width=1.2, stroke_opacity=0.55,
            ),
            txt("HHKG / 01", 16, BLUE, BOLD),
        )
        tag[1].move_to(tag[0])

        title_m = fit_width(txt(title, 31, INK, BOLD), 8.8)
        sub_m = fit_width(txt(subtitle, 18, MUTED), 8.9)
        texts = VGroup(title_m, sub_m).arrange(DOWN, aligned_edge=LEFT, buff=0.055)

        header = VGroup(tag, texts).arrange(RIGHT, buff=0.28, aligned_edge=UP)
        header.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.26)

        prog = txt(progress, 17, MUTED, BOLD)
        prog.to_edge(UP, buff=0.23).to_edge(RIGHT, buff=0.34)

        rule = Line(
            LEFT * 6.8, RIGHT * 6.8,
            color=GRID, stroke_width=1.1, stroke_opacity=0.55
        ).shift(UP * 2.94)

        teacher = txt(TEN_THAY, 16, MUTED)
        teacher.to_edge(DOWN, buff=0.12).to_edge(LEFT, buff=0.30)

        note = txt("Hình 3D minh họa – không nhất thiết theo tỷ lệ", 15, DIM)
        note.to_edge(DOWN, buff=0.12).shift(LEFT * 1.8)

        divider = Line(
            np.array([1.52, -2.88, 0]),
            np.array([1.52, 2.74, 0]),
            color=GRID, stroke_width=1.15, stroke_opacity=0.52,
        )

        self.add_fixed_in_frame_mobjects(header, prog, rule, teacher, note, divider)
        return VGroup(header, prog, rule, teacher, note, divider)

    def card(self, kicker, title, items, accent=GOLD, height=5.25, auto_add=True):
        bg = RoundedRectangle(
            width=5.05,
            height=height,
            corner_radius=0.18,
            fill_color=PANEL,
            fill_opacity=0.97,
            stroke_color=GRID,
            stroke_width=1.35,
            stroke_opacity=0.90,
        ).move_to(RIGHT * 4.28 + DOWN * 0.04)

        accent_line = Line(
            bg.get_corner(UL) + RIGHT * 0.26 + DOWN * 0.28,
            bg.get_corner(UL) + RIGHT * 1.15 + DOWN * 0.28,
            color=accent, stroke_width=5.5,
        )

        k = txt(kicker.upper(), 16, accent, BOLD)
        k.next_to(accent_line, DOWN, buff=0.13, aligned_edge=LEFT)

        t = fit_width(txt(title, 25, INK, BOLD), 4.40)
        t.next_to(k, DOWN, buff=0.12, aligned_edge=LEFT)

        body = VGroup()
        for item in items:
            kind = item[0]
            if kind == "text":
                _, s, size, color, weight = item
                mob = txt(s, size, color, weight)
            elif kind == "math":
                _, s, size, color = item
                mob = mty(s, size, color)
            elif kind == "sep":
                mob = Line(LEFT * 2.0, RIGHT * 2.0, color=GRID, stroke_width=1)
            elif kind == "obj":
                mob = item[1]
            else:
                raise ValueError(f"Unknown card item: {kind}")
            body.add(fit_width(mob, 4.40))

        body.arrange(DOWN, aligned_edge=LEFT, buff=0.19)
        body.next_to(t, DOWN, buff=0.25, aligned_edge=LEFT)
        fit_height(body, height - 1.72)

        group = VGroup(bg, accent_line, k, t, body)
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
        pill = RoundedRectangle(
            width=7.45, height=0.48, corner_radius=0.12,
            fill_color=PANEL_2, fill_opacity=0.96,
            stroke_color=BLUE, stroke_width=1.0, stroke_opacity=0.40,
        ).move_to(LEFT * 2.55 + DOWN * 2.53)
        label = fit_width(txt(text_s, 17, CYAN, BOLD), 6.95).move_to(pill)
        g = VGroup(pill, label)
        self.add_fixed_in_frame_mobjects(g)
        return g

    def legend(self):
        a = Line(LEFT * 0.30, RIGHT * 0.30, color=EDGE, stroke_width=4)
        b = DashedLine(LEFT * 0.30, RIGHT * 0.30, color=CYAN, stroke_width=3.5, dash_length=0.09)
        la = txt("cạnh / đường đang xét", 15, MUTED)
        lb = txt("đường phụ / hình chiếu", 15, MUTED)
        r1 = VGroup(a, la).arrange(RIGHT, buff=0.10)
        r2 = VGroup(b, lb).arrange(RIGHT, buff=0.10)
        g = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        g.move_to(LEFT * 4.45 + DOWN * 2.17)
        self.add_fixed_in_frame_mobjects(g)
        return g

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
        edge_color = DIM if dim else EDGE
        edge_opacity = 0.38 if dim else 0.90
        edge_width = 2.6 if dim else 3.8

        base = face(
            p["A"], p["B"], p["C"], p["D"],
            color=BLUE, opacity=base_fill,
            stroke=BLUE, stroke_width=1.3,
        )

        # Actual polyhedron edges remain solid because the camera moves.
        # Depth is encoded by transparency + dimming, while dashed style is
        # reserved for auxiliary/projection lines.
        edges = VGroup(
            solid(p["A"], p["B"], edge_color, edge_width, edge_opacity),
            solid(p["B"], p["C"], edge_color, edge_width, edge_opacity),
            solid(p["C"], p["D"], edge_color, edge_width, edge_opacity),
            solid(p["D"], p["A"], edge_color, edge_width, edge_opacity),
            solid(p["S"], p["A"], edge_color, edge_width, edge_opacity),
            solid(p["S"], p["B"], edge_color, edge_width, edge_opacity),
            solid(p["S"], p["C"], edge_color, edge_width, edge_opacity),
            solid(p["S"], p["D"], edge_color, edge_width, edge_opacity),
        )

        dots = VGroup(
            Dot3D(p["A"], radius=0.055, color=GOLD),
            Dot3D(p["B"], radius=0.055, color=GOLD),
            Dot3D(p["C"], radius=0.055, color=GOLD),
            Dot3D(p["D"], radius=0.055, color=GOLD),
            Dot3D(p["S"], radius=0.062, color=RED),
        )

        return {"p": p, "base": base, "edges": edges, "dots": dots}

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

        tag = VGroup(
            RoundedRectangle(
                width=2.1, height=0.52, corner_radius=0.10,
                fill_color=PANEL_2, fill_opacity=1,
                stroke_color=BLUE, stroke_width=1.1,
            ),
            txt("SERIES HHKG CHUYÊN SÂU", 17, BLUE, BOLD),
        )
        tag[1].move_to(tag[0])

        title = txt("MỘT CẤU HÌNH – NHIỀU ĐẠI LƯỢNG", 43, INK, BOLD)
        sub = txt("Góc · góc nhị diện · khoảng cách · thể tích · tỷ số", 25, CYAN, BOLD)
        note = txt("Nhìn cấu hình trước, chọn công cụ sau", 23, MUTED)
        brand = txt(TEN_THAY, 18, MUTED)

        g = VGroup(tag, title, sub, note, brand).arrange(DOWN, buff=0.28)
        self.play(FadeIn(tag), FadeIn(title, shift=UP * 0.16), run_time=0.75)
        self.play(FadeIn(sub), FadeIn(note), FadeIn(brand), run_time=0.80)
        self.narrate(
            "Chào các em. Video đầu tiên của series hình học không gian chuyên sâu sẽ dùng đúng một hình chóp để khai thác năm bài toán khác nhau. Ta sẽ không chất công thức lên màn hình. Mỗi cảnh được bố trí hai cột: hình ba chiều ở bên trái, còn đề bài và lời giải ở bên phải. Các cạnh thật của khối được vẽ liền; đường phụ và hình chiếu được vẽ nét đứt. Mục tiêu là để mắt nhìn thấy cấu trúc trước khi tay bắt đầu tính.",
            2.0,
        )

    # ======================================================
    # CONFIGURATION
    # ======================================================
    def configuration(self):
        self.clear_all()
        self.set_camera_orientation(phi=67 * DEGREES, theta=-54 * DEGREES, zoom=0.97)
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
            "Ta xét hình chóp S.ABCD có đáy là hình vuông cạnh bốn, SA bằng ba và vuông góc với mặt phẳng đáy. Hình đã được thu nhỏ và đặt hẳn về bên trái để không bị phần lời giải che lên. Các cạnh của khối đều là nét liền. Chỉ khi xuất hiện đường chiếu, đường phụ hoặc một đường dựng thêm, ta mới dùng nét đứt.",
            1.8,
        )

        self.narrate_camera(
            "Ta xoay camera một góc nhỏ, vừa đủ để nhìn rõ chiều sâu. Không quay quá nhiều vì mục tiêu của hình động là làm sáng cấu trúc, không phải trình diễn. Hãy để ý cạnh SA là đường cao, còn mặt đáy xanh nhạt chỉ dùng để định vị không gian.",
            phi=71 * DEGREES,
            theta=-46 * DEGREES,
            zoom=0.97,
        )

    # ======================================================
    # 1. LINE - PLANE ANGLE
    # ======================================================
    def line_plane_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=66 * DEGREES, theta=-48 * DEGREES, zoom=0.98)
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
            "Muốn tìm góc giữa SC và mặt phẳng đáy, ta không chọn một góc bất kỳ nhìn có vẻ hợp lý. Trước hết phải chiếu đường SC xuống mặt đáy. S chiếu xuống A, còn C vốn đã nằm trong đáy. Vì vậy hình chiếu của SC chính là AC. Đường AC được vẽ nét đứt màu xanh để phân biệt rõ với các cạnh thật của hình chóp.",
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
                ("math", "alpha = angle S C A", 31, GOLD),
                ("math", "A C = 4 sqrt(2)", 30, INK),
                ("math", "tan alpha = (S A)/(A C)", 30, INK),
                ("math", "tan alpha = 3/(4 sqrt(2))", 34, GOLD),
                ("sep",),
                ("text", "Chỉ cần một giá trị lượng giác thì nên dừng ở đây.", 17, MUTED, NORMAL),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Góc cần tìm là góc SCA. Từ đây bài toán hoàn toàn nằm trong tam giác vuông SAC. Đường chéo AC của hình vuông cạnh bốn bằng bốn căn hai. Do đó tang alpha bằng SA trên AC, tức ba trên bốn căn hai. Đây là lời giải ngắn vì ta đã chọn đúng hình chiếu ngay từ đầu.",
            2.0,
        )

        self.takeaway("Đường – mặt  →  tìm hình chiếu của đường lên mặt")
        self.wait(0.5)

    # ======================================================
    # 2. DIHEDRAL
    # ======================================================
    def dihedral(self):
        self.clear_all()
        self.set_camera_orientation(phi=69 * DEGREES, theta=-56 * DEGREES, zoom=0.97)
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
            stroke=PURPLE, stroke_width=2.2,
        )
        section_sab = face(
            p["S"], p["A"], p["B"],
            color=GOLD, opacity=0.09,
            stroke=GOLD, stroke_width=1.7,
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
            "Ở góc nhị diện, cạnh chung BC phải được xác định trước. Sau đó ta cần một mặt cắt vuông góc với BC. Tam giác SAB chính là mặt cắt rất đẹp của cấu hình này. Trong đáy, BA vuông góc BC. Đồng thời BC song song AD, còn AD vuông góc cả AB lẫn SA, nên BC vuông góc với mặt phẳng SAB. Vì thế BS cũng vuông góc BC.",
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
            "Đưa góc nhị diện về ∠ABS",
            [
                ("math", "B A perp B C", 29, CYAN),
                ("math", "B S perp B C", 29, GREEN),
                ("math", "beta = angle A B S", 31, GOLD),
                ("math", "S B = 5", 29, INK),
                ("math", "sin beta = 3/5", 33, GOLD),
                ("math", "tan beta = 3/4", 33, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Vậy góc nhị diện chính là góc ABS. Tam giác SAB vuông tại A và có ba cạnh ba, bốn, năm. Suy ra sin beta bằng ba phần năm, còn tang beta bằng ba phần bốn. Điểm quan trọng không nằm ở phép tính, mà ở việc dựng được mặt cắt vuông góc cạnh chung.",
            1.9,
        )

        self.takeaway("Góc nhị diện  →  cạnh chung  →  mặt cắt vuông góc cạnh chung")
        self.wait(0.5)

    # ======================================================
    # 3. VOLUME
    # ======================================================
    def volume(self):
        self.clear_all()
        self.set_camera_orientation(phi=65 * DEGREES, theta=-48 * DEGREES, zoom=0.99)
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
            "Câu thể tích cố ý được giữ rất sạch. Đáy đã là hình vuông, còn SA đã là đường cao. Khi dữ kiện đã cho đúng đáy và đúng chiều cao, không nên dựng thêm đường phụ làm hình rối hơn.",
            1.5,
        )

        solution = self.card(
            "Lời giải",
            "Dùng trực tiếp đáy × chiều cao",
            [
                ("math", "S_(A B C D) = 4^2 = 16", 30, CYAN),
                ("math", "h = S A = 3", 30, GREEN),
                ("math", "V = 1/3 S_(A B C D) h", 30, INK),
                ("math", "V = 1/3 times 16 times 3", 30, INK),
                ("math", "V = 16", 38, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Diện tích đáy bằng mười sáu, chiều cao bằng ba. Vì vậy thể tích bằng một phần ba nhân mười sáu nhân ba, tức mười sáu. Ta sẽ giữ kết quả này để dùng tiếp ở bài khoảng cách.",
            1.5,
        )

        self.takeaway("Dữ kiện đã cho đúng đáy và chiều cao  →  tính thẳng, không dựng thêm")
        self.wait(0.4)

    # ======================================================
    # 4. DISTANCE TO PLANE
    # ======================================================
    def distance(self):
        self.clear_all()
        self.set_camera_orientation(phi=71 * DEGREES, theta=-57 * DEGREES, zoom=0.97)
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
            "Đoạn vàng DH cho ta hình ảnh đúng của khoảng cách từ D tới mặt phẳng SBC. Nhưng nếu cố tìm vị trí H bằng hình học thuần túy, lời giải sẽ dài. Ta chỉ cần biết DH là chiều cao của tứ diện SBCD khi chọn mặt SBC làm đáy. Vì thế thể tích sẽ thay ta tìm khoảng cách.",
            1.9,
        )

        solution = self.card(
            "Lời giải",
            "Đổi khoảng cách thành thể tích",
            [
                ("math", "V_(S B C D) = 1/2 V_(S A B C D) = 8", 27, CYAN),
                ("math", "S B = 5", 28, INK),
                ("math", "S_(S B C) = 1/2 times 5 times 4 = 10", 27, GREEN),
                ("math", "8 = 1/3 times 10 times d", 29, INK),
                ("math", "d = 12/5", 38, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Tam giác BCD bằng một nửa hình vuông ABCD và có cùng chiều cao SA, nên thể tích tứ diện SBCD bằng tám. Tam giác SBC vuông tại B, với SB bằng năm và BC bằng bốn, nên diện tích bằng mười. Dùng SBC làm đáy: tám bằng một phần ba nhân mười nhân d. Suy ra d bằng mười hai phần năm.",
            2.1,
        )

        self.takeaway("Khoảng cách khó dựng  →  xem nó có thể trở thành chiều cao của một tứ diện hay không")
        self.wait(0.5)

    # ======================================================
    # 5. PARALLEL SECTION + RATIOS
    # ======================================================
    def section_ratio(self):
        self.clear_all()
        self.set_camera_orientation(phi=68 * DEGREES, theta=-49 * DEGREES, zoom=0.97)
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
            stroke=GOLD, stroke_width=2.8,
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
            "Bốn trung điểm cùng chia các cạnh xuất phát từ S theo tỷ số một phần hai. Vì vậy thiết diện MNPQ song song với đáy. Hình chóp nhỏ S.MNPQ đồng dạng với hình chóp lớn S.ABCD theo tỷ số dài một phần hai.",
            1.7,
        )

        solution = self.card(
            "Lời giải",
            "Từ đồng dạng suy ra bình phương và lập phương",
            [
                ("math", "S M/S A = S N/S B = 1/2", 28, CYAN),
                ("math", "(M N P Q) parallel (A B C D)", 28, GREEN),
                ("math", "S_(M N P Q)/S_(A B C D) = (1/2)^2 = 1/4", 26, INK),
                ("math", "V_(S M N P Q)/V_(S A B C D) = (1/2)^3", 26, INK),
                ("math", "= 1/8", 38, GOLD),
            ],
            accent=GOLD,
            auto_add=False,
        )
        self.swap_card(problem, solution)

        self.narrate(
            "Tỷ số diện tích bằng bình phương tỷ số đồng dạng nên bằng một phần tư. Tỷ số thể tích bằng lập phương tỷ số đồng dạng nên bằng một phần tám. Đây là quy luật cần nhìn ra ngay khi một mặt phẳng cắt các cạnh bên theo cùng một tỷ số.",
            1.8,
        )

        self.narrate_camera(
            "Ta xoay nhẹ hình để kiểm tra trực quan rằng thiết diện vàng luôn song song với đáy. Mức quay chỉ vừa đủ cho các em cảm nhận chiều sâu, còn bố cục hai cột vẫn giữ nguyên để mắt không phải chạy khắp màn hình.",
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
                ("math", "tan alpha = 3/(4 sqrt(2))", 28, INK),
                ("math", "sin beta = 3/5", 28, INK),
                ("math", "V = 16", 30, INK),
                ("math", "d(D,(S B C)) = 12/5", 28, INK),
                ("math", "V_(S M N P Q)/V_(S A B C D) = 1/8", 25, GOLD),
            ],
            accent=GOLD,
        )

        self.narrate(
            "Từ cùng một hình chóp, ta đã rút ra năm chiến lược. Góc đường với mặt bắt đầu từ hình chiếu. Góc nhị diện bắt đầu từ cạnh chung và mặt cắt vuông góc. Thể tích phải giữ lời giải ngắn khi đáy và chiều cao đã có sẵn. Khoảng cách khó dựng có thể đổi thành thể tích. Thiết diện song song kéo theo đồng dạng, bình phương cho diện tích và lập phương cho thể tích.",
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
            "Từ video sau, ta đi sâu riêng vào khoảng cách trong không gian, đặc biệt là khoảng cách giữa hai đường chéo nhau và đường vuông góc chung. Toàn bộ series vẫn giữ bố cục hai cột và quy ước nét vẽ thống nhất như video này.",
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
    config.output_file = "hhkg_chuyen_sau_01_manim_typst_PREMIUM_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst)")
    print("Layout: premium two-column geometry lesson")

    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_01_premium.wav"
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

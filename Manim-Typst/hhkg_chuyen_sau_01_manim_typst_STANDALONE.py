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
# HHKG CHUYEN SAU 01 - MANIM + TYPST
# Standalone 100% for GitHub Actions
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
config.background_color = "#0B1120"

ROOT = Path.cwd()
AUDIO_DIR = ROOT / "audio_cache"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR = ROOT / "media"

# ==========================================================
# COLORS
# ==========================================================
BG = "#0B1120"
PANEL = "#0E1D34"
INK = "#EDF4FF"
MUTED = "#7A9ABF"
BLUE = "#38BDF8"
CYAN = "#3ADEC8"
GOLD = "#FFD700"
GREEN = "#4ADE80"
RED = "#FF6B6B"
ORANGE = "#FB923C"
PURPLE = "#C084FC"

# ==========================================================
# TYPOGRAPHY HELPERS
# ==========================================================
def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


def mty(s, size=38, color=INK):
    # Manim 0.21 native Typst math renderer.
    return MathTypst(s, font_size=size, color=color)


def fit_width(mob, width=12.2):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def panel(width=5.5, height=4.7):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        fill_color=PANEL,
        fill_opacity=0.93,
        stroke_color=MUTED,
        stroke_opacity=0.28,
        stroke_width=1.4,
    )


def title_group(title, subtitle=None):
    t = fit_width(txt(title, 36, INK, BOLD), 12.0).to_edge(UP, buff=0.22)
    if subtitle:
        s = fit_width(txt(subtitle, 22, MUTED), 11.5).next_to(t, DOWN, buff=0.08)
        return VGroup(t, s)
    return VGroup(t)


def footer(progress=""):
    a = txt(TEN_THAY, 18, MUTED)
    b = txt(progress, 18, MUTED)
    a.to_edge(DOWN, buff=0.16).to_edge(LEFT, buff=0.34)
    b.to_edge(DOWN, buff=0.16).to_edge(RIGHT, buff=0.34)
    return VGroup(a, b)

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
        except Exception as e:
            last_err = e
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

    filter_complex = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={len(events)}:duration=longest:normalize=0[m]"
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error", *inputs,
            "-filter_complex", filter_complex,
            "-map", "[m]", "-ar", "48000", "-ac", "2",
            "-t", f"{video_duration:.3f}", str(out_wav),
        ],
        check=True,
    )


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-i", str(video), "-i", str(audio),
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(out),
        ],
        check=True,
    )

# ==========================================================
# 3D GEOMETRY HELPERS
# ==========================================================
def P(x, y, z):
    return np.array([float(x), float(y), float(z)])


def seg(a, b, color=INK, width=4, opacity=1.0):
    return Line(a, b, color=color, stroke_width=width, stroke_opacity=opacity)


def face(*points, color=BLUE, opacity=0.16, stroke=BLUE, stroke_width=2):
    return Polygon(
        *points,
        fill_color=color,
        fill_opacity=opacity,
        stroke_color=stroke,
        stroke_width=stroke_width,
    )


def arc_in_plane(center, e1, e2, angle, radius=0.65, color=GOLD, width=6):
    e1 = np.array(e1, dtype=float) / np.linalg.norm(e1)
    e2 = np.array(e2, dtype=float) / np.linalg.norm(e2)
    return ParametricFunction(
        lambda t: center + radius * (math.cos(t) * e1 + math.sin(t) * e2),
        t_range=[0, angle],
        color=color,
        stroke_width=width,
    )

# ==========================================================
# MAIN SCENE
# ==========================================================
class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.92)

    # ---------- narration ----------
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

    # ---------- fixed HUD ----------
    def add_hud(self, title, subtitle, progress):
        h = title_group(title, subtitle)
        f = footer(progress)
        self.add_fixed_in_frame_mobjects(h, f)
        return h, f

    def formula_box(self, lines, width=5.5, height=4.7, shift=RIGHT*3.65 + DOWN*0.05):
        bg = panel(width, height).move_to(shift)
        group = VGroup()
        for item in lines:
            if isinstance(item, Mobject):
                mob = item
            else:
                mob = txt(str(item), 24, INK)
            group.add(mob)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(bg)
        fit_width(group, width - 0.55)
        self.add_fixed_in_frame_mobjects(bg, group)
        return VGroup(bg, group)

    def clear_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.42)
        self.clear()

    # ---------- base configuration ----------
    def config_points(self):
        A = P(-2, -2, 0)
        B = P( 2, -2, 0)
        C = P( 2,  2, 0)
        D = P(-2,  2, 0)
        S = P(-2, -2, 3)
        return A, B, C, D, S

    def make_pyramid(self, base_opacity=0.12, lateral_opacity=0.04):
        A, B, C, D, S = self.config_points()
        base = face(A, B, C, D, color=BLUE, opacity=base_opacity, stroke=BLUE)
        f1 = face(S, A, B, color=PURPLE, opacity=lateral_opacity, stroke=PURPLE)
        f2 = face(S, B, C, color=CYAN, opacity=lateral_opacity, stroke=CYAN)
        f3 = face(S, C, D, color=GREEN, opacity=lateral_opacity, stroke=GREEN)
        f4 = face(S, D, A, color=ORANGE, opacity=lateral_opacity, stroke=ORANGE)
        edges = VGroup(
            seg(A,B), seg(B,C), seg(C,D), seg(D,A),
            seg(S,A), seg(S,B), seg(S,C), seg(S,D),
        )
        points = VGroup(
            Dot3D(A, radius=0.07, color=GOLD),
            Dot3D(B, radius=0.07, color=GOLD),
            Dot3D(C, radius=0.07, color=GOLD),
            Dot3D(D, radius=0.07, color=GOLD),
            Dot3D(S, radius=0.08, color=RED),
        )
        return {
            "A":A,"B":B,"C":C,"D":D,"S":S,
            "base":base,"faces":VGroup(f1,f2,f3,f4),
            "edges":edges,"points":points,
        }

    def vertex_labels(self, G):
        labels = []
        for name, off in [
            ("A", P(-0.28,-0.20,-0.10)),
            ("B", P(0.22,-0.18,-0.08)),
            ("C", P(0.22,0.16,0.02)),
            ("D", P(-0.30,0.15,0.02)),
            ("S", P(-0.28,-0.18,0.18)),
        ]:
            lab = mty(name, 28, GOLD if name != "S" else RED)
            lab.move_to(G[name] + off)
            self.add_fixed_orientation_mobjects(lab)
            labels.append(lab)
        return VGroup(*labels)

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        title = txt("HHKG CHUYÊN SÂU 01", 47, GOLD, BOLD)
        sub = txt("MỘT CẤU HÌNH – NHIỀU ĐẠI LƯỢNG", 37, INK, BOLD)
        line = txt("angle  -  dihedral  -  distance  -  volume  -  ratio", 34, CYAN)
        note = txt("Học cách nhìn hình trước khi chọn công thức", 27, MUTED)
        brand = txt(TEN_THAY, 21, MUTED)
        g = VGroup(title, sub, line, note, brand).arrange(DOWN, buff=0.28)
        self.play(FadeIn(title, shift=UP*0.2), run_time=0.7)
        self.play(FadeIn(sub), Write(line), FadeIn(note), FadeIn(brand), run_time=1.2)
        self.narrate(
            "Chào các em. Đây là video đầu tiên của series hình học không gian chuyên sâu. Thầy không muốn các em học riêng từng công thức góc, khoảng cách hay thể tích. Ta sẽ dùng đúng một hình chóp, rồi khai thác liên tiếp năm câu hỏi khác nhau. Mục tiêu là nhìn ra cấu trúc: hình chiếu nào cần dùng, mặt cắt nào nên chọn, khi nào đổi bài khoảng cách thành bài thể tích, và khi nào dùng đồng dạng để xử lý tỷ số. Nếu nhìn đúng hình, nhiều bài khó sẽ ngắn đi rất nhiều.",
            2.0,
        )

    # ======================================================
    # BUILD CONFIGURATION
    # ======================================================
    def build_configuration(self):
        self.clear_all()
        self.set_camera_orientation(phi=67*DEGREES, theta=-48*DEGREES, zoom=0.90)
        self.add_hud("Cấu hình gốc", "Hình chóp S.ABCD có đáy là hình vuông", "1/7")
        G = self.make_pyramid(base_opacity=0.13, lateral_opacity=0.025)
        self.play(FadeIn(G["base"]), Create(G["edges"]), FadeIn(G["points"]), run_time=1.4)
        labs = self.vertex_labels(G)

        right1 = seg(G["A"] + P(0.36,0,0), G["A"] + P(0.36,0,0.36), GOLD, 4)
        right2 = seg(G["A"] + P(0.36,0,0.36), G["A"] + P(0,0,0.36), GOLD, 4)
        self.play(Create(right1), Create(right2), run_time=0.6)

        box = self.formula_box([
            txt("Giả thiết", 25, GOLD, BOLD),
            mty("A B = B C = 4", 35, CYAN),
            mty("S A = 3", 35, CYAN),
            mty("S A ⟂ (A B C D)", 35, GREEN),
        ], width=4.9, height=3.4, shift=RIGHT*4.0 + DOWN*0.25)

        self.narrate(
            "Ta xét hình chóp S.ABCD. Đáy ABCD là hình vuông cạnh bốn. Cạnh SA dài ba và vuông góc với mặt phẳng đáy. Đây là một cấu hình rất giàu thông tin. Vì SA vuông góc với đáy, điểm A chính là hình chiếu vuông góc của S xuống đáy. Đồng thời tam giác SAB là tam giác vuông ba bốn năm, một chi tiết sẽ xuất hiện nhiều lần trong video.",
            2.0,
        )
        self.begin_ambient_camera_rotation(rate=0.08)
        self.narrate(
            "Thầy cho hình quay chậm để các em tập nhìn không gian. Đừng vội tính. Hãy quan sát: cạnh nào nằm trong đáy, cạnh nào là đường cao, mặt bên nào chứa đường ta quan tâm, và cạnh chung của hai mặt phẳng nằm ở đâu. Hình học không gian tốt bắt đầu từ việc đọc đúng cấu hình.",
            2.0,
        )
        self.stop_ambient_camera_rotation()
        return G

    # ======================================================
    # ANGLE LINE - PLANE
    # ======================================================
    def angle_line_plane(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES, theta=-43*DEGREES, zoom=0.92)
        self.add_hud("Bài 1 – Góc giữa đường thẳng và mặt phẳng", "Tìm góc giữa SC và mặt phẳng đáy", "2/7")
        G = self.make_pyramid(base_opacity=0.14, lateral_opacity=0.015)
        self.add(G["base"], G["edges"], G["points"])
        self.vertex_labels(G)

        SC = seg(G["S"], G["C"], GOLD, 7)
        AC = DashedLine(G["A"], G["C"], color=CYAN, stroke_width=5, dash_length=0.15)
        SA = seg(G["S"], G["A"], GREEN, 6)
        alpha = math.atan2(3, 4*math.sqrt(2))
        arc = arc_in_plane(G["C"], P(-1,-1,0), P(0,0,1), alpha, radius=0.72, color=GOLD)
        self.play(Create(SC), Create(AC), Create(SA), run_time=1.0)
        self.play(Create(arc), run_time=0.7)

        box = self.formula_box([
            txt("Bước 1: tìm hình chiếu", 24, GOLD, BOLD),
            mty('"proj"_(A B C D)(S C) = A C', 31, CYAN),
            mty("A C = 4 sqrt(2)", 34, INK),
            mty("tan alpha = (S A)/(A C)", 34, INK),
            mty("tan alpha = 3/(4 sqrt(2))", 37, GOLD),
        ], width=5.35, height=4.5, shift=RIGHT*3.8 + DOWN*0.1)

        self.narrate(
            "Câu đầu tiên: tìm góc giữa SC và mặt phẳng ABCD. Quy tắc quan trọng nhất là không nhìn góc trực tiếp trong không gian. Ta phải tìm hình chiếu vuông góc của đường SC xuống mặt phẳng đáy. Vì S chiếu xuống A, còn C đã nằm trên đáy, nên hình chiếu của SC chính là AC. Vậy góc giữa SC và đáy là góc SCA.",
            2.0,
        )
        self.narrate(
            "Bây giờ bài toán không còn là hình học không gian nữa mà trở thành một tam giác vuông SAC. Đường chéo AC của hình vuông cạnh bốn bằng bốn căn hai. Trong tam giác vuông tại A, tang của góc alpha tại C bằng cạnh đối SA chia cạnh kề AC, tức bằng ba trên bốn căn hai. Nếu chỉ cần một giá trị lượng giác, ta nên dừng tại đây, không nhất thiết bấm máy ra số đo góc.",
            2.0,
        )
        takeaway = VGroup(
            txt("Mẫu nhận dạng:", 24, MUTED),
            txt("đường – mặt", 24, CYAN, BOLD),
            txt("→ tìm hình chiếu của đường lên mặt", 24, MUTED),
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.62)
        self.add_fixed_in_frame_mobjects(takeaway)
        self.play(FadeIn(takeaway), run_time=0.5)
        self.narrate("Chốt lại: bài góc giữa đường và mặt phẳng trước hết là một bài hình chiếu. Khi đã xác định đúng hình chiếu, góc không gian sẽ trở thành một góc phẳng quen thuộc.", 1.4)

    # ======================================================
    # DIHEDRAL ANGLE
    # ======================================================
    def dihedral_angle(self):
        self.clear_all()
        self.set_camera_orientation(phi=68*DEGREES, theta=-54*DEGREES, zoom=0.92)
        self.add_hud("Bài 2 – Góc nhị diện", "Giữa mặt (SBC) và mặt đáy theo cạnh BC", "3/7")
        G = self.make_pyramid(base_opacity=0.14, lateral_opacity=0.02)
        self.add(G["base"], G["edges"], G["points"])
        self.vertex_labels(G)

        face_sbc = face(G["S"], G["B"], G["C"], color=PURPLE, opacity=0.24, stroke=PURPLE, stroke_width=3)
        bc = seg(G["B"], G["C"], GOLD, 8)
        ba = seg(G["B"], G["A"], CYAN, 7)
        bs = seg(G["B"], G["S"], GREEN, 7)
        beta = math.atan2(3, 4)
        arc = arc_in_plane(G["B"], P(-1,0,0), P(0,0,1), beta, radius=0.68, color=GOLD)
        self.play(FadeIn(face_sbc), Create(bc), run_time=0.8)
        self.play(Create(ba), Create(bs), Create(arc), run_time=0.9)

        box = self.formula_box([
            txt("Cạnh chung", 24, GOLD, BOLD),
            mty("B C", 34, GOLD),
            mty("B A ⟂ B C", 32, CYAN),
            mty("B S ⟂ B C", 32, GREEN),
            mty("beta = angle(A B S)", 33, INK),
            mty("sin beta = 3/5", 36, GOLD),
            mty("tan beta = 3/4", 36, GOLD),
        ], width=5.15, height=4.95, shift=RIGHT*3.9 + DOWN*0.05)

        self.narrate(
            "Câu thứ hai khó hơn: tìm góc nhị diện giữa mặt bên SBC và mặt đáy ABCD theo cạnh chung BC. Sai lầm phổ biến là nhìn thấy hai mặt rồi chọn đại hai đường trên hai mặt. Định nghĩa yêu cầu ta chọn trong mỗi mặt một đường cùng vuông góc với cạnh chung BC, tại cùng một điểm trên cạnh đó.",
            2.0,
        )
        self.narrate(
            "Ở điểm B, đường BA nằm trong đáy và vuông góc BC. Ta cần chứng minh BS cũng vuông góc BC. Vì AD vuông góc AB và AD cũng vuông góc SA, nên AD vuông góc mặt phẳng SAB. Mà BC song song AD, suy ra BC vuông góc mặt phẳng SAB, do đó BC vuông góc BS. Vậy góc nhị diện cần tìm chính là góc ABS.",
            2.0,
        )
        self.narrate(
            "Tam giác SAB là tam giác vuông có ba cạnh ba, bốn, năm. Vì vậy sin beta bằng ba phần năm và tang beta bằng ba phần bốn. Đây là lý do cấu hình ba bốn năm đặc biệt đẹp: một góc nhị diện không gian cuối cùng được đọc ngay từ một tam giác vuông rất quen thuộc.",
            1.8,
        )
        takeaway = txt("Mẫu nhận dạng: góc nhị diện → cắt bởi mặt phẳng vuông góc cạnh chung", 24, MUTED).to_edge(DOWN, buff=0.62)
        self.add_fixed_in_frame_mobjects(takeaway)
        self.play(FadeIn(takeaway), run_time=0.5)

    # ======================================================
    # VOLUME
    # ======================================================
    def volume(self):
        self.clear_all()
        self.set_camera_orientation(phi=66*DEGREES, theta=-46*DEGREES, zoom=0.92)
        self.add_hud("Bài 3 – Thể tích", "Đừng để một câu dễ trở thành câu dài", "4/7")
        G = self.make_pyramid(base_opacity=0.25, lateral_opacity=0.05)
        self.add(G["base"], G["faces"], G["edges"], G["points"])
        self.vertex_labels(G)
        SA = seg(G["S"], G["A"], GOLD, 7)
        self.play(Create(SA), run_time=0.6)

        box = self.formula_box([
            txt("Đáy là hình vuông", 24, GOLD, BOLD),
            mty("S_(A B C D) = 4^2 = 16", 34, CYAN),
            mty("h = S A = 3", 34, GREEN),
            mty('V = 1/3 S_("base") h', 35, INK),
            mty("V = 1/3 times 16 times 3 = 16", 37, GOLD),
        ], width=5.25, height=4.25, shift=RIGHT*3.85 + DOWN*0.1)

        self.narrate(
            "Sau hai câu góc, ta gặp câu thể tích. Đây là chỗ cần kỷ luật: không vì hình đang phức tạp mà biến một câu đơn giản thành lời giải dài. Đáy là hình vuông cạnh bốn nên diện tích đáy bằng mười sáu. SA đã là đường cao và dài ba. Chỉ cần dùng đúng công thức thể tích hình chóp.",
            1.8,
        )
        self.narrate(
            "Thể tích bằng một phần ba nhân diện tích đáy nhân chiều cao, tức một phần ba nhân mười sáu nhân ba bằng mười sáu. Kết quả này sẽ được tái sử dụng ngay ở câu khoảng cách tiếp theo. Một kỹ năng rất quan trọng trong bài nhiều ý là giữ lại các kết quả trung gian có thể dùng tiếp.",
            1.6,
        )

    # ======================================================
    # DISTANCE TO PLANE VIA VOLUME
    # ======================================================
    def distance_to_plane(self):
        self.clear_all()
        self.set_camera_orientation(phi=70*DEGREES, theta=-54*DEGREES, zoom=0.90)
        self.add_hud("Bài 4 – Khoảng cách điểm đến mặt phẳng", "Từ D đến mặt (SBC)", "5/7")
        G = self.make_pyramid(base_opacity=0.10, lateral_opacity=0.01)
        self.add(G["base"], G["edges"], G["points"])
        self.vertex_labels(G)

        sbc = face(G["S"], G["B"], G["C"], color=PURPLE, opacity=0.27, stroke=PURPLE, stroke_width=3)
        tetra_base = face(G["B"], G["C"], G["D"], color=BLUE, opacity=0.18, stroke=BLUE, stroke_width=2)
        H = P(-14/25, 2, 48/25)
        DH = seg(G["D"], H, GOLD, 7)
        hdot = Dot3D(H, radius=0.065, color=GOLD)
        self.play(FadeIn(sbc), FadeIn(tetra_base), run_time=0.8)
        self.play(Create(DH), FadeIn(hdot), run_time=0.8)

        box = self.formula_box([
            txt("Đổi khoảng cách thành thể tích", 23, GOLD, BOLD),
            mty("V_(S B C D) = 1/2 V_(S A B C D) = 8", 30, CYAN),
            mty("S_(S B C) = 1/2 times 4 times 5 = 10", 31, GREEN),
            mty("8 = 1/3 times 10 times d", 33, INK),
            mty("d = 12/5", 41, GOLD),
        ], width=5.35, height=4.45, shift=RIGHT*3.78 + DOWN*0.1)

        self.narrate(
            "Câu khoảng cách từ D đến mặt phẳng SBC thường khiến học sinh cố dựng chân đường vuông góc H rồi mắc kẹt ở việc xác định H nằm ở đâu. Ta vẫn vẽ đoạn DH để hiểu ý nghĩa hình học của khoảng cách, nhưng lời giải sẽ không đi theo hướng dựng H. Ta đổi bài khoảng cách thành bài thể tích của tứ diện SBCD.",
            2.0,
        )
        self.narrate(
            "Tam giác BCD chiếm đúng một nửa hình vuông ABCD và có cùng chiều cao SA, nên thể tích tứ diện SBCD bằng một nửa thể tích hình chóp ban đầu, tức bằng tám. Mặt SBC là một tam giác vuông tại B vì SB vuông góc BC. Ta đã biết SB bằng năm và BC bằng bốn, nên diện tích tam giác SBC bằng mười.",
            2.0,
        )
        self.narrate(
            "Bây giờ xem SBC là đáy của tứ diện SBCD. Chiều cao tương ứng chính là khoảng cách từ D tới mặt phẳng SBC, gọi là d. Ta có tám bằng một phần ba nhân mười nhân d. Suy ra d bằng mười hai phần năm. Không cần tìm tọa độ hay vị trí chính xác của chân H, lời giải vẫn hoàn toàn hình học và rất gọn.",
            2.0,
        )
        takeaway = txt("Mẫu nhận dạng: khoảng cách khó dựng → thử đổi sang thể tích", 24, MUTED).to_edge(DOWN, buff=0.62)
        self.add_fixed_in_frame_mobjects(takeaway)
        self.play(FadeIn(takeaway), run_time=0.5)

    # ======================================================
    # MIDPOINT SECTION + RATIOS
    # ======================================================
    def midpoint_section(self):
        self.clear_all()
        self.set_camera_orientation(phi=67*DEGREES, theta=-46*DEGREES, zoom=0.92)
        self.add_hud("Bài 5 – Thiết diện và tỷ số", "M, N, P, Q là trung điểm bốn cạnh bên", "6/7")
        G = self.make_pyramid(base_opacity=0.15, lateral_opacity=0.015)
        self.add(G["base"], G["edges"], G["points"])
        self.vertex_labels(G)

        M = (G["S"] + G["A"]) / 2
        N = (G["S"] + G["B"]) / 2
        Pp = (G["S"] + G["C"]) / 2
        Q = (G["S"] + G["D"]) / 2
        section = face(M, N, Pp, Q, color=GOLD, opacity=0.33, stroke=GOLD, stroke_width=4)
        dots = VGroup(*[Dot3D(X, radius=0.06, color=GOLD) for X in [M,N,Pp,Q]])
        self.play(FadeIn(section), FadeIn(dots), run_time=0.9)

        for name, X, off in [
            ("M",M,P(-0.15,-0.18,0.12)),
            ("N",N,P(0.16,-0.14,0.10)),
            ("P",Pp,P(0.16,0.15,0.08)),
            ("Q",Q,P(-0.18,0.15,0.08)),
        ]:
            lab = mty(name, 24, GOLD).move_to(X+off)
            self.add_fixed_orientation_mobjects(lab)

        box = self.formula_box([
            mty("S M/S A = S N/S B = 1/2", 32, CYAN),
            mty("(M N P Q) ∥ (A B C D)", 32, GREEN),
            mty("S_(M N P Q)/S_(A B C D) = (1/2)^2 = 1/4", 31, INK),
            mty("V_(S.M N P Q)/V_(S.A B C D) = (1/2)^3", 30, INK),
            mty("= 1/8", 42, GOLD),
        ], width=5.5, height=4.55, shift=RIGHT*3.7 + DOWN*0.05)

        self.narrate(
            "Câu cuối cùng thêm bốn trung điểm M, N, P, Q trên các cạnh SA, SB, SC, SD. Vì cả bốn điểm chia các cạnh bên theo cùng tỷ số một phần hai tính từ đỉnh S, mặt phẳng MNPQ song song với mặt phẳng đáy. Toàn bộ hình chóp nhỏ S.MNPQ đồng dạng với hình chóp lớn S.ABCD theo tỷ số dài một phần hai.",
            2.0,
        )
        self.narrate(
            "Từ đây có hai hệ quả rất mạnh. Diện tích thiết diện tỷ lệ với bình phương tỷ số đồng dạng, nên diện tích MNPQ bằng một phần tư diện tích ABCD. Còn thể tích tỷ lệ với lập phương tỷ số đồng dạng, nên thể tích hình chóp nhỏ bằng một phần tám thể tích hình chóp lớn. Đây là một trong những mẹo tỷ số thể tích quan trọng nhất của hình học không gian phổ thông.",
            2.0,
        )
        self.begin_ambient_camera_rotation(rate=0.07)
        self.narrate(
            "Khi hình quay, các em hãy quan sát thiết diện vàng luôn song song với đáy xanh. Nếu thay trung điểm bằng các điểm cùng chia cạnh theo tỷ số k, quy luật vẫn giữ nguyên: tỷ số diện tích bằng k bình phương và tỷ số thể tích bằng k lập phương. Ta sẽ khai thác rất sâu ý này ở video chuyên về thể tích và tỷ số thể tích.",
            2.0,
        )
        self.stop_ambient_camera_rotation()

    # ======================================================
    # SUMMARY + ROADMAP
    # ======================================================
    def summary(self):
        self.clear_all()
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES, zoom=1.0)
        self.add_hud("Bản đồ tư duy từ một cấu hình", "5 câu hỏi – 5 cách nhìn", "7/7")
        left = VGroup(
            VGroup(txt("1.",24,GOLD,BOLD), txt("Góc đường – mặt",25,INK), txt("→ hình chiếu",25,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("2.",24,GOLD,BOLD), txt("Góc nhị diện",25,INK), txt("→ vuông góc cạnh chung",25,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("3.",24,GOLD,BOLD), txt("Thể tích",25,INK), txt("→ đáy × chiều cao",25,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("4.",24,GOLD,BOLD), txt("Khoảng cách khó",25,INK), txt("→ đổi sang thể tích",25,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
            VGroup(txt("5.",24,GOLD,BOLD), txt("Thiết diện song song",25,INK), txt("→ đồng dạng & tỷ số",25,CYAN,BOLD)).arrange(RIGHT,buff=0.13),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).shift(LEFT*2.9 + UP*0.1)
        self.add_fixed_in_frame_mobjects(left)
        self.play(FadeIn(left, shift=RIGHT*0.15), run_time=0.8)

        right = VGroup(
            txt("Kết quả của cấu hình", 27, GOLD, BOLD),
            mty("tan alpha = 3/(4 sqrt(2))", 31, INK),
            mty("sin beta = 3/5", 31, INK),
            mty("V = 16", 33, INK),
            mty("d(D,(S B C)) = 12/5", 31, INK),
            mty('V_("small")/V_("large") = 1/8', 31, INK),
        ).arrange(DOWN,buff=0.28).shift(RIGHT*3.0 + UP*0.08)
        self.add_fixed_in_frame_mobjects(right)
        self.play(FadeIn(right), run_time=0.8)

        self.narrate(
            "Ta vừa dùng một hình duy nhất để luyện năm tư duy khác nhau. Góc đường với mặt phẳng bắt đầu bằng hình chiếu. Góc nhị diện bắt đầu bằng cạnh chung. Thể tích dùng đúng đáy và chiều cao. Khoảng cách khó dựng có thể đổi thành thể tích. Thiết diện song song mở ra đồng dạng và các quy luật bình phương, lập phương. Đây chính là cách thầy muốn các em học hình học không gian: không ghi nhớ hàng chục mẹo rời rạc, mà xây một bản đồ nhận dạng.",
            2.0,
        )

        roadmap = VGroup(
            txt("Series HHKG tiếp theo", 26, GOLD, BOLD),
            txt("02. Khoảng cách chuyên sâu – hai đường chéo nhau", 22, MUTED),
            txt("03. Góc đường–đường, đường–mặt, mặt–mặt", 22, MUTED),
            txt("04. Góc nhị diện chuyên sâu", 22, MUTED),
            txt("05. Thể tích & tỷ số thể tích", 22, MUTED),
            txt("06. Thiết diện & mặt phẳng cắt", 22, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.52)
        self.add_fixed_in_frame_mobjects(roadmap)
        self.play(FadeIn(roadmap), run_time=0.7)
        self.narrate(
            "Từ video sau, series sẽ tách từng kỹ năng ra để đi sâu: khoảng cách giữa hai đường chéo nhau, các loại góc trong không gian, góc nhị diện, tỷ số thể tích, thiết diện khó, đường vuông góc chung, điểm động, khối tròn xoay và các mô hình thực tế ba chiều. Mỗi video vẫn ưu tiên dựng hình đúng, quay hình đủ chậm và giải thích vì sao chọn được đường phụ hay mặt phẳng phụ.",
            2.0,
        )

        self.clear_all()
        end = VGroup(
            txt("HHKG CHUYÊN SÂU", 45, GOLD, BOLD),
            txt("Nhìn đúng cấu hình → lời giải ngắn lại", 30, CYAN),
            txt("projection  →  section  →  ratio", 34, INK),
            txt(TEN_THAY, 21, MUTED),
        ).arrange(DOWN,buff=0.30)
        self.add_fixed_in_frame_mobjects(end)
        self.play(FadeIn(end), run_time=0.9)
        self.narrate("Các em hãy nhớ: hình học không gian khó không phải vì có quá nhiều công thức, mà vì ta chưa chọn đúng mặt phẳng để nhìn. Hẹn gặp các em ở video hai, chuyên sâu về khoảng cách trong không gian.", 1.6)

    def construct(self):
        self.intro()
        self.build_configuration()
        self.angle_line_plane()
        self.dihedral_angle()
        self.volume()
        self.distance_to_plane()
        self.midpoint_section()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "hhkg_chuyen_sau_01_manim_typst_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    print("Renderer: Manim + native Typst (MathTypst)")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_hhkg_01.wav"
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

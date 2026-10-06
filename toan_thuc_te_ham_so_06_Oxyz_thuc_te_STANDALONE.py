from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time

# ==========================================================
# SERIES ROADMAP - TOAN THUC TE / CT GDPT 2018
# 01. Mo hinh hoa + toi uu mot bien
# 02. Ham nhieu cong thuc: gia, phi, nguong, suc chua
# 03. Toc do - thoi gian - nang suat - chi phi
# 04. Doc do thi thuc te + dao ham + Dung/Sai
# 05. Tich phan trong bai toan thuc te
# 06. Oxyz trong bai toan thuc te (FILE NAY)
# 07. Xac suat - thong ke tu du lieu
# 08. Tong hop Dung/Sai + tra loi ngan kieu TN THPT
#
# Nguyen tac dai han:
# - Uu tien mo hinh thuc te, ham tuong minh, do thi/hinh dong.
# - Han che toi da ham an.
# - Moi bai: doc boi canh -> lap mo hinh -> giai -> dien giai ket qua.
# - 3D de lam ro ban chat, khong dung 3D chi de trang tri.
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

TMPL = TexTemplate()
TMPL.add_to_preamble(r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}
\usepackage{xcolor}
""")


def mtx(s, size=38, color=INK):
    return MathTex(s, font_size=size, color=color, tex_template=TMPL)


def txt(s, size=30, color=INK, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


def fit_width(mob, width=12.2):
    if mob.width > width:
        mob.scale_to_fit_width(width)
    return mob


def make_panel(width=12.2, height=5.3):
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        fill_color=PANEL,
        fill_opacity=0.90,
        stroke_color=MUTED,
        stroke_opacity=0.22,
        stroke_width=1.5,
    )


def title_block(title, subtitle=None):
    t = fit_width(txt(title, 38, INK, BOLD), 12.0).to_edge(UP, buff=0.25)
    if subtitle:
        s = fit_width(txt(subtitle, 23, MUTED), 11.7).next_to(t, DOWN, buff=0.10)
        return VGroup(t, s)
    return VGroup(t)


def footer(page_text=""):
    left = txt(TEN_THAY, 19, MUTED)
    right = txt(page_text, 19, MUTED)
    left.to_edge(DOWN, buff=0.18).to_edge(LEFT, buff=0.38)
    right.to_edge(DOWN, buff=0.18).to_edge(RIGHT, buff=0.38)
    return VGroup(left, right)


def bullet(text, color=INK, size=27, dot_color=BLUE):
    d = Dot(radius=0.055, color=dot_color)
    t = txt(text, size, color)
    return VGroup(d, t).arrange(RIGHT, buff=0.18, aligned_edge=UP)


# ==========================================================
# TTS + MASTER AUDIO
# ==========================================================
def _audio_key(text):
    payload = json.dumps(
        {"text": text, "voice": GIONG_DOC, "rate": TOC_DO_DOC, "pitch": PITCH, "engine": "edge-tts"},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def probe_duration(path: Path) -> float:
    out = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path),
    ], text=True).strip()
    return float(out)


def validate_audio(path: Path):
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError(f"Audio khong hop le: {path}")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"], check=True)


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
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[m]", "-ar", "48000", "-ac", "2",
        "-t", f"{video_duration:.3f}", str(out_wav)
    ], check=True)


def mux_audio(video: Path, audio: Path, out: Path):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(out)
    ], check=True)


class SangLesson(ThreeDScene):
    def setup(self):
        self.audio_events = []

    # ---------- audio ----------
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

    # ---------- layout ----------
    def set_2d(self):
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

    def clear_stage(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.42)

    def add_header_footer(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add(h, f)
        return h, f

    def show_problem(self, title, content, voice, progress):
        self.clear_stage()
        self.set_2d()
        self.add_header_footer(title, "TÌNH HUỐNG", progress)
        panel = make_panel(12.3, 5.15).shift(DOWN * 0.08)
        self.play(FadeIn(panel), run_time=0.45)
        group = VGroup()
        for item in content:
            mob = item if isinstance(item, Mobject) else fit_width(txt(item, 27, INK), 11.1)
            group.add(mob)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(panel)
        fit_width(group, 11.15)
        for mob in group:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.28)
        self.narrate(voice, 1.8)

    def fixed_header(self, title, subtitle, progress):
        h = title_block(title, subtitle)
        f = footer(progress)
        self.add_fixed_in_frame_mobjects(h, f)
        return h, f

    def remove_fixed_group(self, *groups):
        for g in groups:
            self.remove_fixed_in_frame_mobjects(g)
            self.remove(g)

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage(); self.set_2d()
        g = VGroup(
            txt("OXYZ TRONG BÀI TOÁN THỰC TẾ", 46, GOLD, BOLD),
            txt("Drone – radar – khoảng cách – mặt phẳng – đường bay", 29, CYAN),
            VGroup(mtx(r"M(x,y,z)", 38, INK), Arrow(LEFT*0.35, RIGHT*0.35, color=CYAN, stroke_width=3), txt("mô hình không gian", 27, INK)).arrange(RIGHT, buff=0.16),
            txt("3D để nhìn bản chất, công thức để giải gọn", 26, MUTED),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.30)
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.7)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), FadeIn(g[4]), run_time=1.0)
        self.narrate(
            "Chào các em. Video này đưa hệ trục Oxyz vào đúng những tình huống mà ta gặp trong thực tế: xác định vị trí một drone, đo khoảng cách tới radar, tìm thời điểm hai thiết bị bay gần nhau nhất, kiểm tra khoảng cách tới một mặt phẳng an toàn và xác định lúc đường bay cắt qua một ranh giới. Điều quan trọng là ta sẽ luôn bắt đầu bằng hình ảnh không gian, rồi mới viết công thức. Các bài nhìn ba chiều khá phức tạp, nhưng khi chọn đúng đại lượng thì lời giải thường rất gọn.",
            2.0,
        )

        self.clear_stage(); self.set_2d(); self.add_header_footer("Bộ công cụ Oxyz", "Chỉ cần 4 ý nền tảng", "Mở đầu")
        rows = VGroup(
            VGroup(mtx(r"AB=\sqrt{(x_B-x_A)^2+(y_B-y_A)^2+(z_B-z_A)^2}", 33, BLUE), txt("Khoảng cách hai điểm", 24, INK)).arrange(DOWN,buff=0.10),
            VGroup(mtx(r"d(M,(P))=\frac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}", 31, CYAN), txt("Khoảng cách điểm – mặt phẳng", 24, INK)).arrange(DOWN,buff=0.10),
            VGroup(mtx(r"M(t)=(x(t),y(t),z(t))", 34, GOLD), txt("Chuyển động theo tham số thời gian", 24, INK)).arrange(DOWN,buff=0.10),
            VGroup(mtx(r"D^2(t)", 36, ORANGE), txt("Tối ưu bình phương khoảng cách thay vì căn", 24, INK)).arrange(DOWN,buff=0.10),
        ).arrange(DOWN,buff=0.30).shift(DOWN*0.05)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT*0.12), run_time=0.4)
        self.narrate(
            "Bốn công cụ sẽ lặp đi lặp lại. Một, công thức khoảng cách hai điểm. Hai, khoảng cách từ điểm đến mặt phẳng. Ba, tọa độ phụ thuộc thời gian. Và bốn, khi cần tìm khoảng cách nhỏ nhất, ta thường tối ưu bình phương khoảng cách D bình phương để loại căn. Đây là một mẹo rất quan trọng vì nó biến bài toán hình học không gian thành một bài hàm số một biến quen thuộc.",
            2.0,
        )

    # ======================================================
    # 1. DRONE POSITION - DISTANCE TO BASE
    # ======================================================
    def ex1_drone_position(self):
        self.show_problem(
            "Bài 1 – Drone và trạm điều khiển",
            [
                "Một hệ tọa độ không gian dùng đơn vị 100 m.",
                mtx(r"O(0,0,0),\qquad A(3,4,12)", 39, GOLD),
                "Drone đang ở A. Tính khoảng cách từ drone đến trạm O.",
            ],
            "Trạm điều khiển đặt tại gốc O. Drone ở điểm A có tọa độ ba, bốn, mười hai, mỗi đơn vị tọa độ ứng với một trăm mét. Ta cần tính khoảng cách thật từ drone đến trạm. Đây là bài đơn giản nhưng rất quan trọng vì mọi bài chuyển động sau đều dựa trên công thức này.",
            "1/5",
        )

        self.clear_stage()
        self.set_camera_orientation(phi=68*DEGREES, theta=-48*DEGREES, zoom=0.88)
        h, f = self.fixed_header("Bài 1", "Khoảng cách trong không gian", "1/5")
        axes = ThreeDAxes(
            x_range=[0,5,1], y_range=[0,5,1], z_range=[0,13,2],
            x_length=5.2, y_length=5.2, z_length=5.6,
            axis_config={"color":MUTED,"stroke_width":2},
        ).shift(DOWN*0.45)
        O = Dot3D(axes.c2p(0,0,0), radius=0.07, color=GREEN)
        A = Dot3D(axes.c2p(3,4,12), radius=0.085, color=GOLD)
        OA = Line3D(axes.c2p(0,0,0), axes.c2p(3,4,12), color=CYAN, thickness=0.025)
        proj = Line3D(axes.c2p(3,4,0), axes.c2p(3,4,12), color=ORANGE, thickness=0.018)
        ground = Line3D(axes.c2p(0,0,0), axes.c2p(3,4,0), color=BLUE, thickness=0.018)
        self.play(Create(axes), FadeIn(O), FadeIn(A), run_time=1.0)
        self.play(Create(ground), Create(proj), Create(OA), run_time=1.1)
        self.begin_ambient_camera_rotation(rate=0.04)
        self.narrate(
            "Hình ba chiều cho ta thấy khoảng cách O A không phải là độ cao mười hai, cũng không phải là khoảng cách ngang năm. Đó là đường chéo trong không gian, kết hợp cả ba phương x, y và z. Ta có thể nhìn phần chiếu xuống mặt phẳng Oxy trước, rồi nối lên vị trí thật của drone.",
            2.0,
        )
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(axes), FadeOut(O), FadeOut(A), FadeOut(OA), FadeOut(proj), FadeOut(ground), run_time=0.6)
        self.remove_fixed_group(h,f)

        self.set_2d(); self.add_header_footer("Bài 1", "Tính bằng định lý Pythagore 3D", "1/5")
        calc = VGroup(
            mtx(r"OA=\sqrt{3^2+4^2+12^2}", 42, INK),
            mtx(r"=\sqrt{9+16+144}", 40, CYAN),
            mtx(r"=\sqrt{169}=13", 42, GOLD),
            mtx(r"13\cdot100=1300\ \mathrm{m}=1.3\ \mathrm{km}", 40, GREEN),
        ).arrange(DOWN,buff=0.36)
        for e in calc: self.play(Write(e), run_time=0.6)
        self.narrate(
            "Áp dụng công thức khoảng cách, O A bằng căn của ba bình phương cộng bốn bình phương cộng mười hai bình phương. Tổng là một trăm sáu mươi chín nên O A bằng mười ba đơn vị. Mỗi đơn vị là một trăm mét, vì vậy khoảng cách thật là một nghìn ba trăm mét, tức một phẩy ba ki lô mét.",
            1.8,
        )

    # ======================================================
    # 2. MOVING DRONE - MIN DISTANCE TO RADAR
    # ======================================================
    def ex2_radar_min_distance(self):
        self.show_problem(
            "Bài 2 – Drone bay qua vùng radar",
            [
                "Tọa độ drone sau thời gian t được mô hình bởi:",
                mtx(r"M(t)=(t,\,2t,\,12-t),\qquad 0\le t\le6", 38, GOLD),
                "Radar đặt tại O. Tìm thời điểm drone gần radar nhất.",
            ],
            "Bây giờ drone chuyển động. Sau thời gian t, vị trí của nó là M của t. Nếu cứ tối ưu khoảng cách O M có căn thì biểu thức khá nặng. Ta sẽ dùng một mẹo rất đẹp: tối ưu bình phương khoảng cách. Vì căn bậc hai là hàm tăng, điểm làm D nhỏ nhất cũng chính là điểm làm D bình phương nhỏ nhất.",
            "2/5",
        )

        self.clear_stage()
        self.set_camera_orientation(phi=65*DEGREES, theta=-50*DEGREES, zoom=0.88)
        h,f = self.fixed_header("Bài 2", "Điểm chuyển động – khoảng cách thay đổi", "2/5")
        axes = ThreeDAxes(
            x_range=[0,7,1], y_range=[0,13,2], z_range=[0,13,2],
            x_length=5.2, y_length=5.7, z_length=4.8,
            axis_config={"color":MUTED,"stroke_width":2},
        ).shift(DOWN*0.5)
        radar = Dot3D(axes.c2p(0,0,0), radius=0.07, color=RED)
        path = ParametricFunction(lambda u: axes.c2p(u,2*u,12-u), t_range=[0,6], color=BLUE, stroke_width=4)
        t = ValueTracker(0.0)
        drone = always_redraw(lambda: Dot3D(axes.c2p(t.get_value(),2*t.get_value(),12-t.get_value()), radius=0.085, color=GOLD))
        beam = always_redraw(lambda: Line3D(axes.c2p(0,0,0), axes.c2p(t.get_value(),2*t.get_value(),12-t.get_value()), color=CYAN, thickness=0.022))
        self.play(Create(axes), Create(path), FadeIn(radar), FadeIn(drone), Create(beam), run_time=1.2)
        self.narrate_play(
            "Điểm vàng là drone, còn đoạn xanh nhạt là khoảng cách tới radar. Khi drone đi dọc đường bay, đoạn này ngắn dần rồi lại dài ra. Ta cần xác định chính xác thời điểm ngắn nhất chứ không chỉ ước lượng bằng mắt.",
            t.animate.set_value(6.0), min_time=5.0,
        )
        self.play(t.animate.set_value(2.0), run_time=1.2)
        self.narrate("Điểm gần nhất xuất hiện khá sớm trên đường bay. Bây giờ ta chứng minh bằng đại số.",1.2)
        self.play(FadeOut(axes),FadeOut(path),FadeOut(radar),FadeOut(drone),FadeOut(beam),run_time=0.6)
        self.remove_fixed_group(h,f)

        self.set_2d(); self.add_header_footer("Bài 2", "Tối ưu bình phương khoảng cách", "2/5")
        sol = VGroup(
            mtx(r"D^2(t)=t^2+(2t)^2+(12-t)^2", 38, INK),
            mtx(r"=6t^2-24t+144", 39, CYAN),
            mtx(r"=6(t-2)^2+120", 42, GOLD),
            mtx(r"\boxed{t=2}", 44, GREEN),
            mtx(r"D_{\min}=\sqrt{120}=2\sqrt{30}", 39, GREEN),
        ).arrange(DOWN,buff=0.30)
        for e in sol:self.play(Write(e),run_time=0.58)
        self.narrate(
            "Bình phương khoảng cách là t bình phương cộng bốn t bình phương cộng mười hai trừ t tất cả bình phương. Rút gọn rồi hoàn thành bình phương, ta được sáu nhân t trừ hai bình phương cộng một trăm hai mươi. Vì bình phương luôn không âm, giá trị nhỏ nhất đạt khi t bằng hai. Khi đó khoảng cách nhỏ nhất là căn một trăm hai mươi, hay hai căn ba mươi đơn vị.",
            1.9,
        )
        note = VGroup(txt("Mẹo thi rất mạnh:",25,GOLD,BOLD),mtx(r"\min D\iff\min D^2",36,GOLD)).arrange(RIGHT,buff=0.18).to_edge(DOWN,buff=0.65)
        self.play(FadeIn(note),run_time=0.5)

    # ======================================================
    # 3. TWO MOVING DRONES - CLOSEST APPROACH
    # ======================================================
    def ex3_two_drones(self):
        self.show_problem(
            "Bài 3 – Hai thiết bị bay gần nhau nhất",
            [
                mtx(r"A(t)=(t,0,4)", 38, GOLD),
                mtx(r"B(t)=(6-t,3,0),\qquad 0\le t\le6", 38, CYAN),
                "Tìm thời điểm khoảng cách AB nhỏ nhất và kiểm tra ngưỡng an toàn 400 m.",
                "Mỗi đơn vị tọa độ ứng với 100 m.",
            ],
            "Hai thiết bị bay theo hai đường khác nhau. Hệ thống cần biết lúc chúng gần nhau nhất để kiểm tra an toàn. Đây là một kiểu bài rất phù hợp với Oxyz vì ta có thể viết trực tiếp véc tơ hiệu hai vị trí rồi tối ưu độ dài của nó.",
            "3/5",
        )

        self.clear_stage(); self.set_camera_orientation(phi=66*DEGREES,theta=-42*DEGREES,zoom=0.9)
        h,f = self.fixed_header("Bài 3", "Hai điểm cùng chuyển động", "3/5")
        axes = ThreeDAxes(
            x_range=[0,7,1], y_range=[-1,4,1], z_range=[0,5,1],
            x_length=6.6,y_length=4.6,z_length=4.4,
            axis_config={"color":MUTED,"stroke_width":2},
        ).shift(DOWN*0.45)
        pathA = ParametricFunction(lambda u: axes.c2p(u,0,4),t_range=[0,6],color=GOLD,stroke_width=4)
        pathB = ParametricFunction(lambda u: axes.c2p(6-u,3,0),t_range=[0,6],color=CYAN,stroke_width=4)
        t=ValueTracker(0.0)
        A=always_redraw(lambda: Dot3D(axes.c2p(t.get_value(),0,4),radius=0.08,color=GOLD))
        B=always_redraw(lambda: Dot3D(axes.c2p(6-t.get_value(),3,0),radius=0.08,color=CYAN))
        AB=always_redraw(lambda: Line3D(axes.c2p(t.get_value(),0,4),axes.c2p(6-t.get_value(),3,0),color=RED,thickness=0.024))
        self.play(Create(axes),Create(pathA),Create(pathB),FadeIn(A),FadeIn(B),Create(AB),run_time=1.1)
        self.narrate_play(
            "Hai điểm vàng và xanh chuyển động đồng thời. Đoạn đỏ là khoảng cách giữa chúng. Ban đầu đoạn đỏ khá dài, sau đó co lại, đạt ngắn nhất gần giữa hành trình rồi dài ra trở lại.",
            t.animate.set_value(6.0),min_time=5.0,
        )
        self.play(t.animate.set_value(3.0),run_time=1.1)
        self.narrate("Hình cho thấy thời điểm đặc biệt là quanh t bằng ba. Ta tính chính xác.",1.2)
        self.play(FadeOut(axes),FadeOut(pathA),FadeOut(pathB),FadeOut(A),FadeOut(B),FadeOut(AB),run_time=0.6)
        self.remove_fixed_group(h,f)

        self.set_2d(); self.add_header_footer("Bài 3", "Khoảng cách tương đối", "3/5")
        sol=VGroup(
            mtx(r"\overrightarrow{AB}=(6-2t,\,3,\,-4)",38,INK),
            mtx(r"AB^2=(6-2t)^2+3^2+(-4)^2",38,CYAN),
            mtx(r"=4(t-3)^2+25",42,GOLD),
            mtx(r"\boxed{t=3,\quad AB_{\min}=5}",42,GREEN),
            mtx(r"5\cdot100=500\ \mathrm{m}>400\ \mathrm{m}",38,GREEN),
        ).arrange(DOWN,buff=0.28)
        for e in sol:self.play(Write(e),run_time=0.58)
        self.narrate(
            "Véc tơ A B có tọa độ sáu trừ hai t, ba, âm bốn. Bình phương khoảng cách bằng bốn nhân t trừ ba bình phương cộng hai mươi lăm. Vì thế khoảng cách nhỏ nhất tại t bằng ba và bằng năm đơn vị, tức năm trăm mét. Ngưỡng an toàn là bốn trăm mét, nên trong toàn bộ khoảng thời gian xét, hai thiết bị vẫn cách nhau ít nhất một trăm mét nhiều hơn mức yêu cầu.",
            2.0,
        )

    # ======================================================
    # 4. DISTANCE POINT TO SAFETY PLANE
    # ======================================================
    def ex4_safety_plane(self):
        self.show_problem(
            "Bài 4 – Khoảng cách tới mặt phẳng an toàn",
            [
                "Một ranh giới an toàn được mô hình bởi mặt phẳng:",
                mtx(r"(P):\ x+2y+2z-12=0", 40, GOLD),
                mtx(r"M(2,1,5)", 38, CYAN),
                "Mỗi đơn vị tọa độ là 100 m. Drone có cách ranh giới ít nhất 50 m không?",
            ],
            "Một vùng an toàn có thể được mô hình hóa bằng một mặt phẳng. Drone đang ở điểm M. Ta cần đo khoảng cách vuông góc ngắn nhất từ M tới mặt phẳng, rồi so sánh với mức năm mươi mét. Đây là ý nghĩa thực tế trực tiếp của công thức khoảng cách điểm đến mặt phẳng.",
            "4/5",
        )

        self.clear_stage(); self.set_camera_orientation(phi=67*DEGREES,theta=-47*DEGREES,zoom=0.86)
        h,f=self.fixed_header("Bài 4","Mặt phẳng trong không gian", "4/5")
        axes=ThreeDAxes(
            x_range=[-1,7,1],y_range=[-1,6,1],z_range=[0,7,1],
            x_length=6.2,y_length=5.2,z_length=5.0,
            axis_config={"color":MUTED,"stroke_width":2},
        ).shift(DOWN*0.45)
        plane=Surface(
            lambda u,v: axes.c2p(u,v,6-u/2-v),
            u_range=[-0.5,6.5],v_range=[-0.5,5.0],resolution=(12,12),
            fill_color=BLUE,fill_opacity=0.28,stroke_color=BLUE,stroke_opacity=0.25,
        )
        M=Dot3D(axes.c2p(2,1,5),radius=0.09,color=GOLD)
        hx,hy,hz=16/9,5/9,41/9
        H=Dot3D(axes.c2p(hx,hy,hz),radius=0.075,color=GREEN)
        MH=Line3D(axes.c2p(2,1,5),axes.c2p(hx,hy,hz),color=RED,thickness=0.028)
        self.play(Create(axes),FadeIn(plane),FadeIn(M),FadeIn(H),Create(MH),run_time=1.2)
        self.begin_ambient_camera_rotation(rate=0.035)
        self.narrate(
            "Mặt xanh là ranh giới an toàn. Điểm vàng là drone. Đường đỏ được vẽ vuông góc với mặt phẳng và chính là đường ngắn nhất từ drone tới ranh giới. Trong thực tế, đây là khoảng cách cần so với tiêu chuẩn an toàn, chứ không phải khoảng cách tới một điểm tùy ý trên mặt phẳng.",
            2.0,
        )
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(axes),FadeOut(plane),FadeOut(M),FadeOut(H),FadeOut(MH),run_time=0.6)
        self.remove_fixed_group(h,f)

        self.set_2d(); self.add_header_footer("Bài 4", "Thế tọa độ vào công thức khoảng cách", "4/5")
        sol=VGroup(
            mtx(r"d=\frac{|2+2\cdot1+2\cdot5-12|}{\sqrt{1^2+2^2+2^2}}",36,INK),
            mtx(r"=\frac{|2|}{3}=\frac23",42,CYAN),
            mtx(r"\frac23\cdot100\approx66.7\ \mathrm{m}",40,GOLD),
            mtx(r"\boxed{66.7>50}",44,GREEN),
        ).arrange(DOWN,buff=0.34)
        for e in sol:self.play(Write(e),run_time=0.58)
        self.narrate(
            "Thế tọa độ M vào vế trái phương trình mặt phẳng, ta được trị tuyệt đối của hai. Mẫu số là căn một cộng bốn cộng bốn, bằng ba. Khoảng cách là hai phần ba đơn vị, tức khoảng sáu mươi sáu phẩy bảy mét. Vì lớn hơn năm mươi mét, drone thỏa yêu cầu an toàn trong tình huống này.",
            1.8,
        )

    # ======================================================
    # 5. LINE INTERSECTS RESTRICTED PLANE
    # ======================================================
    def ex5_line_plane(self):
        self.show_problem(
            "Bài 5 – Khi nào đường bay chạm ranh giới?",
            [
                "Đường bay của drone:",
                mtx(r"M(t)=(1+t,\,2-t,\,1+2t),\qquad t\ge0", 38, GOLD),
                "Ranh giới vùng kiểm soát:",
                mtx(r"(Q):\ x+y+z=8", 40, CYAN),
                "Tìm thời điểm và vị trí drone đi qua mặt phẳng Q.",
            ],
            "Bài cuối là dạng rất thực tế: một thiết bị chuyển động theo đường thẳng và ta cần biết lúc nào nó đi qua một ranh giới phẳng. Cách giải không cần công thức khoảng cách. Ta chỉ việc thay tọa độ đang phụ thuộc t vào phương trình mặt phẳng. Khi phương trình đúng, điểm đang nằm đúng trên ranh giới.",
            "5/5",
        )

        self.clear_stage(); self.set_camera_orientation(phi=65*DEGREES,theta=-45*DEGREES,zoom=0.88)
        h,f=self.fixed_header("Bài 5","Đường bay cắt mặt phẳng", "5/5")
        axes=ThreeDAxes(
            x_range=[0,5,1],y_range=[-2,4,1],z_range=[0,8,1],
            x_length=5.6,y_length=5.0,z_length=5.3,
            axis_config={"color":MUTED,"stroke_width":2},
        ).shift(DOWN*0.45)
        plane=Surface(
            lambda u,v: axes.c2p(u,v,8-u-v),
            u_range=[0,5],v_range=[-1.5,4],resolution=(12,12),
            fill_color=PURPLE,fill_opacity=0.28,stroke_color=PURPLE,stroke_opacity=0.25,
        )
        path=ParametricFunction(lambda u: axes.c2p(1+u,2-u,1+2*u),t_range=[0,3],color=ORANGE,stroke_width=4)
        t=ValueTracker(0.0)
        drone=always_redraw(lambda: Dot3D(axes.c2p(1+t.get_value(),2-t.get_value(),1+2*t.get_value()),radius=0.09,color=GOLD))
        hit=Dot3D(axes.c2p(3,0,5),radius=0.085,color=GREEN)
        self.play(Create(axes),FadeIn(plane),Create(path),FadeIn(drone),run_time=1.2)
        self.narrate_play(
            "Điểm vàng chạy dọc đường màu cam. Mặt tím là ranh giới. Khi tham số tăng, drone tiến tới mặt phẳng, đi xuyên qua nó rồi sang phía bên kia. Ta cần tìm đúng thời điểm giao nhau.",
            t.animate.set_value(3.0),min_time=5.0,
        )
        self.play(t.animate.set_value(2.0),FadeIn(hit),run_time=1.1)
        self.narrate("Tại t bằng hai, điểm chuyển động nằm đúng trên mặt phẳng. Ta kiểm tra bằng phương trình.",1.2)
        self.play(FadeOut(axes),FadeOut(plane),FadeOut(path),FadeOut(drone),FadeOut(hit),run_time=0.6)
        self.remove_fixed_group(h,f)

        self.set_2d(); self.add_header_footer("Bài 5", "Thay tham số vào phương trình mặt phẳng", "5/5")
        sol=VGroup(
            mtx(r"(1+t)+(2-t)+(1+2t)=8",39,INK),
            mtx(r"4+2t=8",40,CYAN),
            mtx(r"\boxed{t=2}",44,GOLD),
            mtx(r"M(2)=(3,0,5)",42,GREEN),
            mtx(r"3+0+5=8",36,GREEN),
        ).arrange(DOWN,buff=0.30)
        for e in sol:self.play(Write(e),run_time=0.58)
        self.narrate(
            "Thay ba tọa độ của M theo t vào phương trình x cộng y cộng z bằng tám. Các hạng t và âm t triệt tiêu một phần, ta được bốn cộng hai t bằng tám, nên t bằng hai. Khi đó vị trí là ba, không, năm. Kiểm tra ba cộng không cộng năm đúng bằng tám, nên điểm này nằm chính xác trên mặt phẳng Q.",
            1.8,
        )

        self.clear_stage(); self.set_2d(); self.add_header_footer("Một mở rộng rất đáng nhớ", "Mặt cầu radar", "Mở rộng")
        ext=VGroup(
            txt("Nếu vùng phủ radar là mặt cầu",27,INK),
            mtx(r"x^2+y^2+z^2=R^2",42,BLUE),
            txt("và đường bay là",27,INK),
            mtx(r"M(t)=(x(t),y(t),z(t))",38,CYAN),
            txt("thì thời điểm vào/ra vùng phủ được tìm từ",27,INK),
            mtx(r"x^2(t)+y^2(t)+z^2(t)=R^2",40,GOLD),
        ).arrange(DOWN,buff=0.28)
        self.play(FadeIn(ext),run_time=0.8)
        self.narrate(
            "Cùng ý tưởng đó, nếu ranh giới không phải mặt phẳng mà là mặt cầu radar, ta chỉ cần thay tọa độ chuyển động vào phương trình mặt cầu. Các nghiệm theo t chính là những thời điểm thiết bị đi vào hoặc đi ra vùng phủ. Đây là cách nối Oxyz với bài toán chuyển động rất tự nhiên mà không cần dùng hàm ẩn phức tạp.",
            1.8,
        )

    # ======================================================
    # SUMMARY + CHALLENGE
    # ======================================================
    def summary(self):
        self.clear_stage(); self.set_2d(); self.add_header_footer("Bản đồ giải Oxyz thực tế", "Từ bối cảnh đến công thức", "Tổng kết")
        steps=VGroup(
            bullet("1. Chọn hệ trục và đọc đúng đơn vị của tọa độ.",INK,27,BLUE),
            bullet("2. Viết vị trí dưới dạng điểm hoặc điểm chuyển động M(t).",INK,27,CYAN),
            bullet("3. Khoảng cách nhỏ nhất: ưu tiên tối ưu D²(t).",INK,27,GOLD),
            bullet("4. Ranh giới phẳng: dùng phương trình mặt phẳng và vectơ pháp tuyến.",INK,27,ORANGE),
            bullet("5. Thay ngược kết quả vào bối cảnh: thời gian, mét, ngưỡng an toàn.",INK,27,GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.36).shift(DOWN*0.05)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.38)
        self.narrate(
            "Khi gặp Oxyz thực tế, đừng bắt đầu bằng công thức. Hãy chọn hệ trục, đọc đơn vị, rồi viết tọa độ của đối tượng. Nếu đối tượng chuyển động, tọa độ sẽ phụ thuộc t. Nếu cần khoảng cách nhỏ nhất, ưu tiên D bình phương. Nếu gặp ranh giới, nhận diện nó là mặt phẳng hay mặt cầu. Cuối cùng luôn đổi kết quả trở lại đơn vị thật và trả lời đúng câu hỏi của tình huống.",
            2.0,
        )

        self.clear_stage(); self.set_2d(); self.add_header_footer("Bài tự luyện", "Dừng video và thử trước", "Tự luyện")
        q=VGroup(
            txt("Một drone chuyển động theo",27,INK),
            mtx(r"M(t)=(4-t,\,t,\,2),\qquad 0\le t\le4",40,GOLD),
            txt("Radar đặt tại",27,INK),
            mtx(r"O(0,0,0)",38,CYAN),
            txt("Tìm thời điểm drone gần radar nhất.",28,GREEN,BOLD),
        ).arrange(DOWN,buff=0.26)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate("Bài tự luyện: drone có tọa độ bốn trừ t, t, hai. Hãy tìm thời điểm gần radar O nhất. Gợi ý: đừng đạo hàm căn, hãy viết D bình phương trước.",1.5)
        self.wait(1.0)
        sol=VGroup(
            mtx(r"D^2(t)=(4-t)^2+t^2+4",37,INK),
            mtx(r"=2(t-2)^2+12",40,CYAN),
            mtx(r"\boxed{t=2,\quad D_{\min}=2\sqrt3}",42,GOLD),
        ).arrange(DOWN,buff=0.30).shift(DOWN*0.35)
        self.play(FadeIn(sol),run_time=0.8)
        self.narrate("Khai triển rồi hoàn thành bình phương, D bình phương bằng hai nhân t trừ hai bình phương cộng mười hai. Vì thế t bằng hai và khoảng cách nhỏ nhất bằng hai căn ba. Đây chính là mẫu bài các em nên nhận diện thật nhanh.",1.5)

        self.clear_stage(); self.set_2d()
        end=VGroup(
            txt("VIDEO 06 – OXYZ THỰC TẾ",42,GOLD,BOLD),
            VGroup(txt("vị trí",26,CYAN), Arrow(LEFT*0.25,RIGHT*0.25,color=CYAN,stroke_width=3), txt("khoảng cách",26,CYAN), Arrow(LEFT*0.25,RIGHT*0.25,color=CYAN,stroke_width=3), txt("chuyển động",26,CYAN), Arrow(LEFT*0.25,RIGHT*0.25,color=CYAN,stroke_width=3), txt("ranh giới",26,CYAN)).arrange(RIGHT,buff=0.10),
            txt("3D để nhìn – đại số để giải – đơn vị để kết luận",28,INK),
            txt("Tiếp theo: Xác suất – Thống kê từ dữ liệu thực tế",25,MUTED),
            txt(TEN_THAY,21,MUTED),
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(end),run_time=0.9)
        self.narrate("Video tiếp theo trong lộ trình sẽ chuyển sang xác suất và thống kê từ dữ liệu thực tế: bảng số liệu, trung bình, độ lệch chuẩn, xác suất có điều kiện và những câu đúng sai rất dễ nhầm. Hẹn gặp các em ở video tiếp theo.",1.6)

    def construct(self):
        self.intro()
        self.ex1_drone_position()
        self.ex2_radar_min_distance()
        self.ex3_two_drones()
        self.ex4_safety_plane()
        self.ex5_line_plane()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_06_Oxyz_thuc_te_1080p"
    config.format = "mp4"
    config.write_to_movie = True
    config.disable_caching = False

    print(f"Voice: {GIONG_DOC} | Rate: {TOC_DO_DOC} | Pitch: {PITCH}")
    scene = SangLesson()
    scene.render()

    video_path = Path(scene.renderer.file_writer.movie_file_path)
    if not video_path.exists():
        raise RuntimeError(f"Khong tim thay video Manim cuoi: {video_path}")

    video_duration = probe_duration(video_path)
    master_wav = ROOT / "master_narration_oxyz_thuc_te.wav"
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

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
# SERIES ROADMAP - TOAN THUC TE / CT GDPT 2018
# 01. Mo hinh hoa + toi uu mot bien
# 02. Ham nhieu cong thuc: gia, phi, nguong, suc chua
# 03. Toc do - thoi gian - nang suat - chi phi
# 04. Doc do thi thuc te + dao ham + Dung/Sai
# 05. Tich phan trong bai toan thuc te
# 06. Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke tu du lieu
# 08. Tong hop Dung/Sai + tra loi ngan kieu TN THPT (FILE NAY)
#
# Nguyen tac:
# - Uu tien bai toan thuc te, ham tuong minh, hinh dong.
# - Han che toi da ham an.
# - Moi tinh huong: boi canh -> mo hinh -> quan sat -> giai -> dien giai.
# - Cong thuc dung MathTex; tieng Viet dung Text.
# - File standalone, khong phu thuoc module noi bo.
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


def tf_badge(is_true):
    label = "ĐÚNG" if is_true else "SAI"
    col = GREEN if is_true else RED
    box = RoundedRectangle(
        width=1.35, height=0.55, corner_radius=0.11,
        fill_color=col, fill_opacity=0.16,
        stroke_color=col, stroke_width=2,
    )
    word = txt(label, 22, col, BOLD).move_to(box)
    return VGroup(box, word)


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


# ==========================================================
# LESSON
# ==========================================================
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
    def reset_2d_camera(self):
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
        self.reset_2d_camera()
        self.add_header_footer(title, "DỮ KIỆN CHUNG", progress)
        panel = make_panel(12.3, 5.15).shift(DOWN * 0.08)
        self.play(FadeIn(panel), run_time=0.45)
        group = VGroup()
        for item in content:
            if isinstance(item, Mobject):
                mob = item
            else:
                mob = fit_width(txt(item, 27, INK), 11.1)
            group.add(mob)
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(panel)
        fit_width(group, 11.15)
        for mob in group:
            self.play(FadeIn(mob, shift=UP * 0.08), run_time=0.28)
        self.narrate(voice, 1.8)

    def make_axes(self, xr, yr, xlen=7.0, ylen=5.2, shift=LEFT*2.65, xnums=True, ynums=True):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2},
            x_axis_config={"include_numbers": xnums, "font_size": 21},
            y_axis_config={"include_numbers": ynums, "font_size": 21},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 27), mtx("y", 27))
        return ax, labels

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        self.reset_2d_camera()
        g = VGroup(
            txt("VIDEO 08 – TỔNG HỢP LUYỆN THI", 45, GOLD, BOLD),
            txt("Đúng/Sai + Trả lời ngắn từ một tình huống thực tế", 29, CYAN),
            VGroup(
                mtx(r"f", 34, BLUE),
                txt("–", 28, MUTED),
                mtx(r"\int", 36, GREEN),
                txt("–", 28, MUTED),
                mtx(r"Oxyz", 34, ORANGE),
                txt("–", 28, MUTED),
                mtx(r"P(A\mid B)", 34, PURPLE),
            ).arrange(RIGHT, buff=0.18),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.32)
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.7)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), run_time=1.0)
        self.narrate(
            "Chào các em. Video tám là bài tổng hợp của cả series. Thay vì mỗi câu cho một dữ kiện riêng, ta sẽ luyện cách đọc một tình huống thực tế rồi xử lý nhiều mệnh đề hoặc một đáp số ngắn. Các em sẽ gặp hàm nhiều công thức, đạo hàm, tích phân, hình học Oxyz và xác suất. Mục tiêu không phải bấm máy thật nhanh, mà là nhận đúng mô hình và kiểm tra từng kết luận một cách có hệ thống.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Chiến lược làm bài", "Đọc dữ kiện chung trước, xét từng ý sau", "Mở đầu")
        steps = VGroup(
            bullet("1. Gạch chân đại lượng, đơn vị và miền giá trị.", INK, 26, BLUE),
            bullet("2. Viết đúng mô hình trước khi tính.", INK, 26, CYAN),
            bullet("3. Đúng/Sai: mỗi mệnh đề là một bài nhỏ độc lập.", INK, 26, GOLD),
            bullet("4. Trả lời ngắn: tìm đúng đại lượng đề hỏi, không dừng giữa chừng.", INK, 26, ORANGE),
            bullet("5. Luôn diễn giải kết quả trở lại bối cảnh thực tế.", INK, 26, GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        fit_width(steps, 11.7)
        for s in steps:
            self.play(FadeIn(s, shift=RIGHT*0.12), run_time=0.34)
        self.narrate(
            "Năm bước xuyên suốt video là: đọc đại lượng và đơn vị; dựng mô hình; xét từng mệnh đề riêng; với trả lời ngắn thì đi đến đúng đại lượng cuối cùng; và cuối cùng phải kiểm tra xem con số tìm được có ý nghĩa trong bối cảnh hay không.",
            1.6,
        )

    # ======================================================
    # CASE 1 - PIECEWISE REVENUE TRUE/FALSE
    # ======================================================
    def case1_revenue_tf(self):
        self.show_problem(
            "Tình huống 1 – Giá vé và sức chứa",
            [
                "Một rạp có tối đa 120 chỗ. Nếu giá vé là p nghìn đồng thì nhu cầu dự kiến là:",
                mtx(r"d(p)=240-2p,\qquad 30\le p\le100", 38, CYAN),
                "Số vé bán thực tế không vượt quá sức chứa:",
                mtx(r"q(p)=\min\{120,\,240-2p\}", 38, GOLD),
                mtx(r"R(p)=p\,q(p)", 40, GREEN),
            ],
            "Một rạp có một trăm hai mươi chỗ. Khi giá vé là p nghìn đồng, nhu cầu dự kiến bằng hai trăm bốn mươi trừ hai p. Tuy nhiên số vé bán thực tế không thể vượt quá một trăm hai mươi. Ta cần đọc đúng điểm chuyển cơ chế rồi xét bốn mệnh đề.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Tình huống 1", "Từ sức chứa đến hàm doanh thu từng đoạn", "1/5")
        deriv = VGroup(
            mtx(r"240-2p=120\iff p=60", 38, GOLD),
            mtx(r"q(p)=\begin{cases}120,&30\le p\le60\\240-2p,&60<p\le100\end{cases}", 37, CYAN),
            mtx(r"R(p)=\begin{cases}120p,&30\le p\le60\\240p-2p^2,&60<p\le100\end{cases}", 37, GREEN),
        ).arrange(DOWN, buff=0.38)
        fit_width(deriv, 11.4)
        self.play(FadeIn(deriv), run_time=0.9)
        self.narrate(
            "Điểm quan trọng nhất là p bằng sáu mươi. Với giá không quá sáu mươi, nhu cầu ít nhất bằng sức chứa nên rạp bán đủ một trăm hai mươi vé. Khi giá vượt sáu mươi, số vé bán mới thực sự bằng hàm nhu cầu. Vì vậy doanh thu phải viết thành hai công thức.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Tình huống 1", "Đồ thị doanh thu và điểm gãy p = 60", "1/5")
        ax = Axes(
            x_range=[30, 105, 10], y_range=[3000, 7600, 1000],
            x_length=7.0, y_length=5.0, tips=False,
            axis_config={"color": MUTED, "stroke_width": 2},
            x_axis_config={"include_numbers": True, "font_size": 20},
            y_axis_config={"include_numbers": True, "font_size": 18},
        ).shift(LEFT*2.65+DOWN*0.1)
        labels = ax.get_axis_labels(mtx("p", 26), mtx("R", 26))
        c1 = ax.plot(lambda p: 120*p, x_range=[30,60], color=BLUE, stroke_width=4)
        c2 = ax.plot(lambda p: 240*p-2*p*p, x_range=[60,100], color=GREEN, stroke_width=4)
        pv = ValueTracker(35)
        point = always_redraw(lambda: Dot(
            ax.c2p(
                pv.get_value(),
                120*pv.get_value() if pv.get_value() <= 60 else 240*pv.get_value()-2*pv.get_value()**2
            ),
            radius=0.075, color=GOLD
        ))
        vline = always_redraw(lambda: DashedLine(
            ax.c2p(pv.get_value(),3000),
            point.get_center(), color=GOLD, dash_length=0.08
        ))
        kink = Dot(ax.c2p(60,7200), radius=0.085, color=RED)
        right = VGroup(
            mtx(r"R(60)=7200", 37, GOLD),
            mtx(r"R'_-(60)=120", 34, BLUE),
            mtx(r"R'_+(60)=0", 34, GREEN),
        ).arrange(DOWN, buff=0.30).to_edge(RIGHT, buff=0.55).shift(UP*0.5)
        self.play(Create(ax), FadeIn(labels), Create(c1), Create(c2), FadeIn(kink), FadeIn(right), run_time=1.1)
        self.play(FadeIn(point), Create(vline), run_time=0.5)
        self.narrate_play(
            "Quan sát điểm vàng khi giá tăng. Trước sáu mươi nghìn, doanh thu tăng tuyến tính vì rạp luôn bán đủ chỗ. Đúng tại sáu mươi nghìn doanh thu đạt bảy triệu hai trăm nghìn đồng. Sau mốc đó, tăng giá làm số vé giảm và doanh thu đi xuống.",
            pv.animate.set_value(95), min_time=5.0,
        )

        self.clear_stage(); self.add_header_footer("Tình huống 1", "Bốn mệnh đề Đúng/Sai", "1/5")
        statements = VGroup(
            VGroup(txt("a)",24,GOLD,BOLD), mtx(r"p\le60\Rightarrow q(p)=120",30,INK), tf_badge(True)).arrange(RIGHT,buff=0.22),
            VGroup(txt("b)",24,GOLD,BOLD), mtx(r"R'(60)\ \text{exists}",30,INK), tf_badge(False)).arrange(RIGHT,buff=0.22),
            VGroup(txt("c)",24,GOLD,BOLD), mtx(r"R_{\max}=7200\ \text{at}\ p=60",30,INK), tf_badge(True)).arrange(RIGHT,buff=0.22),
            VGroup(txt("d)",24,GOLD,BOLD), mtx(r"R(80)>R(60)",30,INK), tf_badge(False)).arrange(RIGHT,buff=0.22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.46)
        self.play(FadeIn(statements), run_time=0.9)
        calc = VGroup(
            mtx(r"R(80)=240\cdot80-2\cdot80^2=6400", 34, CYAN),
            mtx(r"6400<7200", 36, RED),
        ).arrange(DOWN,buff=0.20).to_edge(DOWN,buff=0.62)
        self.play(FadeIn(calc),run_time=0.6)
        self.narrate(
            "Mệnh đề a đúng. Mệnh đề b sai vì đạo hàm trái bằng một trăm hai mươi còn đạo hàm phải bằng không, nên đạo hàm tại điểm gãy không tồn tại. Mệnh đề c đúng. Mệnh đề d sai vì tại giá tám mươi nghìn, doanh thu chỉ còn sáu triệu bốn trăm nghìn. Kết quả là đúng, sai, đúng, sai.",
            2.0,
        )

    # ======================================================
    # CASE 2 - INTEGRAL SHORT ANSWER
    # ======================================================
    def case2_integral_short(self):
        self.show_problem(
            "Tình huống 2 – Bể nước và trả lời ngắn",
            [
                "Một bể đang có 120 lít nước.",
                "Tốc độ nước vào bể trong 6 phút đầu là:",
                mtx(r"q_{\rm in}(t)=20-2t", 38, BLUE),
                "Nước thoát ra với tốc độ không đổi:",
                mtx(r"q_{\rm out}(t)=5", 38, ORANGE),
                "Hỏi sau 6 phút bể có bao nhiêu lít nước?",
            ],
            "Đây là dạng trả lời ngắn. Điều dễ sai là lấy tích phân của dòng vào mà quên dòng ra, hoặc tính được lượng thay đổi rồi quên cộng một trăm hai mươi lít ban đầu.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Tình huống 2", "Tốc độ ròng quyết định lượng thay đổi", "2/5")
        ax = Axes(
            x_range=[0,6.5,1], y_range=[0,22,5],
            x_length=7.0, y_length=4.9, tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":20},
        ).shift(LEFT*2.65+DOWN*0.15)
        labels = ax.get_axis_labels(mtx("t",26), mtx("q",26))
        cin = ax.plot(lambda t:20-2*t, x_range=[0,6], color=BLUE, stroke_width=4)
        cout = ax.plot(lambda t:5, x_range=[0,6], color=ORANGE, stroke_width=4)
        net = ax.plot(lambda t:15-2*t, x_range=[0,6], color=GREEN, stroke_width=4)
        tau = ValueTracker(0.2)
        area = always_redraw(lambda: ax.get_area(
            net, x_range=[0, max(0.21,tau.get_value())],
            color=GREEN, opacity=0.28
        ))
        point = always_redraw(lambda: Dot(ax.c2p(tau.get_value(),15-2*tau.get_value()),radius=0.065,color=GOLD))
        formula = VGroup(
            mtx(r"r(t)=q_{\rm in}(t)-q_{\rm out}(t)=15-2t",34,GREEN),
            mtx(r"V(6)=120+\int_0^6(15-2t)\,dt",36,GOLD),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.35).shift(UP*1.0)
        self.play(Create(ax),FadeIn(labels),Create(cin),Create(cout),Create(net),FadeIn(formula),run_time=1.0)
        self.play(FadeIn(area),FadeIn(point),run_time=0.5)
        self.narrate_play(
            "Đường xanh lá là tốc độ thay đổi ròng, bằng dòng vào trừ dòng ra. Khi thời gian chạy từ không đến sáu phút, phần diện tích được tô chính là lượng nước tăng thêm trong bể.",
            tau.animate.set_value(6), min_time=4.5,
        )
        solve = VGroup(
            mtx(r"\int_0^6(15-2t)\,dt=\left[15t-t^2\right]_0^6",34,INK),
            mtx(r"=90-36=54",38,CYAN),
            mtx(r"V(6)=120+54=174",40,GOLD),
            mtx(r"\boxed{174}",48,GREEN),
        ).arrange(DOWN,buff=0.26).to_edge(RIGHT,buff=0.50).shift(DOWN*0.85)
        self.play(FadeIn(solve),run_time=0.9)
        self.narrate(
            "Tích phân tốc độ ròng bằng năm mươi bốn lít. Đây mới chỉ là lượng tăng thêm. Cộng với một trăm hai mươi lít ban đầu, ta được một trăm bảy mươi bốn lít. Với câu trả lời ngắn, đáp số cần nhập là một trăm bảy mươi bốn.",
            1.8,
        )

    # ======================================================
    # CASE 3 - OXYZ SHORT ANSWER
    # ======================================================
    def case3_oxyz_short(self):
        self.show_problem(
            "Tình huống 3 – Drone gần radar nhất",
            [
                "Trong hệ trục Oxyz, drone chuyển động theo:",
                mtx(r"M(t)=(t+2,\,2t+1,\,6-t),\qquad0\le t\le5", 36, CYAN),
                "Radar đặt tại gốc tọa độ O.",
                "Tìm thời điểm drone gần radar nhất.",
            ],
            "Ta chuyển sang Oxyz. Drone có ba tọa độ đều phụ thuộc thời gian. Đề chỉ hỏi thời điểm gần radar nhất, vì vậy không cần tối ưu căn khoảng cách. Ta tối ưu bình phương khoảng cách.",
            "3/5",
        )

        self.clear_stage()
        self.set_camera_orientation(phi=68*DEGREES, theta=-48*DEGREES, zoom=0.92)
        fixed_title = title_block("Tình huống 3", "Điểm drone chuyển động thật trong Oxyz")
        fixed_footer = footer("3/5")
        self.add_fixed_in_frame_mobjects(fixed_title, fixed_footer)
        ax = ThreeDAxes(
            x_range=[0,8,1], y_range=[0,12,2], z_range=[0,7,1],
            x_length=6.6, y_length=6.2, z_length=4.8,
            axis_config={"color":MUTED,"stroke_width":2},
        ).shift(DOWN*0.35)
        path = ParametricFunction(
            lambda u: ax.c2p(u+2,2*u+1,6-u),
            t_range=[0,5], color=BLUE, stroke_width=4
        )
        tv = ValueTracker(0)
        drone = always_redraw(lambda: Dot3D(
            ax.c2p(tv.get_value()+2,2*tv.get_value()+1,6-tv.get_value()),
            radius=0.075,color=GOLD
        ))
        ray = always_redraw(lambda: Line3D(
            ax.c2p(0,0,0),
            ax.c2p(tv.get_value()+2,2*tv.get_value()+1,6-tv.get_value()),
            color=CYAN, thickness=0.018
        ))
        self.play(Create(ax),Create(path),FadeIn(drone),Create(ray),run_time=1.2)
        self.begin_ambient_camera_rotation(rate=0.04)
        self.narrate_play(
            "Điểm vàng là drone, còn đoạn xanh nối về gốc là khoảng cách đến radar. Khi drone chuyển động, đoạn này co lại rồi dài ra. Ta cần tìm đúng thời điểm ngắn nhất.",
            tv.animate.set_value(5), min_time=5.0,
        )
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(ax),FadeOut(path),FadeOut(drone),FadeOut(ray),run_time=0.5)
        self.remove_fixed_in_frame_mobjects(fixed_title,fixed_footer)
        self.reset_2d_camera()

        self.add_header_footer("Tình huống 3", "Tối ưu bình phương khoảng cách", "3/5")
        solve = VGroup(
            mtx(r"D^2(t)=(t+2)^2+(2t+1)^2+(6-t)^2", 38, INK),
            mtx(r"=6t^2-4t+41", 40, CYAN),
            mtx(r"=6\left(t-\frac13\right)^2+\frac{121}{3}", 40, GOLD),
            mtx(r"\boxed{t=\frac13}", 48, GREEN),
        ).arrange(DOWN,buff=0.34)
        fit_width(solve,11.3)
        self.play(FadeIn(solve),run_time=0.9)
        self.narrate(
            "Bình phương khoảng cách là sáu t bình phương trừ bốn t cộng bốn mươi mốt. Hoàn thành bình phương, ta được sáu nhân t trừ một phần ba tất cả bình phương, cộng một trăm hai mươi mốt phần ba. Vì vậy thời điểm gần nhất là t bằng một phần ba. Đây là đáp số ngắn gọn nhất của bài.",
            1.9,
        )

        extra = mtx(r"D_{\min}=\sqrt{\frac{121}{3}}=\frac{11}{\sqrt3}\approx6.35", 38, MUTED).to_edge(DOWN,buff=0.72)
        self.play(Write(extra),run_time=0.6)
        self.narrate("Nếu đề hỏi thêm khoảng cách nhỏ nhất, kết quả là mười một chia căn ba, xấp xỉ sáu phẩy ba năm đơn vị.",1.2)

    # ======================================================
    # CASE 4 - PROBABILITY TRUE/FALSE
    # ======================================================
    def case4_probability_tf(self):
        self.show_problem(
            "Tình huống 4 – Kiểm tra chất lượng",
            [
                "Nhà máy có hai dây chuyền A và B.",
                mtx(r"P(A)=0.7,\qquad P(B)=0.3", 38, BLUE),
                mtx(r"P(D\mid A)=0.02,\qquad P(D\mid B)=0.06", 38, ORANGE),
                "D là biến cố sản phẩm bị lỗi.",
                "Xét bốn mệnh đề.",
            ],
            "Một nhà máy có hai dây chuyền. A sản xuất bảy mươi phần trăm sản lượng và có tỷ lệ lỗi hai phần trăm. B sản xuất ba mươi phần trăm và có tỷ lệ lỗi sáu phần trăm. Ta phải phân biệt xác suất lỗi chung với xác suất nguồn gốc khi đã biết sản phẩm bị lỗi.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Tình huống 4", "Cây xác suất: đi xuôi trước, Bayes đi ngược sau", "4/5")
        O = LEFT*5.1+UP*0.4
        Apos = LEFT*2.3+UP*1.6
        Bpos = LEFT*2.3+DOWN*1.2
        AD = RIGHT*0.6+UP*2.1
        AG = RIGHT*0.6+UP*1.0
        BD = RIGHT*0.6+DOWN*0.65
        BG = RIGHT*0.6+DOWN*1.75
        root = Dot(O,color=GOLD,radius=0.07)
        lines = VGroup(
            Line(O,Apos,color=BLUE), Line(O,Bpos,color=PURPLE),
            Line(Apos,AD,color=RED), Line(Apos,AG,color=GREEN),
            Line(Bpos,BD,color=RED), Line(Bpos,BG,color=GREEN),
        )
        labs = VGroup(
            mtx(r"A:\ 0.7",28,BLUE).next_to(Apos,UP,buff=0.08),
            mtx(r"B:\ 0.3",28,PURPLE).next_to(Bpos,DOWN,buff=0.08),
            mtx(r"D:\ 0.02",26,RED).next_to(AD,RIGHT,buff=0.10),
            mtx(r"\overline D:\ 0.98",26,GREEN).next_to(AG,RIGHT,buff=0.10),
            mtx(r"D:\ 0.06",26,RED).next_to(BD,RIGHT,buff=0.10),
            mtx(r"\overline D:\ 0.94",26,GREEN).next_to(BG,RIGHT,buff=0.10),
        )
        calc = VGroup(
            mtx(r"P(D)=0.7\cdot0.02+0.3\cdot0.06", 34, INK),
            mtx(r"=0.014+0.018=0.032", 36, CYAN),
            mtx(r"P(B\mid D)=\frac{0.018}{0.032}=0.5625", 36, GOLD),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.35).shift(UP*0.45)
        self.play(FadeIn(root),Create(lines),FadeIn(labs),FadeIn(calc),run_time=1.1)
        self.narrate(
            "Cây xác suất cho thấy có hai con đường dẫn tới sản phẩm lỗi. Từ A cho xác suất không phẩy không một bốn, từ B cho không phẩy không một tám. Cộng lại, xác suất một sản phẩm ngẫu nhiên bị lỗi là không phẩy không ba hai, tức ba phẩy hai phần trăm. Nếu đã biết sản phẩm lỗi, xác suất nó đến từ B là không phẩy năm sáu hai năm.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Tình huống 4", "Bốn mệnh đề Đúng/Sai", "4/5")
        st = VGroup(
            VGroup(txt("a)",24,GOLD,BOLD),mtx(r"P(D)=3.2\%",30,INK),tf_badge(True)).arrange(RIGHT,buff=0.24),
            VGroup(txt("b)",24,GOLD,BOLD),mtx(r"P(B\cap D)=1.8\%",30,INK),tf_badge(True)).arrange(RIGHT,buff=0.24),
            VGroup(txt("c)",24,GOLD,BOLD),mtx(r"P(B\mid D)=60\%",30,INK),tf_badge(False)).arrange(RIGHT,buff=0.24),
            VGroup(txt("d)",24,GOLD,BOLD),mtx(r"P(D\mid B)>P(D)",30,INK),tf_badge(True)).arrange(RIGHT,buff=0.24),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.46)
        self.play(FadeIn(st),run_time=0.9)
        note = mtx(r"6\%>3.2\%", 38, GREEN).to_edge(DOWN,buff=0.65)
        self.play(Write(note),run_time=0.5)
        self.narrate(
            "Mệnh đề a đúng. b cũng đúng vì xác suất vừa thuộc B vừa lỗi bằng không phẩy ba nhân không phẩy không sáu, tức một phẩy tám phần trăm. c sai vì kết quả Bayes là năm mươi sáu phẩy hai lăm phần trăm, không phải sáu mươi. d đúng vì tỷ lệ lỗi của riêng B là sáu phần trăm, lớn hơn tỷ lệ lỗi chung ba phẩy hai phần trăm.",
            1.9,
        )

    # ======================================================
    # CASE 5 - ENERGY: DERIVATIVE + INTEGRAL TRUE/FALSE
    # ======================================================
    def case5_energy_tf(self):
        self.show_problem(
            "Tình huống 5 – Năng lượng trong pin",
            [
                "Công suất ròng P(t), đơn vị kW, được mô hình trong 6 giờ:",
                mtx(r"P(t)=\begin{cases}4t,&0\le t\le2\\8,&2<t\le4\\-2(t-4),&4<t\le6\end{cases}", 36, GOLD),
                mtx(r"E(0)=20\ \mathrm{kWh}", 38, CYAN),
                "Biết rằng:",
                mtx(r"E'(t)=P(t)", 40, GREEN),
                "Xét bốn mệnh đề về năng lượng E(t).",
            ],
            "Bài cuối kết hợp đọc đồ thị đạo hàm và tích phân. P của t là công suất ròng, còn E của t là năng lượng đang có trong pin. Vì E phẩy bằng P, dấu của P cho biết E tăng hay giảm; còn diện tích dưới đồ thị P cho biết lượng năng lượng thay đổi.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Tình huống 5", "Đồ thị P(t): dấu cho xu hướng, diện tích cho lượng thay đổi", "5/5")
        ax = Axes(
            x_range=[0,6.5,1], y_range=[-5,9,2],
            x_length=7.2, y_length=5.1, tips=False,
            axis_config={"color":MUTED,"stroke_width":2},
            x_axis_config={"include_numbers":True,"font_size":20},
            y_axis_config={"include_numbers":True,"font_size":20},
        ).shift(LEFT*2.65+DOWN*0.05)
        labels = ax.get_axis_labels(mtx("t",26),mtx("P",26))
        p1 = ax.plot(lambda t:4*t,x_range=[0,2],color=BLUE,stroke_width=4)
        p2 = ax.plot(lambda t:8,x_range=[2,4],color=GREEN,stroke_width=4)
        p3 = ax.plot(lambda t:-2*(t-4),x_range=[4,6],color=ORANGE,stroke_width=4)
        a1 = ax.get_area(p1,x_range=[0,2],color=BLUE,opacity=0.23)
        a2 = ax.get_area(p2,x_range=[2,4],color=GREEN,opacity=0.23)
        a3 = ax.get_area(p3,x_range=[4,6],color=ORANGE,opacity=0.28)
        tcur = ValueTracker(0.1)
        def pval(t):
            if t <= 2: return 4*t
            if t <= 4: return 8
            return -2*(t-4)
        dot = always_redraw(lambda: Dot(ax.c2p(tcur.get_value(),pval(tcur.get_value())),radius=0.07,color=GOLD))
        side = VGroup(
            mtx(r"\Delta E_{0\to2}=\frac12\cdot2\cdot8=8",31,BLUE),
            mtx(r"\Delta E_{2\to4}=2\cdot8=16",31,GREEN),
            mtx(r"\Delta E_{4\to6}=-\frac12\cdot2\cdot4=-4",31,ORANGE),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.30).shift(UP*0.45)
        self.play(Create(ax),FadeIn(labels),Create(p1),Create(p2),Create(p3),FadeIn(a1),FadeIn(a2),FadeIn(a3),FadeIn(side),FadeIn(dot),run_time=1.1)
        self.narrate_play(
            "Từ không đến bốn giờ, công suất ròng không âm nên năng lượng tăng. Sau bốn giờ, công suất âm nên năng lượng giảm. Ba vùng diện tích lần lượt cho mức thay đổi tám, mười sáu và âm bốn kilowatt giờ.",
            tcur.animate.set_value(6), min_time=5.0,
        )

        self.clear_stage(); self.add_header_footer("Tình huống 5", "Tính các mốc năng lượng", "5/5")
        calc = VGroup(
            mtx(r"E(2)=20+8=28", 36, BLUE),
            mtx(r"E(4)=28+16=44", 38, GOLD),
            mtx(r"E(6)=44-4=40", 36, ORANGE),
            mtx(r"\max_{[0,6]}E(t)=44", 40, GREEN),
        ).arrange(DOWN,buff=0.34)
        self.play(FadeIn(calc),run_time=0.8)
        self.narrate(
            "Bắt đầu từ hai mươi kilowatt giờ. Sau hai giờ có hai mươi tám. Sau bốn giờ có bốn mươi bốn. Hai giờ cuối pin mất bốn kilowatt giờ nên còn bốn mươi. Vì E tăng trước bốn và giảm sau bốn, năng lượng lớn nhất là bốn mươi bốn tại t bằng bốn.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Tình huống 5", "Bốn mệnh đề Đúng/Sai", "5/5")
        st = VGroup(
            VGroup(txt("a)",24,GOLD,BOLD),mtx(r"E(t)\ \text{increases on}\ [0,4]",30,INK),tf_badge(True)).arrange(RIGHT,buff=0.24),
            VGroup(txt("b)",24,GOLD,BOLD),mtx(r"E(4)=44\ \mathrm{kWh}",30,INK),tf_badge(True)).arrange(RIGHT,buff=0.24),
            VGroup(txt("c)",24,GOLD,BOLD),mtx(r"E(6)=36\ \mathrm{kWh}",30,INK),tf_badge(False)).arrange(RIGHT,buff=0.24),
            VGroup(txt("d)",24,GOLD,BOLD),mtx(r"\max E(t)=44\ \mathrm{kWh}",30,INK),tf_badge(True)).arrange(RIGHT,buff=0.24),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.46)
        self.play(FadeIn(st),run_time=0.9)
        self.narrate(
            "Mệnh đề a đúng, hiểu tăng trên toàn đoạn theo nghĩa không giảm và thực tế tăng đến t bằng bốn. b đúng. c sai vì năng lượng cuối cùng là bốn mươi chứ không phải ba mươi sáu. d đúng. Kết quả là đúng, đúng, sai, đúng.",
            1.7,
        )

        throughput = VGroup(
            txt("Nếu đề hỏi tổng năng lượng trao đổi:",25,MUTED),
            mtx(r"8+16+4=28\ \mathrm{kWh}",34,CYAN),
            txt("phải cộng độ lớn các vùng, không dùng tích phân đại số.",24,MUTED),
        ).arrange(DOWN,buff=0.18).to_edge(DOWN,buff=0.54)
        self.play(FadeIn(throughput),run_time=0.5)
        self.narrate(
            "Một mở rộng hay: nếu hỏi tổng năng lượng đã trao đổi theo cả hai chiều, ta cộng độ lớn các vùng là hai mươi tám kilowatt giờ. Còn tích phân đại số chỉ cho thay đổi ròng bằng hai mươi kilowatt giờ.",
            1.4,
        )

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_stage(); self.reset_2d_camera()
        self.add_header_footer("Bản đồ chiến lược", "Một tình huống – nhiều tầng suy luận", "Tổng kết")
        g = VGroup(
            VGroup(mtx(r"\min,\max",34,BLUE),txt("→ đạo hàm / điểm gãy / biên",26,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"\int r(t)\,dt",34,GREEN),txt("→ lượng tích lũy",26,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"D^2(t)",34,ORANGE),txt("→ tối ưu khoảng cách Oxyz",26,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"P(A\mid B)",34,PURPLE),txt("→ đổi mẫu số theo điều kiện",26,INK)).arrange(RIGHT,buff=0.24),
            VGroup(mtx(r"f'(t)",34,GOLD),txt("→ xu hướng; diện tích → mức thay đổi",26,INK)).arrange(RIGHT,buff=0.24),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.36)
        fit_width(g,11.7)
        for row in g:
            self.play(FadeIn(row,shift=RIGHT*0.12),run_time=0.35)
        self.narrate(
            "Năm tình huống hôm nay thực chất dùng năm chiếc chìa khóa: tối ưu phải kiểm tra cả điểm gãy và biên; tích phân của tốc độ cho lượng tích lũy; khoảng cách Oxyz nên thử bình phương; xác suất có điều kiện phải đổi mẫu số; và đạo hàm cho xu hướng còn diện tích dưới đạo hàm cho mức thay đổi.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Checklist trước khi chốt đáp án", "Rất hữu ích cho Đúng/Sai và trả lời ngắn", "Tổng kết")
        checks = VGroup(
            bullet("Đơn vị đã đúng chưa?", INK, 27, BLUE),
            bullet("Đang xét f hay f'?", INK, 27, CYAN),
            bullet("Có điểm gãy hoặc biên miền bị bỏ sót không?", INK, 27, GOLD),
            bullet("Tích phân là thay đổi ròng hay tổng độ lớn?", INK, 27, ORANGE),
            bullet("Điều kiện xác suất đã đổi mẫu số chưa?", INK, 27, PURPLE),
            bullet("Đáp số cuối có đúng yêu cầu đề hỏi không?", INK, 27, GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.28)
        fit_width(checks,11.7)
        self.play(LaggedStart(*[FadeIn(x,shift=RIGHT*0.12) for x in checks],lag_ratio=0.08),run_time=1.3)
        self.narrate(
            "Trước khi chốt đáp án, hãy tự hỏi sáu câu: đơn vị đã đúng chưa; đang xét hàm hay đạo hàm; có bỏ quên điểm gãy hoặc biên không; tích phân đang biểu diễn thay đổi ròng hay tổng độ lớn; xác suất có điều kiện đã đổi mẫu số chưa; và cuối cùng con số mình ghi có đúng thứ đề đang hỏi hay không.",
            1.8,
        )

        self.clear_stage()
        end = VGroup(
            txt("VIDEO 08 – HOÀN THÀNH CHẶNG 1", 42, GOLD, BOLD),
            txt("Từ mô hình hóa đến câu Đúng/Sai và trả lời ngắn", 28, CYAN),
            mtx(r"\boxed{\text{read}\to\text{model}\to\text{solve}\to\text{interpret}}", 36, GREEN),
            txt("Chặng tiếp theo: các chuyên đề thực tế phân hóa cao.", 25, MUTED),
            txt(TEN_THAY, 21, MUTED),
        ).arrange(DOWN,buff=0.32)
        fit_width(end,12.0)
        self.play(FadeIn(end),run_time=0.9)
        self.narrate(
            "Video tám khép lại chặng đầu của series. Các em đã đi từ mô hình hóa, hàm nhiều công thức, tối ưu, đọc đồ thị, tích phân, Oxyz, xác suất đến bài tổng hợp. Chặng tiếp theo sẽ đi vào các bài thực tế phân hóa cao hơn, nhưng vẫn giữ nguyên nguyên tắc: hình dung được tình huống trước, rồi mới dùng toán để giải.",
            1.7,
        )

    def construct(self):
        self.intro()
        self.case1_revenue_tf()
        self.case2_integral_short()
        self.case3_oxyz_short()
        self.case4_probability_tf()
        self.case5_energy_tf()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_08_tong_hop_luyen_thi_1080p"
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
    master_wav = ROOT / "master_narration_video08.wav"
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

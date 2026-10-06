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
# 05. Tich phan: quang duong - luu luong - dien nang - luong tich luy (FILE NAY)
# 06. Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke tu du lieu
# 08. Tong hop Dung/Sai + tra loi ngan kieu TN THPT
#
# Nguyen tac dai han:
# - Uu tien mo hinh thuc te, ham tuong minh, do thi dong.
# - Han che toi da ham an.
# - Moi bai: hieu don vi -> doc do thi -> lap tich phan -> tinh -> dien giai ket qua.
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


class SangLesson(Scene):
    def setup(self):
        self.audio_events = []

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

    def make_axes(self, xr, yr, xlen=7.0, ylen=5.0, shift=LEFT*2.6, x_label="t", y_label="y"):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx(x_label, 26), mtx(y_label, 26))
        return ax, labels

    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("TOÁN THỰC TẾ HÀM SỐ – VIDEO 05", 43, GOLD, BOLD),
            txt("TÍCH PHÂN = LƯỢNG TÍCH LŨY", 37, INK, BOLD),
            txt("Tốc độ → quãng đường | Lưu lượng → thể tích | Công suất → điện năng", 27, CYAN),
            mtx(r"\text{rate}\ \xrightarrow{\int}\ \text{total}", 39, GOLD),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.30)
        self.play(FadeIn(g[0], shift=UP*0.15), run_time=0.6)
        self.play(FadeIn(g[1]), FadeIn(g[2]), Write(g[3]), FadeIn(g[4]), run_time=1.0)
        self.narrate(
            "Chào các em. Nếu đạo hàm trả lời câu hỏi một đại lượng đang thay đổi nhanh đến mức nào, thì tích phân làm công việc ngược lại: cộng những thay đổi rất nhỏ để thu được tổng lượng đã tích lũy. Vì vậy diện tích dưới đồ thị vận tốc cho quãng đường, diện tích dưới đồ thị lưu lượng cho thể tích nước, còn diện tích dưới đồ thị công suất cho điện năng. Video này sẽ biến ý tưởng đó thành năm bài toán thực tế có hình động.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Một nguyên lý dùng cho rất nhiều bài", "Đơn vị giúp đoán đúng phép toán", "Mở đầu")
        rows = VGroup(
            VGroup(mtx(r"v(t)\,[\mathrm{km/h}]",32,BLUE), Arrow(LEFT*0.35,RIGHT*0.35,color=CYAN), mtx(r"\int v(t)\,dt\,[\mathrm{km}]",32,GOLD)).arrange(RIGHT,buff=0.16),
            VGroup(mtx(r"q(t)\,[\mathrm{L/min}]",32,BLUE), Arrow(LEFT*0.35,RIGHT*0.35,color=CYAN), mtx(r"\int q(t)\,dt\,[\mathrm{L}]",32,GOLD)).arrange(RIGHT,buff=0.16),
            VGroup(mtx(r"P(t)\,[\mathrm{kW}]",32,BLUE), Arrow(LEFT*0.35,RIGHT*0.35,color=CYAN), mtx(r"\int P(t)\,dt\,[\mathrm{kWh}]",32,GOLD)).arrange(RIGHT,buff=0.16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        fit_width(rows, 11.7)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.12) for r in rows],lag_ratio=0.12),run_time=1.2)
        self.narrate(
            "Một mẹo rất mạnh là nhìn đơn vị. Kilômét trên giờ nhân với giờ cho kilômét. Lít trên phút nhân với phút cho lít. Kilowatt nhân với giờ cho kilowatt giờ. Tích phân chính là phiên bản chính xác của phép cộng rate nhân khoảng thời gian khi rate thay đổi liên tục.",
            1.7,
        )


    def why_integral(self):
        self.clear_stage(); self.add_header_footer("Vì sao tích phân biểu diễn lượng tích lũy?", "Cộng rất nhiều thay đổi nhỏ", "Ý tưởng nền")
        ax, labels = self.make_axes((0,7,1),(0,6,1),xlen=7.0,ylen=4.8,shift=LEFT*2.7,x_label="t",y_label="r")
        curve = ax.plot(lambda t: 2+0.5*t, x_range=[0,6], color=BLUE, stroke_width=4)
        bars=VGroup()
        for i in range(6):
            h=2+0.5*i
            poly=Polygon(ax.c2p(i,0),ax.c2p(i+1,0),ax.c2p(i+1,h),ax.c2p(i,h),
                         stroke_color=CYAN,stroke_width=1.5,fill_color=CYAN,fill_opacity=0.22)
            bars.add(poly)
        rhs=VGroup(
            mtx(r"\Delta Q_i\approx r(t_i)\,\Delta t",34,INK),
            mtx(r"\Delta Q\approx\sum_i r(t_i)\,\Delta t",34,CYAN),
            mtx(r"\Delta t\to0",32,ORANGE),
            mtx(r"\boxed{\Delta Q=\int_a^b r(t)\,dt}",39,GOLD),
        ).arrange(DOWN,buff=0.32).to_edge(RIGHT,buff=0.38).shift(UP*0.25)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(rhs),run_time=1.0)
        self.play(LaggedStart(*[FadeIn(b) for b in bars],lag_ratio=0.10),run_time=1.2)
        self.narrate(
            "Ta hiểu bản chất trước khi dùng công thức. Chia thời gian thành nhiều đoạn ngắn. Trong một đoạn rất ngắn, tốc độ thay đổi r gần như không đổi, nên lượng tăng thêm xấp xỉ r nhân độ dài thời gian. Cộng các hình chữ nhật nhỏ cho ta một xấp xỉ của tổng lượng thay đổi. Khi chia thời gian ngày càng mịn, tổng các hình chữ nhật tiến tới đúng diện tích dưới đồ thị, và giới hạn đó chính là tích phân.",
            2.0,
        )
        fine=VGroup()
        for i in range(12):
            a=i*0.5; b=(i+1)*0.5; h=2+0.5*a
            poly=Polygon(ax.c2p(a,0),ax.c2p(b,0),ax.c2p(b,h),ax.c2p(a,h),
                         stroke_color=GREEN,stroke_width=1.0,fill_color=GREEN,fill_opacity=0.20)
            fine.add(poly)
        self.play(ReplacementTransform(bars,fine),run_time=1.0)
        self.narrate(
            "Các hình chữ nhật càng hẹp thì phần thừa thiếu quanh đường cong càng nhỏ. Vì vậy tích phân không phải một mẹo tính diện tích tách rời thực tế; nó chính là phép cộng chính xác của vô số thay đổi vi phân. Trong các bài sau, chỉ cần nhận ra đại lượng trên trục đứng là một tốc độ theo thời gian, các em nên nghĩ ngay đến lượng tích lũy bằng tích phân.",
            1.7,
        )

    # ======================================================
    # 1. VELOCITY -> DISTANCE
    # ======================================================
    def model1_velocity_distance(self):
        self.show_problem(
            "Bài 1 – Vận tốc và quãng đường",
            [
                txt("Một xe thử nghiệm có vận tốc trong 6 giờ đầu:",27,INK),
                mtx(r"v(t)=-t^2+6t,\qquad 0\le t\le6",40,GOLD),
                txt("v tính bằng km/h, t tính bằng giờ.",25,MUTED),
                txt("Tính quãng đường xe đi được trong 6 giờ.",27,CYAN,BOLD),
            ],
            "Vận tốc của xe không cố định. Nó tăng từ không, đạt cực đại rồi giảm về không. Muốn tính quãng đường, ta không thể lấy một vận tốc duy nhất nhân sáu giờ. Ta phải cộng quãng đường rất nhỏ v của t nhân d t trên toàn bộ khoảng thời gian.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 1 – Vận tốc → quãng đường", "Diện tích được tô dần chính là quãng đường tích lũy", "1/5")
        ax, labels = self.make_axes((0,7,1),(0,10,2),xlen=7.0,ylen=4.9,shift=LEFT*2.7,x_label="t",y_label="v")
        curve = ax.plot(lambda t: -t*t+6*t, x_range=[0,6], color=BLUE, stroke_width=4)
        T = ValueTracker(0.05)
        dot = always_redraw(lambda: Dot(ax.c2p(T.get_value(), -T.get_value()**2+6*T.get_value()), radius=0.075, color=GOLD))
        area = always_redraw(lambda: ax.get_area(curve, x_range=[0,max(0.05,T.get_value())], color=CYAN, opacity=0.28))
        guide = always_redraw(lambda: DashedLine(ax.c2p(T.get_value(),0), dot.get_center(), color=MUTED, dash_length=0.10))
        rhs = VGroup(
            mtx(r"s=\int_0^6v(t)\,dt",36,INK),
            mtx(r"=\int_0^6(-t^2+6t)\,dt",34,CYAN),
            mtx(r"=\left[-\frac{t^3}{3}+3t^2\right]_0^6",34,CYAN),
            mtx(r"\boxed{s=36\ \mathrm{km}}",42,GOLD),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.38).shift(UP*0.25)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(rhs),run_time=1.0)
        self.play(FadeIn(area),FadeIn(dot),Create(guide),run_time=0.6)
        self.narrate_play(
            "Hãy nhìn vùng màu xanh nhạt. Khi thời gian tăng, vùng dưới đồ thị được tô thêm từng chút một. Mỗi lát rất mỏng có diện tích gần bằng v của t nhân d t, chính là quãng đường đi trong một khoảng thời gian rất nhỏ. Tổng tất cả các lát từ không đến sáu giờ là tích phân của vận tốc.",
            T.animate.set_value(6.0),min_time=5.0,
        )
        self.narrate(
            "Tính nguyên hàm ta được âm t mũ ba chia ba cộng ba t bình phương. Thay cận sáu và không cho kết quả ba mươi sáu kilômét. Ở bài này vận tốc luôn không âm nên tích phân vận tốc đồng thời chính là tổng quãng đường.",
            1.7,
        )

    # ======================================================
    # 2. FLOW RATE -> VOLUME
    # ======================================================
    def model2_flow_volume(self):
        self.show_problem(
            "Bài 2 – Lưu lượng nước và thể tích",
            [
                txt("Một bể đang được bơm nước với lưu lượng",27,INK),
                mtx(r"q(t)=6+2t,\qquad 0\le t\le5",40,GOLD),
                txt("q tính bằng L/phút, t tính bằng phút.",25,MUTED),
                txt("Ban đầu bể có 120 L. Hỏi sau 5 phút có bao nhiêu lít?",27,CYAN,BOLD),
            ],
            "Ở đây trục đứng không phải lượng nước đang có trong bể, mà là lưu lượng nước đi vào mỗi phút. Vì vậy tích phân của q chỉ cho lượng nước được thêm vào. Muốn biết lượng nước cuối cùng, ta còn phải cộng với một trăm hai mươi lít ban đầu.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 2 – Lưu lượng → lượng nước", "Phân biệt lượng ban đầu và lượng tăng thêm", "2/5")
        ax, labels = self.make_axes((0,6,1),(0,18,3),xlen=6.9,ylen=4.9,shift=LEFT*2.7,x_label="t",y_label="q")
        curve = ax.plot(lambda t: 6+2*t, x_range=[0,5], color=BLUE, stroke_width=4)
        T=ValueTracker(0.05)
        area=always_redraw(lambda: ax.get_area(curve,x_range=[0,max(0.05,T.get_value())],color=GREEN,opacity=0.30))
        dot=always_redraw(lambda: Dot(ax.c2p(T.get_value(),6+2*T.get_value()),radius=0.075,color=GOLD))
        rhs=VGroup(
            mtx(r"\Delta V=\int_0^5(6+2t)\,dt",35,INK),
            mtx(r"=\left[6t+t^2\right]_0^5",34,CYAN),
            mtx(r"=30+25=55\ \mathrm{L}",36,GREEN),
            mtx(r"V_{\mathrm{final}}=120+55",35,INK),
            mtx(r"\boxed{V_{\mathrm{final}}=175\ \mathrm{L}}",40,GOLD),
        ).arrange(DOWN,buff=0.27).to_edge(RIGHT,buff=0.30).shift(UP*0.25)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(rhs),run_time=1.0)
        self.play(FadeIn(area),FadeIn(dot),run_time=0.6)
        self.narrate_play(
            "Lưu lượng tăng tuyến tính từ sáu lên mười sáu lít mỗi phút. Vùng được tô từ không đến thời điểm t chính là tổng lượng nước đã bơm thêm. Khi t đạt năm phút, diện tích này bằng năm mươi lăm lít.",
            T.animate.set_value(5.0),min_time=4.7,
        )
        self.narrate(
            "Nhưng đề hỏi lượng nước có trong bể chứ không chỉ lượng bơm thêm. Vì ban đầu đã có một trăm hai mươi lít, ta cộng một trăm hai mươi với năm mươi lăm và được một trăm bảy mươi lăm lít. Đây là lỗi rất thường gặp: quên giá trị ban đầu.",
            1.8,
        )

    # ======================================================
    # 3. POWER -> ENERGY + AVERAGE POWER
    # ======================================================
    def model3_power_energy(self):
        self.show_problem(
            "Bài 3 – Công suất điện mặt trời",
            [
                txt("Trong 12 giờ ban ngày, công suất một hệ pin được mô hình bởi",27,INK),
                mtx(r"P(t)=3\sin\frac{\pi t}{12},\qquad 0\le t\le12",38,GOLD),
                txt("P tính bằng kW, t tính bằng giờ.",25,MUTED),
                txt("Tính điện năng tạo ra và công suất trung bình.",27,CYAN,BOLD),
            ],
            "Công suất của hệ pin bằng không vào đầu và cuối ngày, lớn nhất gần giữa trưa. Tích phân công suất theo thời gian cho điện năng. Sau đó chia điện năng cho mười hai giờ sẽ cho công suất trung bình trong cả khoảng.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 3 – Công suất → điện năng", "Diện tích dưới đồ thị có đơn vị kWh", "3/5")
        ax, labels = self.make_axes((0,13,2),(0,3.5,0.5),xlen=7.0,ylen=4.8,shift=LEFT*2.7,x_label="t",y_label="P")
        curve=ax.plot(lambda t:3*math.sin(math.pi*t/12),x_range=[0,12],color=BLUE,stroke_width=4)
        T=ValueTracker(0.05)
        area=always_redraw(lambda: ax.get_area(curve,x_range=[0,max(0.05,T.get_value())],color=ORANGE,opacity=0.30))
        dot=always_redraw(lambda: Dot(ax.c2p(T.get_value(),3*math.sin(math.pi*T.get_value()/12)),radius=0.075,color=GOLD))
        rhs=VGroup(
            mtx(r"E=\int_0^{12}P(t)\,dt",35,INK),
            mtx(r"=3\int_0^{12}\sin\frac{\pi t}{12}\,dt",32,CYAN),
            mtx(r"=\frac{72}{\pi}\ \mathrm{kWh}\approx22.92\ \mathrm{kWh}",34,GREEN),
            mtx(r"\overline P=\frac{E}{12}=\frac6\pi\ \mathrm{kW}",34,INK),
            mtx(r"\boxed{\overline P\approx1.91\ \mathrm{kW}}",38,GOLD),
        ).arrange(DOWN,buff=0.27).to_edge(RIGHT,buff=0.22).shift(UP*0.20)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(rhs),run_time=1.0)
        self.play(FadeIn(area),FadeIn(dot),run_time=0.6)
        self.narrate_play(
            "Vùng màu cam là điện năng tích lũy từ đầu ngày đến thời điểm đang xét. Đơn vị cũng kiểm tra được ngay: kilowatt nhân giờ cho kilowatt giờ. Khi quét hết mười hai giờ, ta lấy toàn bộ diện tích dưới nửa sóng sin này.",
            T.animate.set_value(12.0),min_time=5.0,
        )
        self.narrate(
            "Tích phân cho bảy mươi hai trên pi kilowatt giờ, xấp xỉ hai mươi hai phẩy chín hai. Công suất trung bình bằng điện năng chia tổng thời gian, nên bằng sáu trên pi, xấp xỉ một phẩy chín một kilowatt. Giá trị trung bình không phải giá trị cực đại ba kilowatt.",
            1.8,
        )

    # ======================================================
    # 4. RATE OF CHANGE -> STOCK / INVENTORY
    # ======================================================
    def model4_inventory_rate(self):
        self.show_problem(
            "Bài 4 – Tốc độ thay đổi lượng hàng",
            [
                txt("Một kho có 500 sản phẩm lúc đầu ngày.",27,INK),
                txt("Tốc độ thay đổi số hàng trong kho được mô hình bởi",27,INK),
                mtx(r"r(t)=24-4t,\qquad 0\le t\le8",40,GOLD),
                txt("r tính bằng sản phẩm/giờ. Tìm lượng hàng sau 8 giờ và thời điểm nhiều nhất.",26,CYAN,BOLD),
            ],
            "Đây là dạng rất đáng luyện vì đề cho tốc độ thay đổi chứ không cho trực tiếp số hàng. Khi r dương, lượng hàng tăng. Khi r âm, lượng hàng giảm. Tích phân của r từ đầu đến một thời điểm cho độ thay đổi ròng so với năm trăm sản phẩm ban đầu.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 4 – Tốc độ thay đổi → lượng tồn kho", "Dấu của r(t) cho biết tăng hay giảm", "4/5")
        ax, labels = self.make_axes((0,9,1),(-10,28,5),xlen=7.0,ylen=4.9,shift=LEFT*2.7,x_label="t",y_label="r")
        curve=ax.plot(lambda t:24-4*t,x_range=[0,8],color=BLUE,stroke_width=4)
        zero=DashedLine(ax.c2p(0,0),ax.c2p(8,0),color=MUTED,dash_length=0.1)
        T=ValueTracker(0.05)
        dot=always_redraw(lambda: Dot(ax.c2p(T.get_value(),24-4*T.get_value()),radius=0.075,color=GOLD))
        rhs=VGroup(
            mtx(r"r(t)>0\iff0\le t<6",32,GREEN),
            mtx(r"r(6)=0",32,GOLD),
            mtx(r"r(t)<0\iff6<t\le8",32,RED),
            mtx(r"N(t)=500+\int_0^t r(u)\,du",34,CYAN),
            mtx(r"N(8)=500+\int_0^8(24-4t)\,dt",31,INK),
            mtx(r"\boxed{N(8)=564}",39,GOLD),
        ).arrange(DOWN,buff=0.25).to_edge(RIGHT,buff=0.25).shift(UP*0.18)
        self.play(Create(ax),FadeIn(labels),Create(zero),Create(curve),FadeIn(rhs),run_time=1.0)
        self.play(FadeIn(dot),run_time=0.5)
        self.narrate_play(
            "Điểm vàng chạy từ trái sang phải. Trong sáu giờ đầu, r nằm trên trục hoành nên lượng hàng tăng. Tại sáu giờ, r bằng không: đó là thời điểm chuyển từ tăng sang giảm. Vì vậy lượng hàng lớn nhất xảy ra đúng tại t bằng sáu, dù bản thân r tại đó chỉ bằng không.",
            T.animate.set_value(8.0),min_time=5.0,
        )
        maxbox=VGroup(
            mtx(r"N(6)=500+\int_0^6(24-4t)\,dt",31,INK),
            mtx(r"=500+72=572",34,CYAN),
            mtx(r"\boxed{N_{\max}=572}",39,GOLD),
        ).arrange(DOWN,buff=0.22).to_edge(DOWN,buff=0.55).shift(RIGHT*2.0)
        self.play(FadeIn(maxbox),run_time=0.7)
        self.narrate(
            "Sau tám giờ, tích phân r bằng sáu mươi bốn, nên kho có năm trăm sáu mươi bốn sản phẩm. Nhưng lượng lớn nhất không ở cuối ngày. Tại sáu giờ, phần diện tích dương tích lũy đạt bảy mươi hai, nên kho đạt năm trăm bảy mươi hai sản phẩm. Sau đó r âm làm lượng hàng giảm bớt.",
            1.9,
        )

    # ======================================================
    # 5. SIGNED VELOCITY: DISPLACEMENT VS DISTANCE
    # ======================================================
    def model5_signed_velocity(self):
        self.show_problem(
            "Bài 5 – Tích phân có dấu: độ dời hay quãng đường?",
            [
                txt("Một vật chuyển động trên một đường thẳng với vận tốc",27,INK),
                mtx(r"v(t)=t-2,\qquad 0\le t\le5",40,GOLD),
                txt("v tính bằng m/s. Tính độ dời và tổng quãng đường.",27,CYAN,BOLD),
                txt("Chú ý: vật đổi chiều tại thời điểm vận tốc bằng 0.",25,MUTED),
            ],
            "Đây là bài quan trọng nhất của video. Khi vận tốc âm, vật đi theo chiều ngược lại. Tích phân vận tốc có dấu nên phần nằm dưới trục hoành bị trừ. Vì thế tích phân vận tốc cho độ dời. Muốn tổng quãng đường, ta phải cộng độ lớn của từng phần, tức tích phân giá trị tuyệt đối của vận tốc.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 5 – Độ dời khác tổng quãng đường", "Vùng dưới trục hoành mang dấu âm", "5/5")
        ax, labels = self.make_axes((0,6,1),(-3,4,1),xlen=7.0,ylen=4.9,shift=LEFT*2.7,x_label="t",y_label="v")
        curve=ax.plot(lambda t:t-2,x_range=[0,5],color=BLUE,stroke_width=4)
        zero=Line(ax.c2p(0,0),ax.c2p(5.2,0),color=MUTED,stroke_width=2)
        neg_area=ax.get_area(curve,x_range=[0,2],color=RED,opacity=0.30)
        pos_area=ax.get_area(curve,x_range=[2,5],color=GREEN,opacity=0.30)
        T=ValueTracker(0.0)
        dot=always_redraw(lambda: Dot(ax.c2p(T.get_value(),T.get_value()-2),radius=0.075,color=GOLD))
        rhs=VGroup(
            mtx(r"\Delta x=\int_0^5(t-2)\,dt",33,INK),
            mtx(r"=\left[\frac{t^2}{2}-2t\right]_0^5=\frac52\ \mathrm{m}",32,CYAN),
            mtx(r"S=\int_0^5|t-2|\,dt",33,INK),
            mtx(r"=\int_0^2(2-t)\,dt+\int_2^5(t-2)\,dt",29,GREEN),
            mtx(r"=2+\frac92=\boxed{\frac{13}{2}\ \mathrm{m}}",34,GOLD),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.18).shift(UP*0.18)
        self.play(Create(ax),FadeIn(labels),Create(zero),Create(curve),FadeIn(rhs),run_time=1.0)
        self.play(FadeIn(neg_area),FadeIn(pos_area),FadeIn(dot),run_time=0.7)
        self.narrate_play(
            "Từ không đến hai giây, vận tốc âm nên vật đi theo chiều âm. Tại hai giây, vận tốc bằng không và vật đổi chiều. Từ hai đến năm giây, vận tốc dương. Vùng đỏ nằm dưới trục hoành được tính âm trong tích phân, còn vùng xanh được tính dương.",
            T.animate.set_value(5.0),min_time=5.0,
        )
        compare=VGroup(
            VGroup(txt("Độ dời",24,CYAN,BOLD),mtx(r"=\frac52\ \mathrm{m}",32,CYAN)).arrange(RIGHT,buff=0.15),
            VGroup(txt("Quãng đường",24,GOLD,BOLD),mtx(r"=\frac{13}{2}\ \mathrm{m}",32,GOLD)).arrange(RIGHT,buff=0.15),
        ).arrange(DOWN,buff=0.22).to_edge(DOWN,buff=0.55).shift(RIGHT*2.1)
        self.play(FadeIn(compare),run_time=0.7)
        self.narrate(
            "Vì thế độ dời chỉ bằng hai phẩy năm mét: phần đi lùi và đi tới triệt tiêu một phần. Nhưng tổng quãng đường phải cộng cả hai đoạn theo độ lớn, nên bằng sáu phẩy năm mét. Khi vận tốc đổi dấu, luôn kiểm tra đề hỏi độ dời hay tổng quãng đường.",
            1.8,
        )

    def summary(self):
        self.clear_stage(); self.add_header_footer("Bản đồ tư duy tích phân thực tế", "Đọc đơn vị → nhận rate → tích lũy", "Tổng kết")
        steps=VGroup(
            bullet("1. Xác định hàm đang cho là đại lượng hay tốc độ thay đổi của đại lượng.",INK,26,BLUE),
            bullet("2. Kiểm tra đơn vị để biết tích phân sẽ cho đại lượng gì.",INK,26,CYAN),
            bullet("3. Nếu có giá trị ban đầu, phải cộng lại sau khi tích phân.",INK,26,GOLD),
            bullet("4. Nếu rate đổi dấu, phân biệt lượng thay đổi ròng và tổng lượng tuyệt đối.",INK,26,ORANGE),
            bullet("5. Cuối cùng phải diễn giải đáp số trở lại ngữ cảnh thực tế.",INK,26,GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34).shift(DOWN*0.05)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.34)
        self.narrate(
            "Chốt lại năm bước. Hãy xác định mình đang được cho đại lượng hay tốc độ thay đổi của nó. Kiểm tra đơn vị. Lập tích phân trên đúng khoảng. Nếu đề có giá trị ban đầu, nhớ cộng lại. Và khi hàm tốc độ đổi dấu, phải phân biệt thay đổi ròng với tổng lượng tuyệt đối. Cuối cùng, đáp số phải có đơn vị và ý nghĩa thực tế rõ ràng.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài tự luyện – rất sát dạng trả lời ngắn", "Lưu lượng vào và ra đồng thời", "Tổng kết")
        q=VGroup(
            txt("Một bể có 200 L nước ban đầu.",27,INK),
            txt("Lưu lượng vào và ra lần lượt là",26,INK),
            mtx(r"q_{\mathrm{in}}(t)=10+t,\qquad q_{\mathrm{out}}(t)=4+\frac t2",37,GOLD),
            mtx(r"0\le t\le6",34,CYAN),
            txt("Hỏi sau 6 phút bể có bao nhiêu lít nước?",27,GREEN,BOLD),
        ).arrange(DOWN,buff=0.27)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate(
            "Bài tự luyện: khi có cả dòng vào và dòng ra, tốc độ thay đổi ròng của lượng nước bằng lưu lượng vào trừ lưu lượng ra. Các em hãy dừng video, lập một tích phân duy nhất rồi cộng với hai trăm lít ban đầu.",
            1.5,
        )
        sol=VGroup(
            mtx(r"r(t)=q_{\mathrm{in}}(t)-q_{\mathrm{out}}(t)=6+\frac t2",34,INK),
            mtx(r"V(6)=200+\int_0^6\left(6+\frac t2\right)dt",34,CYAN),
            mtx(r"=200+36+9",34,CYAN),
            mtx(r"\boxed{V(6)=245\ \mathrm{L}}",42,GOLD),
        ).arrange(DOWN,buff=0.28).shift(DOWN*0.2)
        self.play(FadeIn(sol),run_time=0.8)
        self.narrate(
            "Tốc độ thay đổi ròng là sáu cộng t chia hai. Tích phân từ không đến sáu cho bốn mươi lăm lít tăng thêm. Cộng với hai trăm lít ban đầu, ta được hai trăm bốn mươi lăm lít.",
            1.5,
        )

        self.clear_stage(); self.add_header_footer("Kế hoạch series", "Video 06: Oxyz trong bài toán thực tế", "Tổng kết")
        roadmap=VGroup(
            VGroup(mtx(r"01\to04",30,MUTED),txt("Mô hình hóa – tối ưu – hàm từng đoạn – đọc đồ thị",25,MUTED)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"05",30,GOLD),txt("Tích phân và lượng tích lũy",25,GOLD,BOLD)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"06",30,CYAN),txt("Oxyz thực tế: vị trí – khoảng cách – mặt phẳng – chuyển động",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"07",30,ORANGE),txt("Xác suất – thống kê từ dữ liệu",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"08",30,GREEN),txt("Tổng hợp Đúng/Sai + trả lời ngắn",25,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.32)
        fit_width(roadmap,11.7)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.1) for r in roadmap],lag_ratio=0.10),run_time=1.2)
        self.narrate(
            "Video tiếp theo sẽ chuyển sang hình học Oxyz nhưng vẫn giữ đúng tinh thần thực tế: vị trí của thiết bị, khoảng cách trong không gian, mặt phẳng giới hạn, đường bay và chuyển động. Ta vẫn ưu tiên hình trực quan và mô hình tường minh thay vì các biểu thức hàn lâm khó đọc.",
            1.7,
        )

        self.clear_stage()
        end=VGroup(
            txt("RATE × THỜI GIAN → LƯỢNG TÍCH LŨY",38,GOLD,BOLD),
            mtx(r"\boxed{\text{total}=\int \text{rate}\,dt}",43,CYAN),
            txt(TEN_THAY,22,MUTED),
        ).arrange(DOWN,buff=0.42)
        fit_width(end,11.8)
        self.play(FadeIn(end[0]),Write(end[1]),FadeIn(end[2]),run_time=0.9)
        self.narrate(
            "Nếu chỉ nhớ một điều sau video này, hãy nhớ rằng tích phân biến một tốc độ thay đổi thành tổng lượng tích lũy. Khi hiểu ý nghĩa đơn vị và diện tích dưới đồ thị, rất nhiều bài tích phân thực tế trở nên tự nhiên thay vì chỉ là thao tác tìm nguyên hàm.",
            1.6,
        )

    def construct(self):
        self.intro()
        self.why_integral()
        self.model1_velocity_distance()
        self.model2_flow_volume()
        self.model3_power_energy()
        self.model4_inventory_rate()
        self.model5_signed_velocity()
        self.summary()


def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_05_tich_phan_thuc_te_1080p"
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
    master_wav = ROOT / "master_narration_toan_thuc_te_ham_so_05.wav"
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

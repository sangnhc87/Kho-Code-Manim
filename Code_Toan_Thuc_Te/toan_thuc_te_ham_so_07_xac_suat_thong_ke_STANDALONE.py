from manim import *
from pathlib import Path
import hashlib
import json
import math
import statistics
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
# 06. Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke tu du lieu (FILE NAY)
# 08. Tong hop Dung/Sai + tra loi ngan kieu TN THPT
#
# Nguyen tac dai han:
# - Uu tien mo hinh thuc te, du lieu, ham tuong minh, hinh dong.
# - Han che toi da ham an.
# - Moi bai: doc boi canh -> du lieu/mo hinh -> giai -> dien giai.
# - Toan hien thi bang LaTeX/MathTex; tieng Viet bang Text.
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


def mean(data):
    return sum(data) / len(data)


def pop_variance(data):
    mu = mean(data)
    return sum((x - mu) ** 2 for x in data) / len(data)


def pop_sd(data):
    return math.sqrt(pop_variance(data))


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
# VISUAL HELPERS
# ==========================================================
def table_cell(w, h, text_mob, fill=PANEL, stroke=MUTED, opacity=0.75):
    box = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=opacity,
                    stroke_color=stroke, stroke_opacity=0.5, stroke_width=1.2)
    text_mob.move_to(box)
    return VGroup(box, text_mob)


def number_strip(data, label, color, y_shift=0.0):
    line = NumberLine(
        x_range=[min(data)-1, max(data)+1, 1],
        length=7.2,
        include_numbers=True,
        font_size=21,
        color=MUTED,
        include_tip=False,
    ).shift(LEFT*1.5 + UP*y_shift)
    dots = VGroup()
    counts = {}
    for value in data:
        level = counts.get(value, 0)
        counts[value] = level + 1
        d = Dot(line.n2p(value) + UP*(0.18 + 0.17*level), radius=0.065, color=color)
        dots.add(d)
    lab = txt(label, 25, color, BOLD).next_to(line, LEFT, buff=0.25)
    return VGroup(line, dots, lab)


def histogram(interval_labels, freqs, colors=None, width=7.0, height=4.4):
    if colors is None:
        colors = [BLUE]*len(freqs)
    max_f = max(freqs)
    baseline = Line(LEFT*width/2, RIGHT*width/2, color=MUTED, stroke_width=2)
    bars = VGroup()
    labels = VGroup()
    values = VGroup()
    n = len(freqs)
    bw = width/n * 0.78
    gap = width/n
    for i, (lab, f) in enumerate(zip(interval_labels, freqs)):
        h = height * f / max_f
        rect = Rectangle(width=bw, height=h, fill_color=colors[i], fill_opacity=0.72,
                         stroke_color=INK, stroke_opacity=0.25, stroke_width=1)
        x = -width/2 + (i+0.5)*gap
        rect.move_to([x, h/2, 0])
        bars.add(rect)
        labels.add(mtx(lab, 24, INK).next_to(rect, DOWN, buff=0.16))
        values.add(mtx(str(f), 25, GOLD).next_to(rect, UP, buff=0.08))
    g = VGroup(baseline, bars, labels, values)
    return g


def probability_tree():
    root = Dot(LEFT*4.7, radius=0.06, color=INK)
    a = Dot(LEFT*1.5+UP*1.55, radius=0.06, color=BLUE)
    b = Dot(LEFT*1.5+DOWN*1.55, radius=0.06, color=ORANGE)
    ad = Dot(RIGHT*2.0+UP*2.35, radius=0.055, color=RED)
    ag = Dot(RIGHT*2.0+UP*0.75, radius=0.055, color=GREEN)
    bd = Dot(RIGHT*2.0+DOWN*0.75, radius=0.055, color=RED)
    bg = Dot(RIGHT*2.0+DOWN*2.35, radius=0.055, color=GREEN)
    lines = VGroup(
        Line(root,a,color=BLUE), Line(root,b,color=ORANGE),
        Line(a,ad,color=RED), Line(a,ag,color=GREEN),
        Line(b,bd,color=RED), Line(b,bg,color=GREEN),
    )
    labels = VGroup(
        mtx(r"A:0.6", 25, BLUE).move_to((root.get_center()+a.get_center())/2+UP*0.2),
        mtx(r"B:0.4", 25, ORANGE).move_to((root.get_center()+b.get_center())/2+DOWN*0.2),
        mtx(r"D:0.02", 24, RED).move_to((a.get_center()+ad.get_center())/2+UP*0.14),
        mtx(r"\overline D:0.98", 24, GREEN).move_to((a.get_center()+ag.get_center())/2+DOWN*0.15),
        mtx(r"D:0.05", 24, RED).move_to((b.get_center()+bd.get_center())/2+UP*0.14),
        mtx(r"\overline D:0.95", 24, GREEN).move_to((b.get_center()+bg.get_center())/2+DOWN*0.15),
    )
    return VGroup(root,a,b,ad,ag,bd,bg,lines,labels)


# ==========================================================
# LESSON
# ==========================================================
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
        self.add_header_footer(title, "BÀI TOÁN", progress)
        panel = make_panel(12.3, 5.15).shift(DOWN*0.08)
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
            self.play(FadeIn(mob, shift=UP*0.08), run_time=0.28)
        self.narrate(voice, 1.8)

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("VIDEO 07 – XÁC SUẤT & THỐNG KÊ TỪ DỮ LIỆU", 42, GOLD, BOLD),
            txt("Đọc dữ liệu trước – tính toán sau", 30, CYAN),
            VGroup(mtx(r"\bar x",34,BLUE), mtx(r"s",34,GREEN), mtx(r"P(A\mid B)",34,ORANGE), mtx(r"P(A_i\mid B)",34,PURPLE)).arrange(RIGHT,buff=0.65),
            txt("Bảng số liệu – biểu đồ – điều kiện – Bayes – Đúng/Sai", 26, MUTED),
            txt(TEN_THAY, 21, MUTED),
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(g[0],shift=UP*0.15),run_time=0.7)
        self.play(FadeIn(g[1]),Write(g[2]),FadeIn(g[3]),FadeIn(g[4]),run_time=1.0)
        self.narrate(
            "Chào các em. Video này không bắt đầu bằng một trang công thức xác suất và thống kê. Ta bắt đầu bằng dữ liệu. Mỗi con số phải kể cho ta một câu chuyện: nhóm nào ổn định hơn, một tỉ lệ đang được tính trên nhóm nào, và khi đã biết một sản phẩm bị lỗi thì xác suất nó đến từ dây chuyền nào. Thầy sẽ đi từ dữ liệu thô, qua biểu đồ, đến xác suất có điều kiện và Bayes, rồi kết thúc bằng một câu đúng sai tổng hợp.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Ba câu hỏi trước khi bấm máy", "Thói quen đọc dữ liệu", "Mở đầu")
        steps=VGroup(
            bullet("1. Đại lượng đang đo là gì? Đơn vị nào?",INK,27,BLUE),
            bullet("2. Ta cần mức điển hình hay mức độ phân tán?",INK,27,GREEN),
            bullet("3. Xác suất đang lấy trên toàn bộ hay trên một nhóm đã biết?",INK,27,ORANGE),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.52)
        self.play(LaggedStart(*[FadeIn(s,shift=RIGHT*0.12) for s in steps],lag_ratio=0.18),run_time=1.2)
        self.narrate(
            "Ba câu hỏi này giúp tránh phần lớn lỗi. Trung bình trả lời mức điển hình. Độ lệch chuẩn trả lời mức phân tán. Còn trong xác suất có điều kiện, mẫu không gian đã bị thu nhỏ bởi điều kiện đứng sau dấu gạch dọc. Nếu không đọc đúng mẫu số mới, rất dễ đổi nhầm xác suất.",
            1.8,
        )

    # ======================================================
    # EX1 SAME MEAN DIFFERENT SPREAD
    # ======================================================
    def ex1_delivery(self):
        A=[18,19,20,20,21,22]
        B=[14,17,20,20,23,26]
        self.show_problem(
            "Bài 1 – Hai tuyến giao hàng, cùng trung bình",
            [
                "Thời gian giao 6 đơn hàng liên tiếp (phút):",
                mtx(r"A:\ 18,19,20,20,21,22",36,BLUE),
                mtx(r"B:\ 14,17,20,20,23,26",36,ORANGE),
                "Tuyến nào ổn định hơn?",
            ],
            "Hai tuyến giao hàng đều có sáu quan sát. Nếu chỉ nhìn trung bình, ta sẽ thấy chúng giống hệt nhau. Nhưng khách hàng còn quan tâm tính ổn định: thời gian có dao động nhiều hay không. Đây là lúc độ lệch chuẩn có ý nghĩa.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 1", "Cùng trung bình nhưng hình dạng dữ liệu khác nhau", "1/5")
        stripA=number_strip(A,"Tuyến A",BLUE,1.25)
        stripB=number_strip(B,"Tuyến B",ORANGE,-1.15)
        self.play(Create(stripA[0]),FadeIn(stripA[2]),run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d,scale=1.4) for d in stripA[1]],lag_ratio=0.10),run_time=1.1)
        self.play(Create(stripB[0]),FadeIn(stripB[2]),run_time=0.7)
        self.play(LaggedStart(*[FadeIn(d,scale=1.4) for d in stripB[1]],lag_ratio=0.10),run_time=1.1)
        mean_line = DashedLine(UP*2.45,DOWN*2.45,color=GOLD,dash_length=0.12).move_to(ORIGIN+LEFT*1.5)
        mean_lab=mtx(r"\bar x=20",30,GOLD).next_to(mean_line,UP,buff=0.08)
        self.play(Create(mean_line),FadeIn(mean_lab),run_time=0.6)
        self.narrate(
            "Trên hai trục số, đường vàng đánh dấu mốc hai mươi phút. Cả hai bộ dữ liệu đều có trung bình bằng hai mươi. Nhưng các chấm xanh nằm sát mốc hai mươi hơn rõ rệt, còn các chấm cam trải rộng từ mười bốn đến hai mươi sáu. Chỉ nhìn hình ta đã dự đoán tuyến A ổn định hơn.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài 1", "Định lượng độ phân tán bằng phương sai và độ lệch chuẩn", "1/5")
        calc=VGroup(
            mtx(r"\bar x_A=\bar x_B=20",38,GOLD),
            mtx(r"s_A^2=\frac{(-2)^2+(-1)^2+0^2+0^2+1^2+2^2}{6}=\frac53",34,BLUE),
            mtx(r"s_A=\sqrt{\frac53}\approx1.29",38,BLUE),
            mtx(r"s_B^2=\frac{(-6)^2+(-3)^2+0^2+0^2+3^2+6^2}{6}=15",34,ORANGE),
            mtx(r"s_B=\sqrt{15}\approx3.87",38,ORANGE),
            mtx(r"\boxed{s_A<s_B}",42,GREEN),
        ).arrange(DOWN,buff=0.24)
        fit_width(calc,11.7)
        for e in calc:self.play(Write(e),run_time=0.55)
        self.narrate(
            "Ta đo khoảng cách của mỗi giá trị tới trung bình. Tuyến A cho phương sai năm phần ba, nên độ lệch chuẩn khoảng một phẩy hai chín phút. Tuyến B có phương sai mười lăm, độ lệch chuẩn khoảng ba phẩy tám bảy phút. Vì độ lệch chuẩn A nhỏ hơn, A ổn định hơn. Một kết luận quan trọng là cùng trung bình không có nghĩa hai bộ dữ liệu giống nhau.",
            2.0,
        )

    # ======================================================
    # EX2 GROUPED DATA
    # ======================================================
    def ex2_grouped(self):
        self.show_problem(
            "Bài 2 – Dữ liệu ghép nhóm từ thời gian chờ",
            [
                "Một quầy dịch vụ ghi thời gian chờ của 30 khách:",
                mtx(r"[0,5):8,\quad[5,10):14,\quad[10,15):6,\quad[15,20):2",34,GOLD),
                "Ước lượng thời gian chờ trung bình từ bảng ghép nhóm.",
            ],
            "Khi dữ liệu nhiều, đề thường không cho từng quan sát riêng lẻ mà cho các khoảng và tần số. Ta không biết chính xác từng thời gian, nên sử dụng giá trị đại diện của mỗi lớp để ước lượng trung bình.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 2", "Biểu đồ tần số cho ta thấy phân bố trước khi tính", "2/5")
        h=histogram([r"[0,5)",r"[5,10)",r"[10,15)",r"[15,20)"],[8,14,6,2],[BLUE,CYAN,ORANGE,PURPLE])
        h.shift(DOWN*0.6)
        self.play(Create(h[0]),run_time=0.4)
        self.play(LaggedStart(*[GrowFromEdge(b,DOWN) for b in h[1]],lag_ratio=0.16),FadeIn(h[2]),FadeIn(h[3]),run_time=1.4)
        self.narrate(
            "Biểu đồ cho thấy lớp từ năm đến mười phút có nhiều khách nhất. Hai lớp bên phải ít dần, nên phần lớn khách không phải chờ quá lâu. Nhưng muốn có một con số đại diện, ta lấy trung điểm mỗi khoảng làm giá trị đại diện.",
            1.6,
        )
        reps=VGroup(
            mtx(r"x_i:\ 2.5,\ 7.5,\ 12.5,\ 17.5",34,CYAN),
            mtx(r"n_i:\ 8,\ 14,\ 6,\ 2",34,GOLD),
        ).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.45).shift(UP*1.1)
        self.play(FadeIn(reps),run_time=0.6)

        self.clear_stage(); self.add_header_footer("Bài 2", "Trung bình của mẫu ghép nhóm", "2/5")
        sol=VGroup(
            mtx(r"\bar x\approx\frac{\sum n_i x_i}{\sum n_i}",40,BLUE),
            mtx(r"=\frac{8\cdot2.5+14\cdot7.5+6\cdot12.5+2\cdot17.5}{30}",34,INK),
            mtx(r"=\frac{235}{30}\approx7.83",40,CYAN),
            VGroup(mtx(r"\boxed{\bar x\approx7.83}",40,GOLD), txt("phút",24,GOLD,BOLD)).arrange(RIGHT,buff=0.16),
        ).arrange(DOWN,buff=0.34)
        fit_width(sol,11.7)
        for e in sol:self.play(Write(e),run_time=0.62)
        self.narrate(
            "Trung điểm các lớp là hai phẩy năm, bảy phẩy năm, mười hai phẩy năm và mười bảy phẩy năm. Ta lấy trung bình có trọng số theo tần số. Kết quả khoảng bảy phẩy tám ba phút. Chữ xấp xỉ rất quan trọng, bởi dữ liệu đã bị ghép nhóm và ta chỉ dùng trung điểm đại diện chứ không biết từng thời gian thật.",
            1.9,
        )
        warning=VGroup(
            txt("Bẫy thường gặp:",26,RED,BOLD),
            txt("Không lấy trung bình đơn giản của 4 trung điểm lớp.",26,INK),
            mtx(r"\frac{2.5+7.5+12.5+17.5}{4}=10",34,RED),
        ).arrange(DOWN,buff=0.20).shift(DOWN*1.55)
        self.play(FadeIn(warning),run_time=0.6)
        self.narrate("Nếu lấy trung bình đơn giản của bốn trung điểm ta được mười phút, nhưng cách đó coi bốn lớp có số khách bằng nhau. Tần số khác nhau nên bắt buộc phải dùng trọng số.",1.4)

    # ======================================================
    # EX3 CONDITIONAL PROBABILITY TABLE
    # ======================================================
    def ex3_conditional(self):
        self.show_problem(
            "Bài 3 – Xác suất có điều kiện từ bảng hai chiều",
            [
                "Kiểm tra 100 sản phẩm từ hai dây chuyền:",
                mtx(r"n_A=60,\ D_A=3;\qquad n_B=40,\ D_B=4",34,GOLD),
                "Chọn ngẫu nhiên một sản phẩm. Tính các xác suất liên quan đến lỗi.",
            ],
            "Bài này rất quan trọng vì cùng một bảng số liệu nhưng đổi điều kiện là đổi mẫu số. Ta sẽ tính xác suất sản phẩm lỗi, xác suất lỗi khi đã biết sản phẩm đến từ B, và xác suất đến từ B khi đã biết sản phẩm bị lỗi.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 3", "Một bảng – ba mẫu số khác nhau", "3/5")
        cell_w,cell_h=2.2,0.82
        rows=[
            ["", "Lỗi", "Tốt", "Tổng"],
            ["A","3","57","60"],
            ["B","4","36","40"],
            ["Tổng","7","93","100"],
        ]
        colors=[[MUTED,GOLD,GREEN,CYAN],[BLUE,RED,GREEN,BLUE],[ORANGE,RED,GREEN,ORANGE],[CYAN,RED,GREEN,CYAN]]
        table=VGroup()
        for r in range(4):
            for c in range(4):
                content = txt(rows[r][c],24,colors[r][c],BOLD if r==0 or c==0 else NORMAL)
                cell=table_cell(cell_w,cell_h,content,fill=PANEL)
                cell.move_to([(c-1.5)*cell_w,(1.5-r)*cell_h-0.15,0])
                table.add(cell)
        self.play(LaggedStart(*[FadeIn(c) for c in table],lag_ratio=0.03),run_time=1.2)
        self.narrate(
            "Hãy nhìn ba mẫu số. Nếu chỉ hỏi xác suất lỗi, ta nhìn toàn bộ một trăm sản phẩm. Nếu đã biết sản phẩm thuộc B, ta chỉ còn bốn mươi sản phẩm ở hàng B. Nếu đã biết sản phẩm bị lỗi, ta chỉ còn bảy sản phẩm ở cột lỗi. Điều kiện đứng sau dấu gạch dọc quyết định tập ta đang xét.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài 3", "Phân biệt P(D|B) và P(B|D)", "3/5")
        sol=VGroup(
            mtx(r"P(D)=\frac7{100}=0.07",38,RED),
            mtx(r"P(D\mid B)=\frac4{40}=0.10",40,ORANGE),
            mtx(r"P(B\mid D)=\frac4{7}\approx0.571",40,BLUE),
            mtx(r"\boxed{P(D\mid B)\ne P(B\mid D)}",42,GOLD),
        ).arrange(DOWN,buff=0.38)
        for e in sol:self.play(Write(e),run_time=0.65)
        self.narrate(
            "Xác suất lỗi chung là bảy phần một trăm. Nếu đã biết sản phẩm từ dây chuyền B, bốn sản phẩm lỗi nằm trong bốn mươi sản phẩm B, nên xác suất là mười phần trăm. Nhưng nếu đã biết sản phẩm lỗi, câu hỏi đổi thành trong bảy sản phẩm lỗi có bao nhiêu sản phẩm từ B; đáp án là bốn phần bảy. Hai xác suất có điều kiện này hoàn toàn khác nhau.",
            2.0,
        )

    # ======================================================
    # EX4 TOTAL PROBABILITY + BAYES
    # ======================================================
    def ex4_bayes(self):
        self.show_problem(
            "Bài 4 – Truy ngược nguồn gốc bằng Bayes",
            [
                "Một nhà máy có hai dây chuyền:",
                mtx(r"P(A)=0.6,\qquad P(B)=0.4",36,BLUE),
                mtx(r"P(D\mid A)=0.02,\qquad P(D\mid B)=0.05",36,RED),
                "Biết một sản phẩm bị lỗi. Xác suất nó đến từ B là bao nhiêu?",
            ],
            "Đây là kiểu suy luận ngược rất thực tế. Ta biết tỉ lệ sản lượng của mỗi dây chuyền và tỉ lệ lỗi trong từng dây chuyền. Khi phát hiện một sản phẩm lỗi, ta muốn truy ngược xem nó có khả năng đến từ B bao nhiêu.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 4", "Cây xác suất: đi xuôi trước, đi ngược sau", "4/5")
        tree=probability_tree().shift(LEFT*0.3)
        self.play(FadeIn(tree[0]),run_time=0.3)
        self.play(Create(tree[7][0]),Create(tree[7][1]),FadeIn(tree[1]),FadeIn(tree[2]),run_time=0.8)
        self.play(Create(tree[7][2]),Create(tree[7][3]),Create(tree[7][4]),Create(tree[7][5]),FadeIn(tree[3]),FadeIn(tree[4]),FadeIn(tree[5]),FadeIn(tree[6]),run_time=1.0)
        self.play(FadeIn(tree[8]),run_time=0.7)
        self.narrate(
            "Cây xác suất giúp ta đi xuôi. Sáu mươi phần trăm sản phẩm từ A và bốn mươi phần trăm từ B. Trong nhánh A, hai phần trăm bị lỗi; trong nhánh B, năm phần trăm bị lỗi. Xác suất đi đến một lá bằng tích xác suất dọc đường đi.",
            1.8,
        )
        paths=VGroup(
            mtx(r"P(A\cap D)=0.6\cdot0.02=0.012",34,BLUE),
            mtx(r"P(B\cap D)=0.4\cdot0.05=0.020",34,ORANGE),
        ).arrange(DOWN,buff=0.20).to_edge(RIGHT,buff=0.25).shift(DOWN*0.1)
        fit_width(paths,5.3)
        self.play(FadeIn(paths),run_time=0.7)

        self.clear_stage(); self.add_header_footer("Bài 4", "Xác suất toàn phần rồi Bayes", "4/5")
        sol=VGroup(
            mtx(r"P(D)=0.6\cdot0.02+0.4\cdot0.05",37,INK),
            mtx(r"P(D)=0.032",42,RED),
            mtx(r"P(B\mid D)=\frac{P(B\cap D)}{P(D)}",38,BLUE),
            mtx(r"=\frac{0.4\cdot0.05}{0.032}=0.625",40,CYAN),
            mtx(r"\boxed{P(B\mid D)=62.5\%}",43,GOLD),
        ).arrange(DOWN,buff=0.30)
        for e in sol:self.play(Write(e),run_time=0.62)
        self.narrate(
            "Trước tiên cộng hai con đường dẫn tới lỗi: không phẩy sáu nhân không phẩy không hai, cộng không phẩy bốn nhân không phẩy không năm, được không phẩy không ba hai. Sau đó dùng Bayes: xác suất vừa thuộc B vừa lỗi chia cho xác suất lỗi. Kết quả sáu mươi hai phẩy năm phần trăm. B chỉ sản xuất bốn mươi phần trăm hàng, nhưng vì tỉ lệ lỗi cao hơn nên trong nhóm hàng lỗi, B chiếm tỉ trọng lớn hơn.",
            2.1,
        )
        insight=VGroup(
            txt("Ý nghĩa:",25,GREEN,BOLD),
            txt("Biết thêm thông tin D làm xác suất của B thay đổi.",25,INK),
        ).arrange(RIGHT,buff=0.18).to_edge(DOWN,buff=0.65)
        self.play(FadeIn(insight),run_time=0.5)

    # ======================================================
    # EX5 TRUE/FALSE INTEGRATED
    # ======================================================
    def ex5_true_false(self):
        self.show_problem(
            "Bài 5 – Một bảng dữ liệu, bốn mệnh đề Đúng/Sai",
            [
                "Khảo sát 200 khách hàng về việc dùng ứng dụng và mức hài lòng:",
                mtx(r"\begin{array}{c|cc|c}&S&\overline S&n\\\hline A&96&24&120\\\overline A&52&28&80\\\hline n&148&52&200\end{array}",34,GOLD),
                "Xét bốn mệnh đề về tỉ lệ, điều kiện và độc lập.",
            ],
            "Đây là bài tổng hợp theo đúng tinh thần đọc dữ liệu. Ta ký hiệu A là khách có dùng ứng dụng và S là khách hài lòng. Từ một bảng duy nhất, bốn mệnh đề sẽ kiểm tra bốn kỹ năng khác nhau.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Mệnh đề a và b: đọc đúng hàng, đúng cột", "5/5")
        statements=VGroup(
            VGroup(txt("a)",27,GOLD,BOLD),mtx(r"P(A)=0.6",36,INK)).arrange(RIGHT,buff=0.18),
            VGroup(txt("b)",27,GOLD,BOLD),mtx(r"P(S\mid A)=0.8",36,INK)).arrange(RIGHT,buff=0.18),
            VGroup(txt("c)",27,GOLD,BOLD),mtx(r"P(A\mid S)=0.8",36,INK)).arrange(RIGHT,buff=0.18),
            VGroup(txt("d)",27,GOLD,BOLD),txt("A và S độc lập.",29,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.38).shift(LEFT*2.7)
        self.play(FadeIn(statements),run_time=0.8)
        result_ab=VGroup(
            mtx(r"P(A)=\frac{120}{200}=0.6",34,GREEN),
            VGroup(txt("a) ĐÚNG",25,GREEN,BOLD)).arrange(RIGHT),
            mtx(r"P(S\mid A)=\frac{96}{120}=0.8",34,GREEN),
            VGroup(txt("b) ĐÚNG",25,GREEN,BOLD)).arrange(RIGHT),
        ).arrange(DOWN,buff=0.20).to_edge(RIGHT,buff=0.45).shift(UP*0.6)
        self.play(FadeIn(result_ab),run_time=0.7)
        self.narrate(
            "Mệnh đề a đúng vì một trăm hai mươi trên hai trăm bằng không phẩy sáu. Mệnh đề b cũng đúng: khi đã biết khách dùng ứng dụng, mẫu số chỉ còn một trăm hai mươi; trong số đó có chín mươi sáu người hài lòng, nên xác suất là không phẩy tám.",
            1.7,
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Mệnh đề c: đảo điều kiện là đổi mẫu số", "5/5")
        ccalc=VGroup(
            mtx(r"P(A\mid S)=\frac{96}{148}=\frac{24}{37}\approx0.649",38,BLUE),
            mtx(r"0.649\ne0.8",40,RED),
            txt("c) SAI",28,RED,BOLD),
        ).arrange(DOWN,buff=0.32)
        self.play(FadeIn(ccalc),run_time=0.8)
        self.narrate(
            "Mệnh đề c cố tình đảo điều kiện. Khi đã biết khách hài lòng, ta chỉ xét một trăm bốn mươi tám khách hài lòng. Trong đó có chín mươi sáu người dùng ứng dụng. Xác suất bằng hai mươi bốn phần ba mươi bảy, khoảng không phẩy sáu bốn chín, không phải không phẩy tám. Vì vậy c sai.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Bài 5", "Mệnh đề d: kiểm tra độc lập", "5/5")
        dcalc=VGroup(
            mtx(r"P(A\cap S)=\frac{96}{200}=0.48",36,CYAN),
            mtx(r"P(A)P(S)=0.6\cdot\frac{148}{200}=0.444",36,ORANGE),
            mtx(r"0.48\ne0.444",40,RED),
            txt("d) SAI – hai biến cố không độc lập",27,RED,BOLD),
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(dcalc),run_time=0.8)
        self.narrate(
            "Để kiểm tra độc lập, so sánh xác suất giao với tích hai xác suất. Xác suất vừa dùng ứng dụng vừa hài lòng là chín mươi sáu trên hai trăm, tức không phẩy bốn tám. Còn P của A nhân P của S bằng không phẩy bốn bốn bốn. Hai số khác nhau, nên A và S không độc lập. Vậy mệnh đề d sai.",
            1.9,
        )
        final=VGroup(
            txt("Kết quả:",28,GOLD,BOLD),
            txt("a) Đúng   b) Đúng   c) Sai   d) Sai",30,INK,BOLD),
        ).arrange(DOWN,buff=0.25).to_edge(DOWN,buff=0.62)
        self.play(FadeIn(final),run_time=0.5)

    # ======================================================
    # SUMMARY
    # ======================================================
    def summary(self):
        self.clear_stage(); self.add_header_footer("Bản đồ tư duy", "Xác suất – thống kê từ dữ liệu thực tế", "Tổng kết")
        steps=VGroup(
            bullet("1. Trung bình: mức điển hình; độ lệch chuẩn: mức phân tán.",INK,26,BLUE),
            bullet("2. Dữ liệu ghép nhóm: dùng giá trị đại diện và trọng số tần số.",INK,26,CYAN),
            bullet("3. P(A|B): điều kiện B quyết định mẫu số mới.",INK,26,ORANGE),
            bullet("4. Xác suất toàn phần: cộng các con đường dẫn tới cùng biến cố.",INK,26,PURPLE),
            bullet("5. Bayes: dùng thông tin đã quan sát để cập nhật xác suất nguồn gốc.",INK,26,GREEN),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34)
        fit_width(steps,11.7)
        for s in steps:self.play(FadeIn(s,shift=RIGHT*0.12),run_time=0.36)
        self.narrate(
            "Chốt lại: trung bình cho biết mức điển hình, nhưng muốn nói ổn định phải nhìn độ phân tán. Với dữ liệu ghép nhóm, giá trị đại diện phải đi kèm tần số. Trong xác suất có điều kiện, mẫu số thay đổi theo thông tin đã biết. Xác suất toàn phần đi xuôi qua các nhánh; Bayes đi ngược từ kết quả quan sát về nguyên nhân. Đây đều là kỹ năng đọc dữ liệu, không phải học thuộc ký hiệu.",
            1.9,
        )

        self.clear_stage(); self.add_header_footer("Bài tự luyện nhanh", "Một phép kiểm tra đọc điều kiện", "Tự luyện")
        q=VGroup(
            mtx(r"P(A)=0.7,\quad P(B\mid A)=0.3",38,BLUE),
            mtx(r"P(\overline A)=0.3,\quad P(B\mid\overline A)=0.1",38,ORANGE),
            txt("Tính",27,INK),
            mtx(r"P(B)",42,GOLD),
        ).arrange(DOWN,buff=0.30)
        self.play(FadeIn(q),run_time=0.7)
        self.narrate("Bài tự luyện: bảy mươi phần trăm thuộc nhóm A. Xác suất B trong A là không phẩy ba, còn trong nhóm không A là không phẩy một. Hãy tính xác suất B bằng công thức xác suất toàn phần.",1.4)
        self.wait(0.8)
        ans=VGroup(
            mtx(r"P(B)=P(A)P(B\mid A)+P(\overline A)P(B\mid\overline A)",34,INK),
            mtx(r"=0.7\cdot0.3+0.3\cdot0.1=0.24",38,CYAN),
            mtx(r"\boxed{P(B)=24\%}",42,GOLD),
        ).arrange(DOWN,buff=0.30).shift(DOWN*0.45)
        self.play(FadeIn(ans),run_time=0.8)
        self.narrate("Ta cộng hai con đường dẫn tới B: đi qua A và đi qua không A. Kết quả bằng không phẩy hai bốn, tức hai mươi bốn phần trăm.",1.3)

        self.clear_stage()
        end=VGroup(
            txt("VIDEO 07 – XÁC SUẤT & THỐNG KÊ THỰC TẾ",40,GOLD,BOLD),
            VGroup(txt("Dữ liệu",26,CYAN,BOLD), Arrow(LEFT*0.28,RIGHT*0.28,color=CYAN,stroke_width=3), txt("mô hình",26,CYAN,BOLD), Arrow(LEFT*0.28,RIGHT*0.28,color=CYAN,stroke_width=3), txt("kết luận",26,CYAN,BOLD)).arrange(RIGHT,buff=0.14),
            txt("Đọc đúng mẫu số quan trọng hơn bấm máy nhanh.",28,INK),
            txt("Tiếp theo: Tổng hợp Đúng/Sai + trả lời ngắn kiểu TN THPT",24,MUTED),
            txt(TEN_THAY,21,MUTED),
        ).arrange(DOWN,buff=0.30)
        fit_width(end,12.0)
        self.play(FadeIn(end),run_time=0.9)
        self.narrate("Video tiếp theo sẽ là bài tổng hợp của cả series: câu đúng sai và trả lời ngắn kiểu thi tốt nghiệp, kết hợp hàm số, đạo hàm, tích phân, Oxyz, xác suất và dữ liệu thực tế. Hẹn gặp các em ở video tám.",1.5)

    def construct(self):
        self.intro()
        self.ex1_delivery()
        self.ex2_grouped()
        self.ex3_conditional()
        self.ex4_bayes()
        self.ex5_true_false()
        self.summary()


# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_07_xac_suat_thong_ke_1080p"
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
    master_wav = ROOT / "master_narration_xac_suat_thong_ke.wav"
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

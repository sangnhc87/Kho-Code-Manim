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
# 03. Toc do - thoi gian - nang suat - chi phi (FILE NAY)
# 04. Doc do thi thuc te + dao ham + Dung/Sai
# 05. Tich phan: quang duong - the tich - luong tich luy
# 06. Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke tu du lieu
# 08. Tong hop Dung/Sai + tra loi ngan kieu TN THPT
#
# Nguyen tac dai han:
# - Uu tien mo hinh thuc te, ham tuong minh, do thi dong.
# - Han che toi da ham an.
# - Moi bai: de bai -> mo hinh -> diem gay -> giai tung mien -> so sanh -> ket luan.
# ==========================================================

# ==========================================================
# SYSTEM CONFIG
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
# LATEX / TEXT HELPERS
# ==========================================================
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
        self.add_header_footer(title, "BÀI TOÁN THỰC TẾ", progress)
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

    def make_axes(self, xr, yr, xlen=6.8, ylen=5.2, shift=LEFT*2.7, x_numbers=True, y_numbers=True):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2},
            x_axis_config={"include_numbers": x_numbers, "font_size": 20},
            y_axis_config={"include_numbers": y_numbers, "font_size": 20},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 27), mtx("y", 27))
        return ax, labels

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("TOÁN THỰC TẾ – HÀM SỐ, PHẦN 03", 45, GOLD, BOLD),
            txt("TỐC ĐỘ – THỜI GIAN – NĂNG SUẤT – CHI PHÍ", 34, INK, BOLD),
            mtx(r"T(x)=\frac{A}{x}+Bx", 44, CYAN),
            txt("Một cấu trúc nhỏ xuất hiện trong rất nhiều mô hình lớn.", 27, MUTED),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.30)
        fit_width(g, 12.0)
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.6)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), FadeIn(g[4]), run_time=1.2)
        self.narrate(
            "Chào các em. Video hôm nay nối tiếp series toán thực tế bằng một nhóm bài rất hay: tốc độ, thời gian, năng suất và chi phí. Nhiều bài nhìn rất khác nhau nhưng sau khi mô hình hóa lại dẫn về vài cấu trúc quen thuộc như A chia x cộng B x, hoặc A chia x cộng B chia M trừ x. Ta sẽ không học thuộc công thức. Mỗi bài đều bắt đầu từ tình huống thực, vẽ hình, xác định miền hợp lý, rồi mới dùng đạo hàm hoặc bất đẳng thức để tối ưu.",
            2.2,
        )

        self.clear_stage(); self.add_header_footer("Bản đồ tư duy", "Ba mối quan hệ xuất hiện liên tục", "Mở đầu")
        rows = VGroup(
            VGroup(mtx(r"t=\frac{s}{v}", 38, BLUE), txt("quãng đường cố định: tốc độ tăng thì thời gian giảm", 26, INK)).arrange(RIGHT,buff=0.30),
            VGroup(mtx(r"t=\frac{W}{q}", 38, CYAN), txt("khối lượng việc cố định: năng suất tăng thì thời gian giảm", 26, INK)).arrange(RIGHT,buff=0.30),
            VGroup(mtx(r"C(x)=\frac{A}{x}+Bx", 38, GOLD), txt("một phần giảm, một phần tăng → thường có điểm cân bằng", 26, INK)).arrange(RIGHT,buff=0.30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.52).shift(DOWN*0.1)
        fit_width(rows, 11.6)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT*0.14), run_time=0.42)
        self.narrate(
            "Ba quan hệ này là xương sống của video. Thời gian bằng quãng đường chia tốc độ. Thời gian làm việc bằng khối lượng công việc chia năng suất. Và khi một thành phần giảm theo x còn một thành phần khác tăng theo x, tổng của chúng thường đạt cực tiểu tại một điểm cân bằng. Nhìn được cấu trúc trước khi đạo hàm sẽ giúp lời giải ngắn hơn rất nhiều.",
            1.9,
        )

    # ======================================================
    # MODEL 1 - TRANSPORT SPEED AND COST
    # ======================================================
    def model1_transport_speed(self):
        self.show_problem(
            "Mô hình 1 – Tốc độ vận tải và tổng chi phí",
            [
                "Một xe chạy 200 km với tốc độ trung bình v km/h, 40 ≤ v ≤ 100.",
                "Chi phí thời gian được quy đổi là 0,4 triệu đồng cho mỗi giờ.",
                "Chi phí nhiên liệu – bảo dưỡng được mô hình hóa bởi v/80 triệu đồng.",
                "Tìm tốc độ làm tổng chi phí nhỏ nhất.",
            ],
            "Đây là một mô hình giả định để luyện cách cân bằng hai loại chi phí. Đi chậm thì mất nhiều thời gian. Đi quá nhanh thì nhiên liệu và hao mòn tăng. Ta cần tìm tốc độ ở giữa sao cho tổng chi phí nhỏ nhất.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 1", "Từ tình huống thực tế đến hàm mục tiêu", "1/5")
        deriv = VGroup(
            mtx(r"t(v)=\frac{200}{v}", 38, BLUE),
            mtx(r"C_{\mathrm{time}}(v)=0.4\cdot\frac{200}{v}=\frac{80}{v}", 38, CYAN),
            mtx(r"C_{\mathrm{run}}(v)=\frac{v}{80}", 38, ORANGE),
            mtx(r"\boxed{C(v)=\frac{80}{v}+\frac{v}{80}},\qquad 40\le v\le100", 42, GOLD),
        ).arrange(DOWN,buff=0.34)
        fit_width(deriv,11.4)
        for m in deriv:self.play(FadeIn(m,shift=UP*0.05),run_time=0.40)
        self.narrate(
            "Thời gian đi hết hai trăm ki lô mét là hai trăm chia v giờ. Mỗi giờ được quy đổi thành không phẩy bốn triệu đồng nên chi phí thời gian là tám mươi chia v. Chi phí vận hành được mô hình hóa là v chia tám mươi. Vì vậy hàm cần tối thiểu hóa là tám mươi chia v cộng v chia tám mươi, trên miền tốc độ từ bốn mươi đến một trăm.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 1", "Điểm vàng chạy trên đồ thị chi phí", "1/5")
        ax,labels=self.make_axes((40,101,10),(1.8,2.65,0.2),xlen=7.0,ylen=4.9,shift=LEFT*2.7)
        curve=ax.plot(lambda v:80/v+v/80,x_range=[40,100],color=BLUE,stroke_width=5)
        v=ValueTracker(42)
        point=always_redraw(lambda:Dot(ax.c2p(v.get_value(),80/v.get_value()+v.get_value()/80),radius=0.08,color=GOLD))
        drop=always_redraw(lambda:DashedLine(ax.c2p(v.get_value(),1.8),point.get_center(),color=MUTED,dash_length=0.10))
        card=VGroup(
            mtx(r"C'(v)=-\frac{80}{v^2}+\frac1{80}",34,INK),
            mtx(r"C'(v)=0\iff v^2=6400",34,CYAN),
            mtx(r"\boxed{v=80}",42,GOLD),
            mtx(r"C_{\min}=1+1=2",36,GREEN),
        ).arrange(DOWN,buff=0.27).to_edge(RIGHT,buff=0.35)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(point),Create(drop),FadeIn(card),run_time=1.1)
        self.narrate_play(
            "Cho tốc độ tăng dần. Ban đầu, phần chi phí thời gian giảm rất nhanh nên tổng chi phí đi xuống. Sau một điểm, chi phí vận hành tăng mạnh hơn phần tiết kiệm thời gian, nên tổng chi phí quay đầu tăng. Điểm thấp nhất xuất hiện tại v bằng tám mươi ki lô mét trên giờ.",
            v.animate.set_value(100),min_time=5.0,
        )
        self.narrate_play(
            "Kéo điểm trở lại vị trí tối ưu. Đạo hàm bằng không cho v bình phương bằng sáu nghìn bốn trăm, nên v bằng tám mươi. Khi đó hai thành phần đều bằng một triệu đồng và tổng nhỏ nhất bằng hai triệu đồng.",
            v.animate.set_value(80),min_time=4.0,
        )
        bonus=VGroup(txt("Lời giải 1 dòng bằng AM-GM:",24,MUTED),mtx(r"\frac{80}{v}+\frac{v}{80}\ge2",36,GOLD)).arrange(DOWN,buff=0.15).to_edge(DOWN,buff=0.62).shift(RIGHT*2.2)
        self.play(FadeIn(bonus),run_time=0.5)
        self.narrate(
            "Còn một lời giải rất đẹp: hai số tám mươi chia v và v chia tám mươi đều dương và có tích bằng một. Theo AM-GM, tổng của chúng ít nhất bằng hai, dấu bằng đúng khi hai số bằng nhau, tức v bằng tám mươi.",
            1.6,
        )

    # ======================================================
    # MODEL 2 - MACHINE RATE AND COMPLETION TIME
    # ======================================================
    def model2_machine_rate(self):
        self.show_problem(
            "Mô hình 2 – Máy chạy nhanh chưa chắc hoàn thành sớm nhất",
            [
                "Một máy phải xử lý 360 đơn vị công việc trong ngày.",
                "Nếu đặt năng suất q đơn vị/giờ thì thời gian xử lý là 360/q giờ.",
                "Chạy nhanh làm tăng thời gian hiệu chỉnh – kiểm tra, mô hình bởi q/40 giờ.",
                "Với 60 ≤ q ≤ 180, tìm q làm tổng thời gian nhỏ nhất.",
            ],
            "Nhiều học sinh có phản xạ rằng máy càng nhanh càng tốt. Nhưng trong thực tế, đẩy tốc độ quá cao có thể làm tăng thời gian kiểm tra, hiệu chỉnh hoặc sửa lỗi. Vì vậy tổng thời gian có thể giảm rồi tăng trở lại.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 2", "Hai phần thời gian kéo ngược nhau", "2/5")
        deriv=VGroup(
            mtx(r"T(q)=\frac{360}{q}+\frac{q}{40}",42,GOLD),
            mtx(r"T'(q)=-\frac{360}{q^2}+\frac1{40}",36,INK),
            mtx(r"T'(q)=0\iff q^2=14400",36,CYAN),
            mtx(r"\boxed{q=120}",42,GOLD),
            mtx(r"T_{\min}=\frac{360}{120}+\frac{120}{40}=6",38,GREEN),
        ).arrange(DOWN,buff=0.29)
        fit_width(deriv,11.3)
        for m in deriv:self.play(FadeIn(m,shift=RIGHT*0.06),run_time=0.38)
        self.narrate(
            "Hàm thời gian có đúng cấu trúc quen thuộc: ba trăm sáu mươi chia q giảm khi q tăng, còn q chia bốn mươi tăng khi q tăng. Đạo hàm bằng không cho q bình phương bằng mười bốn nghìn bốn trăm, nên q bằng một trăm hai mươi. Tổng thời gian nhỏ nhất là sáu giờ.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 2", "Nhìn thấy điểm cân bằng trên đồ thị", "2/5")
        ax,labels=self.make_axes((60,181,20),(5.5,8.1,0.5),xlen=7.0,ylen=4.9,shift=LEFT*2.7)
        curve=ax.plot(lambda q:360/q+q/40,x_range=[60,180],color=CYAN,stroke_width=5)
        q=ValueTracker(60)
        P=always_redraw(lambda:Dot(ax.c2p(q.get_value(),360/q.get_value()+q.get_value()/40),radius=0.08,color=GOLD))
        h=always_redraw(lambda:DashedLine(ax.c2p(q.get_value(),5.5),P.get_center(),color=MUTED,dash_length=0.10))
        card=VGroup(
            VGroup(txt("Xử lý",24,BLUE),mtx(r"\frac{360}{q}",32,BLUE)).arrange(RIGHT,buff=0.15),
            VGroup(txt("Hiệu chỉnh",24,ORANGE),mtx(r"\frac q{40}",32,ORANGE)).arrange(RIGHT,buff=0.15),
            mtx(r"\boxed{q=120}",40,GOLD),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.45)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(P),Create(h),FadeIn(card),run_time=1.0)
        self.narrate_play(
            "Điểm vàng mô tả tổng thời gian khi ta tăng năng suất máy. Từ sáu mươi lên một trăm hai mươi, thời gian xử lý giảm đủ mạnh để kéo tổng đi xuống. Vượt quá một trăm hai mươi, lợi ích giảm dần trong khi thời gian hiệu chỉnh tiếp tục tăng, nên tổng thời gian tăng trở lại.",
            q.animate.set_value(180),min_time=5.0,
        )
        self.narrate_play(
            "Điểm tối ưu một trăm hai mươi còn có một ý nghĩa đẹp: lúc đó thời gian xử lý bằng ba giờ và thời gian hiệu chỉnh cũng bằng ba giờ. Hai cơ chế đối nghịch đã cân bằng đúng tại cực tiểu.",
            q.animate.set_value(120),min_time=4.0,
        )

    # ======================================================
    # MODEL 3 - STAFF ALLOCATION
    # ======================================================
    def model3_staff_allocation(self):
        self.show_problem(
            "Mô hình 3 – Chia 20 nhân viên cho hai công đoạn",
            [
                "Một dự án có hai công đoạn làm tuần tự.",
                "Công đoạn A cần 144 giờ-công; công đoạn B cần 64 giờ-công.",
                "Chia x người cho A và 20 − x người cho B, năng suất mỗi người như nhau.",
                "Tìm cách chia để tổng thời gian hoàn thành nhỏ nhất.",
            ],
            "Bài này rất thực tế: ta có một nguồn lực cố định là hai mươi người nhưng hai công đoạn có khối lượng khác nhau. Chia đều mười và mười nghe có vẻ hợp lý, nhưng chưa chắc tối ưu vì công đoạn A nặng hơn công đoạn B.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 3", "Từ phân bổ nhân lực đến hàm thời gian", "3/5")
        deriv=VGroup(
            mtx(r"T_A(x)=\frac{144}{x}",37,BLUE),
            mtx(r"T_B(x)=\frac{64}{20-x}",37,CYAN),
            mtx(r"T(x)=\frac{144}{x}+\frac{64}{20-x},\qquad 0<x<20",41,GOLD),
            mtx(r"T'(x)=-\frac{144}{x^2}+\frac{64}{(20-x)^2}",35,INK),
            mtx(r"\frac{12}{x}=\frac{8}{20-x}\iff \boxed{x=12}",38,GREEN),
            mtx(r"T_{\min}=\frac{144}{12}+\frac{64}{8}=20",37,GOLD),
        ).arrange(DOWN,buff=0.25)
        fit_width(deriv,11.4)
        for m in deriv:self.play(FadeIn(m,shift=UP*0.04),run_time=0.36)
        self.narrate(
            "Nếu x người làm công đoạn A thì thời gian A là một trăm bốn mươi bốn chia x. Công đoạn B còn hai mươi trừ x người nên thời gian B là sáu mươi bốn chia hai mươi trừ x. Hai công đoạn làm tuần tự nên ta cộng hai thời gian. Giải phương trình đạo hàm bằng không cho x bằng mười hai. Vậy chia mười hai người cho A và tám người cho B, tổng thời gian nhỏ nhất là hai mươi giờ.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 3", "Hình động: nhân lực dịch từ B sang A", "3/5")
        x=ValueTracker(5)
        frame=RoundedRectangle(width=9.4,height=1.35,corner_radius=0.14,stroke_color=MUTED,stroke_width=2).shift(UP*1.1)
        left_bar=always_redraw(lambda:Rectangle(width=max(0.05,9.0*x.get_value()/20),height=0.75,fill_color=BLUE,fill_opacity=0.75,stroke_width=0).align_to(frame,LEFT).shift(RIGHT*0.2))
        right_bar=always_redraw(lambda:Rectangle(width=max(0.05,9.0*(20-x.get_value())/20),height=0.75,fill_color=CYAN,fill_opacity=0.75,stroke_width=0).align_to(frame,RIGHT).shift(LEFT*0.2))
        labA=always_redraw(lambda:VGroup(txt("A",24,INK,BOLD),mtx(fr"x={x.get_value():.1f}",28,INK)).arrange(RIGHT,buff=0.12).move_to(frame.get_center()+LEFT*2.4))
        labB=always_redraw(lambda:VGroup(txt("B",24,INK,BOLD),mtx(fr"20-x={20-x.get_value():.1f}",28,INK)).arrange(RIGHT,buff=0.12).move_to(frame.get_center()+RIGHT*2.4))
        ax,labels=self.make_axes((2,19,2),(18,80,10),xlen=7.0,ylen=3.7,shift=DOWN*1.4+LEFT*1.2)
        curve=ax.plot(lambda z:144/z+64/(20-z),x_range=[2,18],color=ORANGE,stroke_width=4)
        P=always_redraw(lambda:Dot(ax.c2p(x.get_value(),144/x.get_value()+64/(20-x.get_value())),radius=0.07,color=GOLD))
        self.play(Create(frame),FadeIn(left_bar),FadeIn(right_bar),FadeIn(labA),FadeIn(labB),Create(ax),FadeIn(labels),Create(curve),FadeIn(P),run_time=1.1)
        self.narrate_play(
            "Ta thử chuyển dần nhân lực từ B sang A. Khi A có quá ít người, công đoạn A trở thành nút thắt và tổng thời gian rất lớn. Khi chuyển quá nhiều người sang A, B lại thiếu người và thời gian tăng. Điểm vàng trên đồ thị thấp nhất đúng khi x bằng mười hai.",
            x.animate.set_value(17),min_time=5.0,
        )
        self.narrate_play(
            "Vì số nhân viên phải là số nguyên, sau khi tối ưu liên tục ta cần kiểm tra tính khả thi rời rạc. May mắn ở đây nghiệm liên tục đã là số nguyên mười hai, nên không cần làm tròn hay so sánh thêm.",
            x.animate.set_value(12),min_time=4.0,
        )

    # ======================================================
    # MODEL 4 - AVERAGE UNIT COST
    # ======================================================
    def model4_average_cost(self):
        self.show_problem(
            "Mô hình 4 – Sản xuất nhiều chưa chắc rẻ nhất",
            [
                "Một xưởng sản xuất q sản phẩm mỗi ngày, 100 ≤ q ≤ 500.",
                "Chi phí bình quân mỗi sản phẩm được mô hình hóa bởi:",
                mtx(r"A(q)=18+\frac{3600}{q}+0.04q", 42, GOLD),
                "Tìm sản lượng làm chi phí bình quân nhỏ nhất.",
            ],
            "Ba thành phần có ý nghĩa khác nhau. Mười tám là chi phí cơ bản. Ba nghìn sáu trăm chia q là chi phí cố định được phân bổ cho mỗi sản phẩm nên giảm khi sản lượng tăng. Còn không phẩy không bốn q mô tả áp lực tăng ca, hao mòn hoặc kiểm soát chất lượng tăng khi sản xuất quá nhiều.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 4", "Đạo hàm ngắn – ý nghĩa kinh tế rõ", "4/5")
        deriv=VGroup(
            mtx(r"A'(q)=-\frac{3600}{q^2}+0.04",37,INK),
            mtx(r"A'(q)=0\iff q^2=90000",37,CYAN),
            mtx(r"\boxed{q=300}",43,GOLD),
            mtx(r"A(300)=18+12+12=\boxed{42}",39,GREEN),
        ).arrange(DOWN,buff=0.34).shift(UP*0.1)
        self.play(FadeIn(deriv),run_time=0.8)
        self.narrate(
            "Đạo hàm rất ngắn. Âm ba nghìn sáu trăm chia q bình phương cộng không phẩy không bốn bằng không cho q bằng ba trăm. Khi đó chi phí cố định phân bổ là mười hai và phần tăng do vận hành cao cũng là mười hai. Cộng với mười tám, chi phí bình quân nhỏ nhất bằng bốn mươi hai đơn vị.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 4", "Hai thành phần biến đổi ngược chiều", "4/5")
        ax,labels=self.make_axes((100,501,100),(40,61,5),xlen=7.0,ylen=4.8,shift=LEFT*2.7)
        curve=ax.plot(lambda q:18+3600/q+0.04*q,x_range=[100,500],color=BLUE,stroke_width=5)
        q=ValueTracker(100)
        P=always_redraw(lambda:Dot(ax.c2p(q.get_value(),18+3600/q.get_value()+0.04*q.get_value()),radius=0.08,color=GOLD))
        h=always_redraw(lambda:DashedLine(ax.c2p(q.get_value(),40),P.get_center(),color=MUTED,dash_length=0.10))
        card=VGroup(
            VGroup(mtx(r"\frac{3600}{q}",31,BLUE),txt("giảm",23,BLUE)).arrange(RIGHT,buff=0.12),
            VGroup(mtx(r"0.04q",31,ORANGE),txt("tăng",23,ORANGE)).arrange(RIGHT,buff=0.12),
            mtx(r"q=300",39,GOLD),
            mtx(r"A_{\min}=42",37,GREEN),
        ).arrange(DOWN,buff=0.26).to_edge(RIGHT,buff=0.5)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(P),Create(h),FadeIn(card),run_time=1.0)
        self.narrate_play(
            "Khi sản lượng còn thấp, tăng q giúp chia nhỏ chi phí cố định nên chi phí bình quân giảm mạnh. Nhưng sau một mức, phần tăng do tăng ca và vận hành áp lực cao bắt đầu lấn át. Vì vậy đồ thị tạo một đáy tại ba trăm sản phẩm mỗi ngày.",
            q.animate.set_value(500),min_time=5.0,
        )
        self.narrate_play(
            "Ở vị trí tối ưu, hai phần biến thiên lại bằng nhau: ba nghìn sáu trăm chia ba trăm bằng mười hai, còn không phẩy không bốn nhân ba trăm cũng bằng mười hai. Đây chính là dấu hiệu cân bằng của dạng A chia x cộng B x.",
            q.animate.set_value(300),min_time=4.0,
        )

    # ======================================================
    # MODEL 5 - LIFEGUARD PATH
    # ======================================================
    def model5_lifeguard(self):
        self.show_problem(
            "Mô hình 5 – Cứu hộ: chạy bao xa rồi mới bơi?",
            [
                "Trên bờ biển, A cách O một đoạn 120 m. Người gặp nạn S cách bờ tại O một đoạn 60 m.",
                "Nhân viên cứu hộ chạy với tốc độ 6 m/s và bơi với tốc độ 2 m/s.",
                "Chọn điểm M trên AO để chạy từ A đến M, rồi bơi thẳng từ M đến S.",
                "Tìm vị trí M làm tổng thời gian nhỏ nhất.",
            ],
            "Đây là một bài rất đẹp vì kết hợp hình học với đạo hàm. Nếu bơi ngay từ A thì quãng bơi quá dài. Nếu chạy hết đến O rồi mới bơi thì chạy nhiều hơn nhưng bơi ngắn nhất. Điểm tối ưu nằm ở giữa và ta sẽ nhìn thấy nó chuyển động trên hình.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 5", "Hình động của đường chạy – đường bơi", "5/5")
        # Geometry in scene coordinates, scaled so AO=6 units and OS=3 units.
        A=LEFT*4.7+DOWN*1.2
        O=RIGHT*1.3+DOWN*1.2
        S=RIGHT*1.3+UP*2.0
        shore=Line(LEFT*5.3+DOWN*1.2,RIGHT*2.2+DOWN*1.2,color=MUTED,stroke_width=4)
        sea=Rectangle(width=7.5,height=3.4,fill_color=BLUE,fill_opacity=0.08,stroke_width=0).move_to(LEFT*1.55+UP*0.5)
        x=ValueTracker(0)
        # x is OM in metres, mapped linearly: 120 m -> 6 scene units.
        M=always_redraw(lambda:Dot(O+LEFT*(x.get_value()/20),radius=0.085,color=GOLD))
        run_seg=always_redraw(lambda:Line(A,M.get_center(),color=ORANGE,stroke_width=6))
        swim_seg=always_redraw(lambda:Line(M.get_center(),S,color=CYAN,stroke_width=6))
        mlab=always_redraw(lambda:mtx(r"M",27,GOLD).next_to(M,DOWN,buff=0.10))
        labels=VGroup(mtx(r"A",28,INK).next_to(A,DOWN,buff=0.12),mtx(r"O",28,INK).next_to(O,DOWN,buff=0.12),mtx(r"S",28,INK).next_to(S,RIGHT,buff=0.12))
        dims=VGroup(mtx(r"AO=120",30,INK).next_to(shore,DOWN,buff=0.35),mtx(r"OS=60",30,INK).next_to(Line(O,S),RIGHT,buff=0.22))
        formula=VGroup(
            mtx(r"OM=x,\qquad AM=120-x",33,GOLD),
            mtx(r"MS=\sqrt{x^2+60^2}",33,CYAN),
            mtx(r"T(x)=\frac{120-x}{6}+\frac{\sqrt{x^2+3600}}{2}",34,INK),
        ).arrange(DOWN,buff=0.24).to_edge(RIGHT,buff=0.20).shift(DOWN*0.8)
        fit_width(formula,6.0)
        self.play(FadeIn(sea),Create(shore),FadeIn(labels),FadeIn(dims),FadeIn(M),Create(run_seg),Create(swim_seg),FadeIn(mlab),FadeIn(formula),run_time=1.2)
        self.narrate_play(
            "Điểm vàng M có thể trượt trên đoạn A O. Gọi O M bằng x mét. Khi x bằng không, ta chạy hết một trăm hai mươi mét đến O rồi mới bơi. Khi x tăng, đoạn chạy ngắn lại nhưng đoạn bơi dài hơn. Hai thay đổi này kéo thời gian theo hai hướng ngược nhau.",
            x.animate.set_value(90),min_time=5.0,
        )
        self.narrate_play(
            "Ta đưa M trở về gần vị trí tối ưu để chuẩn bị tính toán. Quãng chạy là một trăm hai mươi trừ x, còn quãng bơi là căn x bình phương cộng ba nghìn sáu trăm. Chia cho hai tốc độ tương ứng, ta có hàm thời gian tường minh theo một biến x.",
            x.animate.set_value(15*math.sqrt(2)),min_time=4.0,
        )

        self.clear_stage(); self.add_header_footer("Mô hình 5", "Lời giải gọn và một hệ thức hình học đẹp", "5/5")
        solve=VGroup(
            mtx(r"T'(x)=-\frac16+\frac{x}{2\sqrt{x^2+3600}}",36,INK),
            mtx(r"T'(x)=0\iff \frac{x}{\sqrt{x^2+3600}}=\frac13",36,CYAN),
            mtx(r"9x^2=x^2+3600",35,INK),
            mtx(r"x^2=450\iff \boxed{x=15\sqrt2\approx21.21}",39,GOLD),
            mtx(r"T_{\min}\approx48.28\ \mathrm{s}",38,GREEN),
        ).arrange(DOWN,buff=0.28)
        fit_width(solve,11.4)
        for m in solve:self.play(FadeIn(m,shift=UP*0.05),run_time=0.38)
        self.narrate(
            "Đạo hàm của thời gian bằng âm một phần sáu cộng x chia hai căn x bình phương cộng ba nghìn sáu trăm. Cho đạo hàm bằng không, ta được x chia độ dài M S bằng một phần ba. Bình phương và giải ra x bằng mười lăm căn hai, xấp xỉ hai mươi mốt phẩy hai một mét. Tổng thời gian nhỏ nhất xấp xỉ bốn mươi tám phẩy hai tám giây.",
            2.0,
        )

        gem=VGroup(
            txt("Tính chất đẹp ẩn trong lời giải:",27,GOLD,BOLD),
            mtx(r"\sin\theta=\frac{OM}{MS}=\frac13",38,CYAN),
            mtx(r"\boxed{\sin\theta=\frac{v_{\mathrm{swim}}}{v_{\mathrm{run}}}=\frac{2}{6}}",38,GOLD),
        ).arrange(DOWN,buff=0.28).shift(DOWN*0.1)
        self.play(FadeIn(gem),run_time=0.7)
        self.narrate(
            "Còn một tính chất rất đẹp. Nếu theta là góc giữa đường bơi và phương vuông góc với bờ, thì sin theta bằng O M chia M S. Điều kiện cực trị vừa tìm cho đúng sin theta bằng một phần ba, cũng chính là tỉ số tốc độ bơi chia tốc độ chạy. Một bài tối ưu phổ thông đã hé lộ một quy luật hình học rất gọn.",
            1.9,
        )

    # ======================================================
    # GENERAL PATTERNS + CHALLENGE + ROADMAP
    # ======================================================
    def summary(self):
        self.clear_stage(); self.add_header_footer("Hai mẫu tổng quát rất đáng nhớ", "Nhìn cấu trúc để rút ngắn lời giải", "Tổng kết")
        g=VGroup(
            mtx(r"F(x)=\frac{A}{x}+Bx,\quad A,B>0",40,GOLD),
            mtx(r"x_{\min}=\sqrt{\frac AB},\qquad F_{\min}=2\sqrt{AB}",40,GREEN),
            Line(LEFT*5.2,RIGHT*5.2,color=MUTED,stroke_opacity=0.25),
            mtx(r"G(x)=\frac{A}{x}+\frac{B}{M-x},\quad 0<x<M",38,CYAN),
            mtx(r"x_{\min}=\frac{M\sqrt A}{\sqrt A+\sqrt B}",40,GOLD),
        ).arrange(DOWN,buff=0.34)
        fit_width(g,11.4)
        self.play(LaggedStart(*[FadeIn(m,shift=UP*0.05) for m in g],lag_ratio=0.10),run_time=1.3)
        self.narrate(
            "Sau năm bài, ta rút ra hai mẫu rất hữu ích. Với A chia x cộng B x, cực tiểu đạt tại căn A chia B và giá trị nhỏ nhất là hai căn A B. Với A chia x cộng B chia M trừ x, nghiệm tối ưu là M căn A chia tổng căn A cộng căn B. Nhưng đừng học thuộc máy móc. Hãy nhớ nguồn gốc: một phần giảm khi x tăng, phần kia tăng, và cực tiểu xuất hiện tại điểm cân bằng của hai xu hướng.",
            2.1,
        )

        self.clear_stage(); self.add_header_footer("Bài thử thách 30 giây", "Tự dừng video trước khi xem đáp án", "Tổng kết")
        q=VGroup(
            txt("Một máy cần hoàn thành 600 đơn vị công việc.",27,INK),
            txt("Nếu chạy với năng suất q thì:",27,INK),
            mtx(r"T(q)=\frac{600}{q}+\frac{q}{24},\qquad 60\le q\le180",41,GOLD),
            txt("Tìm q làm thời gian nhỏ nhất.",28,INK,BOLD),
        ).arrange(DOWN,buff=0.30)
        fit_width(q,11.2)
        self.play(FadeIn(q),run_time=0.8)
        self.narrate(
            "Bài thử thách: sáu trăm chia q là thời gian xử lý, còn q chia hai mươi bốn là thời gian hiệu chỉnh. Hãy dừng video và thử dùng cả đạo hàm lẫn mẫu A chia x cộng B x để tìm q tối ưu.",
            1.5,
        )
        self.wait(1.0)
        sol=VGroup(
            mtx(r"T'(q)=-\frac{600}{q^2}+\frac1{24}",35,INK),
            mtx(r"q^2=14400",35,CYAN),
            mtx(r"\boxed{q=120}",42,GOLD),
            mtx(r"T_{\min}=\frac{600}{120}+\frac{120}{24}=10",37,GREEN),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.55)
        self.play(FadeIn(sol),run_time=0.8)
        self.narrate(
            "Đáp án là q bằng một trăm hai mươi. Khi đó hai thành phần đều bằng năm giờ và tổng bằng mười giờ. Một lần nữa, cực tiểu xuất hiện đúng lúc hai phần đối nghịch cân bằng nhau.",
            1.5,
        )

        self.clear_stage(); self.add_header_footer("Kế hoạch series", "Video 04: đọc đồ thị thực tế + câu Đúng/Sai", "Tổng kết")
        roadmap=VGroup(
            VGroup(mtx(r"01",30,MUTED),txt("Mô hình hóa + tối ưu một biến",25,MUTED)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"02",30,MUTED),txt("Hàm nhiều công thức: ngưỡng – phí – sức chứa",25,MUTED)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"03",30,GOLD),txt("Tốc độ – thời gian – năng suất – chi phí",25,GOLD,BOLD)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"04",30,CYAN),txt("Đọc đồ thị thực tế + Đúng/Sai",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"05",30,BLUE),txt("Tích phân: quãng đường – thể tích – lượng tích lũy",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"06\to08",30,ORANGE),txt("Oxyz – xác suất thống kê – tổng hợp thi",25,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.30)
        fit_width(roadmap,11.6)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.1) for r in roadmap],lag_ratio=0.10),run_time=1.4)
        self.narrate(
            "Video tiếp theo sẽ chuyển từ việc tự lập hàm sang kỹ năng đọc một đồ thị thực tế có sẵn. Ta sẽ luyện các mệnh đề đúng sai về tốc độ thay đổi, cực trị, ngưỡng an toàn, tổng lượng và cách phát hiện một kết luận nghe hợp lý nhưng sai. Đây là kiểu đọc hiểu rất phù hợp với định hướng đánh giá năng lực.",
            1.9,
        )

        self.clear_stage()
        end=VGroup(
            txt("MÔ HÌNH TRƯỚC – ĐẠO HÀM SAU",40,GOLD,BOLD),
            mtx(r"\boxed{D\ \longrightarrow\ F(x)\ \longrightarrow\ F'(x)\ \longrightarrow\ x_\ast}",35,CYAN),
            txt(TEN_THAY,22,MUTED),
        ).arrange(DOWN,buff=0.42)
        fit_width(end,11.8)
        self.play(FadeIn(end[0]),Write(end[1]),FadeIn(end[2]),run_time=1.0)
        self.narrate(
            "Chốt lại: trong toán thực tế, đạo hàm chỉ là công cụ ở giữa lời giải. Điều quyết định là mô hình đúng, miền đúng và kết luận đúng đơn vị. Khi làm tốt ba điều đó, rất nhiều bài tối ưu nhìn dài sẽ trở nên ngắn và sáng.",
            1.6,
        )

    def construct(self):
        self.intro()
        self.model1_transport_speed()
        self.model2_machine_rate()
        self.model3_staff_allocation()
        self.model4_average_cost()
        self.model5_lifeguard()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_03_toc_do_thoi_gian_nang_suat_1080p"
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
    master_wav = ROOT / "master_narration_toan_thuc_te_ham_so_03.wav"
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

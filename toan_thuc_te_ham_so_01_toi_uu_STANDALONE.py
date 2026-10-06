from manim import *
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys
import time

# ==========================================================
# SERIES ROADMAP - CT GDPT 2018 / THPT
# 01. Ham so thuc te: mo hinh hoa + toi uu mot bien (FILE NAY)
# 02. Ham nhieu cong thuc: gia, phi, nguong, suc chua
# 03. Toc do - thoi gian - chi phi - nang suat
# 04. Doc do thi thuc te + dao ham + dung/sai
# 05. Tich phan: tong luong, quang duong, the tich, chi phi tich luy
# 06. Hinh hoc toa do Oxyz trong bai toan thuc te
# 07. Xac suat - thong ke trong du lieu thuc te
# 08. Video tong hop dung/sai + tra loi ngan theo phong cach thi TN THPT
#
# Nguyen tac: uu tien ham TUONG MINH; han che toi da ham an.
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

    def make_axes(self, xr, yr, xlen=6.8, ylen=5.2, shift=LEFT*2.7):
        ax = Axes(
            x_range=list(xr), y_range=list(yr),
            x_length=xlen, y_length=ylen,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_numbers": True, "font_size": 20},
        ).shift(shift)
        labels = ax.get_axis_labels(mtx("x", 26), mtx("y", 26))
        return ax, labels

    # ======================================================
    # INTRO
    # ======================================================
    def intro(self):
        self.clear_stage()
        g = VGroup(
            txt("TOÁN THỰC TẾ VỚI HÀM SỐ – PHẦN 1", 45, GOLD, BOLD),
            txt("Mô hình hóa đúng trước – đạo hàm sau", 30, CYAN),
            VGroup(txt("Dữ liệu", 27, INK), Arrow(LEFT*0.30, RIGHT*0.30, color=CYAN, stroke_width=3), mtx(r"f(x)", 34, GOLD), Arrow(LEFT*0.30, RIGHT*0.30, color=CYAN, stroke_width=3), mtx(r"f'(x)", 34, GREEN), Arrow(LEFT*0.30, RIGHT*0.30, color=CYAN, stroke_width=3), txt("quyết định", 27, INK)).arrange(RIGHT, buff=0.14),
            txt(TEN_THAY, 22, MUTED),
        ).arrange(DOWN, buff=0.34)
        # The formula above intentionally uses only ASCII inside \text{}.
        self.play(FadeIn(g[0], shift=UP*0.18), run_time=0.7)
        self.play(FadeIn(g[1]), Write(g[2]), FadeIn(g[3]), run_time=1.0)
        self.narrate(
            "Chào các em. Từ video này, chúng ta chuyển mạnh sang các bài toán thực tế đúng tinh thần chương trình mới. Điều khó nhất không phải đạo hàm, mà là đọc dữ kiện, chọn biến, lập được hàm số đúng, xác định miền hợp lý, rồi mới tối ưu. Thầy sẽ ưu tiên các mô hình tường minh, gần với đời sống, và hạn chế tối đa những bài hàm ẩn nặng tính kỹ thuật.",
            2.0,
        )

        self.clear_stage(); self.add_header_footer("Một nguyên tắc rất quan trọng", "Đừng đạo hàm trước khi mô hình đúng", "Mở đầu")
        steps = VGroup(
            bullet("1. Chọn biến và đơn vị.", INK, 28, BLUE),
            bullet("2. Viết đại lượng cần tối ưu theo đúng biến đó.", INK, 28, CYAN),
            bullet("3. Chốt miền thực tế của biến.", INK, 28, ORANGE),
            bullet("4. Đạo hàm, xét biên, so sánh và kết luận bằng đơn vị thực tế.", INK, 28, GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        for s in steps:
            self.play(FadeIn(s, shift=RIGHT*0.12), run_time=0.35)
        self.narrate(
            "Một bài thực tế đúng nghĩa luôn có bốn lớp. Chọn biến. Lập hàm. Xác định miền. Sau đó mới dùng đạo hàm hoặc một tính chất đặc biệt để tìm giá trị tối ưu. Nếu bỏ miền hoặc quên đơn vị, lời giải toán có thể đúng nhưng kết luận thực tế vẫn sai.",
            1.8,
        )

    # ======================================================
    # MODEL 1: PROFIT QUADRATIC
    # ======================================================
    def model1_profit(self):
        self.show_problem(
            "Mô hình 1 – Sản lượng tối ưu",
            [
                "Một cơ sở bán x sản phẩm mỗi ngày.",
                mtx(r"p(x)=120-2x", 38, GOLD),
                mtx(r"C(x)=20x+200", 38, CYAN),
                "Đơn vị tiền: nghìn đồng. Tìm sản lượng làm lợi nhuận lớn nhất.",
            ],
            "Giá bán mỗi sản phẩm giảm khi sản lượng tăng: p của x bằng một trăm hai mươi trừ hai x, đơn vị nghìn đồng. Chi phí một ngày là hai mươi x cộng hai trăm. Ta cần tìm sản lượng x làm lợi nhuận lớn nhất.",
            "1/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 1", "Doanh thu → lợi nhuận → đỉnh parabol", "1/5")
        deriv = VGroup(
            mtx(r"R(x)=x\,p(x)=120x-2x^2", 36, BLUE),
            mtx(r"P(x)=R(x)-C(x)", 36, INK),
            mtx(r"P(x)=-2x^2+100x-200", 40, GOLD),
            mtx(r"P'(x)=-4x+100", 36, CYAN),
            mtx(r"P'(x)=0\iff x=25", 40, GREEN),
            mtx(r"\boxed{P_{\max}=1050}", 41, GOLD),
        ).arrange(DOWN, buff=0.24).to_edge(RIGHT, buff=0.42).shift(UP*0.05)

        ax, labels = self.make_axes((0,52,10), (-300,1200,300), xlen=6.5, ylen=5.0, shift=LEFT*3.0)
        curve = ax.plot(lambda x: -2*x*x+100*x-200, x_range=[0,50], color=BLUE, stroke_width=4)
        x = ValueTracker(5)
        M = always_redraw(lambda: Dot(ax.c2p(x.get_value(), -2*x.get_value()**2+100*x.get_value()-200), radius=0.075, color=GOLD))
        guide = always_redraw(lambda: DashedLine(ax.c2p(x.get_value(),0), M.get_center(), color=GOLD, dash_length=0.1))
        vmax = Dot(ax.c2p(25,1050), radius=0.09, color=RED)
        vlab = mtx(r"(25,1050)", 26, RED).next_to(vmax, UP, buff=0.08)
        self.play(Create(ax), FadeIn(labels), Create(curve), FadeIn(deriv), FadeIn(M), FadeIn(guide), FadeIn(vmax), FadeIn(vlab), run_time=1.1)
        self.narrate_play(
            "Cho sản lượng tăng dần. Điểm vàng biểu diễn lợi nhuận. Ban đầu lợi nhuận tăng, nhưng sau một mức nào đó, việc giảm giá bán làm lợi nhuận quay đầu. Đỉnh của parabol chính là quyết định tốt nhất.",
            x.animate.set_value(45), min_time=4.5,
        )
        self.narrate_play(
            "Từ p của x, ta có doanh thu bằng x nhân giá bán. Trừ chi phí, lợi nhuận là âm hai x bình phương cộng một trăm x trừ hai trăm. Đạo hàm bằng không tại x bằng hai mươi lăm. Khi đó lợi nhuận lớn nhất bằng một triệu không trăm năm mươi nghìn đồng.",
            x.animate.set_value(25), min_time=4.5,
        )
        note = VGroup(txt("Kết luận thực tế:", 25, MUTED), mtx(r"x=25", 34, GOLD), txt("sản phẩm/ngày", 25, INK)).arrange(RIGHT,buff=0.16).to_edge(DOWN,buff=0.62).shift(RIGHT*2.0)
        self.play(FadeIn(note), run_time=0.5)

    # ======================================================
    # MODEL 2: AVERAGE COST - NICE EQUALITY
    # ======================================================
    def model2_average_cost(self):
        self.show_problem(
            "Mô hình 2 – Chi phí trung bình thấp nhất",
            [
                mtx(r"C(x)=500+20x+0.05x^2,\qquad x>0", 38, GOLD),
                "C(x) là tổng chi phí, đơn vị nghìn đồng.",
                "Tìm mức sản xuất làm chi phí trung bình trên một sản phẩm nhỏ nhất.",
            ],
            "Bài thứ hai rất hay vì nếu chỉ nhìn tổng chi phí thì càng sản xuất càng tốn. Nhưng doanh nghiệp thường quan tâm chi phí trung bình trên một sản phẩm. Từ tổng chi phí, ta phải tự lập hàm trung bình rồi mới tối ưu.",
            "2/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 2", "Một cực tiểu có hai cách giải rất đẹp", "2/5")
        deriv = VGroup(
            mtx(r"A(x)=\frac{C(x)}x=\frac{500}{x}+20+0.05x", 37, GOLD),
            mtx(r"A'(x)=-\frac{500}{x^2}+0.05", 36, CYAN),
            mtx(r"A'(x)=0\iff x^2=10000", 36, INK),
            mtx(r"\boxed{x=100}", 42, GREEN),
            mtx(r"\boxed{A_{\min}=30}", 42, GOLD),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.38).shift(UP*0.25)

        ax, labels = self.make_axes((10,210,20), (25,75,10), xlen=6.5, ylen=5.0, shift=LEFT*3.0)
        curve = ax.plot(lambda x: 500/x+20+0.05*x, x_range=[10,210], color=BLUE, stroke_width=4)
        t = ValueTracker(25)
        M = always_redraw(lambda: Dot(ax.c2p(t.get_value(),500/t.get_value()+20+0.05*t.get_value()),radius=0.075,color=GOLD))
        q = Dot(ax.c2p(100,30), radius=0.09, color=RED)
        qlab = mtx(r"(100,30)", 26, RED).next_to(q, UP, buff=0.08)
        self.play(Create(ax), FadeIn(labels), Create(curve), FadeIn(deriv), FadeIn(M), FadeIn(q), FadeIn(qlab), run_time=1.1)
        self.narrate_play(
            "Khi sản lượng còn ít, phần chi phí cố định năm trăm bị chia cho quá ít sản phẩm nên chi phí trung bình cao. Khi sản lượng quá lớn, thành phần không phẩy không năm x lại kéo chi phí tăng lên. Vì vậy đồ thị có một đáy rất rõ.",
            t.animate.set_value(190), min_time=4.3,
        )
        self.narrate_play(
            "Đạo hàm cho x bằng một trăm. Tại đó chi phí trung bình bằng ba mươi nghìn đồng mỗi sản phẩm.",
            t.animate.set_value(100), min_time=3.5,
        )
        gem = VGroup(
            txt("Cách nhìn đẹp hơn:", 25, MUTED),
            mtx(r"\frac{500}{x}=0.05x=5", 36, CYAN),
            mtx(r"\frac{500}{x}+0.05x\ge2\sqrt{25}=10", 34, GOLD),
        ).arrange(DOWN,buff=0.20).to_edge(DOWN,buff=0.55).shift(RIGHT*2.15)
        self.play(FadeIn(gem), run_time=0.6)
        self.narrate(
            "Điểm đẹp của bài là tại mức tối ưu, hai phần biến thiên năm trăm trên x và không phẩy không năm x bằng nhau, cùng bằng năm. Có thể dùng bất đẳng thức AM GM để ra ngay kết quả mà không cần đạo hàm. Đây là kiểu lời giải ngắn rất đáng nhớ.",
            1.8,
        )

    # ======================================================
    # MODEL 3: HOTEL - DISCRETE DECISION
    # ======================================================
    def model3_hotel(self):
        self.show_problem(
            "Mô hình 3 – Giá phòng và quyết định nguyên",
            [
                "Một khách sạn có 100 phòng.",
                "Giá 500 nghìn đồng/phòng thì thuê hết.",
                "Mỗi lần tăng 20 nghìn đồng thì dự kiến giảm 2 phòng thuê.",
                "Chọn mức tăng nguyên để doanh thu lớn nhất.",
            ],
            "Bài thứ ba thêm một chi tiết rất thực tế: số lần tăng giá phải là số nguyên. Ta sẽ tối ưu trên mô hình liên tục trước, sau đó quay lại kiểm tra hai giá trị nguyên gần nhất. Đây là bước nhiều học sinh thường quên.",
            "3/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 3", "Liên tục trước – rời rạc sau", "3/5")
        formulas = VGroup(
            mtx(r"p(x)=500+20x", 35, BLUE),
            mtx(r"n(x)=100-2x", 35, CYAN),
            mtx(r"R(x)=(500+20x)(100-2x)", 36, GOLD),
            mtx(r"R(x)=50000+1000x-40x^2", 35, INK),
            mtx(r"x_*=\frac{-1000}{2(-40)}=12.5", 36, GREEN),
        ).arrange(DOWN,buff=0.24).to_edge(RIGHT,buff=0.35).shift(UP*0.45)

        ax, labels = self.make_axes((0,30,5), (45000,57000,2000), xlen=6.5, ylen=5.0, shift=LEFT*3.0)
        curve = ax.plot(lambda x: 50000+1000*x-40*x*x, x_range=[0,25], color=BLUE, stroke_width=4)
        x = ValueTracker(0)
        M = always_redraw(lambda: Dot(ax.c2p(x.get_value(),50000+1000*x.get_value()-40*x.get_value()**2),radius=0.075,color=GOLD))
        p12=Dot(ax.c2p(12,56240),radius=0.08,color=GREEN)
        p13=Dot(ax.c2p(13,56240),radius=0.08,color=GREEN)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(formulas),FadeIn(M),run_time=1.0)
        self.narrate_play(
            "Nếu tạm cho x là số thực, doanh thu là một parabol úp và đạt đỉnh tại x bằng mười hai phẩy năm. Nhưng trong bài thực tế, x là số lần tăng hai mươi nghìn đồng, nên x phải nguyên.",
            x.animate.set_value(12.5), min_time=4.1,
        )
        self.play(FadeIn(p12),FadeIn(p13),run_time=0.5)
        compare = VGroup(
            mtx(r"R(12)=740\cdot76=56240", 33, CYAN),
            mtx(r"R(13)=760\cdot74=56240", 33, CYAN),
            mtx(r"\boxed{x\in\{12,13\}}", 37, GOLD),
        ).arrange(DOWN,buff=0.22).to_edge(RIGHT,buff=0.38).shift(DOWN*1.55)
        self.play(FadeIn(compare),run_time=0.7)
        self.narrate(
            "Ta kiểm tra hai số nguyên gần mười hai phẩy năm là mười hai và mười ba. Thật thú vị, cả hai cho cùng doanh thu năm mươi sáu triệu hai trăm bốn mươi nghìn đồng. Vậy khách sạn có hai phương án tối ưu: giá bảy trăm bốn mươi nghìn với bảy mươi sáu phòng, hoặc bảy trăm sáu mươi nghìn với bảy mươi bốn phòng.",
            2.1,
        )

    # ======================================================
    # MODEL 4: CAPACITY PIECEWISE
    # ======================================================
    def model4_capacity(self):
        self.show_problem(
            "Mô hình 4 – Sức chứa tạo hàm nhiều công thức",
            [
                "Một sự kiện có tối đa 180 chỗ.",
                mtx(r"d(p)=300-2p", 38, GOLD),
                "p là giá vé, đơn vị nghìn đồng; d(p) là nhu cầu dự kiến.",
                "Tìm giá vé làm doanh thu lớn nhất.",
            ],
            "Bài thứ tư rất sát tinh thần mô hình hóa: nhu cầu có thể lớn hơn sức chứa, nhưng số vé bán thực tế không thể vượt quá một trăm tám mươi. Vì vậy nếu chỉ viết doanh thu bằng p nhân d của p cho mọi p thì mô hình sẽ sai. Ta bắt buộc phải tạo hàm nhiều công thức.",
            "4/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 4", "Điểm gãy đến từ giới hạn thực tế", "4/5")
        model = VGroup(
            mtx(r"q(p)=\min\{180,\ 300-2p\}", 37, CYAN),
            mtx(r"300-2p=180\iff p=60", 35, INK),
            mtx(r"R(p)=\begin{cases}180p,&0\le p\le60,\\p(300-2p),&60<p\le150.\end{cases}", 38, GOLD),
        ).arrange(DOWN,buff=0.30).to_edge(RIGHT,buff=0.35).shift(UP*0.5)

        ax, labels = self.make_axes((0,155,25), (0,12000,2000), xlen=6.5, ylen=5.0, shift=LEFT*3.0)
        seg1=ax.plot(lambda p:180*p,x_range=[0,60],color=CYAN,stroke_width=4)
        seg2=ax.plot(lambda p:300*p-2*p*p,x_range=[60,150],color=BLUE,stroke_width=4)
        t=ValueTracker(20)
        def rev(p):
            return 180*p if p<=60 else 300*p-2*p*p
        M=always_redraw(lambda:Dot(ax.c2p(t.get_value(),rev(t.get_value())),radius=0.075,color=GOLD))
        kink=Dot(ax.c2p(60,10800),radius=0.085,color=ORANGE)
        opt=Dot(ax.c2p(75,11250),radius=0.09,color=RED)
        self.play(Create(ax),FadeIn(labels),Create(seg1),Create(seg2),FadeIn(model),FadeIn(M),FadeIn(kink),FadeIn(opt),run_time=1.1)
        self.narrate_play(
            "Khi giá vé chưa vượt sáu mươi nghìn, nhu cầu lớn hơn sức chứa nên bán được đủ một trăm tám mươi vé. Doanh thu tăng theo đường thẳng. Tại p bằng sáu mươi xuất hiện một điểm gãy của mô hình.",
            t.animate.set_value(60),min_time=4.2,
        )
        self.narrate_play(
            "Sau ngưỡng đó, số người mua thật sự bằng ba trăm trừ hai p. Doanh thu chuyển thành parabol. Đỉnh của nhánh này ở p bằng bảy mươi lăm nghìn đồng, bán được một trăm năm mươi vé và thu mười một triệu hai trăm năm mươi nghìn đồng.",
            t.animate.set_value(75),min_time=4.7,
        )
        ans=VGroup(mtx(r"p_*=75",36,GOLD),mtx(r"q_*=150",36,GREEN),mtx(r"R_{\max}=11250",36,CYAN)).arrange(DOWN,buff=0.18).to_edge(RIGHT,buff=0.55).shift(DOWN*1.65)
        self.play(FadeIn(ans),run_time=0.6)
        self.narrate("Điểm mấu chốt của bài không phải đạo hàm khó, mà là nhận ra sức chứa tạo ra hai chế độ hoạt động khác nhau. Đây là một dạng rất đáng luyện.",1.5)

    # ======================================================
    # MODEL 5: SPEED COST - EQUALITY AT OPTIMUM
    # ======================================================
    def model5_speed(self):
        self.show_problem(
            "Mô hình 5 – Tốc độ tối ưu của một chuyến đi",
            [
                mtx(r"K(v)=\frac{800}{v}+0.125v,\qquad 40\le v\le100", 39, GOLD),
                "K(v) là chỉ số chi phí tổng hợp của thời gian và nhiên liệu.",
                "Tìm tốc độ làm K(v) nhỏ nhất.",
            ],
            "Mô hình cuối có hai lực kéo ngược nhau. Đi quá chậm làm chi phí thời gian tám trăm trên v rất lớn. Đi quá nhanh làm thành phần nhiên liệu không phẩy một hai năm v tăng. Điểm tối ưu nằm ở nơi hai xu hướng cân bằng.",
            "5/5",
        )

        self.clear_stage(); self.add_header_footer("Mô hình 5", "Hai xu hướng đối nghịch cân bằng tại tối ưu", "5/5")
        ax, labels = self.make_axes((40,105,10), (15,35,5), xlen=6.5, ylen=5.0, shift=LEFT*3.0)
        curve=ax.plot(lambda v:800/v+0.125*v,x_range=[40,100],color=BLUE,stroke_width=4)
        v=ValueTracker(40)
        M=always_redraw(lambda:Dot(ax.c2p(v.get_value(),800/v.get_value()+0.125*v.get_value()),radius=0.075,color=GOLD))
        opt=Dot(ax.c2p(80,20),radius=0.09,color=RED)
        formulas=VGroup(
            mtx(r"K'(v)=-\frac{800}{v^2}+0.125",35,CYAN),
            mtx(r"K'(v)=0\iff v^2=6400",35,INK),
            mtx(r"\boxed{v=80}",42,GREEN),
            mtx(r"K_{\min}=10+10=20",37,GOLD),
        ).arrange(DOWN,buff=0.28).to_edge(RIGHT,buff=0.45).shift(UP*0.4)
        self.play(Create(ax),FadeIn(labels),Create(curve),FadeIn(M),FadeIn(opt),FadeIn(formulas),run_time=1.0)
        self.narrate_play(
            "Cho tốc độ tăng từ bốn mươi lên một trăm. Chi phí giảm trước rồi tăng sau. Điểm thấp nhất nằm đúng ở tám mươi.",
            v.animate.set_value(100),min_time=4.0,
        )
        self.narrate_play(
            "Đạo hàm bằng không cho v bình phương bằng sáu nghìn bốn trăm, nên v bằng tám mươi ki lô mét trên giờ. Và một nét đẹp nữa xuất hiện: tại tốc độ tối ưu, hai thành phần tám trăm trên v và không phẩy một hai năm v đều bằng mười.",
            v.animate.set_value(80),min_time=4.4,
        )
        gem=mtx(r"\boxed{\frac{800}{v}=0.125v=10}",38,GOLD).to_edge(DOWN,buff=0.62).shift(RIGHT*2.0)
        self.play(Write(gem),run_time=0.6)

    # ======================================================
    # SUMMARY + ROADMAP
    # ======================================================
    def summary(self):
        self.clear_stage(); self.add_header_footer("Bản đồ tư duy", "Một bài thực tế tốt thường có điểm gãy hoặc điều kiện rời rạc", "Tổng kết")
        items=VGroup(
            bullet("Lợi nhuận: lập doanh thu trước, rồi trừ chi phí.", INK, 26, BLUE),
            bullet("Chi phí trung bình: nhớ chia tổng chi phí cho sản lượng.", INK, 26, CYAN),
            bullet("Biến nguyên: tối ưu liên tục xong phải kiểm tra các số nguyên gần nhất.", INK, 26, GREEN),
            bullet("Sức chứa, thuế, phí, chiết khấu: thường sinh hàm nhiều công thức.", INK, 26, ORANGE),
            bullet("Tốc độ và thời gian: hay xuất hiện cặp dạng a/x + bx.", INK, 26, GOLD),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.34).shift(DOWN*0.1)
        for i in items:self.play(FadeIn(i,shift=RIGHT*0.12),run_time=0.33)
        self.narrate(
            "Năm mô hình hôm nay đại diện cho năm kiểu tư duy rất hay gặp trong bài thực tế: lợi nhuận, chi phí trung bình, quyết định nguyên, giới hạn sức chứa và cân bằng giữa hai loại chi phí. Các em nên học cách nhận dạng mô hình, thay vì học thuộc từng bài riêng lẻ.",
            1.8,
        )

        self.clear_stage(); self.add_header_footer("Kế hoạch series dài hạn", "Ưu tiên bài thực tế – hạn chế hàm ẩn", "Tổng kết")
        roadmap=VGroup(
            VGroup(mtx(r"01",30,GOLD),txt("Mô hình hóa và tối ưu một biến",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"02",30,CYAN),txt("Hàm nhiều công thức: giá – phí – ngưỡng – sức chứa",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"03",30,BLUE),txt("Tốc độ – thời gian – năng suất – chi phí",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"04",30,GREEN),txt("Đọc đồ thị thực tế và câu Đúng/Sai",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"05",30,ORANGE),txt("Tích phân trong quãng đường, thể tích, lượng tích lũy",25,INK)).arrange(RIGHT,buff=0.18),
            VGroup(mtx(r"06",30,PURPLE),txt("Oxyz, xác suất – thống kê và video tổng hợp",25,INK)).arrange(RIGHT,buff=0.18),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.27)
        fit_width(roadmap,11.6)
        self.play(LaggedStart(*[FadeIn(r,shift=RIGHT*0.1) for r in roadmap],lag_ratio=0.12),run_time=1.5)
        self.narrate(
            "Từ đây series sẽ đi theo một lộ trình dài hạn. Ưu tiên các bài có dữ liệu thực tế, hàm tường minh, hàm nhiều công thức, đồ thị và quyết định tối ưu. Sau đó mới nối sang tích phân, không gian Oxyz, xác suất và thống kê. Các dạng hàm ẩn sẽ chỉ xuất hiện khi thật sự cần thiết, chứ không còn là trọng tâm.",
            2.0,
        )

        self.clear_stage()
        g=VGroup(
            txt("MÔ HÌNH ĐÚNG → HÀM ĐÚNG → KẾT LUẬN ĐÚNG",39,GOLD,BOLD),
            VGroup(txt("Miền thực tế", 27, CYAN, BOLD), txt("quan trọng như", 27, INK), mtx(r"f'(x)", 35, GOLD)).arrange(RIGHT, buff=0.18),
            txt(TEN_THAY,22,MUTED),
        ).arrange(DOWN,buff=0.42)
        self.play(FadeIn(g[0]),Write(g[1]),FadeIn(g[2]),run_time=1.0)
        self.narrate(
            "Điểm thầy muốn các em nhớ nhất là: trong toán thực tế, miền của biến quan trọng không kém đạo hàm. Một nghiệm cực trị chỉ có ý nghĩa khi nó phù hợp với dữ kiện và đơn vị của bài toán. Hẹn gặp các em ở phần hai: hàm nhiều công thức với giá, phí, ngưỡng và sức chứa.",
            1.8,
        )

    def construct(self):
        self.intro()
        self.model1_profit()
        self.model2_average_cost()
        self.model3_hotel()
        self.model4_capacity()
        self.model5_speed()
        self.summary()

# ==========================================================
# RENDER + MASTER AUDIO EXPORT
# ==========================================================
def render_full():
    config.media_dir = str(MEDIA_DIR)
    config.output_file = "toan_thuc_te_ham_so_01_toi_uu_1080p"
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
    master_wav = ROOT / "master_narration_toan_thuc_te_ham_so_01.wav"
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
